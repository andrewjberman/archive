# L8 drain end -- IRPT_DASHBD rounds 15-17, workstream B

**Issuer:** `2.0.0_SA_COO~P` (rounds 15-17); packet written by its dell2 successor lane `2.0.0_SA_COO~D2`, because ~P closed
its session without one | **Date:** 2026-10-07 ~07:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @dd13e99394

All four orders of these rounds are terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, run by this seat for
DB-b-25; the others as the issuer's drain recorded them). 0 JUDGMENT criteria. Watermark of the last compile: 2026-10-04T23:59Z
(REMEDIATION_v5 @6cb0cf8474, rounds 12-14). No order of IRPT_DASHBD is open. No worker branch or worktree of this project exists
(`git branch --list 'wk-IRPT_DASHBD*'`: 0). The adopted-branch inventory (@83d5e34919) lists no IRPT_DASHBD branch.

## Orders

| order | round | drain | criteria | real run / served state |
|---|---|---|---|---|
| DB-b-23 (routes.json declares both live reporting routes, S23) | 15 | @487429cb60 (worker ~9 @ca3d31ae49) | DB15-1-AC1/2/3 PASS under amendments 1 (@a414382a19) and 2 (@bf68fca0ed) | contract inventory only; no served byte moved. The two routes are ROUTED_ELSEWHERE, so the api Terraform root (which builds from DECLARED rows) creates nothing new |
| DB-b-24 (commit the E3 shape ruling and first pull record) | 15 | @28efce5b4d (worker ~10) | DB15-2-AC1/AC2 PASS | a record commit |
| DB-b-25 (the concurrent BD runner never stops silently) | 16 | direct act @98d439936a (no worktree: 1.6 GB disk), amendment 1 @91a4d48e89 | DB16-1-AC1/AC2 PASS; instance @16c21b63db and flip @8ef3439f7b by `2.0.0_SA_COO~P2` | deliverables runner only; relaunch 3 had already loaded the old runner (amendment 1), so the fix serves later runs |
| DB-b-26 (E2 tie-out of 49F served total return vs Black Diamond) | 17 | @0685c40ec0 (worker ~12) | DB17-1-AC1..AC3 PASS, re-run by the issuer | 9,082 planned = 9,078 graded + 4 BD_NO_VALUE; 2,103 within 0.35 pp, 6,975 outside, each with a closed-set reason (UNEXPLAINED 6,250, of which 4,905 fall within tolerance once BD's own fees are netted). 0 vendor calls |

## Other acts in the window

- Ledger `irpt-dashbd-e3-bd-population-pull-20261004` CLOSED @fbc0ee59df: leg P1, 5,252 of 5,252 landed (@54cbe5a477); leg G1,
  the DB-b-26 tie-out.

## Rows surfaced after the watermark (6)

| row | class | standing |
|---|---|---|
| W9-S1 | BLOCKING, ARMED | resolved by DB-b-23 amendment 1; DISARMED by S26 (@dd13e99394, re-measured at HEAD) |
| W9-S2 | OBSERVATION, ARMED | DISARMED by S26 (api/routes.tf filters on DECLARED) |
| W9-S3 | OBSERVATION, ARMED | resolved by DB-b-23 amendment 2; DISARMED by S26 (_contracts 190 passed) |
| W10-S1 | OBSERVATION, INERT | OPEN: W7-S1 described an older bearer line; the ruling file now names batches 248 and 249 |
| W12-S1 | OBSERVATION, INERT | OPEN: the 6,250 UNEXPLAINED segments; fees are not in the closed reason set. A methodology question for the CTO's round-N analysis |
| S26 | OBSERVATION, INERT | the disarm row above (`adjudicates` W9-S1..S3) |

The laptop holds six untracked JSON files under `deliverables/0.9.0_WK_IRPT_DASHBD~7/` and `~8/` (inventory @83d5e34919). They are
not on origin and are not read by this packet.
