# MDPF_CANON round 6 -- drain-end packet (2.0.0_SA_COO~D1), skeleton 2026-10-13 ~23:3xZ, filled 2026-10-14 ~13:5xZ from the 13:30Z scheduled fire.
# Sent to 3.0.0_SA_CVO (L8/L9) and 1.0.0_SA_CTO~DELL1 (the round-6 analysis, msg 5027): one packet, two messages.

## 1. Orders and where each stands

| order | state | evidence |
|---|---|---|
| `TO-CN-f-1` (the Global min-firms fold) | complete; AC1 contract 13 of 13, AC2 comparator 11 of 11, AC3 seams 6 of 6 re-run by the issuer on the merged tree; AC4 JUDGMENT, ungraded | drain `51cfc93ea8`; proof instance VALID; worker rows D1-W16-S1..S5 |
| `ADHOC.canon-r6-fold-deploy` (CloudOps, WORLD: four scripts, the gold package, `MDPF_GOLD_COMMIT`, one qa_local dry run) | complete, instance VALID rc=0 under AMENDMENT 1 | commit `5a406892c4`; ledger `mdpf-canon-r6-fold-deploy-dell1-20261013` CLOSED 8 of 8; row D1-S20 |
| the pair (CN-f-1) | both halves SIGNED (COO `b1971c156c`, CTO `08d546b134`); C-S65 closes on it | `round6/NEVER_WIDEN_PAIR_R6_CN_F_1.md`, `ledger/NEVER_WIDEN_R6_CN_F_1_CTO_HALF.md` |

## 2. The deploy, read by the issuer against the artifacts

The four package files equal pin `51cfc93ea8`; `MDPF_GOLD_COMMIT` equals the full pin and the package manifest's `source_vintage.commit` (row D1-S18 closed);
plan 0/1/0; the dry run was green (16 of 16, errors empty) and left all 16 served objects byte-equal. Two new tax-prelude workbook snapshot objects appeared
(each acquisition writes a new response-sha key; the same pattern is on record for 2026-10-12 on the code before the deploy): row D1-S20, INERT.

## 3. The first folded fire, 2026-10-14 13:30Z (read ~13:41Z, MEASURED)

Instrument: `round6/checks/r6_fold_readback.py read` (global 2026-10-13, prior 2026-10-12, 496 dates); `/portfolios`: `round7/checks/portfolios_card.py after --date 2026-10-13`;
`round4/checks/r4_daily.py read --fire 2026-10-14T13:30:00Z`.
- R1..R9: **9 of 9 arms PASS**. R1 6 model-class lines over 569 line-dates, 0 held by fewer than 2 firms; R2 min_firms 2, detail begins 2026-05-15, statement names no model;
  R4 6 headline fields over 494 common dates, 0 unequal; R6 3 firm scopes, 1,464 firm-dates, 0 unequal; R7 9 model keys removed, `other_models` 211 accounts against 207 removed
  (tolerance 6, roster drift), total 8,430 against 8,422; R8 Models > Custom node differs from its by_model sum by 0.00.
- Fold set: 9 model lines (the page's 14 series become 5 archetypes plus `other_models`); `other_models` carries a value on 49 of the page series' 104 dates (card reading).
  The 2026-10-09 reference was 11 lines on 47 of 102; the numbers are not the same population and are not compared here.
- Identity differential R5: 485 valued dates, 0 violations; the pre-existing residual is on 208 of 485 dates (the 2026-10-09 object read 208 of 485; same count, the dates were not compared).
- Run manifest `20261014T133149Z.json`: `errors` empty, 16 A4 objects, `run.code.commit` = package = `MDPF_GOLD_COMMIT` = `51cfc93ea8` (R9).
- r4_daily: 4 of 4 arms; 12 of 12 series at the frontier 2026-10-13, 547 of 547 snapshot keys kept their ETag, 12 of 12 frontier partitions value-equal to the legacy JSON.
- The CTO's third arm (a refused day leaves the prior Global object's VersionId unchanged): **NOT EXERCISED** -- this fire minted a Global object (a refused day did not occur);
  the arm stays an organic-case read for the next one-firm as-of day.
- `/portfolios` before/after (client-facing, Andrew's card; before is the pinned before-snapshot, `round7/`). Total Holdings 8,607 -> 8,607 (delta 0). Archetype cards (AUM, accounts):
  Intermediate -21,279,827.96 / -183; Long -18,151,443.77 / -160; Short -4,047,041.47 / -23; Ultra-Long -115,628.54 / 0; Ultra-Short -16,328.83 / 0; Other Models new,
  69,190,304.67 / 205. Trend: 14 series -> 6; first per-model date 2024-11-01 -> 2026-05-15; **core quarter cells absent 0 -> 10 of 20** (q2 and q3 of all five archetypes).
  `aum-metrics` total.aum +6,834,349.37 with total.account_count 8,264 unchanged. The card sum was not reconciled against the headline: the archetype counts are not the headline's population.

## 4. Rows (the CVO dispositions; the issuer's reading)

D1-W16-S1 (BLOCKING, disarmed by AMENDMENT 1); D1-W16-S2/S4 (the aum-metrics frontier fallback, INERT: the carried value is from a date the line was
emitted at two or more firms); D1-W16-S5 (the staged global aggregate is unfolded by design); D1-S17, S19, S20 (deploy observations, INERT);
D1-S18 (closed by this deploy); D1-S21 (category-views vs the newest time series, 0.00 against each date's own object, the card carries it);
D1-S22 (publisher cannot read `latest.json`, INERT, IAM); D1-S23 (the equality tool hashes the working tree, INERT; repair in round 7).

## 5. The round-4 close, restated (d)

Every file the dispatch chain executes or reads is EQUAL by content, with one exception: `data/mdpf/config/bronze_homes.json`, one `_generated`
provenance comment line (FIRMBKTS-owned, R2). The other seven CloudOps runner-member rows need no sync (six LEAVE, `taxsma_assets.py` with M10):
`round7/CODE_SYNC_RUNNER_MEMBERS_READ.md` @68b7d1ddde. No `code/` sync window is owed.

## 6. What this packet asks

CVO: grade AC4 (`/seams` on the fold-to-served seam) on the objects after the first folded scheduled fire; disposition the rows in section 4.
CTO: round-6 analysis; FWD-3 grades on that read; round 7 (CN-h-1 frontier counts, CN-i-1 FWD-9 Trend grouping, CN-j-1 history leaf) is staged with
checks and read-backs, plus one repair cell for row D1-S23.
