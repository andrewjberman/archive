# NEVER-WIDEN -- COO HALF, ADDENDUM 12: a home-producer report's trace panel names its file (round-6 cell 6, PFOE x26), at pin CLOUD 722f0db291

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~14:1xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-12 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-11. Every gate, key and condition stands.

**Why:** the round-5 analysis section 4 cell 6 (@56c99763bb), done under the FAST lease so round 6 need not cut it. Diagnosed
13:2xZ: a home-producer report (PFOE, IDVZ) has no bronze file by design. Its rows carry `source_channel` and `silver_uri`.
`render._source` knew only issuer URLs and Bloomberg captures, so the served 10-02 page shows "source URL unavailable (bronze
sidecar unreadable)" on PFOE's 26 trace rows: a read failure that never happened. Code @fd95d02955, drained 722f0db291.

## VERDICT: SIGNED (at pin CLOUD 722f0db291)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** (`/c/tmp/rv_apply13.tfplan`, from `/c/tmp/rv-fast` with HEAD = CLOUD HEAD
722f0db291): the five Lambdas' `source_code_hash` + `last_modified` only; no policy change. Package diff vs the deployed
8075f97ffb: `publish_page.py` (`_fund_files` carries source_channel + silver_uri), `render.py` (`_source` names the home
producer's file).

## THE SERVED DELTA, MEASURED (page day 2026-10-02)

Overlay publish at 722f0db291's code over the served inputs vs the served fast-a1-publish-1002e:
- 26 cells change from "source URL unavailable (bronze sidecar unreadable)" to "Opal home producer file
  (positioning-landing:constituents_issuer_fill s3://opal-data-etfs/bbg/<d>/constituents/constituents_issuer_fill.parquet)";
- 1 line changes: the G0 map date (10-01 -> 10-02), data any republish reads (addendum 11's measurement);
- 0 other lines. Status OK, 13 of 13; 1,572,426 -> 1,575,052 bytes. No A1, AI or check-verdict change.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| N1 | the five stage Lambdas' code | 8075f97ffb (daily WVmRehX8.., fetch irjW3iW9.., canonical hsHgpvG1.., silver ryWkldhF.., publish qetjE6bi..) | in place to 722f0db291 | re-apply from a tree at 8075f97ffb |
| N2 | platinum page 2026-10-02 | batch fast-a1-publish-1002e | republished ONCE, batch fast-a1-publish-1002f, no `refresh_a1` | prior page kept under `revisions/<ts>/` |
| N3 | every later scheduled run | runs 8075f97ffb | runs 722f0db291 | N1's rollback |

No gold object is written.

## ACT-START GATES

1. Plan exactly 0/5/0. 2. Live base equals N1's CodeSha256. 3. NEVER-2 entry `etfs-rivalfunds-fast-a1-r13` opened AND
committed before the apply (`&&`). 4. Nothing in flight. (Served changes resumed on Andrew's word 13:33Z, @74e6e01a5b.)

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied:** the served 10-02 page carries 0 "bronze sidecar unreadable" and 26 "Opal home producer file" cells. It is
  otherwise byte-equal to the measured overlay. 13 of 13.
- **Not applied:** the 26 cells keep the false "unreadable" reason until round 6 cuts cell 6.
