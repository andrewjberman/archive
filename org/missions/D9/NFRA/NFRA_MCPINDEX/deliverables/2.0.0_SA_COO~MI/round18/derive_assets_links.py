"""derive_assets_links.py [--write]: the ASSETS read links of round 18 -- which client_* tool reads which opal-data-assets / opal-data-bd catalog row.

Source of the READ set: the seven client adapters (app/client_adapter_*.py at the OG-ap-23 release), read by NFRA_OPLGTW's own
gr_grant_gen.py, which resolves every ctx.prefix(vendor, segment, layer, table) call (39 resolved) -- the set is NOT typed here; this script runs that
tool and parses the prefixes it prints. Source of the TOOL: RULES below, one per table name, each the adapter function that reads the table as its
main subject (a table several functions read takes the function that reads it for its own sake; the other readers are listed in NOTES).
A catalog row links when its prefix is a prefix the adapters read AND a rule names its table. Rows no adapter reads are listed as UNLINKED with
their gap_owner; nothing here decides whether a tool is owed (that is the CTO's call on the residual list).

Output: assets_read_links.json {links: {entity: tool}, notes, residual}. Without --write it prints the counts and exits 0 only when the self-checks hold.
"""
import glob
import json
import os
import re
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, *([".."] * 8)))
ROWS = os.path.join(ROOT, "workflows", "atom_decomposition", "catalog_entries")
GR = os.path.join(ROOT, "org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~ZS", "gr_grant_gen.py")
OUT = os.path.join(HERE, "assets_read_links.json")
BUCKETS = ("opal-data-assets", "opal-data-bd")
H, T, A, R = "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_resolve_account"

# table name -> the tool whose adapter function reads it as its main subject (vendor-qualified where the name is shared).
RULES = {
    ("blackdiamond", "49f", "dim_account_xref"): R, ("blackdiamond", "49f", "fact_bd_allocation"): A,
    ("blackdiamond", "cottonwood", "fact_holdings"): H, ("blackdiamond", "cottonwood", "fact_transactions"): T,
    ("blackdiamond", "cottonwood", "fact_allocations"): A, ("blackdiamond", "cottonwood", "fact_model_assignment"): A,
    ("blackdiamond", "cottonwood", "fact_model_blend"): A, ("blackdiamond", "cottonwood", "fact_model_definition"): A,
    ("blackdiamond", "cottonwood", "fact_model_roster"): A,
    ("commonwealth", "cottonwood", "positions"): H, ("commonwealth", "cottonwood", "account_day_value"): H,
    ("commonwealth", "cottonwood", "transactions"): T, ("commonwealth", "cottonwood", "crosswalk"): R,
    ("eclipse", "inflection", "fact_models"): A, ("eclipse", "inflection", "fact_model_composition"): A,
    ("orion", "inflection", "fact_positions"): H, ("orion", "inflection", "fact_transactions"): T,
    ("smartx", "platform", "fact_model_allocation_roster"): A, ("smartx", "platform", "fact_allocation_account_map"): R,
    ("smartx", "platform", "fact_allocation_positions"): H, ("smartx", "platform", "fact_allocation_valuation"): H,
    ("smartx", "platform", "fact_model_holdings"): A,
    # schwab: one segment per master (the segment is not typed); the three tables the adapter reads
    ("schwab", "*", "dim_position"): H, ("schwab", "*", "dim_balance"): H, ("schwab", "*", "dim_transaction"): T,
}
NOTES = {
    "client_get_holdings": "also read for holdings: schwab dim_position+dim_balance, bd cottonwood fact_allocations, commonwealth crosswalk, smartx roster+map",
    "client_get_allocation": "also read for allocation: schwab dim_balance+dim_position, orion fact_positions, smartx positions+map+roster",
    "client_get_fees": "reads fact_transactions (orion, bd cottonwood) only; no table is linked to it as its main subject",
}


def resolved_prefixes():
    r = subprocess.run([sys.executable, GR], capture_output=True, text=True, encoding="utf-8", timeout=120, cwd=ROOT)
    pre = re.findall(r"s3://opal-data-[a-z0-9-]+/(\S+)", r.stdout)
    n = re.search(r"ctx\.prefix calls resolved: (\d+)", r.stdout)
    return set(pre), (int(n.group(1)) if n else None)


ENT = "opal_data_assets_silver_"
# how a catalog entity name spells the (vendor, segment) of the adapters' prefix
TOKEN = {("blackdiamond", "49f"): "49f", ("blackdiamond", "cottonwood"): "cottonwood", ("commonwealth", "cottonwood"): "commonwealth_cottonwood",
         ("eclipse", "inflection"): "eclipse_inflection", ("orion", "inflection"): "orion_inflection", ("smartx", "platform"): "smartx"}


def entity_rules():
    """entity name -> (tool, the adapter prefix it must be in, or None for schwab: one segment per master)."""
    out = {}
    for (vendor, seg, table), tool in RULES.items():
        if vendor != "schwab":
            out[ENT + TOKEN[(vendor, seg)] + "_" + table] = (tool, "%s/%s/silver/%s/" % (vendor, seg, table))
    return out


def main():
    read, n_resolved = resolved_prefixes()
    rules = entity_rules()
    links, residual, unmatched_read = {}, [], set(read)
    for f in sorted(glob.glob(os.path.join(ROWS, "*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        if d.get("bucket") not in BUCKETS or d.get("retired"):
            continue
        ent = os.path.splitext(os.path.basename(f))[0]
        tool = None
        m = re.match(r"^%sschwab_(\d+)_(dim_position|dim_balance|dim_transaction)$" % ENT, ent)
        if m:
            tool = RULES[("schwab", "*", m.group(2))]
        elif ent in rules and rules[ent][1] in read:
            tool = rules[ent][0]
            unmatched_read.discard(rules[ent][1])
        if tool:
            links[ent] = tool
        else:
            residual.append({"entity": ent, "bucket": d.get("bucket"), "table": d.get("table"), "gap_owner": d.get("gap_owner"), "read_tool": d.get("read_tool")})
    read_no_row = sorted(p for p in unmatched_read if not p.startswith("schwab/"))
    by_tool = {}
    for t in links.values():
        by_tool[t] = by_tool.get(t, 0) + 1
    print("adapters' resolved prefixes: %d (gr_grant_gen says %s ctx.prefix calls); rows scanned in %s: linked %d, residual %d" %
          (len(read), n_resolved, " + ".join(BUCKETS), len(links), len(residual)))
    print("links by tool:", json.dumps(by_tool, sort_keys=True))
    print("prefixes the adapters read that no catalog row carries: %d %s" % (len(read_no_row), read_no_row[:8]))
    # 22 distinct non-schwab prefixes are printed; the 39 calls include the schwab per-master ones. Every one of the 22 must have matched a row.
    ok = bool(links) and n_resolved is not None and n_resolved >= 30 and len(read) >= 20 and not read_no_row
    if "--write" in sys.argv and ok:
        doc = {"_about": ("Round 18 ASSETS read links (2.0.0_SA_COO~MI): catalog entity -> the client_* tool whose adapter reads its table. Derived by "
                          "derive_assets_links.py from NFRA_OPLGTW's gr_grant_gen.py prefix set and the RULES table in that script; a link takes effect "
                          "only when its tool is in the deployed list (MX-c-31 mechanism)."),
               "links": dict(sorted(links.items())), "notes": NOTES, "residual": residual}
        open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print("wrote %s" % OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
