# Task Order: ADVI_ETLFIX WS-3 -- 49F-MDPF custody + aggregate (Pipeline C) close-out

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-advi-etlfix-ws3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <completed>2026-07-07</completed>
    <reconcile_note>Status-reconciled 2026-07-20 by 2.0.0_SA_COO (Andrew-direct backlog review). MDPF custody flip (bd->schwab-native) FIRED + verified on the 3-way never-widen co-sign @12dd979c7 (2026-07-02); LD-0292 ($528mm 49financial custody defect) CLOSED @0a4fed471 (cured by the pipeline running normally, DO-NOT-REPAIR never broken); mdpf served is T-1 healthy (comp-freshness: as_of 2026-07-18, 1 trading day behind the 2026-07-20 frontier = PASS). The custody-flip substance is DONE and the broader MDPF/ETLFIX work now lives under OPAL_CONSOLIDATION. Superseded-by-completion. NOTE: this reconcile does not separately re-certify the formal WS-3 leg-2 protection-gate pattern DOC (a non-blocking write-up); flag if you want that produced.</reconcile_note>
    <dispatch_state>DISPATCHED (post-reboot /drive cycle; PRD authored 2026-07-02, 5 days undecomposed -- WS-3 carved out first since 0.5.0 is live+idle and is the sole named owner)</dispatch_state>
    <gate_note>COO-RESOLVABLE now. Confirms/closes the custody flip that already fired (0.5.0, commit 12dd979c7, SSM schwab v2 @14:06Z) -- this TO is the close-out + hardening, not new build.</gate_note>
  </metadata>

  <objective>Confirm the 49F custody flip (bd -&gt; schwab-native) is durably freshness-correct day-over-day, get CVO's post-flip per-field parity cert, close the MDPF flip deploy-completion ledger, and harden the leg-2 protection gate (fresh-but-wrong cannot replace known-stale on the first schwab-native nightly) as a reusable pattern per ADVI_ETLFIX PRD WS-3 (docs/architecture/ADVI_ETLFIX_PRD.md Section WS-3).</objective>

  <requirements>
    <requirement id="1">Confirm schwab-native custody has advanced on at least one full nightly cycle post-flip (data_as_of increments, no re-freeze) -- gated on WS-2 Schwab-ingest health (0.7.0~A / 0.6.2 canonical-schwab-si2), verify not assume.</requirement>
    <requirement id="2">CVO post-flip per-field parity cert: bd-vs-schwab-native field-for-field comparison on the transition date, confirming no-unexpected-widen (CTO never-widen caveat from the project JSON).</requirement>
    <requirement id="3">Close the MDPF flip deploy-completion ledger entry (rollback armed per project JSON -- confirm rollback path still valid, then close per CLAUDE.md NEVER-law deploy-completion gate).</requirement>
    <requirement id="4">Document the leg-2 protection gate (fresh-but-wrong vs known-stale) as a generalizable pattern note for WS-5's cross-cutting contract -- do not build the WS-5 contract itself, just leave the pattern description for CTO/CVO/COO to fold in.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-freshness mdpf</run>
        <expect>MDPF custody partition shows data_as_of advancing post-flip (not frozen at the pre-flip date); PASS on the freshness check.</expect>
        <if_mismatch>STOP -- if still frozen, this is NOT a close-out TO, it's a re-open of the freeze; escalate to COO before proceeding.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io schwab_native_ingest</run>
        <expect>WRITES includes the MDPF custody artifact; no unexpected COLUMN GAPS vs the pre-flip bd-sourced schema.</expect>
        <if_mismatch>STOP -- document the schema delta before writing the parity-cert ask to CVO (they need the field map).</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-blast mdpf_custody_flip</run>
        <expect>Downstream consumers limited to the known MDPF_ASSETS aggregate + portal serving layer already documented; no new undeclared consumer appeared.</expect>
        <if_mismatch>STOP -- surface new consumer to COO before closing the ledger.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-freshness mdpf --history 3</run>
        <expect>3 consecutive nightly advances post-flip, no re-freeze.</expect>
        <if_mismatch>Surface to COO/CVO -- do not close the ledger on fewer than 3 confirmed advances.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>Shared surface with WS-2 (49F/Schwab source health, 0.7.0_AE_CloudOps~A + 0.6.2) -- this TO's Requirement 1 is gated on WS-2's ingest health, not independent.</item>
    <item>Shared surface with DATA_SSOTMG (the Schwab-SSOT-cutover coordinating program) -- do not duplicate DATA_SSOTMG's scope; this TO is the ETLFIX-side close-out of the already-fired flip, not the SSOT migration itself.</item>
    <item>CVO owns the parity cert (Requirement 2) -- do not self-cert.</item>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion>comp-freshness mdpf shows 3 consecutive post-flip nightly advances (Requirement 1) -- cite the comp-freshness output in the session log.</criterion>
    <criterion>CVO parity cert delivered and cited by commit hash (Requirement 2).</criterion>
    <criterion>Deploy-completion ledger entry for the MDPF flip shows CLOSED, not just in-window (Requirement 3) -- cite via deploy_ledger.py check output.</criterion>
    <criterion>Session log's Compiler Tools section reproduces every &lt;run&gt; from &lt;compiler_tools_mandate&gt; with observed output and explicit pass/fail vs &lt;expect&gt;. Missing rows = REWORK.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="prd">docs/architecture/ADVI_ETLFIX_PRD.md</ref>
    <ref type="project">org/projects/ADVI_ETLFIX.json</ref>
  </references>
</task_order>
```
