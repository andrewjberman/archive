<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-007-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>complete -- 0.4.0_DS_ClientPlatform~C, commit 675d869f. Catalog at docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>2</wave>
    <phase>P2</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~B" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Compile the unified platinum file catalog from all 4 Wave 1 audit deliverables.
    This is the master specification of every platinum/ file across all ADVI surfaces,
    with provenance, sizing, ownership, and cross-surface sharing annotations.
    This catalog is the blueprint for Phase 3 execution.
  </objective>

  <context>
    Wave 1 produced 5 audit briefs:
    - docs/briefs/ADVI_49PUSH_P2_2.1_partner_analytics.md (~B)
    - docs/briefs/ADVI_49PUSH_P2_2.2_distribution.md (~B)
    - docs/briefs/ADVI_49PUSH_P2_2.3_advisors_tab.md (~C)
    - docs/briefs/ADVI_49PUSH_P2_2.4_books_remaining.md (~D)
    - docs/briefs/ADVI_49PUSH_P2_cross_surface_matrix.md (~D)

    Plus Phase 1 PRD defines the Books tab platinum files already implemented in D_04:
    - docs/architecture/ADVI_49PUSH_P1_PRD.md

    This TO merges all findings into one canonical catalog. No code -- design document only.

    Key findings from Wave 1 to incorporate:
    - advisor_rolling_flows.json (52MB) is dead code (~C finding)
    - PartnerAnalytics header uses D_00 + D_03, not D_01 (~B finding)
    - NNA divergence between D_01 and D_00 (~B finding)
    - 3 cross-surface divergences with canonical resolutions (~D finding)
    - Revenue/Cost Basis panel needs C_05 + D_02 assembly (~D finding)
  </context>

  <requirements>
    <requirement id="1">
      Read ALL 5 audit briefs plus the P1 PRD. Extract every platinum file specification.
    </requirement>

    <requirement id="2">
      Produce the MASTER PLATINUM FILE CATALOG with this structure:

      For each platinum/ file:
      | Field | Description |
      |-------|-------------|
      | Path | Full S3 key (e.g., platinum/firm/dashboard.json) |
      | Count | 1 (firm-level) or ~N (entity-level) |
      | Approx Size | Per file |
      | Producer | Which script writes it (D_04, or D_04 expanded, or new D_05) |
      | Gold Sources | Which gold files/scripts feed it (with specific fields) |
      | Consumers | Which portal components read it (tab + component name) |
      | Shared Across | Which ADVI surfaces share this file |
      | Phase | Which phase delivers it (P1 = already built, P3 = needs building) |
      | Status | DELIVERED (in D_04) or DESIGNED (pending P3) |
    </requirement>

    <requirement id="3">
      CROSS-SURFACE SHARING ANNOTATIONS:
      For files shared across surfaces (e.g., dashboard.json used by Books N1 AND Advisors tab),
      annotate which fields each surface uses. This prevents Phase 3 from accidentally breaking
      one surface while building for another.
    </requirement>

    <requirement id="4">
      DIVERGENCE RESOLUTION TABLE:
      Merge the cross-surface matrix from ~D with the specific divergences found by ~B and ~C.
      For each divergence, document:
      - The metric
      - Current gold sources (divergent)
      - Canonical platinum source (resolved)
      - Which D_04 function implements the resolution
    </requirement>

    <requirement id="5">
      DEAD CODE / DEAD ARTIFACT LIST:
      Compile all dead artifacts found during audits:
      - advisor_rolling_flows.json (52MB, dead)
      - getAdvisorRollingFlows (API endpoint, dead)
      - Any others found in the audit briefs
      Recommend removal timeline (Phase 3 or Phase 5 cleanup).
    </requirement>

    <requirement id="6">
      SCRIPT ARCHITECTURE RECOMMENDATION:
      Based on the catalog, recommend whether Phase 3 should:
      - Option A: Expand D_04 to produce ALL platinum files (firm-level + entity-level)
      - Option B: Create D_05+ for non-Books platinum files
      Include runtime estimate and risk assessment per PRD Phase 3 section.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md -- the master catalog</deliverable>
    <deliverable>Message to COO (2.0.0_SA_COO) with: file count summary, key decisions, recommendation</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT write any code -- this is design only</rule>
    <rule>Do NOT invent platinum files not specified in the audit briefs -- catalog what was designed</rule>
    <rule>Do NOT ignore the cross-surface matrix PENDING columns -- merge ~B and ~C data into them</rule>
  </do_not>
</task_order>
