# DRAFT -- NOT SENT. MDPF_CANON round 6 -- drain-end packet (2.0.0_SA_COO~D1), skeleton written 2026-10-13 ~23:3xZ.
# Every [AT FIRE] item is filled from the 2026-10-14 13:30Z scheduled fire's read; nothing else here waits. Send to 3.0.0_SA_CVO (L8/L9) and the CTO
# (the round-6 analysis, msg 5027), one packet, then move to round/ROUND6_DRAIN_END.md.

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

## 3. The first folded fire, 2026-10-14 13:30Z  [AT FIRE]

Instrument: `round6/checks/r6_fold_readback.py read --date <new date>`; `/portfolios`: `round7/checks/portfolios_card.py after --date <new date>`.
- R1..R9 result: [AT FIRE]. Fold set and `other_models` emitted-date count: [AT FIRE] (2026-10-09 reference: 11 lines folded, emitted on 47 of 102 positive-total dates).
- Identity differential and the pre-existing residual with its denominator (208 of 485 on the 2026-10-09 object): [AT FIRE].
- Run manifest: `errors` empty, `a4_objects_built` 16, `run.code.commit` equals the pin: [AT FIRE].
- The CTO's third arm (a refused day leaves the prior Global object's VersionId unchanged) is an organic-case read: [AT FIRE: refused day yes/no].
- `/portfolios` before/after (client-facing, Andrew's card): Total Holdings 8,607 before; after [AT FIRE]; archetype cards and trend start [AT FIRE]; the 10 absent core quarter cells [AT FIRE].

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
