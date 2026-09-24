# IRPT_BCKEND.TO-IB-rtr-e -- THE ONE OFFLINE ACTUAL-MODULE CHAIN -- result

**Worker:** `0.9.0_WK_IRPT_BCKEND~21` | **Criterion:** `R118-AC5` (JUDGMENT, graded by `3.0.0_SA_CVO`
at L9, never self-graded here) | **Invocation:**
`cd deliverables/0.9.0_WK_IRPT_BCKEND~21 && py -3.12 test_actual_module_chain.py` | **rc=0**,
confirmed via the exact criterion invocation form.

## What was wired, and how

Two files: `test_actual_module_chain.py` (the entry point) and `chain_bridge.mjs` (a Node
subprocess helper, same pattern as the CVO's own read-only reference probe
`org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R17_PROBE.mjs`: a `node:module`
`registerHooks` intercept that blocks only the AWS-SDK network edge --
`SecretsManagerClient.send` / `DynamoDBClient.send` / `S3Client.send` all throw
`NETWORK FORBIDDEN` if ever reached -- and resolves `jsonwebtoken` to a real, locally
`bun install`-provisioned copy under `infra/aws/lambda-edge/auth-validator-edge/node_modules/`
(gitignored; `infra/.gitignore:116`, confirmed via `git check-ignore -v`; nothing under
`node_modules/` is staged or committed by this cell)).

Every step below calls the REAL exported function from the REAL file -- none is restated:

1. **mint** -- `_render_identity/mint.py`'s `mint_render_token()`, called directly in-process
   (Python), from a fixture `ExportBundle`-shaped mapping.
2. **V3** -- `auth-validator-edge/index.mjs`'s `handler()` (which runs the REAL
   `evaluateRenderBranch` internally, calling `render_auth.mjs`'s REAL
   `verifyRenderTokenWithSlots` / `hasForbiddenRenderClaims` / `isRenderAdmissibleUri` /
   `applyRenderHeaders`), invoked via `chain_bridge.mjs` with a real CloudFront-shaped event.
3. **V2** -- `portal-authorizer/index.mjs`'s REAL exported `authorizeRenderToken()`, called
   directly (never through `handler()`, which would require a live DynamoDB/SecretsManager
   origin gate this cell's BOUNDS forbid touching at all -- the same choice the CVO's own probe
   makes).
4. **resolve.py** -- the REAL `trusted_only()` / `classify_principal()`, fed the REAL
   CloudFront-multi-value headers V3 produced (never flattened by this cell -- `normalize_headers`
   already documents and handles that exact shape).
5. **enforce.py** -- a REAL `Enforcer` (real `FirmBinding`, real `resolve_now` /
   `_resolve_render_delegate` / `covers` / `cache_key_for`), constructed with fixture loaders
   (`load_directory`/`load_ownership`/`load_policy`/`load_render_bundle`/
   `load_delegator_identity` -- the same injection seams `enforce.py`'s own class docstring
   documents as this round's fixture-shaped dependencies).
6. **served.py** -- the REAL `key_operation()` boundary, called on the PUBLISHED hyphenated
   operation id (`"performance-report"` etc.) to derive the key spelling actually fed into the
   Enforcer's `Request` -- never hand-typed separately, so a wrong conversion would fail the
   test rather than merely look inconsistent.

Three fully independent fixture "worlds" (different registry tenants, different opaque firm
ids, different account ids, different advisors, different bundle/route/operation) --
`49financial`/performance-report, `cottonwood`/analysis-report, `inflection`/narrative-packet
(the three ENABLED CLIENT firms in `data/firm_registry.json`, confirmed via
`_keys.load_firm_ids()`) -- prove the chain is genuinely parameterized, not coincidentally
correct for one hardcoded case: their resolved `permitted_account_set`s are pairwise disjoint
(asserted in the test's summary check).

## Mechanical result

```
SUMMARY: 12 of 12 top-level checks passed; 0 individual FAIL label(s): []
PASS: the full chain test passed -- 3/3 positive fixtures resolved, 6/6 negative
arms refused/UNKNOWN, plus 3 additional item-7 checks.
```
Full verbatim output captured in this cell's proof-of-spec instance (`output_evidence`).
Denominator: 3 of 3 positive fixture objects correctly resolved (non-overlapping); 6 of 6
CELL-mandated negative arms correctly refused/UNKNOWN; 3 additional item-7 checks beyond the
CELL's 6 mandatory negatives, all passing; 33 individual `[PASS]`/`[FAIL]`-labelled assertions
printed, 33 of 33 PASS, 0 FAIL.

## PRD item 7 (a)-(k), except (g) -- explicit arm-by-arm mapping

PRD `org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md:231-241`, item 7's literal list.
(g) excluded per this order's own CTO ruling 4 (deploy-time IAM policy read).

| Arm | PRD text (paraphrased) | Proven by | Result |
|---|---|---|---|
| **(a)** | a minted token reads each of the three routes for its own tenant and ids | `run_positive(WORLD1/2/3)` -- one world per route (performance/analysis/narrative), each with its own tenant, account_set_id/job_id/report_id, mint -> V3 admit -> V2 authorize -> classify RENDER_DELEGATE -> Enforcer admits -> `covers()` true | PASS x3 |
| **(b) pt 1** ("fourth scoped route") | the same token is refused on a fourth scoped route | `negative_5_unlisted_operation()`'s V2 sub-check (`N5c`): a routeKey outside `RENDER_ROUTE_CLAIMS` | PASS (`N5c`) |
| **(b) pt 2** ("swapped path id") | ...on the same route with a swapped path id | `negative_3_swapped_path_id()`: V2 refuses; V3's uri-only admission is unaffected (control) | PASS (`N3`) |
| **(b) pt 3** ("non-print CloudFront path") | ...and on a non-print CloudFront path | `extra_b_non_admissible_uri()`: a valid token on `/unrelated/non-admissible/path` -- V3 refuses | PASS (`Eb`) |
| **(c)** | a token past `exp` is refused | `negative_2_expired()`: minted with `now` 1000s in the past (`mint_render_token`'s own injectable `now=` test seam) -- V3 refuses `TokenExpiredError` branch | PASS (`N2`) |
| **(d)** | a token signed with the render key carrying `tier internal` or `role admin` is refused at V3 | `negative_1_forbidden_claim()`: a real minted token's claims decoded, `role` overridden to `admin`, re-signed with the SAME render private key -- V3 refuses (`hasForbiddenRenderClaims` branch) AND V2 independently refuses the same forged token (belt-and-braces, CELL arm (a)'s "verifies it independently") | PASS (`N1`) |
| **(e)** | a render token presented to V1 (`/auth/...`) is refused | **NOT re-proven here.** V1 is `infra/aws/opalinvest_dev/lambda/auth-handler/index.ts` -- a DIFFERENT Lambda, outside this cell's `<paths>` grant and outside the five real modules THE CELL names to wire (mint/V3/V2/resolve/enforce/served). Per `mint.py`'s own docstring and the PRD's own item 4 text, V1 (with V4-V7) refuses a render token STRUCTURALLY on wrong key + wrong `aud`, with no render-specific code path at all -- proven by V1's own pre-existing unit tests (IB-rtq-1/round-17 lineage), not this cell's chain. |
| **(f)** | a human portal token still behaves exactly as before (negative-widening arm) | `extra_f_human_token_unaffected()`: a human-shaped token (normal `aud`/`iss`, no render claims) is NOT admitted by the render branch, and the render branch's own fall-through reaches the PRE-EXISTING human path's own Secrets Manager call -- observed as this test's own deliberate `NETWORK FORBIDDEN` guard firing in stderr (never a render-specific refusal reason), which is the evidence the render branch did not intercept or mutate anything for a non-render token. Full end-to-end human-path success is outside BOUNDS (offline, no AWS call) and is a sibling cell's own regression suite's job, not re-proven here. | PASS (`Ef`, partial/structural as described) |
| **(g)** | excluded | -- | N/A per ruling |
| **(h)** | the renderer resolves `RENDER_DELEGATE` and reads its three objects | `run_positive(WORLD1/2/3)`: each world's `classify_principal` returns `RENDER_DELEGATE`, `Enforcer.resolve_now` admits with `principal_class == "RENDER_DELEGATE"`, and `covers()` is true for the object requested -- across all three of the item-4/8 operations (performance/analysis/narrative), one per world | PASS x3 |
| **(i)** | revoking the DELEGATOR's entitlement after the mint makes the next render read refuse | `extra_i_post_mint_revocation()`: the SAME token/headers, first `resolve_now` admits, then a second `Enforcer` (same tenant/directory, ownership loader now reports the advisor's grant revoked) refuses on the identical token | PASS (`Ei`) |
| **(j)** | `X-User-Role renderer` WITHOUT the render marker resolves `UNKNOWN` | `negative_6_missing_render_marker()`: real admitted V3 headers, with `x-render-delegator`/`-bundle`/`-revision` stripped before `classify_principal` -- resolves `UNKNOWN`, reason names the missing headers | PASS (`N6`) |
| **(k) pt 1** ("object outside the bundle's pinned scope") | a render delegate asking for an object outside the bundle's pinned scope ... is refused | World1's own positive run, extended: the delegator's OWN grant includes a third account (`C`) that is NOT in the bundle's pinned `account_ids`; `covers(scope, "account", C)` returns `False` even though the delegator genuinely holds `C` | PASS (`W1: account outside the bundle's PINNED scope is NOT covered`) |
| **(k) pt 2** ("operation outside the three") | ...or for any operation outside the three, is refused | `negative_5_unlisted_operation()`'s Enforcer sub-check (`N5a`/`N5b`): `served.key_operation("summary-report")` is confirmed NOT in `RENDER_DELEGATE_OPERATIONS`, and `Enforcer.resolve_now` refuses `OBJECT_NOT_COVERED` for it | PASS (`N5a`, `N5b`) |

Additional CELL-required negative not directly an item-7 letter (IB-rtr-3's own item (c), the
bundle-id verification that item (k)'s "pinned scope" mechanism depends on):
`negative_4_wrong_bundle_id()` -- a real admitted token, but the `load_render_bundle` loader for
this call declares a DIFFERENT `bundle_id` than the claimed `X-Render-Bundle` -- `Enforcer`
refuses `EMPTY_GRANT` with the bundle-mismatch reason, never served against the wrong bundle's
accounts. PASS (`N4`).

## Judgment note for the CVO's L9 read

This script proves the MECHANICAL bar: every arm above maps to a specific, named test function
and assertion label, and the summary line's `12 of 12` / `0 FAIL` is the printed denominator.
Whether this coverage genuinely satisfies "the full item-7 table" -- in particular whether arm
(e)'s out-of-`<paths>` treatment and arm (f)'s partial/structural proof are acceptable substitutes
for a fuller end-to-end demonstration -- is the CVO's own read, not this worker's say-so.

No edit was made to any of the five real modules' own logic, and none of the six mandatory
negative arms (nor the three extra checks) found a NEW defect in the real modules under test --
every refusal observed is the modules' own EXISTING, documented refusal behavior, exercised
through the real call chain rather than asserted about it.
