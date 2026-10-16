#!/usr/bin/env python3
"""MDPF_CANON round 11 -- the issuer's D4 diff for the CN-s-1 pair (hard STOP, CTO half condition 1).

  python diff_d4.py --response <d4_response.json> --baseline <dir of <scope>__<type>.json> [--since 2026-10-07]

Reads the qa_return_bodies response of the dry-run invoke (bodies keyed by A4 key, each {"body": <utf-8 JSON>, "sha256"}) and
the baseline objects the CloudOps order saved, and diffs each scope/type leaf by leaf. The new body is dated one day after
the baseline, so a top-level array longer by the appended dates is compared on the shared prefix and the appended tail is
reported separately. Prints COUNTS, DATES and key paths only: never a value. Output ends with `D4 DIFF: <k> leaf(s) before
--since, <m> outside the allowed scopes` and exit 0 only when k == 0 (nothing moved before 2026-10-07) and the objects read
are the 16 expected; the allowed-set judgment (which paths may move, per the pair's section 1) is the issuer's reading of the
printed list, never this script's. ASCII only.
"""
import argparse
import json
import os
import sys

SCOPES = ("global", "49financial", "inflection", "cottonwood")
TYPES = ("account-distribution", "aggregate-aua-timeseries", "aum-metrics", "category-views")


def parse_key(k):
    parts = k.split("/")
    # .../gold/mdpf/<scope>/<type>/<date>.json
    for i, p in enumerate(parts):
        if p in SCOPES and i + 1 < len(parts) and parts[i + 1] in TYPES:
            return p, parts[i + 1], parts[-1].replace(".json", "")
    return None, None, None


def walk(a, b, path, dates_a, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a:
                out.append((path + "/" + str(k), "ADDED", None))
            elif k not in b:
                out.append((path + "/" + str(k), "REMOVED", None))
            else:
                walk(a[k], b[k], path + "/" + str(k), dates_a, out)
    elif isinstance(a, list) and isinstance(b, list):
        n = min(len(a), len(b))
        idx = [i for i in range(n) if json.dumps(a[i], sort_keys=True, default=str) != json.dumps(b[i], sort_keys=True, default=str)]
        tail = len(b) - len(a)
        if idx:
            out.append((path, "CELLS", (idx, n)))
        if tail != 0:
            out.append((path, "TAIL", tail))
    elif a != b:
        out.append((path, "VALUE", None))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--response", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--since", default="2026-10-07")
    args = ap.parse_args()
    resp = json.load(open(args.response, encoding="utf-8"))
    bodies = resp.get("bodies") or {}
    print("status=%s errors=%s a4_objects_built=%s bodies=%d" % (resp.get("status"), resp.get("errors"), resp.get("a4_objects_built"), len(bodies)))
    seen = set()
    before_since = 0
    for key in sorted(bodies):
        scope, typ, day = parse_key(key)
        if scope is None:
            print("  UNPARSED KEY", key)
            continue
        seen.add((scope, typ))
        bp = os.path.join(args.baseline, "%s__%s.json" % (scope, typ))
        if not os.path.exists(bp):
            print("  %s/%s: no baseline file" % (scope, typ))
            continue
        new = json.loads(bodies[key]["body"])
        old = json.load(open(bp, encoding="utf-8"))
        diffs = []
        walk(old, new, "", old.get("dates"), diffs)
        # dates for cell indexes come from the OLD object's own axis where the array is aligned to it
        axis = old.get("dates") or []
        print("  %s/%s (new dated %s): %d path difference(s)" % (scope, typ, day, len(diffs)))
        for p, kind, det in diffs:
            if kind == "CELLS":
                idx, n = det
                ds = [axis[i] for i in idx if i < len(axis)] if len(axis) >= n else []
                note = ""
                if ds:
                    note = " dates %s .. %s" % (ds[0], ds[-1])
                    if ds[0] < args.since:
                        before_since += 1
                        note += "  <-- BEFORE %s" % args.since
                print("     %s CELLS %d%s" % (p, len(idx), note))
            elif kind == "TAIL":
                print("     %s TAIL %+d" % (p, det))
            else:
                print("     %s %s" % (p, kind))
    missing = [(s, t) for s in SCOPES for t in TYPES if (s, t) not in seen]
    print("expected 16 scope/type pairs; seen %d; missing %s" % (len(seen), missing))
    print("D4 DIFF: %d leaf(s) moved before %s; missing pairs %d" % (before_since, args.since, len(missing)))
    return 0 if (before_since == 0 and not missing) else 1


if __name__ == "__main__":
    sys.exit(main())
