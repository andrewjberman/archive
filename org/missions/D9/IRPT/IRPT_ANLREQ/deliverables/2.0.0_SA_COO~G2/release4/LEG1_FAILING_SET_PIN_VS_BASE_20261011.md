# Release 4 pin eb72753aad -- the leg-1 failing SET, by test id, against the base (CTO~DELL2 msg 4301)

`python -m pytest infra/aws/lambda/investor-reporting/ycharts/generate/tests -q -rfE --color=no`, dell2, Python 3.14.7, PyMuPDF 1.27.1.

| tree | commit | summary line | failing ids |
|---|---|---|---|
| pin | eb72753aad | 2 failed, 462 passed, 28 skipped, 1 xfailed, 32 errors, 42 subtests passed in 70.16s (0:01:10) | 34 |
| base (box/dell2) | fa1424ddb2 | 2 failed, 461 passed, 28 skipped, 1 xfailed, 32 errors, 42 subtests passed in 76.77s (0:01:16) | 34 |

**Sets identical by id: YES.** Only at the pin: 0. Only on the base: 0.

The order dependence is row IRPT_ANLREQ-D2-S31 (owner 2.0.0_SA_COO~Y2). The suite is graded here by SET, not by count.

## The ids at the pin

```
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_actual_custody_profile_acceptance_retry_and_worker_keep_frozen_attribution[canonical-sdk]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_actual_custody_profile_acceptance_retry_and_worker_keep_frozen_attribution[descriptor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-None]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-duplicate-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-missing-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-prospect]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-None]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-duplicate-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-missing-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-prospect]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_p_reader_consumer_factory_retention_retry_and_revocation[canonical-sdk]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_p_reader_consumer_factory_retention_retry_and_revocation[descriptor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-actor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-directory]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-snapshot]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-actor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-directory]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-snapshot]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_snapshot_revocation_during_retained_blob_read_prevents_worker_release[canonical-sdk]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_snapshot_revocation_during_retained_blob_read_prevents_worker_release[descriptor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-account_ids-value1]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-client_id-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-input_id-portfolio_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-snapshot_id-foreign-snapshot]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-account_ids-value1]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-client_id-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-input_id-portfolio_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-snapshot_id-foreign-snapshot]
FAILED infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_entry.py::test_opal_selected_firm_reaches_custody_service_with_real_actor
FAILED infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_entry.py::test_warm_opal_does_not_elevate_partner
```

## The ids on the base

```
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_actual_custody_profile_acceptance_retry_and_worker_keep_frozen_attribution[canonical-sdk]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_actual_custody_profile_acceptance_retry_and_worker_keep_frozen_attribution[descriptor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-None]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-duplicate-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-missing-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[canonical-sdk-prospect]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-None]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-duplicate-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-missing-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_installed_custody_factory_runs_guarded_entry_with_actual_sdk_profiles[descriptor-prospect]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_p_reader_consumer_factory_retention_retry_and_revocation[canonical-sdk]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_p_reader_consumer_factory_retention_retry_and_revocation[descriptor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-actor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-directory]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[canonical-sdk-snapshot]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-actor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-directory]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-selection]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_retained_retry_and_worker_recheck_current_custody_before_blob_read[descriptor-snapshot]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_snapshot_revocation_during_retained_blob_read_prevents_worker_release[canonical-sdk]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_snapshot_revocation_during_retained_blob_read_prevents_worker_release[descriptor]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-account_ids-value1]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-client_id-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-input_id-portfolio_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[canonical-sdk-snapshot_id-foreign-snapshot]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-account_ids-value1]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-client_id-foreign-client]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-input_id-portfolio_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]
ERROR infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_retained.py::test_wrong_browser_basis_cannot_accept_or_read_retained_input[descriptor-snapshot_id-foreign-snapshot]
FAILED infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_entry.py::test_opal_selected_firm_reaches_custody_service_with_real_actor
FAILED infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_entry.py::test_warm_opal_does_not_elevate_partner
```
