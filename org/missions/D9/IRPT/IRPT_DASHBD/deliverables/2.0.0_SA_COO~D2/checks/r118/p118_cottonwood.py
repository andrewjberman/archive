"""IRPT_DASHBD round 118 (issuer 2.0.0_SA_COO~D2) -- DB-b-232, the Cottonwood reader cut into the filled-report builder
(CTO analysis @5934ffcedc ruling 3; `~C2` ask 7949).

  DB-b-232 (~185, after DB-b-230 on the same queue) a Cottonwood reader (an adapter that reads ONLY the Cottonwood gold prefixes and refuses any other
                  firm's prefix), the contract's Cottonwood members (0.5.3), and two LOCAL QA runs into the private folder.
                                                    DB118-3-AC1 (the reader and its negative tests), AC2 (the contract), AC3 (the two QA runs)

AC3 RECOMPUTES the Cottonwood frontier from the gold (read-only S3 LIST of the account_return_daily date= prefixes) and grades both QA runs
from their private parquet files with DB-b-230's table clauses (p118_hop1.check_rows, firm cottonwood): run 1 at the frontier date holds measured
account-return members; run 2 at a date AFTER the frontier holds EVERY account-return member as the absent form SOURCE_BREAK whose words name the
frontier date, and not one measured figure for those members. The history after the frontier is absent, never zero and never partial.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the clauses on synthetic arms
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~185/RD_COTTONWOOD_QA_R118.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_report_reader.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_cottonwood_report_reader.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
PRIVATE_ROOT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~185/"
FIRM = "cottonwood"
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("49financial", "inflection", "orion/", "eclipse/", "opal-data-49financial", "opal-data-inflection", "opal-data-assets")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")
HEX64 = re.compile(r"[0-9a-f]{64}$")
INFLECTION_SOURCES_SHA = "2b2b2c73ada31fc52249e0a876d091746546f6fd41fbf0f917f2454a665ab325"
FS_KEYS = {"input", "grain", "table", "field", "fold", "claim"}
MIN_TESTS = 8
ACCOUNT_RETURN = "IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
# round 119 (DB-b-233): ten activity and net-gain members now source the account return contract THROUGH their value-summary counterparts;
# they carry no firm_sources of their own, so the 36 members of this check exclude them
REPAIRED_TEN = ("act.beginning_value.household", "act.beginning_value.account", "act.net_gain.household", "act.net_gain.account",
                "act.ending_value.household", "act.ending_value.account", "hold.net_gain_last_12_months", "hold.net_gain_ytd", "hold.net_gain_qtd",
                "hold.net_gain_since_inception")


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


def hop1(root):
    p = Path(__file__).with_name("p118_hop1.py")
    spec = importlib.util.spec_from_file_location("p118_hop1", str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ------------------------------------------------------------------------------------------------ the frontier (read-only LIST)
def frontier_date(root):
    sys.path.insert(0, str(root))
    import boto3
    from lib import opal_naming
    addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=2000-01-01")
    bucket, key = addr[len("s3://"):].split("/", 1)
    prefix = key.rsplit("date=", 1)[0]
    s3 = boto3.client("s3")
    best, n, token = None, 0, None
    while True:
        kw = dict(Bucket=bucket, Prefix=prefix, Delimiter="/")
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        for cp in r.get("CommonPrefixes", []):
            d = cp["Prefix"][len(prefix):].strip("/")
            if d.startswith("date=") and ISO.match(d[5:]):
                n += 1
                best = d[5:] if best is None or d[5:] > best else best
        if not r.get("IsTruncated"):
            break
        token = r["NextContinuationToken"]
    need(best is not None, "no Cottonwood account_return_daily partition listed")
    return best, n


# ------------------------------------------------------------------------------------------------ the contract clauses (pure)
def check_contract(c, base_sha_of_052):
    need(c.get("contract_version") in ("0.5.3", "0.5.4"), "contract_version is not 0.5.3 (or the later 0.5.4 of round 119)")
    ids = [m["id"] for m in c["members"]]
    need(len(ids) == 117 and hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest() ==
         "dce57d0221f5b51ed59edfbe09b53de674f42570347177f606dddce9c76d4eda", "the member list changed")
    lins = [x for x in c["lineage"] if x.get("contract_version") == "0.5.2"]
    need(len(lins) == 1 and HEX64.match(str(lins[0].get("sha256"))) and nes(lins[0].get("reason")), "lineage must carry the 0.5.2 entry")
    lin = lins[0]
    need(base_sha_of_052 is None or lin["sha256"] == base_sha_of_052, "lineage sha256 is not the 0.5.2 bytes' hash")
    g = c.get("gold_table", {})
    need(g.get("table") == "filled_report_values" and isinstance(g.get("columns"), list) and len(g["columns"]) == 13, "gold_table block changed")
    ar = [m for m in c["members"] if isinstance(m.get("source"), dict) and m["source"].get("contract", "").endswith(ACCOUNT_RETURN) and m["id"] not in REPAIRED_TEN]
    need(len(ar) == 36, "expected 36 account-return members, found %d" % len(ar))
    for m in ar:
        fs = (m.get("firm_sources") or {}).get(FIRM)
        need(isinstance(fs, dict) and set(fs) == FS_KEYS and all(nes(fs[k]) for k in FS_KEYS), "member %s lacks a complete Cottonwood source" % m["id"])
        need("cottonwood" in fs["table"] and "account_return_daily" in fs["table"] and "address(" not in fs["table"],
             "member %s: the Cottonwood table must be the Cottonwood account_return_daily address form" % m["id"])
        need(fs["claim"].split(":")[0].strip() in CLAIMS or any(w in fs["claim"] for w in ("derived", "measured", "inferred")), "member %s claim" % m["id"])
        need("frontier" in fs["fold"].lower() or "ends" in fs["fold"].lower(), "member %s: the fold must state the source-ends rule" % m["id"])
    inf = {m["id"]: m["firm_sources"]["inflection"] for m in c["members"] if "firm_sources" in m and "inflection" in m["firm_sources"]}
    need(len(inf) == 8 and hashlib.sha256(json.dumps(inf, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == INFLECTION_SOURCES_SHA,
         "the Inflection sources changed")
    fh = c.get("firm_households", {}).get(FIRM)
    need(isinstance(fh, dict) and fh.get("table") == "account_dim" and fh.get("field") == "household_id" and nes(fh.get("words")),
         "firm_households.cottonwood must name account_dim.household_id with words")
    ui = c.get("unread_inputs")
    need(isinstance(ui, list) and any(isinstance(x, dict) and x.get("table") == "holdings_performance_daily" and nes(x.get("reason")) for x in ui),
         "unread_inputs must record holdings_performance_daily with a reason")
    return True


def sha_of_version(root, version):
    """sha256 of the newest committed contract bytes that read contract_version == version (None when not found)."""
    out = subprocess.run(["git", "-C", str(root), "log", "--format=%H", "--", CONTRACT_REL], capture_output=True, text=True).stdout.split()
    for h in out[:40]:
        b = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (h, CONTRACT_REL)], capture_output=True).stdout
        try:
            if json.loads(b.decode("utf-8")).get("contract_version") == version:
                return hashlib.sha256(b).hexdigest()
        except Exception:
            continue
    return None


# ------------------------------------------------------------------------------------------------ the QA record clauses (pure)
def check_runs(rec, frontier, runs_rows, account_return_ids, parquet_sha):
    """runs_rows: list of the row lists of the two runs, in record order."""
    exp = {"firm", "frontier_date", "partitions_listed", "households_source", "runs", "analysis", "reads", "claim", "files_in_repo",
           "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and rec["frontier_date"] == frontier[0] and rec["partitions_listed"] == frontier[1],
         "frontier: record %s/%s, recount %s/%s" % (rec.get("frontier_date"), rec.get("partitions_listed"), frontier[0], frontier[1]))
    need(nes(rec["households_source"]) and "dry run" in rec["households_source"].lower()
         and "not applied" in rec["households_source"].lower(),
         "households_source must say the gold account_dim is not applied and the frame is the adapter's dry run")
    runs = rec["runs"]
    need(isinstance(runs, list) and len(runs) == 2, "exactly two runs")
    need(runs[0]["as_of"] == frontier[0] and runs[1]["as_of"] > frontier[0] and ISO.match(runs[1]["as_of"]), "run 1 is at the frontier, run 2 after it")
    for run, rows, sha in zip(runs, runs_rows, parquet_sha):
        need(set(run) == {"as_of", "households", "rows", "measured_rows", "text_rows", "absent_rows", "private_parquet"}, "run keys")
        pp = run["private_parquet"]
        need(set(pp) == {"path", "sha256", "rows"} and pp["sha256"] == sha and pp["rows"] == len(rows) == run["rows"]
             and str(pp["path"]).replace("\\", "/").startswith(PRIVATE_ROOT), "private_parquet path, hash or rows")
        n_num = sum(1 for r in rows if r["value_number"] is not None)
        n_txt = sum(1 for r in rows if r["value_text"] is not None)
        n_abs = sum(1 for r in rows if r["absent_kind"] is not None)
        need((run["measured_rows"], run["text_rows"], run["absent_rows"]) == (n_num, n_txt, n_abs), "row-form counts differ from the table")
        need(is_int(run["households"]) and 1 <= run["households"] <= 100, "households must be 1 to 100")
    r1, r2 = runs_rows
    need(sum(1 for r in r1 if r["value_number"] is not None and r["member_id"] in account_return_ids) > 0,
         "run 1 (at the frontier) holds no measured account-return member")
    for r in r2:
        if r["member_id"] in account_return_ids:
            need(r["value_number"] is None and r["value_text"] is None, "run 2 holds a figure for an account-return member after the frontier")
            need(r["absent_kind"] == "SOURCE_BREAK" and frontier[0] in str(r["absent_reason"]),
                 "run 2: an account-return member must be SOURCE_BREAK with words naming the frontier date")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == MODULE_REL and an.get("tracked") is True, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["claim"] in CLAIMS and rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False
         and rec["deployed"] is False, "claim or a flag")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields")
    return True


def module_clauses(text):
    low = text.lower()
    need("address(" in text, "the reader does not use lib/opal_naming address()")
    need(not re.search(r"s3://opal-data-", low), "the reader types a bucket")
    need(not [t for t in FOREIGN if t in low], "the reader names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the reader holds an S3 or DynamoDB write")
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB118-3-AC1":
        mp, tp = root / MODULE_REL, root / TEST_REL
        need(mp.is_file() and tp.is_file(), "no reader or no test file")
        need(is_tracked(root, MODULE_REL) and is_tracked(root, TEST_REL), "the reader or its tests are not tracked")
        module_clauses(mp.read_text(encoding="utf-8"))
        names = re.findall(r"def (test_refuses_\w+)", tp.read_text(encoding="utf-8"))
        need(len(names) >= 2, "the tests need at least two test_refuses_* negative tests (another firm's prefix), found %d" % len(names))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(tp)], cwd=str(root),
                           capture_output=True, text=True, timeout=100)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= MIN_TESTS and "failed" not in r.stdout,
             "pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: %s tests pass including %d test_refuses_* negatives; the reader uses address(), types no bucket, names no other firm, writes nothing"
              % (m.group(1), len(names)))
        return True
    if cid == "DB118-3-AC2":
        check_contract(load_json(root, CONTRACT_REL), sha_of_version(root, "0.5.2"))
        print("OK: contract 0.5.3 carries a Cottonwood source on all 36 account-return members, the household key from account_dim, "
              "holdings_performance_daily recorded unread; members, gold_table and the Inflection sources unchanged; lineage ends 0.5.2")
        return True
    if cid == "DB118-3-AC3":
        h1 = hop1(root)
        rec = load_json(root, REC_REL)
        c = load_json(root, CONTRACT_REL)
        ids = [m["id"] for m in c["members"]]
        absent = {m["id"] for m in c["members"] if m.get("source") == "ABSENT"}
        ar = {m["id"] for m in c["members"] if isinstance(m.get("source"), dict) and m["source"].get("contract", "").endswith(ACCOUNT_RETURN)}
        frontier = frontier_date(root)
        rows_l, sha_l = [], []
        for run_ in rec["runs"]:
            pth = Path(str(run_["private_parquet"]["path"]))
            need(pth.is_file(), "no private QA parquet")
            rows = h1.read_table_rows(pth)
            h1.check_rows(rows, ids, absent, run_["as_of"], firm=FIRM)
            rows_l.append(rows)
            sha_l.append(sha_file(pth))
        check_runs(rec, frontier, rows_l, ar, sha_l)
        print("OK: Cottonwood frontier %s (%d partitions listed); run 1 at the frontier holds measured members; run 2 after it holds every "
              "account-return member as SOURCE_BREAK naming the frontier, no figure" % frontier)
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest(root):
    def row(m, vn=None, vt=None, ak=None, ar=None):
        return dict(firm=FIRM, household_ref="H", as_of="x", member_id=m, row_key="", series_name="", point_date="", value_number=vn,
                    value_text=vt, absent_kind=ak, absent_reason=ar, contract_version="0.5.3", schema_version="1.0")
    ids = {"m.ar1", "m.ar2"}
    frontier = ("2026-06-22", 3325)
    rec = {"firm": FIRM, "frontier_date": "2026-06-22", "partitions_listed": 3325, "households_source": "the gold account_dim is not applied; the frame is the adapter's own dry run",
           "runs": [{"as_of": "2026-06-22", "households": 5, "rows": 2, "measured_rows": 1, "text_rows": 0, "absent_rows": 1,
                     "private_parquet": {"path": PRIVATE_ROOT + "a.parquet", "sha256": "aa" * 32, "rows": 2}},
                    {"as_of": "2026-10-13", "households": 5, "rows": 2, "measured_rows": 0, "text_rows": 0, "absent_rows": 2,
                     "private_parquet": {"path": PRIVATE_ROOT + "b.parquet", "sha256": "bb" * 32, "rows": 2}}],
           "analysis": {"file": MODULE_REL, "sha256": "cc" * 32, "tracked": True},
           "reads": {"s3_reads": 7, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured",
           "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    r1 = [row("m.ar1", vn=1.0), row("m.ar2", ak="SOURCE_BREAK", ar="the source ends 2026-06-22")]
    r2 = [row("m.ar1", ak="SOURCE_BREAK", ar="the source ends 2026-06-22"), row("m.ar2", ak="SOURCE_BREAK", ar="the source ends 2026-06-22")]
    shas = ["aa" * 32, "bb" * 32]
    need(check_runs(rec, frontier, [r1, r2], ids, shas), "GREEN arm")

    def red(mut_rec=None, mut_rows=None, fr=frontier, sh=shas, why=""):
        rc = json.loads(json.dumps(rec))
        rr = [json.loads(json.dumps(r1)), json.loads(json.dumps(r2))]
        if mut_rec:
            mut_rec(rc)
        if mut_rows:
            mut_rows(rr)
        try:
            check_runs(rc, fr, rr, ids, sh)
        except Fail:
            return
        raise Fail("RED arm did not fail: " + why)
    red(fr=("2026-06-23", 3325), why="a frontier that differs from the gold")
    red(mut_rows=lambda rr: rr[1][0].update(value_number=0.0, absent_kind=None, absent_reason=None), why="a zero after the frontier")
    red(mut_rows=lambda rr: rr[1][0].update(absent_kind="NO_SOURCE_YET"), why="the wrong kind after the frontier")
    red(mut_rows=lambda rr: rr[1][0].update(absent_reason="gone"), why="words that do not name the frontier")
    red(mut_rows=lambda rr: rr[0][0].update(value_number=None, absent_kind="SOURCE_BREAK", absent_reason="x"), why="run 1 with nothing measured")
    red(mut_rec=lambda rc: rc["runs"][1].update(as_of="2026-06-22"), why="run 2 not after the frontier")
    red(sh=["aa" * 32, "00" * 32], why="a parquet hash mismatch")
    red(mut_rec=lambda rc: rc.update(households_source="account_dim household_id"), why="households_source without the dry run and not applied words")
    red(mut_rec=lambda rc: rc.update(pushed=True), why="a push flag")
    red(mut_rec=lambda rc: rc["runs"][0].update(households=0), why="no households")
    red(mut_rec=lambda rc: rc.update(households_source="ids 1234567890"), why="a digit run")
    module_clauses("from lib import opal_naming\nx = opal_naming.address('irpt', 'cottonwood', 'gold', t, p)\n")
    for bad, why in (("x = 1", "no address()"), ("address(\n b = 's3://opal-data-cottonwood/'", "a typed bucket"),
                     ("address(\n f = '49financial'", "another firm"), ("address(\n s3.put_object()", "a write call")):
        try:
            module_clauses(bad)
            raise Fail("RED: module clause did not fail: " + why)
        except Fail as e:
            need("RED" not in str(e), str(e))
    print("selftest OK: 1 green and 11 red run arms, 4 red module arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p118_cottonwood.py <repo_root> <criterion_id>")
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
