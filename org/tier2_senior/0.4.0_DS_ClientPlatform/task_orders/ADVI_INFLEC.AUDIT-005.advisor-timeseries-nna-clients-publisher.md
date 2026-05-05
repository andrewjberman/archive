<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-005</id>
    <project>ADVI_INFLEC</project>
    <title>Per-advisor timeseries.json + nna_clients.json publishers — Orion D-chain emit</title>
    <issued_to>0.4.0_DS_ClientPlatform~A (primary) + 0.6.1_AE_PartnerETL (chain add if new script needed)</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- GO withheld — DS~A completing matrix merge first. COO will send GO when matrix v3 is fully closed and DS~A confirms readiness. -->
    <priority>medium</priority>
    <estimated_effort>1-2d (0.5d investigation; 0.5-1d script authoring + catalog add if missing)</estimated_effort>
  </metadata>

  <references>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v3 — RED: per-advisor timeseries.json MISSING; per-advisor nna_clients.json MISSING</ref>
    <ref type="cto_ruling">CTO RAVC3 2026-05-05: AUDIT-005 = per-advisor timeseries.json + nna_clients.json publishers (Orion D-chain)</ref>
    <ref type="existing_pattern">platinum/firm/timeseries_chart.json exists (INF_I_D00b writes gold/artifacts/, INF_D_04 Step 7 pass-through to platinum/firm/); per-advisor equivalent missing</ref>
  </references>

  <context>
    The ADVI_INFLEC audit matrix v3 identifies RED cells for:
    1. platinum/advisors/{id}/timeseries.json — missing for all 4 Inflection advisors
    2. platinum/advisors/{id}/nna_clients.json — missing for all 4 Inflection advisors (or ADV-cohort disabled makes this GRAY — confirm first)

    These are per-advisor equivalents of firm-level artifacts that DO exist. The gap may be:
    A) Scripts exist but not in dispatch catalog (catalog-add only)
    B) Scripts exist but filter logic excludes Inflection advisors
    C) Scripts don't exist yet (new authoring needed, ~1d)
    D) Panels consuming these are GRAY for Inflection — confirm before writing any code

    nna_clients.json: ADV cohort is GRAY for Inflection per layout.ts, so the NNA-cohort drill
    may never trigger. Verify whether BooksTab L2 drill independently needs nna_clients.json.
  </context>

  <phase id="0" when="before any write — scope confirmation">
    <step>
      <run>aws s3 ls s3://opal-data-inf/platinum/advisors/ --recursive | grep -E "timeseries|nna_clients" | head -20</run>
      <expect>Either 0 results (missing, confirm D) or some results (check if all 4 advisors covered)</expect>
      <if_mismatch>If some present for some advisors but not all — catalog/filter gap (B). If none — script gap (C) or GRAY (D).</if_mismatch>
    </step>
    <step>
      <run>comp-transform schema-check ClientsTab (look for nna_clients.json fetch in component tree) AND grep "nna_clients\|timeseries" portal/src/api/endpoints/advisor-intelligence.ts | head -10</run>
      <expect>If nna_clients fetch present in endpoints but artifact missing → RED (pipeline gap). If no fetch present → GRAY by design.</expect>
      <if_mismatch>Document verdict per artifact type; only proceed to Phase 1 for confirmed RED artifacts</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_I_D00b (firm timeseries publisher) — understand pattern for per-advisor equivalent</run>
      <expect>Shows what INF_I_D00b reads + writes; serves as template for per-advisor variant</expect>
      <if_mismatch>N/A — informational step</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="before writing any new script or catalog entry">
    <step>
      <run>comp-blast [closest existing per-advisor script] — blast radius for per-advisor emit changes</run>
      <expect>No overlap with other active TOs' scope</expect>
      <if_mismatch>Coordinate with other active TO authors via MCP before writing</if_mismatch>
    </step>
    <step>
      <run>If new script required: read data/orion/scripts/gold/INF_I_D00c.cumulative_chart.py as template for per-advisor output pattern (OUTPUT_PREFIX pattern, GOLD_ARTIFACTS_PREFIX pattern)</run>
      <expect>Script uses OUTPUT_PREFIX env var for platinum/ output; GOLD_ARTIFACTS_PREFIX for gold/artifacts/ side-write if applicable</expect>
      <if_mismatch>Follow whichever pattern matches existing INF scripts in the dispatch chain</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before committing any new or modified script">
    <step>
      <run>.tools/ds-commit-gate.sh [new/modified scripts]</run>
      <expect>Exit 0 — py_compile + AST + ruff all pass. Script must start with `from __future__ import annotations`.</expect>
      <if_mismatch>Fix all errors before committing</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript deployed [script] for each modified/new script</run>
      <expect>MATCH — runner has your code</expect>
      <if_mismatch>Re-upload</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after AE chain re-run">
    <step>
      <run>aws s3 ls s3://opal-data-inf/platinum/advisors/ --recursive | grep timeseries | wc -l</run>
      <expect>4 — one timeseries.json per Inflection advisor</expect>
      <if_mismatch>If fewer than 4: catalog coverage gap — identify missing advisor keys and fix dispatch</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>AE 0.6.1: if new script added to dispatch catalog, AE 0.6.1 updates the catalog file + re-runs chain. DS~A provides S3-uploaded script + MATCH confirmation before MCP GO to AE.</coord>
    <coord>DS~D: do not touch per-advisor emit scripts while DS~A owns this TO.</coord>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">Phase 0 scope verdict documented: which artifacts are RED (pipeline gap) vs GRAY (by design) — with evidence (S3 ls output + endpoint grep)</criterion>
    <criterion id="AC2">For confirmed RED artifacts: platinum/advisors/{id}/[artifact].json present for all 4 Inflection advisors post-chain</criterion>
    <criterion id="AC3">comp-pipescript deployed MATCH on all new/modified scripts before AE dispatch</criterion>
    <criterion id="AC4">Session log Compiler Tools section reproduces each &lt;run&gt; + observed result + PASS/FAIL vs &lt;expect&gt;</criterion>
    <criterion id="AC5">RAVC3 to COO with scope verdict + commit hash(es) + AC1-4 status</criterion>
  </acceptance_criteria>
</task_order>
