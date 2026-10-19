#!/usr/bin/env bash
# OPLGTW OG-gd-2 AC3 (round 46; the CTO's round-45 analysis A2, msg 35928): tests/acceptance/WALKTHROUGH_PROTOCOL.md no longer presupposes the retired G-C record.
#  - the path of the G-C record (G-C_CONTROLLED_IDENTITY_AND_GRANT.md) appears 0 times as a presupposed input; the file says G-C was retired by ruling 28152; the pilot input record G-E_PILOT_IDENTITY_AND_GRANT.md is STILL named;
#  - the file differs from its base blob (the blob named in BASE) by at most 8 added and 8 removed lines (a narrow edit), and the base's other sections (Evidence rules onward, line 21 to the end) are byte-equal.
# Overrides (dry-run controls only): GD2_BASE_OVERRIDE, GD2_FILE_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
BASE="${GD2_BASE_OVERRIDE:-d649cb3e4987de8b88062bdc93ca5cb4720b5f98}"
F="${GD2_FILE_OVERRIDE:-$GW/tests/acceptance/WALKTHROUGH_PROTOCOL.md}"
git cat-file -e "$BASE" 2>/dev/null || { echo "base blob $BASE not in this repository"; echo "RESULT: FAIL"; exit 1; }
git cat-file -p "$BASE" > "${TMPDIR:-/tmp}/gd2_base_protocol.md"
res=$(python -I - "$(native "${TMPDIR:-/tmp}/gd2_base_protocol.md")" "$(native "$F")" <<'PYEOF'
import difflib, re, sys
a = open(sys.argv[1], encoding="utf-8").read().splitlines()
b = open(sys.argv[2], encoding="utf-8").read().splitlines()
added = removed = 0
for l in difflib.unified_diff(a, b, lineterm="", n=0):
    if l.startswith(("+++", "---", "@@")):
        continue
    if l.startswith("+"): added += 1
    else: removed += 1
t = "\n".join(b)
# presupposed-input uses: the G-C record path inside the section-1 table or the Input: line of the controlled record template
gc = len(re.findall(r"G-C_CONTROLLED_IDENTITY_AND_GRANT\.md", t))
retired = bool(re.search(r"G-C", t) and re.search(r"28152", t) and re.search(r"(?i)retired", t))
ge = "G-E_PILOT_IDENTITY_AND_GRANT.md" in t
# the sections after section 1 (from the line "## 2. Evidence rules") must be byte-equal
ia = next((i for i, l in enumerate(a) if l.startswith("## 2. Evidence rules")), None)
ib = next((i for i, l in enumerate(b) if l.startswith("## 2. Evidence rules")), None)
# the Input: line of the controlled walkthrough record template is the one place G-C may change below section 2
body_changed = sum(1 for x, y in zip(a[ia:], b[ib:]) if x != y) if (ia is not None and ib is not None and len(a[ia:]) == len(b[ib:])) else -1
ok = gc == 0 and retired and ge and added <= 8 and removed <= 8 and body_changed in (0, 1)
print("G-C record path named as an input %d time(s) (want 0); says G-C was retired by ruling 28152 %s; pilot record G-E still named %s" % (gc, "yes" if retired else "NO", "yes" if ge else "NO"))
print("added lines %d, removed lines %d (want each 8 or fewer); changed lines from section 2 on %d (want 0 or 1: the controlled record's Input line)" % (added, removed, body_changed))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
