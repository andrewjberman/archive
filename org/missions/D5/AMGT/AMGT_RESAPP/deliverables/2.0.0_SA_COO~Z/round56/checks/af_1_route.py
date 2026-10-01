"""AMGT_RESAPP round 56 -- AMGT-af-1 AC2: the monthly chatter route, read through the real handler.

Calls lib.research.api.scoped_amgt.handler locally with an API Gateway v2 event for
GET /api/scoped/amgt/lead-panel/timeseries/collected/chatter (live S3, read-only), or grades
a saved response body (--from-json, the positive / negative arms).

The oracle is computed HERE, independently of the route: the latest gold chatter_daily snapshot
(articles_total summed per calendar month) and the latest gold article_security_mention snapshot
(distinct (article_key, security_key) per publisher per month), both through pool_reader, over the
covered universe read fresh (lib/research/coverage/covered_universe.py).

Prints one line per clause and the verdict line:
  THE MONTHLY CHATTER ROUTE SERVES EVERY COVERED NAME FROM GOLD: YES|NO
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from collections import defaultdict

PATH = "/api/scoped/amgt/lead-panel/timeseries/collected/chatter"
CONTROL = ("BA_US_Equity", "2026-09")


def _oracle():
    from lib.research.coverage import pool_reader as pr
    from lib.research.coverage.covered_universe import covered_security_keys

    covered = covered_security_keys()
    daily = pr._gold_latest_snapshot_rows("chatter_daily")
    mentions = pr._gold_latest_snapshot_rows("article_security_mention")
    days = [str(r["day"])[:10] for r in daily]
    as_of = max(days) if days else None
    first_month = min(days)[:7] if days else None
    collected = defaultdict(int)
    for r in daily:
        n = int(r.get("articles_total") or 0)
        if n:
            collected[(r["security_key"], str(r["day"])[:7])] += n
    seen = set()
    by_pub = defaultdict(lambda: defaultdict(int))
    for r in mentions:
        k = (r["article_key"], r["security_key"])
        if k in seen:
            continue
        seen.add(k)
        m = str(r["published_utc"])[:7]
        if first_month and m >= first_month:
            by_pub[(r["security_key"], m)][r["publisher"]] += 1
    return covered, as_of, first_month, collected, by_pub


def _live_body():
    from lib.research.api import scoped_amgt

    ev = {
        "rawPath": PATH,
        "requestContext": {"http": {"method": "GET"}},
        "headers": {"x-firm-id": "bd"},
        "queryStringParameters": None,
    }
    resp = scoped_amgt.handler(ev)
    return resp.get("statusCode"), json.loads(resp.get("body") or "null")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-json", help="grade a saved response body instead of calling the handler")
    a = ap.parse_args()
    if a.from_json:
        status, body = 200, json.load(open(a.from_json, encoding="utf-8"))
    else:
        status, body = _live_body()
    covered, as_of, first_month, collected, by_pub = _oracle()
    print(f"oracle: covered names {len(covered)} (fresh read of research_dossier/); gold as_of {as_of}; "
          f"name-months with collected>0: {len(collected)}")
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    clause("C1 status 200, not refused", status == 200 and isinstance(body, dict) and not body.get("refused"),
           f"status={status} refused={isinstance(body, dict) and body.get('refused')}")
    if not (status == 200 and isinstance(body, dict) and not body.get("refused")):
        print("THE MONTHLY CHATTER ROUTE SERVES EVERY COVERED NAME FROM GOLD: NO")
        return 1
    rows = body.get("rows") or []
    served = {r.get("security_key"): r for r in rows}
    clause("C2 one row per covered name, no other", sorted(served) == covered and len(rows) == len(covered),
           f"served {len(rows)} rows / {len(served)} distinct vs covered {len(covered)}")
    months = body.get("months") or []
    cur = (as_of or "")[:7]
    try:
        y, m = int(cur[:4]), int(cur[5:7])
        prev = [f"{y if m - i > 0 else y - 1}-{(m - i - 1) % 12 + 1:02d}" for i in (1, 2)]
    except ValueError:
        prev = []
    clause("C3 months ascending, include as_of month and the two before",
           months == sorted(months) and cur in months and all(p in months for p in prev),
           f"months {months[:1]}..{months[-1:]} cur={cur}")
    last_day = (datetime.date.fromisoformat(as_of) + datetime.timedelta(days=1)).month != int(cur[5:7]) if as_of else False
    clause("C4 as_of equals newest gold day; source names gold chatter_daily; partial month flagged",
           body.get("as_of") == as_of and "chatter_daily" in str(body.get("source", ""))
           and (last_day or cur in (body.get("partial_months") or [])),
           f"as_of served={body.get('as_of')} oracle={as_of} partial={body.get('partial_months')}")
    zero_rows, mismatch, pub_mismatch = 0, [], []
    for k, r in served.items():
        bm = r.get("by_month") or {}
        for mo, cell in bm.items():
            c = int((cell or {}).get("collected") or 0)
            if c == 0:
                zero_rows += 1
            if c != collected.get((k, mo), 0):
                mismatch.append((k, mo, c, collected.get((k, mo), 0)))
            bp = {p: int(v) for p, v in ((cell or {}).get("by_publisher") or {}).items() if int(v)}
            if bp != dict(by_pub.get((k, mo), {})):
                pub_mismatch.append((k, mo, bp, dict(by_pub.get((k, mo), {}))))
        for (kk, mo), n in collected.items():
            if kk == k and n and mo not in bm and mo in months:
                mismatch.append((k, mo, None, n))
    clause("C5 no zero-collected month cell (an empty month is absent)", zero_rows == 0, f"zero cells {zero_rows}")
    clause("C6 every collected count equals the gold recompute", not mismatch,
           f"mismatches {len(mismatch)} {mismatch[:3]}")
    clause("C7 every by_publisher equals the mention recompute", not pub_mismatch,
           f"mismatches {len(pub_mismatch)} {pub_mismatch[:2]}")
    ck, cm = CONTROL
    cval = int(((served.get(ck) or {}).get("by_month") or {}).get(cm, {}).get("collected") or 0)
    clause("C8 positive control BA_US_Equity 2026-09 collected > 0", cval > 0, f"value {cval}")
    verdict = all(ok)
    print(f"THE MONTHLY CHATTER ROUTE SERVES EVERY COVERED NAME FROM GOLD: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
