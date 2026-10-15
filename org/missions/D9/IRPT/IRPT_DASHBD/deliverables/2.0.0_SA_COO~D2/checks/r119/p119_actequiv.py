"""IRPT_DASHBD round 119, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-233, the contract 0.5.4 and the module TOGETHER
(CTO analysis @d856067e84 ruling 1; the carrier is row IRPT_DASHBD-D2-S56).

  DB-b-233 (~187) the ten activity and net-gain members (act.beginning_value, act.net_gain, act.ending_value at household and account grain, and
                  hold.net_gain for four windows) print the SAME folds as the value-summary members DB-b-202 ruled they equal; the contract
                  says so (0.5.4, equivalences) and the module fills them from their counterparts, so no member is absent for a reason the
                  contract created.                                   DB119-1-AC1 (the table), AC2 (the contract), AC3 (the tests)

The checker grades the private QA parquet with DB-b-230's table clauses (p118_hop1.check_rows) and then, per household, the ten PAIRS: a measured
pair is equal (a figure within 0.005), an absent pair is absent in BOTH members with the same kind, and one measured beside one absent is a defect.
It also requires that no pair is wholly absent when its counterpart is measured for some household. It hashes the 107 members the repair does not
touch, the document, the gold_table, the firm_sources and the lineage.

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
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~187/RD_ACT_EQUIV_R119.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/filled_report_values.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_filled_report_values.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
PRIVATE_ROOT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~187/"
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
# (the value-summary member, the member that must equal it)
PAIRS = (
    ("pvs.last_12_months.beginning_value", "act.beginning_value.household"),
    ("avs.last_12_months.beginning_value", "act.beginning_value.account"),
    ("pvs.last_12_months.net_gain", "act.net_gain.household"),
    ("avs.last_12_months.net_gain", "act.net_gain.account"),
    ("pvs.last_12_months.ending_value", "act.ending_value.household"),
    ("avs.last_12_months.ending_value", "act.ending_value.account"),
    ("pvs.last_12_months.net_gain", "hold.net_gain_last_12_months"),
    ("pvs.ytd.net_gain", "hold.net_gain_ytd"),
    ("pvs.qtd.net_gain", "hold.net_gain_qtd"),
    ("pvs.since_inception.net_gain", "hold.net_gain_since_inception"),
)
CHANGED = tuple(b for _, b in PAIRS)
UNCHANGED_SHA = "a60bc2c028a464482cc8a8303e8f14b6c33257bcca49021745b765010c31bdd1"
DOCUMENT_SHA = "87af1ec8eed20296a46338fa254fb83ebc2117adcc97b66eac179f36b5912dd7"
INFLECTION_SOURCES_SHA = "2b2b2c73ada31fc52249e0a876d091746546f6fd41fbf0f917f2454a665ab325"
REQUIRED_TESTS = ("test_activity_members_equal_value_summary_members", "test_households_come_from_the_adapter",
                  "test_missing_sibling_table_is_no_source_yet", "test_empty_lot_source_is_absent_not_zero")
MIN_TESTS = 22
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")
HEX64 = re.compile(r"[0-9a-f]{64}$")


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


def hop1():
    p = Path(__file__).resolve().parents[1] / "r118" / "p118_hop1.py"
    spec = importlib.util.spec_from_file_location("p118_hop1", str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ------------------------------------------------------------------------------------------------ the pair clauses (pure, over row dicts)
def index_rows(rows):
    """(household_ref, member_id) -> {row_key: row}"""
    out = {}
    for r in rows:
        out.setdefault((r["household_ref"], r["member_id"]), {})[(r["row_key"], r["series_name"], r["point_date"])] = r
    return out


def grade_pairs(rows):
    """Returns {changed member id: dict(both_measured, both_absent, differing)} over every household and every row key; raises Fail on a mismatch."""
    idx = index_rows(rows)
    hs = sorted({r["household_ref"] for r in rows})
    res = {b: {"counterpart": a, "both_measured": 0, "both_absent": 0, "differing": 0} for a, b in PAIRS}
    for a, b in PAIRS:
        for h in hs:
            ra, rb = idx.get((h, a), {}), idx.get((h, b), {})
            need(set(ra) == set(rb), "pair %s / %s: the row keys of a household differ" % (a, b))
            for k, x in ra.items():
                y = rb[k]
                if x["value_number"] is not None and y["value_number"] is not None:
                    if abs(x["value_number"] - y["value_number"]) > 0.005:
                        res[b]["differing"] += 1
                    else:
                        res[b]["both_measured"] += 1
                elif x["absent_kind"] is not None and y["absent_kind"] is not None:
                    if x["absent_kind"] != y["absent_kind"]:
                        res[b]["differing"] += 1
                    else:
                        res[b]["both_absent"] += 1
                elif x["value_text"] is not None and y["value_text"] is not None and x["value_text"] == y["value_text"]:
                    res[b]["both_measured"] += 1
                else:
                    res[b]["differing"] += 1
    for b, v in res.items():
        need(v["differing"] == 0, "%s differs from %s on %d row(s)" % (b, v["counterpart"], v["differing"]))
    return res


def check_pairs_not_all_absent(res, rows):
    """No member of the repair may be wholly absent where its counterpart is measured for some household."""
    idx = index_rows(rows)
    for a, b in PAIRS:
        meas_a = sum(1 for (h, m), d in idx.items() if m == a for r in d.values() if r["value_number"] is not None)
        if meas_a > 0:
            need(res[b]["both_measured"] > 0, "%s is absent everywhere although %s is measured" % (b, a))
    return True


# ------------------------------------------------------------------------------------------------ the contract clauses (pure)
def check_contract(c, sha_of_053):
    need(c.get("contract_version") == "0.5.4", "contract_version is not 0.5.4")
    ms = {m["id"]: m for m in c["members"]}
    need(len(ms) == 117, "the member count changed")
    rest = [m for m in c["members"] if m["id"] not in set(CHANGED)]
    need(hashlib.sha256(json.dumps(rest, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == UNCHANGED_SHA,
         "one of the 107 members the repair must not touch changed")
    for a, b in PAIRS:
        need(b in ms and a in ms, "member %s or %s is missing" % (a, b))
        s = ms[b].get("source")
        need(isinstance(s, dict) and s.get("contract", "").endswith("IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"),
             "member %s must now source the account return contract (the same fold as %s)" % (b, a))
        need(a in str(s.get("fold", "")), "member %s: the fold text must name its counterpart %s" % (b, a))
    need(hashlib.sha256(json.dumps(c["document"], sort_keys=True, separators=(",", ":")).encode()).hexdigest() == DOCUMENT_SHA, "the document layout changed")
    inf = {m["id"]: m["firm_sources"]["inflection"] for m in c["members"] if "firm_sources" in m and "inflection" in m["firm_sources"]}
    need(hashlib.sha256(json.dumps(inf, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == INFLECTION_SOURCES_SHA, "the Inflection sources changed")
    need(isinstance(c.get("gold_table"), dict) and len(c["gold_table"].get("columns", [])) == 13, "gold_table changed")
    eqs = {e["id"]: e for e in c.get("equivalences", [])}
    for a, b in PAIRS:
        need(any(a in e["members"] and b in e["members"] for e in eqs.values()),
             "no equivalence names both %s and %s" % (a, b))
    lins = [x for x in c["lineage"] if x.get("contract_version") == "0.5.3"]
    need(len(lins) == 1 and HEX64.match(str(lins[0].get("sha256"))) and nes(lins[0].get("reason")), "lineage must carry the 0.5.3 entry")
    need(sha_of_053 is None or lins[0]["sha256"] == sha_of_053, "lineage sha256 is not the committed 0.5.3 bytes' hash")
    return True


def sha_of_version(root, version):
    out = subprocess.run(["git", "-C", str(root), "log", "--format=%H", "--", CONTRACT_REL], capture_output=True, text=True).stdout.split()
    for h in out[:60]:
        b = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (h, CONTRACT_REL)], capture_output=True).stdout
        try:
            if json.loads(b.decode("utf-8")).get("contract_version") == version:
                return hashlib.sha256(b).hexdigest()
        except Exception:
            continue
    return None


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, nrows, counts, pairs_res, table_sha, module_sha, tracked):
    exp = {"firm", "as_of", "contract_version", "households", "households_basis", "rows", "measured_rows", "text_rows", "absent_rows",
           "pairs", "private_parquet", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and ISO.match(str(rec["as_of"])) and rec["contract_version"] == "0.5.4", "firm, as_of or contract_version")
    need(is_int(rec["households"]) and 1 <= rec["households"] <= 100 and nes(rec["households_basis"]), "households and basis")
    need(rec["rows"] == nrows and (rec["measured_rows"], rec["text_rows"], rec["absent_rows"]) == counts, "row counts differ from the table")
    pl = rec["pairs"]
    need(isinstance(pl, list) and [p.get("member") for p in pl] == list(CHANGED), "pairs must list the ten members in order")
    for p in pl:
        need(set(p) == {"member", "counterpart", "households_both_measured", "households_both_absent", "households_differing", "claim"} and p["claim"] in CLAIMS,
             "a pair entry has the wrong keys")
        t = pairs_res[p["member"]]
        need(p["counterpart"] == t["counterpart"] and p["households_differing"] == 0, "pair %s counterpart or differing" % p["member"])
        need(p["households_both_measured"] == t["both_measured"] and p["households_both_absent"] == t["both_absent"],
             "pair %s: record %s/%s, recount %s/%s" % (p["member"], p["households_both_measured"], p["households_both_absent"], t["both_measured"], t["both_absent"]))
    pp = rec["private_parquet"]
    need(isinstance(pp, dict) and set(pp) == {"path", "sha256", "rows"} and pp["sha256"] == table_sha and pp["rows"] == nrows
         and str(pp["path"]).replace("\\", "/").startswith(PRIVATE_ROOT), "private_parquet path, hash or rows")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == MODULE_REL and an.get("sha256") == module_sha and an.get("tracked") is True and tracked, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["claim"] in CLAIMS and rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False
         and rec["deployed"] is False, "claim or a flag")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields")
    return True


def run(root, cid):
    root = Path(root)
    h1 = hop1()
    if cid == "DB119-1-AC1":
        rec = load_json(root, REC_REL)
        pq_path = Path(str(rec["private_parquet"]["path"]))
        need(pq_path.is_file(), "no private QA parquet")
        c = load_json(root, CONTRACT_REL)
        ids = [m["id"] for m in c["members"]]
        absent = {m["id"] for m in c["members"] if m.get("source") == "ABSENT"}
        rows = h1.read_table_rows(pq_path)
        nh = h1.check_rows(rows, ids, absent, rec["as_of"])
        need(nh == rec["households"], "households: record %s, table %s" % (rec["households"], nh))
        res = grade_pairs(rows)
        check_pairs_not_all_absent(res, rows)
        counts = (sum(1 for r in rows if r["value_number"] is not None), sum(1 for r in rows if r["value_text"] is not None),
                  sum(1 for r in rows if r["absent_kind"] is not None))
        mp = root / MODULE_REL
        need(mp.is_file(), "no module")
        check_record(rec, len(rows), counts, res, sha_file(pq_path), sha_file(mp), is_tracked(root, MODULE_REL))
        print("OK: %d households, %d rows; all ten pairs equal in every household (%d measured pairs, %d absent pairs, 0 differing); "
              "no member wholly absent beside a measured counterpart" %
              (nh, len(rows), sum(v["both_measured"] for v in res.values()), sum(v["both_absent"] for v in res.values())))
        return True
    if cid == "DB119-1-AC2":
        check_contract(load_json(root, CONTRACT_REL), sha_of_version(root, "0.5.3"))
        print("OK: contract 0.5.4: the ten members source the account return folds and name their counterparts, each pair is in an equivalence; "
              "the other 107 members, the document, gold_table, Inflection sources unchanged; lineage carries 0.5.3")
        return True
    if cid == "DB119-1-AC3":
        mp, tp = root / MODULE_REL, root / TEST_REL
        need(mp.is_file() and tp.is_file() and is_tracked(root, MODULE_REL) and is_tracked(root, TEST_REL), "module or tests missing or untracked")
        h1.module_clauses(mp.read_text(encoding="utf-8"))
        names = set(re.findall(r"def (test_\w+)", tp.read_text(encoding="utf-8")))
        for t in REQUIRED_TESTS:
            need(t in names, "the test file lacks the required test %s" % t)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(tp)], cwd=str(root),
                           capture_output=True, text=True, timeout=100)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= MIN_TESTS and "failed" not in r.stdout,
             "pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: %s tests pass including the pair test; the module uses address(), types no bucket, names no other firm, holds no write" % m.group(1))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest(root):
    def row(h, m, rk="", vn=None, vt=None, ak=None, ar=None):
        return dict(firm=FIRM, household_ref=h, as_of="x", member_id=m, row_key=rk, series_name="", point_date="", value_number=vn, value_text=vt,
                    absent_kind=ak, absent_reason=ar, contract_version="0.5.4", schema_version="1.0")

    def make(h, v):
        rs = []
        for a, b in PAIRS:
            grain_acct = a.startswith("avs.")
            rk = "A1" if grain_acct else ""
            if v is None:
                rs += [row(h, a, rk, ak="INSUFFICIENT_HISTORY", ar="x"), row(h, b, rk, ak="INSUFFICIENT_HISTORY", ar="x")]
            else:
                rs += [row(h, a, rk, vn=v), row(h, b, rk, vn=v)]
        return rs
    good = make("H1", 100.0) + make("H2", None)
    res = grade_pairs(good)
    need(all(v["both_measured"] >= 1 and v["both_absent"] >= 1 for v in res.values()), "green pairs")
    need(check_pairs_not_all_absent(res, good), "green not-all-absent")

    def bad(mut, why):
        rs = [dict(r) for r in good]
        mut(rs)
        try:
            r2 = grade_pairs(rs)
            check_pairs_not_all_absent(r2, rs)
        except Fail:
            return
        raise Fail("RED arm did not fail: " + why)
    bad(lambda rs: rs[1].update(value_number=101.0), "a figure that differs from its counterpart")
    bad(lambda rs: rs[1].update(value_number=None, absent_kind="SOURCE_BREAK", absent_reason="x"), "a measured member beside an absent counterpart")
    bad(lambda rs: rs.__delitem__(1), "a missing counterpart row")
    allabs = [dict(r) for r in good]
    for r in allabs:
        if r["member_id"] == "act.net_gain.household":
            r.update(value_number=None, absent_kind="INSUFFICIENT_HISTORY", absent_reason="x")
    try:
        grade_pairs(allabs)
        raise Fail("RED: a member absent beside a measured counterpart must fail")
    except Fail as e:
        need("RED" not in str(e), str(e))
    # the contract on the live file when it is at 0.5.4, else only the structural arm
    p = Path(root) / CONTRACT_REL
    if p.is_file():
        c = json.loads(p.read_bytes().decode("utf-8"))
        if c.get("contract_version") == "0.5.4":
            check_contract(c, None)
            c2 = json.loads(json.dumps(c))
            c2["members"][0]["label"] = c2["members"][0]["label"] + " x"
            try:
                check_contract(c2, None)
                raise Fail("RED: a changed untouched member must fail")
            except Fail as e:
                need("RED" not in str(e), str(e))
    print("selftest OK: 1 green and 4 red pair arms, the contract arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p119_actequiv.py <repo_root> <criterion_id>")
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
