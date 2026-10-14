# plant_impl_c13.py -- the ISSUER's reference for the c13 checks' planted PASS arm (standing battery clause 1). NOT given to the
# worker, NOT a criterion. Header text (planted): opal-data-mdpf gold is a measured mirror of the served platinum (G4, overlap 100%). C13_PLANT_LAX=1 makes the table-row validator accept everything (the lax arm).
import glob
import importlib.util
import os
import sys

import yaml

_spec = importlib.util.spec_from_file_location("emit_real", os.path.join("workflows", "atom_decomposition", "emit_catalog_v02.py"))
_real = importlib.util.module_from_spec(_spec)
sys.modules["emit_real"] = _real
_spec.loader.exec_module(_real)

CATALOG_ENTRIES_DIR = _real.CATALOG_ENTRIES_DIR
LAYERS = {"gold", "silver", "bronze", "state", "served", "platinum", "dynamodb"}
CLAIM_BLOCKS = ("size", "freshness", "partition", "producer")
BASE = set(_real.ENTRY_REQUIRED_FIELDS) | set(_real.SILVER_READER_FIELDS)
TABLE = ("bucket", "prefix", "table", "layer", "format", "contract", "fork_keys", "nl_tags", "retired", "open_items", "gap_owner")


def _validate_table(name, d):
    if os.environ.get("C13_PLANT_LAX"):
        return []
    e = []
    allowed = BASE | set(TABLE) | ({"retired_reason"} if d.get("retired") is True else set())
    if set(d) != allowed:
        e.append("fields differ")
    c = d.get("contract")
    if not (isinstance(c, dict) and c.get("id") and all(isinstance(c.get(k), dict) for k in CLAIM_BLOCKS)):
        e.append("contract")
    fk = d.get("fork_keys")
    if not (isinstance(fk, dict) and {"firm", "account", "platform"} <= set(fk)):
        e.append("fork_keys")
    if d.get("layer") not in LAYERS:
        e.append("layer")
    if not isinstance(d.get("retired"), bool):
        e.append("retired type")
    if d.get("firm_scope_rule") not in _real.ENTRY_FIRM_SCOPE_RULES:
        e.append("firm_scope_rule")
    if not isinstance(d.get("tools"), list) or not isinstance(d.get("open_items"), list):
        e.append("list fields")
    rt, go = d.get("read_tool"), d.get("gap_owner")
    if (rt is None) == (go is None):
        e.append("read_tool / gap_owner pairing")
    return e


def load_catalog_entries():
    entries, errors = {}, {}
    for path in sorted(glob.glob(os.path.join(CATALOG_ENTRIES_DIR, "*.yaml"))):
        name = os.path.splitext(os.path.basename(path))[0]
        if name.startswith(("need_", "harvest_")):
            continue
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        errs = _validate_table(name, data) if isinstance(data, dict) and "contract" in data else _real.validate_entry(name, data)
        if errs:
            errors[name] = errs
        else:
            entries[name] = data
    return entries, errors


def silver_catalog_row(name, data):
    row = {"entity": name}
    fields = tuple(_real.ENTRY_REQUIRED_FIELDS) + tuple(_real.SILVER_READER_FIELDS)
    if "contract" in data:
        fields = fields + TABLE + ("retired_reason",)
    for f in fields:
        if f in data:
            row[f] = data[f]
    return row
