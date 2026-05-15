<task_order>
  <metadata>
    <id>ADHC_BPMVH.001</id>
    <slug>dsc-fresh-header-supplement-d-min</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 ~18:35Z by COO per Andrew direct product-strategy ratify (via DS~C surface): Q1 D-min YES + Q2 Cottonwood Option (a) ship-before-Cottonwood. 3-project ADHC bundle (LEDGEH + FECACHE_COHERENCE + BPMVH) lands before Cottonwood live ship.</dispatch_unblock_condition>
    <project_code>ADHC_BPMVH</project_code>
    <priority>P1 — Andrew direct investigation surface ratified by CTO v0.2 PRD; partner-demo headline-fresh requirement</priority>
    <sla>~1h wall post-dispatch-unblock</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_BPMVH.md (CTO canonicalize pending via git mv from docs/briefs/inflection-bronze-pmv-hybrid-proposal-20260514.md)</ref>
    <ref type="investigation_anchor">DS~C $156K investigation close (ADVI_INFFIN.015 RAVC2) — decomposition: $50K (1 new HH 1366) + $106,715.66 (13 same-day-rebalance accounts) = $156,715.66 same-day bronze-vs-pmv gap; root cause two Orion endpoints with different trade-settlement reporting latency</ref>
    <ref type="cto_ratify">CTO MCP 2026-05-14 ~18:0X — D1 SEQUENCED / D2 NO BACKFILL / D3 ADDITIVE SCHEMA + 2 discipline asks / D4 NEW INF_D_00e script. AC8 Cottonwood fixture added.</ref>
    <ref type="andrew_direct">2026-05-14 PM: "we definitely need to show current state whenever it comes to headline/global AUA numbers, its just if we have to get clever for the rest."</ref>
    <ref type="defense_in_depth">Sister projects ADHC_LEDGEH + ADHC_FECACHE_COHERENCE — 3-project ADHC defense-in-depth corpus; bundle materialization with NMCOHT 2e45c8e25 + book.json augment ff00b6987 per AE 0.6.1 chain-fire coord</ref>
    <ref type="cottonwood_soft_gate">Andrew product-strategy ratify on FIRMSEP.10 Cottonwood live-ship sequencing — primary risk-window beneficiary; CTO + COO lean Option (a) ship-before-Cottonwood</ref>
  </references>

  <context>
    Two Orion API endpoints feed the Inflection portal at different trade-settlement latencies:
    - **bronze `assets.csv`**: CSV daily-AUM export, dropped to S3 ~morning; captures same-day rebalance trades faster
    - **silver `positions_mv`**: REST `/Portfolio/Clients/{cid}/Assets/{date}` per-client iteration → silver; reconciliation-stable but lags ~24h on same-day trades

    Empirical 2026-05-14: bronze $203,339,876.18 vs pmv $203,183,160.52 = $156,715.66 gap (0.077% firm AUA). Decomposition: $50K from 1 new HH 1366 (bronze captured today; pmv not yet ingested) + $106,715.66 from 13 same-day-rebalance accounts (verified on account 488: bronze shows post-rebalance IEFA/SPYM/BIV; pmv still shows 5/13 BAGIX/HTRB/BSIIX).

    Andrew direct: "headline/global AUA must show current state, get clever for the rest." → D-min sidecar covers the headline-fresh requirement with low blast radius + Andrew's stated priority. D-max (~1-2d INF_B_00 reconciliation) gates on 1-2 weeks of D-min daily-delta observability data — earn-the-right discipline before broader reconciliation rollout.

    Per CTO D4 ratify: D-min implementation is a NEW `INF_D_00e.fresh_header_supplement.py` script (NOT inline in INF_D_04). Marginal authoring cost ~15min more than inline; structural separation pays off for D-max migration + parallel chain execution + observability (separate gold_prof metric) + empirical-isolation testing.
  </context>

  <objective>
    Ship D-min implementation: new gold script `data/orion/scripts/gold/INF_D_00e.fresh_header_supplement.py` that reads bronze `assets.csv` directly, computes `Σ Position MV` filtered to Inflection reps, emits `platinum/firm/header_metrics_fresh.json` with `total_aua_fresh` field + `_meta.source_distribution_manifest` per CTO D3 discipline asks. Per AC8 Cottonwood fixture: emit `_meta.pmv_present: false` when bronze present + pmv absent.
  </objective>

  <scope>
    <files>
      <file action="create">data/orion/scripts/gold/INF_D_00e.fresh_header_supplement.py — new gold script (~50 LOC; `from __future__ import annotations` first import per CLAUDE.md Rule 15)</file>
      <file action="modify">data/orion/scripts/dispatch.sh (or orion-gold-dispatch.sh CHAIN_GOLD_D) — add INF_D_00e to chain definition; coord with AE 0.6.1 on sequencing position</file>
      <file action="readonly_reference">data/orion/scripts/gold/INF_D_04.client_portal_summary.py — bronze fallback pattern at lines 91-93 for `bronze/orion-api/{household,performance,activity}/latest.csv` (existing pattern; D-min uses same bronze-read pattern but to fresh-supplement not fallback)</file>
      <file action="readonly_reference">data/orion/scripts/gold/INF_D_08.nmec_nmnc_nna.py — existing bronze-reader; reference for bronze-load pattern (note: DS~D's 2e45c8e25 source-switched INF_D_08 transactions.csv → accounts_v2; this is DIFFERENT read — assets.csv per Inflection rep filter)</file>
    </files>
  </scope>

  <phase id="1" when="before INF_D_00e creation">
    <step>
      <run>comp-pipescript io INF_D_00e (will return MISSING — script doesn't exist yet; expected)</run>
      <expect>MISSING — script not yet authored. Document baseline for post-creation compare.</expect>
      <if_mismatch>If script already exists (unexpected), surface to COO + verify no concurrent authoring.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_D_04.client_portal_summary (reference for upstream bronze-fallback pattern lines 91-93)</run>
      <expect>Confirms INF_D_04 already reads bronze paths via fallback. D-min uses same I/O pattern but writes new artifact, not augments existing.</expect>
    </step>
    <step>
      <run>S3 empirical pull: aws s3 cp s3://opal-data-inf/bronze/orion-api/2026-05-14/assets.csv - | head -3; aws s3 cp s3://opal-data-inf/silver/api_dims/positions_mv/snapshot_date=2026-05-14/data.parquet - --quiet | python -c "import pandas as pd; import sys; df = pd.read_parquet(sys.stdin.buffer); print(df.shape, df.columns.tolist()[:8])"</run>
      <expect>Verify both endpoints empirically reachable + schema known. Confirms bronze has `account_id`, `Position MV` (or analogue); pmv has `market_value`. Document column-name mapping for INF_D_00e.</expect>
      <if_mismatch>If bronze schema unexpected, surface to COO + AE 0.6.1; may need Orion API contract review.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="INF_D_00e creation">
    <step>
      <run>Create `data/orion/scripts/gold/INF_D_00e.fresh_header_supplement.py` with:
        - `from __future__ import annotations` FIRST import (CLAUDE.md Rule 15)
        - Read bronze `s3://opal-data-inf/bronze/orion-api/{date}/assets.csv` filtered to Inflection reps via accounts_v2 join
        - Compute `Σ Position MV` (firm-level total)
        - Emit `platinum/firm/header_metrics_fresh.json` with shape:
          ```json
          {
            "total_aua_fresh": 203339876.18,
            "_meta": {
              "source": "bronze",
              "bronze_date_used": "2026-05-14",
              "pmv_present": true,
              "pmv_total_aua": 203183160.52,
              "delta_vs_pmv": 156715.66,
              "delta_pct": 0.077,
              "source_schema_version": "bronze_d_min_v1"
            }
          }
          ```
        - AC8 Cottonwood fixture: when bronze present + pmv absent → emit with `_meta.pmv_present: false`, `pmv_total_aua: null`, `delta_vs_pmv: null`, `delta_pct: null`
        - Emit per-partition source-distribution manifest at `platinum/firm/_meta/reconciliation_summary_{date}.json` per CTO D3 discipline ask 2</run>
      <expect>~50 LOC implementation. Docstring documents `source` enum (`bronze` / `bronze_only_no_pmv` for AC8). No emoji per CLAUDE.md.</expect>
    </step>
    <step>
      <run>Local dry-run: `python data/orion/scripts/gold/INF_D_00e.fresh_header_supplement.py --date 2026-05-14 --dry-run` (or equivalent invocation pattern per dispatch.sh)</run>
      <expect>Sentinel: `|total_aua_fresh - bronze raw Σ Position MV| < $0.50`. Empirical match to direct bronze sum confirms no aggregation grain bug.</expect>
      <if_mismatch>Document divergence + investigate before commit.</if_mismatch>
    </step>
    <step>
      <run>Add INF_D_00e to chain definition in `data/orion/scripts/dispatch.sh` (or `orion-gold-dispatch.sh` CHAIN_GOLD_D per current sequencing)</run>
      <expect>Sequencing position: BEFORE INF_D_04 (so INF_D_04 can optionally read header_metrics_fresh.json if needed in future — not used today) OR PARALLEL to INF_D_04 (independent of pmv chain). Coord with AE 0.6.1 on exact position.</expect>
    </step>
  </phase>

  <phase id="3" when="before commit">
    <step>
      <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00e.fresh_header_supplement.py</run>
      <expect>3 checks PASS: py_compile + ds-precommit-check.py + ruff py39 0.15.11.</expect>
      <if_mismatch>Fix surfaced issues before commit. Common: missing `from __future__ import annotations`; PEP-604 union syntax incompatibilities; ruff lint violations.</if_mismatch>
    </step>
    <step>
      <run>.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>" -m "..." -- data/orion/scripts/gold/INF_D_00e.fresh_header_supplement.py data/orion/scripts/dispatch.sh</run>
      <expect>Commit + safe-deploy SHA-MATCH per CLAUDE.md Rule 13.</expect>
    </step>
  </phase>

  <phase id="4" when="after commit">
    <step>
      <run>comp-pipescript deployed INF_D_00e</run>
      <expect>MATCH — runner has the code at expected SHA.</expect>
      <if_mismatch>Block on AE 0.6.1 chain re-fire OR investigate S3 sync drift.</if_mismatch>
    </step>
    <step>
      <run>AE 0.6.1 chain-fire bundled materialization (per COO MCP 18:04Z) — NMCOHT 2e45c8e25 + book.json augment ff00b6987 + this D-min INF_D_00e</run>
      <expect>Single chain run materializes all 3. Sentinel post-chain: `aws s3 cp s3://opal-data-inf/platinum/firm/header_metrics_fresh.json - | jq '._meta.source, ._meta.pmv_present, ._meta.delta_vs_pmv'` returns expected values.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DE 0.4 (FE wiring follow-on)</run>
      <expect>Evidence-bearing close: commit SHA + safe-deploy log + post-chain S3 sentinel check + reconciliation_summary manifest empirical.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: New gold script `INF_D_00e.fresh_header_supplement.py` created with `from __future__ import annotations` first import + ~50 LOC implementation
    AC2: Emits `platinum/firm/header_metrics_fresh.json` with `total_aua_fresh` + `_meta` block per spec
    AC3: Emits per-partition reconciliation_summary manifest at `platinum/firm/_meta/reconciliation_summary_{date}.json` per CTO D3 discipline ask 2
    AC4: `source` enum documented inline in script docstring per CTO D3 discipline ask 1
    AC5: Sentinel `|total_aua_fresh - bronze raw Σ Position MV| < $0.50` PASS in local dry-run
    AC6: AC8 Cottonwood fixture: when bronze present + pmv absent → emit `_meta.pmv_present: false` + null delta fields
    AC7: ds-commit-gate.sh + safe-deploy.sh PASS
    AC8: Cottonwood fixture verified via local dry-run with synthetic pmv-absent input (or empirical when Cottonwood bronze first lands)
    AC9: comp-pipescript deployed MATCH post-commit
    AC10: AE 0.6.1 chain-fire materialization successful; S3 sentinel post-chain confirms expected emit
    AC11: RAVC2 evidence to COO + CC CTO + DE 0.4 with commit SHA + S3 paths + dry-run sentinel output
    AC12: NO behavior change on existing artifacts (`header_metrics.json` etc. untouched); D-min is purely additive
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (comp-pipescript io baseline + INF_D_04 reference) + Phase 4 (comp-pipescript deployed). ds-commit-gate.sh + safe-deploy.sh per Phase 3.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: Andrew product-strategy ratify on dispatch (TO is `staged + dispatch_held=true` until Andrew GO). CTO PRD canonicalize via git mv (separate non-blocking; can ship TO impl before canonicalize lands).
    PARALLEL-OK: 3-project ADHC defense-in-depth corpus (LEDGEH AE 0.7 + FECACHE_COHERENCE DE 0.4 + BPMVH DS~C). Bundle chain-fire materialization with NMCOHT 2e45c8e25 + book.json augment ff00b6987 per AE 0.6.1 coord.
    FE WIRING: DE 0.4 lane — AdvisorPublicProfile.tsx (or header AUA tile component) reads `total_aua_fresh` with fallback to existing `total_aua`. Single conditional. Schedule post DS~C ship + chain materialization.
    PORTAL SUBMODULE: DT 0.4 push post DE 0.4 FE wiring ship.
    D-MAX FOLLOW-ON: gates on 1-2 weeks of D-min daily-delta observability data + Andrew second ratify. NOT in this TO's scope.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>D-min is additive; no existing artifact rewritten. Materializes on next chain run.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. New gold script `data/orion/scripts/gold/INF_D_00e.fresh_header_supplement.py`
    2. dispatch.sh / orion-gold-dispatch.sh CHAIN_GOLD_D updated to include INF_D_00e
    3. ds-commit-gate + safe-deploy PASS
    4. Post-chain S3 sentinel verification (header_metrics_fresh.json + reconciliation_summary manifest)
    5. Session log entry under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-14/DS_C_session?_bpmvh_d_min_ship.md`
    6. RAVC2 to COO + CC CTO + DE 0.4 with AC1-12 evidence
  </deliverables>

  <ravc>DS~C RAVC2 to COO + CC CTO + DE 0.4 on AC1-12 PASS. FE wiring follows in DE 0.4 lane post chain materialization. D-max conditional follow-on gates on 1-2 wk D-min observability.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"`.

    **No PII discipline concerns:** firm-aggregate emit only; no per-HH or per-account identifying info in `header_metrics_fresh.json`. Reconciliation_summary manifest emits per-source aggregate stats (row counts, $ totals); no HH-grain.

    **AC8 Cottonwood fixture importance:** Cottonwood will onboard with bronze-only-no-pmv initial state (positions_mv silver requires several days of REST pulls to build). D-min must gracefully handle bronze-only emit per CTO D3 + AC8. Local dry-run with synthetic pmv-absent input is sufficient; empirical Cottonwood verification on first Cottonwood bronze landing.

    **Bundle materialization opportunity:** per AE 0.6.1 MCP 18:04Z, chain-fire bundling NMCOHT (DS~D 2e45c8e25) + book.json augment (DS~C ff00b6987) + this D-min ship reduces chain-cost + aligns materialization with Cottonwood SOFT-GATE ship-before-Cottonwood lean.

    **D-max scope is OUT-OF-SCOPE for this TO.** D-max gates on 1-2 weeks of D-min daily-delta observability data + Andrew second ratify per CTO D1 sequenced ratify. Specifically: if `delta_vs_pmv` is consistently < $200K firm-wide for 1-2 weeks, D-max may not justify scope; if multi-million $ deltas surface, D-max becomes mandatory. **Don't ship D-max blind.** Earn the right with D-min observability.

    **Primary `_meta.bronze_date_used` fix obsolescence:** DS~D's `2e45c8e25` source-switch on INF_D_08 to `accounts_v2.account_start_date` likely fully obsoletes the lifecycle-classification mechanism the `_meta.bronze_date_used` fix from ADVI_INFFIN.015 was documenting. Memory bank entry `feedback_date_asymmetry_cross_artifact_aua.md` revised to capture obsolescence-by-supersession lesson at DS~C's bench-clear cadence.
  </notes>
</task_order>
