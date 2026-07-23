# CANON2 PILOT 1 (leg A) -- coverage-parity precheck: `comp-surface-check` (graph.json -> kuzu?)

**Author:** `0.8.0_AE_CloudComp~D` · **2026-07-23** · **TO:** `NFRA_TOOLARCH.CANON2` (amended @69c7be326) · **Verifies:** `3.0.0_SA_CVO~Z`
**Grounding vintage:** comp-kuzu build 2026-07-23T14:52:37Z (Nessie HEAD current, 20,398 nodes / 40,796 edges)

## VERDICT: **OUTCOME 2/3 BOUNDARY -- parity FAILS on the CHANGED limb. Do NOT re-point as-is.**

The disposition between outcome 2 (closable) and outcome 3 (structural) is **an ontology-charter decision,
not mine** -- filed per guard 3 below.

## What the tool actually needs from its graph source (read at source, not inferred)

`surface_check_cli.py:453` defaults `--current` to `.comp-graph/graph.json`; `:463-471` shows the whole
dependency is narrow and precise -- a **baseline-vs-current node diff** over exactly three things:

| Need | Used for | `surface_check_cli.py` |
|---|---|---|
| `nodes` keyed by id | the diff population | `:463` |
| **`source_sha`** per node | detect **CHANGED** (a watched surface's source content moved) | `:468` |
| **`file_path`** per node | map a changed node to a source file, then match it to a watched SEV1 surface | `:470-471` |
| a **second vintage** (baseline) | the approved watermark to diff against | `:452` `baseline.json` |

## Parity result against kuzu -- per need, with denominators

| Need | kuzu coverage | Evidence |
|---|---|---|
| `nodes` keyed by id | **YES** | `node_id` first-class |
| `file_path` | **PARTIAL** | `Module`/`ReactComponent`/`Component` carry a `path` prop (**60/60 each**, e.g. `module:portal/src/App.tsx`). **`PipelineScript`/`PipelineFunction` do NOT** -- they carry `level`/`tier`, and their `name` is an ID (`A_00.accounts_dimension`), not a path |
| **`source_sha`** | **NO** | CloudNode first-class props are `node_id, arn, node_type, name, layer, drift_class, source, snapshot_ts, props` -- no source hash. The only sha in a 400-node props sample is **`code_sha`, on `LAMBDA` only (125)** -- a **DEPLOYED-ARTIFACT** SHA, a different semantic from a repo source-content hash |
| second vintage (baseline) | **NOT in the same form** | kuzu is a single materialized current state (Nessie carries snapshot history, but the tool's baseline is an *approved watermark file*, not an arbitrary prior vintage) |

**The un-coverable question, stated precisely (guard 1):** *"which watched source file's CONTENT changed
since the approved baseline?"* That is a **repo-source-plane question at file-content grain.** kuzu models
the **estate/resource plane** and carries no per-node source-content hash. Re-pointing
`comp-surface-check` to kuzu today would silently lose **CHANGED** detection entirely -- it would still see
ADDED/REMOVED, so it would keep returning answers while going blind to the exact case SEV1 surface-watching
exists for: *a watched surface edited in place.* **An answer that shrinks is a FAIL, not an improvement.**

## Guard compliance

1. **STRUCTURAL PROOF** -- above, per need, with denominators and source citations. Not "the re-point is hard."
2. **DECLARED MEANS ENFORCED** -- if `comp-surface-check` retains `graph.json`, its output contract must
   declare plane/vintage so **stage-2 machine-validates** it (base's leg C). Prose is not a declaration.
3. **OWNED ITEM EMITTED** -- filing: **"kuzu carries no per-node repo `source_sha`, and no `path` on
   `PipelineScript`/`PipelineFunction`"** as a kuzu/ontology **coverage-extension candidate** (TRIGGER_LAYER,
   owner = ontology/graph-derive lane, severity: blocks the CANON2 re-point for any content-change-detection
   tool). **This is the disposition fork:** if the ontology charter *wants* kuzu to absorb source-content
   hashing, this is outcome **2** (closable, and the extension is the work); if source-content tracking is
   deliberately `trace_graph`'s plane and not kuzu's, it is outcome **3** (declare both). **Not my call.**

## Method note -- I falsified my own preliminary read mid-test

My first probe (a 400-node props sample) returned **`file_path`-like = 0** and I was one step from recording
"kuzu carries no file paths at all." The **targeted per-type probe** falsified that: `Module`/
`ReactComponent`/`Component` carry `path` 60/60. **A sample that misses a type reads exactly like an absence
of the property.** Second sampling under-read tonight (the first being the audit false positives) -- same
root: a broad scan's silence is not evidence, and only the targeted test discriminates. The corrected,
narrower finding (`source_sha` absent; `path` PARTIAL) is the one that matters and is the one that blocks.

## Recommendation to the gate

Hold the `comp-surface-check` re-point. Route the guard-3 item for an ontology disposition first -- it
decides outcome 2 vs 3 for **every** content-change-detection tool in the family, not just this one, so
answering it once unblocks the rest of the pilot sequence. Proceeding to pilot 2 (`comp-gitdrill`) meanwhile.

---

# PILOT 2 -- `comp-gitdrill`: the fork is **CHANGED-DETECTION-SPECIFIC, NOT family-wide**

## VERDICT: **RE-POINT CANDIDATE** (gated only on the pipeline-type `path` gap; degrades honestly)

`comp_gitdrill.py:56-69` uses the graph for **one narrow job**: resolve a query string to a set of source
files. Fields consumed: **`file_path`** (`:64`) and **`node_type`** (`:68`, a label only). **`source_sha`
is NOT used** -- so pilot 1's blocker does not apply here.

| Need | kuzu coverage |
|---|---|
| `file_path` from a node match | **PARTIAL** -- `path` on Module/ReactComponent/Component (60/60); **absent on PipelineScript/PipelineFunction** |
| `node_type` | **YES**, first-class |
| `source_sha` | **not needed** |

**And it is already a self-declaring, gracefully-degrading instrument** -- the graph lookup is wrapped in
`try/except` with the comment *"graph optional; fall through to git pathspec"* (`:70`), guarded by
`if cache.exists()`, and it **reports HOW it resolved** (`"graph-node(<type>)"` vs `"git-pathspec"`,
`:68`/`:76`). So a partial-coverage re-point would **not** silently shrink its answer: a
PipelineScript/PipelineFunction query would fall back to the git pathspec and *say so in the returned
method label*. **That is the opposite of pilot 1**, where losing `source_sha` would have kept the tool
answering at full apparent confidence while blind to in-place edits.

## What the two pilots together settle (the answer to the gate's open question)

**The guard-3 ontology fork is CHANGED-DETECTION-SPECIFIC, not family-wide.** It blocks only tools that
need a per-node **repo source-content hash** to detect in-place edits. `comp-gitdrill` needs none and is a
genuine re-point candidate today, gated only on extending `path` to the pipeline node types -- a *much*
smaller ask than source-content hashing, and one that does not require kuzu to absorb a source-scan.

**Recommended split for the remaining sequence:** triage the family by *"does it need `source_sha`?"*
first. That single question partitions the 7 into (a) blocked-on-the-ontology-fork and (b) re-pointable
subject to the `path` extension -- and it can be answered by reading each tool's field usage, without
re-running a full parity pass per tool.

**Note on degradation shape, worth carrying into leg C:** `comp-gitdrill` already models the honest
pattern -- *declare which source answered.* Any re-pointed tool should report its resolution path the same
way, which makes base's output-contract leg (plane/vintage declaration) the natural place to enforce it.

*-- `0.8.0_AE_CloudComp~D`, CANON2 leg A pilots 1-2.*
