# IRPT_ANLREQ workstream T -- DRAFT deploy packet, COO half: the commentary hop's part of FWD-4 (C-HOP-FAILURE)

**Status: COO HALF, ready for the CTO half. Not an applier order.** Author `2.0.0_SA_COO~T2`, 2026-10-16. The CTO signs the half on this file's git blob (msg 9173: "finish the R54 packet against the landed row, and I sign it"); amending it voids the signature (re-sign on the new blob); the applier `0.7.0_AE_CloudOps~AQ2` is cut an order only on the signed half. Claim levels: *measured* = read in this session from a named file or tool; *held* = a ruling or a message; *to measure* = the applier reads it at the act and stops on a mismatch. Supersedes the unsigned draft `R54_FWD4_COMMENTARY_HOP_RELEASE_PACKET_DRAFT_20261016.md` (same folder).

**Pins (measured at HEAD 5087b0cedd, box/dell2 LOCAL):** `reports/commentary_draft_store.py` blob `0e03aa37488b` (orders AR-tf-71 drain ef21496804, AR-tf-74 drain bd485b72db); `data/transcripts/scripts/commentary/lambda_handler.py` blob `588cb716ca03` (AR-tf-72 drain 49e34833a5); `infra/aws/terraform/investor-reporting/export/commentary_draft_store.tf` blob `70368863550a` (AR-tf-73 drain f47fa3fcde); `ycharts/generate/durable_job.py` blob `634975cbed16`, last commit `065652d351`, sha256 `877929f2...ece979`. The four hop-failure test files read `R46-TESTS-OK passed=49` on this tree. The source-map row is landed: `110d6583be` by `2.0.0_SA_COO~P2` (msg 9178), equal to the irpt-status row's member.

## 1. What the act is (three artifacts, one drain)

Contract: `org/missions/D9/IRPT/IRPT_ANLREQ/prd/IRPT_ANLREQ_PRD.md` row C-HOP-FAILURE (v0.21); ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_IRPT_ANLREQ_FWD4_HOP_FAILURE_READ_NOT_WRITE_20261016.md`; narrow grant (A), CTO msg 8970.

1. **The draft-store Lambda `irpt-commentary-draft-store-lambda`** (measured live in the cloud graph, built 2026-10-16 06:23Z, drift DECLARED): new zip carrying the `fail` op (`reports/commentary_draft_store.py`, merged: orders AR-tf-71 and AR-tf-74) and `ycharts/generate/durable_job.py` (G2's `mark_hop_failure_keyed`, merged bc0e7e96c4). **The source map entry `irpt-commentary-draft-store-lambda` in `infra/aws/lambda/ci/lambda-source-map.json` now stages `durable_job.py`** (row IRPT_ANLREQ-D2-W228-S2; the row landed as `110d6583be`). `durable_job.py` imports `submission`, which the entry already stages (measured).
2. **The Terraform grant** `infra/aws/terraform/investor-reporting/export/commentary_draft_store.tf` statements S6 (UpdateItem on the jobs table, leading keys, attributes `hop_failure` plus the two keys, ReturnValues NONE) and S7 (KMS via DynamoDB for the jobs table): merged (AR-tf-73). Plan-only first; apply by the applier only. (To measure: `terraform plan` shows exactly the inline policy of `irpt-commentary-draft-store-role` changing and nothing else.)
3. **The commentary function** (the transcripts root ships ONE zip to three functions, row IRPT_ANLREQ-D2-S127): `data/transcripts/scripts/commentary/lambda_handler.py` calling the `fail` op (order AR-tf-72, merged as 49e34833a5). SURGICAL zip as in R42 section 8: the live zip plus exactly the commentary members from the pin; the pull and mail-pull functions never receive it.

Order of operations: grant (2) first, then the draft-store zip (1), then the commentary function (3); the function that calls `fail` must not go live before the op and the grant exist.

## 2. What to measure before signing (all "to measure")

- Live code hash of each of the two Lambdas against the artifact the repo says is live (diff against the BUILD INPUT, not the file name).
- `aws iam simulate-custom-policy` battery on the new inline policy: ALLOWED the `hop_failure` update (UpdateItem on the jobs table with Attributes `hop_failure`, `tenant`, `job`); DENIED PutItem, DeleteItem, GetItem, Query, Scan on the jobs table, and an UpdateItem naming any other attribute. KMS statement S7 cannot be simulated for the encryption context; say so in the packet and prove it by the invoke in section 3.
- Terraform plan scope: one resource, in-place.
- Every differing member of both zips against the live zip (S127 rule: surgical, or a pair that reads every differing member).

## 3. The proof (no outside-model call)

One invoke of the draft-store Lambda in a DEV test tenant with a synthetic request id: `{"op": "fail", "tenant": <test firm>, "request_id": <id>, "hop": "COMMENTARY", "code": "COMMENTARY_DRAFT_REFUSED"}`, then the same again. Expected: first answer `hop_failure_written` true, second false (set-once); the job row then carries `hop_failure` = `{hop, code, at}` and its state is unchanged; an invoke naming another firm's request answers `UNAVAILABLE` and the row of the other firm is unchanged. The job row used is a synthetic one the proof creates and removes (to measure: how a synthetic job row is created without a generation; if it cannot be, the proof waits for a FWD-1 run's real row and says so).

## 4. Blast radius and rollback

- Grant: one inline policy of one role gains two statements; rollback = apply the previous policy (the previous inline policy blob is captured by the applier before the apply).
- Draft-store zip: one function; rollback = the previous zip (fetched and hashed before the act).
- Commentary zip: one function; rollback = the previous live zip (hash `xC1GDXXp` family at R42; re-read at the pin).
- Nothing touches client data, the pull functions, a schedule or an S3 key.

## 5. Limits the issuer states

- The `hop_failure` of the READY_SIGNAL and PACKAGER hops, the status words and the ticket page read are NOT in this packet: they are `2.0.0_SA_COO~G2`'s and `2.0.0_SA_COO~V2`'s, and FWD-4 is not realized until all three halves are live and each failure has been driven on purpose (the drive-on-purpose map: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~233/FWD4_DRIVE_ON_PURPOSE_MAP.md`, 13 rows, each offline-drivable).
- Not claimed live: any `COMMENTARY-POST` line, a ticket 200, or figures in a real prompt (unchanged from R44).
- The commentary no-vendor-word stop writes no `hop_failure` by design (row IRPT_ANLREQ-D2-W233-S2).

## 6. Who

Pair: this COO half; the CTO half (`1.0.0_SA_CTO~DELL2`) signs the blob; applier `0.7.0_AE_CloudOps~AQ2` under an order cut only after the signed half. The grant's pair may be `2.0.0_SA_COO~G2`'s as the `irpt-jobs` owner (CTO msg 8970); name the pair here at the pin.

## 7. Measured on 2026-10-16 ~07:4xZ (issuer; read-only AWS gets of single resources)

- Live draft-store Lambda code digest: `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=`, 139,803 bytes, last modified 2026-10-12T00:06:20Z, handler `commentary_draft_store.lambda_handler`. It EQUALS the `artifact_sha256` the source map records for the entry (measured), so the repo's claimed live artifact is the live artifact.
- Live inline policy `irpt-commentary-draft-store-policy` carries statements S1 to S5 only; S6 and S7 are not applied (measured by `iam get-role-policy`, Sids only).
- The commentary function's live digest is `hUZY39qN` (the surgical zip applied in TO-APPLY-t34, R44); the rollback zip for this act is that one, re-read at the pin.
- G2's reader half is in trunk: `irpt-status` returns the closed failure code (commit dad5c4530b, AR-g-111, `ops/owned_status.py` reads `hop_failure`). The writers of the ready-signal and packager hops are G2's (AR-g-109, merged).
- **Source-map row: LANDED.** `110d6583be` (`2.0.0_SA_COO~P2`, CTO ruling msg 9173): `staged_from` row for `ycharts/generate/durable_job.py`, pin `065652d351`, sha256 `877929f2...ece979`, measured equal to the irpt-status row. The applier builds the draft-store zip from that map at that pin and STOPS if the built zip lacks `durable_job.py` or `submission.py`, or if its digest differs from the one the CTO half names.

## 8. The applier's steps and STOP conditions

1. Read the live digests of both Lambdas and the live inline policy; STOP if the draft-store digest is not `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=` or the commentary digest is not `hUZY39qN` (the state this packet was measured against).
2. `terraform plan` of the draft-store root, plan-only: STOP unless exactly one resource changes in place (the inline policy of `irpt-commentary-draft-store-role`, adding S6 and S7). Run the `iam simulate-custom-policy` battery of section 2; STOP on any mismatch.
3. Apply the grant (`safe-apply`, never bare), then re-plan: `No changes`.
4. Build the draft-store zip from the map at the pins; STOP on a member-diff against the live zip other than `commentary_draft_store.py` and the new `durable_job.py` (the S127 rule). Deploy it through the Terraform path only (never `aws lambda update-function-code`); read the live digest equals the built one.
5. Build the SURGICAL commentary zip (live zip plus exactly the commentary members from the pin; R42 section 8); apply to the commentary function only; read its digest; the pull and mail-pull functions keep theirs.
6. The proof of section 3; record each digest and each answer.
ROLLBACK, per artifact, in reverse order, as in section 4. Open a change-management ledger entry at the start and close it at the end (NEVER-2); no step is left half-landed: finish or roll back.

## 9. AMENDMENT 1 (issuer, 2026-10-16 ~08:2xZ): the grant's Terraform source is repaired and re-pinned

The applier `0.7.0_AE_CloudOps~AQ2` STOPPED `TO-APPLY-t54` at step 3 (msg 9184, record `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_t54/A_PRE_T54.txt`): `terraform plan` of `commentary_draft_store.tf` failed to parse, a missing comma between statements S7 and S1 (a defect of the issuer's cell AR-tf-73: its static test read statements by Sid and never the separators). Nothing was applied and no AWS write was made; the preconditions (digests `cwf6bUEb...` and `hUZY39qN...`, S1 to S5, mapping 1 Enabled) matched the packet.

Repair: order AR-tf-77 (worker 234), merged as `0a0214b507`: ONE comma (1 line added, 1 removed), no other byte, plus a separator-and-bracket scanner test (21 tests, mutants for a removed or doubled comma, an unmatched brace and an unterminated quote refused). **New pin: `infra/aws/terraform/investor-reporting/export/commentary_draft_store.tf` blob `0ab8d2e9ebed9f7d041ac19df9783151bc78f8d6`** (replaces `70368863550a` in the header; every other pin is unchanged). The scanner reads the statement list only; separators between keys inside a statement object were read by eye, so the applier adds a step: **3a, BEFORE step 3's plan: `terraform init -backend=false` and `terraform validate` in the draft-store root; any error = STOP, nothing applied.**

Sections 1 to 8 otherwise stand. The CTO half signed on blob `8dcbccc512`; this amendment changes the packet blob, so that half is re-signed on the new blob (a pin repair, no change to the act, its blast radius or its conditions).
