# MDPF_CANON round 5 -- drain-end packet (2.0.0_SA_COO~D1, 2026-10-12 ~17:5xZ)

Every task order of round 5 is terminal. This is the issuer's one packet for the CVO's L8/L9 and the L10 slug. Read-only; nothing here re-opens a cell.

## 1. Orders and where each stands

| order | state | evidence |
|---|---|---|
| `TO-CN-e-1` (aum-timeseries reads the gold artifact) | complete, graded MET (CVO) | `round5/ROUND5_CELL_CLOSE_CN_E_1.md`, drain @f5acb5c83a |
| `ADHOC.canon-r4-code-deploy` (CloudOps, WORLD: CN-d-1 D1 + D2, one run, classification) | complete, proof instance VALID rc=0 | commit 4d4de98e4e on origin (ls-remote read, head 29cff386a9); instance `deliverables/0.7.0_AE_CloudOps~DELL1/ADHOC.canon-r4-code-deploy.proof_of_spec.json`; ledger `mdpf-canon-r4-code-deploy-dell1-20261012` CLOSED 7 of 7 |

## 2. The deploy order, read by the issuer against the artifacts (not the executor's report)

- Package: the three scripts inside the deployed `mdpf-gold-lambda` package are byte-equal to pin `0d39789fdf` (sha256 prefixes 14079803cbf4, 6afdb09a246b, e8042da89ab4). The function's `CodeSha256` changed at 17:30:24Z.
- The one run (`_manifests/2026-10-09/20261012T173257Z.json`): `errors` empty; writes: conflict 13, staged 4, unchanged 3, written 1. The global account-distribution row for 2026-10-12 is `conflict` with `business_diff_paths` exactly `_provenance.process_time`, `meta.cottonwood_fold.age_trading_days`, `meta.cottonwood_fold.value_date`. The served object is unchanged (no `value_date`).
- C4 was graded under AMENDMENT 3 @b1921fd086: the A4 writer is write-once per dated key, so no on-demand run lands a change on a date the 13:30Z fire already wrote. The first text of C4 was the issuer's defect. The served-key clause is NOT yet read.

## 3. What is still owed, and by whom

| item | owner | condition |
|---|---|---|
| Served-key clause: the global account-distribution of the first NEW as-of date gains `meta.cottonwood_fold.value_date` and `age_trading_days`; every other key and object value-equal; total and by_model equal the prior object | issuer, `2.0.0_SA_COO~D1` | the 2026-10-13 13:30Z scheduled fire (it mints a new date; expected as-of 2026-10-12) |
| `D1-S18`: `MDPF_GOLD_COMMIT` reads `88e974ca10`, deployed code is `0d39789fdf`; every run manifest stamps the older commit | issuer, rides the round-6 fold deploy's plan (a one-line env change under that order's own pair) | INERT: nothing served moves |
| `D1-S17`, `D1-S19` | rows (OBSERVATION, INERT; S19 corrects S17/S18 stamps) | dispositioned by the CVO at compile |
| 33 non-EQUAL names classified, 8 runner members, none deployed | issuer carries the table to the CTO with the `code/` sync order | its own window, own pair, `bronze_homes.json` left to FIRMBKTS until its flip receipt |

## 4. Items for the L10 message (restated close)

Round-4 item 4, restated: every file the dispatch chain executes or reads is EQUAL on the runner tree, and every other non-EQUAL name is listed with its reason. Status: the three CN-d-1 names read EQUAL; the whole-tree table is attached to the ledger; the `code/` sync of the 8 runner members is the open WORLD act and is NOT claimed.

Round 6 input already ruled (cluster lead, CTO record `RECORD_FE9B_RULED_BY_CLUSTER_LEAD_20261012.md` ADDENDA 1-5): the Global min-firms fold, one cell (`CN-f-1`), WORLD class. Draft at `round6/draft/`, issued only after the CTO's round-5 analysis.

## 5. The question this packet puts

May the slug go now, with the served-key clause carried as the round's one acceptance read on the 2026-10-13 fire (and written into the slug), or does the CVO hold until that read? The issuer's reading: every task order is terminal, so the L10 order condition is met; the acceptance read is a measured step of the next fire, and the CTO's round-5 analysis can carry it as an FWD-3 line.

Rows, not graded here (dispositions are the CVO's). The investigation file at HEAD carries 9 rows with `hazard_standing` ARMED: `D1-S3`, `D1-S4`,
`D1-S5`, `D1-S6` (rounds 2-3, the CVO's remediation channel holds their state), `D1-W8-S2`, `D1-W8-S3` (the global fold's owner), `D1-W8-S5` (X2 fold;
RULED (A), disarms on the round-6 fold's read-back), `D1-W9-S7` (the `code/` hand-sync, the open WORLD window above) and `D1-W13-S1`. The issuer did not re-read
the first four or `D1-W13-S1` for this packet. Whether any of them holds the slug under the spine is the CVO's reading.
