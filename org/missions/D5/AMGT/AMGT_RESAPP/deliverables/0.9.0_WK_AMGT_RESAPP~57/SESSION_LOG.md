# Session log -- 0.9.0_WK_AMGT_RESAPP~57 on AMGT-rk-57

Worktree: /c/tmp/wk-amgt-14-57 (branch wk-amgt-14-57, cut from SITEZ HEAD 047aee5478).

## What was built

1. `.tools/surprise-row-gate.py`: `_acceptance_sweep(root, code, round_n=None, merging=False,
   _paths=None)`, its pure classifier `_classify_acceptance(rows_by_id, criteria)`, and supporting
   pure helpers `_order_criteria`, `_order_round`, `_order_label`, `_acceptance_rows_from_instance`,
   `_instance_for_order`, `_task_order_paths_for_sweep`, `_flagged_rows`. A slug-time NOTE ("ACCEPTANCE
   (round N, the slug's own): ...") appended beside the existing L10 precondition note at the site the
   RULED text names (`:1943-1946` at the cut; the exact line moved with the insertion, cited by content
   in the row/instance). A read-only CLI limb `--acceptance <CODE> [--round N]`. Five (in fact five)
   PURE self-test arms named "acceptance ..." in `_self_test()`, deliberately kept free of any git read
   (the real-bytes demonstration lives in the standalone battery, per the RULED text's own split between
   point 4's self-test half and its "real-bytes battery" half).
2. `.tools/tests/test_acceptance_sweep.py`: a 7-arm battery (4 pure, re-deriving the same 4 classifier
   shapes with a DIFFERENT instrument than the self-test's arms; 3 on THIS project's real bytes at HEAD).

## What was found, not assumed

The RULED text's own cited negative control -- `AMGT_RESAPP.TO-AMGT-rk-30.page-scores-render`'s
proof-of-spec instance recording AC1 PASS / AC2 FAIL -- is STALE at this worktree's HEAD: commit
9074091db1 fixed AC2 to PASS after the ROUND_ANALYSIS this cell cites and before this worktree's cut.
Filed as AMGT_RESAPP-Z-W57-S1. The live substitute used throughout (self-consistently, in the battery
and in this instance's own AC3 measurement) is `AMGT_RESAPP.TO-AMGT-rk-20.price-generation-contract`'s
AC1, one of the CTO's three named criterion defects (ROUND_ANALYSIS.round13.md s.1) and still genuinely
FAIL at HEAD, counted terminal by `_open_tos_census`'s proof limb (no `<status>` tag at all).

Separately: `rk-20`, `rk-23.artifact-name-encoding` and `rk-30.scores-adapter-model-tab` -- the CTO's
three named criterion defects -- carry NO `<round>` tag at all (confirmed by direct byte search, not
inference). AC3's own `<expect>` text names these three as FAIL rows the round-13 sweep should list, but
this cell's own RULED build spec defines round strictly by the order's own `<round>` tag, so a
`--round 13` filtered sweep genuinely excludes all three into the "unrounded" bucket (measured: FAIL 0,
unrounded 3) while the UNFILTERED sweep correctly lists all three under FAIL. Filed as
AMGT_RESAPP-Z-W57-S2. AC3 in this instance is graded on the ACTUAL measured output of the literal
invocation, per this order's own precedent for rk-26 ("record the difference, do not force agreement").

## Performance note (not a surprise row; a design constraint acted on directly)

An UNFILTERED `_acceptance_sweep` over this project's ~127 tracked task orders measures ~160s, and
`_open_tos_census` alone measures ~118s -- both against the 120s grading bound every criterion here
runs under. `_acceptance_sweep` gained an injectable `_paths` parameter (same convention as
`_route_precondition_violations`'s `open_tos=None`) so a caller needing one order's real bytes is not
forced to pay for the full project listing; every production caller (the slug-time note, the CLI) still
passes `_paths=None` and gets the full tree listing, unchanged. The battery's one side-by-side arm uses
`_proof_terminal` directly (the same instrument `_open_tos_census` calls internally) rather than the
full census, for the same reason.

## Verification run (this worktree, this HEAD)

- `python .tools/surprise-row-gate.py --self-test`: rc=0, 177 arms (5 new "acceptance ..."), 0 failed.
- `python .tools/tests/test_acceptance_sweep.py`: rc=0, "RESULT: 0 arm(s) failed of 7", "BATTERY PASS".
- `python .tools/surprise-row-gate.py --acceptance AMGT_RESAPP --round 13`: rc=0, deterministic across
  two runs (byte-identical output).
- `python .tools/surprise-row-gate.py org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`
  (dry run on the staged set): rc=0, both new rows admitted, standing corpus pass OK.
