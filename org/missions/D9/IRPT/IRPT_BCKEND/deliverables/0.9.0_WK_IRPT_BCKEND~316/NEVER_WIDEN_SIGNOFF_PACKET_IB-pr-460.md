# Never-widen sign-off packet -- IB-pr-460: what a release of the draft store's `ticket_id` answer would move, for `irpt-commentary-draft-store-lambda`

Prepared by 0.9.0_WK_IRPT_BCKEND~316 for 2.0.0_SA_COO~P2 on TO-IB-pr-460 (round 156; PRD ADDENDUM v0.45; CTO msgs 6024 and 6033). Base `7bd08ac698`; pin `b7da10ca46` (Part A: the change, its tests and the answers file). Nothing was uploaded, deployed or applied: BUILD_ONLY from the committed pin in this worktree against a candidate map (the real map, byte-equal: no row pins the changed member; `candidate_repins.json` is its committed diff, empty, and `make_candidate_map.py` regenerates the map, sha256 `eec6eea6e30cfe09...`; the full copy is not committed because it names client firms and carries an account id; `lambda-source-map.json` untouched), AWS READS only through the `.tools/aws` shim, offline replays with in-memory fakes and synthetic ids. This packet does NOT say which ratified outcome any change serves beyond the `serves` column, and it recommends nothing on timing.

## Read this first

1. **One member moves: `commentary_draft_store.py` (1 of 16), owned by this cell's commit alone.** No rider. The other 15 members are byte-identical to the live package, `acceptance.py` and `submission.py` among them (they stay at their live pins: yes, member bytes equal).
2. **Digests.** Live `AsKY+KWLZBW54N73z9VdnR7SIKMPd9RDoYS8x4vRkpw=` (read 2026-10-11T23:17:34Z UTC; the downloaded package hashes to it). Built `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=` (139803 bytes), twice, byte-identical: True. Rollback S3 version `ToWX4K7J1NpXcwbkf4imLR6Xu0_0aJGn` (content sha256 equals the live digest by bytes; it is the LATEST object).
3. **Replay: 20 arms, 0 unexpected.** A first persist for a record with no usable ticket id (no key, empty, null, integer, list) answers byte-identically on live and built. For a record with one, live answers `status` and `commentary_ref`; built adds `ticket_id` equal to the record's. A replay, six refusals and `get_ref` are identical. `requests.get` is called once per persist on both.
4. **The one consumer ignores the member**: the drafter reads `commentary_ref` only (`lambda_handler.py:125`) and copies three keys (`:135-138`); an offline arm shows identical results for the old and the new answer.
5. **Two facts that differ from the order's expectation**: no staged row pins `commentary_draft_store.py` (it is native to `source_dir`), so the candidate re-pins 0 rows (row `IRPT_BCKEND-D2-W316-S1`); and the map entry's `artifact_sha256` is not the live digest (row `IRPT_BCKEND-D2-W312-S1`, unchanged by this read).

## `irpt-commentary-draft-store-lambda`

| | |
|---|---|
| live CodeSha256 | `AsKY+KWLZBW54N73z9VdnR7SIKMPd9RDoYS8x4vRkpw=` (read 2026-10-11T23:17:34Z; LastModified 2026-10-11T04:12:31.000+0000) |
| built (twice, byte-identical: True) | `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=` (139803 bytes) |
| rollback S3 version | `ToWX4K7J1NpXcwbkf4imLR6Xu0_0aJGn` (2 versions of the key, 1 the same size as live) |
| members live / built / moved / added / removed / unchanged | 16 / 16 / 1 / 0 / 0 / 15 |
| candidate rows re-pinned | 0 (the changed member is native to `source_dir`; `acceptance.py`, `submission.py` and `keys.py` stay at the live pins `283f7e7700`) |
| riders | none |
| live configuration (names only) | handler `commentary_draft_store.lambda_handler`, python3.12, 512 MB, 29 s, role `irpt-commentary-draft-store-role`, layers none, environment variable names: `IRPT_JOBS_TABLE`, `IRPT_REQUESTS_TABLE` |
| import-closure gate (build) | OK: import-closure -- 8 packaged .py file(s), every top-level import satisfied by package/stdlib/runtime/layer. (Nested lazy imports exempt by design.) |
| who may invoke | `irpt-commentary-draft-store-invoke-policy` (`lambda:InvokeFunction` on this one function), attached to `outlook-global-commentary-draft-role` (`transcripts/commentary.tf:256-259`); no resource-based permission is declared |

**Every moved member (1): owning commits and class**

- `commentary_draft_store.py` (THIS CHANGE; live `6ad7ac7211c9...`, built `d0373a342236...`; live blob = commit `20a62c3c6c`, built bytes = the pin blob: True) -- **served**. On a first persist that answers status OK the answer gains a third member, ticket_id, equal to the accepted record's ticket_id when that is a non-empty string; for a record with none (absent, empty, null or not a string) the answer is byte-identical to live's. A replay, every refusal and get_ref are unchanged. resolve_request keeps its two-value return (it now wraps _resolve_record, which holds the same single requests.get read and also yields the ticket id). The only owning commit is IB-pr-460's (b7da10ca46); no earlier unreleased commit touches this path since the live blob (20a62c3c6c). Classed served: the function's answer changes for a record with a ticket id.
    - `b7da10ca46` build(IRPT_BCKEND round 156, 0.9.0_WK_IRPT_BCKEND~316): IB-pr-460 Part A -- the draft store's first-persist OK answer ca  -- serves: IRPT_BCKEND TO-IB-pr-460 (round 156, cell IB-pr-460), Part A: PRD ADDENDUM v0.45, the commentary draft store's persist answer names the request's ticket

**acceptance.py and submission.py.** Not moved. a re-pin of the two staged rows to the round-152 base (e7bb7e923a) would move both: acceptance.py would carry 74bbdbb322 (IB-pr-455, commentary_requested copy) and 2f7cc7be42 (AR-y-37, acting_principal_id required keyword), submission.py would carry 74bbdbb322; both inert in this package because nothing packaged calls accept or lookup (round-152 read, 0.9.0_WK_IRPT_BCKEND~312 member_classes.json). Not applicable to this candidate: neither is re-pinned.

**Branch A** -- release forward, then the module's Terraform path.

1. No source-map row needs to land for the changed member (it is native to `source_dir`; the builder reads it from the tree the build runs in). The build must run from a tree whose `commentary_draft_store.py` is the blob of `b7da10ca46` (sha256 `d0373a3422365401bd5ec1cf27b516ab51611790a32f6dc2586ea15e06216c2c`) and whose staged rows are the ones in the map today; otherwise this read is re-run. The entry's deploy fields are rewritten by `record-terraform-deploy.sh` at the apply.
2. `bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-commentary-draft-store-lambda`; the object's `content-sha256` metadata must read `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=`. A different digest stops the apply.
3. `safe-apply` of the root `infra/aws/terraform/investor-reporting/export` on `module.irpt_commentary_draft_store.aws_lambda_function.this` only; the module takes the object's own VersionId and `content-sha256`, so the plan must show `s3_object_version` and `source_code_hash` and nothing else on the function. Role, environment, handler, runtime, memory and timeout are not changed by this build (Terraform not planned by this order). A change-management ledger entry is opened at the start and closed at completion.

**Branch B** -- redeploy the rollback version, re-read at apply: S3 version `ToWX4K7J1NpXcwbkf4imLR6Xu0_0aJGn` of the function's own artifact key (content sha256 `AsKY+KWLZBW54N73z9VdnR7SIKMPd9RDoYS8x4vRkpw=`), through the same Terraform path, pinning the function to that version. The rollback version is RE-READ AT APPLY (`list-object-versions` and `head-object` on that one key), because a later upload makes today's reading stale. After it the CodeSha256 must read `AsKY+KWLZBW54N73z9VdnR7SIKMPd9RDoYS8x4vRkpw=`. Branch B writes nothing to any record; a draft persisted while the built code ran keeps whatever answer it already returned (the answer is not stored).

## After-read proposed (nothing is persisted)

1. `lambda get-function-configuration`: CodeSha256 equals `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=`; handler, runtime, memory, timeout, role name and environment NAMES equal the table above.
2. One direct invoke of `{"op": "get_ref"}` (a refused shape: status REFUSED, reason INVALID_REQUEST; it reads no table and writes nothing). It shows the built package imports and answers. It does not reach the new member.
3. If a seat can say whose request it is: one direct invoke of `op get_ref` with that request's `{tenant, request_id}` answers the same body as the same invoke before the apply and carries no `ticket_id` (contract). It persists nothing.
4. The drafter's record for its next organic run, as in the consumer section of the json. **What then stays unexercised:** the new member on a live first persist, which needs a persist (a write to S3 and the requests table as svc-commentary) and no draft is persisted for a test.

## The consumer

- **the commentary drafter (outlook-global-commentary-draft-lambda), data/transcripts/scripts/commentary/lambda_handler.py make_draft_store, by direct RequestResponse invoke of this function**, `data/transcripts/scripts/commentary/lambda_handler.py:122-125,135-138`.
- On the new member: Ignores it today. invoke() returns doc.get('commentary_ref') only (line 125) after checking status == OK (line 122); persist_draft (lines 135-138) then requires and copies the three _STORED_FIELDS (line 73: artifact_id, sha256, version_id) and returns nothing else. No line of the drafter reads ticket_id from this function's answer. Offline arm: IB156-1_consumer_arm.json shows put and get_ref returning identical values for today's answer and the built answer.
- The read through it: The offline arm above, run now (it persists nothing and invokes nothing). In the world, the one read through the drafter is passive and persists nothing of its own making: the drafter's record for its next organic run, which ends at stage draft_stored (a first persist, the answer carrying ticket_id when the request's record has one) or draft_exists (get_ref, unchanged), read from its result and its log lines that name request ids only. If no such run occurs the drafter's live behaviour on the new member stays unexercised; no draft is persisted to make one.

## The replay (offline; live zip against built zip; `IB156-1_replay.json`)

20 arms; verdicts: {'identical': 17, 'expected-diff': 3}; negative controls: 2. Harness `replay/run_replay_460.py` over `replay/probe_460.py` and `replay/consumer_arm_460.py`: boto3 is never imported, every port is an in-memory fake, every socket connect is refused, AWS is never called by the replay, every id is synthetic, one tree per `python -I` process. Verdicts are computed from the probe outputs; a comparison that does not come out as stated would read UNEXPECTED (unexpected: 0).

- **identical** first persist, record with no ticket_id key (no usable ticket id): the answer is byte-identical on live and built -- live and built answer ['commentary_ref', 'status'] members ['artifact_id', 'sha256', 'version_id']; the serialized answers are equal.
- **identical** first persist, record with ticket_id is the empty string (no usable ticket id): the answer is byte-identical on live and built -- live and built answer ['commentary_ref', 'status'] members ['artifact_id', 'sha256', 'version_id']; the serialized answers are equal.
- **identical** first persist, record with ticket_id is null (no usable ticket id): the answer is byte-identical on live and built -- live and built answer ['commentary_ref', 'status'] members ['artifact_id', 'sha256', 'version_id']; the serialized answers are equal.
- **identical** first persist, record with ticket_id is an integer (no usable ticket id): the answer is byte-identical on live and built -- live and built answer ['commentary_ref', 'status'] members ['artifact_id', 'sha256', 'version_id']; the serialized answers are equal.
- **identical** first persist, record with ticket_id is a list (no usable ticket id): the answer is byte-identical on live and built -- live and built answer ['commentary_ref', 'status'] members ['artifact_id', 'sha256', 'version_id']; the serialized answers are equal.
- **expected-diff** first persist, record WITH a ticket id: live answers today's two members, built adds ticket_id equal to the record's -- live members ['commentary_ref', 'status']; built members ['commentary_ref', 'status', 'ticket_id']; ticket_id equals the planted synthetic id: True; commentary_ref equal on both.
- **identical** requests.get is called exactly once for a first persist, live and built, with and without a ticket id (no second read) -- calls: live 1 / 1, built 1 / 1.
- **identical** writes: one artifact put and one commentary_ref set per request, live and built, with and without a ticket id -- artifact puts 1 / 1 and ref sets 1 / 1 on both sides in both cases.
- **identical** replay (second put of the same request), record WITH a ticket id: ALREADY_WRITTEN on both, no ticket_id -- live {"reason": "ALREADY_WRITTEN", "status": "REFUSED"}, built {"reason": "ALREADY_WRITTEN", "status": "REFUSED"}.
- **identical** replay (second put of the same request), record WITHOUT a ticket id: ALREADY_WRITTEN on both, no ticket_id -- live {"reason": "ALREADY_WRITTEN", "status": "REFUSED"}, built {"reason": "ALREADY_WRITTEN", "status": "REFUSED"}.
- **identical** refusals (other_tenant, reserved_tenant, unknown_op, extra_key, missing_draft, absent_record), record WITH a ticket id: identical on live and built, each exactly {status, reason} -- reason codes built: other_tenant=UNAVAILABLE, reserved_tenant=INVALID_REQUEST, unknown_op=INVALID_REQUEST, extra_key=INVALID_REQUEST, missing_draft=INVALID_REQUEST, absent_record=UNAVAILABLE.
- **identical** refusals (other_tenant, reserved_tenant, unknown_op, extra_key, missing_draft, absent_record), record WITHOUT a ticket id: identical on live and built, each exactly {status, reason} -- reason codes built: other_tenant=UNAVAILABLE, reserved_tenant=INVALID_REQUEST, unknown_op=INVALID_REQUEST, extra_key=INVALID_REQUEST, missing_draft=INVALID_REQUEST, absent_record=UNAVAILABLE.
- **identical** get_ref before and after a first persist, record WITH a ticket id: identical, no ticket_id -- built before {"commentary_ref": null, "status": "OK"}; after members ['commentary_ref', 'status'].
- **identical** get_ref before and after a first persist, record WITHOUT a ticket id: identical, no ticket_id -- built before {"commentary_ref": null, "status": "OK"}; after members ['commentary_ref', 'status'].
- **expected-diff** crash-recovery branch (artifact exists, commentary_ref never set), record WITH a ticket id: built carries ticket_id, live does not; the first artifact's ref is returned on both -- live members ['commentary_ref', 'status']; built members ['commentary_ref', 'status', 'ticket_id']; refs equal.
- **identical** crash-recovery branch, record WITHOUT a ticket id: identical -- members ['commentary_ref', 'status'] on both.
- **identical** resolve_request(requests, tenant_hint, request_id) still returns exactly (tenant, owner): arity 2 on live and built -- live {'returned': 2}, built {'returned': 2}; the built tree adds _resolve_record: True (live: False).
- **expected-diff** [NEGATIVE CONTROL] NEGATIVE CONTROL: the built tree with commentary_draft_store.py put back to the LIVE bytes -- the first persist for a record WITH a ticket id answers today's two members again -- control answer members ['commentary_ref', 'status'] equal live's and differ from built's: commentary_draft_store.py is the member that adds ticket_id, and this comparison can tell an answer with the member from one without.
- **identical** [NEGATIVE CONTROL] NEGATIVE CONTROL: the same control tree, record WITHOUT a ticket id -- equal to built's answer (the comparison reads identical when nothing differs) -- control answer members ['commentary_ref', 'status'], equal to built's.
- **identical** consumer: the drafter's own make_draft_store, given today's two-member first-persist answer and then the built three-member answer, returns the same three keys for put and the same ref for get_ref -- offline: lambda_handler.make_draft_store over a fake lambda client (no AWS call); persist_draft returned ['artifact_id', 'sha256', 'version_id'] for both answers; existing_draft returned the ref for both; payload ops ['put', 'get_ref'] (IB156-1_consumer_arm.json).

## What is NOT exercised

- a LIVE first persist with a record that carries a ticket_id: it writes an artifact to S3 and rows to the requests table as svc-commentary; no draft is persisted to test a release unless a seat can say whose request it is
- the live record shape of ticket_id: whether any accepted record in the requests table carries one is not established here (IB154-1 read, finding 13); the offline fakes plant a synthetic id
- the real DynamoDB conditional update, the real ArtifactRepository and S3: the replay used in-memory fakes of the request, ref and artifact ports and the unit tests used the repository's own fakes
- the drafter's live behaviour (its role, its DRAFT_STORE_FUNCTION value, its environment): only its committed code was run, against a fake lambda client
- the live invoke-policy attachment and the function's live resource policy (only get-function and get-function-configuration were read); the live environment VALUES (names only were read)
- Terraform: no plan or apply, no S3 write; the module's s3_object_version and source_code_hash path is described in the packet, not run
- the map entry's own record: its artifact_sha256 is not the live CodeSha256 and its _build_note still reads DESIRED (row IRPT_BCKEND-D2-W312-S1); this read does not change it
- the drafter edit that would READ ticket_id: another seat's cell, after this function's release; nothing here reads, copies or posts the member

## Rows and state

Row filed by this worker: `IRPT_BCKEND-D2-W316-S1` in `org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md`. Uploads 0, applies 0, real source-map edits 0, vendor calls 0, functions invoked 0. Scratch packages are outside the worktree and are deleted file by file at the end of the order. Commits are LOCAL on branch `wk-IRPT_BCKEND-316`; nothing is pushed.
