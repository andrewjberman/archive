<task_order>
  <metadata>
    <id>SSCN_DIVDEF.006</id>
    <slug>dt-portal-dev-to-prod-push</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>CLEARED 2026-05-20T17:5xZ. Andrew DEV smoke APPROVED ("Yes it works"). CTO 1.0.0_SA_CTO gated the candidate as the 8-commit cherry-pick set (added cfdf9a5c, the .011 smoke-runner counterpart -- consistency with 2254437c already in set; PROD a clean SSCN superset of DEV) + cherry-pick mechanism. GO fired by COO. Two CTO gate conditions are folded into the scope below as Phase-0 preconditions: (1) cfdf9a5c must be on origin/DEV before the pick (DT pushes it + syncs CLOUD gitlink first); (2) DT runs `git show --stat cfdf9a5c` at pick time and confirms the diff is confined to portal `.frontend-dev/**` with zero `portal/src/**` touch -- halt + re-surface to COO if any src path appears.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- the final ship step; closes the SSCN_DIVDEF project lifecycle. Andrew-direct "focus SSCN today" 2026-05-20.</priority>
    <sla>~15-30min DT wall once the GO fires (+ a few min for the Phase-0 cfdf9a5c push). Cherry-pick 8 commits -> portal PROD -> local build verify -> git push origin PROD -> GHA deploy.yml auto-deploy -> opalinvest.dev smoke.</sla>
    <deadline>None hard -- ship at DT pace post-gate.</deadline>
  </metadata>

  <rewrite_note>
    This TO was originally authored 2026-05-19 by 2.0.0_SA_COO~B for the pre-v0.4 PROD push (.007/.008 era, blanket ff-merge, the old 4-group-strip UX). It is REWRITTEN base-lane 2026-05-20 by 2.0.0_SA_COO to the actual current bundle: SSCN_DIVDEF went through PRD v0.4 (layout revert), v0.5 (Presets dropdown), v0.6 (factor-grouping correction) + a smoke-bug fix (.011 Equal Weight). The PROD push is now an 8-commit SSCN-only CHERRY-PICK (not an ff-merge -- the SSCN commits are interleaved with 12 non-SSCN commits on origin/DEV; cfdf9a5c added on the CTO .006 gate). RAVC2 routing updated to the base C-suite.
  </rewrite_note>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md -- PRD v0.1 through v0.6 (1.0.0_SA_CTO / ~B). The shipped state is the cumulative v0.6 result.</prd>
    <approval>Andrew DEV smoke APPROVED 2026-05-20 -- verified on http://localhost:5175/security-scanner @ portal DEV d71ac15b: DIVZ preset on load, Presets dropdown, reverted pre-5/18 layout, 18 corrected factor groups, Equal Weight fix. "Yes it works."</approval>
    <dt_preflight>DT 0.3.0 read-only pre-flight 2026-05-20: origin/PROD..origin/DEV = 18 commits; the SSCN commits are INTERLEAVED with 12 non-SSCN (ADVI/MDPF/TRSB) -> a blanket DEV->PROD ff-merge would wrongly ship non-SSCN work to PROD; cherry-pick is structurally required. comp-routes trace getUniverseScanner + comp-cache collisions (scanner) PASS. Deploy mechanism: portal deploy.yml fires on push to the PROD branch -> bun build -> aws s3 sync dist/ s3://opalinvest-portal -> CloudFront EVTSA9VEHNZVH create-invalidation -> https://opalinvest.dev.</dt_preflight>
  </references>

  <the_8_sscn_commits>
    The SSCN commit set to cherry-pick from origin/DEV onto portal PROD, in DEV commit order:
    - 45ea7210 -- SSCN_DIVDEF.001 (DIVZ default preset)
    - 2254437c -- SSCN_DIVDEF.001 (smoke constitution; auxiliary)
    - b302f5cf -- SSCN_DIVDEF.005 (universe set 6->5 US-equity)
    - a844f0dd -- SSCN_DIVDEF.007 (surgical pre-5/18 layout revert)
    - b05388dc -- SSCN_DIVDEF.008 (Presets dropdown)
    - 7ef0f4a6 -- SSCN_DIVDEF.010 (Factor Bank "Group" relabel + color polish)
    - d71ac15b -- SSCN_DIVDEF.011 (Equal Weight remainder-spread fix)
    - cfdf9a5c -- SSCN_DIVDEF.011 (smoke runner Scenario 6; test-infra, .frontend-dev/** only)
    cfdf9a5c was added to the set on the CTO .006 gate 2026-05-20: it is the .011 smoke-runner counterpart of d71ac15b; including it keeps PROD's SSCN scope a clean superset of DEV (zero residual SSCN drift on a future promotion), consistent with 2254437c (a smoke constitution already in the set). cfdf9a5c is test-infra (verified diff: 1 file, `.frontend-dev/runners/sscn_divdef_001_runner.mjs`, +61) -- it does not change app behavior or the deployed bundle, so Andrew's DEV smoke at d71ac15b stands. cfdf9a5c is committed local-only as of TO dispatch -- DT pushes it to origin/DEV in Phase 0 before the pick.
    NOTE: the scanner Lambda (security-scanner-v1.1.3, registry regen + 18-group fix) is already on PROD via Terraform -- the Lambda runs against a single PROD AWS account, no DEV/PROD data bifurcation. This TO is portal-branch-only. The corrected 18-group data is already live; this push aligns the portal UI with it.
  </the_8_sscn_commits>

  <context>
    Final PROD ship for SSCN_DIVDEF. Cherry-pick the 8 SSCN commits from origin/DEV onto portal PROD. Post-push the opalinvest.dev Security Scanner becomes:
    - Default load: Russell 1000 universe + 13-factor DIVZ preset, applied via an explicit "Presets:" dropdown showing "DIVZ -- Dividend".
    - Layout: pre-5/18 frozen layout -- NO ranking-method control, NO 4-group rollup strip (both were unauthorized TO-1 additions, reverted by .007); weight input step=1.
    - Universe dropdown: 5 US-equity options (sp500, r1000, rmidcap, sp400, msciusa).
    - Factor Bank tab: factors grouped by the 18 correct master groups; column header "Group" (not "Category"); no "systematic"/"yield" artifacts.
    - Equal Weight button: spreads weights evenly (e.g. 13 factors -> nine 8s + four 7s), no single-factor outlier.
    - Data vintage: asOf 2026-05-18 across all 5 universes.

    MUST be a cherry-pick, NOT `git merge DEV` -- origin/DEV carries 12 non-SSCN commits (ADVI/MDPF/TRSB) interleaved with the SSCN 8; a merge would promote unsmoked cross-pod work to PROD. Andrew's DEV smoke authorizes ONLY the SSCN set.
  </context>

  <scope>
    <step>Phase 0 (pre-PROD tree-verify + cfdf9a5c push -- Andrew-direct instruction, do FIRST + RAVC2 COO before the push). CTO GATE CONDITION 1: cfdf9a5c is committed local-only -- DT MUST push it before the pick or the 8th SHA is unreachable. Steps: (a) `git push origin DEV` from portal so origin/DEV HEAD = cfdf9a5c; (b) bump the parent CLOUD `portal` gitlink to cfdf9a5c, commit via safe-commit.sh (portal path only), `git push origin CLOUD`. Then confirm: portal DEV working tree clean (.frontend-dev/screenshots + .runtmp untracked is fine); origin/DEV HEAD = cfdf9a5c carrying all 8 SSCN commits; parent CLOUD gitlink synced + pushed. RAVC2 COO with working-tree status + origin/DEV HEAD + CLOUD gitlink commit. This is the clean-state gate Andrew asked for.</step>
    <step>Phase 1 (pre-flight, bench-stage OK) -- `cd portal`; `git checkout PROD && git pull origin PROD` (PROD baseline); confirm the 8 SSCN SHAs are on origin/DEV; map their contiguous runs for the cherry-pick order. `bun install` clean.</step>
    <step>Phase 2 (cherry-pick) -- after the GO:
      - CTO GATE CONDITION 2: run `git show --stat cfdf9a5c` and confirm the diff is confined to portal `.frontend-dev/**` with ZERO `portal/src/**` touch. If any `portal/src/**` path appears, HALT and re-surface to COO -- Andrew's d71ac15b smoke covered the .011 fix, not an unexpected src delta riding cfdf9a5c.
      - On portal PROD: cherry-pick the 8 SSCN commits in DEV commit order (45ea7210 -> 2254437c -> b302f5cf -> a844f0dd -> b05388dc -> 7ef0f4a6 -> d71ac15b -> cfdf9a5c). A range-pick of contiguous runs is fine where the runs are contiguous; the result must be exactly those 8, zero non-SSCN commits.
      - If a cherry-pick conflict surfaces (residual risk on shared files -- constants.ts / types.ts / route config): do NOT resolve unilaterally -- RAVC2 PARTIAL to COO with the conflict; COO + CTO adjudicate.
      - `bun run typecheck` + `bun run lint` + `bun run build` on PROD post-cherry-pick -- all exit 0 (lint: a project-wide exit-1 from the 11 known pre-existing react-hooks warnings in an unrelated AUA/Distribution component is acceptable -- it is the same baseline accepted across .007-.011; confirm NO new SecurityScanner lint issue).
    </step>
    <step>Phase 3 (PROD ship) -- `git push origin PROD`. The GHA deploy.yml workflow auto-fires: bun build -> aws s3 sync dist/ s3://opalinvest-portal -> CloudFront EVTSA9VEHNZVH create-invalidation. Monitor the workflow to green. AC8 (CF invalidation) is satisfied automatically by the workflow.</step>
    <step>Phase 4 (PROD smoke) -- smoke https://opalinvest.dev security-scanner page per AC1-AC8. If any AC fails post-push, RAVC2 PARTIAL with the failure -- do NOT roll back unilaterally (Andrew + COO/CTO make the rollback call).</step>
    <step>Phase 5 (RAVC2) -- to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with: the cherry-pick result (PROD log showing exactly the 8 SSCN commits), the GHA deploy.yml run link/status, the opalinvest.dev smoke evidence, AC1-AC8 confirmations. On RAVC2 COMPLETE, COO executes the 3-step SSCN_DIVDEF project closure.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">portal/PROD HEAD includes exactly the 8 SSCN commits (45ea7210 + 2254437c + b302f5cf + a844f0dd + b05388dc + 7ef0f4a6 + d71ac15b + cfdf9a5c) and ZERO non-SSCN commits from origin/DEV. `git log --oneline PROD` verified against the 8-SHA list.</ac>
    <ac id="AC2">`bun run typecheck` + `bun run build` exit 0 on PROD post-cherry-pick; lint shows no NEW SecurityScanner issue (the 11 pre-existing unrelated react-hooks warnings are the accepted baseline).</ac>
    <ac id="AC3">opalinvest.dev first-load: the "Presets:" dropdown shows "DIVZ -- Dividend"; Russell 1000 preselected; the 13 DIVZ factors seeded at the PRD §3.1 weights.</ac>
    <ac id="AC4">No ranking-method control and no 4-group rollup strip render anywhere on the page; weight input is step=1.</ac>
    <ac id="AC5">The Universe dropdown shows exactly the 5 US-equity options (sp500/r1000/rmidcap/sp400/msciusa); switching to each loads scanner data with no 404.</ac>
    <ac id="AC6">Factor Bank tab: factors grouped by the 18 master groups; column header reads "Group"; no "systematic"/"yield" group values; no "Category" user-facing label.</ac>
    <ac id="AC7">Equal Weight button produces an even spread (13 factors -> nine 8s + four 7s, sum 100, no single-factor outlier).</ac>
    <ac id="AC8">CloudFront invalidation fired by the deploy.yml workflow; a new user on opalinvest.dev within ~5min of the push sees the new build. Zero NEW JS console errors on first load (the expected unauthenticated /auth/refresh 401 console noise is pre-existing + benign per the DT 2026-05-20 root-cause -- not introduced here).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before the cherry-pick">
      <step>
        <run>comp-routes trace getUniverseScanner</run>
        <expect>The /api/general/security_scanner/latest/universes/{param}/scanner_data.json route + edge JWT + API GW auth are stable -- unchanged by the 8 SSCN commits. (DT pre-flight already ran this PASS; re-confirm if the DEV tip moved.)</expect>
        <if_mismatch>If the route or auth changed, STOP + RAVC2 COO before pushing.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions (grep scanner)</run>
        <expect>Clean -- no React Query key collision on scanner keys.</expect>
        <if_mismatch>RAVC2 COO -- do not push a cache-corruption risk.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before the push">
      <step>
        <run>bun run typecheck + bun run build on PROD post-cherry-pick</run>
        <expect>Both exit 0 -- the 8-commit cherry-pick result builds clean on the PROD branch.</expect>
        <if_mismatch>A build/type failure post-cherry-pick = a conflict was mis-resolved or a commit is missing a dependency -- RAVC2 COO, do not push.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after the push">
      <step>
        <run>GHA deploy.yml workflow status + opalinvest.dev smoke (AC1-AC8)</run>
        <expect>deploy.yml green; opalinvest.dev serves the new build; AC1-AC8 all pass.</expect>
        <if_mismatch>RAVC2 PARTIAL with the failing AC; no unilateral rollback.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    The cherry-pick mechanism IS the cross-domain control: origin/DEV carries 12 non-SSCN commits (ADVI / MDPF / TRSB) interleaved with the SSCN 7. Promoting ONLY the 7 SSCN SHAs keeps the cross-pod work OFF PROD -- those pods promote their own work under their own sign-off. A blanket `git merge DEV` is FORBIDDEN here. The scanner Lambda (security-scanner-v1.1.3) is already on PROD via Terraform -- not in this push scope; no Lambda/registry touch. No other active TO writes portal/PROD concurrently; if one appears, MCP COO before pushing.
  </cross_domain_coordination>

  <deliverables>
    - portal/PROD with exactly the 8 SSCN commits cherry-picked; pushed to origin/PROD.
    - GHA deploy.yml run to green (s3 sync + CloudFront invalidation).
    - opalinvest.dev smoke evidence (AC1-AC8) + screenshot.
    - Session log under org/tier2_senior/0.3.0_DT_TradingOperations/logs/2026-05-20/ with the cherry-pick log, build transcript, deploy.yml status, smoke results.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO on close. COO then executes the 3-step SSCN_DIVDEF closure (JSON + REGISTRY + PRD status).
  </deliverables>

  <do_not>
    <rule>Do NOT `git merge DEV` into PROD. Cherry-pick the 8 SSCN SHAs ONLY -- a merge ships 12 interleaved non-SSCN commits (ADVI/MDPF/TRSB) to PROD without their pods' sign-off.</rule>
    <rule>Do NOT resolve a cherry-pick conflict unilaterally -- RAVC2 PARTIAL to COO; COO + CTO adjudicate.</rule>
    <rule>Do NOT modify any portal source in this TO -- it is a cherry-pick + push only.</rule>
    <rule>Do NOT touch S3 latest/ or the scanner Lambda -- already on PROD via Terraform (security-scanner-v1.1.3).</rule>
    <rule>Do NOT roll back unilaterally on an AC failure -- RAVC2 PARTIAL; Andrew + COO/CTO make the rollback call.</rule>
    <rule>No emojis in commit messages, the session log, or CLI transcripts (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
