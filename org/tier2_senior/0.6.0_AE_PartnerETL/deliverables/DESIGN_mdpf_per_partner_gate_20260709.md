# DESIGN — `mdpf-daily-trigger`: replace the global AND-gate with a per-partner gate

**archetype:** IMPLEMENT (design)
**Status:** DESIGN ONLY. Nothing deploys. Diff to `1.0.0_SA_CTO` before anything lands.
**Author:** 0.6.0_AE_PartnerETL · **Project:** `MDPF_CADENCE.ae-eventdriven-convergence-gate-trigger`
**Andrew (sovereign), relayed by CTO 20260709T214455Z:** *"49 Financial should not hold up MDPF, that is nonsensical."*
**Co-activation partner:** `0.4.0_DS_ClientPlatform` — abstain-on-stale-minuend guard in
`data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py`. **These are ONE change. COO sequences.**

---

## 0. The defect, stated precisely

`lambda_function.py:301`
```python
gate = {..., "all_fresh": bool(inf["fresh"] and bd["fresh"])}
:303   if GATE_ENFORCE and not gate["all_fresh"]:   ->   DEFER, dispatch nothing
```

`run_date` already follows the INF spine (`:298 run_date = event.get("run_date") or inf.get("as_of") or today`).
**The spine is the driver; the AND-gate is bolted on top of it.** So one partner's custody stall halts the entire
chain, including Inflection, which was fresh every single day.

Live decision log (`/aws/lambda/mdpf-daily-trigger`):
```
  07-07  PASS   inflection as_of=2026-07-07 | 49f rps latest=2026-07-06 behind=1  -> dispatched
  07-08  PASS   inflection as_of=2026-07-08 | 49f rps latest=2026-07-06 behind=2  -> dispatched
  07-09  DEFER  inflection as_of=2026-07-09 | 49f rps latest=2026-07-06 behind=3  -> dispatched=false
```
`s3://opal-data-bd/schwab/silver/rps/` stopped at `date=20260706`. `custody_source="schwab"` (the repoint landed).

**The contract already backs Andrew.** `MDPF_ASSETS_WSA_CONTRACT.md:105` (§3.5-decision-iv, CTO-ratified):
*"The aggregation layer roll-forwards the most recent `as_of_date <= target` **per partner**."*
A global AND-gate is **stricter than the contract it implements** — it converts a contracted *per-partner
degradation* into a *fabric-wide outage*. **The gate is the anomaly, not the stall.**

### The gate itself is NOT broken — do not "fix" it by loosening it
`BD_MAX_LAG_TRADING_DAYS=2` is zero-margin **by design** (fail-safe: defers on the first real producer slip). It
deferred on 07-09 on a **real** slip. Raising it to 3 would mask the slip it correctly caught. My own header
already forbids this (*"Do NOT raise to 3 — that would MASK a real 1-day slip"*). **Composition is the bug;
sensitivity is not.**

---

## 1. THE COUPLING YOU MUST NOT BREAK — verified, exact, on the served artifact

**Un-gating alone resumes a live corruption.** 49F's `non_model_aua` is a **residual**
(`build_mdpf_wse_49f_non_model_aua.py:10-13`):

```
  non_model_aua(49f) = partner_custody_total(49f)      <- Schwab RPS book. STALE (frozen at 07-06).
                     - model_aua_input   (Cohort 1a)   <- WS-B / SmartX. DAILY FRESH.
                     - sma_aua_input     (Cohort 1c)   <- WS-B / SmartX. DAILY FRESH.
```

Measured on `s3://opal-data-mdpf/mdpf/feeds/non_model_aua/49financial/`:

| as_of | partner_custody_total | model_aua_input | sma_aua_input | non_model_aua |
|---|---:|---:|---:|---:|
| 2026-07-02 | 1,614,447,381.76 | 1,386,551,932.37 | 23,305,627.31 | 204,589,822.08 |
| 2026-07-06 | **1,621,251,574.22** | 1,400,957,639.03 | 23,380,776.56 | 196,913,158.63 |
| 2026-07-07 | **1,621,251,574.22** | 1,396,248,911.26 | 23,681,115.78 | 201,321,547.18 |
| 2026-07-08 | **1,621,251,574.22** | 1,390,483,476.75 | 23,474,513.91 | 207,293,583.56 |

```
  07-06 -> 07-08:   d(partner_custody_total) =         +0.00        <- frozen TO THE CENT
                    d(model_aua_input)       = -10,474,162.28
                    d(sma_aua_input)         =     +93,737.35
                    d(non_model_aua)         = +10,380,424.93

  identity check:   d(non_model) = d(custody) - d(model) - d(sma)
                                 =      0.00  - (-10,474,162.28) - (+93,737.35)
                                 = +10,380,424.93        EXACT, to the cent.
```

> **49F's served `non_model_aua` is the motion of its subtrahends, sign-flipped, against a frozen minuend.**
> The plug is not measuring non-model assets. It is measuring SmartX's daily P&L, backwards.

### TWO FIELDS, BOTH EXACT — do not "reconcile" one with the other (my error, CTO 215642Z)

I initially "corrected" CTO's figure. **The correction was wrong; we measured different fields.**

```
  SERVED  platinum/mdpf/aggregate_aua_ts : non_model_aua = custody - model
          -> d(served) = -d(model) = +10,474,162.28          <- CTO's "exactly that". EXACT.
  FEEDER  mdpf/feeds/non_model_aua/49financial : non_model_aua = custody - model - sma
          -> d(feeder) = -(d_model + d_sma) = +10,380,424.93 <- the table above. EXACT.

  served(non_model) - feeder(non_model) == that date's sma_aua_input, to the cent, on all three dates.
```
Both numbers are right. **I corrected a served-artifact claim using a feeder artifact.** The `$93,737.35` is the
drift of a term the served field does not contain.

> **Rule taken from it: never publish a delta without the operands that produced it.**
> Had I shown only the difference, a false correction would have been accepted.

**And the discrepancy is itself a finding (CTO, separate track — NOT part of this co-activation):** the aggregation
layer publishes `custody - model` as `non_model_aua`, folding **$23.47M of 49F's SMA book into "non-model"**, which
violates Andrew-direct Contract AMENDMENT 1 (*"1a and 1c … never a combined figure"*). The identity
`model + non_model == custody` still closes — **a classification error that preserves the sum is invisible to every
check that tests the sum.** COO owns it separately.

**Therefore: ship the gate alone and MDPF publishes a fabricated 49F number EVERY DAY instead of once.**
The gate is currently the only thing suppressing it.

### BLAST RADIUS: UNDETERMINED — and it is not computable from the artifact

I produced two censuses and **retracted the first**:
- assuming the builder selects `max(RPS <= as_of)` → **6 rows**;
- selector-independent (custody unchanged vs prior feeder row while a subtrahend moved) → **8 rows**;
- **overlap: only `2026-07-07` and `2026-07-08`** — the two days already known.

They disagree because **neither can read the minuend's vintage.** Source: `:762 rps_date = args.rps_date or
_latest_rps_partition()` — the latest RPS partition **at build time**, a wall-clock property that is never recorded.
My first census inferred a selector and printed it as *"custody TRUE vintage."* That was an inference presented as a
measurement, and it is retracted.

> **`partner_custody_as_of` (contract §4) is not merely a precondition for the GUARD. It is a precondition for the
> CENSUS. You cannot count the damage until the field exists.**

**Recoverable without the schema change**, from the producer's inputs rather than the artifact: each row carries
`_ingested_at` (write time); reconstruct `_latest_rps_partition()` as of that instant from the RPS partitions'
`LastModified`. *When the artifact cannot answer, the producer's inputs still exist.* Not run inside the 02:00Z
window; CTO's call on the owner.

*(The 06-13/14 weekend rows show `d(model)=+0.00, d(sma)=+0.00` and are correctly flagged by neither method — the
positive control on the discriminator, and the one thing both runs agree on.)*

---

## 2. DESIGN

### 2.1 Dispatch on the INF spine alone
```python
# BEFORE
gate["all_fresh"] = bool(inf["fresh"] and bd["fresh"])
if GATE_ENFORCE and not gate["all_fresh"]:  DEFER

# AFTER
gate["spine_fresh"]     = bool(inf["fresh"])          # the driver; run_date already follows it (:298)
gate["partners"]        = {"inflection": inf, "49financial": bd}
gate["stale_partners"]  = [p for p, v in gate["partners"].items() if not v["fresh"]]
if GATE_ENFORCE and not gate["spine_fresh"]:  DEFER    # ONLY the spine can halt the run
```
**A partner's freshness marks its own block, never the run.** `DEFER` is reserved for the driver being absent —
there is no `run_date` without it.

### 2.2 Per-partner verdicts stamped into the dispatch env — one read, propagated
Reuse the `CUSTODY_SOURCE` pattern exactly (`:293` resolve once → `:336` stamp). It is the right pattern and it
already prevents a mid-flip race; the feeders must not re-derive freshness independently.

```python
bootstrap += [
    f"export CUSTODY_SOURCE={custody_source}",                       # existing
    f"export MDPF_STALE_PARTNERS={','.join(gate['stale_partners'])}",# '' when all fresh
    f"export MDPF_PARTNER_ASOF_49FINANCIAL={bd.get('as_of','')}",
    f"export MDPF_PARTNER_BEHIND_49FINANCIAL={bd.get('behind','')}",
    f"export MDPF_PARTNER_ASOF_INFLECTION={inf.get('as_of','')}",
    f"export MDPF_PARTNER_BEHIND_INFLECTION={inf.get('behind','')}",
]
```
Shell-safe scalars only (no JSON blob in an `export`). Feeders read their own partner's verdict; **no feeder
re-derives freshness**, so gate and compute cannot diverge.

### 2.3 The co-activated guard (DS's lane) — ABSTAIN, never roll forward the residual
This is CTO's own `C_02` rule, one pipeline over:

> **For an ENRICHMENT: substitute, with provenance and a max-age bound.**
> **For a DATED, DERIVED quantity: ABSTAIN + alarm. It may never borrow a value from a date it does not claim.**

`non_model_aua` is a *dated residual*. Its validity requires that minuend and subtrahends **share a vintage** —
which `build_mdpf_wsc_inflection_feeder.py:158` already asserts as an invariant
(*"model_aua_positions (gold) and non_model_aua (silver) views share a vintage"*).

**AMENDED (CTO 215642Z + DS 215306Z) — the predicate is EQUALITY on an INTERSECTION, not `<` on two
independently-selected dates:**

**SUPERSEDED TWICE. Read both corrections — the second one is my own law turned on my own design.**

**(i) CORRECTION 1 (COO 221829Z, binding): THE ABSTAINING FEEDER EMITS THE ROW.**

I originally wrote *"ABSTAIN: emit NO row."* DS wrote *"emit `null` + `abstain_reason`."* **CTO ratified both
within forty minutes and nobody caught it** — the two halves of one co-activation specified different artifacts.

> **An omitted row and a run that never happened print the same nothing.**

**Absence is not evidence.** A missing partner-date is indistinguishable from a dispatch failure, a crashed feeder,
or a partner never onboarded. **A `null` with a reason is a statement.** "Emit no row" is the *silent-skip* pattern —
`A_00`'s `print("0 accounts")`-then-proceed, `C_02`'s SKIP, and `cot_silver_merge:493-496`'s literal
`# CHAINFIX: frozen no-op = successful run` — **sitting inside the fix for it.** I found that last one four hours
ago and then wrote its shape into my own remedy.

**(ii) CORRECTION 2: the predicate must be stated over a field that will exist.**
`partner_custody_as_of` does not exist on the row today (§1). A predicate over a field the artifact does not carry
is unauditable the day after it ships. **It is a contract §4 schema change (`COLS_NON_MODEL_AUA`), not a one-liner**
— and it is the *same* field whose absence made the blast-radius census un-runnable. **A precondition for the
guard AND for the census.**

```python
# in build_mdpf_wse_49f_non_model_aua.py -- REQUIRES contract §4: partner_custody_as_of on the row
common = max(RPS_valuation_dates & WSB_valuation_dates)   # CANONICAL VALUATION DATES, never partition names (§2.3b)

aligned = (custody_vintage == model_vintage == sma_vintage == common)

# ALWAYS emit the row. Never omit it.
row = {
    "firm_id": "49financial",
    "as_of_date":            common,
    "partner_custody_as_of": custody_vintage,   # NEW, contract §4 -- a VALUATION date, not a partition name
    "model_aua_input":  model_val,
    "sma_aua_input":    sma_val,
    "partner_custody_total": custody_val,
    "non_model_aua":  (custody_val - model_val - sma_val) if aligned else None,   # NULL, not absent
    "abstain_reason": None if aligned else
        f"vintage_mismatch custody={custody_vintage} model={model_vintage} sma={sma_vintage} common={common}",
}
if not aligned:
    emit MDPF/Partner PartnerResidualAbstain=1 {Partner=49financial}
    log LOUDLY with all three vintages
```
**The aggregate then abstains for that partner-date on a POSITIVE ASSERTION (`non_model_aua is null` +
`abstain_reason`), never on an absence.**
The calendars are **not nested** (`06-30`/`07-01` are RPS-only; `06-27`/`06-28`/`07-07`/`07-08` are WS-B-only), so
`<` vs `==` is a **$10.47M** distinction. And it must bind **three** operands to one as-of, not two —
`sma_aua_input` is a full term in the identity, not a rounding detail.

### 2.3b — BLOCKED: the intersection must be taken on VALUATION DATES, and neither vendor's is grounded

**CTO STOP (221132Z), and it is not liftable yet.** `max(RPS ∩ WSB)` intersects **partition names**. A name is not a
valuation instant, and Andrew's Orion anchor proved the two can differ: the Inflection spine's row `D` holds the
close of `D-1`.

> **You cannot assert operand agreement on labels whose semantics you have not established.**

What I established, read-only, tonight:

| feed | name ↔ internal field | valuation instant | anchor |
|---|---|---|---|
| Schwab RPS | **ESTABLISHED** — `date=D` == the vendor's own `Business Date`, asserted at `H1[4]` and on every `D1` row of the raw `CRS{D}.RPS` | **UNDETERMINED** | none |
| WS-B model_aua_positions | name == internal `as_of_date`, 3/3 | **UNDETERMINED** | none |
| Inflection spine | — | `D` = close of `D-1` | **Orion, via Andrew** |

- The **raw file states its own date** (the header is split across `H2`/`H3` — `Business` + `Date` — which is why a
  naive scan of `H2` finds none). **The docstring `"schwab/bd — their labels are accurate"` is eliminated as
  evidence; we have the vendor's field instead.** And `convert_schwab_rps_to_parquet.py:53` regexes the partition
  date **from the filename**, while `:39`'s `business_date` column **never lands** — silver keeps only `file_date`,
  the filename echoed back. **The converter discards the vendor's own date**, which is why the artifact could not
  answer and the raw bytes could.
- **WS-B's name matching its own internal field is internal self-consistency, which is not correctness.**
  *Self-consistency requires an anchor outside the system.*
- I attempted an external anchor and **discarded it because it failed its own sanity check**: bd `silver/prices/`
  `2026-07-06` and `2026-07-07` are identical to four decimals across four tickers — **forward-filled**. A
  forward-filled series cannot anchor a valuation date, and its non-match proves nothing in either direction.

**The one call that settles it:** `IEFA`'s actual market close on `2026-07-06`. RPS prices it at `98.3100`.
If that is 07-06's close → RPS `D = close(D)`. If it is 07-02's close → the guard is unsafe. YCharts returned
**HTTP 403** this session. One ticker, one date.

**If RPS `D` really is `close(D)`, then `opal_aggregate_aua(D)` has been summing 49F@`close(D)` with
Inflection@`close(D-1)` under one label since inception** — invisible to every check that tests the sum, and
independent of the stall.

**The row cannot express this today.** DS established there is **no custody vintage field**: the row's only date,
`as_of_date`, tracks the WS-B valuation date (`:67-68`), i.e. the *subtrahend*. The minuend's vintage comes from
`:762 rps_date = args.rps_date or _latest_rps_partition()` — **the latest RPS partition at BUILD TIME**, a
wall-clock property that is discarded. So `partner_custody_total` is not stale-and-unlabelled; **it is stamped
with a date it does not have.** The guard therefore requires emitting `partner_custody_as_of` on the derived row —
**a contract §4 schema change, not a one-liner.**
**Roll-forward is legal for a partner's own last-good *level* (the contract's §3.5-decision-iv). It is illegal for
a *residual computed across two vintages*.** The contract roll-forwards `as_of_date <= target` **per partner** — it
does not authorize mixing one partner's stale minuend with that same partner's fresh subtrahends.

### 2.4 Per-partner staleness alarms replace the global one
Today: `mdpf-daily-freshness-stale`, metric `MDPF/DailyChain TimeseriesStalenessDays`, dimension
**`Service=mdpf-daily-runner`** only. Live state:

```
  State: ALARM   since 2026-07-08T16:46Z
  Reason: "1 datapoint [1.0] was greater than or equal to the threshold (1.0)"
```

**It is latched in ALARM and it is partner-blind.** CloudWatch actions fire on a state *transition*; an alarm
already in ALARM emits nothing when the next partner goes stale. And it cannot say *which* partner.

> **A latched, partner-blind alarm is a disabled control that still looks armed.**
> (Third instance tonight: bd's five `bd-served-vintage-stale-*` latched ~67h; cot's `bd-cot-silver-stale-*`
> reporting `TradingDayLag=0` off a filename proxy; and this.)

Replace with:
```
  metric  MDPF/Partner  PartnerStalenessTradingDays  { Partner = inflection | 49financial }
  alarm   mdpf-partner-stale-{partner}   >  BD_MAX_LAG_TRADING_DAYS   (keep =2; do NOT raise)
          TreatMissingData = breaching
  metric  MDPF/Partner  PartnerResidualAbstain       { Partner = 49financial }
  alarm   mdpf-partner-residual-abstain-{partner}  >= 1
```
Emit the per-partner metric **every fire**, fresh or stale, so each alarm has datapoints to transition on. Delete
or re-create `mdpf-daily-freshness-stale` — a latched alarm must be reset, not left as decoration.

---

## 3. What this does and does not fix

| | before | after |
|---|---|---|
| Inflection series | frozen by 49F's stall | **advances daily** |
| 49F `non_model_aua` | suppressed by the DEFER (accidentally correct) | **ABSTAINS explicitly, and says so** |
| which partner is stale | unknowable from the alarm | `Partner` dimension |
| alarm can re-notify | no (latched since 07-08T16:46Z) | yes, per partner, transitions |
| `BD_MAX_LAG_TRADING_DAYS` | 2 | **2, unchanged** |

**Un-gating without §2.3 turns a once-published fabrication into a daily-published one.** That is strictly worse
than today's outage, and every local signal would call it a fix — *it turns a red thing green without changing the
underlying truth.* Ship them together.

---

## 4. Sequencing + gates

1. **DS** source-grounds the residual mechanism and implements §2.3 (script lane, Rule 13).
2. **0.6.0_AE** implements §2.1/§2.2 (Lambda) and §2.4 (TF alarms) — infra lane.
3. **CTO** reviews the diff. **Nothing deploys without an explicit GO.**
4. **COO** sequences the co-activation. The trigger change and the WS-E guard **land together**, exactly as the
   2026-07-01 repoint brief required (*"the trigger re-point + the WS-E swap must land TOGETHER"*).
5. Post-deploy verification, on artifacts not on alarm state:
   - Inflection `as_of` advances on a day 49F is stale — **read the feed, not the alarm**;
   - a 49F ABSTAIN emits **no** `non_model_aua` row for that date (absence is the correct output);
   - when RPS resumes, the first 49F residual has minuend and subtrahends on the **same vintage**;
   - `mdpf-partner-stale-49financial` **transitions** OK→ALARM→OK (proving it is not latched).

**Not deployed. Not tonight.** Diff to CTO first.

grounding:
  exercised = read `mdpf/feeds/non_model_aua/49financial/{2026-07-02,06,07,08}.parquet` on live S3; the residual
              identity closes to the cent (see §1)
  applied   = `describe-alarms mdpf-daily-freshness-stale` -> State=ALARM since 2026-07-08T16:46Z,
              dimension Service=mdpf-daily-runner (partner-blind); trigger env GATE_ENFORCE=1,
              BD_MAX_LAG_TRADING_DAYS=2, custody_source=schwab
  source    = mdpf-daily-trigger `:293` `:298` `:301` `:303` `:336`;
              build_mdpf_wse_49f_non_model_aua.py `:10-13` `:61-65`;
              build_mdpf_wsc_inflection_feeder.py `:158` (shared-vintage invariant);
              MDPF_ASSETS_WSA_CONTRACT.md `:105` (§3.5-decision-iv per-partner roll-forward)
  NOT claimed = the vintage PROVENANCE of each residual input (that `partner_custody_total` carries a 07-06
              stamp while the inputs carry 07-08). I verified the arithmetic closure, not the provenance.
              That is `0.4.0_DS`'s grounding per CTO's dispatch.
