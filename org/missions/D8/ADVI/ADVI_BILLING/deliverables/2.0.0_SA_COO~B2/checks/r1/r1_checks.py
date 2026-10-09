"""ADVI_BILLING round-1 criterion checks (issuer 2.0.0_SA_COO~B2).

Usage: python r1_checks.py <worktree-root> <criterion-id>
Prints exactly one last line: "<id> PASS" or "<id> FAIL: <reason>". Exit 0 on PASS, 1 on FAIL.
Every check is bounded (one S3 object, one parquet partition, one test file) and terminates well inside 120 s.
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys

QUARTER = "2026Q3"
DEBIT_DATE = "2026-07-07"
WK1 = "org/missions/D8/ADVI/ADVI_BILLING/deliverables/0.9.0_WK_ADVI_BILLING~1"
WK2 = "org/missions/D8/ADVI/ADVI_BILLING/deliverables/0.9.0_WK_ADVI_BILLING~2"
CONTRACT = "org/standards/ADVI_BILLING_FEE_QUARTER_CONTRACT.json"
FIXTURE = "portal/src/pages/AdvisorIntelligence/_shared/__fixtures__/adviBillingFeeQuarter.json"
PANEL_TEST = "src/pages/AdvisorIntelligence/_shared/AdvisorBookFeePanel.test.tsx"
TRN_KEY = "schwab/08335338/silver/fact_trn/date=%s/data.parquet" % DEBIT_DATE
TRN_BUCKET = "opal-data-assets"

TOP_KEYS = {"contract_version", "firm", "relationship_id", "client_key", "quarter", "billing_convention", "billing_convention_claim",
            "period_start", "period_end", "valuation_date", "as_of", "accounts", "household", "steps"}
ACCOUNT_KEYS = {"account_id", "billable_value", "value_source", "schedule", "schedule_claim", "schedule_source",
                "flow_adjustment", "flows_in_period", "excluded_value", "exclusion_reason", "days_in_period",
                "days_in_year", "components"}
COMPONENT_KEYS = {"portion", "rate", "debit_code", "computed_fee", "debited_fee", "debit_date", "difference",
                  "reconcile_class", "difference_reason"}
HOUSEHOLD_KEYS = {"billable_value", "computed_fee", "debited_fee", "difference", "reconcile_class", "difference_reason"}
CLASSES = {"MATCH", "DIFFERS", "NO_DEBIT"}
CLAIMS = {"measured", "inferred", "held", "absent"}
CODE_FOR = {"ADVISOR": "TPFEE", "PLATFORM": "SMFEE"}


def _fail(cid: str, why: str) -> int:
    print("%s FAIL: %s" % (cid, why))
    return 1


def _ok(cid: str) -> int:
    print("%s PASS" % cid)
    return 0


def _load(root: str, rel: str):
    with open(os.path.join(root, rel), "r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_contract_shape(obj) -> str:
    """'' when obj conforms to the round-1 seam contract, else the first defect."""
    if not isinstance(obj, dict):
        return "not an object"
    miss = TOP_KEYS - set(obj)
    if miss:
        return "top-level keys missing: %s" % sorted(miss)
    if obj["billing_convention"] not in {"ADVANCE", "ARREARS", "UNRESOLVED"}:
        return "billing_convention off enum"
    if obj["billing_convention_claim"] not in CLAIMS:
        return "billing_convention_claim off enum"
    if not isinstance(obj["accounts"], list) or not obj["accounts"]:
        return "accounts empty"
    for a in obj["accounts"]:
        miss = ACCOUNT_KEYS - set(a)
        if miss:
            return "account keys missing: %s" % sorted(miss)
        if a["schedule_claim"] not in CLAIMS:
            return "schedule_claim off enum"
        comps = a["components"]
        if not isinstance(comps, list) or {c.get("portion") for c in comps} != {"ADVISOR", "PLATFORM"}:
            return "components must carry exactly ADVISOR and PLATFORM"
        for c in comps:
            miss = COMPONENT_KEYS - set(c)
            if miss:
                return "component keys missing: %s" % sorted(miss)
            if c["debit_code"] != CODE_FOR[c["portion"]]:
                return "debit_code does not match portion"
            err = _class_err(c)
            if err:
                return err
    miss = HOUSEHOLD_KEYS - set(obj["household"])
    if miss:
        return "household keys missing: %s" % sorted(miss)
    err = _class_err(obj["household"])
    if err:
        return "household " + err
    if not isinstance(obj["steps"], list) or len(obj["steps"]) < 3:
        return "steps carries fewer than 3 lines"
    return ""


def _class_err(row) -> str:
    cls = row.get("reconcile_class")
    if cls not in CLASSES:
        return "reconcile_class off enum: %r" % cls
    reason = row.get("difference_reason")
    if cls == "DIFFERS" and not (isinstance(reason, str) and reason.strip()):
        return "DIFFERS without difference_reason"
    if cls != "DIFFERS" and reason not in (None, ""):
        return "difference_reason set on %s" % cls
    return ""


def _builder_address(root: str, client_key: str) -> str:
    sys.path.insert(0, root)
    from lib.opal_naming import address  # noqa: E402 -- read at the worktree's own HEAD
    return address("advi", "49financial", "gold", "advi_billing", "quarter=%s" % QUARTER, "%s.json" % client_key)


def _s3_get(uri: str) -> bytes:
    import boto3
    m = re.match(r"s3://([^/]+)/(.+)$", uri)
    if not m:
        raise ValueError("not an s3 uri: %s" % uri)
    return boto3.client("s3").get_object(Bucket=m.group(1), Key=m.group(2))["Body"].read()


def _record(root: str):
    return _load(root, WK1 + "/AB_T1_RECORD.json")


def ac_1_1(root: str, cid: str) -> int:
    """AB-t-1 built behaviour: the object at the builder address conforms to the contract."""
    try:
        rec = _record(root)
        want = _builder_address(root, rec["client_key"])
        if rec.get("s3_key") != want:
            return _fail(cid, "record s3_key %r != builder address %r" % (rec.get("s3_key"), want))
        obj = json.loads(_s3_get(want).decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 -- any read failure is this criterion's FAIL
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    err = validate_contract_shape(obj)
    if err:
        return _fail(cid, err)
    if obj["quarter"] != QUARTER or obj["client_key"] != rec["client_key"] or obj["relationship_id"] != rec["relationship_id"]:
        return _fail(cid, "quarter/relationship mismatch")
    print("accounts=%d household_class=%s" % (len(obj["accounts"]), obj["household"]["reconcile_class"]))
    return _ok(cid)


def ac_1_2(root: str, cid: str) -> int:
    """AB-t-1 seam probe against the REAL neighbour: debited_fee per component equals Schwab 0833 fact_trn on the debit date."""
    try:
        import pyarrow.parquet as pq
        rec = _record(root)
        obj = json.loads(_s3_get(_builder_address(root, rec["client_key"])).decode("utf-8"))
        dates = sorted({c["debit_date"] for a in obj["accounts"] for c in a["components"] if c.get("debit_date")})
        if not dates or len(dates) > 2 or not all(d.startswith("2026-07-") for d in dates):
            return _fail(cid, "debit dates must be 1-2 July 2026 dates (TPFEE 07-07, SMFEE 07-21); got %s" % dates)
        tbls = {}
        for d in dates:
            t = pq.read_table(io.BytesIO(_s3_get("s3://%s/%s" % (TRN_BUCKET, TRN_KEY.replace(DEBIT_DATE, d)))),
                              columns=["account_id", "tran_srcde", "gross_amount"]).to_pandas()
            t["acct"] = t["account_id"].astype(str).str.zfill(10)
            tbls[d] = t
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    checked = 0
    for a in obj["accounts"]:
        acct = str(a["account_id"]).zfill(10)
        for c in a["components"]:
            if not c.get("debit_date"):
                if c["reconcile_class"] != "NO_DEBIT":
                    return _fail(cid, "component without debit_date must be NO_DEBIT")
                continue
            tbl = tbls[c["debit_date"]]
            rows = tbl[(tbl["acct"] == acct) & (tbl["tran_srcde"] == c["debit_code"])]
            actual = round(abs(float(rows["gross_amount"].sum())), 2) if len(rows) else None
            got = c["debited_fee"]
            if actual is None:
                if c["reconcile_class"] != "NO_DEBIT":
                    return _fail(cid, "no %s row for ...%s but class %s" % (c["debit_code"], acct[-4:], c["reconcile_class"]))
            elif got is None or abs(round(abs(float(got)), 2) - actual) > 0.005:
                return _fail(cid, "debited_fee for ...%s %s disagrees with fact_trn" % (acct[-4:], c["debit_code"]))
            checked += 1
    print("components checked against fact_trn %s: %d" % (DEBIT_DATE, checked))
    return _ok(cid) if checked else _fail(cid, "0 components checked")


def ac_1_3(root: str, cid: str) -> int:
    """AB-t-1: the contract file carries the decomposition's field set, and the valuation-date test is recorded."""
    try:
        con = _load(root, CONTRACT)
        rec = _record(root)
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    blob = json.dumps(con)
    absent = sorted(k for k in TOP_KEYS | ACCOUNT_KEYS | COMPONENT_KEYS if '"%s"' % k not in blob)
    if absent:
        return _fail(cid, "contract omits fields: %s" % absent)
    if con.get("contract_version") != "0.1.0" and con.get("version") != "0.1.0":
        return _fail(cid, "contract version is not 0.1.0")
    cands = rec.get("valuation_date_candidates")
    if not isinstance(cands, list) or len(cands) < 2 or not rec.get("valuation_date_chosen"):
        return _fail(cid, "valuation_date_candidates (>=2) and valuation_date_chosen not recorded")
    return _ok(cid)


def ac_2_1(root: str, cid: str) -> int:
    """AB-t-2 built behaviour + seam: the local-invoke tests (real object bytes; out-of-scope refused) pass."""
    tests = os.path.join(root, "infra/aws/lambda/advi/billing-read/tests")
    if not os.path.isdir(tests):
        return _fail(cid, "no tests dir")
    proc = subprocess.run([sys.executable, "-m", "pytest", tests, "-q", "-rA", "--no-header", "-p", "no:cacheprovider"],
                          cwd=root, capture_output=True, text=True, timeout=110)
    out = proc.stdout + proc.stderr
    passed = re.findall(r"^PASSED \S+::(\S+)", out, re.M)
    if proc.returncode != 0:
        return _fail(cid, "pytest rc=%d" % proc.returncode)
    if not any("real_object" in t for t in passed) or not any("refused" in t for t in passed):
        return _fail(cid, "need a passing test named *real_object* and one named *refused*; passed=%s" % passed)
    print("passed: %s" % ", ".join(passed))
    return _ok(cid)


def ac_2_2(root: str, cid: str) -> int:
    """AB-t-2: the saved plan adds only, and names the builder's function and role."""
    try:
        with open(os.path.join(root, WK1, "AB_T2_PLAN.txt"), "r", encoding="utf-8", errors="replace") as fh:
            plan = fh.read()
    except OSError as exc:
        return _fail(cid, "no plan record: %s" % exc)
    m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", plan)
    if not m:
        return _fail(cid, "no Plan: line")
    if m.group(2) != "0" or m.group(3) != "0":
        return _fail(cid, "plan changes or destroys: %s" % m.group(0))
    for nm in ("advi-49f-billing-read-lambda", "advi-49f-billing-read-role"):
        if nm not in plan:
            return _fail(cid, "plan does not name %s" % nm)
    print(m.group(0))
    return _ok(cid)


def ac_3_1(root: str, cid: str) -> int:
    """AB-t-3 built behaviour: the panel's bun test (server render of the contract fixture) passes."""
    bun = shutil.which("bun")
    if not bun:
        return _fail(cid, "bun not on PATH")
    portal = os.path.join(root, "portal")
    if not os.path.isfile(os.path.join(portal, PANEL_TEST)):
        return _fail(cid, "no panel test file")
    proc = subprocess.run([bun, "test", PANEL_TEST], cwd=portal, capture_output=True, text=True, timeout=110)
    out = proc.stdout + proc.stderr
    m = re.search(r"(\d+) pass", out)
    if proc.returncode != 0 or not m or int(m.group(1)) < 1:
        return _fail(cid, "bun test rc=%d" % proc.returncode)
    print(m.group(0))
    return _ok(cid)


def ac_3_2(root: str, cid: str) -> int:
    """AB-t-3: the fixture the panel renders conforms to the seam contract."""
    try:
        obj = _load(root, FIXTURE)
    except Exception as exc:  # noqa: BLE001
        return _fail(cid, "%s: %s" % (type(exc).__name__, exc))
    err = validate_contract_shape(obj)
    return _fail(cid, err) if err else _ok(cid)


CHECKS = {
    "AB1-1-AC1": ac_1_1, "AB1-1-AC2": ac_1_2, "AB1-1-AC3": ac_1_3,
    "AB1-2-AC1": ac_2_1, "AB1-2-AC2": ac_2_2,
    "AB1-3-AC1": ac_3_1, "AB1-3-AC2": ac_3_2,
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: r1_checks.py <root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    sys.exit(CHECKS[sys.argv[2]](os.path.abspath(sys.argv[1]), sys.argv[2]))
