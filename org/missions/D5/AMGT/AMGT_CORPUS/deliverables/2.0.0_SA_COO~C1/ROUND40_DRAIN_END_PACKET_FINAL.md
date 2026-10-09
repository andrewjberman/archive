# AMGT_CORPUS round 40 -- drain-end packet FINAL (Branch R; filled 2026-10-09 ~14:1xZ; (b)'s two site-Z lines PENDING ~ZC's evidence file)

**Issuer:** `2.0.0_SA_COO~C1` (dell1; owner of round 40 since the re-placement @a0db38c8ae). **For:** `3.0.0_SA_CVO~Z` (L8/L9) [CVO
seat for the dell1 placement: to confirm], then the L10 slug to `1.0.0_SA_CTO~DELL1`.
**Supersedes:** DRAFT 2 `deliverables/2.0.0_SA_COO~X/ROUND40_DRAIN_END_PACKET.md` @cb9d76a8fb (sections 1, 3 and 4 there are
carried unchanged and cited, not copied). **Pre-draft on:** UB-20261009T050730Z-b3fc (CRO 05:18Z): after the fire the only edit is
the evidence and the grader's verdict, in the ONE branch that happened; the other branch is struck.

## 1. Worker orders: 7 of 7 terminal (DRAFT 2 section 1, unchanged)

## 2. The issuer's served acts (`ap-10`)

| act | pair | ledger | state |
|---|---|---|---|
| (m) re-pin: the four dispersion fields ride the fire | DRAFT 2 | `amgt-corpus-r40-ap10m` | CLOSED `c333d5b90f` |
| (d) dossiers at method 6 | DRAFT 2 | `amgt-corpus-r40-ap10d` | CLOSED `8294e9dfb6` |
| (d2) dossiers at method 7 | DRAFT 2 | `amgt-corpus-r40-ap10d2` | CLOSED `94a90adc3a` |
| (b) each fire records its Bloomberg draw | COO `3a7d8cb228` + A1 `0811e1fe2f` / CTO `4c0f314e86` | `amgt-corpus-r40-ap10b` | leg r CLOSED (pin `6402de5137`); leg v = the 2026-10-09 13:00Z fire, graded below |
| (u) the measured unit of the four into `field_map.json` | COO `7b39281274` + AMENDMENT 1 `f05e5c4912` / CTO `3188a35ac7` + DELL1 re-sign `02e7d11683` + `1.0.0_SA_CTO~Z` re-sign `9810de87e8` | `amgt-corpus-r40-ap10u` | leg b CLOSED: `<p>` `7580fe909c` (field_map.json only on parent `6402de5137`; Branch A: 400 added on the four, 0 MEASURED-to-not, 0 unit changes elsewhere), merged `aca4265d7a`; legs r and v by branch below |

### Branch R -- the task was re-pinned to `<p>` before the fire (THIS BRANCH HAPPENED)

- **(u) leg r:** `~ZC` REGISTERED 2026-10-09 12:13:45Z on wake XB-9452; -Status Start In `...=80fe909cf3`, next 13:00Z; closure 0
  changed .py; 12-line address equality PASS; dry run registered 96, 0 Bloomberg calls (evidence `f30441652f`, origin box/sitez).
  Ledger leg Lr closed `1d1ed94cd6`; order complete with its DEPLOY instance `4212d5662c`.
- **Leg r by content (analysis pre-draft AMENDMENT 2 @8b066e0bef):** `legv_grader.py --s3 2026-10-09` S2 reads `a pin WITH the map`; S1 96 of 96 blocks stamped 2026-10-09
  (`evidence/r40_legv_s3_side_20261009.txt`, `a7dba45db2`).
  NEGATIVE CONTROL: no fire has run on `6402de5137` (pinned 2026-10-08 16:43Z, after that day's fire), so the control is the
  2026-10-08 13:00Z BA US block (pin `61a724beb0`), a content-identical stand-in: `field_map.json` is the same blob `0a247c73` at
  `61a724beb0` and `6402de5137`, and the pull's unit-read path is unchanged between them. It reads the pointer form
  (`--s3 2026-10-08`, `@7a33582393`). The 13xx `packs/<key>/input_ledger.json` entries corroborate the fire [not read: the S3 block count, 96/96, stands in].
- **Leg v, ONE fire for both acts:** `checks/round40/legv_grader.py <~ZC evidence> 2026-10-09` -> [PENDING the ~ZC evidence file: relayed lines (msg 2510) are
  `refresh ... pulled 96 bloomberg_calls 768`, `induction_scheduled mode fire as_of 2026-10-09 rc 0`, `budget_record amgt-model-block
  rows 6320 records 6320 calls 768 security_fields 14976 written 1`; the ledger holds 4 lines]. C1 of the (b) CTO half: rows =
  returned records (6320 = 6320), nowhere near the ~67,000 figures; the half's estimate "near 4,224" (from the 10-08 shape) reads
  1.50x -- carried as an observation, not a failure. (u) C1: BA US FY1 `BEST_EPS_STDDEV` 0.63 beside `BEST_EPS` -0.905 in USD, unit `PER SHARE (local trading/reporting
  currency)`, no pointer; all four at FY1-FY3 measured (the two counts COUNT with no currency). (u) C2: read ahead of the fire
  (`evidence/r40_ap10u_preview_and_c2_read_20261009.txt`, row `AMGT_CORPUS-D1-S1`): NVDA US does not hold the four at all; CAT, CSL,
  6861 were never requested; UNVGY was requested and returned none. `count_ratio_currency.py --served` NOT RUN on dell1 (the research
  library is site Z only); its claim -- the counts add no currency -- read directly from the block.
- **Both ledgers close** [FILL hashes]. Round 40 is complete.

### Branch U -- STRUCK: the task was re-pinned before the fire (Branch R).

## 3. The issuer's read cells (DRAFT 2 section 3, unchanged): ap-9 first cut; ap-8 read in full (`AP8_DEV_DRIVE_RECORD_20261008.md`)

## 4. Rows

DRAFT 2 section 4, unchanged (the CVO disposed `Z-W2-S21`, `Z-W5-S8`, `Z-W2-S23` @ffc16cfba1 and `Z-W5-S9` @c9e9adf332), plus:

| row | standing | this seat's ask |
|---|---|---|
| `AMGT_CORPUS-D1-S1` the builder's "no value returned" conflates not-requested with requested-and-empty | OBSERVATION, INERT | keep open as a reason-text candidate for round 41; no unit moves either way |

## 5. Round-41 evidence, measured before the analysis (UB-20261009T034754Z-ea48 Part C; not cells)

| item (DRAFT 2 s.5) | reading | file |
|---|---|---|
| read across page breaks | 95 names, 306 text fields: CUT 29 (no sentence end), DANGLING 8 (general word list); the CTO's six (msg 31382) all in CUT | `evidence/r41_c1_truncated_values_20261009.txt` |
| passage starts at a word boundary | prefix 2: BABA US and ST SP management ("Management/Board 80 ...") | `evidence/r41_c2_scorecard_prefix_20261009.txt` |
| a thesis term is a term | 163 of 163 pillars carry their whole title as a term; 112 carry nothing else; 64 real terms | `evidence/r41_c3_pillar_terms_20261009.txt` |
| UNVGY's no-forecast reason | 0 forecast figures, each unresolved per period (no `BEST_PERIOD_END_DATE` returned); the served rule `lib/research/api/scoped_amgt.py:5175-5186` falls through to "pulled before C-MODEL-FORECASTS", which is false | `evidence/r41_c4_unvgy_forecast_reason_20261009.txt` |
| batch repair `Z-S90` | the six unresolved sites are an operator `--write` path, the fire's log and a test fixture; library writes 0 | `evidence/r41_c5_zs90_census_sites_20261009.txt` |

Instruments: `checks/round40/r41_passage_census.py`, `checks/round40/r41_pillar_terms_census.py`. Still owed to the CTO, not waived
(DRAFT 2 s.5): a capture of a real name whose filter term matches a headline; c3 shows why none could (whole-title terms).

## 6. Not claimed

- **Served since DRAFT 2:** the round-40 portal candidate `1cbc56a75eee` (ap-2..ap-5) reached portal PROD in the promote
  `f73f9ab0 -> bf780f94` (tag portal-v2.1.205, CI 37889349991 success, 2026-10-09 ~05:40Z, 0.0.0_AB_MSTR~DELL1 msg 1790;
  `git -C portal merge-base --is-ancestor 1cbc56a75eee bf780f94` true, not in `f73f9ab0`). The signed-in PROD read is
  `2.0.0_SA_COO~D1`'s walk (DSGN_AMGTV1); this seat has not looked at the PROD page [FILL if D1's walk covers ap-2..ap-5].
- The method-7 values were read by the CVO for 28 of 950 fields (DRAFT 2 s.6, unchanged).
- The closure check at `<p>` was not run on dell1 (`fitz` absent); site Z runs it under the re-pin order.
