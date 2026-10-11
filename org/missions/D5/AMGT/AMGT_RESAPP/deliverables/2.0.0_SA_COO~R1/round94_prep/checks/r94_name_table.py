"""AMGT_RESAPP round-94 PREP -- the subject-by-subject table of the name redeploy (`AMGT-ff-4`): every field of the overlay and peers routes that moves.

  PYTHONPATH=<repo root> python r94_name_table.py <out.json> [--limit N] [--after deployed|local]

BEFORE is the LIVE function's `/overlay` and `/peers` response for each of the 243 MEASURED subjects (Lambda invoke, GET only). AFTER is the checkout's own
handler on the same live pool (`--after local`, the default: the code the redeploy would carry) or the live function again (`--after deployed`: the compare
after the apply). Every JSON path that differs is listed with its before and after; paths are summarised by pattern (list indexes replaced by `[]`) with a
count. Routes carry time-varying fields (a read clock, a feed window); those paths are named in NOISE and counted apart, never hidden.
Read-only; writes only <out.json>.
"""
import collections
import json
import re
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
ROUTES = ("overlay", "peers")
NOISE = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency)", re.I)
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(key, route):
    return {"rawPath": "%s/security/%s/%s" % (PREFIX, key, route), "queryStringParameters": None,
            "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(key, route):
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event(key, route)).encode())["Payload"].read())
    return json.loads(r.get("body") or "{}")


def local(key, route):
    r = scoped_amgt.handler(event(key, route))
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
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    after_fn = live if (sys.argv[sys.argv.index("--after") + 1] if "--after" in sys.argv else "local") == "deployed" else local
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    if limit:
        keys = keys[:limit]
    diffs = []
    for key in keys:
        for route in ROUTES:
            b, a = live(key, route), after_fn(key, route)
            for path, before, after in walk(b, a):
                diffs.append({"subject": key, "route": route, "path": path, "before": before, "after": after,
                              "noise": bool(NOISE.search(path))})
    pattern = collections.Counter()
    subjects = collections.defaultdict(set)
    noise = collections.Counter()
    for d in diffs:
        pat = re.sub(r"\[\d+\]", "[]", d["path"])
        if d["noise"]:
            noise[(d["route"], pat)] += 1
        else:
            pattern[(d["route"], pat)] += 1
            subjects[(d["route"], pat)].add(d["subject"])
    json.dump({"subjects": len(keys), "diffs": diffs}, open(out_path, "w"), default=str)
    print("subjects %d | routes %s | changed paths %d (of which noise %d)" % (len(keys), ",".join(ROUTES), len(diffs) - sum(noise.values()), sum(noise.values())))
    for (route, pat), n in sorted(pattern.items(), key=lambda kv: -kv[1]):
        print("  %-8s %-60s %4d change(s) on %3d subject(s)" % (route, pat[:60], n, len(subjects[(route, pat)])))
    for (route, pat), n in sorted(noise.items()):
        print("  NOISE %-8s %-52s %4d" % (route, pat[:52], n))
    shown = {}
    for d in diffs:
        if not d["noise"]:
            shown.setdefault((d["subject"], d["path"]), d)
    for (subject, path), d in list(shown.items())[:40]:
        print("   %-18s %-8s %s: %r -> %r" % (subject, d["route"], path[:60], str(d["before"])[:40], str(d["after"])[:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
