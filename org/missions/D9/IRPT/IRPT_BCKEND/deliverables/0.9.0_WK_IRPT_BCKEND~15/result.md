# R117-AC2 result -- IB-rtq-2 (0.9.0_WK_IRPT_BCKEND~15)

Criterion invocation, run VERBATIM (anchored at `org/missions/D9/IRPT/IRPT_BCKEND/`, the
directory `deliverables/0.9.0_WK_IRPT_BCKEND~15` is relative to):

```
cd deliverables/0.9.0_WK_IRPT_BCKEND~15 && py -3.12 -m pytest test_render_delegate_resolver_enforcer.py -v && py -3.12 -m pytest infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py -v
```

Both legs exit 0. The second leg's path resolves through a WRAPPER file this cell added at
that exact nested location (row `IRPT_BCKEND-W15-S3` explains why one is needed and what it
does -- it is not a second copy of the test, it loads and re-executes the real
`_scope/tests/test_resolve.py` by absolute path).

A third, separate Node invocation proves the V2 authorizer's render branch (arm (d)):

```
node --test test_edge_render_delegate_v2_authorizer.mjs
```

run from the same `deliverables/0.9.0_WK_IRPT_BCKEND~15` directory. Exit 0.

## Suite 1 -- `test_render_delegate_resolver_enforcer.py` (this cell's new tests: arms (a), (b), (c))

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\AndrewBerman\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\tmp\wk-irpt-17-15
configfile: pytest.ini
plugins: anyio-4.12.1, langsmith-0.7.17, asyncio-1.3.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 20 items

test_render_delegate_resolver_enforcer.py::test_trusted_only_no_longer_drops_the_render_marker PASSED [  5%]
test_render_delegate_resolver_enforcer.py::test_render_markers_are_not_folded_into_trusted_headers_itself PASSED [ 10%]
test_render_delegate_resolver_enforcer.py::test_renderer_with_full_marker_classifies_render_delegate PASSED [ 15%]
test_render_delegate_resolver_enforcer.py::test_renderer_without_any_marker_is_unknown_arm_j PASSED [ 20%]
test_render_delegate_resolver_enforcer.py::test_renderer_with_a_partial_marker_is_unknown_never_a_best_effort_delegate[delegator] PASSED [ 25%]
test_render_delegate_resolver_enforcer.py::test_renderer_with_a_partial_marker_is_unknown_never_a_best_effort_delegate[bundle] PASSED [ 30%]
test_render_delegate_resolver_enforcer.py::test_renderer_with_a_partial_marker_is_unknown_never_a_best_effort_delegate[revision] PASSED [ 35%]
test_render_delegate_resolver_enforcer.py::test_renderer_with_no_origin_or_no_subject_is_unknown_like_anyone_else PASSED [ 40%]
test_render_delegate_resolver_enforcer.py::test_render_delegate_never_falls_through_to_a_human_class PASSED [ 45%]
test_render_delegate_resolver_enforcer.py::test_render_delegate_is_a_member_of_principal_classes PASSED [ 50%]
test_render_delegate_resolver_enforcer.py::test_the_cvo_probes_exact_header_set_now_flips_to_render_delegate_with_the_marker_added PASSED [ 55%]
test_render_delegate_resolver_enforcer.py::test_the_pre_existing_scope_and_authz_suites_still_pass_unmodified PASSED [ 60%]
test_render_delegate_resolver_enforcer.py::test_arm1_entitled_delegator_and_pinned_object_the_three_reads_succeed PASSED [ 65%]
test_render_delegate_resolver_enforcer.py::test_arm2_delegator_revoked_between_mint_and_read_is_refused PASSED [ 70%]
test_render_delegate_resolver_enforcer.py::test_arm3a_an_object_outside_the_bundles_pinned_scope_is_refused PASSED [ 75%]
test_render_delegate_resolver_enforcer.py::test_arm3b_an_operation_outside_the_three_is_refused PASSED [ 80%]
test_render_delegate_resolver_enforcer.py::test_an_empty_intersection_is_a_refusal_never_an_empty_but_successful_answer PASSED [ 85%]
test_render_delegate_resolver_enforcer.py::test_no_delegator_subject_refuses_no_principal PASSED [ 90%]
test_render_delegate_resolver_enforcer.py::test_no_bundle_loader_configured_refuses_rather_than_serving_unpinned PASSED [ 95%]
test_render_delegate_resolver_enforcer.py::test_no_refusal_carries_protected_bytes_for_a_render_delegate PASSED [100%]

============================= 20 passed in 15.34s =============================
```

## Suite 2 -- `infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py` (the REAL pre-existing suite, via the wrapper)

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\AndrewBerman\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\tmp\wk-irpt-17-15
configfile: pytest.ini
plugins: anyio-4.12.1, langsmith-0.7.17, asyncio-1.3.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 29 items

infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_a_custodian_shaped_id_is_reported_as_unprojected_not_as_missing PASSED [  3%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_a_firm_principal_never_carries_a_firm_catalogue PASSED [  6%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_a_forged_firm_override_cannot_reach_another_firms_accounts PASSED [ 10%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_a_forged_header_changes_nothing PASSED [ 13%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_a_wholly_permitted_request_carries_no_partial_reason PASSED [ 17%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_a_wholly_unpermitted_request_is_unsupported_not_an_empty_lookalike PASSED [ 20%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_admin_with_a_firm_is_firm_operations_never_opal_global PASSED [ 24%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_an_unknown_ownership_schema_version_raises_rather_than_reading_as_empty PASSED [ 27%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_browser_safe_view_drops_every_server_only_property PASSED [ 31%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_contract_view_validates_and_drops_the_local_census PASSED [ 34%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_every_trusted_header_is_actually_injected_at_the_line_it_claims PASSED [ 37%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_every_unmatched_ownership_id_carries_exactly_one_reason PASSED [ 41%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_fingerprint_is_stable_and_contract_shaped PASSED [ 44%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_fingerprint_moves_when_one_account_is_removed PASSED [ 48%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_fingerprint_moves_when_only_the_entitlement_revision_moves PASSED [ 51%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_firm_operations_gets_the_firm_population_bounded_by_the_verified_firm PASSED [ 55%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_headers_outside_the_allow_list_are_dropped_and_counted PASSED [ 58%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_lambda_edge_and_multivalue_header_shapes_both_normalize PASSED [ 62%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_missing_origin_marker_or_subject_is_unknown PASSED [ 65%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_no_advisor_id_and_no_admin_is_unknown_and_grants_nothing PASSED [ 68%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_only_an_opal_principal_carries_the_catalogue PASSED [ 72%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_opal_global_requires_the_explicit_roster PASSED [ 75%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_overlap_never_double_counts PASSED [ 79%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_partly_permitted_relationship_returns_the_subset_with_a_reason PASSED [ 82%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_permitted_set_is_the_intersection_and_never_the_grant_alone PASSED [ 86%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_revoked_entitlement_resolves_to_nothing_with_a_reason PASSED [ 89%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_the_resolver_carries_no_partner_role_vocabulary PASSED [ 93%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_the_same_request_in_strict_mode_is_unsupported_and_returns_nothing PASSED [ 96%]
infra\aws\lambda\investor-reporting\_scope\tests\test_resolve.py::test_trusted_set_is_exactly_the_nine_the_validator_injects PASSED [100%]

============================= 29 passed in 0.16s ==============================
```

Note (row `IRPT_BCKEND-W15-S2`): `test_every_trusted_header_is_actually_injected_at_the_line_it_claims`
was FAILING at this worktree's base commit (`86ba92ceb5`), before this cell's own edits, because
`TRUSTED_HEADERS`' stored line numbers (383-391) had drifted from the real injection block in
`auth-validator-edge/index.mjs` (now at 400-408). This cell re-pinned the line numbers
(production code, not the test) so the criterion's own bar -- every pre-existing test passing --
is met.

Also, per BOUNDS ("or elsewhere"), the full pre-existing `_authz/tests/` suite (141 tests) and
the `_scope/tests/test_global.py` suite (21 tests) were run separately and pass unmodified --
both import the SAME `resolve.py`/`enforce.py` this cell edited. `test_render_delegate_resolver_
enforcer.py::test_the_pre_existing_scope_and_authz_suites_still_pass_unmodified` (suite 1, above)
re-proves the `_scope`/`_authz` halves of this from inside this cell's own test file too.

## Suite 3 -- `test_edge_render_delegate_v2_authorizer.mjs` (Node, V2 authorizer render branch, arm (d))

```
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/performance/{accountSetId}',
  method: 'GET'
}
Render token authorized: {
  route: 'GET /api/scoped/investor-reporting/performance/{accountSetId}',
  claimName: 'accountSetId'
}
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/analysis/{jobId}/sections',
  method: 'GET'
}
Render token authorized: {
  route: 'GET /api/scoped/investor-reporting/analysis/{jobId}/sections',
  claimName: 'jobId'
}
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/narrative/{reportId}',
  method: 'GET'
}
Render token authorized: {
  route: 'GET /api/scoped/investor-reporting/narrative/{reportId}',
  claimName: 'reportId'
}
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/holdings/{accountSetId}',
  method: 'GET'
}
Render token presented on a non-render route: GET /api/scoped/investor-reporting/holdings/{accountSetId}
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/performance/{accountSetId}',
  method: 'GET'
}
Render token path id does not match its claim: {
  route: 'GET /api/scoped/investor-reporting/performance/{accountSetId}',
  claimName: 'accountSetId',
  pathIdPresent: true
}
Authorizer invoked: { path: '/investor-reporting/print', method: 'GET' }
Render token presented on a non-render route: GET /investor-reporting/print
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/performance/{accountSetId}',
  method: 'GET'
}
Render token verification failed: { error: 'invalid signature', name: 'JsonWebTokenError' }
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/performance/{accountSetId}',
  method: 'GET'
}
Render token verification failed: { error: 'jwt expired', name: 'TokenExpiredError' }
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/performance/{accountSetId}',
  method: 'GET'
}
Render token verification failed: {
  error: 'jwt issuer invalid. expected: opal-irpt-render',
  name: 'JsonWebTokenError'
}
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/performance/{accountSetId}',
  method: 'GET'
}
Token verified successfully: {
  email: 'advisor.a@49financial.com',
  tier: 'partner',
  role: 'user',
  userType: 'Advisor'
}
Authorization context: {
  email: 'advisor.a@49financial.com',
  tier: 'partner',
  role: 'user',
  userType: 'Advisor',
  allowedFirmIds: '49financial'
}
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/holdings/{accountSetId}',
  method: 'GET'
}
Token verified successfully: {
  email: 'advisor.a@49financial.com',
  tier: 'partner',
  role: 'user',
  userType: 'Advisor'
}
Authorization context: {
  email: 'advisor.a@49financial.com',
  tier: 'partner',
  role: 'user',
  userType: 'Advisor',
  allowedFirmIds: '49financial'
}
Authorizer invoked: {
  path: '/api/scoped/investor-reporting/performance/{accountSetId}',
  method: 'GET'
}
Token verified successfully: {
  email: 'advisor.a@49financial.com',
  tier: 'partner',
  role: 'user',
  userType: 'Advisor'
}
Authorization context: {
  email: 'advisor.a@49financial.com',
  tier: 'partner',
  role: 'user',
  userType: 'Advisor',
  allowedFirmIds: ''
}
✔ RENDER_ROUTE_CLAIMS names exactly the three GETs, each to its own path-id claim (24.327ms)
✔ the three named routes, each with its matching path id, are authorized (7.2396ms)
✔ a fourth, non-render-scoped route is denied outright, never a fallthrough (1.1986ms)
✔ the same route with a swapped path id is denied (1.3378ms)
✔ a render token on a print-adjacent but unlisted route is denied (1.3017ms)
✔ a token claiming the render audience but signed by the WRONG key is denied (1.2618ms)
✔ an expired render token is denied (2.0547ms)
✔ a wrong-issuer render-audience token is denied (2.1353ms)
✔ isRenderAudienceToken is a claim PEEK, true only for aud=irpt-render (2.0062ms)
✔ arm (f) -- a human portal token behaves exactly as before on the SAME routes (negative-widening: this cell never touches the human path) (3.0982ms)
✔ a human token that happens to name accountSetId in pathParameters still authorizes normally (not accidentally parsed by the render route table) (1.5229ms)
ℹ tests 11
ℹ suites 0
ℹ pass 11
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 396.6955
```

Row `IRPT_BCKEND-W15-S4` records the dependency-resolution friction this suite needed to work
around (transient, gitignored, never-committed local `node_modules`) and why the real render-key
secret fetch is deferred to the deploy round.

## Denominators

- Suite 1 (new): 20 of 20 PASSED, rc=0.
- Suite 2 (pre-existing, real file via wrapper): 29 of 29 PASSED, rc=0 -- every pre-existing
  assertion, unmodified.
- Suite 3 (Node, V2 authorizer): 11 of 11 PASSED, rc=0.
- Supplementary (not part of R117-AC2's own invocation, run for BOUNDS' "or elsewhere"):
  `_authz/tests/` 141 of 141 PASSED; `_scope/tests/test_global.py` 21 of 21 PASSED.
