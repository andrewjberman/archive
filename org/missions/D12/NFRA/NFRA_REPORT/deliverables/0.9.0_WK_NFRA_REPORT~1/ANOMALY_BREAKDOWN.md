# ANOMALY BREAKDOWN — connected resources COMPUTED, the written account GENERATED (cell RP-s-12, outcome FWD-12)

Authority: `NFRA_REPORT_PRD.md` manifest row S12 (`FWD-12`), `C-AI` parts 1 and 2 (verbatim below), and
build-ladder rung 2: `org/modules/graph/graph-call-manifest.yaml` is QUERIED here, never rebuilt.
Depends on, and renders through, `STATE_MODEL.md` (`RP-s-1`) and `MONITORED_VS_SERVED.md` (`RP-s-11`) —
both present at this worktree's base, both OBSERVED COMPLETE.

## 0. C-AI parts 1 and 2 — the spine, quoted then enforced

> 1. **DECLARED PER REGION** — every part is `COMPUTED`, `GENERATED` or `QUOTED`, legible without
>    knowing how the report is built.
> 2. **A GENERATED PART IS NEVER THE SOLE CARRIER OF A FACT.** The connected-things breakdown is
>    `COMPUTED` (it comes from the dependency graph); the analysis beside it is `GENERATED` and is a
>    reading OF that evidence. **Strip every generated sentence and the report must still be true and
>    still checkable.**

**TIGHTENED, per this cell's own text:** the written account must assert **NOTHING THE BREAKDOWN DOES
NOT SUPPORT.** Every `GENERATED` sentence in §3/§4 below is checked against this before being written,
not after.

## 1. THE MECHANISM — query the existing graph, never rebuild (build-ladder rung 2)

The connected-things half is answered by `org/modules/graph/graph-call-manifest.yaml`'s own canonical
entry:

```
id: trace.blast.what_breaks
use_case: "What breaks if I change this function/file/artifact (repo blast radius)?"
canonical_call: "comp-blast <fn-or-arn> [--function name] [--check-consumers]"
tool: comp-blast
mode: query-cached
anti_pattern: "Explore-agent sweep or manual grep for dependents"
```

No graph was derived, rebuilt or hand-assembled for this cell. Every connected-resource list below is
`comp-blast`'s own output against the served, cached graph, bounded per call (every invocation below
completed in under 6 seconds; none approached the 120s ceiling).

## 2. THE PER-ROW BLIND-SPOT LIMB — the coordinator's central requirement, built in, not bolted on

**This cell's entire `COMPUTED` half is a connectedness claim drawn from the same graphs `RP-s-7`
measured as incomplete.** Three independent sources establish that a connectedness breakdown can be
confident, complete-looking, and wrong:

1. **`NFRA_REPORT-Z-W1-S1`** (this worker, `RP-s-7`): `comp-blast`'s graph models **NO edge** between
   `GOLD_SCRIPT` nodes and Lambda/portal nodes, positive-control-confirmed on a definitely-live lambda.
2. **`NFRA_REPORT-Z-W1-S2`** (this worker, `RP-s-7`): `comp-pipescript`'s static parser misses a write
   routed through a dynamically-constructed S3 key (prefix concatenation or a key-building helper).
3. **`comp-blast` SAYS SO ABOUT ITSELF, independently, in its own output** (§4b below): a zero-dependent
   result prints `"Zero" = no EXTRACTED edge, NOT provably no consumer. A real consumer reading this via
   a dynamic/FUNC-key (the comp-pipescript miss class) is INVISIBLE here."` — the tool's own maintainers
   named the exact failure mode `NFRA_REPORT-Z-W1-S2` measured, independently of this project.

**Therefore every breakdown in this document carries a fourth, mandatory field beyond
what-feeds-it/what-reads-it/what-else-is-affected: WHAT THIS QUERY CANNOT SEE, stated per row.** A
breakdown with zero connected resources is never rendered as "isolated" or "safe" — it is rendered
`PHANTOM-CONSUMER` (`comp-blast`'s own term, kept rather than replaced, per the "reuse before mint"
discipline) with the specific edge classes this instrument does not model named beside it.

## 3. WORKED EXAMPLE 1 — `trade-submission-api` (anomalous per `RP-s-11`, `NFRA_REPORT-Z-W1-S4`)

**COMPUTED** (`comp-blast arn:aws:apigateway:us-east-1::/apis/w8jnzvs21g --direction both --json`,
WITHIN BUDGET, 30 of 30 traversal, ~6s): 30 connected resources —

| Category | Members |
|---|---|
| Lambda functions (4) | `trade-auth-handler`, `trade-dashboard-api`, `trade-submission-handler`, `trade-workflow-handler` |
| DynamoDB tables (4) | `opal-trade-submissions`, `opal-users-v2`, `trade-security-identifiers`, `trade-users` |
| S3 bucket (1) | `opal-data-trade-submissions` |
| KMS keys (2) | `64f25291-...`, `86cc6c40-...` |
| IAM role + inline policies (3) | `trade-submission-lambda-role` (+ `opal-users-v2-access`, `trade-submission-policy`) |
| API routes (7) | 7 route ids under this API |
| Lambda layer (1) | `openpyxl-layer` |
| Code-graph cluster nodes (8) | `motif:a-api` + 7 `motifi:a-api:*` sub-nodes |

**GENERATED** (a reading OF the table above, asserting nothing beyond it): *If `trade-submission-api`
misbehaves or is compromised, the resources whose data or behavior could be affected are these four
Lambda functions, four DynamoDB tables (including one literally named `trade-security-identifiers`),
one S3 bucket, and the KMS keys encrypting them. `RP-s-11` (`MONITORED_VS_SERVED.md` §3b, this same
worker) already established that none of the estate's 51 CloudWatch alarms names this API by ID or
name — so nothing in this connected set would surface an anomaly on this surface automatically.*
**Strip-test: remove the paragraph above and the table and the RP-s-11 citation both still stand alone,
true and checkable — the paragraph adds no fact not already in one of the two.**

**WHAT THIS QUERY CANNOT SEE (declared, per row):** `comp-blast`'s graph models AWS-native
resource-to-resource edges (API Gateway → Lambda → DynamoDB/S3/KMS/IAM) with real specificity here — 30
distinct, named resources, not a generic placeholder. It does **not** model whether any of these four
Lambdas' own Python code additionally reads or writes a gold-layer artifact or reaches a portal
component (`NFRA_REPORT-Z-W1-S1`'s edge class) — if `trade-submission-handler` also touched gold-layer
data, that specific edge would be invisible to this exact query, the same way it was invisible for every
gold script `RP-s-7` walked.

## 4. WORKED EXAMPLE 2 — the CloudFront distribution `E1DHJH4Y1W8YC2` (anomalous per `RP-s-11`)

### 4a. COMPUTED

`comp-blast arn:aws:cloudfront::313476888478:distribution/E1DHJH4Y1W8YC2 --direction both
--check-consumers`, WITHIN BUDGET, **0 of 0 traversal**:

```
PHANTOM-CONSUMER: ...E1DHJH4Y1W8YC2 -- zero dependents IN GRAPH (both directions)
  Node type: CLOUDFRONT_DISTRIBUTION
  "Zero" = no EXTRACTED edge, NOT provably no consumer. A real consumer
  reading this via a dynamic/FUNC-key (the comp-pipescript miss class) is
  INVISIBLE here. Verify (grep the artifact key / comp-pipescript consumers)
  before treating as orphan -- do not assume safe-to-delete.
```

**Positive control, run in the same breath:** the sibling distribution `EVTSA9VEHNZVH` returns
`CONSUMER-OK ... has 353 dependent(s)` on the identical call — the zero above is not a broken probe.

### 4b. GENERATED (asserting nothing beyond §4a)

*This distribution returns zero connected resources from `comp-blast`'s graph, in either direction, while
its sibling returns 353 through the identical call — the tool itself states this is not proof of no
consumer, naming the same dynamic-key blind spot `NFRA_REPORT-Z-W1-S2` measured independently. Combined
with `RP-s-11`'s separate finding (zero of 51 CloudWatch alarms reference this distribution by its
structural `DistributionId` dimension), two independent instruments now return the same "nothing found"
answer for this surface — which is stronger than either alone, but neither instrument can rule out a
consumer or a monitor reached through a path outside what it models.* **This document does NOT
conclude the distribution is unused, orphaned, or safe to remove — that conclusion is not supported by
either instrument and is not made here.**

**WHAT THIS QUERY CANNOT SEE (declared, per row):** everything — this is the `PHANTOM-CONSUMER` case
itself. No connected-resource claim of any kind is made for this row beyond "the graph extracted zero
edges," and the reason that could be false (a dynamic-key consumer) is named in the same sentence as the
zero, not left for a reader to discover later.

## 5. THE STRIP TEST, PERFORMED ON THIS WHOLE DOCUMENT (feeds AC3, graded at L9, not here)

Removing every `GENERATED` paragraph in §3–§4 leaves: the `trace.blast.what_breaks` manifest entry (§1);
the 30-resource table with its category breakdown (§3); the `PHANTOM-CONSUMER` output block and the
353-dependent positive control (§4a); and the three cited surprise rows (§2). **Every one of those is
still true and still checkable on its own** — none depends on a `GENERATED` sentence to be verifiable,
and no fact stated in a `GENERATED` paragraph is absent from a `COMPUTED` or `QUOTED` region beside it.
This is offered as the evidence for `3.0.0_SA_CVO~Z`'s L9 grading, not as a self-grade.

## 6. What this document does NOT do

- Does not conclude any surface is safe to delete, orphaned, or definitively unused — `PHANTOM-CONSUMER`
  is rendered as a declared instrument limit, never as a negative finding about the world (same
  discipline `RP-s-11`'s `INSTRUMENT-CANNOT-SEE` state and `RP-s-7`'s declared blindnesses already
  established for this project).
- Does not rebuild, extend, or modify `org/modules/graph/graph-call-manifest.yaml` — read and cited only,
  per build-ladder rung 2 and CLAUDE.md rule 20 (QUERY, NEVER REBUILD).
- Does not generate an account for a row this cell has not also computed a breakdown for — no anomalous
  row anywhere in this project is described in prose without its `comp-blast` table or `PHANTOM-CONSUMER`
  block beside it.
