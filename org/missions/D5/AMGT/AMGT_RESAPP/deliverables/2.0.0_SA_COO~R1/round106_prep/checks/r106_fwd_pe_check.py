"""AMGT_RESAPP round-106 PREP -- `AMGT-bm-2`: a served forward P/E whose price and EPS are in DIFFERENT currencies is withheld with a stated reason.

  PYTHONPATH=<checkout root> python r106_fwd_pe_check.py <population.json> [--workers 4]

`population.json` is `round106_prep/forward_pe_population.json` (r106_forward_pe_population.py over the live function): per name, each served BEST_PE_RATIO forecast row with the price currency (header PX_LAST) and the BEST_EPS currency
of the same period. For every resolved name this reads the LIVE function's /thesis body (the base) and the checkout's own handler on the same pool (the candidate) and checks, over the model block's forecast figures:
  F1  the candidate serves exactly the base's BEST_PE_RATIO rows MINUS the rows whose price and EPS currencies differ (a minor unit of the same currency, GBp over GBP, stays: it is the same currency);
  F2  every row it keeps is EQUAL to the base's row (value, currency, basis, every key);
  F3  every withheld row has an entry in `model.forecast_withheld` of the candidate: `{mnemonic: BEST_PE_RATIO, fiscal_year, fiscal_period, reason}` whose reason names BOTH currency codes;
  F4  PBR US (the arm: USD price, BRL EPS) withholds its forward rows and its reason names `USD` and `BRL`;
  F5  with the BEST_PE_RATIO forecast rows, the `model.forecast_withheld` key, the `ai_fill` block (`~R2`'s workstream: the live function runs with `AMGT_AIFILL_ROOT=/var/empty/aifill-hold` since 2026-10-14 05:10Z and its `as_of` and `reason` are environment-dependent) and the check-face rows of those figures set aside on both sides, the two bodies differ only in float representation and request clocks (0 other paths);
  F6  the count of withheld rows equals the population's different-currency count (a number printed beside the denominator).
Prints `names N | base forward P/E rows B | candidate C | withheld W (population D) | names with a withheld row K` and `R106 FORWARD PE CHECK: YES|NO (n of 6 arms)` with one PASS/FAIL line per arm. Writes nothing.
"""
import concurrent.futures
import contextlib
import io
import json
import re
import sys

import os

import boto3

os.environ.setdefault("AMGT_AIFILL_ROOT", "/var/empty/aifill-hold")  # as the live function (the AI-fill hold); the block itself is set aside in F5
sys.path.insert(0, ".")
from lib.research.api import scoped_amgt as m  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

CLOCK = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency|as_of_read)", re.I)
_LAM = boto3.client("lambda", region_name="us-east-1")
MN = "BEST_PE_RATIO"


def event(key):
    return {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(key):
    r = json.loads(_LAM.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event(key)).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def local(key):
    with contextlib.redirect_stdout(io.StringIO()):
        r = m.handler(event(key))
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def rid(f):
    return (str(f.get("fiscal_year")), str(f.get("fiscal_period")))


def pe_rows(body):
    return {rid(f): f for f in (body.get("model") or {}).get("forecast_figures", []) if f.get("mnemonic") == MN}


def set_aside(node, counts):
    """Remove BEST_PE_RATIO forecast rows, `forecast_withheld` and the check-face rows of BEST_PE_RATIO at every depth."""
    if isinstance(node, dict):
        return {k: set_aside(v, counts) for k, v in node.items() if k not in ("forecast_withheld", "ai_fill")}
    if isinstance(node, list):
        out = []
        for item in node:
            if isinstance(item, dict) and item.get("mnemonic") == MN:
                counts["rows"] += 1
                continue
            if isinstance(item, dict) and MN in str(item.get("figure_id", "")):
                counts["check"] += 1
                continue
            out.append(set_aside(item, counts))
        return out
    return node


def walk(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            yield from walk(a.get(k, "<absent>"), b.get(k, "<absent>"), "%s.%s" % (path, k))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            yield path + ".<length>", len(a), len(b)
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, "%s[%d]" % (path, i))
    elif a != b:
        yield path, a, b


def same_number(a, b):
    try:
        x, y = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y))


def one(key):
    (sb, b), (sa, a) = live(key), local(key)
    rb, ra = pe_rows(b), pe_rows(a)
    unresolved = [u for u in ((a.get("model") or {}).get("forecast_withheld") or []) if u.get("mnemonic") == MN]
    nb, na = set_aside(b, {"rows": 0, "check": 0}), set_aside(a, {"rows": 0, "check": 0})
    other = [(p, x, y) for p, x, y in walk(nb, na) if not (CLOCK.search(p) or same_number(x, y))]
    return {"key": key, "status": (sb, sa), "base": rb, "cand": ra, "unresolved": unresolved, "other": other}


def main():
    pop = json.load(open(sys.argv[1], encoding="utf-8"))
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    expected = {}
    for r in pop:
        for row in r["rows"]:
            p, e = (row.get("price_currency") or ""), (row.get("eps_currency") or "")
            if p and e and p.upper() != e.upper():
                expected[(r["key"], str(row["fiscal_year"]))] = (p, e)
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    res = []
    real_stdout = sys.stdout
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for r in pool.map(one, keys):
            res.append(r)
    sys.stdout = real_stdout  # redirect_stdout across threads can leave stdout swapped
    f1 = f2 = f3 = True
    f5 = True
    withheld = 0
    names_w = set()
    base_n = cand_n = 0
    for r in res:
        base_n += len(r["base"])
        cand_n += len(r["cand"])
        want = {k: v for k, v in r["base"].items() if (r["key"], k[0]) in expected}
        keep = {k for k in r["base"] if k not in want}
        if set(r["cand"]) != keep:
            f1 = False
            print("  F1 %s: candidate rows %s vs expected %s" % (r["key"], sorted(r["cand"])[:4], sorted(keep)[:4]))
        for k in keep:
            if r["cand"].get(k) != r["base"][k]:
                f2 = False
                print("  F2 %s %s differs" % (r["key"], k))
        for k in want:
            withheld += 1
            names_w.add(r["key"])
            p, e = expected[(r["key"], k[0])]
            hit = [u for u in r["unresolved"] if str(u.get("fiscal_year")) == k[0] and p in str(u.get("reason")) and e in str(u.get("reason"))]
            if not hit:
                f3 = False
                print("  F3 %s %s: no forecast_withheld entry naming %s and %s" % (r["key"], k, p, e))
        if r["other"]:
            f5 = False
            print("  F5 %s %s" % (r["key"], r["other"][0][0][:80]))
    pbr = next((r for r in res if r["key"] == "PBR_US_Equity"), None)
    f4 = bool(pbr and not pbr["cand"] and pbr["unresolved"] and all("USD" in str(u.get("reason")) and "BRL" in str(u.get("reason")) for u in pbr["unresolved"]))
    f6 = withheld == len(expected)
    bad = [r["key"] for r in res if r["status"] != (200, 200)]
    print("names %d | base forward P/E rows %d | candidate %d | withheld %d (population %d) | names with a withheld row %d | status not (200, 200): %s" % (len(res), base_n, cand_n, withheld, len(expected), len(names_w), bad[:4]))
    arms = [("F1 candidate rows = base rows minus the different-currency rows", f1), ("F2 kept rows equal the base's", f2), ("F3 every withheld row has a reason naming both currencies", f3),
            ("F4 PBR US withholds with a reason naming USD and BRL", f4), ("F5 no other path differs (floats and clocks only)", f5), ("F6 withheld count equals the population", f6)]
    for name, ok in arms:
        print("   %s %s" % ("PASS" if ok else "FAIL", name))
    ok = all(x for _, x in arms) and not bad
    print("R106 FORWARD PE CHECK: %s (%d of 6 arms)" % ("YES" if ok else "NO", sum(1 for _, x in arms if x)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
