# OPAL_BRDSEP.T1 — Opal asset base by segment, 2026-04-01 → 2026-08-11

**Author:** `0.4.0_DS_ClientPlatform~O` · 2026-08-12
**TO:** `OPAL_BRDSEP.T1` @`cb1a5ab78a` · **Issued by:** `1.0.0_SA_CTO` · **Spec:** Andrew-direct, quoted verbatim in TO §0
**Type:** Measurement deliverable. **Changes no served artifact.** All reads read-only; nothing written under `platinum/`.
**Determinism control (T1-A9):** extraction run twice, output byte-identical across 514 lines.

> **HOW TO READ THIS.** Every figure carries its own as-of date. **The four segments do not share one window** —
> two reach 2026-08-11, two stop at 2026-08-10, and two have no 2026-04-01 baseline at all. That asymmetry is the
> deliverable's main finding, not a footnote. **No single headline growth rate is computed** (per TO §6); §6 below
> gives the segments and the arithmetic to combine them, and the organic-vs-onboarding framing call is Andrew's.

---

## 1. THE ONE-PARAGRAPH ANSWER

Across 2026-04-01 → 2026-08-11 the Opal asset base grew on every segment that can be measured across the whole
window. **49 Financial** — the only segment with clean measured endpoints on both dates — went from
**$1.212B to $1.452B in Opal model assets (+$238.7M, +19.7%)**, and its total custodied base from
**$1.482B to $1.737B (+$254.9M)**. **Inflection Wealth Management** is a genuine near-zero start:
**$0 → $144.98M** of Opal model assets, launching 2026-05-15. **Cottonwood Capital Advisory** stands at
**$136.53M** of Opal model assets, but **has no April-1 baseline in the estate** — its measured history begins
2026-07-20. **ETF Float** — Opal ETF assets not held inside the three managed books — is **$105.98M** at 08-11,
and also has no April-1 baseline. **The two segments without an April-1 baseline are not small:** together they
carry $242.5M at the end of the window, and any "total growth" figure that treats their April-1 value as zero
is overstating growth by an unknown amount that is **at most** those $242.5M and **certainly not zero**.

---

## 2. SEGMENT × {START, END, DELTA} — every cell dated (T1-A1)

**Primary measure = Opal model assets** (the measure Andrew's methodology names for Inflection and Cottonwood).
The 49F total-custody line is shown beneath it because his 1b says *"total AUM"* for that leg.

| Segment | Start | as-of | End | as-of | Delta | Basis |
|---|---:|---|---:|---|---:|---|
| **49 Financial** (Schwab `08242234`) — Opal model AUA | $1,212,782,514.51 | 2026-04-01 | $1,451,519,328.79 | 2026-08-11 | **+$238,736,814.28** (+19.68%) | measured both ends |
| **49 Financial** — total custodied (model + non-model) | $1,482,015,684.99 | 2026-04-01 | $1,736,948,738.65 | 2026-08-11 | **+$254,933,053.66** (+17.20%) | measured both ends |
| **Inflection Wealth Management** — Opal model AUA | $0.00 | 2026-04-01 | $144,978,896.75 | **2026-08-10** | **+$144,978,896.75** | measured both ends; see §4.2 |
| **Cottonwood Capital Advisory** — Opal model AUA | **NO BASELINE** | 2026-04-01 | $136,530,322.99 | **2026-08-10** | **UNCOMPUTABLE** | see §4.3 |
| **ETF Float** | **NO BASELINE** | 2026-04-01 | $105,976,737.76 | 2026-08-11 | **UNCOMPUTABLE** | see §5 |

**Gross Opal-ETF assets** (the quantity ETF Float is derived from, before the managed-book subtraction):

| Cohort | Start | as-of | End | as-of | Delta |
|---|---:|---|---:|---|---:|
| DIVZ + IDVZ (like-for-like) | $380,090,654.30 | 2026-04-01 *(interpolated — §4.1)* | $496,914,800.00 | 2026-08-11 | **+$116,824,145.70** (+30.74%) |
| PFDE + PFOE | **NO BASELINE** | 2026-04-01 | $257,769,042.00 | 2026-08-11 | **UNCOMPUTABLE** |
| **All four Opal ETFs** | — | — | **$754,683,842.00** | 2026-08-11 | — |

> ⛔ **DO NOT SUBTRACT $754,683,842.00 − $380,090,654.30.** That difference (+$374.6M, +98.6%) is arithmetically
> valid and **substantively false**: it counts two ETFs entering our *measurement* as if they entered *existence*.
> PFDE and PFOE were **incepted 2025-12-30**, three months before the window opened. See §4.1.

---

## 3. CLIENT AND ACCOUNT COUNTS (T1-A7)

| Segment | Metric | Start | as-of | End | as-of | Delta |
|---|---|---:|---|---:|---|---:|
| **49 Financial** | Accounts (`fact_acc` dimension) | 6,683 | 2026-04-01 | 7,189 | 2026-08-11 | **+506** |
| **49 Financial** | Accounts (`fact_rps`, position-bearing) | 5,586 | 2026-04-01 | 6,060 | 2026-08-11 | **+474** |
| **49 Financial** | Clients (distinct `ssn_tin_number`) | 4,020 | 2026-04-01 | 4,268 | 2026-08-11 | **+248** |
| **Inflection** | Accounts in Opal models (platinum) | 0 | 2026-04-01 | 548 | 2026-08-10 | **+548** |
| **Inflection** | Accounts in Opal-named models (Orion silver) | 17 | 2026-04-01 | 600 | 2026-08-11 | **+583** |
| **Inflection** | Clients in Opal-named models (Orion silver) | 4 | 2026-04-01 | 266 | 2026-08-11 | **+262** |
| **Inflection** | Firm-wide accounts / clients | 880 / 311 | 2026-04-01 | 948 / 318 | 2026-08-11 | +68 / +7 |
| **Cottonwood** | Accounts | **NO BASELINE** | 2026-04-01 | 314 | 2026-08-10 | **UNCOMPUTABLE** |
| **ETF Float** | — | *n/a — float is a dollar residual, not an account cohort* | | | | |

**Two account numbers for 49F, deliberately.** `fact_acc` is the account *dimension* (every open account);
`fact_rps` counts accounts *holding positions* that day. Neither is wrong; they answer different questions and
differ by ~1,100. The dimension count is the one to quote for "number of accounts".

⛔ **Cottonwood `account_count` must never be totalled across models.** The producer's own note:
*"account_count is per-model and fans out +1 per underlying model on a blend; summing it across models
double-counts (447 vs 296 on 2026-07-22)."* The 314 above is the artifact's own cross-section total, not a sum.

---

## 4. THE THREE HAZARDS, AND WHAT MEASUREMENT DID TO THEM

### 4.1 ETF April-1 baseline — **PARTLY RESOLVED, and it split into two different answers per ticker** (T1-A2)

CTO's issuance recorded *"no source under `opal-data-etfs` reaches 2026-04-01"* and named four prefixes.
**A fifth prefix does reach it.** `silver/netassets/` is a date-partitioned series of **353 partitions spanning
2025-05-30 → 2026-08-11** — it covers both window endpoints. The pre-issuance enumeration saw
`silver/holdings/` (60 partitions, from 2026-05-18) and not its sibling.

That does not make the baseline simply "available". Per ticker:

| Ticker | 2026-04-01 value | Nature of that value | Genuine observations |
|---|---:|---|---|
| DIVZ | $229,314,418.64 | **INTERPOLATED** (`inferred=True`, `msn_anchored_interpolated`) | 73 of 353 dates |
| IDVZ | $150,776,235.66 | **INTERPOLATED** (same) | 73 of 353 dates |
| PFDE | — | **ABSENT** | 60 of 60 (all issuer-reported, from 2026-05-18) |
| PFOE | — | **ABSENT** | 60 of 60 (same) |

**DIVZ/IDVZ — the interpolation is anchored, and a stronger figure exists.** The series carries genuine
issuer-reported **month-end anchors**, and one sits one day before the window start:

> **2026-03-31 issuer month-end: DIVZ $231,767,565.96 + IDVZ $149,894,362.78 = $381,661,928.74.**

That is a measured number one calendar day off the window start, against the interpolated 04-01 figure of
$380,090,654.30 — a 0.41% difference. **Recommendation: quote the 03-31 anchored figure for any board-facing
ETF baseline** and state the date; it is a measurement rather than a reconstruction.

**PFDE/PFOE — `UNCOMPUTABLE-BY-CONSTRUCTION`, with a mechanism, not a shrug.** These are Pathfinder funds
(not TrueShares), **incepted 2025-12-30**, so they *existed* on 2026-04-01 and hold $257,769,042.00 by 08-11.
Their absence from our April-1 data is a **coverage onset (2026-05-18), not a launch**. The estate identified an
issuer historical file — `FilepointOpalCap.40O6.O6_DailyNAVHistorical.csv`, from inception — but it
**carries NAV and market price only, with no `Net Assets` and no `Shares Outstanding`**, and the probe computes
net assets as `nav × shares`. So historical net assets cannot be reconstructed exactly from the one source that
reaches back, and the recommendation on record was to start the true series at first probe — which is what
happened. *(Source-grounded: `docs/briefs/mdpf-pfde-pfoe-etf-netassets-feasibility-20260518.md:23-24,60,84`.)*

**Reaching further would require a vendor-egress call to `pathfinderetfs.com`, which I do not hold** — the
standing lift is Cottonwood Black Diamond only. Flagged, not attempted. Even with it, the field needed does not
exist in the historical file.

### 4.2 Inflection's zero — **CONFIRMED, and it is basis-scoped, which matters at the margin** (T1-A4)

CTO's pre-grounding reproduces exactly: 2026-04-01 model AUA **$0.00**, accounts **0**, `count_basis=measured`;
last zero 2026-05-14, first non-zero 2026-05-15; the artifact declares a clean launch step
(`launch_seam: {date_pre: 2026-05-14, launch: 2026-05-15, model_pre: 0.0, clean_step: true}`).

**A second in-estate source disagrees at small magnitude, and the disagreement is real.** Orion silver
`fact_positions` for 2026-04-01 carries **402 rows across 17 accounts and 4 clients in Opal-*named* models**
(Opal Intermediate Growth, Opal Long Term, Opal Short Term, Opal Ultra Short Term), all `isManaged=True`,
custodian `Fidelity_Inflection`, totalling **$914,144.89**.

**Both are correct about different things, and the platinum figure is not wrong.** Platinum `model_aua` is the
**Eclipse-crosswalked** model basis, which genuinely begins at the 2026-05-15 launch. The Orion rows are
**Orion-side display names** at a different custodian. So:

> **Inflection's "0 → $144.98M" is a true statement about the Opal model programme. It is not a statement that
> Opal-named assets at Inflection were zero on 2026-04-01 — those were $914,144.89, or 0.63% of the segment's
> end value.** If the board framing is "assets we did not have in April", the $0.91M belongs as a deduction or a
> footnote; if it is "the Inflection model programme", $0 is right.

I am **not** adjudicating which framing is wanted — TO §6 reserves that to Andrew.

### 4.3 Cottonwood — **the 18-name reconciliation is clean; the April-1 baseline is not** (T1-A5)

**Two-set reconciliation against the live sweep, both sets reported:**

- **ON-LIST-NOT-FOUND: EMPTY.** All 18 of Andrew's strategies resolve on today's roster.
  Several required normalization: **"Moderate Income Portfolio"** appears on the roster as
  **"Opal Moderate Income Portfolio"**, and **"Anna \*9238"** carries a **leading space** in the roster name.
  **Measured, not estimated: an exact-string reconciliation reports 4 of the 18 as missing** — `Anna *9238`,
  `Moderate Income Portfolio`, `Opal - Beecherl Legg`, `Opal - Income` — all four of which are present.
  The normalization step is load-bearing; see the mutant in §12.
- **FOUND-NOT-ON-LIST (Opal-named, not among the 18): 5 strategies, 2 accounts.**

| Strategy | Accounts |
|---|---:|
| Opal Hendrickson LT/UST | 1 |
| Opal Sat 50+ 15% cash | 1 |
| Opal Long Term Aggressive | 0 |
| Opal Long Term Conservative | 0 |
| Opal Satellite 90 | 0 |

**Denominators:** Andrew's list = 18. Roster = **63** strategies (`totalResultCount` 63, single page, 63 rows read
— not a page of a larger set). Roster Opal-named total = 21. Accounts on the 18 matched = **322**.

**The superset check has a structural limit I am stating rather than papering over.** The daily producer pulls
composition under `MODEL_DETAIL_SCOPE=opal_closure`, which **seeds only on strategies whose name contains
"opal"** and walks downward — so a strategy holding an Opal model *without* an Opal name is invisible to it.
Today's landing carries composition for **29 of 63** strategies (46%). **Therefore my "found-not-on-list" set is
complete for *name*-based discovery and cannot be complete for *composition*-based discovery from bronze alone.**

That gap was independently closed 5 days ago by a full 62/62 live composition sweep
(`org/tier2_senior/0.7.0_AE_CloudOps/deliverables/BD_REBALANCER_OPAL_COMPOSITION_SCAN_20260807.md`), which found
**22 Opal-touching strategies / 308 accounts**, and the only non-Opal-named Opal-composed strategies it found
were **Anna \*9237 and Anna \*9238 — both already on Andrew's 18.** Andrew's list is, on that evidence, complete
on the composition axis as of 2026-08-07.

**On the "live current sweep" instruction:** the estate's own `cot-rebalancer-runner` pulls
`rebalancer.bdreporting.com` daily and landed **today, 2026-08-12 02:00Z**. I reconciled against that landing
rather than issuing a duplicate vendor call — same endpoint, same day, and it is the sanctioned raw-vendor path.
The 08-07 independent live scan corroborates the bronze with zero drift.

**Cottonwood's April-1 baseline does not exist.** `point_class` is `absent` at 2026-04-01 —
**absent, not zero.** The artifact declares `first_tracked_date: 2026-07-20` with only **12 measured dates**
(2026-07-20 → 2026-08-10) out of 451, and the sanctioned interpolated backfill reaches only back to 2026-05-28.
**Cottonwood was a Black Diamond client well before April 2026** — this is a coverage onset, exactly as with
PFDE/PFOE, and its April-1 Opal model AUA is `UNCOMPUTABLE-BY-CONSTRUCTION` from the estate.

---

## 5. ETF FLOAT — the subtraction, stated per firm (T1-A6)

`ETF Float = gross Opal-ETF net assets − all firm-specific holdings of those ETFs`

| Component | DIVZ | IDVZ | PFDE | PFOE | Total | as-of |
|---|---:|---:|---:|---:|---:|---|
| **Gross ETF net assets** | 298,966,800.00 | 197,948,000.00 | 164,376,380.00 | 93,392,662.00 | **754,683,842.00** | 2026-08-11 |
| − 49 Financial | 184,265,487.96 | 154,869,907.93 | 133,069,694.91 | 71,924,619.00 | −544,129,709.80 | 2026-08-11 |
| − Inflection | 18,643,253.86 | 14,660,883.13 | 12,327,918.02 | 6,937,900.73 | −52,569,955.74 | 2026-08-11 ⚠ |
| − Cottonwood | 17,860,264.77 | 14,972,326.70 | 12,172,844.14 | 7,002,003.09 | −52,007,438.70 | **2026-08-10** |
| **= ETF Float** | | | | | **$105,976,737.76** | mixed, see above |

**Total subtrahend $648,707,104.24 — i.e. 86.0% of all Opal ETF assets sit inside the three managed books,**
and the float is the remaining 14.0%.

⚠ **Inflection's 08-11 ownership values are identical to the cent, on all four tickers, to its 08-10 values**,
while the underlying ETF NAVs moved between those dates. That is a **carry-forward signature**, not market
stasis. The file names `holdings_2026-08-11.parquet` as its source. I did not chase it (out of mandate) —
**surfaced to CTO.** Effect is bounded: it can only shift the float by Inflection's one-day drift, order $0.1M.

**ETF Float has no April-1 value.** The per-firm ownership dailies begin **2026-05-01** (49F, Inflection) and
**2026-06-08** (Cottonwood). With no subtrahend before May, the float's April-1 value is
`UNCOMPUTABLE-BY-CONSTRUCTION` — not zero.

---

## 6. THE ARITHMETIC TO COMBINE (no single headline rate — TO §6)

**Segments that support a full-window delta:**

```
49 Financial, Opal model AUA        +$238,736,814.28   (04-01 -> 08-11, both measured)
Inflection,   Opal model AUA        +$144,978,896.75   (04-01 -> 08-10, 0 -> X)
                                    ----------------
Full-window measured growth          +$383,715,711.03
```

**Segments that do NOT support a full-window delta — end values only, April-1 baseline absent:**

```
Cottonwood, Opal model AUA           $136,530,322.99   as-of 2026-08-10
ETF Float                            $105,976,737.76   as-of 2026-08-11
                                    ----------------
End-value, growth UNATTRIBUTED       $242,507,060.75
```

**If the framing is "total Opal asset base at the end of the window":**

```
49 Financial   Opal model AUA        $1,451,519,328.79   2026-08-11
Inflection     Opal model AUA          $144,978,896.75   2026-08-10
Cottonwood     Opal model AUA          $136,530,322.99   2026-08-10
ETF Float                              $105,976,737.76   2026-08-11
                                     ------------------
TOTAL OPAL ASSET BASE                $1,839,005,286.29   mixed as-of 08-10/08-11
```

**Three framing choices are live and all three are Andrew's, not mine:**
1. **49F on model AUA or total custody?** Using total custody raises 49F by $285.4M at the end and the
   full-window delta by $16.2M.
2. **Is Cottonwood's $136.5M "growth"?** It is new *to our measurement*. It is almost certainly not new
   *to Opal* — treating it as in-window growth is the same error as the PFDE/PFOE ETF trap.
3. **Does Inflection start at $0 or at $0.91M?** (§4.2.)

---

## 7. ASSUMPTIONS, GAPS AND DECLARED EXCLUSIONS

| # | Item | Status |
|---|---|---|
| 1 | **49F account = `08242234`** (MDPF Model Portfolios), Andrew-**CONFIRMED** 2026-08-12 ~1820Z. Full 8 digits used throughout; zero bare 4-digit forms. | RESOLVED |
| 2 | **ETF April-1 baseline** — DIVZ/IDVZ available (interpolated; better anchor at 2026-03-31). PFDE/PFOE unreconstructible. | PART-RESOLVED / PART-`UNCOMPUTABLE` |
| 3 | **Inflection endpoint is 2026-08-10, not 08-11** — the artifact's `as_of_last`. Not relabelled. | DECLARED |
| 4 | **Cottonwood endpoint is 2026-08-10**, and it has **no April-1 baseline**. | DECLARED |
| 5 | **Cottonwood two-set reconciliation** — both sets reported; composition axis limited by name-gating, closed by the 08-07 full scan. | RESOLVED w/ stated limit |
| 6 | **49F client count uses `ssn_tin_number`** as the client key — a taxpayer-identifier proxy for household. Counts only; no values read or stored. | ASSUMPTION, stated |
| 7 | **Inflection 08-11 ETF ownership appears carried forward** from 08-10. | SURFACED to CTO, not chased |
| 8 | **Vendor egress not exercised.** Cottonwood BD reconciled via our own daily landing (today 02:00Z) + the 08-07 live scan. No `pathfinderetfs.com` call — no lift held. | DECLARED EXCLUSION |
| 9 | **No single headline growth rate computed**, per TO §6. | DECLARED EXCLUSION |
| 10 | **Nothing written under `platinum/`.** All platinum reads read-only; `account-distribution.json` untouched. | CONFIRMED |

---

## 8. DENOMINATORS FOR EVERY SCAN REASONED FROM (T1-A8)

| Scan | Denominator |
|---|---|
| `opal-data-etfs` full enumeration | 695 objects (silver 414 / daily 205 / snapshots 61 / platinum 13 / config 1 / csv 1) |
| ETF net-assets series | 353 partitions, 826 rows, 353 distinct dates, 2025-05-30 → 2026-08-11 |
| ETF genuine observations | DIVZ 73 of 353 · IDVZ 73 of 353 · PFDE 60 of 60 · PFOE 60 of 60 |
| Cottonwood BD roster | 63 of 63 (`totalResultCount`=63, `pageCount`=1) — full listing, not a page |
| Cottonwood composition landed today | 29 of 63 strategies (46%) — name-gated by `opal_closure` |
| Cottonwood platinum series | 12 measured of 451 axis dates |
| 49F `fact_rps` | 555 partitions; 84,022 rows (04-01) / 93,697 rows (08-11) |
| 49F `fact_acc` | 646 partitions; 6,683 rows (04-01) / 7,189 rows (08-11); tin present on 100% of rows both dates |
| Inflection `fact_positions` | 2,297 partitions; 24,148 rows (04-01) / 35,262 rows (08-11) |
| Inflection platinum series | 442 dates, 2024-11-01 → 2026-08-10 |
| 49F platinum series | 443 dates, 2024-11-01 → 2026-08-11 |

---

## 9. WHAT SURPRISED ME

1. **The April-1 ETF baseline existed on a prefix nobody had looked at** — and finding it did *not* end the
   question, it split it per ticker. The interesting answer was neither "resolved" nor "declare 05-15".
2. **The naive ETF delta is +98.6% and it is wrong.** Two funds entering *measurement* look exactly like two
   funds entering *existence*. The only thing separating them was an inception date in a 3-month-old brief.
3. **Cottonwood has the identical defect and it was not on anyone's hazard list.** Same shape (coverage onset
   masquerading as a zero), larger dollars ($136.5M), and I only found it because the artifact says `absent`
   rather than `0` — a producer that had written `0.0` there would have passed silently into a board number.
4. **Two honest instruments disagreed about Inflection's April-1 zero**, and both were right about their own
   basis. The disagreement is only 0.63% of the segment, but it is the difference between "we had none of this"
   and "we had a little of this".
5. **An exact-match reconciliation would have reported 4 of Andrew's 18 strategies as missing — all present.**
   His hand-written list is accurate; the *roster* is what differs (a prepended "Opal ", a leading space, and
   two dash/whitespace variants). I expected this to bite once or twice; it bites four times. **The hazard CTO
   flagged was that a name scan drops 3 strategies; the symmetric hazard — that name matching invents missing
   ones — was the larger of the two.**

---

## 10. COMPILER TOOLS

| Tool | Call | Result | Note |
|---|---|---|---|
| `comp-which` | ETF holdings source routing | near-tie, 3 of 75 | Correctly declined to guess; routed me to `comp-estate` |
| `comp-estate` | `etfs` → **rejected**, `etf-reports` | PASS after correction | `etfs` is not a vertical — the tool named the 29 valid ones rather than guessing |
| `comp-estate etf-reports` | producer topology | PASS | Gave the 9 producers; its own C0 roster self-labels *"do NOT use as a census denominator"*, so I did not |
| `comp-find` | `PFDE` | PASS — 1,843 hits / 26,096 files, bands HEAD=58 | **The finding of the session.** The HEAD band surfaced the inception brief immediately |
| `comp-find --name` | `rebalance` | PASS — 17 of 17 | Found the existing BD pipeline + both prior scans; build-ladder rung 2 |
| `comp-to` | `OPAL_BRDSEP.T1` | PASS | Session TO context set race-free |

**What worked:** `comp-find`'s band classification. Searching `PFDE` returned 1,843 hits; the HEAD band put the
one document that answered the question — the inception date — at the top of the first page.
**What I did not use:** `comp-pipescript` — I authored no gold/silver script; this TO is measurement only.
**Gap found:** `comp-estate` has no `etfs` vertical although `opal-data-etfs` is a canonical bucket with 695
objects and 9 producers; the vertical is spelled `etf-reports`, which reads as a *reporting* thread rather than
the asset thread. A reasonable question — "what is in the ETFs pipeline?" — does not route on the obvious name.

---

## 11. EVIDENCE INDEX

| Figure | Source |
|---|---|
| ETF net assets, both endpoints | `s3://opal-data-etfs/silver/netassets/{2026-04-01,2026-08-11}.parquet` |
| ETF 03-31 issuer anchor | `s3://opal-data-etfs/silver/netassets/2026-03-31.parquet` (`inferred=False`) |
| PFDE/PFOE inception + no historical shares | `docs/briefs/mdpf-pfde-pfoe-etf-netassets-feasibility-20260518.md:23-24,60,84` |
| 49F / Inflection / Cottonwood model AUA | `s3://opal-data-portal-v2/platinum/mdpf/{firm}/aggregate-aua-timeseries.json` |
| Cottonwood coverage truth | same file, `meta.first_tracked_date`, `meta.covered_dates`, `meta.composed_backfill` |
| Inflection launch seam | same file, `meta.launch_seam` |
| Cottonwood strategy roster | `s3://opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_models/2026-08-12/page_000.json` |
| Cottonwood composition scan (independent) | `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/BD_REBALANCER_OPAL_COMPOSITION_SCAN_20260807.md` |
| Per-firm ETF ownership | `s3://opal-data-etfs/daily/{firm}/{date}.json` |
| 49F accounts + clients | `s3://opal-data-assets/schwab/08242234/silver/{fact_acc,fact_rps}/date=…` |
| Inflection accounts + clients | `s3://opal-data-assets/orion/inflection/silver/fact_positions/date=…` |

---

## 12. CONTROLS — both mutants FIRED (T1-A9 + mutant)

**A passing assertion never mutated has never been tested.** Two controls, each removing one step of my own
method and re-running it:

**Mutant 1 — remove cohort-matching from the ETF delta.**

```
MUTATED (no cohort match): 754,683,842.00 - 380,090,654.30 = +374,593,187.70  (+98.55%)
CORRECT (cohort-matched) : 496,914,800.00 - 380,090,654.30 = +116,824,145.70  (+30.74%)
DIVERGENCE = $257,769,042.00        -> FIRED-AS-EXPECTED (2.2x apart)
```

Without the control, the ETF segment reports **triple-digit growth**. This is the exact number a reasonable
analyst produces from these two artifacts in good faith.

**Mutant 2 — remove name-normalization from the Cottonwood reconciliation.**

```
MUTATED (exact string only): on-list-not-found = 4  -> ['Anna *9238','Moderate Income Portfolio',
                                                        'Opal - Beecherl Legg','Opal - Income']
CORRECT (normalized)       : on-list-not-found = 0  -> EMPTY
                                    -> FIRED-AS-EXPECTED (4 false findings manufactured)
```

**Determinism (T1-A9).** Full extraction run twice from the same local mirrors:
`python extract_brdsep_t1.py > run1.json` / `> run2.json`; `diff run1.json run2.json` →
**IDENTICAL, 0 differing lines across 514 lines.** STABLE.
