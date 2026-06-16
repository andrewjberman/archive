<to_id>NFRA_INFRPT.P0</to_id>
<project>NFRA_INFRPT</project>
<title>Stop the misleading output (quick-wins, land FIRST): KILL dead AI-calls section + REPLACE SmartX false-STALE with real served-freshness + RE-HOME the AI triage/security briefing to Claude</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_assignees>none (AE-lane Lambda + IAM work; the dedicated execution lane is allocation-TBD — see priority)</co_assignees>
<issued_by>2.0.0_SA_COO (NFRA_INFRPT decomposition 2026-06-16; Andrew-direct via CVO proposal 6d5954360)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>staged</status>
<priority>HIGH (Andrew-direct). Land-FIRST: stops the report emitting actively-misleading output (false "STALE", meaningless 0/0/100%, dead triage) at the next run. GATE: AE capacity only (0.7.0_AE on YANG TO-4 + GCONTR load; allocation TBD). The Claude re-home mechanism is RESOLVED = BEDROCK InvokeModel (CTO 185342Z) — no longer a gate. NOTE: the report now runs 13:00 UTC (CVO moved the cron 0 14 -> 0 13, LIVE + verified) — Phase-3 verify against the 13:00 run or a controlled invoke.</priority>

<references>
  <ref type="proposal">docs/briefs/infra-report-revamp-proposal-20260616.md (CVO, 6d5954360) — §2/§3/§6 teardown + the new section design</ref>
  <ref type="generator">infra/aws/lambda/infrastructure_monitor/lambda_function.py (opal-infrastructure-monitor; SES email + S3 archive opal-data-portal-v2/infrastructure/reports/)</ref>
  <ref type="ground-truth">SmartX false-STALE: EC2 i-06ebcb27395eb3f49 stopped 06-01; live writer = opal-smartx-ingestion-pipeline Lambda (CloudWatch 11:30:35Z "MDLP daily re-source ... dead-source pipeline skipped", wrote account-distribution/aum-metrics fresh). OpenAI key broken = opal/external-apis fetch failing (line 629).</ref>
</references>

<scope>
Three quick-wins in lambda_function.py, each removing or correcting actively-misleading output:

**(a) KILL the AI/OpenAI-calls section (§3).** Delete the success/failure grep over the 6 hardcoded Lambdas' logs (produces "Success 0 / Failed 0 / Success Rate 100%" — a 100% computed from ZERO calls reads as all-good, worse than nothing). Remove the section from the email + JSON. (OpenAI is NOT deprecated — 64 Lambdas still use it; this kills the broken TRACKER, not OpenAI usage. Token-accurate AI spend belongs in the cost view, P2/H.)

**(b) REPLACE the SmartX section (§2) false-STALE with real served-artifact freshness.** Remove the hardcoded dead EC2 (i-06ebcb27395eb3f49) + opal-data-smartx-v2/exports/ folder watch (reports "Overall STALE" off a folder nobody writes since 06-01). Replace with the LIVE served-artifact freshness: head-object mtime of the opal-smartx-ingestion-pipeline outputs (account-distribution.json / aum-metrics.json on opal-data-portal-v2) vs the daily cadence -> OK if fresh-today, WATCH/RED if stale. (This is a minimal stand-in until the full Freshness section lands in P1 — but it MUST stop the false alarm now; alarm-fatigue trains readers to ignore "STALE".)

**(c) RE-HOME the AI error-triage (§6) + security briefing (§5) to Claude.** §6 is the single biggest degradation — it was the actionability engine, now dead on the broken opal/external-apis OpenAI-key fetch (line 629). Re-home to Claude (firm default model) -> restores per-error root-cause + severity + new-vs-chronic for the Lambda-error list, + the security briefing (trend / top-N new / suppress chronic-accepted). **Access mechanism = BEDROCK InvokeModel (CTO-ruled 185342Z) — NOT an Anthropic-key-in-secretsmanager.** Rationale: a fetchable secret reintroduces the EXACT fragility that silently broke the original triage (the OpenAI key fetch failing -> triage dead); Bedrock's IAM-auth has no key to fetch/rotate/break, is AWS-native, keeps infra-telemetry IN-AWS (no Anthropic-API egress of error/security/cost data), and its spend shows in Cost Explorer (self-consistent with the MONEY section). Add `bedrock:InvokeModel` to the role via Terraform; REMOVE the broken OpenAI secretsmanager fetch (line 629); and CONFIRM Bedrock Claude model-access is ENABLED in us-east-1 (an enable-model-access step if not). Do NOT re-home onto another breakable secret.

NOT in P0 (later phases): the full Freshness section (P1/B), Drift (P1/E), cost depth (P2/A), graph-HEAD (P3/C), contract-integrity (P3/D), the agent-JSON feed + portal surface (P3 delivery). P0 = stop the bleeding only.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-iam service opal-infrastructure-monitor</run>
      <expect>Current ops include secretsmanager:GetSecretValue (line 629, the broken OpenAI fetch) + ce:GetCostAndUsage + S3 + CloudWatch + EC2 + SES + logs. Enumerate before the re-home: the Claude path adds EITHER bedrock:InvokeModel (Bedrock) OR a different secretsmanager secret ARN (Anthropic API).</expect>
      <if_mismatch>If the re-home mechanism is undecided, STOP the §6 leg and confirm CTO's ruling (Bedrock vs secret) before coding it. Legs (a)+(b) proceed regardless.</if_mismatch>
    </step>
    <step>
      <run>comp-blast opal-infrastructure-monitor (or the report artifact opal-data-portal-v2/infrastructure/reports/)</run>
      <expect>Consumers = the SES email (andrew@opalinvest.com) + the S3 archive. No portal/agent consumer yet (that's P3). Removing §3 + changing §2 breaks no downstream consumer.</expect>
      <if_mismatch>If a downstream consumer parses the report JSON's §3/§2 keys, document + preserve a compatible shape or coordinate before removing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy">
    <step>
      <run>comp-iam gaps  (ONLY if iam.tf changed — i.e. the Claude re-home added bedrock:InvokeModel or a new secret read)</run>
      <expect>No NEW permission gap. If Bedrock chosen: bedrock:InvokeModel present on the role before deploy. If alt-secret: the new secret ARN readable.</expect>
      <if_mismatch>Resolve the gap (add the perm in iam.tf via Terraform) before apply. Deploy is Terraform-only (Rule 1, safe-apply).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Trigger one report (the monitor is invoke-on-demand — a controlled invoke is fine, it is a lightweight report Lambda, NOT a heavy gold run) + inspect the emitted email + the S3-archived JSON</run>
      <expect>§3 AI/OpenAI-calls section ABSENT. §2 SmartX section reports REAL served-artifact freshness (fresh-today = OK, NOT a false "STALE" off the dead EC2 folder). §6 error-triage + §5 security briefing are Claude-generated (root-cause + severity present, no "AI summary unavailable").</expect>
      <if_mismatch>Section still misleading -> fix + re-invoke. The whole point of P0 is the next report stops misleading the reader.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- P0 is self-contained on the report Lambda. It does NOT touch the data pipelines, only how the monitor REPORTS on them.
- The §2 SmartX-freshness stand-in is a minimal version of P1's full Freshness section (B) — P1 generalizes it per-pipeline; P0 just stops the false alarm. No conflict (P1 supersedes the stand-in).
- The Claude re-home mechanism (Phase-1 gate) is the one architecture decision shared with CTO; resolve before the §6 leg.
- Deploy is Terraform-only (Rule 1). EC2 not involved (the report is a Lambda).
</cross_domain_coordination>

<acceptance_criteria>
- The §3 AI/OpenAI-calls section is removed from both the email and the archived JSON.
- The §2 SmartX section reports the LIVE served-artifact freshness (opal-smartx-ingestion-pipeline outputs' mtime vs daily cadence), NOT the dead-EC2-folder false "STALE".
- §6 error-triage + §5 security briefing are Claude-generated (no "AI summary unavailable"; root-cause + severity restored), via the CTO-ruled access mechanism.
- Deployed via Terraform (safe-apply, 0-diff verified); lambda-source-map updated; comp-iam gaps clean if iam.tf changed.
- Phase-3 verify on a real report run (controlled invoke or next scheduled): the three corrections are live in the emitted artifact.
- Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail vs <expect>.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>P0 changes the report GENERATOR's logic only (what it reports + how it triages). No data pipeline / served-artifact re-emit; the report reads live state each run. The change affects only future report runs (next invoke), which is the intended verification point.</no_reprocess_needed></data_reprocess_scope>
