# Qalqan AI — Goszakup fraud graph
# Relationship-graph analysis over procurement data: customer ↔ supplier ↔
# founder ↔ address ↔ official. Detects affiliation, collusion, cartels —
# the economic-threat core (ДЭР). Pure Python (no networkx dependency).

from datetime import datetime, UTC

# Node type → display color (consumed by the graph viz)
NODE_COLORS = {
    "customer": "#00d4ff", "supplier": "#a855f7", "founder": "#f59e0b",
    "address": "#22c55e", "official": "#ef4444",
}

_PRICE_COLLUSION_RATIO = 0.985   # winning bid ≥98.5% of start price → no real discount
_REPEAT_WINNER_LIMIT = 3         # supplier wins ≥3 tenders from one customer
_NEW_WINNER_DAYS = 30


def _days_ago(date_str) -> int | None:
    try:
        dt = datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return (datetime.now(UTC) - dt).days
    except Exception:
        return None


def build_fraud_graph(data: dict) -> dict:
    """Build a relationship graph + detect affiliation/collusion patterns.

    Input: {"companies": [{bin, name, role(customer|supplier), address,
            founders[], officials[], reg_date, employees}], "tenders":
            [{id, customer_bin, winner_bin, bidders[], amount, ref_price, date}]}
    Returns: {nodes, edges, findings, risk_score, summary}.
    """
    companies = {c["bin"]: c for c in data.get("companies", []) if c.get("bin")}
    tenders = data.get("tenders", [])

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    findings: list[dict] = []
    risky_nodes: set[str] = set()
    risky_edges: set[tuple] = set()

    def node(nid, label, ntype):
        if nid not in nodes:
            nodes[nid] = {"id": nid, "label": label, "type": ntype, "risk": False}
        return nid

    def edge(a, b, kind, risk=False):
        edges.append({"source": a, "target": b, "kind": kind, "risk": risk})
        if risk:
            risky_edges.add((a, b))

    # ── Build nodes + structural edges ───────────────────────────────────────
    for bin_, c in companies.items():
        role = c.get("role", "supplier")
        cid = node(f"co:{bin_}", c.get("name", bin_), "customer" if role == "customer" else "supplier")
        for f in c.get("founders", []):
            edge(cid, node(f"fo:{f}", f, "founder"), "founded_by")
        for o in c.get("officials", []):
            edge(cid, node(f"of:{o}", o, "official"), "official")
        addr = c.get("address")
        if addr:
            edge(cid, node(f"ad:{addr}", addr, "address"), "at_address")

    for t in tenders:
        cust, win = t.get("customer_bin"), t.get("winner_bin")
        if cust and win and f"co:{cust}" in nodes and f"co:{win}" in nodes:
            edge(f"co:{cust}", f"co:{win}", "awarded")

    # ── Fraud patterns ───────────────────────────────────────────────────────
    def flag(rule, score, kk, ru, en, involved):
        findings.append({"rule": rule, "score": score, "kk": kk, "ru": ru, "en": en,
                         "nodes": involved})
        for nid in involved:
            risky_nodes.add(nid)

    def _set(c, key):
        return set(c.get(key, []) or [])

    # Per awarded customer→supplier pair: shared founder / address (affiliation)
    repeat = {}
    for t in tenders:
        cust, win = t.get("customer_bin"), t.get("winner_bin")
        c, s = companies.get(cust), companies.get(win)
        if not c or not s:
            continue
        repeat[(cust, win)] = repeat.get((cust, win), 0) + 1

        shared_f = _set(c, "founders") & _set(s, "founders")
        if shared_f:
            edge(f"co:{cust}", f"co:{win}", "affiliated", risk=True)
            flag("shared_founder", 40,
                 f"Тапсырыс беруші мен жеңімпаз ортақ құрылтайшы: {', '.join(shared_f)}",
                 f"Заказчик и победитель имеют общего учредителя: {', '.join(shared_f)}",
                 f"Customer and winner share a founder: {', '.join(shared_f)}",
                 [f"co:{cust}", f"co:{win}"] + [f"fo:{x}" for x in shared_f])

        if c.get("address") and c.get("address") == s.get("address"):
            edge(f"co:{cust}", f"co:{win}", "same_address", risk=True)
            flag("shared_address", 35,
                 f"Тапсырыс беруші мен жеңімпаз бір мекенжайда: {c['address']}",
                 f"Заказчик и победитель по одному адресу: {c['address']}",
                 f"Customer and winner at same address: {c['address']}",
                 [f"co:{cust}", f"co:{win}", f"ad:{c['address']}"])

        # Official of customer is also a founder of the winner (conflict of interest)
        coi = _set(c, "officials") & _set(s, "founders")
        if coi:
            flag("conflict_of_interest", 45,
                 f"Тапсырыс берушінің лауазымды тұлғасы жеңімпаздың құрылтайшысы: {', '.join(coi)}",
                 f"Чиновник заказчика — учредитель победителя: {', '.join(coi)}",
                 f"Customer's official is the winner's founder: {', '.join(coi)}",
                 [f"co:{cust}", f"co:{win}"])

        # Price collusion: winning bid suspiciously close to start price
        amt, ref = t.get("amount"), t.get("ref_price")
        if amt and ref and ref > 0 and amt / ref >= _PRICE_COLLUSION_RATIO:
            flag("price_collusion", 25,
                 f"Жеңімпаз баға бастапқының {round(amt/ref*100,1)}%-і — нақты бәсеке жоқ",
                 f"Цена победителя — {round(amt/ref*100,1)}% от стартовой — сговор",
                 f"Winning bid is {round(amt/ref*100,1)}% of start price — collusion",
                 [f"co:{cust}", f"co:{win}"])

        # Shell winner
        if isinstance(s.get("employees"), (int, float)) and s["employees"] <= 1:
            flag("shell_winner", 20,
                 "Жеңімпаз 0-1 қызметкер — қалқа компания",
                 "У победителя 0-1 сотрудник — фирма-однодневка",
                 "Winner has 0-1 employees — shell company",
                 [f"co:{win}"])

        # New winner
        age = _days_ago(s.get("reg_date"))
        if age is not None and age < _NEW_WINNER_DAYS:
            flag("new_winner", 20,
                 f"Жеңімпаз {age} күн бұрын тіркелген",
                 f"Победитель зарегистрирован {age} дн. назад",
                 f"Winner registered {age} days ago",
                 [f"co:{win}"])

    # Repeat winner (same customer→supplier ≥ N)
    for (cust, win), n in repeat.items():
        if n >= _REPEAT_WINNER_LIMIT:
            flag("repeat_winner", 25,
                 f"Бір жеткізуші осы тапсырыс берушіден {n} тендер жеңді",
                 f"Один поставщик выиграл {n} тендеров у этого заказчика",
                 f"One supplier won {n} tenders from this customer",
                 [f"co:{cust}", f"co:{win}"])

    # Cartel: multiple bidders on the same tender share a founder or address
    for t in tenders:
        bidders = [companies[b] for b in t.get("bidders", []) if b in companies]
        for i in range(len(bidders)):
            for j in range(i + 1, len(bidders)):
                a, b = bidders[i], bidders[j]
                sf = _set(a, "founders") & _set(b, "founders")
                same_addr = a.get("address") and a.get("address") == b.get("address")
                if sf or same_addr:
                    edge(f"co:{a['bin']}", f"co:{b['bin']}", "cartel", risk=True)
                    why = (f"ортақ құрылтайшы {', '.join(sf)}" if sf else f"бір мекенжай {a.get('address')}")
                    flag("cartel_bidding", 35,
                         f"Бір тендерде байланысты қатысушылар ({why}) — картель",
                         f"Связанные участники одного тендера ({'общий учредитель ' + ', '.join(sf) if sf else 'один адрес'}) — картель",
                         f"Linked bidders on one tender ({'shared founder' if sf else 'same address'}) — cartel",
                         [f"co:{a['bin']}", f"co:{b['bin']}"])

    for nid in risky_nodes:
        if nid in nodes:
            nodes[nid]["risk"] = True

    # de-dup edges by (source, target, kind); keep risk if any duplicate is risky
    edge_map: dict[tuple, dict] = {}
    for e in edges:
        k = (e["source"], e["target"], e["kind"])
        if k in edge_map:
            edge_map[k]["risk"] = edge_map[k]["risk"] or e["risk"]
        else:
            edge_map[k] = e
    edges = list(edge_map.values())

    score = min(sum(f["score"] for f in findings), 100)
    verdict = "DANGEROUS" if score >= 50 else "SUSPICIOUS" if score >= 20 else "SAFE"
    # de-dup findings by (rule, nodes)
    seen, uniq = set(), []
    for f in findings:
        k = (f["rule"], tuple(sorted(f["nodes"])))
        if k not in seen:
            seen.add(k)
            uniq.append(f)

    return {
        "verdict": verdict,
        "risk_score": score,
        "nodes": list(nodes.values()),
        "edges": edges,
        "findings": uniq,
        "summary": {
            "companies": len(companies), "tenders": len(tenders),
            "nodes": len(nodes), "edges": len(edges), "flags": len(uniq),
        },
    }


def demo_graph_data() -> dict:
    """A juicy demo procurement dataset for the graph viz."""
    return {
        "companies": [
            {"bin": "C1", "name": "Әкімдік (Akimat)", "role": "customer",
             "address": "Абай 38", "founders": ["Серік А."], "officials": ["Нұрлан Қ."], "employees": 120},
            {"bin": "S1", "name": "ТОО «Альфа Строй»", "role": "supplier",
             "address": "Абай 38", "founders": ["Серік А."], "reg_date": "2026-06-01", "employees": 1},
            {"bin": "S2", "name": "ТОО «Бета Групп»", "role": "supplier",
             "address": "Желтоқсан 12", "founders": ["Айгүл М."], "employees": 8},
            {"bin": "S3", "name": "ТОО «Гамма Trade»", "role": "supplier",
             "address": "Желтоқсан 12", "founders": ["Айгүл М."], "employees": 5},
            {"bin": "S4", "name": "ТОО «Дельта»", "role": "supplier",
             "address": "Сейфуллин 5", "founders": ["Нұрлан Қ."], "employees": 3},
        ],
        "tenders": [
            {"id": "T1", "customer_bin": "C1", "winner_bin": "S1", "bidders": ["S1", "S2", "S3"],
             "amount": 99_800_000, "ref_price": 100_000_000, "date": "2026-06-10"},
            {"id": "T2", "customer_bin": "C1", "winner_bin": "S1", "bidders": ["S1", "S4"],
             "amount": 49_900_000, "ref_price": 50_000_000, "date": "2026-05-20"},
            {"id": "T3", "customer_bin": "C1", "winner_bin": "S1", "bidders": ["S1"],
             "amount": 30_000_000, "ref_price": 30_000_000, "date": "2026-04-15"},
            {"id": "T4", "customer_bin": "C1", "winner_bin": "S4", "bidders": ["S4", "S2"],
             "amount": 19_900_000, "ref_price": 20_000_000, "date": "2026-03-11"},
        ],
    }
