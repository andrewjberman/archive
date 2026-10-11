# Release 4 pin eb72753aad -- the two PyMuPDF test legs, run on dell2 (CTO~DELL2 msg 4294)

Run by 2.0.0_SA_COO~G2 in worktree C:/dev/rel-anlreq-r4. Interpreter, Python and PyMuPDF versions are the first lines of the raw output.

## Result

| leg | command | result |
|---|---|---|
| 1 | `python -m pytest infra/aws/lambda/investor-reporting/ycharts/generate/tests -q` | rc 1: 2 failed, 462 passed, 28 skipped, 1 xfailed, 32 errors |
| 2 | `python .../ycharts/generate/tests/run_offline_suite.py` | rc 0, summary all_pass true |
| release tests | `pytest .../tests/test_resident_worker.py` at the pin | 54 passed, 8 skipped; `-k release`: 5 passed |

## The 34 leg-1 failures are not this release's: three controls

All 34 are in `test_custody_entry.py` (2 failed) and `test_custody_retained.py` (32 errors, `KeyError: 'data'`).

| control | tree | result |
|---|---|---|
| the two custody files alone | pin eb72753aad | 42 passed, 2 skipped |
| the two custody files alone | box/dell2 @d1ed899ba9 | 42 passed, 2 skipped |
| the full suite | box/dell2 @fe28500304 (no 390 s half) | 2 failed, 461 passed, 28 skipped, 1 xfailed, 32 errors |

The base fails the same 34 without the release's change, and the pin's one extra pass is the 390 s test it adds. The custody
tests pass alone and fail inside the full run on both trees: an order dependence in the suite, pre-existing. The pin differs
from the base under `infra/aws/lambda/investor-reporting` in 2 files (`resident_worker.py` and its test).

NOT established: which earlier test leaves the state the custody tests trip on.

## Raw output of the two legs

```
commit: eb72753aad
interpreter: C:\Users\Test\AppData\Local\Programs\Python\Python314\python.exe
python: 3.14.7
PyMuPDF: 1.27.1: 1.27.1
2026-10-11T06:37:07Z
=== LEG 1 pytest ycharts/generate/tests
E        +    where handle = <served.Entry object at 0x000002420D6F8150>.handle
E        +    and   {'body': '{"request_id": "custody-request", "client_id": "c100000000000000000001", "account_ids": ["acc_a1000000000000...queryStringParameters': {'selected_tenant': '49financial'}, 'routeKey': 'POST /api/scoped/investor-reporting/analysis'} = event()

infra\aws\lambda\investor-reporting\ycharts\generate\tests\test_custody_entry.py:78: AssertionError
=========================== short test summary info ===========================
FAILED infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_entry.py::test_opal_selected_firm_reaches_custody_service_with_real_actor - AssertionError: {'contract_version': 'v1', 'ok': False, 'operation': 'analy...
FAILED infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_entry.py::test_warm_opal_does_not_elevate_partner - assert 'data' in {'contract_version': 'v1', 'ok': False, 'operation': 'anal...
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_actual_custody_profile_acceptance_retry_and_worker_keep_frozen_attribution[descriptor] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_actual_custody_profile_acceptance_retry_and_worker_keep_frozen_attribution[canonical-sdk] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-snapshot] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-selection] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-actor] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-directory] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-snapshot] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-selection] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-actor] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-directory] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_snapshot_revocation_during_retained_blob_read_prevents_worker_release[descriptor] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_snapshot_revocation_during_retained_blob_read_prevents_worker_release[canonical-sdk] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-snapshot_id-foreign-snapshot] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-account_ids-value1] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-client_id-foreign-client] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-input_id-portfolio_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-snapshot_id-foreign-snapshot] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-account_ids-value1] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-client_id-foreign-client] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-input_id-portfolio_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-None] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-missing-selection] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-duplicate-selection] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-foreign-client] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-prospect] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-None] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-missing-selection] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-duplicate-selection] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-foreign-client] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-prospect] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_p_reader_consumer_factory_retention_retry_and_revocation[descriptor] - KeyError: 'data'
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_p_reader_consumer_factory_retention_retry_and_revocation[canonical-sdk] - KeyError: 'data'
2 failed, 462 passed, 28 skipped, 1 xfailed, 32 errors, 42 subtests passed in 77.13s (0:01:17)
leg1 rc=1
2026-10-11T06:38:26Z
=== LEG 2 run_offline_suite.py
      "upload_field": "holdings",
      "zero_fee": {
        "error": "invalid_management_fee",
        "recorded_fee_that_succeeds": 0.003,
        "status": 422
      }
    }
  },
  "suite": "IB-s-9 offline proof of the YCharts generation chain",
  "summary": {
    "a_seven_steps": true,
    "all_pass": true,
    "amend_guarded_bound_silent": true,
    "b_submitting_before_side_effect": true,
    "c_never_the_newest": true,
    "d_settings_read_back": true,
    "e_bodies_per_s8": true,
    "f_the_201_is_wrapped": true,
    "g_schema_valid": true,
    "h_offline": true,
    "v010_three_recipes_one_handler": true,
    "v08_measured_contracts_and_decision_table": true
  }
}
RESULT-END
leg2 rc=0
2026-10-11T06:38:27Z
```
