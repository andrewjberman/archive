"""AMGT_RESAPP round-94 PREP -- the table of the name redeploy (`AMGT-ff-4`) over the RANKED lists: every field of each `/lead-panel/rankings/{movement}/{subject}`
response that moves, the live function against the checkout's own handler on the same live pool.

  PYTHONPATH=<repo root> python r94_rankings_table.py <out.json> [--after deployed|local]

The ranked lists are keyed by movement x subject (`scoped_amgt.MOVEMENTS` x `scoped_amgt.SUBJECTS`), not by security, so `r94_name_table.py` (overlay and peers per
subject) does not read them; a ranked row's `name` is the third place the classifications table's name is served (AMGT-ff-1 amendment 1). Every JSON path that
differs is listed with its before and after; paths are summarised by pattern (list indexes replaced by `[]`) with a count; time-varying paths are counted apart.
Read-only; writes only <out.json>.
"""
import collections
import json
import re
import sys

import boto3

from lib.research.api import scoped_amgt

FN = "opal-amgt-scoped-api"
NOISE = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency)", re.I)
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(movement, subject):
    return {"rawPath": "%s/lead-panel/rankings/%s/%s" % (scoped_amgt.ROUTE_PREFIX, movement, subject), "queryStringParameters": None,
            "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(movement, subject):
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event(movement, subject)).encode())["Payload"].read())
    return json.loads(r.get("body") or "{}")


def local(movement, subject):
    r = scoped_amgt.handler(event(movement, subject))
    return json.loads(r.get("body") or "{}")


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
    diffs = []
    served = {}
    for movement in scoped_amgt.MOVEMENTS:
        for subject in scoped_amgt.SUBJECTS:
            b, a = live(movement, subject), after_fn(movement, subject)
            combo = "%s/%s" % (movement, subject)
            served[combo] = {"rows_before": len(b.get("rows") or []), "rows_after": len(a.get("rows") or []),
                             "status_before": b.get("ranking_status"), "status_after": a.get("ranking_status")}
            for path, before, after in walk(b, a):
                diffs.append({"combo": combo, "path": path, "before": before, "after": after, "noise": bool(NOISE.search(path))})
    pattern = collections.Counter()
    combos = collections.defaultdict(set)
    noise = collections.Counter()
    for d in diffs:
        pat = re.sub(r"\[\d+\]", "[]", d["path"])
        if d["noise"]:
            noise[pat] += 1
        else:
            pattern[pat] += 1
            combos[pat].add(d["combo"])
    json.dump({"combos": served, "diffs": diffs}, open(out_path, "w"), default=str)
    print("combos %d | changed paths %d (of which noise %d)" % (len(served), len(diffs) - sum(noise.values()), sum(noise.values())))
    for combo, s in sorted(served.items()):
        print("  %-24s rows %4d -> %4d | status %s -> %s" % (combo, s["rows_before"], s["rows_after"], s["status_before"], s["status_after"]))
    for pat, n in sorted(pattern.items(), key=lambda kv: -kv[1]):
        print("  %-64s %4d change(s) on %d combo(s)" % (pat[:64], n, len(combos[pat])))
    for pat, n in sorted(noise.items()):
        print("  NOISE %-56s %4d" % (pat[:56], n))
    shown = {}
    for d in diffs:
        if not d["noise"]:
            shown.setdefault((d["combo"], d["path"]), d)
    for (combo, path), d in list(shown.items())[:40]:
        print("   %-22s %s: %r -> %r" % (combo, path[:60], str(d["before"])[:40], str(d["after"])[:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
