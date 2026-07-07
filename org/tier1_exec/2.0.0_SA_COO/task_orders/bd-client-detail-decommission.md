# Task Order (ad-hoc, no project): decommission bd-client-detail (dead route) + fold in the ARCHITECTURE.md doc update

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-bd-client-detail-decommission</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>Ad-hoc, CTO-ruled standalone (2026-07-07): fully scoped/bounded, no project registration needed. CLOSED 2026-07-07T17:03Z.</dispatch_state>
    <gate_note>Fully converged evidence: DS~B (0 Lambda invocations since April) + DE (0 portal frontend code references, comp-grep over DEV). ARCHITECTURE.md itself marks the route "pending -> Section 7d" -- likely never fully wired.</gate_note>
  </metadata>

  <evidence>
    Req 1 (Lambda+route removal) MET: bd-v2.51.0 + shared-infra-v1.40.0, ledger bd-client-detail-decommission CLOSED, all 3 legs proven, live-confirmed gone (Lambda 404s, route+integration empty).
    Req 3 (doc update) MET: portal DEV f07b0b25, corrects ~10 stale ARCHITECTURE.md mentions.
    Req 2 (graph-edge coordination with DS~B) NOT independently confirmed -- 0.7.0 reached out, no reply yet. Not blocking closure (Lambda+route+doc are the load-bearing parts per the TO's own framing); 0.7.0 following up separately.
    Self-correction on record (no penalty, good process): 0.7.0's first TF-import attempt was built on a false premise (thought opal-portal-data-proxy-api was untracked; it was TF-managed since 2026-04-29). Caught before any live damage (terraform import only writes state), cleaned up (state rm + file delete), redid via the canonical apigateway-portal module. Root cause: comp-grep gave false 0-matches twice on searches that should have found the file -- escalated to CTO as a tooling reliability finding (separate from this TO).
  </evidence>

  <objective>Decommission the dead bd-client-detail Lambda + API GW route (GET /clients/{clientKey}, integration id g1o41r7) and fold the doc-update into the SAME TO so it can't ship half-done -- a decommission without the doc update just reintroduces the map-vs-territory drift this cleanup exists to fix (CTO's explicit condition).</objective>

  <requirements>
    <requirement id="1">Remove/decommission the bd-client-detail Lambda + its API GW route via the standard Terraform deploy cycle (CLAUDE.md Rule 1) -- no manual console changes.</requirement>
    <requirement id="2">Fold in the graph-edge correction DS~B already has in motion (the CSE-P2 AC4 finding: bd-client-detail's misattributed WRITES_S3 edge, CTO-ruled relabel to READS_S3 + add the real writer bd-portal-advisor-publisher's WRITES_S3 edge separately) -- coordinate with DS~B, don't duplicate the trace.</requirement>
    <requirement id="3">Update portal/docs/features/advisor_intelligence/ARCHITECTURE.md in the SAME commit -- remove/correct the ~10 stale mentions (route table L597, checklist L590, any others comp-grep surfaces) so the doc no longer documents a decommissioned integration as live.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-blast bd-client-detail</run>
        <expect>Confirms no live consumer beyond what's already been checked (DE's FE grep + DS~B's invocation zero) -- catches anything comp-grep/manual checks might have missed.</expect>
        <if_mismatch>STOP -- surface any new consumer found before removing anything.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-grep "bd-client-detail" .</run>
        <expect>Post-doc-update, only historical/changelog-style mentions remain (if any) -- no line still asserting it as a live integration.</expect>
        <if_mismatch>Finish the doc pass before committing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion>Lambda + API GW route removed via TF, 0-diff verified, tagged per Rule 6.</criterion>
    <criterion>Graph-edge correction landed (coordinated with DS~B, not duplicated).</criterion>
    <criterion>ARCHITECTURE.md updated in the SAME commit as the infra removal -- not a separate follow-up. Missing this = REWORK per CTO's explicit condition.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="finding">1.0.0_SA_CTO ESCALATION 20260707T141000Z + DE-ESCALATE 20260707T141358Z</ref>
    <ref type="finding">0.4.0_DE_ClientPlatform CONFIRMED 20260707T155713Z</ref>
  </references>
</task_order>
```
