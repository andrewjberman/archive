# Never-widen sign-off packet -- r37 (version 2) Lambda leg: irpt-ycharts-generate (the upload door) takes the O1 owner fallback AND the Ticket Center ticket confirmation, at pin 3fac627b03

**Supersedes** `NEVER_WIDEN_PACKET_R37_UPLOAD_DOOR_OWNER_RESOLUTION_20261020.md` (blob `11b96f429a`, CTO half signed @7f9a2ddaca, zip `51dc323c...`, never uploaded). This version adds a second mover and a widening of who takes the Opal producer; it needs its own CTO half.
**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** PRD IRPT_ANLREQ v0.24 O1 (an Opal staff user is never refused) and FWD-1 item (3) ("the Opal-generated report: the Opal producer, not YCharts"); CTO msg 11206 item 2 (a MUST cell: `confirm_ticket` also stamps an `analysis_request` created through `/tickets` when `created_by` equals the request principal); the earlier O1 hunk design `O1_OWNER_RESOLUTION_HUNK_FOR_P2_REVIEW_20261019.md`. **Ledger:** `irpt-ycdgen-o1-r37-20261020`.
**Scope:** ONE Lambda code release (`irpt-ycharts-generate`, the Analysis Request upload door). No IAM, route, queue, table, secret, schema or resident host moves. No vendor call. The other eight Lambdas that stage `_authz/served.py` do NOT move.

## 0. Why the second mover (measured)

Run 5C (IB2 receipt `irpt_anlreq_commentary_e2e5c/A_E2E5C.txt`) got past the door and the schema and was then retained by the resident three times with `RecipeRefused`. The issuer ran the repository's `prepare_normalized_upload` on the retained 5C document: "holdings row has no provider receipt" (SPY, AGG, TIMXX are KEPT_BY_HISTORY, the door's notices). That is the VENDOR recipe. The request took it because `producer_for(record)` (`ycharts/generate/resident_worker.py`) picks the Opal producer only when the accepted principal is on `OPAL_PRODUCER_PRINCIPALS` (two names) or the accepted record carries `ticket_confirmed` True, which the door stamps from `confirm_ticket(ticket_id, principal)` (`submission_service.py:148-158`). `confirm_ticket` was True only for a ticket whose `source` starts with `dashboard_form:`, which only `POST /api/scoped/tickets/submit` sets; the Ticket Center creates a staff ticket with `POST /api/scoped/tickets`, where the ticket service sets `source` to the body's value or `"portal"` (`ticket_center/lambda_function.py:1399`; a CREATE body claiming `dashboard_form:` is rejected) and stores `created_by` as the token subject always. So NO Ticket Center filing was ever stamped. Run 5D (allow-listed principal, Opal producer) passed: READY 25 s after submit, R2 sections 3 (no builder-only, no not-in-this-version).

## 1. What ships

Pin `3fac627b038f1a3e2e453bb7ca6360b08adf879c` (the map edit: `infra/aws/lambda/ci/function-map/irpt-ycharts-generate.json`, numstat 2 2 in this commit; the O1 `served.py` pin `720e125d31` is already in the map at trunk). Two movers against the live package (CodeSha256 `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=`, 107 members):

| member | live sha256 (12) | built sha256 (12) | attribution |
|---|---|---|---|
| `served.py` (from `_authz/served.py`, staged pin `720e125d31`) | `30c0eb88ec38` | `600a934c4b34` | AR-y-415 (O1): `_create_owner` and `_advisor_owner` fall back to the signed-in principal for a staff filer with no advisor or an unprovisioned one; `AdvisorUnprovisioned`; +26 / -13 lines. Unchanged from version 1; DASHBD `a3058c274c` is NOT carried. |
| `ticket_confirmation.py` (staged pin `752e87d46b73`, was `a0da937b3e77`) | `073cc8314304` | `e76593c7951a` | AR-y-440 (merged `57fbab70491`; product commit `752e87d46b73`): `confirm` also returns True for an `analysis_request` whose `source` does NOT start with `dashboard_form:` and whose top-level `created_by` equals the principal (case-insensitive after strip); a `dashboard_form:` source is still decided ONLY by `requester.email`; every other case and any exception is False. 21 lines changed in the file (diffstat: the function body and its docstring). |

Zip (built twice byte-identical by worker `0.9.0_WK_IRPT_ANLREQ~319`, record `0.9.0_WK_IRPT_ANLREQ~319/r59/R37V2_BUILD.json`; the issuer re-measured the file): sha256 `3e50a3366b3f4512d107f735e735bc49dce5ef0de9b68762de8f2c4b19d68d80`, CodeSha256 `PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA=`, 639224 bytes, 107 members; against the live members file: `moved = [served.py, ticket_confirmation.py]`, 0 added, 0 removed, 105 same. Stage folder `C:/dev/irpt-release-r37o2` (version 1's `r37o1` is superseded).
Tests: AR-y-440's seven new tests (`test_ticket_confirmation_create_path.py`, 7 passed; on the UNCHANGED code 4 fail, T1 and T2 among them) and the three existing ticket test files (13 passed, 10 subtests, before and after); `_authz` 375 passed for the O1 hunks (version 1).

## 2. Blast radius (read from the code at the pin)

| the door answers for | BEFORE | AFTER |
|---|---|---|
| an Opal staff filer, no advisor named, tenant listed | refused `NOT_AUTHORIZED` | the owner is the filer's own (`access.prospect_owner()`); stored |
| an advisor named and provisioned | the advisor's owner | the same |
| an advisor named, unprovisioned (no partner profile / user row absent, disabled or of another firm) | refused | the filer's own owner; the typed email is dropped |
| partner email/firm MISMATCH, unregistered firm, unreadable query, unresolvable owner | refused | refused |
| the accepted record of a request whose ticket was made by `POST /tickets` as `analysis_request` by the same principal (every Ticket Center filing) | `ticket_confirmed` absent, so the VENDOR producer | `ticket_confirmed` True, so the OPAL producer |
| the accepted record of a request whose ticket came from the submit form | stamped when `requester.email` equals the principal | the same |
| a ticket of another type, or created by someone else, or unreadable | not stamped | not stamped |
| any other route, role, table, key | unchanged | unchanged |

**Who gains.** The O1 change grants no new principal class (the filer-may-act rule is `uploads.py`'s, unchanged). The confirm change WIDENS who takes the Opal producer: any principal whose own `/tickets`-created `analysis_request` ticket accompanies an accepted request, instead of the two allow-listed names. That is the CTO's ruling (msg 11206 item 2), the allowed creators are those the ticket service's CREATE route admits (internal humans and service principals, by its RBAC), and the effect is on which PRODUCER builds the report, not on who may read or write anything. `created_by` is server-written (the token subject), so a client cannot choose it. **Writers counted.** `_create_owner` has one caller (the internal-subject create branch); `confirm_ticket` has one caller (the submission service's accept step), whose failure leaves the request accepted and unstamped. **Failure:** any exception in `confirm` is False.

## 3. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger `irpt-ycdgen-o1-r37-20261020`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming `irpt-ycharts-generate`, its role or its key is a STOP). Apply outside the weekday 11:30Z-14:15Z band and outside 05:45Z-07:00Z on Tuesday 2026-10-20; never alongside another IB2 act (the CTO's order: this release, then r34m v2, then run 6).
1. **R0, before-reads.** `get-function irpt-ycharts-generate` CodeSha256 equals `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=`; the key's latest S3 VersionId, downloaded and hashed, equals it (record the VersionId: the rollback source); the credential-less refusal envelope of the upload door (status, body sha256).
2. **U, build and upload.** Throwaway worktree detached at the pin, `BUILD_ONLY=1`: the printed CodeSha256 must equal `PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA=` (any other: ABORT, nothing uploaded); then the same build without `BUILD_ONLY` (one new object version); read back (sha256 equals `3e50a336...`). `MSYS_NO_PATHCONV` unset; a private TMPDIR.
3. **C, scoped plan.** Root `infra/aws/terraform/investor-reporting/ycharts` (the module is declared at `generate.tf:377`; if R0 finds the root differs, STOP and say so), `-target=module.irpt_ycharts_generate.aws_lambda_function.this`: `Plan: 0 to add, 1 to change, 0 to destroy`, attributes `last_modified`, `s3_object_version`, `source_code_hash` only. Anything else: STOP, nothing applied.
4. **A, apply** with `safe-apply` on the saved plan; never `aws lambda update-function-code`.
5. **V, after-reads.** G1 CodeSha256 equals the table; G2 live object vs the previous version differs in exactly `served.py` and `ticket_confirmation.py` (denominator 107); G3 the refusal envelope equals R0's; G4 `release-census.py` against the live zip prints `changed_members=0`.
6. **Map record and close** in the applier's worktree (`artifact_*` and `last_deployed_*` of the entry); close the ledger.

## 4. Rollback, per key

Copy the previous S3 VersionId (recorded at R0) onto the key, the scoped plan, `safe-apply`, read `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=` back. Nothing else moves. After a rollback, Ticket Center filings are again unstamped (the vendor producer).

## 5. Not claimed

- That the live zip is unchanged since the issuer's read of 2026-10-20 (R0 proves it).
- That a real staff upload with an unprovisioned advisor succeeds end to end, or that a Ticket Center filing now reaches a report (run 6 proves it, after r34m v2).
- That the Opal producer handles every kept or unresolved holding (the kept UNKNOWN ticker path through C-SWAP is not yet exercised past the door).
- That the typed advisor email is kept as attribution anywhere (it is dropped).
- That the six other function-map files that still name the old `served.py` sha are current (worker row `IRPT_ANLREQ-D2-W314-S1`; those Lambdas do not move).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one Lambda code object (one S3 object version) and its function configuration. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
