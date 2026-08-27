<to_id>NFRA_GRAPHS.D7-FIX.T5</to_id>
<project>NFRA_GRAPHS</project>
<title>D7-FIX T5 — comp-platinum attribution improvements (full-key resolution + Lambda producer ingestion + dynamic-URL annotation)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (D7-FIX.T4 RAVC2 root-cause + DE D7 pilot FP pattern, ~170000Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_GRAPHS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<priority>P3 — tooling improvement; no production breakage; improves scan accuracy for future D7-class pilots</priority>

<scope>
Three comp-platinum attribution improvements surfaced by D7-FIX.T4 investigation (DS) + the DE D7 pilot auth:NONE FP pattern:

1. FULL-KEY ATTRIBUTION (not prefix-based): comp-platinum currently resolves `platinum/advisors/{id}/` artifacts by PREFIX to the earliest D_04 function writing any `platinum/advisors/` key. This produces wrong function attribution for `nna_clients.json` (right script D_04, wrong function — build_firm_mix_summary vs build_advisor_nna_clients L2653) and `timeseries.json` (same — build_advisor_summaries L687), and completely wrong script attribution for `exec_summary.json` (D_04 prefix match; real producer = exec_summary_generator Lambda, infra/aws/lambda/exec-summary-generator/exec_summary/). Fix: resolve producers by FULL key match (filename), not prefix alone.

2. LAMBDA PRODUCER INGESTION: comp-platinum has no Lambda producers in its graph. Lambda-produced platinum artifacts fall onto prefix-sharing gold scripts. Fix: ingest known Lambda producers into the platinum producer graph so Lambda-produced artifacts attribute correctly. Minimum required: exec_summary_generator -> `platinum/advisors/{id}/exec_summary.json`. Systematic Lambda-producer audit is P3 deferred (D4 post-stitch scope); at minimum hard-code the known Lambda producer from T6 investigation.

3. DYNAMIC-URL ANNOTATION (from DE D7 pilot, 8-hit FP): `auth: NONE` on a `{param}/book.json{param}` dynamic URL is a static-analysis false positive — comp-platinum emits bare `auth: NONE` even when CF behavior covers the path. Fix: detect `{param}/...{param}` dynamic URL pattern and emit `auth: NONE (dynamic URL — verify via comp-routes)` instead of bare `auth: NONE`. Converts a misleading signal to actionable.

Sequencing: items 1+2 are coupled (same prefix-match root cause); item 3 is independent. Recommend 1+2 together, 3 can ride separately or bundle.

Acceptance:
- comp-platinum for BD AdvisorPublicProfile / DistributionTab / ClientsTab resolves `nna_clients.json` to `D_04::build_advisor_nna_clients()`, `timeseries.json` to `D_04::build_advisor_summaries()`, `exec_summary.json` to `exec_summary_generator Lambda`
- comp-platinum for any component fetching a `{param}/book.json{param}` URL shows `auth: NONE (dynamic URL ...)` not bare `auth: NONE`
- graph-call-manifest.yaml `anomaly.orphan.dead_producer` + `anomaly.auth.missing_edge` anti_pattern notes remain accurate (COO author-line patch if text update needed)
- No regression in comp-platinum cached/warm performance baseline
- RAVC2 to COO on completion

Note: T6 (exec_summary_generator source recovery) is a companion TO — run T6 investigation before finalizing item 2 source code, as the Lambda .py may need to be in-repo first.
</scope>
