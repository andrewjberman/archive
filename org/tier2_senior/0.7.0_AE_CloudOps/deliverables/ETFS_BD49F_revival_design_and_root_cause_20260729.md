# bd-49f-etf-ownership-daily REVIVAL -- root cause + writer/trigger design

**Author:** `0.7.0_AE_CloudOps~A` · 2026-07-29 ~0125Z
**Authority:** Andrew-direct ~0107Z + ~0113Z (verbatim in COO 011043Z / 011436Z; COO recorded) --
"AE~A makes sure the writer is hooked up properly ... im not sure why ingestion stopped on
07-06-2026, need to see whats up with that certainly."
**Status: DESIGN + ROOT CAUSE ONLY. Deploy freeze holds (CTO 234106Z). No apply, no deploy tonight.**
Same no-`infra/`-edits discipline as the Design-A deliverable (4c early-activation hazard); the diffs
below land as the executing commit in the post-freeze apply window, which I own (COO 011043Z item 4).

---

## 1. ROOT CAUSE OF THE 07-06 STOP -- source-confirmed, two causes compounding

**Answer to Andrew's question: ingestion did not stop. It was never started, and the last hand-fire
hit a frozen source's frontier.**

**(a) The producer was NEVER SCHEDULED -- by explicit design, not by omission.**
The TF landing commit is the primary source: `349c91e35b` (2026-06-25, `0.5.0_AE_OpalETL`), verbatim:
> "**NO event trigger (S-D2 monthly batch, rides next Schwab batch)**"

The TF file declares role + policies + module ONLY -- no rule, no permission, ever (full resource
census of `bd-49f-etf-ownership-daily.tf`; also zero `aws_cloudwatch_event_rule` for this function
anywhere in `bd-pipeline/*.tf`). So COO's "no rule AND no resource policy" is not decay -- it is the
W2 design: a hand-fired batch producer. **"It stopped" and "it was never started" are different
defects; this is the second.** Every slice ever written came from manual invokes:
`daily/49financial/` write-time clusters are exactly three -- 06-25 13:42-16:13Z (vintages
05-01..06-24, the W2 landing backfill), then 07-14 05:12Z (vintages 06-25..07-06), nothing since.

**(b) The 07-14 hand-fire reached vintage 07-06 because the SOURCE was frozen there.**
`opal-data-bd/schwab/silver/rps/` partition write-times (head-object, per object):
- `date=20260707`..`date=20260713` -- all written **2026-07-16T05:42Z** (one batch)
- `date=20260721`..`date=20260723` -- all written **2026-07-24T15:44Z** (one batch; the recorded
  49F Schwab RPS freeze resolution -- silver rolled to 07-23 on 07-24)

So on 07-14T05:12Z the newest partition that EXISTED was `date=20260706`: the hand-fire correctly
walked to the then-frontier and stopped. The producer code did nothing wrong; nobody fired it again
after the source unfroze.

**(c) Downstream consequence (why this is money):** AVGCAP's calendar-day carry-forward turns this
gap into ~6 real days + ~25 carried days in July's 49F rebate basis, and carry-forward cannot
distinguish a weekend from a dead producer. DS~A is measuring the exposure; the backfill repairs the
past; **the schedule below is what prevents recurrence.**

**(d) The "two functions" question (COO 011436Z item 4) -- resolved live:** exactly ONE function
exists in Lambda (`aws lambda list-functions` census: `bd-49f-etf-ownership-daily`).
`bd-49f-etf-ownership-daily-canonical` is a REPO DIR ONLY -- a pre-staged TRUE-DAILY variant sourcing
BD `gold/canonical/holdings`, deliberately NOT deployed (`9e89b0d702`): its own record says the
canonical basis runs **~3.5-4.4% BELOW** RPS-monthly and needs a DS/DE/COO basis decision before any
flip. **This revival does NOT touch it** -- reviving W2 on the same RPS source is basis-neutral with
the backfill and with all history. The canonical flip stays a separate, explicitly-gated decision.
Trigger wiring below targets `bd-49f-etf-ownership-daily` and nothing else.

---

## 2. RECOMMENDED GO-FORWARD: re-source the writer to the monolith `fact_rps` (DS~A seam 012417Z)

**DS~A's backfill (15/15, 07-07..07-27, landed 012417Z) changed the best answer.** It sourced
`s3://opal-data-assets/schwab/08242234/silver/fact_rps/` (S1 position grain -- NOT `fact_rps_s2`,
the ticker-less S2 summary) and proved **28/28 exact-to-the-cent equivalence** against the existing
burst artifacts: monolith ≡ bd-tree silver on this quantity, so the re-source is **basis-neutral**.
The two sources are NOT operationally equal:

| | bd-tree `opal-data-bd/schwab/silver/rps` | monolith `fact_rps` |
|---|---|---|
| Cadence | EPISODIC -- AE-run conversion batches (measured: 5 partitions at 07-16T05:42Z, 3 at 07-24T15:44Z) | **METRONOME -- D+1 10:16Z ±4s daily incl Sat** (head-object verified: 07-24/25/28 all 10:16:0xZ) |
| Vintage holes | Multi-day batches -> the batch-vintage hole (§3.1) needs a per-partition accelerator + code parse | **None -- one partition per trading day, on schedule** |
| Route status | Depends on the 49-schwab-conv manual/OneDrive trigger upstream | The settled canonical route (49F AUA SOURCE = SCHWAB, monolith standing) |

**Design: floor-ONLY, `cron(45 10 * * ? *)` daily incl weekends** -- 29 min after the measured
10:16Z landing. No accelerator: `opal-data-assets` has **EventBridge DISABLED** (verified live;
only direct bucket->Lambda hooks exist), so an accelerator would require a monolith-wide bucket
config change for ≤29 min of latency on a metronome source. Not worth the blast radius; if the
landing time ever drifts, the floor emits the prior partition with honest `source_as_of` and the
next floor catches up -- the NEVER#4 property holds.

**Pieces:**
- **Writer body:** DS~A's `compute_slice` (`data/etfs/scripts/backfill/backfill_49f_daily_from_monolith_rps.py`
  @1667aa073d) is the ONE computation per CTO's one-producer law -- the Lambda embeds/imports it,
  never re-derives. Compute = DS lane; handler shell + deploy + trigger + IAM = mine. Function
  identity RETAINED (`bd-49f-etf-ownership-daily`, same role, same output contract
  `daily/49financial/{date}.json` schema_version 1.0, AES256, universe config-read).
- **Trigger TF:** 3 resources (floor rule + target + permission), same shape as Design A's floor.
- **IAM delta: ONE Sid** -- the live role today gets `implicitDeny` on the exact monolith key
  (single-arn simulate, tonight): add `GetObject` on
  `opal-data-assets/schwab/08242234/silver/fact_rps/*` + extend the ListBucket prefix condition.
  The write grant (`daily/49financial/*`) and firm-separation shape are already landed + exercised
  (§3.4). NOTE: this role is NOT on the fan-in fence (it never mutates the monolith -- read-only
  there; write goes to opal-data-etfs, which its own grants already scope).
- **First natural fire:** the 07-28 slice, next 10:45Z after apply (DS~A deliberately did not
  manufacture it -- correct; the first scheduled emit IS the acceptance evidence).
- **Retire-not-park:** on the first clean scheduled emit, the bd-tree read path retires from this
  producer (one producer per measured quantity), and `daily/_stage_49f_canonical/` +
  the undeployed `-canonical` repo dir fold into the retire/E-pass paperwork. The ~4% canonical
  basis decision stays parked and is untouched by this design.

**Price (recommended path):** +3 TF resources · 1 IAM Sid + 1 list-prefix extension · handler shell
edit (embed compute_slice; drop the bd-tree walk) · zero bucket config change · apply in my
post-freeze window, CTO gate, ledger + NEVER#6 discipline · verification = the 10:45Z fire's own
artifact (vintage 07-28+, cent-exact vs DS~A's cross-check for the shared date).

---

## 3. FALLBACK (original design, superseded in preference by §2): revive on the bd-tree source

### 3.1 Why a plain floor is NOT enough on THIS source (the batch-vintage hole)

The handler emits ONE slice per invoke: explicit `event["date"]` -> that partition, else -> the
NEWEST partition (`:121-134`). The upstream lands in MULTI-DAY BATCHES (measured: 5 partitions at
once on 07-16, 3 at once on 07-24). A newest-only floor (or newest-only accelerator) over a 3-day
batch emits only the max date -- **the intermediate vintages never get true slices, and AVGCAP
carries forward over days whose real values exist.** On a reporting surface that is a blemish; on a
rebate basis it is a wrong number with a correct-looking mechanism. The fix is per-partition
targeting, which needs the partition date from the S3 event key.

### 3.2 One SMALL ADDITIVE handler branch (fallback-path code change, ~8 lines)

EventBridge input transformers cannot substring a key, so the handler parses it. Additive, backward
compatible (explicit `date` and bare-invoke paths unchanged), before the `target_date` block:

```python
# ADDITIVE (revival 2026-07-29): an S3-via-EventBridge invoke carries the created
# object's key -- target THAT partition, so a multi-day batch landing emits every
# vintage, not just the newest (the rebate-basis batch-vintage hole).
if isinstance(event, dict) and not event.get("date"):
    _k = (((event.get("detail") or {}).get("object") or {}).get("key") or "")
    _m = re.search(r"date=(\d{8})/", _k)
    if _m:
        event = dict(event, date=_m.group(1))
```
(`import re` at top; `_norm_yyyymmdd` already accepts `YYYYMMDD`.) Idempotent overwrite semantics
unchanged; a re-delivered event converges.

### 3.3 TF diff (fallback path)

```hcl
# FLOOR (NEVER#4): daily incl weekends. 15:30Z = after the observed morning-class
# conversion landings (05:42Z measured 07-16) and before the 16:00Z
# etf-ownership-dashboard-daily read; afternoon-class landings (15:44Z measured
# 07-24) ride the accelerator below or the next floor. Upstream is EPISODIC
# (AE-run Schwab conversions), N=2 landings measured -- the floor is the freeze
# backstop with honest source_as_of, not the freshness vector.
resource "aws_cloudwatch_event_rule" "bd_49f_etf_ownership_scheduled_floor" {
  name                = "bd-49f-etf-ownership-scheduled-floor"
  description         = "Scheduled floor for the 49F ETF-ownership rebate-basis producer (Andrew-direct 2026-07-29 revival; NEVER#4 -- a revenue-basis producer with no schedule is a defect). Emits the newest available RPS partition daily; source_as_of carries the true vintage."
  schedule_expression = "cron(30 15 * * ? *)"
}
resource "aws_cloudwatch_event_target" "bd_49f_etf_ownership_scheduled_floor" {
  rule      = aws_cloudwatch_event_rule.bd_49f_etf_ownership_scheduled_floor.name
  target_id = "Bd49fEtfOwnershipScheduledFloor"
  arn       = module.bd_49f_etf_ownership_daily.function_arn
}
resource "aws_lambda_permission" "sched_floor_bd_49f_etf_ownership" {
  statement_id  = "SchedFloorBd49fEtfOwnership"
  action        = "lambda:InvokeFunction"
  function_name = module.bd_49f_etf_ownership_daily.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.bd_49f_etf_ownership_scheduled_floor.arn
}

# ACCELERATOR: per-partition, fires once per created date= partition so batch
# landings emit EVERY vintage (the 3.1 hole). opal-data-bd ALREADY has S3->
# EventBridge enabled (get-bucket-notification-configuration shows the
# EventBridgeConfiguration block live) -- NO bucket change needed.
resource "aws_cloudwatch_event_rule" "bd_49f_etf_ownership_on_rps_partition" {
  name        = "bd-49f-etf-ownership-on-rps-partition"
  description = "Accelerator: new RPS silver partition -> emit that vintage's ownership slice (handler parses date= from the event key). Floor above is the NEVER#4 backstop."
  event_pattern = jsonencode({
    "source"      = ["aws.s3"],
    "detail-type" = ["Object Created"],
    "detail" = {
      "bucket" = { "name" = ["opal-data-bd"] },
      "object" = { "key" = [{ "prefix" = "schwab/silver/rps/date=" }, { "suffix" = "data.parquet" }] }
    }
  })
}
resource "aws_cloudwatch_event_target" "bd_49f_etf_ownership_on_rps_partition" {
  rule      = aws_cloudwatch_event_rule.bd_49f_etf_ownership_on_rps_partition.name
  target_id = "Bd49fEtfOwnershipOnRpsPartition"
  arn       = module.bd_49f_etf_ownership_daily.function_arn
}
resource "aws_lambda_permission" "rps_partition_bd_49f_etf_ownership" {
  statement_id  = "RpsPartitionBd49fEtfOwnership"
  action        = "lambda:InvokeFunction"
  function_name = module.bd_49f_etf_ownership_daily.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.bd_49f_etf_ownership_on_rps_partition.arn
}
```

⚠ PATTERN CAVEAT to verify at apply: TWO match objects on `object.key` (`prefix` + `suffix`) is an
AND within one key only on newer EventBridge pattern semantics -- verify the landed rule matches a
real partition key with `aws events test-event-pattern` BEFORE trusting it; if it ORs, collapse to
the `prefix` match alone (suffix filtering is cosmetic here -- only `data.parquet` lands under
`date=` prefixes today, and the handler head-object-validates anyway).

### 3.4 What needs NO change -- each verified tonight, not assumed (holds for BOTH paths except as noted)

- **IAM: ZERO change.** Live inline `s3-etf-ownership` on `bd-49f-etf-ownership-daily-role` already
  grants exactly the revival's needs. Exercised (single-arn simulates, controls separate): read own
  RPS newest `date=20260723` **allowed**; write `daily/49financial/*` **allowed**; read universe
  config **allowed**; NEGATIVE firm-sep control cot-read **implicitDeny**; NEGATIVE cross-prefix
  write to `daily/inflection/*` **implicitDeny**. Firm separation holds by grant shape (NEVER#1
  clean-by-design, as the landing commit claimed -- now exercised, not just claimed).
- **Output prefix: already correct.** Live env `OUTPUT_PREFIX=daily/49financial/` -- the writer was
  never pointed at the doc's phantom `daily/49f/` (COO item 3 checked; the trap does not bite here,
  it bites doc-readers).
- **Source: alive.** RPS silver frontier `date=20260723` (freeze resolved 07-24). The producer
  revived today emits vintage 07-23 immediately.

### 3.5 Price (fallback path)

| Item | Cost |
|---|---|
| Code | +~8 additive lines (event-key date parse) + `import re`; no behavior change on existing paths |
| TF | +6 resources (2 rules, 2 targets, 2 permissions), one file |
| IAM | **Zero** (exercised) |
| Bucket config | **Zero** (S3->EventBridge already enabled on opal-data-bd) |
| Apply | post-freeze window (mine, CTO gate): safe-apply targeted, 0-diff, tag `bd-pipeline-v{next}`, ledger opened-at-start, NEVER#6 in-session |
| Backfill | **DS~A's lane** (CTO request, Andrew-direct). Seam position sent separately: backfill should INVOKE this lambda per date (one producer, one code path) rather than write the schema from a second script |

### 3.6 Post-apply verification (fallback path)

1. Rules ENABLED + both permission Sids on the function policy (config half).
2. `test-event-pattern` against a real partition key (pattern caveat above).
3. Floor: next 15:30Z fire -> TriggeredRules datapoint + `daily/49financial/2026-07-23.json` (or
   newer) LastModified advances.
4. Accelerator: on the next real conversion batch, every landed `date=` partition has a same-day
   slice with matching vintage -- the batch-vintage hole is the specific thing to watch land closed.

---

## 4. Open calls routed with this design

1. **CTO ratify:** §2 recommended path (monolith re-source, floor cron(45 10 * * ? *), the one-Sid IAM delta, compute_slice reuse) -- or direct the §3 fallback; on the fallback, ratify floor 15:30Z + the ~8-line handler branch (it is the difference between
   "scheduled" and "every real vintage emitted" on a rebate basis); the pattern-caveat verify step.
2. **Basis decision explicitly NOT taken here:** the pre-staged canonical TRUE-DAILY variant
   (~4% basis step) stays parked; someone (DS/DE/COO) owns that decision separately.
3. **Freeze exception: NOT assumed.** Andrew's "easy fix" changes priority, not the freeze (COO
   011436Z). If CTO wants this in tonight under an exception, the legs are ready; otherwise it is
   first in my post-freeze window alongside Design A.
