# LGIC_LGCTFM.TO-LT-r-1-r10 -- split the flat class, then take the re-route that exists: result

Assignee: `0.9.0_WK_LGIC_LGCTFM~1`. Worktree: `wk-lgic-lgctfm-10-1`. Branch base (base_sha, every verdict
line and every row): `75ae38afb85f4b2836afdc9474c2860940cb2223`.

## Instrument confirmation

`python org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r10/check_lt_r10.py
selftest-arms` -> `VERDICT: PASS-ARMS-DISCRIMINATE`, rc=0, 19 arms driven (4 POSITIVE, 1 WIRING, 14
mutant/other), run BEFORE any record was written or any file added.

## Population, re-derived (not inherited)

Read `ROUTED_ROW_REMEDY_R9.json`'s `remedy.rows` at commit `58effd2aec52218829c68cebda7526dae1b8b0fa`
and took every row whose `class == "UNEXECUTABLE-AS-ROUTED"` (the flat value): `LGIC_LGCTFM-S18`,
`LGIC_LGCTFM-W1-S21` -- 2 of 7 rows in that record. This is byte-for-byte the same pair the order's own
framing table names, but it was re-derived from the round-9 record itself per the order's instruction,
not copied from the table.

## The split

| id | new class | why |
|---|---|---|
| `S18` | `UNEXECUTABLE-IN-PRINCIPLE` | routes to a POSITIVE-SATISFIABILITY ARM for `x2-flag`/`x3-filed` dispatched by `check_lt_r1.py`'s own CMD table; no sibling file can register a CMD-table entry, and that file is round 1's PINNED fixed input of a CLOSED round. No conformant form exists from any cell barred from editing it. |
| `W1-S21` | `UNEXECUTABLE-AS-ROUTED-RE-ROUTABLE` | routes to documentation "in that arm's own carrier", but the row's own basis narrows this to a PLACEMENT requirement -- "carried where a later re-derivation will meet them" -- not an edit. A sibling document beside the checker is conformant, cheap, and additive. |

Both rows name what the split requires: `S18`'s `names` field states what would have to change (round 1
re-opened, or a future round that legitimately re-touches `check_lt_r1.py` adds the arm as part of that
repair); `W1-S21`'s `names` field states the conformant alternative (the sibling document, on the
LGIC_ENFORCE round-13 `RETIRED.md` precedent).

## The re-route performed

Added `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/DRIFT_CAUSES.md`,
carrying the three drift causes `LGIC_LGCTFM-W1-S21` found and grounded at a third position (
`org/missions/D14/LGIC/LGIC_LGCTFM/surprise-channel/investigations/INVESTIGATION_v1.md#LGIC_LGCTFM-W1-S21`,
surfaced 2026-09-18T08:00Z):

1. **Live-builder drift** (`e2-reproduce`): `lib/opal_naming.py`'s `grade()` now returns
   `advi-inf-accounts-v2-daily` where the frozen contract holds `{system}-inf-accounts-v2-daily` -- 273 of
   278 rows reproduce, 5 diverge (`R-0251`, `R-0257`, `R-0264`, `R-0265`, `R-0266`).
2. **A pin whose path predates the file** (`S2R1-AC8`): the evidence cites
   `org/standards/LGCTFM_CONTRACT.schema.json@ef8197ed07`, and that path does not exist at that commit --
   the schema was added 24 minutes later by a different cell (`e2daf62f07`).
3. **A quoted measurement that went stale inside its own cell** (`E2R1-AC5`): the grep-for-`FORK_CONTROLS`
   result it quotes was already false when written -- the string entered the file 3m40s before the
   evidence's own proof commit.

The document states, about itself: it adds no arm, changes none of `check_lt_r1.py`'s output, and does
not make `x2-flag`/`x3-filed` distinguish an empty window from a satisfied one -- that closure is `S18`'s,
and `S18` has no conformant form.

## Additivity, anchored to this cell's own base

`check_lt_r1.py`'s blob at this cell's base (`75ae38afb85f4b2836afdc9474c2860940cb2223`) is
`8835d6519b67d96bb6bc07b4230c0be81a4590f0`; the same read at HEAD after this cell's commit is identical.
Not one byte of that file, or of `FORK_CONTROLS.json`, `PLANTED_CONTRACT.json`, `SUBJECT_CONTROL.json`
(the other three `fixed_inputs/r1/` carriers), was touched -- `git status --porcelain` never showed any of
the four throughout this cell's work.

## Not performed (BOUNDS)

- **No arm was added to `check_lt_r1.py` to satisfy `S18`.** It has no conformant form; a cell that found
  a way would have falsified the class rather than satisfied the round. None was found, and none was
  attempted.
- **No disarm on either row.** Both name `2.0.0_SA_COO~G`; a disarm is the row owner's act under R-19. The
  disposition is `3.0.0_SA_CVO`'s at L9.
- **`S26` is not this round's.** It closed at `LGIC_LGCTFM-S55` @`d180c2077f` under `1.0.0_SA_CTO`'s R-81
  scope ruling @`80bb078627`; the analysis names it explicitly as not round 10's work.

## Mechanical criteria

- `R1R10-AC1` -- `python check_lt_r10.py r1-reclass` -> `VERDICT: PASS-R1-RECLASS`, rc=0.
- `R1R10-AC2` -- `python check_lt_r10.py r1-reroute` -> `VERDICT: PASS-R1-REROUTE`, rc=0.
- `R1R10-AC3` -- `python check_lt_r10.py r10-vintage-field` -> `VERDICT: PASS-R10-VINTAGE-FIELD`, rc=0.
- `R1R10-AC4` -- `python check_lt_r10.py r10-stale-proofs` -> `VERDICT: PASS-R10-STALE-PROOFS`, rc=0 (1
  fixed-input commit since `R10_BASE.json`'s `cut_pin` `021d1947bb`, informational only -- it is this
  round's own minting issuance `75ae38afb8`; 0 proofs at risk, 0 enumerated, SET EQUALITY holds).
- `R1R10-AC5` -- judgment, recorded `UNVERIFIABLE-BY-INSTRUMENT`, routed to `3.0.0_SA_CVO` at L9, over
  BOTH classes per the order's partition-quantified bar (a row wrongly marked `RE-ROUTABLE` is equally
  wrong as one wrongly marked `IN-PRINCIPLE`).

## Controls

- **mutant (reclass)** -- backed up the committed `ROUTED_ROW_RECLASS_R10.json` to `.scratch/`, overwrote
  `reclass.re_routable` 1 -> 99 (rows unchanged); re-run flipped `VERDICT: PASS-R1-RECLASS` ->
  `VERDICT: FAIL-R1-RECLASS` naming both the count disagreement ("the rows carry 1") and "the class
  arithmetic does not close against the rows carried"; restored the original committed bytes from the
  backup, `git status --porcelain` on the path read clean after restore, and the re-run reproduced the
  original `VERDICT: PASS-R1-RECLASS` output exactly. FIRED-AS-EXPECTED.
- **mutant (re-route)** -- moved the committed `DRIFT_CAUSES.md` out of `fixed_inputs/r1/` to `.scratch/`;
  re-run flipped `VERDICT: PASS-R1-REROUTE` -> `VERDICT: FAIL-R1-REROUTE` naming "the re-route names an
  artifact that does not exist"; moved the file back to its committed path, `git status --porcelain` on
  the path read clean after restore, and the re-run reproduced the original `VERDICT: PASS-R1-REROUTE`
  output exactly. FIRED-AS-EXPECTED.
- **determinism** -- two consecutive runs of each of the four commands against the unmodified committed
  records, diffed byte-for-byte: 0 diff lines on all four. STABLE.

## proof-of-spec-check

`python .tools/proof-of-spec-check.py
org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/LGIC_LGCTFM.TO-LT-r-1-r10.split-and-reroute.proof_of_spec.json
R1R10-AC1,R1R10-AC2,R1R10-AC3,R1R10-AC4,R1R10-AC5 --governing-order
org/missions/D14/LGIC/LGIC_LGCTFM/task-orders/LGIC_LGCTFM.TO-LT-r-1-r10.split-and-reroute.md` -- see this
order's `<status>` flip commit for the recorded rc.

## Not done here (BOUNDS)

No row was disarmed. `check_lt_r1.py` and the other three `fixed_inputs/r1/` carriers stayed read-only
throughout, verified by blob comparison and by `git status --porcelain` never showing any of the four.
`S26` was not touched; it is not this round's work.
