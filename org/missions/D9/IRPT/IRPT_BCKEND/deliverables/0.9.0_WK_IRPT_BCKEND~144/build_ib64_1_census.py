#!/usr/bin/env python3
"""IRPT_BCKEND TO-IB-pr-342 (worker ~144): the NOT_IN_DIRECTORY census, recomputed from the sources.

READ-ONLY (S3 get/head/list only). Run from the repo root of the worktree:
    python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~144/build_ib64_1_census.py <out.json>
Writes only <out.json>. No raw custodian number is written: every account is the estate's opaque `acc_` form
(see `id_space` in each evidence string).
"""
import collections
import io
import json
import sys

import boto3
import pandas as pd

sys.path.insert(0, "infra/aws/lambda/investor-reporting/_ids")
import ids  # noqa: E402

FIRM = "49financial"
S3 = boto3.client("s3", region_name="us-east-1")
BD_BUCKET = "opal-data-bd"            # directory_runner.firm_bucket_map()["49financial"]
GOLD_BUCKET = "opal-data-49financial"  # runners_49f/runner_common.py:34 GOLD_BUCKET
SILVER_BUCKET = "opal-data-assets"     # runners_49f/runner_common.py:33 SILVER_BUCKET


def jget(bucket, key):
    return json.loads(S3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8"))


def pq(bucket, key, columns=None):
    return pd.read_parquet(io.BytesIO(S3.get_object(Bucket=bucket, Key=key)["Body"].read()), columns=columns)


def parts(bucket, prefix):
    out = set()
    for pg in S3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for c in pg.get("CommonPrefixes", []):
            out.add(c["Prefix"])
    return sorted(out)


def main(out_path):
    own_key = "platinum/49financial/ownership_map.json"
    own = jget(BD_BUCKET, own_key)
    ptr = jget(BD_BUCKET, "investor-reporting/directory/latest.json")
    dr = jget(BD_BUCKET, ptr["key"])
    as_of = ptr["as_of_business_date"]
    dir_ids = set()
    for e in dr["entries"]:
        dir_ids.update(e["ids"]["account_ids"])

    seam = ids.load_seam_index("custodian_key_seam")["index"]
    proj = ids.projection_for_firm(FIRM)

    xdates = [p for p in parts(SILVER_BUCKET, "blackdiamond/49f/silver/dim_account_xref/") if p.split("=")[-1].rstrip("/") <= as_of]
    xp = xdates[-1]
    x_asof = xp.split("=")[-1].rstrip("/")
    xref = pq(SILVER_BUCKET, xp + "data.parquet")
    xref_row = {str(r.bd_account_id): r for r in xref.itertuples()}
    rel = pq(GOLD_BUCKET, "gold/advi/dimensions/dim_relationship/date=%s/data.parquet" % as_of, ["account_id"])
    acc = pq(GOLD_BUCKET, "gold/advi/dimensions/dim_account/date=%s/data.parquet" % as_of,
             ["account_id", "account_is_open", "absent_from_feed_since"])
    rel_set = set(rel.account_id.astype(str))
    acc_ix = acc.set_index(acc.account_id.astype(str))

    # every xref / fee-role partition: a key seen in none of them has no bridge on any date
    seen_x, seen_f = set(), set()
    xparts = parts(SILVER_BUCKET, "blackdiamond/49f/silver/dim_account_xref/")
    fparts = parts(SILVER_BUCKET, "blackdiamond/49f/silver/dim_advisor_fee_role/")
    for p in xparts:
        seen_x |= set(pq(SILVER_BUCKET, p + "data.parquet", ["bd_account_id"]).bd_account_id.astype(str))
    for p in fparts:
        seen_f |= set(pq(SILVER_BUCKET, p + "data.parquet", ["bd_account_id"]).bd_account_id.astype(str))
    fba = pq(SILVER_BUCKET, "blackdiamond/49f/silver/fact_bd_allocation/date=2026-08-18/data.parquet", ["accountid"])
    tax = pq(SILVER_BUCKET, "blackdiamond/49f/silver/fact_taxsma_report/date=2026-07-17/data.parquet", ["bd_account_id"])
    seen_o = set(fba.accountid.astype(str)) | set(tax.bd_account_id.astype(str))

    distinct = {}
    for g in own["advisors"].values():
        for a in g.get("accounts") or []:
            distinct.setdefault(str(a), a)
    raws = list(distinct)

    accounts, n_in = [], 0
    for raw in raws:
        p = proj("account", raw)
        if p in dir_ids:
            n_in += 1
            continue
        if raw in seam:
            sid = str(seam[raw]).zfill(10)
            a = acc_ix.loc[sid]
            assert sid not in rel_set
            reason = "ACCOUNT_CARRIED_ABSENT_FROM_FEED_NOT_IN_RELATIONSHIP"
            ev = ("id_space=directory (seam-mapped, the id the directory would carry); bridge=seam@xref 2026-09-16 -> Schwab id; "
                  "Schwab id is in dim_account@%s (account_is_open=%s, absent_from_feed_since=%s) and NOT in dim_relationship@%s"
                  % (as_of, a.account_is_open, str(a.absent_from_feed_since)[:10], as_of))
            acct = p
        elif raw in xref_row:
            r = xref_row[raw]
            nums = [str(getattr(r, c)).strip().zfill(10) for c in ("bd_account_number", "bd_original_account_number")]
            hit = any(n in acc_ix.index for n in nums)
            assert not any(n in rel_set for n in nums)
            assert pd.isna(r.schwab_account_id) and str(r.match_method) == "unresolved"
            if hit:
                reason = "XREF_UNRESOLVED_NUMBER_IN_DIM_ACCOUNT_ONLY"
                ev = ("id_space=custodian-key mint (not a directory-space id); xref@%s row has schwab_account_id null, match_method=unresolved; "
                      "its account number is a dim_account@%s account that is NOT in dim_relationship@%s" % (x_asof, as_of, as_of))
            else:
                reason = "XREF_UNRESOLVED_NO_SCHWAB_MATCH"
                ev = ("id_space=custodian-key mint (not a directory-space id); xref@%s row has schwab_account_id null, match_method=unresolved; "
                      "its account number matches no dim_account@%s account; absent from the seam snapshot (826 None values removed, pr-339)"
                      % (x_asof, as_of))
            acct = ids.opaque_account(FIRM, raw)
        else:
            assert raw not in seen_x and raw not in seen_f and raw not in seen_o
            reason = "BD_KEY_ABSENT_FROM_EVERY_BRIDGE_SOURCE"
            ev = ("id_space=custodian-key mint (not a directory-space id); key in ownership map, in NONE of: dim_account_xref (%d partitions), "
                  "dim_advisor_fee_role (%d partitions), fact_bd_allocation@2026-08-18, fact_taxsma_report@2026-07-17; so no path to a Schwab id"
                  % (len(xparts), len(fparts)))
            acct = ids.opaque_account(FIRM, raw)
        accounts.append({"account": acct, "firm": FIRM, "reason": reason, "evidence": ev})

    reason_set = [
        "BD_KEY_ABSENT_FROM_EVERY_BRIDGE_SOURCE",
        "XREF_UNRESOLVED_NO_SCHWAB_MATCH",
        "XREF_UNRESOLVED_NUMBER_IN_DIM_ACCOUNT_ONLY",
        "ACCOUNT_CARRIED_ABSENT_FROM_FEED_NOT_IN_RELATIONSHIP",
        "FENCE_COTTONWOOD_BUCKET_DENIED",
        "UNEXPLAINED",
    ]
    by = collections.OrderedDict((r, 0) for r in reason_set)
    for a in accounts:
        by[a["reason"]] += 1
    out = {
        "granted_total": len(raws),
        "in_directory_total": n_in,
        "not_in_directory_total": len(accounts),
        "per_firm": {
            "49financial": {"granted": len(raws), "in_directory": n_in, "not_in_directory": len(accounts),
                            "directory": "%s entries=%d account_ids=%d as_of=%s" % (ptr["directory_revision"], len(dr["entries"]), len(dir_ids), as_of)},
            "inflection": {"granted": 0, "in_directory": 0, "not_in_directory": 0,
                           "note": "no ownership_map object at s3://opal-data-inf/platinum/inflection/ownership_map.json (404 head); latest.json read, entry_count 294; no grant population"},
            "cottonwood": {"granted": 0, "in_directory": 0, "not_in_directory": 0,
                           "note": "s3://opal-data-cot/platinum/cottonwood/ownership_map.json has advisors=0; s3://opal-data-cottonwood is denied (403) and was not read past the probe"},
        },
        "sources": {
            "ownership_map": "s3://%s/%s (schema_version 1, 190 advisors, distinct accounts by string)" % (BD_BUCKET, own_key),
            "directory": "s3://%s/%s -> %s" % (BD_BUCKET, "investor-reporting/directory/latest.json", ptr["key"]),
            "projection": "infra/aws/lambda/investor-reporting/_ids/ids.py projection_for_firm (custodian_key_seam.json then mint)",
            "xref": "s3://%s/%s date=%s (the build's own xref, directory_runner.py Firm49F.load)" % (SILVER_BUCKET, "blackdiamond/49f/silver/dim_account_xref", x_asof),
            "directory_build_source": "s3://%s/gold/advi/dimensions/dim_relationship/date=%s and dim_account (same date)" % (GOLD_BUCKET, as_of),
            "bridge_search": "dim_account_xref %d partitions, dim_advisor_fee_role %d partitions, fact_bd_allocation 2026-08-18, fact_taxsma_report 2026-07-17" % (len(xparts), len(fparts)),
        },
        "reason_set": reason_set,
        "by_reason": dict(by),
        "accounts": accounts,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("granted=%d in=%d not_in=%d by_reason=%s" % (len(raws), n_in, len(accounts), dict(by)))


if __name__ == "__main__":
    main(sys.argv[1])
