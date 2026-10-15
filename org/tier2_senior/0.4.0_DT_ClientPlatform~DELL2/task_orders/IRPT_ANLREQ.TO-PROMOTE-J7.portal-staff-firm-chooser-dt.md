<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-PROMOTE-J7.portal-staff-firm-chooser-dt</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is one commit on one page: the Ticket Center's New Analysis Request form for an Opal STAFF caller gains its Firm chooser (the served Global list) and loses the sentence 'Opal staff open requests from the queue rather than file them, so this form cannot be submitted from here'; five files (AnalysisRequestParts.tsx, TicketCenter.tsx, three tests); no API, IAM or data change.
comp-routes: RUN-AS-A-READ -- step 6 reads the staff form on PROD through the served routes it already calls (directory/resolve, analysis/comparisons); no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading the CTO's rulings (msgs 8332, 8343), the chosen-set record and rows S118 and S119 against this order; the lens: a sweep that carries more than J7, c8c3 riding in (the live intake Lambda refuses commentary_requested until IB-pr-456 applies, so it would break every PROD filing), a PROD tip that moved since the cherry-pick check, a promote that passes typecheck and fails the vite build, a read of the staff form that is really a partner login. The order requires an exact payload of one commit, the gates re-run at GO, and a staff-class read stated as such or stated ABSENT. NOT seen (blind): the vite build of PROD plus J7 and the live staff form after the push, until steps 3 and 6; denominator: 1 commit, 5 files, 4 criteria lines, 1 page.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZZ10: the PROD promote of the staff firm chooser (J7).
<owned_cells>AR-y-349</owned_cells>
</decomp_ref>

  <objective>
    Promote ONE portal commit, J7 (`cand/dell2/anlreq-internal-filer-chooses-firm`, commit 6f4e5f671f09), from DEV to PROD through /prod-deploy's chosen-set release, and nothing else; verify CI; then read on PROD that an Opal staff caller sees the firms and the catalogue; report to 2.0.0_SA_COO~Y2 once. EXCLUDED: `cand/dell2/anlreq-commentary-always-requested` (c8c3, commit 406345bce1).
  </objective>

  <context>
    Load /prod-deploy first; its steps are yours. The set is accepted by the CTO (msgs 8332 and 8343): the record is org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/prod_promote/J7_CHOSEN_SET_20261015.md (commit 2982fd8c55). Authority to push: the CTO's msg 8332 (the Ticket Center is Opal-internal, ruling 2402 @a69c390948; Andrew approved J7 as open call 1f3e; no further word is needed). The page list and class go in the receipt as /prod-deploy asks: Ticket Center (analysis request filing, staff caller), Opal-internal per the ruling; the approval row 1f3e lists client-facing: print both words, then ship, since the CTO and Andrew's approval cover it.
    WHY: Andrew opened the PROD Ticket Center as staff and saw 'The Opal model list is not loaded', no tickers and 'Your firms are still loading' (rows IRPT_ANLREQ-D2-S118 and S119): origin/PROD has the staff-not-filing sentence and no staff firm chooser; origin/DEV has the chooser (source read at both refs; the record is org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~150/r41/STAFF_FIRMS_CATALOGUE_READ.json).
    MEASURED by the issuer (2026-10-15 ~14:4xZ, scratch worktree at origin/PROD c3b21a40e29f): J7 is ONE commit on a base already in PROD, an ancestor of origin/DEV; its cherry-pick applies with no conflict; `tsc -b --noEmit` rc 0; `bun test src/pages/TicketCenter` 121 pass, 0 fail (23 files). NOT run by the issuer: the vite build; anything on PROD after the push. The PROD tip may move before your GO: you re-check.
    The other approved DEV candidates (8500 held-submit words, 7b45 advisory fee, fde0 model order, 7773 partner-firm stack) are NOT dependencies and are NOT in the set.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Open the NEVER-2 ledger irpt-portal-j7-20261015 (deploy-completion contract, .tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote merge on PROD), and commit it. Read the CTO's msgs and this order's chosen-set record; derive the workspace root, never type a device path.
    2. Re-check the set against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD`; in an ephemeral worktree at that tip, merge or cherry-pick ONLY `6f4e5f671f09`; `git log origin/PROD..HEAD` must list exactly that one commit (plus the merge commit /prod-deploy makes, if any); `git diff --stat origin/PROD..HEAD` must name exactly the five files above. Any other file or commit (c8c3's `406345bce1` above all): STOP, nothing pushed, tell 2.0.0_SA_COO~Y2.
    3. Run /prod-deploy's gates on that tree: zero TypeScript errors (`bun run typecheck`), `bun test src/pages/TicketCenter`, and the vite build (`bun run build`, as /prod-deploy's own step states it). Print each result. A failure: STOP.
    4. Promote with /prod-deploy's own mechanics for a chosen set: `--features cand/dell2/anlreq-internal-filer-chooses-firm`, the main portal tree never leaves DEV, the push from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha and have it pushed; never an unaudited override. Declare no freeze beyond /prod-deploy's.
    5. Read the CI conclusion with `gh run view --json` (never `gh run watch`): success, the deployed sha equal to the promoted sha, the tag peeled. Print the sha and the run id.
    6. Read, on PROD, that a staff caller sees the firms and the catalogue: use the smoke instrument your earlier promote reads used (`portal/scripts/ui-smoke.mjs`, origin the PROD site) as an Opal STAFF-class login, open the Ticket Center, New Analysis Request, and record whether the Firm chooser lists firms (not 'Your firms are still loading') and, after a firm is chosen, whether 'The Opal model list is not loaded' is gone and the model list and tickers appear; screenshot and read it. State the login's class in the record. If no sanctioned staff-class login is available to you, write the line ABSENT with the reason: do NOT mint a user, do NOT use a partner login as a stand-in, and do NOT ask for a credential.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_j7/A_PROMOTE_J7.txt with, ONE line each, exactly: `J1 payload exactly 1 commit 6f4e5f671f09 (c8c3 absent)`; `J2 gates typecheck 0 tests pass build ok`; `J3 CI success deployed sha <12 hex> tag peeled`; `J4 PROD staff read firms and catalogue loaded` or `J4 PROD staff read ABSENT <reason>`. Then the PROD sha before and after, the run id, the receipt (pages and class) and the screenshot path. A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `wk-provision`/`git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2): "J7 promoted" with the sha, the run id and the four lines.
  </the_act>

  <bounds>
    One commit, one page, the portal PROD branch. No API, IAM, data, Lambda or Terraform act. c8c3 and every other candidate stay out; a sweep of DEV is not a promote. No PROD user is minted. Rollback: revert the promote merge on PROD through /prod-deploy's own mechanics, on 2.0.0_SA_COO~Y2's word (the page returns to the staff-not-filing sentence; no data is touched).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_j7/IRPT_ANLREQ.TO-PROMOTE-J7.portal-staff-firm-chooser-dt.proof_of_spec.json`.
    <criterion id="PJ7-AC1" cell_refs="AR-y-349">The payload is exactly the one commit and the gates were green.<invocation>grep -c -E '^(J1 payload exactly 1 commit 6f4e5f671f09 \(c8c3 absent\)|J2 gates typecheck 0 tests pass build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_j7/A_PROMOTE_J7.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PJ7-AC2" cell_refs="AR-y-349">CI succeeded on the promoted sha, and the staff read on PROD is recorded (loaded, or honestly ABSENT).<invocation>grep -c -E '^(J3 CI success deployed sha [0-9a-f]{12} tag peeled|J4 PROD staff read (firms and catalogue loaded|ABSENT .+))$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_j7/A_PROMOTE_J7.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PJ7-AC3" cell_refs="AR-y-349">The ledger irpt-portal-j7-20261015 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-portal-j7-20261015_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a PROMOTE order to a tier-2 DT seat under the CTO's rulings (msgs 8332, 8343), not a worker cell; the cell AR-y-349 is the issuer's, as for TO-APPLY-R31R.
