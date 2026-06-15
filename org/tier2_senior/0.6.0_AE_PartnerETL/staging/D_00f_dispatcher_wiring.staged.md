# STAGED (NOT ACTIVATED) — D_00f.advisor_nna_canonical dispatcher wiring

**Status:** STAGED — HOLD on activation pending CVO gate-c 38MB size clearance (DS handoff 200445Z).
**Author:** 0.6.0_AE_PartnerETL (bd-TRIO infra lane) · **Date:** 2026-06-15
**Apply target:** `data/black_diamond/scripts/gold/gold_dispatch.sh` (CLOUD_OPS_OR_ETL = AE lane)
**Two-leg ship:** DS .py leg DONE (`D_00f.advisor_nna_canonical.py`, commit 89d4ac6a7, deployed md5==ETag `4eab732756a8d4b9d60ba490d1a2298f` — AE-verified independently). This is leg 2 (dispatcher wiring).

## Ground-truth verified before authoring
- C4 deploy: repo md5 == S3 ETag == DS-claimed `4eab7327…` — PASS, no drift.
- C6 deps (D_00f reads): `gold/canonical/nna/{date}.parquet` (C_01 atomic output, dynamic-key paginated read — D_00f.py:85,141-160) + `gold/dimensions/accounts_dimension_latest.parquet` (A_00 output, D_00f.py:88). BOTH produced before any PHASE_D → no reorder needed. comp-pipescript io D_00f: Group D / Order 300; statically detected only the accounts_dim read + 0 writes (the nna read + the platinum/firm write are dynamic-key, invisible to static analysis — confirmed from source, NOT a real gap).
- Write target: `platinum/firm/advisor_nna_canonical.json` (D_00f.py:49,80), opal-data-bd, firm-separated. FE already consumes this key (advisor-intelligence.ts:383) — currently empty; D_00f will populate (the 38MB the size-gate is about).
- No CATALOG-name collision: `D_00f` absent from current CATALOG (D_00, D_00b, D_00c, D_01..D_04 only).

## The diff (5 load-bearing edits + help-text hygiene)

### 1. CATALOG — insert after D_00c (full-rebuild publisher, --upload, NO --incremental per DS)
```
 D_00c|D_00c.portal_leaderboard.py|--upload
+D_00f|D_00f.advisor_nna_canonical.py|--upload
 D_01|D_01.partner_analytics.py|--upload
```

### 2. CHAIN_DOWNSTREAM (line ~142) — for --chain downstream / --from modes
```
-CHAIN_DOWNSTREAM="C_03 C_05 C_07 C_06 C_08 D_00 D_00b D_00c D_01 D_02 D_03 D_04"
+CHAIN_DOWNSTREAM="C_03 C_05 C_07 C_06 C_08 D_00 D_00b D_00c D_00f D_01 D_02 D_03 D_04"
```

### 3. GROUP_D (line ~153) — for --group D mode
```
-GROUP_D="D_00 D_00b D_00c D_01 D_02 D_03 D_04"
+GROUP_D="D_00 D_00b D_00c D_00f D_01 D_02 D_03 D_04"
```

### 4. run_chain_parallel() — NEW PHASE_D5 (D_00f alone), inserted AFTER PHASE_D4, before the COMPLETE banner
This is the load-bearing one for the NIGHTLY: chain:full executes the hardcoded PHASE blocks, NOT the
CHAIN_DOWNSTREAM list. Omitting this = D_00f silently never runs in the nightly. Own phase = ZERO change
to existing phase concurrency (maximally non-breaking, bar-c); deps long-satisfied by PHASE_D5.
```
     echo "--- PHASE_D4: D_04 ---"
     run_background D_04
     wait_phase PHASE_D4
 
+    echo "--- PHASE_D5: D_00f ---"
+    run_background D_00f
+    wait_phase PHASE_D5
+
     echo "================================================================"
     echo "  PARALLEL CHAIN COMPLETE"
```

### 5. Help-text / dependency-display hygiene (cosmetic, non-load-bearing)
- line ~47 `#   downstream    = ... D_04` → append ` D_00f` (keep list parity with CHAIN_DOWNSTREAM)
- lines ~731,~737 (dependency-display downstream lists) → add D_00f
- lines ~782-784 (D-publisher descriptions) → add `D_00f  advisor_nna_canonical (advisor_nna_canonical.json)`

## PRE-ACTIVATION CHECKLIST (run when CVO clears the size gate — BEFORE commit+deploy)
1. [ ] CVO gate-c: 38MB artifact accept-as-is OR size-reduced (DS-flagged; CVO+FE decide). DS pings on clear.
2. [ ] IAM write-check (my lane): confirm the bd-gold-layer-runner role has PutObject on
       `opal-data-bd/platinum/firm/*` — D_00f --upload writes there; DS dry-run exercised READ only, not the
       --upload PUT. `comp-iam service` / inspect runner role before first --upload. (Likely covered — sibling
       D-publishers write platinum-class keys — but VERIFY, don't assume.)
3. [ ] Apply the 5 edits to gold_dispatch.sh; `bash -n` clean; comp-pipescript io D_00f still resolves.
4. [ ] Commit (AE author) + deploy gold_dispatch.sh to s3://opal-data-bd/code/gold/ (my lane); verify md5==ETag.
5. [ ] Open a fresh deploy_ledger.py ledger for the activation (publisher first-publish = a served-state change;
       the 38MB artifact MOVES a currently-empty served key → this IS a never-widen-relevant served movement,
       needs the size-gate sign-off as its gate, unlike A_02/P1's DELTA=0).
6. [ ] First-publish via the next scheduled nightly (preferred) OR DS one-time --upload; verify served artifact
       LastModified+content (not rc=0) per C4 discipline.

## OPEN DESIGN NOTE (for DS/CVO)
PHASE_D5 runs D_00f SERIALLY at chain end (safest). If its peak RSS is light, it can fold into PHASE_D2
(`D_00b || D_01 || D_00f`) to save wall-time — needs D_00f's peak-memory profile from a real --upload run
first (the B-phase memory-contention lesson: don't co-locate blind). Deferred as a post-activation optimization.
