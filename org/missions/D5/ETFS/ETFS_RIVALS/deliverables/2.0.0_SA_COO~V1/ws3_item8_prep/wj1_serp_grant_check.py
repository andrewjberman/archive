"""RIV-wj-1 AC1 (CTO ruling ADDENDUM 7 @aa290d707e) -- the generated stack grants the daily Lambda ONE read of the ONE
existing Bright Data key secret, and carries its name and the zone in that Lambda's environment. Nothing else moves.

    python wj1_serp_grant_check.py      (run from the repository root; read-only; regenerates into a temp dir)

Regenerates with `infra/aws/terraform/etfs-rivalfunds/gen_policies.py --out <tmp>` and compares with the committed copies
at the base commit e17ab4e69d (`git show`):
  (1) the daily Lambda's policy has exactly ONE statement more than at the base: Action exactly
      ["secretsmanager:GetSecretValue"], Resource exactly [ARN] (no wildcard);
  (2) every other statement of the daily policy, and the other four policies, are unchanged;
  (3) the daily Lambda's environment gains exactly RIVALFUNDS_SERP_SECRET = ARN and BD_SERP_ZONE = serp_opal, and keeps
      its two existing keys; no other Lambda gains an environment; nothing else in generated.auto.tfvars.json changes;
  (4) the committed copies in the working tree equal the fresh regeneration byte for byte, line endings normalized
      (a Windows checkout writes CRLF).
Exit 0 = PASS, 1 = FAIL.
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(os.getcwd())
T = "infra/aws/terraform/etfs-rivalfunds"
BASE = "e17ab4e69d"
ARN = "arn:aws:secretsmanager:us-east-1:313476888478:secret:find-insure/bright-data/api-key-7ojPkd"
DAILY = "etfs-rivalfunds-daily-lambda"
CRLF, LF = bytes([13, 10]), bytes([10])


def show(path):
    r = subprocess.run(["git", "show", f"{BASE}:{path}"], capture_output=True, text=True, encoding="utf-8",
                       env={**os.environ, "MSYS_NO_PATHCONV": "1"})
    if r.returncode != 0:
        raise SystemExit(f"git show {BASE}:{path} failed: {r.stderr.strip()}")
    return r.stdout


tmp = pathlib.Path(tempfile.mkdtemp(prefix="wj1-"))
r = subprocess.run([sys.executable, f"{T}/gen_policies.py", "--out", str(tmp)], capture_output=True, text=True)
fails = []
if r.returncode != 0:
    print(r.stdout[-800:], r.stderr[-800:])
    print("WJ1 RESULT: FAIL 1 failures")
    sys.exit(1)
new_vars = json.loads((tmp / "generated.auto.tfvars.json").read_text(encoding="utf-8"))
old_vars = json.loads(show(f"{T}/generated.auto.tfvars.json"))
pol_names = sorted(p.name for p in (tmp / "policies").glob("*.json"))
for pn in pol_names:
    new = json.loads((tmp / "policies" / pn).read_text(encoding="utf-8"))
    old = json.loads(show(f"{T}/policies/{pn}"))
    if pn != f"{DAILY}.json":
        if new != old:
            fails.append(f"(2) {pn} changed")
        continue
    added = [s for s in new["Statement"] if s not in old["Statement"]]
    removed = [s for s in old["Statement"] if s not in new["Statement"]]
    print(f"{pn}: statements {len(old['Statement'])} -> {len(new['Statement'])}; added {added}; removed {removed}")
    if len(added) != 1 or removed:
        fails.append(f"(1)/(2) the daily policy must gain exactly one statement and lose none (added {len(added)}, removed {len(removed)})")
    elif added[0].get("Action") != ["secretsmanager:GetSecretValue"] or added[0].get("Resource") != [ARN] or added[0].get("Effect") != "Allow":
        fails.append(f"(1) the new statement is not GetSecretValue on exactly {ARN}")
lam_new, lam_old = new_vars.get("lambdas", {}), old_vars.get("lambdas", {})
env_new = (lam_new.get(DAILY) or {}).get("environment", {})
env_old = (lam_old.get(DAILY) or {}).get("environment", {})
print(f"daily environment keys: {sorted(env_old)} -> {sorted(env_new)}")
want = dict(env_old, RIVALFUNDS_SERP_SECRET=ARN, BD_SERP_ZONE="serp_opal")
if env_new != want:
    fails.append("(3) the daily environment is not the old keys plus RIVALFUNDS_SERP_SECRET=ARN and BD_SERP_ZONE=serp_opal")
for fn in lam_new:
    if fn != DAILY and (lam_new[fn].get("environment") or {}) != ((lam_old.get(fn) or {}).get("environment") or {}):
        fails.append(f"(3) {fn} environment changed")
rest_new = dict(new_vars, lambdas={k: {kk: vv for kk, vv in v.items() if kk != "environment"} for k, v in lam_new.items()})
rest_old = dict(old_vars, lambdas={k: {kk: vv for kk, vv in v.items() if kk != "environment"} for k, v in lam_old.items()})
if rest_new != rest_old:
    fails.append("(3) generated.auto.tfvars.json changed outside the daily environment")
for rel in ["generated.auto.tfvars.json"] + [f"policies/{p}" for p in pol_names]:
    if (ROOT / T / rel).read_bytes().replace(CRLF, LF) != (tmp / rel).read_bytes().replace(CRLF, LF):  # Windows checkout: CRLF
        fails.append(f"(4) committed {T}/{rel} differs from the regeneration")
for f in fails:
    print("FAIL:", f)
print(f"WJ1 RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
