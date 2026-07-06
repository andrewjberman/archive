# NFRA_CMTQUE — Phase-0 Grounding + TO-3/TO-1 Scaffold Plan

**Author:** 0.7.0_AE_CloudOps~B (single executor, Andrew pre-instantiated)
**Date:** 2026-07-06
**PRD:** docs/architecture/NFRA_CMTQUE_PRD.md (1.0.0_SA_CTO, Andrew-direct, @12b920bea)
**Substrate:** LOCKED local-daemon + local-queue (Andrew-ratified via COO 154640Z); cloud = observability ONLY; NO cloud-SQS branch in any TO.

---

## 1. Phase-0 grounding (source-read, not self-report)

Four sources read end-to-end / characterized:

### 1.1 `.tools/safe-commit.sh` (the interface + gates I must preserve byte-for-byte)

**Interface contract (G3 — 1300+ fabric callers; a signature change is a fabric-wide break):**
- Args: `[--force] [--author "name <email>"] [-m "msg"] [git-commit-opts...] -- <path1> [path2...]`
- `--help`/`-h` OR zero args -> help, exit 0.
- Missing `--` OR empty pathspec -> `ERROR: pathspec required`, exit 2.
- Not in a git repo -> exit 2.
- `--force` -> FORCE=1 (stripped from forwarded args).
- Tokens before `--` that aren't `--force`/`--help` -> COMMIT_ARGS (forwarded verbatim to `git commit --only`).
- Tokens after `--` -> PATHSPEC (forwarded to `git add -f` + `git commit --only`).

**Exit codes callers depend on (must be reproduced by the enqueue client):**
| Code | Meaning |
|---|---|
| 0 | commit landed |
| 1 | contamination-abort OR sensitive-leak block |
| 2 | usage error / not a repo |
| 3 | mutex timeout ("commit storm" cliff) |
| (passthrough) | `git commit` own exit — pre-commit hook fail, nothing-to-commit, etc. (`exit $?` at :371) |

**Body sequence (what the worker reproduces in its uncontended critical section):**
1. `REPO_ROOT=git rev-parse --show-toplevel`; `AUDIT_LOG=<repo>/org/git-author-override-audit.log` (env `SAFE_COMMIT_AUDIT_LOG` overridable).
2. **mkdir-mutex** on `$(git rev-parse --absolute-git-dir)/commit-queue.lock`, `LOCK_TIMEOUT_SEC=60`, dead-PID + age-based stale reclaim, `exit 3` on timeout. *(This is the thing we replace with the queue; worker holds NO cross-agent lock — it is the sole writer.)*
3. Extract `AGENT` from `--author` for audit attribution.
4. **BASELINE** = `git diff --cached --name-only` (pre-staged peers). *(Retired under single-writer — D5.)*
5. `git add -f -- <pathspec>` (force overrides .gitignore — the reason the sensitive gate exists).
6. **IN_SCOPE** = `git diff --cached --name-only -- <pathspec>` (git's own pathspec expansion; dir-pathspec safe).
7. **SENSITIVE-LEAK GATE** (fail-closed): `_LEAK_ALWAYS_RE` (`.har/.pem/.p12/.pfx/.jks/.keystore/.ppk`, id_rsa/dsa/ecdsa/ed25519, .netrc/.pgpass) always block; `_LEAK_IF_IGNORED_RE` (`.env/.key/.crt/.cer`, cookie/secret/credential/password/apikey/private_key/access_token/auth_token, `.aws/.ssh/.gnupg/sources/`) block only if ALSO `git check-ignore`'d; `_LEAK_EXCLUDE_RE` (`.env.template/.example/.sample/.dist`) exempt. On hit: `git reset HEAD -- <hits>`, `SENSITIVE-BLOCK` audit line, exit 1. Override: `SAFE_COMMIT_ALLOW_SENSITIVE="reason"` (audited). **MOVES TO WORKER (§4).**
8. **Contamination check**: EXTRA = staged \ IN_SCOPE \ BASELINE; EXTRA>0 && !FORCE -> exit 1; FORCE -> `FORCE-BYPASS` audit + proceed. **RETIRED under single-writer (D5)** — worker's index is uncontended so EXTRA is always empty.
9. Advisory `comp-surface-check` (never blocks) + advisory `comp-coverage-check` (never blocks).
10. `git commit --only "${COMMIT_ARGS[@]}" -- "${PATHSPEC[@]}"`; `exit $?`.

**Load-bearing detail for the queue:** pathspec + `git commit` run **relative to the caller's CWD**. The request MUST capture `cwd` so the worker resolves paths identically. Relevant env (`SAFE_COMMIT_ALLOW_SENSITIVE`, `SAFE_COMMIT_AUDIT_LOG`, `GIT_*` author overrides) must ride in the request.

### 1.2 `org/mcp/inbox-watch.sh` (the local-daemon + atomic-mv idiom for TO-3)

- **Atomic-mv exactly-once claim:** `mv "$src" "$dest" 2>/dev/null || continue` — concurrent losers skip silently. This is the FIFO-drain primitive.
- **Daemon loop:** `while true; do for f in dir/*; do …; done; sleep 5; done`.
- **Lexical FIFO:** files named `20260706T153610Z_...` — ISO-8601 UTC timestamp prefix sorts lexically = chronologically. Glob iteration `for f in dir/*` is lexically ordered -> natural FIFO.
- **Sentinel/ack:** append delivered name to `.unread-deliveries`.
- **Rule-16 clean:** no pgrep/pkill/flock in the stream path; pure `mv`/`for`/`sleep`.

### 1.3 `infra/aws/terraform/globgrph/item2b.tf` (the SQS/Lambda semantics I localize — D2/D4/D7)

- SQS standard + DLQ (`maxReceiveCount=3`, 24h DLQ retention); ESM `batch_size=100`, `MaximumBatchingWindow=120s` debounce, `ReportBatchItemFailures`, **`maximum_concurrency=2`**.
- **The named catastrophe:** uncapped concurrency during the 06-09/10 burst put N executions in a Nessie commit race -> every loser a 409 -> SQS retry -> **298k-DLQ flood**. Capped to 2 (SQS-ESM minimum); in-code retry absorbs residual 2-writer conflicts.
- **My inversions:** (a) **concurrency=1 HARD** (git index is a stricter single-writer than Nessie — 2 is not safe here); (b) **NO debounce/batching** (D4 — each agent's commit is distinct author/msg/hash; worker drains a burst back-to-back, one commit per request); (c) DLQ + loud-fail preserved (D7/G5).

### 1.4 `infra/aws/lambda/globgrph/incremental_updater/lambda_function.py` (the retry idiom — D2/G5)

- Bounded exponential backoff: `COMMIT_MAX_ATTEMPTS=5`, `BASE=1s`, `CAP=15s`, `delay=min(CAP, BASE*2^(attempt-1))`.
- Retry ONLY transient (`CommitFailedException` 409 / `CommitStateUnknownException` 5xx-ambiguous); **fail LOUD on exhaustion** (`ICEBERG_COMMIT_CAS_EXHAUSTED` + publish + raise). The whole prior P0 was a *silent* freeze -> doctrine is loud-never-silent.
- **Critical git adaptation:** a **git gate rejection is DETERMINISTIC** (contamination/sensitive/owned-paths/ds-gate fail identically on retry) -> it must NOT be retried. Only genuinely-transient faults (a pre-commit hook flake, a transient FS/index lock, `index.lock` contention) are retryable. Gate rejects go straight to `result=rejected+reason` (+ DLQ), immediately + loud.

### 1.5 Caller surface (G3 interface freeze)

`grep -rl safe-commit.sh` = ~1347 files (PRD cited 1338; delta = churn). Dominant real invocation shapes (the AC2 compat matrix): `--author "<serial> <email>" -m "msg" -- <paths>`; `--force --author … -- <path>`; `--help`/no-args; parens/brackets in `-m`; directory pathspec; new-file-under-gitignored-prefix. Most of the 1300+ are agents (interactive), not scripts — so the freeze is a behavioral contract, verified by the compat matrix, not just a call-site edit.

---

## 2. Locked architecture (single local substrate)

```
agent (unchanged CLI) --> safe-commit.sh [THIN ENQUEUE CLIENT, TO-2]
    | writes REQUEST {req_id, author, commit_args, pathspec, cwd, env, force, enqueue_ts}
    | to  <gitdir>/commit-queue/requests/<ts>_<reqid>.json   (atomic-mv from tmp)
    | then BLOCKS polling  <gitdir>/commit-queue/results/<reqid>.json
    v
LOCAL DURABLE QUEUE [TO-3]   requests/ + results/ + dlq/ + worker.pid + worker.hb
    v
COMMIT-WORKER DAEMON [TO-1]  single process, concurrency=1, sole git-index writer
    | claim oldest request (atomic-mv to processing/), then in its critical section:
    |   git add -f -- <pathspec> ; sensitive-leak gate ; git commit --only <args> -- <pathspec>
    | transient fault -> bounded retry (5x, 1..15s) ; hard/gate fail -> dlq/ + result=rejected
    | write results/<reqid>.json {status, hash|reason, exit_code, stdout, stderr}  (atomic-mv)
    | emit CloudWatch metrics (liveness hb, queue depth, latency, dlq depth)
    v
client reads result -> reproduces exit code + stdout/stderr -> caller sees identical behavior
```

**D6 graceful degradation:** if `worker.hb` is stale / `worker.pid` dead, the client FALLS BACK to the current in-line mkdir-mutex path (today's exact behavior) and the liveness alarm fires. A dead worker degrades to today, never blocks.

---

## 3. TO-3 scaffold — local durable queue substrate

**Location:** `$(git rev-parse --absolute-git-dir)/commit-queue/` (per-worktree, like the existing lock; gitignored by virtue of living under .git).

**Dirs:** `requests/` `processing/` `results/` `dlq/` + files `worker.pid` `worker.hb` (heartbeat ts).

**Request file** `requests/<enqueue_ts>_<reqid>.json` (ISO-ts prefix = lexical FIFO; reqid = pid+counter+nonce):
```json
{"req_id","enqueue_ts","cwd","author","commit_args":[...],"pathspec":[...],
 "force":0,"env":{"SAFE_COMMIT_ALLOW_SENSITIVE":null,"SAFE_COMMIT_AUDIT_LOG":null}}
```
Written to `requests/.tmp.<reqid>` then `mv` into place (atomic; the worker never sees a half-written request).

**Result file** `results/<reqid>.json`:
```json
{"req_id","status":"committed|rejected|error","commit_hash":null,"reason":null,
 "exit_code":0,"stdout":"","stderr":"","worker_ts":""}
```

**Correlation + crash-durability:** client polls `results/<reqid>.json`; worker claims a request by `mv requests/X -> processing/X` (atomic — exactly-once even if two workers ever raced, though concurrency=1 forbids it); result is written ONLY after the git commit returns (so a worker crash mid-commit leaves the request in `processing/` for a startup-sweep to re-queue or DLQ, never a lost/duplicate commit). Ack = result-file presence.

**Substrate is a library** (`commit_queue_lib.sh` — enqueue/claim/result/dlq/paths helpers) so client + worker share one implementation; Rule-16 clean (mv/for/sleep/stat only).

---

## 4. TO-1 scaffold — commit-worker daemon (concurrency=1)

**Singleton:** on start, if `worker.pid` names a live PID -> exit (one worker per gitdir). Write own pid; `trap` cleanup on EXIT.

**Loop (concurrency=1 HARD — one request fully done before the next is claimed):**
```
while true:
  refresh worker.hb (liveness heartbeat + CloudWatch metric)
  req = oldest requests/*.json   (lexical FIFO)
  if none: sleep(short); continue
  mv req -> processing/          (atomic claim)
  cd req.cwd
  # === serial critical section (the ONLY git-index access in the fabric) ===
  git add -f -- <pathspec>
  sensitive-leak gate (moved from client, §1.1 step 7) -> hit => result=rejected(reason=sensitive) + dlq + continue
  git commit --only <commit_args> -- <pathspec>   (pre-commit/owned-paths hook fires here, attributed to req.author — R4)
  classify:
     rc==0            -> result=committed, hash=git rev-parse HEAD, exit_code=0
     transient fault  -> bounded retry (5x, delay=min(15, 2^(n-1)))
     hard/gate fail   -> result=rejected(reason, exit_code, stderr) + dlq/  (NO retry — deterministic)
  write results/<reqid>.json (atomic-mv)
  rm processing/<req>
```

**Gate placement (§4 of PRD, preserved):** sensitive-leak -> worker (needs staged set); owned-paths -> worker (rides the real `git commit` pre-commit hook); ds-commit-gate -> stays **agent-side fail-fast** (don't enqueue a non-compiling `.py`) + worker re-assert; author identity -> `req.author` applied verbatim; `--force` + FORCE-BYPASS/SENSITIVE audit -> worker writes them, attributed to `req.author` (**R4** — hook + audit must credit the REQUESTER, not the worker process; explicit check in TO-1/TO-5).

**Retire (D5):** the BASELINE-capture + contamination apparatus is NOT ported — the worker's index is uncontended, so `git diff --cached` can only ever show the worker's own in-scope stage. `git commit --only` remains scoped to the pathspec regardless.

**Fairness (R3, design-for not v1-block):** note per-agent round-robin so one agent's burst can't starve the FIFO; v1 is strict FIFO.

**Metrics (TO-4 wires the alarms):** worker emits liveness hb, per-commit latency (enqueue_ts->result), queue depth, dlq depth to CloudWatch.

---

## 5. Non-negotiables carried (from GO + PRD)

- concurrency=1 HARD (git index single-writer; the 298k-DLQ 2-writer race is the named catastrophe — do NOT repeat).
- safe-commit.sh interface byte-for-byte (exit codes + arg parse + stdout) — AC2 compat matrix gates it.
- ALL gates preserved: sensitive-leak (fail-closed), owned-paths, ds-gate, author-identity, atomic per-agent commit, --force + audit.
- Graceful degradation (D6): worker-down -> in-line mutex fallback + delivering liveness alarm.
- LOCAL daemon + LOCAL queue only; cloud = observability. No cloud-SQS branch.
- Loud-never-silent (G5): every request -> hash OR dlq+reason; nothing silently dropped; exhaustion fails loud.

---

## 6. Build order + risk isolation

1. **TO-3** (queue lib) — new files only; touches NOTHING live.
2. **TO-1** (worker) — new files only; a running worker with no client enqueuing is inert.
3. **TO-2** (client) — the ONLY change to `safe-commit.sh`; gated behind a worker-liveness check + feature flag so default = today's mutex path until TO-6.
4. **TO-4** (observability) — Terraform (Rule 1), comp-iam for grants.
5. **TO-5** (retire contamination guard + gate-wire) — worker-path proof (sensitive gate fail-closes in the worker).
6. **TO-6** (cutover) — CTO arch-gate: feature-flag, canary, full-burst load test vs mutex baseline, rollback. SEV care.

**Nothing touches the live commit path until TO-2's flag is flipped (TO-6, CTO-gated).** TO-3 + TO-1 are pure additive scaffold — zero fabric risk to build now.

**CTO arch-gates:** (a) worker gate-integration (TO-1/TO-5), (b) the TO-6 cutover. Both flagged for 1.0.0_SA_CTO review before landing on the live path.

---

## 7. TO-4 — Observability + alarms (design; Terraform apply HELD for box recovery)

**Status:** design authored 2026-07-06. TO-1's worker already emits metrics to a local sink (`cw_metric` -> `<queue>/metrics.log`); TO-4 replaces that sink body with `aws cloudwatch put-metric-data` and provisions the alarms via Terraform (Rule 1). The apply is HELD only for box health (terraform would time out on the currently-degraded host) — the design is complete.

### 7.1 Metrics (namespace `Opal/CommitQueue`, dimension `Repo=<gitdir basename>`)
| Metric | Emit point | Meaning |
|---|---|---|
| `WorkerLiveness` (=1 each loop) | daemon loop top | worker is alive + draining; ABSENCE = stall |
| `QueueDepth` | each idle poll | pending requests not yet claimed (backlog) |
| `CommitLatencyMs` | on each result | enqueue_ts -> result (the metric G1 targets: no storm/timeout) |
| `Committed` (count) | on committed result | throughput |
| `RejectedCount` (count) | on client-visible rejection | user-error rate (NOT poison) |
| `DlqDepth` (count) | on any DLQ move | POISON: transient-exhausted / corrupt / crash-orphan |
| `RecoveredCommitted` (count) | crash-sweep landed-recovery | how often the PRE_HEAD recovery saved a landed commit |

### 7.2 Alarms (Terraform)
1. **WorkerDown (CRITICAL)** — `WorkerLiveness` **missing for >= 3 min** with `treat_missing_data = breaching`. Worker down = commits not landing (the fabric falls back to today's mutex via D6, so it degrades not halts, but the loud signal is mandatory). This is the alarm that must DELIVER.
2. **DlqDepth > 0** — any poison request. Fires on `DlqDepth >= 1`. (The DLQ-split — TO-5 — is WHY this stays a real poison signal: user-errors never enter the DLQ, so depth>0 is always actionable.)
3. **QueueBacklog** — `QueueDepth > N` sustained M min (slow-drain / stuck worker not yet dead).
4. **CommitLatencyHigh** — `CommitLatencyMs` p-high over the mutex baseline (degradation; tune against the TO-6 load-test baseline).

### 7.3 Delivering-subscriber (the PendingConfirmation lesson — AC4)
The alarm SNS topic MUST have a **CONFIRMED** subscriber, not a silently-expiring email PendingConfirmation. Wire the alarm to the fabric's existing **ops-alert channel** (a confirmed endpoint), and VERIFY delivery by an exercise (fire a test alarm -> observe it arrive), not by reading the TF config. "Assert a real subscriber" — a config-read that shows a subscription is INSUFFICIENT (Rule 22a: BEHAVIOR claims need exercise). AC4 = "alarm DELIVERS", exercised.

### 7.4 IAM nuance (flag for CTO / comp-iam)
The commit-worker is a **LOCAL daemon** on the repo host, not a Lambda — so its `put-metric-data` runs under **whatever IAM identity the local `aws` CLI assumes on that host**, NOT a Terraform-modeled Lambda/EC2 role. Consequence: `comp-iam service <lambda>` does NOT cover this grant (it models TF Lambda/EC2 policies). TO-4 must: (a) identify the local host's aws identity, (b) attach a least-privilege `cloudwatch:PutMetricData` (scoped to the `Opal/CommitQueue` namespace via a condition if supported), (c) the alarm->SNS publish is CloudWatch-service-principal on the SNS topic policy (Terraform-modeled, comp-iam-visible). Ground the local-identity grant on **live** `aws sts get-caller-identity` + `get-role-policy`/`get-user-policy` (Rule 22a APPLIED layer), not the comp-iam DESIRED view.

### 7.5 Degradation tie-in (D6)
WorkerDown (7.2 #1) is the loud signal that pairs with `cq_worker_alive()` returning false -> `safe-commit` (TO-2) falling back to the in-line mutex. So a worker death is: (a) invisible to callers (they degrade to today's behavior), (b) LOUD to ops (the delivering alarm). Never a silent fabric stall.

