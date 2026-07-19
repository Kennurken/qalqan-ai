# Qalqan AI — dynamic HTML page renderers (/stats, /admin).
# Static page shells live in templates.py; these two are built from live data.
# Every DB-derived value goes through html.escape (stored-XSS defense) — keep it
# that way when adding columns.

import html


def _e(v) -> str:
    """HTML-escape any DB-derived value before interpolating into a page."""
    return html.escape(str(v)) if v is not None else ""


# ── /stats ────────────────────────────────────────────────────────────────────

def render_stats_page(trends: dict, whitelist_size: int) -> str:
    total = trends.get("total_checks", 0)
    dist = trends.get("verdict_distribution", {})
    dangerous = dist.get("DANGEROUS", 0)
    suspicious = dist.get("SUSPICIOUS", 0)
    safe_cnt = dist.get("SAFE", 0)
    top_domains = trends.get("top_domains_checked", [])[:5]
    top_reported = trends.get("top_reported_domains", [])[:5]

    top_dom_html = "".join(
        f'<div class="row-item"><span class="ri-name">{_e(d["domain"])}</span><span class="ri-count">{_e(d["checks"])}</span></div>'
        for d in top_domains
    ) or '<div class="row-item muted">Нет данных</div>'
    top_rep_html = "".join(
        f'<div class="row-item"><span class="ri-name">{_e(d["domain"])}</span><span class="ri-count ri-danger">{_e(d["reports"])}</span></div>'
        for d in top_reported
    ) or '<div class="row-item muted">Нет данных</div>'

    danger_pct = round(dangerous / total * 100) if total else 0
    susp_pct = round(suspicious / total * 100) if total else 0
    safe_pct = round(safe_cnt / total * 100) if total else 0

    return f"""<!DOCTYPE html>
<html lang="kk"><head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Статистика</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0e1a;color:#e2e8f0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;padding:0}}
.navbar{{background:rgba(10,14,26,.95);border-bottom:1px solid #1e2d4a;padding:16px 24px;display:flex;align-items:center;justify-content:space-between}}
.logo{{color:#00d4ff;font-weight:700;font-size:18px;text-decoration:none}}
.nav-back{{color:#64748b;font-size:14px;text-decoration:none}}
.nav-back:hover{{color:#00d4ff}}
.page{{max-width:1000px;margin:0 auto;padding:40px 24px}}
h1{{font-size:28px;font-weight:700;margin-bottom:6px}}
.subtitle{{color:#64748b;font-size:14px;margin-bottom:40px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:40px}}
.card{{background:#131d35;border:1px solid #1e2d4a;border-radius:14px;padding:24px}}
.card-num{{font-size:36px;font-weight:800;color:#00d4ff;font-variant-numeric:tabular-nums}}
.card-num.danger{{color:#ef4444}}
.card-num.warn{{color:#f59e0b}}
.card-num.safe{{color:#22c55e}}
.card-label{{font-size:12px;color:#64748b;margin-top:4px;text-transform:uppercase;letter-spacing:.5px}}
.section{{margin-bottom:32px}}
.section-title{{font-size:16px;font-weight:600;margin-bottom:16px;color:#94a3b8}}
.row-item{{display:flex;justify-content:space-between;align-items:center;padding:10px 16px;background:#0f1629;border-radius:8px;margin-bottom:6px;font-size:13px}}
.ri-name{{color:#e2e8f0;font-family:monospace}}
.ri-count{{color:#00d4ff;font-weight:600}}
.ri-danger{{color:#ef4444}}
.muted{{color:#64748b}}
.bar-wrap{{background:#0f1629;border-radius:8px;height:28px;margin-bottom:10px;overflow:hidden;position:relative}}
.bar-fill{{height:100%;display:flex;align-items:center;padding-left:10px;font-size:12px;font-weight:600;color:#0a0e1a;transition:width .5s ease}}
.bar-label{{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:12px;color:#64748b}}
.report-btn{{display:inline-flex;align-items:center;gap:8px;background:#00d4ff;color:#0a0e1a;padding:12px 24px;border-radius:10px;font-weight:700;font-size:14px;text-decoration:none;margin-top:24px}}
.report-btn:hover{{opacity:.85}}
footer{{text-align:center;padding:32px;color:#334155;font-size:12px;border-top:1px solid #1e2d4a;margin-top:40px}}
:focus-visible{{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}}::selection{{background:rgba(122,162,247,.32)}}
</style></head><body>
<div class="navbar">
  <a class="logo" href="/"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:1em;height:1em;vertical-align:-0.14em"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg> Qalqan AI</a>
  <a class="nav-back" href="/">← Басты бет</a>
</div>
<div class="page">
  <h1>Статистика</h1>
  <p class="subtitle">Нақты уақыт деректері · Real-time from Supabase</p>

  <div class="grid">
    <div class="card"><div class="card-num">{total}</div><div class="card-label">Барлығы тексерілді</div></div>
    <div class="card"><div class="card-num danger">{dangerous}</div><div class="card-label">Қауіпті анықталды</div></div>
    <div class="card"><div class="card-num warn">{suspicious}</div><div class="card-label">Күдікті</div></div>
    <div class="card"><div class="card-num safe">{safe_cnt}</div><div class="card-label">Қауіпсіз</div></div>
    <div class="card"><div class="card-num">{danger_pct}%</div><div class="card-label">Қауіп үлесі</div></div>
    <div class="card"><div class="card-num">{whitelist_size}</div><div class="card-label">Ақ тізім</div></div>
  </div>

  <div class="section">
    <div class="section-title">Вердикт бойынша бөлініс</div>
    <div class="bar-wrap"><div class="bar-fill" style="width:{danger_pct}%;background:#ef4444">{danger_pct}% ОПАСНО</div><div class="bar-label">{dangerous} сайт</div></div>
    <div class="bar-wrap"><div class="bar-fill" style="width:{susp_pct}%;background:#f59e0b">{susp_pct}% ПОДОЗРИТЕЛЬНО</div><div class="bar-label">{suspicious} сайт</div></div>
    <div class="bar-wrap"><div class="bar-fill" style="width:{safe_pct}%;background:#22c55e">{safe_pct}% БЕЗОПАСНО</div><div class="bar-label">{safe_cnt} сайт</div></div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
    <div class="section">
      <div class="section-title">Жиі тексерілген домендер</div>
      {top_dom_html}
    </div>
    <div class="section">
      <div class="section-title">Жиі хабарланған домендер</div>
      {top_rep_html}
    </div>
  </div>

  <a class="report-btn" href="/report/generate">PDF есеп жүктеу</a>
</div>
<footer>Qalqan AI v5.1.0 · Деректер: Supabase PostgreSQL · © 2026 Барахат Мұхтар · Қыдырбек Елдос</footer>
</body></html>"""


# ── /admin ────────────────────────────────────────────────────────────────────

def _row_color(verdict: str) -> str:
    return {"DANGEROUS": "#ef4444", "SUSPICIOUS": "#f59e0b", "SAFE": "#10b981"}.get(verdict, "#94a3b8")


def _fmt_time(ts) -> str:
    return (ts or "")[:19].replace("T", " ")


def _rows_logs(logs: list[dict]) -> str:
    rows = ""
    for r in logs[:50]:
        c = _row_color(r.get("verdict", ""))
        rows += (
            f"<tr>"
            f"<td>{_e(_fmt_time(r.get('created_at')))}</td>"
            f"<td style='max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{_e(r.get('domain',''))}</td>"
            f"<td><span style='color:{c};font-weight:bold'>{_e(r.get('verdict',''))}</span></td>"
            f"<td>{_e(r.get('score',''))}</td>"
            f"<td>{_e(r.get('top_source',''))}</td>"
            f"<td>{'AI' if r.get('ai_used') else '—'}</td>"
            f"<td>{_e(r.get('latency_ms',''))}</td>"
            f"</tr>"
        )
    return rows


def _rows_reports(reports: list[dict]) -> str:
    rows = ""
    for r in reports[:50]:
        rows += (
            f"<tr>"
            f"<td>{_e(_fmt_time(r.get('created_at')))}</td>"
            f"<td style='max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{_e(r.get('domain',''))}</td>"
            f"<td><span style='background:#7c3aed;padding:2px 6px;border-radius:4px;font-size:11px'>{_e(r.get('category',''))}</span></td>"
            f"<td>{_e(r.get('lang',''))}</td>"
            f"<td style='max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{_e(r.get('comment','')) or '—'}</td>"
            f"</tr>"
        )
    return rows


def _rows_appeals(appeals: list[dict]) -> str:
    rows = ""
    for r in appeals[:50]:
        rows += (
            f"<tr>"
            f"<td>{_e(_fmt_time(r.get('created_at')))}</td>"
            f"<td style='max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{_e(r.get('domain',''))}</td>"
            f"<td><span style='color:#ef4444'>{_e(r.get('verdict_received',''))}</span></td>"
            f"<td style='max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{_e(r.get('reason','')) or '—'}</td>"
            f"</tr>"
        )
    return rows


def render_admin_page(data: dict) -> str:
    reports = data["reports"]
    appeals = data["appeals"]
    logs = data["check_logs"]

    total_checks = len(logs)
    total_reports = len(reports)
    total_appeals = len(appeals)
    dangerous = sum(1 for r in logs if r.get("verdict") == "DANGEROUS")
    pct_dangerous = round(dangerous / total_checks * 100) if total_checks else 0

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Admin</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#0a0f1e;color:#e2e8f0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh}}
  .topbar{{background:linear-gradient(135deg,#1e3a5f,#1e1b4b);padding:16px 32px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #334155}}
  .topbar h1{{font-size:20px;font-weight:700;background:linear-gradient(135deg,#3b82f6,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
  .topbar span{{font-size:12px;color:#64748b;margin-left:auto}}
  .stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:24px 32px}}
  .stat-card{{background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:20px;text-align:center}}
  .stat-card .num{{font-size:36px;font-weight:800;margin-bottom:4px}}
  .stat-card .label{{font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:.5px}}
  .tabs{{display:flex;gap:0;padding:0 32px;border-bottom:1px solid #1e293b}}
  .tab{{padding:12px 20px;font-size:13px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:#64748b;transition:all .2s;background:none;border-left:none;border-right:none;border-top:none}}
  .tab.active{{color:#3b82f6;border-bottom-color:#3b82f6}}
  .tab:hover{{color:#93c5fd}}
  .panel{{display:none;padding:24px 32px}}
  .panel.active{{display:block}}
  .table-wrap{{overflow-x:auto;border-radius:8px;border:1px solid #1e293b}}
  table{{width:100%;border-collapse:collapse;font-size:13px}}
  th{{background:#0f172a;padding:10px 12px;text-align:left;font-weight:600;color:#64748b;font-size:11px;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #1e293b}}
  td{{padding:10px 12px;border-bottom:1px solid #0f172a;vertical-align:top}}
  tr:hover td{{background:rgba(59,130,246,.06)}}
  tr:last-child td{{border-bottom:none}}
  .badge{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}}
  .refresh-btn{{float:right;background:#1e40af;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:13px}}
  .refresh-btn:hover{{background:#2563eb}}
  .section-title{{font-size:15px;font-weight:700;margin-bottom:16px;color:#94a3b8;display:flex;align-items:center;gap:8px}}
  .count{{font-size:12px;background:#1e293b;padding:2px 8px;border-radius:20px;color:#64748b}}
  @media(max-width:768px){{.stats{{grid-template-columns:repeat(2,1fr)}}.topbar{{padding:12px 16px}}.panel,.tabs{{padding-left:16px;padding-right:16px}}}}
:focus-visible{{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}}::selection{{background:rgba(122,162,247,.32)}}
</style>
</head>
<body>
<div class="topbar">
  <div style="font-size:24px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:1em;height:1em;vertical-align:-0.14em"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg></div>
  <h1>Qalqan AI — Admin Dashboard</h1>
  <span id="clock"></span>
</div>

<div class="stats">
  <div class="stat-card">
    <div class="num" style="color:#3b82f6">{total_checks}</div>
    <div class="label">Тексерулер / Checks</div>
  </div>
  <div class="stat-card">
    <div class="num" style="color:#ef4444">{pct_dangerous}%</div>
    <div class="label">Қауіпті / Dangerous</div>
  </div>
  <div class="stat-card">
    <div class="num" style="color:#f59e0b">{total_reports}</div>
    <div class="label">Шағымдар / Reports</div>
  </div>
  <div class="stat-card">
    <div class="num" style="color:#8b5cf6">{total_appeals}</div>
    <div class="label">Апелляциялар / Appeals</div>
  </div>
</div>

<div class="tabs">
  <button class="tab active" onclick="showTab('logs')">Check Logs ({total_checks})</button>
  <button class="tab" onclick="showTab('reports')">Reports ({total_reports})</button>
  <button class="tab" onclick="showTab('appeals')">Appeals ({total_appeals})</button>
  <button class="refresh-btn" onclick="location.reload()">↻ Refresh</button>
</div>

<div id="logs" class="panel active">
  <div class="section-title">Recent Check Logs <span class="count">last 50</span></div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Time</th><th>Domain</th><th>Verdict</th><th>Score</th><th>Source</th><th>AI</th><th>ms</th></tr></thead>
      <tbody>{_rows_logs(logs)}</tbody>
    </table>
  </div>
</div>

<div id="reports" class="panel">
  <div class="section-title">User Reports <span class="count">last 50</span></div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Time</th><th>Domain</th><th>Category</th><th>Lang</th><th>Comment</th></tr></thead>
      <tbody>{_rows_reports(reports)}</tbody>
    </table>
  </div>
</div>

<div id="appeals" class="panel">
  <div class="section-title">User Appeals <span class="count">last 50</span></div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Time</th><th>Domain</th><th>Verdict was</th><th>Reason</th></tr></thead>
      <tbody>{_rows_appeals(appeals)}</tbody>
    </table>
  </div>
</div>

<script>
function showTab(id) {{
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', ['logs','reports','appeals'][i]===id));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('active', p.id===id));
}}
function tick() {{
  document.getElementById('clock').textContent = new Date().toLocaleString('ru-KZ');
}}
tick(); setInterval(tick, 1000);
// Auto-refresh every 60s
setTimeout(() => location.reload(), 60000);
</script>
</body>
</html>"""
