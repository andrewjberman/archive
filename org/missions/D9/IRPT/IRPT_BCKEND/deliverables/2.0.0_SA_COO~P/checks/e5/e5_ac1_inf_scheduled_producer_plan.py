"""~E round 5 AC1 (IB-er-501) -- the holdings-performance root schedules the Inflection producer too (1.0.0_SA_CTO 102832:
an INF switch needs a SCHEDULED producer and fire, never a gold written only by a local run).

Usage: python e5_ac1_inf_scheduled_producer_plan.py <worktree root>
Runs `terraform plan` (terraform on PATH, v1.14+; the root's locals need && short-circuit) on
infra/aws/terraform/investor-reporting/holdings-performance and reads `terraform show -json` of that plan.
Pass, all of:
  (1) the plan CREATES exactly one aws_scheduler_schedule whose target input JSON has source == "orion";
  (2) after the plan, some IAM policy document on the producer's role names an `orion/` silver object prefix AND the
      Inflection gold prefix `irpt/inflection/gold/holdings_performance_daily/` (builder output);
  (3) no policy document names a `blackdiamond` prefix (Cottonwood is not in this cell), and no ONE policy document
      grants both the 49F and the Inflection gold (firm isolation: a function and role per scheduled source);
  (4) the plan destroys nothing (the 49F function, role and schedule keep their addresses).
Read-only against AWS (plan with -lock=false); writes a plan file under the system temp dir only.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
tf_root = root / "infra/aws/terraform/investor-reporting/holdings-performance"
tf = shutil.which("terraform")
if not tf:
    print("E5-AC1 FAIL (terraform not on PATH)")
    sys.exit(1)
plan = os.path.join(tempfile.mkdtemp(prefix="e5ac1_"), "plan.bin")
subprocess.run([tf, "-chdir=%s" % tf_root, "init", "-input=false", "-no-color", "-reconfigure"], capture_output=True, check=True)
r = subprocess.run([tf, "-chdir=%s" % tf_root, "plan", "-input=false", "-no-color", "-lock=false", "-out=%s" % plan],
                   capture_output=True, text=True)
if r.returncode != 0:
    print((r.stdout + r.stderr)[-1500:])
    print("E5-AC1 FAIL (plan did not run)")
    sys.exit(1)
doc = json.loads(subprocess.run([tf, "-chdir=%s" % tf_root, "show", "-json", plan], capture_output=True, check=True).stdout)
changes = doc.get("resource_changes", [])
created_orion = []
for c in changes:
    if c["type"] == "aws_scheduler_schedule" and c["change"]["actions"] == ["create"]:
        for t in (c["change"]["after"] or {}).get("target") or []:
            try:
                if json.loads(t.get("input") or "{}").get("source") == "orion":
                    created_orion.append(c["address"])
            except ValueError:
                pass
destroys = [c["address"] for c in changes if "delete" in c["change"]["actions"]]
policies = []
for c in changes:
    after = c["change"].get("after") or {}
    for key in ("policy", "inline_policy"):
        v = after.get(key)
        if isinstance(v, str) and v.strip().startswith("{"):
            policies.append(v)
        elif isinstance(v, list):
            policies += [x.get("policy", "") for x in v if isinstance(x, dict)]
# unchanged resources keep their policy in prior_state/planned_values
for res in (doc.get("planned_values", {}).get("root_module", {}).get("resources", [])
            + [r for m in doc.get("planned_values", {}).get("root_module", {}).get("child_modules", []) for r in m.get("resources", [])]):
    v = (res.get("values") or {}).get("policy")
    if isinstance(v, str):
        policies.append(v)
blob = "\n".join(policies)
orion_silver = "orion/" in blob
inf_gold = "irpt/inflection/gold/holdings_performance_daily/" in blob
bd = "blackdiamond" in blob
# firm isolation: no ONE policy document may grant both firms' gold (a role per scheduled source)
mixed = [p for p in policies if "irpt/49financial/gold/" in p and "irpt/inflection/gold/" in p]
print("created schedules with source orion: %s" % created_orion)
print("policy names orion/ silver: %s | INF gold prefix: %s | blackdiamond: %s | policies granting both firms: %d | destroys: %s"
      % (orion_silver, inf_gold, bd, len(mixed), destroys))
ok = len(created_orion) == 1 and orion_silver and inf_gold and not bd and not mixed and not destroys
print("E5-AC1 PASS" if ok else "E5-AC1 FAIL")
sys.exit(0 if ok else 1)
