# NFRA_TOOLARCH.CANON -- Tool Data-Source Audit: comp-kuzu canonical vs floating JSON

**Author:** `0.8.0_AE_CloudComp~D` · **Date:** 2026-07-23 · **Status:** P1 AUDIT + exhibit root-cause (design decisions routed to CTO~Z gate)
**TO:** `NFRA_TOOLARCH.CANON` (issued `1.0.0_SA_CTO~Z` @7e0f8005d) · **Verifies:** `3.0.0_SA_CVO~Z` · **Gate (design):** `1.0.0_SA_CTO~Z`
**Constitution:** `docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md` (a per-tool json snapshot is a private denominator that silently drifts -- the s.2 defect)
**Andrew-direct (VERBATIM, in the TO):** *"some of these comp-tools actually rely on floating jsons outside of comp-kuzu canonical which is not acceptable at all."*

---

> ## !! CORRECTION 2026-07-23 ~21:20Z (self-caught during the CANON2 pilot) -- COUNT 12 -> 10, FAMILY 9 -> 7 !!
>
> **Two tools in the `graph.json` family are FALSE POSITIVES of my own mechanical scan, and they were
> BOTH the approved pilot pair -- so the pilot sequencing is VOID and re-selected.**
>
> - **`comp-manifest-check` -- NOT a reader. It is the LINTER THAT ENFORCES THIS VERY RULE.** Its only
>   `graph.json` occurrences are a docstring (`:13`) and a **lint-rule message string** (`:216` -- *"reads
>   graph.json (the trace-graph cache) directly. Query via the cached comp-trace..."*). A targeted grep for
>   `open|json.load|read_text|Path(...graph.json)` returns **zero hits**. My scanner counted the rule TEXT
>   as a data source -- it flagged the enforcement as the violation.
> - **`comp-graph` -- NOT a consumer. It is a status/freshness reporter.** `:151` `gpath = _CACHE_DIR /
>   "graph.json"` is a `stat()` for AGE reporting, done identically for kuzu at `:214-219`
>   (`kuzu.stat().st_mtime`). It must reference BOTH artifacts *by design* -- that is its job.
>
> **CORRECTED NUMBERS:** floating-json set **10 of 84** (was 12); `graph.json` re-point family **7**
> (comp-blast, comp-build, comp-diff, comp-trace, comp-xref via `cli.py`; comp-gitdrill
> `TraceGraph.load` `:60`; comp-surface-check `:453` default) -- all seven ground-verified as genuine.
>
> **WHY THIS HAPPENED, stated plainly:** the audit declared its floating-json set "ground-verified", but I
> verified the shared backing (`cli.py`) and the *material clusters* -- I did **not** verify each tool's
> OWN backing individually. `comp-manifest-check` and `comp-graph` have their own backings and were carried
> on the mechanical signal alone. **That is this program's own defect class committed inside the audit
> diagnosing it: a classification asserted at a coverage its evidence did not reach.** Caught only because
> the CANON2 pilot forced me to read the two tools at source.
>
> **PILOT RE-SELECTED:** `comp-surface-check` is the better first pilot -- it already **parameterizes its
> source** (`--current`, `:830`, defaulting to graph.json), so a re-point is a source-option change rather
> than surgery. `comp-gitdrill` second (single, explicit `TraceGraph.load`). The `cli.py` five move
> together as one change and go last.

## Bottom line

**12 of 84 wrapped comp-tools read a floating-JSON graph/estate projection as a data source, in 3 families
with 3 DIFFERENT severities.** The audit set is DERIVED (every wrapper's backing python scanned + the
projection reads ground-verified at source), not the one Andrew named plus a guess. The exhibit
(pipescript-mdpf stale key) is grounded to a **two-layer** cause: the floating resolver is frozen AND the
canonical kuzu graph is itself stale on the mdpf thread -- so a naive "reroute to kuzu" would NOT fix it.

## Method + denominator

For each of the 84 `comp-*` wrappers (+`pipescript`), resolved the backing python and scanned it for (a)
actual kuzu-canonical use (`import kuzu` / `kuzu_nessie_db` / shelling `comp-kuzu`, NOT a docstring
mention) and (b) every `.json` filename it references, then classified each json as
projection / loud-vintage / config-SoR / arg-like. Reproducible: `deliverables/tool_source_audit.py`.
**Precision note (honest denominator):** the audit is precise on its TARGET -- the floating-json-projection
set is ground-verified at source. The residual 63 tools (inline/util/config/live-AWS) are classified
coarsely by signal; the KUZU-canonical-only count (9) is a conservative floor (the mechanical kuzu-use
regex under-counts helper-mediated reads), not a claim that only 9 tools touch canonical.

| Class | N | Meaning |
|---|---|---|
| **FLOATING-JSON PROJECTION** | **12** | reads a json snapshot substituting for the canonical graph -- **the audit target** |
| LOUD-VINTAGE derived | 6 | reads a derived json but DISCLOSES its age on every number -- the **accepted** exception |
| KUZU-CANONICAL (verified) | 9+ | reads `kuzu_nessie_db` (floor; conservative) |
| inline / util / config / live-AWS | ~57 | grep/gate/util, source-of-record config (EC2_MANIFEST, lambda-source-map), or direct AWS |

---

## The 3 floating-JSON families -- ranked by severity

### Family 1 (ACUTE -- the exhibit): `estate-coverage-resolver.json` -- silently stale, frozen at generation

- **Tools (2):** `comp-pipescript`, `pipescript` (`pipeline_cli.py:1183`, `pipescript_cli.py:44`).
- **Why acute:** the resolver is *generated by `gen-estate-resolver.py` from a FROZEN manifest*
  (`estate-coverage-manifest` @61e91d334) plus hand-written served-key description strings. It carries
  `platinum/mdpf/aggregate_aua_timeseries.json (CloudFront-served, LIVE fresh 2026-06-15 ...)`
  (`estate-coverage-resolver.json:1674`) -- asserted as authoritative with **no vintage disclosure to the
  user**. It is the s.2 defect exactly: intent (what the tool reports) and denominator (the frozen snapshot)
  are the same artifact, so the tool cannot report staleness even when wrong. **This is what mis-scoped the
  MDPF key chase tonight.**

### Family 2 (ARCHITECTURAL, but self-invalidating -- NOT silent drift): `graph.json` -- the trace-graph cache

- **Tools (9):** `comp-blast, comp-build, comp-diff, comp-gitdrill, comp-graph, comp-manifest-check,
  comp-surface-check, comp-trace, comp-xref` (all via `cli.py` / `trace_graph.build_graph`).
- **Why NOT acute:** `graph.json` is a **source-scanned** cache built by `build_graph(_WORKSPACE)`
  (`cli.py:45`), and it is **HEAD-pinned / self-invalidating** -- `cli.py:54` rebuilds on any source-file
  SHA drift, so it never serves stale-vs-source. **The kuzu re-point is a KNOWN, DOCUMENTED deferred
  follow-on** -- `cli.py:56` verbatim: *"the literal Kuzu-projection re-point, is the deferred follow-on."*
  So this family is a **second graph projection separate from kuzu** (the non-uniformity Andrew flagged) but
  it does not silently drift; it answers a *different* question (source-level call/import/dataflow) than
  kuzu's resource graph. Re-pointing it to kuzu is the real "one canonical projection" fix but is a **heavy
  build with a coverage risk** (kuzu must be shown to carry what `trace_graph` provides before the re-point,
  or the structure tools lose coverage -- the census R-0/frontend boundary is the warning).

### Family 3 (UPSTREAM PRODUCER, not a competing reader): `stitch_graph.json`

- **Tools (2):** `comp-stitch-refresh` (PRODUCES it -- `derive_stitch.py`, reads local repo + an AWS-resource
  S3 snapshot), `comp-graph` (reads it). `stitch_graph.json` is an **upstream input to the kuzu build**, not
  a floating substitute read in place of canonical. It matters here because the mdpf staleness *originates*
  in the stitch's source mapping / AWS snapshot (see root-cause below).

### The accepted exception (do NOT reroute): `nerves-risk-edges.json` (6 tools, LOUD-VINTAGE)

`comp-pulse` + the risk-reflex overlay in `comp-blast/build/diff/trace/xref` read `nerves-risk-edges.json`,
but `comp_pulse.py:79` reads it and **SAYS SO on every number** (`"danger map: 20.2h old"`; regenerable via
`nerves_lexical build`). This is the TO's sanctioned pattern -- a derived artifact that is loud about its
vintage, not silently authoritative. **Recommend: keep, unchanged.** It is the model the resolver should
follow.

---

## The exhibit, grounded (scope C: is the tool stale, or the canonical graph?)

**Answer: BOTH -- and the canonical is the deeper cause (case C-ii).** Live-grounded, three surfaces:

| Surface | mdpf aggregate-AUA key | State |
|---|---|---|
| **Live S3** (DE/COO truth, read not re-ruled) | `s3://opal-data-portal-v2/json/mdpf/global/aggregate-aua-timeseries.json` | **EXISTS, fresh 2026-07-23, 242KB** -- the current served rollup |
| **Live S3** (old) | `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua_timeseries.json` | still present, 2026-07-18, 444KB (pre-revamp) |
| **kuzu canonical** | only `platinum/mdpf/aggregate_aua_timeseries.json` (1 node) | **STALE -- has NO node for the current `json/mdpf/global/` key** |
| **estate-coverage-resolver.json** | `platinum/...` asserted *"LIVE fresh 2026-06-15"* | **doubly wrong** -- wrong path AND wrong date (older than the file's own 07-18 mtime) |

**Consequence for the fix:** rerouting `pipescript` to read kuzu is **necessary but INSUFFICIENT** -- kuzu
itself lacks the current key. The canonical mdpf thread must be **refreshed first** (re-index the current
`json/mdpf/global/*` keys + reflect the gold-append/portal-overwrite two-write). That refresh is
graph-derive work in the stitch/AWS-snapshot producer -- **coordinate with the graph-refresh owner; do NOT
hand-edit the canonical projection** (per the TO's coordination mandate).

---

## Recommendations (design decisions -> CTO~Z gate)

1. **Family 1 exhibit -- two-step fix, both coordinated:**
   - **(a) Refresh canonical** so kuzu carries the current `json/mdpf/global/aggregate-aua-timeseries.json`
     node (+ the two-write). Owner: graph-refresh / stitch producer. *This unblocks any reroute.*
   - **(b) Reroute** `pipescript`/`comp-pipescript` served-key facts to derive from canonical, and/or
     **INTERIM**: make the resolver LOUD-VINTAGE (print its generation vintage + a staleness warning on
     every served-key line, the `comp-pulse` pattern) so it stops *silently* asserting a frozen key. The
     interim disclosure is small and in-lane; **I recommend landing it now** to kill the silent-mis-scope
     while (a)+(b) are built. **Gate: your call on interim-disclose-now vs wait-for-reroute.**
2. **Family 2 (`graph.json`, 9 tools) -- the real "one canonical projection" reroute is a SIBLING TO, not
   this one.** It is heavy (source-graph -> kuzu coverage parity must be proven first, or the structure
   tools regress) and the re-point is already tracked as a deferred follow-on (`cli.py:56`). **Recommend: a
   dedicated TO, coordinated with base 0.8.0 (integration owner) + NFRA_KUZUSPLIT refresh model, gated on a
   kuzu-covers-trace_graph parity check.** Not silent drift, so not urgent -- but it IS the structural
   answer to Andrew's "one canonical projection."
3. **Family 3 / stitch:** the fix for the exhibit's canonical-staleness lives here; fold into rec 1(a).
4. **`nerves-risk-edges.json` (loud-vintage):** keep unchanged -- the sanctioned pattern.

## Item D -- comp-routes CloudFront static-rewrite gap: **RECOMMEND SEPARATE TO** (your ruling)

`comp-routes` traces Lambda routes only; the MDPF serve is a CloudFront **static** `/json/*` rewrite (no
Lambda), so no comp-tool gives the full frontend->S3 hop. **Recommend a SEPARATE TO**, because: (i) it is a
comp-routes *capability build* (new CF-static-rewrite modeling), orthogonal to CANON's *data-sourcing*
audit; (ii) it is main-CTO's co-equal item (you noted 195623Z), so a separate TO keeps the two owners
un-entangled; (iii) folding a build into an audit TO blurs the acceptance. It is a real coverage gap
(consistent with my P1 census R-0/serve-plane boundary) and should be named + owned, just not here.

---

## Acceptance-criteria status

1. Floating-json audit, denominator printed, set DERIVED -- **done** (12/84, 3 families, ground-verified).
2. Reroute-or-justify per tool -- **done as recommendations** (routed to gate; `nerves` justified as
   loud-vintage; `graph.json` = sibling TO; resolver = refresh+reroute).
3. Exhibit diagnosed -- **done** (case C-ii, canonical stale, live-grounded); **the FIX is blocked on a
   canonical refresh I must not hand-edit** -- interim loud-vintage disclosure recommended for immediate
   landing; before/after pending the gate ruling on interim-vs-wait.
4. comp-routes CF gap -- **named + recommended SEPARATE TO** (your ruling).
5. Session log + compiler-tools-log -- pending (this session's log).

*-- `0.8.0_AE_CloudComp~D`. Audit reproducible: `deliverables/tool_source_audit.py`; live-S3 + kuzu grounding @2026-07-23 ~20:1xZ (kuzu built 2026-07-23T14:52:37Z, HEAD current).*
