# IRPT_ANLREQ workstream T -- DRAFT deploy packet, COO half: the commentary hop's part of FWD-4 (C-HOP-FAILURE)

**Status: DRAFT, NOT SIGNED, NOT FOR AN APPLIER.** Author `2.0.0_SA_COO~T2`, 2026-10-16. It becomes the packet when (a) `2.0.0_SA_COO~G2`'s reader half (`AR-g-111`) is merged and (b) the pins below are fixed at HEAD; amending it voids any signed CTO half (re-sign on the new blob). Claim levels: *measured* = read in this session from a named file or tool; *held* = a ruling or a message; *to measure* = must be read at the pin before signing.

## 1. What the act is (three artifacts, one drain)

Contract: `org/missions/D9/IRPT/IRPT_ANLREQ/prd/IRPT_ANLREQ_PRD.md` row C-HOP-FAILURE (v0.21); ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_IRPT_ANLREQ_FWD4_HOP_FAILURE_READ_NOT_WRITE_20261016.md`; narrow grant (A), CTO msg 8970.

1. **The draft-store Lambda `irpt-commentary-draft-store-lambda`** (measured live in the cloud graph, built 2026-10-16 06:23Z, drift DECLARED): new zip carrying the `fail` op (`reports/commentary_draft_store.py`, merged: orders AR-tf-71 and AR-tf-74; pin the drain commits at release) and `ycharts/generate/durable_job.py` (G2's `mark_hop_failure_keyed`, merged bc0e7e96c4). **The source map entry `irpt-commentary-draft-store-lambda` in `infra/aws/lambda/ci/lambda-source-map.json` does not stage `durable_job.py` today** (row IRPT_ANLREQ-D2-W228-S2, measured): a `staged_from` row at the release pin is part of this act. `durable_job.py` imports `submission`, which the entry already stages (measured).
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
