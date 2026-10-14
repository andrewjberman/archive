"""glib.py -- the round-14 checks' ONE reader of the CRO's G2, G5 and G6 data-contract files, each at a PINNED commit, and the
rules that turn a contract into a silver_datasets table row. Read with `git show <pin>:<path>`, never the working copy: the CRO may
amend a file after the cut, and a check graded against a moving file grades a different object each run.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

DIR = "org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/GATEWAY_DATA_CONTRACTS_20261014/"
PINS = {"G2": ("339a2804d7", DIR + "G2_assets_silver.md", 131),
        "G5": ("35f45893a7", DIR + "G5_etfs.md", 36),
        "G6": ("35f45893a7", DIR + "G6_news.md", 12),
        "G4": ("7ec87a87e5", DIR + "G4_mdpf_delta.md", 7)}
BASE_PIN = "8c74d1d902"   # the round-12 drain commit: the existing silver/portal source rows the generator must not disturb
CATALOG_DIR = "workflows/atom_decomposition/catalog_entries"
EXPECT_ROWS = 174         # 131 + 36 + 12 + 7 = 186 contracts, less the 12 that an existing silver_datasets row already catalogues (see in_scope)
# PRD v0.13: the two G4 feeds marked do-not-serve (a row flagged retired: never a tool target), with G4 routing as the reason.
DO_NOT_SERVE = ("opal-data-mdpf/feeds/partner_held_etf_49financial", "opal-data-mdpf/feeds/non_model_aua")
# PRD v0.14 (Andrew-direct ~15:0xZ, client data ONLY from the opal-data-assets vendor silver folders): the account-grain MDPF feeds are
# NOT_SERVED, a retired row whose reason cites the record.
NOT_SERVED = ("opal-data-mdpf/feeds/model_aua_positions_49financial", "opal-data-mdpf/feeds/model_aua_positions_inflection")
NOT_SERVED_RECORD = "ANDREW_DIRECT_20261014_150xZ_CLIENT_DATA_ONLY_OPAL_DATA_ASSETS_VENDOR_SILVER.md @9a314c1e98"


def enc(contract_id):
    """The row's contract.id: the contract_id with every `/` replaced by `:`. An IDENTIFIER, not an S3 address: the commit-time
    naming gate grades any slash-bearing string as an S3 key and refuses it as out-of-pattern."""
    return str(contract_id).replace("/", ":")


def retired_reason(c):
    """The reason a row is retired (never a tool target), or None."""
    cid = c["contract_id"]
    if cid in DO_NOT_SERVE:
        return "do-not-serve: " + str(c.get("routing") or "")
    if cid in NOT_SERVED:
        return "not_served: %s -- client data only from the opal-data-assets vendor silver folders" % NOT_SERVED_RECORD
    return None

# The issuer's vendor-tool -> client_* map (OPLGTW PRD v3.1 ruling 1). A name that is not a key passes through unchanged.
# A G2 tool with no client_* tool (balances, find_holders, flows, documents, delivery, eclipse, prices, workbook rows, platform
# lists) is NOT mapped: its tables are catalogued with read_tool null ("a table no question reaches is catalogued but gets no
# adapter this round").
CLIENT_MAP = {
    "schwab_resolve_account": "client_resolve_account", "blackdiamond_resolve_account": "client_resolve_account",
    "commonwealth_resolve_account": "client_resolve_account",
    "blackdiamond_get_holdings": "client_get_holdings", "schwab_get_positions": "client_get_holdings",
    "orion_get_holdings": "client_get_holdings",
    "blackdiamond_list_transactions": "client_get_transactions", "schwab_list_transactions": "client_get_transactions",
    "orion_list_transactions": "client_get_transactions", "commonwealth_list_transactions": "client_get_transactions",
    "blackdiamond_get_model_assignment": "client_get_allocation", "blackdiamond_get_model_targets": "client_get_allocation",
    "orion_get_allocation": "client_get_allocation", "smartx_allocation_by_account": "client_get_allocation",
    "smartx_model_assignments": "client_get_allocation", "smartx_model_detail": "client_get_allocation",
    "blackdiamond_get_unrealized_lots": "client_get_lots", "blackdiamond_list_realized": "client_get_lots",
    "schwab_get_realized_lots": "client_get_lots", "schwab_get_tax_lot_detail": "client_get_lots",
    "schwab_get_unrealized_lots": "client_get_lots",
    "orion_get_household_performance": "client_get_performance", "orion_get_account_performance": "client_get_performance",
    "commonwealth_get_performance": "client_get_performance",
    "blackdiamond_get_account_fee_roles": "client_get_fees", "blackdiamond_list_fees": "client_get_fees",
    "blackdiamond_get_account_profile": "client_get_profile", "smartx_account_lookup": "client_get_profile",
    "blackdiamond_list_insurance": "client_get_insurance",
}


def git_show(pin, path):
    r = subprocess.run(["git", "show", "%s:%s" % (pin, path)], capture_output=True)
    if r.returncode != 0:
        print("ERROR: git show %s:%s rc=%d" % (pin, path, r.returncode))
        sys.exit(9)
    return r.stdout.decode("utf-8")


def group_text(g):
    pin, path, _n = PINS[g]
    return git_show(pin, path)


def parse(text):
    out = []
    for b in re.findall(r"```json\n(.*?)\n```", text, re.S):
        d = json.loads(b)
        if isinstance(d, dict) and "contract_id" in d:
            out.append(d)
    return out


def load_all():
    """{contract_id: (group, contract)} over G2, G5, G6; exits 9 unless each group parses to its pinned count."""
    allc = {}
    for g, (_pin, _path, n) in PINS.items():
        cs = parse(group_text(g))
        if len(cs) != n:
            print("ERROR: %s parsed %d contracts, expected %d" % (g, len(cs), n))
            sys.exit(9)
        for c in cs:
            if c["contract_id"] in allc:
                print("ERROR: duplicate contract_id %s" % c["contract_id"])
                sys.exit(9)
            allc[c["contract_id"]] = (g, c)
    return allc


def in_scope(c):
    """The generator rows a contract unless an existing silver_datasets row already catalogues the same table (catalog_entry.
    data_catalog_key `silver_datasets.<entity>`: the 12 Schwab dim contracts). A contract that points at a channel text (the `news`
    row) is NOT catalogued at table grain, so it is in scope: the channel keeps its text, the table gets its row."""
    key = str((c.get("catalog_entry") or {}).get("data_catalog_key") or "")
    return not (bool((c.get("catalog_entry") or {}).get("present")) and key.startswith("silver_datasets."))


def entity(cid):
    return re.sub(r"[^a-z0-9]+", "_", cid.lower()).strip("_")


def candidates(c):
    out = []
    for p in c.get("proposed_tools") or []:
        n = str(p["name"]).split(" ")[0]
        if n.lower().startswith("none") or not n:
            continue
        out.append(CLIENT_MAP.get(n, n))
    return out


def expected_read_tool(c, deployed):
    for t in candidates(c):
        if t in deployed:
            return t
    return None


def behind(c):
    """Trading days behind T-1, from whichever key the contract's freshness carries; None when it states none."""
    f = c.get("freshness") or {}
    for k in ("trading_days_behind_t1", "trading_days_behind", "trading_days_behind_T-1"):
        if isinstance(f.get(k), (int, float)) and not isinstance(f.get(k), bool):
            return f[k]
    return None


def marks(c):
    """The (staleness, emptiness) words a row's business_meaning must carry (PRD v0.12 item 4: frozen or empty is never current):
    ('NOT CURRENT: <n> trading days behind', 'EMPTY: no objects') or None for each that does not apply."""
    n = behind(c)
    stale = "NOT CURRENT: %s trading days behind" % (int(n) if float(n) == int(n) else n) if n is not None and n > 5 else None
    empty = "EMPTY: no objects" if (c.get("size") or {}).get("objects") == 0 else None
    return stale, empty


def firm_rule(c):
    f = (c.get("fork_keys") or {}).get("firm") or {}
    vals = [v for v in (f.get("values") or []) if str(v) not in ("global", "opal-internal")]
    return "firm-scoped" if vals else "opal-internal-only"


def base_rows_dir():
    """The existing non-harvest catalog source rows at BASE_PIN, materialised into a temp dir (git show). Cached."""
    global _BASE
    if "_BASE" in globals() and _BASE:
        return _BASE
    ls = subprocess.run(["git", "ls-tree", "--name-only", BASE_PIN, CATALOG_DIR + "/"], capture_output=True)
    names = [n for n in ls.stdout.decode("utf-8").split() if n.endswith(".yaml")]
    d = tempfile.mkdtemp(prefix="c14base_")
    for n in names:
        r = subprocess.run(["git", "show", "%s:%s" % (BASE_PIN, n)], capture_output=True)
        with open(os.path.join(d, os.path.basename(n)), "wb") as f:
            f.write(r.stdout)
    _BASE = d
    return d
