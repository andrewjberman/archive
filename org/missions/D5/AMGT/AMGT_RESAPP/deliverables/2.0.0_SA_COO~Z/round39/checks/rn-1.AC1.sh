#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-1 AC1 -- the class census on the two files reads size=0, and neither carries a
# text-[10px] or text-[9px] token. usage: bash <this>
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
F1=src/ui/components/panels/PanelHeader.tsx; F2=src/components/DataTimestamp.tsx
node scripts/ui-class-census.mjs "$F1" "$F2" | tee /dev/stderr > .scratch.rn1.census.txt 2>/dev/null || node scripts/ui-class-census.mjs "$F1" "$F2" > .scratch.rn1.census.txt
cat .scratch.rn1.census.txt
z=$(grep -c ' size=0 ' .scratch.rn1.census.txt); t=$(cat "$F1" "$F2" | grep -c -E 'text-\[(9|10)px\]')
rm -f .scratch.rn1.census.txt
echo "files with size=0: $z of 2; text-[9px|10px] tokens across both: $t"
[ "$z" -eq 2 ] && [ "$t" -eq 0 ]
