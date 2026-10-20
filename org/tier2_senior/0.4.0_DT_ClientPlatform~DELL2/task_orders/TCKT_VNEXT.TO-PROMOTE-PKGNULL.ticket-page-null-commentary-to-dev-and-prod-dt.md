<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-PROMOTE-PKGNULL.ticket-page-null-commentary-to-dev-and-prod-dt</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>SERVED</risk>
<round>20</round>
<workstream>PKGNULL</workstream>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is ONE branch of ONE commit on the portal DEV branch (by the approved merge-forward route) and then on the portal PROD branch: the Ticket Center analysis-request package block reads a null commentary as "Commentary not available" and the package type accepts a null pair (3 files: tickets.ts, AnalysisRequestParts.tsx, one new test); no API, IAM, data, Lambda or Terraform act (the ticket-service half is LIVE since 00:22Z, TO-R20-REL2). The page is Opal-internal (staff-only Ticket Center rows); approval row dell2-20261019T235854Z-6473 is APPROVED by 1.0.0_SA_CTO~DELL2 (msg 11115, class opal-internal).
comp-routes: RUN-AS-A-READ -- step 6 reads the staff Ticket Center on PROD; no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: RUN-AS-A-READ -- IB2's and Y2's PROD runs are asked at step 1 and the promote never overlaps one. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading the CTO's rulings (msgs 11065, 11078, 11099, 11115), the issuer's payload read at the cut (1 commit, 0 merges, 3 files, none matching trade) and this order; the lens: a PROD tip that moved since the cut (it was facddeb687b8 at the cut), a builder that merges a second branch, a promote that passes typecheck and fails the vite build, a promote that overlaps another seat's PROD run or promote. The order requires the exact base, head and counts, a PROMOTE-LIST naming ONE branch, and the gates at GO. NOT seen (blind): the vite build and the live page after the push, until steps 3 and 6; denominator: 1 branch, 1 commit, 3 files.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> round 20 AMENDMENT 4: the page half of cell `R20-lm-7` (the cell itself is `TCKT_VNEXT.TO-R20-LM7`, drained at `99267e3a254`).
<owned_cells>R20-lm-7</owned_cells>
</decomp_ref>

  <objective>
    Land ONE branch on portal DEV by the approved route and promote it to PROD through /prod-deploy's chosen-set release, and nothing else: `cand/dell2/pkg-null-commentary`, head `e83292d07ba3a2aa218895a3276c28cd25110ff7`, ONE commit cut from `origin/PROD` `facddeb687b8ec44a6ec18f90d3784ae138e8171` (row dell2-20261019T235854Z-6473, APPROVED by the CTO, class opal-internal). Verify CI; read on PROD that the deploy ran and that PROD equals the branch; report once to 2.0.0_SA_COO~V2 with the run id (cc 1.0.0_SA_CTO~DELL2). The branch only ACCEPTS and SHOWS a null pair, so it is safe to ship before the packager ever sends one (CTO msg 11099); the packager half ships later and is not yours.
  </objective>

  <context>
    WHY: IRPT_ANLREQ v0.24 FWD-1 ACCEPT: "a commentary failure never withholds the other three". The ticket service already admits `pdf_ref` and `commentary_ref` null together (LIVE 00:22Z, `REL2-OK`, TO-R20-REL2). The page must read a null commentary as "Commentary not available" (a plain line: no Open control, no alert) and the other three files still open. The branch is the one commit `e83292d0` of worker 0.9.0_WK_TCKT_VNEXT~53 (cell R20-lm-7 Part B, order TCKT_VNEXT.TO-R20-LM7), cherry-picked onto the PROD head and pushed as `cand/dell2/pkg-null-commentary`. MEASURED by the issuer (2026-10-20 ~00:50Z, portal fetch): `git rev-parse origin/PROD` = facddeb687b8ec44a6ec18f90d3784ae138e8171; `git rev-parse origin/cand/dell2/pkg-null-commentary` = e83292d07ba3a2aa218895a3276c28cd25110ff7; one commit, 0 merges, 3 files (`src/api/endpoints/tickets.ts`, `src/pages/TicketCenter/AnalysisRequestParts.tsx`, `src/pages/TicketCenter/__tests__/package-commentary-null.test.tsx`); candidate gates in a scratch worktree: `bun test ./src/pages/TicketCenter` 235 pass 0 fail, `tsc -b` clean. NOT run by the issuer here: the vite build; anything on DEV or PROD after the push. The PROD tip may move before your GO: you re-check. Your inbox watcher has missed GOs before: run `check-inbox` first.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~V2 and wait.
    1. Run `check-inbox`. Open the NEVER-2 ledger tckt-portal-pkgnull-20261020 (.tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote on PROD), and commit it. Read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the portal PROD branch is a STOP, EXCEPT a stale entry of your own seat whose legs are all closed with proof and whose deploy sha you MEASURE as an ancestor of origin/PROD (with a negative control): close it with `.tools/deploy_ledger.py close`, print the measurement, commit, go on. Ask 2.0.0_SA_COO~Y2 and 0.7.0_AE_CloudOps~IB2 whether a PROD promote, release or a PROD run of theirs is due or open from now until about 90 minutes later (the CTO's run 4 of IB2 is a PROD staff filing), print the answers; silence for 10 minutes reads as none. Derive the workspace root, never type a device path.
    2. Re-check the set against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD` (must read `facddeb687b8ec44a6ec18f90d3784ae138e8171`; any other value: STOP, nothing pushed, tell 2.0.0_SA_COO~V2, who re-cuts); `git rev-parse origin/cand/dell2/pkg-null-commentary` must read `e83292d07ba3a2aa218895a3276c28cd25110ff7`; `git rev-list --count origin/PROD..origin/cand/dell2/pkg-null-commentary` must print 1; merges must print 0; `git diff --name-only origin/PROD origin/cand/dell2/pkg-null-commentary | wc -l` must print 3 and the same list piped to `grep -i trade` must print nothing. Any other value: STOP. `python .tools/open-calls.py approval-status --branch cand/dell2/pkg-null-commentary` must print one APPROVAL line with state=APPROVED valid=yes.
    3. DEV by the approved route: `bash .tools/portal-merge-forward.sh cand/dell2/pkg-null-commentary --push` (it merges as a MERGE commit with the trailers Feature: and Approved-By: in an ephemeral worktree and prints a result line with merge=<sha>). A refusal is a STOP with its text. If it refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha; never an unaudited override. Print the result line and `git -C portal rev-parse origin/DEV`.
    4. Run /prod-deploy's gates on the tree the builder cuts: `bun run typecheck` 0 errors, `bun test src/pages/TicketCenter src/pages/InvestorReporting` (print the counts; a failing test is compared line by line against the same command at origin/PROD in a detached worktree: the failing lines must be the same, else STOP), and `bun run build`. Print each result. A failure: STOP.
    5. Promote with /prod-deploy's mechanics for a chosen set: `--features cand/dell2/pkg-null-commentary` and NOTHING ELSE (the PROMOTE-LIST must name exactly one branch, row dell2-20261019T235854Z-6473; any other: STOP). The main portal tree never leaves DEV; the push is from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha; never an unaudited override. Read the CI conclusion with `gh run view --json` (never `gh run watch`): success, deployed sha equal to the promoted sha, tag peeled. Print sha and run id. Then `git -C portal fetch origin`; `git diff --stat e83292d07ba3a2aa218895a3276c28cd25110ff7 origin/PROD` must print nothing OR only the promote's own merge (state which) and `git merge-base --is-ancestor e83292d07ba3a2aa218895a3276c28cd25110ff7 origin/PROD` must exit 0.
    6. Read, on PROD, that a staff caller can open the Ticket Center after the promote, with the smoke instrument your earlier promote reads used (`portal/scripts/ui-smoke.mjs`, origin the PROD site) as an Opal STAFF-class login: open the Ticket Center board, record that the board loads and an analysis-request row, if one exists, still shows its package block; screenshot and read it. State the login's class. If no sanctioned staff-class login is available, write ABSENT with the reason: do NOT mint a user, use a partner login as a stand-in or ask for a credential. Do NOT open, file, retry or edit any ticket.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_pkgnull/A_PROMOTE_PKGNULL.txt with, ONE line each, exactly: `K1 payload exactly 1 branch cand/dell2/pkg-null-commentary e83292d07b 1 commits 3 files (trade absent)`; `K2 gates typecheck 0 tests lines-equal-PROD build ok`; `K3 CI success deployed sha <12 hex> run <id> tag peeled`; `K4 PROD staff read board loaded` or `K4 PROD staff read ABSENT <reason>`. Then the DEV merge sha, the PROD sha before and after, the run id, the receipt (pages and class, in words: the Ticket Center analysis-request package block, Opal-internal, row 6473 approved by the CTO) and the screenshot path. A line that did not hold is written `<tag> FAIL <what>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~V2 (cc 1.0.0_SA_CTO~DELL2): "dell2 portal null-commentary page promoted to PROD" with the DEV merge sha, the PROD sha before and after, the run id, the time PROD went live and the four lines.
  </the_act>

  <bounds>
    One branch (1 commit): the portal DEV branch by the approved merge-forward route, then the portal PROD branch. No API, IAM, data, Lambda or Terraform act. No second branch rides; a sweep of DEV is not a promote. No PROD user is minted. No ticket is opened, filed, retried or edited. Rollback: revert the promote on PROD through /prod-deploy's own mechanics, on 2.0.0_SA_COO~V2's or 1.0.0_SA_CTO~DELL2's word only (no data is touched; the DEV merge stays and is reverted by the same word).
  </bounds>

<paths>
org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/
org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
</paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_pkgnull/TCKT_VNEXT.TO-PROMOTE-PKGNULL.ticket-page-null-commentary-to-dev-and-prod-dt.proof_of_spec.json`.
    <criterion id="PKN-AC1" cell_refs="R20-lm-7"><invocation>grep -c -E '^(K1 payload exactly 1 branch cand/dell2/pkg-null-commentary e83292d07b 1 commits 3 files \(trade absent\)|K2 gates typecheck 0 tests lines-equal-PROD build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_pkgnull/A_PROMOTE_PKGNULL.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PKN-AC2" cell_refs="R20-lm-7"><invocation>grep -c -E '^(K3 CI success deployed sha [0-9a-f]{12} run [0-9]+ tag peeled|K4 PROD staff read (board loaded|ABSENT .+))$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_pkgnull/A_PROMOTE_PKGNULL.txt</invocation><expect>^2$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a PROMOTE order to a tier-2 DT seat under the CTO's rulings (msgs 11065, 11078, 11099, 11115) on the approved row 6473, not a worker cell; the cell R20-lm-7 is the issuer's, as for TO-PROMOTE-BACKOFF.
