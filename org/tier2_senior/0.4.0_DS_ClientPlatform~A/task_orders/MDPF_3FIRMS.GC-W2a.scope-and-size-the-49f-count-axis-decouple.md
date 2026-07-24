<task_order>
<id>MDPF_3FIRMS.GC-W2a</id>
<title>W-2a — SCOPE AND SIZE the 49F count-axis decouple: the PRIMARY fix for the 40 holes. Plus converge the count_provenance class set with DE before W-4 renders it.</title>
<project>MDPF_3FIRMS</project>
<workstream>Global-Count closeout — THE PRIMARY FIX. Andrew ruled MDPF counts primary through to VALIDATED (~1432Z).</workstream>
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T14:53Z</issued_at>
<status>pending</status>
<authorization>Andrew-direct ~1432Z (MDPF counts PRIMARY, "completing and validating the fix i asked for") -> CTO W-2 ruling @145037Z on your own W-1 data. Scope-bounded to MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT; MDPF_3FIRMS_PRD decomposition REMAINS HELD (LD-0333).</authorization>

<references>
  <ref type="input">YOUR OWN W-1 @b078877020 — the 21-of-22 finding and the `:1656` firm-axis poison ARE the basis of this TO</ref>
  <ref type="ruling">CTO W-2 @145037Z — rejects sum-present-firms as a standalone fix; names the 49F count-axis decouple as PRIMARY</ref>
  <ref type="prd">docs/architecture/MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT.md, amended @eb68497b9 with your corrections</ref>
</references>

<scope>
**YOUR MEASUREMENT CHANGED THE RULING, AND THIS IS THE WORK IT PRODUCED.** CTO pre-framed option (b) —
"sum what is present + carry the basis" — and then REJECTED HIS OWN OPTION on your data: with 49F absent
on 21 of 22 trading-day nulls, summing present firms publishes a 2-firm number beside 3-firm neighbours
and **converts a VISIBLE HOLE into an INVISIBLE BASIS CHANGE.** Your simulation is what proved it (model
axis reproduces the historical 0/94/255 defect exactly; firm axis is worse than an honest null on 15 of 22
dates without a coverage qualifier).

**PART 1 — SCOPE AND SIZE THE 49F COUNT-AXIS DECOUPLE. This is a SCOPING deliverable, not a build.**
CTO: *"Scope it, size it, and tell me what it costs; if it is tractable it is the whole answer for the
holes."* Restoring 49F's count coverage populates those dates **at full 3-firm basis** — a genuinely
smooth, genuinely single-basis line, rather than a fuller chart that is less true.
Answer, concretely:
- **WHAT the decouple actually is.** 49F's own artifact meta names it as the mechanism that retires this.
  Establish what it means in code and data, not from the meta string alone.
- **WHY the 20 legacy-omitted dates are omitted.** Your W-1 marked this INFERRED-and-not-claimed because
  you did not open the upstream import — the artifact self-labels them *"UNCHECKED, not clean."* **That
  open question is now the centre of the primary fix.** Profile it; do not infer it.
- **WHICH of the 22 trading-day holes the decouple would actually fill**, and which would remain. A fix
  that fills 14 of 22 is a different decision from one that fills 22.
- **COST/RISK/BLAST RADIUS**, including whether it touches the value axis or only the count axis.

**PART 2 — JOINT PRECONDITION WITH 0.4.0_DE, AND IT GATES W-4.**
CTO: *"DE and DS~A must converge on the class set BEFORE W-4 renders it, or we will ship a chart that
faithfully displays a mislabel. Flag it as a joint precondition, not a note."*
You found the `exempt_absorbed` COLLISION (18 fallback-labelled dates; 07-20 mis-branched). DE measured
SIX classes on the wire (measured / exempt_absorbed / band_2firm / lag_window / frontier_stamp /
source_absent) and is building a render driven ONLY by that class. **A faithful render of an unreliable
label ships a confident wrong statement.**
Converge with DE directly — do not relay through me — on: which classes are ENUMERATED decisions vs
FALLBACK defaults, what 07-20 should actually be, and whether a fallback-derived label is distinguishable
from an enumerated one at read time. **Agree the class set, then DE renders it.**
</scope>

<explicitly_out_of_scope>
- **BUILDING the decouple.** Part 1 is scope + size + cost at CTO's gate. He decides whether it is tractable.
- **The silent sum-present-firms fix — REJECTED outright by W-2.** Do not build it, and if anyone proposes
  it as a quick win, CTO's words: *"that is the defect with better optics."*
- **The FE.** W-4 is DE's under GC-W45.
- **W-7 axis hygiene** — base DS, now RE-GRADED to correctness on your evidence (@af0295106).
</explicitly_out_of_scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0 corollary 3:
- **Part 1.** *Easiest pass:* report that the decouple "would fix the holes" by citing 49F's meta string,
  which already says so. **The meta is the CLAIM, not the evidence** — that is the same inheritance trap
  W-1's AC-4 named, one artifact over. Size it against what the import actually does.
- **The 20 omitted dates.** *Easiest pass:* carry your own W-1 INFERRED label forward unchanged and call
  the scoping complete. It was correct to mark it INFERRED then; **carrying it forward now would be
  inheriting your own inference**, which is the same defect with a shorter chain.
- **Part 2.** *Easiest pass:* agree a class set with DE by adopting whichever of you states one first.
  Convergence is not agreement — the question is which labels are ENUMERATED and which are FALLBACK, and
  that has a measurable answer.
**MISSING THIRD STATE:** a hole is not `fillable | unfillable`. It is
`fillable-by-decouple | unfillable-and-must-be-labelled | NOT-YET-DETERMINED`. CTO's option (3) — a
labelled partial — exists precisely for the middle state, and only with W-4 live.
</forbidden_shortcuts>

<acceptance_criteria>
1. **A per-date verdict** over the 22 trading-day holes: filled-by-decouple / remains-and-must-be-labelled /
   undetermined. Counts sum to 22, denominator stated.
2. **The 20 legacy-omitted dates PROFILED, not inferred** — a source-confirmed mechanism with
   `file:line @ commit-ish`, or an explicit UNDETERMINED naming what you could not reach and why.
3. **Cost/risk/blast radius** stated plainly enough for CTO to rule tractable-or-not.
4. **A CONVERGED class set agreed with DE in writing**, distinguishing enumerated from fallback labels,
   with 07-20 resolved. Both of you cite the same set.
5. Explicit-Z, denominators printed, served bytes, NEVER#4 (no ad-hoc gold run).
</acceptance_criteria>

<deliverables>
  - The scoping report at `org/tier2_senior/0.4.0_DS_ClientPlatform~A/deliverables/`.
  - The converged class set, referenced by both you and DE.
  - Report to CTO (he gates tractability) + COO. CVO takes validation — write for a verifier, as you did on W-1.
</deliverables>

<notes>
**CTO asked me to tell you directly: your work changed the ruling.** His words — *"That is the highest
compliment available here: it ran first, it was narrow, and it overturned the CTO's stated mechanism inside
half an hour."* The `:1656` firm-axis finding is now the centre of the fix, and the model-cell edit he had
described to Andrew as close-to-simple is retired because you measured instead of confirming.
</notes>
</task_order>
