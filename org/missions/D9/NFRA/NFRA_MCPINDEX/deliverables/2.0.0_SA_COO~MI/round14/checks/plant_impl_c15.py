# plant_impl_c15.py -- the ISSUER's reference for the c15 checks' planted PASS arm (standing battery clause 1). NOT given to the
# worker, NOT a criterion. C15_PLANT_LAX=1 makes the table-row validator accept everything; C15_PLANT_NOJOIN=1 skips the registry join.
import glob
import importlib.util
import json
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


def _str_or_null(v):
    return v is None or (isinstance(v, str) and bool(v.strip()))


def _validate_table(name, d):
    if os.environ.get("C15_PLANT_LAX"):
        return []
    e = []
    allowed = BASE | set(TABLE) | ({"retired_reason"} if d.get("retired") is True else set())
    if set(d) != allowed:
        e.append("fields differ")
    c = d.get("contract")
    if not (isinstance(c, dict) and set(c) == {"id", "label"} | set(CLAIM_BLOCKS) and c.get("id") and c.get("label")
            and all(isinstance(c.get(k), dict) for k in CLAIM_BLOCKS)):
        e.append("contract")
    fk = d.get("fork_keys")
    if not (isinstance(fk, dict) and set(fk) <= {"firm", "account", "platform"} and all(v is None or isinstance(v, dict) for v in fk.values())):
        e.append("fork_keys")
    if not _str_or_null(d.get("prefix")) or not _str_or_null(d.get("table")) or not _str_or_null(d.get("bucket")):
        e.append("prefix or table")
    if d.get("layer") not in LAYERS:
        e.append("layer")
    if not isinstance(d.get("retired"), bool) or (d.get("retired") is True and not d.get("retired_reason")):
        e.append("retired")
    if d.get("firm_scope_rule") not in _real.ENTRY_FIRM_SCOPE_RULES:
        e.append("firm_scope_rule")
    if not isinstance(d.get("tools"), list) or not isinstance(d.get("open_items"), list):
        e.append("list fields")
    rt, go = d.get("read_tool"), d.get("gap_owner")
    if (rt is None) == (go is None):
        e.append("read_tool / gap_owner pairing")
    return e


def _join(data):
    if os.environ.get("C15_PLANT_NOJOIN"):
        return data
    sys.path.insert(0, os.path.join(os.getcwd(), "lib"))
    import opal_naming
    p = os.path.join(opal_naming.REGISTRY_DIR, "catalog_fork_keys.json")
    rows = json.load(open(p, encoding="utf-8")).get("rows", {}) if os.path.exists(p) else {}
    hit = rows.get((data.get("contract") or {}).get("id"))
    if hit:
        data = dict(data)
        data.update(hit.get("restore") or {})
        data["key_template"] = hit.get("key_template")
    return data


def load_catalog_entries():
    entries, errors = {}, {}
    for path in sorted(glob.glob(os.path.join(CATALOG_ENTRIES_DIR, "*.yaml"))):
        name = os.path.splitext(os.path.basename(path))[0]
        if name.startswith(("need_", "harvest_")):
            continue
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        table = isinstance(data, dict) and "contract" in data
        errs = _validate_table(name, data) if table else _real.validate_entry(name, data)
        if errs:
            errors[name] = errs
        else:
            entries[name] = _join(data) if table else data
    return entries, errors


def silver_catalog_row(name, data):
    row = {"entity": name}
    fields = tuple(_real.ENTRY_REQUIRED_FIELDS) + tuple(_real.SILVER_READER_FIELDS)
    if "contract" in data:
        fields = fields + TABLE + ("retired_reason", "key_template")
    for f in fields:
        if f in data:
            row[f] = data[f]
    return row
