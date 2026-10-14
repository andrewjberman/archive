"""AMGT_RESAPP round-106 PREP -- the forward P/E population: for every resolved name, each served BEST_PE_RATIO forecast row, the price currency (the header PX_LAST) and the BEST_EPS currency of the same period.

  PYTHONPATH=<repo root> python r106_forward_pe_population.py <out.json> [--workers 4]

Reads the LIVE function (GET, /thesis, Lambda invoke). Prints `names N | forward P/E rows R | price and EPS in the same currency S | minor-unit pair M | different currency D | EPS or price currency absent A` and the first different-currency names.
Writes nothing but <out.json>. A currency pair is `(price currency, eps currency)`; the minor-unit pairs are those `lib/research/api/case_rule.is_minor_unit_quote` names (GBp over GBP).
"""
import concurrent.futures
import json
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_LAM = boto3.client("lambda", region_name="us-east-1")


def body(key):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(_LAM.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(ev).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def one(key):
    st, b = body(key)
    m = b.get("model") or {}
    px = next((h.get("currency") for h in b.get("header_figures", []) if h.get("mnemonic") == "PX_LAST"), None)
    rows = []
    eps = {(f.get("fiscal_year"), f.get("fiscal_period")): f for f in m.get("forecast_figures", []) if f.get("mnemonic") == "BEST_EPS"}
    for f in m.get("forecast_figures", []):
        if f.get("mnemonic") != "BEST_PE_RATIO":
            continue
        e = eps.get((f.get("fiscal_year"), f.get("fiscal_period")))
        rows.append({"fiscal_year": f.get("fiscal_year"), "value": f.get("value"), "price_currency": px, "eps_currency": (e or {}).get("currency"), "eps_value": (e or {}).get("value")})
    return {"key": key, "status": st, "rows": rows}


def main():
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for r in pool.map(one, keys):
            res.append(r)
    json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), default=str)
    same = minor = diff = absent = total = 0
    diff_names = {}
    for r in res:
        for row in r["rows"]:
            total += 1
            p, e = row["price_currency"], row["eps_currency"]
            if not p or not e:
                absent += 1
            elif p == e:
                same += 1
            elif p.upper() == e.upper():
                minor += 1
            else:
                diff += 1
                diff_names.setdefault(r["key"], set()).add((p, e))
    print("names %d | forward P/E rows %d | same currency %d | minor-unit pair %d | different currency %d | currency absent %d" % (len(res), total, same, minor, diff, absent))
    for k, v in sorted(diff_names.items())[:30]:
        print("  DIFFERENT %-22s %s" % (k, sorted(v)))
    print("names with a different-currency forward P/E: %d" % len(diff_names))


if __name__ == "__main__":
    main()
