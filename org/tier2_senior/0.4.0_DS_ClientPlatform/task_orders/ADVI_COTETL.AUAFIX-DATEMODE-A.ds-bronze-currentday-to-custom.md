<to_id>ADVI_COTETL.AUAFIX-DATEMODE-A</to_id>
<project>ADVI_COTETL</project>
<title>AUAFIX DATEMODE-A (DS commit-leg) -- cot_bronze_ingest.py TABLE_DATE_MODE: holdings/alloc/unrealized CurrentDay -> Custom (carry AE diagnosis; Rule-13 commit-lane)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<consult>0.7.0_AE_CloudOps (diagnosing owner -- supplies the exact ("Custom-N",end) tuple + the 3-table mapping; cross-tool: AE diagnoses, DS commits per Rule 13)</consult>
<issued_by>2.0.0_SA_COO (COTETL AUAFIX re-scope; supersedes the RETIRED consolidated-merge CHAINFIX; CTO L2 ruling 135603Z)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>pending</status>
<!-- GO 2026-06-22 (COO /drive cycle-5): P0 ~$24M/6.5% cot firm-AUA understatement. AE probe (135354Z) PROVED internal CurrentDay date-mislabeling; CTO L2 RULED (135603Z). This is the REAL fix; the consolidated-merge CHAINFIX is RETIRED (off-target/0-consumer). -->

<objective>
Root (CTO-ruled, AE-probed): holdings/alloc/unrealized BD exports use dateRangeType=CurrentDay, which stamps LIVE current data with a stale early-June asOfDate (BD HAS date-distinct data thru 06/18 -- $373.6M/06-08 -> $390.5M/06-15 -> $397.7M/06-18, MVs all differ). transactions/realized already use Custom-14 and advance correctly. FIX: switch the 3 stuck tables to Custom mode, mirroring transactions.
</objective>

<the_fix>
In cot_bronze_ingest.py TABLE_DATE_MODE: change holdings, allocations, unrealized from ("CurrentDay", 0) to Custom mode with PER-TABLE windows (NOT blind Custom-14 -- these are point-in-time SNAPSHOTS / the AUA basis, not transactions' 14d restatement log; CTO 135924Z). Take AE's exact per-table ("Custom-N", end) tuple verbatim from the DATEMODE-B re-provision (end=latest-complete-business-day; AE's minimal per-table lookback). Cross-tool: AE diagnoses + re-provisions, DS commits the matching edit. NO other logic change.

HARD SEQUENCE GATE (CTO 135924Z): this code edit is INERT until AE re-provisions the 3 BD templates + updates templates/{table}.json templateId (the runner reuses the PERSISTED templateId -- banked reference_bd_datamining_blank_selection_template_status_error). SO the order is NON-PARALLEL: (1) AE re-provisions templates to Custom [DATEMODE-B] -> (2) AE hands DS the per-table windows -> (3) THIS DS edit matches the re-provisioned config -> (4) AE backfill pull -> (5) nightly-verify. Do NOT commit until AE confirms templates re-provisioned + windows handed (code==templates is a hard gate).
</the_fix>

<data_reprocess_scope>
REPROCESS REQUIRED (bronze patch, CTO Auto-Rule #4). Forward-fix alone leaves silver/holdings at 06-08. After the code lands + AE re-provisions the templates, a BACKFILL pull of holdings/alloc/unrealized for 06-09..latest must flow bronze -> silver -> gold (AE orchestrates the pull in DATEMODE-B; DS confirms the silver/gold consume the backfilled bronze partitions). Verify silver/holdings gains partitions > 06-09 post-backfill.
</data_reprocess_scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io cot_bronze_ingest</run>
      <expect>Confirms TABLE_DATE_MODE consumers + the holdings/alloc/unrealized write paths; no unexpected downstream.</expect>
      <if_mismatch>STOP; surface to COO if the edit touches an unexpected consumer.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/ds-commit-gate.sh (py_compile + ds-precommit-check + ruff py39 + from __future__ import annotations)</run>
      <expect>Clean on cot_bronze_ingest.py (the FA future-import + py39 ruff per Rules 14/15).</expect>
      <if_mismatch>STOP; isolate the intended change; do NOT --fix bundle pre-existing debt (CTO Rule-A pattern if bd-fork debt surfaces).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-pipescript deployed cot_bronze_ingest</run>
      <expect>MATCH (the edited script deployed to opal-data-cot/code/bronze/).</expect>
      <if_mismatch>Re-deploy via the DS QA cycle (Rule 13); confirm MATCH before AE runs the backfill.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. cot_bronze_ingest.py TABLE_DATE_MODE: holdings/alloc/unrealized = Custom (per AE's tuple); committed via ds-commit-gate (clean), deployed MATCH.
2. Session-log Compiler Tools section reproduces every <run> + observed result + pass/fail vs <expect>.
3. Coordinated with AE DATEMODE-B (template re-provision + backfill). 
4. BINDING VERIFICATION GATE (project-level, shared with DATEMODE-B): served cot firm-AUA data_as_of advances PAST 06-09 AND total_aua ~$397.7M on the NEXT SCHEDULED NIGHTLY (validate-on-served, no ad-hoc gold run). NOT accepted until the nightly confirms.
</acceptance_criteria>
