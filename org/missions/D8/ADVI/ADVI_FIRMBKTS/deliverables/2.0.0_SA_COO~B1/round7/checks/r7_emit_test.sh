#!/bin/bash
# ADVI_FIRMBKTS round 7, FB-j-2: the dispatcher's emit_chain_complete prints the CLI's error text (first 300 chars) in its WARN.
# usage: bash r7_emit_test.sh <path to gold_dispatch.sh>
# Extracts the function from the file, runs it against a stubbed `aws`, and prints a last line `EMIT TEST: <n> of 3 arms`.
# The stub is a shell function (it shadows any aws binary); no network, no AWS call, no write. Issuer-owned; never edit.
SCRIPT="$1"
if [ -z "$SCRIPT" ] || [ ! -f "$SCRIPT" ]; then echo "EMIT TEST: 0 of 3 arms (script not found)"; exit 1; fi
FN=$(sed -n '/^emit_chain_complete() {/,/^}/p' "$SCRIPT")
if [ -z "$FN" ]; then echo "EMIT TEST: 0 of 3 arms (function not found)"; exit 1; fi

run_arm() {  # $1 = stub mode ; prints the function's stdout, then a line RC=<n>
  (
    CHAIN_LABEL="probe-label"; SCRIPT_IDS="A_01"; MODE="chain"
    log_ts() { echo "2026-01-01T00:00:00Z"; }
    STUB_MODE="$1"
    aws() {
      case "$STUB_MODE" in
        ok)   printf '{\n    "FailedEntryCount": 0,\n    "Entries": [{"EventId": "x"}]\n}\n'; return 0 ;;
        long) printf '%s%s\n' "$(printf 'E%.0s' $(seq 1 400))" "TAILMARK"; return 255 ;;
        multi) printf 'alpha\nbeta\n'; return 255 ;;
      esac
    }
    eval "$FN"
    emit_chain_complete 0
    echo "RC=$?"
  ) 2>&1
}

PASS=0
E300=$(printf 'E%.0s' $(seq 1 300))
E301=$(printf 'E%.0s' $(seq 1 301))

OUT=$(run_arm long)
if printf '%s' "$OUT" | grep -q "WARN: EventBridge chain-complete put-events failed" \
   && printf '%s' "$OUT" | grep -q "$E300" \
   && ! printf '%s' "$OUT" | grep -q "$E301" \
   && ! printf '%s' "$OUT" | grep -q "TAILMARK"; then
  echo "PASS E1 a failing call prints the first 300 characters of the CLI text, no more"; PASS=$((PASS+1))
else
  echo "FAIL E1 a failing call prints the first 300 characters of the CLI text, no more"
fi

OUT=$(run_arm ok)
if printf '%s' "$OUT" | grep -q "EventBridge chain-complete emitted" && ! printf '%s' "$OUT" | grep -q "WARN:"; then
  echo "PASS E2 a successful call prints the emitted line and no WARN"; PASS=$((PASS+1))
else
  echo "FAIL E2 a successful call prints the emitted line and no WARN"
fi

OUT=$(run_arm multi)
if [ "$(printf '%s\n' "$OUT" | grep -c 'WARN:')" = "1" ] \
   && printf '%s' "$OUT" | grep -q "WARN:.*alpha beta" \
   && printf '%s' "$OUT" | grep -q "^RC=0$"; then
  echo "PASS E3 a multi-line error text is one WARN line and the function still returns 0"; PASS=$((PASS+1))
else
  echo "FAIL E3 a multi-line error text is one WARN line and the function still returns 0"
fi
echo "EMIT TEST: $PASS of 3 arms"
[ "$PASS" = "3" ]
