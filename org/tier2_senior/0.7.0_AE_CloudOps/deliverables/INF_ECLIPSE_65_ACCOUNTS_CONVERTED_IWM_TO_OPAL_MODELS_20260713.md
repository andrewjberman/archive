# THE ~$13M **RISE** IN INFLECTION MODEL ASSETS IS A RE-LABELLING, NOT AN INFLUX

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-13 · **Asked by:** Andrew (direct, in-session)
**Question:** *"Inflection appeared with ~133m model assets, up from ~120m I recall. Check the Eclipse
records for the last few days — does anything resemble an influx in capital?"*

> # ⛔⛔ RETRACTED TWICE. READ THIS BOX, NOT THE ORIGINAL HEADLINE. ⛔⛔
> **v1 headline:** *"the ~$133M IS NOT AN INFLUX"* — **overclaimed** (MSTR, 233737Z).
> **v2 headline:** *"the ~$13M rise is a RE-LABELLING"* — **WRONG AXIS. Andrew corrected it directly**
> (via MSTR, 234542Z). **The filename still carries v2 and is now wrong too. This box is the finding.**
>
> ## THE ERROR: I MEASURED WHETHER **INFLECTION** GREW. NOBODY ASKED THAT. THE QUESTION WAS WHETHER **OPAL** GAINED — AND IT DID.
> ```
> BEFORE (07-09): the 65 sat on IWM models  = INFLECTION WEALTH MANAGEMENT'S OWN IN-HOUSE SHELF.  NOT Opal AUM.
> AFTER  (07-10): the 65 sit on Opal models = OPAL AUM.
> ```
> **VERIFIED ON THE ARTIFACT (2026-07-10):** the book's teams are `Inflection Wealth Management` (821) /
> `Peter Lee` (29) / `Patrick Scanlan` (6), and the non-Opal models are **`IWM Moderate Taxable`,
> `IWM Aggressive Index`, `IWM Moderately Aggressive Tax-Deferred`…** — **`IWM` is the partner's OWN house
> models, i.e. the INCUMBENT WE TOOK THE MONEY FROM. It is not a shelf inside Opal.**
> ## ⇒ **~$11.4M CROSSED FROM A COMPETITOR'S SHELF ONTO OURS. THAT IS OPAL AUM ARRIVING. THAT IS THE BUSINESS WORKING.**
>
> **My control (whole book FLAT) was real, my positive-control was real — and the DENOMINATOR WAS THE WRONG
> ONE.** *"When a slice rises, always measure the whole" — **but the whole of WHAT?** I measured the whole of
> the PARTNER. The subject of the question was OPAL.*
> ### **A RIGOROUS INSTRUMENT POINTED AT THE WRONG AXIS PRODUCES A CONFIDENT, WELL-GROUNDED, WRONG ANSWER — AND IT SURVIVES REVIEW.** *(It survived mine, and MSTR's.)*

> # THE CORRECTED FINDING — ALL THREE CLAUSES, NONE OF THEM ALONE
> ## 1. **OPAL GAINED ~$11.4M OF MODEL AUM.** On 2026-07-10, **65 accounts converted from Inflection's
> ##    in-house `IWM` models onto Opal models.** **REAL. A COMPETITIVE WIN. DO NOT SUPPRESS IT.**
> ## 2. **IT IS NOT NEW CLIENT CAPITAL.** Inflection's total book was **flat-to-down** on the week; **0 new
> ##    portfolios** (856 -> 856); **59 of the 65 accounts were created 2025-08.** ⇒ **A CONVERSION of
> ##    existing relationships — NOT 65 new clients, NOT new deposits.** *Honest and useful. "It didn't
> ##    happen" was not.*
> ## 3. **IT IS ASSIGNED, NOT YET TRADED** (§4). All 65 carry `tradesPending=1`; `lastRebalancedOn` is
> ##    byte-identical across both days. **The $11.4M is REAL — the question is WHEN it counts, not WHETHER
> ##    it exists.** *A TIMING/BASIS defect, not an existence one.* **This is now the primary finding.**

**READ-ONLY INVESTIGATION.** INF chain remains HELD. No gold run, no ad-hoc trigger, no sentinel write,
no guard flipped. Every number below is read from landed bronze artifacts.

---

## 1. THE SERIES (bronze/eclipse/{date}/portfolios_full.json, filter: modelId in the 9 Opal model IDs)

```
date          rows  opal-portfolios  accts       totalValue     managedValue
2026-06-23     855              467    464      122,517,495      119,219,449
2026-06-30     855              472    465      122,509,723      118,970,674
2026-07-02     856              474    467      122,227,270      118,646,505
2026-07-06     856              474    467      122,866,034      119,281,848
2026-07-07     856              474    467      123,562,809      119,964,140
2026-07-08     856              475    468      125,450,227      121,914,654
2026-07-09     856              475    468      125,093,869      121,564,610
2026-07-10     856              540    533      136,859,722     132,747,440   <-- +65 accts / +$11.77M
```

**The `~133m` figure = `managedValue` on 07-10 = $132,747,440.** (`totalValue` = $136.9M. Whoever quotes
this number must say WHICH measure — they differ by $4.1M.)

**Andrew's `~120m` = the documented 06-23 waypoint** ($122.5M total / $119.2M managed).

**FILTER VALIDATED AGAINST AN INDEPENDENT SOURCE (positive control):** my cut reproduces
`data/inf/API/domains/eclipse/DOMAIN.md` §3's CVO-confirmed waypoint **exactly** — spec says
"467 / $122.5M @ 06-23"; I compute **467 / $122,517,495**. The filter was not tuned to fit the answer.

## 2. THE MECHANISM — SOURCE-CONFIRMED ON THE ARTIFACT, NOT INFERRED

Diffing the 07-09 and 07-10 portfolio sets by portfolio `id`:

```
portfolios 07-09: 856   |  07-10: 856      <-- THE BOOK DID NOT GROW
BRAND-NEW portfolio ids on 07-10:      0
portfolio ids that VANISHED:           0
newly ON an Opal model:               65   <-- ALL 65 EXISTED ON 07-09
```

**What model they were on the DAY BEFORE  ->  what they landed ON:**
```
17  IWM Aggressive Index                18  -> Opal Intermediate Growth
10  IWM Moderate Index                  16  -> Opal Long Term
 9  IWM Moderately Aggressive Index     13  -> 50/50 Opal Intermediate/Opal Long Term
 5  IWM Moderate Tax-Deferred           11  -> Opal Short Term
 5  IWM Aggressive Tax-Deferred          7  -> Opal Ultra Long Term
 (+ 19 more across IWM Moderately Conservative / Taxable / Tax-Deferred)
```

**Their value did not change — only their shelf did:**
```
value on 07-09, sitting on IWM models :  $11,346,150
value on 07-10, sitting on Opal models:  $11,400,606
delta                                 :      +$54,456  (+0.48% -- ONE DAY OF MARKET DRIFT)
```

**They are not new accounts. 59 of the 65 were created in 2025-08** (plus 2 in 2025-11, 1 each in 2025-09 /
2025-12 / 2026-02 / 2026-05). **These are year-old accounts.**

## 3. THE CONTROL THAT SETTLES IT — A TRANSFER, NOT AN INFLOW

If new money arrived, the WHOLE Eclipse book rises. If it is internal re-modeling, the Opal slice rises
and the IWM slice falls by the same amount, and the total is flat. **Measured:**

```
                          07-09            07-10          delta
WHOLE BOOK (all 856)   200,311,015      200,956,826      +$0.65M   <-- FLAT (ordinary daily drift)
  Opal slice           125,093,869      136,859,722     +$11.77M
  IWM / other slice     75,217,146       64,097,104     -$11.12M   <-- LOSES WHAT OPAL GAINS
```

> ## **THE OPAL SLICE GAINED ALMOST EXACTLY WHAT THE IWM SLICE LOST. THE TOTAL DID NOT MOVE.**
> ## **THAT IS A TRANSFER BETWEEN SHELVES, NOT CAPITAL ARRIVING AT THE FIRM.**

For the week, the whole book is **DOWN** ($202.5M on 07-06 -> $201.0M on 07-10). **No material new money
entered the Eclipse-managed book at all.**

## 4. >> THE NUANCE THAT MATTERS MOST: THEY ARE ASSIGNED, BUT **NOT YET TRADED** <<

A real re-model leaves trading fingerprints. **These have none — yet:**

```
lastRebalancedOn, the 65 movers, on 07-10:  33x 2026-01-15 · 7x 2026-04-02 · 7x 2026-05-06 · ...
lastRebalancedOn, the SAME 65,   on 07-09:  33x 2026-01-15 · 7x 2026-04-02 · 7x 2026-05-06 · ...
                                            ^^ BYTE-IDENTICAL. NOT REBALANCED.
tradesPending on 07-10:  1  for ALL 65
CONTROL (65 already-Opal accounts):  54 of 65 last rebalanced 2026-07-01  <-- these DO rebalance
```

**So: the 65 have been ASSIGNED to Opal models and are QUEUED FOR REBALANCE, but still physically hold
their old IWM allocations.** Consequences, and they cut both ways:

- **The $11.4M is real and is really assigned to Opal models.** This is a genuine commercial event --
  Inflection is migrating more of its book onto our models. That is the documented pattern (DOMAIN.md §3:
  399/$93.6M @05-18 -> 467/$122.5M @06-23 -> **540/$136.9M @07-10**). **It is good news.**
- **But "Opal model assets = $133M" currently counts $11.4M of accounts whose holdings are still IWM's.**
  If "model assets" means *assigned to an Opal model*, $133M is correct. If it is read as *invested per the
  Opal model*, it is overstated by $11.4M until those trades execute. **Say which you mean.**
- **Expect a burst of trading activity on these 65** when the rebalance runs. That is expected, not an
  anomaly -- do not let it re-alarm someone downstream as a second "event."

## 5. WHAT I DID NOT AND CANNOT ESTABLISH (stated, not blurred)

- **Eclipse is a MODEL-OVERLAY surface, not a custodial ledger.** It shows model assignment + Eclipse's
  intraday valuation. It does **not** carry deposit/withdrawal flows. A capital inflow would still surface
  here as book value growth -- and the whole book is **flat-to-down** on the week -- but I am inferring
  "no deposits" from **absence of value growth**, not reading a cash-flow field. Sharpest test available
  on this surface; not a custodial confirmation.
- **Latest partition = 2026-07-10 (Friday).** Today is **Monday 2026-07-13**, so Friday IS T-1 and the
  partition is **correctly current, NOT stale** (NEVER#1; 07-11/07-12 = weekend, 07-03/07-04 = the July-4
  observance). **Whether the migration continued today is UNKNOWN -- there is no 07-13 partition, and I did
  not and will not trigger a pull to create one.**
- **Eclipse's ~3.4% valuation lag vs Orion EOD is structural** (DOMAIN.md §2: Eclipse `currentValue` is
  rebalance-day intraday; Orion is EOD/T+1-settled). **These numbers will NOT tie exactly to an
  Orion-sourced AUM figure, and forcing them to is a known error.**

## 5b. >> SECOND FINDING: THE NUMBER BEING SPOKEN IS NOT THE NUMBER BEING SERVED <<

Measured on the SERVED artifact (DDB `opal-assets-daily-aua`, read-only):

```
run_date 2026-07-10 · cohort_id inflection_models · cohort_name "Inflection (Opal Models)"
  value         136,859,722.32     <-- my bronze totalValue: 136,859,722.32   EXACT TO THE CENT
                                       managedValue would be 132,747,440 -- IT IS NOT THIS
  value_class   partner_model_total     basis  partner_aua     additive  TRUE
  source_field  sum(partners[inflection].by_model[].model_value)
```

> ## **THE "~133m" IN CIRCULATION IS `managedValue`. THE SYSTEM SERVES `totalValue` = $136.9M.**
> **They differ by $4.1M. Nothing in the artifact declares which is which, so both have been circulating
> under one name — and the spoken one reached the principal.** **Neither figure is quotable without its
> basis: say WHICH, or say NEITHER.**

**AND THE ROW CANNOT CARRY THE TRUTH AS IT STANDS.** `account_count` **ABSENT** (the `etf_*__held_inflection`
rows *do* carry it — 476/478; this one does not) · `trades_pending` **ABSENT** · `value_basis` **ABSENT** ·
and `additive: TRUE`, so it is summed as-is. **The one row that most needs to declare its basis is the one
row with no field to declare it in.** Required (CTO~B, PRD v0.20 `a12e7d0b9`): `value_basis`,
`trades_pending_count`, `trades_pending_value`. **I did NOT touch the emitter — INF is HELD and it is not my
file. Flagging, not fixing. A verified defect is not a licence.**

## 6. THE HEADLINE FOR ANYONE REPORTING THIS NUMBER

> ### ⛔ **MY v1/v2 HEADLINE HERE — *"'Inflection brought in ~$13M' IS FALSE and must not be said"* — IS ITSELF RETRACTED.**
> **It would have SUPPRESSED A REAL WIN.** Opal gained ~$11.4M of model AUM. Saying "that didn't happen" to
> protect against an overstatement is **the opposite error, and it is the more expensive one** — an
> understated win is still a wrong number in front of the principal, and this one argues against our own product.

> # THE TRUE STATEMENT — SAY ALL THREE CLAUSES OR NONE
> *"On 2026-07-10, **Opal gained ~$11.4M of model AUM**: 65 accounts converted from Inflection's in-house
> `IWM` models onto Opal models. This is a **conversion of existing Inflection relationships — not 65 new
> clients and not new deposits** (their total book was flat-to-down; zero new portfolios; 59 of the 65
> accounts date to 2025-08). The accounts are **assigned and queued for rebalance, not yet traded**, so the
> holdings are still IWM allocations until those trades execute. The rest of the 120->133 move is market
> drift on the existing book."*

**Quotable. Bounded. And it does not sell the win short OR oversell it.**
