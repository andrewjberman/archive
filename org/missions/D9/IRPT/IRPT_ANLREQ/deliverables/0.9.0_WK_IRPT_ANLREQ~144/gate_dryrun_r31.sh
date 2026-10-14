#!/bin/bash
# TO-AR-y-338 step 4 dry run: the two sha256 gate lines of install_r31.sh, copied verbatim (found by a fixed-string match,
# exactly one line each), evaluated against scratch copies in the worktree's .scratch. The host script is NEVER executed;
# only its sha256 gate is evaluated. Nothing is uploaded, installed or run on a host.
set -u
DL=/c/dev/wk-irpt-anlreq-144/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~144
I=$DL/install_r31.sh
H=$DL/resident_host_install_0485393f3a-r31.sh
SUMS=C:/dev/irpt-release-r31/irpt-resident-0485393f3a-r31.package.SHA256SUMS
S=/c/dev/wk-irpt-anlreq-144/.scratch/gate_r31_p2
rm -rf "$S"; mkdir -p "$S"
cp "$H" "$S/host_ok.sh"; cp "$H" "$S/host_bad.sh"; cp "$H" "$S/host_bad_g2.sh"
cp "$SUMS" "$S/sums_ok"; cp "$SUMS" "$S/sums_bad"
python -I - "$S/host_bad.sh" "$S/sums_bad" "$S/host_bad_g2.sh" <<'PY'
import sys
for p, off in ((sys.argv[1], 100), (sys.argv[2], 50), (sys.argv[3], 100)):
    b = bytearray(open(p, 'rb').read()); b[off] ^= 0x01; open(p, 'wb').write(bytes(b))
PY
n1=$(grep -c -F 'sha256sum $T |' "$I")
n2=$(grep -c -F 'sha256sum $S |' "$I")
echo "gate lines found: gate1=$n1 gate2=$n2 (want 1 and 1)"
[ "$n1" = 1 ] && [ "$n2" = 1 ] || { echo "REFUSE: gate lines not found exactly once"; exit 9; }
G1=$(grep -F 'sha256sum $T |' "$I")
G2=$(grep -F 'sha256sum $S |' "$I")
WANT=$(grep '^WANT=' "$I" | cut -d= -f2)
WANTSUM=$(grep '^WANTSUM=' "$I" | cut -d= -f2)
echo "WANT (install_r31.sh)    = $WANT"
echo "WANTSUM (install_r31.sh) = $WANTSUM"
echo "gate1: $G1"
echo "gate2: $G2"
# gate 1: the fetched host script (T) against WANT; gate 2: the fetched package sums (S) against WANTSUM
gate1() { ( T="$1"; eval "$G1" ); }
gate2() { ( S="$1"; T="$2"; eval "$G2" ); }
gate1 "$S/host_ok.sh"; echo "gate1 unchanged host script copy: rc=$?"
gate1 "$S/host_bad.sh"; echo "gate1 one-byte host script copy (byte 100 flipped): rc=$?"
gate2 "$S/sums_ok" "$S/host_ok.sh"; echo "gate2 unchanged package sums copy: rc=$?"
gate2 "$S/sums_bad" "$S/host_bad_g2.sh"; echo "gate2 one-byte package sums copy (byte 50 flipped): rc=$?"
