# TASK ORDER — ADVI_COTETL.PROBEFIX

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete — CLOSED as already-satisfied (cot self-recovered via human re-auth 06-29 01:57Z; hypothesis falsified from source; NO cot code defect). The real live dead-cookie is 49f -> handled via ADVI_BDAPIMIG.P1-DURABLE (0.6.2_AE) per Andrew's durable-port-only call. The probe SEMANTIC fix (200-no-token -> emit 0) is GO'd as follow-on. COO-accepted 2026-06-29.</status>
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

## GROUNDING NOTE — 0.7.0_AE_CloudOps, 2026-06-29T13:02Z (Rule 22, before any fix)

Mechanism grounded from source + live state. **TO hypothesis FALSIFIED; objective already satisfied.** RAVC to COO 20260629T130233Z.

- **Hypothesis falsified:** probe Lambda has only 2 commits ever (33cf3ec71, 952417807 v0.5.1); NO probe edit at 06-26T14:14. `put_metric_data(AuthTokenOK)` present + correct at `bd-cot-freshness-probe/lambda_function.py:124-139` (emit) and `:312-325` (call). AuthTokenOK emitted hourly for ~2 days AFTER the alleged mod for both firms — a dropped emit cannot do that.
- **cot already healthy (no fix):** AuthTokenOK Firm=cot emitting hourly 06-29 02:00Z->12:00Z; alarm `bd-cot-authtoken-absence` = OK live. Recovery cause: cot session secret re-authed by a human at 06-29 01:57Z (`blackdiamond/cot/session` LastChanged). The 06-28 09:00Z->06-29 02:00Z gap was the soft-dead-cookie window. A cot "metric restore" deploy would be a NO-OP. **Holding.**
- **The live ALARM is 49f (different firm), a REAL dead cookie:** `bd-49f-authtoken-absence` = ALARM; `bd-49f-keepalive` logs HTTP 401 cookie DEAD every cycle since >=04:33Z, publishing opal-bd-49f-cookie-alerts; `blackdiamond/49f/session` LastChanged 06-26 21:13Z. Needs the SAME human BD re-auth that fixed cot. 49f silver still 1td-fresh (not yet frozen).
- **Probe SEMANTIC bug (both twins):** a soft-dead cookie returns `/auth/token` HTTP 200 WITHOUT access_token; code `:313-321` mis-buckets `200 && !has_token` as transient (auth_ok=None -> no datapoint) instead of dead (emit 0). So `authtoken-dead` stays falsely OK and the dead state masquerades as "absence/blind." Proposed fix (firm-parameterized -> covers cot+49f): emit AuthTokenOK=0 on 200-without-token so the DEAD alarm fires the real re-auth signal. **RAVC1 GO requested before TF deploy** (cross-firm + alarm-behavior change).

Awaiting COO: (1) close cot PROBEFIX as already-satisfied; (2) routing of the 49f human re-auth; (3) GO on the probe semantic fix.

## Sequencing

Do this FIRST — it's small and it restores the freshness monitor that your AUAFIX-DATEMODE work
relies on (the probe also reports `silver/holdings 58.3h/2td` + served AUA 2td, consistent with your
open AUAFIX-DATEMODE-C). Then resume your existing 6-TO queue (COTETL AUAFIX-DATEMODE-B/C/L1,
DC1/DC2 crawls, TSGRAPH P2-2) in its established order. If you believe a different sequence is
right given your queue's prior GOs, MCP me — but the blind verifier closes first.
