# EN-m-2 round 16 -- the retired-marker, result record

## 1. What this cell does, and its honest limit

`3.0.0_SA_CVO`'s round-15 L9 named a residual: `p37-producers` is RETIRED in a record but still runs from
the tree and still returns PASS. This cell adds an ADDITIVE `RETIRED.md` sibling beside `check_en_r13.py`
so a reader who opens `fixed_inputs/r13/` learns the retirement without a byte of the pinned checker
being touched. **It does not stop `p37-producers` from returning PASS to a runner who invokes the CMD
directly.** It raises the floor for a reader who opens the directory; it does not change the instrument's
own output. That sentence is required by the order and is repeated here.

## 2. What was retired, and by what record

Three CMDs in `check_en_r13.py`, all sharing `count_report()` at line 74:

- `p37-population` -- FAILS loudly since round 14 (re-counts 0 vs the record's hard-coded 1303)
- `p37-tokens` -- FAILS loudly since round 14 (re-counts 0 distinct vs the record's 9)
- `p37-producers` -- **PASSES silently** -- the exact hazard this round exists to catch

Retired by `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/DISCRIMINATOR_SWEEP_R15.json`
(committed `a08f5000ac`), because round 14's escape-everywhere repair (`EN-r-7`) zeroed the brace
discriminator these three CMDs read the population off.

## 3. The blob pair -- the criterion that proves additivity

`check_en_r13.py`'s round-13 pin is `c2865743ed` (`git log --follow` on the file returns exactly one
commit -- the round-13 L6 issuance -- so the file has never been touched since):

```
$ git rev-parse c2865743ed:org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r13/check_en_r13.py
80da489681358bb7650ee6f1092ad09b3aa90eef
$ git rev-parse HEAD:org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r13/check_en_r13.py
80da489681358bb7650ee6f1092ad09b3aa90eef
```

IDENTICAL. Not one byte of the pinned fixed input moved.

## 4. A BLOCKING gap: the marker file itself is not committed

**This is the one thing this record cannot dress up as clean.** The order's BOUNDS prose grants
`fixed_inputs/r13/RETIRED.md` in these words: *"the ONE new file
`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r13/RETIRED.md`, and this
order's own file. Nothing else."* But the order's own mechanical `<paths>` XML block -- the only thing
`.tools/owned-paths-validate.py` reads -- carries exactly one line, the investigation file, and does not
name `RETIRED.md`. `safe-commit.sh` refused the commit (rc=1) citing `ADHC_OWNPTH.005`: *"no NON-TERMINAL
task order at HEAD issued_to this serial names this path in its `<paths>` block ... a missing path is a
cut defect, never an override."*

Per operating instructions this is a BLOCKING row, never an override and never a widened grant taken
unilaterally: filed as `LGIC_ENFORCE-W1-S106`, ARMED, disarm owner `2.0.0_SA_COO~G` (the order's issuer,
who owns the `<paths>` grant). `RETIRED.md` exists on disk in this worktree at the correct sibling path,
full text quoted in this instance's `declared_exclusions`, but is **not in git** as of this record's pin.

`RETIRED_MARKER_R16.json` -- the RECORD describing the marker -- IS committed (already granted under this
worker's own `deliverables/` folder), and the three mechanical criteria PASS against it, exactly as the
order predicted: *"it takes your two blob hashes on trust ... it does not open RETIRED.md."* `M2R16-AC4`
at L9 is where this gap is visible, and this record says so rather than letting a mechanical PASS imply
more than it proves.

## 5. Criteria table

| id | verdict | invocation | denominator |
|---|---|---|---|
| M2R16-AC1 | PASS-M2-MARKER | `check_en_r16.py m2-marker` | 1 record graded, 3/3 fields non-empty, 2/2 blobs equal |
| M2R16-AC2 | PASS-R16-VINTAGE-FIELD | `check_en_r16.py r16-vintage-field` | 1 of 1 records present, 2/2 fixed inputs resolvable |
| M2R16-AC3 | PASS-R16-STALE-PROOFS | `check_en_r16.py r16-stale-proofs` | 1 commit since cut, 0 at risk, 0 enumerated |
| M2R16-AC4 | UNVERIFIABLE-BY-INSTRUMENT | judgment, CVO at L9 | N/A -- includes the S106 gap disclosure |

## 6. What is not claimed

This record does not claim the marker file has reached the tree -- it names exactly why it has not and
who disarms it. It does not claim `p37-producers`' behavior changed. It does not re-measure R-38's
population or touch any pinned fixed input. It does not read or write EN-s-1's record.
