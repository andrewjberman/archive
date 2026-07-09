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

Refinement to CTO's statement (`214455Z`): the plug rose by **`-(d_model + d_sma)`**, not by `-d_model` alone.
His `model_aua` figure `-10,474,162.28` is exact; the `+93,737.35` SMA drift accounts for the residual difference.

**Therefore: ship the gate alone and MDPF publishes a fabricated 49F number EVERY DAY instead of once.**
The gate is currently the only thing suppressing it.

*(Caveat, held: I verified the arithmetic identity on the served feed. The `source_pipeline`/vintage attribution of
each input — i.e. that `partner_custody_total` genuinely carries a 07-06 vintage while the inputs carry 07-08 — is
`0.4.0_DS`'s to source-ground per CTO's dispatch. My claim is the closure, not the provenance.)*

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

```python
# in build_mdpf_wse_49f_non_model_aua.py, before emitting the row
if as_of(partner_custody_total) < as_of(model_aua_input):
    ABSTAIN: emit NO row for this date; emit MDPF/Partner PartnerResidualAbstain=1 {Partner=49financial}
    log LOUDLY with both vintages. Do NOT roll the residual forward.
```
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
