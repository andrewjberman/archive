# Never-widen sign-off packet -- IB-pr-399: irpt-narrative -- the TypeError fixed while a no-row internal caller stays bound to opal-capital

Prepared by 0.9.0_WK_IRPT_BCKEND~264 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO half @7f294053f0, msg 2765, on row `IRPT_BCKEND-D2-W262-S1`; the TypeError is row `IRPT_BCKEND-D2-W201-S6`). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. Files beside this packet: `IB102-3_release_census.json`, `IB102-3_release_replay.json`, `replay/` (the scripts). This packet SUPERSEDES the irpt-narrative half of `0.9.0_WK_IRPT_BCKEND~262/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md` (its artifact `NbzUcWz1...` is no longer the one to sign; holdings is unaffected).

**READ THIS FIRST.**

1. **The fix.** IB-pr-394's restage (narrative's `errors.py` and `served.py` rows to `74a62fb46c`) is kept: it removes the TypeError. What changes is narrative's own `entry.py`: `ENTRY` is now a `NarrativeEntry` (a subclass of the shared `served.Entry`) whose `handle` drops `selected_tenant` before the shared boundary reads it, for ONE case only -- an Opal internal caller (`verified_internal_subject`, not the svc-custody subject, not `x-user-type: service`) that has NO maintained profile row (`_internal_allowed_firms` returns None: no row, no attribute, or an empty list). That caller stays on its verified `X-Firm-Id` (`opal-capital`), as it does on the live function, whatever it selects, including a firm the registry does not know. The shared `_authz/served.py` and every other host are untouched.
2. **A caller with a profile row is narrowed as on the other hosts** (row-listed selection admitted and bound to the selected firm; unlisted refused FIRM_BINDING; a malformed row or `ALL` refused). Live narrative ignored the selection for such a caller too, so a row-listed caller selecting a listed firm now binds to that firm where live bound opal-capital -- the IB-pr-387 narrowing, narrower than the no-row reach this cell removes, and the same as every other host.
3. **One difference remains and is NOT closed by this cell (row `IRPT_BCKEND-D2-W264-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2): the Opal roster.** The arm below is identical on the bound firm and the public code. The roster the boundary hands `enforcer_for` is not: live hands none, the built boundary hands the caller's own email, which `classify_principal` reads as OPAL_GLOBAL inside opal-capital. That is a property of the shared `served.py` the order does not let a worker edit, it rode in with IB-pr-394's restage, and its effect on what a narrative request may name was not measured. The signer decides it.

## Root cause and fix

- **TypeError (row W201-S6).** `served._record` calls `errors.public_line(..., admitted=)`; narrative's staged `errors.py` (`bc3727b3a3`) lacks the keyword. Fixed by IB-pr-394 (rows restaged to `74a62fb46c`), kept here unchanged; tests `-k served_error_path` (4) pass.
- **Widening (row W262-S1).** The restaged `served.py` honours `selected_tenant`; with no profile row an internal caller was admitted for any registered firm. Fixed in `narrative/entry.py` (`NarrativeEntry._held_to_verified_firm`, `_drop_selection`) at the code commit `cabad9008c`. Any error reading the selection or the row falls through to the shared boundary, which refuses.
- **Tests** (`narrative/tests/test_opal_capital_binding.py`, 12 test items over 14 cases, `-k opal_capital_binding`): a flat `python -I` tree built the way the builder builds it (staged blobs at their pin, sha256-verified), the real `entry.ENTRY`, an enforcer stub that records the firm it is asked for. No-row internal selecting inflection is bound to opal-capital via the query, a JSON body, a base64 body, a nested `selection`, a row without the attribute and an empty list; an own-firm selection and no selection are unchanged; a row-listed caller is admitted on its list and refused off it; `ALL` is refused; a plain firm user selecting another firm is refused; an unregistered firm is not refused wider; and a NEGATIVE CONTROL runs the shared `served.Entry` with the same event and must bind inflection.

## The pin and the build

- **Release pin P: `cabad9008cc06080562a444640116ae8445423be`** (branch `wk-IRPT_BCKEND-264`): the code commit. Everything committed after it is deliverables and the surprise row; none touches `lambda-source-map.json`, the host tree or `_authz/`.
- The source map needed no edit: `entry.py` is already in narrative's `files[]` and the `served.py`/`errors.py` rows are IB-pr-394's.
- Census: `infra/aws/lambda/ci/release-census.py irpt-narrative --pin P --map infra/aws/lambda/ci/lambda-source-map.json`, live zip read from AWS (read only).
- BUILD_ONLY from a clean tree (porcelain 0 lines before and after both builds), built twice, byte-identical: **YES**. Command: `TMPDIR=<scratch> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` (the REAL source map, no override). The zip is kept in scratch only; nothing uploaded.

| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |
|---|---|---|---|---|---|---|
| `irpt-narrative` | `QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw=` | `4223512a9682a17e`... | 215376 | `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=` | 22 | `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` |

`live_before` = `aws lambda get-function-configuration` CodeSha256 (last modified 2026-09-21T15:05:28.000+0000); it equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`: **yes**, which is the rollback version.

## Changed members and their owners (every one owned)

`irpt-narrative` -- function=irpt-narrative pin=cabad9008c built_members=27 live_members=19; changed_members=22
- changed `enforce.py` (built `18f04af84b9c`, live `d1c8e7e09467`): e9311289b1, 4bca50737e
- changed `entry.py` (built `b914faa7f698`, live `ca9d9d47eec8`): cabad9008c, 630de21b95
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

Owners are the commits that touched each member's source path after the commit holding the LIVE blob, up to the commit holding the BUILT blob (an added member: the commit that introduced the blob). `entry.py` is owned by this cell's code commit `cabad9008c` and `630de21b95`. The other 21 members are IB-pr-394's list unchanged: the map's staged pins and source files, which no cell of this order changes; they release with it because live narrative was last built 2026-09-21.

## Writers of the changed property

- **The firm an internal caller's request is bound to.** Writers of the bound firm in `served.Entry.handle`: **N=2**: `verified = header(headers, 'X-Firm-Id')` (the edge-verified claim) and `verified = selected` after the selection checks. This cell adds one gate BEFORE the second: `NarrativeEntry` removes the selection from the event for a no-row non-service internal caller, so the second writer never fires for it. Both branches are covered by the replay and the tests: with a row, narrowed; with NO row, bound to the verified firm.
- **The Opal roster handed to `enforcer_for`:** unchanged by this cell and different from live (row W264-S1).

## The route: admitted and another-firm-refused

Route set: `docs/contracts/investor-reporting/v1/routes.json` at P, handler `irpt-narrative`: 1 route. Columns: **U-own** plain firm user (x-firm-id cottonwood), no selection; **U-other** that user selecting inflection; **U-claim** that user restating firm_id=inflection; **A** internal caller with row `[cottonwood]` selecting cottonwood; **B** that caller selecting inflection; **C** an unrelated Opal internal caller with NO row selecting inflection (built / live); **S** svc-custody-statement on this operation. Cells are `bound firm/public code`; UNEXPECTED is the stub's own stop after admission.

| route | U-own | U-other | U-claim | A (built / live) | B (built / live) | C (built / live) | S |
|---|---|---|---|---|---|---|---|
| GET /api/scoped/investor-reporting/narrative/{reportId} (`narrative-packet`) | cottonwood/UNEXPECTED | None/FIRM_BINDING (live cottonwood/UNEXPECTED) | cottonwood/FIRM_BINDING | cottonwood/UNEXPECTED / opal-capital/UNEXPECTED | None/FIRM_BINDING / opal-capital/UNEXPECTED | **opal-capital/UNEXPECTED / opal-capital/UNEXPECTED** | cottonwood/UNEXPECTED |

Reading: C is the cell this order is about -- built and live both bind opal-capital; before this cell (negative control row below) built bound inflection. A is a real change against live (built binds the listed firm, live bound opal-capital) and is the narrowing the other hosts have. B is refused where live would have bound opal-capital. For a plain firm user the built boundary refuses another firm, and the live boundary never reaches it. Tests cited as the second cover: `_authz/tests/test_allowed_firm_ids.py`, `_authz/tests/test_svc_custody_statement.py`, the four `served_error_path` tests and the twelve `opal_capital_binding` test items.

## The replay (offline; live versus built artifacts; `IB102-3_release_replay.json`)

The replay drives the zip's own `entry.ENTRY` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layer `irpt-common:5` extracted beside it), profile row injected and `enforcer_for` stubbed to raise, so every admitted case also crosses `served._record`. **admitted** = the boundary bound the request to the firm and handed `enforcer_for` the roster; **refused** = FIRM_BINDING / NOT_AUTHORIZED.

| arm | verdict | negative control | detail |
|---|---|---|---|
| plain firm user (x-firm-id cottonwood), no selection: bound to its OWN firm through the built zip, same (firm, code) as the live zip | identical | no | 1 of 1 routes |
| plain firm user selecting inflection: refused FIRM_BINDING through the built zip; the live zip never reaches inflection either (another firm is refused) | expected-diff | yes | 1 of 1 routes refused FIRM_BINDING on built and never reached inflection on live; 0 of 1 identical built vs live (irpt-narrative live=cottonwood/UNEXPECTED) |
| plain firm user restating firm_id=inflection in the query: refused FIRM_BINDING through the built zip, same as the live zip | identical | yes | 1 of 1 routes |
| internal caller WITH a profile row allowedFirmIds [cottonwood], selecting cottonwood: admitted and bound to cottonwood through the built zip (live ignores the selection) | expected-diff | no | 1 of 1 routes admitted on built (bound to cottonwood); live bound to cottonwood on 0 (live zips: irpt-narrative=opal-capital) |
| internal caller, row [cottonwood], selecting inflection: refused FIRM_BINDING through the built zip (live: see detail) | expected-diff | yes | 1 of 1 routes refused on built; live bound to inflection on 0 (irpt-narrative live=opal-capital/UNEXPECTED) |
| no_row_internal_selects_other_firm | identical | no | an Opal internal caller (x-firm-id opal-capital) with NO profile row selecting inflection, through the REAL entry.ENTRY of each zip: 1 of 1 routes bind to the same firm with the same code (built opal-capital/UNEXPECTED, live opal-capital/UNEXPECTED); the Opal roster handed to enforcer_for (recorded, not part of the verdict): irpt-narrative built=['ops@opalinvest.com'] live=None |
| NEGATIVE CONTROL: the same built tree with entry.py put back to its pre-IB-pr-399 bytes binds the no-row internal caller to inflection (the widening this cell removes) | expected-diff | yes | 1 of 1 routes bind to inflection without NarrativeEntry (pre-binding entry.py = 6cbf2707cf) |
| a row-listed caller is narrowed identically with and without NarrativeEntry (row [cottonwood] selecting inflection: refused FIRM_BINDING) | identical | no | 1 of 1 routes refused on built and 1 of 1 on the pre-binding entry |
| internal_error_refusal | identical | no | an internal error (the enforcer cannot be built) is recorded and refused through the BUILT zip's real entry.ENTRY: 1 of 1 routes answer ok=false, public_reason_code UNEXPECTED, no internal_correlation_id on the wire status, nothing escapes the boundary (no TypeError), and print exactly one irpt_error line of the staged errors.py shape ['correlation_id', 'event', 'operation', 'public_reason_code']; built: irpt-narrative escaped=None code=UNEXPECTED log_events=1 |
| NEGATIVE CONTROL: internal_error_refusal through the same built tree with errors.py put back to the pre-IB-pr-394 blob (bc3727b3a3): the TypeError escapes the boundary | expected-diff | yes | 1 of 1 routes: escaped=TypeError |
| error path: no case through the built zips raises (no HARNESS_* code), i.e. served._record meets the staged errors.py without TypeError | identical | no | 1 routes x 7 cases each; HARNESS_* codes on built: none; on live: none |
| NEGATIVE CONTROL: the same built trees with errors.py put back to the pre-IB-pr-394 narrative blob (bc3727b3a3) raise TypeError on the error path | expected-diff | yes | 1 of 1 routes answer HARNESS_TypeError in all three probed cases |
| NEGATIVE CONTROL: svc-custody-statement (cottonwood) on these hosts' operations is never on the Opal roster through the built zip | identical | yes | 1 of 1 routes: built code irpt-narrative=UNEXPECTED |

`internal_error_refusal` (issuer ruling per CTO analysis ADDENDUM 14, msg 2804, row W201-S6; AMENDMENT 1 to the order, recorded by 2.0.0_SA_COO~P2 at the drain) replays an internal error through the BUILT zip's real `entry.ENTRY`: the staged `errors.py` shape, one `irpt_error` line, no TypeError; its NEGATIVE CONTROL puts the old `errors.py` back and the TypeError escapes.

`no_row_internal_selects_other_firm` is **identical** on bound firm and public code; the roster is recorded in its detail and is the content of row W264-S1.

## Branch A (released)

1. From a clean tree at P (or a descendant whose `lambda-source-map.json`, `narrative/` and `_authz/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` and compare the printed sha256 to `QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw=` (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`).
2. The Terraform deploy path of the module `infra/aws/terraform/investor-reporting/narrative/lambda.tf`; no IAM, route, schedule, layer or environment change. Effect on served bytes: narrative answers through `served.py` `74a62fb46c`'s boundary with the TypeError fixed, a no-row internal caller still on opal-capital, a row-listed caller narrowed, and the members listed above added or changed.
3. Per-family image/layer: none touched. The ledger entry names irpt-narrative.

## Branch B (rolled back)

- `irpt-narrative`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` (its CodeSha256 is the `live_before` value `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest.

The source-map state reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).

## The replay arm for the applier (rerun before the ledger)

From the repo root, scratch directory OUTSIDE the worktree holding `zips/irpt-narrative.1.zip` (the zip to be uploaded): `python replay/run_replay.py <scratch> P <out.json>` (reads the live zip and the layer from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if `no_row_internal_selects_other_firm` is not `identical`, if any arm is `UNEXPECTED`, if the error-path arm shows a HARNESS_ code, or if either NEGATIVE CONTROL does not behave (the harness then is not reaching the cell it measures). Delete the scratch directory afterwards.

## The after-read

One request as an Opal internal caller selecting another firm: expected the answer bound to opal-capital (as before); one refused request (e.g. a firm user selecting another firm) logs one `irpt_error` JSON line with the public reason code and no `TypeError` in the function's log group. Either read is UNEXERCISED until the apply; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.

## Rows

`IRPT_BCKEND-D2-W264-S1` (OBSERVATION, ARMED, disarm owner 2.0.0_SA_COO~P2): the Opal roster. Closes by this cell: the firm-binding half of `IRPT_BCKEND-D2-W262-S1` (the roster half moves to W264-S1); the release itself stays with the signer.
