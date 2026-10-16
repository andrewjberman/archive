"""discover_buckets.py <gateway dir>: the PRD v0.17 "done by" line -- opal_discover returns a row for every bucket, asked in plain words.

Run IN-PROCESS under the gateway's own venv and its own deployed catalog (on the host through discover_buckets_host.sh, or on a tree). For each bucket the
catalog holds, it takes ONE real catalog row of that bucket, uses that row's own first plain-words example question as the ask (nothing is typed here), calls the
deployed opal_discover as the Opal-internal principal, and records whether a returned match is that row's dataset (SERVED, the done-by test). It also records, as information, whether the match echoes the
bucket field and, for opal-data-assets and opal-data-bd, the vendor and firm. Prints one BUCKET line per bucket and two denominator lines; exits 0 only when every bucket is served.
"""
import collections
import os
import sys

import yaml

gw = os.path.abspath(sys.argv[1])
sys.path.insert(0, gw)
os.chdir(gw)
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

cat = yaml.safe_load(open(os.path.join(gw, "app", "refs", "DATA_CATALOG.yaml"), encoding="utf-8"))
by_bucket = collections.OrderedDict()
for sec in ("silver_datasets", "portal_datasets", "harvest_datasets"):
    for r in cat.get(sec) or []:
        if isinstance(r, dict) and r.get("entity") and r.get("bucket") and r.get("example_questions") and not r.get("retired"):
            by_bucket.setdefault(r["bucket"], []).append(r)

ok = echo = 0
for bucket, rows in sorted(by_bucket.items()):
    row = rows[0]
    ask = str(row["example_questions"][0])
    res = od.discover(ask, g.OPAL_INTERNAL)
    ms = res.get("matches", []) or []
    hit = [m for m in ms if m.get("dataset") == row["entity"]]
    # SERVED: plain words returned the catalog row of this bucket (the row is picked from the bucket, so the bucket is the catalog's).
    served = bool(hit)
    ok += served
    # ECHO (information, not the done-by test): does the match carry the bucket, and for assets/bd the vendor and firm, as fields?
    b_echo = bool(hit) and hit[0].get("bucket") == bucket
    vf_echo = bool(hit) and hit[0].get("vendor") == row.get("vendor") and hit[0].get("firm") == row.get("firm")
    echo += b_echo
    print("BUCKET %-20s rows=%-3d ask=%r matches=%d row=%s served=%s bucket_echo=%s vendor_firm_echo=%s"
          % (bucket, len(rows), ask[:60], len(ms), row["entity"][:44], "YES" if served else "NO", b_echo,
             vf_echo if bucket in ("opal-data-assets", "opal-data-bd") else "n/a"))
print("buckets served by plain words: %d of %d" % (ok, len(by_bucket)))
print("buckets whose match echoes the bucket field: %d of %d" % (echo, len(by_bucket)))
sys.exit(0 if ok == len(by_bucket) and by_bucket else 1)
