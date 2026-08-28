# TO D1_CATVIEWS.TO-M1-DS — MAP THE DOLLAR VALUES ONTO THE L2 NODES

<id>D1_CATVIEWS.TO-M1-DS.l2-dollar-values-mapped</id>
<decomp_ref>`workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md` — `D1-h-r4` (Custom Models L2 is INCOMPLETE; remedy = registry edit fed by per-Partner composition rulesets), `D1-h-v3` (L2 drill), `D1-inv-4` (view-plane sum). **NO new cell.**</decomp_ref>
<issued_to>DS-class. ⛔ **NO LIVE DS LANE — seating is `0.0.0_AB_MSTR~Z`'s act on Andrew's word.** A TO outlives its seat; this is cut so the work is specified, not because a lane exists.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T15:0xZ</issued>
<status>pending -- CUT, UNSEATED. No executor assigned; no lane is being asked to hold anything.</status>
<priority>P1 — ⛔ **PREREQUISITE FOR `D1_CATVIEWS.TO-S1-DE`.** Shipping the suppression rule first would empty the entire L2 layer.</priority>

<authority>
**ANDREW-DIRECT ~15:0xZ, VERBATIM** (relayed by `3.0.0_SA_CVO~Z`, msg 13251, item 5):
> *"It's there but no dollar values attached need that sorted."*
</authority>

## 1. MEASURED STATE — what he is looking at

Read off his own screenshots by `1.0.0_SA_CTO~Z` (13190):
```
MODELS > PRIMARY  $178.36M   Ultra-Short / Short / Intermediate / Long / Ultra-Long Term   ALL "--"
MODELS > CUSTOM   $8.43M     Opal Global All Equity TR / 50-50 INT-LTC / 50-50 ST-INT /
                             Fixed Income                                                 ALL "--"
```
>> **The L1 parents carry money. Every L2 child carries none.** That is his *"asset value isnt mapped
to them."*

⭐ **LEAD, NOT A SPEC:** the Primary L2 set is the **TERM LADDER** — Ultra-Short / Short / Intermediate
/ Long / Ultra-Long — **the same five books as `MODEL_BOOKS` on Positioning.** ⚠ Do NOT reorder
`MODEL_BOOKS` to make a join convenient: `customBlend.ts:27-41` silently misaligns blended cells on a
reorder. **Read it; do not rearrange it.**

## 2. ACCEPTANCE CRITERIA

| id | criterion |
|---|---|
| `TM1-AC1` | **EVERY L2 node under `Models` carries a dollar value on the SERVED artifact**, for at least one firm. Print key, bucket, byte size and `LastModified` (UTC, `s3api`). ⛔ **From a SCHEDULED run — an ad-hoc artifact is never production evidence.** |
| `TM1-AC2` | ⛔ **THE SUM INVARIANT HOLDS AND IS PRINTED, BOTH PLANES.** `D1-inv-4`: the L2 children sum to their L1 parent, and the rendered L0 set sums to `total_aua − Insurance`. **Recompute both from the served block; assert both; print both.** A mapping that produces values which do not reconcile is worse than `--`. |
| `TM1-AC3` | ⛔ **THE `D1-h-r4` GAP IS DISCLOSED, NEVER PADDED.** Registry Custom = 3 members, all `served=False`; his own example *"Opal Fixed Income"* was **0 hits** at decomp time. **If a model he named is still absent, the panel DISCLOSES it. Do not invent a row to make the set look complete.** |
| `TM1-AC4` | **NO VALUE IS INFERRED.** Every L2 dollar figure is traceable to a producer-side source, cited `file:line @ <commit-ish>`. ⛔ **A derived-by-the-portal number is out of scope and forbidden** — the value belongs in the artifact. |
| `TM1-AC5` | ⛔ **STATE WHAT IS STILL UNMAPPED, IF ANYTHING, AS A COUNT WITH ITS DENOMINATOR.** "All mapped" requires the denominator printed. **An unmapped node that renders `--` after this TO is a FAIL unless it is named and its reason stated.** |

## 3. ⛔ TRAPS — measured today, not hypothetical

- ⛔ **UNMAPPED IS NOT ZERO.** These nodes are **unmapped**, not empty. **A value of 0 asserted for an
  unmapped node is a false frame on a money figure.** The distinction goes in the pipeline's counts.
  ⚠ **It does NOT go on the page** — Andrew ruled the render never tells a client which
  (*"a null is a 0 in this case, if only practically, think about the end user"*).
- ⛔ **DO NOT SHIP `TO-S1-DE` BEFORE THIS.** Suppression against today's data hides the whole L2 layer.
- ⚠ **The producer writes ONCE DAILY at 13:50:50Z** (`opal-assets-mdpf-portal-publisher-daily`).
  Anything landing today is visible **tomorrow at the earliest**. ⛔ **NO AD-HOC PRODUCER RUN.**
- ⚠ **A served-artifact claim names the WRITER, not the trigger.** The gold floor is 13:30Z; the served
  write is the 13:50Z publisher. **They are different clocks and conflating them cost a sovereign look
  today.**

## 4. NOT YOURS
⛔ The **render-side suppression** — that is `TO-S1-DE`, and it is BLOCKED on this.
⛔ The **`predicate_reason` prose** — a separate producer-side item; that row IS populated.
⛔ The **PROD promote** — Andrew's word, **per promote**. No standing authorization.

<proof_of_spec>
  <criterion id="TM1-AC1" cell_refs="D1-h-v3"/>
  <criterion id="TM1-AC2" cell_refs="D1-inv-4"/>
  <criterion id="TM1-AC3" cell_refs="D1-h-r4"/>
  <criterion id="TM1-AC4" cell_refs="D1-h-v3"/>
  <criterion id="TM1-AC5" cell_refs="D1-h-r4"/>
  <expected_criteria>TM1-AC1,TM1-AC2,TM1-AC3,TM1-AC4,TM1-AC5</expected_criteria>
  <alignment_denominators>cells declared: 3 (D1-h-r4, D1-h-v3, D1-inv-4); criteria: 5. FORWARD — 5 of 5 carry >=1 cell_ref. BACKWARD — 3 of 3 reachable (D1-h-v3 from AC1+AC4; D1-inv-4 from AC2; D1-h-r4 from AC3+AC5). Unmapped 0; untraceable 0. NO cell added — this is the value-mapping half of a surface the decomp already declares.</alignment_denominators>
</proof_of_spec>
