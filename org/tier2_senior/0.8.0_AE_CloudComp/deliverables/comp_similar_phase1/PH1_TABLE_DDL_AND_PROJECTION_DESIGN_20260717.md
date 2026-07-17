# NFRA_COMPSIMILAR PH1 — resource_summaries table DDL + Kuzu-projection design (routes to CTO plan-gate)

**Author:** 0.8.0_AE_CloudComp~D · **Date:** 2026-07-17 · **Vintage:** CLOUD HEAD `8a0e1f5c5`
**Depends:** base's `summary_corpus.py` (adopted, self-test PASS 4/4) · **Gates:** TF apply held for CTO plan-gate; Kuzu projection held on NFRA_KUZUSPLIT P1.
**Companion:** `PHASE1_STATUS.md` (base's corpus engine record). This doc = the HELD remainder base handed off (table + projection), now specced.

---

## 0. Mandate phase-1 grounding — DONE (Rule 22, before-write gate)

| Check | Method (exercised) | Result |
|---|---|---|
| Engine adopted + works | `summary_corpus.py --self-test` | **PASS 4/4** (corpus-collapse LOW / functional-twin HIGH / blind-row UNKNOWN / name-exclusion) |
| `resource_summaries` absent (net-new) | `aws s3 ls .../warehouse/globgrph/` | **ABSENT** — existing: graph_nodes/edges/contracts, cse(+test), fedobs_*, code_heat, ms_heat |
| `graph_nodes` has no summary field | `comp-kuzu "MATCH (n:CloudNode) RETURN n.*"` | **CONFIRMED absent** — schema = node_id/arn/node_type/name/layer/drift_class/source/snapshot_ts/props |

IAM simulate (`glue:CreateTable`/`s3:PutObject` on the exact new ARN, one `--resource-arns`/call + isolated positive
control, Rule 22a) is **deferred one step** — it depends on the write-path ruling (§3). It runs against whichever
catalog CTO confirms, then attaches to the TF plan.

## 1. Table DDL (settled — modeled on the `cse_store.py` sibling-table precedent)

Same Nessie REST catalog + `globgrph` namespace as graph_nodes/edges/cse (reuse, not a new store —
`cse_store.py:5,84-86`). **Append-only, ARN-keyed, latest-version-wins on read; NEVER overwrite/delete/repartition**
(`cse_store.py:322-324` — an authored overlay is immutable-by-append like the C0 log).

```
globgrph.resource_summaries  (pyiceberg Schema; field ids stable)
  1  arn              String  required   # the resource key (identity)
  2  node_type        String  required   # partition + LEFT-JOIN/query dimension
  3  summary          String  required   # the functional summary text (derive-at-scan v1; authored overlay PH3)
  4  authored_by      String  required   # "derive-at-scan@<graph-HEAD>" (PH1) | serial (PH3 authored)
  5  authored_at      String  required   # ISO8601 UTC
  6  source_inputs    String  optional   # JSON provenance: the node_type+layer+edge-neighborhood the summary was derived from
  7  summary_version  Long    required   # monotonic per-ARN; read resolves MAX(version) per arn (append-only versioning)
  8  marker_head      String  optional   # graph HEAD the derive read (vintage pin — cse AC6 marker_head precedent)
  9  ingested_at      Long    optional   # writer append epoch ms
Partition: identity by (node_type, authored_date)  # mirrors cse (source, event_date); small table (~1894 rows)
```
- **AC-2 semantics (append-only proven):** a 2nd summary for an ARN = `table.append()` of a new row with
  `summary_version+1` — the prior row stays; readers take `MAX(summary_version)` per arn. No overwrite path exists.
- **Taxonomy:** OPAL_TAXONOMY-conformant from birth; **NO freshness-twin** (per base ruling 2b + the fabric-wide
  suspend-new-alert-systems directive 2026-07-17 — this table ships with zero SES/SNS/CloudWatch leg).
- **One marker-HEAD:** the append re-stamps `warehouse/_branch_head.main.json` to carry `resource_summaries`
  ALONGSIDE the graph tables (cse_store.py:87-90 precedent) — so a reader sees ONE version-consistent HEAD over
  graph + summaries. **This is what lets the Kuzu projection ride ONE refresh model (§4).**

## 2. Adopted engine → table wiring (derive-at-scan is the v1 populate source)

`summary_corpus.py` returns an in-memory `{arn -> SummaryDoc}` (table-/projection-independent). The write-back:
for each ARN's derived SummaryDoc → one `resource_summaries` row (`summary`=doc text, `authored_by`=
`derive-at-scan@<HEAD>`, `source_inputs`=the graph facts JSON, `summary_version`=next-per-arn, `marker_head`=the
graph HEAD read). PH1 AC-2 exercises this on 3 real ARNs; the full 1894-ARN populate is a batched append. The
engine is unchanged — the store-writer consumes its output.

## 3. THE ONE OPEN ARCH FORK for CTO's plan-gate — the WRITE PATH

Nessie REST is **in-VPC-only** (unreachable from the dev box — `kuzu_nessie_load.py:11-17`, brief §11). Two ways to
create+write `resource_summaries`, and they diverge on the "ONE refresh model" condition:

- **Option A (RECOMMEND — the cse precedent):** create + append via an **in-VPC actor** (a small ECS producer,
  `cse_producer.tf` template, or extend an existing in-VPC producer). Keeps ONE Nessie catalog + ONE marker-HEAD +
  ONE refresh model — the projection reads it from the same HEAD as the graph. **Cost:** a new ECS task + TF + IAM
  (this is the TF-apply-gated diff). Pure-add, NEW-TERRITORY.
- **Option B (the TO's IAM hint):** a **Glue-catalog** Iceberg table, dev-box-writable via GlueCatalog + `s3:PutObject`.
  Simpler write, no ECS. **But** a Glue table is NOT in the Nessie marker-HEAD → the Kuzu projection needs a SECOND
  read path → **violates the ONE-refresh-model standing condition.** Not recommended for that reason.

**The TO's compiler-mandate names `glue:CreateTable` (Option B) while base's spec + PRD 4.2 say "globgrph Nessie
catalog" (Option A) — a genuine discrepancy I am surfacing, not silently resolving.** Recommendation: **A** (one
catalog / one marker / one refresh model = the whole point of co-owning both projects). CTO's ruling picks the
catalog; the IAM simulate + the TF plan follow it.

## 4. Kuzu LEFT-JOIN projection — the KUZUSPLIT coupling, SETTLED as ONE refresh model (held on P1 to build)

**The design that makes both projects coherent (this is the reconciliation the standing condition asked for):**
the summary is an **editorial OVERLAY applied AFTER the graph projection**, never a `graph_nodes` column. So:

- **`comp-kuzu-full`** (MSTR startup): full graph projection → THEN LEFT-JOIN `resource_summaries` HEAD
  (latest-version-per-arn) onto `CloudNode` by `arn`, setting `n.summary` + `n.summary_version`.
- **`comp-kuzu-inc`** (every agent): incremental MERGE/DETACH-DELETE on the graph delta → THEN **re-apply the
  overlay** from `resource_summaries` HEAD. **Critical invariant:** a node MERGE from `graph_nodes` carries NO
  summary, so the overlay re-application must run after every graph delta or an upserted node loses its editorial
  layer (null summary). The overlay step is therefore a member of BOTH refresh modes — ONE refresh path, two graph
  modes, one shared overlay re-apply. This composes cleanly with the P0/P1 model (the overlay is cheap: a bounded
  join keyed on arn, applied on the same tmp DB before the atomic swap).
- **Serve-labeled-stale (§4 gate) interaction:** when `-inc` serves labeled-stale (large delta, pre-MSTR-full),
  the overlay it carries is ALSO prior-vintage — consistent, honestly labeled. No special case.

**Build order:** this projection lands **with/after KUZUSPLIT P1** (I own both) — the `kuzu_cli.py` mode flag P1
adds is where the overlay-re-apply hooks in. Building them together avoids two refresh paths.

## 5. Lane note (no carve-out needed for THIS slice)

The table store-writer + TF live in `infra/aws/globgrph/**` + `infra/aws/terraform/globgrph/**` — **AE-writable**
(`0.8.0_AE_CloudComp` enumerated in the infra/aws AE lane). So the PH1 table work does NOT need the
`org/modules/graph` ANY_EXEC carve-out. That carve-out is needed only for (a) base's `summary_corpus.py` (base's ask
open with CTO) and (b) my PH2 `.tools/comp-similar` + `comp_similar*.py` — I'll request it when I open PH2.

## 6. What I need from CTO (plan-gate)

1. **Rule the write-path fork (§3):** Option A (Nessie/in-VPC, recommended — one refresh model) vs B (Glue). This
   gates the store-writer design + the IAM target + the TF plan.
2. On A: confirm the ECS-producer approach (or an existing in-VPC actor to extend) so the TF diff is minimal pure-add.
3. Then I: run the IAM simulate on the exact ARN, author the store-writer (`infra/aws/globgrph/resource_summaries_store.py`,
   cse_store template, dev-box self-testable) + the TF, and route the **held** plan for your plan-gate before any apply.

**Status:** PH1 grounded + specced to the arch fork. Blocked-forward on (a) CTO write-path ruling and (b) KUZUSPLIT
P1 for the projection — both real external gates, not stalls. Engine adopted + verified; schema settled; the
KUZUSPLIT coupling is reconciled as ONE overlay-over-two-graph-modes refresh path.
