<task_order>
  <metadata>
    <id>ADVI_SHARED.007</id>
    <slug>rd-lint-residual-sweep</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO. All three gates met: (1) .004 SHIPPED 2057099c + 74a29229 (Cat A 16→0); (2) .005 SHIPPED d9882117 (Cat B 9→0; audit predicted 12); (3) .006 SHIPPED bf97a24b→35e0adf9 (firmId canonicalization). Audit §F.0 drift pattern confirmed third consecutive correction — expect Cat OTHER actual count significantly under 76 predicted; lint baseline should be tight enough that .007 ships in well under the original ~1d SLA.</dispatch_unblock_condition>
    <project_code>ADVI_SHARED</project_code>
    <priority>P1 — Category OTHER lint warnings (76 per audit §F.0 — PRD framing was 5x undercount); subdivisible per audit recommendation</priority>
    <sla>~1d wall post-unblock (CTO ratified subdivision pattern — RD discretion on per-file commits vs per-warning-class commits)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §4.2 SHARED.007 + §3.6 lint regression gate (gate ships in .012)</ref>
    <ref type="audit">docs/briefs/ADVI_SHARED_AUDIT.md §F.0 PRD framing correction (Cat OTHER = 76 not ~15) + §F.1 per-file warning table + §F.4 supplement candidates</ref>
    <ref type="cto_ratify">Session66 RAVC4 Item 3 + bonus: SHARED.007 subdivision into 007a/b/c/d ratified — RD discretion on subdivision granularity within this TO scope</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
  </references>

  <context>
    Resolve Category OTHER lint warnings — actual count 76 per audit §F.0 (PRD §2.4 predicted ~15; framing 5x off).

    Audit §F.1 per-file breakdown:
    - InflectionInsightsPanel.tsx: 12 `no-explicit-any` + 4 dep-array fixes (Cat OTHER total 16)
    - DistributionTab.tsx: 9 `set-state-in-effect` + 2 `exhaustive-deps` + 2 preserved-memo + 2 `unused-imports` (Cat OTHER total 14 — **largest single-file load**)
    - AdvisorPublicProfile.tsx: 5 `unused-imports` + 1 `exhaustive-deps` + 1 preserved-memo (7)
    - ClientsTab.tsx: 5 `unused-imports` (post-2026-05-12 BooksTab migration left these — `eslint --fix` may handle)
    - AdvisorsTab.tsx: 2 Cat OTHER (alongside 3 Cat B)
    - AdvisorBookView.tsx: 2 `no-explicit-any` + 2 `unused-imports` (4)
    - FeeEfficiencyPanel.tsx: 1 `unused-imports` (alongside 1 Cat A)
    - AuthContext.tsx: 2 `exhaustive-deps` (low priority — careful with auth lifecycle stability)
    - Remaining residuals per audit §F.1 detail

    **CTO-ratified subdivision pattern** (per session66 RAVC4):
    - **007a — Type-tightening:** `no-explicit-any` sweep (16 instances; treat sentinel-keep where API response shapes genuinely require `any`)
    - **007b — Effect→useQuery migration:** `set-state-in-effect` warnings (9 in DistributionTab — same pattern as RD's 2026-05-12 BooksTab N1→useQuery migration; concrete refactor target)
    - **007c — Dependency-array + memo:** `exhaustive-deps` + `preserved-memo` warnings; careful per-file (AuthContext stability)
    - **007d — Import sweep:** `unused-imports` (eslint --fix candidate; lowest risk)

    RD discretion on whether to ship 007a/b/c/d as four separate commits or one bundled commit (per RD discipline). Single TO covers all.

    **Dead-code cleanup** (audit §C.1-.7):
    - `DEFAULT_FIRM_ID` + `AVAILABLE_FIRMS` in `_partners/49financial/constants.ts` (dead — delete)
    - `DEFAULT_FIRM_ID` + `AVAILABLE_FIRMS` in `_partners/inflection/constants.ts` (dead — delete)
    - Stale W5.1 TODO comments in `_partners/inflection/roles.ts` (audit §C.4 stale)
  </context>

  <objective>
    Sweep 76 Cat OTHER lint warnings to ≤10 residual (project-level AC-3 from PRD §8). Delete dead-code constants per audit §C. Sentinel-keep `any` only where API response shapes genuinely require it (documented per instance). Effect→useQuery migration on DistributionTab `set-state-in-effect` warnings.
  </objective>

  <scope>
    <files>
      <file action="modify">Per audit §F.1 per-file table — 76 Cat OTHER warnings across ~10 files</file>
      <file action="delete">_partners/49financial/constants.ts DEFAULT_FIRM_ID + AVAILABLE_FIRMS dead code</file>
      <file action="delete">_partners/inflection/constants.ts DEFAULT_FIRM_ID + AVAILABLE_FIRMS dead code</file>
      <file action="modify">_partners/inflection/roles.ts — remove stale W5.1 TODO comments (audit §C.4)</file>
      <file action="readonly_reference">docs/briefs/ADVI_SHARED_AUDIT.md §F + §C verbatim</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | grep -E "no-explicit-any|set-state-in-effect|exhaustive-deps|unused-imports" | wc -l</run>
      <expect>Baseline ~76 per audit §F.0 (Cat OTHER total); tolerate drift ±5 since 2026-05-12.</expect>
      <if_mismatch>If significant drift, COO surface — concurrent commits affected scope.</if_mismatch>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | grep "set-state-in-effect"</run>
      <expect>9 in DistributionTab.tsx per audit §F.1 — concrete useQuery migration list.</expect>
      <if_mismatch>Re-enumerate per current state.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors per commit.</expect>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | tail -5</run>
      <expect>Cat OTHER count drops from baseline ~76 to ≤10 residual.</expect>
      <if_mismatch>Finish sweep before commit OR document sentinel-keep instances inline.</if_mismatch>
    </step>
    <step>
      <run>bun run dev + visual smoke per partner</run>
      <expect>Zero regression — sweep is hygiene, not feature change.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | wc -l</run>
      <expect>Total lint warning count drops from baseline 101 to ≤10 (per PRD §8 AC-3) post .004 + .005 + .007.</expect>
      <if_mismatch>Surface residual class to COO for .008 readiness.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Cat OTHER lint warnings drop to ≤10 residual.
    AC2: Dead-code deleted: 49F + Inflection constants.ts DEFAULT_FIRM_ID + AVAILABLE_FIRMS.
    AC3: Stale W5.1 TODO comments removed from _partners/inflection/roles.ts.
    AC4: Sentinel-keep `any` instances documented inline (per-instance comment explaining API-shape constraint).
    AC5: DistributionTab `set-state-in-effect` 9 warnings — useQuery-migrated OR explicitly justified per-instance.
    AC6: AuthContext `exhaustive-deps` — careful evaluation (DO NOT break auth lifecycle); skip + sentinel-keep if risky.
    AC7: tsc 0 errors per commit.
    AC8: Visual smoke clean per partner.
    AC9: Session log with subdivision breakdown (007a/b/c/d distribution) + per-instance sentinel-keep documentation.
    AC10: MCP RAVC2 to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>Phases above.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: .004 + .005 (close Cat A + Cat B first; then .007 sweeps residual + Cat OTHER). .006 RAVC2 (firmId rename may surface additional unused-imports).
    PARALLEL-OK: post-unblock, ship in parallel with .008 smoke-gate.
    PORTAL SUBMODULE: DT 0.4 push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE lint hygiene only.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Cat OTHER sweep (~66 warning fixes; ≤10 residual)
    2. Dead-code deletion per §C
    3. Stale-comment removal per §C.4
    4. Session log with subdivision breakdown
    5. MCP RAVC2 to COO
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO on AC1-10 PASS.</ravc>

  <notes>
    **Audit framing correction:** PRD §2.4 5x undercount on Cat OTHER. This TO absorbs the additional scope without further subdivision into separate TOs (RD discretion on commit-level subdivision per CTO ratify).

    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.

    **Sentinel-keep policy:** `any` types on API response shapes that genuinely need flexibility (e.g., loose JSON from gold emits where shape varies across pipelines) are KEEP-with-inline-comment. RD judgment on per-instance basis.
  </notes>
</task_order>
