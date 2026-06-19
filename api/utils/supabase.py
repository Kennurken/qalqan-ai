import asyncio
import os
import hashlib
import logging
import httpx

logger = logging.getLogger("qalqan")

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


async def log_check(domain: str, verdict: str, score: int, top_source: str,
                    ai_used: bool, ai_skipped: bool, latency_ms: int) -> None:
    if not _available():
        return
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            await client.post(
                f"{_url()}/rest/v1/check_logs",
                headers=_headers(),
                json={
                    "domain": domain,
                    "verdict": verdict,
                    "score": score,
                    "top_source": top_source,
                    "ai_used": ai_used,
                    "ai_skipped": ai_skipped,
                    "latency_ms": latency_ms,
                }
            )
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


async def get_dashboard_data(sample: int = 2000) -> dict | None:
    """Aggregated analytics for the regulator dashboard: daily time series,
    threat-type breakdown, verdict distribution, top malicious domains, KPIs.
    Returns None if Supabase unavailable (caller falls back to demo data)."""
    if not _available():
        return None
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            logs_r, rep_r = await asyncio.gather(
                client.get(
                    f"{_url()}/rest/v1/check_logs"
                    "?select=domain,verdict,score,top_source,created_at"
                    f"&order=created_at.desc&limit={sample}",
                    headers=_headers(),
                ),
                client.get(
                    f"{_url()}/rest/v1/reports"
                    "?select=domain,category,created_at"
                    "&order=created_at.desc&limit=1000",
                    headers=_headers(),
                ),
            )
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

        daily: dict[str, dict] = {}
        verdict_dist: dict[str, int] = {}
        threat_types: dict[str, int] = {}
        tier_counts: dict[str, int] = {}
        danger_domains: dict[str, int] = {}
        scores: list[int] = []

        for row in logs:
            day = (row.get("created_at") or "")[:10]
            v = (row.get("verdict") or "").upper()
            src = row.get("top_source", "")
            dom = row.get("domain", "")
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
            if v == "DANGEROUS" and dom:
                danger_domains[dom] = danger_domains.get(dom, 0) + 1
            sc = row.get("score")
            if isinstance(sc, (int, float)):
                scores.append(int(sc))

        rep_cats: dict[str, int] = {}
        for row in reps:
            c = row.get("category", "")
            if c:
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
        }
    except Exception as e:
        logger.warning(f"get_dashboard_data failed: {e}")
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
