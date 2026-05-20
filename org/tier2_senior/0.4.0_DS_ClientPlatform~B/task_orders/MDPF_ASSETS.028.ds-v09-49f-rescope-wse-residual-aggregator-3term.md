<task_order>
  <metadata>
    <id>MDPF_ASSETS.028</id>
    <slug>ds-v09-49f-rescope-wse-residual-aggregator-3term</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-20 (authored on PRD v0.9, 8951ce8f0)</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>CONFIRMED by 1.0.0_SA_CTO~B 2026-05-20 (203606Z, reviewed vs PRD v0.9 §3.4/§3.0.1, no redline) + GO'd by 2.0.0_SA_COO~B. CTO~B confirmations folded in: methodology_version stamp = `v0_9`; the Phase-0 RPS-vs-crosswalk decision is CTO~B's call on DS~B's coverage/completeness characterization (CTO~B lean = the crosswalk IF the RPS ~5% gap -- ~$80M on $1.65B, material -- cannot be cleanly closed, but DS~B's empirical finding decides; do NOT pre-decide). The Phase-0 Schwab-whole-source finding routes to CTO~B mid-execution.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF CRITICAL PATH. PRD v0.9 (Andrew's 3rd + final 49F-basis revision) re-scopes the 49F headline to the full Schwab 49F book. This TO re-scopes WS-E (1b) + the aggregator (headline formula) TOGETHER -- they MUST co-land (the SMA-inclusive/exclusive choice has to be consistent across both or the headline double-counts or under-counts).</priority>
    <sla>~4-6h DS wall -- WS-E residual re-scope + aggregator 3-term revert + fixture re-baseline + reconciliation; the Schwab-whole-source Phase-0 decision is the variable.</sla>
    <deadline>Critical path -- prompt. Gates .029 (.016-equivalent full backfill) + .030 (.026-equivalent legacy emit), both of which CTO~B sequences AFTER this lands.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.9 (committed 8951ce8f0) -- §3.4 + §3.0.1 are the formula of record.</prd>
    <origin>Andrew Mandate Change 3, settled 2026-05-20 (3rd + final 49F-basis revision), via CTO~B. Resolved by the MDPF_ASSETS.027 SmartX-coverage probe (SmartX cannot yield a clean 1b -- opal7 credential model-only) + Andrew's explicit mechanism choice.</origin>
    <v09_mandate>49F (Cohort 1) = the FULL SCHWAB 49F book (~$1.65B). 1a (model) + 1c (SMA) from SmartX (the WS-B feeder already pulls both). 1b (non-model) = Schwab_49F_whole MINUS 1a MINUS 1c -- the partitioned residual. 1a + 1b + 1c = the full Schwab value; the three are DISJOINT (1b is SMA-EXCLUSIVE). Headline = full Schwab 49F + 2a (Eclipse Inflection model) ~= $1.75B. Cohort 0 + 2b audit-only/excluded. v0.9 SUPERSEDES v0.7 (full-BD-book certified_aua) AND v0.8 (1c-nested-in-1b).</v09_mandate>
    <basis_history>49F basis revisions: (1) Schwab-only ~$1.655B; (2) v0.7 full-BD-book certified_aua ~$1.81B; (3) v0.9 full-Schwab-49F-book ~$1.65B (this TO). .024 (aggregator 2-term) + .025 (WS-E full-BD-book) + .016 (backfill) were built + RAVC-accepted on basis (2) -- they are CLOSED and kept as the historical record; this is a FRESH TO, not a re-open.</basis_history>
    <pipeline_rule>Rule 13 (DS commit + S3 deploy cycle for data/*/scripts/gold/*.py + feeders). Rule 14 (.tools/ds-commit-gate.sh every .py edit). Rule 15 (`from __future__ import annotations` first import). Rule 17 (gold tier -- business-logic field-handling permitted; silver stays passthrough).</pipeline_rule>
  </references>

  <context>
    PRD v0.9 re-scopes the 49F headline from the v0.7 full-Black-Diamond-book basis to the full Schwab 49F book. Two scripts change and MUST land together: the WS-E feeder (1b derivation) and mdpf_aggregate_aua.py (the headline formula). v0.9's 1b is the SMA-EXCLUSIVE residual Schwab_49F_whole - 1a - 1c, so the aggregator's 49F partition reverts to a 3-TERM sum 1a + 1c + 1b. The v0.8 2-term formula existed ONLY because v0.8's 1b was SMA-inclusive; v0.9 flips BOTH in lockstep -- SMA-exclusive 1b <-> 3-term sum. If WS-E and the aggregator land separately, an intermediate state either double-counts SMA (3-term sum over a SMA-inclusive 1b) or under-counts (2-term over a SMA-exclusive 1b). Hence one atomic TO.
  </context>

  <scope>
    <step>Phase 0 -- SCHWAB-WHOLE SOURCE PICK (architecture call -> route to CTO~B). 1b = Schwab_49F_whole - 1a - 1c needs a COMPLETE daily Schwab 49F total. Two candidate sources: (A) Schwab RPS silver (~95% coverage per MDPF_ASSETS.011) -- already in-pipeline, but the ~5% gap must be characterized + a completeness story given; (B) revive the retired compute_partner_custody_total crosswalk (.025/.016 Correction 7 deleted it -- git-recoverable). Investigate both, characterize coverage/completeness/freshness, and route a Phase-0 finding + recommendation to 1.0.0_SA_CTO~B (CC 2.0.0_SA_COO~B). CTO~B makes the RPS-vs-crosswalk call. Do NOT proceed to Phase 1 until CTO~B rules the source.</step>
    <step>Phase 1 -- WS-E re-scope. Re-scope the WS-E 1b derivation to 1b = Schwab_49F_whole - 1a - 1c (SMA-EXCLUSIVE residual) off the CTO~B-ruled Schwab-whole source. 1a + 1c from the existing WS-B SmartX feeder. The output 1b must be the disjoint non-model residual -- NOT SMA-inclusive (that was v0.8). Preserve the methodology_version stamp convention (-> v0_9 or per CTO~B).</step>
    <step>Phase 2 -- aggregator re-scope. Revert mdpf_aggregate_aua.py's 49F partition to a 3-TERM sum: 49F_total = 1a + 1c + 1b. This reverts .024's 2-term formula. SAFE -- no SMA double-count -- BECAUSE v0.9's 1b is SMA-exclusive (Phase 1). Headline opal_aggregate_aua = 49F_total (1a+1c+1b) + 2a. Cohort 0 + 2b stay audit-only/excluded. The §7 reconcile sentinels + identity checks must pass on the 3-term v0.9 output.</step>
    <step>Phase 3 -- fixture re-baseline + reconciliation. Re-baseline the aggregator + WS-E fixtures to v0.9 expected values. Reconcile the live v0.9 run vs known anchors -- 49F_total should land at ~$1.65B (full Schwab book), headline ~$1.75B. Sentinel-3 independent recompute must equal the headline to $0.00.</step>
    <step>Phase 4 -- DS commit + S3 deploy per Rule 13, BOTH scripts in ONE commit/deploy (co-land): ds-commit-gate.sh -> safe-commit.sh agent --author -> push CLOUD -> aws s3 cp both scripts -> comp-pipescript deployed MATCH. WS-E feeder + aggregator deploy together -- no intermediate state where one is v0.9 and the other v0.8.</step>
    <step>Phase 5 -- RAVC2 to 2.0.0_SA_COO~B (CC 1.0.0_SA_CTO~B): the Schwab-whole-source decision, the WS-E + aggregator diffs, fixture re-baseline, the reconciliation transcript vs anchors, deployed commit + S3 MATCH.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC0">Phase-0 Schwab-whole-source finding routed to CTO~B; CTO~B's RPS-vs-crosswalk ruling obtained before Phase 1. [Gates Phases 1-5.]</ac>
    <ac id="AC1">WS-E 1b = Schwab_49F_whole - 1a - 1c, SMA-EXCLUSIVE (disjoint from 1c), off the CTO~B-ruled source.</ac>
    <ac id="AC2">mdpf_aggregate_aua.py 49F partition = 3-TERM sum 1a + 1c + 1b; headline = 49F_total + 2a; Cohort 0 + 2b audit-only.</ac>
    <ac id="AC3">WS-E + aggregator land in ONE commit + ONE S3 deploy -- no intermediate v0.9/v0.8 mixed state.</ac>
    <ac id="AC4">Reconciliation: 49F_total ~= $1.65B, headline ~= $1.75B vs anchors; §7 identity + sentinels PASS; sentinel-3 independent recompute == headline to $0.00. Fixtures re-baselined to v0.9, all PASS.</ac>
    <ac id="AC5">Rule 13 deploy cycle (comp-pipescript deployed MATCH). Rule 14 gate. Rule 15 first-import. No emoji. Session log with Compiler Tools section. RAVC2 to COO~B CC CTO~B.</ac>
  </acceptance_criteria>

  <out_of_scope>
    The .016-equivalent full Schwab+SmartX historical backfill -> a separate fresh TO (MDPF_ASSETS.029), sequenced AFTER this lands (CTO~B's sequence), non-destructive dry-run first. The .026-equivalent legacy-emit re-scope -> a separate fresh TO (MDPF_ASSETS.030), after .029. Re-opening the closed .024/.025/.016 (kept as historical record). Cohort 0 / 2b methodology (audit-only, unchanged).
  </out_of_scope>

  <deliverables>
    - WS-E feeder (1b SMA-exclusive residual) + mdpf_aggregate_aua.py (3-term 49F partition) re-scoped to PRD v0.9, co-landed in one commit + one S3 deploy; fixtures re-baselined; reconciliation vs anchors; RAVC2 to COO~B CC CTO~B.
  </deliverables>
</task_order>
