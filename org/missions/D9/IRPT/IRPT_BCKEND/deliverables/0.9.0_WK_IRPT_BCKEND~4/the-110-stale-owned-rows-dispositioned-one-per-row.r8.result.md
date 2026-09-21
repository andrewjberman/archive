# IRPT_BCKEND.TO-IB-rth-4 -- RESULT

**Serial:** `0.9.0_WK_IRPT_BCKEND~4` · **Cell:** `IB-rth-4` · **Round:** 8 · **Worktree HEAD at write time:** `4009c22cf551234d9b82c79e7e48b532665cff48`

## (a) ENUMERATION -- RE-MEASURED, NOT INHERITED

Instrument: `srg._stale_open_row(srg._remediation_rows_for_project(root, "IRPT_BCKEND"), current_round=8, srg.STALE_OPEN_ROW_N_ROUNDS)` -- the gate's own resolver, called directly (`.tools/surprise-row-gate.py`), never re-derived.

- Total remediation rows (latest per id): **168**
- `STALE_OPEN_ROW_N_ROUNDS` = **2** (read from the gate, never hand-typed)
- Re-measured **at round 7** (for comparison against the disclosed figure): **110** -- exactly matches the round-7 gate's nine-times-disclosed count, confirming the instrument is the same one that produced "110".
- Re-measured **at round 8** (this cell's own write time -- IB-rth-4 is itself a round-8 cut): **150**

**THE GATE'S "110" WAS ALREADY STALE BY THE TIME THIS CELL RAN.** The set grows with the round number by construction (the same shape LGIC_ENFORCE's analogous cell `EN-b-42-r9` measured: 91 at round 8's register, 94 re-measured at round 9's own cut). **THE CELL'S DENOMINATOR IS 150, NOT 110.** Every later count in this record is `N of 150`.

Full id set: see `DISPOSITION_R8.json` -> `stale_ids` (150 entries, sorted).

## (b) DISPOSITION -- ONE PER ROW, NEVER A SWEEP

**Method (per row, no bulk close, no age close):**
1. Structural check: is there a LATER remediation row (in this project's own append-only channel) that closes this id? By construction, NO -- `_remediation_rows_for_project` returns the LATEST row per id, and all 150 of the measured ids resolve to a row whose `remediation.state == "OPEN"` as that latest row. A closing row, had one existed, would have made the id fall OUT of the stale set entirely (state != OPEN), so its absence from a smaller set is not evidence -- the id's continued PRESENCE in the 150 is the evidence that no closing row exists.
2. Independent live-evidence probe: citations were extracted from every row's own `mechanism`+`remedy` text (`path.ext:NN` patterns) and checked for existence in the worktree at HEAD. **This probe was found UNRELIABLE as resolution evidence** and is NOT used to assert any DISARM: only 19 of 150 rows cite a path that resolves to a real repo file at all (most citations are lambda-relative shorthand, e.g. `holdings/entry.py` rather than the real `infra/aws/lambda/investor-reporting/holdings/entry.py`), so a "missing" result reflects the probe's wrong grain, not removal/resolution. Per the order's own bound ("DISARM only with EVIDENCE the hazard is resolved") and CLAUDE.md's "a false complete is far worse than a stale pending", **no DISARM is asserted on this signal.**
3. Authority check, read from EACH row's OWN schema fields (never invented, never uniform by fiat): for `hazard_standing == ARMED` rows (125 of 150) the schema's `disarm` block names `disarm.owner`; for `hazard_standing == INERT` rows (25 of 150, no disarm block) the same discipline reads `remediation.owner` (== the row's own `owner` field, "the lane that builds the remediation" per `remediation_row.schema.json`). **In every one of the 150 rows this owner token is `2.0.0_SA_COO~B` (113 rows) or `1.0.0_SA_CTO` (37 rows) -- NEVER this cell's own serial.** 40 of the 150 (all round-v6 rows) carry the graduation protocol's own explicit boilerplate stating it in words: *"its DISARM stays `<owner>`'s own act ... disarming is not disposing (R-19/R-21). No part of this row's substance is re-decided by [this cell]."* The remaining 110 rows carry the identical structural fact without the literal sentence (the schema's `disarm`/`remediation` owner field IS the discipline, sentence or no sentence).

**RESULT: 150 of 150 rows disposed CARRIED**, owner = that row's own `disarm.owner` (ARMED) or `remediation.owner` (INERT) leading serial token, verified to parse as a real seat serial for every row (0 unextractable). Zero DISARMED (no reliable resolving evidence found for any row). Zero STAYS-ARMED (every row carries a named, addressable owner in its own schema fields -- the STAYS-ARMED default is for a row with NO special-authority holder, which none of these 150 are: each one's OWN record already names who must act, which is exactly the CARRY test the order states -- "a row whose disposition needs another seat's authority ... recorded as CARRY with the owner named").

Per-row table, denominator, and coverage assertion: `DISPOSITION_R8.json` (committed) and `battery_ib_rth_4.py`'s printed table (re-derives live and cross-checks against the committed record on every run).

## (c) REPORT

```
DENOMINATOR:   150 (re-measured at round 8, this cell's own write time)
DISARMED:      0 of 150
STAYS-ARMED:   0 of 150
CARRIED:       150 of 150  (113 -> 2.0.0_SA_COO~B, 37 -> 1.0.0_SA_CTO)
SUM CHECK:     0 + 0 + 150 == 150 -> True
```

R79-AC1: every row in the 150-row denominator carries exactly one disposition (CARRIED) with its own evidence (no closing row exists + the row's own owner field + a mechanism excerpt, per-row, never templated to a blanket sentence) and a real owner token. Counts sum to the denominator. **PASS-by-output** (`battery_ib_rth_4.py`, token `IBR79-EVERY-ROW-DISPOSITIONED-COUNTS-SUM-TO-DENOMINATOR`).

## WHAT THIS CELL DID NOT DO

- No source, build, deploy, apply, or served change (records-only, as bound).
- No row was closed by age -- the AGE-ONLY reason pattern is refused by the battery itself (mutant-tested).
- No bulk close -- every row's disposition line cites that row's own mechanism excerpt and owner field; the battery cross-checks coverage id-by-id.
- No new channel row was written: zero DISARM rows were warranted by the evidence found, so `surprise-channel/remediations/` is untouched by this cell (the `<paths>` grant covers it for exactly the DISARM case, which did not arise).

## CONTROLS

- **Mutant** (3 arms, all FIRED-AS-EXPECTED): (1) blanking one row's `reason` -> battery FAILs "carries an empty evidence/reason"; (2) replacing one row's `reason` with a bare age statement ("stale 2 rounds") -> battery FAILs "reads as AGE-ONLY ... NO ROW CLOSED BY AGE"; (3) dropping one row's disposition entry entirely -> battery FAILs "carr[ies] NO disposition entry". Record restored byte-identical after each arm (verified: clean re-run afterward reproduces the original PASS output).
- **Determinism**: two consecutive clean runs of `battery_ib_rth_4.py` produce byte-identical stdout (165 lines, `diff` empty).
