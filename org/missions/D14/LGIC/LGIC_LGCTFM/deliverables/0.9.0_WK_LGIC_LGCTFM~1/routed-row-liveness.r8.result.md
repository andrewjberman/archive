# LGIC_LGCTFM.TO-LT-l-1-r8 -- routed-row liveness re-read: result

Assignee: `0.9.0_WK_LGIC_LGCTFM~1`. Worktree: `wk-lgic-lgctfm-8-1`. Branch base: `a7bafce14e`.

## Instrument confirmation

`python org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r8/check_lt_r8.py selftest-arms`
-> `VERDICT: PASS-ARMS-DISCRIMINATE`, rc=0, 24 arms driven (7 POSITIVE-SATISFIABILITY, 2 WIRING, 15
mutant/other), run BEFORE any record was written.

## What was built

`ROUTED_ROW_LIVENESS_R8.json`, committed at `34b1555823`. Denominator 23, re-counted at write time from
`REMEDIATION_ROUTE_R7.json @e788f77fd1` (that file's own `population` field). Every one of the 23 routed
rows got exactly one verdict, with `evidence` naming what was read AT HEAD -- a `git log <cut_pin>..HEAD --
<path>` window, a `git show <hash>` of a commit independently verified as an ancestor of HEAD, or a direct
read of the artifact the row describes. No row's evidence is the route's own prose quoted back.

Counts: **STILL-LIVE 7, ALREADY-REMEDIED 9, NOT-THIS-SEATS 7** (23 total).

### Two rows graduated past the route's own uncertainty (the direction this round exists to catch)

- **`LGIC_LGCTFM-S32`** -- ALREADY-REMEDIED, closed_by `aad67ca4bc`. The route's own basis called this
  "unverified... routed rather than assumed done" because round 7's worker had read only round-7's fixed
  inputs. A direct `git show aad67ca4bc` (round 4's own L6 issuance, an ancestor of HEAD, landed BEFORE
  round 7 was even cut) shows the owed E5R3-AC4 sentence verbatim, both in the commit body and in
  decomposition s.15.
- **`LGIC_LGCTFM-W1-S37`** -- ALREADY-REMEDIED, closed_by `a7bafce14e`. This very round's own task order
  (the WORKER FACE this cell executed) reads verbatim: "the run prints its own arm counts; this order does
  not quote them (`W1-S37`)" -- direct, in-project, HEAD-vintage evidence the standing practice the row
  asks for is now followed, one round after the row named round 7's own order as the still-live violation.

### Collision recorded, not resolved

`LGIC_LGCTFM-S18` and `LGIC_LGCTFM-W1-S21` both name `check_lt_r1.py`, a **PINNED fixed input of round 1,
a CLOSED round**. Editing it is the identical stale-proof hazard LGIC_ENFORCE round 16 (`14d80144dd`) is
handling ADDITIVELY -- a `RETIRED.md` sibling, never a touch to the pinned checker, because touching it
"would ACTIVELY ENDANGER something graded." Both rows are recorded STILL-LIVE with the collision stated in
their own `evidence`; the collision itself is not resolved by this cell, per the order's instruction.

## Mechanical criteria

- `L1R8-AC1` -- `python check_lt_r8.py l1-liveness` -> `VERDICT: PASS-L1-LIVENESS`, rc=0.
- `L1R8-AC2` -- `python check_lt_r8.py r8-vintage-field` -> `VERDICT: PASS-R8-VINTAGE-FIELD`, rc=0.
- `L1R8-AC3` -- `python check_lt_r8.py r8-stale-proofs` -> `VERDICT: PASS-R8-STALE-PROOFS`, rc=0 (1
  fixed-input commit since `R8_BASE.json`'s `cut_pin` 082fbb3502, informational only -- it is this round's
  own minting issuance `a7bafce14e`; 0 proofs at risk, 0 enumerated, SET EQUALITY holds).
- `L1R8-AC4` -- judgment, recorded `UNVERIFIABLE-BY-INSTRUMENT`, routed to `3.0.0_SA_CVO` at L9.

## Controls

- **mutant** -- overwrote `liveness.still_live` 7 -> 8 in the committed record (rows unchanged); re-run
  flipped `VERDICT: PASS-L1-LIVENESS` -> `VERDICT: FAIL-L1-LIVENESS` naming `still_live says 8 but 7 rows
  carry it`; restored the original committed bytes from a pre-mutation backup, `git status --porcelain`
  read clean after restore, and the re-run reproduced the original `VERDICT: PASS-L1-LIVENESS` output
  exactly. FIRED-AS-EXPECTED.
- **determinism** -- two consecutive runs of each of the three commands against the unmodified committed
  record, `diff`'d byte-for-byte: no differences on any of the three. STABLE.

## proof-of-spec-check

`python .tools/proof-of-spec-check.py <instance> L1R8-AC1,L1R8-AC2,L1R8-AC3,L1R8-AC4 --governing-order
org/missions/D14/LGIC/LGIC_LGCTFM/task-orders/LGIC_LGCTFM.TO-LT-l-1-r8.routed-row-liveness.md` ->
`VALID (rc=0)`, acceptance rows=4, violations=0.

## Not done here (BOUNDS)

Nothing was remedied, disarmed or dispositioned. `REMEDIATION_v1.md` and every pinned fixed input
(including `check_lt_r1.py`) were read-only throughout. This record is the input to the next round's
remedies.
