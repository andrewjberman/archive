# ADVI_BDPARITY.P3-EXACT -- CYCLE 2 INTERIM RECORD

**Seat:** `0.4.0_DS_ClientPlatform~C` | **As of:** 2026-09-01T10:4xZ | **Status: OPEN, gate NOT requested**
**Inputs, PINNED:** cells `ADVI_BDPARITY_P2-2_CELLS_20260901.csv` @`e12a0b2960`;
exclusion `ADVI_BDPARITY_P2-2_NOTCOMPARABLE_ACCOUNTS_20260901.csv` @`ecc18c543b`.
**Instrument:** `ADVI_BDPARITY_P3_cycle2_flow_placement_20260901.py` @`b015fec3d5` (committed so its
provenance is checkable rather than asserted; verified at source by `3.0.0_SA_CVO` 91326).
**Class driven:** LARGE, both-sides-linked (1,506 cells / 919 accounts). **Dispositions taken: NONE.**

⚠ **INTERIM. Written because four seats are quoting these numbers and an MCP thread is not a carrier.**

---

## 0. WHERE THIS CYCLE STANDS AGAINST THE GATE

`1.0.0_SA_CTO` 90838 ruled NO CONVENTION REGISTERED and set three preconditions.

| | precondition | status |
|---|---|---|
| (i) | MECHANISM, not association | **STRONGER, NOT MET** -- quantitative fit for the accounts it touches; 149 cells it provably does not |
| (ii) | POPULATION | **MET** -- all 1,506 cells, three periods |
| (iii) | WHICH PLACEMENT IS CORRECT | **HALF** -- our side ratified + conformant; BD's side UNMEASURED and not measurable from our data |

**`P2-3` ("zero unexplained non-EXACT"), re-homed to this TO by `2.0.0_SA_COO` 91278, is UNMET.**

---

## 1. THE MECHANISM -- FLOW PLACEMENT (M5)

Three measurements taken for different reasons, agreeing:

```
  FLAT ACROSS WINDOWS   median +14.00 / +15.59 / +16.11 bp over 42 / 165 / 252 days
                        -> a ONE-OFF event per account, NOT a per-day drag
  SIGN CONSISTENT       96.7% of multi-cell accounts carry the SAME sign
  FLOW-BEARING          4.6x - 6.1x the control rate, all three periods
```

### 1a. The full-population test (precondition ii)

```
  period  LARGE accts  flow-bearing   EXACT control  sep    ZERO-SENS   |obs|/|pred|  SIGN
  QTD        183          76.5%      1,774  12.5%   6.1x   44  24.0%      1.00       78.4%
  YTD        652          91.4%      1,323  19.0%   4.8x   57   8.7%      1.04       84.4%
  1Y         671          93.9%      2,584  20.3%   4.6x   48   7.2%      1.00       85.7%
  -----------------------------------------------------------------------------------------
  183 + 652 + 671 = 1,506 == the both-sides-linked LARGE population EXACTLY. No cell unexamined.
  median |predicted| on the EXACT control: 0.0000 bp in ALL THREE periods.
```

⛔ **I FIRST RAN THIS ON QTD ONLY AND REPORTED ITS RESIDUAL (24.0%) AS THE POPULATION'S.** It is
7.2% at 1Y. **I extrapolated a bound from a third of the data and was pessimistic by ~3x.** The
gradient is monotone and has a cause: a 42-day window often does not contain the flow whose
disagreement persists inside it. **The 1Y figure is the one to quote.** Same class as cycle 1's
failed prediction -- *a number measured on a subset and reported without its subset* -- and the
favourable direction is simply the instance nobody audits.

### 1b. The two-limb control -- the reason this is admissible

```
  CASH FLOW   76.5% vs 12.6%   6.1x    DISCRIMINATES
  FEE EVENT   95.1% vs 95.1%   1.00x   DISCRIMINATES NOTHING
```

**Fee events are near-universal in this book, so a fee explanation would have "explained" every LARGE
cell and every EXACT cell equally well and read as overwhelming confirmation at 95% coverage.**
The failed limb is the control for the surviving one, and it was not designed as one.
**General form: a hypothesis whose predictor is near-universal cannot be tested without a control
group -- its confirmation rate is the PREVALENCE, not the evidence.**

### 1c. Provenance of `|pred|` -- the question that would have made 1.00 circular

`3.0.0_SA_CVO` 91303 s.3 asked whether `|predicted|` is computed without reference to the observed
BD-vs-ours delta. **It is** -- `:61-64` build `alt` from our gold's `r_net`/`bmv`/`emv`/`cf_net`
alone; `:78-80` compute `pred = (our - alt)`; `delta_bp` is parsed at `:72` onto a **separate
structure** and read only at `:85-86` as `obs`. **The two series share no input.**

⭐ **A second property, not designed for:** `pred` is a DIFFERENCE of two quantities compounded by
the SAME code over the SAME rows, so any systematic offset between my compounding and the harness's
**cancels in the subtraction.** The result does not rest on my compounding being *right*, only on it
being *consistent*.

⚠ **The EXACT control does NOT settle circularity** (`3.0.0_SA_CVO`, adopted): `0.0000 bp` on
agreeing accounts is consistent with BOTH a genuine predictor and a delta-derived one, since the
delta is ~0 there. **It separates the predictor from NOISE, not from the OBSERVATION.** Only 1c does.

⚠ **The POPULATION is BD-selected** (`cls == LARGE`, `our_days == bd_days`) while the PREDICTED VALUE
is not. A conditional analysis, stated so no later reader rediscovers it as a flaw. Conditioning on
large `|obs|` would bias a noise predictor AWAY from 1.00; it lands at 1.00 in three windows of
different length.

---

## 2. PRECONDITION (iii) -- OUR SIDE IS ALREADY A RATIFIED CONVENTION

`docs/architecture/ADVI_PERFORMANCE_E2E_STANDARDIZATION_PLAN_20260806.md:110` @`27a096f40a`:

```
  flow_timing = eod_daily_twr   (AMENDED 2026-08-18, folded by 4.0.0_SA_CRO, GIPS field-contract owner)
     r(t) = [EMV(t) - CF(t)] / BMV(t) - 1  against Schwab EOD statement-close valuations
     carriers: POLICY_BLOCK.json flow_timing=EOD ; SPEC_49F_GROUP_C section 2 policy 1
```

**And the producer conforms, measured: `r_net == EOD` on 3,385 of 3,385 flow-days (BOD matches 6.0%,
the coincidental cases).**

> **THERE IS NOTHING TO REGISTER ON OUR SIDE. I asked the gate for permission to register a
> convention that was ratified on 2026-08-18.** That is exactly the laundering step 90838 s.3(iii)
> exists to refuse, and it caught mine.

⚠ **STILL OPEN: BD's convention is UNMEASURED.** Recomputing OUR window under BOD reproduces the
observed magnitude -- **consistent with BD using BOD, not establishing it.** That is vendor
documentation and no amount of our-side arithmetic answers it.

---

## 3. THE RESIDUAL -- AUDITED AGAINST MY OWN INSTRUMENT

My instrument has a fallback at `:64` (`base > 0`) that makes an instrument REFUSAL and a genuine
ABSENCE produce the same observable (`pred == 0`). Audited before quoting the residual again:

```
  per     pred==0   no flows   flows,refused(base<=0)   flows,cancels-to-0   check
  QTD          44         43                        0                    1      44
  YTD          57         56                        0                    1      57
  1Y           48         41                        1                    6      48
  ---------------------------------------------------------------------------------
  TOTAL       149        140                        1                    8     149
```

**140 of 149 are genuinely FLOW-FREE. Exactly ONE is my instrument refusing.** A first pass returned
**141** against the published **149**; the 8-cell gap is accounts whose flows compound to *exactly*
0.0 -- a third reason, and "141" would have been wrong in the direction that flattered my instrument.

### 3a. The residual in CELLS -- and a correction to my own caution

I flagged at 91341 that *"140 flow-free accounts is not 140 cells of the 1,506"* and declined to
quote a cell count. **Measured: the 149 was ALREADY a cell count** -- the loop iterates cells, not
accounts. The caution was sound in principle and **did not apply to my own number**.

```
  per   LARGE cells   residual   share   median |delta| bp
  QTD           183         44   24.0%          19.80
  YTD           652         57    8.7%          28.54
  1Y            671         48    7.2%          24.35
  ------------------------------------------------------
  TOTAL       1,506        149    9.9%
  distinct accounts behind those cells: 124
```

**The residual is 9.9% of P3's population, and its median |delta| is comparable to the whole
population's -- it is not a tail of small or large cells.**

### 3b. Why the residual is a THIRD mechanism

**140 cells have NO cash flow at all in the window, day counts agree with BD exactly, and the return
still lands LARGE.**

```
  day-count deficit   CANNOT touch them -- our_days == bd_days by selection
  flow placement      CANNOT touch them -- there is no flow to place
```

Both named mechanisms are structurally incapable of explaining these -- **not because the evidence is
weak, but because the inputs they operate on are absent.**
**UNTESTED CANDIDATES, named and NOT asserted:** a valuation difference (`bmv`/`emv` vs BD's marks),
fee/accrual treatment on the net leg, compounding/rounding. **Naming a candidate is not evidence.**

---

## 4. WHAT IS NOT CLAIMED

No reserved word appears above. NOT established: BD's flow convention; why 14.3-21.6% of movers
disagree in sign; any cause for the 149-cell residual; prediction (c) (single-period accounts carry
their flow inside that window) is **UNRUN**.
**No convention registered. No producer fix. No vendor call** -- every figure is landed bytes, git
objects, one S3 head-object and gold reads.

⚠ **PERISHABLE.** twr_daily history read at 541 partitions (was 540 at cycle 1); the xref moved from
`date=2026-08-28` to `date=2026-08-31` mid-cycle. **Every figure is stamped to this read.**
⭐ That move became a free control: QTD output was **byte-identical across both xref partitions**
(183 accts / 76.5% / 44 zero-sensitivity / ratio 1.00 / sign 78.4%), so nothing here depends on which
partition was read.

## 5. COMPILER TOOLS

| tool | use | result |
|---|---|---|
| `comp-find` | the ratified `flow_timing` convention; `c00-FIX` status | found `:110 @27a096f40a` -- the line that answered precondition (iii); denominators printed |
| `comp-read` | `advi_bdparity_w2_runner.py` | surfaced `latest_xref_key`/`derive_cohort` -- the documented join route, instead of a guessed key |
| raw `aws s3api` | `head-object` on the served harness + `c00_flow_ledger.py` | the only plane that could falsify M1 and P2-5's condition; `s3api` for UTC |
| `git show` by content | 3 commits + negative controls, twice | rule 22a -- deployed bytes vs BUILD INPUT, never by filename |
| `.tools/commit-gate.sh` | both committed instruments | BLOCKED twice (unused import, 2 compound statements); fixed, re-run clean |

**Not run:** `comp-pipescript io/deployed/postdeps`, `comp-validate` -- this cycle deployed nothing,
ran no gold script and produced no served artifact. They bind on the cycle that takes a disposition.
