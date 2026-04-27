# Task Order: ADVI_INFLV2.001 — Phase 0 Joint Scope Freeze: BooksTab Inventory + Txn-Only Feasibility

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform + 0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — start immediately, parallel to INFGRD.003 chain (no data dependency)</priority>
  </metadata>

  <objective>
    Jointly produce the INFLV2 Phase 0 scope freeze: a panel-by-panel inventory of the
    49F/BD BooksTab and a txn-only feasibility verdict for each panel in the Inflection
    context. Andrew's direction: "0.4.0_DE check what all we're providing there for 49
    and work with DS to try and find what we can provide for now solely off of what we
    have in Transactions data."

    This deliverable gates INFLV2.004 (DS~A Revenue Ops brief) and is the joint
    DE+DS input to INFLV2.007 (BooksTab Inflection mode implementation).
  </objective>

  <scope>
    <task id="1" label="DE: 49F BooksTab panel inventory">
      Enumerate every panel currently rendered in the BooksTab for 49F/BD:
        - Component names + file paths in portal/src/
        - S3 key(s) each panel reads (platinum artifact)
        - Fields consumed from each artifact
        - Current render status for Inflection (renders / errors / blank / not-present)

      Reference: INFLEC_BD_PARITY_MATRIX.md §2 (commit b1629b88) as starting point.
      Supplement with live code inspection — the matrix may be incomplete.

      Output: a table in the joint deliverable with columns:
        Panel | Component path | S3 key | Fields | Inflection render status
    </task>

    <task id="2" label="DS~A: Txn-only feasibility verdict per panel">
      For each panel identified by DE, assess whether the panel's data requirement
      can be met from Orion transactions (s3://opal-data-inf/bronze/orion/) without
      external joins (no Schwab custodian data, no fee schedules, no geographic enrichment).

      Verdict options:
        FEASIBLE: data exists in Orion TRN/AUM/SlickGrid; can emit from gold scripts
        PARTIAL: subset of fields feasible; document what's achievable vs what's missing
        DEFER: requires data source not available (geo, fee, Schwab). Mark DEFER with reason.
        DROP: Andrew explicitly ruled out (geo cohort = DROP per PRD §3)

      Output: feasibility column added to DE's table + notes on implementation path
      for FEASIBLE/PARTIAL panels.
    </task>

    <task id="3" label="Joint: consolidate and commit">
      Merge DE panel inventory + DS~A feasibility verdicts into a single markdown doc:
        docs/architecture/INFLV2_BOOKS_SCOPE_FREEZE.md

      Also confirm or update INFLEC_BD_PARITY_MATRIX.md §2 (Books column) to match
      the Phase 0 findings.

      Commit with:
        git commit --only docs/architecture/INFLV2_BOOKS_SCOPE_FREEZE.md [+matrix if updated]
        Author: whichever agent does the final merge
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      INFLV2_BOOKS_SCOPE_FREEZE.md committed with panel inventory table covering all
      BooksTab panels visible in 49F portal for firmId=49financial.
    </criterion>
    <criterion id="2">
      Every panel has a FEASIBLE / PARTIAL / DEFER / DROP verdict with a one-line
      justification referencing available Orion fields or the explicit DROP reason.
    </criterion>
    <criterion id="3">
      INFLEC_BD_PARITY_MATRIX.md §2 Books column updated to match verdicts (or explicitly
      confirmed unchanged if matrix already correct).
    </criterion>
    <criterion id="4">
      RAVC sent to 2.0.0_SA_COO from DE (lead) confirming both DE inventory + DS~A
      feasibility are consolidated. Subject:
      RAVC — ADVI_INFLV2.001 COMPLETE | [N] panels inventoried | [N] FEASIBLE | [N] DEFER/DROP
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Scope freeze only — no implementation in this TO. Output is a doc
    + updated matrix. Implementation is INFLV2.007 (DE) gated on .005 + .006.</constraint>
    <constraint>No emojis in code or docs committed to repo.</constraint>
    <constraint>Coordinate: DE leads, DS~A contributes feasibility. One RAVC from
    DE on joint completion.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="none"
                note="No gate — start immediately, parallel to INFGRD.003 chain."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">docs/architecture/INFLV2_BOOKS_SCOPE_FREEZE.md — joint
    panel inventory + feasibility table.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO from DE with panel counts.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §3 (Andrew direction on Books)</ref>
    <ref type="matrix">docs/architecture/INFLEC_BD_PARITY_MATRIX.md v0.3 (commit b1629b88)</ref>
    <ref type="portal">portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx</ref>
  </references>
</task_order>
```
