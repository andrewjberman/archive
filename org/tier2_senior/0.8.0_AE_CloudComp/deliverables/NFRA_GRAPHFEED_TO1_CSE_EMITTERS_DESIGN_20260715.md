# NFRA_GRAPHFEED.W1 TO-1 — Standing CSE emitters: RAVC'd design (for the CTO schedule-shape ruling)

**Author:** 0.8.0_AE_CloudComp~Z · **Date:** 2026-07-15 ~19:0xZ · **Authority:** LD-0299 Andrew-direct GO (MSTR wave TO 184610Z; CTO accepted the design gate 184428Z)
**Evidence base:** NFRA_GRAPH_ESTATE_ASSESSMENT_20260715.md (LD-0298 @ 263124baf) + source grounding cited inline.

## 0. BEFORE state (banked this session, served instrument)

- `comp-fedobs` header: `SERVED vintage as-of 2026-07-15T04:30:38Z  marker_head=cdcdc289bbc9  cse_log_total=342`.
- The 342 seed already contains a bounded graph_head slice (`run_id=graphhead-dfc00300271c`) → **event_id dedup against existing rows is mandatory for the backfill** (a naive `--full` re-append would duplicate that slice).
- `comp-kuzu` provenance header: `cse: ABSENT FROM MARKER -- vintage unverifiable` (LD-0298 sec-5).

## 1. Root causes, source-grounded

| Gap | Mechanism | Citation |
|---|---|---|
| CSE log frozen at 342 | Emitters exist but nothing standing runs them; `cse_producer.tf` is a **forward reference that was never built** | `cse_store.py:35` names it; `comp-glob "*.tf" infra/aws/terraform/globgrph` = 22 files, no `cse_producer.tf` |
| `cse` absent from marker | `_stamp_unconditional` REPLACES `table_metadata` wholesale; `incremental_updater` stamps a **3-table tuple hourly**, erasing the `cse` row the 4-table writers put | `_provenance.py:242-268` (docstring cites the 2026-07-10 measurement: derive stamped 4 @02:09:13Z, incremental erased `cse` @05:00:19Z); `lambda_function.py:575-579` (3-tuple); `derive_runner.py:413-417` (already 4-tuple, incl. `cse`) |
| No idempotency layer | `cse_store.append_cses` is append-only with **no event_id dedup** (`cse_store.py:357-404`) | re-run of any emitter today would append duplicates |

## 2. Design (additive-only; zero mutation of graph_nodes/graph_edges write paths; no existing emitter modified)

### (b) The standing scheduled emit — ONE new orchestrator + ONE new TF file

**`infra/aws/globgrph/cse_producers_nightly.py`** (new, baked into the derive image), run as a separate one-shot Fargate task (fedobs_producer.tf treatment — NOT folded into the derive; the derive is untouched, which is strictly stronger than the best-effort bar):

1. **Dedup spine:** scan `globgrph.cse` `selected_fields=["event_id"]` → in-memory set; print `count_before` (the retrieval denominator).
2. **graph_head producer:** reuse `cse_emit_graphhead.build_graph_head_cses()` (imported, unmodified) at FULL scope → filter to event_ids **not** in the existing set → `cse_store.append_cses` (one Nessie commit). Stable ids (`graph_head:node:{nid}` / `graph_head:edge:{src}->{et}->{dst}`) mean: **first run = the ~55k backfill; every later run = only the graph delta; re-run = 0 rows.** Leg (a) and the AC-3 idempotency proof are the same code path.
3. **Staged-batch sweep:** list `s3://opal-313476888478-globgrph/warehouse/cse_ingest/pending/*.jsonl` → per batch: reconstruct + `validate_batch` fail-closed → dedup-filter → append → move to `.../done/`; an invalid batch moves to `.../rejected/` LOUD (never silently retried forever). This is the standing ingest lane for the four LOCAL-source producers (deploy / frontend_coevolution / promote / agent local emits), which read repo/git state a Fargate task cannot see. Prefix sits INSIDE `warehouse/` → covered by the existing bucket-wide RW grant, zero IAM delta.
4. **agent producer in-VPC** (OPTION B, your ruling): reuse `cse_emit_agent.agent_cse()` over recent `s3://opal-mcp-audit/audit/dt=*/*.jsonl` keys (metadata-only, SAFE_TOOLS allowlist, redaction-safe by construction) → dedup → append. **This is the one producer whose source already lives in the cloud, and the only one that guarantees daily novelty** — without it, a quiet estate day (zero new graph nodes, zero staged batches) makes `cse_log_total` legitimately flat and the strictly-increasing AC fails on an honest day.
5. **Marker stamp:** `cse_store.stamp_marker` (4-table tuple) — best-effort, never unwinds a landed append.
- Per-producer try/except isolation: one producer failing never blocks the others; summary line per producer (`appended= / skipped_existing= / rejected=`); rc=1 only if the dedup snapshot itself fails or every producer fails.

**`infra/aws/terraform/globgrph/cse_producer.tf`** (new — the file `cse_store.py:35` forward-references): log group `/ecs/globgrph-cse-producer` + task-def on the derive image with command override `["python","/app/cse_producers_nightly.py"]` + events role (`ecs:RunTask` + `iam:PassRole`) + EventBridge cron. Pure "to add" — no existing resource modified (Option B adds one read-only statement; see §4).

**Dockerfile** (+3 COPY lines, 0.7.0-coordinated rebuild): `cse_emit_graphhead.py`, `cse_emit_agent.py`, `cse_producers_nightly.py`. COPY-only, functionally inert to the derive entrypoint (same class as the fedobs/comp_learns adds).

### (a) The backfill

The **first fire** of the same code path (manual `ecs run-task` post-apply, 0.7.0's run-task lane per the 07-14 handshake precedent), immediately followed by a second fire for the AC-3 count-before/count-after=0 proof. No separate backfill script — one code path, idempotent by construction.

### (c) The cse marker stamp

- `incremental_updater/lambda_function.py:577`: tuple `("graph_nodes","graph_edges","graph_contracts")` → `+ "cse"`. One line. The role already holds bucket-wide RW (iam.tf:159-182) → `load_table(globgrph.cse)` is covered (verify with simulate anyway, §4).
- Zip rebuild delta stated exactly: the one-line fix + `_provenance.py` 07-08→HEAD (adds the DORMANT CAS/merge path, `GLOBGRPH_MARKER_CAS` unset → `_stamp_unconditional` = today's behavior byte-for-byte + one INFO line). Vendoring stays the Dockerfile's "BOTH from one source" condition (image already rebuilt 07-14 from the same `_provenance.py`).
- Deploy: rebuild zip → upload `s3://opal-313476888478-lambda-artifacts/globgrph/incremental_updater.zip` → `safe-apply` (TF `source_code_hash` tracks the repo zip, item2b.tf:149). Rule-2 order: commit → plan → apply → 0-diff → tag.
- `derive_runner` stamp path: **already 4-table in repo AND deployed** (measured 02:09:13Z 2026-07-10 stamped 4 tables) — verified, not changed.

## 3. THE RULING REQUESTED (schedule shape + two options)

**Proposed schedule: `cron(30 3 * * ? *)` — 03:30Z.**
Rationale: 02:00Z derive (measured ~9 min duration; ample margin) → **03:30Z CSE emit** → 04:00Z comp_learns → 04:30Z fedobs. The emit lands after the derive (vintages track the graph, per the TO's sequencing constraint) and **before the 04:30 fedobs federation, so the nightly signal reads TODAY'S events same-night** — the loop is fed the morning after every emit, and the AC-1 oracle (comp-fedobs header) advances daily. The task does not touch Trino (catalog + Nessie + S3 direct), so the 04:00/04:30 Trino-load serialization is unaffected.

**Option A (zero IAM delta):** producers = graph_head delta + staged-batch sweep only; task runs as `derive_runner_task` (the established cse-truth-writer identity — `cse_store.py` design: "runs AS THE DERIVE role"). Honest limitation: strictly-increasing AC-1 is NOT guaranteed on a quiet day.

**Option B (recommended): Option A + the in-VPC agent producer.** IAM shape — your call between:
- **B1:** one additive read-only statement (`s3:GetObject` + `s3:ListBucket` on `opal-mcp-audit`/`audit/*`) on `derive_runner_task` (modifies an existing role's policy; smallest diff), or
- **B2:** a NEW dedicated `opal-globgrph-cse-producer-task` role (warehouse RW mirror + audit read; purely additive, least-privilege, fedobs-style purpose-built role; keeps audit-lake read OFF the broad derive identity).

My recommendation: **B2 + 03:30Z**. Purely-additive posture, least privilege, and the strictly-increasing AC rides a real daily stream instead of luck.

## 4. Verification plan (Rule 22a layers)

- **IAM (applied):** `aws iam simulate-principal-policy` — events role `ecs:RunTask` on the new task-def ARN; task role `s3:GetObject` on one exact audit key (Option B); **ONE `--resource-arns` per call; positive control as a SEPARATE invocation.** `comp-iam service` run but treated as necessary-not-sufficient.
- **Behavior (exercised):** first fire → served `comp-fedobs` header `cse_log_total` > 342; second fire same-day → appended=0 from the graph_head leg (idempotency), >0 from agent leg (novelty); two consecutive SCHEDULED runs → strictly increasing.
- **AC-4 (snapshots untouched):** graph_nodes/graph_edges `snapshot_id` read from the marker before/after each emitter run — must be identical.
- **Marker (c):** after the next hourly incremental fire post-apply, marker JSON carries the `cse` row (the erase stops); `comp-kuzu` header ABSENT-FROM-MARKER line gone.

## 5. Coordination + gates

- **0.7.0 (standing rebuild owner):** derive-image rebuild with the 3 new COPY sources — staged heads-up sent; execution on your GO.
- **One-applier:** globgrph TF apply routed per the standing rule (0.7.0 lane on CTO GO, per the 07-14 Gate-B precedent); targeted apply of this file's resources only — the `item2c` SNS email subscription pre-existing drift row must NOT land as a side effect (same exclusion as the fedobs apply-day checklist, fedobs_producer.tf:31-44).
- **NEVER#5:** deploy-completion ledger opened at deploy-start, closed at completion.
- This design folds the staged FEDOBS(a) recurring-emit thread (07-14, held at the base-lane gate) — same standing-producer need, one mechanism, not duplicated.
