<task_order>
<id>MDPF_3FIRMS.GC-BF0</id>
<title>BF0 — CAPABILITY ASSESSMENT: can each puller feeding the 22 missing trading dates actually TARGET a historical date, and can we VERIFY it pulled that date? Assessment ONLY. No backfill TO issues until this passes CTO's gate.</title>
<project>MDPF_3FIRMS</project>
<workstream>Global-Count closeout — CRITICAL PATH. Andrew ruled MDPF counts PRIMARY through to VALIDATED.</workstream>
<issued_to>0.6.2_AE_PartnerETL~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T14:56Z</issued_at>
<status>staged</status>
<authorization>**ANDREW-DIRECT ~1452Z, VERBATIM** (at CTO's terminal, relayed 145314Z): *"Yeah I think we need TOs targeted at strategic backfill to the extent they are available for the missing dates, contingent on the ability to verify that backfill is pulling the verifiable targeted date. Some pullers may need ad-hoc or adjusted versions from their scheduled form to accomodate specific date targeting, those need to be assessed and validated for capability first."*</authorization>

<references>
  <ref type="input">`0.4.0_DS_ClientPlatform~A` W-1 @b078877020 — **the exact 22 dates and the per-date firm-leg classes are already measured. DO NOT RE-DERIVE THEM.** (49F absent on 21 of 22: A=14 legacy-omitted, B=5 both-legs, E=2 past count_coverage_end; INF on the 22nd.)</ref>
  <ref type="ruling">CTO W-2 @145037Z (superseded as to primary path by Andrew ~1452Z; its REJECTION of sum-present-firms still stands)</ref>
  <ref type="precedent">`0.6.2_AE_PartnerETL~A`, measured 2026-07-24 on the cot tree: `_as_of_for(:291-297)` returns run_date unless `BD_SNAPSHOT_ASOF_LAG_BDAYS > 0`, and `land_to_s3` keys off `end_date` = the as-of — **so each nightly can land exactly ONE as-of: its own run date.**</ref>
</references>

<scope_narrowed authority="ANDREW-DIRECT ~1456Z, relayed by CTO 145636Z" added="2026-07-24T15:00Z">
**READ THIS FIRST — IT NARROWS THE ASSESSMENT TO TWO NAMED SYSTEMS AND REMOVES A THIRD.**
Andrew, VERBATIM: *"Yes so in this case the surfaces in question are fairly small, its SMartX for 49, and
Eclipse for Inflection. We've already established Cottonwood cannot get backfill counts so no need to
explore that at this time."*

```
49F count axis  -> SMARTX      ASSESS   (21 of the 22 trading-day holes)
INF count axis  -> ECLIPSE     ASSESS   ( 1 of the 22: 2026-05-21)
COTTONWOOD      -> OUT OF SCOPE.  ESTABLISHED as incapable of backfill counts.
                   DO NOT ASSESS IT. Do not re-derive the finding. Do not spend
                   a probe confirming what the sovereign says is settled.
```
The A/B/C/D assessment below applies **UNCHANGED** to those two, and **B (fidelity) still governs.**

⚠ **A BOUNDARY THAT REMOVES WORK — DO NOT "FIX" THE PRE-05-28 ERA.** Cottonwood is covered on only
**47 of 447 dates** (`meta.firm_axis_reconciliation`, `cottonwood_covered_first` = 2026-05-28). For the
~400 dates BEFORE 05-28, a 2-firm count is **NOT A DEFECT** — Cottonwood simply was not there. Those are
`measured` and **CORRECT**. Any "gap" you find before 2026-05-28 is the absence of a firm that did not
exist in the data yet.
</scope_narrowed>

<scope>
**THE ORDER IS THE INSTRUCTION.** Andrew said capability is assessed and validated **FIRST**. This TO is
that assessment. **It authorizes NO backfill.** Backfill TOs are authored afterwards, one per capable
puller, gated by CTO.

>> **THE FAILURE MODE ANDREW NAMED BEFORE WE HIT IT — AND WE ALREADY HAVE A MEASURED INSTANCE.**
   A puller that cannot target a date **does not fail loudly.** It pulls its OWN RUN DATE and lands it
   under the key you asked for. That is a backfill that **reports success and silently writes the wrong
   date's data over a gap — worse than the gap it filled.** The cot-tree instance above is exactly this
   shape, in production, found this morning. **ASSUME THE ANSWER IS OFTEN NO.**

**PER PULLER feeding the 22 missing trading dates, assess FOUR things — SOURCE-CONFIRMED, never inferred
from a docstring or from a flag's existence:**

**A. TARGETING** — can it accept an explicit target date at all? Cite the parameter and the line
(`file:line @ commit-ish`). **A flag that EXISTS is not a flag that WORKS** — note whether any caller has
ever exercised it.

**B. FIDELITY — THE LOAD-BEARING ONE.** Run with target date D: does the landed artifact actually contain
**D's data**, verifiable **INDEPENDENTLY of the puller's own claim**? **An artifact stamped D proves the
stamp, not the content.** State what the independent check IS for that specific puller — a content field
carrying the date, a row count that differs by date, a vendor-side as-of, a cross-check against a date we
already hold.
>> **IF THERE IS NO INDEPENDENT CHECK, THE PULLER FAILS B REGARDLESS OF A.** Andrew's word is
   *"verifiable."* Not verified-by-the-thing-being-verified.

**C. AVAILABILITY** — does the upstream source still HAVE D? These go back to **2025-12-24** and vendor
retention is finite. *"To the extent they are available"* is Andrew's qualifier and it is **PER-DATE, not
global.** Expect a partial answer; report the boundary honestly rather than assuming the oldest are
recoverable.

**D. SAFETY** — does an ad-hoc/adjusted run disturb scheduled state, current partitions, or downstream
event chains? **A backfill that re-triggers a live chain is a different incident.** Note especially
anything that could fire a completion signal.
</scope>

<verdict_schema>
Per puller, exactly one: **BACKFILL-CAPABLE** (A+B+C pass) · **NEEDS-ADJUSTED-VERSION** (specify the
change) · **NOT-CAPABLE** (say why) · **DATA-UNAVAILABLE**.
**NO BACKFILL TO WILL ISSUE AGAINST A PULLER THAT HAS NOT PASSED B.**
</verdict_schema>

<explicitly_out_of_scope>
- **ANY BACKFILL.** Assessment only. Do not pull a date "to test it" beyond what an isolated,
  non-destructive capability probe requires — and if a probe writes anything, say so and where.
- **The 49F count-axis decouple** (forward-looking half) — `0.4.0_DS_ClientPlatform~A`, GC-W2a.
- **The FE render** — `0.4.0_DE`, GC-W45.
- **Re-deriving the 22 dates or the firm-leg classes.** W-1 measured them. Use them.

⚠ **SCOPE BOUNDARY ON THE AD-HOC AUTHORIZATION — DO NOT OVER-READ IT.** Andrew authorized ad-hoc or
adjusted **PULLER** runs for targeted backfill. That is **NOT** a relaxation of **NEVER#4** (no ad-hoc
GOLD runs to validate work) — different act, different layer, different purpose. **Nobody may cite this
directive to justify an ad-hoc gold run, and a backfill puller run is not a validation instrument.**
</explicitly_out_of_scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0 corollary 3:
- **B.** *Easiest pass:* run with target D, observe an object at the target key, mark FIDELITY pass.
  **THE OBJECT EXISTING AT THE TARGET KEY IS THE FORBIDDEN EVIDENCE** — it is exactly what a puller that
  ignores the target produces. The check must be able to tell D's data from the run date's data.
- **A.** *Easiest pass:* find a `--date` / `as_of` parameter in a signature and mark TARGETING pass.
  A parameter that is accepted and then overwritten by `_as_of_for()`-style logic reads identical at the
  signature. **Follow it to where the key is built.**
- **C.** *Easiest pass:* check the newest available date and generalise backwards. **Retention boundaries
  are per-date; the oldest dates here are seven months old.**
- **VERDICTS.** *Easiest pass:* mark ambiguous pullers NEEDS-ADJUSTED-VERSION because it sounds
  actionable. If you cannot determine B, the verdict is **NOT-CAPABLE (undetermined)**, not a softer label.
**MISSING THIRD STATE:** a date is not `backfillable | not-backfillable`. It is
`backfillable | unavailable-upstream | CAPABILITY-UNDETERMINED` — and the third is the one that must never
be quietly rounded into the first.
</forbidden_shortcuts>

<acceptance_criteria>
1. **A per-puller table** with A/B/C/D each verdicted and each carrying `file:line @ commit-ish` or the
   exercised evidence. Denominator stated: how many pullers feed the 22 dates, and how many you assessed.
2. **For every puller passing B: the NAMED INDEPENDENT CHECK**, concrete enough that a backfill TO can
   carry it verbatim as an acceptance criterion, and concrete enough that CVO can run it without you.
3. **A per-date availability boundary** across the 22 dates (oldest 2025-12-24) — not a global claim.
4. **Explicit statement of anything a capability probe wrote**, or that nothing was written.
5. Explicit-Z timestamps; NEVER#4 respected and explicitly affirmed.
</acceptance_criteria>

<deliverables>
  - The assessment report at `org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/`.
  - **To CTO — he GATES it before any backfill TO issues.** CC COO.
</deliverables>

<notes>
Register as `0.6.2_AE_PartnerETL~B` — the FULL suffixed serial. `0.6.2_AE_PartnerETL~A` is LIVE and holds
the retry-net verify (SoD) and the D_00 cliff design; **do not take their work and do not collide with
them.** Their `_as_of_for` finding is the pattern you are looking for elsewhere — talk to them directly.
</notes>
</task_order>
