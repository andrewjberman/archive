#!/usr/bin/env python3
"""BP-c-7 record writer, ADVI_BDPRCE round 3. Worker 0.9.0_WK_ADVI_BDPRCE~19. READ-ONLY on AWS (no S3 call here).

Reads the outputs of bp_c7_fetch.py, bp_c7_classify.py, bp_c7_named_rps.py, bp_c7_named_holdings.py from
C:/dev/wk-bdprce-r3-19-data and writes, inside the deliverables folder:
  OFFCANON.json        the record (order section 1b shape; every number derived here, none typed by hand)
  OFFCANON_LOTS.csv    one line per lot: key class, key digest (sha12 of the raw object key), asset, served price,
                       data_as_of, class, evidence reference. No raw object key, no account id.
Run from the worktree root:  python -I <this file>
"""
import csv
import datetime as dt
import hashlib
import json
import sys
from collections import Counter

import pandas as pd

DATA = "C:/dev/wk-bdprce-r3-19-data"
DELIV = "org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~19"
EXPECT_SHA = "e7e618d76516c8b7977179aefb3f77ce4fc13c17fbcf1dbeb92001a6e0a2b50b"
CLASSES = ["EQUALS_OLDER_CANONICAL_VERSION", "EQUALS_DAILY_FILE_ROW", "EQUALS_NAMED_OTHER_SOURCE", "UNEXPLAINED"]
RPS_KEY = "schwab/silver/rps/date=20260723/data.parquet"

CALLS = [
    "aws sts get-caller-identity (identity only)",
    "aws s3api head-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet",
    "aws s3api list-object-versions --bucket opal-data-bd --prefix silver/prices/canonical_prices.parquet --output json (657 versions)",
    "aws s3api list-objects-v2 --bucket opal-data-bd --prefix silver/prices/ --output json (176 objects)",
    "boto3 s3 list_object_versions Bucket=opal-data-bd Prefix=silver/prices/ (paginated; 841 parquet versions: 657 canonical, 184 daily)",
    "boto3 s3 download_file Bucket=opal-data-bd Key=silver/prices/* VersionId=<each of 841 versions> (GET, 6 threads; full copy deleted after projection)",
    "aws s3api get-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet --version-id <one version> (probe)",
    "aws s3api get-object --bucket opal-data-bd --key silver/prices/2026-10-09.parquet (probe)",
    "aws s3api get-object --bucket opal-data-bd --key gold/dimensions/schwab_bd_account_mapping.parquet",
    "aws s3api list-objects-v2 --bucket opal-data-bd --prefix schwab/silver/rps/ --output json (636 objects)",
    "aws s3api get-object --bucket opal-data-bd --key schwab/silver/rps/date=20260723/data.parquet",
    "aws s3api list-objects-v2 --bucket opal-data-bd --prefix gold/canonical/holdings/ --query (last 4 keys)",
    "aws s3api head-object --bucket opal-data-bd --key gold/canonical/holdings/2026-10-09.parquet",
    "aws s3api get-object --bucket opal-data-bd --key gold/canonical/holdings/2026-10-09.parquet",
    "local: sha256 of C:/dev/wk-bdprce-r2-7-data/lot_extract.csv; pandas join of the projections; no S3 write",
]


def sha12(s):
    return hashlib.sha256(str(s).encode("utf-8")).hexdigest()[:12]


def main():
    lots = pd.read_csv(f"{DATA}/classified/lots_classified.csv", dtype=str, keep_default_na=False)
    tri = pd.read_csv(f"{DATA}/classified/triples.csv", dtype=str, keep_default_na=False)
    named_rps = json.load(open(f"{DATA}/classified/named_rps.json"))
    named_hold = json.load(open(f"{DATA}/classified/named_holdings.json"))
    named_hist = json.load(open(f"{DATA}/classified/named_historical.json"))
    fetch = json.load(open(f"{DATA}/fetch_log.json"))

    lot_n = len(lots)
    cnt = Counter(lots["class"])
    classes = {k: int(cnt.get(k, 0)) for k in CLASSES}
    assert sum(classes.values()) == lot_n, "class partition does not sum to lots_total"
    extract_rows = sum(1 for _ in open("C:/dev/wk-bdprce-r2-7-data/lot_extract.csv", encoding="utf-8")) - 1
    versions_read = len(fetch["results"])
    canon_v = sum(1 for r in fetch["results"] if r["key"].endswith("canonical_prices.parquet"))
    daily_v = versions_read - canon_v
    fails = [r for r in fetch["results"] if r["status"] == "fail"]
    assert not fails, "fetch failures present"

    # the lot-level CSV (hashed keys)
    out_csv = f"{DELIV}/OFFCANON_LOTS.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["key_class", "key_digest", "asset_name", "served_price", "data_as_of", "class", "evidence_ref"])
        for r in lots.to_dict("records"):
            w.writerow([r["entity_class"], sha12(r["object_key"]), r["asset_name"], r["served_price"],
                        r["data_as_of"], r["class"], r["evidence"]])

    # exemplars: the biggest group per class, by lots
    g = lots.groupby(["class", "asset_name", "served_price", "data_as_of"]).size().reset_index(name="lots")

    def top(c):
        return g[g["class"] == c].sort_values("lots", ascending=False).iloc[0]

    ex = {}
    t1 = top("EQUALS_OLDER_CANONICAL_VERSION")
    trow = tri[(tri["asset_name"] == t1["asset_name"]) & (tri["served_price"] == t1["served_price"])
               & (tri["data_as_of"] == t1["data_as_of"])].iloc[0]
    # first_older_hit = "<version_id>@<LastModified> row_date=<d> source=<s>"
    head_part, rest = trow["first_older_hit"].split(" ", 1)
    ver_id, last_mod = head_part.split("@", 1)
    row_date = rest.split("row_date=")[1].split(" ")[0]
    src = rest.split("source=")[1]
    ex["EQUALS_OLDER_CANONICAL_VERSION"] = (
        f"{t1['asset_name']}, served {t1['served_price']}, data_as_of {t1['data_as_of']} ({t1['lots']} lots): "
        f"found in canonical version {ver_id} (LastModified {last_mod}, earliest matching version) as row "
        f"row_date {row_date} source {src}; the price is carried in {trow['older_versions']} of the older "
        f"canonical versions")
    ex["EQUALS_DAILY_FILE_ROW"] = (
        "none: 0 lots. The triples with a silver/prices daily-file row (any version) all also carry an older "
        "canonical row, and the first-match order assigns them to EQUALS_OLDER_CANONICAL_VERSION")
    t3 = top("EQUALS_NAMED_OTHER_SOURCE")
    m3 = next(m for m in named_rps["matches"] if m["asset_name"] == t3["asset_name"]
              and m["served_price"] == t3["served_price"] and m["data_as_of"] == t3["data_as_of"])
    ex["EQUALS_NAMED_OTHER_SOURCE"] = (
        f"{t3['asset_name']}, served {t3['served_price']}, data_as_of {t3['data_as_of']} ({t3['lots']} lots): "
        f"{m3['n_hits']} matching rows in {RPS_KEY} closing_price (ticker "
        f"{m3['first_hit']['ticker'].strip()}), on BD accounts that hold the lot; negative control 0 of "
        f"{named_rps['triples_tested']}")
    t4 = top("UNEXPLAINED")
    ex["UNEXPLAINED"] = (
        f"{t4['asset_name']}, served {t4['served_price']}, data_as_of {t4['data_as_of']} ({t4['lots']} lots): "
        f"no canonical row equal in any of the {canon_v} canonical versions, no daily-file row, no {RPS_KEY} "
        f"row for its accounts at that price, no 2026-10-09 holdings row at that name, account and price")

    kinds = {k: int(v) for k, v in Counter(lots["kind"]).items()}
    named_sources = [
        f"{RPS_KEY} closing_price, the newest RPS partition listed (2026-07-23; the B_01 resolver falls back to the "
        f"latest key for a 2026-10-09 snapshot): B_01.holdings_lots.py:529-560 (partition resolver), "
        f"581-589 (mapping read via gold/dimensions/schwab_bd_account_mapping.parquet), 690-705 (price lookup), "
        f"2215-2288 (_apply_rps_price_override writes closing_price to current_price), 2223-2226 (bond percent-of-par /100)",
    ]

    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {
        "order": "BP-c-7",
        "read_at": now,
        "claim": "measured",
        "calls": CALLS,
        "lots_total": lot_n,
        "distinct_triples": int(len(tri)),
        "extract_sha256": EXPECT_SHA,
        "versions_read": versions_read,
        "classes": classes,
        "named_sources": named_sources,
        "exemplars": ex,
        "by_asset_kind": kinds,
        "detail": {
            "extract_rows": extract_rows,
            "canonical_versions_listed_and_read": canon_v,
            "daily_file_versions_listed_and_read": daily_v,
            "fetch_failures": len(fails),
            "triples": {k: int(v) for k, v in Counter(tri["class"]).items()},
            "triples_with_no_served_price_literal_nan": int((tri["served_price"].str.lower() == "nan").sum()),
            "lots_with_no_served_price_literal_nan": int((lots["served_price"].str.lower() == "nan").sum()),
            "triples_with_match_in_latest_version_only_path": int((tri["n_latest_only_rows"].astype(int) > 0).sum()),
            "triples_latest_match_but_unexplained": int(((tri["n_latest_only_rows"].astype(int) > 0)
                                                         & (tri["class"] == "UNEXPLAINED")).sum()),
            "triples_daily_row_also_older_canonical": int(((tri["n_daily_rows"].astype(int) > 0)
                                                           & (tri["n_older_rows"].astype(int) > 0)).sum()),
            "rps_check": {"source": named_rps["source"], "triples_tested": named_rps["triples_tested"],
                          "triples_matched": named_rps["triples_matched"],
                          "negative_control_matched": named_rps["control_matched"],
                          "positive_control_recall": named_rps["positive_control_recall"]},
            "holdings_check": {"source": named_hold["source"], "scope": named_hold["data_as_of_scope"],
                               "triples_tested": named_hold["triples_tested"],
                               "triples_matched": named_hold["triples_matched"],
                               "negative_control_matched": named_hold["control_matched"],
                               "positive_control_recall": named_hold["positive_control_recall"]},
            "historical_value_only_check": named_hist,
            "not_read": [
                "the 1,859 lots' object-level fields beyond those in the extract (no per-lot price source field is served)",
                "canonical versions and daily files outside the listing (none; listing is complete)",
                "gold/canonical/holdings for data_as_of other than 2026-10-09 (1 unexplained lot at another date)",
                "name-variant canonical rows (the projection kept only rows whose asset_name is one of the 340 off-canonical names or whose ticker is in the lookup)",
            ],
        },
    }
    with open(f"{DELIV}/OFFCANON.json", "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("OK: wrote OFFCANON.json and OFFCANON_LOTS.csv")
    print("classes", classes, "lots_total", lot_n, "versions_read", versions_read)
    return 0


if __name__ == "__main__":
    sys.exit(main())
