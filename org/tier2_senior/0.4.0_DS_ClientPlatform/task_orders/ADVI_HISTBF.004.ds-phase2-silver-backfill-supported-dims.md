<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_HISTBF.004</id>
    <project>ADVI_HISTBF</project>
    <title>Phase 2 — Silver backfill for SUPPORTED dims (positions_mv + assets_v2); historical bronze → silver conversion</title>
    <issued_to>0.4.0_DS_ClientPlatform + 0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-30</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>1-3d (depends on silver builder investigation outcome + date-range scale)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_HISTBF.md §3 Phase 2</ref>
    <ref type="phase1_gate">ADVI_HISTBF.003 RAVC4 (SUPPORTED dims bronze complete to earliest-available-date)</ref>
    <ref type="bronze_output">s3://opal-data-inf/bronze/orion-api-v2/&lt;date&gt;/&lt;dim&gt;.parquet (Phase 1 output)</ref>
    <ref type="silver_builder">data/orion/scripts/bronze/ (INF_B_00 post-DIAGFIX.012 refactor 4bc5381b2 — positions_mv pass-through + accounts_v2 JOIN; net -93 LOC)</ref>
    <ref type="silver_builder_daily">data/orion/scripts/silver/ (convert_orion_to_silver.py or equivalent — daily run pattern; Phase 2 extends to date-range iteration)</ref>
    <ref type="eligibility_matrix">docs/data/inflec_histbf_eligibility_matrix.md (HISTBF.001 output — SUPPORTED: positions_mv, assets_v2; PARTIAL: billing, activity, performance; CURRENT-ONLY: accounts_v2, household_rep_mapping, household)</ref>
    <ref type="diagfix012">DIAGFIX.012 Phase 5 (INF_B_00 refactor; positions_mv pass-through replaces TRN-as-price; validates to ~$197.36M dry-run AUA)</ref>
  </references>

  <context>
    Phase 1 (HISTBF.003) produces historical bronze partitions at s3://opal-data-inf/bronze/orion-api-v2/&lt;date&gt;/&lt;dim&gt;.parquet for SUPPORTED dims (positions_mv, assets_v2) back to silver/transactions origin (2020-05-26). Phase 1 scale: ~450K REST calls, ~125h, multi-day.

    Phase 2 converts those historical bronze partitions through the silver layer. The existing daily silver runner processes current-day data; Phase 2 must iterate over the full historical date range and produce silver outputs for each date.

    Key open question (must resolve in Phase 0 of this TO): does the post-DIAGFIX.012 INF_B_00 / silver builder handle arbitrary historical date partitions, or does it assume "today"? If it hardcodes date logic, extension is required before Phase 2 can run.

    PARTIAL dims (billing, activity, performance) are OUT OF SCOPE for this TO. DS~B is conducting deeper research on Envision endpoint behavior and rep attribution for those dims. Phase 2b will cover PARTIAL dims after DS~B research closes. This TO focuses on the two SUPPORTED REST dims only.

    CURRENT-ONLY dims (accounts_v2, household_rep_mapping, household): no historical data accessible; document as "current snapshot is earliest available" — no silver backfill action needed.
  </context>

  <scope>

  ## Phase 0 — Silver builder investigation (before any code write)

    1. **Audit silver builder historical partition support**.
       - Read data/orion/scripts/bronze/INF_B_00.py (post-DIAGFIX.012 4bc5381b2) and any silver-layer convert scripts.
       - Run comp-pipescript io on the silver builder: identify all date-related inputs (hardcoded TODAY, partition key construction, bronze read path pattern).
       - Determine: does the builder accept a --date YYYY-MM-DD flag (or equivalent) to process an arbitrary historical partition? Or does it assume current?
       - Document finding in Phase 0 session log: NATIVE (no changes needed) or EXTENSION-REQUIRED (add --date flag + historical partition read logic).

    2. **Silver output path audit**.
       - Confirm where silver outputs land for current daily runs (s3://opal-data-inf/silver/.../).
       - Verify historical date partitions write to the same path structure (s3://opal-data-inf/silver/&lt;dim&gt;/&lt;date&gt;/ or equivalent) without overwriting current-day state.
       - If path structure is ambiguous, document + resolve before writing any historical silver.

    3. **Gold chain dependency audit**.
       - Run comp-blast on silver outputs for positions_mv + assets_v2 to identify downstream gold consumers.
       - Determine: does the gold chain (inf-gold-dispatch.sh) need to re-run per historical date, or does it consume silver as a cumulative input where a single re-run at the end suffices?
       - This determines whether Phase 2 is "silver only" or "silver + gold re-run" scope.

  ## DS sub-tasks (.004a — `0.4.0_DS_ClientPlatform`)

    4. **Silver builder extension (if EXTENSION-REQUIRED)**.
       - Add --date YYYY-MM-DD flag to silver builder (or equivalent date-override mechanism).
       - Builder reads bronze partition at s3://opal-data-inf/bronze/orion-api-v2/{date}/{dim}.parquet.
       - Writes silver output to correct historical partition path.
       - Preserves existing "no --date = today" behavior (no regression on daily run).
       - from __future__ import annotations required; ds-commit-gate.sh clean.

    5. **Date-range iteration script** at data/orion/scripts/silver/run_silver_backfill.py (new):
       - Accepts --start YYYY-MM-DD, --end YYYY-MM-DD, --dims [positions_mv, assets_v2, ...]
       - Iterates date range; for each date, checks if bronze partition exists in S3; if yes, invokes silver builder for that date; if no, skips with log entry.
       - Tracks completed dates to support --resume (skip already-converted silver partitions).
       - Emits per-date completion log to stdout (plain ASCII; no emojis).
       - NOT rate-limited (silver conversion is local compute + S3 read/write; no ORIAPI calls).

    6. **CURRENT-ONLY dim documentation**. Write or update docs/data/inflec_histbf_recovery_protocol.md (or a new docs/data/inflec_histbf_silver_backfill_scope.md) with:
       - accounts_v2, household_rep_mapping, household: "current snapshot is earliest available; no silver backfill action; daily dispatch provides ongoing coverage."
       - PARTIAL dims: "pending DS~B research; covered by HISTBF.Phase2b TO after research closes."

    7. **Silver output validation**. After backfill run completes for each SUPPORTED dim:
       - Row count plausibility check: compare historical silver row counts against current-day row counts × expected date ratio.
       - AUA spot-check: sample 3 historical dates; verify managed_value sums are non-zero and plausible (don't need to match Andrew's targets — just non-null, non-zero, monotonically reasonable).
       - comp-validate on silver output artifact (if validator config exists for silver layer).
       - Document in session log.

    8. **Phase 2 close report**. At completion:
       - SUPPORTED dims silver complete: date range covered, row counts, S3 paths.
       - CURRENT-ONLY dims documented.
       - PARTIAL dims deferred to Phase 2b (DS~B gate).
       - Gold chain re-run recommendation (if Phase 0 audit shows gold re-run needed).
       - Save to org/tier2_senior/0.4.0_DS_ClientPlatform/logs/&lt;date&gt;/histbf_phase2_close.md.

    9. **Pre-commit gate + future annotations** per CLAUDE.md Rules 14 + 15 on all .py edits.

  ## AE sub-tasks (.004b — `0.6.1_AE_PartnerETL`)

    10. **Chain reg verification**. Confirm orion-gold-dispatch.sh CATALOG entries accommodate historical silver partitions as inputs. If gold chain needs re-run post-silver-backfill (per Phase 0 audit §3), confirm dispatch mechanism and IAM for a historical-range chain run.

    11. **S3 path conflict check**. Before DS runs silver backfill: verify no existing silver partitions at the historical date paths would be overwritten by the backfill. If conflicts exist, document + resolve protocol with DS before write starts.

    12. **Coordinate Phase 2b scoping with DS~B**. When DS~B PARTIAL research closes, AE 0.6.1 confirms: (a) Envision dim silver builder extension needed? (b) Monthly range job outputs compatible with existing silver schema? Feed this into COO for Phase 2b TO authoring.

  </scope>

  <acceptance_criteria>
    1. Phase 0 silver builder audit complete: NATIVE or EXTENSION-REQUIRED verdict documented in session log.
    2. Silver output path confirmed non-conflicting with daily run outputs.
    3. Gold chain dependency audit complete: gold re-run scope clarified (silver-only vs silver+gold).
    4. Silver builder extended with --date flag if EXTENSION-REQUIRED; existing daily behavior preserved (regression check).
    5. run_silver_backfill.py authored + pre-commit-gate clean.
    6. Silver backfill executed for positions_mv + assets_v2 for full date range (2020-05-26 → Phase 1 end date).
    7. CURRENT-ONLY dims documented in scope doc; no silver backfill attempted for those dims.
    8. Silver output validation passes (row count plausibility + AUA spot-check on 3 dates).
    9. Phase 2 close report written with S3 paths + row counts + gold re-run recommendation.
    10. RAVC4 to COO + CTO with: silver builder verdict (NATIVE/EXTENSION), run_silver_backfill.py path, S3 silver partition count for each dim, 3-date AUA spot-check results, gold chain re-run recommendation.

    Phase 2b (PARTIAL dims) is a separate TO gated on DS~B research close. This TO closes on SUPPORTED dims only.
  </acceptance_criteria>

  <data_reprocess_scope>
    <no_reprocess_needed>Phase 2 writes NEW historical silver partitions not previously produced; no existing silver data is overwritten or semantically altered; daily silver run is additive (existing daily outputs unchanged); downstream gold consumers read current-state silver and are unaffected until a deliberate gold re-run is triggered post-Phase-2</no_reprocess_needed>
  </data_reprocess_scope>

  <execution_gate>
    <hard_gate>HISTBF.003 RAVC4 (Phase 1 bronze backfill complete for SUPPORTED dims). Phase 2 execution cannot begin until bronze historical partitions exist at s3://opal-data-inf/bronze/orion-api-v2/&lt;date&gt;/&lt;dim&gt;.parquet for the full target date range.</hard_gate>
    <soft_gate>DIAGFIX.012 Phase 5 RAVC4 (confirms INF_B_00 refactor is validated; silver builder starting point is clean). Phase 0 audit should run after Phase 5 confirms clean.</soft_gate>
    <parallel_ok>Phase 0 investigation (§1-3) + silver builder extension authoring (§4) + run_silver_backfill.py authoring (§5) MAY proceed in parallel with Phase 1 execution. Code can be written and tested locally while Phase 1 bronze fills in. Actual backfill execution (§6) gates on HISTBF.003 close.</parallel_ok>
  </execution_gate>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-pipescript io [silver builder script] — identify date inputs, bronze read path, silver write path</check>
      <check>comp-blast [silver output artifacts] — identify gold consumers downstream</check>
    </before_write>
    <before_commit>
      <check>.tools/ds-commit-gate.sh on all .py edits (silver builder extension + run_silver_backfill.py)</check>
      <check>from __future__ import annotations on all new/modified silver scripts (CLAUDE.md Rule 15)</check>
    </before_commit>
    <after_commit>
      <check>comp-pipescript deployed [silver builder] MATCH after S3 upload</check>
      <check>AE 0.6.1 chain reg confirmation (CATALOG entries for historical silver partition paths)</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_artifacts>
      <artifact>s3://opal-data-inf/bronze/orion-api-v2/&lt;date&gt;/&lt;dim&gt;.parquet (Phase 1 output; Phase 2 reads)</artifact>
      <artifact>s3://opal-data-inf/silver/&lt;dim&gt;/&lt;date&gt;/ (Phase 2 output; gold chain reads)</artifact>
      <artifact>data/orion/scripts/silver/run_silver_backfill.py (NEW DS script)</artifact>
      <artifact>data/orion/scripts/bronze/INF_B_00.py (DS extends if EXTENSION-REQUIRED; AE confirms chain reg)</artifact>
    </shared_artifacts>
    <coordination_protocol>
      DS leads Phase 0 audit + silver builder extension + backfill execution. AE confirms chain reg + S3 path non-conflict before DS write starts. DS~B PARTIAL research feeds into Phase 2b (separate TO; COO authors after DS~B closes). Direct MCP DS + AE for S3 path + chain reg questions; COO routes only if blocked.
    </coordination_protocol>
  </cross_domain_coordination>
</task_order>
