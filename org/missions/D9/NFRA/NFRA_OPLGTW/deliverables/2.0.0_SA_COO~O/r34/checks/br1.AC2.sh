#!/usr/bin/env bash
# OPLGTW OG-br-1 AC2 (round-34 E4, the SI2 puller; rows W39-S1/S2), in infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:
# - the enumerate branch calls Release-SessionLock before its exit 0;
# - the per-type date list is forced to an array (@( ... )), so a one-file type prints its date, not '2..0';
# - the script still parses (PowerShell AST, 0 errors).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F=infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1
blk=$(awk '/^if \(\$Mode -eq .enumerate.\) \{/{f=1} f{print} f&&/^\}/{exit}' "$F")
rel=$(printf '%s\n' "$blk" | awk '/Release-SessionLock/{r=NR} /exit 0/{e=NR} END{print (r && e && r<e) ? "yes" : "no"}')
arr=$(printf '%s\n' "$blk" | grep -cE '\$ds = @\(')
perr=$(powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path '$F').Path,[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
echo "enumerate branch releases the lock before exit: $rel; date list forced to array: $arr (want 1); parse errors: $perr (want 0)"
[ "$rel" = yes ] && [ "$arr" = 1 ] && [ "$perr" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
