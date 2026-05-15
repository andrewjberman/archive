<task_order>
  <metadata>
    <id>ADVI_TXNAMG.002</id>
    <slug>dsb-consumer-migration</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_TXNAMG</project_code>
    <priority>P1 — completes the ADVI_DWSPLT TO-3 consumer migration; INF_D_05 is a live 7-day-stale partner-facing surface (InflectionInsightsPanel). Phases A+B run immediately, parallel to TO-1.</priority>
    <sla>~4-6h wall for Phases A+B. Phase C is a short confirmation pass post-TO-3 ship.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_TXNAMG.md (PRD v0.1, commit e7fecbf93) — §2.4 consumer state, §4.4 complete consumer sweep table, §6 TO-2, §7-Q1 (RULED latest-snapshot, f6a13a672).</prd>
    <evidence>COO topology brief docs/briefs/inf-infinc006-topology-coo-packet-20260515.md Addendum A (7cb7a7657) — INF_D_05 max_date 2026-05-08 / 7d stale empirical.</evidence>
  </references>

  <context>
    ADVI_DWSPLT TO-3 migrated 6 silver/transactions consumers + the txn_cache_reader path to the canonical camelCase Rule-17 schema, but missed INF_D_05.activity_scan and left INF_D_00.portal_aggregates migrated-partial. The COO consumer sweep (PRD §4.4) is the complete map: 10 real consumers — 8 SHIELDED, INF_D_05 UNMIGRATED, INF_D_00 MIGRATED-PARTIAL. This TO closes that gap so every consumer is on the canonical schema before the amalgamating writer (TO-3) ships. The amalgamated silver is a superset of the current REST-only camelCase schema, so a consumer that reads the REST canonical columns (transDate/accountId/id) is correct against both pre- and post-TO-3 silver — Phases A+B are testable NOW against writer #2's current daily camelCase output and do not wait on TO-3.
  </context>

  <objective>
    Every silver/transactions consumer reads the canonical camelCase schema with a source-select that lands on the live full-history snapshot — no concat-all of stale partitions, no snake-schema requirement, no masked bronze-fallback.
  </objective>

  <scope>
    <phase id="A" gate="none — start immediately">
      INF_D_05.activity_scan.py migration. `_load_txn_partition` (lines 168-201) currently requires snake_case account_id/trans_date/trans_id — it cannot read the camelCase canonical partition (return None) nor the writer-#3 null-trans_date partitions (dropna drops all rows), so it runs on one surviving old snapshot frozen at 2026-05-08 (7 days stale; runner log chain_full_20260515_060048, INF_D_05a 07:08:37Z). Migrate it to a canonical camelCase source-select — the Path A.2 pattern (mtime-sort + canonical-col check, latest full-history snapshot), NOT concat-all of ~1,515 partitions. Reference the shielded consumers' source-select (INF_B_02 / INF_C_01 / txn_cache_reader) as the working pattern.
      §7-Q1 RULED latest-snapshot (Andrew via CTO 2026-05-15, commit f6a13a672 — PRD §7-Q1). INF_D_05 is the canonical concat-all reader §7-Q1 was about; the ruling CONFIRMS this phase's working directive — migrate to a latest full-history snapshot source-select. Concat-all of the ~1,515 per-date partitions is rejected; the superseded partitions go inert (not re-emitted, not deleted). No amendment — proceed exactly as written.
    </phase>
    <phase id="B" gate="none — start immediately">
      INF_D_00.portal_aggregates verify-and-clean. It `_newest()`-source-selects silver but expects a snake "Phase-A" schema (trans_date/trans_amount/units/nav_price); under post-TO-3-DWSPLT camelCase silver it likely fails the column check (:444 WARN) and silently falls back to reading bronze/transactions/ directly (:448). VERIFY empirically which path it takes today. Then either fix the column mapping so the silver-read path works on canonical camelCase, OR remove the dead fallback if INF_D_00 should read silver canonically. Goal: INF_D_00's silver-read path is confirmed-live, not masked.
    </phase>
    <phase id="C" gate="TO-3 ship">
      8-shielded-consumer confirmation-run. After TO-3 (the amalgamating writer) ships, confirmation-run the 8 SHIELDED consumers (INF_A_-1, INF_A_00, INF_A_03, INF_B_02, INF_C_01, INF_D_02, INF_D_06, INF_build_canonical_prices) — verify each produces non-zero output reading the amalgamated silver. No code change expected (amalgamated = superset; canonical cols still present) — this is a regression check, not a migration.
      FOLDED — TO-5 housekeeping (§7-Q1 latest-snapshot disposition). The PRD §6 TO-5 candidate (stale silver-partition disposition) collapsed to housekeeping under the §7-Q1 ruling and is folded here per COO/CTO 2026-05-15 — not authored as a standalone TO. As part of this confirmation pass: confirm NO concat-all-per-date reader remains anywhere in the silver/transactions consumer set — INF_D_05 (Phase A) was the last one; the 8 shielded + INF_D_00 must all be latest-snapshot source-selects. The ~1,515 superseded per-date silver/transactions/ partitions are left INERT — not re-emitted, not deleted by this TO (an optional later archive sweep is explicitly out of scope). This adds no migration work; it is one verification line item on the Phase C run.
    </phase>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">INF_D_05 recency gap CLOSED — post-migration, activity_scan_1y.json max(transDate) is current (within ~1 day of run date), not frozen at 2026-05-08. Verified by a chain or single-script run.</ac>
    <ac id="AC2">INF_D_05 reads via canonical camelCase source-select (latest full-history snapshot), not concat-all; no snake-schema requirement remains in _load_txn_partition.</ac>
    <ac id="AC3">INF_D_00 silver-read path confirmed: either fixed to read canonical camelCase silver, or the dead bronze-fallback removed — the path is no longer ambiguous/masked.</ac>
    <ac id="AC4">Phase C: 8 shielded consumers each produce non-zero output against the post-TO-3 amalgamated silver.</ac>
    <ac id="AC5">No emoji; from __future__ import annotations preserved; Rule 17 respected (these are gold-tier consumer scripts — INF_D_05/INF_D_00 may filter/derive as gold tier permits; do not touch silver).</ac>
    <ac id="AC6">TO-5 fold (§7-Q1 latest-snapshot): post-confirmation, NO concat-all-per-date reader remains in the silver/transactions consumer set — every consumer is a latest-snapshot source-select. The ~1,515 superseded per-date partitions are left inert (no re-emit, no delete in this TO). Asserted as part of the Phase C run.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (before writing): comp-pipescript io INF_D_05 + ds-commit-gate.sh. Phase 2 (before commit): ds-commit-gate.sh (py_compile + ds-precommit-check.py + ruff --target-version py39). Phase 3 (after commit): chain-run or single-script run + activity_scan_1y.json max(transDate) recency check. Copy verbatim per PRD §6.</compiler_tools_mandate>

  <cross_domain_coordination>
    Phases A+B run PARALLEL to TO-1 (ADVI_TXNAMG.001, DS~D) — no overlap (TO-1 touches no code; TO-2 touches gold consumer scripts INF_D_05/INF_D_00). Phase C gates on TO-3 (ADVI_TXNAMG.003, DS~D — the amalgamating writer) shipping. INF_D_05 + INF_D_00 are gold-tier scripts under data/orion/scripts/gold/ — DS-owned, no AE/DT coordination needed. §7-Q1 RULED latest-snapshot (Andrew via CTO, f6a13a672) — Phase A's INF_D_05 read model is confirmed; the PRD §6 TO-5 candidate (stale-partition disposition) is folded into Phase C as a verification line item (see Phase C / AC6), not a separate TO. No shared-file collision with TO-3 (TO-3 edits convert_transactions_to_silver.py — silver; TO-2 edits gold consumers).
  </cross_domain_coordination>

  <deliverables>
    <item>INF_D_05.activity_scan.py migrated; INF_D_00.portal_aggregates verified/cleaned — committed + safe-deploy per the DS cycle (CLAUDE.md Rule 13).</item>
    <item>Phase C confirmation evidence (8 shielded consumers non-zero post-TO-3).</item>
    <item>Session log with Compiler Tools section + RAVC2.</item>
  </deliverables>

  <ravc>DS~B RAVC2 to COO + CC CTO. Phases A+B close on their own evidence (recency gap closed); Phase C closes post-TO-3. Surface to COO if §7-Q1 ruling is needed before finalizing INF_D_05.</ravc>

  <notes>
    INF_D_05 feeds platinum/firm/activity_scan_*.json → InflectionInsightsPanel — a live partner-facing surface currently rendering 7-day-stale activity data. Phase A is the highest-value fix in this TO. The 8 shielded consumers are NOT broken — Phase C is a regression sentinel, not migration work; do not over-scope it.
  </notes>
</task_order>
