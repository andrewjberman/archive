# Task Order: ADVI_INFLV2.013 — Joint: Enrichment/Dim Table Field Scoping

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-013</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform + 0.4.0_DS_ClientPlatform~A + 0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — Andrew directed; gates INFLV2.004 + potential ADVI_INFLEC_ENRICH project</priority>
  </metadata>

  <objective>
    Andrew direction (2026-04-27 session): "have DS~A and ~B work together with DE to figure
    out what fields we are going to want to look into for enrichment/dim tables."

    Joint design session using three inputs already in-hand:
    1. INFLV2_BOOKS_SCOPE_FREEZE.md (14 PARTIAL panels + 2 DEFER — each has named missing fields)
    2. docs/data/orion_reporting_fields_catalog.md (~700 fields, 66 domains — DS~B authored)
    3. Portal component field maps (DE knowledge: exact field names each component reads)

    Output: INFLEC_ENRICH_SCOPE.md — a prioritized dim/enrichment table candidate list that
    answers: "given the Orion catalog and our PARTIAL panel gaps, which enrichment tables
    should we build first, and what do they unblock?"

    This is SCOPING ONLY. No implementation in this TO.
  </objective>

  <scope>
    <task id="1" label="DE: enumerate exact missing fields per PARTIAL panel">
      For each PARTIAL panel in INFLV2_BOOKS_SCOPE_FREEZE.md, specify the exact field names
      the component currently attempts to render that return empty/null for Inflection:
        - Component path + specific prop / data key that is empty
        - Expected data shape (string, number, array of X)
        - Source artifact key where the field WOULD live if published
        - Whether the field is present in 49F but absent in INFLEC (parity gap)
          or absent in both (net-new)

      Focus on N1 and L3 panels (highest user-visible impact under Option A).
      L2 panels are HIDDEN_INFLEC — lower priority, flag but don't spend depth here.
      L4 panels: enumerate but mark as deferred if per-account publisher bundle is the blocker.

      DE is the authority on what the components actually consume. This step does NOT require
      checking Orion sources — that is DS~A + DS~B.
    </task>

    <task id="2" label="DS~B: map missing fields to Orion catalog tags">
      For each missing field DE enumerates, search orion_reporting_fields_catalog.md for a
      matching or equivalent Orion reporting tag. Produce a mapping table:

        Missing field | Orion tag (or NOT_IN_CATALOG) | Catalog domain section | Notes

      Also flag:
        - Tags with suspected copy-paste bugs (mark [COPY_PASTE_SUSPECT]) per catalog caveats
        - Tags where the spelling may differ from actual API tag (RiskQuestionnnaire typo class)
        - Tags that supply the field directly (no computation needed) vs tags that supply
          raw inputs requiring a gold-script computation to produce the portal field

      Parallel with DE task 1: DS~B can also walk the PARTIAL panels from scope-freeze
      directly and do a best-effort pre-map before DE's exact field names land.

      Input: DE task 1 output (field names) + INFLEC_PARITY_FILL_CANDIDATES.md (INFLV2.012,
      if committed). If .012 is not yet committed, work from the scope-freeze directly.
    </task>

    <task id="3" label="DS~A: assess pipeline category per mapped tag">
      For each Orion tag DS~B maps, classify the build path:
        A) ALREADY_AVAILABLE: field is derivable from current Orion bronze TRN/AUM/accounts_dim
           silver pull — just missing a publisher script or gold aggregation step
        B) NEW_ORION_PULL: field requires pulling a different Orion reporting-tag endpoint
           (not the same transactions/AUM/accounts_dim tables we pull today)
        C) COMPUTE_ONLY: field exists in our data but requires a new gold computation
           (e.g. TWR from daily AUM + cashflows — data in hand, need script)
        D) EXTERNAL_DEP: field has no Orion source; requires Schwab custodian data,
           fee schedules, or other non-Orion source

      DS~A is the authority on what the current silver/bronze pipeline supplies.
      Flag category D fields for DEFER — they belong to a separate enrichment track.
    </task>

    <task id="4" label="Joint: cluster into dim/enrichment table candidates + prioritize">
      Cluster the mapped fields (from tasks 1-3) into logical dim/enrichment tables.
      Use Orion catalog domain sections as a starting point:
        - Account Dimension (status, tax rates, custodian, SMA flag, tax transition)
        - Household + Member (suitability, time horizon, risk tolerance)
        - Performance + Attribution (TWR/IRR, Sharpe, Sortino, Drawdown, Capture, Alloc/Select)
        - Tax (OCI realized/unrealized, cost basis, gain-loss)
        - Registration (investment objective, net worth, qualified investor)
        - (Lower priority) Billing, Custom Indexing, Beneficiary/RMD — note but defer

      For each candidate table, produce:
        Table name | Fields supplied | Panels unblocked (count + names) | Build path (A/B/C/D)
        | Priority (HIGH/MED/LOW) | Rough effort (days: 1/3/5/10+)

      Priority formula:
        HIGH = unblocks 3+ PARTIAL panels OR unblocks a FEASIBLE/PARTIAL N1 panel
        MED = unblocks 1-2 panels, build path A or C (data in hand)
        LOW = build path B or D, or only unlocks L4/L2 panels

      FEASIBLE panels (6 in scope-freeze) do NOT need enrichment — skip them.
      2 DEFER panels (fee schedule, AI summary): note as EXTERNAL_DEP, no further work here.
    </task>

    <task id="5" label="Joint: commit output doc">
      Commit: docs/architecture/INFLEC_ENRICH_SCOPE.md

      Sections:
        1. Summary table (dim table candidates, priority, effort, panels unblocked)
        2. Field-to-tag mapping table (DE field → DS~B Orion tag → DS~A build path)
        3. High-priority table deep-dives (one paragraph each for HIGH priority tables)
        4. Defer list (EXTERNAL_DEP + lower priority tables)
        5. Next steps: which tables feed INFLV2.004 Revenue Ops brief?

      Author: 0.4.0_DE_ClientPlatform (lead), with DS~A + DS~B contributions noted inline.
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      docs/architecture/INFLEC_ENRICH_SCOPE.md committed. Summary table covers all 14 PARTIAL
      + 2 DEFER panels from INFLV2_BOOKS_SCOPE_FREEZE.md.
    </criterion>
    <criterion id="2">
      Every PARTIAL panel's missing fields have either an Orion tag mapping or a NOT_IN_CATALOG
      classification.
    </criterion>
    <criterion id="3">
      Each candidate dim/enrichment table has a build-path classification (A/B/C/D) from DS~A
      and a priority rating.
    </criterion>
    <criterion id="4">
      At least the HIGH-priority tables have a one-paragraph deep-dive with effort estimate.
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO from DE (lead). Subject:
      RAVC — ADVI_INFLV2.013 COMPLETE | [N] dim tables identified | [N] HIGH priority | [N] panels unblocked
      This RAVC is the gate signal for COO to dispatch INFLV2.004 (Revenue Ops brief).
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Scoping ONLY — no implementation, no new scripts, no new S3 operations.</constraint>
    <constraint>DE task 1 should be based on code inspection, not assumptions.
    If a component's field contract is ambiguous, note it and DS~A resolves from gold output.</constraint>
    <constraint>DS~B: do NOT edit INFLEC_BD_PARITY_MATRIX.md — DS~A owns that file for
    any further updates. Output goes to INFLEC_ENRICH_SCOPE.md only.</constraint>
    <constraint>No emojis in committed docs.</constraint>
    <constraint>Sequencing: DE task 1 + DS~B task 2 can run in parallel. DS~A task 3 follows
    once DE task 1 output is available (DS~A needs exact field names). Task 4+5 joint after
    all three individual tasks complete.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="none"
                note="No gate — start immediately. INFLV2.012 (DS~B cross-ref) output is
                additive input but not required; DS~B can work from scope-freeze directly."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">docs/architecture/INFLEC_ENRICH_SCOPE.md</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO from DE (lead). Gates INFLV2.004 dispatch.</deliverable>
  </deliverables>

  <references>
    <ref type="scope-freeze">docs/architecture/INFLV2_BOOKS_SCOPE_FREEZE.md (14 PARTIAL + 2 DEFER panels)</ref>
    <ref type="catalog">docs/data/orion_reporting_fields_catalog.md (~700 fields, 66 domains — DS~B)</ref>
    <ref type="parity">docs/architecture/INFLEC_BD_PARITY_MATRIX.md v0.3.2 (matrix alignment)</ref>
    <ref type="cross-ref">docs/architecture/INFLEC_PARITY_FILL_CANDIDATES.md (INFLV2.012 — DS~B, in progress)</ref>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §3 (Andrew Books direction)</ref>
  </references>
</task_order>
```
