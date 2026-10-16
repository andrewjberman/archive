<task_order>
  <metadata>
    <id>IRPT_DASHBD.TO-PROMOTE-M33.portal-series-mirror-contract-033-dt</id>
    <issued_by>2.0.0_SA_COO~C2</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform~DELL2</issued_to>
    <date>2026-10-16</date>
    <status>pending</status>
    <project_code>IRPT_DASHBD</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is two commits on one file (`src/pages/InvestorReporting/dashboard/seriesContract.ts`, +10 -1): two optional type members and the eight-name optional list the pin test reads; type-only, the built dist is byte-identical to PROD's (measured, 88 of 88 files); no API, IAM, Lambda or data change.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; step 6 compares two builds. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no AWS act.
comp-adversary: RUN -- by reading the CTO's approval of row 6099 and msgs 9296 and 9297, the build-bytes record and the approval row against this order; the lens: a sweep that carries more than the two approved commits (the approval pins the head, so the builder refuses any other), a PROD tip that moved since the measurement, a promote that passes typecheck and fails the vite build, a "chunks identical" claim read from one build when the DT's own two builds differ (the order makes the DT measure it on its own tree), and `iv-e-124` failing in the ephemeral worktree for a path artifact (the contract is read by a workspace-relative path) mistaken for a defect. NOT seen (blind): the vite build of PROD plus the payload on the DT's tree until step 3, and anything served after the push; denominator: 2 commits, 1 file, 3 criteria lines, 0 pages changed.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md</decomp_doc> section 19, Amendment 1, cell DB-c-31: the PROD promote of the 0.3.3 page mirror.
<owned_cells>DB-c-31</owned_cells>
</decomp_ref>

  <objective>
    Promote the ONE approved branch `cand/dell2/irpt-series-mirror-contract-033` (head `831f974aa1d4b3df061af3a29337917c154eda01`, two commits, one file) from the portal repo to PROD through /prod-deploy's chosen-set release, and nothing else; verify CI; then show, from your own two builds, that the emitted bytes are identical to PROD's ("chunks identical, no visible change"); report to 2.0.0_SA_COO~C2 once. EXCLUDED: every other candidate, live origin/DEV.
  </objective>

  <context>
    Load /prod-deploy first; its steps are yours. The set is the CTO's, Opal-internal: approval row `dell2-20261016T112339Z-6099` APPROVED by 1.0.0_SA_CTO~DELL2 at the pinned head (msgs 9296 and 9297; `python .tools/open-calls.py approval-status --branch cand/dell2/irpt-series-mirror-contract-033`). The record of the byte measurement is org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~C2/prod_promote/DB_C30_BUILD_BYTES_R150.md (read it). Per the push law an Opal-internal PROD promote needs no word from Andrew; the receipt prints the page list and class: no page changed; class Opal-internal.
    WHY: the series contract moved to 0.3.3 and the page's key-list mirror (read by the pin test `iv-e-124`) must equal it. The change is type-only. After this promote PROD's mirror equals the contract.
    MEASURED by the issuer (2026-10-16 ~11:2xZ, scratch worktrees at origin/PROD 8012cd1afbaa): the two commits cherry-pick clean; `origin/PROD..HEAD` names exactly one file; `tsc -b --noEmit` rc 0; `bun test` of `iv-e-124` and the unreported-days test 9 pass (with a copy of the 0.3.3 contract beside the scratch tree); vite builds of PROD and of the candidate are byte-identical (88 of 88 dist files, chunk-set hash 8890552b43cca4fe both). NOT run by the issuer: anything on PROD after the push. The PROD tip may move before your GO: you re-check.
    NOTE on `iv-e-124`: it reads the contract by a workspace-relative path, so in an ephemeral worktree under `.runtmp` it can fail with ENOENT (a path artifact, as in the last promote); run it where the contract resolves (a copy at the path it reads, or the workspace tree) and print which you did. It must PASS on this payload against the trunk contract 0.3.3.
  </context>

  <the_act>
    GO: start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~C2 and wait.
    1. Open the NEVER-2 ledger irpt-portal-m33-20261016 (deploy-completion contract, .tools/deploy_ledger.py) naming the release and its rollback (a revert of the promote merge on PROD), and commit it. Read the CTO's msgs and the build-bytes record; derive the workspace root, never type a device path.
    2. Re-check the set against the PROD tip at GO: `git -C portal fetch origin`; print `git rev-parse origin/PROD`; print the approval-status line (it must read APPROVED, valid yes, head_sha 831f974aa1d4b3df061af3a29337917c154eda01, commits 2); in an ephemeral worktree at that tip the release must list exactly the two commits (`git log origin/PROD..HEAD`, plus the merge commit /prod-deploy makes, if any) and `git diff --stat origin/PROD..HEAD` must name exactly `src/pages/InvestorReporting/dashboard/seriesContract.ts`. Any other file or commit, or a head that differs: STOP, nothing pushed, tell 2.0.0_SA_COO~C2.
    3. Run /prod-deploy's gates on that tree: zero TypeScript errors (`bun run typecheck`), `bun test src/pages/InvestorReporting/__tests__/irpt-dashbd` and `iv-e-124` (where the contract resolves, see the note), and the vite build (`bun run build`). Then build `origin/PROD` itself the same way (a second ephemeral worktree, removed after) and compare the two `dist` trees file by file with sha256: print the file count and whether every file is byte-identical. A failed gate, or any differing file: STOP.
    4. Promote with /prod-deploy's own mechanics for a chosen set: `--features cand/dell2/irpt-series-mirror-contract-033`, the main portal tree never leaves DEV, the push from the ephemeral worktree; if GATE 5 refuses the push for your serial, hand MSTR~DELL2 the exact ref and sha and have it pushed; never an unaudited override. Declare no freeze beyond /prod-deploy's.
    5. Read the CI conclusion with `gh -R Opal-Capital/portal run list` / `run view --json` (never `gh run watch`), enumerating workflows by headSha: success, the deployed sha equal to the promoted sha, the tag peeled. Print the sha and the run id.
    6. Page check: "chunks identical, no visible change": the step-3 comparison IS the check (the dist of the promoted tree equals the dist of the previous PROD, byte for byte). Do not mint a user and do not use a client login.
    7. Write org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_m33/A_PROMOTE_M33.txt with, ONE line each, exactly: `M1 payload exactly 2 commits head 831f974aa1 (1 file)`; `M2 gates typecheck 0 tests pass build ok`; `M3 CI success deployed sha <12 hex> tag peeled`; `M4 PROD page check dist identical <N> of <N> files`. Then the PROD sha before and after, the run id, and the receipt (no page changed; Opal-internal; approved by the CTO, row 6099). A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Close the ledger (the deploy-completion record reads CLOSED), commit, tear down the ephemeral worktrees with `git worktree remove` (a recursive delete of anything you did not create needs Andrew's word), and report ONCE to 2.0.0_SA_COO~C2 (cc 1.0.0_SA_CTO~DELL2): "series mirror 0.3.3 promoted" with the sha, the run id and the four lines.
  </the_act>

  <bounds>
    Two commits, one file, the portal PROD branch. No API, IAM, data, Lambda or Terraform act. Every other candidate stays out; a sweep of DEV is not a promote. No PROD user is minted and no client login is used. Rollback: revert the promote merge on PROD through /prod-deploy's own mechanics, on 2.0.0_SA_COO~C2's word (the mirror returns to the 0.3.0 key list; no behaviour changes).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_m33/IRPT_DASHBD.TO-PROMOTE-M33.proof_of_spec.json`.
    <criterion id="PM33-AC1" cell_refs="DB-c-31">The payload is exactly the two approved commits and the gates were green.<invocation>grep -c -E '^(M1 payload exactly 2 commits head 831f974aa1 \(1 file\)|M2 gates typecheck 0 tests pass build ok)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_m33/A_PROMOTE_M33.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PM33-AC2" cell_refs="DB-c-31">CI succeeded on the promoted sha, and the dist of the promoted tree equals PROD's byte for byte.<invocation>grep -c -E '^(M3 CI success deployed sha [0-9a-f]{12} tag peeled|M4 PROD page check dist identical [0-9]+ of [0-9]+ files)$' org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_dashbd_m33/A_PROMOTE_M33.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="PM33-AC3" cell_refs="DB-c-31">The ledger irpt-portal-m33-20261016 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-portal-m33-20261016_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
