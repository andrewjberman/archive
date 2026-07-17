# NFRA_COMPSIMILAR — PRD / CTO-gate brief

**Tool:** `comp-similar` · **Project:** NFRA_COMPSIMILAR · **Macro:** NFRA
**Author:** 0.8.0_AE_CloudComp · **Date:** 2026-07-17 · **Status:** PRD v0.1 — AWAITING CTO ARCH-GATE
**Gate:** 1.0.0_SA_CTO (registration invariant + arch) · **Sovereign:** Andrew-direct (verbatim @dc4207c7c / 1d81e760b / 3d326af47)
**Home:** DRAFT in 0.8.0_AE_CloudComp deliverables (authored per Andrew-direct); **CTO promotes to `docs/architecture/NFRA_COMPSIMILAR_PRD.md` at his gate** (architecture-docs lane = ANY_CTO, owned-paths-enforced — a draft awaiting his gate lives here until adopted).
**Priority:** P3 (OPAL_CONSOLIDATION cleanup) — the compose-the-triad half is directly consolidation-useful; the new tool slots behind it, but it FEEDS the decommission column, so it is in-scope, not deferred.
**Source assessment:** `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/DECOMMISSION_TOOLING_ASSESSMENT_20260717.md` @890e66375

> This brief is deliberately three documents in one, because Andrew scoped it that way: **the WHY**
> (the doctrine — why a similarity tool exists and how it completes a family), **the HOW** (the
> operator playbook — how to actually use comp-similar *with* comp-dups / comp-debris / comp-heat /
> comp-drift to find something), and **the WHAT** (the infrastructure to build). A tool shipped
> without its doctrine and its usage is a tool nobody reaches for; the estate has ~60 of those risks
> already. Build the concept and the playbook, not just the executable.

---

## 0. TL;DR

`comp-similar` scores **BM25 lexical similarity over a resource's SUMMARY** (what it *does*), where
comp-dups scores over its NAME and file-body (what it *is called* / *is made of*). It is the
**functional-overlap** axis the decommission tool-family is missing. Its headline use is Andrew's
**superseded-twin fast-scan**: a decommission candidate = a similar-name cluster where two resources
have **very high summary similarity** AND a **large hot-vs-cold heat divergence** — i.e. one resource
quietly replaced another and the old one was left running. Engine = the existing `dup_scan.py` BM25
class (copy-reuse). The only genuinely new substrate is a **stable resource-summary corpus**, stored
as an ARN-keyed append-only Iceberg table projected into Kuzu as a node property. Advisory, never
deletes, hold-aware — same discipline as comp-dups and comp-debris.

---

## 1. WHY — the doctrine

### 1.1 The mission: consolidation makes confusion, and confusion is a correctness cost
OPAL_CONSOLIDATION moves the estate onto one monolith (`opal-data-assets`) with consistent runners
(the inf/cot/bd gold EC2s migrating onto the shared buckets). **Migrations do not delete the thing
they replace — they leave it running.** The old bucket, the old Lambda, the superseded table linger:
cold, overlapping, and — this is the load-bearing harm — **confusing to an agent.** An agent greps
the estate, finds two buckets that look like they do the same job, and cannot tell which is live.
That is not untidiness; it is the exact failure class CLAUDE.md 17a names ("deployed wins, rewrite the
canonical repo" cements a violation) and the false-outage class NEVER#1 names (reasoning from a dead
artifact). **Andrew, verbatim:** *"so agents do not get confused with deprecated or overlapping
resources."* The product of this work is not disk savings — it is **an estate an agent can reason
about without tripping over its own history.**

### 1.2 Why no single signal finds a superseded resource
Every existing coldness/duplication signal has a documented failure mode that makes it insufficient
ALONE — and each failure mode is exactly the one the estate has already been burned by:

- **Coldness alone** (comp-debris) can't tell *superseded* from *rare-event guard*. comp-debris's own
  refinement #1 refuses to: a never/rarely-invoked resource is `STILLBORN-OR-GUARD`, not cold. A
  monthly compliance Lambda looks identical to abandoned debris on invocation count.
- **Name-similarity alone** (comp-dups) false-positives on *expected architecture*: `bd`/`cot`/`inf`
  same-named resources are firm-separation by design, and comp-dups already SUPPRESSES 276 cross-firm
  pairs auditably. A name match is not a duplication.
- **Structural (body) similarity alone** (comp-dups content tier) misses a functional twin with a
  *different implementation* — two buckets serving the same data written by different producers share
  no bytes.
- **A blind read is not a dead resource** (comp-debris refinement #2, the anti-correlation trap): a
  resource we could not measure reads UNKNOWN, never cold.

### 1.3 The heuristic (Andrew's algorithm) — jointly sharp
Supersession becomes visible only at the **intersection**, and comp-similar supplies the axis that
completes it:

```
  SUPERSEDED-TWIN(a, b)  ⟺   name_similar(a, b)          [comp-dups name tier — cluster]
                        AND   summary_similar(a, b) ≥ HI  [comp-similar — they DO the same thing]
                        AND   |heat(a) − heat(b)| large   [comp-heat / comp-debris — one hot, one cold]
                                with one HOT and one COLD

  ⟹  the COLD one is a decommission candidate; its HOT twin is the live replacement.
```

Each clause kills the others' false positives: **summary-similarity** confirms two coincidentally
similar-named things are actually functional twins; the **heat DIVERGENCE** (not mere coldness) is
the supersession tell — the whole point is that one is hot *because* it replaced the other; the
**name cluster** makes the scan fast (compute the expensive summary similarity only within
name-clusters that already diverge on heat). Individually weak, jointly sharp. This is the
monolith-cutover shape precisely: `opal-data-inf` (cold) beside `opal-data-assets/.../inf` (hot),
names + summaries near-identical.

---

## 2. THE FAMILY — how comp-similar ties into the others

The decommission tools are **orthogonal axes on the same resource**, and decommission *confidence*
comes from **agreement across axes** — never one reading. comp-similar adds the FUNCTIONAL axis:

| Tool | Axis it measures | The question it answers | Its blind spot (why the others are needed) |
|---|---|---|---|
| `comp-debris` | **Invocation** (CloudWatch/CloudTrail last-invoke) | *Is it still running?* | Can't tell superseded from a rare guard; Lambda-only in v1 |
| `comp-heat` | **Write/data freshness × git code-heat** (Trino federation) | *Is its data/code still moving?* | Freshness ≠ purpose; blind to whether a twin exists |
| `comp-dups` | **Name + file-body** (BM25, structural) | *Is there a literal/structural twin?* | Misses functional twins with different code/names |
| **`comp-similar`** *(new)* | **Summary / semantics** (BM25 over what it DOES) | *Does a differently-named resource do the same job?* | Similarity is a hypothesis; needs heat-divergence to mean "superseded" |
| `comp-drift` | **Propagation / map-vs-territory** | *Did a change ripple correctly; is our belief true?* | Sees consistency, not usage |
| `comp-deadgrant` | **Access (dead grant × fail-silent reader)** | *Is a grant dead / a reader silent?* | Getter-level, security-first, not a decommission verdict |
| `comp-trigger` | **Wiring** (EventBridge/Scheduler forensics) | *Is anything wired to fire it?* | Wiring present ≠ used; absent ≠ dead (manual invokes) |
| `comp-iam` *(expanded)* | **Identity plane** (last-used, who-can-reach) | *Does anything still hold/use its grants?* | Today: Terraform-DESIRED, action-only, no last-used |

**The conceptual spine:** comp-dups answers *"is this the same THING?"* (structure); comp-similar
answers *"does this do the same JOB?"* (function). A migration produces functional twins that are
NOT structural twins (new producer, new code, new name) — invisible to comp-dups, visible to
comp-similar. That is the gap it fills, and why Andrew flagged it as its own tool rather than a
comp-dups mode: **same engine, different corpus, different question.**

---

## 3. HOW TO USE IT — the decommission playbook

This is the operator doctrine. It must ship with the tool (in the manifest note + the comp-which
routing), because a family of eight tools with no stated workflow is eight tools nobody composes.

### 3.1 The investigation pipeline (broad → confirm → dispose)
```
  STAGE 1 — LEDGER (broad, cheap):   comp-debris  → the coldest-first candidate tail
                                      (EXTEND past Lambda to S3/DDB/EC2/EventBridge via CloudTrail)

  STAGE 2 — CONFIRM (on the cold tail ONLY — never the whole estate):
     comp-similar   → does the cold candidate have a HOT functional twin?  (supersession)
     comp-dups      → does it have a structural/name twin?                  (literal duplication)
     comp-heat      → is its data/code actually stale, or just uninvoked?   (freshness corroboration)
     comp-trigger   → is anything wired to fire it?                         (orphan check)
     comp-deadgrant / comp-iam last-used → does anything still hold/use it? (access-dead)
     comp-drift     → is the record consistent with reality?               (belief-vs-truth)

  STAGE 3 — DISPOSITION:  agreement across axes → confidence-graded verdict →
     OPAL_LCLRPO census-cleared batch → CTO gate → Andrew delete-word.  (never a new disposal path)
```

### 3.2 The FAST SCAN (comp-similar's headline mode — Andrew's "scan very fast")
Skip the full ledger. Directly enumerate superseded twins:
```
  comp-similar supersede   # for every similar-name cluster with a heat-divergent pair,
                           # rank by summary_similarity × heat_divergence → the candidate list
```
This is the one-pass estate scan for "old version left running next to its replacement."

### 3.3 Situation → tool (extends the CLAUDE.md comp-tools table)
| Situation | Reach for |
|---|---|
| "What in the cloud has gone dormant?" | `comp-debris` (the ledger) |
| "Is this cold thing superseded, or a rare guard?" | `comp-similar supersede` + `comp-heat` (twin + divergence) |
| "Are there literal duplicates / dead twins?" | `comp-dups` |
| "Do these two differently-named resources do the same job?" | `comp-similar <a> <b>` |
| "Is anything still wired to / still granted this?" | `comp-trigger` + `comp-iam` last-used |
| "Does our record of this resource match reality?" | `comp-drift` |
| "I have a cold candidate — is it safe to retire?" | run STAGE 2 (all axes) → OPAL_LCLRPO |

**Discipline that binds every use (inherited from comp-debris / comp-dups):** never-invoked ≠ cold;
UNKNOWN is a band, not cold; a resource with NO summary is UNKNOWN (no twin *known*), never "unique";
ADVISORY — the tools produce a worklist, removal is human-confirm + hold-aware (INF-chain / frozen /
sovereign names excluded from any reap output).

---

## 4. WHAT WE BUILD — the infrastructure

### 4.1 Engine — reuse, don't reinvent
The `dup_scan.py` BM25 class (`org/modules/graph/debtscan/dup_scan.py:84`) is a self-contained scorer
over `[doc_strings]`. comp-similar reuses it verbatim (Andrew's stated intent). Confirmed cheap: the
comp-state 12s-fix proved the BM25 layer was never the cost — serial subprocess I/O was — so a corpus
assembled in ONE graph read stays fast. **Engine convention** (mirrors comp-dups, locked with CVO to
avoid a fork): engine reuse lives at the debtscan home; tool = `.tools/comp-similar` (thin wrapper).

### 4.2 Corpus — the stable resource-summary location (THE novel substrate)
Andrew named the crux: *"somehow get a stable summary location of the resource."* Resolved:

- **NOT AWS Description fields.** Description exists on Lambda/IAM/EventBridge/SG but NOT S3/DDB — most
  of the consolidation surface — so a Description corpus is structurally blind to the majority of the
  estate (the identical failure class as comp-iam being action-not-(action,resource): a tool
  confident while blind to half its subject).
- **A per-resource SUMMARY, stored as an ARN-keyed overlay** (grounded, source assessment Part E):
  the `graph_nodes` schema is `[node_id, arn, node_type, name, layer, drift_class, source,
  snapshot_ts, props]` — **there is no summary field today**, and `props` is empty for the S3 node
  sampled. So the summary location must be **established, not read.**
  - **Storage:** a new append-only Iceberg table in the globgrph Nessie catalog — `resource_summaries`
    — keyed on **ARN** (confirmed the natural key: for cloud resources `node_id == arn`, e.g.
    `arn:aws:s3:::opal-data-inf`). Schema: `arn, node_type, summary, authored_by, authored_at,
    source_inputs, summary_version`. Snapshot-versioned; current-state = latest-per-ARN — the same
    discipline as the `*_snap` siblings.
  - **NOT a column on `graph_nodes`** — that table is machine-derived and regenerated every derive /
    incremental_updater run; an editorial column would be clobbered. Editorial and derived content
    live in separate tables.
  - **Projection to Kuzu:** the comp-kuzu refresh LEFT-JOINs `resource_summaries` (latest-per-ARN)
    onto `graph_nodes` on node_id/ARN, so every current-state node carries a `summary` property in
    full fidelity. Because it is a join-overlay, a re-derive NEVER clobbers the editorial layer — the
    one-off authoring investment is durable **by construction.** New resources left-outer-null until
    an incremental pass fills them.
- **v1 corpus without waiting on authoring — DERIVE-AT-SCAN:** for v1, synthesize each summary
  document from what the graph already holds (`node_type + name + layer + arn + producer/served/
  consumer edges + drift/reachability flags`) — exactly what `pipescript` already projects per thread.
  Uniform across resource types, no producer change. The authored `resource_summaries` overlay (§4.6)
  is the enrichment that replaces derive-at-scan where it is too thin — never a Description fallback
  for thin classes (re-opens the S3/DDB hole).

### 4.3 The joint-scan algorithm
`supersede` mode: (1) cluster ARN-bearing resources by name similarity (reuse comp-dups' name tier +
its cross-firm/env/service suppressors, so expected same-names don't cluster); (2) within each
cluster, compute heat per member (comp-heat / comp-debris band); (3) keep clusters with a HOT∧COLD
divergence; (4) compute summary BM25 only on those (the cost gate); (5) rank by `summary_sim ×
heat_divergence`, emit the cold member as the candidate + its hot twin as the named replacement.

### 4.4 CLI surface (proposed — CTO rules the final shape)
```
  comp-similar <arn|name> [arn|name]   # pairwise / one-vs-corpus summary similarity, ranked
  comp-similar supersede               # the fast superseded-twin scan (headline mode)
  comp-similar cluster [--type T]      # functional clusters across the estate (overlap census)
  comp-similar --json / --self-test    # machine output + offline regression gate
```

### 4.5 Registration (the COMPCLOSE invariant — non-negotiable for the gate)
A new `.tools/comp-*` MUST satisfy `comp-manifest-check` (existence + routable + completeness):
- `tools_index` entry in `org/modules/graph/graph-call-manifest.yaml` (full house-style note: engine
  convention, dogfood target, cadence, the comp-which routing string), OR excluded-with-reason;
- a curated comp-which routing rule (e.g. *"do two resources do the same job / find a functional
  duplicate or a superseded resource left running next to its replacement → comp-similar"*);
- a routing-test addition (comp-similar is a live routing target; gibberish still abstains — must not
  regress the frozen `comp-which-routing-baseline.json`);
- coverage-map entry; `comp-manifest-check` PASS.

### 4.6 The one-off summary-authoring pass (costing, from the source assessment Part E)
To populate `resource_summaries` with authored (not derived) summaries: **~841 independent cloud
resources** is the natural one-off scope (of 1,894 ARN-bearing; the ~1,050 dependent nodes — log
groups, policies, alarms, event-source-mappings — get mechanically-derived summaries). **~549** of
those are the prime compute/storage/data/eventing decommission targets, the recommended FIRST cut.
Each is a bounded per-node subagent task (read graph neighborhood + TF def + last-modified → 2-3
sentences); derive-at-scan pre-populates all mechanically so subagents ENRICH only the ambiguous /
high-value ones. Out of scope: the ~18,500 code/document nodes (already covered by code-heat /
ms-heat / comp-dups).

---

## 5. FAILURE MODES comp-similar must NOT ship with (controls, not care)

The estate's binding lesson (CONTROLS_OVER_CARE): a tool must be built so it CANNOT lie, not carefully.

- **False-twin (summary too coarse):** two resources score HIGH summary-similarity but do genuinely
  different jobs. CONTROL: similarity is never a verdict alone — the `supersede` mode requires the
  heat-divergence corroboration; a bare `comp-similar <a> <b>` reports a *score + a hypothesis*, never
  "duplicate."
- **Corpus-collapse into comp-dups:** if the summary is derived from the NAME, comp-similar just
  re-runs comp-dups. CONTROL: the summary corpus must be independently sourced (edges/purpose, not
  name); the self-test asserts a name-identical / purpose-different pair scores LOW and a
  name-different / purpose-identical pair scores HIGH.
- **The blind-row trap:** a resource with no summary row must be UNKNOWN (no twin *known*), never
  reported as unique. CONTROL: `resource_summaries` coverage is printed as a denominator on every run
  ("scanned N of M resources; K UNKNOWN-no-summary").
- **Dogfood regression target** (mirrors comp-dups' opal-users triplication): the monolith-cutover
  pairs — an old `opal-data-{inf,cot,bd}` path vs its `opal-data-assets` successor — MUST surface as
  superseded twins once both carry summaries; a run that cannot find a known-present superseded pair
  is a broken instrument reporting silence.
- **Hold-aware:** INF-chain / frozen / sovereign-named resources excluded from any candidate/reap
  output (reuse comp-debris' `_HELD_RX`).

---

## 6. ARCH DECISIONS FOR CTO'S GATE

1. **Corpus for v1:** derive-at-scan (i) vs authored-overlay-first (ii). Recommendation: (i) for v1,
   (ii) as enrichment. CTO's arch call.
2. **`resource_summaries` table:** approve the new Iceberg table + the Kuzu LEFT-JOIN projection into
   the current-state layer (a change to the comp-kuzu projection path — coordinate 0.7.0 for the
   derive/refresh side).
3. **comp-similar vs a comp-dups mode:** ship as its own tool (Andrew's framing, different
   corpus+question) vs a `comp-dups --summary` mode. Recommendation: own tool (registration clarity +
   comp-which routing distinctness). CTO rules.
4. **Where the summary-authoring pass runs** (the ~549-841 subagent fan-out): its own TO under this
   project, gated behind the compose-the-triad half.
5. **Heat source for `supersede`:** comp-heat (object/data) vs comp-debris (invocation) vs both. Both
   is most robust (data-cold AND invoke-cold = strongest supersession); CTO rules the join.

---

## 7. ACCEPTANCE CRITERIA (machine-checkable)

- `comp-similar <a> <b>` returns a bounded BM25 score + explicit hypothesis framing (never a bare
  "duplicate" verdict); `--self-test` PASSES the name-identical/purpose-different LOW +
  name-different/purpose-identical HIGH mutants.
- `comp-similar supersede` surfaces the dogfood superseded pair (a migrated `opal-data-*` path vs its
  `opal-data-assets` successor) once both carry summaries; prints the coverage denominator
  (scanned/total/UNKNOWN-no-summary) on every run.
- `resource_summaries` exists in Nessie, ARN-keyed, append-only; the Kuzu projection carries a
  `summary` property on ARN-bearing nodes; a graph re-derive leaves the summaries intact (join-overlay
  proof).
- `comp-manifest-check` PASSES (existence + routable + completeness); the frozen routing baseline does
  NOT regress (zero pollution, 100% gibberish abstention preserved).
- Advisory + hold-aware: held-named resources absent from candidate output; no delete verb.

## 8. Sequencing & scope

- **Phase 0** (this brief) → CTO arch-gate.
- **Phase 1** — the corpus: `resource_summaries` table + Kuzu projection + derive-at-scan populate.
- **Phase 2** — `comp-similar` engine + `supersede` mode + registration.
- **Phase 3** — the authored one-off summary pass (~549 prime targets first) as enrichment.
- **Priority:** P3, behind the compose-the-triad half of the assessment; but comp-similar FEEDS the
  decommission column (the superseded-twin scan IS the overlap detector), so it is in-scope for the
  consolidation cleanup, not a deferral.
- **Boundaries:** ADVISORY, never deletes (disposal = OPAL_LCLRPO's existing CTO-gated,
  Andrew-delete-word path — no second disposal path). Hold-aware. Sovereign boundary: bd/49F/Schwab
  reads follow the live block state (currently lifted; the D4 zero-reader window on opal-data-schwab
  still binds — no calls without 0.5.0's timing ack).
