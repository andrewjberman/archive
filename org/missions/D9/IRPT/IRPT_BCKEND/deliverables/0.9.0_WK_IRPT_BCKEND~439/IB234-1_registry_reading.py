"""IB234-1 registry reading: the ARN prefixes the iam.tf locals build, evaluated from the registry files alone.

Performs the same lookups the HCL locals in infra/aws/terraform/inf-pipeline/iam.tf perform (systems.json by key,
scopes.json by key, tiers.json FIRM homes by tier), composes the ARN prefixes the way those locals compose them,
and compares them, character for character, with lib/opal_naming.py address() output for the bronze and silver layers.
No AWS call, no terraform run, no registry write.

Run from the worktree root:  python <path to this file> <worktree root>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
REG = ROOT / "infra" / "logic" / "registry"
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming as mod  # noqa: E402

SOURCE_KEY = "orion"
SCOPE_KEY = "inflection"
TABLE = "scope_account_returns"
POLICY_ARGS = {"system": "orion", "scope": "inflection", "function": "scope-account-feed", "kind": "policy"}


def load(name):
    return json.loads((REG / name).read_text(encoding="utf-8"))


systems = {r["key"]: r for r in load("systems.json")["systems"]}
scopes = {r["key"]: r for r in load("scopes.json")["scopes"]}
firm_tiers = load("tiers.json")["homes"]["FIRM"]

source = systems[SOURCE_KEY]["key"]
scope = scopes[SCOPE_KEY]["long"]

evaluated = {}
for tier in ("bronze", "silver"):
    bucket = firm_tiers[tier]["bucket"]
    key = "%s/%s/%s/%s" % (source, scope, tier, TABLE)
    arn_prefix = "arn:aws:s3:::%s/%s/*" % (bucket, key)
    list_prefix = "%s/*" % key
    addr = mod.address("orion", "inflection", tier, TABLE, "date=2000-01-01", "x")
    expected = re.sub(r"^s3://", "arn:aws:s3:::", addr).replace("date=2000-01-01/x", "*")
    evaluated[tier] = {"arn_prefix": arn_prefix, "list_prefix": list_prefix, "address_arn": expected}

match = all(v["arn_prefix"] == v["address_arn"] for v in evaluated.values())
object_prefixes = [evaluated[t]["arn_prefix"] for t in ("bronze", "silver")]
list_prefixes = [evaluated[t]["list_prefix"] for t in ("bronze", "silver")]
for tier in ("bronze", "silver"):
    print("LAYER %s" % tier)
    print("  local object ARN prefix : %s" % evaluated[tier]["arn_prefix"])
    print("  address() object prefix : %s" % evaluated[tier]["address_arn"])
    print("  local list prefix       : %s" % evaluated[tier]["list_prefix"])
    print("  equal                   : %s" % (evaluated[tier]["arn_prefix"] == evaluated[tier]["address_arn"]))

policy_name = mod.name(POLICY_ARGS["system"], POLICY_ARGS["scope"], POLICY_ARGS["function"], POLICY_ARGS["kind"])
verdict, canon = mod.grade(policy_name, "IAM_POLICY")
print("POLICY name()=%s grade(IAM_POLICY)=%s canonical=%s" % (policy_name, verdict, canon))
print("OBJECT_PREFIXES %s" % json.dumps(object_prefixes))
print("LIST_PREFIXES %s" % json.dumps(list_prefixes))
print("RESULT %s" % ("MATCH" if match and verdict == "CONFORMANT" else "MISMATCH"))
sys.exit(0 if match and verdict == "CONFORMANT" else 1)
