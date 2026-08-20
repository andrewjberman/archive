# MDPF_INFACTUAL.001 — the inflection ETF holdings: ACTUAL vs ESTIMATE

**Author:** `0.4.0_DS_ClientPlatform~A` · 2026-08-19
**TO:** `MDPF_INFACTUAL.001` (COO, issued 2026-07-29; GO'd 2026-08-19 ~2303Z)
**Disposition:** CTO arch ruling 231610Z — **do NOT build the feeder**; this measurement is banked as the
TO's actual deliverable. Close disposition executes at COO.
**Authority for the ask:** Andrew-direct, verbatim — *"there is absolutely no excuse for any kind of
interpolation or estimation when it comes to asset valuation; that is a raw pull."*

---

## 1. THE ANSWER

**The actual value is $50,615,505.11. The served estimate was $58,266,275.67. The estimate ran
13.13% high — not the ~1–3% the design doc documented.**

| ticker | ACTUAL (measured) | ESTIMATE (model_aua × target_weight) | delta |
|---|---:|---:|---:|
| DIVZ | 18,512,156.58 | 18,382,174.73 | **+0.71%** |
| IDVZ | 14,155,735.71 | 17,367,784.99 | −18.49% |
| PFDE | 11,412,064.92 | 14,300,934.55 | −20.20% |
| PFOE | 6,535,547.90 | 8,215,381.40 | −20.45% |
| **TOTAL** | **50,615,505.11** | **58,266,275.67** | **−13.13%** |

*Date 2026-07-28 (the TO's stated baseline date, so the two sides are comparable).*

**Andrew's rule is satisfiable today with a one-line sum, no vendor call and no new machinery:**

```
held_value(inflection, TICKER, D) = SUM(currentValue)
  FROM s3://opal-data-assets/orion/inflection/silver/fact_assets/date=D
  WHERE ticker == TICKER
```

---

## 2. DENOMINATOR AND PREDICATE (TO §7.6)

| control | value |
|---|---|
| rows scanned | **35,098** |
| accounts in partition | **943** (943 distinct `accountId`, 325 distinct `clientId`) |
| distinct tickers in partition | **1,656** |
| predicate | `ticker IN {DIVZ, IDVZ, PFDE, PFOE}` |
| rows matching predicate | 2,330 (581 / 581 / 584 / 584) |
| accounts holding ≥1 target ETF | **587 of 943** |
| positive control | 9,590 non-target rows carry `currentValue > 0` — the scan is not returning a degenerate slice |

---

## 3. SOURCE CAVEATS — BOTH RESOLVED BY ENUMERATION, NOT CONSTRUCTION

The TO explicitly warned not to inherit either caveat and not to construct the path.

**Caveat 1 — eclipse vs orion.** Enumerated both prefixes:
- `eclipse/inflection/silver/` → `fact_model_composition`, `fact_models`, `fact_portfolios_full`,
  `fact_portfolios_simple` — **model only, no custody positions**
- `orion/inflection/silver/` → `fact_assets`, `fact_performance`, `fact_positions`, `fact_transactions`

ETF holdings are a custody quantity ⇒ **orion**. The handoff doc's "Eclipse-positions" wording is stale, as
the TO suspected.

**Caveat 2 — `fact_assets` vs `fact_positions`.** Both exist and both carry every needed column. Measured
both rather than picking:

| | fact_assets | fact_positions |
|---|---|---|
| partitions | 2,305 (2020-04-28 → 2026-08-19) | 2,304 (2020-04-24 → 2026-08-19) |
| cols | 63 | 64 |
| rows @2026-07-28 | 35,098 | 35,098 |
| the four ETF sums | **identical** | **identical** |

**The caveat is moot — they return byte-identical results.** ⚠ But that is itself a smell worth someone's
attention: two near-duplicate silver tables, same grain, same content, independently maintainable.

---

## 4. THE JOIN IS SOUND — TESTED, BECAUSE ACCEPTANCE #2 SAID TO

TO §7.2: *"The inflection held values MOVE DOWN ~1-3%… A move UP, or a move of the wrong magnitude, means
the join is wrong — investigate, do not accept."* I got −13.13% **with DIVZ moving UP**, so I tested rather
than shipped:

| check | result |
|---|---|
| duplicate `(accountNumber, ticker)` rows | **0 of 2,330** — the sum is not inflated |
| `\|currentValue − currentShares × currentPrice\| > 0.01` | **0 of 2,330** (max abs diff 0.0050) — internally consistent |
| per-ticker shares/price | DIVZ 473,942 @ 39.06 · IDVZ 406,192 @ 34.85 · PFDE 416,423 @ 27.41 · PFOE 289,163 @ 22.60 — no anomalous price |

**The join is correct. The acceptance bar is what is wrong.**

---

## 5. WHY −13% AND NOT −1-3%: THE ETFs ARE MID-RAMP

| date | DIVZ | IDVZ | PFDE | PFOE | TOTAL |
|---|---:|---:|---:|---:|---:|
| 2026-01-30 | 107,661 | 94,876 | 45,531 | 44,948 | 293,017 |
| 2026-03-31 | 106,778 | 94,710 | 61,283 | 58,036 | 320,807 |
| 2026-05-29 | 0 | 0 | 7,715,909 | 4,429,661 | 12,145,570 |
| 2026-06-30 | 15,340,135 | 11,939,814 | 9,787,219 | 5,669,537 | 42,736,705 |
| 2026-07-28 | 18,512,157 | 14,155,736 | 11,412,065 | 6,535,548 | 50,615,505 |
| 2026-08-19 | 19,054,952 | 14,383,167 | 12,302,340 | 6,595,984 | 52,336,443 |

**The estimate assumes positions sit AT target weight; the book is still transitioning INTO it.** So the
estimate measures **intent** against a portfolio that has not arrived — which is precisely the distinction
Andrew drew. DIVZ, which has ramped furthest, sits nearest target (+0.71%); the three still filling lag ~20%.

**The "~1-3% HIGH" figure describes a CONVERGED state that does not hold here.** It expired exactly the way
the materiality threshold in the TO's §2 expired — a number measured once and carried forward as a bar.
**Rider 1 of CTO's ruling: correct that bar on the TO face, or it misleads the next reader as it nearly
misled me.**

---

## 6. ⚠ THE DEFECT THIS TO EXISTS TO FIX IS NO LONGER SERVED

The TO targets `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json`. **That prefix holds zero
objects.** It was not deleted — it moved:

- `platinum/mdpf/archive/aggregate_aua/` — 439 objects, last data **2026-08-05**, all moved
  **2026-08-06T21:42:09Z**
- live successor: `platinum/mdpf/{firm}/aggregate-aua-timeseries.json`, produced by
  `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`

**Swept every live served object rather than concluding from one key:**

| | |
|---|---|
| objects under `platinum/mdpf/` | 484 |
| live (non-archive) `.json` | **40** |
| live keys containing any of DIVZ/IDVZ/PFDE/PFOE, `attribution_basis`, `target_weight` | **0 of 40** |
| read failures | **0** |
| **positive control** — same scanner on `archive/aggregate_aua/2026-08-05.json` | `{DIVZ:3, IDVZ:3, PFDE:3, PFOE:3, attribution_basis:4, target_weight:9}` |

The archived file's value is verbatim `"rps_actual:49financial;target_weight:inflection"` — the exact defect.
**The scanner discriminates, so the absence is a finding and not an artifact of asking wrongly.**

⇒ **The ETF decomposition stopped being served on 2026-08-05. The defect was retired by supersession, not by
fix.** Building the feeder would land correct code on a consumerless path — build-ladder rung 1, debt the
moment it lands. **CTO ruling 231610Z: do not build.** Whether the decomposition RETURNS to the served layer
was a **product** decision — **AND IT IS NOW RULED.**

### ⚖ ANDREW-DIRECT 2026-08-20, VERBATIM — AND IT CORRECTS MY FRAMING

> *"Model Portfolios doesn't display ETF attribution and never has. Even if there was some json being
> stored in opal-data-portal-v2/platinum/mdpf/ somewhere or similar, there was never any ETF holdings
> displayed there, so i dont see the relevance here."*

**He is right, and my error is precise: I measured the SERVED (S3) plane and drew a conclusion about the
PRODUCT (display) plane.** The 484-object sweep above is sound about S3 and says nothing about what a user
sees. Source-confirmed against the portal *after* his ruling:

| probe | portal result |
|---|---|
| `attribution_basis` | **0 hits / 1,281 files** |
| `held_by_partner` · `target_weight` · `etf_attribution` | **0 hits each** |
| `etf_decomposition` | **1 real source hit** — `portal/src/api/portal-proxy.ts:498`, a **TypeScript interface field** declaring an artifact's shape |
| `etf_decomposition` in components/pages | **0 hits / 291 files** — nothing renders it |
| `DIVZ` (71 hits) | a **screener preset** (`SSCN_DIVDEF`) — an unrelated feature |

**A TYPE DECLARATION IS NOT A DISPLAY.** `portal-proxy.ts:505` further records the root fetcher **KILLED
2026-08-04** as a dead consumer.

⇒ **The ETF decomposition was never a product surface** — a gold/served artifact with a type binding and no
renderer. **So the ~$7.7mm overstatement never reached a client.** That is materially better news than "it
stopped being served," and it retires the premise under this TO entirely rather than merely superseding its
target.

*This is the reader-plane class I already carry a memory line on (`feedback_zero_access_oracle_must_match_the_reader_plane`): a storage-plane oracle answering a display-plane question. I walked into a known class, and my `/open-calls` recommendation to restore it stood on the same wrong plane.*

---

## 7. §3'S PREMISE — CHECKED AT SOURCE, BECAUSE THE MANDATED TOOL COULD NOT ANSWER

`comp-pipescript io mdpf_aggregate_aua.py --pipeline mdpf` returned:

```
READS: (none detected)      WRITES: (none detected)
WARN: no s3_layout constants or hardcoded S3 paths detected.
```

The TO encodes that tool's silence as a **STOP trigger**. I did not fire it: **an instrument that detects
nothing at all — including reads that certainly exist — has not made a negative finding.** Checked the
premise at source instead, and it is intact and firm-agnostic:

- `mdpf_aggregate_aua.py:177` — `partner_held_etf` in the feeder registry
- `:459-461` — the `(firm_id, ticker)` override loop, keyed generically
- `:1141-1150` — loads the feeder and passes `partner_held` into `build_etf_decomposition`
- `comp-find "partner_held_etf"` — 383 hits across **27,060 files scanned**

**CTO rider 2: this is a real instrument defect, routed to the instrument-repair queue with this file as the
fixture.** As written, the TO's gate would have produced a false STOP.

---

## 8. BANKED, NO ACTION TAKEN

- **Two-homes:** `wsd_partner_held_etf.py` exists in two independently-editable homes —
  `data/mdpf/scripts/feeders/` and `infra/aws/lambda/mdpf-pipeline/wsd-49f-partner-held-etf-daily/`. Rule 22a's
  one-producer-two-homes shape, where a filename-resolved drift check reads clean while the copies diverge.
  *(CTO rider 3: joins the 0.8.0 T4 census as instance #3 of the night.)*
- **`mdpf-feeder-accelerator` carries `ScheduleExpression: None`** — event-driven only, the no-schedule shape
  CLAUDE.md names. Not chased.
- Two near-duplicate silver tables (`fact_assets` / `fact_positions`), same grain, identical content (§3).

## 8b. BOTH OPEN CALLS RULED (Andrew-direct, 2026-08-20)

| call | ruling (verbatim) | consequence |
|---|---|---|
| Does the product display ETF attribution / should it return? | *"doesn't display ETF attribution and never has… i dont see the relevance here"* | The re-cut is **DEAD, not deferred** — no feeder now, and none on a later yes. |
| Re-value the 526 historical in-kind partitions? | *"Leave it"* | Historical partitions stay **declared-and-labelled**. No a03+b01 backfill program. My recommendation, adopted. |

**Both close permanently. Neither is parked work and neither returns to my board.**

## 9. WHAT I DID NOT DO

No feeder built. No aggregator edit. No deploy, no apply, no push. Nothing served was touched. The TO is
**not** closed by me — disposition executes at COO on CTO's recommendation.
