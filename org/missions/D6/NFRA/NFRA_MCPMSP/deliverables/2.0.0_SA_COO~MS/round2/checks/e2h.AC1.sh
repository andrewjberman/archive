#!/usr/bin/env bash
# MS-sh-1 AC1 (the built behaviour, on fixtures): opal_ai/opal/runtime-msp/hooks/test_sender_gate.sh ends with
# "RESULT: PASS" and reports each named case PASS: served_answer_allows_send, denied_answer_blocks_send,
# no_query_blocks_send, other_chat_served_blocks_send.
. "$(dirname "$0")/_root.sh"
T="opal_ai/opal/runtime-msp/hooks/test_sender_gate.sh"
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 bash "$T" 2>&1 | tr -d '\r')
n=0; line=""; for c in served_answer_allows_send denied_answer_blocks_send no_query_blocks_send other_chat_served_blocks_send; do k=$(printf '%s\n' "$out" | grep -cE "^(PASS|OK):? *$c"); line="$line $c=$k"; [ "$k" -ge 1 ] && n=$((n+1)); done
fin=$(printf '%s\n' "$out" | grep -c '^RESULT: PASS')
echo "hook fixture cases:$line; final RESULT: PASS lines=$fin"
if [ "$n" = 4 ] && [ "$fin" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
