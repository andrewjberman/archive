<task_order>
  <metadata>
    <id>ADVI_49FRECN.001B</id>
    <project>ADVI_49FRECN</project>
    <title>Phase 0 Slice B — Missing-Account Investigation + 49F-Side Integration</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>complete</status>
    <priority>P1 — parallel with .001A + .001C; you also own .001D consolidation</priority>
    <estimated_effort>1–1.5d</estimated_effort>
    <parallel_with>ADVI_49FRECN.001A (DS~A), ADVI_49FRECN.001C (DS~C)</parallel_with>
  </metadata>

  <context>
    49F partner data accuracy investigation v2. Quantified gaps: 3.59% AUA undershoot, 586 missing
    accounts (8.86% undercount). Drift from ADVI_AUAVAR 99.1% baseline (2026-03-09).

    You are the natural primary on this — you already hold the Schwab/49F NNA reconciliation
    context from `bea387a9` 2026-04-21 (Schwab TRN NNA enrichment AE A+B; your Phase 6 C_01
    merge pending). The missing-account angle has the highest probability of overlap with
    your existing scope.

    Parallelization map:
    - DS~A: Opal-side axis matrix + account-id list extraction (.001A)
    - **YOU (DS~B): missing-account trace + 49F-side data integration + final consolidation** (.001B + .001D)
    - DS~C: AUA decomposition + classification drift verification (.001C)
  </context>

  <objective>
    (1) Obtain 49F-side reference snapshot from Andrew + integrate it into DS~A's matrix shell.
    (2) Trace representative missing accounts bronze→silver→gold to produce hypothesis buckets.
    (3) Identify per-custodian feed gaps.
    (4) Cross-link with your in-flight Schwab TRN NNA Phase 6 C_01 work — flag merge-vs-parallel.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>49F-side reference snapshot acquisition</title>
      <detail>
        MCP Andrew (`@andrew@opal.agent` or via direct ping) requesting 49F's reference snapshot
        at the date DS~A picked in .001A. Request:
        - Total AUA + total account count at that date
        - Per-advisor breakdown if available
        - Per-account-type breakdown if available
        - Per-custodian breakdown if available
        - Account-id list at the same date (critical for #2 set-diff)

        If Andrew can only share partial data, document what's available and proceed.
        Do NOT block the rest of the work waiting for the perfect snapshot.
      </detail>
    </ac>

    <ac id="2">
      <title>Account-id set-diff: 49F vs Opal</title>
      <detail>
        Set-diff Andrew's 49F account-id list against DS~A's Opal account-id list (.001A AC #5):
        - **MISSING_FROM_OPAL** = in 49F, not in Opal (expected ~586)
        - **MISSING_FROM_49F** = in Opal, not in 49F (could be closed-still-listed; should be ~0 or small)
        - **MATCHED** = both sides

        Quantify each bucket. Sample 10–20 representative IDs from MISSING_FROM_OPAL for #3 trace.
      </detail>
    </ac>

    <ac id="3">
      <title>Bronze→silver→gold trace for representative missing accounts</title>
      <detail>
        For each sampled missing account-id:
        1. Search `s3://opal-data-bd/bronze/...` — is the account in bronze ingestion at all?
        2. If yes — search silver. Where does it disappear? Which step / which filter / which transform drops it?
        3. If no — is the BD feed missing the account? Which custodian is it on? Was it new since BD's last full sync?
        4. Hypothesis classification:
           - In-flight rollover (account opened recently, not yet on BD's daily feed)
           - Closed-still-listed (49F still reporting it as part of historical book; Opal already drops)
           - Sub-account / sleeve double-count divergence
           - Joint-account 1-vs-2 representation difference
           - Specific custodian feed gap
           - Trust/fiduciary linkage edge case
           - UNKNOWN — flag for deeper dive
      </detail>
    </ac>

    <ac id="4">
      <title>Per-custodian feed gap audit</title>
      <detail>
        For each custodian represented in 49F's data (Schwab / Fidelity / TD / Pershing / etc.):
        - Are we getting that custodian's BD feed at all?
        - If yes, count the accounts per custodian in Opal vs 49F. Where's the biggest gap?
        - If a custodian is entirely missing from Opal, that's a P0 finding.
      </detail>
    </ac>

    <ac id="5">
      <title>Schwab TRN NNA Phase 6 C_01 cross-link</title>
      <detail>
        You have Phase 6 C_01 merge pending under Schwab TRN NNA enrichment scope. Compare
        what you find in #3 (missing accounts) and #4 (custodian gaps) against C_01's scope.
        - Is there overlap? If yes, propose merge (collapse C_01 into the Phase 1 remediation TOs from .001D).
        - Is C_01 a strict subset / superset / disjoint? Document explicitly.
      </detail>
    </ac>

    <ac id="6">
      <title>Fill 49F-side columns in DS~A's matrix shell</title>
      <detail>
        With 49F's data in hand (per #1), populate the 49F count + 49F AUA + delta + gap classification
        columns in DS~A's per-advisor / per-account-type / per-custodian tables. Append to your section
        in `docs/architecture/49F_RECONCILIATION_2026-05-01.md` under `## Slice B — Missing Accounts + 49F Integration (DS~B)`.
      </detail>
    </ac>
  </acceptance_criteria>

  <constraints>
    <constraint>Same as .001A: discovery only, 49F-only scope, compiler tools first, pre-commit gate on any Python helper.</constraint>
    <constraint>If MCP to Andrew bounces or he's unavailable for the snapshot data, proceed with what's available + log the gap.</constraint>
    <constraint>Don't block .001D consolidation on Schwab Phase 6 C_01 merge analysis — that can be a Phase 1 TO recommendation.</constraint>
  </constraints>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 to CTO with: commit refs, missing-account hypothesis classification table, custodian gap findings, Schwab C_01 overlap verdict. Then proceed to .001D consolidation when .001A + .001C are also complete.</on_complete>
  </ravc_target>
</task_order>
