# TASK ORDER — ADVI_COTETL.PROBEFIX

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<date>2026-06-29</date>
<priority>P2 — critical-surface blind monitor (do FIRST, ahead of the AUAFIX queue; small fix)</priority>

## Objective

Restore the `AuthTokenOK` CloudWatch metric emission in the `bd-cot-freshness-probe` Lambda so the
`bd-cot-authtoken-absence` alarm returns to OK. The cot auth/freshness verifier is currently BLIND.

## Grounded context (COO /drive cycle 1, 2026-06-29)

- Alarm `bd-cot-authtoken-absence` in ALARM since 2026-06-28T14:27Z (~22h). Critical-surface SQS delivered it; COO handled + deleted the SQS copy (CloudWatch alarm remains the durable record).
- **GROUNDED (live state):** the probe runs hourly with **0 Lambda errors**; its own 12:26Z log says `OK: /auth/token 200 + access_token -- cookie good`. cot silver is **fresh through the 06-29 partition**, incremental manifests updated 06-28 22:04Z. **The pipeline is HEALTHY — this is NOT a freeze recurrence.** Only the monitor's metric emission is broken.
- **HYPOTHESIS (source-unconfirmed — CONFIRM before fixing, Rule 22):** the probe's 2026-06-26T14:14Z modification (the cot DURABLE GATEWAY AUTH / PIECE-2 work) likely **dropped or renamed the `put_metric_data(AuthTokenOK, namespace=BD/COT/Auth, dim Firm=cot)` call**. The alarm is correctly catching a vanished metric, not a real auth failure. **Read the probe source / the 06-26 diff and confirm the actual mechanism before changing anything** — do not fix on the hypothesis.

## Work

1. CONFIRM the mechanism: read the probe source + the 06-26T14:14Z change; identify exactly why no `AuthTokenOK` SAMPLE_COUNT datapoint is emitted despite a clean run.
2. Restore the `AuthTokenOK` metric emission (namespace `BD/COT/Auth`, dimension `Firm=cot`, the value the alarm expects — SAMPLE_COUNT≥1 per run clears it).
3. Redeploy via **Terraform only** (Lambda = TF-only, CLAUDE.md Rule 1; use `.tools/safe-apply.sh`). Update the source map if the function source changed.
4. Verify: next hourly run emits the metric; alarm transitions ALARM → OK.

<compiler_tools_mandate>
- `comp-iam service bd-cot-freshness-probe` if any new boto3/cloudwatch perm is implicated (PutMetricData).
- `comp-pipescript deployed` / source-map check on redeploy.
- Ground the fix against the LIVE alarm state (ALARM→OK), not the self-report.
</compiler_tools_mandate>

<cross_domain_coordination>
bd-cot monitoring Lambda — cot-firm-separated infra, AE-owned. No DS/portal surface. Touches only the probe Lambda + its TF + (if needed) its IAM. Coordinate with no other active TO; the AUAFIX-DATEMODE chain is adjacent (same cot pipeline) but a different surface.
</cross_domain_coordination>

<acceptance_criteria>
1. Root cause CONFIRMED from source (cite file:line), not the hypothesis.
2. `bd-cot-authtoken-absence` alarm state = OK (verified live via `aws cloudwatch describe-alarms`), AND the `AuthTokenOK` metric shows a fresh SAMPLE_COUNT≥1 datapoint.
3. Redeploy was Terraform (0-diff plan→apply), source map updated if source changed.
4. RAVC to 2.0.0_SA_COO with the confirmed mechanism + the alarm OK evidence.
</acceptance_criteria>

## Sequencing

Do this FIRST — it's small and it restores the freshness monitor that your AUAFIX-DATEMODE work
relies on (the probe also reports `silver/holdings 58.3h/2td` + served AUA 2td, consistent with your
open AUAFIX-DATEMODE-C). Then resume your existing 6-TO queue (COTETL AUAFIX-DATEMODE-B/C/L1,
DC1/DC2 crawls, TSGRAPH P2-2) in its established order. If you believe a different sequence is
right given your queue's prior GOs, MCP me — but the blind verifier closes first.
