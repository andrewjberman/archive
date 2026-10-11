"""AMGT_RESAPP round-95 PREP -- the table of the rank timeseries asked for EVERY measured subject's ticker (not only the tickers a ranked list holds).

  PYTHONPATH=<repo root> python r95_series_by_ticker_table.py <out.json> [--after deployed|local]

`r94_rankings_table.py` asks the timeseries for the tickers each ranked list holds, so a measured subject outside every list (CSL_AU_Equity) is never read. This reads, for each of
the four movement x subject combinations, the series of EVERY MEASURED crosswalk subject's Bloomberg ticker (one request per combination, `tickers=` the whole list): BEFORE is
the LIVE function, AFTER is the checkout's own handler (`--after local`, the default) or the live function again (`--after deployed`). Every JSON path that differs is listed
with its before and after; time-varying paths are counted apart. Read-only; writes only <out.json>.
"""
import collections
import json
import re
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
NOISE = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency)", re.I)
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(movement, subject, tickers):
    return {"rawPath": "%s/lead-panel/timeseries/%s/%s" % (scoped_amgt.ROUTE_PREFIX, movement, subject),
            "queryStringParameters": {"tickers": ",".join(tickers)}, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(movement, subject, tickers):
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event(movement, subject, tickers)).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def local(movement, subject, tickers):
    r = scoped_amgt.handler(event(movement, subject, tickers))
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


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


def main():
    out_path = sys.argv[1]
    after_fn = live if (sys.argv[sys.argv.index("--after") + 1] if "--after" in sys.argv else "local") == "deployed" else local
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    pairs = []
    for k in keys:
        t = (scoped_amgt.resolve_identity(k) or {}).get("bloomberg")
        if t:
            pairs.append((k, t))
    tickers = [t for _k, t in pairs]
    key_of = {t: k for k, t in pairs}
    diffs, statuses = [], {}
    for movement in scoped_amgt.MOVEMENTS:
        for subject in scoped_amgt.SUBJECTS:
            (sb, b), (sa, a) = live(movement, subject, tickers), after_fn(movement, subject, tickers)
            statuses["%s/%s" % (movement, subject)] = (sb, sa, len(b.get("series") or []), len(a.get("series") or []))
            for path, before, after in walk(b, a):
                m = re.match(r"\.series\[(\d+)\]", path)
                ticker = ((b.get("series") or [{}] * 999)[int(m.group(1))].get("ticker") if m and int(m.group(1)) < len(b.get("series") or []) else None)
                diffs.append({"combo": "%s/%s" % (movement, subject), "ticker": ticker, "subject": key_of.get(ticker), "path": path,
                              "before": before, "after": after, "noise": bool(NOISE.search(path))})
    json.dump({"statuses": statuses, "diffs": diffs}, open(out_path, "w"), default=str)
    print("tickers asked %d | combos %d | statuses (live, after, series before, series after): %s" % (len(tickers), len(statuses), json.dumps(statuses)))
    real = [d for d in diffs if not d["noise"]]
    print("changed paths %d (noise %d)" % (len(real), len(diffs) - len(real)))
    pat = collections.Counter(re.sub(r"\[\d+\]", "[]", d["path"]) for d in real)
    for p, n in sorted(pat.items(), key=lambda kv: -kv[1]):
        print("  %-48s %4d" % (p[:48], n))
    for d in real[:30]:
        print("   %-16s %-14s %s: %r -> %r" % (d["subject"], d["combo"], d["path"][:44], str(d["before"])[:44], str(d["after"])[:44]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
