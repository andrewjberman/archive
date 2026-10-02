# NEVER-WIDEN -- COO HALF, ADDENDUM 11: publish-page bronze-read grant + F5 prompt + round 5's drained code, at pin CLOUD 8075f97ffb

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~13:2xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-11 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-10. Every gate, key and condition stands.
**Apply gate beyond the pair:** Andrew's word that served changes resume after his 13:00Z read (next-calls CALL 1).

**Why:**
1. The publish-page Lambda cannot read the bronze sidecars. Every marker-driven page (the 07:00 ET publish) shows
   "source URL unavailable (bronze sidecar unreadable)" x108 until the 09:00 ET sweep republishes through the daily
   Lambda. Grant @fd0d285da3.
2. F5 prompt a1-chain/4 @0839079a9c (readings named by label).
3. Round 5's drained code -- m-2 collector dedup, l-1 v0.8 leg inert, s-6 G4 as-of guard (@e4e9eedfa9, @213540f408) --
   so the Lambdas run what the vehicle runs from the CLOUD tree.

## VERDICT: SIGNED (at pin CLOUD 8075f97ffb)

## THE PLAN, MEASURED

**Plan: 0 to add, 6 to change, 0 to destroy** (`/c/tmp/rv_apply12.tfplan`, from `/c/tmp/rv-fast` with HEAD = CLOUD HEAD
8075f97ffb):
- the five Lambdas' `source_code_hash` + `last_modified`;
- `aws_iam_role_policy.stage["rivalfunds-publish-page-lambda"]`: exactly four ADDED lines and none removed. GetObject on
  `opal-data-etfs/bloomberg/etfs/bronze/holdings/*` and `opal-data-etfs/issuer-site/etfs/bronze/holdings/*`, plus the
  same two as ListBucket prefixes. No Put, no other role.
Package diff vs the deployed f122e4476b: ai_accounts (F5), universe.py, peer_groups.json, collector_bloomberg.py,
enrichment_bloomberg.py (round 5). No rivalfunds file changed between 213540f408 and 8075f97ffb.

## THE SERVED DELTA, MEASURED (page day 2026-10-02), CODE ISOLATED FROM DATA

- **A1 tables:** the three producers' `handler_entry` run at f122e4476b and at 213540f408 over the SAME current inputs
  (`round5/a1_at_pin.py` on extracted packages, overlay sink; `round5/a1_compare.py`) -> `a1_code_delta_addendum11_20261002.json`.
  holding_contribution 0 of 79,317 values changed; buying_trend 0 of 5,423; input_census 0 of 12,496. Rows and columns
  are identical.
- **Page:** overlay publish of 2026-10-02 at 213540f408 vs the served fast-a1-publish-1002e: ONE line differs, the G0
  map date (10-01 -> 10-02). That is a newer map object the 13:00Z sweep wrote, which any republish reads; 0 code lines.
- **The grant:** moves marker-driven pages only (the next 07:00 ET publish): their trace panels carry source links and
  capture detail as the daily-Lambda pages already do. Not covered: PFOE's 26 home-producer lines (round-6 cut list #6).

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| M1 | the five stage Lambdas' code | f122e4476b (daily 336g/dQ/.., fetch YW2+zw+T.., canonical uOmcfR6A.., silver 4Gw36ziQ.., publish h+vC/B3i..) | in place to 8075f97ffb | re-apply from a tree at f122e4476b |
| M2 | rivalfunds-publish-page-policy | 2 bronze prefixes absent | + GetObject / ListBucket on the 2 bronze holdings prefixes | re-apply from a tree at f122e4476b (the policy is generated from gen_policies.py) |
| M3 | the next scheduled runs (07:00 ET 2026-10-05 onward) | run f122e4476b without the grant | run 8075f97ffb with it | M1 + M2 rollback |

No republish and no gold object: the 10-02 page stays fast-a1-publish-1002e (its code delta is 0).

## ACT-START GATES

1. Andrew's word (CALL 1). 2. Plan exactly 0/6/0 with the policy diff above. 3. Live base equals M1's CodeSha256.
4. NEVER-2 entry `etfs-rivalfunds-fast-a1-r12` opened AND committed before the apply (`&&`). 5. Nothing in flight.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied:** the five CodeSha256 move and the publish-page policy carries the two bronze reads (read back with
  `get-role-policy`). The served 10-02 page is unchanged. On the next 07:00 ET publish (10-05), "source URL unavailable"
  appears only on PFOE's home-producer lines.
- **Not applied:** Monday's 07:00 ET page shows the x108 "source URL unavailable" until the 09:00 ET sweep. The Lambdas
  keep f122e4476b while the vehicle runs round 5's code from the CLOUD tree -- the split that M1 closes.
