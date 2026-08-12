# OPAL_BRDSEP.T1 — Opal asset base by segment, September board update

**Author:** `0.4.0_DS_ClientPlatform~O` · 2026-08-12 · **REVISED 1855Z under Andrew-direct ruling (§0)**
**TO:** `OPAL_BRDSEP.T1` @`cb1a5ab78a` · **Issued by:** `1.0.0_SA_CTO` · Andrew's methodology verbatim in TO §0
**Type:** Measurement deliverable. **Changes no served artifact.** Read-only throughout; nothing written under `platinum/`.
**Determinism (T1-A9):** extraction run twice, byte-identical, 0 differing lines of 178.

---

## 0. ANDREW-DIRECT, 2026-08-12 ~1855Z — VERBATIM. This section governs the whole deliverable.

> *"This is a start but you need to use THE ENTIRE aum of the 0824 account not just the models, there
> should be 1.74b in there or so for 49 not 1.4b. Make sure you are using the full total from that
> account. regarding cottonwood, you can count 0 as the start. Regarding ETFs, just get the delta from
> 5-15 or whever the first available info is to now."*

Three rulings, all applied. **His phrasing is the ruling; the paraphrase below is navigation, not authority.**

| # | Ruling | What changed |
|---|---|---|
| 1 | **49 Financial = the ENTIRE `08242234` account, not the model slice** | Segment is now $1.737B at the end, not $1.451B. He is right, and his "1.74b or so" matches my measured figure to the decimal — **the number he wanted was already in my table, on the second row; I led with the wrong one.** |
| 2 | **Cottonwood start = 0** | Overrides the `UNCOMPUTABLE-BY-CONSTRUCTION` I had landed. Cottonwood now contributes +$136.53M. |
| 3 | **ETF leg = first-available → now** | Retires the April-1 ETF question as a *requirement*. The leg now runs from 2026-05-18 (first date all four Opal ETFs carry issuer-reported data). |

**What ruling 2 changed and what it did not.** The *framing* changed; the *data* did not. There is still no
2026-04-01 Cottonwood measurement — coverage remains **21 of 132 days**. Counting the start as zero is his
call to make and I have made it as instructed; the coverage caveat travels with the number rather than
withholding it.

---

## 1. THE ANSWER

**Total Opal asset base at the end of the window: $2,124,434,696.15.** Measured growth across the
segments, each on its own stated window: **+$531,268,608.91**.

**49 Financial** — the entire Schwab `08242234` account — grew from **$1,482,015,684.99 (2026-04-01) to
$1,736,948,738.65 (2026-08-11), +$254,933,053.66 (+17.20%)**. **Inflection Wealth Management** is a true
zero start: **$0 → $144,978,896.75**, launching 2026-05-15. **Cottonwood Capital Advisory** contributes
**+$136,530,322.99** against a ruled zero start. **ETF Float** — Opal ETF assets *not* held inside the three
managed books — **fell slightly, from $111,150,402.25 to $105,976,737.76 (−$5,173,664.49, −4.65%)**, because
the managed books grew faster than the funds and absorbed float. Separately, **gross Opal-ETF assets** grew
from **$643,330,643.00 (2026-05-18) to $754,683,842.00 (2026-08-11), +$111,353,199.00 (+17.31%)**.

---

## 2. SEGMENT × {START, END, DELTA} — every cell dated (T1-A1)

| Segment | Start | as-of | End | as-of | Delta | % |
|---|---:|---|---:|---|---:|---:|
| **49 Financial** — entire account `08242234` | $1,482,015,684.99 | 2026-04-01 | $1,736,948,738.65 | 2026-08-11 | **+$254,933,053.66** | +17.20% |
| **Inflection Wealth Management** — Opal model AUA | $0.00 | 2026-04-01 | $144,978,896.75 | 2026-08-10 | **+$144,978,896.75** | — (0 start) |
| **Cottonwood Capital Advisory** — Opal model AUA | $0.00 ᴿ | 2026-04-01 | $136,530,322.99 | 2026-08-10 | **+$136,530,322.99** | — (0 start) |
| **ETF Float** | $111,150,402.25 | 2026-07-20 | $105,976,737.76 | 2026-08-11 | **−$5,173,664.49** | −4.65% |
| | | | **$2,124,434,696.15** | mixed | **+$531,268,608.91** | |

ᴿ = **ruled**, not measured (§0 ruling 2).

**Gross Opal-ETF assets** — the quantity ETF Float is derived from, before the managed-book subtraction.
Reported separately because **it is not a fifth segment and must not be added to the total** (its
firm-held portion is already inside the three managed segments; that is what the float subtraction exists
to prevent):

| Cohort | Start | as-of | End | as-of | Delta | % |
|---|---:|---|---:|---|---:|---:|
| All four Opal ETFs | $643,330,643.00 | 2026-05-18 | $754,683,842.00 | 2026-08-11 | **+$111,353,199.00** | +17.31% |
| DIVZ + IDVZ (from his named 5-15) | $405,106,800.00 | 2026-05-15 | $496,914,800.00 | 2026-08-11 | +$91,808,000.00 | +22.66% |

**Per-ticker, 2026-05-18 → 2026-08-11 — and one of the four fell:**

| Ticker | Start | End | Delta |
|---|---:|---:|---:|
| DIVZ | $241,896,600.00 | $298,966,800.00 | +$57,070,200.00 |
| IDVZ | $158,742,800.00 | $197,948,000.00 | +$39,205,200.00 |
| PFDE | $131,731,488.00 | $164,376,380.00 | +$32,644,892.00 |
| **PFOE** | $110,959,755.00 | $93,392,662.00 | **−$17,567,093.00** |

---

## 3. THE 49 FINANCIAL NUMBER IS TIED OUT TO THE ACCOUNT ITSELF

He said *"make sure you are using the full total from that account"* — so I did not rest on the portal
aggregate. I summed the account's own Schwab silver and tied the two together:

| Measure | 2026-04-01 | 2026-08-11 |
|---|---:|---:|
| `dim_balance.net_mv_plus_cash` summed over all accounts (**the account's own books**) | $1,482,015,684.99 | $1,736,948,738.65 |
| `platinum/mdpf/49financial` `partner_custody_total` (**the portal aggregate**) | $1,482,015,684.99 | $1,736,948,738.65 |
| **Difference** | **$0.00** | **$0.00** |

**Exact tie at both endpoints**, across 6,683 and 7,190 account rows. Two independently-derived paths to
the same figure, so the number is not resting on one producer's self-report.

**Why positions alone would have been wrong.** Summing `fact_rps` position market values gives
$1,447,503,078.33 / $1,709,537,020.04 — **$27.4M light at the end**, because positions exclude cash and
money-market balances. `net_mv_plus_cash` is the full total; the position sum is not.

---

### 3a. THE BASIS OF THE 49 FINANCIAL FIGURE — one sentence, so the frame travels with the number

> **The $1,736,948,738.65 figure is the total value of the Schwab custody account `08242234` (Model
> Portfolios) as of 2026-08-11 — net market value plus cash across all 7,190 accounts in that one
> account, including both Opal-model and non-model holdings, and excluding any 49 Financial assets held
> at any other custodian or in any other Schwab account (notably `08335338`, ADVI).**

This matters because **the portal serves different, larger 49 Financial numbers on different bases** —
a headline of $1,911,578,939.87 (`basis=held_certified`, `cert_data_as_of` 2026-07-31) and a trend
series at $1,778,539,360.83. **Those are not in conflict with this one until someone assumes they are
measuring the same scope.** I have not reconciled them and this deliverable does not claim to; the
sentence above exists so a reader cannot set this figure beside the portal's and conclude one is broken.
*(Basis question raised by `0.0.0_AB_MSTR` 2026-08-12 ~1858Z; the portal's own headline-vs-trend
difference is a separate open item at Andrew, held by CTO.)*

### 3b. JUNE CROSS-REFERENCE on the ruled basis — requested by CTO

Requested because a June board comparison was derived on the **model** basis, which the ruling changes.
Reported with frames; **what June's $1.82B headline contained is not adjudicated here — that is Andrew's deck.**

| Date | 49F ENTIRE account `08242234` | 49F model slice | Inflection model AUA |
|---|---:|---:|---:|
| 2026-06-12 | $1,661,023,355.72 | $1,396,731,878.62 | $122,119,749.91 |
| 2026-06-30 | $1,642,683,674.43 | $1,391,024,495.74 | **ABSENT** (`point_class`=absent) |
| 2026-08-11 | $1,736,948,738.65 | $1,451,519,328.79 | $144,978,896.75 *(as-of 08-10)* |

**49 Financial alone does not reach $1.82B at either June date on either basis.** On the ruled
entire-account basis it is **$158,976,644.28 short at 2026-06-12** and $177,316,325.57 short at 06-30.
The ruling narrows the margin substantially — from $423.3M short on the model basis to $159.0M short —
but does not close it.

⛔ **No combined figure is given for 2026-06-30, deliberately.** Inflection's model AUA that day is
`absent`, not zero. Forming a 49F + Inflection total there would require substituting zero for an
absent measurement — **the precise error this deliverable exists to prevent**, and my own first pass at
this table did exactly that before the `point_class` check caught it. At 2026-06-12, where both legs
are `measured`, 49F-entire + Inflection-model = **$1,783,143,105.63**.

---

## 4. CLIENT AND ACCOUNT COUNTS (T1-A7)

| Segment | Metric | Start | as-of | End | as-of | Delta |
|---|---|---:|---|---:|---|---:|
| **49 Financial** | Accounts (`fact_acc` dimension) | 6,683 | 2026-04-01 | 7,189 | 2026-08-11 | **+506** |
| **49 Financial** | Clients (distinct `ssn_tin_number`) | 4,020 | 2026-04-01 | 4,268 | 2026-08-11 | **+248** |
| **49 Financial** | Accounts holding positions (`fact_rps`) | 5,586 | 2026-04-01 | 6,060 | 2026-08-11 | +474 |
| **Inflection** | Accounts in Opal models (platinum) | 0 | 2026-04-01 | 548 | 2026-08-10 | **+548** |
| **Inflection** | Accounts in Opal-named models (Orion silver) | 17 | 2026-04-01 | 600 | 2026-08-11 | +583 |
| **Inflection** | Clients in Opal-named models (Orion silver) | 4 | 2026-04-01 | 266 | 2026-08-11 | +262 |
| **Inflection** | Firm-wide accounts / clients | 880 / 311 | 2026-04-01 | 948 / 318 | 2026-08-11 | +68 / +7 |
| **Cottonwood** | Accounts | 0 ᴿ | 2026-04-01 | 314 | 2026-08-10 | **+314** |
| **ETF Float** | — | *not an account cohort — a dollar residual* | | | | |

⛔ **Cottonwood `account_count` must never be totalled across models.** Producer's own note: *"account_count
is per-model and fans out +1 per underlying model on a blend; summing it across models double-counts (447
vs 296 on 2026-07-22)."* The 314 is the artifact's own cross-section, not a sum.

---

## 5. ETF FLOAT — and why its start is 2026-07-20 and not the feed's onset

`ETF Float = gross Opal-ETF net assets − all firm-specific holdings of those ETFs`

| Component | 2026-07-20 | 2026-08-11 |
|---|---:|---:|
| Gross ETF net assets | $738,190,364.00 | $754,683,842.00 |
| − 49 Financial | −$528,132,730.04 | −$544,129,709.80 |
| − Inflection | −$48,614,453.13 | −$52,569,955.74 ⚠ |
| − Cottonwood | −$50,292,778.58 | −$52,007,438.70 *(as-of 08-10)* |
| **= ETF Float** | **$111,150,402.25** | **$105,976,737.76** |

**86.0% of all Opal ETF assets sit inside the three managed books**; the float is the remaining 14.0%.

### ⛔ The float's start date is set by data completeness, not by feed existence — and this is a trap

Applying *"first available info"* literally to the float gives a **badly wrong** answer. The per-firm
ownership feeds exist from 2026-05-01 (49F, Inflection) and 2026-06-08 (Cottonwood) — but **Cottonwood's
feed is RAMPING at onset, not complete**:

| Date | Cottonwood ETF ownership | Accounts (DIVZ) |
|---|---:|---:|
| 2026-06-08 | $194,520.46 | 5 |
| 2026-07-01 | $2,185,981.67 | 12 |
| 2026-07-08 | $8,405,539.19 | 19 |
| **2026-07-15** | **$47,748,363.75** | **293** |
| 2026-08-10 | $52,007,438.70 | 309 |

**274 accounts appear in a single week.** That is the feed onboarding, not Cottonwood buying $39M of ETFs
across 274 newly-opened accounts in seven days — and it coincides exactly with the producer's own declared
`first_tracked_date` of **2026-07-20**.

**An incomplete subtrahend inflates the float.** Computing the float at the 06-08 feed onset yields a
**+$657.9M "increase"** that is entirely a coverage artifact — and 2026-06-08 carries no netassets
partition at all, so the gross would read $0.00. **The float's honest start is the producer's declared
2026-07-20**, which is what §2 uses.

⚠ **Inflection's 08-11 ownership values are identical to the cent, on all four tickers, to its 08-10
values**, while the underlying NAVs moved — a carry-forward signature. Surfaced to CTO, not chased. Bounds
the float by roughly one day of Inflection drift, order $0.1M.

---

## 6. THE ARITHMETIC (no single headline rate — TO §6)

```
49 Financial   entire account 08242234   +$254,933,053.66    04-01 -> 08-11
Inflection     Opal model AUA            +$144,978,896.75    04-01 -> 08-10  (true 0 start)
Cottonwood     Opal model AUA            +$136,530,322.99    04-01 -> 08-10  (RULED 0 start)
ETF Float                                  -$5,173,664.49    07-20 -> 08-11
                                        ------------------
                                          +$531,268,608.91

END-OF-WINDOW BASE
49 Financial                            $1,736,948,738.65    2026-08-11
Inflection                                $144,978,896.75    2026-08-10
Cottonwood                                $136,530,322.99    2026-08-10
ETF Float                                 $105,976,737.76    2026-08-11
                                        ------------------
TOTAL                                   $2,124,434,696.15
```

**⛔ Do not add gross ETF assets ($754.7M) to this total.** The firm-held portion is already inside the
three managed segments; only the float belongs in the sum. That is precisely what the subtraction is for.

**Two framing choices remain open and both are Andrew's:**
1. **Is Cottonwood's $136.53M "growth"?** He has ruled it counts from zero, which I have applied. It is
   new *to our measurement*; whether it is new *to Opal* is a different question, and Cottonwood was a
   client before we tracked it.
2. **Does Inflection start at $0 or at $914,144.89?** (§7.3.) 0.63% of that segment.

**One asymmetry to state plainly:** 49 Financial is measured as the **entire account**, while Inflection
and Cottonwood are measured as the **Opal model slice** — per his methodology, which named models for
those two. The segments are therefore not like-for-like measures of the same thing.

---

## 7. WHAT THE MEASUREMENT FOUND

### 7.1 The April-1 ETF baseline — resolved, then superseded by ruling 3

The pre-issuance enumeration recorded that no source under `opal-data-etfs` reaches 2026-04-01.
**`silver/netassets/` does** — 353 partitions, 2025-05-30 → 2026-08-11, covering both original endpoints;
the enumeration had caught its sibling `silver/holdings/`. Per ticker the answer split: DIVZ/IDVZ have an
April-1 value that is **interpolated**, with a genuine issuer month-end anchor one day earlier
(**2026-03-31: $381,661,928.74**); PFDE/PFOE have none and cannot get one — the issuer historical file
carries NAV and price but **no Net Assets and no Shares Outstanding**, and net assets is `nav × shares`
(`docs/briefs/mdpf-pfde-pfoe-etf-netassets-feasibility-20260518.md:84`).

**Ruling 3 supersedes this for the board number** — his window starts after the interpolation ends, so
every ETF figure in §2 is issuer-reported, none interpolated. The finding stands as a data-quality fact
and is no longer load-bearing.

### 7.2 The $257.8M trap that ruling 3 also retires

PFDE/PFOE were **incepted 2025-12-30** — before the original window opened — and entered our *measurement*
2026-05-18. Under the original framing, subtracting the two totals counted a coverage onset as growth:
**+98.55%** against a like-for-like **+30.74%**. Under ruling 3 the cohort is constant across the window,
so the trap cannot fire. **Recorded because the same shape recurs in §5 and §7.3, where it is still live.**

### 7.3 Inflection's zero is real but basis-scoped

Platinum's $0 at 2026-04-01 is a zero of the **Eclipse-crosswalked model basis** and reproduces exactly
(`launch_seam: {date_pre: 2026-05-14, launch: 2026-05-15, model_pre: 0.0, clean_step: true}`). Orion silver
`fact_positions` shows **$914,144.89 across 17 accounts / 4 clients in Opal-*named* models** that day, all
`isManaged=True` at custodian `Fidelity_Inflection`. Both instruments are right about different bases.
0.63% of the segment. Reported, not adjudicated.

### 7.4 Cottonwood strategy reconciliation — both sets (T1-A5)

- **ON-LIST-NOT-FOUND: EMPTY.** All 18 of Andrew's strategies resolve on today's roster (17 exact, 1
  normalized: *"Moderate Income Portfolio"* → roster *"Opal Moderate Income Portfolio"*; *" Anna \*9238"*
  carries a leading space).
- **FOUND-NOT-ON-LIST: 5 Opal-named strategies, 2 accounts** — Opal Hendrickson LT/UST (1), Opal Sat 50+
  15% cash (1), Opal Long Term Aggressive (0), Opal Long Term Conservative (0), Opal Satellite 90 (0).

**Denominators:** list = 18; roster = **63 of 63** (`totalResultCount` 63, `pageCount` 1 — full listing,
not a page); roster Opal-named = 21; accounts on the matched 18 = **322**.

**Stated limit:** composition is pulled under `MODEL_DETAIL_SCOPE=opal_closure`, which seeds only on names
containing "opal" — **29 of 63 (46%) landed**. So this set is complete for *name*-based discovery and
structurally cannot be complete for *composition*-based discovery from bronze alone. The independent
62/62 live scan of 2026-08-07 closes that axis and found the only non-Opal-named Opal-composed strategies
to be **Anna \*9237 and Anna \*9238 — both already on the 18**.

**On "a live current sweep":** `cot-rebalancer-runner` pulls `rebalancer.bdreporting.com` daily and landed
**today at 02:00Z**. I reconciled against that landing — same endpoint, same day, the sanctioned raw-vendor
path — rather than issuing a duplicate vendor call. The 08-07 independent scan corroborates it, zero drift.

---

## 8. ASSUMPTIONS, GAPS AND DECLARED EXCLUSIONS

| # | Item | Status |
|---|---|---|
| 1 | **49F account `08242234`** (Model Portfolios), Andrew-confirmed ~1820Z. Every identifier I author is full 8-digit; the one 4-digit form in this file is inside his verbatim quotation in §0, which is not mine to alter and is resolved in the table directly beneath it. | RESOLVED |
| 2 | **49F = entire account**, tied out $0.00 against the account's own `dim_balance` at both endpoints. | RESOLVED, ruling 1 |
| 3 | **Cottonwood start = 0** — a RULING, not a measurement. Coverage is 21 of 132 days; caveat carried. | RULED, ruling 2 |
| 4 | **ETF leg starts 2026-05-18** (first date all four carry issuer data); his named 05-15 given for DIVZ+IDVZ. | RESOLVED, ruling 3 |
| 5 | **ETF Float starts 2026-07-20**, not the 06-08 feed onset — the subtrahend was ramping. | RESOLVED w/ mechanism |
| 6 | **Inflection endpoint is 2026-08-10**, its artifact's `as_of_last`. Not relabelled 08-11. | DECLARED |
| 7 | **49F client count uses `ssn_tin_number`** as a household proxy. Counts only; no values read or stored. | ASSUMPTION, stated |
| 8 | **Inflection 08-11 ETF ownership appears carried forward** from 08-10. | SURFACED to CTO, not chased |
| 9 | **No vendor egress exercised.** Reconciled against our own daily landing + the 08-07 live scan. | DECLARED EXCLUSION |
| 10 | **No single headline growth rate**, per TO §6. | DECLARED EXCLUSION |
| 11 | **Nothing written under `platinum/`.** | CONFIRMED |

---

## 9. DENOMINATORS FOR EVERY SCAN REASONED FROM (T1-A8)

| Scan | Denominator |
|---|---|
| `opal-data-etfs` enumeration | 695 objects (silver 414 / daily 205 / snapshots 61 / platinum 13 / config 1 / csv 1) |
| ETF net-assets series | 353 partitions, 826 rows, 353 dates; **60 of 353 carry all four tickers** |
| ETF genuine observations | DIVZ 73 of 353 · IDVZ 73 of 353 · PFDE 60 of 60 · PFOE 60 of 60 |
| 49F `dim_balance` | 6,683 rows (04-01) / 7,190 rows (08-11); `net_mv_plus_cash` non-null on 100% of both |
| 49F `fact_acc` | 646 partitions; 6,683 / 7,189 rows; tin present on 100% of rows |
| 49F `fact_rps` | 555 partitions; 84,022 / 93,697 rows |
| Inflection `fact_positions` | 2,297 partitions; 24,148 / 35,262 rows |
| Cottonwood ETF-ownership dailies | 41 files, 2026-06-08 → 2026-08-10 |
| Cottonwood BD roster | 63 of 63 (`totalResultCount`=63, `pageCount`=1) |
| Cottonwood composition landed today | 29 of 63 (46%) — name-gated |
| Cottonwood platinum series | 12 measured of 451 axis dates |
| Platinum series lengths | 49F 443 dates → 2026-08-11 · Inflection 442 → 08-10 · Cottonwood 451 → 08-10 |

Every S3 listing was materialised and counted client-side — no `--query length()` on a paginated `list-*`.

---

## 10. WHAT SURPRISED ME

1. **The number Andrew asked for was already in my own table, one row down.** I had measured the entire
   account correctly and led with the model slice. The failure was presentation, not measurement — and a
   reader who takes the top row of a table is behaving reasonably.
2. **The ETF Float's start date is set by its weakest input.** It is a subtraction across three feeds, so
   it cannot begin until *every* firm's feed is complete — and "exists" is not "complete". Cottonwood's
   feed existed from 06-08 carrying 4% of its eventual value.
3. **The coverage-onset shape appeared three separate times** — PFDE/PFOE in the ETF gross, Cottonwood in
   the model series, and Cottonwood again in the ETF-ownership feed. Each time it looks exactly like
   growth. The only reliable tell was a count ramping alongside the value.
4. **PFOE fell $17.6M** while the other three rose. A cohort total moving +17% concealed one constituent
   moving −16%.
5. **An exact-match reconciliation reports 4 of Andrew's 18 strategies as missing** when all four are
   present. The flagged hazard was that a name scan *drops* 3; the symmetric hazard — that name matching
   *invents* missing ones — was larger.

---

## 11. COMPILER TOOLS

| Tool | Call | Result | Note |
|---|---|---|---|
| `comp-which` | ETF source routing | near-tie, 3 of 75 | declined to guess; routed to `comp-estate` |
| `comp-estate` | `etfs` → REJECTED; `etf-reports` | PASS after correction | named the 9 producers; its C0 roster self-labels "not a census denominator", so it was not used as one |
| `comp-find` | `PFDE` | PASS — 1,843 hits / 26,096 files, HEAD=58 | surfaced the inception brief on page 1 |
| `comp-find --name` | `rebalance` | PASS — 17 of 17 | found the existing BD pipeline + both prior scans; avoided a duplicate vendor call |
| `comp-to` | `OPAL_BRDSEP.T1` | PASS | race-free per-session TO context |
| `commit-gate.sh` | extraction scripts | PASS | "All checks passed!" |
| `proof-of-spec-check.py` | instance + 9 expected ids | VALID | coverage checked against the TO's minted set |

**What worked:** `comp-find`'s band classification — `PFDE` returned 1,843 hits and the HEAD band put the
one document carrying the inception date on page 1.
**Gap found:** `comp-estate` has no `etfs` vertical though `opal-data-etfs` is canonical (695 objects, 9
producers); it is spelled `etf-reports`. The obvious question does not route on the obvious name.

---

## 12. CONTROLS — three mutants, all FIRED

**Mutant 1 — remove cohort-matching from the ETF delta** (the original April-1 framing):

```
MUTATED  754,683,842.00 - 380,090,654.30 = +374,593,187.70  (+98.55%)
CORRECT  496,914,800.00 - 380,090,654.30 = +116,824,145.70  (+30.74%)   FIRED, 2.2x apart
```

**Mutant 2 — remove name-normalization from the Cottonwood reconciliation:**

```
MUTATED  on-list-not-found = 4  -> ['Anna *9238','Moderate Income Portfolio',
                                    'Opal - Beecherl Legg','Opal - Income']
CORRECT  on-list-not-found = 0  -> EMPTY                                 FIRED, 4 false findings
```

**Mutant 3 — take "first available info" literally for the ETF Float** (start at the 06-08 feed onset
instead of the 07-20 completeness date):

```
MUTATED  float delta = +$657,896,761.38   (and gross reads $0.00 -- no netassets partition on 06-08)
CORRECT  float delta =   -$5,173,664.49                                  FIRED, sign inverted
```

**Mutant 3 is the one that matters**: it inverts the *direction* of the answer, turning a $5.2M decline
into a $658M increase, and it is the reading a careful person gets by following the instruction literally.

**Determinism (T1-A9):** `python extract_brdsep_t1_v2.py` run twice → **IDENTICAL, 0 differing lines of
178.** STABLE. Structural, not lucky: the extraction reads local mirrors of landed artifacts, so a re-run
cannot pick up a mid-flight producer write.

---

## 13. EVIDENCE INDEX

| Figure | Source |
|---|---|
| 49F entire-account total | `s3://opal-data-assets/schwab/08242234/silver/dim_balance/date=…` (`net_mv_plus_cash`) |
| 49F tie-out | `s3://opal-data-portal-v2/platinum/mdpf/49financial/aggregate-aua-timeseries.json` |
| 49F accounts + clients | `.../silver/fact_acc/date=…`, `.../silver/fact_rps/date=…` |
| ETF net assets, all endpoints | `s3://opal-data-etfs/silver/netassets/{date}.parquet` |
| ETF 03-31 issuer anchor | `s3://opal-data-etfs/silver/netassets/2026-03-31.parquet` (`inferred=False`) |
| PFDE/PFOE inception + no historical shares | `docs/briefs/mdpf-pfde-pfoe-etf-netassets-feasibility-20260518.md:23-24,60,84` |
| Inflection / Cottonwood model AUA | `s3://opal-data-portal-v2/platinum/mdpf/{firm}/aggregate-aua-timeseries.json` |
| Cottonwood coverage + strategy roster | same file `meta`; `s3://opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_models/2026-08-12/` |
| Cottonwood composition scan (independent) | `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/BD_REBALANCER_OPAL_COMPOSITION_SCAN_20260807.md` |
| Per-firm ETF ownership | `s3://opal-data-etfs/daily/{firm}/{date}.json` |
| Inflection accounts + clients | `s3://opal-data-assets/orion/inflection/silver/fact_positions/date=…` |
