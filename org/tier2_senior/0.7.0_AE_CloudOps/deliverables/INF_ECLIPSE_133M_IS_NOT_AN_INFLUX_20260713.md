# INFLECTION ~$133M "MODEL ASSETS" IS **NOT** AN INFLUX OF CAPITAL

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-13 · **Asked by:** Andrew (direct, in-session)
**Question:** *"Inflection appeared with ~133m model assets, up from ~120m I recall. Check the Eclipse
records for the last few days — does anything resemble an influx in capital?"*

> # ANSWER: NO. NOT ONE DOLLAR OF NEW CAPITAL.
> ## It is an INTERNAL RE-MODELING: on **2026-07-10**, **65 existing Inflection accounts (~$11.4M)** were
> ## re-assigned from **Inflection's own in-house `IWM` models** onto **Opal models**.
> ## The money was already at Inflection, already in Eclipse, already managed. **It moved shelves.**

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

## 6. THE HEADLINE FOR ANYONE REPORTING THIS NUMBER

> **"Inflection brought in ~$13M" IS FALSE AND MUST NOT BE SAID.**
> **The true statement:** *"On 2026-07-10 Inflection migrated 65 existing accounts (~$11.4M) from their
> in-house IWM models onto Opal models. The accounts are assigned and queued for rebalance, not yet traded.
> Inflection's total book was flat-to-down on the week. The remaining ~$2M of the 120->133 move is three
> weeks of market drift on the existing book."*

**Zero dollars of new client capital are visible in this data.**
