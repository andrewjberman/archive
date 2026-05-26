<task_order>
<metadata>
  <to_id>ADVI_DEMOV1.VAL-FE</to_id>
  <project>ADVI_DEMOV1</project>
  <title>Andrew UAT visual-smoke (closes original AC4 + Phase 6 close-out gate)</title>
  <assigned_to>Andrew (sovereign UAT)</assigned_to>
  <coordinated_by>2.0.0_SA_COO</coordinated_by>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — Andrew UAT engagement</status>
  <priority>HIGH (Phase 6 close-out gate; closes original Phase 5 deferred AC4 visual-smoke)</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_DEMOV1.md v0.4.1 commit `332a56f0f` (Phase 6 §6.1 TO-VAL-FE spec).</ref>
    <ref type="predecessor">TO-008 SHIPPED `03a85441` portal/DEV (DE 0.4); TO-009 Phase 1 COMPLETE — `origin/DEV` at `03a85441` + CI green + local builds clean (DT 0.4 verified ~16:50Z).</ref>
    <ref type="ac1_reality">Portal has single CF distribution `EVTSA9VEHNZVH` (opalinvest.dev); DEV-branch CI = build-validation only (no S3+CF deploy); PROD-branch ships to live. AC1 satisfied via origin/DEV SHA + CI green + local builds equivalent surrogate per DT 0.4 reality-reconciliation 16:50Z.</ref>
  </references>
  <dependencies>
    <dependency>TO-009 Phase 1 COMPLETE ✓ (origin/DEV at 03a85441).</dependency>
    <dependency>Andrew sovereign engagement for UAT — open invitation; no SLA.</dependency>
  </dependencies>
</metadata>

<scope>
Andrew-direct visual smoke on local portal dev server (built from origin/DEV at `03a85441`), backend talking to live opalinvest.dev (L@E + Lambda + opal-data-demo bucket all pre-deployed per LD-0055 + .007 closure).

**Local UAT runtime (per PRD §6.1 + DT 0.4 reconciliation):**
```bash
cd portal/.runtmp/portal-dev-verify   # DEV worktree at 03a85441
bun run dev --port 5175               # local dev server
# Visit http://localhost:5175 + login as demo@demo.test
```

**4-smoke surface (Andrew runs):**
- **Smoke-A:** Partner-selector dropdown shows "Demo" alongside "49 Financial" + "Inflection Wealth Management"
- **Smoke-B:** Selecting "Demo" mounts DemoView (3-tab canonical layout per `_partners/demo/index.tsx` mirroring 49F)
- **Smoke-C:** Data populates from opal-data-demo across surfaces (advisors / clients / accounts; canonical format; no empty-panel placeholders)
- **Smoke-D:** No PII leak — surface-confirmation that all rendered names/identifiers are fake-pseudonymized (zero real-49F-PII leak)

**UAT disposition signals:**
- **PASS:** Andrew MCPs ws COO (or any path) with PASS signal → I MCP DT 0.4 to proceed Phase 3 (PROD cherry-pick)
- **CONCERN/REWORK:** Andrew surfaces specific finding → I route to DE 0.4 (DemoView fix) OR ws CTO (architectural) OR back to DT 0.4 (deploy-side) per finding scope
- **DEFER:** Andrew non-responsive >1 /drive cycle (~20min) — TO-VAL-FE stays in `pending` state; project ADVI_DEMOV1 stays active for AC4 closure; cap-impact minimal (DE 0.4 + DT 0.4 KEEP-ACTIVE pending the gate). Standing-posture indefinite-OK per `feedback_anticipatory_patience_discipline`.
</scope>

<acceptance_criteria>
- AC1: Andrew runs Smoke-A through Smoke-D from local dev server at `03a85441` build.
- AC2: All 4 smoke surfaces PASS visually (partner-selector + DemoView mount + data populates + no-PII-leak).
- AC3: Andrew sovereign sign-off (any positive signal: MCP "PASS" / direct verbal / commit message). Closes original Phase 5 deferred AC4 visual-smoke + completes Phase 6 close-out chain.
- AC4: COO MCP to DT 0.4 with UAT PASS → DT 0.4 proceeds Phase 3 (PROD cherry-pick + parent submodule pointer bump + tag).
</acceptance_criteria>

<compiler_tools_mandate>
N/A — Andrew sovereign UAT scope. No comp-* tools applicable.

Banking note: TO-009 AC1 wording-vs-portal-deploy-model gap surfaced by DT 0.4 reality-reconciliation (16:50Z) — PRD/TO AC text references "DEV CloudFront deploy" but portal has only PROD CF distribution. Candidate 8th comp-tool R&D extension (sister to ADHC_COMPIL_V5 Fix 3 `comp-registry sync` class) — model DEV-branch-CI-only vs PROD-branch-deploy semantics for AC text generation. Banking for ADHC_COMPIL_V5 v0.2 or v6 consideration.
</compiler_tools_mandate>

<expected_evidence>
- Andrew sovereign PASS signal (MCP / commit / verbal)
- Optional: screenshot or surface-confirmation note from Andrew side
- COO confirmation MCP to DT 0.4 triggering Phase 3
</expected_evidence>

<notes>
**Phase 6 close-out chain:**
TO-008 ✓ → TO-009 Phase 1 ✓ → **TO-VAL-FE (this) → TO-009 Phase 3 (cherry-pick PROD)** → 3-step project-close (or .006 + AC5 disjointness carry-forward per CY-0124 if open).

**Andrew engagement path:** Andrew has been heavily engaged today (multiple direct sovereign messages on YALP_MKTOVR, ADVI_DEMOV1 Phase 6, ADHC_COMPIL_V5). UAT gate may resolve quickly OR defer. No SLA pressure; the project holds at Phase 2 pause-for-UAT until signal lands.

**State carry-forward absorbed (DT 0.4 banked):**
- Main `portal/` tree pre-stranded on PROD `0be05530` (2026-05-22 pre-this-session damage); DT 0.4 Phase 4 AC5 cleans up
- Parent ws submodule gitlink unbumped (Phase 4 bumps post-PROD-cherry-pick)
- Tag drift: local v2.1.72 / remote v2.1.98 — DT 0.4 sources from origin via `git ls-remote --tags origin 'portal-v*' | sort -V | tail -3` per `feedback_git_fetch_before_deriving_deploy_head` discipline

Architectural questions → ws CTO. UAT coordination / Phase 3 trigger → me. UAT PASS signal can come from Andrew via any channel; I route to DT 0.4 same operational window.
</notes>
</task_order>
