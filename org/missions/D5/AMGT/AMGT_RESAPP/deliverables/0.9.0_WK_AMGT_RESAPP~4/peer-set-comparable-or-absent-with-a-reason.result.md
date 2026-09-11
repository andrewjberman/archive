# AMGT_RESAPP.TO-AMGT-s-8 -- session log

Worker: `0.9.0_WK_AMGT_RESAPP~4`. Worktree: `wk-AMGT_RESAPP-1-4`, cut from
`SITEZ @f8c76bd3a4`.

## AC1 -- F6 re-measured first

Invocation: `python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/f6_remeasure.py`,
run at 2026-09-11T00:05Z:

```
F6 RE-MEASURED: stale-set 48 / own-set 4 / no-CSC 2 of 54 workbooks; vintage 2026-09-11T00:05Z
F6 CITED (brief @19ce7d5b4d, CRO method): stale-set 48 / own-set 4 / no-CSC 2 of 54 workbooks -- agreement: {'stale_set': True, 'own_set': True, 'no_csc': True, 'denominator': True}
```

AMGT-s-12's own committed AC3 output (identity-layer-the-root.result.md:72):

```
AC3: F6 RE-MEASURED: stale-set 48 / own-set 4 / no-CSC 2 of 54 workbooks; vintage 2026-09-10T23:20Z (unaffected -- CSC-sheet scoring never touched bloomberg_ticker)
```

**Agreement: AGREE** -- both runs partition the same 54-workbook denominator
identically (48/4/2); only the vintage stamp differs. This is the third read of the
same instrument (AMGT-s-11's distribution measurement, AMGT-s-12's own AC3, this run)
and all three agree.

**Side effect** -- filed as `AMGT_RESAPP-Z-W4-S1` (surprise-channel investigation
file, this project): running the script overwrites
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/f6_remeasure.json`
in place (`git diff` shows only `read_started_at`/`read_finished_at` moving from
`2026-09-10T23:20Z` to `2026-09-11T00:05Z`; every other field, including the
partition, is byte-identical). Not committed by this worker.

## AC2 -- the four tests

Invocation: `python -m pytest lib/research/peers/tests -q`

```
....                                                                     [100%]
4 passed in 0.57s
```

1. `test_shared_defect_refuses_two_non_telecoms_carrying_kpn_set` -- ASML
   (Information Technology) and AstraZeneca (Health Care) both carrying the
   unmodified 12-ticker KPN set -> REFUSE, pair named.
2. `test_shared_defect_admits_two_telecoms_carrying_kpn_set` -- KPN and Telefonica
   (both Communication Services) sharing the same set -> ADMIT (the difference arm).
3. `test_analyst_entered_set_marked_basis_analyst` -- `analyst_override` ->
   `basis == "analyst"`.
4. `test_subject_with_no_classification_yields_absent_with_reason` -- a synthetic
   model_block with no `GICS_SECTOR_NAME` figure -> `basis == "absent"`,
   `reason == "subject classification not in the landed record"`.

## AC3-AC6

- AC3: `python -c "..."` over the three real `peer_set_*.json` files: `peer sets 3 |
  bases ['absent'] | every set carries test+reason True | any absent without reason
  False`.
- AC4: same glob, KPN-ticker check: `derived or absent sets carrying a KPN telecom
  ticker 0`.
- AC5: `grep -r -c -i -E 'openpyxl|\.xlsx|xlrd|CSC' lib/research/peers/ | grep -v -c
  ':0$'` -> `0`.
- AC6: `grep -r -c -i -E 'blpapi|blp_client|ReferenceDataRequest|8194'
  lib/research/peers/ | grep -v -c ':0$'` -> `0`.

## Controls

### Mutant 1 -- the C-SHARED-DEFECT subgroup exemption

`.scratch/shared_defect_mutant.py` (not committed): the "same subgroup -> ADMIT"
exemption's `continue` replaced with `pass` (falls through to REFUSE regardless of
subgroup). Re-ran the AC2-test-2 fixture (two telecoms, same set) against both:

```
MUTANT (subgroup exemption disabled) telecom-case verdict: REFUSE violations: 1
REAL (unmutated) telecom-case verdict: ADMIT violations: 0
MUTANT-RESULT: FIRED-AS-EXPECTED -- the subgroup exemption is load-bearing for the difference arm
```

### Mutant 2 -- the F2 quota guard in engine.py

`.scratch/engine_mutant.py` (not committed): the `if not candidate_universe: return
absent(...)` guard replaced with `if False: ...` (dead code -- guard disabled). Called
against the real, current production input (`candidate_universe=None`, the state for
all three landed securities today):

```
MUTANT (F2 quota guard disabled) peers('BABA_US_Equity', model_block_dir=<real dir>): RAISED TypeError: 'NoneType' object is not iterable
REAL (unmutated) peers('BABA_US_Equity', model_block_dir=<real dir>): basis=absent reason="candidate universe not classified; a quota decision (F2) precedes derivation -- subject's own GICS_SECTOR_NAME='Consumer Discretionary' is known, but no other covered name in the corpus has been classified by the same field, so no candidate can be tested for membership"
MUTANT-RESULT: FIRED-AS-EXPECTED -- without the guard, today's real production call CRASHES instead of returning the guard's own honest basis=absent
```

### Determinism

Two full runs each of `engine.peers()` (all three real security_keys) and
`shared_defect.check()` (the AC2-test-1 fixture), `vintage` masked before comparison:

```
engine.peers() x3 securities, run1==run2 (vintage masked): True
shared_defect.check() x1 fixture, run1==run2: True
DETERMINISM: STABLE
```

## The derived path, exercised against a synthetic candidate universe

Not run against the real corpus at this cut (classifying it is F2's quota decision,
not spent here) -- exercised once to confirm the mechanism is correct, so a second
engineer reading `engine.py` and this log has a concrete, checked example of what
"derive" does once a classified pool exists:

```
basis: derived
members: ['PDD US']
reason: derived from a classified candidate universe of 4 name(s): same GICS_SECTOR_NAME='Consumer Discretionary', market-cap band 0.2x-5.0x of subject's CUR_MKT_CAP=269839299644.40002
EXERCISE-RESULT: derived path produces the expected classification+cap-band-filtered set
```

(Candidate pool: PDD US same sector, cap ratio 0.556x -> included; JD US same sector,
cap ratio 0.148x -> excluded, out of the 0.2x-5.0x band; BA US -> excluded, wrong
sector (Industrials); TOOSMALL US -> excluded, cap ratio 0.0037x, out of band.)

## Commits (this worktree, branch `wk-AMGT_RESAPP-1-4`)

1. Status flip `staged` -> `pending`.
2. `lib/research/peers/` (engine.py, shared_defect.py, __init__.py, tests/), the
   surprise row, and the deliverables in this folder (build_peer_sets.py, the three
   `peer_set_*.json` outputs, `SPEC_SECTION_peers.md`, `README.md`, this log).
3. The proof-of-spec instance + status flip to `complete`.
