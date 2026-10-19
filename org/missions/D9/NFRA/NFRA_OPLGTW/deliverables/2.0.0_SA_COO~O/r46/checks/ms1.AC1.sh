#!/usr/bin/env bash
# OPLGTW OG-ms-1 AC1: master 08403355 is registered in the gateway's entitlement code, audit set, BOTH contract copies and the
# scopes registry, and nothing else changed against the worker branch's merge-base with box/sitez (run in the WORKER worktree).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
BASE="${MS1_BASE:-$(git merge-base HEAD box/sitez)}"
GW="infra/aws/ec2/opal-gateway"
python - "$GW" "$BASE" <<'EOF'
import json, re, subprocess, sys
gw, base = sys.argv[1], sys.argv[2]
M = "08403355"
def rd(p):
    return open(p, encoding="utf-8", newline="").read()
de = rd(gw + "/app/data_entitlement.py"); au = rd(gw + "/app/schwab_audit.py")
ok_de = bool(re.search(r'(?m)^MASTERS\s*=\s*\(\s*"08242234"\s*,\s*"08335338"\s*,\s*"08403355"\s*\)', de))
ok_au = bool(re.search(r'(?m)^_MASTERS\s*=\s*frozenset\(\{[^}]*"08403355"[^}]*\}\)', au))
dep = gw + "/deploy/NFRA_OPLGTW_CONTRACT.json"; std = "org/standards/NFRA_OPLGTW_CONTRACT.json"
try:
    c = json.loads(rd(dep))
except Exception:
    c = {}
nm, nd, nc = len(c.get("masters", {})), len(c.get("data_prefixes", [])), len(c.get("completion_prefixes", []))
ok_c = nm == 3 and nd == 12 and nc == 3 and M in c.get("masters", {}) and all(
    ("schwab/%s/silver/%s/" % (M, t)) in c.get("data_prefixes", []) for t in ("dim_position", "dim_balance", "dim_asset", "dim_transaction")) and (
    "schwab/%s/meta/complete/" % M) in c.get("completion_prefixes", [])
eq = open(dep, "rb").read() == open(std, "rb").read()
ti = [bool(re.search(r'"target_instance_type"\s*:\s*"t4g\.large"', rd(p))) for p in (dep, std)]
try:
    sc = json.loads(rd("infra/logic/registry/scopes.json"))
    s = json.dumps(sc)
    firm_ok = '"masters": ["08242234", "08335338", "08403355"]' in rd("infra/logic/registry/scopes.json")
    def walk(o):
        if isinstance(o, dict):
            if o.get("key") == M and o.get("class") == "MASTER" and o.get("vendor") == "schwab" and o.get("firm") == "49financial":
                return True
            return any(walk(v) for v in o.values())
        if isinstance(o, list):
            return any(walk(v) for v in o)
        return False
    row_ok = walk(sc)
except Exception:
    firm_ok = row_ok = False
names = subprocess.run(["git", "diff", "--name-only", base, "--", "."], capture_output=True, text=True).stdout.split()
named = {gw + "/app/data_entitlement.py", gw + "/app/schwab_audit.py", dep, std, "infra/logic/registry/scopes.json", gw + "/tests/test_og_ms1.py"}
outside = [n for n in names if n not in named and not n.startswith(gw + "/tests/")]
print("MASTERS names 08403355: %s; schwab_audit _MASTERS names 08403355: %s; contract masters %d (want 3), data_prefixes %d (want 12), completion_prefixes %d (want 3): %s; the two contract copies byte-equal: %s; target_instance_type t4g.large in both: %s"
      % ("yes" if ok_de else "no", "yes" if ok_au else "no", nm, nd, nc, "yes" if ok_c else "no", "yes" if eq else "no", "yes" if all(ti) else "no"))
print("scopes.json firm masters 3 and a MASTER row for 08403355: %s" % ("yes" if firm_ok and row_ok else "no"))
print("files changed against the merge-base %d; outside the named set %d (want 0)" % (len(names), len(outside)))
ok = ok_de and ok_au and ok_c and eq and all(ti) and firm_ok and row_ok and not outside and gw + "/tests/test_og_ms1.py" in names
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
EOF
