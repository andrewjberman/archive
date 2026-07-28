# HELD WORK -- roster single-sourcing in `mdpf_aggregate_aua.py` (GO CANCELLED 20260728T205052Z)

**Status:** GO **CANCELLED, not deferred** (CTO 205052Z). Reading (1) -- CANONICAL ONLY: the revamp builder
already carries cottonwood (`build_global_artifact(a49, ainf, acot)`, exercised ~15:00Z), so Andrew's
*"Yes, cottonwood should be included"* (2026-07-28T203435Z) is **already satisfied in the canonical
lineage**. **Ruling 1 stands: legacy keeps running, untouched and unfixed.**

**Why this folder exists:** the edits were made and then reverted; the worktree is clean and byte-identical
to HEAD. CTO: *"Keep the patch."* Three findings survive the cancellation and two are live defects.

| file | what it is |
|---|---|
| `mdpf_aggregate_aua.roster-single-source.patch` | 142-line diff, re-appliable. NEVER APPLIED, NEVER COMMITTED. |
| `test_mdpf_aggregate_roster_single_source.py.held` | 8 tests incl. the PARTNER-#4 test + the structural assertion that found finding #1 |

**Why preserved as a patch rather than left in the tree:** this is a SHARED worktree, and CLAUDE.md's own
provenance note records uncommitted work being swept into an unrelated agent's commit twice in 40 minutes
(`6d14f2d15` "test subject"). A dirty tree during a hold risks held work landing under a foreign author with
no GO at all.

---

## FINDING #2 -- LIVE DIVERGENCE AGAINST A SOVEREIGN RULING (the one that survives everything)

```
producer  mdpf_aggregate_aua.py:91   INFLECTION_PARTNER_ONBOARD_DATE = "2026-05-18"
roster    inflection model.value     effective_from = "2026-05-15"
            ruling:        1.0.0_SA_CTO @f642948889 -- Andrew-direct 2026-07-21 VERBATIM
                           "it was 0, 5-15 was the beginning"
            corroboration: eclipse fact_portfolios_full FIRST PARTITION = 2026-05-15 (partition identity)
```
**The private copy has been three days divergent from a sovereign ruling for a week**, corroborated
independently by partition identity. **Not "a duplicated literal" -- the delay fuse in
`docs/doctrine/CONTROLS_OVER_CARE.md` §III-e, already burning, invisible until a structural test looked.**

**It is also why "declared" was insufficient: the producer's value IS declared -- declaratively, locally,
and wrong.**

**Measured impact:** a 3-day historical window (2026-05-15..05-17) in which the legacy sentinel would not
expect inflection, so an absence there could not fire. **Real, bounded, historical.** RECORDED, not patched
-- not worth breaking Ruling 1.

> **ACCEPTANCE CRITERION, inherited by whoever retires or re-points this producer:**
> **the divergence must be resolved TOWARD THE ROSTER, never by "reconciling" the roster to the code.**
> The roster carries the sovereign ruling; the code carries a stale copy.

## FINDING #1 -- a THIRD partner literal. BASIS QUESTION, RULED. Surfaced, deliberately NOT rewired.

```
mdpf_aggregate_aua.py:167   HEADLINE_NONMODEL_FIRMS = ("49financial",)
```
Found by the structural test (`test_producer_restates_no_partner_set`), which a fixture cannot fake away.
Neither the GO nor I had named it -- the GO named two sites, this is a third.

**NOT rewired, on purpose:** it encodes a **BASIS rule** (CTO basis-B, 2026-07-22: the headline non-model
band is 49F-only), not an expectation of *who exists*. Rewiring it inside a wiring GO would be a value
change disguised as a wiring change, on the client-facing number.

**CTO RULING 205052Z:**
- **It must NOT derive from the partner roster.** *"Who exists"* and *"whose non-model counts toward the
  headline"* are different questions; deriving the second from the first would **silently move the headline
  the moment a fourth partner is added.**
- **It should also not stay a bare literal** -- it encodes a ruling with no citation in the file.
- **Interim: annotate the literal in place with its ruling reference, no behavior change.**
  ⚠ **NOT DONE HERE.** That is an edit to the LEGACY producer, which Ruling 1 places out of bounds, and this
  item was just cancelled for exactly that contradiction. **It needs an explicit GO naming it as permitted
  under Ruling 1 (or is CTO's own to land).** Surfaced to CTO 20260728T~2052Z rather than assumed.
- Whether it becomes a declared `fee_scope`/`headline_basis` block is **CTO's design item**, not routed here.

## FINDING #3 -- BLAST RADIUS the GO never mentioned

```
data/mdpf/scripts/backfill/build_mdpf_process_backfill.py:621
    onboard = dt.date.fromisoformat(agg.INFLECTION_PARTNER_ONBOARD_DATE)
```
**A THIRD consumer imports the constant, so it cannot simply be deleted** -- and single-sourcing it to the
roster **silently shifts that backfill's cutoff by three days** (`:618` "NEVER write a date >= onboard").
The held patch **derives the constant and flags the consequence rather than absorbing it.**
**The "harmless" half of a single-sourcing change is the half that moves a backfill boundary.**

## RELATED, from CTO's consumer census (raises what the DDB stall is worth)

`dim_mdpf_aggregate_aua_timeseries.py:330-354` -- the REVAMP builder **reads the legacy-fed DDB**
(`opal-assets-daily-aua`, cohort `49f_schwab_custody`). **Separate on the write path, COUPLED on the read
path.** Its rules handle *absence* honestly (`HONESTLY ABSENT`, never carried forward) but consume a
*present-but-stale* value as *"EXACTLY its value ... no judgment"* -- **so a value-stall propagates into a
sovereign-canonical series.** Does not affect this cancellation (the read is 49F-custody-only); it raises
the value of the 13-cohort stall work. Going to the AE-base successor with the stall.

---

# AE REVIEW OF THE HELD PATCH (0.7.0_AE_CloudOps 20260728T210128Z) -- BOTH FINDINGS ACCEPTED

## F-2 -- the held patch was QUANTITY-BLIND. **FIXED IN THE PATCH, 2026-07-28T~2106Z.**

AE: the `:1132` replacement called `expected_partners_for(date)` and relied on a **default**
`quantity="value"`. **Quantity is exactly what cottonwood's roster row splits** (`model.value`
2026-05-28 vs `model.count` 2026-07-22, `unbackfillable_before`), and `mdpf_roster`'s own docstring
names a collapse as *"recreating the defect in a different shape."*

**Correct, and worse than reported: BOTH call sites under-specified** -- `:742` (pre-existing, which my
patch left untouched) as well as `:1132`. My patch removed the literal and left the *semantic* implicit.

**FIX APPLIED TO THE PRESERVED PATCH -- stronger than "pass it explicitly":**
```python
def expected_partners_for(date: str, leg: str, quantity: str) -> set:   # NO DEFAULTS
...
expected           = expected_partners_for(date, leg="model", quantity="value")   # :742
expected_partners  = expected_partners_for(date, leg="model", quantity="value")   # :1132
```
**Defaults REMOVED entirely, so under-specifying is a `TypeError` at the call site rather than a quiet
choice.** A default that silently picks a semantic is the same shape as a private literal: the decision is
made, locally, invisibly. Both value-bearing sites consume `model_aua`/`sma_aua`/`non_model_aua` blocks, so
`quantity="value"` is the correct binding -- now stated, not assumed.

**Held tests extended to 11 (all passing, exercised against the patched copy):** a `TypeError` test for a
missing `quantity`, one for a missing `leg`, and a **structural `inspect.signature` assertion** that fails
if a default is ever re-added -- because a behavioural test alone still passes if someone restores a default
while the current call sites happen to stay explicit.

**Patch regenerated and dry-run verified to apply cleanly to the repo file. The shared worktree was NEVER
dirtied**: all editing was done on a scratchpad copy of the HEAD blob, since the item is under a hold.

## F-3 -- `build_portal_gold_accrual.py` RUNTIME PRECONDITION. **REAL, and it is mine. Declared, not papered over.**

AE asked (framed as a question, at CTO's instruction, not as an accusation) whether the accrual script can
run on the runner. **Independently re-measured here -- AE's numbers reproduce exactly:**
```
mdpf-daily-dispatch.sh:125  s3 sync s3://opal-data-mdpf/code/scripts/ -> /opt/mdpf/scripts/ --delete
  34 objects under that prefix (AE's count, reproduced)
  only 2 *.json: aggregate_aua_count_backfill_pre0518.json, mdpf_model_registry.json
  partner_roster.json: ABSENT -- and absent BUCKET-WIDE, not just from that prefix
  POSITIVE CONTROL: code/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py present @124,241 B
```
**The answer is yes, it would fail-close on every scheduled run**, and `--delete` would remove any
hand-placed copy on the next dispatch. **P1 ran local/QA and that was correct for P1 (start-forward,
nothing reads the accrual) -- but I never STATED the precondition, and "works in QA, fail-closes in
production" is exactly the undeclared difference that this session has been paying for all day.**

**ACTION TAKEN (`build_portal_gold_accrual.py`, my lane, not the legacy producer -- Ruling 1 not implicated):**
the precondition is now **declared in the docstring with its measurement**, and the fail-closed path emits a
message naming the runtime requirement, the measured absence, the `--delete` hazard, and the owning lane.
**EXERCISED** (a control that has never fired is not a control), with a positive control confirming the
normal path still resolves 4 scopes / 11 objects.

>> **DELIBERATELY NOT FIXED HERE: no S3 fallback, no vendored roster copy.** Publishing the roster into the
   synced prefix is AE's lane. Inventing a second roster-resolution mechanism inside a consumer is the
   duplicate-authority defect this entire thread is about -- it would "fix" the symptom by creating the
   disease one layer down. **Fail-closed with a precise message is the correct behaviour until AE's
   publication lands.** <<

## F-1 (AE's framing, adopted) -- "enroll cottonwood" was a MISNOMER

Cottonwood has been a declared roster partner since 07-24; **the script never ASKS**. So the fix is
**subtraction** (remove the private literals), not addition. **The literal reading of the dispatch -- add
`"cottonwood"` to both sets -- would have added a 4th hardcoded string AND falsely asserted cottonwood
COUNT back to 2026-05-28**, contradicting the `unbackfillable_before: 2026-07-22` bound. The held patch has
the right shape; F-2 was its one gap.

---

## WHAT THIS ITEM DID NOT DO -- do not over-read it

- Does **not** resolve the 13-of-32 gold-DDB value stall.
- Does **not** fix the LABEL defect (a 2-firm number named `opal_aggregate_aua` asserting firm-wide
  completeness; the ~$168.3mm is **two quantities, not a gap** -- 0824/0833 law).
- Does **not** touch the serve, legacy, or any deployed artifact. Nothing was committed or deployed.
