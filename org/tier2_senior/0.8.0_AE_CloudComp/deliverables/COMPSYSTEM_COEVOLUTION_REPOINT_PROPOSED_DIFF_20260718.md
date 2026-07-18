# Proposed diff -- comp_system.py: coevolution_pairs = realized snap (primary) + frontend as *_surfaced

**Author:** 0.8.0_AE_CloudComp~A · **For:** 1.0.0_SA_CTO to land under exec authority (comp_system.py is exec-locked, org/modules/graph) · **Date:** 2026-07-18 · **Ruling:** CTO option (b), msg 010046Z · **Status:** PROPOSED (grounded), not applied.

## Grounding (done first, per CTO "don't repoint onto a stale snap")
Three distinct co-evolution surfaces exist; the realized-diversity one CTO wants is the GRAPHFEED snap:
- `fedobs_frontend_coevolution.json` (local committed, DS~B) -- **6 pairs**. The frontend-curated subset. What `_read_fedobs` reads today.
- `fedobs_observations.json` (S3, fedobs_observe) -- the live reflective co-evolution rows (cse_log_total=56,791). comp-fedobs's default; NOT the snap.
- **`fedobs_coevolution_snap`** (Nessie table `globgrph.fedobs_coevolution_snap`) -- the realized standing snap. **No local/served JSON exists**; its one cheap served key is the R1 twin heartbeat `s3://opal-313476888478-globgrph/warehouse/snap_ingest/last_append/fedobs_coevolution_snap.json` = `{"appended": 1729, "at": "2026-07-17T17:43:21Z"}` (verified LIVE this session).

**Read-path decision (the non-obvious part):** the snap has no cheap local read; `_read_fedobs` is a local no-creds `open()`. Three options: (A) read the snap heartbeat via one S3 GetObject; (B) subprocess comp-fedobs (reads the observations surface, a *different* number, not the snap); (C) pyiceberg the snap table (heavy, cred-bound). **Recommend (A):** it is the snap's own summary key, tiny, and degrades to UNKNOWN off-VPC/no-creds -- preserving comp_system's always-runnable + no-fabrication invariants (introduces the compiler's first S3 read, defensively imported like `yaml`).

**One caveat (documented in-code):** `appended` is the last run's append count. The coevolution producer writes the FULL current pair set each nightly run (not a delta), so `appended` == realized pairs for the latest snapshot_date. If it ever switches to true-delta appends, `appended` would understate -> then have snap_store emit an explicit `realized_pairs` in the heartbeat (a tiny follow-up).

## The diff (unified, against current HEAD)

```diff
@@ def _read_fedobs()  (relabel frontend -> *_surfaced; it is now the SECONDARY)
 def _read_fedobs() -> dict:
-    """Grounded read of the served FEDOBS artifact (the DS~B frontend-co-evolution measure) -- the
-    diversity metric source. Returns {} keys UNKNOWN if the artifact is absent (never fabricated)."""
+    """Grounded read of the served FRONTEND FEDOBS artifact (the DS~B frontend-co-evolution measure)
+    -- the SURFACED/curated co-evolution subset. Since 2026-07-18 (CTO ruling option-b) this is the
+    *_surfaced SECONDARY; the PRIMARY realized-diversity headline is _read_snap_realized(). Returns
+    UNKNOWN keys if the artifact is absent (never fabricated)."""
     path = os.path.join(WS, "org", "tier2_senior", "0.4.0_DS_ClientPlatform", "deliverables",
                         "fedobs_frontend_coevolution.json")
     try:
         with open(path, encoding="utf-8") as fh:
             data = json.load(fh)
         measures = data.get("measures", [])
         pairs = sum(1 for m in measures if (m.get("co_sessions") or 0) > 0)
-        return {"cse_log_total": len(measures), "coevolution_pairs": pairs,
-                "vintage": "served artifact %s (%d measures)" % (os.path.basename(path), len(measures))}
+        return {"cse_log_total": len(measures), "coevolution_pairs_surfaced": pairs,
+                "vintage": "served artifact %s (%d measures, frontend-surfaced subset)"
+                           % (os.path.basename(path), len(measures))}
     except Exception:  # noqa: BLE001
-        return {"cse_log_total": UNKNOWN, "coevolution_pairs": UNKNOWN, "vintage": UNKNOWN}
+        return {"cse_log_total": UNKNOWN, "coevolution_pairs_surfaced": UNKNOWN, "vintage": UNKNOWN}
+
+
+def _read_snap_realized() -> dict:
+    """Grounded read of the REALIZED co-evolution diversity -- the GRAPHFEED standing snap
+    (fedobs_coevolution_snap), the audit's #1 maturity lever (CTO ruling option-b, 2026-07-18).
+    Source = the snap's own served summary key: the R1 twin heartbeat snap_store.py OVERWRITES after
+    every nightly append, s3://{SNAPSHOT_BUCKET}/warehouse/snap_ingest/last_append/
+    fedobs_coevolution_snap.json -> {"appended": N}. The nightly producer writes the FULL current
+    pair set each run (not a delta), so 'appended' == the realized pair count of the latest
+    snapshot_date. boto3/S3 imported+called DEFENSIVELY: no creds / off-VPC / absent -> UNKNOWN, never
+    fabricated (comp-system stays runnable everywhere; the number is honest-or-absent). If the
+    producer ever moves to true-delta appends, track an explicit realized_pairs in the heartbeat."""
+    bucket = os.environ.get("SNAPSHOT_BUCKET", "opal-313476888478-globgrph")
+    key = "warehouse/snap_ingest/last_append/fedobs_coevolution_snap.json"
+    try:
+        import boto3  # noqa: PLC0415  -- defensive/optional; module import must never require it
+        body = boto3.client("s3", region_name="us-east-1").get_object(Bucket=bucket, Key=key)["Body"].read()
+        hb = json.loads(body)
+        realized = hb.get("appended", UNKNOWN)
+        return {"realized_pairs": realized,
+                "vintage": "snap heartbeat s3://%s/%s (appended=%s @ %s)"
+                           % (bucket, key, realized, hb.get("at", "?"))}
+    except Exception:  # noqa: BLE001
+        return {"realized_pairs": UNKNOWN, "vintage": UNKNOWN}

@@ def compute_metrics()  (primary = snap; add *_surfaced)
     recs = _read_promote_manifest()
     fed = _read_fedobs()
+    snap = _read_snap_realized()
@@
-        "coevolution_pairs": _metric(
-            fed.get("coevolution_pairs", UNKNOWN), "fedobs_frontend_coevolution.json (served)",
-            fed.get("vintage", UNKNOWN)),
+        "coevolution_pairs": _metric(
+            snap.get("realized_pairs", UNKNOWN),
+            "fedobs_coevolution_snap heartbeat (realized, GRAPHFEED nightly)",
+            snap.get("vintage", UNKNOWN)),
+        "coevolution_pairs_surfaced": _metric(
+            fed.get("coevolution_pairs_surfaced", UNKNOWN),
+            "fedobs_frontend_coevolution.json (surfaced subset)",
+            fed.get("vintage", UNKNOWN)),
         "cse_measures": _metric(
             fed.get("cse_log_total", UNKNOWN), "comp-fedobs cse_log_total (served)",
             fed.get("vintage", UNKNOWN)),

@@ def compile_model()  (diversity: primary snap + *_surfaced + label-the-basis note)
 def compile_model() -> dict:
     fed = _read_fedobs()
+    snap = _read_snap_realized()
@@
-    diversity = {"metric": "observe-surface DIVERSITY (co-evolution pairs; CTO Q4: diversity not raw volume)",
-                 "coevolution_pairs": fed.get("coevolution_pairs", UNKNOWN),
-                 "cse_measures": fed.get("cse_log_total", UNKNOWN),
-                 "note": "the loop/federated maturity headline; thin-seed until PROMOTE + frontend producers diversify it",
-                 "vintage": fed.get("vintage", UNKNOWN)}
+    diversity = {"metric": "observe-surface DIVERSITY (co-evolution pairs; CTO Q4: diversity not raw volume)",
+                 "coevolution_pairs": snap.get("realized_pairs", UNKNOWN),
+                 "coevolution_pairs_surfaced": fed.get("coevolution_pairs_surfaced", UNKNOWN),
+                 "cse_measures": fed.get("cse_log_total", UNKNOWN),
+                 "note": "PRIMARY = realized diversity from the GRAPHFEED standing snap (nightly); "
+                         "*_surfaced = the frontend-curated subset -- label-the-basis, CTO ruling option-b",
+                 "vintage": snap.get("vintage", UNKNOWN)}

@@ def render_markdown()  (show both, labeled)
-           "- coevolution_pairs: %s | cse_measures: %s | vintage: %s" % (d["coevolution_pairs"], d["cse_measures"], d["vintage"]),
+           "- coevolution_pairs (realized): %s | coevolution_pairs_surfaced (frontend): %s | cse_measures: %s | vintage: %s"
+           % (d["coevolution_pairs"], d.get("coevolution_pairs_surfaced", "UNKNOWN"), d["cse_measures"], d["vintage"]),
```

## Unchanged / verified-safe
- `self_test` check-5 asserts `"coevolution_pairs" in diversity_metric` -- still true (primary key kept). 9/9 stays green.
- No `cs:` managed-region marker references coevolution (only tools_index/ledger_union) -- no sibling-doc marker churn.
- `_render_metrics` iterates the metrics dict -> the new `coevolution_pairs_surfaced` row renders automatically.
- Fail modes: no boto3 / no creds / off-VPC / absent key -> `coevolution_pairs` reports UNKNOWN (honest), never fabricated; `--check` unaffected (fingerprint watches `.tools/comp-*` + graph yaml + DS deliverables, not S3).

## After landing
Drop the compiler-pointer residual rows in 07_maturity + 04_federated (I hold them until you land, per your instruction), and regenerate 06 -- `coevolution_pairs` will then read ~1,729 realized with `coevolution_pairs_surfaced=6`.
