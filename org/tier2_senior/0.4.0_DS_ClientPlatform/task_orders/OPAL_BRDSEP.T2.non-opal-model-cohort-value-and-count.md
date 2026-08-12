# Task Order: OPAL_BRDSEP.T2 -- the NON-Opal-model cohort, value + count, in the accounts we already serve

<task_order>
<to_id>OPAL_BRDSEP.T2</to_id>
<title>Cohort value + count of everything in the in-scope accounts that is NOT in an Opal model</title>
<issued_to>0.4.0_DS_ClientPlatform~O</issued_to>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued>2026-08-12</issued>
<status>pending</status>
<phase>INVESTIGATION</phase>
<priority>P1 -- September board update, Andrew-named</priority>
<predecessor>OPAL_BRDSEP.T1 (complete @7a3916acd8; revised @e2991bf495, June figures @e991f93e13)</predecessor>
</task_order>

## 0. Andrew-direct, VERBATIM (2026-08-12 ~1910Z, CTO terminal)

> "the 1.82b number is completely irrelevant, Alyssas numbers do not matter at all and are neither rooted
> to reality nor in scope for our outputs. our interest here is the 0824 schwab total and delta, the total
> of inflection models only, the total of cottonwood models only, as both came in during the period, as
> well as the ETF Float delta that we are aware of. Additionally, I want to get a cohort value count on all
> values in these accounts that are *NOT* contained in an opal model, because we may want to include those
> figures as well somewhere: [the 18 strategies, section 3]"

**TWO RULINGS IN THAT PARAGRAPH, and the first one closes work rather than opening it:**

1. **THE JUNE / $1.82B COMPARISON IS DEAD.** Out of scope, not to be reconciled, not to be footnoted. Any
   residual thread chasing what June's headline contained is **CLOSED** -- do not spend on it. The T1
   segment set he enumerates is confirmed as the complete scope of the asset question.
2. **NEW WORK: the NON-Opal-model cohort** -- value AND count -- in the accounts we already serve.

## 1. What this measures, and why it is not a restatement of T1

T1 measured **what is IN Opal models**. This measures **what sits BESIDE them in the same accounts**.

It is a wallet-share question: assets already inside relationships Opal touches, not currently in an Opal
model. That is why he wants it -- **the figure is an opportunity denominator, not an asset claim**, and it
must never be added to the T1 asset base or presented as Opal AUA. Report it as its own quantity.

## 2. The ambiguity in "these accounts", and how to resolve it WITHOUT asking

"These accounts" admits two readings and they give materially different numbers. **Do not pick one. Report
BOTH, per firm, each with its own frame** -- both are cheap once the data is loaded, and the choice is
presentational, which makes it Andrew's:

- **(A) WALLET-SHARE denominator:** accounts holding **at least one** Opal model. Value in those accounts
  not attributable to an Opal model. *(This is the more natural reading of "these accounts" and I expect it
  is the one he means.)*
- **(B) FIRM-WIDE denominator:** all in-scope accounts at the firm, whether or not they hold an Opal model.

## 3. Per-firm definition of "an Opal model" -- these differ, do not generalise across firms

### 3a. 49 Financial -- Schwab account `08242234`
Non-Opal-model value = **entire account** minus **Opal-model value**.
`CTO-NOTE:` T1 already establishes both endpoints on the ruled basis, so the difference is derivable and is
a **cross-check on your own answer, not a substitute for measuring it**: at 2026-08-11, entire
$1,736,948,738.65 minus model $1,451,519,328.79 = **$285,429,409.86**. If your independent measurement
disagrees with that subtraction, the disagreement is the finding -- report it, do not reconcile it away.
Use the FULL 8-digit account form throughout your output.

### 3b. Inflection Wealth Management
Opal models = the **7 `opal_*` models** in `s3://opal-data-portal-v2/platinum/mdpf/inflection/`
(`opal_intermediate`, `opal_blend_5050_int_ltc`, `opal_long_term_conservative`, `opal_blend_5050_st_int`,
`opal_short_term`, `opal_long_term_aggressive`, `opal_ultra_short_term`).
⚠ **Basis hazard, already measured in T1:** the platinum model figure is an **Eclipse-crosswalked** basis
and Orion silver carries $914,144.89 in Opal-NAMED models at Fidelity_Inflection custody that platinum
reads as zero. **State which basis your non-model figure is the complement OF.** A complement inherits its
base's frame.

### 3c. Cottonwood Capital Advisory -- the 18 strategies are the Opal-model definition

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

**CARRY YOUR OWN T1 FINDINGS FORWARD -- both directions bit, and the second bit harder:**
- Three entries carry **no "opal" string** (`Anna *9237`, `Anna *9238`, `Moderate Income Portfolio`), so a
  name scan silently drops them.
- **Exact-string matching INVENTS missing ones** -- you measured **4 of 18** falsely reporting absent
  (leading space on `Anna *9238`; roster spells `Opal Moderate Income Portfolio`; `Opal - Beecherl Legg`;
  `Opal - Income`). Use the same resolution you built in T1; do not re-derive it naively.
- T1 also found **5 Opal-named strategies across 2 accounts NOT on the 18-list**. **A strategy that is
  Opal-composed but off-list is a CLASSIFICATION question, not a silent inclusion or exclusion** -- report
  it in its own line either way and let Andrew rule.

## 4. Deliver, per firm and per denominator (A and B)

| field | note |
|---|---|
| non-Opal-model **VALUE** | with as-of date |
| non-Opal-model **ACCOUNT count** | |
| non-Opal-model **CLIENT count** | |
| the **Opal-model** side of the same denominator | so the split is legible without arithmetic |
| **as-of date + basis** per cell | never a bare number |

**ALSO OWED, carried from T1's open gap:** **Cottonwood account and client deltas** across the window --
T1 delivered these for 49F and Inflection and not for Cottonwood. Same absent-not-zero discipline applies.

## 5. Hazards -- all three MEASURED in T1, all three recur here

1. **ABSENT IS NOT ZERO.** Load-bearing **three times** in T1 (Cottonwood's baseline, the ETF Float
   subtrahend, Inflection's 06-30 point -- the last of which you caught in your OWN arithmetic). A
   complement is a **subtraction**, so an absent minuend silently becomes a fabricated total. Check
   `point_class` before differencing anything.
2. **COVERAGE ONSET PRESENTS AS GROWTH.** Three appearances in T1. **Your own tell is the spec: a COUNT
   ramping alongside the VALUE.** Any count in this TO gets that check.
3. **A QUANTITY DEFINED BY SUBTRACTION STARTS AT ITS WEAKEST INPUT.** Every figure here is a complement.
   `EXISTS IS NOT COMPLETE` -- take start dates from the **producer's declared** first-tracked date, never
   from where a jump appears to sit.

## 6. `<compiler_tools_mandate>`
Phase 1 `comp-which` routing (note: the ETF vertical is spelled `etf-reports`, not `etfs` -- your T1
finding). Phase 2 `.tools/commit-gate.sh` on any `.py`. Phase 3 re-run each headline read.
**Determinism: full extraction twice, diffed.** Mutants where a framing choice exists.

## 7. `<cross_domain_coordination>`
`platinum/` **READ-ONLY**; `account-distribution.json` is a **LIVE SERVED PORTAL BELL**. cot and bd are
**separate firm pipelines -- never mirror or sync**. Cottonwood Black Diamond egress remains **LIFTED**
(cot-BD only); T1 did not need it and you should not spend it unless our own landing is insufficient.

## 8. `<acceptance_criteria>`

| id | criterion |
|---|---|
| T2-A1 | Non-Opal value + account count + client count delivered per firm, under BOTH denominators A and B. |
| T2-A2 | Every cell carries an as-of date and a stated basis. |
| T2-A3 | 49F result cross-checked against the T1 subtraction ($285,429,409.86 at 08-11); agreement or disagreement stated explicitly. |
| T2-A4 | Inflection result names which basis it complements (Eclipse-crosswalked vs Orion-inclusive). |
| T2-A5 | Cottonwood 18-strategy resolution reuses the T1 matcher; on-list-not-found and found-not-on-list both reported. |
| T2-A6 | Off-list Opal-composed strategies reported as their own line, not silently included or excluded. |
| T2-A7 | Cottonwood account + client deltas across the window delivered (the T1 gap). |
| T2-A8 | Every count carries the count-ramp check against coverage onset. |
| T2-A9 | Denominator printed on every scan. Determinism diff reported. |

## 9. `<proof_of_spec>`
Criterion set **T2-A1..T2-A9** minted here. Fill a `PROOF_OF_SPEC.schema.json` instance from your own
efforts; validate with `.tools/proof-of-spec-check.py` before flipping `complete`.
`UNCOMPUTABLE-BY-CONSTRUCTION` / `UNVERIFIABLE-BY-INSTRUMENT` are available and preferred over a
substituted figure.

## 10. Framing calls -- NOT yours, and NOT blocking

Still open at Andrew from T1 and unchanged: whether Cottonwood's $136.53M is "growth"; Inflection
$0 vs $914,144.89. **Do not adjudicate either.** New from this TO: whether off-list Opal-composed
strategies count as Opal models. Report, do not decide.

**Nothing here requires my approval to proceed.** Surprise channel: one line to me, no action, keep working.
