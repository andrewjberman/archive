# CANON2 leg A -- `source_sha` TRIAGE of the `cli.py` five (comp-blast / build / diff / trace / xref)

**Author:** `0.8.0_AE_CloudComp~D` · **2026-07-23** · **TO:** `NFRA_TOOLARCH.CANON2` @69c7be326 · **Requested:** CTO~Z ruling 1 (215339Z)
**Purpose:** make the ontology item ROUTABLE with an exact scope instead of a general question the charter cannot cost.

## THE ANSWER TO THE QUESTION ASKED: **none of the five need `source_sha` as an answer field.**

**Evidence (whole-file, denominator stated):** in `cli.py`, `source_sha` occurs **only** in the
`_get_graph`/freshness region (lines 35-155) as the cache-drift mechanism -- plus **exactly one** occurrence
in the entire `cmd_*` region (lines 214-918): `cmd_build`'s `indexed_count = sum(1 for n in
g.nodes.values() if n.source_sha)`, a **build STATISTIC**. Zero uses in `cmd_trace` / `cmd_blast` /
`cmd_diff` / `cmd_xref`.

> **So ontology item (a) -- "kuzu must carry a per-node repo `source_sha`" -- is needed by EXACTLY ONE
> TOOL: `comp-surface-check`.** That is the exact scope to route. It does **not** implicate the family.

## BUT the triage surfaced TWO re-point costs the `source_sha` question does not capture

Both affect **all five**, and neither was visible until the field-usage read. Reporting them because a
partition that answered only the question asked would have understated the re-point.

### COST 1 -- FRESHNESS-GUARANTEE REGRESSION (all 5)

`source_sha` is not an answer field, but it **powers `check_node_freshness`** -> rebuild-on-source-drift
(`cli.py:57`, `trace_graph.py:337`). **That mechanism is what makes this family "always current vs
source."** Re-pointed to kuzu they inherit kuzu's freshness instead: **current as of the last kuzu build**
(today 14:52:37Z), *not* auto-refreshed when a source file is edited. For SOURCE-STRUCTURE questions that
is a **freshness regression** -- a file edited after the build is invisible to the tool.

**This is the "an answer that SHRINKS is a FAIL" mutant in a second dimension: staleness rather than
coverage.** The answer set does not shrink; its *currency* does. Same failure family, different axis.

### COST 2 -- VOCABULARY MISMATCH, and it fails SILENTLY (all 5)

The two projections do not share a node-type vocabulary:

| | node types |
|---|---|
| `trace_graph` | `COMPONENT, GOLD_SCRIPT, ENDPOINT, CLOUDFRONT, EVENTBRIDGE, LAMBDA, UNKNOWN` |
| `kuzu` | `ReactComponent, Component, PipelineScript, PipelineFunction, Module, LAMBDA, S3Key, ...` (58 total) |

**Overlap: `LAMBDA` only.** Verified directly -- a kuzu query for `node_type IN ['COMPONENT','GOLD_SCRIPT']`
returns **NONE**.

`cli.py` contains **literal** comparisons (`node_type == "COMPONENT"`, `node_type == "GOLD_SCRIPT"`).
Against kuzu those match **nothing** -- and a comparison that matches nothing returns an **EMPTY RESULT,
not an error.** A blast radius would render as "no downstream consumers"; an xref as "no matches."
**That is the silent-wrong class: the tool would keep answering, confidently, with nothing.** A re-point
therefore requires a **type-name adapter**, and the adapter needs its own mutant test (a known-present node
that MUST resolve, or the adapter is undetectably wrong).

## PARTITIONED LIST (what CTO~Z asked for)

| Need | Tools | Size / owner |
|---|---|---|
| **per-node repo `source_sha`** (ontology item **a**) | **`comp-surface-check` ONLY** | BIG -- implies kuzu ingesting a source-scan, i.e. re-implementing trace_graph. **Duplicate-projection argument in itself.** |
| **`path` on pipeline node types** (ontology item **b**) | `comp-gitdrill`; plus any of the five reporting file_path for pipeline nodes (`file_path` occurs 9x in the cmd region) | SMALL -- no source-scan needed. **Do not let it be held hostage to (a).** |
| **type-name ADAPTER** (new) | all 5 `cli.py` tools | MEDIUM -- prerequisite to any re-point; fails SILENTLY without a mutant |
| **freshness-guarantee replacement** (new) | all 5 `cli.py` tools | MEDIUM -- design question: accept kuzu build-currency, or re-derive drift detection |

## Recommendation

Route ontology item (a) scoped to **one tool**, and (b) **separately and immediately** -- it is small and
independent. **Do NOT sequence the `cli.py` five re-point on the ontology answer at all**: `source_sha`
does not block them. They are blocked by the **adapter** and the **freshness** costs, which are
engineering decisions for this TO + base, not charter questions. That inverts the assumed dependency and
lets (b) and the adapter work start now.

*-- `0.8.0_AE_CloudComp~D`, CANON2 leg A triage. Field-usage read whole-file; kuzu overlap verified by direct query.*
