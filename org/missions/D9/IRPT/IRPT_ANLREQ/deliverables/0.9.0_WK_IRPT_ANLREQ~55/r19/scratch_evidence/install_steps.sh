#!/usr/bin/env bash
# AR-y-196 scratch install proof. FILE OPERATIONS ONLY, on scratch paths. No systemctl, no sudo, no host, no network.
# Host paths replaced: /opt/irpt-resident -> $S/opt/irpt-resident ; /opt/investor-reporting-ycharts -> $S/opt/investor-reporting-ycharts
# Every command below is an installer / host-script line (cited) or a control (labelled CONTROL).
set -u
S=/c/dev/ar196-55-scratch
SW=C:/dev/ar196-55-scratch
ARC=/c/dev/ar195-55-tarballs
R=$S/opt/irpt-resident
H=$S/opt/investor-reporting-ycharts
OLD=0485393f3a-st32
NEW=069b8f797e-scratch
OLDROOT=$R/$OLD
ROOT=$R/$NEW
LOG=$S/commands_run.log
: > "$LOG"
run() { echo "+ $*" | tee -a "$LOG"; "$@"; rc=$?; echo "  rc=$rc" | tee -a "$LOG"; return $rc; }

echo "== PART A: live-shaped OLD root = A1 tarball (live-pin build, 182 members) + 144 dummy files named like the st32-only members" | tee -a "$LOG"
run mkdir -p "$H/pydeps" || exit 1
run mkdir -p "$OLDROOT" || exit 1
run tar -xzf "$ARC/live_0485393f3a_A1.tar.gz" -C "$OLDROOT" || exit 1
while IFS= read -r name; do
  mkdir -p "$OLDROOT/$(dirname "$name")" && printf 'DUMMY unbuilt live member (scratch placeholder, not the live bytes)\n' > "$OLDROOT/$name" || { echo "dummy failed: $name"; exit 1; }
done < "$S/bin/unbuilt_st32_only.names"
echo "  dummies written: $(wc -l < "$S/bin/unbuilt_st32_only.names")" | tee -a "$LOG"
python -I "$S/bin/census.py" "$SW/opt/irpt-resident/$OLD" "$S/census_before.json" "$S/bin/unbuilt_st32_only.names" || exit 1

echo "== PART B: E1 = the host procedure for a NEW pin (st32 host script lines 20, 23, 44-45, 47-58; installer lines 8, 17-20, 39)" | tee -a "$LOG"
# installer line 8: package_root="$(realpath -e -- "$1")" -- checked on the NEW root after extraction below
# st32 host script line 20: rm -rf "$ROOT"; mkdir -p "$ROOT"   (the NEW pin's directory only; the OLD root is not an argument)
run rm -rf "$ROOT" || exit 1
run mkdir -p "$ROOT" || exit 1
# line 23: tar -xzf <release tarball> -C "$ROOT"
run tar -xzf "$ARC/release_069b8f797e_B1.tar.gz" -C "$ROOT" || exit 1
cd "$ROOT" || exit 1
# line 44: cp -a $H/pydeps/. "$ROOT/"   (H/pydeps is the HOST shared directory; the OLD root is not a source here)
run cp -a "$H/pydeps/." "$ROOT/" || exit 1
# line 45: rm -rf "$ROOT/bin"
run rm -rf "$ROOT/bin" || exit 1
# lines 47-58: SHA256SUMS generated over the whole new root (see bin/gen_sha256sums.py for the one separator adaptation)
run python -I "$S/bin/gen_sha256sums.py" || exit 1
# installer line 8 (realpath -e), line 17 (SHA256SUMS present), line 18-20 (entry), line 39 (sha256sum --check --strict)
run realpath -e -- "$ROOT" || exit 1
run test -f "$ROOT/SHA256SUMS" && echo "  installer line 17: SHA256SUMS present" | tee -a "$LOG"
ENTRY="$ROOT/ycharts/generate/resident_main.py"; run test -f "$ENTRY" && echo "  installer line 18-20: entry present" | tee -a "$LOG"
echo "+ sha256sum --check --strict SHA256SUMS   (installer line 39)" | tee -a "$LOG"
sha256sum --check --strict SHA256SUMS > "$S/sha_check_new_root.txt" 2>&1; rc=$?; echo "  rc=$rc (output in sha_check_new_root.txt: $(wc -l < "$S/sha_check_new_root.txt") lines)" | tee -a "$LOG"
cd "$S" || exit 1
python -I "$S/bin/census.py" "$SW/opt/irpt-resident/$NEW" "$S/census_after_E1.json" "$S/bin/unbuilt_st32_only.names" || exit 1
python -I "$S/bin/compare.py" "$S/census_before.json" "$S/census_after_E1.json" "$S/compare_E1.json" | tee -a "$LOG"

echo "== PART C: CONTROL E2 = the same release extracted IN PLACE over a copy of the OLD root (not what the host script does)" | tee -a "$LOG"
OVL=$R/overlay-control-$OLD
run rm -rf "$OVL" || exit 1
run cp -a "$OLDROOT" "$OVL" || exit 1
run tar -xzf "$ARC/release_069b8f797e_B1.tar.gz" -C "$OVL" || exit 1
python -I "$S/bin/census.py" "$SW/opt/irpt-resident/overlay-control-$OLD" "$S/census_after_E2.json" "$S/bin/unbuilt_st32_only.names" || exit 1
python -I "$S/bin/compare.py" "$S/census_before.json" "$S/census_after_E2.json" "$S/compare_E2.json" | tee -a "$LOG"
echo "DONE" | tee -a "$LOG"
