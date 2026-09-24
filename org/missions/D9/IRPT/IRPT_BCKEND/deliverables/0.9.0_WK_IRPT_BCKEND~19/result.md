# IRPT_BCKEND.TO-IB-rtr-3 -- result

Criterion R118-AC3's own invocation, run verbatim from the project directory
(`org/missions/D9/IRPT/IRPT_BCKEND`):

```
cd deliverables/0.9.0_WK_IRPT_BCKEND~19 && py -3.12 -m pytest test_enforcer_real_operations_and_identity_adapter.py -v
```

## Full verbatim output

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\AndrewBerman\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\tmp\wk-irpt-18-19
configfile: pytest.ini
plugins: anyio-4.12.1, langsmith-0.7.17, asyncio-1.3.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 14 items

test_enforcer_real_operations_and_identity_adapter.py::test_real_render_operations_are_confirmed_from_routes_json_and_key_operation PASSED [  7%]
test_enforcer_real_operations_and_identity_adapter.py::test_render_delegate_operations_matches_the_real_served_vocabulary PASSED [ 14%]
test_enforcer_real_operations_and_identity_adapter.py::test_each_real_operation_is_admitted_through_the_actual_resolve_render_delegate_path[performance_report] PASSED [ 21%]
test_enforcer_real_operations_and_identity_adapter.py::test_each_real_operation_is_admitted_through_the_actual_resolve_render_delegate_path[analysis_report] PASSED [ 28%]
test_enforcer_real_operations_and_identity_adapter.py::test_each_real_operation_is_admitted_through_the_actual_resolve_render_delegate_path[narrative_packet] PASSED [ 35%]
test_enforcer_real_operations_and_identity_adapter.py::test_a_fourth_unrelated_operation_is_refused_object_not_covered PASSED [ 42%]
test_enforcer_real_operations_and_identity_adapter.py::test_differing_subject_and_advisor_id_resolves_correct_grant PASSED [ 50%]
test_enforcer_real_operations_and_identity_adapter.py::test_without_the_loader_a_subject_that_is_not_the_real_advisor_id_still_refuses PASSED [ 57%]
test_enforcer_real_operations_and_identity_adapter.py::test_bundle_id_mismatch_between_claimed_and_loaded_is_refused PASSED [ 64%]
test_enforcer_real_operations_and_identity_adapter.py::test_bundle_id_match_is_admitted PASSED [ 71%]
test_enforcer_real_operations_and_identity_adapter.py::test_a_loader_that_declares_no_bundle_id_is_never_checked PASSED [ 78%]
test_enforcer_real_operations_and_identity_adapter.py::test_cache_key_separates_by_revision_for_the_same_intersection PASSED [ 85%]
test_enforcer_real_operations_and_identity_adapter.py::test_revocation_control_still_passes PASSED [ 92%]
test_enforcer_real_operations_and_identity_adapter.py::test_no_refusal_carries_protected_bytes PASSED [100%]

============================= 14 passed in 0.11s ==============================
```

rc=0. 14 of 14 PASSED, mapping onto the criterion's own enumerated components:

- real-operation-name admission (3): the three parametrized
  `test_each_real_operation_is_admitted_through_the_actual_resolve_render_delegate_path[...]`
  cases (plus two supporting tests confirming the tuple is derived from the real
  `docs/contracts/investor-reporting/v1/routes.json` via `served.key_operation()`, never
  hand-transformed).
- fourth-operation refusal (1): `test_a_fourth_unrelated_operation_is_refused_object_not_covered`.
- differing-subject-advisor-id resolution (1): `test_differing_subject_and_advisor_id_resolves_correct_grant`
  (plus `test_without_the_loader_a_subject_that_is_not_the_real_advisor_id_still_refuses`, the
  backward-compatibility control).
- bundle-mismatch refusal (1): `test_bundle_id_mismatch_between_claimed_and_loaded_is_refused`
  (plus `test_bundle_id_match_is_admitted` and `test_a_loader_that_declares_no_bundle_id_is_never_checked`
  as positive/no-regression controls).
- cache-key revision-separation (1): `test_cache_key_separates_by_revision_for_the_same_intersection`.
- the unmodified revocation control still passing: `test_revocation_control_still_passes`, the
  SAME arm-2 scenario (delegator revoked between mint and read -> EMPTY_GRANT) IB-rtq-2's own
  file proves, reproduced fresh in this cell's own deliverable against the CORRECTED real
  operation names (see `IRPT_BCKEND-W19-S1` -- the OLD deliverable file's literal 'performance'
  default cannot pass after item (a)'s rename, through no fault of the algebra; the algebra
  itself is unmodified in expectation and is what this test proves).

## Supplementary (not part of this criterion's own invocation)

Pre-existing `_authz/tests/` suite, unmodified, re-run after this cell's edits:

```
141 passed in 14.47s
```

`.tools/commit-gate.sh` on both touched files:

```
All checks passed!
OK: no unguarded strict-utf8 log reads.
All checks passed!
OK: no unguarded strict-utf8 log reads.
OK: pre-commit gate clean for 2 of 2 file(s)
```

Mutant control (before/after on the SAME code this cell touched): reverting
`RENDER_DELEGATE_OPERATIONS` to the pre-cell placeholder tuple
(`("performance", "analysis_sections", "narrative")`) and re-running this deliverable's own
`test_render_delegate_operations_matches_the_real_served_vocabulary` FAILS (tuple mismatch,
`AssertionError`); restoring the fix, it PASSES again. Independently, running the IB-rtq-2
pre-existing deliverable file (`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
0.9.0_WK_IRPT_BCKEND~15/test_render_delegate_resolver_enforcer.py`) against the ORIGINAL
enforce.py (git show 7a55a7327d, this order's own cut) gives `1 failed, 19 passed` (one
pre-existing, unrelated citation-drift failure -- see IRPT_BCKEND-W19-S1); the SAME file against
this cell's fixed enforce.py gives `5 failed, 15 passed` -- the delta is exactly the four cases
whose default operation name is the now-superseded placeholder, none of them an algebra
regression (confirmed directly by this cell's own `test_revocation_control_still_passes`, which
reproduces the SAME scenario with the corrected operation name and PASSES).
