<task_order>
<id>MDPF_3FIRMS.GC-W2b</id>
<title>W-2b — ESTABLISH WHAT THE SERVED COUNT ACTUALLY COUNTS. Definition-first, read-only. This is a GATE IN FRONT OF the decouple, not a detail inside it. No repoint is authorized until a definition reproduces the served figure EXACTLY.</title>
<project>MDPF_3FIRMS</project>
<workstream>Global-Count closeout — the prerequisite gating the entire FORWARD-LOOKING half.</workstream>
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T15:44Z</issued_at>
<status>staged</status>
<authorization>CTO gate ruling 154238Z on your own GC-W2a tractability verdict: *"the prerequisite is ESTABLISHING WHAT THE SERVED COUNT ACTUALLY COUNTS. That is not a detail inside the decouple, it is a gate in front of it. No repoint is authorized until that definition exists and reproduces the served figure exactly."*</authorization>

<references>
  <ref type="input">YOUR OWN GC-W2a @694175f91 — the 0.04% finding IS the reason this TO exists</ref>
  <ref type="input">GC-W1 @b078877020 (CVO PASS-VALIDATED @6e6c8af47) — the firm-axis poison and the frontier stamp</ref>
</references>

<scope>
**YOUR OWN FINDING CREATED THIS TASK, AND CTO ACCEPTED IT FOR THE REASON YOU GAVE — NOT THE ONE THAT WAS
EASIER.** He ruled the decouple NOT TRACTABLE as scoped, and named the binding reason as **the 0.04%, not
the 0-of-22.** The 0-of-22 only says it is the wrong tool for the collection. The 0.04% says something
worse: the roster **looked like the answer** (right grain, allocation_id + model + advisor, closures
represented, accumulating 8→11 partitions) and **does not reproduce the served count under ANY filter** —
open −3/−13, +workingClose overshoots, all-rows 9,470, T-1 fails, and the producer's constant is ALREADY
`ROSTER_OPEN_STATUS="open"`, so **the intended filter is the one that misses.**

> **−3 on 7,126 is 0.04% — inside every tolerance we own, and the fingerprint instrument is vacuous on 49F
> per the hold record. A repoint would have SHIPPED, PASSED, AND BEEN QUIETLY WRONG.** Not a hole anyone
> could see: a plausible number displacing a correct one, defeating every check we have.

**THE TASK: produce a DEFINITION of the served per-model account count that REPRODUCES THE SERVED FIGURE
EXACTLY.** Not within tolerance. Exactly, or a named, explained residual you can defend per-account.

Answer, concretely:
- **WHICH ACCOUNTS are in the count** — the inclusion predicate, source-confirmed, with `file:line @
  commit-ish`. Funded? open? non-zero sleeve? as-of which instant?
- **WHICH MODEL** an account is attributed to when it holds more than one, and how the per-model figures
  relate to the distinct-account total. (W-1 already measured that the per-model sums exceed the distinct
  count — 442 vs 294 on the cottonwood fold, +147 on the by-model key sums. **That relationship is part of
  the definition, not an anomaly.**)
- **THE RECONCILIATION**: definition applied to a retained source → the served figure, for at least two
  dates on different sides of any basis seam you can identify.

**IF NO DEFINITION REPRODUCES IT, THAT IS THE FINDING** and it is a valuable one — it would mean the served
count is not derivable from anything we retain, which shapes what CTO tells Andrew about the recurring half.
Say so plainly rather than reporting the closest near-miss as a success.
</scope>

<explicitly_out_of_scope>
- **ANY REPOINT, ANY BUILD, ANY PRODUCER CHANGE.** Definition-first, READ-ONLY. CTO's gate is explicit: no
  repoint is authorized until the definition exists and reproduces exactly.
- **The 22-date collection** — dead on capability (~B: both pullers NOT-CAPABLE). Not yours.
- **The vendor question.** Egress is gated and it is not your lane. Denominator = OUR estate, as you scoped
  it last time.
- The render (`0.4.0_DE`, W-4 now cleared to commit) and the Schwab silver roll-forward (`0.6.2~C`).
</explicitly_out_of_scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0 corollary 3 — and this TO's easiest-pass is
**the exact defect it exists to prevent**:
- **THE EASIEST PASS IS TO REPORT THE CLOSEST FILTER AS THE DEFINITION.** `open` at −3 is 0.04% and every
  tolerance we own would accept it. **A near-miss reported as a definition is the 0.04% defect wearing this
  TO's hat.** EXACT, or an explained residual — never "close enough."
- *Easiest pass on attribution:* infer the model-attribution rule from the producer's constant. **The
  constant is what the code INTENDS; the served figure is what it PRODUCED**, and your own finding is that
  they disagree. Ground on the output.
- *Easiest pass on reconciliation:* reconcile ONE date and generalise. **Pick dates on different sides of a
  basis seam** — a definition that reproduces only `measured` dates is not a definition of the served count.
**MISSING THIRD STATE:** the outcome is not `definition-found | definition-not-found`. It is
`reproduces-exactly | reproduces-with-an-explained-residual | NOT-DERIVABLE-FROM-RETAINED-SOURCES` — and the
third is a real, reportable result, not a failure to try harder.
</forbidden_shortcuts>

<acceptance_criteria>
1. **A stated definition** — inclusion predicate + model attribution + as-of semantics — each element carrying
   `file:line @ commit-ish` or the measured evidence it rests on.
2. **EXACT reproduction of the served figure on ≥2 dates on different sides of a basis seam**, or a residual
   explained per-account. Denominators printed.
3. **An explicit verdict** from the three-state set above.
4. The per-model-vs-distinct relationship stated as part of the definition, not left as an anomaly.
5. Read-only affirmed; NEVER#4 (no ad-hoc gold run); explicit-Z throughout.
</acceptance_criteria>

<deliverables>
  - The definition report at `org/tier2_senior/0.4.0_DS_ClientPlatform~A/deliverables/`.
  - To CTO (he gates the decouple on this) + COO. Written for CVO, as you did on W-1.
</deliverables>

<notes>
CTO's words on why this is yours: *"it is exactly their demonstrated strength. If they get it, mechanism (2)
becomes fixable; if they cannot, that is a finding that shapes what we tell Andrew about the recurring half."*
Your open-ended frontier-stamp finding is what made the forward-looking half matter — this is the gate in
front of fixing it.
</notes>
</task_order>
