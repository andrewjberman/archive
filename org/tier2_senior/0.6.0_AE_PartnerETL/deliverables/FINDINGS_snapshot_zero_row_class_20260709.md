# Snapshot zero-row / value-absent defect class — findings + proposed guards

**archetype:** DIAGNOSE
**Author:** 0.6.0_AE_PartnerETL
**Date:** 2026-07-09 (written inside the 02:00Z cot/bd P0 window)
**Ratified by:** 1.0.0_SA_CTO (200747Z, 202240Z) — items 1 and 2 assigned to DS's script lane (Rule 13);
items 3 and 4 found while grounding, routed here for a lane call.
**Grounding standard:** every number below is a live artifact read or a source line. No ad-hoc gold was run
(NEVER #4). Nothing was written to S3. The BD probes were GET-only.

---

## 0. The class, in one sentence

An instrument reports confidently on something other than what it claims to measure, and the null it emits is
produced by two different worlds — one healthy, one broken.

Tonight's instances, all on the same data path:

| # | Check | Passes on | Actually means |
|---|---|---|---|
| 1 | `s3_object_exists(silver/allocations/{d})` | a 0-row stub | "a file is there", not "there is data" |
| 2 | `bytes > 30KB` | a 0-row 94-col parquet (46,277 B) | schema is big, rows are zero |
| 3 | `sorted(keys)[-1]` | the newest **stub** | newest name, not newest data |
| 4 | `row_count > 0` | 11,754 rows at `nzf = 0.0000` | rows exist, values do not |
| 5 | a latched CloudWatch ALARM | silence | cannot re-notify; silence is the rail, not the state |
| 6 | `cloudtrail lookup-events` on the PutObject | an empty result | the `opal-data-bd` data-event selector is `readWriteType = ReadOnly` — the write was **never captured**, not "never happened" |
| 7 | `grep -c '\`'` on a commit message | `0` | never written, **or written and executed away** |
| 8 | `gap_pct` inside its historical band | two operands degrading together | a ratio is stable while both sides die (§2) |
| 9 | a `SKIP` from a guard that fails closed | total silence | **a control that fails closed and silently is indistinguishable from a control that never ran** |

**The discriminating question is never "did I see nothing." It is "would I have seen something, had there been
something to see?"** Every instrument used below was given a positive control before it was allowed to report.

**And the corresponding test on any proposed REMEDY** (CTO 210135Z, adopted as a standing check):

> **The locally-correct fix is often the destructive one. The tell: it turns a red thing green without changing
> the underlying truth.**

Two proposals tonight failed that test — reaping `bd-allocation-processor` (§4), and repointing the `C_02` picker
at the latest non-empty partition (§3). Both would have turned a red signal green. Neither moves the truth.

---

## 1. `_ingest_one` needs a per-table VALUE floor — not just a row check

**Lane: DS (script).** `data/cot/scripts/bronze/cot_bronze_ingest.py`

`SNAPSHOT_TABLES = {holdings, allocations, unrealized}` are 0-row-REJECTED pre-write at `:711`. That is a **row**
test. Only `holdings` has a second gate — the non-zero-market-value floor at `:730-735`
(`HOLDINGS_COMPLETENESS_FLOOR = 0.50`, `:478`). **`allocations` and `unrealized` have no value gate at all.**

Measured live tonight against BD, COTTONWOOD tenant:

```
holdings  as-of 2026-07-09 : 11,754 rows   604,077 B   nzf = 0.0000  ( 0.00%)  -> floor REJECTs (correct)
holdings  as-of 2026-07-07 :               856,067 B   nzf = 0.8364  (83.64%)  -> lands (correct)
```

**Exactly zero valued positions across 11,754 rows.** `row_count > 0` passes that table. Only the nzf floor
catches it. This is not hypothetical — it is the current state of BD's holdings export for 07-09, and that floor
is the single thing standing between it and a served AUA. It is also why cot's served AUA is *stale, not corrupt*.

The exposure: `allocations` feeds `certified_aua` via `account_market_value`. A rows-present / value-absent
allocations export would pass `:711`, land, reach silver, and be certified.

### Proposed change

`SNAPSHOT_TABLES` should mean **row-checked AND value-checked**, with the value column declared per table:

```python
SNAPSHOT_VALUE_COL = {
    "holdings":    "market_value",           # already enforced via _holdings_nonzero_mv_fraction
    "allocations": "account_market_value",   # C_02's certified_aua basis
    "unrealized":  None,                     # no cert dependency; row check only (see note)
}
```

Reject pre-write when the value column is present and its non-zero fraction departs from the tenant's normal
envelope (§5). Fail-OPEN on an unparseable/absent value column — never reject on uncertainty; that is the existing
`has_data == -1` posture and it should be preserved.

**Pairs with DS's `ADVI_COTETL.AUAFIX-L6` snapshot-zeroed exclusion rule.** They are different layers and both are
needed: the exclusion rule stops a zeroed snapshot from being **trusted** downstream; this stops a valued-zero one
from being **written** at all.

---

## 2. `C_02` computes `gap_pct` and throws it away

**Lane: DS (script).** `data/black_diamond/scripts/gold/C_02.client_performance.py`

```
:326  certified_aua = float(silver.loc[~excl_mask, 'account_market_value'].sum())
:331  if certified_aua <= 0:  SKIP   # shuts the ALL-ZERO door only
:334  gap_abs = certified_aua - gold_aua
:335  gap_pct = gap_abs / gold_aua
:337-347  cert = {..., 'gap_pct': ...}; s3.put_object(...)      # WRITTEN
:348  log(f'... gap_pct={gap_pct:+.4%}')                        # ONLY LOGGED
```

- Rows land **all-zero** → sums to 0 → `<= 0` → SKIP. Guarded (the 2026-06-30 BRANCH-A floor).
- Rows land **partially valued** → `certified_aua` is **positive but understated** → sails past `<= 0` →
  cert written, `put_object`'d, served. **Client-facing, positive, wrong.** Strictly harder to see than a $0 cert.

`gap_pct` is *the exact quantity that detects that state*. It is computed, serialized into the cert, logged, and
**enforced nowhere**. The defect and its detector are three lines apart.

### Proposed change
`|gap_pct|` beyond a **calibrated, signed** threshold → **SKIP + alarm**, not `log()`. Hold last-good.

### RE-SCOPED (CTO 210135Z, after I calibrated it): `gap_pct` is a CERT-QUALITY guard. It is **not** a partial detector.

I built the 02:30Z harness, dry-ran it, and it flagged the last **healthy** cert as understated. So I measured the
distribution before relying on it:

```
  n = 70 certs      min = -3.0971%     max = +11.6661%     median = +2.2219%
  2026-06-11..06-18 :  +1.32% .. +1.65%     (scrape era)
  2026-06-24..07-02 :  +5.42% .. +11.67%    (recent, HEALTHY)
```

Three reasons it cannot be the partial detector:

1. **A symmetric `|gap_pct| > 2%` band false-alarms on every recent healthy cert.** I picked 2% from nothing — a
   threshold sized on no baseline. The same error as the flat `nzf >= 0.95`, repeated ninety minutes later on a
   different quantity. *Knowing the lesson did not prevent it. Calibrating did.*
2. **The sign is backwards.** A partial *understates* `certified_aua` → `gap_pct` goes strongly **negative**.
   Healthy certs are strongly **positive**, and the historical floor already reaches **-3.10%**, so a mild partial
   lands inside the known-good band and passes.
3. **The fatal one — it is measuring the wrong operand:**
   ```
     06-18  certified 1,853,454,815.85   gold 1,829,248,213.41   +1.32%
     06-24  certified 1,815,151,730.66   gold 1,714,581,760.81   +5.87%
            certified barely moved.  GOLD FELL ~$115M.
   ```
   The gap widened because the *other* operand degraded. And the two operands **share an upstream failure**: the
   same 0-row stubs null `account_type` in `A_00`'s `accounts_dimension`, which feeds **both** `C_02`'s liability
   exclusion **and** the gold side.

> **GENERAL FORM (bank this): a comparison is only a detector if its operands fail INDEPENDENTLY.**
> Two quantities that degrade together produce a stable ratio while both are dying. **The gap looks healthiest
> precisely when the failure is total.**

**The 02:30Z primary is therefore the direct `nzf` + `sum` read on the landed `silver/allocations/{data_date}.parquet`**
against the tenant envelope (§5): it binds the property the cert depends on, it shares no operand with gold, and it
is the only instrument here with a validated positive control. `gap_pct` is recorded, never decisive.

COO's catch stands — a computed-and-discarded quantity in an artifact *is* a finding. **Re-scope its claim, do not
discard it.** It catches a cert diverging from gold for *any* reason; it never catches a partial.

---

## 3. `C_02:310` asks "does the file exist" where it must ask "does the file have rows"

**Lane: DS (script). Found while grounding COO's 07-08 partition question. This one is load-bearing tonight.**

```
:306  data_date  = result['date'].max()                      # max date in client_performance
:309  silver_key = f'silver/allocations/{data_date}.parquet'
:310  if not s3_object_exists(s3, S3_BUCKET, silver_key):  SKIP
```

Live state of the 49F plane, row-counted (never bytes):

```
  07-01  6,828 REAL 94col       07-06      0 STUB 94col
  07-02  6,833 REAL 94col       07-07      0 STUB 94col   <- client_performance.date.max() TODAY
  07-03      0 STUB 94col       07-08  6,870 REAL 92col   <- the ONLY real recent partition
  07-04      0 STUB 94col       07-09      0 STUB 94col
  07-05      0 STUB 94col
```

The 07-07 stub **exists**. The absent-guard passes. C_02 reads it, sums `account_market_value` to `0.00`, hits the
`<= 0` floor, SKIPs, writes no cert — and `D_00._resolve_served_aua` BRANCH-A holds the last-good certified value,
**$1,837,159,865.68, frozen since 2026-07-02.**

That is *why* certifications stop at `2026-07-02.json`: **`data_date` walked into the stub range on 07-03 and never
came out.** Mechanism confirmed against the artifacts, not assumed.

Both branches, computed on the real bytes:

```
  data_date = 2026-07-07 -> certified_aua =             0.00 -> SKIP -> FROZEN
  data_date = 2026-07-08 -> certified_aua = 1,844,022,461.17 -> cert written -> UN-FREEZE (+6,862,595.49)
```

`1,844,022,461.17` is penny-identical to `0.4.0_DS~B`'s independent C_02 simulation.

### Proposed change — and the remedy is NOT the same as `A_00`'s

`:310` must assert **`row_count > 0`**, not `exists`. But what it does on failure differs by artifact kind, and
this distinction is load-bearing (CTO ruling 204424Z, correcting my first proposal):

> **For an ENRICHMENT: substitute, with provenance and a max-age bound.**
> **For a DATED CERTIFICATION: ABSTAIN + alarm. A cert may never borrow a value from a date it does not claim.**

- `A_00` enriches a **dimension**. Substituting the latest non-empty allocations partition — carrying provenance
  and bounded by a max age — is acceptable, because an enrichment asserts no date.
  (`A_00:337 latest_key = sorted(alloc_keys)[-1]` today selects the 07-09 stub and nulls `account_type`.)
- `C_02` writes a **dated certification**: *"as of `data_date`, certified AUA is X."* Silently sourcing 07-08's
  allocations while `data_date` reads 07-07 would emit a cert that is **internally false** — right number, wrong
  date — and it would pass every check we have. So `C_02` must **ABSTAIN + alarm**, never substitute.

The real defect is upstream: `data_date` (the performance frontier) walked into a stub range on 07-03 and never
came out. **That is the thing to fix; the abstain is what makes it visible instead of silent.**

### CORRECTION (MSTR 205418Z, source-refuted by DS `b8ee3a08a`) — and it is better than what I wrote

`C_02:331`'s `certified_aua <= 0` floor **already fires**, and its log line already prints the row count. So
**`C_02` fails closed. It is the guard working, not the guard missing** — and fixing the `:310` proxy un-freezes
nothing.

Worse, the "obvious" repair is destructive. Repointing the picker at the latest **non-empty** partition selects
07-08 (6,870 rows) while `gold_aua` still derives from 07-07 — `:306-307` co-derive both. A cert lands, the freeze
visibly ends, and **the artifact keyed `{07-07}` carries a 07-08 number. It lies about its own as-of.**
(And the `+$6,862,595.49` is **real market flow**, not an error being corrected.)

That is the same species as reaping `bd-allocation-processor`: **the locally-correct fix is the destructive one.
The tell, both times: the "fix" turns a red thing green without changing the underlying truth.**

**THE REAL DEFECT: the SKIP is silent and unbounded. Nothing watches for cert ABSENCE.**

Seven days passed with no certification written and no signal, because `data_as_of` kept advancing while only the
*value* was dead. The system correctly refused to certify garbage — and then said nothing about refusing, for a
week, on a client-facing number.

> **A control that fails closed and silently is indistinguishable from a control that never ran.**

This is the session's through-line arriving from the opposite direction: not an instrument reporting what it did
not measure, but an instrument measuring correctly and **reporting nothing at all.**

**So the watcher goes on the guard FIRING, not on the picker:**
```
  alarm when: no gold/validation/aua_certification/{d}.json exists for the current performance frontier
              (i.e. C_02 ran and SKIPped) for N consecutive runs
  the SKIP must be LOUD and BOUNDED: emit a metric/alarm on the skip path itself, not only a log line
  C_02:310 -> row_count > 0 else ABSTAIN + ALARM (the abstain is what makes the refusal visible)
```
Cert **absence** is the signal. It was available for seven days and nobody was listening for it.

**Consequence if unfixed:** the un-freeze fires **iff** the chain lands `data_date` on exactly 2026-07-08. One day
either side is a stub. Tomorrow `data_date` is 07-09 → stub → **the freeze returns**.

### Where `data_date` lands is MEASURABLE, not a guess — and the answer inverts the intuition

`data_date` is txn-anchored: `A_03:1545 global_end_date = unit_events['trade_date'].max()`. Confirmed on live data
— `trade_date.max()` today is **2026-07-07**, and `client_performance.date.max()` is **2026-07-07**, exactly.

The lag from partition-date to `trade_date.max()` **changed regime**, so extrapolating it is unsafe:

```
  06-29..07-06 partitions (scrape era) : trade_date.max() == partition date   (lag 0)
  07-08, 07-09 partitions (REST era)   : trade_date.max() == partition - 2    (lag 2, n=2)
  07-07 partition                      : 0 ROWS (empty)
```

So instead of extrapolating from n=2, ask BD (read-only, single-day `Custom` windows ≤3d to avoid the 14d
heavy-query error), 49F tenant, measured 2026-07-09T21:00Z:

```
  transactions trade_date 2026-07-08 : rows = 4,204  ->  POSTED
  transactions trade_date 2026-07-09 : rows =     0  ->  NOT POSTED
```

⇒ tonight's pull sees `trade_date.max() = 07-08` ⇒ `perf.date.max() = 07-08` ⇒ `C_02` reads the **real** partition
⇒ **the un-freeze fires.**

**THE INVERSION — this is the state to guard:**

| BD posts 07-09 txns? | allocations 07-09 | `perf` lands | `C_02` reads | outcome |
|---|---|---|---|---|
| **NO** (state at 21:00Z) | n/a | 07-08 | REAL, 6,870 rows | **UN-FREEZE** |
| **YES** | 0-row STUB (runner REJECTs it at `:711`) | 07-09 | the STUB | SKIP → **STILL FROZEN** |

The runner's reject guard means allocations 07-09 **cannot** land tonight. So if BD posts 07-09 **transactions**
before 02:00Z, the performance frontier steps onto a date whose allocations partition is a stub, and the freeze
holds.

> **More data breaks the un-freeze.** The transaction feed advancing is normally the healthy signal; tonight it is
> the failure mode. The observation that means "progress" and the observation that means "regression" are the same
> observation.

Same ET root, wearing a different coefficient: a 00:00Z pull asks BD for a date that has not posted in ET.

---

## 4. `lag=1` silently changed WHICH converter produces snapshot silver

**Lane: 0.6.0_AE (runner infra). NOT touched tonight — it is the 02:00Z runner.**

```
  bd-49f-runner :137-138   "Both the idempotency check and the sentinel must key off `end`, not run_date,
                            or they look for a file the pull never wrote."
  bd-49f-runner :206       mod.emit_bronze_sentinel(run_date, landed)        <- passes run_date
  bd-silver-merge :57-63   derives its date from the sentinel PATH bronze/{date}/_BRONZE_COMPLETE.json
```

With `BD_SNAPSHOT_ASOF_LAG_BDAYS=1`, a snapshot table lands under **as_of** while the sentinel carries **run_date**.
The canonical converter therefore goes looking for `ALLOCATIONS_DAILY_{run_date}.xlsx` — a file the pull never
wrote — and **never converts the real as_of file.**

The only thing that converts it is the legacy `bd-allocation-processor`, which is triggered by the raw xlsx S3
event (`prefix=forwardfill_v2/allocations/ suffix=.xlsx`) and keys its date off the **filename**.

Live timeline, 2026-07-09:
```
  09:13:23Z  bd-49f-runner (lag=1) lands ALLOCATIONS_DAILY_2026-07-08.xlsx   (12,935,870 B, REAL)
  09:14:13Z  bd-allocation-processor writes 92-col silver/allocations/2026-07-08.parquet
  09:14:57Z  runner emits bronze/2026-07-09/_BRONZE_COMPLETE.json            (run_date, not as_of)
```

**Attribution is reproduced, not inferred.** Running BD's real 07-08 export through `pd.read_excel` +
`bd-allocation-processor:62` (`col.lower().replace(' ','_').replace('.','_')`) + its `:74` rename yields **all 92
observed columns in exact order**, including the pandas duplicate-header fingerprint (`Flat Fee.1` →
`flat_fee_1`). No other path in the estate produces that.

**So the "shape anomaly" is currently the only producer of real 49F allocation silver.** Deleting the legacy
processor — the obvious cleanup — would remove the un-freeze.

### Shape is consumer-INERT (verified per consumer)
```
  C_02  needs account_type + account_market_value  -> both present in the 92-col file. VERIFIED on bytes.
  A_03  returns set() unless account_id + account_is_open present. Tolerant.
  A_00  takes alloc[available] (intersection). Tolerant.
  A_01  DOES NOT READ silver/allocations AT ALL.
```
`comp-pipescript io A_01` lists 4 reads, none of them `silver/allocations`. Its only three `alloc` strings are
docstring lines (`:18`, `:19`, `:29`, claiming `fee_bps` "from latest allocation"). Discriminating check, because a
0-hit grep proves nothing on its own: the same grep returns **7** hits for `silver/transactions`, and `SPLIT_COLS`
(`:74-76`) are documented at `:69` as *"names in silver/transactions/"*.

**Therefore the raw `*_split_%` column names cannot break advisor attribution.** `0.4.0_DS~B`'s INFERRED is now
SOURCE-CONFIRMED. `A_01`'s docstring is a false record.

### Proposed change
Emit the sentinel keyed on the snapshot `end` (as_of), or have `bd-silver-merge` read the per-table `as_of` map the
runner already returns (`:215 "as_of": {t: a for t, a in landed}`) instead of parsing the path. Until then the
canonical converter is permanently one day off for snapshot tables whenever the lag is on.

---

## 5. Threshold doctrine: measure NORMAL, not ABNORMAL

**CTO ruling 202240Z**, replacing a flat `nzf >= 0.95`:

> We can measure NORMAL. We cannot measure ABNORMAL — we have never seen a partial. So the abort condition must
> not be a classifier for "is this a partial." It must be an **anomaly detector against a tight baseline**: "is
> this consistent with a normal day?" If not → abort.

The decision is asymmetric: a false abort costs one more frozen night (the status quo); a false pass costs a
positive, plausible, **wrong** client-facing AUA. **Bias hard toward abort.**

Baselines measured live tonight, `allocations`, four known-good days each (as-of 07-02 / 07-06 / 07-07 / 07-08):

| tenant | nzf range | spread | sum band |
|---|---|---|---|
| cot | 0.9986 – 1.0000 | 14 bp | $814.51M – $818.51M (±0.25%) |
| bd (49F) | 0.9727 – 0.9736 | 9 bp | $9.6077B – $9.6716B (±0.34%) |

Two different populations: bd carries ~2.7% structurally zero-value (closed/dormant) accounts; cot ~0.1%. **A
single cross-plane constant was always going to be wrong for one of them.** `0.95` sits 4.9pp below cot's floor and
2.3pp below bd's, against spreads of 14bp and 9bp — it cannot fire on a partial leaving 96–99% of accounts valued,
which is the only case it exists for. It was sized to catch the failure already seen (`nzf = 0`), not the one
identified as dangerous.

**Envelope in force:**
```
  proceed ONLY if:  rows > 0
                AND nzf  >= tenant_baseline_min - 0.005     (cot >= 0.9936,  bd >= 0.9677)
                AND |sum - tenant_median| / tenant_median <= 0.02
  anything else with rows > 0 -> ABORT + page CTO.   0 rows -> stays armed; rejects at :711.
  keep nzf >= 0.95 as an absolute backstop -- a floor, not the discriminator.
```

Validated in both directions before being allowed to govern anything: all 8 known-good days PASS (no false abort);
five synthetic abnormal states ABORT, including the two the old 0.95 floor waved through (49F at 96%, cot at 99%),
and one caught by the **sum** co-signal alone while `nzf` passed. Two independent statistics beat one.

**Caveat retained:** n = 4 normal days per plane, **zero observed partials**. The alarm side of the threshold is
extrapolated from the normal side. Enough to establish that 0.95 is loose; not enough to certify any specific
replacement. Sizing it properly needs a real partial or a vendor statement on settlement semantics.

---

## 6. Instrument discipline that produced the above

- **Positive control before trusting any instrument.** The value-probe was validated on a known-good day
  (`cot 07-08 → 1,441/1,441 nonzero, 100.00%`) before it was allowed to report on an unknown one.
- **Never a second probe.** The BD probe imports the *real* `cot_bronze_ingest` module and switches tenant by env,
  exactly as `bd-49f-runner:54-57` does — so auth, template, `_window_for` and the row-probe are the runner's own
  code paths. Two independently-written probes would compare two *instruments* when we mean to compare two
  *tenants*.
- **Ground applied state, not declared state.** `ssm.tf:58` claims the trigger Lambda passes `DryRun`; the deployed
  zip (`CodeSha256 7dJLylE7psMM95J8Y8vxhckpX9aNIidvh9ZY7Du7mu0=`) contains zero `Parameters` and zero `DryRun`
  refs. The comment justifying a live booby-trap is itself false.
- **A 0-hit grep proves nothing on its own.** Absence of a match and absence of the instrument look identical. Ask
  instead: *would I have seen something, had there been something to see?* (Same error as reading a latched
  alarm's silence as health — all five bd staleness alarms have been latched in ALARM ~67h and structurally cannot
  re-notify.)

---

## 7. Status of each item

| # | Item | Lane | State |
|---|---|---|---|
| 1 | `_ingest_one` per-table value floor | DS (script) | ratified by CTO; spec above |
| 2 | `C_02` `gap_pct` enforcement | DS (script) | ratified by CTO; wanted tonight even if it lands next week |
| 3 | `C_02:310` `exists` → `row_count > 0`; latest-non-empty selection | DS (script) | **new; load-bearing for L6** |
| 4 | sentinel keyed on `run_date` vs `end` | 0.6.0_AE (runner infra) | **new**; NOT touched inside the window; awaiting CTO ruling on whether it lands before tomorrow's gold |
| 5 | strip both `DryRun` params + fix `ssm.tf:58` and the retry-net comment | 0.6.0_AE (doc/TF) | deferred post-window by CTO (a doc edit publishes a new SSM version and advances the default; the trigger resolves the default) |
