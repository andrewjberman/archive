<task_order>
  <metadata>
    <id>IRPT_DASHBD.TO-PROMOTE-UD.portal-unreported-days-sentence-dt</id>
    <issued_by>2.0.0_SA_COO~C2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-16</date>
    <status>pending</status>
    <project_code>IRPT_DASHBD</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<round>148</round>
<workstream>B-CW</workstream>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is four commits (six files) on one page: the Investor Reporting dashboard's Performance tab gains one note for a series that carries unreported trading days (none served today), and the series mirror accepts two new optional names and a null income; no API, IAM, Lambda or data change.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; step 6 reads the built bundle the site serves. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading Andrew's word (ANDREW_DIRECT_20261016_062xZ_APPROVE_92C0), the CTO's msgs 9101 and 9125, the approval row 92c0 and the chosen-set record against this order; the lens: a sweep that carries more than the approved four commits (the approval pins the head, so any other head is refused by the builder), a PROD tip that moved since the payload check, a promote that passes typecheck and fails the vite build, `iv-e-124` red against the trunk contract on this payload (named, by design, to cell DB-c-26) mistaken for a defect in this promote, and a page read claimed as live when no account carries the field. The order requires the exact payload, the gates re-run at GO, the test gate named, and a page read stated as FIXTURE-ONLY. NOT seen (blind): the vite build of PROD plus the payload and the served bundle after the push, until steps 3 and 6; denominator: 4 commits, 6 files, 3 criteria lines, 1 page.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md</decomp_doc> section 17, Amendment 1, cell DB-c-28: the PROD promote of the unreported-days sentence.
<owned_cells>DB-c-28</owned_cells>
</decomp_ref>

  <objective>
    Promote the ONE approved branch `cand/dell2/irpt-fwd10-unreported-days-sentence` (head `9c24c7bdac5775d18a66460748adbb694d2b1f98`, four commits) from the portal repo to PROD through /prod-deploy's chosen-set release, and nothing else; verify CI; then read, on the served bundle, that the sentence text is shipped; report to 2.0.0_SA_COO~C2 once. EXCLUDED: the mirror cell DB-c-26 (not in the approved head), every other candidate, live origin/DEV.
  </objective>

  <context>
    Load /prod-deploy first; its steps are yours. The set is Andrew's and the CTO's: the record is org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~C2/prod_promote/UNREPORTED_DAYS_CHOSEN_SET_20261016.md (read it, it names two facts you must read before GO). Authority to push: Andrew's word "approve 92c0" (org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_062xZ_APPROVE_92C0_DELETE_BOTH_SCRATCH_FOLDERS.md) as classed by the CTO's msg 9125: the page is CLIENT-FACING and approved for PROD. Print the page and class in the receipt: Investor Reporting dashboard, Performance tab; client-facing; approved by Andrew, row dell2-20261016T055011Z-92c0.
    WHY: FWD-10 of IRPT_DASHBD: a person can always tell which trading days the source did not report. The Cottonwood series carrying the field are published (939 accounts) but no live account shows the sentence until the publish pair's Act 4 and the daily schedule land (CTO msg 9022), so the read in step 6 is FIXTURE-ONLY and is labelled so.
    MEASURED by the issuer (2026-10-16 ~05:5xZ, scratch worktree at origin/PROD a062c56e53b1): the four commits are a clean cherry-pick set; the two-dot diff is exactly the six files in the record; `tsc -b --noEmit` rc 0; the new test and `iv-e-124` 9 pass (against contract 0.3.0 then). NOT run by the issuer: the vite build; anything on PROD after the push. The PROD tip may move before your GO: you re-check.
    KNOWN RED, NOT YOURS: on this payload `iv-e-124` (`__tests__/dsgn-irptv1/iv-e-124.series-contract.test.ts`) reads the trunk contract, now 0.3.1 with six optional names, against a mirror of five. The sixth name is cell DB-c-26 (a separate candidate to follow); do not add it, do not edit the test, do not skip it silently: your test gate is `bun test src/pages/InvestorReporting/__tests__/irpt-dashbd` (the new test, 8 tests), and you print `iv-e-124`'s result as a labelled known-red line.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~C2 and wait.
    1. Open the NEVER-2 ledger irpt-portal-ud-20261016 (deploy-completion contract, .tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote merge on PROD), and commit it. Read Andrew's record, the CTO's msgs 9101 and 9125 and this order's chosen-set record; derive the workspace root, never type a device path.
    2. Re-check the set against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD`; print `python .tools/open-calls.py approval-status --branch cand/dell2/irpt-fwd10-unreported-days-sentence` (it must read APPROVED, valid yes, head_sha 9c24c7bdac5775d18a66460748adbb694d2b1f98, commits 4); in an ephemeral worktree at that tip the release must list exactly the four commits (`git log origin/PROD..HEAD`, plus the merge commit /prod-deploy makes, if any) and `git diff --stat origin/PROD..HEAD` must name exactly the six files in the record. Any other file or commit, or a head that differs: STOP, nothing pushed, tell 2.0.0_SA_COO~C2.
    3. Run /prod-deploy's gates on that tree: zero TypeScript errors (`bun run typecheck`), `bun test src/pages/InvestorReporting/__tests__/irpt-dashbd`, and the vite build (`bun run build`, as /prod-deploy's own step states it). Print each result, and the labelled known-red `iv-e-124` line. A failure of the three gates: STOP.
    4. Promote with /prod-deploy's own mechanics for a chosen set: `--features cand/dell2/irpt-fwd10-unreported-days-sentence`, the main portal tree never leaves DEV, the push from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha and have it pushed; never an unaudited override. Declare no freeze beyond /prod-deploy's.
    5. Read the CI conclusion with `gh -R Opal-Capital/portal run list` / `run view --json` (never `gh run watch`), enumerating workflows by headSha: success, the deployed sha equal to the promoted sha, the tag peeled. Print the sha and the run id.
    6. Read the page FIXTURE-ONLY: the served site's built JavaScript contains the sentence text `not reported by the source` (fetch the served bundle the site's index names and search it; print the count of matches in the one bundle file that holds it, never a client value). State that no live account carries `unreported_trading_days` yet, so no account's screen shows the sentence. Do NOT mint a user, do NOT use a client login, and do NOT ask for a credential.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_ud/A_PROMOTE_UD.txt with, ONE line each, exactly: `U1 payload exactly 4 commits head 9c24c7bdac (DB-c-26 absent)`; `U2 gates typecheck 0 tests pass build ok`; `U3 CI success deployed sha <12 hex> tag peeled`; `U4 PROD page read FIXTURE-ONLY bundle carries the sentence text`. Then the PROD sha before and after, the run id, the receipt (page and class), and the labelled known-red line for `iv-e-124`. A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktree with `git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~C2 (cc 1.0.0_SA_CTO~DELL2): "unreported-days sentence promoted" with the sha, the run id and the four lines.
  </the_act>

  <bounds>
    Four commits, one page, the portal PROD branch. No API, IAM, data, Lambda or Terraform act. The mirror cell DB-c-26 and every other candidate stay out; a sweep of DEV is not a promote. No PROD user is minted and no client login is used. Rollback: revert the promote merge on PROD through /prod-deploy's own mechanics, on 2.0.0_SA_COO~C2's word (the Performance tab returns to the round 146 note set; no data is touched).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_ud/IRPT_DASHBD.TO-PROMOTE-UD.proof_of_spec.json`.
    <criterion id="PUD-AC1" cell_refs="DB-c-28">The payload is exactly the four approved commits and the gates were green.<invocation>grep -c -E '^(U1 payload exactly 4 commits head 9c24c7bdac \(DB-c-26 absent\)|U2 gates typecheck 0 tests pass build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_ud/A_PROMOTE_UD.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PUD-AC2" cell_refs="DB-c-28">CI succeeded on the promoted sha, and the fixture-only read of the served bundle is recorded.<invocation>grep -c -E '^(U3 CI success deployed sha [0-9a-f]{12} tag peeled|U4 PROD page read FIXTURE-ONLY bundle carries the sentence text)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_ud/A_PROMOTE_UD.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PUD-AC3" cell_refs="DB-c-28">The ledger irpt-portal-ud-20261016 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-portal-ud-20261016_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
