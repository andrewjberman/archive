<to_id>NFRA_INFRPT.P1</to_id>
<project>NFRA_INFRPT</project>
<title>The high-value new signals: DATA FRESHNESS (per-pipeline served-artifact age vs cadence) + DRIFT (manifest/surface/source-map/terraform)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_assignees>0.4.0_DS_ClientPlatform (or a data-platform DS) — the served-artifact freshness wiring (comp-freshness / pipescript reuse); AE owns the Lambda + drift checks</co_assignees>
<issued_by>2.0.0_SA_COO (NFRA_INFRPT decomposition 2026-06-16; CVO proposal 6d5954360 §B/§E)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>staged</status>
<priority>HIGH (biggest operational payoff; all from existing comp-tools). Lands AFTER P0 (P0 stops the misleading output; P1 adds the signals the fabric keeps getting bitten by). Gate: P0 landed + AE/DS capacity.</priority>

<references>
  <ref type="proposal">docs/briefs/infra-report-revamp-proposal-20260616.md §B (FRESHNESS) + §E (DRIFT) + the section table</ref>
  <ref type="reuse">.tools/comp-freshness, pipescript (served lists), comp-manifest-check, comp-surface-check, lambda-source-map.json, terraform state</ref>
</references>

<scope>
**(B) DATA FRESHNESS section.** For each pipeline (bd-gold, inf, cot, mdpf, yang/model_portfolios, NNA, news): served-artifact age vs its cadence -> STATUS OK/WATCH/RED. THE signal the firm keeps getting bitten by (inf/mdpf staleness P0; the SmartX false-STALE P0 replaced a stand-in for this). Reuse comp-freshness + the pipescript served lists; do NOT hardcode paths (that is exactly what made the SmartX section drift). For a D-1 pipeline, freshness = serving-day keyed (per the D1-freshness lesson), not same-day.
**(E) DRIFT section.** "Did anything change/deploy that shouldn't have?" — comp-manifest-check (source-map drift) + comp-surface-check (critical-surface drift) + lambda-source-map vs deployed + terraform drift. Surface NEW drift since the last report (state-change, not a standing list).
Both sections emit the per-line STATUS (OK/WATCH/ACT/RED) + a one-line reason + a pointer (the action-first format).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-freshness (enumerate the served-artifact set + cadences) + pipescript --list (the canonical pipeline/served map)</run>
      <expect>The freshness section is DERIVED from comp-freshness/pipescript output, NOT a hardcoded path list -> it cannot drift the way the SmartX section did. Confirm coverage of bd/inf/cot/mdpf/yang/NNA/news.</expect>
      <if_mismatch>If a pipeline's served artifact is not in comp-freshness, surface it (a coverage gap is itself a finding) — do NOT silently omit.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service opal-infrastructure-monitor</run>
      <expect>The freshness reads (S3 head-object mtimes) + drift reads use existing perms (S3 + the comp-tool outputs). No new IAM unless a new data source is read.</expect>
      <if_mismatch>Add any new read perm via Terraform + comp-iam gaps.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy">
    <step>
      <run>comp-iam gaps (if iam.tf changed)</run>
      <expect>No new gap.</expect>
      <if_mismatch>Resolve before apply (Terraform-only).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Trigger a report + verify the Freshness + Drift sections against KNOWN live state (e.g. a deliberately-stale pipeline reads RED; a fresh one OK)</run>
      <expect>Freshness STATUS matches ground truth per pipeline; Drift surfaces real recent drift (or honestly "none since last report"). No false-STALE, no false-clean.</expect>
      <if_mismatch>Reconcile to ground truth — the whole point is the monitor matches reality.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- P1/B supersedes P0's minimal SmartX-freshness stand-in (generalizes it per-pipeline). No conflict — P0 stopped the false alarm, P1 builds the real section.
- FRESHNESS feeds the P3 agent-JSON feed (a freshness RED -> a /drive dispatch signal). Emit the per-pipeline STATUS in a structured shape P3 can consume.
- DS owns the comp-freshness/pipescript served-artifact wiring; AE owns the Lambda integration + the drift checks (comp-manifest/surface, terraform). Coordinate the section's data contract before the DS commits the freshness compute.
</cross_domain_coordination>

<acceptance_criteria>
- FRESHNESS section: per-pipeline served-artifact age vs cadence -> OK/WATCH/RED, DERIVED from comp-freshness/pipescript (no hardcoded paths), covering bd/inf/cot/mdpf/yang/NNA/news.
- DRIFT section: new manifest/surface/source-map/terraform drift since last report (state-change, not a standing list).
- Phase-3 verify against known live state (a stale pipeline reads RED; fresh reads OK) — no false-STALE, no false-clean.
- Deployed via Terraform; comp-iam gaps clean if iam.tf changed.
- Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Report-generator logic only; reads live served-artifact state each run. No pipeline re-emit.</no_reprocess_needed></data_reprocess_scope>
