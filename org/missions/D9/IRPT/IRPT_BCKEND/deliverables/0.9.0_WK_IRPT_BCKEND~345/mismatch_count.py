#!/usr/bin/env python3
"""IB-pr-494 (IRPT_BCKEND round 170, worker 0.9.0_WK_IRPT_BCKEND~345): the READ-ONLY count of 49 Financial
accounts whose ACCOUNT node id differs from the directory's account id.

Runs the builder's own code path (holdings_49f.build_49f_actual and the holdings_snapshot helpers) and reads S3
with boto3 GET/HEAD/LIST calls only. Account keys and node ids live in memory only; the script prints and
records COUNTS only, and creates no scratch file. The Tax membership snapshot is fetched into memory with the
builder's own address resolution, and is never copied to local disk.
"""
import datetime as dt
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parents[7]
GOLD = REPO / "data" / "assets" / "scripts" / "gold" / "investor_reporting"
OUT = Path(__file__).resolve().parent / "IB170-3_node_id_mismatch_count.json"
AS_OF = dt.date.today().isoformat()
TAX_TABLE = "taxsma_workbook_projection"
TAX_OBJ = "taxsma_workbook_projected_snapshot.json"
STATES = ("served", "refused", "withheld")
CLASSES = ("equal", "differs_resolvable", "differs_unresolvable")

sys.path.insert(0, str(GOLD))

import boto3  # noqa: E402
import holdings_snapshot as hs  # noqa: E402
import holdings_49f as h49  # noqa: E402
from opal_naming import address  # noqa: E402


class Stop(Exception):
    pass


def tax_bytes(s3, firm):
    """The retained Tax membership snapshot, in memory, resolved as holdings_snapshot.retained_capture does."""
    override = os.environ.get("IRPT_49F_TAX_MEMBERSHIP_SNAPSHOT") or None
    if override:
        return Path(override).read_bytes()
    probe = urlparse(address("gateway", firm, "bronze", TAX_TABLE, "date=%s" % AS_OF))
    date = hs._latest_date_partition(s3, probe.netloc, probe.path.lstrip("/").rsplit("/", 1)[0] + "/", as_of=AS_OF)
    if date is None:
        return None
    found = urlparse(address("gateway", firm, "bronze", TAX_TABLE, "date=%s" % date, TAX_OBJ))
    got = s3.get_object(Bucket=found.netloc, Key=found.path.lstrip("/"))
    return got["Body"].read()


def tax_from_bytes(raw):
    """The same Traded=Yes membership rule as holdings_49f.tax_membership_from_snapshot, on in-memory bytes."""
    doc = json.loads(raw.decode("utf-8"))
    traded, rejected = set(), 0
    for row in doc.get("rows") or []:
        if row.get("row_kind") != "ACCOUNT_SLOT":
            continue
        if h49._text(row.get("Traded")).casefold() != "yes":
            continue
        account = h49.normalize_tax_account(row.get("Account Number"))
        if account is None:
            rejected += 1
            continue
        traded.add(account)
    return {"accounts": traded, "traded_row_count": len(traded) + rejected, "rejected_identity_rows": rejected,
            "provenance": {"contract": doc.get("contract")}}


def classify(firm, raw, nid, dir_ids):
    if dir_ids is None:
        return "differs_unresolvable"
    if nid in dir_ids:
        return "equal"
    if hs.opaque_id("account", firm, hs._pad10(raw)) in dir_ids:
        return "differs_resolvable"
    return "differs_unresolvable"


def run():
    s3 = boto3.client("s3")
    firm = h49._firm_id()
    raw_tax = tax_bytes(s3, firm)
    if raw_tax is None:
        raise Stop("tax membership snapshot not landed at or before the run date (the builder refuses)")
    tax = tax_from_bytes(raw_tax)
    raw_tax = None
    # the builder's own tax reader is replaced by the in-memory parse above; every other step is the builder's
    h49.tax_membership_from_snapshot = lambda _path: tax
    frames = h49.load_49f_sources(s3, AS_OF)
    custody = frames["custody_date"]
    raw_keys = [h49._text(v) for v in frames["balance"]["account_id"]]
    accounts = sorted(set(raw_keys))
    if not accounts:
        raise Stop("denominator is 0")
    nodes, out = h49.build_49f_actual(s3, AS_OF, tax_membership_path="in-memory")
    manifest = out["manifest"]
    if manifest["custody_date"] != custody:
        raise Stop("custody partition moved between the two reads")
    dir_ids = hs._directory_account_ids(s3, hs.firm_bucket_map().get(firm, ""), firm)

    acc_nodes = {n["node_id"] for n in nodes if n.get("node_kind") == "ACCOUNT"}
    refused_keys = {r["account"] for r in manifest["refused_accounts"]}
    withheld_ids = {w["account_id"] for w in manifest["drill_withheld"]}

    tally = {s: dict({"n": 0}, **{c: 0 for c in CLASSES}) for s in STATES}
    c = {"refused_balance_row_no_node": 0, "refused_membership_conflict_node_built": 0,
         "refused_membership_conflict_also_withheld": 0, "withheld_not_refused": 0,
         "unpartitioned": 0, "account_nodes_outside_balance": 0}
    nids = set()
    for raw in accounts:
        nid = hs.opaque_id("account", firm, raw)
        nids.add(nid)
        if raw in refused_keys:
            state = "refused"
            c["refused_balance_row_no_node"] += 1
        elif nid in refused_keys:
            state = "refused"
            c["refused_membership_conflict_node_built"] += 1
            if nid in withheld_ids:
                c["refused_membership_conflict_also_withheld"] += 1
        elif nid in withheld_ids:
            state = "withheld"
            c["withheld_not_refused"] += 1
        elif nid in acc_nodes:
            state = "served"
        else:
            c["unpartitioned"] += 1
            continue
        tally[state]["n"] += 1
        tally[state][classify(firm, raw, nid, dir_ids)] += 1
    c["account_nodes_outside_balance"] = len(acc_nodes - nids)
    if c["unpartitioned"]:
        raise Stop("%d balance account(s) fall outside the three states" % c["unpartitioned"])
    if sum(tally[s]["n"] for s in STATES) != len(accounts):
        raise Stop("the states do not sum to the denominator")

    not_established = [
        "as_of is the run date; the custody partition is the latest dim_balance date at or before it (recorded as as_of).",
        "States are partitioned by the builder's precedence, not by the TO's wording: refused first, then withheld, then served.",
        "refused holds %d balance row(s) that refused with no ACCOUNT node (node id computed for the count only) and "
        "%d membership-conflict account(s) whose ACCOUNT node IS built and whose conflict row is refused; %d of those "
        "are also drill-withheld and are counted under refused."
        % (c["refused_balance_row_no_node"], c["refused_membership_conflict_node_built"],
           c["refused_membership_conflict_also_withheld"]),
        "withheld holds %d account(s) whose ACCOUNT node is built and whose drill is withheld, not also refused; under the "
        "TO's own served definition these would overlap served, so they are counted only under withheld."
        % c["withheld_not_refused"],
        "served holds the accounts whose ACCOUNT node is built and that are neither refused nor withheld.",
        "%d ACCOUNT node(s) in the build fall outside the custody balance accounts (expected 0)."
        % c["account_nodes_outside_balance"],
        "custody balance rows: %d; distinct accounts: %d." % (len(raw_keys), len(accounts)),
        "the Tax membership snapshot was read into memory by the builder's own address resolution; no local copy was made.",
    ]
    if dir_ids is None:
        not_established.append("no directory has landed for this firm: directory_present is false, so no account is "
                               "classed equal and every account is differs_unresolvable.")

    record = {
        "as_of": custody,
        "directory_present": dir_ids is not None,
        "denominator": len(accounts),
        "states": tally,
        "not_established": not_established,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
        fh.write("\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Stop as exc:
        print("STOP: %s" % exc)
        sys.exit(2)
    except h49.FortyNineRefused as exc:
        print("STOP: builder refused: %s" % str(exc)[:160])
        sys.exit(2)
    except Exception as exc:  # noqa: BLE001 -- report the class and the S3 error code only, never a key
        resp = getattr(exc, "response", None)
        code = resp.get("Error", {}).get("Code") if isinstance(resp, dict) else None
        print("STOP: %s%s" % (type(exc).__name__, (" error_code=%s" % code) if code else ""))
        sys.exit(2)
