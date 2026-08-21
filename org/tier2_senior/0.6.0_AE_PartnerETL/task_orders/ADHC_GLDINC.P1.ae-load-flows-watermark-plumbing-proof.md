<task_order>
<metadata>
  <to_id>ADHC_GLDINC.P1</to_id>
  <project>ADHC_GLDINC (gold incrementalization build — Andrew-approved; 0.6.0 LEAD)</project>
  <title>AE: load_flows watermark plumbing-proof — windowed/watermarked read of load_flows_from_transactions (C_01/C_02/C_03) as a SHADOW with §4b parity scorecard; zero-correctness, oracle serves</title>
  <assigned_to>0.6.0_AE_PartnerETL</assigned_to>
  <issued_by>self (GLDINC LEAD) — COO GO to stage 2026-06-08T1316Z; CTO "proceed with GLDINC P1" 2026-06-08T1316Z. Awaits COO/CTO endorsement of this brief before BUILD (mirrors P0 design→endorse→build).</issued_by>
  <issued_date>2026-06-08</issued_date>
  <status>superseded -- flipped 2026-08-21 by the ISSUER (0.6.0_AE_PartnerETL as GLDINC LEAD, per the COO-or-issuer rule): the DELIVERY MECHANISM this TO orders (shadow harness after the oracle + standing gold/_parity comparator + daily scorecard + 5-clean-nights counter) is the exact class Andrew COMPLETE-VETOED 2026-08-04 ("We do not do all these extra paths... The comparator is also a HORRIBLE idea... Delete all of that and mark it all as deprecated" -- CLAUDE.md NEVER no-shadow-channels x2, memory/feedback_no_shadow_channels_veto_build_correctly_and_port.md), which postdates this 06-08 TO by 8 weeks; latest + most-restrictive binds. THE NEED SURVIVES THE MECHANISM: the ~4x nightly full-scan of silver/transactions (lib/nna_flows.py:87) is still a real I/O cut, and the four byte-identity traps + CTO cache-boundary principle in this TO's scope remain the correct design substrate. The sanctioned re-form is Andrew's verbatim method: build the windowed path correctly (tests + ad-hoc run-and-read QA comparison, nothing standing), then DIRECT PORT on the production schedule with same-window rollback -- a NEW TO in that form needs COO/CTO endorsement per this TO's own design->endorse->build lifecycle (build endorsement was never granted, so no build work is stranded). Routed to COO cc CTO 2026-08-21.</status>
  <priority>NEXT after P0+W2a (both validated-live + RAVC-closed 6/8). First shadow/parity phase → activates the GLDINC daily_watch scorecard obligation (COO /drive attests through 2026-07-05). LOW risk (zero-correctness by construction).</priority>
</metadata>

<scope>
## Design of record
`docs/briefs/gldinc-p1-load-flows-watermark-plumbing-proof-design-20260608.md` (this session). PRD anchors: §5 hidden full-scan, §5a unifying restatement primitive, §4b parity machine + daily-watch, §6 P1 row.

## Anchor (verified)
`lib/nna_flows.py:87 load_flows_from_transactions(max_workers=128)` full-scans the ENTIRE `silver/transactions/` prefix every call (no date arg, :100-105). Consumers, each a fresh full-scan: `C_01.canonical_nna.py` (:783,:861 ×2), `C_02.client_performance.py` (:269), `C_03.account_performance.py` (:156) → ~4 full-scans/nightly. Pure I/O cut shared across 3 scripts.

## The correctness subtlety (designed for — see brief §3; CTO correction 2026-06-08 folded in)
`load_flows_from_transactions` is NOT a pure per-partition map: an AUA-dependent garbage filter (`_load_latest_silver_aua()`, :248+) re-evaluates EVERY historical event against TODAY's silver AUA each night, plus a current-state (account,date) txn-date exclusion list and a cross-partition composite dedup (:145-149). RESOLUTION: cache at the AUA-invariant, PER-EVENT, **PRE-DEDUP + PRE-DROPNA (truly-raw)** boundary — `gold/_state/load_flows/preflt_events.parquet` holding minimal raw per-event columns (account_id, trade_date raw, transaction_id, transaction_type/action, action, market_value, description + source_order_key) snapshotted right after the sorted parallel-read concat (:122-124), for date ≤ watermark. FOUR byte-identity traps, all resolved + DS-co-verified 2026-06-08: (1) **per-event grain** [CTO] — garbage filter is per-event (:250→:259→:280) BEFORE the :285 groupby; (2) **dedup-over-union** — composite dedup :145-149 is trade_date-keyed but watermark is file-date, so a cross-boundary twin survives per-block dedup; (3) **order-stability** — :128/:148 keep='last' is row-order-dependent, union must re-sort by source_order_key to the oracle's sorted(keys) concat order; (4) **raw pre-:128/pre-dropna** [DS] — oracle dedups (:128) BEFORE dropna (:132), so a null-field row can win the dedup then be dropped, suppressing its twin; a post-dropna cache loses that winner → divergence. CTO principle for the cache family: cache boundary UPSTREAM of every cross-event/current-state op. Each night: window-read date>watermark partitions → extract raw per-event cols → UNION with cache → re-sort → run the WHOLE transform from :128 over the union (transaction_id dedup → coercion+dropna → composite dedup → static exclusions → classification → txn-date exclusions → per-event AUA garbage filter vs CURRENT AUA → groupby-to-daily) → byte-identical by construction; dominant txn-read I/O cut for date ≤ watermark.

## Build ownership split (Option A — DS co-dev, accepted 2026-06-08 134123Z)
CTO-GO'd 133416Z (deploy-class confirm). DS (0.4.0, reconcile-correctness + Rule-13 gold-.py deploy owner) owns `lib/nna_flows.py`: `_transform_events_to_daily()` extraction + `load_flows_from_transactions_windowed()` + watermark/cache + restatement fallback; commits + S3-deploys the gold .py. AE (0.6.0, GLDINC infra lead) owns `gold_dispatch.sh` shadow-after-oracle wiring + `gold/_state` + `gold/_parity` S3 plumbing + IAM + deploy sequencing (next nightly ~23:00Z); co-authors shadow-diff + §4b scorecard emitter (.py-vs-.sh emitter ownership settled at pairing — if .py it rides DS's deploy, if .sh it's AE's). DS-3-trap reconcile sign-off + trap-4 recorded above.

## Build (CTO-GO'd; pairing in progress)
1. `lib/nna_flows.py`: add `load_flows_from_transactions_windowed(watermark)` ALONGSIDE the unchanged oracle entry point (oracle untouched, stays the served path). Caches minimal RAW per-event rows to `gold/_state/load_flows/preflt_events.parquet` (PER-EVENT grain per CTO correction); watermark at `gold/_state/load_flows/watermark.json` (max_partition_date + per-partition LastModified fingerprint, current-version metadata only). Whole transform (dedup→exclusions→classification→garbage→groupby) runs over the per-event union each night.
2. Restatement DETECT-and-fall-back (P1 scope): if any partition for date ≤ watermark shows advanced LastModified (§5a primitive) → full-scan fallback + cache rebuild that run; scorecard records the fallback. (Incremental restatement-REPAIR deferred to §5/§5a's own phase.)
3. Shadow harness: runs AFTER the oracle on the EXISTING nightly runner (§4b P1 — no new EC2). Writes incremental output to `gold/_parity/load_flows/{run_date}/incremental.parquet` (NEVER a served key), diffs vs oracle.
4. Scorecard emitter: `gold/_parity/load_flows/{run_date}/scorecard.json` per §4b (key_set_symmetric_diff, row_count_delta, exact_match_rate, within_epsilon_rate + max_abs/rel_diff frozen-epsilon, headline_metric_diffs [total inflow/outflow/implied-NNA/account_count], clean_night_counter, restatement_fallback flag). THIS is the daily_watch deliverable COO attests.
5. Deploy to `code/gold/` ahead of a nightly; validate the FIRST scorecard on the next SCHEDULED nightly. ZERO ad-hoc bd-gold runs.

## P2 fold-in (COO ruling 2026-06-08)
The deferred empirical P0 resume==fresh byte-identical check rides the P2 parity-machine at zero marginal cost → carried as an explicit AC into the P2 staging TO (not this one). Capture opportunistically on a natural mid-chain death if one precedes P2.

<acceptance_criteria>
- [ ] AC1 — `load_flows_from_transactions_windowed()` + watermark/cache lifecycle implemented; oracle entry point UNCHANGED (byte-diff of the oracle function = 0). py_compile + ds-commit-gate + ruff pass. `from __future__ import annotations` present (lib module; PEP-604 already in use at :53).
- [ ] AC2 — Shadow harness wired AFTER the oracle on the nightly runner; writes ONLY to `gold/_parity/` + `gold/_state/` (never a served key — verify no served-key write).
- [ ] AC3 — Scorecard.json emitted per §4b schema on the first post-deploy SCHEDULED nightly; structurally valid + readable by COO /drive.
- [ ] AC4 — FIRST nightly scorecard: key_set_symmetric_diff=0, row_count_delta=0, exact_match_rate=100.000%, headline_metric_diffs=0/within-epsilon (OR a clean restatement_fallback night). Any non-fallback diff≠0 = STOP + BLOCKED-ASK with the gap.
- [ ] AC5 — clean_night_counter ≥ 5 consecutive (cutover-readiness; cutover itself separately Andrew-gated, NOT in this TO).
- [ ] AC6 — RAVC2 staging→COO+CTO now; RAVC2 first-scorecard + 5-night readiness when reached.
</acceptance_criteria>

<compiler_tools_mandate>
- Before write: `comp-pipescript io C_01.canonical_nna.py` (+ C_02/C_03) — confirm load_flows feed + no COLUMN GAPS introduced; `comp-blast load_flows_from_transactions` — confirm the 3 consumers are the full blast radius (no surprise 4th caller).
- Before commit: `.tools/ds-commit-gate.sh lib/nna_flows.py` (py_compile + ds-precommit-check + ruff) — Python edit on a gold lib.
- Before run: `comp-pipescript deployed` MATCH on the dispatch + lib before the nightly relies on it; `comp-pipescript postdeps` (load_flows has no served-key post-step — shadow only).
- After: confirm scorecard freshness on the SERVED `_parity` artifact (not a proxy).
</compiler_tools_mandate>
<cross_domain_coordination>`silver/transactions/` (read-only, shared upstream — AE Schwab ingest + DS silver own writes; P1 reads only). C_01/C_02/C_03 are DS-authored gold scripts — the lib change is shared; coordinate with 0.4.0_DS before the consumer cutover (NOT in this staging TO — cutover is a later Andrew-gated step). `gold/_state/` + `gold/_parity/` are NEW non-served prefixes (no IAM change expected — opal-data-bd/* already granted; verify with comp-iam if a new bucket/prefix policy is needed). NFRA R3a right-size (r6i.4xlarge) unaffected — shadow rides the same box, windowed read is cheaper than the oracle it follows.</cross_domain_coordination>
</scope>
</task_order>
