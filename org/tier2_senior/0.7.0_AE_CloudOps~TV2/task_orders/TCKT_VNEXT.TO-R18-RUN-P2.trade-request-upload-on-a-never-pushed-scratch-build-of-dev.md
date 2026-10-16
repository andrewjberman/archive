<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R18-RUN-P2.trade-request-upload-on-a-never-pushed-scratch-build-of-dev</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-16</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>18</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R18.md</decomp_doc> (round 18): cell `R18-tf-6`, PART 2 of the live run (PART 1, the Meeting Request, is `TCKT_VNEXT.TO-R18-RUN`).
<owned_cells>R18-tf-6</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer adds a CONDITIONAL GO amendment on the signed run pair (its AMENDMENT 3, both halves) naming the sha of the portal `DEV` head to build from. On the GO, run ONE live Trade Request journey (FWD-10) on a NEVER-PUSHED SCRATCH BUILD of DEV in which the single line hiding Trade Request from the New Ticket list is removed: a detached worktree, one changed line, served on `http://localhost:5174` for the run only, then stopped and removed. File the placeholder trade form for the firm `cottonwood` as a minted synthetic filer, read the ticket and the form's object, remove the filer, and write one result file.
  </objective>

  <context>
    Authority: the CTO's msg 9769 (ruling (c): "Andrew's hold binds what is pushed or shown. The scratch build lives in a detached worktree, is served on localhost only for the run, and is never pushed, merged or shown, then deleted. The form object is synthetic, listed by key and VersionId, and deleted after the grade. The hide stays on DEV and PROD; lifting it is Andrew's."), the run pair `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` (the original sections 1 to 4, AMENDMENT 1 for the origin, AMENDMENT 3 for this part). Andrew's hold: hide `4d601023` on his word of 2026-10-13 ~18:5xZ, "we should not push this til we actually have a functioning channel for that". Your own STOP (msg 9764, row `TCKT_VNEXT-D2-S56`) found it. PART 1 (`TO-R18-RUN`, FWD-11) is independent. The release is live (applied 2026-10-16T17:57:19Z, both checks REL-OK).
    The model is `TO-R18-RUN` sections 1 to 3 and step 3: the filer's identity row (`USER#tckt-r18-filer-<stamp>@opal.invalid`, `PROFILE`, `firmId opal-capital`, `userType "test-filer"`, `allowedFirmIds` the LIST `["cottonwood"]`, `attribute_not_exists(PK)`), one RS256 token (the current signing slot, `exp` at most 20 minutes after `iat`, key and token in memory only, the key read reported after the fact through `0.0.0_AB_MSTR~DELL2`), the placeholder file `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/PLACEHOLDER_TRADE_FORM.pdf`.
  </context>

  <go>
    STAGED. The GO is an AMENDMENT to this order citing the signed pair's AMENDMENT 3 at its blob and naming the `DEV` sha. Then, in order:
    1. STEP 0: open the NEVER-2 ledger entry (also naming the scratch worktree) and keep it open until the identity row reads ABSENT and the worktree is removed. Measure the blobs the GO names. Start gate (any failing item is a STOP before anything is created): the release is live (`r18_rel_check.py` REL-OK); the sha the GO names is on `origin/DEV` and carries `c05e3dda` and `12c164a0`; no open ledger names `opal-ticket-api`, `opal-tickets` or `opal-users-v2` in any live worktree (print the denominator); `git -C <portal> worktree list` prints no scratch path from an earlier run.
    2. STEP 1, THE SCRATCH BUILD: `git -C <portal> worktree add --detach <path> <sha>` (`<path>` derived from `git rev-parse --show-toplevel`, never typed absolute); link the dependencies to the shared portal's `node_modules`; remove the one `.filter(([v]) => v !== 'trade_request')` of `src/pages/TicketCenter/TicketCenter.tsx` (the type select near line 730); print `git -C <path> diff --stat` and the changed-line count (exactly one removed and one added line); NEVER commit, branch, stash, push or merge in it.
    3. STEP 2: serve it (`bun run dev --port 5174`; resolve bun by the profile). Open a Playwright browser on `http://localhost:5174` and print the page's origin; any other origin is a STOP.
    4. STEP 3, the Trade Request: mint the filer row and its token; as the filer open the Ticket Center, New Ticket, the type select must now list Trade Request, choose it, the firm `cottonwood`, the placeholder PDF, submit. The page makes three calls (upload-presign, the browser's PUT to the presigned URL, the ticket CREATE): print the PUT request's `Origin` header (it must read `http://localhost:5174`). ConsistentRead the ticket (`ticket_type trade_request`, `status open`, `attachment.key` under `portal/cottonwood/state/ticket_attachments/trade-form/`), `head-object` the form (size 643, its VersionId), and record the WE_* token of the CREATE.
    5. STEP 4, CLOSE: stop the dev server; REMOVE the scratch worktree (`git -C <portal> worktree remove --force <path>`), print `git -C <portal> worktree list` (no scratch path) and `git -C <portal> status --short` (unchanged from the start); wait until the token's `exp` has passed; delete the filer row and read it ABSENT with ConsistentRead.
    6. STEP 5: write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_run/R18_RUN_P2_RESULT.json` with the keys `browser_origin`, `put_origin_header`, `identity`, `firm`, `tf_ticket`, `tf_filer`, `row_deleted_at`, `token_exp`, `row_absent_after`, `form_key`, `form_name`, `form_version_id`, `placeholder_named`, `no_engine_call`, `token_printed`, `scratch_diff_lines` (1), `scratch_removed` (true), `change_ledger`. Run `r18_run_check_trade.py` (RUN-OK (trade only)); close the ledger only after it prints that. Write the proof instance beside this order, flip it, write your session log and report once to `2.0.0_SA_COO~V2`.
    If a STOP fires, report it FIRST with the world as left, and remove the worktree and the row first.
  </go>

  <bounds>
    The blast radius is the pair's AMENDMENT 3: one `opal-tickets` item, one 643-byte synthetic object in `opal-data-cottonwood` (left until the issuer's delete after the CVO's grade), one `opal-users-v2` row, ONE detached worktree. No push, merge, branch, commit or stash of the scratch build; no change to `origin/DEV` or PROD; no screenshot or description of the scratch build shown outside your record. No Lambda environment change (no routing window), no IAM, no Terraform, no meeting ticket, no coordinator identity. No claim, no complete, no report, no IRPT write.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R18RUNP2-AC1" cell_refs="R18-tf-6"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_CHECKS/r18_run_check_trade.py</invocation><expect>^RUN-OK </expect></criterion>
</proof_of_spec>
`R18RUNP2-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file`: no result file yet). The check re-reads the trade ticket and the form's object (size and VersionId equal to the recorded one) and the identity row from the live tables and S3 with read-only calls, and reads the result file's `scratch_diff_lines` and `scratch_removed`.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the identity row is written and deleted with the operator's own credentials; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`.
comp-adversary: the control is the check's independent live re-read and the pair's STOP conditions; the lens: the scratch build left behind or committed (the removal and the status read), a screenshot of it shown (forbidden), the object's VersionId lost (it is printed), a page origin other than `http://localhost:5174`, a second filer row.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R18-tf-6): a live run under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
