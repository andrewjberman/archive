"""MDPF_TAXSMA TX-r-1 leg V2 -- the served plane before and after the first scheduled publisher run on the new code.

    py -3.12 tx_r_1_served_delta.py baseline <out.json>     # capture (run before the 13:50Z fire)
    py -3.12 tx_r_1_served_delta.py compare  <baseline.json> # compare (run after it)

Read-only. Stores SHAPES and HASHES, never values. A scheduled run legitimately moves the frontier (a new
as-of day), so the comparison is: (1) the key-path SHAPE of every served document is unchanged (no Tax field
appeared), (2) every history value at a date the baseline already carried is unchanged, (3) the Tax member is
still served with a null amount, (4) the publisher wrote a fresh manifest on the new code.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sys

import boto3

BUCKET = "opal-data-portal-v2"
ROOT = "platinum/mdpf"
SCOPES = ("49financial", "cottonwood", "global", "inflection")
TYPES = ("aggregate-aua-timeseries", "aum-metrics", "account-distribution", "category-views")
TIME_KEYS = {"generated_at", "process_time", "last_updated", "source_vintage_age_hours", "built_at", "as_of",
             "frontier_date", "run_id"}


def shape(o, path="", out=None):
    """The set of key paths, with list indices collapsed -- a document's structure without its values."""
    out = set() if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            shape(v, path + "/" + str(k), out)
    elif isinstance(o, list):
        for v in o:
            shape(v, path + "[]", out)
    else:
        out.add(path)
    return out


def history_hashes(doc):
    """date -> sha256 of every date-aligned series value at that date (aggregate timeseries only)."""
    dates = doc.get("dates")
    if not isinstance(dates, list):
        return {}
    cols = {}

    def collect(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                collect(v, path + "/" + str(k))
        elif isinstance(o, list) and len(o) == len(dates) and path != "/dates":
            cols[path] = o

    collect(doc)
    return {d: hashlib.sha256(json.dumps([(p, cols[p][i]) for p in sorted(cols)], sort_keys=True,
                                         default=str).encode()).hexdigest() for i, d in enumerate(dates)}


def tax_member(doc):
    try:
        for m in doc["nodes"]["SMA"]["children"]["ALT Strategies"]["members"]:
            if m.get("member_id") == "tax":
                return {"present": True, "aum_is_null": m.get("aum") is None, "keys": sorted(m)}
    except (KeyError, TypeError):
        pass
    return {"present": False}


def capture():
    s3 = boto3.client("s3", region_name="us-east-1")
    out = {"captured_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "docs": {}}
    for scope in SCOPES:
        for typ in TYPES:
            key = "%s/%s/%s.json" % (ROOT, scope, typ)
            try:
                o = s3.get_object(Bucket=BUCKET, Key=key)
            except Exception as e:  # noqa: BLE001 -- an absent key is a recorded result
                out["docs"][key] = {"error": type(e).__name__}
                continue
            doc = json.loads(o["Body"].read())
            sh = sorted(shape(doc))
            rec = {"last_modified": o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "shape_paths": len(sh), "shape_sha256": hashlib.sha256("\n".join(sh).encode()).hexdigest(),
                   "tax_named_paths": [p for p in sh if "tax" in p.lower()]}
            if typ == "aggregate-aua-timeseries":
                rec["history"] = history_hashes(doc)
            if typ == "category-views":
                rec["tax_member"] = tax_member(doc)
            out["docs"][key] = rec
    m = s3.list_objects_v2(Bucket=BUCKET, Prefix=ROOT + "/_manifests/")
    objs = sorted(m.get("Contents", []), key=lambda x: x["LastModified"])
    out["latest_manifest"] = ({"key": objs[-1]["Key"], "last_modified": objs[-1]["LastModified"].strftime(
        "%Y-%m-%dT%H:%M:%SZ")} if objs else None)
    out["manifest_listing_truncated"] = bool(m.get("IsTruncated"))
    return out


def main(argv):
    if len(argv) != 3 or argv[1] not in ("baseline", "compare"):
        print(__doc__)
        return 2
    now = capture()
    if argv[1] == "baseline":
        json.dump(now, open(argv[2], "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
        print("baseline: %d documents at %s" % (len(now["docs"]), now["captured_at"]))
        return 0
    base = json.load(open(argv[2], encoding="utf-8"))
    bad = 0
    print("baseline %s -> now %s, %d documents" % (base["captured_at"], now["captured_at"], len(base["docs"])))
    for key in sorted(base["docs"]):
        b, n = base["docs"][key], now["docs"].get(key, {"error": "ABSENT"})
        if "error" in b or "error" in n:
            ok = b.get("error") == n.get("error")
            print("%-4s %s: baseline %s, now %s" % ("OK" if ok else "FAIL", key, b.get("error"), n.get("error")))
            bad += 0 if ok else 1
            continue
        problems = []
        if b["shape_sha256"] != n["shape_sha256"]:
            problems.append("shape moved (%d -> %d paths)" % (b["shape_paths"], n["shape_paths"]))
        if b["tax_named_paths"] != n["tax_named_paths"]:
            problems.append("tax-named paths %s -> %s" % (b["tax_named_paths"], n["tax_named_paths"]))
        if "history" in b:
            moved = [d for d, h in b["history"].items() if n.get("history", {}).get(d) != h]
            if moved:
                problems.append("%d of %d baseline dates changed (first %s)" % (len(moved), len(b["history"]), moved[0]))
        if "tax_member" in b and b["tax_member"] != n.get("tax_member"):
            problems.append("tax member %s -> %s" % (b["tax_member"], n.get("tax_member")))
        fresh = n["last_modified"] > b["last_modified"]
        print("%-4s %s: rewritten %s%s" % ("FAIL" if problems else "OK", key, fresh,
                                           ("; " + "; ".join(problems)) if problems else ""))
        bad += 1 if problems else 0
    print("manifest: baseline %s -> now %s" % (base.get("latest_manifest"), now.get("latest_manifest")))
    print("documents as expected: %d of %d" % (len(base["docs"]) - bad, len(base["docs"])))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
