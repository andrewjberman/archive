<to_id>ADVI_COTETL.AUAFIX-L1</to_id>
<project>ADVI_COTETL</project>
<title>Verify the 06-19 nightly unblocks the cot silver->gold->AUA chain end-to-end (SERVED artifacts) -- else manual run + re-root-cause</title>
<assigned_to>0.7.0_AE_CloudOps (chain-verify lead) + 0.4.0_DS_ClientPlatform (silver side)</assigned_to>
<issued_by>2.0.0_SA_COO (AUAFIX PRD decomposition, 2026-06-18; CTO PRD ef04a08cc)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>pending</status>
<priority>HIGH -- EVENT-GATED on the 06-19 02:00Z nightly (tomorrow-AM). GATES L2-L5. NOT tonight: the nightly runs at 02:00Z, reviewed tomorrow-AM (no overnight watcher per standing rule). Fires on the artifact landing.</priority>

<references>
  <ref type="prd">docs/architecture/ADVI_COTETL_AUAFIX_PRD.md (ef04a08cc) -- §2 Layer A, §3 partial fix, §5 L1, §7 AC1</ref>
  <ref type="seams">org/seams/cottonwood-bronze-silver-gold-platinum-aua-freeze.md (ddacf120a, AE /seams root-cause)</ref>
  <ref type="partial-fix">DS db9521f3c (dup xlsx header mangle) + 864139e7a (sentinel gate-semantics) + b09296f08 (sentinel emission) -- deployed code/silver/, POST-dates the 06-18 nightly, UNVERIFIED.</ref>
</references>

<scope>
Confirm the 06-19 02:00Z nightly unblocks the chain end-to-end AGAINST THE SERVED ARTIFACTS (never self-report, never rc=0):
- transactions silver succeeds (dup 'Tax Status' header no longer freezes the merge) -> `silver_complete.json` EMITS -> the `cot-silver-complete` EventBridge rule fires gold-run -> fresh gold/platinum AUA `data_as_of` ADVANCES past 06-09.
- AE leg: chain-verify (comp-pipescript deployed cot + the EventBridge fire + the SERVED gold/platinum artifact freshness). DS leg: transactions silver succeeded + partitions advanced past 06-09 + sentinel emitted.
- If it does NOT unblock -> manual chain-run + re-root-cause (the partial-fix premise is FALSIFIED -> re-diagnose before asserting fixed).
- SURFACE the **sentinel-required-set question** to CTO: is `transactions` correctly REQUIRED in the sentinel gate, or should it be snapshot-first-exempt (as holdings is)? -- CTO determination (do not self-resolve). This L1 produces the data; CTO rules.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="tomorrow-AM, before declaring verified">
    <step>
      <run>comp-pipescript deployed cot (confirm silver/gold scripts MATCH live) + read the SERVED gold/platinum AUA artifact's data_as_of (head-object / comp-freshness if registered) -- NOT the run log</run>
      <expect>silver_complete emitted on the 06-19 nightly; gold-run fired; served AUA data_as_of > 06-09. The SERVED artifact is ground truth.</expect>
      <if_mismatch>Chain did NOT unblock -> manual run + re-root-cause. The partial-fix premise is falsified; do NOT declare AC1 met. Escalate to COO+CTO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **GATES L2-L5** -- this is the lead leg. L2/L3/L5 proceed only after L1 confirms (or escalates a manual fix). L4 (alert) is independent-ish (rides F-1) but its synthetic-freeze test wants the chain live.
- **DS (silver side) + AE (chain-verify):** converge on the silver-success signal (DS confirms the transactions merge + sentinel emit; AE confirms the downstream EventBridge fire + served freshness). The DS leg bundles into DS's tomorrow-AM re-engagement.
- **CTO determination:** the sentinel-required-set (transactions REQUIRED vs snapshot-first-exempt) is a CTO call -- L1 surfaces the data, CTO rules. Do not self-resolve.
- **No overnight watcher:** the nightly self-produces; review tomorrow-AM (standing rule).
</cross_domain_coordination>

<acceptance_criteria>
- AC1 (PRD): the cot gold->platinum chain demonstrably FIRES on the 06-19 nightly's SERVED artifacts (silver_complete emits -> gold-run -> AUA data_as_of advances past 06-09) -- OR the chain is proven to need a manual fix + that fix lands + re-verifies. Verified on the SERVED artifact, not self-report.
- The sentinel-required-set question is SURFACED to CTO with the L1 data (transactions required vs snapshot-first-exempt).
- Session log Compiler Tools section reproduces the `<run>` checks with observed served-artifact state + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Verification leg (read SERVED artifacts). If a manual chain-run is needed, that is a DS gold-run (Rule 13, DS commit cycle) -- a re-run of the existing chain, not new reprocessing logic.</no_reprocess_needed></data_reprocess_scope>
