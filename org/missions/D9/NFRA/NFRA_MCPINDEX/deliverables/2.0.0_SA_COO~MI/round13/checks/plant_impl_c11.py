# plant_impl_c11.py -- the ISSUER's reference for the c11 checks' planted PASS arm (standing battery clause 1). NOT given to the
# worker, NOT a criterion. It implements, minimally, what c11.AC1-AC3 grade, so the checks can be shown to PASS on a correct
# implementation and to FAIL on a lax one (C11_PLANT_LAX=1: the loader accepts everything).
#
# DATA_CATALOG v0.5 (planted header text for AC3).
# Andrew-direct 2026-10-14 ~12:4xZ, verbatim: "We need to colonize that bucket. We need to figure out all the gold and silver tables that are in that bucket and where we want to create tools because the asset managers need to be able to do direct research right to the bucket."
# Record: org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_124xZ_GATEWAY_DATA_CONTRACTS_CENSUS_CRO_FANOUT.md
import glob
import importlib.util
import os
import shutil
import sys
import tempfile

import yaml

_HEADER = """
version: 0.5
supersedes: v0.4 (planted)
"""

_REAL_PATH = os.path.join("workflows", "atom_decomposition", "emit_catalog_v02.py")
_spec = importlib.util.spec_from_file_location("emit_real", _REAL_PATH)
_real = importlib.util.module_from_spec(_spec)
sys.modules["emit_real"] = _real
_spec.loader.exec_module(_real)

CATALOG_ENTRIES_DIR = _real.CATALOG_ENTRIES_DIR
TOOL_INDEX_DIR = _real.TOOL_INDEX_DIR
TOP = {"amgt", "barrons", "bloomberg", "crosswalk", "derived", "drafting", "filings", "ft", "identity", "issuer-site", "lib",
       "management", "packs", "peers", "posture", "publication-links", "publications", "raw", "scores", "sec", "seeking-alpha",
       "social", "universe", "wsj"}
FIELDS = set(_real.HARVEST_FIELDS) | {"table", "layer", "format", "contract", "nl_tags", "retired"}
LAYERS = {"gold", "silver", "bronze", "state"}
CLAIMS = {"measured", "inferred", "absent"}


def _validate(name, d):
    if os.environ.get("C11_PLANT_LAX"):
        return []
    e = []
    allowed = set(FIELDS) | ({"retired_reason"} if d.get("retired") is True else set())
    if set(d) != allowed:
        e.append("fields differ")
    pre = d.get("prefix", "")
    if pre in ("amgt/harvest/gold/",) or pre.split("/")[0] not in TOP or not pre.endswith("/"):
        e.append("prefix")
    if name != "harvest_" + _real.harvest_slug(pre):
        e.append("name")
    if not isinstance(d.get("retired"), bool):
        e.append("retired type")
    if d.get("layer") not in LAYERS:
        e.append("layer")
    c = d.get("contract")
    if not (isinstance(c, dict) and c.get("id") and (c.get("size") or {}).get("claim") in CLAIMS):
        e.append("contract")
    return e


def load_harvest_entries():
    rows, errors = {}, {}
    for path in sorted(glob.glob(os.path.join(CATALOG_ENTRIES_DIR, "harvest_*.yaml"))):
        name = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        errs = _real._resolve_prefix_key(name, data) or _validate(name, data)
        if errs:
            errors[name] = errs
        else:
            rows[name] = data
    return rows, errors


def load_tool_index(row_ids, census=None, row_keys=None):
    served = {t["tool"] for t in census["tools"]}
    tmp = tempfile.mkdtemp(prefix="plant_ti_")
    for f in glob.glob(os.path.join(TOOL_INDEX_DIR, "*")):
        if os.path.isfile(f):
            shutil.copy(f, tmp)
    with open(os.path.join(tmp, "members.yaml"), encoding="utf-8") as f:
        members = yaml.safe_load(f)
    for t in ("harvest_list", "harvest_read"):
        if t in served:
            members["members"].append({"tool": t, "member": "b", "owner": "AMGT_HARVST"})
    with open(os.path.join(tmp, "members.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(members, f, sort_keys=False)
    _real.TOOL_INDEX_DIR = tmp
    try:
        return _real.load_tool_index(row_ids, census=census, row_keys=row_keys)
    finally:
        _real.TOOL_INDEX_DIR = TOOL_INDEX_DIR
        shutil.rmtree(tmp, ignore_errors=True)


def harvest_read_tool_errors(rows, served):
    return ["%s: read_tool %s is not a served tool" % (k, r["read_tool"]) for k, r in rows.items()
            if r.get("read_tool") and r["read_tool"] not in served]
