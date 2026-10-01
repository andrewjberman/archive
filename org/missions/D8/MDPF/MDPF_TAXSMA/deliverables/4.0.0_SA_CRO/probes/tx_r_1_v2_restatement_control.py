"""TX-r-1 leg V2 control: is a restated recent date NORMAL between consecutive daily documents?

Reads the Gold function's own dated documents (opal-data-assets, portal/gold/mdpf/<scope>/aggregate-aua-timeseries/
<date>.json) for consecutive days and counts, per pair, the shared axis dates at which any series value differs.
Pairs wholly on the OLD code are the control; the last pair crosses the release. Read-only."""
import json
import sys

import boto3

B = "opal-data-assets"
SCOPES = ("49financial", "cottonwood", "global", "inflection")
s3 = boto3.client("s3")


def keys(scope):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(
            Bucket=B, Prefix="portal/gold/mdpf/%s/aggregate-aua-timeseries/" % scope):
        for o in page.get("Contents", []):
            out.append((o["Key"], o["LastModified"].strftime("%Y-%m-%dT%H:%MZ")))
    return sorted(out)


def load(key):
    return json.loads(s3.get_object(Bucket=B, Key=key)["Body"].read())


def series(doc):
    """{series path: list} for every list aligned to the date axis, top level and by_model."""
    n = len(doc["dates"])
    out = {}
    for k, v in doc.items():
        if isinstance(v, list) and len(v) == n and k != "dates":
            out[k] = v
    for mk, entry in (doc.get("by_model") or {}).items():
        for k, v in (entry or {}).items():
            if isinstance(v, list) and len(v) == n:
                out["by_model/%s/%s" % (mk, k)] = v
    return out


def diff(a, b):
    ia = {d: i for i, d in enumerate(a["dates"])}
    ib = {d: i for i, d in enumerate(b["dates"])}
    sa, sb = series(a), series(b)
    changed = {}
    for name in sorted(set(sa) & set(sb)):
        for d in ia:
            if d in ib and sa[name][ia[d]] != sb[name][ib[d]]:
                changed.setdefault(d, []).append(name)
    return changed, sorted(set(sb) - set(sa)), sorted(set(sa) - set(sb))


def main():
    last = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for scope in SCOPES:
        ks = keys(scope)[-last:]
        print("%s: %d dated documents read (newest %s written %s)" % (scope, len(ks), ks[-1][0].rsplit("/", 1)[1], ks[-1][1]))
        docs = [(k.rsplit("/", 1)[1][:-5], w, load(k)) for k, w in ks]
        for (da, wa, a), (db, wb, b) in zip(docs, docs[1:]):
            changed, added, removed = diff(a, b)
            tops = sorted({n.split("/")[0] for names in changed.values() for n in names})
            print("  %s (written %s) -> %s (written %s): %d shared date(s) restated %s | series %s | top-level keys added %s removed %s | tax keys in newer: %s"
                  % (da, wa, db, wb, len(changed), sorted(changed)[:6], tops[:6],
                     sorted(set(b) - set(a)), sorted(set(a) - set(b)),
                     sorted(k for k in b if "tax" in k.lower() or k in ("aggregate_basis", "base_excluding_tax_aua"))))


if __name__ == "__main__":
    main()
