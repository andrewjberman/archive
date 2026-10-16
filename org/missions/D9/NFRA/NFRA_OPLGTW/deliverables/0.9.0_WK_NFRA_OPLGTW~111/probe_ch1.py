"""NFRA_OPLGTW OG-ch-1 probe (worker 0.9.0_WK_NFRA_OPLGTW~111), re-run as AC2 by the issuer.

Imports the client core and every app/client_adapter_*.py on this head, registers them all in one process, and
prints exactly one verdict line of booleans. No account, name or amount is read or printed.
"""
import glob
import importlib
import json
import os
import sys


def _find_root():
    """The worktree root: the directory whose infra/aws/ec2/opal-gateway carries app/client_core.py."""
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(cur, "infra", "aws", "ec2", "opal-gateway", "app", "client_core.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("probe ch1: gateway not found above " + __file__)
        cur = parent


ROOT = _find_root()
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, GW)

from app import client_core as core  # noqa: E402
from app import client_role  # noqa: E402

ROSTER = os.path.join(ROOT, "data", "mdpf", "config", "partner_roster.json")

# (a) every adapter file on this head registers, one module each
files = sorted(glob.glob(os.path.join(GW, "app", "client_adapter_*.py")))
mods = [importlib.import_module("app." + os.path.basename(f)[:-3]) for f in files]
core._adapters.clear()
for mod in mods:
    core.register_adapter(mod)
registered = sum(len(held) for held in core._adapters.values())
adapters_registered_equals_files = registered == len(files) and len(files) > 0

# (b) the two Black Diamond firms route to different modules, and the fence names one segment for each over the repo
# catalog read through the core's own loader (app/refs/DATA_CATALOG.yaml, query_v0._catalog)
try:
    bd_49 = core._adapter("blackdiamond", "49financial")
    bd_cw = core._adapter("blackdiamond", "cottonwood")
    bd_split = bd_49 is not bd_cw
except core.CoreRefusal:
    bd_split = False
# the loader returns {"catalog": <the YAML document>, "rows_by_key": ...}; the probe passes the document's own "catalog" key
catalog_ctx = core.Ctx(catalog_doc=core._runtime_catalog()["catalog"])
bd_split = (bd_split and catalog_ctx.firm_segments("blackdiamond", "49financial") == ["49f"]
            and catalog_ctx.firm_segments("blackdiamond", "cottonwood") == ["cottonwood"])

# (c) the two firm role keys differ, and neither equals the other's environment variable name
key_49 = client_role.role_key("blackdiamond", "49f")
key_cw = client_role.role_key("blackdiamond", "cottonwood")
env_49 = client_role.role_env_name(key_49)
env_cw = client_role.role_env_name(key_cw)
role_keys_distinct = key_49 != key_cw and key_49 != env_cw and key_cw != env_49 and env_49 != env_cw

# (d) the roster name map reaches 49financial, and inflection when the file names it
with open(ROSTER, encoding="utf-8") as fh:
    file_firms = {p.get("firm_id") for p in json.load(fh).get("partners", []) if isinstance(p, dict)}
core.ROSTER_FILE = ROSTER
mapped = set(core.Ctx(catalog_doc={}).firm_roster().values())
roster_names_mapped = "49financial" in mapped and ("inflection" not in file_firms or "inflection" in mapped)

print("probe ch1: adapters_registered_equals_files %s; bd_split %s; role_keys_distinct %s; roster_names_mapped %s"
      % (adapters_registered_equals_files, bd_split, role_keys_distinct, roster_names_mapped))
