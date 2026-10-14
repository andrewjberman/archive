"""g1lib.py -- the round-13 checks' ONE reader of G1 (the CRO's harvest data-contract census), at a PINNED commit.

The pin is read with `git show <pin>:<path>`, never the working copy: the CRO may amend the file after the cut, and a
check graded against a moving file would grade a different object each run.
"""
import json
import re
import os
import subprocess
import sys
import tempfile

PIN = "0d7c29b3c5"
G1_PATH = "org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/GATEWAY_DATA_CONTRACTS_20261014/G1_harvest.md"
EXPECT_CONTRACTS = 78
LEGACY_HYPHEN_TABLES = ("research-backlog", "research-continuation", "research-dossier", "research-fund-form",
                        "research-model-typecast", "research-sector-template")
# NINE legacy read addresses (their prefixes predate the canon, which spells them with `_`): the six hyphenated gold tables that
# round 12 registered, and THREE bronze/silver research-report tables the commit-time naming gate refuses as literals (round 13).
# prefix -> legacy_addresses.json key. A row names the KEY, never the literal.
LEGACY_PREFIXES = dict(
    [("amgt/harvest/gold/%s/" % t, "harvest-gold-" + t) for t in LEGACY_HYPHEN_TABLES] +
    [("amgt/harvest/bronze/research-report/", "harvest-bronze-research-report"),
     ("amgt/harvest/bronze/research-report-extract/", "harvest-bronze-research-report-extract"),
     ("amgt/harvest/silver/research-report/", "harvest-silver-research-report")])
NEW_LEGACY_KEYS = ("harvest-bronze-research-report", "harvest-bronze-research-report-extract", "harvest-silver-research-report")


def enc(contract_id):
    """The row's contract.id: G's contract_id with every `/` replaced by `:`. It is an IDENTIFIER, not an S3 address: the
    commit-time naming gate grades any slash-bearing string as an S3 key and refuses these 78 as out-of-pattern."""
    return str(contract_id).replace("/", ":")


def use_registry():
    """Point lib/opal_naming at PLANT_REGISTRY_DIR when set (the cut-time planted arms only: a registry copy that already holds the
    three new legacy rows). Unset in every criterion."""
    d = os.environ.get("PLANT_REGISTRY_DIR")
    if d:
        sys.path.insert(0, os.path.join(os.getcwd(), "lib"))
        import opal_naming
        opal_naming.REGISTRY_DIR = d


def plant_registry_dir():
    """A temp copy of infra/logic/registry with the three new legacy rows added (planted arms only). Returns its path."""
    import shutil
    d = tempfile.mkdtemp(prefix="c12reg_")
    src = os.path.join("infra", "logic", "registry")
    shutil.copytree(src, d, dirs_exist_ok=True)
    p = os.path.join(d, "legacy_addresses.json")
    doc = json.load(open(p, encoding="utf-8"))
    for prefix, key in LEGACY_PREFIXES.items():
        if key in NEW_LEGACY_KEYS:
            doc["legacy_addresses"].append({"key": key, "bucket": "opal-data-harvest", "template": prefix, "shape": "prefix",
                                            "params": [], "reader": "NFRA_MCPINDEX", "evidence": "planted for the check arms",
                                            "note": "AMGT_HARVST owns any rename (R19)."})
    json.dump(doc, open(p, "w", encoding="utf-8"), indent=1)
    return d
RETIRE_REQUIRED = ("publication-links/v1/", "publications/v1/")
RETIRE_CONDITIONAL = "amgt/harvest/gold/research-dossier/"


def g1_text():
    r = subprocess.run(["git", "show", "%s:%s" % (PIN, G1_PATH)], capture_output=True)
    if r.returncode != 0:
        print("ERROR: git show %s:%s rc=%d: %s" % (PIN, G1_PATH, r.returncode, r.stderr.decode("utf-8", "replace")[:200]))
        sys.exit(9)
    return r.stdout.decode("utf-8")


def load_g1():
    """(contracts_by_prefix, registry_list, text). Exits 9 unless exactly 78 unique contracts parse."""
    text = g1_text()
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
    contracts, registry = {}, []
    for b in blocks:
        d = json.loads(b)
        if isinstance(d, dict) and "contract_id" in d:
            if d["s3_prefix"] in contracts:
                print("ERROR: duplicate s3_prefix in G1: %s" % d["s3_prefix"])
                sys.exit(9)
            contracts[d["s3_prefix"]] = d
        elif isinstance(d, list):
            registry = d
    if len(contracts) != EXPECT_CONTRACTS:
        print("ERROR: G1 @%s parsed %d contracts, expected %d" % (PIN, len(contracts), EXPECT_CONTRACTS))
        sys.exit(9)
    return contracts, registry, text


def slug(prefix):
    """The emitter's harvest_slug rule (emit_catalog_v02.py): a gold table is its own directory name; else `/` and `-` -> `_`."""
    root = "amgt/harvest/gold/"
    p = str(prefix)
    if p.startswith(root) and p != root:
        return p[len(root):].strip("/").lower()
    return re.sub(r"[^a-z0-9]+", "_", p.strip("/").lower()).strip("_")


def legacy_key(prefix):
    return LEGACY_PREFIXES.get(prefix)


def expected_read_tool(contract, deployed):
    """The round-13 read_tool policy (PRD v0.11 item 3): the first G1-proposed typed tool that is DEPLOYED; else harvest_read if
    deployed; else None (no gateway tool reads the row yet). A tool that is not deployed is never named."""
    for p in contract.get("proposed_tools") or []:
        if p["name"] in deployed:
            return p["name"]
    if "harvest_read" in deployed:
        return "harvest_read"
    return None


BASE_PIN = "8c74d1d902"   # the round-12 catalog writer's drain commit: the 39 harvest rows MX-c-12 must preserve the routing text of
CATALOG_DIR = "workflows/atom_decomposition/catalog_entries"


def base_rows_dir():
    """The 39 harvest_*.yaml rows at BASE_PIN, materialised into a temp dir (git show, never the working copy). Cached."""
    import os
    import tempfile
    global _BASE
    if "_BASE" in globals() and _BASE:
        return _BASE
    ls = subprocess.run(["git", "ls-tree", "--name-only", BASE_PIN, CATALOG_DIR + "/"], capture_output=True)
    names = [n for n in ls.stdout.decode("utf-8").split() if os.path.basename(n).startswith("harvest_")]
    if ls.returncode != 0 or len(names) != 39:
        print("ERROR: %d harvest rows at %s (want 39)" % (len(names), BASE_PIN))
        sys.exit(9)
    d = tempfile.mkdtemp(prefix="c12base_")
    for n in names:
        r = subprocess.run(["git", "show", "%s:%s" % (BASE_PIN, n)], capture_output=True)
        with open(os.path.join(d, os.path.basename(n)), "wb") as f:
            f.write(r.stdout)
    _BASE = d
    return d
