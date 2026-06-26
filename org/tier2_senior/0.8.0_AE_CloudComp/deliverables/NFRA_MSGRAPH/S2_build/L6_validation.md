# NFRA_MSGRAPH.S2 — L6 validation procedure (run post the 02:00 UTC nightly)

**Purpose:** close the deploy-completion ledger's final leg (L6) against the SCHEDULED nightly's SERVED artifacts (CTO step-6 + the 3 L6 close-conditions, 171106Z). Run this after the 02:00 UTC `opal-globgrph-derive-runner-nightly` completes (~tomorrow AM).

## L6 BASELINE (captured 2026-06-26 ~17:12Z, PRE-MS-nightly — comp-kuzu)

| metric | pre-MS value |
|---|---|
| total nodes | **12,644** |
| `layer='aws'` nodes | **12,644** |
| `source='ms'` nodes | **0** |

The strict-superset invariant tomorrow: **`layer='aws'` count stays EXACTLY 12,644** (unchanged — the additive proof) AND **`source='ms'` count > 0** (MS first-class + categorized). Total = 12,644 + ms_count.

## CTO's 3 L6 close-conditions (171106Z)

1. **AWS-superset invariant (load-bearing) — assert BOTH halves:** MS nodes first-class + categorized AND AWS node count UNCHANGED (not just "MS present").
2. **CVO independent live verification** on the nightly's artifacts (verifier-not-fixer; the served artifact is the truth, not my self-report).
3. **Content-verify the nightly's emitted artifacts** (the MERGE leg the read-only smoke did NOT exercise) + confirm the **SS4 cert held on the FULL nightly run**.

## Run (post-nightly)

```bash
# 1. confirm the nightly ran MS-enabled + succeeded (CloudWatch logs of the derive task)
aws logs tail /ecs/globgrph/derive-runner --since 6h --region us-east-1 2>&1 | grep -E "MS_EXTRACT_(START|COMPLETE|DISABLED)|MS_CONTENT_COMMS_LEAK|DERIVE_RUNNER_COMPLETE|ICEBERG_NODES_WRITTEN"
#    EXPECT: "OK: MS_EXTRACT_COMPLETE nodes=... edges=..." + "OK: DERIVE_RUNNER_COMPLETE"
#    A "MS_CONTENT_COMMS_LEAK" line = the catastrophic-floor cert FIRED (would have failed the derive) -> investigate, do NOT close.

# 2. THE SUPERSET INVARIANT (both halves) -- against the SERVED nightly graph
comp-kuzu "MATCH (n) RETURN n.layer AS layer, count(*) AS n ORDER BY n DESC"
#    ASSERT: layer='aws' == 12644 (UNCHANGED) AND layer='ms' > 0 (added). Read the provenance header = current.

comp-kuzu "MATCH (n) WHERE n.source='ms' RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC"
#    ASSERT: MS_SITE / MS_LIBRARY / MS_FOLDER / MS_FILE / MS_DRIVE_ONEDRIVE / MS_USER present + categorized (no UNCATEGORIZED).

comp-kuzu "MATCH ()-[e]->() WHERE e.layer='ms' RETURN e.edge_type AS t, count(*) AS c ORDER BY c DESC"
#    ASSERT: CONTAINS + OWNED_BY present (day-one edges).

# 3. SS4 held on the FULL run: no comms/content node_type leaked into the served graph
comp-kuzu "MATCH (n) WHERE n.layer='ms' AND NOT n.node_type IN ['MS_SITE','MS_LIBRARY','MS_FOLDER','MS_FILE','MS_DRIVE_ONEDRIVE','MS_USER','MS_GROUP'] RETURN count(*) AS leaked_should_be_0"
#    ASSERT: 0 (the closed MS node_type set held; no comms/content class leaked).

# 4. AWS-unchanged spot: a known AWS node still present + AWS count exact
comp-kuzu "MATCH (n) WHERE n.layer='aws' RETURN count(*) AS aws_should_be_12644"
```

## On all-green

1. `python .tools/deploy_ledger.py close-leg --slug nfra-msgraph-s2-ms-ingest --leg-id L6 --proof "<the comp-kuzu output: aws=12644 unchanged + ms nodes first-class/categorized + SS4 held 0-leak + DERIVE_RUNNER_COMPLETE>"`
2. `python .tools/deploy_ledger.py close --slug nfra-msgraph-s2-ms-ingest` (closes the ledger — all 6 legs proven).
3. RAVC COO the SERVED result → COO GOes S3 (held on exactly this). RAVC CTO (deploy + live confirm, all 3 conditions). Loop CVO for the independent live verification (condition 2).
4. S2 is then fully CLOSED; the MS estate is comp-kuzu-queryable; S3 heat-map cut unblocked.

## If the nightly's MS path failed (not-green)

- A gateway error (NeedsLogin / HTTP) → the derive logs `WARN: MS_EXTRACT_FAIL` and the AWS derive is UNAFFECTED (best-effort fold) — the graph is still the clean AWS-only 12,644. Fix the gateway path (check `/ms/health`), re-enable on the next nightly. NOT a rollback.
- A `MS_CONTENT_COMMS_LEAK` (return 1, no commit) → the catastrophic floor fired; the whole derive failed closed (graph stale). Investigate the leak (should be cert-impossible), do NOT close L6, escalate.
- Rollback if needed: set `GLOBGRPH_MS_ENABLED` unset on the task-def (revert to AWS-only, byte-identical) via safe-apply.
