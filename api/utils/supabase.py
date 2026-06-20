import asyncio
import os
import hashlib
import json
import logging
import httpx

logger = logging.getLogger("qalqan")

_WHITELIST: set[str] | None = None


def _trusted_domains() -> set[str]:
    """Whitelisted domains — used to scrub false-positives from dashboard stats."""
    global _WHITELIST
    if _WHITELIST is None:
        try:
            p = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "whitelist.json")
            with open(p, encoding="utf-8") as f:
                _WHITELIST = set(json.load(f).get("trusted_domains", []))
        except Exception:
            _WHITELIST = set()
    return _WHITELIST


def _is_trusted(dom: str, wl: set[str]) -> bool:
    return dom in wl or any(dom.endswith("." + td) for td in wl)

def _url() -> str:
    return os.getenv("SUPABASE_URL", "").rstrip("/")

def _key() -> str:
    return os.getenv("SUPABASE_SERVICE_KEY", "")

def _headers() -> dict:
    return {
        "apikey": _key(),
        "Authorization": f"Bearer {_key()}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

def _available() -> bool:
    return bool(_url() and _key())

def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]


async def log_report(domain: str, url: str, category: str, comment: str,
                     lang: str, reporter_ip: str) -> bool:
    if not _available():
        return False
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(
                f"{_url()}/rest/v1/reports",
                headers=_headers(),
                json={
                    "domain": domain,
                    "url_hash": _hash(url),
                    "category": category,
                    "comment": comment[:500] if comment else None,
                    "lang": lang,
                    "reporter_ip_hash": _hash(reporter_ip),
                }
            )
            return r.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"Supabase log_report failed: {e}")
        return False


async def log_appeal(domain: str, verdict_received: str, reason: str) -> bool:
    if not _available():
        return False
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(
                f"{_url()}/rest/v1/appeals",
                headers=_headers(),
                json={
                    "domain": domain,
                    "verdict_received": verdict_received,
                    "reason": reason[:500] if reason else None,
                }
            )
            return r.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"Supabase log_appeal failed: {e}")
        return False


# KZ oblast / city ISO 3166-2 subdivision codes → readable names (Vercel geo header)
KZ_REGIONS = {
    "10": "Абай", "11": "Ақмола", "15": "Ақтөбе", "19": "Алматы обл.",
    "23": "Атырау", "27": "БҚО", "31": "Жамбыл", "33": "Жетісу",
    "35": "Қарағанды", "39": "Қостанай", "43": "Қызылорда", "47": "Маңғыстау",
    "55": "Павлодар", "59": "СҚО", "61": "Түркістан", "62": "Ұлытау",
    "63": "ШҚО", "71": "Астана", "75": "Алматы қ.", "79": "Шымкент",
}


async def log_check(domain: str, verdict: str, score: int, top_source: str,
                    ai_used: bool, ai_skipped: bool, latency_ms: int,
                    country: str | None = None, region: str | None = None) -> None:
    if not _available():
        return
    base = {
        "domain": domain, "verdict": verdict, "score": score, "top_source": top_source,
        "ai_used": ai_used, "ai_skipped": ai_skipped, "latency_ms": latency_ms,
    }
    geo = {}
    if country:
        geo["country"] = country
    if region:
        geo["region"] = region
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.post(f"{_url()}/rest/v1/check_logs", headers=_headers(),
                                  json={**base, **geo})
            # country/region columns may not exist yet — retry without geo so logging never breaks
            if r.status_code >= 400 and geo:
                await client.post(f"{_url()}/rest/v1/check_logs", headers=_headers(), json=base)
    except Exception as e:
        logger.warning(f"Supabase log_check failed: {e}")


async def get_trends(days: int = 7) -> dict | None:
    """
    Returns trend data from check_logs + reports tables.
    Fetches last N rows and aggregates in Python (avoids GROUP BY dependency).
    Returns None if Supabase not available.
    """
    if not _available():
        return None
    try:
        async with httpx.AsyncClient(timeout=6) as client:
            logs_r, rep_r = await asyncio.gather(
                client.get(
                    f"{_url()}/rest/v1/check_logs"
                    "?select=domain,verdict,top_source,ai_used,ai_skipped,latency_ms"
                    "&order=created_at.desc&limit=1000",
                    headers=_headers(),
                ),
                client.get(
                    f"{_url()}/rest/v1/reports"
                    "?select=domain,category"
                    "&order=created_at.desc&limit=500",
                    headers=_headers(),
                ),
            )

        if logs_r.status_code != 200:
            return None

        logs = logs_r.json() if logs_r.status_code == 200 else []
        reps = rep_r.json() if rep_r.status_code == 200 else []

        # --- Aggregate check_logs ---
        domain_counts: dict[str, int] = {}
        verdict_dist: dict[str, int] = {}
        source_counts: dict[str, int] = {}
        ai_used = ai_skipped = 0
        latencies: list[int] = []

        for row in logs:
            d = row.get("domain", "")
            if d:
                domain_counts[d] = domain_counts.get(d, 0) + 1
            v = row.get("verdict", "")
            if v:
                verdict_dist[v] = verdict_dist.get(v, 0) + 1
            s = row.get("top_source", "")
            if s:
                source_counts[s] = source_counts.get(s, 0) + 1
            if row.get("ai_used"):
                ai_used += 1
            if row.get("ai_skipped"):
                ai_skipped += 1
            lat = row.get("latency_ms")
            if lat:
                latencies.append(int(lat))

        top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:8]

        # --- Aggregate reports ---
        rep_domain_counts: dict[str, int] = {}
        category_counts: dict[str, int] = {}
        for row in reps:
            if (row.get("category") or "").startswith("vote:"):
                continue  # community votes are not scam reports
            d = row.get("domain", "")
            if d:
                rep_domain_counts[d] = rep_domain_counts.get(d, 0) + 1
            c = row.get("category", "")
            if c:
                category_counts[c] = category_counts.get(c, 0) + 1

        top_reported = sorted(rep_domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_checks": len(logs),
            "top_domains_checked": [{"domain": d, "checks": c} for d, c in top_domains],
            "verdict_distribution": dict(sorted(verdict_dist.items(), key=lambda x: x[1], reverse=True)),
            "top_detection_sources": [{"source": s, "count": c} for s, c in top_sources],
            "ai_stats": {
                "ai_used": ai_used,
                "ai_skipped": ai_skipped,
                "heuristics_only": len(logs) - ai_used,
            },
            "avg_latency_ms": round(sum(latencies) / len(latencies)) if latencies else None,
            "total_reports": len(reps),
            "top_reported_domains": [{"domain": d, "reports": c, "auto_blocked": c >= 5} for d, c in top_reported],
            "report_categories": dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True)),
        }
    except Exception as e:
        logger.warning(f"Supabase get_trends failed: {e}")
        return None


# Community auto-block thresholds (crowd-sourced)
COMMUNITY_BLOCK_MIN_SIGNALS = 5   # reports + confirmations
COMMUNITY_BLOCK_MIN_IPS = 3       # distinct reporters


def community_auto_block(reports: int, confirms: int, disputes: int, unique_ips: int) -> bool:
    """Pure crowd-block decision (Sybil-resistant): enough signals from enough
    distinct reporters, and not contested (confirms must exceed disputes unless
    there are no disputes). Extracted for unit testing."""
    signals = reports + confirms
    return (signals >= COMMUNITY_BLOCK_MIN_SIGNALS
            and unique_ips >= COMMUNITY_BLOCK_MIN_IPS
            and (disputes == 0 or confirms > disputes))


async def get_community_stats(domain: str) -> dict:
    """Crowd intelligence for a domain: reports, confirm/dispute votes, auto-block status.
    Backed by the reports table (votes stored with category vote:confirm / vote:dispute)."""
    base = {"domain": domain, "reports": 0, "confirms": 0, "disputes": 0,
            "unique_voters": 0, "crowd_score": 0, "auto_blocked": False}
    if not _available() or not domain:
        return base
    try:
        async with httpx.AsyncClient(timeout=4) as client:
            r = await client.get(
                f"{_url()}/rest/v1/reports",
                headers=_headers(),
                params={"domain": f"eq.{domain}",
                        "select": "category,reporter_ip_hash", "limit": "2000"},
            )
        if r.status_code != 200:
            return base
        reports = confirms = disputes = 0
        ips: set[str] = set()
        for row in r.json():
            c = row.get("category") or ""
            iph = row.get("reporter_ip_hash")
            if iph:
                ips.add(iph)
            if c == "vote:confirm":
                confirms += 1
            elif c == "vote:dispute":
                disputes += 1
            else:
                reports += 1
        signals = reports + confirms
        auto = community_auto_block(reports, confirms, disputes, len(ips))
        return {"domain": domain, "reports": reports, "confirms": confirms, "disputes": disputes,
                "unique_voters": len(ips), "crowd_score": signals - disputes, "auto_blocked": auto}
    except Exception as e:
        logger.warning(f"get_community_stats failed: {e}")
        return base


async def record_vote(domain: str, vote: str, reporter_ip: str) -> dict:
    """Record a community confirm/dispute vote (one per IP per domain). Returns updated stats."""
    if not _available() or not domain:
        return {"ok": False, "reason": "storage_unavailable"}
    cat = "vote:confirm" if vote == "confirm" else "vote:dispute"
    ip_hash = _hash(reporter_ip)
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            chk = await client.get(
                f"{_url()}/rest/v1/reports", headers=_headers(),
                params={"domain": f"eq.{domain}", "reporter_ip_hash": f"eq.{ip_hash}",
                        "category": "in.(vote:confirm,vote:dispute)", "select": "id", "limit": "1"},
            )
            if chk.status_code == 200 and chk.json():
                stats = await get_community_stats(domain)
                return {"ok": False, "already_voted": True, "stats": stats}
            r = await client.post(
                f"{_url()}/rest/v1/reports", headers=_headers(),
                json={"domain": domain, "url_hash": _hash(domain), "category": cat,
                      "comment": None, "lang": "ru", "reporter_ip_hash": ip_hash},
            )
            ok = r.status_code in (200, 201)
        stats = await get_community_stats(domain)
        return {"ok": ok, "stats": stats}
    except Exception as e:
        logger.warning(f"record_vote failed: {e}")
        return {"ok": False, "reason": "error"}


async def get_dashboard_data(sample: int = 2000) -> dict | None:
    """Aggregated analytics for the regulator dashboard: daily time series,
    threat-type breakdown, verdict distribution, top malicious domains, KPIs.
    Returns None if Supabase unavailable (caller falls back to demo data)."""
    if not _available():
        return None
    try:
        base = f"{_url()}/rest/v1/check_logs?order=created_at.desc&limit={sample}"
        async with httpx.AsyncClient(timeout=8) as client:
            logs_r = await client.get(
                base + "&select=domain,verdict,score,top_source,created_at,region,country",
                headers=_headers())
            if logs_r.status_code != 200:
                # region/country columns may not exist yet — fall back to base columns
                logs_r = await client.get(
                    base + "&select=domain,verdict,score,top_source,created_at",
                    headers=_headers())
            rep_r = await client.get(
                f"{_url()}/rest/v1/reports"
                "?select=domain,category,created_at&order=created_at.desc&limit=1000",
                headers=_headers())
        if logs_r.status_code != 200:
            return None
        logs = logs_r.json()
        reps = rep_r.json() if rep_r.status_code == 200 else []

        # Map raw detection source → human threat category
        def _cat(src: str) -> str:
            s = (src or "").lower()
            if "pyramid" in s or "afm" in s:
                return "Финпирамиды"
            if "gambling" in s:
                return "Гемблинг"
            if "phishing" in s or "blacklist" in s:
                return "Фишинг"
            if "goszakup" in s:
                return "Госзакуп-фрод"
            if "ai" in s or "groq" in s or "gemini" in s:
                return "AI-вердикт"
            if "domain" in s or "url" in s:
                return "Подозр. инфраструктура"
            if "kz" in s:
                return "KZ-угрозы"
            if "whitelist" in s:
                return "Доверенные"
            return "Прочее"

        wl = _trusted_domains()
        daily: dict[str, dict] = {}
        verdict_dist: dict[str, int] = {}
        threat_types: dict[str, int] = {}
        tier_counts: dict[str, int] = {}
        danger_domains: dict[str, int] = {}
        regions: dict[str, dict] = {}
        scores: list[int] = []

        for row in logs:
            day = (row.get("created_at") or "")[:10]
            v = (row.get("verdict") or "").upper()
            src = row.get("top_source", "")
            dom = row.get("domain", "")
            # KZ regional aggregation (Vercel geo: country=KZ, region=ISO subdivision)
            if (row.get("country") or "").upper() == "KZ" and row.get("region"):
                rname = KZ_REGIONS.get(str(row["region"]))
                if rname:
                    rr = regions.setdefault(rname, {"total": 0, "threats": 0})
                    rr["total"] += 1
                    if v in ("DANGEROUS", "SUSPICIOUS"):
                        rr["threats"] += 1
            if day:
                d = daily.setdefault(day, {"total": 0, "threats": 0})
                d["total"] += 1
                if v in ("DANGEROUS", "SUSPICIOUS"):
                    d["threats"] += 1
            if v:
                verdict_dist[v] = verdict_dist.get(v, 0) + 1
            if src:
                tier_counts[src] = tier_counts.get(src, 0) + 1
            if v in ("DANGEROUS", "SUSPICIOUS") and src not in ("whitelist", "cache"):
                threat_types[_cat(src)] = threat_types.get(_cat(src), 0) + 1
            # Top-dangerous list: skip non-domains (no dot) and whitelisted domains
            # (stale/garbage rows must never present a trusted brand as "dangerous")
            if v == "DANGEROUS" and dom and "." in dom and not _is_trusted(dom, wl):
                danger_domains[dom] = danger_domains.get(dom, 0) + 1
            sc = row.get("score")
            if isinstance(sc, (int, float)):
                scores.append(int(sc))

        rep_cats: dict[str, int] = {}
        for row in reps:
            c = row.get("category", "")
            if c and not c.startswith("vote:"):
                rep_cats[c] = rep_cats.get(c, 0) + 1

        series = [{"date": d, **daily[d]} for d in sorted(daily.keys())][-30:]
        total = len(logs)
        dangerous = verdict_dist.get("DANGEROUS", 0)
        suspicious = verdict_dist.get("SUSPICIOUS", 0)
        return {
            "kpis": {
                "total_checks": total,
                "threats_blocked": dangerous,
                "suspicious": suspicious,
                "block_rate_pct": round(100 * dangerous / total, 1) if total else 0,
                "total_reports": len(reps),
                "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            },
            "time_series": series,
            "verdict_distribution": dict(sorted(verdict_dist.items(), key=lambda x: -x[1])),
            "threat_types": dict(sorted(threat_types.items(), key=lambda x: -x[1])),
            "tier_effectiveness": dict(sorted(tier_counts.items(), key=lambda x: -x[1])[:8]),
            "top_dangerous_domains": [
                {"domain": d, "count": c}
                for d, c in sorted(danger_domains.items(), key=lambda x: -x[1])[:12]
            ],
            "report_categories": dict(sorted(rep_cats.items(), key=lambda x: -x[1])),
            "regions": dict(sorted(regions.items(), key=lambda x: -x[1]["threats"])),
        }
    except Exception as e:
        logger.warning(f"get_dashboard_data failed: {e}")
        return None


async def get_federated_feed(limit: int = 500) -> list[dict] | None:
    """Threat indicators contributed by partners/CERTs (category 'federated:*').
    Aggregated by domain with contribution counts. None if Supabase unavailable."""
    if not _available():
        return None
    try:
        async with httpx.AsyncClient(timeout=6) as client:
            r = await client.get(
                f"{_url()}/rest/v1/reports"
                "?select=domain,category,created_at&category=ilike.federated*"
                f"&order=created_at.desc&limit={limit}",
                headers=_headers())
        if r.status_code != 200:
            return None
        agg: dict[str, dict] = {}
        for row in r.json():
            d = row.get("domain", "")
            if not d:
                continue
            a = agg.setdefault(d, {"domain": d, "contributions": 0, "types": set(),
                                   "last": row.get("created_at")})
            a["contributions"] += 1
            cat = row.get("category", "")
            if ":" in cat:
                a["types"].add(cat.split(":", 1)[1])
        return [{"domain": v["domain"], "contributions": v["contributions"],
                 "types": sorted(v["types"]), "last": v["last"]}
                for v in sorted(agg.values(), key=lambda x: -x["contributions"])]
    except Exception as e:
        logger.warning(f"get_federated_feed failed: {e}")
        return None


async def get_admin_data(limit: int = 100) -> dict | None:
    """Fetch recent reports, appeals, and check_logs for admin dashboard."""
    if not _available():
        return None
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            reports_r, appeals_r, logs_r = await asyncio.gather(
                client.get(
                    f"{_url()}/rest/v1/reports"
                    "?select=id,domain,category,comment,lang,created_at"
                    f"&order=created_at.desc&limit={limit}",
                    headers=_headers(),
                ),
                client.get(
                    f"{_url()}/rest/v1/appeals"
                    "?select=id,domain,verdict_received,reason,created_at"
                    f"&order=created_at.desc&limit={limit}",
                    headers=_headers(),
                ),
                client.get(
                    f"{_url()}/rest/v1/check_logs"
                    "?select=id,domain,verdict,score,top_source,ai_used,latency_ms,created_at"
                    f"&order=created_at.desc&limit={limit}",
                    headers=_headers(),
                ),
            )
        return {
            "reports": reports_r.json() if reports_r.status_code == 200 else [],
            "appeals": appeals_r.json() if appeals_r.status_code == 200 else [],
            "check_logs": logs_r.json() if logs_r.status_code == 200 else [],
        }
    except Exception as e:
        logger.warning(f"get_admin_data failed: {e}")
        return None


async def check_health() -> dict:
    if not _available():
        return {"status": "disabled", "reason": "env vars not set"}
    try:
        async with httpx.AsyncClient(timeout=4) as client:
            r = await client.get(
                f"{_url()}/rest/v1/check_logs?select=id&limit=1",
                headers=_headers(),
            )
            if r.status_code == 200:
                return {"status": "ok"}
            return {"status": "error", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:80]}
