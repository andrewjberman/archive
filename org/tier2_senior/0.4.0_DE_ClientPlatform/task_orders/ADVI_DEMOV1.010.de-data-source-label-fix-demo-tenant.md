<task_order>
<metadata>
  <to_id>ADVI_DEMOV1.010</to_id>
  <project>ADVI_DEMOV1</project>
  <title>Demo tenant data-source label: "Black Diamond" → "Database Connected: Lone Pine Analytics" (Andrew UAT F3)</title>
  <assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatch this cycle (follow-on post-Phase-6 close)</status>
  <priority>MEDIUM (Andrew UAT finding F3; tiny 3-line patch; non-blocking on Phase-6 close which IS shipped end-to-end)</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_DEMOV1.md — Phase 6 close-out follow-on; v0.4.2 wording-refinement candidate alongside Cognito→DynamoDB + §6.1 internal-staff dropdown</ref>
    <ref type="uat_brief">docs/briefs/advi-demov1-uat-backend-findings-20260526.md `ad37838b1` (DT 0.4) — F3 routing definitive: "0.4.0_DE_ClientPlatform frontend (3-line patch in `demo/{index.tsx,constants.ts,layout.ts}`); tiny — TO-010 candidate"</ref>
    <ref type="andrew_uat_quote">Andrew direct sovereign 2026-05-26 ~17:55Z: "all of that is backend issue, we can proceed with our frontend task orders and work on this subject unhindered."</ref>
    <ref type="closure_chain">Project ADVI_DEMOV1 CLOSED COMPLETE 2026-05-26 (3-step atomic close Option B; JSON+REGISTRY shipped this commit; PRD Status COMPLETE routed CTO). TO-010 is post-closure adjacent follow-on; ships into a closed project per LD-0030 carry-open pattern.</ref>
  </references>
  <dependencies>
    <dependency>None — F3 is frontend-class fix surfaced clean from DT 0.4 Phase 2 UAT; no upstream dependency.</dependency>
  </dependencies>
</metadata>

<scope>
Per DT 0.4 UAT brief `ad37838b1` F3 finding: Demo tenant page currently shows data-source label "Black Diamond" (inherited from 49F-template). Demo identity is "Lone Pine Analytics" (per pseudonymization); label should read "Database Connected: Lone Pine Analytics" matching the demo-firm canonical name.

**3-line patch in portal/src/pages/AdvisorIntelligence/_partners/demo/:**
- `index.tsx` — data-source label string update
- `constants.ts` — firm-name constant (if surfaced via constant)
- `layout.ts` — layout config field (if surfaced via layout)

**Out of scope:**
- F1 (numbers × 0.667 transform-logic) → AE 0.6.0 backend (separate routing)
- F2 (account-# Fee Summary classify) → AE 0.6.0 backend (separate routing)
- PRD §1 + §6.1 wording-rot (Cognito + demo@demo.test) → ws CTO ANY_CTO lane (v0.4.2 OR Phase 6 close-out scribe note; deferred)
</scope>

<acceptance_criteria>
- AC1: Demo tenant page data-source label renders "Database Connected: Lone Pine Analytics" (or equivalent canonical demo-firm identifier per pseudonymizer ground-truth).
- AC2: No "Black Diamond" string remains in demo/* tree (grep-clean).
- AC3: Patch lands on portal/DEV branch via DE 0.4 normal workflow; subsequent PROD promotion via DT-pod (separate follow-on; not gating).
- AC4: Local dev-server smoke confirms label change visible (single visual smoke; no full Andrew UAT re-run needed — Phase 6 UAT scope already PASS).
</acceptance_criteria>

<compiler_tools_mandate>
N/A — 3-line cosmetic patch; no compiler-graph relevance. Standard DE 0.4 `bun run dev` + visual smoke + commit.
</compiler_tools_mandate>

<cross_domain_coordination>
- **DT 0.4 follow-on:** post-DE ship, DT 0.4 picks up PROD promotion (or folds into next portal-tag bump cycle). Coordination optional given tiny patch + non-blocking nature.
- **No CTO/CVO routing required** — cosmetic scope.
- **Phase 6 close discipline:** ADVI_DEMOV1 is CLOSED-COMPLETE; TO-010 ships as carry-open follow-on. Does NOT re-open project status.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for the 3-line patch + visual smoke confirmation
- Brief session log entry (light)
- RAVC2-Request to ws COO (light close-out MCP; ~5min wall)
</expected_evidence>

<notes>
**Tiny scope:** 3-line patch + visual smoke + commit; ETA ~15-30min wall.

**Carry-open status:** Phase 6 project closure (3-step atomic shipped this /drive #102 cycle) does NOT block TO-010. Post-closure follow-ons are acceptable per LD-0030 staging pattern (sister to .006 Path B PII-tagging follow-on which also rides post-closure). RAVC2-Request closure routes to me but project re-open is NOT required.

**Standby-prep eligible** — DE 0.4 has full TO-008 demo-tenant context; this is a tiny continuation of same surface area. STANDBY-PREP→delivery compression eligible per [[standby-prep-compress-to-delivery-when-context-sufficient]].

**Pre-existing wording-rot bundling:** if convenient, fold the Cognito→DynamoDB language fix in same patch (no agent dependency; pure string change). Otherwise hold for v0.4.2 CTO scribe.

**No urgency** — Andrew UAT-PASS-FRONTEND-SCOPE was clean; this is cosmetic polish per Andrew direct sovereign "we can proceed with our frontend task orders ... unhindered" disposition.
</notes>
</task_order>
