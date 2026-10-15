"""IRPT_DASHBD round 118 (issuer 2.0.0_SA_COO~D2) -- DB-b-230, hop 1 of the filled-report serve path: the gold table `filled_report_values`
(CTO analysis @5934ffcedc ruling 2; IB-pr-551 CTO half @82183fcfaf).

  DB-b-230 (~185) a gold script writes one row per household x member x row x series point (value, or the absent kind and its words) at the firm's
                  gold address, LOCAL to a private folder for one QA run of 49 Financial on one date; the contract gains the table (0.5.2).
                                                                                                         DB118-1-AC1 (the table), AC2 (the contract), AC3 (the tests)

The checker grades FORM and CONSISTENCY from the private QA parquet and RECOMPUTES one number from the real neighbour: for two households (the two
lowest sha256 of household_ref) the household ending value equals the sum of market_value_eod over its accounts in the 49 Financial
account_return_daily partition of as_of (read-only S3 GET), whenever that member is not absent.

COLUMNS (the table's schema, in order; every column a string except value_number, a double):
  firm, household_ref, as_of, member_id, row_key, series_name, point_date, value_number, value_text, absent_kind, absent_reason,
  contract_version, schema_version
A row holds EXACTLY ONE of: value_number (not null; value_text, absent_kind, absent_reason null), value_text (not null; the others null),
or the absent form (absent_kind in the contract's absent_kinds and absent_reason words; value_number and value_text null). row_key, series_name and
point_date are empty strings where they do not apply. Reserved member ids (value_text rows): household.first_data_date, account.last4,
account.first_data_date, account.window_status.<qtd|ytd|last_12_months|since_inception>.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the clauses on synthetic arms
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~185/RD_FILLED_REPORT_VALUES_R118.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/filled_report_values.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_filled_report_values.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
PRIVATE_ROOT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~185/"
COLUMNS = ["firm", "household_ref", "as_of", "member_id", "row_key", "series_name", "point_date", "value_number", "value_text",
           "absent_kind", "absent_reason", "contract_version", "schema_version"]
KEY = ("household_ref", "member_id", "row_key", "series_name", "point_date")
RESERVED = ("household.first_data_date", "account.last4", "account.first_data_date", "account.window_status.qtd",
            "account.window_status.ytd", "account.window_status.last_12_months", "account.window_status.since_inception")
ABSENT_KINDS = ("NO_SOURCE_YET", "INSUFFICIENT_HISTORY", "SOURCE_BREAK")
FIRM = "49financial"
BASE_VERSION, BASE_SHA = "0.5.1", "0b515243b310bb95de8d9bebdb0f2725b70626307adcc9f4fb80298883692df4"
MEMBER_IDS_SHA = "dce57d0221f5b51ed59edfbe09b53de674f42570347177f606dddce9c76d4eda"
DOCUMENT_SHA = "87af1ec8eed20296a46338fa254fb83ebc2117adcc97b66eac179f36b5912dd7"
ABSENT_SOURCED_SHA = "3ab9045846002afbd19d869e9811f96b91febac202a2874f7ba5078894f4a582"
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("cottonwood", "inflection", "orion/", "eclipse/", "opal-data-cottonwood", "opal-data-inflection")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")
MIN_TESTS = 14
# Amendment 1 of DB-b-232 (2026-10-15): the repairs of rows W185-S7 and W185-S8 are graded here, on the module they repair
REQUIRED_TESTS = ("test_households_come_from_the_adapter", "test_missing_sibling_table_is_no_source_yet",
                  "test_empty_lot_source_is_absent_not_zero")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load_json(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def is_tracked(root, rel):
    return subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel], capture_output=True, text=True).returncode == 0


# ------------------------------------------------------------------------------------------------ the table clauses (pure, over a list of row dicts)
def check_rows(rows, member_ids, absent_sourced, as_of, firm=FIRM):
    """rows: list of dicts keyed by COLUMNS. Raises Fail on the first violated clause."""
    need(len(rows) > 0, "the table is empty")
    seen = set()
    by_h = {}
    for r in rows:
        need(set(r) == set(COLUMNS), "a row has the wrong columns: %s" % sorted(set(r) ^ set(COLUMNS)))
        for c in ("firm", "household_ref", "as_of", "member_id", "row_key", "series_name", "point_date", "contract_version", "schema_version"):
            need(isinstance(r[c], str), "column %s is not a string" % c)
        need(r["firm"] == firm and r["as_of"] == as_of, "firm or as_of differs from the record")
        need(nes(r["household_ref"]) and nes(r["member_id"]) and nes(r["contract_version"]) and nes(r["schema_version"]), "an empty key column")
        k = tuple(r[c] for c in KEY)
        need(k not in seen, "a duplicate key: member %s" % r["member_id"])
        seen.add(k)
        vn, vt, ak, ar = r["value_number"], r["value_text"], r["absent_kind"], r["absent_reason"]
        forms = [vn is not None, vt is not None, ak is not None]
        need(sum(forms) == 1, "a row does not hold exactly one of a number, a text or the absent form (member %s)" % r["member_id"])
        if vn is not None:
            need(isinstance(vn, float) and vn == vn and abs(vn) < 1e15, "value_number is not a finite float")
            need(ar is None, "a measured row carries an absent reason")
        elif vt is not None:
            need(nes(vt) and ar is None, "a text row is empty or carries an absent reason")
            if vt == "UNHELD":
                need(r["member_id"].startswith("hold.allocation"), "UNHELD outside hold.allocation (member %s)" % r["member_id"])
        else:
            need(ak in ABSENT_KINDS and nes(ar), "the absent form needs a kind in the three and words (member %s)" % r["member_id"])
        by_h.setdefault(r["household_ref"], []).append(r)
    ids = set(member_ids)
    for h, rs in by_h.items():
        got = {r["member_id"] for r in rs}
        need(got - set(RESERVED) == ids, "a household does not carry exactly the contract's members (missing %d, extra %d)" %
             (len(ids - got), len(got - set(RESERVED) - ids)))
        need(set(RESERVED) <= got, "a household lacks a reserved document row")
        for r in rs:
            if r["member_id"] in absent_sourced:
                need(r["absent_kind"] == "NO_SOURCE_YET", "an ABSENT-sourced member does not carry NO_SOURCE_YET")
        accts = {r["row_key"] for r in rs if r["member_id"] == "account.last4"}
        need(len(accts) >= 1 and "" not in accts, "a household has no account rows")
        for r in rs:
            if r["member_id"].startswith("account."):
                need(r["row_key"] in accts, "a reserved account row names an account the household lacks")
    return len(by_h)


# ------------------------------------------------------------------------------------------------ the seam probe (read-only GET of the neighbour)
def ending_value_probe(root, rows, as_of, member_id):
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=%s" % as_of)
    bucket, key = addr[len("s3://"):].split("/", 1)
    body = boto3.client("s3").get_object(Bucket=bucket, Key=key.rstrip("/") + "/data.parquet")["Body"].read()
    t = pq.read_table(io.BytesIO(body), columns=["account_id", "market_value_eod", "day_quality"]).to_pydict()
    mv = {a: v for a, v in zip(t["account_id"], t["market_value_eod"])}
    by_h = {}
    for r in rows:
        by_h.setdefault(r["household_ref"], []).append(r)
    picks = sorted(by_h, key=lambda h: hashlib.sha256(h.encode("utf-8")).hexdigest())[:2]
    checked = 0
    for h in picks:
        rs = by_h[h]
        accts = sorted({r["row_key"] for r in rs if r["member_id"] == "account.last4"})
        mine = [r for r in rs if r["member_id"] == member_id and r["row_key"] == ""]
        need(len(mine) == 1, "the household ending value member is not one household-grain row")
        m = mine[0]
        if m["value_number"] is None:
            continue
        need(all(a in mv and mv[a] is not None for a in accts), "a measured household ending value over an account with no gold value")
        exp = sum(mv[a] for a in accts)
        need(abs(m["value_number"] - exp) <= 0.01, "household ending value %.2f differs from the gold sum %.2f" % (m["value_number"], exp))
        checked += 1
    return checked, len(picks)


# ------------------------------------------------------------------------------------------------ the contract clauses (pure)
def check_contract(c, base_members_ok=True):
    need(c.get("contract_version") in ("0.5.2", "0.5.3"), "contract_version is not 0.5.2 (or the later 0.5.3 that DB-b-232 lands)")
    ids = [m["id"] for m in c["members"]]
    need(len(ids) == 117 and hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest() == MEMBER_IDS_SHA, "the member list changed")
    absent = [m["id"] for m in c["members"] if m.get("source") == "ABSENT"]
    need(hashlib.sha256("\n".join(sorted(absent)).encode()).hexdigest() == ABSENT_SOURCED_SHA, "the ABSENT-sourced member set changed")
    need(hashlib.sha256(json.dumps(c["document"], sort_keys=True, separators=(",", ":")).encode()).hexdigest() == DOCUMENT_SHA,
         "the document layout changed")
    lins = [x for x in c["lineage"] if x.get("contract_version") == BASE_VERSION]
    need(len(lins) == 1 and lins[0].get("sha256") == BASE_SHA and nes(lins[0].get("reason")),
         "lineage must carry the 0.5.1 bytes' sha256 and a reason")
    g = c.get("gold_table")
    need(isinstance(g, dict), "no gold_table block")
    need(g.get("table") == "filled_report_values", "gold_table.table")
    need(g.get("columns") == COLUMNS, "gold_table.columns differ from the schema")
    need(isinstance(g.get("address_rule"), str) and "address(" in g["address_rule"] and "date=" in g["address_rule"],
         "gold_table.address_rule must name lib/opal_naming address() and the date partition")
    for k in ("grain", "reader", "reserved_member_ids", "row_forms"):
        need(k in g and g[k], "gold_table.%s missing" % k)
    need(g["reserved_member_ids"] == list(RESERVED), "gold_table.reserved_member_ids differ")
    need(g.get("claim") in CLAIMS, "gold_table.claim not in the four words")
    return True


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, nrows, table_sha, module_sha, tracked):
    exp = {"firm", "as_of", "contract_version", "households", "households_basis", "rows", "members_expected", "measured_rows", "text_rows",
           "absent_rows", "private_parquet", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and ISO.match(str(rec["as_of"])) and rec["contract_version"] == "0.5.2", "firm, as_of or contract_version")
    need(is_int(rec["households"]) and 1 <= rec["households"] <= 100, "households must be 1 to 100 (the QA sample)")
    need(nes(rec["households_basis"]), "households_basis words")
    need(rec["members_expected"] == 117, "members_expected is not 117")
    need(rec["rows"] == nrows and rec["measured_rows"] + rec["text_rows"] + rec["absent_rows"] == nrows, "row counts do not add up to the table")
    pp = rec["private_parquet"]
    need(isinstance(pp, dict) and set(pp) == {"path", "sha256", "rows"} and pp["sha256"] == table_sha and pp["rows"] == nrows
         and str(pp["path"]).replace("\\", "/").startswith(PRIVATE_ROOT), "private_parquet path, hash or rows")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == MODULE_REL and an.get("sha256") == module_sha and an.get("tracked") is True and tracked,
         "analysis file, hash or tracked flag")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["claim"] in CLAIMS, "claim")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False,
         "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields")
    return True


def module_clauses(text):
    low = text.lower()
    need("address(" in text, "the module does not use lib/opal_naming address()")
    need(not re.search(r"s3://opal-data-|opal-data-49financial", low), "the module types a bucket")
    need(not [t for t in FOREIGN if t in low], "the module names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the module holds an S3 or DynamoDB write")
    return True


def read_table_rows(path):
    import pyarrow.parquet as pq
    t = pq.read_table(path)
    need(t.column_names == COLUMNS, "the parquet columns differ from the schema: %s" % t.column_names)
    d = t.to_pydict()
    return [{c: d[c][i] for c in COLUMNS} for i in range(t.num_rows)]


def run(root, cid):
    root = Path(root)
    if cid == "DB118-1-AC1":
        rec = load_json(root, REC_REL)
        pq_path = Path(str(rec["private_parquet"]["path"]))
        need(pq_path.is_file(), "no private QA parquet")
        c = load_json(root, CONTRACT_REL)
        ids = [m["id"] for m in c["members"]]
        absent = {m["id"] for m in c["members"] if m.get("source") == "ABSENT"}
        rows = read_table_rows(pq_path)
        nh = check_rows(rows, ids, absent, rec["as_of"])
        need(nh == rec["households"], "households: record %s, table %s" % (rec["households"], nh))
        n_num = sum(1 for r in rows if r["value_number"] is not None)
        n_txt = sum(1 for r in rows if r["value_text"] is not None)
        n_abs = sum(1 for r in rows if r["absent_kind"] is not None)
        need((rec["measured_rows"], rec["text_rows"], rec["absent_rows"]) == (n_num, n_txt, n_abs), "row-form counts differ from the table")
        mp = root / MODULE_REL
        need(mp.is_file(), "no module")
        check_record(rec, len(rows), sha_file(pq_path), sha_file(mp), is_tracked(root, MODULE_REL))
        eq = next(e for e in c["equivalences"] if e["id"] == "ENDING_VALUE_HOUSEHOLD")
        checked, picked = ending_value_probe(root, rows, rec["as_of"], eq["members"][0])
        print("OK: filled_report_values: %d households, %d rows (%d measured, %d text, %d absent), every contract member per household, "
              "no duplicate key, ending value equals the gold sum for %d of %d probed households" % (nh, len(rows), n_num, n_txt, n_abs, checked, picked))
        return True
    if cid == "DB118-1-AC2":
        check_contract(load_json(root, CONTRACT_REL))
        print("OK: contract %s carries gold_table filled_report_values (13 columns); members, document and absent-sourced set unchanged; lineage holds the 0.5.1 bytes' hash" % load_json(root, CONTRACT_REL)["contract_version"])
        return True
    if cid == "DB118-1-AC3":
        mp, tp = root / MODULE_REL, root / TEST_REL
        need(mp.is_file() and tp.is_file(), "no module or no test file")
        need(is_tracked(root, MODULE_REL) and is_tracked(root, TEST_REL), "the module or its tests are not tracked")
        module_clauses(mp.read_text(encoding="utf-8"))
        names = set(re.findall(r"def (test_\w+)", tp.read_text(encoding="utf-8")))
        for t in REQUIRED_TESTS:
            need(t in names, "the test file lacks the required repair test %s" % t)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(tp)], cwd=str(root),
                           capture_output=True, text=True, timeout=100)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= MIN_TESTS and "failed" not in r.stdout,
             "pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: %s tests pass; the module uses address(), types no bucket, names no other firm, holds no S3 or DynamoDB write" % m.group(1))
        return True
    raise Fail("unknown criterion %s" % cid)


# ------------------------------------------------------------------------------------------------ self-test
def selftest(root):
    ids = ["m.a", "m.b", "hold.allocation", "m.na"]
    absent = {"m.na"}

    def row(h, m, rk="", vn=None, vt=None, ak=None, ar=None, sp="", pd=""):
        return dict(firm=FIRM, household_ref=h, as_of="2026-10-13", member_id=m, row_key=rk, series_name=sp, point_date=pd, value_number=vn,
                    value_text=vt, absent_kind=ak, absent_reason=ar, contract_version="0.5.2", schema_version="1.0")

    def household(h):
        rs = [row(h, "household.first_data_date", vt="2020-01-02"),
              row(h, "account.last4", "A1", vt="1234"), row(h, "account.first_data_date", "A1", vt="2020-01-02")]
        rs += [row(h, "account.window_status." + w, "A1", vt="MEASURED") for w in ("qtd", "ytd", "last_12_months", "since_inception")]
        rs += [row(h, "m.a", vn=10.0), row(h, "m.b", "A1", vn=5.0), row(h, "hold.allocation", "equity", vn=1.0),
               row(h, "hold.allocation", "cash", vt="UNHELD"), row(h, "m.na", ak="NO_SOURCE_YET", ar="no source yet")]
        return rs

    good = household("H1") + household("H2")
    need(check_rows(good, ids, absent, "2026-10-13") == 2, "GREEN arm failed")

    def red(mut, why):
        rs = [dict(r) for r in good]
        mut(rs)
        try:
            check_rows(rs, ids, absent, "2026-10-13")
        except Fail:
            return
        raise Fail("RED arm did not fail: " + why)

    red(lambda rs: rs.append(dict(rs[-1])), "a duplicate key")
    red(lambda rs: rs[-5].update(value_number=1.0, value_text="x"), "two forms in one row")
    red(lambda rs: rs[-5].update(value_number=None), "no form in a row")
    red(lambda rs: rs[-1].update(absent_kind="MADE_UP"), "an absent kind outside the three")
    red(lambda rs: rs[-1].update(absent_reason=" "), "an empty absent reason")
    red(lambda rs: rs[-1].update(absent_kind=None, absent_reason=None, value_number=0.0), "an ABSENT-sourced member filled with zero")
    red(lambda rs: rs[-1].update(absent_kind="SOURCE_BREAK"), "an ABSENT-sourced member with the wrong kind")
    red(lambda rs: [rs.remove(r) for r in list(rs) if r["household_ref"] == "H2" and r["member_id"] == "m.b"], "a missing member")
    red(lambda rs: rs.append(row("H1", "m.zz", vn=1.0)), "an extra member")
    red(lambda rs: rs[-6].update(value_text="UNHELD", value_number=None), "UNHELD outside hold.allocation")
    red(lambda rs: rs[8].update(value_number=float("nan")), "a NaN")
    red(lambda rs: rs[0].update(firm="other"), "a different firm")
    red(lambda rs: [rs.remove(r) for r in list(rs) if r["household_ref"] == "H1" and r["member_id"] == "account.last4"], "a household with no account rows")
    # contract clauses: build a synthetic contract that passes, then break it
    base = json.loads((Path(root) / CONTRACT_REL).read_bytes().decode("utf-8")) if (Path(root) / CONTRACT_REL).is_file() else None
    if base is not None and base.get("contract_version") in ("0.5.2", "0.5.3"):
        check_contract(base)
        b2 = json.loads(json.dumps(base))
        b2["gold_table"]["columns"] = COLUMNS[:-1]
        try:
            check_contract(b2)
            raise Fail("RED: a short column list must fail")
        except Fail as e:
            need("columns" in str(e), "contract RED arm failed for another reason: %s" % e)
    # module clauses
    module_clauses("from lib import opal_naming\nx = opal_naming.address('irpt', f, 'gold', t, p)\n")
    for bad, why in (("x = 1", "no address()"), ("address(\n b = 's3://opal-data-49financial/'", "a typed bucket"),
                     ("address(\n f = 'cottonwood'", "another firm"), ("address(\n s3.put_object()", "a write call")):
        try:
            module_clauses(bad)
            raise Fail("RED: module clause did not fail: " + why)
        except Fail as e:
            need("RED" not in str(e), str(e))
    # record clauses
    rec = {"firm": FIRM, "as_of": "2026-10-13", "contract_version": "0.5.2", "households": 25, "households_basis": "the 25 lowest",
           "rows": 10, "members_expected": 117, "measured_rows": 4, "text_rows": 4, "absent_rows": 2,
           "private_parquet": {"path": PRIVATE_ROOT + "x.parquet", "sha256": "ab" * 32, "rows": 10},
           "analysis": {"file": MODULE_REL, "sha256": "cd" * 32, "tracked": True},
           "reads": {"s3_reads": 9, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured",
           "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    need(check_record(rec, 10, "ab" * 32, "cd" * 32, True), "record GREEN arm")
    for mut, why in ((lambda r: r.update(rows=11), "rows"), (lambda r: r["private_parquet"].update(sha256="00" * 32), "table hash"),
                     (lambda r: r.update(pushed=True), "push flag"), (lambda r: r.update(households=101), "households over the sample"),
                     (lambda r: r.update(members_expected=116), "member count"), (lambda r: r["reads"].update(s3_writes=1), "a write"),
                     (lambda r: r.update(households_basis="ids 1234567890"), "a digit run")):
        r2 = json.loads(json.dumps(rec))
        mut(r2)
        try:
            check_record(r2, 10, "ab" * 32, "cd" * 32, True)
            raise Fail("RED: record clause did not fail: " + why)
        except Fail as e:
            need("RED" not in str(e), str(e))
    try:
        check_record(rec, 10, "ab" * 32, "cd" * 32, False)
        raise Fail("RED: an untracked module must fail")
    except Fail as e:
        need("RED" not in str(e), str(e))
    print("selftest OK: 1 green and 13 red table arms, contract and module arms, 1 green and 8 red record arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p118_hop1.py <repo_root> <criterion_id>")
            sys.exit(2)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
