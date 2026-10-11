# IRPT_ANLREQ release 6 -- the READY gate on the commentary composition read: the GRANT first, then the function -- never-widen pair, COO half

COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-11. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Shape ruled by `1.0.0_SA_CTO~DELL2` msg 5208 on armed row `IRPT_ANLREQ-D2-S53`: no hand pin; ONE pair; the IAM grant first; then the
function from the trunk; a census naming the live blob read from the downloaded package and correcting the map; two after-reads.
This half signs the act's blast radius and both branches. NOT APPLIED; no apply order exists until both halves are signed.

Claim words: MEASURED = this seat ran or read it; WORKER = worker `0.9.0_WK_IRPT_ANLREQ~53`'s read, with its own claim word.

## 1. What is released, and why in this order

- **Code:** `irpt-commentary-composition-read-lambda` from the trunk. Its one behaviour change is the READY gate (cell `AR-y-81`,
  commit `d6824da73a`): before any artifact is read, the request's job row is read; unless it reads READY the answer is the refusal
  `UNAVAILABLE`, the code a missing or other-tenant request already gets.
- **Grant:** the function's role reads the jobs table: `dynamodb:GetItem` on it under the unchanged `LeadingKeys` condition, and the
  `kms:Decrypt` table-name context naming both tables (cell `AR-y-91`, commit `4b9f44a664`; Terraform TEXT, merged @eba5acba8f).
- **Why the grant is FIRST:** with the code and without the grant, the job read is denied and EVERY composition read refuses,
  READY requests included (INFERRED from the code and the policy). With the grant and without the code, nothing uses it: inert.
  So the only safe intermediate state is "grant applied, old code". The applier does not start step 2 until step 1 is READ as applied.

## 2. Artifact, live, rollback

- **Build** (MEASURED: this seat's own BUILD_ONLY on the worker's branch; WORKER built it twice identical):
  `DbvBUxTGlCsdG4htVOhbI4NBxBMNbmjD6BLpMGu2Yo4=`, 16 members. It builds ONLY with `BAU_PARITY_SKIP=1` (row `IRPT_ANLREQ-D2-S34`,
  a known defect of this function's entry; the skip turns the whole parity check off, and this pair says so instead of hiding it).
  The applier builds at a commit on origin that contains `eba5acba8f`; a digest other than `DbvBUxTG...` is an ABORT.
- **Live / ROLLBACK:** `ZZmWOFSA/GjO0d/cKHSm9G5+xDc5sNfEHOpbmfIabQ0=`, LastModified 2026-10-09T13:18:10Z (MEASURED by this seat
  ~15:1xZ; WORKER's download hashed to the same digest). The applier records the S3 object version it replaces at step 0; rollback
  is that version copied back onto the key and a targeted apply, as release 5's rollback was done.
- **Census:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/r9/COMPOSITION_READ_RELEASE_CENSUS.json`
  (blob f5167ebd9f). WORKER, from the downloaded live package: 16 members; the live `commentary_composition.py` is byte-equal to the
  blob at commit `20534db618` (the only one of 2 commits that matches); the 12 pinned members equal their pins.
- **Writers, counted (MEASURED: a native search of every `.tf` under `infra/aws/terraform` for the function's name, its Terraform
  names and its locals: 17 lines in 2 files).** The function's CODE: N = 1, `module "irpt_commentary_composition_read"`,
  `investor-reporting/export/commentary_composition.tf:88`. The role's INLINE POLICY: N = 1, `aws_iam_role_policy.commentary_composition_read`,
  the same file `:55`. The other two resources the search finds do not write this role: `aws_iam_policy.commentary_composition_invoke`
  (`:119`) is the INVOKE permission handed to the drafter, attached to the drafter's role in `transcripts/commentary.tf:250`.
  NOT read: whether the module at `:88` itself attaches a managed policy to the role (its source was not opened); the applier's
  step-0 `get-role-policy` and a `list-attached-role-policies` on that ONE role settle it.

## 3. Blast radius

**The function: 3 of 16 members differ from live** (WORKER; 0 added, 0 removed):

| member | owning commits | served effect | claim | why |
|---|---|---|---|---|
| `commentary_composition.py` | d6824da73a | CHANGES ANSWER | inferred (the gate's five tests pass; nothing was exercised live) | refuses `UNAVAILABLE` unless the job reads READY |
| `repository.py` | 589aee38f0, 3fc99be70f | INERT | inferred | the svc-commentary read path resolves the same reader entry; the additions are write-side or for another subject |
| `retention.py` | 3fc99be70f | INERT | inferred | only the write limb changed, which this function never calls |

All three readings are INFERRED. The two INERT members are not this round's change: they have sat on the trunk, unpinned, since their
commits, and ride this release because the entry builds them from the tree. An INERT member that changes an answer is a failed
after-read (A1) and takes the rollback.

**The grant:** one role, two statements widened by one table each; no new action, no new principal, the `LeadingKeys` condition
unchanged. WORKER confirmed from files: the jobs table's partition key is `tenant` (`core/dynamodb.tf:63`), so the condition fits; it
uses the same KMS key (`core/dynamodb.tf:78`, `core/outputs.tf:10`); `tables.jobs` is exported (`core/outputs.tf:37`).
`terraform fmt -check` was NOT run (no terraform on the worker's path): the applier's plan is the first parse of this text.

**Who calls this function: N = 1** (WORKER's census of round 8): the commentary drafter `outlook-global-commentary-draft-lambda`
(`data/transcripts/scripts/commentary/lambda_handler.py:83`). No portal reader and no other service reads its answer. The drafter
already records a refused composition read as `failed` at stage `composition` (no model call, no draft, nothing sent): MEASURED by
the round-8 test that drives the drafter's handler.
**Who is affected today:** nothing on a product path. No event source feeds the drafter (0 mappings and 0 subscriptions on its queue
at 06:09Z today, the applier's read; not re-measured). After this release a hand-built invoke for a request whose job is not READY
gets no draft.

**Shared Terraform root.** The grant's text is on the trunk. Any seat's plan of `investor-reporting/export` will show this role
policy change until it is applied. That is expected and INERT; it must not be applied as a rider on another seat's act without this
pair's step-1 read being recorded.

## 4. Steps and after-reads (the applier's, in order)

| # | act or read | expect |
|---|---|---|
| 0 | read live `CodeSha256`; the S3 object version now serving; the role policy as live (`get-role-policy`) | `ZZmWOFSA...`; version recorded; S1 and S2 name the requests table only |
| 1 | ledger opened and committed; plan `investor-reporting/export`, targeted at the role policy: ONE resource to change, 0 add, 0 destroy; `safe-apply` | - |
| G1 | `get-role-policy` again | S1 lists both tables under the same condition; S2's context lists both. NOT a simulate: the box's identity is denied `SimulatePrincipalPolicy` on roles; the grant is PROVEN by A1 below, not by this read |
| G2 | one composition read of a READY request on the OLD code (the before arm of A1), by a direct invoke with the closed request shape | answers as before the grant: the grant alone changed nothing |
| 2 | build at the pinned commit (`BUILD_ONLY` first: digest `DbvBUxTG...`), upload, plan targeted at the function: ONE resource, `safe-apply` | live `CodeSha256` = `DbvBUxTG...`; re-plan 0 |
| A1 | the same composition read of that READY request | the SAME answer as G2, byte for byte but for nothing: the gate passes a READY job and the two INERT members changed nothing |
| A2 | a composition read of a request whose job does not read READY (`REQ-4b5155ac2ea9467ab771b414`, job RECEIVED, by the laptop's record of today) | the refusal `UNAVAILABLE` |
| A3 | a composition read of a well-formed request id that does not exist | `UNAVAILABLE`, as before |
| 3 | the source map entry corrected to the release (the census's `map_corrections_needed`: the digest, `last_deployed_commit`, `last_deployed_at`, the stale `_build_note`); ledger closed | - |

A1 and A2 are direct invokes of the composition-read function itself (the drafter is not invoked; no model is called; no draft is
written; no message is sent). Whether this box's identity may invoke that function is NOT known to this seat: the applier reads it at
step 0 and, if it may not, STOPS before step 1 and says so. A READY request readable by the composition read must exist for G2 and A1:
if none can be found, the release does not start (an apply whose only passing after-read is a refusal proves nothing about READY).

## 5. Both branches

- **G1 shows the grant; G2 unchanged; live reads the build; A1 equals G2; A2 and A3 refuse `UNAVAILABLE`:** record, correct the map,
  close the ledger. Row `IRPT_ANLREQ-D2-S53` disarms on A1 and A2 read. Workstream G is told the gate is live.
- **A1 refuses (the grant is not effective, or an INERT member was not inert), or A1 differs from G2:** ROLL BACK the function at once
  to the step-0 version; re-read the digest and G2's read; the grant STAYS (it is inert and the next attempt needs it); close the
  ledger ROLLED_BACK; file a row with the refusal text.
- **A2 answers instead of refusing:** the gate is not doing its work; roll back the function the same way and file a row.
- **Step 1 fails or its plan shows more than the one policy:** STOP; nothing was changed on the function; report.
- **Half-landed between steps 1 and 2** is the designed safe state (grant applied, old code): it may stand, recorded in the ledger,
  if step 2 cannot proceed.

## 6. Owed before any apply order is cut

1. The count of writers: DONE, section 2.
2. The CTO half on this file's blob.
3. `eba5acba8f` (or a descendant) on origin.
