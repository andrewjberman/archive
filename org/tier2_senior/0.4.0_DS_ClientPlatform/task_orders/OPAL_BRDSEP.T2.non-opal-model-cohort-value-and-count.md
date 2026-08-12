# Task Order: OPAL_BRDSEP.T2 -- the 18 Cottonwood Strategies, decomposed by constituent Model into Opal vs the balance

> ## ⛔ AMENDED 2026-08-12 ~1930Z -- SCOPE NARROWED AND THE DECOMPOSITION CHANGED. THIS SUPERSEDES v1.
> **v1 specced a three-firm wallet-share sweep (49F + Inflection + Cottonwood, two denominators).
> THAT WAS MY MIS-SPEC, not a change of Andrew's mind** -- I built a broad question out of an
> ambiguous phrase while he was describing one specific structure. v1's 49F cross-check and its
> Eclipse-vs-Orion basis question are **MOOT for T2** (the Inflection basis observation survives as a
> T1 fact). Work already done on the v1 shape: **keep it committed and mark it DESCOPED, do not
> delete it.** Operative spec = the amendment message 20260812T193333Z + this file.

<task_order>
<to_id>OPAL_BRDSEP.T2</to_id>
<title>Full value of the 18 Cottonwood Rebalance Strategies, broken out by constituent Model, split Opal-tagged vs the balance</title>
<issued_to>0.4.0_DS_ClientPlatform~O</issued_to>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued>2026-08-12</issued>
<amended>2026-08-12 ~1930Z (scope narrowed, decomposition restated)</amended>
<status>pending</status>
<phase>INVESTIGATION</phase>
<priority>P1 -- September board update, Andrew-named</priority>
<predecessor>OPAL_BRDSEP.T1 (complete @7a3916acd8; revised @e2991bf495; June figures @e991f93e13, DESCOPED)</predecessor>
</task_order>

## 0. Andrew-direct, VERBATIM

**~1910Z (the descoping + the confirmed asset scope):**
> "the 1.82b number is completely irrelevant, Alyssas numbers do not matter at all and are neither
> rooted to reality nor in scope for our outputs. our interest here is the 0824 schwab total and delta,
> the total of inflection models only, the total of cottonwood models only, as both came in during the
> period, as well as the ETF Float delta that we are aware of. Additionally, I want to get a cohort value
> count on all values in these accounts that are *NOT* contained in an opal model, because we may want to
> include those figures as well somewhere: [the 18 strategies]"

**~1925Z (THE OPERATIVE CLARIFICATION -- this defines the task):**
> "It is specifically for the group of 'Strategies' i sent from the Cottonwood Rebalance endpoint. I want
> to know the full value of those 'Strategies', broken out by its constituent 'Models' of which i want a
> total from anything tagged 'Opal' and the balance of the strategy with anything non-Opal Model."

**The June / $1.82B thread is CLOSED — descoped, not answered.** Do not reconcile it, do not footnote it.

## 1. The shape -- one firm, two levels

**COTTONWOOD ONLY.** 49 Financial and Inflection are **OUT** of T2.

```
LEVEL 1   STRATEGY  (the 18 from the Cottonwood Black Diamond Rebalance endpoint)
            -> full value of each strategy, and the total across all 18

LEVEL 2   CONSTITUENT MODELS inside each strategy
            -> value per constituent model
            -> subtotal: everything TAGGED OPAL
            -> subtotal: THE BALANCE (everything non-Opal)

ASSERT, per strategy and in total:  opal_subtotal + non_opal_subtotal == strategy_total
```

## 2. The 18 Strategies (Andrew's list, verbatim, authoritative)

```
Anna *9237                        Opal Satellite 15
Anna *9238                        Opal Satellite 30
Blended Opal / Satellite 50       Opal Satellite 40
Moderate Income Portfolio         Opal Satellite 50
Opal - Beecherl Legg              Opal Satellite 60
Opal - Cash + Satellite 50        Opal Satellite 70
Opal - Income                     Opal Satellite 80
Opal 66% Long Term / 34% UST      Opal Satellite 98
                                  Opal Ultra Short Term
                                  Opal UST/ Sat 70
```

## 3. ⛔ THE NAME IS NOT THE CLASSIFIER, AT EITHER LEVEL

**The strategy names themselves show why this task exists and why T1's number is not this number.**
Several are explicitly **blends**: `Blended Opal / Satellite 50`, `Opal - Cash + Satellite 50`,
`Opal 66% Long Term / 34% UST`, `Opal UST/ Sat 70`.

- A strategy carrying **"Opal" in its name can hold non-Opal constituents** (UST, cash).
- A strategy **without "Opal" in its name can hold Opal constituents** — measured in T1: `Anna *9237`,
  `Anna *9238`, `Moderate Income Portfolio`.

**Therefore the Opal / non-Opal split CANNOT be derived from the strategy name at either level.** It must
come from constituent-model tagging.

### The definitional question -- ANSWER IT OUT LOUD, DO NOT RESOLVE IT SILENTLY

**What makes a constituent model "tagged Opal"?**
- If the Rebalance endpoint carries a real **tag / attribute field** — use it, and say so.
- If the only available signal is the constituent's **NAME**, you are applying a name heuristic at a
  **second** level — and you have already measured at the strategy level that a name heuristic **drops
  members** (3 of 18 carry no "opal" string) **and invents absences** (4 of 18 false-missing on spacing and
  name variants). **State which signal you used**, and give the count of constituents whose classification
  was **judged** rather than **read**. **Never present a judged classification as a read one.**

## 4. Composition coverage is the likely binding constraint -- and this is what the vendor lift is FOR

T1 measured the composition axis as **name-gated, 29 of 63 landed (46%)**, with AE's 62/62 scan of 08-07 as
the closer. **A within-strategy decomposition needs composition for all 18, not 46%.**

**If our own landing cannot supply it, SPEND THE LIFT.** `cot-BD` (Cottonwood Black Diamond) egress is
**LIFTED and standing** — a live Rebalance sweep is exactly its purpose. You correctly declined it on T1
because our own data sufficed; if it does not suffice here, use it. **Report which source each constituent
came from.** Scope bound: cot-BD only — not bd/49f, not ycharts, not any other vendor.

## 5. Reconciliation against T1 -- REPORT THE DELTA, DO NOT TUNE TO IT

T1 put Cottonwood Opal model AUA at **$136,530,322.99**. Your Opal-tagged constituent subtotal is a
**different cut** of related data and **either direction is informative and neither is a defect**:
- **LOWER** if T1's figure counted Opal-*named* strategies whose constituents are partly non-Opal;
- **HIGHER** if non-Opal-named strategies carry Opal constituents T1 did not reach.

**Report the delta explicitly and explain its direction. Do not adjust one figure toward the other.**

## 6. Deliver

1. Per strategy (18 rows): **strategy total**, **Opal-tagged subtotal**, **non-Opal balance**, each with
   as-of date and source.
2. Per strategy: the **constituent-model breakdown** with per-model values.
3. **Totals across all 18** for the same three columns.
4. The **identity assertion** (`opal + non_opal == total`) reported per strategy and in aggregate — asserted,
   not assumed.
5. The **classification-signal statement** (section 3) and the judged-vs-read count.
6. The **T1 reconciliation** (section 5).
7. **Cottonwood account + client deltas** across the window — carried from T1's open gap.
8. **Denominator on every scan.**

## 7. Hazards -- all measured in T1, all live here

1. **ABSENT IS NOT ZERO.** The balance is a **subtraction**, so an absent minuend produces a **wrong number
   that looks complete**. Check `point_class` before differencing anything. (Load-bearing three times in T1,
   once inside the lane's own arithmetic.)
2. **COVERAGE ONSET PRESENTS AS GROWTH.** Tell = **a COUNT ramping alongside the VALUE**. Apply to every
   count reported here.
3. **A SUBTRACTION STARTS AT ITS WEAKEST INPUT.** `EXISTS IS NOT COMPLETE` — start dates from the
   **producer's declared** first-tracked date, never from where a jump appears to sit.

## 8. `<compiler_tools_mandate>`
Phase 1 `comp-which` routing (ETF vertical is spelled `etf-reports`, per your T1 finding). Phase 2
`.tools/commit-gate.sh` on any `.py`. Phase 3 re-run each headline read. **Determinism: extraction twice,
diffed.** Mutants wherever a classification or framing choice exists.

## 9. `<cross_domain_coordination>`
`platinum/` **READ-ONLY**; `account-distribution.json` is a **LIVE SERVED PORTAL BELL**. cot and bd are
**separate firm pipelines — never mirror or sync.** T2 produces a measurement deliverable and changes no
served artifact.

## 10. `<acceptance_criteria>`

| id | criterion |
|---|---|
| T2-A1 | All 18 strategies reported with strategy total, Opal-tagged subtotal, non-Opal balance. |
| T2-A2 | Constituent-model breakdown delivered per strategy, with per-model values. |
| T2-A3 | Identity `opal + non_opal == total` asserted per strategy AND in aggregate; violations reported, not silently balanced. |
| T2-A4 | Classification signal stated explicitly (tag field vs name heuristic) + count of judged-vs-read constituents. |
| T2-A5 | Source stated per constituent (own landing vs live Rebalance sweep). |
| T2-A6 | Delta against T1's $136,530,322.99 reported with its direction explained. |
| T2-A7 | Cottonwood account + client deltas delivered. |
| T2-A8 | Every count carries the count-ramp check; every scan prints its denominator. |
| T2-A9 | Determinism diff reported. |

## 11. `<proof_of_spec>`
Criterion set **T2-A1..T2-A9**. Fill a `PROOF_OF_SPEC.schema.json` instance from your own efforts; validate
with `.tools/proof-of-spec-check.py` before flipping `complete`. `UNCOMPUTABLE-BY-CONSTRUCTION` /
`UNVERIFIABLE-BY-INSTRUMENT` are available and **preferred over a substituted figure**.

## 12. Not yours to decide -- report, do not adjudicate

Open at Andrew: whether Cottonwood's $136.53M is "growth"; Inflection $0 vs $914,144.89; whether the **5
off-list Opal-named strategies** (T1, across 2 accounts) count as Opal models — **now more load-bearing, not
less, since the same question may recur at the constituent level inside a strategy.**

**Nothing here requires my approval to proceed.** Surprise channel: one line to me, no action, keep working.
