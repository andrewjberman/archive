<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-REVERT-C8C3.portal-commentary-requested-revert-dt</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-15</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is one revert on one page: the Ticket Center's New Analysis Request form stops sending commentary_requested true on the wire (c8c3, commit 406345bce1, merged on PROD in 45a3e18f) and the filing hint (469b, a6b83f692084) stays; files c8c3 touched: contracts/submission-request.ts, analysisRequest.ts (its region), the test analysis-commentary-always-requested.test.ts; no API, IAM or data change.
comp-routes: RUN-AS-A-READ -- step 6 reads the staff form on PROD through the served routes it already calls; no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading the CTO's ruling addendum 1 (msg 8534) and AQ2's chain-stall read (msg 8529) against this order; the lens: a revert that also removes the hint, a revert taken against the wrong parent of the merge, a PROD tip that moved since, a revert that passes typecheck and fails the vite build. The order requires the revert's first-parent choice stated, a diff of exactly c8c3's files, the hint's files untouched, and the gates re-run. NOT seen (blind): the vite build of the reverted tree and the live form after the push, until steps 3 and 6; denominator: 1 merge reverted, 3 files, 4 criteria lines, 1 page.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZZ19: the PROD revert of c8c3 alone (the hint 469b stays).
<owned_cells>AR-y-358</owned_cells>
</decomp_ref>

  <objective>
    REVERT c8c3's merge on PROD through /prod-deploy's mechanics, and nothing else: the merge commit 45a3e18f (feature cand/dell2/anlreq-commentary-always-requested into release/20261015T180116Z) is reverted so that the Ticket Center form no longer sends commentary_requested true; the filing hint (merge 9176227f, 469b) STAYS. Verify CI; read on PROD that a staff caller still sees the firms and the catalogue; report to 2.0.0_SA_COO~Y2 once.
  </objective>

  <context>
    Load /prod-deploy first; its steps are yours. The ruling is the CTO's (msg 8534, ruling org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_ANLREQ_PROD_PROMOTE_RELEASE_AFTER_FWD1_WINDOW2_20261015.md ADDENDUM 1 @31cb7b5938): you promoted the filing hint and c8c3 at 18:0xZ (PROD 33ad65ee -> 45a3e18f, your record org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_hint/A_PROMOTE_HINT.txt); AQ2's read of the FWD-1 window-2 chain (org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_READ_FWD1R2_STALL.txt, msg 8529) shows the resident's packaging step refuses (ReportRefused, then CurrentAuthorityRefused) and the commentary message went to the dead-letter queue: with c8c3 every PROD staff filing starts a chain that ends there. c8c3 re-promotes when one DEV window delivers 4 of 4 attachments. The approvals stand (469b closed approved; c8c3 closed approved). The issuer's word for this revert: given by this order (CTO msg 8534: YES).
    The PROD tip at the issuer's last read: 45a3e18f197c485eb6534f4e29d49fd5e9636c98 (a later tip is possible if another promote landed: you re-check). The merge to revert is `45a3e18f` itself when it is still the tip or an ancestor of it; its FIRST parent is the release branch carrying the hint (`9176227f`): the revert keeps the first parent's content (`git revert -m 1`), which is the tree with the hint and without c8c3.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Open the NEVER-2 ledger irpt-portal-revert-c8c3-20261015 (deploy-completion contract, .tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote merge on PROD), and commit it. Read the CTO's msgs and this order's chosen-set record; derive the workspace root, never type a device path.
    2. Re-check against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD`; confirm `45a3e18f` is the tip or an ancestor of it (`merge-base --is-ancestor`), that its first parent is `9176227f` (`git rev-parse 45a3e18f^1`), and that c8c3's commit `406345bce1` is reachable only through it. In an ephemeral worktree at the tip: `git revert -m 1 45a3e18f` (identity on the command line if the checkout has none). `git diff --stat <tip>..HEAD` must name exactly c8c3's files (`src/pages/InvestorReporting/contracts/wire/submission-request.ts` or the path c8c3 names, `src/pages/TicketCenter/analysisRequest.ts`, `src/pages/TicketCenter/__tests__/analysis-commentary-always-requested.test.ts`) and NOT touch `AnalysisRequestParts.tsx`, `TicketCenter.tsx` or `__tests__/filing-hint.test.tsx`; the filing-hint code must still be present (`grep -c filingHints src/pages/TicketCenter/analysisRequest.ts` at least 1). Any other file or a missing hint: STOP, nothing pushed, tell 2.0.0_SA_COO~Y2.
's gates on that tree: zero TypeScript errors (`bun run typecheck`), `bun test src/pages/TicketCenter`, and the vite build (`bun run build`, as /prod-deploy's own step states it). Print each result. A failure: STOP.
    4. Ship the revert with /prod-deploy's own mechanics for a chosen set (here the one revert commit): `the revert commit as a single release commit, the main portal tree never leaves DEV, the push from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha and have it pushed; never an unaudited override. Declare no freeze beyond /prod-deploy's.
    5. Read the CI conclusion with `gh run view --json` (never `gh run watch`): success, the deployed sha equal to the promoted sha, the tag peeled. Print the sha and the run id.
    6. Read, on PROD, that a staff caller still sees the firms and the catalogue after the promote: use the smoke instrument your earlier promote reads used (`portal/scripts/ui-smoke.mjs`, origin the PROD site) as an Opal STAFF-class login, open the Ticket Center, New Analysis Request, and record whether the Firm chooser lists firms (not 'Your firms are still loading') and, after a firm is chosen, whether 'The Opal model list is not loaded' is gone and the model list and tickers appear; screenshot and read it. State the login's class in the record. If no sanctioned staff-class login is available to you, write the line ABSENT with the reason: do NOT mint a user, do NOT use a partner login as a stand-in, and do NOT ask for a credential.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_revert/A_REVERT_C8C3.txt with, ONE line each, exactly: `R1 revert of 45a3e18f only (hint kept)`; `R2 gates typecheck 0 tests pass build ok`; `R3 CI success deployed sha <12 hex> tag peeled`; `R4 PROD staff read firms and catalogue loaded` or `R4 PROD staff read ABSENT <reason>`. Then the PROD sha before and after, the run id, the receipt (pages and class) and the screenshot path. A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `wk-provision`/`git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2): "c8c3 reverted" with the sha, the run id and the four lines.
  </the_act>

  <bounds>
    One revert commit, one page, the portal PROD branch. No API, IAM, data, Lambda or Terraform act; no queue message is received, redriven or deleted. The filing hint and every other commit on PROD stay. No PROD user is minted. Rollback of this revert: none planned (c8c3 re-promotes through its own order when one DEV window delivers 4 of 4 attachments).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_revert/IRPT_ANLREQ.TO-REVERT-C8C3.portal-commentary-requested-revert-dt.proof_of_spec.json`.
    <criterion id="RC8-AC1" cell_refs="AR-y-358">The revert is exactly c8c3's merge, the hint is kept and the gates were green.<invocation>grep -c -E '^(R1 revert of 45a3e18f only \(hint kept\)|R2 gates typecheck 0 tests pass build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_revert/A_REVERT_C8C3.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="RC8-AC2" cell_refs="AR-y-358">CI succeeded on the promoted sha, and the staff read on PROD is recorded (loaded, or honestly ABSENT).<invocation>grep -c -E '^(R3 CI success deployed sha [0-9a-f]{12} tag peeled|R4 PROD staff read (firms and catalogue loaded|ABSENT .+))$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_revert/A_REVERT_C8C3.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="RC8-AC3" cell_refs="AR-y-358">The ledger irpt-portal-revert-c8c3-20261015 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-portal-revert-c8c3-20261015_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a PROMOTE order to a tier-2 DT seat under the CTO's ruling (msgs 8530, 8534), not a worker cell; the cell AR-y-358 is the issuer's, as for TO-PROMOTE-HINT.
