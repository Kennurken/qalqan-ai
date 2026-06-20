"""Goszakup fraud-graph: affiliation / collusion / cartel detection."""
from fastapi.testclient import TestClient

import api.index as m
from api.services.goszakup_graph import build_fraud_graph, demo_graph_data

client = TestClient(m.app)


def test_demo_flags_collusion():
    g = build_fraud_graph(demo_graph_data())
    assert g["verdict"] == "DANGEROUS"
    rules = {f["rule"] for f in g["findings"]}
    # core economic-fraud patterns must fire on the demo scenario
    for r in ("shared_founder", "shared_address", "conflict_of_interest",
              "cartel_bidding", "repeat_winner", "price_collusion"):
        assert r in rules, f"missing {r}"


def test_clean_data_is_safe():
    data = {
        "companies": [
            {"bin": "C1", "name": "Akimat", "role": "customer", "address": "A1",
             "founders": ["X"], "employees": 100},
            {"bin": "S1", "name": "Honest LLP", "role": "supplier", "address": "B9",
             "founders": ["Y"], "employees": 40, "reg_date": "2019-01-01"},
        ],
        "tenders": [{"id": "T1", "customer_bin": "C1", "winner_bin": "S1",
                     "bidders": ["S1"], "amount": 70_000_000, "ref_price": 100_000_000,
                     "date": "2026-05-01"}],
    }
    g = build_fraud_graph(data)
    assert g["verdict"] == "SAFE"
    assert g["findings"] == []


def test_edges_deduped():
    g = build_fraud_graph(demo_graph_data())
    keys = [(e["source"], e["target"], e["kind"]) for e in g["edges"]]
    assert len(keys) == len(set(keys)), "edges must be unique"


def test_graph_endpoints():
    d = client.get("/goszakup/graph/demo").json()
    assert d["_source"] == "demo" and d["summary"]["flags"] > 0
    assert client.get("/goszakup/graph").status_code == 200
    r = client.post("/goszakup/graph", json={"companies": [], "tenders": []})
    assert r.status_code == 200 and r.json()["verdict"] == "SAFE"
