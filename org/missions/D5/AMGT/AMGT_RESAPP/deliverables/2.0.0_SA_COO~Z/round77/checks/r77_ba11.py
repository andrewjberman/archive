"""AMGT_RESAPP round 77 -- AMGT-ba-11: the adapter cell, the one writer of lib/research/api/scoped_amgt.py this round.

  --crit AC1|AC3 --where local|deployed [--names N]

AC1 (build; the handler is called in-process for `local`, the deployed function is invoked for `deployed`):
    C1 PRD v0.41: POST /refresh is gone -- the route answers 404 and the route table no longer lists it;
    C2 the name-search hookup (ba-9): GET /resolve?q=Lenovo answers 200 with status "candidates" listing
       992_HK_Equity, and GET /resolve?q=992 HK answers status "exact"; the route table lists GET .../resolve;
    C3 row Z-S278: on every covered name's /overlay, an absent `chatter` carries a non-empty `chatter_absent_reason`
       and an absent `price` a non-empty `price_absent_reason` (a present axis carries None for its reason);
    C4 the news-day hookup (ba-8): every covered name's `top_band` either serves items for a day inside the last 30
       days, or serves items [] with items_reason exactly "No news in the last 30 days" (a failed read keeps its own
       plain reason and is counted, never passed as "no news");
    C5 the translated-text hookup (ba-10): on /thesis for the names that serve drafted sentences, every served sentence
       carries the keys `text_translated`, `translated` and `source_language` (denominator printed, above 0).
AC3 (control): lib/research/api/tests/test_scoped_amgt_mount.py passes -- the adapter's route table and the gateway
    route list in infra/aws/terraform/harvest/scoped-amgt-api.tf still agree after the /refresh -> /resolve swap.
(AC2 is the worker's own print_equal.py; see the order.)
Verdict: R77 BA11 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
NO_NEWS = "No news in the last 30 days"


def _event(path, query=None, method="GET", body=None):
    ev = {"rawPath": path, "requestContext": {"http": {"method": method}}, "headers": {"x-firm-id": "opal"},
          "queryStringParameters": query}
    if body is not None:
        ev["body"] = json.dumps(body)
    return ev


def _sentences(node, out):
    """Every dict that looks like a served drafted sentence: it carries `text` and `verbatim_check`."""
    if isinstance(node, dict):
        if "verbatim_check" in node and "text" in node:
            out.append(node)
        for value in node.values():
            _sentences(value, out)
    elif isinstance(node, list):
        for value in node:
            _sentences(value, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC3"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    ap.add_argument("--names", type=int, default=0, help="limit the covered names read (0 = all)")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC3":
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "lib/research/api/tests/test_scoped_amgt_mount.py"], capture_output=True, timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 the mount test passes", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    from lib.research.api import scoped_amgt
    from lib.research.coverage.covered_universe import covered_security_keys

    if a.where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(event):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        def raw(event):
            return scoped_amgt.handler(event)

    def body(path, query=None, method="GET", payload=None):
        r = raw(_event(path, query, method, payload))
        try:
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
        except (ValueError, TypeError):
            return r.get("statusCode"), {}

    table = [" ".join(line.split()) for line in scoped_amgt.scoped_amgt_route_table()]
    code, _ = body(f"{PREFIX}/refresh", method="POST", payload={"security_key": "BA_US_Equity"})
    clause("C1 POST /refresh is gone", code == 404 and f"POST {PREFIX}/refresh" not in table,
           f"status {code}; listed {f'POST {PREFIX}/refresh' in table}")

    c1, b1 = body(f"{PREFIX}/resolve", {"q": "Lenovo"})
    c2, b2 = body(f"{PREFIX}/resolve", {"q": "992 HK"})
    cands = [c.get("security_key") for c in (b1.get("candidates") or [])]
    clause("C2 GET /resolve answers a name and an exact form",
           c1 == 200 and b1.get("status") == "candidates" and "992_HK_Equity" in cands and c2 == 200
           and b2.get("status") == "exact" and b2.get("security_key") == "992_HK_Equity"
           and f"GET {PREFIX}/resolve" in table, f"{c1} {b1.get('status')} {cands[:3]}; {c2} {b2.get('status')}")

    keys = sorted(covered_security_keys())
    if a.names:
        keys = keys[: a.names]
    today = datetime.datetime.now(datetime.timezone.utc).date()
    bare, bad_band, with_items, no_news, failed_reads, absent_band = [], [], 0, 0, 0, []
    for key in keys:
        _, ov = body(f"{PREFIX}/security/{key}/overlay")
        for axis in ("chatter", "price"):
            reason = ov.get(axis + "_absent_reason")
            if ov.get(axis) is None and not (isinstance(reason, str) and reason.strip()):
                bare.append((key, axis))
            if ov.get(axis) is not None and reason is not None:
                bare.append((key, axis + " present with a reason"))
        band = ov.get("top_band")
        if not isinstance(band, dict):
            absent_band.append(key)
            continue
        items = band.get("items") or []
        if items:
            with_items += 1
            try:
                age = (today - datetime.date.fromisoformat(str(band.get("day")))).days
            except ValueError:
                age = None
            if age is None or age < 0 or age > 30:
                bad_band.append((key, band.get("day")))
        elif band.get("items_reason") == NO_NEWS:
            no_news += 1
        elif isinstance(band.get("items_reason"), str) and "did not complete" in band.get("items_reason"):
            failed_reads += 1
        else:
            bad_band.append((key, band.get("items_reason")))
    print(f"   names {len(keys)}; bare axis nulls {len(bare)} e.g. {bare[:3]}")
    print(f"   top_band: absent {len(absent_band)}; with items {with_items}; no news in 30 days {no_news}; "
          f"failed reads {failed_reads}; bad {len(bad_band)} e.g. {bad_band[:3]}")
    clause("C3 an absent chatter or price axis carries its reason", keys and not bare, f"{len(bare)} bare")
    clause("C4 every top band shows the newest news day in 30 days or the plain reason",
           keys and not bad_band and not absent_band and not failed_reads, f"bad {len(bad_band)} failed {failed_reads}")

    served, missing = 0, 0
    for key in keys:
        _, th = body(f"{PREFIX}/security/{key}/thesis")
        found = []
        _sentences(th, found)
        for s in found:
            served += 1
            if not {"text_translated", "translated", "source_language"} <= set(s):
                missing += 1
    print(f"   drafted sentences served {served}; lacking the three translation keys {missing}")
    clause("C5 every served sentence carries the translation keys", served > 0 and missing == 0,
           f"{served - missing} of {served}")
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R77 BA11 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
