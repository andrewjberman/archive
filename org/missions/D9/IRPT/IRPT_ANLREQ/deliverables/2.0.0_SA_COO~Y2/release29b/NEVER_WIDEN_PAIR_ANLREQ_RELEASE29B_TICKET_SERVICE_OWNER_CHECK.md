# IRPT_ANLREQ release 29b -- the ticket service's owner check on the attachment's input_id (row W101-S3) and the one read grant it needs, ONE window, ONE package, TWO sequential applies (grant, then code) -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No apply order exists and none is cut on this file until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-14. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
It follows release 29 (CTO half signed on blob `5e8b3cbd95`; legs L2, L4, L3 applied and read live) and carries only what the CTO's rulings 7620 (the owner check at SUBMIT-FORM) and 7633 (the grant shape: `dynamodb:GetItem` only, on `irpt-requests` only, `LeadingKeys` the three firms, the owner attributes only) ask for. Cells: `AR-y-316` (the check, merged `49f70cd078`, with its AMENDMENT 1: CLIENT-class callers only), `AR-y-320` (the build, merged `ab3042aedc`; record `deliverables/0.9.0_WK_IRPT_ANLREQ~130/r40/OPAL_TICKET_API_BUILD.json`).

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened, with its check re-run (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read. A statement with none of these words is a plan.

## 1. What moves

One served package and one IAM statement, applied as two sequential Terraform applies in the root `infra/aws/terraform/ticket-center`:

| step | what | applier |
|---|---|---|
| G | the policy `opal_ticket_api_ddb` (`aws_iam_role_policy`) gains ONE statement `IrptRequestsInputOwnerRead`; a NEW data source `data.aws_dynamodb_table.irpt_requests` (a plan-time read, no managed resource) | `0.7.0_AE_CloudOps~AQ2` |
| C | the Lambda `opal-ticket-api`: code (`lambda_function.py`, the only member) and ONE environment variable `IRPT_REQUESTS_TABLE` | `~AQ2` |

Writers of the moved member into a served package: `lambda_function.py` of `ticket_center` is carried by the Lambda only (**N = 1**; RECORD, the build record). **Not in this release:** the intake release (`AR-y-318`, `AR-y-319`: its own pair), the portal candidate (`AR-y-317`, an approval row for Andrew), the Shares price source.

## 2. Start state (RECORD / MEASURED; the applier re-reads it at step 0, and any difference ABORTS)

- **Lambda `opal-ticket-api`:** CodeSha256 `C/Rt/FnSqOj7SnZC1GeoEilj8jbCKdvAUHnxYrnNZNM=`, 34057 bytes, one member `lambda_function.py` sha256 `cfa99176f89f7cdb32c3e171bdfdf930a605ee51fd3e590b1a55e878073d4d70`; S3 `ticket-center/opal-ticket-api.zip` latest VersionId `7vn6xyMOZjpSaKwiT73UaNfXj6mNSljr` of 22 (MEASURED by this seat 2026-10-14 ~14:38Z: CodeSha256 and size; MEASURED by `AR-y-320` from AWS: the version list, whole JSON). Release 28's own upload is that latest version.
- **The role policy:** `opal_ticket_api_ddb` holds the tickets-table statement, `UsersDirectoryReadForClaimEnrichment` and `UsersDirectoryEmailIndexQueryForClaimEnrichment` (Terraform source, `main.tf` lines 113-178). **The live policy was NOT read by this seat or by `AR-y-320`:** step R0g reads it.
- **The Terraform state:** NOT read (no plan was run by any seat).
- **The artifact data source is NOT pinned to a version** (RECORD, `terraform_note`): the plan resolves the key's LATEST version, so the apply follows its own upload with no other write to the key.

## 3. Artifact, pins, rollback (MEASURED by this seat: the zip re-hashed; the checker and proof re-run)

- **Zip:** `opal-ticket-api-r29b.zip`, staged on the dell2 box under `C:/dev/irpt-release-r29b/` (outside the repository), sha256 `160f0c75fbc2bdc07c6adf4af8187e2299ae35e97c4cd59768ab61d16da9bf80`, 35325 bytes; expected CodeSha256 `Fg8MdfvCvcB8at9K+Bh+IpmuNel8TNWXaKth0W2pv4A=`. Built from trunk `ebbadcb0e1c7ba6693229ffe6b29b5b62bbd3333` (it contains `49f70cd078`) with `TMPDIR=<private> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh ticket-center opal-ticket-api`, twice, byte-identical, guard count 8 each time. Against the live package exactly `lambda_function.py` differs (blob `1e93b765`, sha256 `d112ba42...`), nothing only in live, nothing only in the release (RECORD; `Y320-BUILD-OK`, proof VALID, re-run by this seat).
- **The no-move control** reproduces the live package at `4279513f95` (the release-28 input), byte-identical, `differs_from_live []`. **The order's first base `97d2d4bede` did NOT reproduce it** (it builds the previous package): row `W130-S1`, the issuer's error; this file names `4279513f95`.
- **Tests on the release tree:** `infra/aws/lambda/ticket_center/tests/` 300 passed, 0 failed (plus 42 subtests); `test_submit_input_owner.py` 21 passed (RECORD).
- **Rollback of the code:** S3 VersionId `7vn6xyMOZjpSaKwiT73UaNfXj6mNSljr` (sha256 `0bf46dfc...`, 34057 bytes) copied onto the key as a new latest version, then the Lambda-target plan and `safe-apply`, CodeSha256 read back `C/Rt/FnSq...`. **Rollback of the grant:** `terraform` removal of the statement by the same root (the statement is additive; removing it with the code rolled back changes nothing else). Roll the CODE back before the GRANT.
- **The Terraform plan, in order** (RECORD, `terraform_note` of the build record): **(G)** `-target=aws_iam_role_policy.opal_ticket_api_ddb`: one in-place update, the new statement only; read the statement back with `get-role-policy`. **(C)** upload the zip with the builder script WITHOUT `BUILD_ONLY` (one new object version; read it back, sha256 equal), then `-target=module.opal_ticket_api.aws_lambda_function.this`: `Plan: 0 to add, 1 to change, 0 to destroy`, attributes `environment` (the one added variable), `last_modified`, `s3_object_version`, `source_code_hash` ONLY. **One combined plan does NOT order the two** (no `depends_on`; the Lambda references the role, not the policy).

## 4. Blast radius -- what a person or a system meets

**4a. THE ONE WIDENING (the grant, step G; CTO 7633):** the role `opal-ticket-api-role` may now call `dynamodb:GetItem` on the table `irpt-requests`, ONLY for partition keys (`tenant`) in `49financial`, `inflection`, `cottonwood` (`dynamodb:LeadingKeys`), and (by condition) for the attributes `tenant`, `request_revision`, `identity`, `owner` (`dynamodb:Attributes`, `ForAllValues:StringEquals`, with `dynamodb:Select` = `SPECIFIC_ATTRIBUTES` `IfExists`). **Who gains:** the ticket Lambda (a service role), not a person; no person gains any ability. **What it can read:** the retained-input row `INPUT#<id>` (and any other row of those three tenants, by key) projected to those four attributes; the `owner` attribute holds `firm_id`, `principal_id` (an email), `principal_class`, `advisor_id`. **Limits named:** (i) for a `GetItem` with NO projection the `ForAllValues` test on `dynamodb:Attributes` is vacuously true, so what holds the read to the owner attributes is the CODE's `ProjectionExpression` (`INPUT_OWNER_ATTRS`, graded by the worker's `iam_shape_check.py`), not IAM alone (INFERRED from the IAM evaluation rules; **not verified against the simulator**); (ii) `dynamodb:Select` is not populated for a `GetItem`, so that condition is inert; (iii) a new firm is a grant edit.
**4b. Behaviour changes (code, step C; RECORD, `AR-y-316` and its AMENDMENT 1):** a CLIENT-class caller's `analysis_request` SUBMIT is refused with HTTP 400 and the one text `attachment.input_id is not available to the caller` unless the retained input is the caller's own: the row is read keyed on the caller's VERIFIED firm; it must exist, its `tenant` and `identity` must equal the firm and the input id, its `owner.firm_id` the firm, and its `owner.principal_id` the caller's email (lowercased; the portal authorizer's email is the JWT subject, the door's `principal_id` the same subject: read from source, not measured with a live token). A read that raises answers HTTP 503 (fail closed). **An INTERNAL human's submit is NOT checked** (the reader is not called): as today. CREATE, LIST, REPORT, PACKAGE and the draft routes are unchanged. **Before:** any client login could file a ticket naming another firm's input (row `W101-S3`, release-28 pair line 56). **After:** it cannot.
**4c. Mixed state (the failure the order prevents):** the code without the grant refuses EVERY client filing with a 503 (nothing reaches the ticket table); hence **G before C**, and **if G fails or reads wrong, C does not open**.

## 5. Order of the window and the after-reads

Each read carries its claim word; a missing read is `ABSENT`, and ABSENT is not EXERCISED.

**Step 0 (the applier, within the hour before the first act):** R0a: this file and BOTH halves signed at the same blob; one NEVER-2 ledger (`irpt-ticket-r29b-<date>`; legs G grant, U upload, C code, V after-reads); no open deploy entry in any live worktree names `opal-ticket-api`, the ticket role or `ticket-center` (every worktree read, the denominator printed). R0b: the Lambda CodeSha256 and the key's latest VersionId equal section 2; **a newer version means someone released: ABORT and cut a rebuild cell.** R0g: read the live inline policy `opal-tickets-table-rw` of the role (`get-role-policy`) and the attached policies; print the existing statements by `Sid`; anything beyond section 2's list is a STOP. R0h: read the credential-less refusal envelope of the Lambda (status and body sha256) BEFORE any change.
**Step G:** the scoped plan on the policy target: exactly one in-place update, adding the one statement (read the plan's diff: the `Action`, the `Resource`, the three firms and the four attributes must equal section 4a; ANY other change is a STOP, nothing applied); `safe-apply`; read the policy back: the statement present exactly once, equal to section 4a.
**Step U + C:** build in a detached worktree at `ebbadcb0e1c7ba6693229ffe6b29b5b62bbd3333` (`git -c core.longpaths=true`), private TMPDIR, guard count printed, `BUILD_ONLY=1` first: the printed CodeSha256 must equal `Fg8MdfvCvcB8at9K+Bh+IpmuNel8TNWXaKth0W2pv4A=` (any other: ABORT before any upload); then the same build WITHOUT `BUILD_ONLY` (one new object version), read back (sha256 equals `160f0c75...`); the Lambda-target plan (the attributes of section 3 only); `safe-apply`.
**After-reads (V):** T1 CodeSha256 reads `Fg8MdfvC...`; T2 the zip has one member `lambda_function.py` with sha256 `d112ba42...`; T3 the credential-less refusal envelope equals the one read at R0h; T4 the environment equals the previous plus `IRPT_REQUESTS_TABLE=irpt-requests` (read both, compare); T5 the role's effective policy: the simulator for `dynamodb:GetItem` on the `irpt-requests` table ARN allowed, and on a table outside the statement (for example `opal-users-v2` `PutItem`) unchanged from before (print the conditions the simulator could not evaluate).
**The sitting (V6), SYNTHETIC callers only, REFUSAL arms only (they write no ticket and send no mail):** with minted synthetic users as in release 29's sitting (rows deleted after `exp`, GSI and ConsistentRead ABSENT): **K1** a minted advisor B of `49financial` files an `analysis_request` whose attachment names advisor A's retained input (the release-29 sitting's D1 input, which stays until the delete call is done): expect HTTP 400 `attachment.input_id is not available to the caller`. **K2** a minted advisor C of `cottonwood` names the same input: expect the same 400. **K3** the same call as K1 with a syntactically valid input id that exists nowhere: expect the SAME 400 text (one text for not-found, other-firm and other-owner). **Reading the arms:** a 503 on K1 or K2 means the grant is missing or wrong (the read was denied): STOP and roll the CODE back. A 400 on K1 PROVES the read succeeded and returned a row whose owner is not B. **The positive arm (the owner files its own input, 201) is NOT run here:** it writes a ticket and sends mail, so it is the FWD-1 run's one filing (the CTO's round-40 step 4). Until it runs, the 201 path is covered by 21 unit tests and not by a live call.

## 6. Both branches (the expected outcome is stated for each; a mixed state is the failure the order prevents)

| state | safe? | evidence |
|---|---|---|
| G applied, C not | **SAFE** | the statement is unused until the code reads the table (INFERRED); rollback is removing it |
| C applied, G not (or G read wrong) | **UNSAFE: every client analysis filing answers 503** | RECORD, `_check_input_owner` fails closed; hence G first |
| both applied, K1/K2 answer 400 | the intended state | section 5 V6 |
| both applied, K1 answers 201 | **the check is not firing:** BLOCKING; roll the code back | INFERRED |
| rollback | CODE first, then the GRANT | section 3 |

**If R0b or R0g fails:** the window does not open. **If an after-read fails:** the code rolls back to VersionId `7vn6xyMOZjpSaKwiT73UaNfXj6mNSljr` before anything else moves; the grant may stay (additive).

## 7. Limits named

- The staged zip is on the dell2 box only; the applier runs there (INFERRED from the lane name).
- The live role policy, the Terraform state and the `irpt-requests` rows were not read by this seat (R0g, the plan and the sitting read them).
- The caller-to-owner mapping (the email equals the door's `principal_id`) was read from source, not measured with a live token; K1 and the FWD-1 run's own filing measure it.
- The IAM condition semantics (limits (i) and (ii) in 4a) are not verified against the simulator with a condition context.
- The release builds from a trunk commit (`ebbadcb0e1`) that also carries unrelated trunk changes (the CI builder and map); only the packaged member was compared with the live package.
- Row `W130-S1` (the first control base) and the first-write rows of the cells are dispositioned in the round-40 compile.

## 8. Owed before any apply order is cut

1. The CTO half on this file's blob, covering both branches of section 6, including: **(a)** that G is the only widening and 4a names all of it, with limits (i) and (ii); **(b)** the V6 arms, and that the positive arm belongs to the FWD-1 run; **(c)** the synthetic callers B and C (minted users of `49financial` and `cottonwood`, one sitting).
2. The applier order(s) to `0.7.0_AE_CloudOps~AQ2` (G, U+C, V and V6), each carrying a `# pipeline-override:` line, cut by this seat only after (1).
3. The NEVER-2 ledger opened at the start of the window.
