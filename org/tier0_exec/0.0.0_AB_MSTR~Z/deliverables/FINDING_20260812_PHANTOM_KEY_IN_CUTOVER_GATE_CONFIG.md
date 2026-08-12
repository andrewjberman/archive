# FINDING — a phantom key from a six-week-old GO is live in a config a CUTOVER GATE loads by default

**Raised by:** `0.8.0_AE_CloudComp~Z` (read-only exercise) -> `1.0.0_SA_CTO~Z` -> Andrew via
MSTR~Z. **Nothing acted on. Nothing should be tonight.**

## ⛔ SCOPE BOUND — STATED FIRST, BY THE RAISER, BEFORE IT WAS ASKED FOR

**The live comparators were NOT run. There is NO claim that `comp-parity` produces a wrong
parity result.** The tool is honest on that limb: it reports G1 as RECORDED, static, explicitly
not re-measured, and instructs the reader to re-run the comparators. **What the void does when
they run is UNMEASURED.** Without this bound the finding reads as "the cutover gate is broken,"
which nobody has shown.

## The chain, four hops, each measured

1. A **GO cited a key that never existed**.
2. The key entered `49f_parity_config.yaml:121` (`bd_served`) — **still present today**.
3. `comp-estate` emits it as SERVED (PC-003).
4. `comp-parity` **loads that config BY DEFAULT** and reports `valid: OK`, `rc=0`, plus
   `cutover-jump surfaces (vs BD, informational): 3` — **with the void never named in the
   output** (grep `header_metrics|missing|not found|absent|skip` -> zero hits).

**So `valid` means SCHEMA-SHAPED, not TARGET-RESOLVABLE**, and the surface count silently
includes a surface that can never produce a comparison. That tool's own header calls it the
daily dual-gated proof whose multi-day CLEAN streak is the cutover criterion.

## Why it reaches Andrew

**The propagation path runs through AUTHORIZATIONS, not only through a tool.** A key that never
existed was cited in an approval, landed in a config, and is now counted by the gate that
measures readiness for a cutover — his decision surface.

## The governance half, which is the larger finding

`infra/aws/compdiff/freeze_monitor.py:141` **already records this.** Six weeks ago an agent
grounded every key against live artifacts, **refused the bad one, used the correct one,
documented the discrepancy, and flagged the config drift to COO. They did the work correctly.
Every hop still stands.** The finding is a code comment, doing nothing, while both artifacts it
names remain wrong.

> **A fabric that cannot route a correct finding into a mechanism converts diligence into
> archaeology.** (CTO~Z)

## Disposition (no action taken)

Config edit -> its owning lane. `comp-parity` remedy -> its owner. `0.8.0` has registered
`comp-parity` as a candidate entity for a future instruments run with `valid: OK` as the
verdict-vocabulary cell to open on — the right home, since it is an un-decomposed comp-* verdict
tool squarely in program scope. Two law edits already landed on the tool half (CLAUDE.md Rule
21's `comp-estate` row was actively misclassifying: a served S3 key reads as a "KEY" under its
keys-are-live wording, so a reader applying the rule correctly is directed to the wrong
conclusion; corrected, header warrant scoped to freshness only).
