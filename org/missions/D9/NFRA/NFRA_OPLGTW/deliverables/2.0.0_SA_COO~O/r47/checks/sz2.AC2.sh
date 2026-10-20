#!/usr/bin/env bash
# OPLGTW OG-sz-2 AC2 (round 47): the edit to tests/test_og_rv2.py is the SMALLEST that restores the premise: against the pinned blob 1e40e66dc1 (the file at the issuance) at most 12 lines changed, only in the wide-part section (the row count
# 120 becomes one smaller count N between 60 and 119, in the part builder's argument, the two row-count assertions and the comments/docstring that name it), every assertion about the narrowing is kept (columns_dropped, the 15-column set,
# "within the 50 KB answer", not truncated), and N rows narrowed fit 51200 bytes as served is the test's own assertion (the test passes).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F=infra/aws/ec2/opal-gateway/tests/test_og_rv2.py
PIN=1e40e66dc191d9ccd36fb99a4c001a5e915daa24
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python3 -I - "$(native "$F")" "$PIN" <<'PYEOF'
import difflib, re, subprocess, sys
new = open(sys.argv[1], encoding="utf-8").read().splitlines()
old = subprocess.run(["git", "show", sys.argv[2]], capture_output=True).stdout.decode("utf-8").splitlines()
sm = difflib.unified_diff(old, new, lineterm="", n=0)
removed = [l[1:] for l in sm if l.startswith("-") and not l.startswith("---")]
added = [l[1:] for l in difflib.unified_diff(old, new, lineterm="", n=0) if l.startswith("+") and not l.startswith("+++")]
changed = max(len(removed), len(added))
rm_ok = all(("120" in l) or ("rows" in l and "within" in l) for l in removed) if removed else False
keep = ["columns_dropped", "set(wide[\"trades\"][0])", "within the 50 KB answer", "not wide.get(\"truncated\")"]
keep_ok = all(sum(1 for l in new if k in l) >= sum(1 for l in old if k in l) and sum(1 for l in old if k in l) >= 1 for k in keep)
m = re.search(r"_wide_trade_part\((\d+)\)", "\n".join(new))
n = int(m.group(1)) if m else None
n_ok = n is not None and 60 <= n <= 119
asserts_ok = n is not None and len(re.findall(r"==\s*%d\b" % n, "\n".join(new))) >= 2
left120 = sum(1 for l in new if re.search(r"\b120\b", l))
print("lines changed %d (want 1 to 12); every removed line names the old row count or the row-count comment: %s" % (changed, "ok" if rm_ok else "NO"))
print("narrowing assertions kept: %s; new row count N %s (want 60 to 119); N appears in the part builder call and in at least two row-count assertions: %s; lines still naming 120: %d (want 0)" % ("ok" if keep_ok else "NO", n, "ok" if (n_ok and asserts_ok) else "NO", left120))
print("OK" if 1 <= changed <= 12 and rm_ok and keep_ok and n_ok and asserts_ok and left120 == 0 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
