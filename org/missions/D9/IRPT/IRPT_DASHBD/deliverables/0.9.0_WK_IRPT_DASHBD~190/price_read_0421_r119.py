"""IRPT_DASHBD round 119 (worker 0.9.0_WK_IRPT_DASHBD~190) -- DB-b-236, the 2026-04-21 price read.

READ-ONLY. For the 49 Financial account_return_daily partition of 2026-04-21: the accounts whose guard_state is
GRADED_DISAGREED are profiled against the holdings_performance_daily partition of the same day (the neighbour the
guard reads): accounts without a holdings row, the holdings status of each, excluded_count above zero or not, and
the excluded_weight bands. The security level is decided from the column list of the holdings partition: a
security-grain source would carry a security identifier, a price or a price-source column; if none is present the
level is ABSENT. A positive control runs the security selection function on a synthetic set.

Reads: GET only, two objects (data.parquet of each of the two partitions). Writes: one counts-only private file
under the worker's private evidence folder. Nothing else; no record is written here.

Usage: python -I <this file> <repo_root>
"""
import hashlib
import io
import json
import os
import sys
from pathlib import Path

FIRM_KEY = "49financial"
DAY = "2026-04-21"
TABLE_ACCT = "account_return_daily"
TABLE_HOLD = "holdings_performance_daily"
REGISTRY_REL = "data/firm_registry.json"
FG_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
FOLDER = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~190/"
ANALYSIS_REL = FOLDER + "price_read_0421_r119.py"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~190"
PRIVATE_NAME = "price_read_0421_r119_counts.json"
BANDS = ("zero", "le_1pct", "1_to_10pct", "gt_10pct")
GUARD_GD = "GRADED_DISAGREED"
SECURITY_HINTS = ("security", "cusip", "isin", "ticker", "symbol", "price")


class Stop(Exception):
    pass


class Reader(object):
    """GET only. There is deliberately no method that changes a remote object."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.gets = 0

    def get(self, bucket, key):
        self.gets += 1
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def locate(naming, table):
    addr = naming.address("irpt", FIRM_KEY, "gold", table, "date=%s" % DAY)
    rest = addr[len("s3://"):]
    bucket, _, key = rest.partition("/")
    return addr, bucket, key.rstrip("/") + "/data.parquet"


def read_cols(reader, naming, table, cols):
    """Returns (columns as lists, the partition's full column names, the address read)."""
    import pyarrow.parquet as pq
    addr, bucket, key = locate(naming, table)
    body = reader.get(bucket, key)
    names = pq.read_schema(io.BytesIO(body)).names
    t = pq.read_table(io.BytesIO(body), columns=cols).to_pydict()
    return t, names, addr


def band_of(w):
    if w is None or w == 0:
        return "zero"
    if w <= 0.01:
        return "le_1pct"
    if w <= 0.10:
        return "1_to_10pct"
    return "gt_10pct"


def profile(disagreed, holdings):
    """disagreed: set of account ids; holdings: dict account -> (status, excluded_count, excluded_weight)."""
    by_status = {}
    ex_zero = 0
    ex_pos = 0
    no_row = 0
    bands = dict((b, 0) for b in BANDS)
    for a in sorted(disagreed):
        h = holdings.get(a)
        if h is None:
            no_row += 1
            continue
        st = str(h[0])
        by_status[st] = by_status.get(st, 0) + 1
        if (h[1] or 0) > 0:
            ex_pos += 1
        else:
            ex_zero += 1
        bands[band_of(h[2])] += 1
    return {"accounts": len(disagreed), "no_holdings_row": no_row, "by_status": dict(sorted(by_status.items())),
            "excluded_count_zero": ex_zero, "excluded_count_positive": ex_pos, "excluded_weight_bands": bands}


def select_security(row):
    """One (account, security) pair -> 'flat', 'absent' or None (not selected)."""
    if row.get("excluded"):
        return None
    if row.get("position_moved") is not True:
        return None
    price = row.get("price_return")
    if price is None:
        return "absent"
    if price == 0:
        return "flat"
    return None


def positive_control():
    cases = [
        ("flat_price_moving_position", {"price_return": 0.0, "position_moved": True, "excluded": False}, "flat"),
        ("absent_price_moving_position", {"price_return": None, "position_moved": True, "excluded": False}, "absent"),
        ("moving_price", {"price_return": 0.012, "position_moved": True, "excluded": False}, None),
        ("excluded_flat_price", {"price_return": 0.0, "position_moved": True, "excluded": True}, None),
    ]
    observed = [(name, select_security(r)) for name, r, _e in cases]
    expected = [(name, e) for name, _r, e in cases]
    passed = observed == expected
    return {"passed": bool(passed),
            "description": "four synthetic (account, security) pairs through the selection function: a flat price with a "
                           "moving position, an absent price with a moving position, a moving price, and an excluded "
                           "security with a flat price",
            "expected": "; ".join("%s=%s" % (n, e) for n, e in expected),
            "observed": "; ".join("%s=%s" % (n, o) for n, o in observed)}


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    fg = json.loads(Path(repo, FG_REL).read_bytes().decode("utf-8"))
    d0 = fg["dates"][0]
    if d0["date"] != DAY:
        raise Stop("the flow-guard record's first date is not %s" % DAY)
    value_rows = d0["by_cause"]["VALUE"] + d0["by_cause"]["FLOW_AND_VALUE"]
    print("FLOW-GUARD RECORD %s: VALUE %d + FLOW_AND_VALUE %d = value_rows %d"
          % (DAY, d0["by_cause"]["VALUE"], d0["by_cause"]["FLOW_AND_VALUE"], value_rows))

    pc = positive_control()
    print("POSITIVE CONTROL: passed=%s" % pc["passed"])
    if not pc["passed"]:
        raise Stop("the positive control failed: %s" % pc["observed"])

    sys.path.insert(0, repo)
    from lib import opal_naming as naming
    with open(os.path.join(repo, REGISTRY_REL), "rb") as fh:
        registry = json.loads(fh.read().decode("utf-8"))
    firms = [f for f in registry.get("firms", []) if f.get("firm_id") == FIRM_KEY]
    if len(firms) != 1:
        raise Stop("the registry does not enumerate exactly one row for the firm")

    reader = Reader()
    ar, ar_names, ar_addr = read_cols(reader, naming, TABLE_ACCT, ["account_id", "guard_state"])
    hp, hp_names, hp_addr = read_cols(reader, naming, TABLE_HOLD,
                                      ["account_id", "status", "excluded_count", "excluded_weight"])

    guard_counts = {}
    disagreed = set()
    for a, g in zip(ar["account_id"], ar["guard_state"]):
        guard_counts[str(g)] = guard_counts.get(str(g), 0) + 1
        if g == GUARD_GD:
            disagreed.add(a)
    holdings = {}
    hp_dups = 0
    for a, s, c, w in zip(hp["account_id"], hp["status"], hp["excluded_count"], hp["excluded_weight"]):
        if a in holdings:
            hp_dups += 1
        holdings[a] = (s, c, w)
    if hp_dups:
        raise Stop("the holdings partition carries %d duplicate account rows; a BLOCKING row is owed" % hp_dups)

    prof = profile(disagreed, holdings)
    if sum(prof["excluded_weight_bands"].values()) != prof["accounts"] - prof["no_holdings_row"]:
        raise Stop("excluded-weight bands do not sum")
    if prof["excluded_count_zero"] + prof["excluded_count_positive"] != prof["accounts"] - prof["no_holdings_row"]:
        raise Stop("excluded counts do not sum")
    if sum(prof["by_status"].values()) != prof["accounts"] - prof["no_holdings_row"]:
        raise Stop("by_status does not sum")

    sec_hits = [c for c in hp_names if any(h in c.lower() for h in SECURITY_HINTS)]
    if sec_hits:
        raise Stop("the holdings partition carries security-grain columns (%d); the READ branch is not built this round"
                   % len(sec_hits))
    words = ("The neighbour the guard reads, the IRPT_BCKEND gold table %s, is account grain: its %s partition "
             "carries %d columns, none a security identifier, a price or a price-source column, and its producer's "
             "emitted column list is account grain (one row per account). The account_return_daily partition is "
             "account grain too. No security-grain price return or price source exists in the holdings gold for this "
             "firm and day, so the account-level profile stands as the answer."
             % (TABLE_HOLD, DAY, len(hp_names)))
    security = {"state": "ABSENT", "words": words, "claim": "absent"}

    os.makedirs(PRIVATE_DIR, exist_ok=True)
    private = {"scope": "counts only: partition row counts, guard-state counts, holdings column count, profile counts",
               "account_return_rows": len(ar["account_id"]), "guard_state_counts": dict(sorted(guard_counts.items())),
               "holdings_rows": len(hp["account_id"]), "holdings_columns": len(hp_names),
               "account_return_columns": len(ar_names), "profile": prof, "s3_reads": reader.gets}
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(private, indent=2, sort_keys=True) + "\n")

    out = {"date": DAY, "value_rows": value_rows, "account_profile": prof, "security_level": security,
           "positive_control": pc, "s3_reads": reader.gets,
           "analysis_sha256": sha256_of(os.path.abspath(__file__)), "analysis_file": ANALYSIS_REL}
    print("PROFILE JSON: " + json.dumps(out, sort_keys=True, indent=1))
    print("COUNTS: account_return_rows %d; guard_state_counts %s; holdings_rows %d; holdings_columns %d; s3_reads %d"
          % (len(ar["account_id"]), dict(sorted(guard_counts.items())), len(hp["account_id"]), len(hp_names),
             reader.gets))
    print("ADDRESSES: account_return partition and holdings partition resolved by lib opal_naming address()")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Stop as e:
        print("STOP: %s" % e)
        sys.exit(3)
