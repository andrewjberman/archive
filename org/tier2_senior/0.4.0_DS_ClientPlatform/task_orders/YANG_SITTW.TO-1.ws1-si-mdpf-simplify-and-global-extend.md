<to_id>YANG_SITTW.TO-1</to_id>
<project>YANG_SITTW</project>
<title>WS-1 Since-Inception: MDPF cohort-simplification (collapse 1c SMA into 1b plug) + Global-view extend to 2024-11-01 (Option A demarcated)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<co_assignees>0.4.1_RD_ModelPortfolios (FE component) + 0.4.0_DE_ClientPlatform (FE wiring)</co_assignees>
<issued_by>2.0.0_SA_COO (PRD §7 decomposition, 2026-06-16; CTO handoff YANG_SITTW v0.2 42f6d414a)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>staged</status>
<priority>**UP-FIRST — Andrew-direct 2026-06-16 "YANG macro project up first"** (supersedes the prior "NOT urgent / slot behind OPLMCP/GCONTR"). **EXECUTION-GATED ON SPAWN**: Pod 4 DS 0.4.0 + RD 0.4.1 + DE 0.4.0 are OFFLINE — COO spawn-request routed to MSTR 2026-06-16. TO-1 is the FIRST YANG TO to GO (self-contained; the data-correction has standalone integrity value — removes a fabricated served layer). COO fires GO on spawn-confirm.</priority>

<references>
  <ref type="prd">docs/architecture/YANG_SITTW.md (v0.2, 42f6d414a) — §3 WS-1 RESOLVED (data-lineage trace), §6 compiler evidence, §7 TO-1, §8 acceptance</ref>
  <ref type="producer">data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py — emits json/mdpf/global/aggregate-aua-timeseries.json (opal-data-portal-v2)</ref>
  <ref type="consumer">portal/src/pages/ModelPortfolios.tsx:370 getMdpfAggregateAUATimeSeriesByFirm('global') — the Global-view consumer</ref>
  <ref type="finding">item-(d) brief: smartx_allocations Sept-2024->May-2026 = ZERO SMA rows -> 1c=$0 recommended, but shipped v0.9 interpolated 1c anyway ($19.67M @ 2024-11-01 fabricated). Confirmed-real floor = 2024-11-01 (served = 413 pts; MDPF_COUNTS legacy also floors there).</ref>
</references>

<scope>
Two legs, one TO (the data leg is load-bearing + carries the never-widen gate; the FE leg consumes its output).

**(a) DS (MDPF owner) — cohort simplification in build_aggregate_aua_timeseries.py:**
- Collapse the 1c/SMA carve-out into the 1b plug: **`1b' = Schwab_total - 1a`** (everything-non-model). The SMA stays inside 1b' to its EXACT REAL extent ($0 pre-2026-05-20, real after) — NO estimation/ratio/interpolation/fabricated cohort.
- Drop the `sma_aua` field + the SMA carve-out logic. Root-cause (note in the TO closeout) WHY item-(d)'s `1c=$0` recommendation didn't ship in v0.9 (interpolated-1c shipped instead) — so the class doesn't recur.
- Re-derive the served artifact. **Total + Non-Model-band value UNCHANGED** (the total was always real Schwab; 1b is a plug) — this purely removes the spurious internal SMA label + the `sma_aua` field.

**(b) RD/DE — Global-view FE extension (Option A):**
- Extend the Global-view x-axis to **2024-11-01** (real model-1a stack + real Schwab-derived 1b' band).
- DEMARCATE the **2024-11-01 -> 2026-01-15** deep tail as estimate-basis (shading / "estimated history" marker) — estimate must NEVER render as measured. (Per-date provenance is MEASURED from 2026-01-16; live-real from 2026-05-18.)

**Scope ceiling:** Global aggregate view ONLY. Per-firm views UNCHANGED.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-pipescript io build_aggregate_aua_timeseries</run>
      <expect>READS platinum/mdpf/{date}.json; WRITES json/mdpf/global/aggregate-aua-timeseries.json -> ModelPortfolios Global consumer. Enumerate EVERY consumer of the cohort split / sma_aua field BEFORE dropping it.</expect>
      <if_mismatch>STOP. If ANY consumer reads sma_aua / cohort_class='sma' directly (portal or downstream), surface to COO before dropping the field — a direct consumer breaks. (PRD: the model stack already excludes sma; Non-Model band = total-model; confirm empirically.)</if_mismatch>
    </step>
    <step>
      <run>comp-transform schema-check [the Global chart component on ModelPortfolios.tsx]</run>
      <expect>The Global-view component's data contract; confirm no field MISSING after the x-axis extend + the sma_aua removal.</expect>
      <if_mismatch>MISSING = runtime undefined. Reconcile the FE type to the new (sma_aua-free) shape before wiring.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit/deploy (the never-widen gate)">
    <step>
      <run>Re-derive + diff served-before vs served-after (the never-widen evidence)</run>
      <expect>TOTAL (every date) UNCHANGED + Non-Model-band value (every date) UNCHANGED; ONLY delta = the `sma_aua` field removed + the internal cohort split re-labeled. 0 movement in any plotted series.</expect>
      <if_mismatch>STOP — do NOT deploy. Any total / Non-Model-band movement means the collapse changed a served value (a widen, not a relabel) — re-examine the plug arithmetic. This is the CTO+COO never-widen sign-off gate (served-artifact change): post the before/after, get the co-sign, THEN deploy.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Served-artifact verify (aws s3 cp the deployed json/mdpf/global/aggregate-aua-timeseries.json) + Global-view render check</run>
      <expect>2024-11-01 floor renders; deep-tail demarcation present; sma_aua field GONE; total/Non-Model-band match the pre-change values; per-firm views unregressed.</expect>
      <if_mismatch>STALE/regressed -> re-run the deploy cycle or revert; surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- TO-1 is STANDALONE on the TTW axis (no §5 TTW dependency — WS-1 is the SI timeseries, not WS-2).
- Internal Pod-4 handoff: DS leg (a) re-emits the served artifact -> the FE leg (b) consumes the new (sma_aua-free, 2024-11-01-floored) shape. DS commits + QA-deploys the producer FIRST (data_contract.xml updated), THEN RD/DE wire the FE against the deployed shape (no shape ambiguity).
- **NEVER-WIDEN (CTO+COO co-sign, locked at PRD-decomposition):** the re-derive MOVES the served json/mdpf/global/aggregate-aua-timeseries.json (drops sma_aua + re-splits cohorts) = served-output movement -> requires the CTO+COO never-widen sign-off at the Phase-2 before/after. NOT a DELTA=0-skip (the artifact content changes). The before/after (total + Non-Model-band UNCHANGED, only sma_aua removed) IS the never-widen evidence. CTO concurred 2026-06-16 (171643Z); COO co-signs when the before/after lands. Do NOT deploy before the co-sign.
</cross_domain_coordination>

<acceptance_criteria>
- Producer emits the simplified series: `1b' = Schwab_total - 1a`, NO `sma_aua` field, no fabricated SMA cohort; re-derived + QA-deployed (DS full commit->deploy cycle; data_contract.xml updated).
- Phase-2 before/after proves TOTAL + Non-Model-band UNCHANGED at every date (the never-widen evidence) + CTO+COO co-sign recorded.
- Global view renders from the 2024-11-01 floor with the 2024-11-01->2026-01-15 deep tail DEMARCATED as estimate-basis; per-firm views unchanged.
- comp-transform schema-check clean on the Global component (no runtime-undefined).
- Session log Compiler Tools section reproduces every `<run>` with observed output + pass/fail vs `<expect>`. Root-cause note on why item-(d)'s 1c=$0 didn't ship in v0.9.
</acceptance_criteria>

<data_reprocess_scope><reprocess_required>The producer logic change re-derives the served json/mdpf/global/aggregate-aua-timeseries.json (re-emit the full series under 1a+1b'). Phase-3 verifies the deployed served object mtime > commit-time + the new shape. The before/after (Phase-2) is the never-widen gate; only the internal cohort split + sma_aua field change, total/band never move.</reprocess_required></data_reprocess_scope>
