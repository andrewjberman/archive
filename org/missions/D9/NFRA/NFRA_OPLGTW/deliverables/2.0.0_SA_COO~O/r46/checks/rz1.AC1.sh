#!/usr/bin/env bash
# OPLGTW OG-rz-1 AC1: the unit's memory limits, the test bounds and the contract's target instance type name the t4g.large host,
# and nothing else changed against the base (box/sitez at the cut).
#  - deploy/opal-gateway.service: MemoryHigh=5600M, MemoryMax=6400M, MemoryHigh strictly below MemoryMax;
#  - deploy/NFRA_OPLGTW_CONTRACT.json: target_instance_type == t4g.large;
#  - tests/test_og_un1.py names the new bounds (4000..7000, the new expected lines);
#  - git diff against the base: exactly the three files; in the contract exactly one changed line.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
BASE="${RZ1_BASE:-96cca43b19604141f85b819037a3b92f6c2bdf03}"
GW="infra/aws/ec2/opal-gateway"
python - "$GW" "$BASE" <<'EOF'
import json, re, subprocess, sys
gw, base = sys.argv[1], sys.argv[2]
def rd(p):
    return open(p, encoding="utf-8", newline="").read()
unit = rd(gw + "/deploy/opal-gateway.service")
mh = re.findall(r"(?m)^MemoryHigh=(\d+)M\s*$", unit); mm = re.findall(r"(?m)^MemoryMax=(\d+)M\s*$", unit)
ok_u = mh == ["5600"] and mm == ["6400"]
ok_lt = ok_u and int(mh[0]) < int(mm[0])
m = re.search(r'"target_instance_type"\s*:\s*"([^"]+)"', rd(gw + "/deploy/NFRA_OPLGTW_CONTRACT.json"))
ok_c = bool(m) and m.group(1) == "t4g.large"
t = rd(gw + "/tests/test_og_un1.py")
ok_t = ("4000 <= max_mb <= 7000" in t) and ('"MemoryHigh=5600M"' in t) and ('"MemoryMax=6400M"' in t) and ("1000 <= max_mb <= 1500" not in t)
names = subprocess.run(["git", "diff", "--name-only", base, "--", "."], capture_output=True, text=True).stdout.split()
want = {gw + "/deploy/opal-gateway.service", gw + "/tests/test_og_un1.py", gw + "/deploy/NFRA_OPLGTW_CONTRACT.json"}
files_ok = set(names) == want
d = subprocess.run(["git", "diff", "-U0", base, "--", gw + "/deploy/NFRA_OPLGTW_CONTRACT.json"], capture_output=True, text=True).stdout
chg = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
contract_ok = len(chg) == 2 and all("target_instance_type" in l for l in chg)
outside = (0 if contract_ok else max(len(chg), 1)) + len(set(names) - want)
print("unit MemoryHigh %sM MemoryMax %sM (want 5600M and 6400M): %s; MemoryHigh strictly below MemoryMax: %s" % (mh[0] if mh else "?", mm[0] if mm else "?", "yes" if ok_u else "no", "yes" if ok_lt else "no"))
print("contract target_instance_type %s (want t4g.large): %s; test_og_un1 names the new bounds: %s" % (m.group(1) if m else "?", "yes" if ok_c else "no", "yes" if ok_t else "no"))
print("files changed against the base %d (want 3); lines changed outside the named ones %d (want 0)" % (len(names), outside))
ok = ok_u and ok_lt and ok_c and ok_t and files_ok and outside == 0
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
EOF
