#!/usr/bin/env bash
# MX-g-1 AC1 (the gate's own arms): `naming-gate.py --self-test` exits 0 -- every existing arm still passes -- AND it
# prints the two new arms by name: `ARM legacy_address_own_reader CONFORMANT` and `ARM legacy_address_other_reader REFUSE`.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 300 python .tools/naming-gate.py --self-test 2>&1 | tr -d '\r'); rc=$?
own=$(printf '%s\n' "$out" | grep -c 'ARM legacy_address_own_reader CONFORMANT')
oth=$(printf '%s\n' "$out" | grep -c 'ARM legacy_address_other_reader REFUSE')
printf '%s\n' "$out" | tail -6
echo "self-test rc=$rc; own-reader arm $own; other-reader arm $oth"
if [ "$rc" = 0 ] && [ "$own" -ge 1 ] && [ "$oth" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
