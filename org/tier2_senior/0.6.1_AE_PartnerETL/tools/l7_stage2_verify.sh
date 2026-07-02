#!/usr/bin/env bash
# =============================================================================
# l7_stage2_verify.sh -- L7 Stage-2 N-nightly-verify harness (0.6.1_AE_PartnerETL)
# =============================================================================
# Turnkey GREEN/RED read for the L7 event-on-_BRONZE_COMPLETE full-chain trigger
# (inf-gold-full-on-bronze-complete, Stage-1 deployed 20260702, ledger
# advi-infref-l7-stage1-bronzecomplete-trigger CLOSED). Run once per nightly (or
# after the fact for any RUN_DATE) to prove the new trigger is the SOLE working
# path BEFORE the human-gated Stage-3 delete (9 crons + aggregator +
# s3-notification + inf-canonical-prices-daily). N consecutive GREEN = the gate.
#
# Confirms (COO dispatch 20260702T225026Z + CTO first-exercise checklist 220637Z):
#   (a) the event-fired inf-gold-full chain LANDS: the rule fires on
#       _BRONZE_COMPLETE (mode=full,source=bronze-complete) -> chain runs ->
#       served header_metrics advances to RUN_DATE.
#   (b) it lands AFTER Orion-settle (>= bronze-runner completion, ~13:30Z/9:30ET)
#       so the timing intent holds -- the rule fires ON the sentinel write, so
#       verify the sentinel overall=success + its completed_at is post-settle.
#   (c) the inf-gold-trigger-dlq-depth alarm stays clean (no DLQ'd fire).
#   (d) T2 cadence: silver/historical_prices.parquet lands before the chain
#       consumes it (INF_S_00 T2 fallback tier -- graceful if late, but watch).
#   (e) as_of holiday-normalization: on a NYSE-closed RUN_DATE (e.g. 07-03
#       July-4-obs) served data_as_of must be the PRIOR trading day, not RUN_DATE.
#
# Usage:  bash l7_stage2_verify.sh [RUN_DATE=YYYY-MM-DD]   (default: today UTC)
# Read-only: aws describe/get + s3 cp to stdout only. Never mutates.
# Git Bash 3.6.7-safe (no pgrep/flock/etc; GNU date -d is present); ASCII only.
# =============================================================================
set -uo pipefail

RUN_DATE="${1:-$(date -u +%Y-%m-%d)}"
BUCKET="opal-data-inf"
RULE="inf-gold-full-on-bronze-complete"
DLQ_ALARM="inf-gold-trigger-dlq-depth"
TRIGGER_LOG="/aws/lambda/inf-gold-trigger"

# NYSE 2026 closed dates (mirrors data/inf/scripts/silver/_orion_vendor_asof.py --
# 2-party-verified 2026 set; extend before coverage lapses).
NYSE_CLOSED_2026="2026-01-01 2026-01-19 2026-02-16 2026-04-03 2026-05-25 2026-06-19 2026-07-03 2026-09-07 2026-11-26 2026-12-25"

PASS=0; FAIL=0; WARN=0
ok(){   echo "OK:   $1"; PASS=$((PASS+1)); }
red(){  echo "RED:  $1"; FAIL=$((FAIL+1)); }
warn(){ echo "WARN: $1"; WARN=$((WARN+1)); }
info(){ echo "        $1"; }

is_nyse_closed(){ # $1=YYYY-MM-DD -> 0 if closed (weekend or holiday)
  local d="$1"; local dow
  dow=$(date -u -d "$d" +%u 2>/dev/null || echo 0)   # 6=Sat 7=Sun
  [ "$dow" = "6" ] || [ "$dow" = "7" ] && return 0
  case " $NYSE_CLOSED_2026 " in *" $d "*) return 0;; esac
  return 1
}
prior_trading_day(){ # $1=YYYY-MM-DD -> most recent open day strictly before it
  local d="$1" i
  for i in 1 2 3 4 5 6 7; do
    d=$(date -u -d "$d -1 day" +%Y-%m-%d 2>/dev/null) || { echo ""; return; }
    if ! is_nyse_closed "$d"; then echo "$d"; return; fi
  done
  echo ""
}

echo "=== L7 Stage-2 verify -- RUN_DATE=$RUN_DATE ($(date -u +%FT%TZ)) ==="

# --- (a1) rule fired on _BRONZE_COMPLETE ---------------------------------------
INV=$(aws cloudwatch get-metric-statistics --namespace AWS/Events \
  --metric-name Invocations --dimensions Name=RuleName,Value="$RULE" \
  --start-time "${RUN_DATE}T00:00:00Z" --end-time "${RUN_DATE}T23:59:59Z" \
  --period 86400 --statistics Sum \
  --query "Datapoints[0].Sum" --output text 2>/dev/null)
if [ -n "$INV" ] && [ "$INV" != "None" ] && awk "BEGIN{exit !($INV>=1)}" 2>/dev/null; then
  ok "(a1) rule $RULE fired $INV time(s) on $RUN_DATE"
else
  red "(a1) rule $RULE NOT observed firing on $RUN_DATE (Invocations=${INV:-none}) -- did _BRONZE_COMPLETE land? was another trigger the one that won the lock?"
fi

# --- (a2) inf-gold-trigger invoked with source=bronze-complete (corroborating) --
EPOCH_START=$(date -u -d "${RUN_DATE}T00:00:00Z" +%s 2>/dev/null)
if [ -n "$EPOCH_START" ]; then
  NSRC=$(aws logs filter-log-events --log-group-name "$TRIGGER_LOG" \
    --start-time "${EPOCH_START}000" \
    --filter-pattern 'source=bronze-complete' \
    --query "length(events)" --output text 2>/dev/null)
  if [ -n "$NSRC" ] && [ "$NSRC" != "None" ] && awk "BEGIN{exit !($NSRC>=1)}" 2>/dev/null; then
    ok "(a2) inf-gold-trigger logged source=bronze-complete ($NSRC event(s)) on/after $RUN_DATE"
  else
    warn "(a2) no source=bronze-complete log line found (a1 rule-fired + a3 served-advanced are primary; a competing trigger may have won the lock -- inspect if a1/a3 disagree)"
  fi
else
  warn "(a2) skipped -- could not compute epoch for $RUN_DATE (date -d)"
fi

# --- (a3) chain LANDED: pipeline-complete + served header advanced --------------
PC=$(aws s3 cp "s3://$BUCKET/gold/meta/pipeline-complete.json" - 2>/dev/null)
PC_DATE=$(echo "$PC" | python -c "import json,sys; print(json.load(sys.stdin).get('run_date',''))" 2>/dev/null)
if [ "$PC_DATE" = "$RUN_DATE" ]; then
  ok "(a3a) gold/meta/pipeline-complete.json run_date=$PC_DATE"
else
  red "(a3a) pipeline-complete.json run_date=$PC_DATE != $RUN_DATE -- chain did not complete for the date"
fi
HM=$(aws s3 cp "s3://$BUCKET/platinum/firm/header_metrics.json" - 2>/dev/null)
HM_GEN=$(echo "$HM" | python -c "import json,sys; print(json.load(sys.stdin).get('generated_at',''))" 2>/dev/null)
HM_ASOF=$(echo "$HM" | python -c "import json,sys; print(json.load(sys.stdin).get('data_as_of',''))" 2>/dev/null)
if echo "$HM_GEN" | grep -q "^$RUN_DATE"; then
  ok "(a3b) served header_metrics generated_at=$HM_GEN (advanced to $RUN_DATE)"
else
  red "(a3b) served header_metrics generated_at=$HM_GEN did NOT advance to $RUN_DATE (frozen?)"
fi
info "served data_as_of=$HM_ASOF"

# --- (b) after Orion-settle: sentinel overall=success + post-settle -------------
SENT=$(aws s3 cp "s3://$BUCKET/bronze/orion-api/$RUN_DATE/_BRONZE_COMPLETE.json" - 2>/dev/null)
SENT_OVERALL=$(echo "$SENT" | python -c "import json,sys; print(json.load(sys.stdin).get('overall',''))" 2>/dev/null)
SENT_AT=$(echo "$SENT" | python -c "import json,sys; print(json.load(sys.stdin).get('completed_at',''))" 2>/dev/null)
if [ "$SENT_OVERALL" = "success" ]; then
  ok "(b1) bronze/orion-api/$RUN_DATE/_BRONZE_COMPLETE overall=success completed_at=$SENT_AT"
elif [ -n "$SENT_OVERALL" ]; then
  warn "(b1) bronze sentinel overall=$SENT_OVERALL (NOT success) -- the rule STILL fired on it (fire-on-existence, overall-gate deferred); gold ran on partial/failed bronze -> inspect + confirm served correctness. This is the class the overall-gate hardening would catch."
else
  red "(b1) no _BRONZE_COMPLETE sentinel for $RUN_DATE -- bronze-runner did not complete; the trigger had nothing to fire on"
fi
# completed_at is written by the bronze-runner (>= ~13:30Z start); the rule fires
# ON this write, so the chain is structurally post-settle. Flag if suspiciously early.
if [ -n "$SENT_AT" ]; then
  SENT_HH=$(echo "$SENT_AT" | sed -n 's/.*T\([0-9][0-9]\):.*/\1/p')
  if [ -n "$SENT_HH" ] && awk "BEGIN{exit !($SENT_HH>=13)}" 2>/dev/null; then
    ok "(b2) bronze completed_at hour=${SENT_HH}Z (>= 13Z / 9ET -- post Orion-settle, timing intent holds)"
  else
    warn "(b2) bronze completed_at hour=${SENT_HH}Z (< 13Z) -- unexpectedly early; confirm Orion-settle timing"
  fi
fi

# --- (c) DLQ alarm clean --------------------------------------------------------
DLQ_STATE=$(aws cloudwatch describe-alarms --alarm-names "$DLQ_ALARM" \
  --query "MetricAlarms[0].StateValue" --output text 2>/dev/null)
if [ "$DLQ_STATE" = "OK" ]; then
  ok "(c) $DLQ_ALARM StateValue=OK -- no DLQ'd gold-fire"
elif [ "$DLQ_STATE" = "INSUFFICIENT_DATA" ]; then
  warn "(c) $DLQ_ALARM StateValue=INSUFFICIENT_DATA (no datapoints yet -- benign pre-first-fire; re-check after the run)"
else
  red "(c) $DLQ_ALARM StateValue=$DLQ_STATE -- a gold-trigger fire FAILED into the DLQ; inspect the DLQ message + inf-gold-trigger errors"
fi

# --- (d) T2 cadence: historical_prices freshness --------------------------------
HP_LM=$(aws s3api head-object --bucket "$BUCKET" --key silver/historical_prices.parquet \
  --query "LastModified" --output text 2>/dev/null)
if [ -n "$HP_LM" ] && [ "$HP_LM" != "None" ]; then
  info "(d) silver/historical_prices.parquet LastModified=$HP_LM (T2 fallback -- confirm it precedes the chain's INF_S_00 consume; graceful if one-day-late, watch for chronic lag)"
  ok "(d) historical_prices present (T2 cadence check -- manual eyeball on the timestamp vs chain start)"
else
  warn "(d) silver/historical_prices.parquet not found via head-object -- T2 (yahoo) tier unavailable; INF_S_00 falls back to T1 txn-observed + T4 carry-forward (degrades, not fatal)"
fi

# --- (e) as_of holiday-normalization -------------------------------------------
if is_nyse_closed "$RUN_DATE"; then
  EXP=$(prior_trading_day "$RUN_DATE")
  echo "  [holiday-edge] $RUN_DATE is NYSE-CLOSED -> served data_as_of MUST be prior trading day $EXP (as_of-normalization)"
  if [ -n "$EXP" ] && [ "$HM_ASOF" = "$EXP" ]; then
    ok "(e) served data_as_of=$HM_ASOF == prior-trading-day $EXP (holiday-normalization correct)"
  elif [ "$HM_ASOF" = "$RUN_DATE" ]; then
    red "(e) served data_as_of=$HM_ASOF == RUN_DATE on a NYSE-CLOSED day -- holiday-normalization FAILED (expected $EXP). Orion forward-label leaked to served."
  else
    warn "(e) served data_as_of=$HM_ASOF; expected prior-trading-day $EXP on this NYSE-closed date -- verify manually"
  fi
else
  info "(e) $RUN_DATE is a NYSE trading day -- no holiday-normalization edge to check (served data_as_of=$HM_ASOF)"
fi

# --- verdict -------------------------------------------------------------------
echo "=== VERDICT: PASS=$PASS RED=$FAIL WARN=$WARN ==="
if [ "$FAIL" -eq 0 ]; then
  echo "GREEN: L7 event-trigger exercised cleanly for $RUN_DATE (WARN items are advisory -- read them)."
  exit 0
else
  echo "RED: $FAIL hard check(s) failed for $RUN_DATE -- NOT a clean exercise. Do NOT count toward N-nightly-GREEN; inspect + RAVC CTO before Stage-3."
  exit 1
fi
