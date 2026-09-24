#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-1 AC2 (BOUND) -- every other graded column inside main stays PASS on 6 of 6 states,
# read from the SAME run AC1 wrote. usage: bash <this> <out-dir-relative-to-repo-root>
set -u
OUT=${1:?out dir}
ROOT="$(git rev-parse --show-toplevel)"; LOG="$ROOT/$OUT/run.log"
[ -s "$LOG" ] || { echo "no run.log at $OUT -- run AC1 first"; exit 2; }
ok=1
for col in 2:bandContainersTopLevel 3:fonts 4:weights 6:radii 7:shadows 8:lowContrastChars 9:purpleFills; do
  i=${col%%:*}; name=${col#*:}
  n=$(awk -F'\t' -v i="$i" '/== scope=main/{f=1;next} /^== /{f=0} f && NF>=11 && $1!="state" && $i=="PASS" {c++} END{print c+0}' "$LOG")
  echo "$name PASS $n of 6"
  [ "$n" -eq 6 ] || ok=0
done
[ "$ok" -eq 1 ]
