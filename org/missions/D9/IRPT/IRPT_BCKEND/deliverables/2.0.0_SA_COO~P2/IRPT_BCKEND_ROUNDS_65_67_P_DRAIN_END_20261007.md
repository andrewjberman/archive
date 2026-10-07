# L8 drain end -- IRPT_BCKEND rounds 65-67, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~13:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Every order of rounds 65, 66 and 67 is terminal and drained. Judgment criteria: 0 in all six orders. Each mechanical criterion was
re-run by the issuer on the shared tree after the drain.

## Round 65 -- the export read fails open (row W142-S4, PRIORITY)

| order | slot | drain | result |
|---|---|---|---|
| IB-pr-343 export receipt names its covered accounts | ~145 | @fb7e208d16; amendment 2 @75a4c2eaeb (fix @34f71024a1) | `export/entry.py` `_covered` refuses an empty account list (fail-closed); both ExportReceipt schemas require `facts.covered_account_ids` (minItems 1); amendment 2 logs one `irpt_export_read_admitted` line (opaque principal, export, covered account ids) per admitted receipt/download read and none on a refusal. IB65-1-AC1, AC2 and guard PASS; proof VALID. |
| IB-pr-344 backfill covered accounts, dry run | ~145 | @fb7e208d16 | `deliverables/0.9.0_WK_IRPT_BCKEND~145/IB65-2_backfill_census.json`. HOLLOW on the KMS-encrypted receipts: this identity lacks kms:Decrypt (row W145-S5). No `--apply` until it is re-run under an identity holding kms:Decrypt. |
| IB-pr-345 cross-scope read exposure | ~146 | @84bbbeca63 | `deliverables/0.9.0_WK_IRPT_BCKEND~146/IB65-3_exposure_census.json`. 0 cross-scope reads identified; NOT PROVABLE, because no read was logged before amendment 2. The live `irpt-export-render` is still fail-open (row W146-S1, ARMED). |

## Round 66 -- the print page refuses an unknown kind (CTO review msg 403)

| order | slot | drain | result |
|---|---|---|---|
| IB-pr-346 | ~147 | @39b7d4dbce | `readReportKind` refuses any kind it does not know; `custody-report` and an unknown kind are refused with 0 requests; tsc -b and eslint rc 0. The CTO PASSED it. The portal commits are waiting on Andrew's word to land on DEV (row S365). |

## Round 67 -- reach, and null-likes

| order | slot | drain | result |
|---|---|---|---|
| IB-pr-347 who can reach the export read now (CTO msg 525) | ~148 | @1b4348496c | `deliverables/0.9.0_WK_IRPT_BCKEND~148/IB67-1_export_reach.json`: **non_opal_reach = 7 of 52 principals read** (6 limited-grant 49financial advisors, whom the fail-open branch widens, and 1 cottonwood admin, whom it does not widen past the firm). The routes can be called directly through the API: the App.tsx gate is client-side only, and the gateway authorizer admits any valid human JWT. This is an offline resolver run, a point-in-time snapshot taken with no token minted. IB67-1-AC1 and guard PASS; proof VALID. |
| IB-pr-348 null-like guard is case-insensitive (E-P8 criterion 4) | ~149 | @6300aa6122 | `_ids/ids.py` treats '', none, nan and null in any case as unmapped; `_ids` 48 passed. IB67-2-AC1 re-run PASS at HEAD. Side effect: IRPT_CUSTDY's refusal-tracer test has no refusing spelling left (row IRPT_CUSTDY-S10, owned by ~K2, INERT; the repair is to retire the test). |

## Rows and what stays open

- **W148-S1** (BLOCKING, ARMED): 7 non-Opal principals reach a fail-open read. Per CTO msg 525 this is a security exception, and
  the COO asked for an emergency laptop release of IB-pr-343 by hash under both halves (message 20261007T125826Z to
  `1.0.0_SA_CTO~DELL2`). Disarm: the release's after-read shows the deployed `_covered` refusing an empty list.
- **W148-S2** (OBSERVATION): this dell2 identity read the cot ownership map and directory, which contradicts fence row S347. Nothing
  was widened.
- **W146-S1** (ARMED) disarms with the same release. **W145-S5**: the backfill has to be re-run under kms:Decrypt before `--apply`.
- **Push state:** LOCAL. ls-remote origin CLOUD read ce19192c3f; neither @34f71024a1 nor @1b4348496c is on origin.
