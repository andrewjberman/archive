"""AMGT_RESAPP round-98 PREP -- the WHOLE-BODY table of the /thesis route for the /13 redeploy (`AMGT-be-1`): every JSON path of every name's response that moves.

  PYTHONPATH=<repo root> python r98_thesis_fullbody_compare.py <out.json> [--after local|deployed]

`aw4_compare.py` grades only the fields `aw4_capture.py` keeps (team_sheet, fiscal_year_figures, header_figures, check_face, ...). This reads the WHOLE body: BEFORE is the LIVE
function's `/thesis` response for each resolved name (95), AFTER is the checkout's own handler on the same live pool (`--after local`, the pin's tree: the code the redeploy would
carry) or the live function again (`--after deployed`: the compare after the apply). Every JSON path that differs is classified:
  team_sheet   under `model.team_sheet` (AMGT_CORPUS leg p: the served /13 field)
  float_repr   the two values are numbers (or numeric strings) equal to 1e-9 relative: the live runtime (python3.11, builtin `sum` uncompensated) and a python3.12+ checkout print
               a sum's last digit differently; named WHOLE, never hidden
  clock        a read clock or generation stamp (`read_at`, `generated_at`, ...)
  other        anything else: Branch C of the AMGT_CORPUS aw-4 half and of the AMGT_RESAPP pair
Prints one line per class with its path-pattern counts and every `other` and `float_repr` path whole, then a verdict `R98 THESIS FULLBODY: YES|NO` (YES = zero `other` paths and every name
status 200 before and after). Read-only; writes only <out.json>. The output holds client research content: it stays local and uncommitted.
"""
import collections
import concurrent.futures
import json
import re
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.corpus import dossier
from lib.research.harvest import store

FN = "opal-amgt-scoped-api"
CLOCK = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency|as_of_read)", re.I)
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(key):
    return {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}},
            "headers": {"x-firm-id": "opal"}}


def live(key):
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event(key)).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def local(key):
    r = scoped_amgt.handler(event(key))
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


def same_number(a, b):
    try:
        x, y = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y))


def one(key, after_fn):
    (sb, b), (sa, a) = live(key), after_fn(key)
    out = []
    for p, before, after in walk(b, a):
        if p.startswith(".model.team_sheet"):
            kind = "team_sheet"
        elif CLOCK.search(p):
            kind = "clock"
        elif same_number(before, after):
            kind = "float_repr"
        else:
            kind = "other"
        out.append({"key": key, "path": p, "before": before, "after": after, "kind": kind})
    return key, sb, sa, out


def main():
    out_path = sys.argv[1]
    after_fn = live if (sys.argv[sys.argv.index("--after") + 1] if "--after" in sys.argv else "local") == "deployed" else local
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    statuses, diffs, failed = {}, [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for fut in concurrent.futures.as_completed([pool.submit(one, k, after_fn) for k in keys]):
            try:
                key, sb, sa, d = fut.result()
                statuses[key] = (sb, sa)
                diffs.extend(d)
            except Exception as exc:  # a failed read is counted and named, never dropped
                failed.append("%s: %s" % (type(exc).__name__, str(exc)[:100]))
    json.dump({"statuses": statuses, "diffs": diffs, "failed": failed}, open(out_path, "w", encoding="utf-8"), default=str)
    bad = {k: v for k, v in statuses.items() if v != (200, 200)}
    print("names %d | read %d | failed %d | status not (200, 200): %d %s" % (len(keys), len(statuses), len(failed), len(bad), sorted(bad)[:6]))
    by = collections.Counter(d["kind"] for d in diffs)
    print("changed paths %d: %s" % (len(diffs), dict(by)))
    pat = collections.Counter((d["kind"], re.sub(r"\[\d+\]", "[]", d["path"])) for d in diffs if d["kind"] in ("team_sheet", "clock"))
    for (kind, p), n in sorted(pat.items(), key=lambda kv: -kv[1])[:12]:
        print("  %-10s %-70s %5d" % (kind, p[:70], n))
    for d in diffs:
        if d["kind"] in ("float_repr", "other"):
            print("  %-10s %-18s %s: %r -> %r" % (d["kind"].upper(), d["key"], d["path"][:80], str(d["before"])[:40], str(d["after"])[:40]))
    ok = not failed and not bad and by.get("other", 0) == 0 and len(statuses) == len(keys)
    print("R98 THESIS FULLBODY: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
