<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-PROMOTE-BACKOFF.portal-upload-resolving-backoff-dt</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-19</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is ONE branch of ONE commit on the portal PROD branch: the Ticket Center Analysis Request form keeps re-posting an upload that reads RESOLVING, with a growing wait of up to four minutes (it was fifteen seconds), and says so in the status line (4 files: TicketCenter.tsx, analysisRequest.ts and two test files); no API, IAM, data, Lambda or Terraform act. The page is client-facing (a partner login can open the Ticket Center); approval row dell2-20261019T192242Z-f75e is APPROVED, ruled by andrew (CTO msgs 10923 and 10933).
comp-routes: RUN-AS-A-READ -- step 6 reads the staff Ticket Center on PROD; no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading the CTO's rulings (msgs 10851, 10855, 10923, 10933), the issuer's payload read at the cut (1 commit, 0 merges, 4 files, none matching trade) and this order; the lens: a PROD tip that moved since the cut (the PROD-promote of ~V2's R20-PROD2 closed 19:26Z, so the tip may have moved), a builder that merges a second branch, a promote that passes typecheck and fails the vite build, a promote that touches Andrew's ticket. The order requires the exact base, head and counts, a PROMOTE-LIST naming ONE branch, and the gates at GO. NOT seen (blind): the vite build and the live page after the push, until steps 3 and 6; denominator: 1 branch, 1 commit, 4 files.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ71: the PROD promote of the PROD-based recut of the upload RESOLVING backoff.
<owned_cells>AR-y-411</owned_cells>
</decomp_ref>

  <objective>
    Promote ONE branch to PROD through /prod-deploy's chosen-set release, and nothing else: `cand/dell2/anlreq-prod-recut-v3`, head `a9cc52661e1adbc37e0df9e0d30cb742d86954ec`, ONE commit cut from `origin/PROD` `8cd45f623bdfae12ac6e4cfcfc8e0d74325ed4c3` (row dell2-20261019T192242Z-f75e, APPROVED, ruled by andrew). Verify CI; read on PROD that the deploy ran and that PROD equals the branch; report once to 2.0.0_SA_COO~Y2 with the run id (cc 1.0.0_SA_CTO~DELL2). You do NOT touch Andrew's ticket TCK-20261017-5af976ff and you do NOT merge into DEV: the fold of PROD into DEV is the issuing COO's step (CTO msg 10617).
  </objective>

  <context>
    WHY: a staff filing's commentary upload reads RESOLVING for longer than the form's old fifteen-second wait, so the form gave up while the door was still working; the branch re-posts with a wait that grows to four minutes in total and shows "still checking". It is already on DEV at 10b6fd06fa89 (row 56ed). The branch is the PROD-based recut by worker 305's predecessor chain (cell AR-y-411, order org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-y-411.prod-based-recut-backoff-and-filing-hint-pair.md). The filing-hint pair commit was NOT carried (archived as archive/cand/dell2/anlreq-filing-hint-keep-equal-pair).
    MEASURED by the issuer (2026-10-19 ~19:40Z, portal fetch): `git rev-parse origin/PROD` = 8cd45f623bdfae12ac6e4cfcfc8e0d74325ed4c3; `git rev-parse origin/cand/dell2/anlreq-prod-recut-v3` = a9cc52661e1adbc37e0df9e0d30cb742d86954ec; `git rev-list --count origin/PROD..origin/cand/dell2/anlreq-prod-recut-v3` = 1; merges 0; `git diff --name-only` lists 4 files and none matches `trade`. NOT run by the issuer here: the vite build; anything on PROD after the push. The PROD tip may move before your GO: you re-check.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Open the NEVER-2 ledger irpt-portal-anlreq-backoff-20261019 (.tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote on PROD), and commit it. Read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the portal PROD branch is a STOP, EXCEPT a stale entry of your own seat whose legs are all closed with proof and whose deploy sha you MEASURE as an ancestor of origin/PROD (with a negative control): close it with `.tools/deploy_ledger.py close`, print the measurement, commit, go on. Derive the workspace root, never type a device path.
    2. Re-check the set against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD` (must read `8cd45f623bdfae12ac6e4cfcfc8e0d74325ed4c3`; any other value: STOP, nothing pushed, tell 2.0.0_SA_COO~Y2, who re-cuts); `git rev-parse origin/cand/dell2/anlreq-prod-recut-v3` must read `a9cc52661e1adbc37e0df9e0d30cb742d86954ec`; `git rev-list --count origin/PROD..origin/cand/dell2/anlreq-prod-recut-v3` must print 1; merges must print 0; `git diff --name-only origin/PROD origin/cand/dell2/anlreq-prod-recut-v3 | wc -l` must print 4 and the same list piped to `grep -i trade` must print nothing. Any other value: STOP.
    3. Run /prod-deploy's gates on the tree the builder cuts: `bun run typecheck` 0 errors, `bun test src/pages/TicketCenter src/pages/InvestorReporting` (print the counts; a failing test is compared line by line against the same command at origin/PROD in a detached worktree: the failing lines must be the same, else STOP), and `bun run build`. Print each result. A failure: STOP.
    4. Promote with /prod-deploy's mechanics for a chosen set: `--features cand/dell2/anlreq-prod-recut-v3` and NOTHING ELSE (the PROMOTE-LIST must name exactly one branch, row dell2-20261019T192242Z-f75e; any other: STOP). The main portal tree never leaves DEV; the push is from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha; never an unaudited override.
    5. Read the CI conclusion with `gh run view --json` (never `gh run watch`): success, deployed sha equal to the promoted sha, tag peeled. Print sha and run id. Then `git -C portal fetch origin`; `git diff --stat a9cc52661e1adbc37e0df9e0d30cb742d86954ec origin/PROD` must print nothing and `git merge-base --is-ancestor a9cc52661e1adbc37e0df9e0d30cb742d86954ec origin/PROD` must exit 0.
    6. Read, on PROD, that a staff caller can open the Ticket Center after the promote, with the smoke instrument your earlier promote reads used (`portal/scripts/ui-smoke.mjs`, origin the PROD site) as an Opal STAFF-class login: open New Analysis Request, record whether the Firm chooser lists firms and the model list and tickers appear; screenshot and read it. State the login's class. If no sanctioned staff-class login is available, write ABSENT with the reason: do NOT mint a user, use a partner login as a stand-in or ask for a credential. Do NOT open, file, retry or edit any ticket.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_backoff/A_PROMOTE_BACKOFF.txt with, ONE line each, exactly: `K1 payload exactly 1 branch cand/dell2/anlreq-prod-recut-v3 a9cc52661e 1 commits 4 files (trade absent)`; `K2 gates typecheck 0 tests lines-equal-PROD build ok`; `K3 CI success deployed sha <12 hex> run <id> tag peeled`; `K4 PROD staff read firms and catalogue loaded` or `K4 PROD staff read ABSENT <reason>`. Then the PROD sha before and after, the run id, the receipt (pages and class, in words: the Ticket Center is client-facing, included under Andrew's word via row f75e) and the screenshot path. A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2): "dell2 portal backoff promoted to PROD" with the PROD sha before and after, the run id, the time PROD went live and the four lines. Do not merge into DEV.
  </the_act>

  <bounds>
    One branch (1 commit), the portal PROD branch. No API, IAM, data, Lambda or Terraform act. No second branch rides; a sweep of DEV is not a promote. No PROD user is minted. No ticket is opened, filed, retried or edited. No merge into DEV. Rollback: revert the promote on PROD through /prod-deploy's own mechanics, on 2.0.0_SA_COO~Y2's or 1.0.0_SA_CTO~DELL2's word only (no data is touched).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_backoff/IRPT_ANLREQ.TO-PROMOTE-BACKOFF.portal-upload-resolving-backoff-dt.proof_of_spec.json`.
    <criterion id="PBO-AC1" cell_refs="AR-y-411">The payload is exactly the one branch and the gates were green.<invocation>grep -c -E '^(K1 payload exactly 1 branch cand/dell2/anlreq-prod-recut-v3 a9cc52661e 1 commits 4 files \(trade absent\)|K2 gates typecheck 0 tests lines-equal-PROD build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_backoff/A_PROMOTE_BACKOFF.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PBO-AC2" cell_refs="AR-y-411">CI succeeded on the promoted sha, and the staff read on PROD is recorded (loaded, or honestly ABSENT).<invocation>grep -c -E '^(K3 CI success deployed sha [0-9a-f]{12} run [0-9]+ tag peeled|K4 PROD staff read (firms and catalogue loaded|ABSENT .+))$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_backoff/A_PROMOTE_BACKOFF.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PBO-AC3" cell_refs="AR-y-411">The ledger irpt-portal-anlreq-backoff-20261019 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-portal-anlreq-backoff-20261019_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a PROMOTE order to a tier-2 DT seat under the CTO's rulings (msgs 10851, 10855, 10923, 10933) and Andrew's word on row f75e, not a worker cell; the cell AR-y-411 is the issuer's, as for TO-PROMOTE-SET.
