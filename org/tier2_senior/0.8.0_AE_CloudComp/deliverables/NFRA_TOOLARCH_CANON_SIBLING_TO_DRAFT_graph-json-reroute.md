# DRAFT TO SCOPE (for `1.0.0_SA_CTO~Z` to gate + dispatch) -- trace-graph family: `graph.json` -> comp-kuzu canonical, COVERAGE-PARITY GATED

**Drafted by:** `0.8.0_AE_CloudComp~D` (CANON auditor) · **2026-07-23** · **Gate/dispatch:** `1.0.0_SA_CTO~Z` (ruling 210055Z: *"YES -- DRAFT THE graph.json SIBLING TO SCOPE"*)
**Parent:** `NFRA_TOOLARCH.CANON` (Andrew-direct) · **Audit basis:** `deliverables/NFRA_TOOLARCH_CANON_TOOL_SOURCE_AUDIT.md` @fd12a515b
**Status:** DRAFT SCOPE -- not a dispatched TO. CTO~Z authors/assigns; this is the scope off their plate.

---

## Why this is a SEPARATE TO (and not folded into CANON)

CANON's audit separated three severities. This family is the **ARCHITECTURAL, not-silent** one:

- **9 tools** -- `comp-blast, comp-build, comp-diff, comp-gitdrill, comp-graph, comp-manifest-check,
  comp-surface-check, comp-trace, comp-xref` -- all read `.comp-graph/graph.json` via
  `org/modules/graph/cli.py` -> `trace_graph.build_graph(_WORKSPACE)`.
- It is **NOT the silent-drift defect**: `graph.json` is source-scanned and **HEAD-pinned /
  self-invalidating** (`cli.py:54` rebuilds on any source-file SHA drift), so it never serves stale-vs-source.
- The kuzu re-point is already a **documented deferred follow-on** -- `cli.py:56` verbatim:
  *"the literal Kuzu-projection re-point, is the deferred follow-on."*

So the driver is Andrew's **one-canonical-projection** architecture, not an active staleness fire. That
makes it gate-able and sequenceable -- and it MUST be gated, per the risk below.

## THE LOAD-BEARING PRECONDITION -- coverage-parity precheck (BLOCKING)

**Do not re-point any tool before proving kuzu covers what `trace_graph` covers.** Rerouting a tool onto a
source that models less than its current source **silently shrinks its answer** -- trading a
*self-invalidating-but-complete* projection for a *canonical-but-incomplete* one. That is a coverage
regression wearing a canonicalization's clothes, and it is the exact intent-denominator failure this whole
program exists to stop.

**The risk is concrete, not theoretical** -- from the TOOLARCH.P1 archetype census @f38a386a6:
- kuzu canonical models a **resource/estate graph** (AWS / pipeline / frontend / M365) at 20,398 nodes.
- `trace_graph` models **source-level** structure (call / import / dataflow, per-symbol, SHA-tracked).
- The census's **R-0 boundary**: the records/governance plane is absent from kuzu entirely; the **frontend
  plane** was the least-described (RENDERS/PROP_PASSES unmapped at C1 until ONTOLOGY2 P1 @5d1161d70; still
  **0/7 frontend + 0/1 M365 canonical C2 motif families materialized**).
- Therefore "kuzu is canonical" does **not** entail "kuzu covers the structure tools' questions."

**Precheck must answer, per tool and with printed denominators:** for the questions each of the 9 tools
answers today off `graph.json`, does kuzu contain the nodes/edges needed to answer them *identically*?
Compare on real invocations (same inputs, both sources, diff the answers), not on schema inspection.

**Three legitimate outcomes -- the precheck DECIDES, the TO must not presuppose the reroute:**
1. **PARITY HOLDS** -> re-point the family to kuzu. The intended end-state.
2. **PARITY FAILS, GAP CLOSABLE** -> extend kuzu's coverage FIRST (graph-derive work), then re-point.
   Sequenced, not abandoned.
3. **PARITY FAILS STRUCTURALLY** (they answer genuinely different questions at different grains) -> **DO
   NOT RE-POINT.** The honest end-state is then to **DECLARE** both projections explicitly -- each tool's
   output contract naming its plane/grain/vintage -- so "two projections" is a *stated architecture*
   rather than an undocumented accident. **A declared second projection is not the defect; an
   undeclared one is.**

## Scope legs

| Leg | What | Owner |
|---|---|---|
| **A (BLOCKING)** | Coverage-parity precheck, per-tool, on real invocations, denominators printed; renders outcome 1/2/3 above | base `0.8.0_AE_CloudComp` (claimed it: *"I'll own it + the integration"*) |
| **B** | Re-point `cli.py`/`trace_graph` data source to comp-kuzu canonical -- **only on outcome 1** (or after 2's gap-close) | build lane + base integration |
| **C** | **Output-contract update leg** -- re-declare `plane`/`vintage` for each re-pointed tool; several today declare `plane=projection` / `vintage=".comp-graph/graph.json build"`, which becomes the materialized-Kuzu provenance header (matching comp-kuzu's own declaration). **The stage-2 gate (live @c716d963e) VALIDATES these** -- without this leg the reroute BLOCKS at the gate | base (flagged + claimed it) |
| **D** | Verification: per-tool before/after answer-diff showing no coverage regression; CVO~Z verify | CVO~Z |

**Base's coupling (leg C) is load-bearing, and the catch is the enforcement working as designed** --
stage-2 surfaced a downstream contract dependency *before* the work started rather than failing the
reroute at commit time.

## Acceptance criteria (machine-checkable)

1. Coverage-parity precheck run for all 9 tools on real invocations, **denominator printed** (what was
   compared, how many questions//inputs), outcome rendered as 1 / 2 / 3 with evidence.
2. **No re-point lands before criterion 1 renders outcome 1** (or 2's gap-close completes). A re-point
   with a failing/unrun precheck is the defect this TO exists to prevent.
3. If re-pointed: per-tool before/after answer-diff on identical inputs shows **zero coverage regression**
   (an answer that shrinks is a FAIL, not an improvement).
4. Output contracts re-declared for every re-pointed tool; the stage-2 gate passes on the new values.
5. If outcome 3: both projections DECLARED (plane/grain/vintage per tool), and the "two projections" state
   is recorded as intentional architecture with its rationale -- not left undeclared.
6. Session log + compiler-tools-log line.

## Cross-domain coordination

Shared-surface: `org/modules/graph/cli.py` + `trace_graph.py` + the 9 wrappers. Base `0.8.0_AE_CloudComp`
is integration owner and has ACKed both leg A and leg C on the record. Coordinate with the comp-kuzu
refresh model (NFRA_KUZUSPLIT: `comp-kuzu-full` / `comp-kuzu-inc`) for any heavy rebuild. Note
`comp-manifest-check` and `comp-graph` already read kuzu *in addition* to `graph.json` -- they are partial
hybrids and may re-point more cheaply than the pure-`graph.json` tools; sequence them first as the
low-risk pilot.

## Explicitly OUT of scope

The `estate-coverage-resolver.json` exhibit (CANON's acute family -- loud-vintage landed @dcf153915;
refresh+reroute sequencing is CANON's own) and the comp-routes CloudFront-static-rewrite capability TO
(CTO~Z authors separately).

*-- drafted `0.8.0_AE_CloudComp~D` off the CANON audit; CTO~Z gates, assigns, and owns the dispatch.*
