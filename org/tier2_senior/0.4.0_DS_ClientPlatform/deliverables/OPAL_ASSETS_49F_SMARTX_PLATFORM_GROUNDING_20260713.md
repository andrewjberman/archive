# OPAL_ASSETS -- `49f_smartx_platform`: the $290mm gap, GROUNDED

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** DIAGNOSE
**Requested by:** 0.0.0_AB_MSTR ("the one I want grounded first")
**Routed to:** 1.0.0_SA_CTO~B (architect, OPAL_ASSETS), 0.0.0_AB_MSTR
**Status:** GROUNDED (source + served). **NO CODE CHANGED.** The remedy is a DESIGN decision, not a bug-fix -- see sec 5.

---

## 0. BOTTOM LINE

**The hypothesis was RIGHT IN KIND and WRONG IN MECHANISM, and the mechanism is the part that matters.**

We publish a cohort named **"49F SMArtX (platform)"** whose value is **the 5-term-model sleeve**, not the platform.
The true platform total **is already computed and served in the same JSON block, one key away.**

| | value (as_of 2026-07-06) |
|---|---:|
| what we publish as `49f_smartx_platform` | **$1,400.96mm** <- `model_aua` = the MODEL SLEEVE |
| the platform total, in the SAME served block | **$1,621.25mm** <- `total_aua` |
| **the binding defect (ours, real)** | **$220.29mm** understated |
| residual vs Manav's 1,691.11 **after** that fix | **$69.86mm** -- **STILL OPEN, see sec 4** |
| total gap vs Manav | $290.15mm |

**The $290mm is TWO defects stacked, not one.** Anyone who "fixes" it to match Manav in one move is
laundering the second one.

---

## 1. THE LINE THAT ASSIGNS THE VALUE (Rule 22: `file:line @ commit-ish`)

`infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py:566-567 @ bf7269a1e`

```python
elif vkind == "partner_model_aua":
    val = pb.get("model_aua")
```

The cohort spec that routes there -- `:79-80 @ bf7269a1e`:

```python
{"id": "49f_smartx_platform", "name": "49F SMArtX (platform)", "masters": ["08242234"],
 "vkind": "partner_model_aua", "partner": "49financial"},
```

Provenance string the emitter stamps on the row (`:491-492`): `partners[49financial].model_aua`.
Basis label (`:416`): `partner_platform_view`.

> **A field labelled `partner_platform_view` is bound to a key that is not the platform.**

## 1a. ⚠️ THE SUM-OF-MODELS STORY IS FALSE AT THE EMITTER AND TRUE AT THE PRODUCER

MSTR warned: *"Do NOT let the arithmetic seduce you. 1400.96 ~= 1404.94 is a COINCIDENCE-SHAPED CLUE, not
evidence. Find the LINE that assigns the value."* **That warning was load-bearing and it fired.**

- **The emitter does NOT sum the models.** It reads ONE served field (`:567`). Summing models is a
  *different* vkind -- `partner_model_sum` (`:568-569`) -- used only by `inflection_models`.
- **But `model_aua` IS the 5-term-model sum, at the PRODUCER.** Measured on the served artifact:

```
sum(5 term models) == model_aua        resid -0.01   HOLDS  (float cent)
sum(2 sma models)  == sma_aua          resid +0.00   HOLDS
sum(all 7 by_model)== model_aua+sma_aua resid -0.01  HOLDS
```

**Had I chased the arithmetic I would have "fixed" the emitter -- the wrong file -- and the number would
have moved for the wrong reason.** The numbers agreed for a reason that lived one layer upstream.
*This is the exact class MSTR flagged: an expectation matched to 2dp while measuring the wrong layer.*

---

## 2. WHY `model_aua` IS STRUCTURALLY A SUBSET (producer-side, source-confirmed)

`data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py:22`:

```
"non_model_aua":  [...]   # 1b' = Schwab_total - 1a
```

`non_model_aua` is DEFINED as `Schwab_total - model_aua`. So `model_aua` is a strict component by
construction; the platform total is the sum of the parts. **Confirmed exactly on the served artifact:**

```
model_aua + sma_aua + non_model_aua == total_aua          resid  0.0000   HOLDS
total_aua == partner_custody_total                        resid  0.0000   HOLDS
```

**SERVED 49financial block, `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/2026-07-10.json`
(as_of 2026-07-06, `rolled_forward_partners: {49financial: 2026-07-06}`):**

| key | value | mm |
|---|---:|---:|
| `model_aua` | 1,400,957,639.03 | 1400.96 | <- **what we publish as "platform"** |
| `sma_aua` | 23,380,776.56 | 23.38 |
| `non_model_aua` | 196,913,158.63 | 196.91 |
| **`total_aua`** | **1,621,251,574.22** | **1621.25** | <- **the actual platform total** |
| `partner_custody_total` | 1,621,251,574.22 | 1621.25 |

---

## 3. 🔴 THE SECOND CROSSED NAME -- AND IT IS WHY THIS IS NOT A ONE-LINE FIX

**The platform total is ALREADY PUBLISHED TODAY -- under a different cohort, named after the wrong master.**

Both cohort 8 and cohort 9 read master **08242234** right now (`:76-80 @ bf7269a1e`, `masters: ["08242234"]` on
both). They differ only in WHICH key they take:

| cohort | name it carries | what it ACTUALLY computes today | value |
|---|---|---|---:|
| 8 `49f_schwab_custody` | "49F Schwab custody (**BD**)" | the **SmartX (08242234)** custody TOTAL | **1621.25** |
| 9 `49f_smartx_platform` | "49F **SMArtX** (platform)" | the **model sleeve** of 08242234 | 1400.96 |

Cohort 8 is *intended* to be master **08335338** (`expected_masters`, `:77`) but 08335338 does not flow yet
(that is G2). It therefore currently serves the 08242234 total -- **disclosed** as `incomplete`, correctly.

> **So the number Manav's "49F SMArtX" should be compared against (1621.25) is being served under
> `49f_schwab_custody`, while the cohort actually NAMED `49f_smartx_platform` serves a sleeve.**
> The names describe the INTENDED post-G2 world, not today's computation.

**CONSEQUENCE -- the naive fix is a trap.** Rebinding cohort 9 to `total_aua` today makes cohorts 8 and 9
**numerically identical (1621.25 == 1621.25)** until G2 lands. That is not obviously wrong -- they are
genuinely the same master today -- but it is a design decision with a double-count smell, and it must be
made deliberately, not as a side-effect of closing a variance to Manav.

**AUM HEADLINE IS NOT AT RISK EITHER WAY.** Cohort 9 is **NOT in the additive set**
(`value_class = platform_model_aua`; the additive set is `{49f_schwab_custody, inflection_models}`,
`:392-404`, which reproduces mdpf's certified headline at residual $0.0000 on 427/427 partitions).
**Rebinding cohort 9 does not move Opal's AUM.** It is a reporting/label surface only. *That is the good
news and it is also why nobody caught it: the wrong number was never load-bearing enough to fail a check.*

---

## 4. THE $69.86mm RESIDUAL -- STILL OPEN. DO NOT PAPER IT.

After correcting the binding (1621.25), we are **still $69.86mm below Manav's 1,691.11**.

**I am NOT closing this and I am NOT explaining it away.** Status: `INFERRED`, non-actionable per Rule 22.

**Leading hypothesis (UNPROVEN):** our 49F block is stale. `as_of = 2026-07-06`, and the artifact itself
declares `rolled_forward_partners: {"49financial": "2026-07-06"}` -- this is the known **G1** staleness
(49F feed rolled-forward since 07-06). Manav's sheet is presumably a later vintage. 69.86 / 1621.25 =
**4.3%**, which is a plausible few-days market+flows move -- **and "plausible" is exactly the word that
should stop me from asserting it.**

**MSTR's framing stands and is confirmed:** staleness does NOT explain the $290mm. It may well explain the
$69.86mm remainder. **Those are different claims and I am only making the first one.**

**THE TEST THAT SETTLES IT (needs G1, cannot be run by me today):**
re-read `partners[49financial].total_aua` at a **fresh (non-rolled-forward)** vintage and re-compare to a
Manav figure **of a known matching date**. Two inputs I do not have: (a) an un-staled 49F block, (b) the
as_of of Manav's 1,691.11.
> **I cannot obtain (b) -- the OPAL_ASSETS constraint is strictly internal, no comms to Manav (Andrew-direct).**
> So (b) must come from whoever holds his sheet, with its date. **A number without its as_of cannot close a
> variance** -- that is the same vintage-less-citation error one layer over.

**⛔ AND THE OBVIOUS SHORTCUT IS A DOOR.** The mdpf 49F block is stale because the mdpf chain is *correctly
idle* -- it is event-driven on the INF spine sentinel, and the INF chain is HELD. **Un-staling it by hand
(writing `gold/meta/pipeline-complete.json`) DISPATCHES THE HELD INF CHAIN.** I did not do it, and nobody
should do it to close this variance. **The staleness is a symptom of a deliberate hold, not a bug.**

---

## 5. RECOMMENDATION -- A DECISION FOR CTO~B, NOT A FIX FOR ME

Per MSTR: *"your job is to make the decision legible, not to make the number match Manav's."* Applying that
here, because this is definitional in the same way the ETF `additive` question is.

**The question to settle: what is the cohort `49f_smartx_platform` FOR?**

- **(A) It means "the SmartX 08242234 platform total"** (which is what its NAME says, and what Manav appears
  to mean). -> Rebind to `total_aua` (`:567` -> `pb.get("total_aua")`), change `value_class` to a total
  class, and **accept that it equals cohort 8 until G2 lands.** Closes $220.29mm of the gap. Leaves $69.86mm.
- **(B) It means "the Opal-model sleeve inside SmartX"** (which is what it COMPUTES). -> **Then the name and
  the basis label are the defect.** Rename to `49f_smartx_model_sleeve` / basis `partner_model_sleeve`.
  Number unchanged; **the variance vs Manav is then EXPECTED and explained, not a gap** -- and Manav's
  "49F SMArtX" maps to cohort 8's 1621.25 instead.
- **(C) Both are wanted** -> keep cohort 9 as the sleeve (renamed per B) and add the platform total as its
  own row. Most honest; costs a taxonomy row (the 14-cohort set is Andrew's, so this needs his nod).

**My read (a recommendation, not a ruling): (B) or (C).** The computation is not wrong -- `model_aua` is a
real, wanted, correctly-derived quantity. **The NAME is wrong.** Changing the number to fit the name would
*destroy* a correct quantity to satisfy a label; changing the label preserves both. And per the PRD's own
doctrine (`:133-143`, the `model_value_sum` / `custody_composite` renames): **"A FIELD NAME IS NOT A
SPECIFICATION, AND THESE TWO NAMES DETONATED FOUR TIMES."** This is the fifth detonation of the same class,
in the same file, and the file already knows the lesson.

**Whatever is chosen, cohort 8's name is ALSO wrong today** (sec 3) and should be settled in the same change.

---

## 6. WHAT I DID NOT TOUCH

- **No code changed.** No emitter edit, no rebind, no rename.
- **INF chain: not touched.** No sentinel write, no de-collision, no stamp, no gold run, no trigger.
  The mdpf staleness was *observed and left alone* -- I read the served artifact only (S3 GET, read-only).
- **Frozen files untouched:** `build_assets_dim.py`, `_orion_api_silver_lib.py`, `convert_transactions_to_silver.py`.
- No vendor API called. No spawns.

## 7. GROUNDING (Rule 22a)

| axis | evidence |
|---|---|
| **desired** (source) | `lambda_function.py:566-567,79-80,416,491-492 @ bf7269a1e` (HEAD of that file, `0.8.0_AE_CloudComp`, 2026-07-13T10:32Z); `build_aggregate_aua_timeseries.py:22` |
| **applied** (served) | `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/2026-07-10.json`, 9689 bytes, downloaded + parsed; identities recomputed, resid <= $0.01 |
| **exercised** | The 5 identity checks in sec 1a/2 were RUN against the served bytes, not read off a doc. The two independent sources (my parse + CTO~B's briefing table) agree to the cent on all 8 49F rows. |

**Denominator note:** ONE served partition (2026-07-10) was checked, not all 427. The identities are
structural (they are definitional in the producer) so I expect them to hold estate-wide, **but I did not
measure that** -- `sum(5 term) == model_aua` across the full denominator is UNVERIFIED and I am not
claiming it. *(Per `:392-404`: an exact match on one partition cannot separate two decompositions -- it took
the full denominator to do that. Same caution applies to me.)*
