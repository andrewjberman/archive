# Task Order: ADVI_INFLV2.005 — DS: Implement Andrew-Selected Revenue Ops Insight

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-005</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform + 0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-27</date>
    <status>complete</status><!-- ffd4484b3 INF_D_05+D_07 + 6c8fddbdc INF_D_06; S3 MATCH; dispatch wiring updated; RAVC to COO+AE+DE 20260429 -->
    <priority>HIGH — gates INFLV2.007 (DE BooksTab), INFLV2.009 (AE chain rerun)</priority>
  </metadata>

  <objective>
    Implement the InflectionInsightsPanel data artifact for the winner(s) selected by
    Andrew from the INFLV2.004 3-candidate brief. This TO is authored now; Andrew's
    pick fills in the specific implementation details.

    Output: a new platinum artifact (or extension of existing) that feeds
    InflectionInsightsPanel.tsx (to be built in INFLV2.007).
    Artifact key TBD by Andrew's pick — COO will update this TO with specifics
    after Andrew's selection.
  </objective>

  <scope>
    <task id="1" label="Review Andrew pick + COO implementation spec">
      After Andrew selects a candidate from INFLV2.004, COO will send an updated
      implementation spec to DS with:
        - Chosen insight name
        - Platinum artifact key (e.g., platinum/firm/insights_panel.json)
        - Required JSON shape (data fields + structure)
        - Gold script target (new script or D_04 extension)
      Wait for that spec update before coding. Do NOT implement speculatively.
    </task>

    <task id="2" label="Implement gold script or D_04 extension">
      Write the data-emit logic per the implementation spec:
        - Compute insight metric from Orion transactions
        - Emit to platinum artifact at confirmed S3 key
        - Follow existing gold script patterns (from __future__ import annotations,
          pre-commit gate, comp-validate before signaling)
    </task>

    <task id="3" label="Define platinum artifact type contract">
      Document the output JSON shape in a brief comment at the top of the script
      and in a one-paragraph addition to docs/architecture/INFLV2_BOOKS_SCOPE_FREEZE.md
      under "InflectionInsightsPanel artifact contract".
    </task>

    <task id="4" label="Pre-commit gate + commit">
      .tools/ds-commit-gate.sh on all modified/new scripts.
      comp-validate on the new platinum artifact.
      git commit --only [scripts] --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Pre-commit gate PASS for all modified scripts.
    </criterion>
    <criterion id="2">
      comp-validate exits 0 on the new platinum artifact.
    </criterion>
    <criterion id="3">
      Platinum artifact emitted at the confirmed S3 key with non-null insight data.
    </criterion>
    <criterion id="4">
      Type contract documented (artifact JSON shape visible to DE without reading gold scripts).
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO + 0.6.1_AE_PartnerETL + 0.4.0_DE_ClientPlatform with commit hash
      + artifact key + JSON shape summary.
      Subject: RAVC — ADVI_INFLV2.005 COMPLETE | InflectionInsightsPanel artifact live | [hash]
      This RAVC is the go-signal for INFLV2.007 (DE) + INFLV2.009 (AE chain rerun).
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gates: INFLV2.004 COMPLETE + Andrew pick received by COO.
    COO will dispatch the implementation spec after Andrew's selection.
    Do not start implementation without the spec.</constraint>
    <constraint>No emojis in code or print statements.</constraint>
    <constraint>from __future__ import annotations first import in all modified scripts.</constraint>
    <constraint>Do NOT run chain rerun — that is INFLV2.009 (AE scope).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A"
                task="ADVI_INFLV2.004"
                status="open"
                note="3-candidate brief must be complete and Andrew pick received
                before implementation begins."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">New gold script or D_04 extension emitting InflectionInsightsPanel
    artifact. Type contract in INFLV2_BOOKS_SCOPE_FREEZE.md.</deliverable>
    <deliverable type="mcp">RAVC to COO + AE + DE. Go-signal for INFLV2.007 + INFLV2.009.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §3 (Revenue Ops direction)</ref>
    <ref type="gate">INFLV2.004 — design brief + Andrew pick</ref>
    <ref type="scope_freeze">docs/architecture/INFLV2_BOOKS_SCOPE_FREEZE.md (artifact contract home)</ref>
  </references>
</task_order>
```
