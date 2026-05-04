# Scope Memo — HISTBF Bronze Transactions Stream-Fix

**Author:** 0.4.0_DS_ClientPlatform~D
**Date:** 2026-05-04
**Requested by:** 2.0.0_SA_COO
**For:** CTO + Andrew ship-decision

---

## 1. Root Cause — Confirmed: Pure IAM, Not OOM

**Verdict: IAM failure only. No OOM occurred. The script never reached parquet assembly.**

### Stderr Evidence (Wave B v5 progress file `2f0abf97`, `dim=transactions`)

```
botocore.errorfactory.AccessDenied: An error occurred (AccessDenied) when calling
the GetObject operation:
  User: arn:aws:sts::313476888478:assumed-role/inf-bronze-runner-ec2-role/i-083ad9ae297f88e9f
  is not authorized [to perform s3:GetObject on orion/jwt/current.json]
```

- **Elapsed at failure: 1.5s** — startup time, before any Orion API call
- **Exit code: 1**
- **Mechanism:** `pull_inflection_transactions_rest.py` line 330 calls `_load_jwt(s3)` which does `s3.get_object(Bucket="opal-data-inf", Key="orion/jwt/current.json")`. EC2 instance role `inf-bronze-runner-ec2-role` lacked `s3:GetObject` on the `orion/jwt/*` prefix.

### IAM Fix Status

AE 0.6.1 IAM v1.7.14 (SSM c2722e05): `s3:GetObject` on `orion/jwt/*` for `inf-bronze-runner-ec2-role`. Status as of 2026-05-04: **applied**. Retry is IAM-unblocked.

---

## 2. OOM Risk Assessment (Secondary — Not Yet Observed)

The script was NOT refactored for this Wave. Its memory pattern warrants assessment before the next retry:

### Memory Pattern (`pull_inflection_transactions_rest.py`)

```python
all_rows: list[dict] = []       # accumulates ALL rows in-process
# ...per account loop...
all_rows.extend(rows)           # unbounded growth
# ...end loop...
df = pd.DataFrame(all_rows)    # materializes once; peak memory ~2× list size
buf = BytesIO()
df.to_parquet(buf, index=False) # third copy in BytesIO
```

**Peak memory = ~3× raw data volume.** No streaming, no chunking.

### Data Volume Estimate

| Factor | Value | Source |
|--------|-------|--------|
| Total accounts | ~1,160 | script comment ("~1,160 total calls") |
| Observed max rows/account | 3,454 | DS~B Phase 0 probe note |
| Estimated avg rows/account | 200–500 | 6yr history, not all accounts active full period |
| Low estimate (200 avg) | ~232K rows | safe — ~120 MB peak |
| Mid estimate (500 avg) | ~580K rows | borderline — ~300 MB peak |
| High estimate (1,500 avg) | ~1.74M rows | OOM risk on t3.small (~870 MB peak) |

**t3.small has 2 GB RAM.** Python + OS + boto3/pandas baseline consumes ~400–500 MB. Usable headroom: ~1.5 GB.

**Conclusion:** OOM is POSSIBLE but not confirmed. Actual row count per account is unknown without a successful run. A smoke test with `--limit-clients 20` would bound the estimate before committing to full pull.

---

## 3. Silver/Transactions Gap Status — Observability Only

**silver/transactions/ is complete. No data gap exists.**

| Path | Count | Coverage | Source |
|------|-------|----------|--------|
| `silver/transactions/{date}.parquet` | **1,502 files** | 2020-05-26 → 2026-04-28 (business days) | Prior separate silver-layer pull, 2026-04-29 |
| `bronze/transactions/{date}.parquet` | **0 files** | — | Wave B v5 failed at IAM startup |

The silver transactions data was produced via a direct silver pull (not through bronze EC2 runner path) on 2026-04-29. The gold chain does not read from `bronze/transactions/` — it reads from `silver/transactions/`. All downstream gold scripts have full transactional history.

**The bronze gap is observability-only.** Having bronze allows lineage auditing and re-runs of the silver builder with updated rep attribution logic. It is NOT required for current gold output.

---

## 4. Fix Options (Ranked)

### Option A — Instance Upsize + IAM-Fixed Retry

**Approach:** With IAM v1.7.14 already applied, retry the existing script on a t3.medium (4 GB) instead of t3.small (2 GB). No code changes.

**Steps:**
1. Smoke test: `python3 pull_inflection_transactions_rest.py --limit-clients 20 --dry-run` on t3.small — verifies IAM, measures memory per 20-client slice
2. If memory is safe: run full `--upload` on t3.small
3. If t3.small OOMs: upsize to t3.medium for the run only (no Terraform change needed — SSM launch as different instance type, or stop/resize existing)

**Cost estimate (full run):**
- 1,160 accounts × ~1.5s avg per call (rate-limited, adaptive) = ~29 min
- t3.small: $0.0208/hr × 0.5hr = **~$0.01**
- t3.medium: $0.0416/hr × 0.5hr = **~$0.02**
- Effectively free.

**Risk:** If total rows exceed ~500K and peak memory is >1.5 GB, t3.medium handles it. t3.large (8 GB) is the backstop. Code is simple, retry is low-effort.

**Verdict: LOW EFFORT, LOW RISK. Correct first move.**

---

### Option B — Streaming Refactor (Chunk-per-N-accounts, S3 merge)

**Approach:** Refactor the script to:
1. Process accounts in batches of N (e.g., 100)
2. After each batch, flush `all_rows` → parquet part-file → upload to S3 staging prefix (`bronze/transactions/staging/{pull_date}/part-{N}.parquet`)
3. After all batches complete, read all part-files, concat, deduplicate, write final `bronze/transactions/{pull_date}.parquet`

**Eliminates OOM entirely.** Peak memory per batch ≤ 100 accounts × max_rows.

**Effort:** ~2-3 hours engineering. Pre-commit gate + smoke test required.

**When to use:** Only if Option A OOMs on t3.medium. Given silver already exists and this is P3, streaming refactor before even trying Option A is overengineering.

**Verdict: RESERVE — implement only if Option A fails on t3.medium.**

---

### Option C — Hybrid (Recommended)

**Approach:** Option A first with smoke-test gate. Promote to Option B if and only if t3.medium OOMs.

**Sequence:**
1. AE 0.6.1 confirms IAM v1.7.14 deployed on inf-bronze-runner-ec2-role (already done)
2. DS~D runs `--limit-clients 20 --dry-run` smoke test on existing t3.small
3. Measure peak RSS; extrapolate to full 1,160 client run
4. If projected memory < 1.2 GB: run full on t3.small
5. If 1.2–1.8 GB: upsize to t3.medium for one run
6. If > 1.8 GB or OOM: implement Option B streaming refactor

**Verdict: RECOMMENDED. Minimum viable effort. Ships the bronze fix without premature refactor.**

---

## 5. Does the Parallel ThreadPoolExecutor Pattern Apply?

**Short answer: Partially, with caveats.**

The positions_mv/assets_v2 parallel pattern (ThreadPoolExecutor 32 workers, per-thread S3 clients) gave 16× speedup because: (1) the bottleneck was S3 I/O (network-bound, releases GIL), (2) no rate limiter dependency, (3) each task was independent.

Transactions differ:

| Factor | positions_mv/assets_v2 | transactions |
|--------|------------------------|-------------|
| Bottleneck | S3 GET + pandas transform | Orion API HTTP calls (rate-limited) |
| Rate limiter | None | AdaptiveRateLimiter — shared state across workers |
| GIL behavior | S3 I/O releases GIL | HTTP requests release GIL (similar) |
| OOM risk | No (one date at a time) | YES (all_rows list grows across all accounts) |
| Independence | Per date — fully independent | Per account — rate limiter must coordinate |

**Parallelism would help run-time:** With 4-8 workers and rate-limiter-aware dispatch, ~29 min could drop to ~8-15 min. But:
- The AdaptiveRateLimiter state (RPS tracking, backoff) is not thread-safe without modification
- More concurrent requests = higher 429/backoff risk from Orion API
- If we hit 429s, parallelism backfires

**Recommendation for this TO:** Do NOT add parallelism in the same pass as the IAM fix. Keep scope minimal — fix IAM, test, run. If run time becomes an issue (it's ~30 min on t3.small, negligible), revisit parallelism separately with rate-limiter refactor.

---

## 6. Go/No-Go for Current Sprint

**Recommendation: DEPRIORITIZE. P3 — no-go for current sprint.**

Rationale:
- Silver is complete (1,502 files). Gold chain reads silver, not bronze. **No downstream impact.**
- Bronze gap is observability-only.
- IAM fix is already applied (AE 0.6.1 v1.7.14). The retry is unblocked but non-urgent.
- Option C (smoke test → full run) can be executed in <1hr of engineering time whenever scheduled.
- Competing priorities: HISTBF.004 gold chain integrity verification, Phase 2b PARTIAL dims (billing/activity) pending DS~B research close.

**If CTO or Andrew wants to ship this sprint:** Option C (smoke test + t3.small retry) can be executed immediately by DS~D in <1hr. No Terraform changes required. No code changes required (IAM already fixed). Schedule at next available EC2 slot.

---

## Appendix: Wave B v5 Transactions Error (Verbatim)

```json
{
  "dim": "transactions",
  "chunk_start": "inception",
  "chunk_end": "current",
  "status": "fail",
  "exit_code": 1,
  "elapsed_s": 1.5,
  "error": ", line 1094, in _make_api_call\n    raise error_class(parsed_response, operation_name)\nbotocore.errorfactory.AccessDenied: An error occurred (AccessDenied) when calling the GetObject operation: User: arn:aws:sts::313476888478:assumed-role/inf-bronze-runner-ec2-role/i-083ad9ae297f88e9f is not authoriz"
}
```
