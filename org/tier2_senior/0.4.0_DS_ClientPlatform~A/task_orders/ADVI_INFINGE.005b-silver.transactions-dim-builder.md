<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.005b-silver</id>
    <project>ADVI_INFINGE</project>
    <title>transactions DIM_BUILDER in convert_orion_api_to_silver.py (9th dim; silver/api_dims/transactions)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>complete</status><!-- Dispatched session 59 via MCP GO. DS~A RAVC2 ACK received 20260506T~1500Z (session 60). Formalized here for scope clarity and acceptance criteria. SHIPPED 2026-05-07: T-1 default-date fix fd4105bec + bronze-S3 read fix 2aaa504d9; closed per AE 0.6.1 log 59edf4bf9 + COO log 54dd08969 + 17c9a301a. Empirical close confirmed in 848f12c28 Phase 2 review 2026-05-08. Lane-copy retroactively flipped 2026-05-13 by 1.0.0_SA_CTO during startup ground-truth reconciliation. -->
    <priority>high</priority>
    <estimated_effort>~1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="cto_ruling_q_c">1.0.0_SA_CTO RULING 20260506T~1410Z — Q-C: ADD transactions DIM_BUILDER to convert_orion_api_to_silver.py (9th dim, NOT a separate file). SILVER_BUILDERS stale comment to be removed.</ref>
    <ref type="cto_ruling_q_b">Q-B: silver output key = silver/api_dims/transactions (no v2 suffix; no v1 predecessor to version against).</ref>
    <ref type="bronze_source">Bronze input from orchestrator: bronze/orion-api/{date}/transactions.csv (CSV, 29 columns per AE 0.6.1 Phase 0 RAVC2 report)</ref>
    <ref type="silver_file">data/orion/scripts/silver/convert_orion_api_to_silver.py — existing 8 DIM_BUILDERs; add transactions as 9th following same pattern</ref>
    <ref type="ravc_routing">RAVC3 recipient: 0.6.1_AE_PartnerETL (NOT COO). AE 0.6.1 INFINGE.005b Phase 1 GO gates on this RAVC3.</ref>
    <ref type="context_session59">Session 59 COO log: CTO ruling Q-C issued ~20260506T1410Z. DS~A verbally dispatched for silver builder. AE 0.6.1 staging INFINGE.005b Lambda until DS~A RAVC3.</ref>
  </references>

  <context>
    AE 0.6.1 is building inf-api-txn Lambda (INFINGE.005b TO-5b) that pulls bronze transactions data
    via pull_inflection_transactions_v2.py and then calls convert_orion_api_to_silver.py to convert
    bronze to silver. The Lambda invokes the silver converter with --dim transactions.

    The transactions DIM_BUILDER does not yet exist in convert_orion_api_to_silver.py.
    DS~A must add it following the existing 8-dim pattern in that file.

    CTO rulings:
    - Q-A: REPLACE pattern — Lambda writes bronze/orion-api/{date}/transactions.csv (same key as
      orchestrator). Orchestrator transactions DimSpec decommissioned at Lambda cutover.
    - Q-B: silver key = silver/api_dims/transactions (no v2 suffix; no v1 to version against)
    - Q-C: ADD transactions DIM_BUILDER to convert_orion_api_to_silver.py (9th dim).
      SILVER_BUILDERS stale comment to be removed.

    No gold script currently reads silver/api_dims/transactions/ — this is foundational infrastructure.
    Lambda cutover to silver is the immediate consumer; gold consumers TBD in future scope.
  </context>

  <steps>
    <step id="1">
      <objective>Read convert_orion_api_to_silver.py to understand existing DIM_BUILDER pattern.</objective>
      <run>
        Read data/orion/scripts/silver/convert_orion_api_to_silver.py.
        Identify: SILVER_BUILDERS dict/list, existing build_*_dim() function signatures, common
        bronze input reading pattern, parquet write pattern, output path convention.
        Identify the stale SILVER_BUILDERS comment to be removed (per CTO Q-C ruling).
      </run>
    </step>

    <step id="2">
      <objective>Understand bronze input schema (transactions.csv).</objective>
      <run>
        AE 0.6.1 RAVC2 reports bronze/orion-api/{date}/transactions.csv = 29 columns.
        Check a recent partition: aws s3 ls s3://opal-data-inf/bronze/orion-api/ and pick a
        recent date. Read the header row: aws s3 cp s3://opal-data-inf/bronze/orion-api/{date}/transactions.csv -
        | head -1
        Identify the column set for the parquet conversion.
      </run>
    </step>

    <step id="3">
      <objective>Implement build_transactions_dim() and register in SILVER_BUILDERS.</objective>
      <run>
        Add build_transactions_dim(df) function following existing pattern.
        Key requirements:
        - Input: raw CSV data from bronze/orion-api/{date}/transactions.csv
        - Output: parquet written to silver/api_dims/transactions/{snapshot_date}/data.parquet
        - Follow column naming / type conventions of existing dims
        - Add transactions to SILVER_BUILDERS dict/list (wherever existing dims are registered)
        - Remove the stale SILVER_BUILDERS comment called out in Q-C ruling
        - from __future__ import annotations must be present (Rule 15 — already in file, verify)
      </run>
    </step>

    <step id="4">
      <objective>Pre-commit gate.</objective>
      <run>.tools/ds-commit-gate.sh data/orion/scripts/silver/convert_orion_api_to_silver.py</run>
      <expect>py_compile + ds-precommit-check.py + ruff all exit 0.</expect>
    </step>

    <step id="5">
      <objective>Commit + push.</objective>
      <run>
        .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~A &lt;0.4.0_DS_ClientPlatform~A@opal.agent&gt;" \
          -m "feat(ADVI_INFINGE.005b-silver): add transactions DIM_BUILDER to convert_orion_api_to_silver.py (9th dim; silver/api_dims/transactions)" \
          -- data/orion/scripts/silver/convert_orion_api_to_silver.py

        git push
      </run>
      <expect>Commit lands on CLOUD. Push succeeds.</expect>
    </step>

    <step id="6">
      <objective>RAVC3 to AE 0.6.1 (NOT COO).</objective>
      <run>
        Send RAVC3 to 0.6.1_AE_PartnerETL with:
        - Commit hash
        - Confirmation: build_transactions_dim() implemented + registered in SILVER_BUILDERS
        - Silver output key: silver/api_dims/transactions/{date}/data.parquet
        - Pre-commit gate: PASS (py_compile + ds-precommit-check + ruff all exit 0)
        - SILVER_BUILDERS stale comment removed: confirm
        - from __future__ import annotations: confirm present
      </run>
      <expect>AE 0.6.1 receives RAVC3 and issues INFINGE.005b Phase 1 GO for Lambda implementation.</expect>
    </step>
  </steps>

  <acceptance_criteria>
    <criterion id="AC1">build_transactions_dim() function implemented in convert_orion_api_to_silver.py following existing DIM_BUILDER pattern.</criterion>
    <criterion id="AC2">transactions registered in SILVER_BUILDERS (dict or list, matching existing convention).</criterion>
    <criterion id="AC3">Silver output path: silver/api_dims/transactions/{date}/data.parquet (no v2 suffix).</criterion>
    <criterion id="AC4">Stale SILVER_BUILDERS comment removed per CTO Q-C ruling.</criterion>
    <criterion id="AC5">Pre-commit gate PASS: py_compile + ds-precommit-check.py + ruff all exit 0.</criterion>
    <criterion id="AC6">from __future__ import annotations present as first import (Rule 15).</criterion>
    <criterion id="AC7">RAVC3 sent directly to 0.6.1_AE_PartnerETL (not COO) with commit hash + all AC confirmations.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="before_edit">Read data/orion/scripts/silver/convert_orion_api_to_silver.py to understand existing pattern. No comp-* tool needed for this scope (silver script, not gold).</phase>
    <phase id="before_commit">.tools/ds-commit-gate.sh data/orion/scripts/silver/convert_orion_api_to_silver.py — all 3 checks exit 0.</phase>
    <phase id="after_commit">None required for this scope (foundational silver builder; no gold consumer yet to validate via comp-validate).</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>RAVC3 goes to AE 0.6.1, NOT COO. AE gates INFINGE.005b Phase 1 (Lambda implementation) on this RAVC3.</item>
    <item>Do NOT edit AE 0.6.1's task orders or infra files. DS~A scope is convert_orion_api_to_silver.py only.</item>
    <item>If bronze transactions.csv schema is unclear, ask AE 0.6.1 via MCP before implementing. Do not guess column types.</item>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT send RAVC3 to COO — send directly to AE 0.6.1 (0.6.1_AE_PartnerETL).</rule>
    <rule>Do NOT create a separate build_transactions_dim.py file — add to convert_orion_api_to_silver.py per CTO Q-C ruling.</rule>
    <rule>Do NOT use v2 suffix in silver key — silver/api_dims/transactions (no suffix) per CTO Q-B ruling.</rule>
    <rule>Do NOT skip pre-commit gate (Rule 14).</rule>
  </do_not>

  <go_signal>
    <issued_at>20260506T~1358Z (session 59 MCP dispatch)</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO issued. DS~A RAVC2 ACK received 20260506T~1500Z. Proceed to implementation.</message>
  </go_signal>

</task_order>
