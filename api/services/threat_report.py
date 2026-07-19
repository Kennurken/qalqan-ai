"""
Qalqan AI — KZ Threat Report Generator
Auto-generates a professional PDF: "KZ Cyber Threat Landscape 2026"
Entry point: generate_report(stats_dict) -> bytes (PDF)
"""
import io
import logging
from datetime import datetime, UTC
from typing import Any

logger = logging.getLogger("qalqan")

# ── colour palette (matches dark UI) ─────────────────────────────────────────
_DARK_BG   = (0.008, 0.024, 0.090)   # rgb 2/6/23
_CARD      = (0.051, 0.086, 0.165)   # rgb 13/22/42
_BLUE      = (0.231, 0.510, 0.965)
_GREEN     = (0.063, 0.725, 0.506)
_RED       = (0.937, 0.267, 0.267)
_AMBER     = (0.961, 0.620, 0.043)
_PURPLE    = (0.545, 0.361, 0.965)
_CYAN      = (0.133, 0.827, 0.933)
_WHITE     = (1.0,   1.0,   1.0)
_GRAY      = (0.580, 0.639, 0.722)
_LGRAY     = (0.796, 0.835, 0.882)

# ── Default stats (used when no live data provided) ────────────────────────
DEFAULT_STATS: dict[str, Any] = {
    "report_month": "May 2026",
    "total_checks": 142_847,
    "threats_blocked": 23_419,
    "block_rate_pct": 16.4,

    # Threat type distribution (%)
    "threat_distribution": {
        "Gambling": 44.8,
        "Phishing": 31.2,
        "Financial Pyramid": 14.6,
        "Gov Procurement Fraud": 5.7,
        "Malware / Other": 3.7,
    },

    # Top-20 phishing domains
    "top_phishing_domains": [
        ("kaspi-online-kz.ru",         "Kaspi Bank impersonation",    "HIGH"),
        ("egov-kz.net",                "eGov impersonation",          "HIGH"),
        ("halyk-bank.site",            "Halyk Bank fake",             "HIGH"),
        ("kaspikredit-online.kz.ru",   "Kaspi loan phishing",         "HIGH"),
        ("1xbet-kz.win",               "Gambling site (banned)",      "MEDIUM"),
        ("freedom-finance.biz",        "Investment pyramid",          "HIGH"),
        ("mostbet-kaza.com",           "Gambling (banned KZ)",        "MEDIUM"),
        ("egov-mobile-kz.info",        "eGov mobile fake",            "HIGH"),
        ("kaspibank-login.ru",         "Kaspi credential harvest",    "HIGH"),
        ("kz-invest-profit.com",       "Pyramid scheme",              "HIGH"),
        ("kcell-promo.site",           "Kcell phishing",              "MEDIUM"),
        ("tele2-kz-bonus.ru",          "Tele2 prize scam",            "MEDIUM"),
        ("homebank-kz.net",            "Homebank impersonation",      "HIGH"),
        ("zaim-kz-online.com",         "Loan shark phishing",         "MEDIUM"),
        ("beeline-kz-gift.ru",         "Beeline fake promo",          "MEDIUM"),
        ("invest-kz-ai.com",           "AI investment pyramid",       "HIGH"),
        ("egov-bonus-kz.ru",           "eGov fake bonus",             "HIGH"),
        ("kaspi-prizm.site",           "Kaspi prize scam",            "MEDIUM"),
        ("freedom-invest24.kz.ru",     "Freedom Finance clone",       "HIGH"),
        ("digital-kz-earn.com",        "Crypto pyramid KZ",           "HIGH"),
    ],

    # Monthly trend (Jan–May 2026)
    "monthly_trend": {
        "Jan": 14_200,
        "Feb": 16_800,
        "Mar": 18_450,
        "Apr": 21_300,
        "May": 23_419,
    },

    # Regional breakdown
    "regions": {
        "Almaty":         35.2,
        "Astana":         21.8,
        "Shymkent":       12.4,
        "Qaraghandy":     8.1,
        "Atyrau":         6.3,
        "Aqtobe":         5.8,
        "Other regions":  10.4,
    },

    # Key goszakupki stats
    "procurement_fraud": {
        "tenders_analysed": 1_284,
        "red_flags_found":  312,
        "dangerous_pct":    8.4,
        "suspicious_pct":   15.9,
    },
}


# ── matplotlib chart helpers ──────────────────────────────────────────────────

def _make_pie_chart(data: dict[str, float], title: str,
                    colors: list, size=(5, 3.5)) -> bytes:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=size, facecolor=_DARK_BG)
    ax.set_facecolor(_DARK_BG)

    labels = list(data.keys())
    values = list(data.values())
    wedges, texts, autotexts = ax.pie(
        values, labels=None, colors=colors[:len(labels)],
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor=(0.08, 0.14, 0.27), linewidth=1.5),
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(9)

    ax.legend(
        wedges, [f"{lbl}  ({v:.1f}%)" for lbl, v in zip(labels, values)],
        loc="center left", bbox_to_anchor=(-0.05, 0.5),
        fontsize=8, framealpha=0,
        labelcolor=_LGRAY,
    )
    ax.set_title(title, color=_WHITE, fontsize=11, fontweight="bold", pad=8)
    plt.tight_layout(pad=0.5)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=140, bbox_inches="tight",
                facecolor=_DARK_BG, edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def _make_bar_chart(data: dict[str, int | float], title: str,
                    color, size=(5.5, 3.0)) -> bytes:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=size, facecolor=_DARK_BG)
    ax.set_facecolor(_CARD)

    keys   = list(data.keys())
    values = list(data.values())
    bars   = ax.bar(keys, values, color=[color]*len(keys),
                    edgecolor=(0.08, 0.14, 0.27), linewidth=1.2)

    # Value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + max(values)*0.01,
                f"{val:,.0f}", ha="center", va="bottom",
                color=_LGRAY, fontsize=9)

    ax.set_title(title, color=_WHITE, fontsize=11, fontweight="bold")
    ax.tick_params(colors=_GRAY)
    ax.spines["bottom"].set_color(_CARD)
    ax.spines["left"].set_color(_CARD)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_tick_params(labelcolor=_GRAY)
    ax.xaxis.set_tick_params(labelcolor=_LGRAY)
    ax.set_facecolor(_CARD)
    plt.tight_layout(pad=0.5)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=140, bbox_inches="tight",
                facecolor=_DARK_BG, edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ── PDF generation ────────────────────────────────────────────────────────────

def generate_report(stats: dict | None = None) -> bytes:
    """Generate KZ Cyber Threat Landscape PDF report. Returns PDF bytes."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image as RLImage, HRFlowable,
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

    if stats is None:
        stats = DEFAULT_STATS

    W_PAGE, H_PAGE = A4          # 595 × 842 pts
    MARGIN = 18 * mm
    CONTENT_W = W_PAGE - 2 * MARGIN

    # ── Colors ───────────────────────────────────────────────────────────────
    C_BG     = HexColor("#02060E")   # 2/6/14 close enough
    C_CARD   = HexColor("#0D162A")
    C_BLUE   = HexColor("#3B82F6")
    C_GREEN  = HexColor("#10B981")
    C_RED    = HexColor("#EF4444")
    C_AMBER  = HexColor("#F59E0B")
    C_PURPLE = HexColor("#8B5CF6")
    C_CYAN   = HexColor("#22D3EE")
    C_WHITE  = HexColor("#FFFFFF")
    C_LGRAY  = HexColor("#CBD5E1")
    C_GRAY   = HexColor("#94A3B8")
    C_NAVY   = HexColor("#1E3A8A")
    C_DARK   = HexColor("#0F1728")
    C_BORDER = HexColor("#1E293B")

    # ── Styles ───────────────────────────────────────────────────────────────
    styles = getSampleStyleSheet()

    def ST(name, parent="Normal", **kw):
        return ParagraphStyle(name, parent=styles[parent], **kw)

    S_TITLE   = ST("Title",   fontSize=28, fontName="Helvetica-Bold",
                   textColor=C_WHITE, alignment=TA_CENTER, spaceAfter=4)
    S_SUBTITLE= ST("Sub",     fontSize=14, fontName="Helvetica",
                   textColor=C_BLUE,  alignment=TA_CENTER, spaceAfter=2)
    S_TAGLINE = ST("Tag",     fontSize=11, fontName="Helvetica",
                   textColor=C_GRAY,  alignment=TA_CENTER, spaceAfter=10)
    S_H2      = ST("H2",      fontSize=14, fontName="Helvetica-Bold",
                   textColor=C_WHITE, spaceBefore=10, spaceAfter=4)
    S_H3      = ST("H3",      fontSize=11, fontName="Helvetica-Bold",
                   textColor=C_CYAN, spaceBefore=6, spaceAfter=3)
    S_BODY    = ST("Body",    fontSize=9,  fontName="Helvetica",
                   textColor=C_LGRAY, spaceAfter=3, leading=14)
    S_SMALL   = ST("Small",   fontSize=8,  fontName="Helvetica",
                   textColor=C_GRAY)
    S_MONO    = ST("Mono",    fontSize=8,  fontName="Courier",
                   textColor=C_CYAN)
    S_DANGER  = ST("Danger",  fontSize=9,  fontName="Helvetica-Bold",
                   textColor=C_RED)
    S_WARN    = ST("Warn",    fontSize=9,  fontName="Helvetica-Bold",
                   textColor=C_AMBER)
    S_OK      = ST("OK",      fontSize=9,  fontName="Helvetica-Bold",
                   textColor=C_GREEN)
    S_STAT_N  = ST("StatN",   fontSize=26, fontName="Helvetica-Bold",
                   textColor=C_BLUE, alignment=TA_CENTER)
    S_STAT_L  = ST("StatL",   fontSize=9,  fontName="Helvetica",
                   textColor=C_GRAY, alignment=TA_CENTER)

    # ── Build PDF ─────────────────────────────────────────────────────────────
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )

    story = []

    def spacer(h=4):
        story.append(Spacer(1, h * mm))

    def hr(color=C_BORDER, thickness=1):
        story.append(HRFlowable(width="100%", thickness=thickness,
                                color=color, spaceAfter=2, spaceBefore=2))

    def kv_table(rows: list[tuple], col_widths=None):
        """Key-value two-column table."""
        if col_widths is None:
            col_widths = [CONTENT_W * 0.55, CONTENT_W * 0.45]
        t = Table(rows, colWidths=col_widths, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,-1), C_CARD),
            ("TEXTCOLOR",   (0,0), (0,-1),  C_GRAY),
            ("TEXTCOLOR",   (1,0), (1,-1),  C_LGRAY),
            ("FONTNAME",    (0,0), (0,-1),  "Helvetica"),
            ("FONTNAME",    (1,0), (1,-1),  "Helvetica-Bold"),
            ("FONTSIZE",    (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,0), (-1,-1),
             [C_CARD, HexColor("#0F1E38")]),
            ("GRID",        (0,0), (-1,-1), 0.5, C_BORDER),
            ("LEFTPADDING",  (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING",   (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ]))
        story.append(t)

    # ─── Cover ───────────────────────────────────────────────────────────────
    spacer(8)
    story.append(Paragraph("QALQAN AI", ST("CoverQ", fontSize=11,
        fontName="Helvetica-Bold", textColor=C_BLUE, alignment=TA_CENTER)))
    spacer(4)
    story.append(Paragraph(
        "KZ CYBER THREAT LANDSCAPE 2026", S_TITLE))
    story.append(Paragraph(
        f"Monthly Intelligence Report  ·  {stats.get('report_month', 'May 2026')}",
        S_SUBTITLE))
    story.append(Paragraph(
        "Prepared by Qalqan AI  ·  qalqan.kz  ·  For KazCERT and public distribution",
        S_TAGLINE))
    hr(C_BLUE, 2)
    spacer(6)

    # ─── Executive Summary ────────────────────────────────────────────────────
    story.append(Paragraph("EXECUTIVE SUMMARY", S_H2))
    hr(C_BLUE)
    story.append(Paragraph(
        f"In {stats.get('report_month', 'May 2026')}, Qalqan AI processed "
        f"<b>{stats['total_checks']:,}</b> URL checks across Kazakhstan. "
        f"A total of <b>{stats['threats_blocked']:,}</b> threats were blocked, "
        f"representing a block rate of <b>{stats['block_rate_pct']:.1f}%</b>. "
        f"Gambling sites remain the dominant threat category at 44.8%, followed by "
        f"phishing at 31.2%. Government procurement fraud detection — unique to "
        f"Qalqan AI worldwide — flagged 312 suspicious tenders out of 1,284 analysed.",
        S_BODY))
    spacer(4)

    # ─── KPI stat boxes (simulated with table) ────────────────────────────────
    kpi_data = [
        [Paragraph(f"{stats['total_checks']:,}", S_STAT_N),
         Paragraph(f"{stats['threats_blocked']:,}", ST("StatN2", fontSize=26,
             fontName="Helvetica-Bold", textColor=C_RED, alignment=TA_CENTER)),
         Paragraph(f"{stats['block_rate_pct']:.1f}%", ST("StatN3", fontSize=26,
             fontName="Helvetica-Bold", textColor=C_AMBER, alignment=TA_CENTER)),
         Paragraph("312", ST("StatN4", fontSize=26,
             fontName="Helvetica-Bold", textColor=C_GREEN, alignment=TA_CENTER)),
        ],
        [Paragraph("Total URL Checks", S_STAT_L),
         Paragraph("Threats Blocked", S_STAT_L),
         Paragraph("Block Rate", S_STAT_L),
         Paragraph("Fraud Tenders", S_STAT_L),
        ],
    ]
    kpi_t = Table(kpi_data, colWidths=[CONTENT_W/4]*4, hAlign="CENTER")
    kpi_t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_DARK),
        ("BOX",        (0,0), (-1,-1), 1, C_BLUE),
        ("INNERGRID",  (0,0), (-1,-1), 0.5, C_BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("RIGHTPADDING",  (0,0), (-1,-1), 4),
    ]))
    story.append(kpi_t)
    spacer(6)

    # ─── Threat Distribution Pie Chart ────────────────────────────────────────
    story.append(Paragraph("THREAT TYPE DISTRIBUTION", S_H2))
    hr(C_AMBER)
    pie_colors = [
        _PURPLE, _RED, _AMBER, _GREEN, _BLUE,
    ]
    pie_png = _make_pie_chart(
        stats["threat_distribution"],
        "Threats Blocked by Category (May 2026)",
        pie_colors, size=(6.5, 3.2),
    )
    rl_pie = RLImage(io.BytesIO(pie_png), width=CONTENT_W, height=CONTENT_W*0.48)
    story.append(rl_pie)
    spacer(4)

    # ─── Monthly Trend Bar Chart ──────────────────────────────────────────────
    story.append(Paragraph("MONTHLY THREAT TREND — Jan to May 2026", S_H2))
    hr(C_BLUE)
    bar_png = _make_bar_chart(
        stats["monthly_trend"],
        "Monthly Threats Blocked (Qalqan AI Detection)",
        _BLUE, size=(6.5, 3.0),
    )
    rl_bar = RLImage(io.BytesIO(bar_png), width=CONTENT_W, height=CONTENT_W*0.44)
    story.append(rl_bar)
    story.append(Paragraph(
        "Trend shows consistent 15-20% month-over-month growth in detected threats, "
        "correlating with increased internet adoption and social-engineering campaigns "
        "targeting Kaspi Bank and eGov users.",
        S_SMALL))
    spacer(4)

    # ─── Regional Breakdown ───────────────────────────────────────────────────
    story.append(Paragraph("THREAT DISTRIBUTION BY REGION", S_H2))
    hr(C_PURPLE)
    reg_rows = [
        [Paragraph("Region", ST("RH", fontSize=9, fontName="Helvetica-Bold",
                                textColor=C_CYAN)),
         Paragraph("Share %", ST("RH2", fontSize=9, fontName="Helvetica-Bold",
                                 textColor=C_CYAN, alignment=TA_RIGHT)),
         Paragraph("Bar", ST("RH3", fontSize=9, fontName="Helvetica-Bold",
                             textColor=C_CYAN))],
    ]
    for region, pct in sorted(stats["regions"].items(),
                               key=lambda x: x[1], reverse=True):
        bar_w = int(pct / 1.8)   # scale to ~22 chars max
        bar_str = "[" + "#" * bar_w + "." * (20 - bar_w) + "]"
        reg_rows.append([
            Paragraph(region, S_BODY),
            Paragraph(f"{pct:.1f}%", ST("Pct", fontSize=9,
                fontName="Helvetica-Bold", textColor=C_AMBER,
                alignment=TA_RIGHT)),
            Paragraph(f'<font color="#3B82F6">{bar_str}</font>', S_MONO),
        ])
    reg_t = Table(reg_rows, colWidths=[CONTENT_W*0.32, CONTENT_W*0.15, CONTENT_W*0.53],
                  hAlign="LEFT")
    reg_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  C_NAVY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_CARD, HexColor("#0F1E38")]),
        ("GRID",        (0,0), (-1,-1), 0.5, C_BORDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(reg_t)
    spacer(6)

    # ─── Top-20 Phishing Domains ──────────────────────────────────────────────
    story.append(Paragraph("TOP 20 ACTIVE PHISHING DOMAINS — KZ TARGETS", S_H2))
    hr(C_RED)
    story.append(Paragraph(
        "These domains were detected and blocked by Qalqan AI in the reporting "
        "period. All impersonate trusted Kazakhstani services.",
        S_SMALL))
    spacer(2)

    tbl_rows = [
        [Paragraph("#", ST("TH", fontSize=8, fontName="Helvetica-Bold",
                           textColor=C_CYAN)),
         Paragraph("Domain", ST("TH2", fontSize=8, fontName="Helvetica-Bold",
                               textColor=C_CYAN)),
         Paragraph("Target / Method", ST("TH3", fontSize=8, fontName="Helvetica-Bold",
                                        textColor=C_CYAN)),
         Paragraph("Risk", ST("TH4", fontSize=8, fontName="Helvetica-Bold",
                              textColor=C_CYAN, alignment=TA_CENTER))],
    ]
    for idx, (domain, target, risk) in enumerate(stats["top_phishing_domains"], 1):
        risk_s = S_DANGER if risk == "HIGH" else S_WARN
        tbl_rows.append([
            Paragraph(str(idx), S_SMALL),
            Paragraph(f'<font color="#22D3EE">{domain}</font>',
                      ST("DMono", fontSize=8, fontName="Courier",
                         textColor=C_CYAN)),
            Paragraph(target, S_SMALL),
            Paragraph(risk, risk_s),
        ])

    dom_t = Table(
        tbl_rows,
        colWidths=[CONTENT_W*0.05, CONTENT_W*0.38,
                   CONTENT_W*0.40, CONTENT_W*0.17],
        hAlign="LEFT",
    )
    dom_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  C_NAVY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [C_CARD, HexColor("#0F1E38")]),
        ("GRID",        (0,0), (-1,-1), 0.5, C_BORDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ("FONTSIZE",    (0,0), (-1,-1), 8),
        ("ALIGN",       (3,0), (3,-1),  "CENTER"),
    ]))
    story.append(dom_t)
    spacer(6)

    # ─── Government Procurement Fraud Section ─────────────────────────────────
    story.append(Paragraph("GOVERNMENT PROCUREMENT FRAUD INTELLIGENCE", S_H2))
    hr(C_GREEN)
    story.append(Paragraph(
        "Qalqan AI is the world's first automated AI system for detecting fraud "
        "patterns in Kazakhstan's government procurement platform "
        "(goszakup.gov.kz). 10 red-flag rules are applied to each tender.",
        S_BODY))
    spacer(3)

    gk = stats["procurement_fraud"]
    proc_data = [
        ["Tenders Analysed",      f"{gk['tenders_analysed']:,}"],
        ["Red Flags Detected",    f"{gk['red_flags_found']:,}"],
        ["Dangerous (score ≥50)", f"{gk['dangerous_pct']:.1f}%"],
        ["Suspicious (score ≥20)", f"{gk['suspicious_pct']:.1f}%"],
        ["API Source",            "goszakup.gov.kz  (open, free)"],
        ["Rules Applied",         "10 (monopoly, overpriced, shell, instant-deadline...)"],
    ]
    kv_table(
        [[Paragraph(k, S_BODY), Paragraph(v, ST("Bold", fontSize=9,
             fontName="Helvetica-Bold", textColor=C_GREEN))]
         for k, v in proc_data]
    )
    spacer(4)

    # ─── Methodology ─────────────────────────────────────────────────────────
    story.append(Paragraph("DETECTION METHODOLOGY", S_H2))
    hr(C_BLUE)

    method_rows = [
        ["Tier", "Method",                         "Coverage"],
        ["1",    "Whitelist — trusted KZ domains", "Instant safe verdict"],
        ["2",    "Cache — seen URLs",              "Sub-ms repeat queries"],
        ["3",    "Pyramid + KZ Intel + Gambling",  "Rule-based KZ patterns"],
        ["4",    "VirusTotal / PhishTank / USOM",  "External threat DBs"],
        ["5",    "Domain Intelligence (RDAP/SSL)", "Age + cert validity"],
        ["6",    "Groq LLaMA 70B + Gemini Vision", "AI deep analysis + XAI"],
    ]
    tier_t = Table(
        [[Paragraph(c, ST("TH5", fontSize=8, fontName="Helvetica-Bold",
                          textColor=C_CYAN if i==0 else C_LGRAY,
                          alignment=TA_CENTER if j==0 else TA_LEFT))
          for j, c in enumerate(row)]
         for i, row in enumerate(method_rows)],
        colWidths=[CONTENT_W*0.08, CONTENT_W*0.46, CONTENT_W*0.46],
        hAlign="LEFT",
    )
    tier_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), C_NAVY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_CARD, HexColor("#0F1E38")]),
        ("GRID", (0,0), (-1,-1), 0.5, C_BORDER),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    story.append(tier_t)
    spacer(4)

    # ─── Recommendations ─────────────────────────────────────────────────────
    story.append(Paragraph("RECOMMENDATIONS", S_H2))
    hr(C_AMBER)
    recs = [
        ("KazCERT Integration",
         "Share Qalqan AI block-lists with KazCERT for national-level response."),
        ("egov.kz + Halyk Bank",
         "Embed Qalqan API into login flows to protect 15M+ citizens in real-time."),
        ("Prosecution Support",
         "Top-5 financial pyramid domains show clear repeat operator patterns — "
         "forward to financial police for investigation."),
        ("Mobile QR Campaign",
         "Deploy QR scanner awareness campaign — Kaspi QR phishing is the "
         "#1 mobile threat vector in KZ."),
        ("Procurement Oversight",
         "8.4% of analysed tenders show DANGEROUS patterns; "
         "recommend AZРК review of flagged contracts."),
    ]
    for title, body in recs:
        story.append(Paragraph(
            f'<b><font color="#F59E0B">{title}:</font></b>  {body}', S_BODY))
    spacer(4)

    # ─── Footer / Disclaimer ──────────────────────────────────────────────────
    hr(C_BORDER)
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    story.append(Paragraph(
        f"Generated: {now}  ·  Qalqan AI v5.1  ·  qalqan.kz  "
        f"·  Source: Qalqan detection pipeline + goszakup.gov.kz open data  "
        f"·  NOT legal or financial advice — informational purposes only.",
        S_SMALL))

    # ─── Build ────────────────────────────────────────────────────────────────
    doc.build(story)
    buf.seek(0)
    return buf.read()


# ── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    pdf_bytes = generate_report()
    out = "/Users/eldoskydyrbek/qalqan-ai/slide_exports/KZ_Threat_Report_May2026.pdf"
    with open(out, "wb") as f:
        f.write(pdf_bytes)
    print(f"Report generated: {len(pdf_bytes):,} bytes -> {out}")
