#!/usr/bin/env bash
# OPLGTW OG-up-1 AC3 (R33's two texts and its one read): both caller skill texts name opal_data_refresh_status and carry
# the line "never re-send on a dropped transport"; and UP1_0126Z_READ.json records the 2026-10-07 ~01:26Z execution: its
# terminal status and whether it overlapped the 01:30:43Z gateway restart.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
n=0; ok=0
for f in .claude/skills/terminal-upload/SKILL.md org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/opal_bbgtml/BBG_DAILY_SKILL.md; do
  n=$((n+1)); grep -q 'opal_data_refresh_status' "$f" 2>/dev/null && grep -qi 'never re-send on a dropped transport' "$f" 2>/dev/null && ok=$((ok+1))
done
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~29/UP1_0126Z_READ.json"
rd=no
if [ -f "$F" ]; then python "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r25/checks/up1_read_ok.py" "$(native "$F")" && rd=yes; fi
echo "skill texts carrying the status read and the no-re-send line: $ok of $n; the 01:26Z execution read recorded: $rd"
[ "$ok" = "$n" ] && [ "$rd" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
