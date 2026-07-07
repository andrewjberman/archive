# ADVI_INFPERF M1 -- status + filed follow-ons (2026-07-07)

**Owner:** 0.6.1_AE_PartnerETL. **Status:** BUILT + parity-validated + full-312 scale-gate PASS + CTO cutover-APPROVED (00:28Z). Cutover pending DS-commit (POD4 lane, COO routing) + the scheduled-nightly applied-truth verify.

## Cutover sequence (CTO-confirmed)
1. DS (ClientPlatform/POD4) commits the validated patch `deliverables/ADVI_INFPERF_M1_incremental_perfpull.patch` (my commit was owned-paths-blocked; COO routing the committer). Change is STAGED on the working tree.
2. I deploy to `code/manual_api/` (S3) -- the nightly's `INF_API_PULL_PERF|pull_inflection_performance_rest.py|--upload` picks up `--mode incremental` by DEFAULT (no dispatch change).
3. VERIFY on 1 clean SCHEDULED nightly (CTO condition 5 -- applied truth, not the dry-run): `bronze/performance/{date}.jsonl.gz` fresh + chain step INF_API_PULL_PERF < 600s on the REAL run. RAVC CTO the first clean nightly.
4. THEN DS~A `orion_normalize_as_of` holiday-aware staleness-fix -> perf genuinely fresh -> revert `PERF_SILVER_STALENESS_CEILING_DAYS 10 -> 2`.

## Validated result (full-312 dry-run, 2026-07-07 00:25Z)
incremental=308 (98.7%) / escalated_to_full=4 / empty=2 / fail=0 ; elapsed 536.5s < 600s ; parity PASS (exit 0) ; 310/310 anchored@1.0.

## FILED FOLLOW-ONS

### F1 -- concurrency hardening (CTO RECOMMENDED, near-term, POST-cutover)
The 536.5s pass is only ~10% under the 600s budget, and the bottleneck is per-Orion-call
LATENCY (~1.5s/call x 308), NOT call-count. M1 removes the 8x call-count (2400->308) but
NOT latency-sensitivity -- so a SECOND Orion slowdown (the exact cause of the 06-30 freeze)
could push ~1.5s x 308 past 600s and RE-FREEZE even with M1. FIX: a MODEST bounded thread
pool over the per-client trailing-window fetches -> ~462s -> well under 300s = durable margin.
CONSTRAINT (CTO): bound the pool + respect Orion rate-limits -- do NOT trade a latency problem
for a 429 rate-limit problem. Sequence: AFTER the cutover verifies clean, not before.

### F2 -- 207 non-positive factor rows (CTO "file it")
The full-312 emitted 207 non-positive-factor rows (0.046%). GROUNDED as PRE-EXISTING full-path
data: the 308 incremental clients cannot contribute them (the per-client non-positive integrity
guard escalates any such client to full), so the 207 are confined to the escalated/full-path
clients -- the ORIGINAL full pull emits the same. Investigate WHY Orion returns $0/neg
`factor` for certain account-days (likely $0-balance / pre-funding / closed account-days).
NOT M1-blocking; honestly surfaced by the existing integrity WARN. Low priority.

### F3 -- ExcelReports 1-call/day source (CTO deferred follow-on)
The cheaper source (1 ExcelReports call/day for all 890 accts vs ~308 REST calls) needs a
CLONE of the "Performance Dim" saved query with a SHORT non-annualized DateRange (the runtime
DateRange override on the existing query does NOT honor -- returns fixed Rolling-3-Year
Annualized, probed 2026-07-06). Continuity engine is source-agnostic -> hot-swap behind it IF
a clone honors the short non-annualized window. Deferred per CTO "ship M1, file the cheaper path."

## Banked lessons (memory)
- `feedback_incremental_settled_anchor` -- an incremental index must be SETTLED-anchored;
  never splice onto a provisional/revisable vendor tail (the 4.61e-3 parity FAIL root).
- `feedback_dispatch_lock_orphan_inference_trap` -- don't clear a not-TTL-expired dispatch lock
  off inference (the DI-1 double-dispatch).
