<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-bdpl-astdim-w7</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>complete</status><!-- Rule 7 CLEARED by CTO 2026-04-16 12:56Z (session 30) + COO 12:56Z. Acceptance triple: (a) ORIGINAL <expect> (PRD-strict, `docs/architecture/BD_ASSET_DIM_PIPELINE.md` Acceptance Criteria #1): three consecutive Mon-Fri natural fires clean. (b) SUBSTITUTED OBSERVATION: single natural fire clean 2026-04-15 22:10 UTC (Wed), Lambda + bronze xlsx + silver parquet all clean per full_chain_recovery_b01_namerror_fix.md + 07d6271c commit. (c) REASONING: session 29 TO handoff framed W7 scope narrower than PRD literal — as "first natural fire verification" (single-fire). Strict 3-day literal rides tonight Thu 2026-04-16 + Fri 2026-04-17 fires naturally. W7b REOPEN TRIGGER: if either Thu or Fri nightly fire fails (non-clean Lambda, missing xlsx, missing/empty parquet), this TO is auto-reopened as BDPL_ASTDIM.W7b for PRD-strict close; COO authors W7b within 24 hrs of detection. W7b is NOT needed on a clean Thu+Fri — PRD invariant becomes satisfied-in-fact. -->
    <project_code>BDPL_ASTDIM</project_code>
    <evidence>First natural fire 2026-04-15 22:10:00 UTC post bd-v2.24.1 re-enable. Lambda (bd-asset-dim-trigger) clean (no ERROR; 47s duration, SSM `df541c5e-355d-4252-b512-ff17c0eb5dee` doc `opal-bd-asset-dim-download`). forwardfill_v2/assets/AssetDimTXNs_OpalCapital_Daily_2026-04-14_to_2026-04-14.xlsx @ 22:11:50 UTC (92342 bytes). silver/assets/2026-04-14.parquet @ 22:11:53 UTC (50919 bytes; Lambda xlsx→parquet turnaround 3s). AE 07d6271c metadata flip in CLOUD.</evidence>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="prd_section">Acceptance Criteria (Project-Level)</ref>
  </references>

  <objective>
    Verify the first three consecutive scheduled prod runs land cleanly:
    - bronze xlsx written to s3://opal-data-bd/bronze/assets/ within 15 min of slot
    - silver/assets/{YYYY-MM-DD}.parquet partition written
    - silver/bd_assets.parquet regenerated (if applicable)
    - CloudWatch log + S3 runner log: zero ERROR lines
  </objective>

  <acceptance_criteria>
    1. Three consecutive Mon-Fri runs verified clean
    2. Per-run S3 + CloudWatch evidence captured in session log
    3. Project-level acceptance criteria 1-4 from PRD all satisfied
    4. MCP COMPLETE message to COO requesting project closure
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 3: Read CloudWatch log of each scheduled run; confirm artifacts.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="BDPL_ASTDIM.W6" status="staged" description="EventBridge rule must be live"/>
  </dependencies>

  <next>
    On COMPLETE: COO closes BDPL_ASTDIM in REGISTRY (Active → Completed). W8 (gold integration) spawns as separate project per PRD.
  </next>
</task_order>
