<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-PROMOTE-HINT.portal-filing-hint-and-commentary-requested-dt</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-15</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is two commits on one page: the Ticket Center's New Analysis Request form: (1) the filing hint 469b (the upload door's own "Did you mean X?" with Use and Keep; Keep sends nothing yet) and (2) c8c3 (the submit always sends commentary_requested true on the wire); six files (AnalysisRequestParts.tsx, TicketCenter.tsx, analysisRequest.ts, contracts/submission-request.ts, two tests); no API, IAM or data change. The live intake Lambda accepted commentary_requested true on 2026-10-15 ~17:00Z (FWD-1 window 2).
comp-routes: RUN-AS-A-READ -- step 6 reads the staff form on PROD through the served routes it already calls; no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading the CTO's rulings (msgs 8332, 8459, 8519), the FWD-1 window-2 record and the two candidates against this order; the lens: a sweep that carries more than the two commits, a third candidate (above all the Keep equal-pair candidate, which waits on the door release) riding in, a PROD tip that moved since the scratch merge, a promote that passes typecheck and fails the vite build, a promote that makes every PROD filing send commentary_requested while the attachment chain is stalled. The order requires an exact payload of two commits, the gates re-run at GO, and a revert of c8c3 alone on the issuer's word. NOT seen (blind): the vite build of the combined tree and the live staff form after the push, until steps 3 and 6; denominator: 2 commits, 6 files, 4 criteria lines, 1 page.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZZ17: the PROD promote of the filing hint (469b) and the commentary-requested submit (c8c3).
<owned_cells>AR-y-356</owned_cells>
</decomp_ref>

  <objective>
    Promote TWO portal commits from their candidate branches to PROD through /prod-deploy's chosen-set release, and nothing else: `cand/dell2/anlreq-filing-hint-did-you-mean` (commit a6b83f692084b2f599d0b6142aa61c75bb735a42, the filing hint, call 469b) and `cand/dell2/anlreq-commentary-always-requested` (commit 406345bce1, c8c3, the submit always asks for the AI commentary). Verify CI; then read on PROD that a staff caller still sees the firms and the catalogue; report to 2.0.0_SA_COO~Y2 once. EXCLUDED: `cand/dell2/anlreq-filing-hint-keep-equal-pair` (the Keep that posts the equal pair; it waits on the door release) and every other candidate.
  </objective>

  <context>
    Load /prod-deploy first; its steps are yours. The release is the CTO's (msg 8519, ruling org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_ANLREQ_PROD_PROMOTE_RELEASE_AFTER_FWD1_WINDOW2_20261015.md @1fc2dfcaaa): FWD-1 window 2 (record org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_RUN_FWD1_R2.txt) filed a ticket and the live intake ACCEPTED the request with commentary_requested true (IB-pr-456's acceptance exercised); the attachments did not arrive (0 of 4), and a read of the chain is under way (TO-READ-FWD1R2). The hint is approved as call 469b (CTO msg 8459, class Opal-internal, ruling 2402 @a69c390948: the Ticket Center is staff-only); c8c3 is approved as call c8c3 (closed, approved). The receipt names the page and class in words and says plainly: a filing now reaches acceptance, and the attachments are not yet delivered.
    MEASURED by the issuer (2026-10-15 ~17:55Z, scratch worktree at origin/PROD 33ad65ee): the two commits merge with no conflict (c8c3 touches contracts/submission-request.ts, analysisRequest.ts and a test; the hint touches the three Ticket Center files and a test); `tsc -b --noEmit` rc 0; `bun test src/pages/TicketCenter` 135 pass, 0 fail (25 files); the diff against PROD is exactly six files. NOT run by the issuer: the vite build; anything on PROD after the push. The PROD tip may move before your GO: you re-check.
    THE REVERT RULE (CTO msg 8519): if the chain read shows commentary_requested causes the stall, c8c3 is reverted on PROD that turn and the hint stays. You do not decide that: on the issuer's word only, revert the c8c3 commit alone through /prod-deploy's own mechanics.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Open the NEVER-2 ledger irpt-portal-hint-c8c3-20261015 (deploy-completion contract, .tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote merge on PROD), and commit it. Read the CTO's msgs and this order's chosen-set record; derive the workspace root, never type a device path.
    2. Re-check the set against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD`; in an ephemeral worktree at that tip, merge ONLY `cand/dell2/anlreq-filing-hint-did-you-mean` and `cand/dell2/anlreq-commentary-always-requested` (each one commit: `a6b83f692084` and `406345bce1`); `git log origin/PROD..HEAD` must list exactly those two commits (plus the merge commits /prod-deploy makes); `git diff --stat origin/PROD..HEAD` must name exactly six files: `src/pages/InvestorReporting/contracts/wire/submission-request.ts` (or the path the c8c3 commit names), `src/pages/TicketCenter/AnalysisRequestParts.tsx`, `TicketCenter.tsx`, `analysisRequest.ts`, `__tests__/analysis-commentary-always-requested.test.ts` and `__tests__/filing-hint.test.tsx`. Any other file or commit (the Keep equal-pair candidate above all): STOP, nothing pushed, tell 2.0.0_SA_COO~Y2.
    3. Run /prod-deploy's gates on that tree: zero TypeScript errors (`bun run typecheck`), `bun test src/pages/TicketCenter`, and the vite build (`bun run build`, as /prod-deploy's own step states it). Print each result. A failure: STOP.
    4. Promote with /prod-deploy's own mechanics for a chosen set: `--features cand/dell2/anlreq-filing-hint-did-you-mean,cand/dell2/anlreq-commentary-always-requested` (the form /prod-deploy's own step states for a list), the main portal tree never leaves DEV, the push from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha and have it pushed; never an unaudited override. Declare no freeze beyond /prod-deploy's.
    5. Read the CI conclusion with `gh run view --json` (never `gh run watch`): success, the deployed sha equal to the promoted sha, the tag peeled. Print the sha and the run id.
    6. Read, on PROD, that a staff caller still sees the firms and the catalogue after the promote: use the smoke instrument your earlier promote reads used (`portal/scripts/ui-smoke.mjs`, origin the PROD site) as an Opal STAFF-class login, open the Ticket Center, New Analysis Request, and record whether the Firm chooser lists firms (not 'Your firms are still loading') and, after a firm is chosen, whether 'The Opal model list is not loaded' is gone and the model list and tickers appear; screenshot and read it. State the login's class in the record. If no sanctioned staff-class login is available to you, write the line ABSENT with the reason: do NOT mint a user, do NOT use a partner login as a stand-in, and do NOT ask for a credential.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_hint/A_PROMOTE_HINT.txt with, ONE line each, exactly: `K1 payload exactly 2 commits a6b83f692084 406345bce1 (keep-equal-pair absent)`; `K2 gates typecheck 0 tests pass build ok`; `K3 CI success deployed sha <12 hex> tag peeled`; `K4 PROD staff read firms and catalogue loaded` or `K4 PROD staff read ABSENT <reason>`. Then the PROD sha before and after, the run id, the receipt (pages and class) and the screenshot path. A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `wk-provision`/`git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~Y2 (cc 1.0.0_SA_CTO~DELL2): "hint and c8c3 promoted" with the sha, the run id and the four lines.
  </the_act>

  <bounds>
    Two commits, one page, the portal PROD branch. No API, IAM, data, Lambda or Terraform act. The Keep equal-pair candidate and every other candidate stay out; a sweep of DEV is not a promote. No PROD user is minted. Rollback: revert the promote merge on PROD (both commits), or c8c3 alone, through /prod-deploy's own mechanics, on 2.0.0_SA_COO~Y2's word only (no data is touched).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_hint/IRPT_ANLREQ.TO-PROMOTE-HINT.portal-filing-hint-and-commentary-requested-dt.proof_of_spec.json`.
    <criterion id="PHC-AC1" cell_refs="AR-y-356">The payload is exactly the two commits and the gates were green.<invocation>grep -c -E '^(K1 payload exactly 2 commits a6b83f692084 406345bce1 \(keep-equal-pair absent\)|K2 gates typecheck 0 tests pass build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_hint/A_PROMOTE_HINT.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PHC-AC2" cell_refs="AR-y-356">CI succeeded on the promoted sha, and the staff read on PROD is recorded (loaded, or honestly ABSENT).<invocation>grep -c -E '^(K3 CI success deployed sha [0-9a-f]{12} tag peeled|K4 PROD staff read (firms and catalogue loaded|ABSENT .+))$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_hint/A_PROMOTE_HINT.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PHC-AC3" cell_refs="AR-y-356">The ledger irpt-portal-hint-c8c3-20261015 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-portal-hint-c8c3-20261015_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a PROMOTE order to a tier-2 DT seat under the CTO's rulings (msgs 8459, 8519), not a worker cell; the cell AR-y-356 is the issuer's, as for TO-PROMOTE-J7.
