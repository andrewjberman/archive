"""ADVI_BILLING round-2 criterion checks (issuer 2.0.0_SA_COO~B2).

Usage: python r2_checks.py <worktree-root> <criterion-id>
Prints one last line "<id> PASS" or "<id> FAIL: <reason>". Exit 0 on PASS, 1 on FAIL. Every check is bounded
(one test file, one S3 object, one served summary) and finishes inside 120 s.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import re
import subprocess
import sys

D = "org/missions/D8/ADVI/ADVI_BILLING/deliverables"
WK3, WK4 = D + "/0.9.0_WK_ADVI_BILLING~3", D + "/0.9.0_WK_ADVI_BILLING~4"
R1 = D + "/2.0.0_SA_COO~B2/checks/r1/r1_checks.py"
CROSSWALK_COLS = {"schwab_account_number", "bd_account_id", "bd_relationship_id", "opal_relationship_id", "match_method", "claim"}
SMARTX_COLS = ["AllocationID", "Brokerage Account Number", "Sleeve Type", "Fee Period Start", "Fee Period End",
               "Advisor Fee Rate", "Client Fee Rate", "UMA Fee Rate", "Model Fee Rate", "Current Period Estimate Valuation",
               "Days in Period", "Days in Year", "Net SmartX Fee", "Net Advisor Fee", "Fee Debit"]
THREAD_KEY = "z08219260"


def _fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    return 1


def _ok(cid):
    print("%s PASS" % cid)
    return 0


def _load(root, rel):
    with open(os.path.join(root, rel), "r", encoding="utf-8") as fh:
        return json.load(fh)


def _pytest(root, cid, rel, need=()):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return _fail(cid, "no test file %s" % rel)
    env = dict(os.environ, PY_COLORS="0", NO_COLOR="1", FORCE_COLOR="0")
    proc = subprocess.run([sys.executable, "-m", "pytest", path, "-q", "-rA", "--color=no", "-p", "no:cacheprovider"],
                          cwd=root, capture_output=True, text=True, timeout=110, env=env)
    passed = re.findall(r"^PASSED \S+::(\S+)", proc.stdout + proc.stderr, re.M)
    if proc.returncode != 0 or not passed:
        return _fail(cid, "pytest rc=%d passed=%d" % (proc.returncode, len(passed)))
    for token in need:
        if not any(token in t for t in passed):
            return _fail(cid, "no passing test named *%s*" % token)
    print("passed %d: %s" % (len(passed), ", ".join(passed)))
    return _ok(cid)


def _s3_get(uri):
    import boto3
    m = re.match(r"s3://([^/]+)/(.+)$", uri)
    return boto3.client("s3").get_object(Bucket=m.group(1), Key=m.group(2))["Body"].read()


def _address(root, *args):
    sys.path.insert(0, root)
    from lib.opal_naming import address  # noqa: E402 -- the worktree's own builder
    return address(*args)


def _r1_validator(root):
    spec = importlib.util.spec_from_file_location("r1c", os.path.join(root, R1))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validate_contract_shape


def ac_2_1(root, cid):
    return _pytest(root, cid, "data/assets/scripts/gold/runners_49f/tests/test_d08_ownership_gap.py", ("missing",))


def ac_2_2(root, cid):
    try:
        rec = _load(root, WK4 + "/OWNERSHIP_GAP_R2.json")
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    miss, added = rec.get("missing_before") or [], rec.get("present_after_fix") or []
    if len(miss) != 5 or set(miss) - set(added):
        return _fail(cid, "missing_before must list 5 advisorKeys, all present_after_fix (got %d / %d)" % (len(miss), len(added)))
    if rec.get("other_advisors_changed") != 0:
        return _fail(cid, "other_advisors_changed must be 0, got %r" % rec.get("other_advisors_changed"))
    if rec.get("written") is not False:
        return _fail(cid, "the cell must not write the served map (written must be false)")
    return _ok(cid)


def ac_3_1(root, cid):
    return _pytest(root, cid, "infra/aws/ec2/opal-gateway/tests/test_advi_site_to_s3.py", ("refuses", "builder_address"))


def ac_4_1(root, cid):
    return _pytest(root, cid, "data/assets/scripts/silver/advi_billing/tests/test_smartx_fee_statement.py", ("parses",))


def ac_4_2(root, cid):
    try:
        con = _load(root, "org/standards/ADVI_BILLING_SMARTX_FEE_STATEMENT_CONTRACT.json")
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    src = con.get("source_columns")
    if not isinstance(src, list):
        return _fail(cid, "contract lacks a source_columns list")
    names = {str(c.get("name") if isinstance(c, dict) else c) for c in src}
    absent = [c for c in SMARTX_COLS if c not in names]
    if absent:
        return _fail(cid, "source_columns omits %s" % absent)
    want = _address(root, "advi", "49financial", "silver", "smartx_fee_statement", "quarter=2026Q3", "data.parquet")
    if want not in json.dumps(con):
        return _fail(cid, "contract does not carry the builder address %s" % want)
    return _ok(cid)


def _crosswalk(root):
    rec = _load(root, WK3 + "/AB_E5_RECORD.json")
    want = _address(root, "advi", "49financial", "gold", "household_crosswalk", "date=%s" % rec["date"],
                    "household_crosswalk.parquet")
    if rec.get("s3_key") != want:
        raise ValueError("record s3_key %r != builder address %r" % (rec.get("s3_key"), want))
    import pyarrow.parquet as pq
    return rec, pq.read_table(io.BytesIO(_s3_get(want))).to_pandas()


def ac_5_1(root, cid):
    try:
        rec, df = _crosswalk(root)
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    miss = CROSSWALK_COLS - set(df.columns)
    if miss:
        return _fail(cid, "crosswalk lacks columns %s" % sorted(miss))
    cov = rec.get("coverage") or {}
    for k in ("schwab_accounts_total", "schwab_accounts_mapped", "client_keys_total", "client_keys_mapped", "allocations_partition"):
        if k not in cov:
            return _fail(cid, "record coverage lacks %s" % k)
    print("rows=%d mapped %s/%s accounts, %s/%s client keys" % (len(df), cov["schwab_accounts_mapped"], cov["schwab_accounts_total"],
                                                                cov["client_keys_mapped"], cov["client_keys_total"]))
    return _ok(cid)


def ac_5_2(root, cid):
    """Seam probe against the REAL neighbour: the thread household's BD accounts equal the served summary's accounts."""
    try:
        _, df = _crosswalk(root)
        summ = json.loads(_s3_get("s3://opal-data-bd/platinum/clients/%s/summary.json" % THREAD_KEY))
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    served = {str(a["account_id"]) for a in summ["detail"].get("accounts", [])}
    got = set(df[df["bd_relationship_id"].astype(str) == THREAD_KEY]["bd_account_id"].astype(str))
    if not served or got != served:
        return _fail(cid, "crosswalk accounts for the thread household (%d) != served summary accounts (%d)" % (len(got), len(served)))
    return _ok(cid)


def ac_6_1(root, cid):
    return _pytest(root, cid, "data/assets/scripts/gold/advi_billing/tests/test_fee_quarter_v2.py", ("crosswalk", "smartx"))


def ac_6_2(root, cid):
    try:
        obj = _load(root, ".scratch/advi_billing/AB_E6_DRYRUN.json")
        validate = _r1_validator(root)
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    err = validate(obj)
    if err:
        return _fail(cid, err)
    if obj.get("client_key") != THREAD_KEY or obj.get("household_source") != "household_crosswalk":
        return _fail(cid, "dry run must be for %s with household_source household_crosswalk" % THREAD_KEY)
    return _ok(cid)


def ac_1_1(root, cid):
    """AB-e-1: five probes recorded with a status and a class each; the ledger named in the record is closed."""
    try:
        rec = _load(root, D + "/0.7.0_AE_CloudOps~AB2/AB_E1_PROBES.json")
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    probes = rec.get("probes") or []
    want = {"in_book", "out_of_book", "firm_admin", "other_firm", "execute_api_bypass"}
    got = {p.get("class") for p in probes}
    if got != want or len(probes) != 5:
        return _fail(cid, "probes must be exactly the five classes %s; got %s" % (sorted(want), sorted(str(g) for g in got)))
    for p in probes:
        if not isinstance(p.get("status"), int) or p.get("method") != "GET" or not p.get("route"):
            return _fail(cid, "probe %s lacks an integer status, method GET or route" % p.get("class"))
        if re.search(r"eyJ[A-Za-z0-9_-]{10,}", json.dumps(p)):
            return _fail(cid, "probe %s carries token bytes" % p.get("class"))
    slug = rec.get("ledger_slug") or ""
    if not slug or os.path.exists(os.path.join(root, "org/critical_paths/.open_deploys/%s.json" % slug)):
        return _fail(cid, "ledger %r missing or still open" % slug)
    print("; ".join("%s=%s" % (p["class"], p["status"]) for p in probes))
    return _ok(cid)


CHECKS = {"AB2-1-AC1": ac_1_1, "AB2-2-AC1": ac_2_1, "AB2-2-AC2": ac_2_2, "AB2-3-AC1": ac_3_1, "AB2-4-AC1": ac_4_1, "AB2-4-AC2": ac_4_2,
          "AB2-5-AC1": ac_5_1, "AB2-5-AC2": ac_5_2, "AB2-6-AC1": ac_6_1, "AB2-6-AC2": ac_6_2}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: r2_checks.py <root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    sys.exit(CHECKS[sys.argv[2]](os.path.abspath(sys.argv[1]), sys.argv[2]))
