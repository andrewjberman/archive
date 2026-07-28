# G7 -- Cottonwood pair/slice generation-gap review + the Finding-A mechanism

**Author:** 0.4.0_DS_ClientPlatform · **Gate:** 1.0.0_SA_CTO · **Date:** 2026-07-28 ~23:4xZ
**Scope:** repo `data/assets/scripts/gold/build_cottonwood_mdpf_{pair,slice}.py` vs the
S3-deployed copies at `s3://opal-data-mdpf/code/scripts/assets_gold/`. Architectural review,
not a sync. All comparisons on `diff --strip-trailing-cr`; every claim grounded on a live
read tonight. **Deploy freeze honoured: nothing here was deployed; recommendations gate on CTO.**

## 1. The "976-line generation gap" was a diff-instrument artifact

Raw `diff` counts CRLF-vs-LF as every-line-changed. Normalized:

| script | deployed (vintage) | repo (HEAD) | real gap |
|---|---|---|---|
| pair | 490 lines, 22:50:07Z tonight (tolerance-patched) | 494 lines @1893366183 (07-23) | **26 lines, 2 blocks** |
| slice | 386 lines, 07-23 10:55:23Z | 450 lines @bb3267fa57 (W-2b, 07-23 16:25) | **80 lines, substantive** |

Control-the-retrieval note for the record: the recorded "976" entered the record from an
un-normalized diff and survived three sessions. The gap is real; the magnitude was the
instrument's.

## 2. PAIR -- no architectural fork; a clean two-way UNION merge (CTO ruled the form, 234057Z)

Exactly two divergent blocks, each generation ahead on one:
- **Repo-only:** the Andrew-direct 134545Z two-source basis correction --
  `BASIS = "bd-rebalancer-models + bd-datamining-values"` + `COTTONWOOD_BASIS_DETAIL`
  emitted in both artifacts' meta. The deployed copy still says `bd-datamining-holdings`
  (names only the value source; sovereign-corrected label).
- **Deployed-only:** the CTO 224741Z identity-(i) tolerance recal (0.01 -> 0.02 + per-run
  delta logging), recorded divergence @16ed33b6c6. **This block is load-bearing:** tonight's
  WO-1 run logged delta 0.0100 -- exactly AT the old boundary. The repo copy deployed as-is
  could have refused tonight's pair.

**Resolution (AFTER tomorrow's fires, my Rule-13 cycle, CTO gate):** UNION -- repo basis
correction + deployed tolerance block, both provenances cited in the merged source.

## 3. SLICE -- the substantive gap, and it is HALF of one defect with Finding A

Repo carries W-2b (PRD @e1d525341, three-quantity convention): `holdings_total_by_date`
(measured SUM('Market Value') per fact_holdings partition -- keyed by the HOLDINGS date),
`partner_custody_total` = that measured series, `non_model_aua` = BALANCE (total - model,
both-legs-present only), + a W-2b identity gate. Deployed copy predates all of it and emits
all-None totals. Repo generation wins architecturally; BUT see 4 -- the model-value date
semantics are defective in BOTH generations, so the W-2b alignment and the Finding-A fix
must be designed as ONE slice change (CTO's instinct confirmed: they are one defect family).

## 4. FINDING-A MECHANISM -- source-confirmed, three stacked causes, one root

**Symptom:** fresh slice (22:54:48Z) value frontier 07-22 while its own silver reads
holdings 07-24 / allocations 07-27 / roster 07-28.

**Root: a two-date fact forced onto a one-date key.** `build_dim_model_portfolio` (dispatch
`:523`) writes ONE partition per run at `date=<ASSIGNMENT date, same-day>` whose values are
as-of `value_date` (latest holdings <= assignment). The partition parquet CARRIES BOTH
COLUMNS (measured tonight):

```
dim date=2026-07-21: assignment 07-21, value_date 07-20, opal $125,618,015.02
dim date=2026-07-22: assignment 07-22, value_date 07-20, opal $125,618,015.02  <- SAME snapshot twice
dim date=2026-07-28: assignment 07-28, value_date 07-24, opal $126,377,399.72  <- tonight
```

The slice (both generations) then keys `covered` on the PARTITION date and stamps values at
it. Three consequences, each measured:
1. **False vintage in the existing artifact:** the slice's two "measured" dates 07-21/07-22
   are BOTH the 07-20 holdings snapshot, forward-dated 1-2 trading days. (My aggregate carry
   label `as_of=2026-07-22` inherits this -- the true vintage is 07-20.)
2. **The 07-23..07-27 dim hole is the `:523` IAM-outage scar** -- runs died at `:523` before
   tonight's grant, so no partitions landed. Backfillable from silver history (holdings
   partitions exist through 07-24, assignments daily).
3. **The axis clip hides tonight's data entirely:** the only fresh partition is
   `date=2026-07-28`, but the slice spans the global axis, which ends 07-27 -- so
   `covered = [d for d in dates if d in gold_by_date]` EXCLUDES it, and the fresh
   $126.38M-as-of-07-24 is invisible. Frontier stays 07-22. **The IAM fix was necessary and
   is working; it was never sufficient -- this is the NEW defect the directive's second
   branch anticipated.**

**Same class as Amendment 5's diagnosis** (same-day assumptions encoded against T-1/D+2
reality), one layer down: the gold key asserts same-day; the data inside is D+2.
**Same defect as the DDB `cottonwood_bd_models` 2-of-447 all-None class** (CTO 234057Z
rhyme, confirmed): every consumer downstream of this slice sees exactly the 2 covered
dates, however fresh the run.

## 5. Proposed fix design (ONE slice change; CTO gates; execute AFTER tomorrow's fires)

1. **Key model values at the partition's OWN `value_date` column** (read from the parquet,
   never inferred from the key). Covered set = distinct value_dates. Collisions are real
   (07-21+07-22 both value 07-20): dedup rule = per value_date take the LATEST
   assignment_date's partition, assert dollar-equality across collapsed partitions
   (identical tonight; a mismatch is a real drift finding, reported not averaged).
   `assignment_date` rides per-row provenance/meta -- two dates, both ride (the pair
   already obeys this; the slice joins it).
2. **W-2b alignment rides the same edit** -- its holdings totals are ALREADY value-date-keyed,
   so re-keying model values makes the two series share one honest axis and the W-2b
   identity gate becomes meaningful at the frontier.
3. **Dim backfill 07-23..07-27** (assignment dates; values will roll to their true holdings
   vintages) -- re-emit from historical inputs per the standing backfill law; dispatch/AE
   coordination, not a slice edit.
4. **Pair UNION merge** (sect. 2) in the same post-fires window.
5. **End-state observable:** slice frontier lands AT the holdings silver frontier by
   construction (run-date independent); the aggregate's carry then operates on TRUE
   vintages (tonight it would carry as_of=07-24, age 1, $126,377,399.72 -- inside window 3
   honestly rather than via a forward-dated label).

## 6. What tomorrow's 15:00Z run will show WITHOUT any of this (freeze-compliant baseline)

The chain will rebuild dim at date=07-29 (values as-of holdings frontier), the slice will
still clip it if the axis ends 07-28, and covered stays {07-21, 07-22} -> the aggregate
carries from labeled 07-22 (true 07-20) while the pair/aum_metrics sit at the true holdings
frontier. Expected and understood -- the evidence run proves the SCHEDULE (D2), not this
defect's fix.
