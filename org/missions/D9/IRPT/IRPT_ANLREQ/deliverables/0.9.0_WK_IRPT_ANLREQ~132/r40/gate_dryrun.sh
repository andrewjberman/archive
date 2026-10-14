#!/bin/bash
# AR-y-324 step 5 dry run: the two sha256 gate lines of install_r30.sh (lines 23 and 25, copied verbatim) evaluated
# against scratch copies; the host script is NEVER executed, only its sha256 gate is evaluated.
set -u
S=/c/dev/wk-irpt-anlreq-132/.scratch/r40
G=$S/gate
I=$S/scripts/install_r30.sh
H=$S/scripts/resident_host_install_0485393f3a-r30.sh
SUMS=C:/dev/irpt-release-r30/irpt-resident-0485393f3a-r30.package.SHA256SUMS
rm -rf "$G"; mkdir -p "$G"
cp "$H" "$G/host_ok.sh"; cp "$H" "$G/host_bad.sh"; cp "$H" "$G/host_bad_g2.sh"
cp "$SUMS" "$G/sums_ok"; cp "$SUMS" "$G/sums_bad"
python -I - "$G/host_bad.sh" "$G/sums_bad" "$G/host_bad_g2.sh" <<'PY'
import sys
for p, off in ((sys.argv[1], 100), (sys.argv[2], 50), (sys.argv[3], 100)):
    b = bytearray(open(p, 'rb').read()); b[off] ^= 0x01; open(p, 'wb').write(bytes(b))
PY
WANT=$(grep '^WANT=' "$I" | cut -d= -f2)
WANTSUM=$(grep '^WANTSUM=' "$I" | cut -d= -f2)
G1=$(sed -n '23p' "$I")
G2=$(sed -n '25p' "$I")
echo "WANT (install_r30.sh)    = $WANT"
echo "WANTSUM (install_r30.sh) = $WANTSUM"
echo "gate1 line 23: $G1"
echo "gate2 line 25: $G2"
# gate 1: the fetched host script (T) against WANT; gate 2: the fetched package sums (S) against WANTSUM
gate1() { ( T="$1"; eval "$G1" ); }
gate2() { ( S="$1"; T="$2"; eval "$G2" ); }
gate1 "$G/host_ok.sh"; echo "gate1 unchanged host script copy: rc=$?"
gate1 "$G/host_bad.sh"; echo "gate1 one-byte host script copy (byte 100 flipped): rc=$?"
gate2 "$G/sums_ok" "$G/host_ok.sh"; echo "gate2 unchanged package sums copy: rc=$?"
gate2 "$G/sums_bad" "$G/host_bad_g2.sh"; echo "gate2 one-byte package sums copy (byte 50 flipped): rc=$?"
