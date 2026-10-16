# NEVER-WIDEN ASK -- NFRA_OPLGTW.TO-OG-ap-27 (the internal reader role gets the read of the four prefixes the OG-ap-23 served read found denied)

**From:** `0.7.0_AE_CloudOps~ZS`, 2026-10-16 ~09:0xZ. **To the three halves:** `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`, `3.0.0_SA_CVO~Z`.
**Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-27.release-gap-grants-to-internal-reader.md`; the issuer's Phase A GO is msg 34855, with msg 34858 (put the CTO's ruling in the widening). Evidence of the gap: `deliverables/0.7.0_AE_CloudOps~Z/CODE_SERVED.json`, row `NFRA_OPLGTW-Z-S164`. CTO ruling msg 34853.
**Measurements:** `W/GAP_BEFORE.json`, `W/GAP_PLAN.txt`, where `W` = `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/`.
**State of the world:** nothing is applied. The targeted plan reads **2 to add, 0 to change, 0 to destroy** (two inline policies on `gateway-global-internal-reader-role`). Recommendation: **SIGN**.

The signature binds to `infra/aws/terraform/opal-gateway/gateway_release_gap_read_iam.tf` at sha256-16 `be09d3dd3aaebdd9` (4703 bytes, `terraform fmt -check` clean).
Any change to that hash re-opens every half; it is not applied on a stale hash.

## 1. The diff

One new file, no existing file changes: `infra/aws/terraform/opal-gateway/gateway_release_gap_read_iam.tf`. It holds two `opal_name` module calls (the names are `lib/opal_naming.py name("gateway","global",<function>,"policy")`
output: `gateway-global-etfs-gap-read-policy` and `gateway-global-mdpf-gap-read-policy`) and two `aws_iam_role_policy` resources on `aws_iam_role.int_reader`, each with two statements. No registry row was needed (the builder accepted both names).
The addresses were read from the COMMITTED catalog rows at `HEAD` (`infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`, the `bucket` and `prefix` fields), and they agree with the four lines in the order; no HEAD row disagreed.
Before state (`W/GAP_BEFORE.json`): the internal reader holds 7 inline policies (4,112 characters of the 10,240 limit) and 0 attached; neither new name is present. With the two new policies the total is about 5,022.

## 2. The widening

The internal reader role gains `s3:GetObject` on the prefix objects and a prefix-confined `s3:ListBucket`, read-only, on four prefixes of two buckets. Nothing is removed and no other role moves.

| bucket | prefix (stem) | catalog rows it covers | data |
|---|---|---|---|
| `opal-data-etfs` | `bbg/` | 7 rows `opal_data_etfs_silver_bbg_*` (characteristics, constituents_issuer_fill, derived_geo_allocation, derived_sector_allocation, derived_summary, fund_daily, history_topup), all `firm_scope_rule: opal-internal-only` | Opal-internal Bloomberg fund reference data |
| `opal-data-etfs` | `snapshots/` | `opal_data_etfs_silver_snapshots`, `opal-internal-only` | Opal-internal fund NAV and net-asset snapshots |
| `opal-data-etfs` | `mdpf/etfs/gold/new_securities/` | `opal_data_etfs_gold_mdpf_new_securities`, `opal-internal-only` | Opal-internal list of newly appearing securities |
| `opal-data-mdpf` | `mdpf/feeds/model_composition/` | `opal_data_mdpf_feeds_model_composition`, `firm_scope_rule: firm-scoped` | model composition per firm |

`bbg/` is granted as a whole stem, as the order states, so it covers seven catalog rows even though three tools read some of them. Each statement: `GetObject` on `<bucket>/<prefix>*`; `ListBucket` on the bucket with `s3:prefix` `StringLike` on `<prefix>*` only. No `*` resource, no bucket-wide object ARN, no Put or Delete, no unconditioned ListBucket.
**Not granted:** `silver/*` of `opal-data-etfs`. The CTO's message names "opal-data-etfs/silver/*" for the three etfs tools; that is the table family's label, not the key prefix (the keys sit under `bbg/`, `snapshots/` and `mdpf/etfs/gold/new_securities/`), and `silver/*` would cover tables no tool of this release reads.

**The firm-scoped row, stated plainly so the halves sign knowing both facts.** The catalog row for `mdpf/feeds/model_composition/` reads `firm_scope_rule: firm-scoped` (model holdings forked by firm; its catalog prefix is `mdpf/feeds/model_composition/<firm>/`, objects for `49financial` and `inflection`). (1) The IAM prefix here is NOT firm-confined: it stops before the firm segment, no firm token is typed, and IAM cannot fence the firms apart. (2) The gateway tool `mdpf_get_model_composition` is in `NATIVE_TOOLS` (any Opal principal, one firm per call) in `app/data_entitlement.py`.
**The CTO's ruling (msg 34857, relayed by the issuer in msg 34858):** `mdpf_get_model_composition` stays NATIVE, no re-cut, the code halves stand; Ruling 2 binds client account-level data, and model composition is Opal's own model definition delivered to a partner firm (the `OG-ap-20` precedent).

## 3. The tools

`etfs_get_new_securities` reads `mdpf/etfs/gold/new_securities/` (`date={D}/new_securities.json`); `etfs_get_fund_bloomberg_characteristics` reads `bbg/` (the order names `bbg/{as_of}/fund_daily.parquet` and `bbg/{as_of}/constituents/derived_*.parquet`); `etfs_get_fund_snapshot` reads `snapshots/snapshot_{date}.json`; `mdpf_get_model_composition` reads `mdpf/feeds/model_composition/<firm>/...` (parquet), one firm per call. All four are Opal-principal-only tools; a non-Opal call is refused by the gateway before any S3 call. (Tool-to-prefix pairs are the order's; this seat did not read the tool code.)

## 4. The order of acts (Phase B, on a GO naming all three halves signed at the hash)

1. Ledger `nfra-oplgtw-grants-ap27`, entry and sentinel first; `comp-schedule --drift` at the act.
2. One `safe-apply`, targeted at the two resources: the plan must read 2 add / 0 change / 0 destroy.
3. Read back from IAM: both policies on `gateway-global-internal-reader-role`, equal to the file, absent from any other role. Simulator, ONE resource per call: `s3:GetObject` allowed on a probe key under each of the four prefixes; `s3:ListBucket` allowed with each prefix as the `s3:prefix` context value; NOT allowed on an out-of-scope key and prefix of each bucket (`ap27-negative-control/`), run as their own invocations; a positive control (a principal holding `s3:*`) beside any deny read. Targeted re-plan: `No changes`.
4. This is BEFORE the re-deploy of `3d5c9c8bf1`, which waits on `ap27.AC2` PASS.

## 5. Both branches

An in-prefix read serves (the core reads through the internal reader and the prefix is granted); an out-of-prefix read stays denied by IAM (no statement covers it); a non-Opal call is still refused by the gateway before any S3 call. The applier cannot assume the internal reader, so the IAM branch is read by the simulator only; the served branch is the release re-deploy's proof.

## 6. The rollback

A `safe-apply` targeted destroy of the two policies (or `delete-role-policy` for each of the two names on the internal reader). The prior state is `W/GAP_BEFORE.json` (7 policies, document hashes recorded); the release re-deploy has not happened at this step, so nothing serves these reads yet. Trunk: `git revert` of the `.tf` commit via `safe-commit`.

## 7. The triggers

The act is complete only when ALL hold: (1) both policies read back live on the internal reader and equal the file; (2) the simulator allows the four prefixes (GetObject and ListBucket) and refuses the out-of-scope key and prefix of each bucket; (3) the targeted re-plan reads `No changes`; (4) the ledger is CLOSED and `W/GAP_APPLIED.json` is written. Any other reading stops the act, both policies are destroyed, and an ARMED row names `2.0.0_SA_COO~O`.

## 8. The gaps

Two limits stated: the simulator reads the IAM branch only, so no object was read and the served branch is the re-deploy's; and `bbg/` as a whole stem covers seven catalog rows, four of which (`constituents_issuer_fill`, `derived_geo_allocation`, `derived_sector_allocation`, `history_topup`) may not be read by any of this release's tools. They are `opal-internal-only` and the stem is the order's.

---

## CTO half

**Half: `1.0.0_SA_CTO~Z`** -- sign / refuse: ______________

## COO half

**Half: `2.0.0_SA_COO~O`** -- sign / refuse: ______________

## CVO half

**Half: `3.0.0_SA_CVO~Z`** -- sign / refuse: ______________
