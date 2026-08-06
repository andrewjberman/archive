# MDPF_PROPVALIDATION — state-coherence framing for §6 "Explicit open holes"

**Author:** `0.0.0_AB_MSTR~Z` (site Z) · 2026-08-06
**Addressed:** `1.0.0_SA_CTO~Z` (owns the assessment), `2.0.0_SA_COO~Z` (owns decomposition off it)
**Source pack:** `projects/MDPF_PROPVALIDATION/` (5 docs, CVO-authored read-only review)
**Andrew-direct, this terminal, 2026-08-06:** stand up a dedicated ~Z team for this project; *"The
first step will be assessing what is still unresolved in the unresolved section in the context of the
project and making sure that state coherence is complete, filling in any gaps on that basis and then
diligently executing end to end."*

This document is FRAMING, not the assessment. CTO~Z owns the assessment and may overturn any of it.
What MSTR is fixing here is the **shape** of §6, because the shape is what will mislead an executor.

---

## 1. The test being applied

CLAUDE.md Rule 24 postulate (iv), STATE COHERENCE — the stability frame:

> Name the state axis, then ask whether ONE remedy moves every value together. If building the obvious
> instrument delivers some values and structurally cannot deliver others, the axis is a stability defect
> and YOU MUST NAME WHICH VALUES DO NOT MOVE.

§6 presents ten items (H1–H10) as one flat list under one heading, with one instruction
("do not fill these by assumption") and one disposition ("implementation proof obligations ... recorded
in the deploy ledger"). That framing asserts they are all in the same state.

**They are not.** The obvious remedy — run the Phase 0 probes and censuses — closes five of them and
**structurally cannot close the other five.** Two of those five can never be closed by any amount of
work at all.

---

## 2. The four classes

State axis: **what actually closes this item?**

### Class A — CLOSEABLE BY MEASUREMENT (a probe or census closes it)

| Hole | Closing act |
|---|---|
| H1 | Probe Eclipse + the MDPF-required Assets endpoints at the proposed early hour; prove or refute early-hour equivalence for every row the all-row INF mirror carries. |
| H2 | Actually execute and accept the early SmartX probe (07:45/08:00/08:15 ET). |
| H3 *(source-visible half only — see §3)* | Static import + S3 read/write graph over the real package closure; repo/source-map/Terraform/SSM/portal/Lambda-env sweep. |
| H5 | Build the package; benchmark memory/duration on the built Linux artifact. |
| H8 | Reconstruct deployed publisher provenance from artifact/hash/commit history; correct the source map in the cutover commit. |

These five move together under Phase 0 + Phase 5 step 3. This is the class the plan is built for.

### Class B — AUTHORITY-GATED (no measurement closes it; only Andrew's word does)

| Hole | Why measurement cannot close it |
|---|---|
| H4 | Whether the 08-06 consolidation direction authorizes **terminating** the EC2 instance and deleting EBS — as opposed to removing it from the production route — is a question about the scope of a sovereign instruction. No probe answers it. The doc is correct that the 08-05 ruling did not authorize teardown. |

**Consequence, and this is the actionable half:** H4 must be raised to Andrew **now**, not discovered at
Phase 6 with the team standing at the teardown step. Per the no-inferred-gates rule the team must not
manufacture a hold around it either — the correct handling is *stop/detach after acceptance, execute
everything else, and carry the irreversible act as a named open sovereign item.* The closure template
in §"Final closure statement" already anticipates this with `remaining irreversible teardown item:
<none or H4 exact record>`.

### Class C — STRUCTURALLY UNCLOSEABLE (the instrument cannot see the thing)

| Hole | Why |
|---|---|
| H10 | A source census is blind to an unregistered external or manual reader **by construction**. CloudTrail data events may not be enabled for these buckets; if they are not, the observation does not exist and cannot be created retroactively. |
| H3 *(external half)* | Same blindness, inherited. |

**The honest close is a RECORDED LIMITATION, not a proof** — and the doc already says exactly this
("do not falsely claim mathematical proof of no external reader"). The failure mode to guard is
**silent upgrade**: a zero-reader source census reported at Phase 6 as "proved zero readers." The
ledger row must name the telemetry actually checked, and state plainly that absence of an external
reader is unproven.

### Class D — STANDING CONSTRAINTS, NOT HOLES (they never "close")

| Hole | What it actually is |
|---|---|
| H6 | A **do-not-touch constraint** plus a consumer-contract pin. `as_of_first`/`as_of_last`/`firm_id`/`scope=null` are preserved, not cleaned up, for the whole cutover. |
| H7 | A **standing re-pin obligation** that re-fires at every phase boundary, not once at the start. The tree and the AWS plane both moved *during this session*. |
| H9 | A **ledger-discipline rule** applied continuously: code retention is legal, active-path retention is a no-shadow violation. |

**Why the reclassification matters mechanically: a checklist item gets ticked once; a constraint must
not be.** Leaving these in a list titled "open holes" invites exactly one tick each, after which
nothing re-checks them — and H7 in particular is guaranteed to go stale the moment it is ticked.

---

## 3. Gaps to fill on this basis (the "filling in any gaps" half)

1. **Split H3.** As written it spans two states on one row — a source-visible census (Class A) and an
   external-reader question (Class C) — which is a same-grain violation at row level, the same defect
   one axis down. Two rows, two dispositions, two different closing acts.
2. **Pre-position H4 as a sovereign ask.** Draft it now, surface it now; do not let it surface as a
   Phase 6 blocker. It is the only item on the list whose resolution is not ours to produce.
3. **Convert H10 into a declared limitation with named telemetry**, drafted before Phase 6 so nobody is
   improvising an honesty caveat under deploy pressure.
4. **Lift H6/H7/H9 into a STANDING CONSTRAINTS register** carried in the deploy ledger and re-asserted
   at each phase boundary, out of the open-holes checklist entirely.
5. **State the denominator in the closure statement.** "Open holes closed: N of 10" is a misleading
   statistic across four classes. Report per class, or report 5 Class-A closures plus the explicit
   disposition of the other five.

---

## 4. What is NOT in scope of this framing

- No judgement on the technical correctness of the pack's findings. The two corrections it carries
  (this is not a no-schedule outage; delaying MDPF past 10:16 ET is not a valid fix) read as
  well-grounded and are CTO~Z's to verify, not mine to ratify.
- **No new gate.** Nothing here is an approval step, co-sign, or hold. CLAUDE.md's 2026-08-06
  no-gates rule binds: the classification is an honesty instrument for the ledger, not a checkpoint
  anyone must pass. The pack's own use-discipline says the same — *"REQUIRED PROOF rows are work to
  complete before the production apply; they are not approval gates."*
- No decomposition. Phases 0–6 → TOs is COO~Z's, off the corrected classification.

---

## 5. Standing site-Z conditions the team inherits

- **SITEZ is the execution branch.** Commit to your own lane freely; **push is the integrator's**
  (`0.0.0_AB_MSTR~Z`), taken in the `:55`–`:00` window. Never `git rebase` (NEVER#7).
- **This is a shared worktree with one checkout.** The pack is right that it was heavily dirty; treat
  the scratchpad as the only safe harbour for working files.
- **`comp-freshness` was blind on this device until `2c4510421` today** — it scored every S3 artifact
  `N/A/WARN` and rendered failed retrievals as "prefix not found". Fixed and exercised. If you are
  reading freshness verdicts produced on this box **before** that commit, discard them.
- Site Z coordinates with the laptop over the agentbus only; work is not routed to main-fabric seats
  from here.
