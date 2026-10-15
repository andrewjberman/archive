"""IRPT_DASHBD round 119, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-234, the Cottonwood input to account_return_daily from Black Diamond
values and external flows, keyed by the Black Diamond account key (CTO analysis @d856067e84 ruling 2; B-CW round-117 ruling 3; ask 8040).

  DB-b-234 (~188) a pure derivation adapter over two Black Diamond silver frames (fact_allocations: the account value; fact_transactions: the
                  external flows) that reads only the Cottonwood Black Diamond silver grant, applies the ONE method of account_return_daily
                  (r_t = (V_t - F_t) / V_(t-1) - 1, the link rule, the skipped-day rule, the flow guard's FLOW_UNRECONCILED, never a fill),
                  labels every row `computed from Black Diamond values and flows`, and writes nothing to AWS; one LOCAL derivation for at most 25
                  accounts into the private folder, the seam of 2026-06-22 and 2026-06-23 read and stated.
                                     DB119-2-AC1 (the adapter and its tests), AC2 (the derivation), AC3 (the seam)

AC2 grades the private parquet: the contract's column names, firm cottonwood, the Black Diamond account key form (11 characters), the identity
r_t = (V_t - F_t) / V_(t-1) - 1 on every MEASURED row against the previous row of the same account, no return on a row that is not MEASURED, the key
overlap with the household frame, and it RECOMPUTES the account value of three (account, date) pairs from the Black Diamond silver itself.
AC3 RECOMPUTES the seam: the Cottonwood account_return_daily frontier, the first and last fact_allocations partition and whether the link-base day exists.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the clauses on synthetic arms
"""
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~188/RD_COTTONWOOD_BD_RETURN_R119.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_cottonwood_bd_account_return_daily.py"
ACCOUNT_CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
PRIVATE_ROOT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~188/"
FRAME = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~161/account_dim_dry_run.parquet"
BUCKET = "opal-data-assets"
SILVER = "blackdiamond/cottonwood/silver/"
FIRM = "cottonwood"
LABEL = "computed from Black Diamond values and flows"
KEY_LEN = 11
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("49financial", "inflection", "orion/", "eclipse/", "opal-data-49financial", "opal-data-inflection")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
REQUIRED_TESTS = ("test_unresolved_transaction_type_is_counted_never_signed", "test_absent_value_day_is_absent_never_zero")
MIN_TESTS = 10
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")


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


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def is_tracked(root, rel):
    return subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel], capture_output=True, text=True).returncode == 0


def p118(name):
    p = Path(__file__).resolve().parents[1] / "r118" / name
    spec = importlib.util.spec_from_file_location(name[:-3], str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ------------------------------------------------------------------------------------------------ the table clauses (pure, over a dict of columns)
def check_table(t, contract_columns, as_rows=None):
    """t: dict column -> list. Raises Fail on the first violated clause. Returns (rows, accounts, by_day_quality)."""
    need(list(t.keys()) == list(contract_columns), "the parquet columns differ from the contract's: %s" % list(t.keys()))
    n = len(t["account_id"])
    need(n > 0, "the table is empty")
    need(all(f == FIRM for f in t["firm"]), "a row's firm is not cottonwood")
    need(all(isinstance(a, str) and len(a) == KEY_LEN for a in t["account_id"]), "an account key is not the %d-character Black Diamond form" % KEY_LEN)
    keys = set()
    for a, d in zip(t["account_id"], t["business_date"]):
        need((a, d) not in keys, "a duplicate (account, date)")
        keys.add((a, d))
    by_acct = {}
    for i in range(n):
        by_acct.setdefault(t["account_id"][i], []).append(i)
    dq = {}
    for a, idxs in by_acct.items():
        idxs.sort(key=lambda i: t["business_date"][i])
        for j, i in enumerate(idxs):
            q = t["day_quality"][i]
            dq[q] = dq.get(q, 0) + 1
            r = t["total_return_daily"][i]
            if q != "MEASURED" and q != "LARGE_FLOW":
                need(r is None, "a row that is %s carries a return" % q)
                continue
            need(r is not None, "a MEASURED row carries no return")
            need(j > 0, "the first row of an account cannot be MEASURED (no previous value)")
            v0 = t["market_value_eod"][idxs[j - 1]]
            v, f = t["market_value_eod"][i], t["external_flow"][i]
            need(v0 is not None and v0 > 0 and v is not None and f is not None, "a MEASURED row without a positive previous value or its inputs")
            need(abs(r - ((v - f) / v0 - 1.0)) < 1e-9, "the identity r = (V - F) / V0 - 1 fails on a MEASURED row")
    return n, len(by_acct), dq


def pick_probes(t, k=3):
    rows = [(hashlib.sha256((a + d).encode("utf-8")).hexdigest(), a, d, v) for a, d, v in zip(t["account_id"], t["business_date"], t["market_value_eod"]) if v is not None]
    return [(a, d, v) for _, a, d, v in sorted(rows)[:k]]


# ------------------------------------------------------------------------------------------------ recounts (read-only)
def silver_partitions(s3, table):
    out, tok = [], None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=SILVER + table + "/", Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        out += [c["Prefix"].rstrip("/").rsplit("date=", 1)[1] for c in r.get("CommonPrefixes", []) if "date=" in c["Prefix"]]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    return sorted(out)


def recompute_value(s3, key_col, value_col, account, day):
    import pyarrow.parquet as pq
    body = s3.get_object(Bucket=BUCKET, Key="%sfact_allocations/date=%s/data.parquet" % (SILVER, day))["Body"].read()
    t = pq.read_table(io.BytesIO(body), columns=[key_col, value_col]).to_pydict()
    vals = [v for k, v in zip(t[key_col], t[value_col]) if k == account]
    need(len(vals) >= 1, "the probed account is not in the silver partition of %s" % day)
    return sum(float(v) for v in vals if v is not None)


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, n, accounts, dq, table_sha, overlap, module_sha, tracked, seam_truth):
    exp = {"firm", "source_label", "method_version", "value_column", "account_key_column", "accounts", "account_basis", "window", "rows", "by_day_quality",
           "private_parquet", "key_overlap", "seam", "unresolved_types", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed",
           "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and rec["source_label"] == LABEL and is_int(rec["method_version"]), "firm, source_label or method_version")
    need(nes(rec["value_column"]) and nes(rec["account_key_column"]) and nes(rec["account_basis"]), "column names and basis words")
    need(is_int(rec["accounts"]) and 1 <= rec["accounts"] <= 25 and rec["accounts"] == accounts, "accounts: record %s, table %s" % (rec["accounts"], accounts))
    w = rec["window"]
    need(isinstance(w, dict) and set(w) == {"first_date", "last_date"} and ISO.match(str(w["first_date"])) and ISO.match(str(w["last_date"])), "window form")
    need(rec["rows"] == n and rec["by_day_quality"] == dict(sorted(dq.items())) or rec["by_day_quality"] == dq, "rows or by_day_quality differ from the table")
    pp = rec["private_parquet"]
    need(isinstance(pp, dict) and set(pp) == {"path", "sha256", "rows"} and pp["sha256"] == table_sha and pp["rows"] == n
         and str(pp["path"]).replace("\\", "/").startswith(PRIVATE_ROOT), "private_parquet path, hash or rows")
    ko = rec["key_overlap"]
    need(isinstance(ko, dict) and set(ko) == {"frame_accounts", "derived_accounts", "overlap", "claim"} and ko["claim"] in CLAIMS, "key_overlap form")
    need(ko["derived_accounts"] == accounts and ko["overlap"] == overlap and overlap >= 1 and is_int(ko["frame_accounts"]) and ko["frame_accounts"] > 0,
         "key_overlap: record %s, recount overlap %s (must be at least 1)" % (ko, overlap))
    sm = rec["seam"]
    need(isinstance(sm, dict) and set(sm) == {"commonwealth_last_date", "bd_first_date", "bd_last_date", "first_derived_date", "link_base_exists", "words", "claim"}
         and sm["claim"] in CLAIMS, "seam form")
    for k in ("commonwealth_last_date", "bd_first_date", "bd_last_date"):
        need(sm[k] == seam_truth[k], "seam.%s: record %s, recount %s" % (k, sm[k], seam_truth[k]))
    need(sm["link_base_exists"] is seam_truth["link_base_exists"], "seam.link_base_exists differs from the recount")
    need(ISO.match(str(sm["first_derived_date"])) and sm["first_derived_date"] > sm["commonwealth_last_date"] or sm["first_derived_date"] >= sm["bd_first_date"],
         "seam.first_derived_date")
    need(nes(sm["words"]) and "2026-06-22" in sm["words"] and "2026-06-23" in sm["words"], "the seam words must name 2026-06-22 and 2026-06-23")
    need(isinstance(rec["unresolved_types"], dict) and all(nes(a) and is_int(b) and b >= 0 for a, b in rec["unresolved_types"].items()), "unresolved_types form")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == MODULE_REL and an.get("sha256") == module_sha and an.get("tracked") is True and tracked, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["claim"] in CLAIMS and rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False
         and rec["deployed"] is False, "claim or a flag")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def module_clauses(text):
    low = text.lower()
    need(not re.search(r"s3://opal-data-", low), "the adapter types a bucket")
    need(not [t for t in FOREIGN if t in low], "the adapter names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the adapter holds an S3 or DynamoDB write")
    need(LABEL.lower() in low, "the adapter must carry the label '%s'" % LABEL)
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB119-2-AC1":
        mp, tp = root / MODULE_REL, root / TEST_REL
        need(mp.is_file() and tp.is_file() and is_tracked(root, MODULE_REL) and is_tracked(root, TEST_REL), "adapter or tests missing or untracked")
        module_clauses(mp.read_text(encoding="utf-8"))
        text = tp.read_text(encoding="utf-8")
        names = set(re.findall(r"def (test_\w+)", text))
        need(len([x for x in names if x.startswith("test_refuses_")]) >= 3, "at least three test_refuses_* tests are required")
        for t in REQUIRED_TESTS:
            need(t in names, "the test file lacks the required test %s" % t)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(tp)], cwd=str(root),
                           capture_output=True, text=True, timeout=100)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= MIN_TESTS and "failed" not in r.stdout,
             "pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: %s tests pass including the unresolved-type and absent-value tests; the adapter carries the label, types no bucket, names no other firm, writes nothing" % m.group(1))
        return True
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    s3 = boto3.client("s3")
    rec = load(root, REC_REL)
    if cid == "DB119-2-AC2":
        pp = Path(str(rec["private_parquet"]["path"]))
        need(pp.is_file(), "no private derivation parquet")
        cc = [c["name"] for c in load(root, ACCOUNT_CONTRACT_REL)["columns"]]
        t = pq.read_table(str(pp)).to_pydict()
        n, accounts, dq = check_table(t, cc)
        frame = set(pq.read_table(FRAME, columns=["account_id"]).to_pydict()["account_id"])
        overlap = len(set(t["account_id"]) & frame)
        for a, d, v in pick_probes(t):
            ref = recompute_value(s3, rec["account_key_column"], rec["value_column"], a, d)
            need(abs(ref - v) <= 0.01, "the account value of a probed (account, date) differs from the silver: %.2f against %.2f" % (v, ref))
        mpth = root / MODULE_REL
        seam_truth = {"commonwealth_last_date": rec["seam"]["commonwealth_last_date"], "bd_first_date": rec["seam"]["bd_first_date"],
                      "bd_last_date": rec["seam"]["bd_last_date"], "link_base_exists": rec["seam"]["link_base_exists"]}
        check_record(rec, n, accounts, dq, sha_file(pp), overlap, sha_file(mpth), is_tracked(root, MODULE_REL), seam_truth)
        print("OK: %d rows for %d accounts (the Black Diamond key, %d in the household frame); the identity r = (V - F) / V0 - 1 holds on every MEASURED row; "
              "three probed account values equal the silver" % (n, accounts, overlap))
        return True
    if cid == "DB119-2-AC3":
        parts = silver_partitions(s3, "fact_allocations")
        need(parts, "no fact_allocations partition listed")
        cw_last = p118("p118_cottonwood.py").frontier_date(root)[0]
        sm = rec["seam"]
        truth = {"commonwealth_last_date": cw_last, "bd_first_date": parts[0], "bd_last_date": parts[-1], "link_base_exists": "2026-06-22" in set(parts)}
        for k, v in truth.items():
            need(sm[k] == v, "seam.%s: record %s, recount %s" % (k, sm[k], v))
        need(nes(sm["words"]) and "2026-06-22" in sm["words"] and "2026-06-23" in sm["words"], "the seam words must name 2026-06-22 and 2026-06-23")
        need(ISO.match(str(sm["first_derived_date"])) and sm["first_derived_date"] >= parts[0], "seam.first_derived_date")
        print("OK: seam recounted from the gold and the silver: Cottonwood account_return_daily ends %s; fact_allocations runs %s to %s (%d partitions); link base 2026-06-22 %s"
              % (cw_last, parts[0], parts[-1], len(parts), "exists" if truth["link_base_exists"] else "ABSENT"))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest(root):
    cols = ["firm", "account_id", "business_date", "market_value_eod", "external_flow", "total_return_daily", "day_quality"]

    def tbl(rows):
        return {c: [r[i] for r in rows] for i, c in enumerate(cols)}
    k1, k2 = "A0000000001", "B0000000002"
    good = [(FIRM, k1, "2026-06-23", 100.0, 0.0, None, "NOT_MEASURABLE"), (FIRM, k1, "2026-06-24", 110.0, 0.0, 0.10, "MEASURED"),
            (FIRM, k1, "2026-06-25", 165.0, 50.0, (165.0 - 50.0) / 110.0 - 1.0, "MEASURED"), (FIRM, k2, "2026-06-23", 50.0, 0.0, None, "NOT_MEASURABLE")]
    n, a, dq = check_table(tbl(good), cols)
    need((n, a) == (4, 2) and dq == {"NOT_MEASURABLE": 2, "MEASURED": 2}, "green table")
    need(len(pick_probes(tbl(good), 3)) == 3, "probes")

    def red(mut, why):
        rows = [list(r) for r in good]
        mut(rows)
        try:
            check_table(tbl([tuple(r) for r in rows]), cols)
        except Fail:
            return
        raise Fail("RED arm did not fail: " + why)
    red(lambda r: r[1].__setitem__(5, 0.11), "a return that breaks the identity")
    red(lambda r: r[0].__setitem__(5, 0.5), "a return on a row that is not MEASURED")
    red(lambda r: r[1].__setitem__(5, None), "a MEASURED row with no return")
    red(lambda r: r[0].__setitem__(1, "A000001"), "a short account key")
    red(lambda r: r[0].__setitem__(0, "other"), "another firm")
    red(lambda r: r.append(list(r[0])), "a duplicate (account, date)")
    red(lambda r: r[0].__setitem__(6, "MEASURED"), "a first row that claims MEASURED")
    red(lambda r: r[1].__setitem__(3, None), "a MEASURED row with no value")
    try:
        check_table({"x": [1]}, cols)
        raise Fail("RED: wrong columns must fail")
    except Fail as e:
        need("RED" not in str(e), str(e))
    module_clauses("LABEL = 'computed from Black Diamond values and flows'\nx = reader.get()\n")
    for bad, why in (("x = 1", "no label"), ("LABEL='computed from Black Diamond values and flows'\nb='s3://opal-data-cottonwood/'", "a typed bucket"),
                     ("LABEL='computed from Black Diamond values and flows'\nf='49financial'", "another firm"),
                     ("LABEL='computed from Black Diamond values and flows'\ns3.put_object()", "a write call")):
        try:
            module_clauses(bad)
            raise Fail("RED: module clause did not fail: " + why)
        except Fail as e:
            need("RED" not in str(e), str(e))
    seam = {"commonwealth_last_date": "2026-06-22", "bd_first_date": "2026-04-22", "bd_last_date": "2026-10-13", "link_base_exists": True}
    rec = {"firm": FIRM, "source_label": LABEL, "method_version": 3, "value_column": "Account Market Value", "account_key_column": "AccountID", "accounts": 2,
           "account_basis": "the lowest sha256", "window": {"first_date": "2026-06-22", "last_date": "2026-06-25"}, "rows": 4,
           "by_day_quality": {"MEASURED": 2, "NOT_MEASURABLE": 2}, "private_parquet": {"path": PRIVATE_ROOT + "a.parquet", "sha256": "ab" * 32, "rows": 4},
           "key_overlap": {"frame_accounts": 999, "derived_accounts": 2, "overlap": 2, "claim": "measured"},
           "seam": {"commonwealth_last_date": "2026-06-22", "bd_first_date": "2026-04-22", "bd_last_date": "2026-10-13", "first_derived_date": "2026-06-23",
                    "link_base_exists": True, "words": "Commonwealth to 2026-06-22, Black Diamond from 2026-06-23", "claim": "measured"},
           "unresolved_types": {}, "analysis": {"file": MODULE_REL, "sha256": "cd" * 32, "tracked": True},
           "reads": {"s3_reads": 5, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured",
           "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    need(check_record(rec, 4, 2, {"MEASURED": 2, "NOT_MEASURABLE": 2}, "ab" * 32, 2, "cd" * 32, True, seam), "record GREEN")
    for mut, why in ((lambda r: r["key_overlap"].update(overlap=0), "zero overlap"), (lambda r: r["seam"].update(words="no dates"), "seam words"),
                     (lambda r: r.update(source_label="x"), "label"), (lambda r: r["seam"].update(bd_first_date="2026-05-01"), "seam recount"),
                     (lambda r: r.update(pushed=True), "push flag"), (lambda r: r.update(account_basis="ids 1234567890"), "digit run"),
                     (lambda r: r.update(accounts=3), "accounts")):
        r2 = json.loads(json.dumps(rec))
        mut(r2)
        try:
            check_record(r2, 4, 2, {"MEASURED": 2, "NOT_MEASURABLE": 2}, "ab" * 32, 2 if why != "zero overlap" else 0, "cd" * 32, True, seam)
            raise Fail("RED: record clause did not fail: " + why)
        except Fail as e:
            need("RED" not in str(e), str(e))
    print("selftest OK: 1 green and 9 red table arms, 4 red module arms, 1 green and 7 red record arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p119_bdreturn.py <repo_root> <criterion_id>")
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
