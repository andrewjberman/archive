# AMGT_CORPUS round 40 -- drain-end packet FINAL (PRE-DRAFT, 2026-10-09 ~05:3xZ; two branches; filled after the 13:00Z fire)

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
| (u) the measured unit of the four into `field_map.json` | COO `7b39281274` + AMENDMENT 1 `f05e5c4912` / CTO `3188a35ac7` + DELL1 re-sign `02e7d11683` + `1.0.0_SA_CTO~Z` re-sign [FILL: hash or ABSENT] | `amgt-corpus-r40-ap10u` | leg b CLOSED: `<p>` `7580fe909c` (field_map.json only on parent `6402de5137`; Branch A: 400 added on the four, 0 MEASURED-to-not, 0 unit changes elsewhere), merged `aca4265d7a`; legs r and v by branch below |

### Branch R -- the task was re-pinned to `<p>` before the fire (strike if Branch U)

- **(u) leg r:** `~ZC` report [FILL: time registered, -Status Start In `...\7580fe909cf3`, closure + addresses equal]; ledger leg Lr
  closed [FILL hash].
- **Leg r by content (analysis pre-draft AMENDMENT 2 @8b066e0bef):** `legv_grader.py --s3 2026-10-09` S2 reads [FILL: `a pin WITH the map`].
  NEGATIVE CONTROL: no fire has run on `6402de5137` (pinned 2026-10-08 16:43Z, after that day's fire), so the control is the
  2026-10-08 13:00Z BA US block (pin `61a724beb0`), a content-identical stand-in: `field_map.json` is the same blob `0a247c73` at
  `61a724beb0` and `6402de5137`, and the pull's unit-read path is unchanged between them. It reads the pointer form
  (`--s3 2026-10-08`, `@7a33582393`). The 13xx `packs/<key>/input_ledger.json` entries corroborate the fire [FILL count].
- **Leg v, ONE fire for both acts:** `checks/round40/legv_grader.py <~ZC evidence> 2026-10-09` -> [FILL: `legv build k/3`, the L1/L2/L3
  lines, the ledger lines and spent]. (u) C1: BA US FY1 `BEST_EPS_STDDEV` [FILL value] beside `BEST_EPS` [FILL value] in [FILL
  currency], unit [FILL: expect `PER SHARE (local trading/reporting currency)`, no pointer]. (u) C2: read ahead of the fire
  (`evidence/r40_ap10u_preview_and_c2_read_20261009.txt`, row `AMGT_CORPUS-D1-S1`): NVDA US does not hold the four at all; CAT, CSL,
  6861 were never requested; UNVGY was requested and returned none. `count_ratio_currency.py --served` [FILL: `crc served build 1/1
  control 1/1`].
- **Both ledgers close** [FILL hashes]. Round 40 is complete.

### Branch U -- the fire ran on `6402de5137` (strike if Branch R)

- **Why not re-pinned:** [FILL: no `1.0.0_SA_CTO~Z` re-sign by 12:30Z / no `<p>` at site Z by 12:45Z / an equality check unequal /
  `~ZC` did not act]. The fallback of both CTO halves; nothing served moved.
- **(b) leg v:** grader as above [FILL]; ledger `amgt-corpus-r40-ap10b` closes [FILL hash].
- **(u) carried:** legs r and v wait for the next fire under the original order (leg 0 = (b) leg v, now met). `amgt-corpus-r40-ap10u`
  stays OPEN with Lb closed; the re-pin order stands for the 2026-10-10 window. Round 40 closes with (u) named as the one carried act.

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
