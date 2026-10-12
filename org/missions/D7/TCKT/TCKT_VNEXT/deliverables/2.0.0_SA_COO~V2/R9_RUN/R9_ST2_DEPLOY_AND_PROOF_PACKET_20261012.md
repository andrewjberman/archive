# Packet -- R9-st-2 deploy and R9-st-3 proof: an internal caller's users row must be status `active` (TCKT_VNEXT round 9)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-12 ~01:4xZ. **Applier:**
`0.7.0_AE_CloudOps~TV2`.

**Authority:** PRD `prd/TCKT_VNEXT_PRD.md` v0.4 ADDENDUM 4 @fc2100e1e2 (C-FENCE), ratified-text half signed by `3.0.0_SA_CVO`
@1fc5ceaef5; the CTO's msgs 6236 and 6240 (two conditions on this pair, met in sections 3 and 4). Decomposition
`decompositions/TCKT_VNEXT_DECOMP_R9.md`: `R9-st-1` (built, merged @873130546e), `R9-ct-1` (the count, @e7bb608065), `R9-st-2`
(this apply) and `R9-st-3` (the proof, five direct invocations, in this same pair).

**COO half: SIGNED below.** Code only: no env, no route, no IAM, no grant. **THIS APPLY NARROWS WHO IS SERVED.**

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `873130546e`; file sha256 `4136587ae35a4c3f5c951f3e8dec4662f94f12a6075b92cd4a5f54ed0bef7cf9` (`git show HEAD:<file> \| sha256sum`, this seat) |
| the diff from the live build's file | 5 added / 1 removed, all inside `_profile_scope`: two docstring lines, and three lines after the row is fetched and before the firm list is read. Every hunk read by this seat |
| tests on the merged tree | `ST-ACTIVE-OK passed=5 of 5`; `ST-REGRESS-OK passed=206 failed=0`; `commit-gate.sh` clean (this seat, 01:2xZ) |
| live now | `opal-ticket-api` CodeSha256 `lAt/vc4X...`, LastModified 2026-10-12T00:22:08Z, Successful (this seat, `get-function-configuration`, 01:3xZ); deployed handler `f99a314b...` by the applier's download at 00:2xZ, NOT re-downloaded since |
| plan expected | `0 to add, 1 to change, 0 to destroy` (the function's source_code_hash only) |

## 2. What moves

Every route that resolves a scope, for ONE class of caller: INTERNAL (firm `opal-capital`, not a service subject) whose ONE PROFILE
row does not carry `status` exactly the string `active`. Before: served, with whatever firm list the row holds. After: 403
`{"error": "firm scope lookup failed"}`, the failed-lookup answer, and one log line
`FIRM-SCOPE-NOT-ACTIVE: <table> PROFILE row for an internal caller is not active; refusing`, which carries neither an address
nor the status value.

**Not moved, each held by a test:** an `active` row with no firm list (every firm), an empty list (every firm), a list, a
malformed value (refused); no row (refused); more than one row (refused); a lookup error (refused); clients and service subjects
(they never reach the lookup). **It widens nothing.**

## 3. The same test in two functions (the CTO's condition 1)

Printed by the applier from `infra/aws/opalinvest_dev/lambda/auth-handler/src/auth.ts` at HEAD (blob `0dbd69957da0dc8c`), into
`org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r9_ct1/ACTIVE_INTERNAL_ROWS_BY_DOMAIN_20261012.json` @e7bb608065, and read
there by this seat:

| where | the comparison as printed | what a refusal does |
|---|---|---|
| sign-in, `auth.ts:106` (after the credential check) | `if (user.status !== 'active') {` | `throw new Error('Account disabled');` |
| sign-in, `auth.ts:255` (at code redemption) | `if (user.status !== 'active') {` | the same |
| refresh, `auth.ts:538` | `if (user.status !== 'active') {` | the same |
| the ticket service, `lambda_function.py:384` at `873130546e` (printed by this seat from the merge's diff) | `if got.get("status") != "active":` | `return None, _resp(403, {"error": "firm scope lookup failed"})` |

Both admit exactly the string `active` and refuse every other value and an absent one; neither lower-cases or strips. The
worker's mutant that lower-cased and stripped the value failed a test (`Active` was admitted), so the exactness is held by a
test and not only by reading. The deployed sign-in is tied to that source by the applier's three reads (live hash equals the
source map's artifact hash; no `src` change since the recorded commit; the guards present at it). **One difference, stated:** the
two functions read the row by different keys. Sign-in reads the user it has just authenticated; the ticket service finds the row
by the caller's lower-cased address through the email index. A row whose stored address differs in case from its lower-cased
form would be found by one and not the other; round 7 counted 0 such rows among the internal ones.

## 4. Who is refused after it, and the count the CTO asked for (condition 2)

**The closed status set** (round 8, the applier, 56 PROFILE rows read whole): `active` 54, `disabled` 2, absent 0, no other value.
Internal rows: 23 = 21 active + 2 disabled. **The release refuses exactly the two disabled rows.** Both are refused at sign-in
today. Digest `e95c05c7ae90`: non-human tooling. Digest `04fc361f3802`: reads as a person at an external company's domain; no
event on any ticket; row last updated 2026-07-14.

**The count** (`r9_ct1`, @e7bb608065, a re-scan of 86 items, 56 PROFILE, with the firm list projected; its check re-run by this
seat, `CT-COUNT-OK active_internal=21 opal=20 non_opal=1`): of 21 ACTIVE rows carrying the internal firm id, 19 are on
`opalinvest.com`, 1 on a reserved test domain (counted on the Opal side: a reserved domain cannot be an outside party), and
**ONE is on a domain that is not Opal's**: digest `1af514167abb`, domain `thewhitelabelcreative.com`, `userType` null, NO firm
list, row last updated 2026-10-01, no event on any ticket. It reads as a person. **It is active, so it can sign in, and it is an
INTERNAL caller reading every firm, to this service and to every service that classes by firm id. This release does not move
it: admitted before, admitted after.** **NOT MOVED, by the CTO's ruling (msg 6259, answering this seat's msg 6258): "put the pair. The status release does not
move that row and does not wait on it." It is row TCKT_VNEXT-D2-S53 (ARMED, owner the CTO). No seat on dell2 changes,
disables or probes that row, and NO context is constructed for its address: no arm of this pair uses it.** It is not round 8's disabled row, whose domain is spelled without the leading article.

## 5. Branches and rollback

Every status below is read from a PARSED value: the invoke's response payload loaded as JSON and its integer `statusCode` taken,
never a string compared against captured shell output (round 7's near miss).

| branch | what is written | rollback |
|---|---|---|
| apply succeeds; S3 and S5 refused, S4 served | the function code | none |
| apply succeeds; **S4 (an ACTIVE row) is refused** | the function code | **ROLL BACK AT ONCE**, on the applier's own parsed reading: re-apply the build of `09488abbb1` (handler `f99a314b...`), same method. That reading means active staff are locked out. The rollback re-admits the disabled rows by direct invoke, as today |
| apply succeeds; S3 is SERVED | the function code | none taken; STOP and report: the release did not do what it says, and nothing is worse than before |
| apply succeeds; S5 is SERVED | the function code | **ROLL BACK AT ONCE**: the no-row refusal of round 7 has been lost, which is worse than before |
| apply fails partway | nothing else to land (code only) | re-apply `09488abbb1`; the ledger stays open until one holds |
| step 1 finds the live handler is NOT `f99a314b...` | nothing: STOP before any plan | none |
| S1 (before) is NOT served, or S2 (before) is NOT refused | nothing: STOP before any plan. The "before" state is not what this pair says | none |
| the plan shows anything but 1 to change, any route or any env diff | nothing: STOP | none |

## 6. The act, its five invocations and its after-reads

Row TCKT_VNEXT-D2-S46 (ARMED, owner the CTO) is the instrument and is cited here: a direct invoke goes around the authorizer.
Five invocations, all `GET`, each with a constructed context; no token is made; no identity is minted; no grant is added; **no
users row is written, changed or deleted** (the disabled row is used as it stands).

0. Open the NEVER-2 ledger entry FIRST; every live worktree's `.open_deploys/` unioned with its denominator; an open entry
   naming `opal-ticket-api` other than this one is a STOP.
1. Before: the live package downloaded, the deployed handler `f99a314b...`; env key names and count (9) with a hash of each
   value; the ticket route census (11); `opal-tickets` ItemCount; the control ticket `TCK-20261011-e6433610`'s status and events
   length; and the two rows the arms use, re-read: digest `e95c05c7ae90` still one PROFILE row, status `disabled`; digest
   `3e5db3675c91` still one PROFILE row, status `active`, no firm list. **If either row no longer reads so: STOP.**
2. **S1, BEFORE:** a constructed INTERNAL caller with the address of the DISABLED tooling row (digest `e95c05c7ae90`), `GET` the
   control ticket. Expected **200**.
3. **S2, BEFORE:** a constructed INTERNAL caller with a made-up address that has no row (round 7's N1 caller shape), the same
   `GET`. Expected **403** (round 7's release).
4. Build and upload; the zip's handler hashes `4136587a...`. Plan, then `safe-apply`: exactly 1 to change.
5. After: CodeSha256 equals the zip; the deployed handler is `4136587a...`; env unchanged (9 and 9); routes unchanged (11).
6. **S3, AFTER:** the S1 caller, the same `GET`. Expected **403**, body `{"error": "firm scope lookup failed"}`.
7. **S4, AFTER, the twin:** a constructed INTERNAL caller with the address of digest `3e5db3675c91`: a NON-HUMAN verification
   identity on `opalinvest.com`, one PROFILE row, status `active`, no firm list (the applier's first choice; the alternate
   `686bd73cd5e9` is a service-prefixed subject and is not used). No person's address is constructed. The same `GET`. Expected
   **200**.
8. **S5, AFTER:** the S2 caller, the same `GET`. Expected **403**, the same body.
9. The log group, the minutes of steps 6 to 8, with a QUOTED filter pattern and a positive control that matches first (row
   D2-S51): `FIRM-SCOPE-NOT-ACTIVE` lines, expected 1; `FIRM-SCOPE-NO-ROW` lines, expected 1; none containing an at-sign.
10. ItemCount unchanged; the control ticket unchanged; the two rows of step 1 unchanged. The replan is 0-diff.
11. `RESULT.json` holds, per arm, the parsed function status, the refusal body's field names and `error` for a refusal, and for a
    served arm the KEY NAMES and `status` only. **A served answer's body is never persisted. No address in any tracked file.**

## 7. What this pair does not show

- That a real signed-in staff member is served after the release (the organic case; S4 is its constructed arm).
- The fence between two internal callers with rows and different firm lists. Tests only.
- Anything about the one active external-domain row (section 4): it is not moved and not exercised.
- Row D2-S46 is narrowed and not closed: a direct invoke can still present any ACTIVE internal address.

## 8. COO half

SIGNED, `2.0.0_SA_COO~V2`, 2026-10-12 ~01:4xZ, for exactly: the code of `873130546e` (handler `4136587a...`) applied to
`opal-ticket-api` by `safe-apply` with a plan of 1 to change; five direct `GET` invocations S1 to S5 as section 6 names them;
the reads of steps 1, 5, 9 and 10; the rollbacks of section 5. Blast radius: the one function's code. Writers of that property:
ONE (the ticket-center Terraform root, applied by `0.7.0_AE_CloudOps~TV2` under this project's orders; N = 1). Both branches of
every expected outcome are in section 5. Nothing here reaches the vendor path, the users table's rows, or any other service.
Put on the CTO's answer to the non-zero count (msg 6259: "put the pair, with the row stated as not moved").
