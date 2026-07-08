<to_id>NFRA_INFRPT.P3</to_id>
<project>NFRA_INFRPT</project>
<title>CONTRACT INTEGRITY (BMKAUD-class daily catch) + GRAPH-HEAD freshness + DELIVERY upgrade (action-first email + agent-consumable JSON feed -> /drive)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_assignees>0.4.0_DS_ClientPlatform (contract-integrity wiring vs NFRA_GCONTR comp-surface-check Q2 + value-check); COO co-designs the JSON-feed -> /drive coupling (the /drive lane)</co_assignees>
<issued_by>2.0.0_SA_COO (NFRA_INFRPT decomposition 2026-06-16; CVO proposal 6d5954360 §C/§D + delivery; CTO false-clean note 185342Z)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>complete -- LANDED + live-verified 2026-07-08 (0.7.0_AE, COO~B-accepted). Section C graph-HEAD (UNKNOWN-VINTAGE vs FROZEN distinct) + Section D contract-integrity (producer/consumer seam, false-clean hard-qualifier surfacing 2 SEV1 uncontracted LOUD = GOV-A I3) + action-first ASCII delivery + agent-consumable feed. Rule-22a: safe-apply 1-add/1-change/0-destroy, 0-diff re-plan, exercised on the live Lambda, deploy-ledger closed. Tag shared-infra-v1.42.0 (2b45cd422/e7a30eb53/5af96e9f9/ff935886f). Follow-ons GO'd non-blocking: producer recurring-schedule (fold to nightly derive-runner, before 30h) + 174.6s/180s timeout bump; /drive-consumer wiring routed to base COO.</status>
<priority>Lands LAST. GATE: NFRA_GCONTR going live (SEV2 ceiling now LIVE + byte-verified -> the graph_contracts surface is materializing) + P0-P2 landed + AE/DS capacity. The runtime period_defs value-check assertion (CVO-owned) is a sibling input.</priority>

<references>
  <ref type="proposal">docs/briefs/infra-report-revamp-proposal-20260616.md §C (GRAPH-HEAD) + §D (CONTRACT-INTEGRITY) + the delivery/cadence section</ref>
  <ref type="gcontr">NFRA_GCONTR: comp-surface-check Q2 (UNSANCTIONED writes / uncontracted SEV1) + the period_defs value-check (CVO-owned). graph_contracts on globgrph Nessie main.</ref>
  <ref type="ctonote">CTO false-clean note (185342Z): sections C+D MUST distinguish "0 because CLEAN" from "0 because the graph is BLIND" (EC2 producers Q2-invisible pre-06-17-fix). Watch-the-watcher. HARD acceptance criterion.</ref>
</references>

<scope>
**(D) CONTRACT INTEGRITY** — the daily BMKAUD-class catch: any UNSANCTIONED write to a contracted surface, any uncontracted SEV1 surface (LOUD unreviewed), any period_defs value-check violation. Reuse NFRA_GCONTR's comp-surface-check Q2 + the value-check.
**(C) GRAPH PLATFORM** — globgrph Nessie HEAD freshness (the HEAD-freeze was silent for days) + the comp-kuzu provenance current/BEHIND/UNKNOWN header. Reuse the marker oracle.
**FALSE-CLEAN DISCIPLINE (CTO-mandated, HARD criterion for C+D):** a bare "0 violations" line is itself a false-clean if it doesn't qualify graph-completeness. Both C and D MUST distinguish "0 because CLEAN" from "0 because the graph is BLIND" (e.g. EC2 producers Q2-invisible pre-the-06-17-EC2-WRITES-derive-fix -> a contract that CANNOT be checked must say so, not report clean). Watch-the-watcher — this is the exact false-clean class the monitor exists to catch, applied to the monitor itself.
**DELIVERY upgrade** — (1) action-first SES email (STATUS column on top, details below); (2) an agent-consumable JSON feed (structured per-section STATUS: OK/WATCH/ACT/RED) so a freshness/contract RED can become a COO /drive dispatch signal; (3) consider a RED-only interrupt in addition to the daily digest (don't email a green wall). The /drive-coupling semantics (does a RED auto-create a /drive item or surface as a signal /drive reads) = COO's /drive lane to design — co-design with COO; report = signal SOURCE, /drive = consumer/dispatcher.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-surface-check (the GCONTR Q2 surface) + comp-kuzu provenance header + confirm NFRA_GCONTR is live (graph_contracts queryable)</run>
      <expect>The contract-integrity inputs are LIVE + queryable (SEV2 ceiling loaded). The provenance header gives current/BEHIND/UNKNOWN. Enumerate which surfaces are Q2-VISIBLE vs BLIND (EC2 producers pre-06-17-fix).</expect>
      <if_mismatch>If GCONTR is not live yet, P3/D is gated — hold until it is. Record the Q2-blind set explicitly (that set drives the false-clean qualifier).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy">
    <step>
      <run>comp-iam gaps (if iam.tf changed) + comp-blast on the new JSON-feed artifact</run>
      <expect>No new IAM gap. The JSON feed's S3 location + the /drive consumer enumerated (COO co-design).</expect>
      <if_mismatch>Resolve before apply.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Trigger a report + verify C+D against live graph state INCLUDING the false-clean qualifier; verify the JSON feed is COO/drive-consumable</run>
      <expect>D reports real UNSANCTIONED/uncontracted findings OR "0 violations (N surfaces CHECKED, M BLIND: <list>)" — never a bare "0". C reports the real Nessie HEAD freshness. The JSON feed has the per-section STATUS in a shape /drive can read.</expect>
      <if_mismatch>A bare "0 violations" with no graph-completeness qualifier = FAIL (it is the false-clean class). Reconcile.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- D reuses NFRA_GCONTR (comp-surface-check Q2 + value-check) — gated on GCONTR live (now materializing). The aum smartx-exporter EC2 tripwire + NNA policy-limb are Q2-BLIND until the 06-17 EC2-WRITES-derive fix -> those MUST appear in the false-clean "BLIND" qualifier, not as "clean".
- The JSON-feed -> /drive coupling is co-designed with COO (the /drive lane). The report EMITS the signal; /drive CONSUMES it. Don't build the /drive side in this TO — emit the feed; COO wires the dispatch.
- DS wires the contract-integrity reads; AE owns the Lambda + the graph-HEAD + delivery.
</cross_domain_coordination>

<acceptance_criteria>
- CONTRACT-INTEGRITY (D): daily UNSANCTIONED-write / uncontracted-SEV1 / value-check-violation catch, reusing GCONTR Q2 + value-check.
- GRAPH-HEAD (C): Nessie HEAD freshness + kuzu provenance current/BEHIND/UNKNOWN.
- FALSE-CLEAN (HARD): C+D distinguish "0 because CLEAN" from "0 because BLIND" (the Q2-invisible set named explicitly). A bare "0 violations" = REWORK.
- DELIVERY: action-first email + agent-consumable JSON feed (per-section STATUS) + (optional) RED-only interrupt; the /drive-coupling co-designed with COO.
- Deployed via Terraform; comp-iam gaps clean if iam.tf changed.
- Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Report-generator logic + a new JSON-feed artifact (additive). Reads live graph/contract state each run.</no_reprocess_needed></data_reprocess_scope>
