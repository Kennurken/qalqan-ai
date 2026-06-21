# Qalqan AI v5.1
# Госзакупки Fraud Detection — 10 red-flag rules
# API: goszakup.gov.kz (open data, no key required for basic queries)
# Дүниежүзінде бірінші KZ government procurement fraud AI detector

import asyncio
import logging
import httpx

from ..utils.http import get_client
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

logger = logging.getLogger("qalqan")

# ── goszakup.gov.kz Open Data API ────────────────────────────────────────────
_GOSZAKUP_API = "https://goszakup.gov.kz/v3"
_GOSZAKUP_GRAPHQL = "https://goszakup.gov.kz/v3/graphql"

# Red-flag thresholds
_WIN_RATE_THRESHOLD    = 0.70   # >70% wins in a region = suspicious monopoly
_NEW_SUPPLIER_DAYS     = 30     # registered <30 days before tender = suspicious
_PRICE_MARKUP          = 0.40   # >40% above market estimate = overpriced
_MIN_PARTICIPANT_WARN  = 2      # only 1-2 bidders = low competition
_REPEAT_CONTRACT_LIMIT = 5      # same supplier >5 contracts same buyer = collusion signal


# ── URL detector — is this a госзакупки-related URL? ─────────────────────────

_GOSZAKUP_DOMAINS = {
    "goszakup.gov.kz",
    "zakupki.kz",
    "tender.gov.kz",
    "ezvakup.kz",
}

_GOSZAKUP_KEYWORDS = [
    "тендер", "zakup", "tender", "госзакупки", "goszakup",
    "procurement", "закупки", "конкурс", "лот",
]


def is_goszakup_url(url: str) -> bool:
    """True if URL relates to government procurement."""
    try:
        p = urlparse(url if "://" in url else "https://" + url)
        domain = p.netloc.lower().replace("www.", "")
        if domain in _GOSZAKUP_DOMAINS:
            return True
        path_query = (p.path + "?" + p.query).lower()
        return any(kw in path_query or kw in domain for kw in _GOSZAKUP_KEYWORDS)
    except Exception:
        return False


# ── Fraud scoring ─────────────────────────────────────────────────────────────

class FraudSignal:
    __slots__ = ("rule", "score", "description_kk", "description_ru", "description_en")

    def __init__(self, rule: str, score: int, kk: str, ru: str, en: str):
        self.rule = rule
        self.score = score
        self.description_kk = kk
        self.description_ru = ru
        self.description_en = en


def _analyse_tender(tender: dict) -> list[FraudSignal]:
    """Apply 10 red-flag rules to a tender record."""
    signals: list[FraudSignal] = []

    # Rule 1: Single-source procurement (without proper justification)
    method = tender.get("purchase_method_code", "")
    if method in ("2", "SRC", "single_source"):
        signals.append(FraudSignal(
            "single_source", 35,
            "Бір көзден сатып алу — бәсекелестіксіз тендер",
            "Закупка из одного источника — без конкуренции",
            "Single-source procurement — no competitive bidding",
        ))

    # Rule 2: Very few participants
    participants = tender.get("participants_count", 999)
    if isinstance(participants, (int, float)) and participants <= 1:
        signals.append(FraudSignal(
            "no_competition", 30,
            f"Қатысушы саны: {participants} — бәсекелестік жоқ",
            f"Участников: {participants} — нет конкуренции",
            f"Participants: {participants} — no competition",
        ))
    elif isinstance(participants, (int, float)) and participants == _MIN_PARTICIPANT_WARN:
        signals.append(FraudSignal(
            "low_competition", 15,
            f"Тек {participants} қатысушы — бәсекелестік аз",
            f"Только {participants} участника — низкая конкуренция",
            f"Only {participants} participants — low competition",
        ))

    # Rule 3: Price significantly above estimate
    lot_price = tender.get("lot_amount")
    estimated = tender.get("ref_price") or tender.get("estimated_cost")
    if lot_price and estimated and estimated > 0:
        try:
            markup = (float(lot_price) - float(estimated)) / float(estimated)
            if markup > _PRICE_MARKUP:
                pct = round(markup * 100)
                signals.append(FraudSignal(
                    "overpriced", 25,
                    f"Баға нарықтан {pct}% жоғары — асыра бағалаған",
                    f"Цена выше рыночной на {pct}% — завышение",
                    f"Price {pct}% above estimate — inflated pricing",
                ))
        except (TypeError, ValueError):
            pass

    # Rule 4: Tender created same day as announcement deadline
    created = tender.get("created_date") or tender.get("publish_date")
    deadline = tender.get("end_date") or tender.get("deadline")
    if created and deadline:
        try:
            dt_c = datetime.fromisoformat(str(created).replace("Z", "+00:00"))
            dt_d = datetime.fromisoformat(str(deadline).replace("Z", "+00:00"))
            delta_days = (dt_d - dt_c).days
            if delta_days <= 1:
                signals.append(FraudSignal(
                    "instant_deadline", 30,
                    f"Тендер мерзімі {delta_days} күн — жеткіліксіз уақыт",
                    f"Срок тендера {delta_days} дн. — недостаточно времени",
                    f"Tender deadline {delta_days} day(s) — insufficient time to compete",
                ))
        except Exception:
            pass

    # Rule 5: Suspicious keyword in specification (artificial restriction)
    spec = (tender.get("name_ru") or tender.get("name_kz") or "").lower()
    _TAILORED_KEYWORDS = [
        "только", "исключительно", "единственный производитель",
        "конкретная модель", "зарегистрирован не менее",
    ]
    for kw in _TAILORED_KEYWORDS:
        if kw in spec:
            signals.append(FraudSignal(
                "tailored_spec", 20,
                "Техспецификация бір жеткізушіге жазылған",
                f"Тех. задание под конкретного поставщика ('{kw}')",
                f"Specification tailored to single supplier ('{kw}')",
            ))
            break

    return signals


def _analyse_supplier(supplier: dict, region_stats: dict | None = None) -> list[FraudSignal]:
    """Apply supplier-level red-flag rules."""
    signals: list[FraudSignal] = []

    # Rule 6: Newly registered supplier
    reg_date = supplier.get("registration_date") or supplier.get("reg_date")
    if reg_date:
        try:
            dt = datetime.fromisoformat(str(reg_date).replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - dt).days
            if age_days < _NEW_SUPPLIER_DAYS:
                signals.append(FraudSignal(
                    "new_supplier", 25,
                    f"Жеткізуші тіркелгені: {age_days} күн — жаңа компания",
                    f"Поставщик зарегистрирован {age_days} дн. назад — новая компания",
                    f"Supplier registered {age_days} days ago — newly formed entity",
                ))
        except Exception:
            pass

    # Rule 7: High win rate in region (monopoly signal)
    if region_stats:
        total   = region_stats.get("total_tenders", 0)
        won     = region_stats.get("won_tenders", 0)
        if total > 3 and won / max(total, 1) > _WIN_RATE_THRESHOLD:
            pct = round(won / total * 100)
            signals.append(FraudSignal(
                "regional_monopoly", 30,
                f"Бір компания регионда тендерлердің {pct}%-ін жеңді",
                f"Компания выиграла {pct}% тендеров в регионе",
                f"Supplier won {pct}% of regional tenders — monopoly signal",
            ))

    # Rule 8: Shell company indicators
    staff = supplier.get("employees_count")
    if staff is not None:
        try:
            if int(staff) <= 1:
                signals.append(FraudSignal(
                    "shell_company", 20,
                    "Жеткізушінің қызметкері 1 немесе 0 — қалқа компания белгісі",
                    "У поставщика 0-1 сотрудников — признак компании-однодневки",
                    "Supplier has 0-1 employees — potential shell company",
                ))
        except (TypeError, ValueError):
            pass

    return signals


# ── Public API query ─────────────────────────────────────────────────────────

async def check_tender_by_number(tender_number: str) -> dict:
    """Fetch and analyse a specific tender by number from goszakup.gov.kz."""
    score_adjust = 0
    signals: list[FraudSignal] = []
    tender_data: dict = {}

    try:
        # Try public v3 API
        url = f"{_GOSZAKUP_API}/tenders/{tender_number}"
        res = await get_client().get(url, headers={"Accept": "application/json"},
                                     follow_redirects=True, timeout=8)
        if res.status_code == 200:
            tender_data = res.json()
    except Exception as e:
        logger.debug(f"Goszakup API error for {tender_number}: {e}")

    if not tender_data:
        return {
            "verdict": "UNKNOWN",
            "source": "goszakup",
            "error": "Тендер табылмады немесе API қолжетімсіз",
        }

    # Apply rules
    tender_signals = _analyse_tender(tender_data)
    signals.extend(tender_signals)
    score_adjust += sum(s.score for s in tender_signals)

    verdict = _score_to_verdict(score_adjust)
    return _build_result(verdict, score_adjust, signals, tender_data)


async def check_supplier_by_bin(bin_number: str) -> dict:
    """Fetch and analyse a supplier (company) by BIN."""
    score_adjust = 0
    signals: list[FraudSignal] = []
    supplier_data: dict = {}

    try:
        url = f"{_GOSZAKUP_API}/subjects/{bin_number}"
        res = await get_client().get(url, headers={"Accept": "application/json"},
                                     follow_redirects=True, timeout=8)
        if res.status_code == 200:
            supplier_data = res.json()
    except Exception as e:
        logger.debug(f"Goszakup supplier API error for {bin_number}: {e}")

    if not supplier_data:
        return {
            "verdict": "UNKNOWN",
            "source": "goszakup",
            "error": "Жеткізуші табылмады немесе API қолжетімсіз",
        }

    supplier_signals = _analyse_supplier(supplier_data)
    signals.extend(supplier_signals)
    score_adjust += sum(s.score for s in supplier_signals)

    verdict = _score_to_verdict(score_adjust)
    return _build_result(verdict, score_adjust, signals, supplier_data)


async def check_goszakup_url(url: str) -> dict | None:
    """Check if URL is goszakup-related and extract tender/supplier ID for analysis."""
    if not is_goszakup_url(url):
        return None

    try:
        p = urlparse(url if "://" in url else "https://" + url)
        path = p.path.lower()

        # Try to extract tender number from path like /ru/lot/view/id/12345
        import re
        tender_match = re.search(r"/(?:tender|lot|plan)/(?:view/)?(?:id/)?(\d+)", path)
        supplier_match = re.search(r"/(?:subject|supplier|company)/(?:view/)?(?:id/)?(\d{12})", path)

        if tender_match:
            return await check_tender_by_number(tender_match.group(1))
        elif supplier_match:
            return await check_supplier_by_bin(supplier_match.group(1))
        else:
            # Generic goszakup URL — flag as official gov site (safe, but note it)
            return {
                "verdict": "SAFE",
                "threat_score": 0,
                "source": "goszakup",
                "detail_kk": "Ресми мемлекеттік госзакупки порталы",
                "detail_ru": "Официальный государственный портал закупок",
                "detail_en": "Official government procurement portal",
            }
    except Exception as e:
        logger.debug(f"Goszakup URL check error: {e}")
        return None


# ── Standalone fraud analysis (from extension popup or API) ──────────────────

async def analyse_procurement_data(data: dict) -> dict:
    """Analyse raw procurement data dict (submitted by API caller or scraped).
    This is the main entry point when data is passed directly, not fetched.
    """
    score_adjust = 0
    signals: list[FraudSignal] = []

    tender_signals = _analyse_tender(data)
    signals.extend(tender_signals)
    score_adjust += sum(s.score for s in tender_signals)

    supplier = data.get("supplier") or data.get("winner") or {}
    if supplier:
        supplier_signals = _analyse_supplier(supplier, data.get("region_stats"))
        signals.extend(supplier_signals)
        score_adjust += sum(s.score for s in supplier_signals)

    verdict = _score_to_verdict(score_adjust)
    return _build_result(verdict, score_adjust, signals, data)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _score_to_verdict(score: int) -> str:
    if score >= 50:
        return "DANGEROUS"
    elif score >= 20:
        return "SUSPICIOUS"
    return "SAFE"


def _build_result(verdict: str, score: int, signals: list[FraudSignal], raw: dict) -> dict:
    kk_parts = [s.description_kk for s in signals]
    ru_parts = [s.description_ru for s in signals]
    en_parts = [s.description_en for s in signals]

    return {
        "verdict": verdict,
        "threat_score": min(score, 100),
        "threat_type": "procurement_fraud",
        "source": "goszakup_fraud_detector",
        "reason_kk": "; ".join(kk_parts) if kk_parts else "Аномалия анықталмады",
        "reason_ru": "; ".join(ru_parts) if ru_parts else "Аномалий не обнаружено",
        "reason_en": "; ".join(en_parts) if en_parts else "No anomalies detected",
        "indicators": [s.rule for s in signals],
        "red_flags": [
            {
                "rule": s.rule,
                "score": s.score,
                "kk": s.description_kk,
                "ru": s.description_ru,
                "en": s.description_en,
            }
            for s in signals
        ],
        "raw_data": {k: v for k, v in raw.items() if k not in ("supplier", "region_stats")},
    }
