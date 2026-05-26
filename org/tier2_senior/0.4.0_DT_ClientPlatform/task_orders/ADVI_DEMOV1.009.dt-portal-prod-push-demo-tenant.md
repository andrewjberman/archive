<task_order>
<metadata>
  <to_id>ADVI_DEMOV1.009</to_id>
  <project>ADVI_DEMOV1</project>
  <title>Portal DEV → PROD push (demo-tenant; ~30min-1h)</title>
  <assigned_to>0.4.0_DT_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <completed>2026-05-26T17:38Z by 0.4.0_DT_ClientPlatform</completed>
  <ship_evidence>
    Phase 1: portal/origin/DEV @ 03a8544155 (push 4938bf36..03a85441; VALGATE D-1 PASS; GitHub CI run 26460394795 GREEN 2m15s; bun tsc + bun build clean locally).
    Phase 2: Andrew UAT PASS-frontend-scope ~17:30Z (Smoke-A dropdown ✓, Smoke-B 3-tab ✓, Smoke-C populates with F1 finding, Smoke-D names pseudonymized excellent with F2 finding). Backend findings briefed via docs/briefs/advi-demov1-uat-backend-findings-20260526.md (commit ad37838b1) routing F1+F2 to AE 0.6.0, F3 to DE pod.
    Phase 3: portal/origin/PROD @ b7b201a610 (cherry-pick 03a85441 onto PROD via ephemeral worktree at portal/.runtmp/portal-prod-cherry; tsc -b --noEmit gate PASS; pushed 0be05530..b7b201a6). Ephemeral worktree removed clean.
    Phase 4: parent CLOUD commit 794cf9c0a (portal gitlink 0be05530 -> b7b201a6 via update-index --cacheinfo; main portal tree stayed on DEV throughout per strand-discipline). Tag portal-v2.1.73 (6e5d9a9257) pushed --follow-tags.
    Strand AC5 SAT: main portal tree on DEV @ 03a85441 post-ship (pre-existing 0.3.0_DT strand un-done at Phase 3 prep).
  </ship_evidence>
  <priority>HIGH (Andrew sovereign direct ~15:45Z Phase 6 completion chain; TO-009 closes the DEV→PROD ship gap)</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_DEMOV1.md v0.4.1 commit `332a56f0f` (ws CTO; Phase 6 §6.1 TO-009 spec).</ref>
    <ref type="predecessor">TO-008 SHIPPED `03a85441` portal/DEV + `bafe89aa6` workspace session log (DE 0.4; 6-item single coordinated commit; ws COO RAVC2-ACCEPT `20260526T154838Z`).</ref>
    <ref type="serial_revival">DT 0.4 spawn via /allocation #8 ALLOCATION-IMPLICIT-LIFT (Andrew Phase 6 directive implicit-lift parallel to DE 0.4 #7 + AE 0.7 #6 patterns).</ref>
    <ref type="strand_discipline">`feedback_portal_prod_promotion_strands_main_tree` — MUST use `git worktree add` ephemeral worktree for PROD cherry-pick; NEVER `git checkout PROD` in the main tree.</ref>
  </references>
  <dependencies>
    <dependency>TO-008 RAVC2-Accepted ✓ (portal/DEV `03a85441` on remote).</dependency>
    <dependency>Andrew UAT (TO-VAL-FE) between DEV push + PROD cherry-pick — gates the cherry-pick step.</dependency>
    <dependency>AC9-INDEPENDENT per PRD §6.1 — read-only portal connection scope.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD v0.4.1 §6.1 TO-009:

**Phase 1 — DEV push:**
1. Verify TO-008 `03a85441` committed cleanly to portal submodule DEV branch (already on remote via DE 0.4 ship)
2. Verify `bun tsc` + `bun build` clean locally on DEV checkout
3. Push portal submodule DEV branch to remote DEV (likely already pushed by DE 0.4; verify)

**Phase 2 — Andrew UAT pause (TO-VAL-FE):**
- Andrew runs UAT on DEV CloudFront deploy (Smoke-A through Smoke-D per PRD §6.1)
- Wait for UAT PASS signal before proceeding to PROD

**Phase 3 — PROD cherry-pick:**
- Use **ephemeral worktree** per [[feedback_portal_prod_promotion_strands_main_tree]]:
  ```bash
  cd portal
  git worktree add ../portal-prod-cherry PROD
  cd ../portal-prod-cherry
  git cherry-pick 03a85441
  git push origin PROD
  cd -
  git worktree remove ../portal-prod-cherry
  ```
- **NEVER** `git checkout PROD` in the main `portal/` tree (strands the tree on PROD; sticky failure 2x recurred 2026-05-22)

**Phase 4 — Parent repo submodule pointer bump:**
- In workspace parent repo (`ajb_workspace`), bump portal submodule SHA to the PROD cherry-pick commit
- Commit: `git submodule update --remote portal` OR explicit `(cd portal && git checkout PROD)` in main `ajb_workspace` (then verify main tree NOT stranded — `git -C portal checkout DEV` back at end)
- Tag `portal-v2.1.83` (or next sequential per `git tag --list 'portal-v*'`)
- Push parent repo + tags: `git push origin CLOUD --follow-tags`
</scope>

<acceptance_criteria>
- AC1: DEV branch on portal remote carries TO-008 commit `03a85441`; DEV CloudFront deploy reflects new code (verify via curl on DEV CloudFront).
- AC2: Andrew UAT on DEV PASS (TO-VAL-FE acceptance; Smoke-A through Smoke-D per PRD §6.1).
- AC3: PROD branch on portal remote carries cherry-pick of `03a85441`; PROD CloudFront deploy reflects new code.
- AC4: Parent repo `ajb_workspace` portal submodule pointer bumped to PROD cherry-pick SHA + tagged `portal-v2.1.83` (or next sequential) + pushed `--follow-tags`.
- AC5: Main portal worktree NOT stranded on PROD post-push (per strand discipline; main tree should be back on DEV).
- AC6: `git status` on parent repo clean post-pointer-bump (no working-tree pollution).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 2 (before parent-pointer-bump):**
- `git status` on parent repo to ensure clean state pre-bump
- `git -C portal log --oneline -1` to verify pointer target is correct PROD cherry-pick SHA
**Phase 3 (after PROD cherry-pick push):**
- Verify on portal remote: `git ls-remote origin PROD` matches the cherry-pick SHA
- Verify CloudFront deploy reflects new code (curl)
**Phase 4 (after parent commit):**
- `git status` clean
- `git -C portal status` clean + on DEV branch (not stranded)
- Tag pushed: `git ls-remote --tags origin portal-v2.1.83`
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-VAL-FE Andrew UAT gate:** between Phase 1 DEV push + Phase 3 PROD cherry-pick. Coordinate with me (ws COO) when DEV deploy reflects new code + Andrew is engaged for UAT.
- **DE 0.4** already shipped TO-008 (DE-pod work done); no DE coordination required for TO-009.
- **AE 0.7** is on ADHC_COMPIL_V5.001 critical path; not involved in TO-009 (CloudFront propagation is automatic post-cherry-pick).
</cross_domain_coordination>

<expected_evidence>
- Portal DEV branch HEAD SHA + DEV deploy curl evidence
- Andrew UAT PASS signal (forwarded via MCP)
- Portal PROD branch HEAD SHA (cherry-pick of 03a85441) + PROD deploy curl evidence
- Parent repo commit hash + portal submodule pointer SHA + tag `portal-v2.1.83` (or next sequential)
- Session log with archetype DEPLOY + Compiler Tools section + ephemeral-worktree pattern citation
- `git status` clean evidence (main tree on DEV; parent repo clean)
</expected_evidence>

<notes>
**Spawn-with-direction context:** Andrew sovereign-direct Phase 6 dispatch ~15:45Z + DE 0.4 spawn 15:23Z + TO-008 ship 16:00Z = Phase 6 first-step shipped fast. TO-009 closes the DEV→PROD ship gap so Andrew UAT can fire.

**Strand-discipline reminder (Andrew banked precedent):** `feedback_portal_prod_promotion_strands_main_tree` — 2x recurred 2026-05-22 on pod 3 + SSCN. **ALWAYS** use `git worktree add` ephemeral worktree for PROD cherry-pick. Main `portal/` tree stays on DEV throughout.

**TO-VAL-FE Andrew UAT** is a separate thin TO (`ADVI_DEMOV1.VAL-FE.andrew-uat-demo-tenant-visual-smoke`) — I'll author just-in-time when DEV deploy reflects new code. The UAT gate sits BETWEEN your Phase 1 push and Phase 3 cherry-pick.

**Project ADVI_DEMOV1 close-out trajectory:** TO-008 ✓ → TO-009 (this) → TO-VAL-FE → 3-step project close (or .006 + AC5 disjointness banking carry-forward per CY-0124).

**Tag pattern:** check `git tag --list 'portal-v*' | sort -V | tail -3` for current pattern; bump minor for Phase 6 ship.

Architectural questions / PRD scope → ws CTO (1.0.0_SA_CTO). Dispatch / RAVC2 / blockers → me (2.0.0_SA_COO).
</notes>
</task_order>
