<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-PROMOTE-PRICEDATE.portal-no-price-date-t1-dt</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-16</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is two commits on one CLIENT-FACING page: the Investor Reporting analysis tab's prospect composer loses its price-date input and says "Prices are the T-1 close." (AR-y-360), and the prospect header card is handed the as-of "T-1 close" (AR-y-361); three files (ProspectComposer.tsx, one new test, one re-pinned test); no API, IAM or data change. The live door has ignored a sent priceDate since release 33 (closed 2026-10-16 02:49Z), so the page no longer needs to send one.
comp-routes: RUN-AS-A-READ -- step 6 reads the page on PROD through the routes it already calls; no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading Andrew's word (call 40fa, "all recs approved", record ANDREW_DIRECT_20261016_034xZ_40FA_DBFB_APPROVED_C02C_POSTPONED_RELAY_DELL2.md @ed83fa869d) and the candidate against this order; the lens: a sweep that carries more than the two commits, another candidate riding in (the Ticket Center decision-tree chain above all: it is DEV only and waits on FWD-1 run 3), a PROD tip that moved since the scratch merge (it has moved twice since the branch was cut), a branch pushed whole instead of merged (its two-dot diff against a moved PROD reads as a revert of other work), a promote that passes typecheck and fails the vite build. The order requires an exact payload of two commits merged at the PROD tip at GO, the three-file diff, the gates re-run, and the CI read. NOT seen (blind): the vite build of the merged tree and the live page after the push, until steps 3 and 6; denominator: 2 commits, 3 files, 4 criteria lines, 1 page.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZZ31: the PROD promote of the no-price-date composer (AR-y-360) and the T-1 as-of (AR-y-361).
<owned_cells>AR-y-370</owned_cells>
</decomp_ref>

  <objective>
    Promote TWO portal commits from `cand/dell2/anlreq-no-price-date-t1-asof` (head 83993e17965a15da496fd20ca809867c1d3df2c2: `39bebae9` AR-y-360 and `83993e17` AR-y-361) to PROD through /prod-deploy's chosen-set release, and nothing else. Verify CI; then read on PROD the Investor Reporting prospect composer; report to 2.0.0_SA_COO~Y2 once. EXCLUDED: `cand/dell2/anlreq-filing-notice` (the Ticket Center decision tree; DEV only) and every other candidate.
  </objective>

  <context>
    Load /prod-deploy first; its steps are yours. This is a CLIENT-FACING page (the Investor Reporting analysis tab can be opened by a partner-firm or client login), so the promote waited on Andrew's word, and he gave it: call dell2-20261016T024308Z-40fa, "all recs approved" (~03:4xZ 2026-10-16), relayed by the CTO (msg 9000); the dell2 record is org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_034xZ_40FA_DBFB_APPROVED_C02C_POSTPONED_RELAY_DELL2.md @ed83fa869d. The condition he set in the row (r33 live) holds: the Lambda `irpt-ycharts-generate` kxOEgpbs... is live and ignores a sent priceDate (record org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r33/A_AFTER_R33.txt).
    MEASURED by the issuer (2026-10-16 ~03:5xZ, scratch worktree at origin/PROD ab2c4365): `git merge --no-ff origin/cand/dell2/anlreq-no-price-date-t1-asof` merges with no conflict; `git diff --stat origin/PROD..HEAD` names exactly three files: `src/pages/InvestorReporting/tabs/analysis/ProspectComposer.tsx`, `src/pages/InvestorReporting/tabs/analysis/tests/prospect-no-price-date.test.tsx`, `src/pages/InvestorReporting/__tests__/dsgn-irptv1/s55.component-wiring.test.tsx` (+196 -11); the two commits are the only ones `git log origin/PROD..HEAD` lists besides the merge. The candidate's own tests: 8 pass (the new file 7, the wiring test 1); typecheck rc 0 on the candidate at an earlier PROD tip. NOT run by the issuer at this tip: the vite build; anything on PROD after the push. The PROD tip moves often (it moved twice since the branch was cut): you re-check at GO and you MERGE, you do not push the branch itself.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Open the NEVER-2 ledger irpt-portal-pricedate-20261016 (deploy-completion contract, .tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote merge on PROD), and commit it. Read Andrew's record above and this order; derive the workspace root, never type a device path.
    2. Re-check the set against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD`; in an ephemeral worktree at that tip, merge ONLY `cand/dell2/anlreq-no-price-date-t1-asof` (head 83993e17965a15da496fd20ca809867c1d3df2c2); `git log origin/PROD..HEAD` must list exactly the two commits `39bebae9` and `83993e17` (plus the merge commits /prod-deploy makes); `git diff --stat origin/PROD..HEAD` must name exactly the three files above. Any other file or commit: STOP, nothing pushed, tell 2.0.0_SA_COO~Y2.
    3. Run /prod-deploy's gates on that tree: zero TypeScript errors (`bun run typecheck`), `bun test src/pages/InvestorReporting/tabs/analysis/tests/prospect-no-price-date.test.tsx src/pages/InvestorReporting/__tests__/dsgn-irptv1/s55.component-wiring.test.tsx`, and the vite build (`bun run build`, as /prod-deploy's own step states it). Print each result. A failure: STOP.
    4. Promote with /prod-deploy's own mechanics for a chosen set: `--features cand/dell2/anlreq-no-price-date-t1-asof`, the main portal tree never leaves DEV, the push from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha and have it pushed; never an unaudited override. Declare no freeze beyond /prod-deploy's. The receipt names the page and its class in words (Investor Reporting analysis tab, client-facing, approved by Andrew, call 40fa).
    5. Read the CI conclusion with `gh run view --json` (never `gh run watch`): success, the deployed sha equal to the promoted sha, the tag peeled. Print the sha and the run id.
    6. Read, on PROD, the prospect composer: use the smoke instrument your earlier promote reads used (`portal/scripts/ui-smoke.mjs`, origin the PROD site) as an Opal STAFF-class login, open Investor Reporting, the Analysis tab, the prospect composer, and record: no date input and no "price date" label on the composer, the sentence "Prices are the T-1 close." present; screenshot and read it. State the login's class in the record. If no sanctioned staff-class login is available to you, write the line ABSENT with the reason: do NOT mint a user, do NOT use a partner login as a stand-in, and do NOT ask for a credential.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_pricedate/A_PROMOTE_PRICEDATE.txt with, ONE line each, exactly: `K1 payload exactly 2 commits 39bebae9 83993e17 (3 files, decision tree absent)`; `K2 gates typecheck 0 tests pass build ok`; `K3 CI success deployed sha <12 hex> tag peeled`; `K4 PROD composer read no date input, T-1 sentence present` or `K4 PROD composer read ABSENT <reason>`. Then the PROD sha before and after, the run id, the receipt (page and class) and the screenshot path. A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `wk-provision`/`git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2): "no-price-date composer promoted" with the sha, the run id and the four lines.
  </the_act>

  <bounds>
    Two commits, three files, one page, the portal PROD branch. No API, IAM, data, Lambda or Terraform act. The decision-tree chain (`cand/dell2/anlreq-filing-notice`) and every other candidate stay out; a sweep of DEV is not a promote. No PROD user is minted. Rollback: revert the promote merge on PROD through /prod-deploy's own mechanics (`git revert -m 1`), on 2.0.0_SA_COO~Y2's or the CTO's word only (no data is touched).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_pricedate/IRPT_ANLREQ.TO-PROMOTE-PRICEDATE.portal-no-price-date-t1-dt.proof_of_spec.json`.
    <criterion id="PPD-AC1" cell_refs="AR-y-370">The payload is exactly the two commits and the gates were green.<invocation>grep -c -E '^(K1 payload exactly 2 commits 39bebae9 83993e17 \(3 files, decision tree absent\)|K2 gates typecheck 0 tests pass build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_pricedate/A_PROMOTE_PRICEDATE.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PPD-AC2" cell_refs="AR-y-370">CI succeeded on the promoted sha, and the composer read on PROD is recorded (read, or honestly ABSENT).<invocation>grep -c -E '^(K3 CI success deployed sha [0-9a-f]{12} tag peeled|K4 PROD composer read (no date input, T-1 sentence present|ABSENT .+))$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_pricedate/A_PROMOTE_PRICEDATE.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PPD-AC3" cell_refs="AR-y-370">The ledger irpt-portal-pricedate-20261016 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-portal-pricedate-20261016_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a PROMOTE order to a tier-2 DT seat on Andrew's word (call 40fa) and the CTO's relay (msg 9000), not a worker cell; the cell AR-y-370 is the issuer's, as for TO-PROMOTE-HINT.
