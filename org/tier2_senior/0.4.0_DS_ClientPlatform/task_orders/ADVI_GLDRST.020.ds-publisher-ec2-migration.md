# ADVI_GLDRST.020 — DS: Port Publisher Lambda Logic to EC2 Gold Runner Scripts

<task_order>
  <issuer>1.0.0_SA_CTO</issuer>
  <issued>2026-04-06</issued>
  <agent>0.4.0_DS_ClientPlatform</agent>
  <status>complete</status>
  <!-- COO session 17 correction: 3 commits (a3b2d209, 732ccc22, 422d9b07) deliver 11a/11b. AE rerunning with new scripts. -->
  <priority>high</priority>
  <project>ADVI_GLDRST</project>
  <depends_on>none — can start immediately</depends_on>
</task_order>

## Context

`bd-portal-advisor-publisher` (Lambda) hits the 900s hard timeout writing ~7,200
S3 objects (3,596 clients x dual-write). The dataset keeps growing and Lambda
cannot scale past 900s. Andrew approved moving this work into the EC2 gold runner
as scripts 11a/11b, which have no timeout constraint and already have all data loaded.

The publisher Lambda had a NameError scoping bug fixed in bd-v2.21.3+v2.21.4 (57s
when it works), but the timeout will recur as the client count grows.

## Deliverables

### 11a_publish_portal_aggregates.py

Port the logic from `bd-portal-publisher` Lambda:
- timeseries_chart.json
- implementor_leaderboard.json
- clients_tab.json
- header_metrics.json
- filters.json
- snapshots/

Source: `data/black_diamond/lambdas/bd-portal-publisher/lambda_function.py`

### 11b_publish_advisor_client_detail.py

Port the logic from `bd-portal-advisor-publisher` Lambda:
- implementor_leaderboard (per-advisor)
- advisor book.json files (~32)
- client detail.json files (~3,596)

Source: `data/black_diamond/lambdas/bd-portal-advisor-publisher/lambda_function.py`

### Requirements

1. Scripts must write to NEW structured paths only (`gold/artifacts/`, `gold/entities/`).
   Do NOT carry over dual-write — that is being eliminated.
2. Scripts run after script 10 in the gold sequence. They should load data from
   the same parquet files the publisher Lambdas read (account_performance.parquet,
   client_dimension.parquet, etc.) but can read them locally from the EC2 filesystem
   instead of from S3.
3. Include the CloudFront invalidation that currently happens in the publisher Lambda.
4. Write `pipeline-complete.json` sentinel AFTER 11b finishes (move from run_gold_layer.sh
   if needed, or keep it there and just ensure ordering).
5. Follow existing gold script conventions (lib/ imports, s3_layout.py paths,
   logging to stdout).

## Acceptance

- 11a + 11b produce identical S3 output to the publisher Lambdas (new paths only)
- Scripts complete within the gold runner without timeout
- CloudFront invalidation fires after all writes
- Uploaded to S3 artifact bucket, ready for AE deploy

## After This TO

- AE deploys 11a/11b to EC2
- DE migrates portal reads to new paths (GLDRST.021)
- DS removes dual-write from scripts 01-10 (subset of GLDRST.010 scope)
- Publisher Lambdas can be deprecated (kept dormant as fallback initially)
