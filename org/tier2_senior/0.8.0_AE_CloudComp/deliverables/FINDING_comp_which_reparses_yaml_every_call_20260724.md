# FINDING: comp-which re-parses 133KB of YAML on EVERY call — a latency tax on the estate's mandated first reflex

**Author:** 0.8.0_AE_CloudComp~B · **Date:** 2026-07-24 · **To:** 1.0.0_SA_CTO~Z · **Verifies:** 3.0.0_SA_CVO~Z
**Origin:** surfaced by NFRA_TOOLARCH.LATENCY / the self-route gate reassignment. **Stands alone** — it is
not contingent on the gate fix and is directly Andrew's "fast AND reliable" framing on the tool the law
tells everyone to reach for first.

## The finding

`comp-which` **re-parses its two largest YAML inputs on every single invocation, uncached:**
- `_manifest_matches()` at `.tools/comp-which:992` re-reads + `yaml.safe_load`s the **133KB**
  `graph-call-manifest.yaml` (invoked at `:1490` and `:1734`).
- `_load_ledger()` at `.tools/comp-which:1016` re-reads + `yaml.safe_load`s the coverage ledger
  (invoked at `:1072`, `:1093`, `:1762`).

**Measured (cProfile, one warm call, import already paid):**
- `yaml.safe_load` is called **10 times per query**.
- YAML parsing is **~2.87s of a ~2.96s profiled call = ~97% of call time**. (Unprofiled wall-clock is
  ~0.9s/call; the ratio is the load-bearing number, the absolute drifts with profiler overhead.)
- A 65-tool self-route gate run = 65 × 10 = **~650 manifest/ledger parses**.

## Why it is not a test-harness annoyance — it is estate-wide

- **Rule 21 makes `comp-which` the DEFAULT REFLEX** for every search and inspection, for every agent,
  every session: *"comp-which is the DEFAULT for every search + inspection; a raw search is the
  EXCEPTION."*
- `org/mcp/comp-which-rail.log` carries **12,147 `ROUTE-POSTERIOR` events**. At ~0.9s/call that is a
  standing, per-invocation tax on the exact first move the law mandates.
- This is the **latency** half of Andrew's original mechanical framing (*"how the tools get their data
  and it has to be FAST and reliable"*) — the half NFRA_MSBEFF measured reliability and coverage for but
  never measured. It is, per CTO~Z, likely the single most valuable thing LATENCY has produced so far.

## The fix (belongs IN comp-which, lands with Design B)

Memoize both loaders inside `comp-which` — a module-level cache (or `functools.lru_cache`) keyed on the
file path, so the 133KB manifest and the ledger parse **once per process** instead of once per call. This
is an internal caching change, **not** a standard-contract change, so it stays in the comp lane and does
not route to main CTO.

**Packaging (CTO~Z ruling):** the memoization rides in the SAME `comp-which` commit as Design B (bounding
+ killing the nested `:1201` subprocess), because both edit `comp-which` and both must land THROUGH the
now-evaluable self-route gate. That commit does double duty: **bound the hang AND kill the re-parse tax.**

## Measurement discipline note (against my own record)

I initially attributed the self-route member's cost to **interpreter startup + import graph paid 68
times** — and CTO~Z ratified that. It was **wrong**: warm invocation (import paid once) still cost
~0.9s/call, and the cached module fetch is ~1µs. The cost is YAML, re-done per call. I caught this by
**profiling before reporting** rather than by being corrected — the third wrong mechanism I stated this
session, and the first I killed myself. A cost diagnosis stated from plausibility is a hypothesis; a
cProfile is grounding. **The 97% figure is measured, not reasoned.**
