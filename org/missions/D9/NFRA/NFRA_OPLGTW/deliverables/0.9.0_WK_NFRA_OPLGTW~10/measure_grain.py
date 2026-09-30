"""NFRA_OPLGTW OG-v-6 steps 1-2: fix D_NEW / D_PREV from the closure markers and measure the
declared grain on the 12 version-pinned qualified silver snapshots. Writes GRAIN_DECLARATION.json.
Counts, hashes, VersionIds and dates only -- never a key value. pyarrow is used to decode Parquet
only; grouping is Python collections.Counter. No import of the Gateway."""
from __future__ import annotations

import itertools
import json
import os
import sys
from collections import Counter

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import og_v6_common as C  # noqa: E402

CONTRACT = os.path.join(C.REPO_ROOT, "org", "standards", "NFRA_OPLGTW_CONTRACT.json")
# The contract's masked account column is account_ref; the source column is account_id (the Gateway
# hides the raw id). The candidate search treats account_ref as the contract name of account_id.
SRC_TO_CONTRACT = {"account_id": "account_ref"}
CONTRACT_TO_SRC = {"account_ref": "account_id"}


def latest_markers(master):
    raw = C.aws(["s3api", "list-object-versions", "--bucket", C.BUCKET,
                 "--prefix", f"schwab/{master}/meta/complete/",
                 "--query", "Versions[?IsLatest].[Key,VersionId,LastModified]", "--output", "json"])
    out = {}
    for key, vid, lm in json.loads(raw):
        d = key.rsplit("date=", 1)[1][: -len(".json")]
        out[d] = {"key": key, "version_id": vid, "last_modified": lm}
    return out


def blank(v):
    return v is None or (isinstance(v, str) and v.strip() == "")


def measure(path, grain):
    t = pq.read_table(path, columns=list(grain))
    keys = list(zip(*[t.column(c).to_pylist() for c in grain]))
    cnt = Counter(keys)
    coll = [k for k, v in cnt.items() if v > 1]
    return {
        "rows": t.num_rows,
        "colliding_keys": len(coll),
        "extra_rows": sum(cnt[k] - 1 for k in coll),
        "colliding_keys_with_blank_component": sum(1 for k in coll if any(blank(x) for x in k)),
        "rows_in_colliding_keys": sum(cnt[k] for k in coll),
    }


def candidate_superset(path, dataset, contract_fields):
    """Smallest superset of the declared grain, from contract columns, unique on this snapshot."""
    base = [SRC_TO_CONTRACT.get(c, c) for c in C.DECLARED_GRAIN[dataset]]
    extras_pool = [f for f in contract_fields[dataset] if f not in base]
    src_of = lambda f: CONTRACT_TO_SRC.get(f, f)  # noqa: E731
    need = sorted(set(src_of(f) for f in base + extras_pool))
    t = pq.read_table(path, columns=need)
    col = {c: t.column(c).to_pylist() for c in need}
    n = t.num_rows
    for k in (1, 2, 3, 4):
        found = []
        for extra in itertools.combinations(extras_pool, k):
            cols = [col[src_of(f)] for f in base + list(extra)]
            seen = set(zip(*cols))
            if len(seen) == n:
                found.append(list(extra))
        if found:
            return {"label": "CANDIDATE", "columns": base + found[0], "extra_columns_added": k,
                    "alternatives_at_this_size": len(found), "spec_decision_owner": "1.0.0_SA_CTO~O"}
    return {"label": "CANDIDATE", "columns": "NONE_FOUND", "searched_extra_columns_up_to": 4,
            "spec_decision_owner": "1.0.0_SA_CTO~O"}


def main():
    with open(CONTRACT, "r", encoding="utf-8") as fh:
        contract_fields = json.load(fh)["fields"]

    lm = {m: latest_markers(m) for m in C.MASTERS}
    both = sorted(set(lm["08242234"]) & set(lm["08335338"]), reverse=True)
    markers = {}   # (master, date) -> (marker doc, listing row)

    def marker(m, d):
        if (m, d) not in markers:
            row = lm[m][d]
            markers[(m, d)] = (C.get_marker(m, d, row["version_id"]), row)
        return markers[(m, d)]

    def qualified(d):
        return all(marker(m, d)[0].get("closure", {}).get("status") == "qualified" for m in C.MASTERS)

    qual = []
    for d in both:
        if qualified(d):
            qual.append(d)
        if len(qual) == 2:
            break
    d_new, d_prev = qual
    dates = {"D_NEW": d_new, "D_PREV": d_prev}
    marker_rec = []
    for tag, d in dates.items():
        for m in C.MASTERS:
            doc, row = marker(m, d)
            marker_rec.append({"tag": tag, "master": m, "date": d, "key": row["key"],
                               "version_id": row["version_id"], "last_modified": row["last_modified"],
                               "closure_status": doc["closure"]["status"],
                               "closure_id": doc["closure"]["closure_id"]})

    snaps = []
    for m in C.MASTERS:
        for d in (d_prev, d_new):
            doc, _ = marker(m, d)
            for ds in C.DATASETS:
                obj = doc["closure"]["tables"][ds]
                assert obj["disposition"] == "PRESENT", (m, d, ds)
                o = obj["object"]
                path = C.fetch_silver(o["key"], o["version_id"], f"{m}_{ds}_{d}_{o['version_id']}.parquet")
                grain = C.DECLARED_GRAIN[ds]
                r = measure(path, grain)
                status = "HOLDS" if r["colliding_keys"] == 0 else "COLLIDES"
                rec = {"dataset": ds, "master": m, "date": d, "tag": "D_NEW" if d == d_new else "D_PREV",
                       "key": o["key"], "version_id": o["version_id"],
                       "declared_grain": list(grain), "rows": r["rows"],
                       "marker_declared_rows": obj.get("rows"),
                       "colliding_keys": r["colliding_keys"], "extra_rows": r["extra_rows"],
                       "colliding_keys_with_blank_component": r["colliding_keys_with_blank_component"],
                       "rows_in_colliding_keys": r["rows_in_colliding_keys"], "status": status}
                if status == "COLLIDES":
                    rec["candidate_unique_superset"] = candidate_superset(path, ds, contract_fields)
                snaps.append(rec)
                print(f"{m} {d} {ds}: rows={r['rows']} colliding_keys={r['colliding_keys']} "
                      f"extra_rows={r['extra_rows']} {status}")
    doc = {
        "schema_version": "1.0", "cell": "OG-v-6", "worker": "0.9.0_WK_NFRA_OPLGTW~10",
        "dates": dates, "markers": marker_rec,
        "grain_source": "infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py:136-140 @73e5968e67, inlined by the task order in source column names; this script never reads it",
        "candidate_note": "candidate_unique_superset is a CANDIDATE only; adopting a different grain is a spec decision for 1.0.0_SA_CTO~O, never this cell's. account_ref is the contract name of source account_id (assumed). Column names only, never a key value.",
        "snapshot_count": len(snaps), "snapshots": snaps,
    }
    with open(C.GRAIN_PATH, "w", encoding="ascii") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    print("OK: wrote", C.GRAIN_PATH, "snapshots", len(snaps), "dates", dates)


if __name__ == "__main__":
    main()
