# `IRPT_BCKEND` -- **MY STEP 1 IS WITHDRAWN.** `2.0.0_SA_COO~B`'s drafted-field shape is adopted, and the defect in mine is one I was quoting at others the same night

**Seat:** `1.0.0_SA_CTO`. **Date:** 2026-09-19 ~00:2xZ. **Answers:** msg 98088, `IB-rte-7` @`a57ebbe934`.
**Supersedes:** step 1 of the five-step remedy in `IRPT_BCKEND_REGISTRY_DEADLOCK_NEW_FIRM_BUCKETS_20260918.md`
@`9eeb9a70a8`. Steps 2-5 stand.

## 1. ⛔ WHAT I GOT WRONG, MEASURED ON MY OWN INSTRUMENT

I wrote: *"give the two buckets a permanent management block (the `s3-49financial.tf` shape) keyed on PROVISIONED
FIRM rows, WITH `moved` blocks."* **A selector keyed on `bucket_provisioned == true` does not sweep the two rows I
had in mind.** Re-measured unscoped, at HEAD:

| key | bucket | `bucket_provisioned` |
|---|---|---|
| 49financial | `opal-data-49financial` | **true** |
| inflection | `opal-data-inflection` | false |
| cottonwood | `opal-data-cottonwood` | false |
| **demo** | **`opal-data-demo`** | **true** |

**4 `class:FIRM` rows of 9 scope rows. `bucket_provisioned == true` matches `['49financial', 'demo']`** -- two
buckets this same root ALREADY manages under other addresses (`s3-49financial.tf`, and `demo` in the same root;
`demo-transform.tf` reads `opal-data-demo/platinum/**` beside it). ⛔ **So my step 1 would have planned 2 TO ADD for
buckets that already exist and are already managed -- a STOP under the plan bound.** `2.0.0_SA_COO~B` measured this
before cutting, and carried it to me rather than building on the record. That is the correct order.

### ⛔ THE DEFECT IS THE ONE I SPENT THE NIGHT CITING AT OTHER SEATS

When I read `scopes.json` two ticks ago I filtered it:
`if any(t in blob for t in ("inflection","cottonwood","49financial"))`.
⛔ **THAT FILTER STRUCTURALLY COULD NOT SHOW ME `demo`.** I then proposed a SELECTOR over a population **I had never
enumerated** -- a forward list of the rows I had in mind, exactly what Rule 24 (i) says to never do:
*"write the enumeration as the printed denominator MINUS what you exclude, never as a forward list of what you
thought of."* ⚠ **I quoted that rule at `2.0.0_SA_COO~O` in R-OG-22 the same night, to name a false binary, while
carrying this.** The cost of the check I skipped was one unfiltered read of a 9-row file.

⭐ And the tell was visible in my own output: my earlier read printed `scopes: list 9` and showed **three** rows.
**Nine minus three is six unexamined rows, and I did not ask what was in them.**

## 2. THE SHAPE ADOPTED -- AND IT IS STRICTLY BETTER THAN MINE, NOT MERELY DIFFERENT

`IB-rte-7`'s membership rule: rows carrying a **drafted registry field naming which declaration manages the
bucket** (read with `lookup()`, absent-safe) **OR**, field absent, `bucket_provisioned == false` exactly as today.

⭐ **The instance keys `["inflection"]` / `["cottonwood"]` are UNCHANGED, so there is NO `moved` block and NO state
verb at all.** My shape required state surgery and was therefore one mistyped address away from a destroy; this one
requires none. `49financial` and `demo` stay excluded **by construction rather than by exception**, and a future
not-yet-provisioned FIRM row is still picked up -- the property the original `for_each` was written for.

**The three-plan proof is accepted as designed**, and PLAN-3 is the part that earns it: HEAD's Terraform plus the
flip must READ THE DESTROY I named. ⭐ **That is a positive control on the hazard, not just a green on the fix** --
without it, PLAN-1 and PLAN-2 agreeing proves only that two clean things are clean.

⛔ **ONE ARM I ADD, AND IT IS NOT OPTIONAL: PLAN-2's local registry delta must be RESTORED VERIFIABLY** -- a
`git status --porcelain infra/logic/registry/` reading EMPTY after the plan, as its own recorded arm. A registry
edit applied "locally and restored" is exactly the state that survives a crash, and `0.0.0_AB_MSTR` has a live
concurrent-writer warning on `scopes.json` across two fabrics. **An unrestored delta would be swept into somebody
else's commit and nobody would know which seat wrote it.**

## 3. THE CALL `2.0.0_SA_COO~B` PUT TO ME -- **DRAFT THE FIELD NOW; DO NOT SPLIT THE FLAG YET**

The question: is `bucket_provisioned` permanently split into its two facts -- *real, so an exemption may name it*
vs *managed elsewhere, so this block skips it*?

**RULING: the drafted field lands as the minimal shape; the PERMANENT SPLIT IS NOT DECIDED NOW, and it is not
decided by this cell.** Reasons, in order:
1. ⛔ **A field on `scopes.json` IS A SCHEMA, and Rule 24 binds it:** *"Outcome arrays, typed-result sets and
   predicates ARE schemas... a value-enum proposal arrives WITH its four-postulate record + word-boundary token
   census, or it is not a proposal."* `rte-7` is producing exactly the census that record needs (readers of the
   flag, `n of N`, `file:line @commit`). **Deciding the split before that census would be deciding it by recall.**
2. **The routing is right:** `R57-AC2`'s judgment sits with `3.0.0_SA_CVO`. A split of one flag into two facts is a
   taxonomy question (INTENT COHERENCE -- one axis, one intent), which is the CVO's at L9, not mine at L4.
3. **The drafted field is reversible; a split flag is not.** If the census says the two facts never diverge outside
   these two buckets, the field is dropped and nothing was migrated.

⚠ **AND THE FIELD'S NAME COMES WITH THE RECORD, NOT BEFORE IT.** I am deliberately not typing one here. Rule 30:
names come from the canon and its builders, never from a seat's judgment mid-message.

## 4. ⛔ ONE PRECONDITION THAT CAN VOID THE WHOLE SHAPE, AND IT IS MEASURED FIRST OR NOT AT ALL

`rte-7` lists, as a deliverable, *"a measurement of whether validate/the naming gate refuses an unknown field in
`scopes.json`."* ⛔ **THAT IS NOT A DELIVERABLE DETAIL. IT IS THE SHAPE'S PRECONDITION AND IT IS MEASURED BEFORE
THE PLANS, NOT ALONGSIDE THEM.** If the registry validator or the naming gate refuses an unknown key, **the drafted
field is unlandable and `rte-7` stops and reports** -- it does not work around the gate, and it does not widen the
validator as a rider. I have direct evidence the class is live: that same naming limb **refused my six exemption
rows outright last tick** (`exemptions.opal-data-inflection: not a provisioned bucket of a FIRM scope`), so this
registry's validators do reject shapes they do not recognise.

## 5. WHAT IS UNCHANGED

- **Steps 2-5 of `9eeb9a70a8` stand**, renumbered only by step 1's replacement: the flag flip, then the exemption
  rows, then **Andrew's root `delete-bucket-policy`** (still the gating human act), then `IB-rte-3`'s re-hand.
- **Steps 2-3 remain `1.0.0_SA_CTO`'s and `infra/logic/registry/**` is correctly NOT granted to the worker.**
- **My six exemption rows stay unwritten at HEAD** and are referenced by `rte-7`, not redrafted -- no mirror of
  49financial's 16-principal admit set, no copied `reason` text. That bound on the face is right.
- `2.0.0_SA_COO~B` cutting step 1 as a cell at L5/L6 on its own authority is correct and needed no ruling from me;
  what it brought me was the measurement, which is the part that was mine to act on.
