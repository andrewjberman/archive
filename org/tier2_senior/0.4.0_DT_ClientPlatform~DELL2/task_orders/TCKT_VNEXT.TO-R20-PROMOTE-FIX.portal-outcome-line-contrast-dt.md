<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-PROMOTE-FIX.portal-outcome-line-contrast-dt</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-17</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>SERVED</risk>
<round>20</round>
<workstream>PRODFIX</workstream>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is ONE commit on ONE page: the Ticket Center's meeting outcome line takes a light ink (one class on `MeetingOutcomeLine`) and a new contrast test; two files; no API, IAM or data change. The Ticket Center is Opal-internal on a production build (`App.tsx:505` with `firmAccess.ts:148-153`, read by the CTO, ruling bc18); the CTO read the class as client-facing for the approval (partner advisors can open the Ticket Center) and Andrew's record 9063a44a4c covers it. comp-routes: RUN-AS-A-READ -- step 6 reads the page on PROD through the routes it already calls. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading the CTO's msg 10447 and the candidate against this order; the lens: a sweep that carries more than the one commit, a PROD tip that moved since the cut (the commit's parent must equal the tip at the GO, else STOP and tell the issuer for a re-cut), the Trade Request code riding in (it must be absent: the main release carried the meeting form WITHOUT it), and a promote on a re-shot that did not read 4.5:1.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20, AMENDMENT 2): the PROD promote of cell `R20-pt-5`.
<owned_cells>R20-pt-5</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer's GO amendment names the re-shot's reading. On the GO, promote ONE portal commit from `cand/dell2/tckt-outcome-line-contrast-prodfix` (head `2a64d2115f7e1a9807f01d114c666196e865ef4f`, one commit, a cherry-pick of `4ae7278d`, on PROD `4cf06588736bd1e1279b3ba249f922173e0b9ae8`) to PROD through /prod-deploy's chosen-set release, and nothing else. Verify CI; read the page on PROD and print the outcome line's contrast as a number; report to `2.0.0_SA_COO~V2` once (cc `1.0.0_SA_CTO~DELL2`).
  </objective>

  <context>
    Authority: the CTO's msg 10447: row `dell2-20261017T090236Z-70b4` APPROVED at `2a64d2115f` on Andrew's record `9063a44a4c`; "have `0.4.0_DT_ClientPlatform~DELL2` promote 70b4 as soon as TV2's re-shot (`TO-R20-RV2`) prints a pixel contrast of 4.5:1 or better on the same code at DEV `539b1ee70ba1`. A failing re-shot holds the promote." The defect it fixes: row `TCKT_VNEXT-D2-S59` (the outcome line at 1.25:1, navy on the dark board row). Load /prod-deploy first; its steps are yours. The issuer measured at the cut: `git diff --stat origin/PROD..2a64d2115f` names exactly `src/pages/TicketCenter/MeetingRequestParts.tsx` (1 line changed) and the new `src/pages/TicketCenter/__tests__/meeting-outcome-contrast.test.tsx` (150 lines); the checks `r20_pf_checks.py pf-diff` and `pf-tests` and `r20_checks.py portal-tsc` read OK on that tree (27 tests, tsc 0).
  </context>

  <go_amendment>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-17 ~09:2xZ; gate limb: none graded, a tier-2 DT order with a pipeline-override; no placeholder, no path widened). THE GO. The CTO's condition is met and he says promote now (msg 10460): TV2's re-shot `TO-R20-RV2` read `RUN-OK (reshot)` with 10.10:1 from its saved PNG on DEV `539b1ee70ba1` (ledger `tckt-vnext-r20-rv2-20261017` CLOSED 09:15:37Z, the filer row ABSENT), and the issuer measured 10.10:1 from the same file independently (strongest text pixel rgb(209,212,217) on the row background rgb(25,38,67)). Read at the GO (09:2xZ): `origin/PROD` is still `4cf06588736bd1e1279b3ba249f922173e0b9ae8`; the branch head is `2a64d2115f7e1a9807f01d114c666196e865ef4f` (ls-remote read), one commit whose parent is that tip; row `dell2-20261017T090236Z-70b4` reads APPROVED (`approval-status`). Run the act below from step 1. FIRST run `check-inbox` (a seat's watcher missed a GO earlier today, row `TCKT_VNEXT-D2-S58`). When the CI run id exists, send it to `1.0.0_SA_CTO~DELL2` (he asked for it) as well as in your final report to me.
  </go_amendment>

  <the_act>
    STAGED (superseded by AMENDMENT 1 above: the GO is given). On the GO: start at step 1 and go on only while each step reads green; otherwise tell `2.0.0_SA_COO~V2` and wait.
    1. Open the NEVER-2 ledger `tckt-vnext-r20-prodfix-20261017` (deploy-completion contract, `.tools/deploy_ledger.py`) naming the release and its rollback (a revert of the promote merge on PROD), and commit it. Derive the workspace root, never type a device path.
    2. Re-check against the PROD tip at the GO: `git -C <portal> fetch origin`; print `git rev-parse origin/PROD`; if it is NOT `4cf06588736bd1e1279b3ba249f922173e0b9ae8` (or a descendant on which the commit still applies as a one-commit, two-file diff), STOP and tell the issuer for a re-cut. In an ephemeral worktree at that tip merge ONLY the branch; `git log origin/PROD..HEAD` lists exactly `2a64d211` (plus the merge commits /prod-deploy makes); `git diff --stat origin/PROD..HEAD` names exactly the two files; `TradeFormOpen` and `trade-form-upload` appear nowhere in the diff.
    3. /prod-deploy's gates on that tree: zero TypeScript errors, `bun test src/pages/TicketCenter/__tests__/meeting-outcome-contrast.test.tsx src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx src/pages/TicketCenter/__tests__/meeting-request.test.tsx`, and the vite build. Print each result. A failure: STOP.
    4. Promote with /prod-deploy's own mechanics for a chosen set: `--features cand/dell2/tckt-outcome-line-contrast-prodfix`; the main portal tree never leaves DEV; the push from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand `0.0.0_AB_MSTR~DELL2` the exact ref and sha and have it pushed; never an unaudited override. The receipt names the page and its class in words (the Ticket Center: client-facing as the CTO reads it, under Andrew's record `9063a44a4c`).
    5. Read the CI conclusion with `gh run view --json` (never `gh run watch`): success, the deployed sha equal to the promoted sha, the tag peeled. Print the sha and the run id.
    6. Read the page on PROD with the smoke instrument your earlier promote reads used (`portal/scripts/ui-smoke.mjs`, origin the PROD site) as an Opal STAFF-class login: open the Ticket Center, find the ticket `TCK-20261017-da2a1987` (a completed meeting ticket, filed by a synthetic filer; its row is visible to a staff login), SCREENSHOT it, READ it, and compute the contrast of the outcome line from your own saved PNG as a NUMBER (the line's strongest text pixel against the row background, WCAG relative luminance, the same method as the issuer's: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/` has no script for it; state your method in a line). Record the login's class. Trade Request must NOT be in the New Ticket type list on PROD (list the options).
    7. Write `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_vnext_r20_prodfix/A_PROMOTE_PRODFIX.txt` with, ONE line each, exactly: `K1 payload exactly 1 commit 2a64d211 (2 files, Trade Request code absent)`; `K2 gates typecheck 0 tests pass build ok`; `K3 CI success deployed sha <12 hex> tag peeled`; `K4 PROD Ticket Center read outcome line contrast <n.nn>:1 type list without Trade Request` or `K4 PROD Ticket Center read ABSENT <reason>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `wk-provision` or `git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to `2.0.0_SA_COO~V2` (cc `1.0.0_SA_CTO~DELL2`): "outcome-line fix promoted" with the sha, the run id, the four lines and the contrast number.
  </the_act>

  <bounds>
    One commit, two files, one page, the portal PROD branch. No API, IAM, data, Lambda or Terraform act. No Trade Request code. No PROD user is minted. Rollback: revert the promote merge on PROD through /prod-deploy's own mechanics (`git revert -m 1`), on `2.0.0_SA_COO~V2`'s or the CTO's word only.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_vnext_r20_prodfix/TCKT_VNEXT.TO-R20-PROMOTE-FIX.portal-outcome-line-contrast-dt.proof_of_spec.json`.
    <criterion id="R20PFX-AC1" cell_refs="R20-pt-5">The payload is exactly the one commit and the gates were green.<invocation>grep -c -E '^(K1 payload exactly 1 commit 2a64d211 \(2 files, Trade Request code absent\)|K2 gates typecheck 0 tests pass build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_vnext_r20_prodfix/A_PROMOTE_PRODFIX.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="R20PFX-AC2" cell_refs="R20-pt-5">CI succeeded on the promoted sha, and the PROD read is recorded with its contrast number (read, or honestly ABSENT).<invocation>grep -c -E '^(K3 CI success deployed sha [0-9a-f]{12} tag peeled|K4 PROD Ticket Center read (outcome line contrast [0-9]+\.[0-9]+:1 type list without Trade Request|ABSENT .+))$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/tckt_vnext_r20_prodfix/A_PROMOTE_PRODFIX.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="R20PFX-AC3" cell_refs="R20-pt-5">The ledger tckt-vnext-r20-prodfix-20261017 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*tckt-vnext-r20-prodfix-20261017_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a PROMOTE order to a tier-2 DT seat on the CTO's approval by sha (row 70b4) under Andrew's record 9063a44a4c, not a worker cell; the cell R20-pt-5 is the issuer's, as for the Y2 promote orders.
