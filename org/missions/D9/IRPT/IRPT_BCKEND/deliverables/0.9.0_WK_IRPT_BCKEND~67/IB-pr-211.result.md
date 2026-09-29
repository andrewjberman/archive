# IB-pr-211 -- session log (0.9.0_WK_IRPT_BCKEND~67)

## Cell

Window 21: a RENDER_DELEGATE export read Performance and the adapter refused with
`PerformanceAccessRefused("a render read carries no request to name its grant")` (corr-d490a5849a80,
public OBJECT_NOT_COVERED). Cause: `entry._authorize_release` re-resolves scope after the slow compute
and called `_resolve_selected(scope, current_ctx, reference)` at line 61 WITHOUT `request`, so
`_resolve_render_selection` -> `_render_grant(request, ctx)` refused on `request is None`. The first
resolution (`_performance_report` -> `_resolve_selected(scope, ctx, reference, request)`) already passed
the request; only the release re-check dropped it.

## Baseline

`python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/checks/r21/p21_1_ac1_release_passes_request.py .`
before the fix:
```
arm A: request handed to _resolve_selected: False
arm B: a changed selection still refuses: True
P21-1-AC1 FAIL
```
rc=1 -- matches the task order's stated base case (arm A false, arm B true).

## Fix

`infra/aws/lambda/investor-reporting/performance/entry.py` line 61:
`_resolve_selected(scope, current_ctx, reference)` -> `_resolve_selected(scope, current_ctx, reference, request)`.
No other line touched; the human path (`resolve_selection`, unchanged signature call) and the
"computed selection no longer matches" refusal (line 62-63) are untouched.

## After fix

Same checker:
```
arm A: request handed to _resolve_selected: True
arm B: a changed selection still refuses: True
P21-1-AC1 PASS
```
rc=0.

Added `test_the_release_recheck_passes_the_request_for_a_render_delegate` to
`infra/aws/lambda/investor-reporting/performance/tests/test_render_selection.py`: builds a real stamped
render grant (`test_render_principal.stored` fixture + `_pin`), a `RENDER_DELEGATE` scope, and calls
`entry._authorize_release` directly through a fake boundary/enforcer whose `resolve_now` returns that
scope for the SAME request object; the call must complete without raising, proving the re-check's
`_render_grant` call received a real request and read the grant.

Full suite `python -m pytest test_render_selection.py test_render_principal.py -v` (from
`infra/aws/lambda/investor-reporting/performance/tests`): 13 passed, 0 failed -- the new test plus all
12 pre-existing tests, including the "computed selection no longer matches" and human-path arms.

`.tools/commit-gate.sh` on both changed files: clean (py_compile + ds-precommit + ruff).

## Surprises

None filed -- the cause, fix location and acceptance behaviour all matched the task order's description
exactly; no premise failed and no capability was missing.
