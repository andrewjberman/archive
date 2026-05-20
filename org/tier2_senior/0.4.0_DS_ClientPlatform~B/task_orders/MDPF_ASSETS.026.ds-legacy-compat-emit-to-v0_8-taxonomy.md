<task_order>
  <metadata>
    <id>MDPF_ASSETS.026</id>
    <slug>ds-legacy-compat-emit-to-v0_8-taxonomy</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-20 (authored on CTO~B ruling re: MDPF_ASSETS.022 scope inversion)</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>TWO-STAGE. STAGE 0 (Phase 0 delta-quantification dry-run) is UNBLOCKED NOW -- it is non-mutating (a dry-run + diff, no commit, no S3 deploy, no live-artifact change) and DS~B should execute it immediately and route the delta figure to 1.0.0_SA_CTO~B. STAGE 1 (Phases 1-4, the actual build_legacy_compat_emit.py change) is DISPATCH_HELD on Andrew sign-off: build_legacy_compat_emit.py is the SoT for non_model_assets.json, the LIVE artifact the current Model Portfolios page reads -- (b) MOVES the live page's displayed AUA. CTO~B surfaces the now-vs-WS-F timing decision to Andrew WITH the Phase-0 delta figure; on Andrew sign-off, COO~B flips dispatch_held=false and DS~B executes Stage 1.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P2 -- successor to MDPF_ASSETS.022 part (b). Brings build_legacy_compat_emit.py (the legacy non_model_assets.json emitter, SoT for the LIVE Model Portfolios page) to the v0.8 taxonomy established by .024 (2-term headline) + .025 (full-BD-book certified_aua 1b) + .016 (Cohort-0 backfill). Until this ships, the live partner-facing page shows the pre-correction methodology (notably the ~$25M SMA double-count) for the whole Phase-2.5->3 window.</priority>
    <sla>Phase 0: ~30-60min DS (dry-run + diff + delta report). Stage 1 (Phases 1-4): ~2-3h DS -- a small, well-understood mirror of the .024 fix.</sla>
    <deadline>None hard. Phase 0 promptly (it gates Andrew's decision). Stage 1 on Andrew sign-off.</deadline>
  </metadata>

  <references>
    <origin>CTO~B ruling 2026-05-20 on the MDPF_ASSETS.022 scope inversion (DS~B's catch). .022 closed (a)-scope-only; part (b) carved here as a fresh TO rather than a .022 amendment because .022's AC1/AC4 are inverted by the v0.8 taxonomy. CTO~B: "build_legacy_compat_emit.py is the SoT for non_model_assets.json -- the LIVE artifact the current Model Portfolios page reads. (b) MOVES the live page's displayed AUA. The methodology is already Andrew-ruled (v0.8 = full-BD-book + 1c-subdivision) -- so (b) is not a new methodology decision -- BUT changing a live CEO-facing number, even toward more-correct, is not something we do without him knowing."</origin>
    <methodology_already_ruled>v0.8 is fully Andrew-ruled: full-Black-Diamond-book certified_aua basis for 1b; 1c (SMA) is a non-additive display-only sub-slice of 1b, NEVER summed separately; headline opal_aggregate_aua = 1a + 1b + 2a (2-term per cohort: model + non_model). This TO does NOT re-decide methodology -- it applies the already-ruled methodology to the legacy emitter.</methodology_already_ruled>
    <canonical_reference>data/mdpf/scripts/gold/mdpf_aggregate_aua.py is the .024-corrected reference -- the 2-term headline + 1b SMA-inclusive logic is already correct there. build_legacy_compat_emit.py must be brought to match.</canonical_reference>
    <pipeline_rule>Rule 13 (DS owns commit + S3 deploy cycle for data/*/scripts/gold/*.py). Rule 14 (.tools/ds-commit-gate.sh on every .py edit). Rule 15 (`from __future__ import annotations` first import). Rule 17 (gold-tier only -- build_legacy_compat_emit.py is a gold script, business-logic field-handling permitted).</pipeline_rule>
  </references>

  <context>
    Under the v0.8 taxonomy correction (.024/.025/.016), the WS-A canonical aggregator mdpf_aggregate_aua.py now emits the corrected 2-term headline with full-BD-book certified_aua as the 1b basis and 1c (SMA) as a non-additive sub-slice. build_legacy_compat_emit.py -- which emits the legacy non_model_assets.json that the LIVE Model Portfolios page consumes -- still emits the pre-correction methodology. The known divergences: (1) the ~$25M SMA double-count (legacy subtracts `- sma_aua` from non_model_aum, making 1b SMA-EXCLUSIVE; v0.8 has 1b SMA-INCLUSIVE with 1c as a display-only sub-field); (2) the 1b basis difference (legacy computes 1b against compute_49f_broader_custody; v0.8 uses certified_aua, the full Black Diamond book). DS~B located the change site at build_legacy_compat_emit.py L499-503. This TO quantifies the total live-page delta (Phase 0) then, on Andrew sign-off, applies the v0.8 fix (Stage 1).
  </context>

  <scope>
    <step>Phase 0 -- DELTA QUANTIFICATION (UNBLOCKED NOW; non-mutating). Dry-run a v0.8-corrected build_legacy_compat_emit.py against the CURRENT live non_model_assets.json for a recent production date. Compute and report the EXACT total figure the live Model Portfolios page would move by under v0.8 -- broken out by component: (i) the SMA double-count removal (~$25M est), (ii) the 1b basis change (certified_aua vs compute_49f_broader_custody), (iii) any residual. Do NOT commit, do NOT S3-deploy, do NOT touch the live artifact -- this is a local dry-run + diff only. Route the delta figure to 1.0.0_SA_CTO~B (CC 2.0.0_SA_COO~B). CTO~B takes the now-vs-WS-F timing decision to Andrew WITH this number.</step>
    <step>Phase 1 -- STAGE 1, DISPATCH_HELD on Andrew sign-off. [SPEC CORRECTED 2026-05-20 per the .026 Phase-0 findings -- see amendment block.] Apply the v0.8 taxonomy to build_legacy_compat_emit.py via TWO changes (NOT an SMA-term removal -- Phase 0 Finding 1 established the legacy emitter's non_model_aum at L619 is ALREADY SMA-inclusive; there is no `- sma_aua` term to drop, that part of the original spec is a verified no-op, component delta $0): (1) ALIGN THE 1b BASIS to certified_aua (full Black Diamond book) per .025, matching mdpf_aggregate_aua.py -- net effect ~+$12.5M; (2) REMOVE etf_public_residual / Cohort 0 from enterprise_total -- v0.8/.024 ruled Cohort 0 audit-only, but the legacy emitter currently sums it INTO enterprise_total (~$91.33M on RPS-coverage dates); this is the dominant component. Net live-page headline delta: -$78,832,234.94 on 2026-05-18 (~$0 to +$5M on pre-RPS-coverage historical dates). Phase-0 brief: docs/briefs/mdpf-assets-026-phase0-legacy-emit-delta-20260520.md (commit 40c74ef4e).</step>
    <step>Phase 2 -- fixture / reconciliation. Update any build_legacy_compat_emit.py fixtures to v0.8 baselines. Cross-validate: legacy non_model_assets.json totals should now reconcile to-the-cent against mdpf_aggregate_aua.py platinum output for the same date (both v0.8). Add a methodology_version="v0_8_ruling2" stamp to the legacy artifact for consumer-side discontinuity detection (consistent with .022(a) + .016).</step>
    <step>Phase 3 -- DS commit + S3 deploy cycle per Rule 13: .tools/ds-commit-gate.sh -> .tools/safe-commit.sh with agent --author -> push CLOUD -> aws s3 cp the updated script to the canonical s3:// gold-scripts path -> comp-pipescript deployed MATCH. Then trigger / await the legacy emit so non_model_assets.json refreshes to v0.8.</step>
    <step>Phase 4 -- empirical verification + RAVC2. AC1-AC5 transcripts; RAVC2 to 2.0.0_SA_COO~B CC 1.0.0_SA_CTO~B.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC0">Phase 0 delta quantified: exact total live-page AUA delta reported, component-broken-out (SMA double-count / 1b basis change / residual), routed to CTO~B. [Stage 0 -- gates Andrew decision; satisfiable before Stage 1 dispatch.]</ac>
    <ac id="AC1">build_legacy_compat_emit.py enterprise_total EXCLUDES etf_public_residual / Cohort 0 (v0.8 audit-only ruling) -- the dominant Phase-0-quantified component; Cohort 0 still emitted as an audit field, not summed into the headline.</ac>
    <ac id="AC2">1b basis aligned to certified_aua (full Black Diamond book) per .025, matching mdpf_aggregate_aua.py.</ac>
    <ac id="AC2b">No SMA-term change applied (Phase-0 Finding 1: legacy non_model_aum L619 is already SMA-inclusive -- verified no-op; AC2b is satisfied by confirming the emitter is left SMA-inclusive, no regression).</ac>
    <ac id="AC3">Legacy non_model_assets.json totals reconcile TO-THE-CENT against mdpf_aggregate_aua.py platinum output for the same date (both v0.8). Transcript captured.</ac>
    <ac id="AC4">methodology_version="v0_8_ruling2" stamped on the legacy artifact.</ac>
    <ac id="AC5">DS commit + S3 deploy per Rule 13: ds-commit-gate.sh -> safe-commit.sh agent --author -> push CLOUD -> aws s3 cp -> comp-pipescript deployed MATCH. No console-side shortcuts. No emoji. `from __future__ import annotations` first import. Session log with Compiler Tools section.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>comp-pipescript io build_legacy_compat_emit (column-gap check); comp-blast build_legacy_compat_emit (downstream consumers of non_model_assets.json -- the live page).</before_write>
    <before_commit>.tools/ds-commit-gate.sh per Rule 14.</before_commit>
    <after_commit>comp-pipescript deployed MATCH post-aws-s3-cp.</after_commit>
  </compiler_tools_mandate>

  <out_of_scope>
    Re-deciding the v0.8 methodology (already Andrew-ruled). The WS-F Phase-3 legacy-page replacement (separate workstream; this TO is the interim-correctness path if Andrew chooses now-over-WS-F). mdpf_aggregate_aua.py (already .024-corrected; this TO brings the legacy emitter to match it).
  </out_of_scope>

  <deliverables>
    - Phase 0: delta-quantification dry-run report routed to CTO~B. DONE 2026-05-20 (DS~B, brief docs/briefs/mdpf-assets-026-phase0-legacy-emit-delta-20260520.md, commit 40c74ef4e).
    - Stage 1: build_legacy_compat_emit.py at v0.8 taxonomy; non_model_assets.json refreshed; fixtures re-baselined; commit on CLOUD + S3 deploy + MATCH; RAVC2.
  </deliverables>

  <amendment id="A1" date="2026-05-20" by="2.0.0_SA_COO~B">
    SPEC CORRECTION per the .026 Phase-0 delta-quantification findings (DS~B, brief docs/briefs/mdpf-assets-026-phase0-legacy-emit-delta-20260520.md, commit 40c74ef4e). The original Phase-1 spec ("mirror the .024 fix -- drop the `- sma_aua` term") was based on a mis-read of build_legacy_compat_emit.py L499-503. Phase 0 established:
    - Finding 1: NO SMA double-count in the legacy emitter. The emitted non_model_aum (L619) is ALREADY SMA-inclusive -- there is no `- sma_aua` term to drop. The original spec's SMA-term removal is a verified no-op (component delta $0).
    - Finding 2: the dominant component is Cohort 0. The live legacy enterprise_total currently INCLUDES etf_public_residual (~$91.33M on RPS-coverage dates); v0.8/.024 ruled Cohort 0 audit-only. Removing it is -$91.33M; the 1b basis change is only +$12.5M.
    - Net: applying v0.8 to the legacy emitter moves the LIVE Model Portfolios headline by -$78,832,234.94 on 2026-05-18 (the live page is currently OVER-stating by that amount), ~$0 to +$5M on pre-RPS-coverage historical dates.
    Phase 1 step + AC1 + AC2b corrected accordingly: the Stage-1 change is (1) 1b basis -> certified_aua, (2) Cohort 0 OUT of enterprise_total -- NOT an SMA-term removal. Stage 1 remains DISPATCH_HELD on Andrew sign-off (CTO~B carries the now-vs-WS-F timing decision to Andrew WITH the -$78.83M figure).
  </amendment>
</task_order>
