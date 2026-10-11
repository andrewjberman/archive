"""AMGT_RESAPP round-94 PREP -- the table of the name redeploy (`AMGT-ff-4`) over the OTHER routes that read a name: the per-security `timeline` (its word cloud
drops the security's own name words, `_word_cloud_own_words`), the per-security `thesis`, and the collected-chatter list (`monthly_chatter.read_monthly_chatter`,
which names its rows through the shared chain).

  PYTHONPATH=<repo root> python r94_other_routes_table.py <out.json> [--after deployed|local]

BEFORE is the LIVE function's response; AFTER is the checkout's own handler on the same live pool (`--after local`, the default) or the live function again
(`--after deployed`: the compare after the apply); numbers equal to 1e-9 are equal (the runtimes print a float's last digit differently). Subjects: the two whose names move (SAN_FP_Equity, CSL_AU_Equity) and ten controls. Every JSON path that
differs is listed with its before and after; paths under `model.team_sheet` and `model_rows` are AMGT_CORPUS leg p's (METHOD /12) and are counted apart as
CORPUS; time-varying paths are counted apart as NOISE. Read-only; writes only <out.json>.
"""
import collections
import json
import re
import sys

import boto3

from lib.research.api import scoped_amgt

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
MOVERS = ("SAN_FP_Equity", "CSL_AU_Equity")
CONTROLS = ("ASML_NA_Equity", "SAP_GY_Equity", "BA_US_Equity", "ROG_SW_Equity", "TSM_US_Equity", "IMB_LN_Equity", "BABA_US_Equity", "AZN_LN_Equity",
            "GSK_LN_Equity", "NVO_US_Equity")
NOISE = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency|as_of_read)", re.I)
CORPUS = re.compile(r"(team_sheet|model_rows|dossier_fields|method_version)", re.I)
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(path, query=None):
    return {"rawPath": PREFIX + path, "queryStringParameters": query, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(path, query=None):
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event(path, query)).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def local(path, query=None):
    r = scoped_amgt.handler(event(path, query))
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
    elif a != b and not _same_number(a, b):
        yield path, a, b


def _same_number(a, b):
    """The live runtime and the checkout print a float's last digit differently (a string `z_score` '-0.3885143449429056' vs '-0.38851434494290565'): equal to 1e-9."""
    try:
        x, y = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y))


def main():
    out_path = sys.argv[1]
    after_fn = live if (sys.argv[sys.argv.index("--after") + 1] if "--after" in sys.argv else "local") == "deployed" else local
    reads = []
    for key in MOVERS + CONTROLS:
        reads.append(("timeline", key, "/security/%s/timeline" % key, None))
        reads.append(("thesis", key, "/security/%s/thesis" % key, None))
    for days in ("30", "90", "365"):
        reads.append(("collected", "days=%s" % days, "/lead-panel/timeseries/collected/chatter", {"days": days}))
    diffs, statuses = [], {}
    for route, subject, path, query in reads:
        (sb, b), (sa, a) = live(path, query), after_fn(path, query)
        statuses["%s %s" % (route, subject)] = (sb, sa)
        for p, before, after in walk(b, a):
            kind = "noise" if NOISE.search(p) else ("corpus" if CORPUS.search(p) else "name")
            diffs.append({"route": route, "subject": subject, "path": p, "before": before, "after": after, "kind": kind})
    json.dump({"statuses": statuses, "diffs": diffs}, open(out_path, "w"), default=str)
    print("reads %d | statuses %s | changed paths %d" % (len(reads), json.dumps(sorted(set(str(v) for v in statuses.values()))), len(diffs)))
    by = collections.Counter((d["route"], d["kind"]) for d in diffs)
    for (route, kind), n in sorted(by.items()):
        print("  %-10s %-7s %5d path(s)" % (route, kind, n))
    names = [d for d in diffs if d["kind"] == "name"]
    pattern = collections.Counter((d["route"], re.sub(r"\[\d+\]", "[]", d["path"])) for d in names)
    subjects = collections.defaultdict(set)
    for d in names:
        subjects[(d["route"], re.sub(r"\[\d+\]", "[]", d["path"]))].add(d["subject"])
    for (route, pat), n in sorted(pattern.items(), key=lambda kv: -kv[1])[:40]:
        print("  NAME %-9s %-64s %4d on %s" % (route, pat[:64], n, ",".join(sorted(subjects[(route, pat)]))[:60]))
    for d in names[:30]:
        print("   %-10s %-16s %s: %r -> %r" % (d["route"], d["subject"], d["path"][:70], str(d["before"])[:50], str(d["after"])[:50]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
