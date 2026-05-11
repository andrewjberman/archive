<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.INF_C02_C03_TLS_HARDEN</id>
    <project>ADVI_INFNNA</project>
    <title>INF_C_02 + INF_C_03 TLS hardening — cap ThreadPoolExecutor at 32 workers + boto3 Config(max_pool_connections=128, retries=adaptive) — prevent TLS UNEXPECTED_EOF on 2019-stale-era key reads</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>~15 min (~5min per script + cascade re-validate)</estimated_effort>
    <actual_effort>~15min (edit + gate + standalone re-run both + commit + S3 deploy + SHA verify)</actual_effort>
    <authorized_by>1.0.0_SA_CTO ratified 2026-05-11 — Option B (script-side reduce-parallelism) post-empirical-evidence cascade `b9967954` 2/2 retries exhausted on TLS-layer drops</authorized_by>
    <closed_date>2026-05-11</closed_date>
    <closed_by>0.4.0_DS_ClientPlatform~A</closed_by>
    <closed_via>RAVC2 to COO 2026-05-11 ~17:50Z. Commit `4e82e8c45`. INF_C_02 + INF_C_03 both PASS standalone re-run rc=0; no TLS/Connection errors. S3 deploy MATCH on both (ceff93acc1b58333 + 8ab7c76c9c6b19a2). 32-worker cap + boto3 Config(max_pool_connections=128, retries=adaptive) live in both scripts. INF_C_03 second ThreadPool (line 184, was 64) also capped 32 for uniformity.</closed_via>
  </metadata>

  <references>
    <ref type="empirical_incident">Cascade `b9967954` 2026-05-11 — INF_C_02 + INF_C_03 both failed rc=1 with `ConnectionClosedError` + `SSLError UNEXPECTED_EOF` on `canonical_performance_2019-XX-XX.parquet` keys. 4/4 retry budget exhausted. Same error class on 2nd retry attempt confirms client-side cause, not AWS rate-limit.</ref>
    <ref type="diagnosis">DS~A diagnosis: `ThreadPoolExecutor(max_workers=min(len(dates), 256))` vastly oversubscribes boto3's default 10-connection HTTPS pool → keep-alive churn → TLS handshake retries → SSLError UNEXPECTED_EOF. Empirically confirmed by error-class shift attempt 1→2.</ref>
    <ref type="affected_scripts">data/orion/scripts/gold/INF_C_02.client_performance.py + INF_C_03.account_performance.py</ref>
    <ref type="cto_ruling">1.0.0_SA_CTO 2026-05-11 ~17:30Z — Option B ratified (not A retry-config; not C SSM PROD path; not D wait-and-retry)</ref>
  </references>

  <context>
    Cascade `b9967954` validated SILVER-UNIFY end-to-end with 35/37 OK. C_02 + C_03 failed transient TLS drops — NOT code regression (same scripts succeeded Friday + this AM). Root cause empirically isolated to client-side connection-pool oversubscription on Windows-local execution.

    Option B fix per CTO ruling: surgical script-side reduce-parallelism + boto3 Config tuning. Single-line per script change. Same root-cause coverage as Option A retry-config but smaller blast radius.

    **Why not other options:**
    - A (retry-config only): both fix root cause; B's smaller change wins
    - C (SSM to PROD runner): AE+IAM friction + scope creep; B is DS-lane
    - D (wait + plain retry): pure-retry pattern; 4 attempts already burned with same error class shift — client-side cause, won't self-resolve

    Cascade pragmatic close already accepted: this TO ships TODAY as hardening, NOT gate-blocker. Next PROD chain run will hit the same Windows-local oversubscription pattern if invoked locally; this fix prevents recurrence.

    Cascade `b9967954` is also the first instance demonstrating that Windows-local subprocess execution exhibits this failure mode — the equivalent EC2 ProcessPool (via SSM) path has different threading semantics and may not be affected. Hardening covers both empirically.
  </context>

  <scope>
    <step>
      **Open INF_C_02.client_performance.py + INF_C_03.account_performance.py.** Identify the boto3 S3 client init + the `ThreadPoolExecutor(max_workers=...)` invocation. Likely 2 distinct sites per script (S3 client + thread pool).
    </step>

    <step>
      **Apply boto3 Config** to S3 client init in BOTH scripts:
      ```python
      from botocore.config import Config
      _S3_CONFIG = Config(
          retries={'max_attempts': 10, 'mode': 'adaptive'},
          max_pool_connections=128,
      )
      s3 = boto3.client('s3', config=_S3_CONFIG)
      ```
      Place the `_S3_CONFIG` definition module-level for clarity; reuse in all client instances if multiple.
    </step>

    <step>
      **Cap ThreadPoolExecutor workers** in BOTH scripts:
      ```python
      # was: max_workers=min(len(dates), 256)
      # now:
      max_workers=min(len(dates), 32)
      ```
      32 workers × 128 pool-connections = 4x safety margin (vs prior 256 × 10 = 25x oversubscription).

      Document in inline comment: `# CAP at 32 (TLS pool exhaustion at 256+; see ADVI_INFNNA.INF_C02_C03_TLS_HARDEN 2026-05-11)`
    </step>

    <step>
      **Pre-commit gate** per CLAUDE.md rule 14:
      `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_C_02.client_performance.py data/orion/scripts/gold/INF_C_03.account_performance.py`
      All three checks (py_compile + ds-precommit-check + ruff) must exit 0.
    </step>

    <step>
      **Local standalone re-run validation:**
      - `python data/orion/scripts/gold/INF_C_02.client_performance.py` → expect rc=0
      - `python data/orion/scripts/gold/INF_C_03.account_performance.py` → expect rc=0
      
      Each should complete in ~3min on Windows-local with capped workers. Capture wall-clock + verify all date partitions read successfully (no ConnectionClosed / SSLError in stderr).
    </step>

    <step>
      **Commit + push + S3 deploy + SHA verify** (manual hashlib since INF not in comp-pipescript deployed coverage yet):
      - `aws s3 cp` both scripts → `s3://opal-data-inf/code/gold/`
      - SHA256 local vs S3 MATCH per DS~B's pattern this morning
      - Author: `0.4.0_DS_ClientPlatform~A`
    </step>

    <step>
      **RAVC2 to COO** with:
      - Empirical retry: both scripts rc=0 with capped workers
      - Wall-clock comparison (pre-cap fail vs post-cap success)
      - SHA MATCH evidence on S3 deploy
      - Note: subsequent local cascades + PROD chain triggers will exercise the hardened code path
    </step>
  </scope>

  <acceptance_criteria>
    1. **boto3 Config applied** in both scripts with `max_pool_connections=128` + adaptive retries.
    2. **max_workers cap at 32** in both scripts with inline-comment audit trail.
    3. **Pre-commit gate PASS** all 3 checks on both files.
    4. **Local standalone re-run** both scripts rc=0 in ~3min each.
    5. **No TLS/Connection errors** in stderr during re-run.
    6. **S3 deploy MATCH** SHA256 verified.
    7. **RAVC2 delivered** with empirical evidence.
  </acceptance_criteria>

  <blocking>
    None. DS~A bandwidth-gated only. Cascade close already accepted via pragmatic gate-acceptance; this TO is post-close hardening, not blocker.
  </blocking>

  <notes>
    **Why 32 not 64 or 16:** 32 workers × 128 pool-connections = 4x safety margin. boto3 docs recommend matching pool-connections to worker count or higher; 4x is comfortable headroom for in-flight requests + keep-alive churn. 64 workers would be 2x margin (still acceptable); 16 workers leaves obvious throughput on the table.

    **Why not bump to 64 with boto3 Config alone:** retry-config addresses recovery, but capping parallelism addresses root cause. Capping at 32 + Config gives belt-and-suspenders.

    **Future-proofing for EC2 SSM path:** EC2 runners have different network stack + more network bandwidth. The 32-worker cap is conservative for local Windows; EC2 could likely sustain 64+ workers. But uniform 32 across both execution paths simplifies reasoning + matches local-laptop reality. If EC2 throughput becomes a bottleneck, separate TO can introduce env-var-controlled worker cap.

    **DSFLOW backlog candidate:** "ThreadPool sizing convention" — flag any script with max_workers > 32 for review. CTO surfaced this as deferred-backlog item; this TO is the empirical anchor.

    **Stale-era observation cross-reference:** the failing keys (`canonical_performance_2019-09-18.parquet`, etc.) are DS~B's STALE-PURGE zone. After STALE-PURGE re-author + DATE_CLIP TOs ship, these stale-era keys won't be iterated at all → TLS-pool exhaustion surface naturally shrinks. This TO is the immediate defense; DATE_CLIP is the long-term fix.
  </notes>
</task_order>
