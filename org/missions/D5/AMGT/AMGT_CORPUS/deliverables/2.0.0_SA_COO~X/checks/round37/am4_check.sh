#!/usr/bin/env bash
# AMGT_CORPUS round 37, CRPS-am-4 (row Z-W4-S4) -- `induction_request --pick` writes nothing. Issuer's file.
# RUN from the repository root under test:  bash am4_check.sh
# Plants a sentinel in the request file the module used to write, runs `python -m lib.research.corpus.induction_request --pick`,
# then restores the file's original bytes (or removes it if it did not exist). Prints one line per arm, then
# `am4 build <p>/1 control <q>/1`.
#   b1  the sentinel bytes are unchanged after the run (the read-only verb wrote nothing there).
#   c1  the run still reads the population and decides: rc 0, a `picked ` line and `vendor_calls 0` in its output.
set -u
TOP="$(git rev-parse --show-toplevel)"
cd "$TOP" || exit 2
F="org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~2/induction_request.json"
TMP="$(mktemp -d)"
HAD=0
if [ -f "$F" ]; then HAD=1; cp "$F" "$TMP/orig.json"; fi
mkdir -p "$(dirname "$F")"
printf 'SENTINEL am4 %s\n' "$$" > "$F"
cp "$F" "$TMP/sentinel"
PYTHONPATH="$TOP" timeout 110 python -m lib.research.corpus.induction_request --pick > "$TMP/out.txt" 2>&1
RC=$?
if cmp -s "$TMP/sentinel" "$F"; then B1=1; B1N="sentinel unchanged"; else B1=0; B1N="file REWRITTEN by --pick"; fi
if [ "$HAD" = 1 ]; then cp "$TMP/orig.json" "$F"; else rm -f "$F"; fi
C1=0
if [ "$RC" = 0 ] && grep -q '^picked ' "$TMP/out.txt" && grep -q '^vendor_calls 0$' "$TMP/out.txt"; then C1=1; fi
echo "ARM b1 $([ $B1 = 1 ] && echo PASS || echo FAIL) $B1N"
echo "ARM c1 $([ $C1 = 1 ] && echo PASS || echo FAIL) rc $RC; $(grep -m1 '^picked ' "$TMP/out.txt" | cut -c1-80); $(grep -m1 '^vendor_calls' "$TMP/out.txt")"
echo "am4 build $B1/1 control $C1/1"
rm -rf "$TMP"
