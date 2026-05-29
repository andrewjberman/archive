<task_order>
<id>FIND_INSURE.024</id>
<title>FIND_INSURE Phase 2A — LinkedIn/Lusha LIVE-DISPATCH loop (cost-gate-verified, Option-B 24-IMO subset)</title>
<issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<project>FIND_INSURE</project>
<created>2026-05-29</created>
<note>BACKFILL — this TO documents work GO'd via MCP 2026-05-29T18:24Z (DS~C lane bring-up) + scope-confirmed 18:25Z, executed + RAVC2-ACCEPTED 18:41Z. Authored post-hoc for the audit record per TO_COMPILER_GATE + CTO request (run provenance). The GO authorized start; this file closes the structural record.</note>

<references>
  <ref type="prd">docs/architecture/FIND_INSURE.md (v0.7.2)</ref>
  <ref type="config">Option B subset config dabb2e106 (top-quintile + adjacent-Series, ~24 IMOs; Andrew Q1 resolution 2026-05-28)</ref>
  <ref type="deliverable">docs/briefs/find-insure-024-ranked-target-list-20260529.md (d481a3a32)</ref>
  <ref type="upstream">scoring.json (DS~E .023, 99/99 @2026-05-27); Blocker-2 live-wire (f4d424037)</ref>
</references>

<scope>
Fire the FIND_INSURE Phase 2A LinkedIn/Lusha org-chart enrichment LIVE-DISPATCH loop over the Option-B 24-IMO subset, run_date=2026-05-27, under the light/fast/local v0.1 regime (B local/SSM driver; no heavy API-trial protocols; deployed-Lambda productionization deferred per AC6). Cost-gate-live-verify probe is a HARD precondition (verify the live cost-gate behaves before fanning the loop). IMO research-subject data is NOT client PII — SSE-S3 baseline (no SSE-KMS apparatus required) per Andrew sovereign 2026-05-28.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write/run">
    <step>
      <run>cost-gate-live-verify probe (data/find/imo/scripts/_meta/costgate_live_verify_probe.py)</run>
      <expect>Exit 0, all 3 live legs PASS: LiveCostGate (DDB find-insure-cost-state atomic ADD, isolated 9999-01-01 partition, delta-asserted), LiveAlerter (SNS publish), LiveS3Writer (S3 PutObject). Distinguish a real cost-gate failure from a stale encryption-mode assertion.</expect>
      <if_mismatch>STOP. A real cost-gate leg failure blocks the loop. A stale aws:kms assertion (PRD-v0.5 era; SSE-S3 ruling makes KMS optional) is a probe-staleness finding, NOT a cost-gate failure — log it + proceed.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="during run (driver HARD-GATE protocol)">
    <step>
      <run>dry-run -> canary-1 (single IMO) -> full --live, with cost-gate hard-halt active</run>
      <expect>dry-run resolves all 24 (0 missing-domain); canary clean; full run completes with NO hard-halt (cost-gate held within budget).</expect>
      <if_mismatch>STOP on hard-halt or canary failure; surface to COO before --live fan.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after run">
    <step>
      <run>aws s3 ls per-IMO gold under corp/{slug}/gold/linkedin-scrape/2026-05-27/</run>
      <expect>_company_scored.json + employees_scored.json present + non-empty for scored IMOs; benign no_company_match rows carried transparently.</expect>
      <if_mismatch>Surface partial/empty artifacts to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
  <criterion>cost-gate-live-verify probe exit 0, all 3 legs PASS (KMS-flag dispositioned: matches deployed reality OR flagged as probe-staleness, non-blocking).</criterion>
  <criterion>.024 loop fires over the 24-IMO Option-B subset at run_date=2026-05-27 with NO uncontrolled cost-gate hard-halt.</criterion>
  <criterion>Per-IMO gold scores land on S3; ranked target-list deliverable produced (human brief + machine table).</criterion>
  <criterion>Session log Compiler Tools section reproduces each mandate run + observed result + pass/fail vs expect.</criterion>
</acceptance_criteria>

<evidence>
Commit 6c3ffc871 (DS~C, work-cycle:1835Z). Probe VERIFIED LIVE (exit 0, 3 legs PASS; aws:kms assertion PASSED = matched deployed reality, CMK find-insure-data-key exists; conditional probe-maintenance follow-up only if infra later stripped to SSE-S3). Loop: 24 IMOs, 52 credits, NO hard-halt, 23/24 bronze=completed, 1 benign no_company_match (annuity-solutions, 0 credits). Gold ranked-scores landed s3://opal-data-imo/corp/{slug}/gold/linkedin-scrape/2026-05-27/ (top: preferred-marketing-associates 0.39 / eagle-strategies 0.375 / integrity-marketing-group 0.35). Ranked target-list brief d481a3a32. COO RAVC2-ACCEPT 2026-05-29T18:41Z. Analytical findings: series_licensed dimension dormant by-design (org-chart-only tier; contact-reveal deferred v0.7.3); score compression 0.19-0.39 (depth lever = contact-reveal, not breadth).
</evidence>
</task_order>
