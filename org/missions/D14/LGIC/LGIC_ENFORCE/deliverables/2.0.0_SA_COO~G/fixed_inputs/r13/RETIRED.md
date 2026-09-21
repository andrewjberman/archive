# RETIRED -- three CMDs in `check_en_r13.py` no longer measure what they claim

**This file is additive only. Not one byte of `check_en_r13.py` beside it has been touched.** It exists so
that a reader who opens this directory -- without first reaching the retiring record below -- learns the
retirement before trusting a green.

## What is retired, and why

Round 14's repair (`EN-r-7`) made `PLACEHOLDER_POPULATION_TABLE_R13.md` escape `{`/`}` to `(`/`)` through
one renderer, one rule. That repair is correct and STANDS. Its side effect: no column of the rendered
table carries a literal brace byte any more -- and `check_en_r13.py:74`'s `count_report()` identifies
R-38's placeholder population by regex-matching literal `{` bytes in that same rendered table. Round 14
zeroed the discriminator these three CMDs read the population off.

Three CMDs in `check_en_r13.py`, **all sharing `count_report()` at line 74**, are RETIRED:

- **`p37-population`** -- re-counts the population against the rendered table. Since round 14, this
  returns a clean 0 that DISAGREES with the record's own hard-coded 1303, so it FAILS loudly
  (`FAIL-P37-POPULATION`).
- **`p37-tokens`** -- re-counts the distinct placeholder tokens off the same broken re-count. Also FAILS
  loudly since round 14 (`FAIL-P37-TOKENS`).
- **`p37-producers`** -- the silent hazard this project's round 16 exists to catch: `core_producers()`
  computes `silent = tokens_measured - attributed - unattributed`. With the broken `count_report()`
  returning `tokens_measured={}`, `silent` is trivially empty no matter what the record claims, so this
  CMD **PASSES** -- a clean, denominator-bearing agreement with a broken instrument
  (`PASS-P37-PRODUCERS`). **This is the one a runner who never reads this file will not see.**

## The retiring record

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/DISCRIMINATOR_SWEEP_R15.json`
(committed `a08f5000ac`, round-15 cell `EN-d-1`) is the record that retired these three CMDs, after an
unscoped repo-wide sweep (44 hits / 36309 files scanned) traced every reader of the rendered table forward
to its consumers. Its companion narrative is
`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/discriminator-sweep.r15.result.md`.
Round 15's L9 (`3.0.0_SA_CVO` @`c6ac61b33a`) confirmed the residual this marker exists to close: *"'RETIRED'
is a fact about the sweep record and not a fact about the instrument ... a reader who reaches the instrument
without reaching `DISCRIMINATOR_SWEEP_R15.json` gets a green from a detector the estate has formally
retired."*

## What a real re-point needs, and why it is not done here

A working re-point exists in principle: point `count_report()` at the raw `canonical` field of
`NAMING_CENSUS_REPORT.r13.md`'s fenced JSON rows (verified to carry the literal `{token}` on exactly 1303
of 3264 rows) instead of the rendered, now-escaped table bytes. Making that real means editing
`check_en_r13.py` -- a **PINNED FIXED INPUT OF A CLOSED ROUND**. Editing it after round 13's proofs were
pinned against it is the exact stale-proof hazard this project runs an arm for; round 15's L9 named it in
these words: *"it would ACTIVELY ENDANGER something graded."* So the re-point is **not made here**. It is
named for this fixed input's owner, `2.0.0_SA_COO~G`.

## What this marker does NOT close

**This file does not stop `p37-producers` from returning PASS.** Anyone who runs the CMD directly --
without first opening this directory -- still gets a green. This marker raises the floor for a reader who
opens the directory; it does not change the instrument's own output.
