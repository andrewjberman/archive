#!/usr/bin/env bash
# OPLGTW OG-en-33 AC1 (round 44; row Z-S399): the both-orders check (r38/checks/_bothorders.sh) no longer discards the forward pytest text. CONTROLS with two stub test runners; the stubs, not the gateway, make the outcome.
# Contract of the repaired script: env BOTHORDERS_PYTEST (default "python -m pytest -q -p no:cacheprovider") is the runner it calls as `( cd "$GW" && timeout 280 $BOTHORDERS_PYTEST <files> )`;
# env BOTHORDERS_OUT (default a fresh mktemp dir) receives <label>.forward.txt and <label>.reverse.txt = the FULL runner output of each order.
# When an order's last line carries no "N passed", the script prints `<label> <order>: NO PASS LINE; saved <path>` plus the last 15 lines of that text, and the verdict is FAIL.
#  ARM A (the stub prints a traceback for the forward order and "3 passed" for the reverse order): the output has `forward: NO PASS LINE; saved <path>`, the saved file holds the traceback line, and RESULT: FAIL.
#  ARM B (the stub prints "3 passed in 0.1s" for both orders): `forward: passed 3; failed 0`, `reverse: passed 3; failed 0`, RESULT: PASS.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
S=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/_bothorders.sh
D=$(mktemp -d); OUT="$D/out"; mkdir -p "$OUT"
cat > "$D/stubA.sh" <<'EOF'
#!/usr/bin/env bash
case "$1" in *aaa_first*) echo "Traceback (most recent call last): STUB-BOOM";; *) echo "3 passed in 0.1s";; esac
EOF
cat > "$D/stubB.sh" <<'EOF'
#!/usr/bin/env bash
echo "3 passed in 0.1s"
EOF
chmod +x "$D/stubA.sh" "$D/stubB.sh"
# the runner is called from inside $GW; the file arguments need not exist for a stub
ra=$(BOTHORDERS_PYTEST="bash $(native "$D/stubA.sh")" BOTHORDERS_OUT="$OUT" bash "$S" ctl tests/aaa_first.py tests/zzz_second.py 2>&1 | tr -d '\r'); rca=$?
rb=$(BOTHORDERS_PYTEST="bash $(native "$D/stubB.sh")" BOTHORDERS_OUT="$OUT" bash "$S" ctlb tests/aaa_first.py tests/zzz_second.py 2>&1 | tr -d '\r'); rcb=$?
nopass=$(printf '%s\n' "$ra" | grep -cE '^ctl forward: NO PASS LINE; saved ')
saved=$(printf '%s\n' "$ra" | grep -E '^ctl forward: NO PASS LINE; saved ' | head -1 | sed 's/.*saved //')
holds=0; [ -n "$saved" ] && [ -f "$saved" ] && grep -q 'STUB-BOOM' "$saved" && holds=1
afail=$(printf '%s\n' "$ra" | grep -c '^RESULT: FAIL')
bpass=$(printf '%s\n' "$rb" | grep -c '^ctlb forward: passed 3; failed 0'); bpass2=$(printf '%s\n' "$rb" | grep -c '^ctlb reverse: passed 3; failed 0'); bres=$(printf '%s\n' "$rb" | grep -c '^RESULT: PASS')
rm -rf "$D"
echo "arm A (forward prints a traceback): NO PASS LINE reported $nopass (want 1); the saved forward text holds the traceback $holds (want 1); RESULT: FAIL printed $afail (want 1); exit $rca (want 1)"
echo "arm B (both orders print 3 passed): forward line $bpass (want 1), reverse line $bpass2 (want 1), RESULT: PASS printed $bres (want 1); exit $rcb (want 0)"
[ "$nopass" = 1 ] && [ "$holds" = 1 ] && [ "$afail" = 1 ] && [ "$rca" = 1 ] && [ "$bpass" = 1 ] && [ "$bpass2" = 1 ] && [ "$bres" = 1 ] && [ "$rcb" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
