# Never-widen sign-off packet -- IB-pr-409: irpt-narrative -- a no-row Opal caller classes UNKNOWN as live does; the TypeError fix and the opal-capital binding kept

Prepared by 0.9.0_WK_IRPT_BCKEND~272 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO ADDENDUM 18.1, msg 3284, on row `IRPT_BCKEND-D2-S48`). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays against a SYNTHETIC directory, AWS reads only (the live zip, its layer, its CodeSha256 and S3 version); no client-data enumeration. Files beside this packet: `IB110-1_release_census.json`, `IB110-1_release_replay.json`, `IB110-1_red_list.json`, `replay/` (the scripts). This packet SUPERSEDES `0.9.0_WK_IRPT_BCKEND~264/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-399.md`: its artifact `QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw=` is the build IB-pr-401 STOPPED on and is no longer the one to sign.

**READ THIS FIRST.**

1. **The fix.** The shared `served.Entry.handle` hands `enforcer_for` the caller's own email as the Opal roster for every verified Opal internal caller; for a caller with NO maintained profile row that classes OPAL_GLOBAL (`enforce.py:790`: any advisor in its own firm), where the live irpt-narrative hands no roster and classes UNKNOWN. `narrative/entry.py` now drives the shared handle on a request-local copy of the entry whose `enforcer_for` passes the roster through `NarrativeEntry._live_roster`: a roster naming a caller with no profile row (`_internal_allowed_firms` -> None), or whose row cannot be read, is replaced by None, which is exactly what the live boundary hands. Only irpt-narrative changes, and only `narrative/entry.py` among its members relative to IB-pr-399.
2. **The shared `_authz/served.py` is UNCHANGED**: `git diff bd9c06d2fb HEAD -- infra/aws/lambda/investor-reporting/_authz/` is empty (blob `12b0ac90c8` at the base and at the pin), and no other host's code is touched. The packaged `served.py` member is the STAGED blob `_authz/served.py@74a62fb46c` (sha256 prefix `87d9ecc49747`, the same as IB-pr-399's census), which the source map pins and this cell does not edit.
3. **The enforcer-scope arm now reads IDENTICAL**, driven as in row D2-S48 (each tree's own `_scope.resolve` with the roster that tree's boundary hands `enforcer_for`): live and built both class the no-row caller UNKNOWN with nothing granted. Its NEGATIVE CONTROL, the stopped `QiNRKpaC` entry.py, reads OPAL_GLOBAL on the same arm and grants the whole synthetic firm population, so the harness is reaching the cell it measures.
4. **ONE difference remains, outside this order and stated rather than hidden (row `IRPT_BCKEND-D2-W272-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2):** a caller WITH a maintained profile row (`allowedFirmIds` non-empty) keeps the roster the shared boundary hands it, as the order says ("a row-listed caller is unchanged"), so it classes OPAL_GLOBAL on built where live classes it UNKNOWN. That is the same class change IB-pr-399 carried for that caller (built == stopped on the arm below); this cell does not change it and does not widen it. The signer decides it.

## Root cause and fix

- **Cause (row D2-S48).** The restaged `served.py` computes `principals = frozenset([email]) if subject is not None else self.opal_principal_ids` and calls `self.enforcer_for(verified, principals)`. The live boundary called `enforcer_for(verified)`. `resolve.classify_principal` puts the roster check (branch 2) before the advisor and admin branches, so a roster hit is OPAL_GLOBAL.
- **Fix (`narrative/entry.py`, this cell's code commit `b8a49eee0e`).** `NarrativeEntry.handle` makes `view = copy.copy(self)` (the warm Entry is never mutated, and an `enforcer_for` stub installed on the instance is still the callee), installs a wrapper that calls the original `enforcer_for(tenant, self._live_roster(roster))`, and runs `served.Entry.handle(view, ...)`. The IB-pr-399 selection drop (`_held_to_verified_firm`) is unchanged. The roster is replaced only when it is a request-local email set whose caller has no profile row; a row read error grants nothing (fail closed to the live roster); None and the Entry's own roster pass through.
- **Tests** (`narrative/tests/test_no_row_unknown.py`, 13 items, `-k no_row_unknown`): a flat `python -I` tree built the way the builder builds it (staged blobs at their pin, sha256-verified), the real `entry.ENTRY`, an enforcer stub that records the roster, then that tree's own `resolve.classify_principal`. No-row callers (no row, attribute absent, empty list, null list, selecting another firm, own firm, no selection) get roster None and class UNKNOWN; a read error, an `ALL` row and a service principal grant nothing; a row-listed caller and a plain firm user match the shared boundary; the warm Entry is not mutated; the CONTROL drives the shared `served.Entry` and must read OPAL_GLOBAL. With the fix reverted 9 of the 13 fail. The existing `-k served_error_path` and `-k opal_capital_binding` tests pass; narrative suite 69 passed.

## The pin and the build

- **Release pin P: `b8a49eee0e580ebb9a80949a1e5469af7663e0e4`** (branch `wk-IRPT_BCKEND-272`): the code commit. Everything committed after it is deliverables and rows; none touches `lambda-source-map.json`, the host tree or `_authz/`.
- The source map needed no edit (`entry.py` is already in narrative's `files[]`).
- Census: `infra/aws/lambda/ci/release-census.py irpt-narrative --pin P --map infra/aws/lambda/ci/lambda-source-map.json`, live zip read from AWS (read only).
- BUILD_ONLY from a clean tree (porcelain 0 lines before and after both builds), built twice, byte-identical: **YES**. Command: `TMPDIR=<scratch> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` (the REAL source map, no override). The zip is kept in scratch only; nothing uploaded.
- **Built sha256 (CodeSha256 form): `iEwSFL34JQJbihTmChB79GkjXwJaEl9WzMJY2sBEs4k=`** -- different from the stopped `QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw=`. 21 of the 22 changed members carry the same sha256 prefix as IB-pr-399's census; the one that differs is `entry.py` (`3a64eed013e7`).

| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |
|---|---|---|---|---|---|---|
| `irpt-narrative` | `iEwSFL34JQJbihTmChB79GkjXwJaEl9WzMJY2sBEs4k=` | `884c1214bdf82502`... | 216107 | `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=` | 22 | `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` |

`live_before` = `aws lambda get-function-configuration` CodeSha256 (last modified 2026-09-21T15:05:28.000+0000); it equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`: **yes**, which is the rollback version.

## Changed members and their owners (every one owned)

`irpt-narrative` -- function=irpt-narrative pin=b8a49eee0e built_members=27 live_members=19; changed_members=22
- changed `enforce.py` (built `18f04af84b9c`, live `d1c8e7e09467`): e9311289b1, 4bca50737e
- changed `entry.py` (built `3a64eed013e7`, live `ca9d9d47eec8`): b8a49eee0e, cabad9008c, 630de21b95
- changed `errors.py` (built `b60f25ccaa70`, live `784ee313ed70`): 4fffe13f01
- changed `event_policy.json` (built `346e626bad4e`, live `d60745bedcb2`): a12b0df4e7
- changed `evidence.py` (built `6a3064cc866f`, live `fe7a41c46df0`): ac4eb443b3
- changed `fixtures/FIXTURE_MANIFEST.json` (built `f04956460562`, live `0d7ee782eb64`): a12b0df4e7
- changed `fixtures/performance_report_inf.json` (built `753e3cc6cb07`, live `f9fe05d6bcf5`): a12b0df4e7
- changed `fixtures/topics_predating.json` (built `835800678898`, live `dfb1bacca07f`): a12b0df4e7
- changed `fixtures/topics_window.json` (built `9d7473e24dfc`, live `8a4290315e78`): a12b0df4e7
- changed `handler.py` (built `8deb7938ee7f`, live `f04a619fd0cb`): ac4eb443b3
- changed `loaders.py` (built `b84bb2918fc1`, live `0c086052e6e6`): 79c4d64a0c, ffbffcac50, 81785d9ae3
- changed `prose.py` (built `6a3df88e25ee`, live `171c3898e971`): 118612b599, ac4eb443b3
- changed `resolve.py` (built `24b407fa00ff`, live `086a55a7d9d4`): 81785d9ae3, a0967bb920, 4bca50737e
- changed `served.py` (built `87d9ecc49747`, live `ba0cea6d4246`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e, cd9a61bb0c +22
- added `canonical_profile_reads.py` (built `0ec4a717f2aa`, live `-`): 2704705672
- added `custody.py` (built `23cda6b0e3dd`, live `-`): 4911c398d9
- added `keys.py` (built `56ee3cc22e80`, live `-`): 48313e9c0e
- added `maintained_sources.py` (built `774eca9bde60`, live `-`): 15b9f85eb3
- added `owner_reads.py` (built `f9e1f5d3274e`, live `-`): 4911c398d9
- added `prospect.py` (built `b7e5c9335caa`, live `-`): a85e7d6329
- added `selection.py` (built `7ba910b85e2f`, live `-`): a176e4bc11
- added `selection_store.py` (built `583507a70e3a`, live `-`): 33e630885f

Owners are the commits that touched each member's source path after the commit holding the LIVE blob, up to the commit holding the BUILT blob (an added member: the commit that introduced the blob). `entry.py` is owned by this cell's code commit `b8a49eee0e`.

## Blast radius

- **Function:** `irpt-narrative` only (one route, `GET /api/scoped/investor-reporting/narrative/{reportId}`). No other function, layer, IAM, route, schedule, environment or table changes.
- **Members:** the 22 changed members above vs live; relative to the stopped IB-pr-399 build, ONE member differs: `entry.py`.
- **Shared code:** `_authz/served.py` is unchanged (blob `12b0ac90c8`); the fix lives in `narrative/entry.py` only.
- **Effect on served bytes:** a no-row Opal internal caller is bound to opal-capital (IB-pr-399) AND classed UNKNOWN as live (this cell); a row-listed caller is narrowed and classed as on IB-pr-399; the TypeError is fixed.

## Writers of the changed property

- **The Opal roster handed to `enforcer_for`.** Writers: **N=2**: `served.Entry.handle`'s `principals = ...` (shared, unchanged) and `NarrativeEntry._live_roster` (this cell). The second can only REPLACE a non-empty request-local roster with None; it cannot add a principal.
- **The firm a request is bound to:** unchanged by this cell (IB-pr-399's `_held_to_verified_firm`).

## The red list (CTO ADDENDUM 18, row D2-S46)

`pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/` at the pin: **9 failed, 176 passed, 13 skipped in 9.69s**. The FAILED node ids (9):
- `_contracts\test_owned_request_contracts.py::test_public_routes_are_declared_against_the_installed_status_handler`
- `_contracts\test_upload_contract.py::test_route_denominators_are_measured_and_upload_is_declared_against_generate`
- `_contracts\tests\test_seam_paired.py::test_the_consumer_fixture_source_is_named_and_non_empty`
- `_contracts\tests\test_seam_paired.py::test_every_declared_route_has_a_response_contract_whose_refs_resolve`
- `_contracts\tests\test_seam_paired.py::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]`
- `_contracts\tests\test_seam_paired.py::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[custody-report-persist]`
- `_contracts\tests\test_seam_paired.py::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[custody-report-read]`
- `_contracts\tests\test_seam_paired.py::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[export-receipt]`
- `_contracts\tests\test_seam_paired.py::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[submit-export]`

Their targets are the public-route count against the installed status handler, the upload route denominator, and the response contracts / fixtures of `analysis-request-original, custody-report-persist, custody-report-read, export-receipt, submit-export`. This cell changes 2 paths vs its base (infra/aws/lambda/investor-reporting/narrative/entry.py, infra/aws/lambda/investor-reporting/narrative/tests/test_no_row_unknown.py); the packaged members' source paths number 22. Intersection with the red tests' target surface (`infra/aws/lambda/investor-reporting/_contracts/`, `docs/contracts/investor-reporting/`) and with any path naming a red operation: **0 changed, 0 member, 0 naming** -- STOP = **no**. No investor-reporting `_contracts` test about `narrative-packet` is red. This packet does not cite "suite green".

## The enforcer-scope arm (row D2-S48's method)

Driven with the resolver's OWN TRUSTED_HEADERS: x-origin-verify=cloudfront, x-user-email=ops@opalinvest.com, x-firm-id=opal-capital; x-advisor-id, x-user-role, x-user-type absent. Directory: SYNTHETIC (two opal-capital accounts, one account of another firm); ownership empty. One tree per process.

| case | live (class / roster / permitted) | built (this cell) | stopped QiNRKpaC (negative control) |
|---|---|---|---|
| no_row_no_selection | UNKNOWN / roster None / permitted_account_set 0 | UNKNOWN / roster None / permitted_account_set 0 | OPAL_GLOBAL / roster ['ops@opalinvest.com'] / permitted_account_set 2 |
| no_row_selecting_other | UNKNOWN / roster None / permitted_account_set 0 | UNKNOWN / roster None / permitted_account_set 0 | OPAL_GLOBAL / roster ['ops@opalinvest.com'] / permitted_account_set 2 |
| row_listed_no_selection | UNKNOWN / roster None / permitted_account_set 0 | OPAL_GLOBAL / roster ['ops@opalinvest.com'] / permitted_account_set 2 | OPAL_GLOBAL / roster ['ops@opalinvest.com'] / permitted_account_set 2 |

The first two rows are the arm: built == live, UNKNOWN, nothing granted (`identical`). The stopped tree reads OPAL_GLOBAL with the whole synthetic firm population (negative control, `expected-diff`). The third row is the one remaining difference (item 4 above).

## The replay (offline; live versus built artifacts; `IB110-1_release_replay.json`)

The replay drives the zip's own `entry.ENTRY` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layer extracted beside it), profile row injected and `enforcer_for` stubbed to raise. IB-pr-399's 13 arms re-run (same names, same verdicts) plus 3 new arms: `no_row_internal_enforcer_scope`, its negative control, and the row-listed caller against the stopped build. Verdicts are exactly `identical` or `expected-diff`; 16 arms, no UNEXPECTED.

| arm | verdict | negative control | detail |
|---|---|---|---|
| plain firm user (x-firm-id cottonwood), no selection: bound to its OWN firm through the built zip, same (firm, code) as the live zip | identical | no | 1 of 1 routes |
| plain firm user selecting inflection: refused FIRM_BINDING through the built zip; the live zip never reaches inflection either (another firm is refused) | expected-diff | yes | 1 of 1 routes refused FIRM_BINDING on built and never reached inflection on live; 0 of 1 identical built vs live (irpt-narrative live=cottonwood/UNEXPECTED) |
| plain firm user restating firm_id=inflection in the query: refused FIRM_BINDING through the built zip, same as the live zip | identical | yes | 1 of 1 routes |
| internal caller WITH a profile row allowedFirmIds [cottonwood], selecting cottonwood: admitted and bound to cottonwood through the built zip (live ignores the selection) | expected-diff | no | 1 of 1 routes admitted on built (bound to cottonwood); live bound to cottonwood on 0 (live zips: irpt-narrative=opal-capital) |
| internal caller, row [cottonwood], selecting inflection: refused FIRM_BINDING through the built zip (live: see detail) | expected-diff | yes | 1 of 1 routes refused on built; live bound to inflection on 0 (irpt-narrative live=opal-capital/UNEXPECTED) |
| no_row_internal_selects_other_firm | identical | no | an Opal internal caller (x-firm-id opal-capital) with NO profile row selecting inflection, through the REAL entry.ENTRY of each zip: 1 of 1 routes bind to the same firm with the same code (built opal-capital/UNEXPECTED, live opal-capital/UNEXPECTED); the Opal roster handed to enforcer_for (recorded, not part of the verdict): irpt-narrative built=None live=None |
| NEGATIVE CONTROL: the same built tree with entry.py put back to its pre-IB-pr-399 bytes binds the no-row internal caller to inflection (the widening this cell removes) | expected-diff | yes | 1 of 1 routes bind to inflection without NarrativeEntry (pre-binding entry.py = 6cbf2707cf) |
| a row-listed caller is narrowed identically with and without NarrativeEntry (row [cottonwood] selecting inflection: refused FIRM_BINDING) | identical | no | 1 of 1 routes refused on built and 1 of 1 on the pre-binding entry |
| internal_error_refusal | identical | no | an internal error (the enforcer cannot be built) is recorded and refused through the BUILT zip's real entry.ENTRY: 1 of 1 routes answer ok=false, public_reason_code UNEXPECTED, no internal_correlation_id on the wire status, nothing escapes the boundary (no TypeError), and print exactly one irpt_error line of the staged errors.py shape ['correlation_id', 'event', 'operation', 'public_reason_code']; built: irpt-narrative escaped=None code=UNEXPECTED log_events=1 |
| NEGATIVE CONTROL: internal_error_refusal through the same built tree with errors.py put back to the pre-IB-pr-394 blob (bc3727b3a3): the TypeError escapes the boundary | expected-diff | yes | 1 of 1 routes: escaped=TypeError |
| error path: no case through the built zips raises (no HARNESS_* code), i.e. served._record meets the staged errors.py without TypeError | identical | no | 1 routes x 7 cases each; HARNESS_* codes on built: none; on live: none |
| NEGATIVE CONTROL: the same built trees with errors.py put back to the pre-IB-pr-394 narrative blob (bc3727b3a3) raise TypeError on the error path | expected-diff | yes | 1 of 1 routes answer HARNESS_TypeError in all three probed cases |
| NEGATIVE CONTROL: svc-custody-statement (cottonwood) on these hosts' operations is never on the Opal roster through the built zip | identical | yes | 1 of 1 routes: built code irpt-narrative=UNEXPECTED |
| no_row_internal_enforcer_scope | identical | no | row D2-S48's method: an Opal internal caller (x-origin-verify cloudfront, x-user-email ops@opalinvest.com, x-firm-id opal-capital; x-advisor-id, x-user-role, x-user-type absent) with NO profile row, through each tree's REAL entry.ENTRY, then each tree's OWN _scope.resolve with the roster THAT TREE's boundary hands enforcer_for, against a SYNTHETIC directory (2 opal-capital accounts, 1 of another firm; no client data). No selection: live roster=None class=UNKNOWN permitted=0; built roster=None class=UNKNOWN permitted=0. Selecting inflection: live roster=None class=UNKNOWN permitted=0; built roster=None class=UNKNOWN permitted=0. Class and permitted_account_set identical, both UNKNOWN, nothing granted |
| NEGATIVE CONTROL: the stopped build's entry.py (IB-pr-399 @cabad9008c, the tree whose sha256 is QiNRKpaC, row D2-S48) on the same enforcer-scope arm reads OPAL_GLOBAL and grants the whole firm population | expected-diff | yes | stopped roster=['ops@opalinvest.com'] class=OPAL_GLOBAL permitted=2; stopped roster=['ops@opalinvest.com'] class=OPAL_GLOBAL permitted=2 (live: live roster=None class=UNKNOWN permitted=0) |
| a row-listed internal caller's roster and class through the built zip are unchanged from the stopped IB-pr-399 build (live: UNKNOWN; see detail and the packet) | identical | no | row [cottonwood], no selection: live roster=None class=UNKNOWN permitted=0; built roster=['ops@opalinvest.com'] class=OPAL_GLOBAL permitted=2; stopped roster=['ops@opalinvest.com'] class=OPAL_GLOBAL permitted=2. built == stopped on roster, class and permitted set: True. Against live this caller still differs (live hands no roster); that difference is outside this cell's order and is stated in the packet |

## Branch A (released)

1. From a clean tree at P `b8a49eee0e580ebb9a80949a1e5469af7663e0e4` (or a descendant whose `lambda-source-map.json`, `narrative/` and `_authz/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` and compare the printed sha256 to `iEwSFL34JQJbihTmChB79GkjXwJaEl9WzMJY2sBEs4k=` (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`).
2. The Terraform deploy path of the module `infra/aws/terraform/investor-reporting/narrative/lambda.tf`; no IAM, route, schedule, layer or environment change. Effect on served bytes: narrative answers through `served.py` `74a62fb46c`'s boundary (unchanged shared file) with the TypeError fixed, a no-row internal caller on opal-capital and classed UNKNOWN as live, a row-listed caller narrowed, and the members listed above added or changed.
3. Per-family image/layer: none touched. The ledger entry names irpt-narrative.

## Branch B (rolled back)

- `irpt-narrative`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` (its CodeSha256 is the `live_before` value `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest.

The source-map state reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).

## The replay arm for the applier (rerun before the ledger)

From the repo root, scratch directory OUTSIDE the worktree holding `zips/irpt-narrative.1.zip` (the zip to be uploaded): `python <deliverables>/replay/run_replay.py <scratch> b8a49eee0e580ebb9a80949a1e5469af7663e0e4 <out.json>` (reads the live zip and the layer from AWS, runs `replay/authz_case_runner.py` and `replay/enforcer_scope_runner.py` per tree). STOP the apply if `no_row_internal_enforcer_scope`, `no_row_internal_selects_other_firm` or `internal_error_refusal` is not `identical`, if any arm is `UNEXPECTED`, if the error-path arm shows a HARNESS_ code, or if a NEGATIVE CONTROL does not behave (the harness then is not reaching the cell it measures). The IB-pr-399 half's other conditions are unchanged. Delete the scratch directory afterwards.

## The after-read

One request as an Opal internal caller selecting another firm: expected the answer bound to opal-capital (as before); one refused request (e.g. a firm user selecting another firm) logs one `irpt_error` JSON line with the public reason code and no `TypeError` in the function's log group. Either read is UNEXERCISED until the apply; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.

## Rows

`IRPT_BCKEND-D2-W272-S1` (OBSERVATION, ARMED, disarm owner 2.0.0_SA_COO~P2): a row-listed internal caller still classes OPAL_GLOBAL on built vs UNKNOWN on live (unchanged from IB-pr-399, per the order). `IRPT_BCKEND-D2-W272-S2` (OBSERVATION, INERT): the IB-pr-399 replay driver derived its pre-binding control from `pin^`, which at this pin is IB-pr-399's own entry; the control is now pinned to `cabad9008c^`.
