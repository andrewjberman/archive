#!/usr/bin/env python3
"""MDPF_CANON CN-p-1 -- the ONE-TIME publish of the Trend groups onto the as-of-2026-10-13 dated objects (ADDENDUM 1 of the pair).

Issuer's instrument (2.0.0_SA_COO~D1). It builds the replacement bodies and writes NOTHING to AWS: the only write path is the
CloudOps order's own put_object, after this script and the readback have both passed.

What it builds, for each of the four scopes: (a) the `aggregate-aua-timeseries` body = the EXISTING newest dated object plus exactly
the keys the merged CN-p-1 code adds (`client_supervised_aua`, `etf_strategies_aua`, `alt_strategies_aua`, `carried_dates`, and on
Global `meta.trend_groups`), computed by the code's own `apply_global_trend_groups` over the existing body; (b) the `category-views`
body = the EXISTING newest dated object minus the `muni` member of `SMA > ALT Strategies`. Nothing else in either body moves: the
script REFUSES (exit 1) if any other path differs, so the counts CN-h-1 and CN-l-1 move at the first scheduled fire are NOT moved here.

  python build_publish_bodies.py --from-s3 --out DIR         existing objects read from s3://opal-data-assets/portal/gold/mdpf (read-only)
  python build_publish_bodies.py --served DIR --out DIR      the same over local copies <scope>__aggregate-aua-timeseries.json / <scope>__category-views.json

Output in --out: <scope>__aggregate-aua-timeseries.json (+ .prior.json = the existing body, for the readback's R6),
<scope>__category-views.json, and PUBLISH_PLAN.json (per object: key, existing VersionId and sha256, new sha256). ASCII only.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys

SCOPES = ("global", "49financial", "inflection", "cottonwood")
BUCKET = "opal-data-assets"
PREFIX = "portal/gold/mdpf"
TYPES = ("aggregate-aua-timeseries", "category-views")
NEW_TOP = ("client_supervised_aua", "etf_strategies_aua", "alt_strategies_aua", "carried_dates")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def diff_paths(a, b, path=""):
    """Paths at which two JSON values differ (lists compared elementwise, dicts by key)."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append(("added", path + "/" + k))
            elif k not in b:
                out.append(("removed", path + "/" + k))
            else:
                out += diff_paths(a[k], b[k], path + "/" + k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(("length", path))
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                out += diff_paths(x, y, "%s[%d]" % (path, i))
    elif a != b:
        out.append(("changed", path))
    return out


def alt_members(cv):
    return (((cv or {}).get("nodes") or {}).get("SMA", {}).get("children", {}).get("ALT Strategies"))


def load(args):
    """Returns {scope: {type: (key, body_bytes, version_id)}} and the optional boto3 client."""
    out, s3 = {}, None
    if args["--from-s3"]:
        import boto3
        s3 = boto3.client("s3")
        for s in SCOPES:
            out[s] = {}
            for t in TYPES:
                ks = []
                for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="%s/%s/%s/" % (PREFIX, s, t)):
                    ks += [c["Key"] for c in pg.get("Contents", []) if c["Key"].endswith(".json")]
                key = sorted(ks)[-1]
                r = s3.get_object(Bucket=BUCKET, Key=key)
                out[s][t] = (key, r["Body"].read(), r.get("VersionId"))
    else:
        d = args["--served"]
        for s in SCOPES:
            out[s] = {}
            for t in TYPES:
                p = os.path.join(d, "%s__%s.json" % (s, t))
                out[s][t] = ("%s/%s/%s/LOCAL.json" % (PREFIX, s, t), open(p, "rb").read(), None)
    return out, s3


def main(argv):
    args = {a: (argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else True) for i, a in enumerate(argv) if a.startswith("--")}
    if "--out" not in args or not (args.get("--from-s3") or args.get("--served")):
        print(__doc__)
        return 2
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    for sub in ("", "data/mdpf/scripts/silver", "data/mdpf/scripts/gold"):
        sys.path.insert(0, os.path.join(root, sub) if sub else root)
    import boto3
    import mdpf_gold_consolidator as c

    existing, s3 = load(args)
    s3 = s3 or boto3.client("s3")
    import datetime as dt
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    legs, part = c.load_smartx_sma_legs(s3, today)
    if not legs:
        print("ERROR: no SMArtX partition read (legs empty); refusing to build")
        return 1
    out = args["--out"]
    os.makedirs(out, exist_ok=True)
    plan, bad = {}, []
    for s in SCOPES:
        key, raw, ver = existing[s]["aggregate-aua-timeseries"]
        doc = json.loads(raw)
        round_trip = c._canon_bytes(doc) == raw
        built = c.apply_global_trend_groups({("global" if s == "global" else s): doc}, legs, part)[("global" if s == "global" else s)]
        diffs = diff_paths(doc, built)
        allowed = {("added", "/" + k) for k in NEW_TOP}
        if s == "global":
            allowed |= {("added", "/meta/trend_groups")}
        extra = [d for d in diffs if d not in allowed]
        missing = sorted(allowed - set(diffs))
        if extra or missing:
            bad.append((s, "timeseries", "unexpected %s; missing %s" % (extra[:4], missing[:4])))
        body = c._canon_bytes(built)
        _, cvraw, cvver = existing[s]["category-views"]
        cvdoc = json.loads(cvraw)
        cvnew = copy.deepcopy(cvdoc)
        node = alt_members(cvnew)
        before = [m.get("member_id") for m in (node or {}).get("members", [])]
        if node is None or "muni" not in before:
            bad.append((s, "category-views", "no muni member to remove: %s" % before))
        else:
            node["members"] = [m for m in node["members"] if m.get("member_id") != "muni"]
        cvdiff = diff_paths(cvdoc, cvnew)
        if len(cvdiff) != 1 and not (cvdiff and all(d[1].startswith("/nodes/SMA/children/ALT Strategies/members") for d in cvdiff)):
            bad.append((s, "category-views", "unexpected diff %s" % cvdiff[:4]))
        cvkey = existing[s]["category-views"][0]
        cvbody = c._canon_bytes(cvnew)
        open(os.path.join(out, "%s__aggregate-aua-timeseries.json" % s), "wb").write(body)
        open(os.path.join(out, "%s__aggregate-aua-timeseries.prior.json" % s), "wb").write(raw)
        open(os.path.join(out, "%s__category-views.json" % s), "wb").write(cvbody)
        plan[s] = {
            "aggregate-aua-timeseries": {"key": key, "existing_version_id": ver, "existing_sha256": sha(raw), "new_sha256": sha(body),
                                         "new_bytes": len(body), "canon_round_trip_equal": round_trip},
            "category-views": {"key": cvkey, "existing_version_id": cvver, "existing_sha256": sha(cvraw), "new_sha256": sha(cvbody),
                               "new_bytes": len(cvbody), "members_before": before,
                               "canon_round_trip_equal": c._canon_bytes(cvdoc) == cvraw},
        }
        print("OK: %-12s ts +%s keys (round trip %s); cv members %s -> %s" % (
            s, sorted(NEW_TOP) if s != "global" else sorted(NEW_TOP) + ["meta.trend_groups"], round_trip, before, [m for m in before if m != "muni"]))
    json.dump({"smartx_partition": part, "smartx_dates": len(legs), "built_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "objects": plan}, open(os.path.join(out, "PUBLISH_PLAN.json"), "w"), indent=2, sort_keys=True)
    if bad:
        print("REFUSED: %d violation(s): %s" % (len(bad), bad))
        return 1
    print("BUILT: 8 bodies in %s (4 timeseries, 4 category-views); PUBLISH_PLAN.json written; nothing written to AWS" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
