# LT-n-2 -- run ids and content hashes on every number round 1's judgment records cite

`LGIC_LGCTFM.TO-LT-n-2-r2` | `0.9.0_WK_LGIC_LGCTFM~2` | branch `wk-lgic-lgctfm-2-2`

Record: `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~2/NUMBER_PINS_R2.json`
Instrument: `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~2/pin_numbers_r1.py` (committed)

## The set is a SUBTRACTION, and here is the whole ledger

The denominator is **520** -- every maximal digit run in every STRING field of the 14 round-1
judgment acceptance rows. The 14 proof instances are enumerated **by existence** (`git ls-files`
over the project's deliverables, filtered to `*.proof_of_spec.json`), never from a typed list, and
the 14 judgment criterion ids come from `R2_BASE.json`'s `round_1_judgment_criteria.by_id`.

**The FIELD the denominator reads** is every string-valued key of the acceptance row --
`output_evidence`, `denominator`, `invocation`, `criterion_verbatim`, `expect`, `method`, `status`,
`status_reason`, `criterion_id` -- the widest field set the row offers, chosen so a citation cannot
hide in a field the sweep skipped. Naming the field is not decoration: R-50 was ruled against the
issuing seat hours before this cut for censusing a ledger's `decided` column while the act consumed
`disposition`, and a subtraction over the wrong field arrives with a real denominator and so reads
as measured.

| | count | |
|---|---|---|
| STAGE 0 digit runs (the domain) | 520 | |
| - IDENTIFIER_FRAGMENT (stage 1, mechanical) | 401 | glued to a word: a commit pin, a row id, a serial, a path |
| - AGENT_SERIAL | 49 | a digit inside `3.0.0_SA_CVO`, `0.9.0_WK_...` |
| - PATH_OR_IDENTIFIER_GLUED | 5 | an address, not a quantity |
| - SECTION_NUMBER | 8 | `sections 1.1, 1.2, 3, 4, 5, 6` |
| - DOC_FILE_NUMBER_PREFIX | 7 | `02_DOCTRINE`, `06_`, `10_`, `11_` |
| - QUANTITY_ON_A_PRE_EXISTING_REPO_FILE | 6 | measured, but not on a produced artifact -- see below |
| - ENUMERATED_STEP_LABEL | 5 | `(1)`, `(2)`, `at step 2` |
| - CONFIG_THRESHOLD_QUOTED_FROM_THE_FILE_UNDER_TEST | 4 | `warn=24h/fail=30h` |
| - SOURCE_LINE_NUMBER | 3 | `line 655/955`, `line 180-187` |
| - FIRM_NAME | 2 | `49 Financial` |
| - FILE_LENGTH_OF_A_PRE_EXISTING_FILE | 1 | `437-line file` |
| - STRUCTURAL_RULE_CARDINALITY | 1 | `a 2-member group` |
| **= RESIDUE (RUN_MEASURED_QUANTITY)** | **28 tokens** | the class this cell pins |

The ledger closes against its own denominator, and the run refuses if it does not.

**The 28 residue tokens dedupe to 17 members**: 16 pinned + 1 excluded. Every residue token is
covered by exactly one member and the per-criterion counts must agree, so nothing is lost between
the residue and the pinned set.

```
numbers_found 17 == pinned 16 + excluded 1   -> True
```

## Choosing the domain is itself a claim, so here it is, stated to be refused

The class pinned is **a quantity measured on an artifact ROUND 1 PRODUCED** -- a run directory's
output, or a cell deliverable. A quantity measured on a **pre-existing repo file the cell merely
read** is excluded BY CLASS (6 tokens: `2 of 2 named README sections`, `1 of 1 manifest code path`,
`result 0 uncovered`, `returns 0 hits`), because R-40's subject is a run or a produced artifact and
such a file already resolves through the commit pin its own row carries. That line is this cell's
claim about its own axis. It is printed rather than assumed.

## E3R1-AC6 is EXCLUDED BY NAME, with its reason

A silent omission and a stated exclusion are different states. `E3R1-AC6` is in `excluded`, keyed by
its own criterion id, with this reason:

> NOT re-graded against R-40, by `1.0.0_SA_CTO`'s round-1 analysis item 2, verbatim: *"`S11`'s
> run-ids on every number; `E3` is NOT re-graded against R-40."* Its judgment was SOUND AT ITS OWN
> VINTAGE -- it ran before `LT-e-4` made the untypeable plant opt-in, which is what moved the
> population from 271 tensions to 179. Re-grading it would falsify a correct grade.

That one member accounts for **all 5** of the residue tokens `E3R1-AC6` cites (`rules_colliding 1`,
`271` tensions, `1084` factor cells twice, `0` defective), and the record names them individually
under `excluded_tokens_named_not_pinned` so the exclusion hides nothing.

## Every hash carries its instrument, and every hash was computed twice

Each pin is `git hash-object` (which prefixes `blob <len>` and a NUL byte) **and** is required to
equal `git rev-parse HEAD:<path>`. That second read is not ceremony: `core.autocrlf` is `true` on
this box, this worktree renders the channel file at 593 CRLF while its HEAD blob is pure LF, and a
worktree hash would have been the CHECKOUT's rather than the record's.

Two positive controls fell out of it. `git hash-object` over the graded run's `contract.json`
returns `33204e29839de89af81fb293317cce3ccdf2266d`, byte-for-byte the value `R2_BASE.json` publishes
as `graded_run_round_1.contract_git_hash_object`; and the graded run's `plan.json` returns
`f26d46db87f3d8bcbf7b7ff13dafe708030c6d48`, the value the checker's own simulated-correct record
carries for `X1R1-AC6`. Two hashes this cell computed independently agree with two the issuer
published.

## The 16 pins

| member | value | run | kind | measured on | content hash (`git hash-object`) | re-measured |
|---|---|---|---|---|---|---|
| `E2R1-AC5:7` | 7 | `f73efe6113` | cell_commit | `~1/forks/SEEDS.json` | `fef64c9254...` | 7 |
| `P1R1-AC6:1626` | 1626 | `7b01900dda` | cell_commit | `~2/plan_r1/plan.json` | `576b347091...` | 1626 |
| `V1R1-AC5:20` | 20 | `20260917T202556Z-bb29248` | run_home | `~3/REPRODUCTION.json` | `1fcd256748...` | 20 |
| `V1R1-AC5:5-ALIAS` | 5 | `20260917T202556Z-bb29248` | run_home | `~3/REPRODUCTION.json` | `1fcd256748...` | 5 |
| `V1R1-AC5:4-CONFORMANT` | 4 | `20260917T202556Z-bb29248` | run_home | `~3/REPRODUCTION.json` | `1fcd256748...` | 4 |
| `V1R1-AC5:1-NOT-GRADED` | 1 | `20260917T202556Z-bb29248` | run_home | `~3/REPRODUCTION.json` | `1fcd256748...` | 1 |
| `V1R1-AC5:5-OUT-OF-PATTERN` | 5 | `20260917T202556Z-bb29248` | run_home | `~3/REPRODUCTION.json` | `1fcd256748...` | 5 |
| `V1R1-AC5:5-RAISE` | 5 | `20260917T202556Z-bb29248` | run_home | `~3/REPRODUCTION.json` | `1fcd256748...` | 5 |
| `V1R1-AC5:184` | 184 | `20260917T202556Z-bb29248` | run_home | `bb29248/contract.json` | `84d4d1e62b...` | 184 |
| `X1R1-AC6:184` | 184 | `20260918T011619Z-8db9eb1` | run_home | `8db9eb1/contract.json` | `33204e2983...` | 184 |
| `X1R1-AC6:179` | 179 | `20260918T011619Z-8db9eb1` | run_home | `8db9eb1/contract.json` | `33204e2983...` | 179 |
| `X1R1-AC6:1074` | 1074 | `20260918T011619Z-8db9eb1` | run_home | `8db9eb1/plan.json` | `f26d46db87...` | 1074 |
| `X1R1-AC6:0` | 0 | `20260918T011619Z-8db9eb1` | run_home | `8db9eb1/contract.json` | `33204e2983...` | absent (stated) |
| `X3R1-AC5:0-CLOSED` | 0 | `20260918T002711Z-caf0983` | run_home | `caf0983/DIFF.md` | `aa8003eff1...` | 0 |
| `X3R1-AC5:1-OPENED` | 1 | `20260918T002711Z-caf0983` | run_home | `caf0983/DIFF.md` | `aa8003eff1...` | 1 |
| `X3R1-AC5:179-UNCHANGED` | 179 | `20260918T002711Z-caf0983` | run_home | `caf0983/DIFF.md` | `aa8003eff1...` | 179 |

15 of 16 were **re-measured against their own artifact and agree**. The sixteenth, `X1R1-AC6:0`
(schema errors), records `re_measured_by_this_cell: absent` with its reason: re-running the schema
validation would re-grade `X1R1-AC1`, a closed mechanical criterion, and this cell moves no grade.

**`V1R1-AC5`'s run is NOT the graded run.** `REPRODUCTION.json`'s own `contract` field names
`20260917T202556Z-bb29248`, so its numbers are pinned there and not to `8db9eb1`. That is a case the
convention exists for, and it is the kind of thing a copied hash cannot produce.

## What the pins resolve (measured, and NO GRADE MOVES)

`S11` reads `1626` and `1074` as numbers that "cannot both be true of one plan", and reads E3's
271-tension population as one that "no longer exists anywhere". Pinning each number to its artifact
falsifies both readings in the same way -- the numbers were never about one artifact:

- **Pre-opt-in lineage**: `~2/plan_r1/contract.json`, `git hash-object`
  `413f0215c2370a3a5f521fbf248f5d323a02a897`, **278 rows / 271 tensions**, byte-identical to
  `~1/walk/contract.json`. Its plan carries **1626** packages. Cited by `P1R1-AC6` (1626) and
  `E3R1-AC6` (271).
- **Post-opt-in lineage**: `8db9eb1/contract.json`, `33204e29839de89af81fb293317cce3ccdf2266d`,
  **184 rows / 179 tensions**. Its plan carries **1074** packages. Cited by `X1R1-AC6`.

`LT-e-4`'s opt-in plant is the whole difference. Both package counts are true of their own plan, and
**the 271-tension population is tracked at HEAD in two byte-identical files** -- it is content-
addressable, not gone. Filed as surprise row `LGIC_LGCTFM-W2-S4`; the decision that follows from it
belongs to the seat that owns `S11`'s disarm, never to this worker. `E3R1-AC6` stays excluded by
name either way.

## Acceptance

| criterion | verdict | invocation | deciding line |
|---|---|---|---|
| N2R2-AC1 | PASS-by-output | `check_lt_r2.py n2-subtraction` | `VERDICT: PASS-N2-SET-IS-A-SUBTRACTION` |
| N2R2-AC2 | PASS-by-output | `check_lt_r2.py n2-e3` | `VERDICT: PASS-N2-E3-EXCLUDED-BY-NAME` |
| N2R2-AC3 | PASS-by-output | `check_lt_r2.py n2-pins` | `VERDICT: PASS-N2-EVERY-NUMBER-CARRIES-ITS-RUN` |
| N2R2-AC4 | PASS-by-output | `check_lt_r2.py n2-hash-instrument` | `VERDICT: PASS-N2-EVERY-HASH-NAMES-ITS-INSTRUMENT` |
| N2R2-AC5 | RECORDED (judgment) | -- | `UNVERIFIABLE-BY-INSTRUMENT`, for `3.0.0_SA_CVO` at L9 |

`selftest-arms` was run FIRST and returned `VERDICT: PASS-ARMS-DISCRIMINATE`, 28 arms driven, 10
POSITIVE-SATISFIABILITY. No arm was unsatisfiable by a correct record, so no blocking row was owed
on the checker.

## What the instrument refused, three times, before it passed

Worth recording because each refusal was the control doing its job on THIS cell's own work, not on
round 1's:

1. The classifier's path rule claimed `post == "/"`, which ate the verdict spread `(5/4/1/5/5`.
2. Narrowed to "followed by a digit", it still ate `ALIAS 5/CONFORMANT 4/NOT-GRADED 1/...`.
3. Narrowed to "slash-bounded on both sides", it still ate the middle of `5/4/1/5/5`.

Each time `EXPECTED_RESIDUE` -- the residue declared per `(criterion, field, token, occurrence)` --
refused the run and named the exact tokens lost. A rule that quietly eats a real quantity cannot
pass. The fourth form is a positive predicate for a slash-separated numeric list, and it holds.

A fourth refusal came from the re-measure limb: reading a verdict only as `('ALIAS', ...)` counted
`RAISE` as **0** against a cited **5**, because a raise renders as `RAISE: K1: ...`. The instrument
refused rather than reporting a correct number as wrong -- which is exactly the direction a
"number is wrong" finding must fail in.
