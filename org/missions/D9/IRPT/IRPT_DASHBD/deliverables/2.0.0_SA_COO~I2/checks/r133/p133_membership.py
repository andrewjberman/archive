"""IRPT_DASHBD round 133, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the S60 membership read (cell DB-i-21).

CTO round-132 analysis (ruling 3, enrichment E2): the landed feed carries 39 accounts as ABSENT NO_START_DATE_AT_SOURCE while the
round-119 account-record read counted 40 roster accounts with a null accountStartDate. Which account moves between the two, by hashed
id? Is S60's account (the one the Scope groups miss; its sha256 is recorded in ACCOUNT_RECORD_READ_R119.json) in either set, and what
class does the feed give it? Counts and sha256 of the id string only; no id, no date, no value.

The worker reads (read-only): the landed silver's latest partition through the GET-only InflectionSilverReader (reason_class per
account), and the round-119 private roster response (a local file). It writes a PRIVATE extract and the repo record.

  DBI133-2-AC1  the record is complete and carries no identifier or date; the script is a tracked file hashed as recorded with no
                write, vendor-call or secret token, built on InflectionSilverReader; the extract's hash equals the recorded one; every
                count, both set differences (by sha256), S60's membership and class, and the verdict equal the checker's recompute from
                the extract; S60's sha256 equals the one in ACCOUNT_RECORD_READ_R119.json; no write, no push, no deploy.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import copy
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parents[8]
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~321/S60_MEMBERSHIP_R133.json"
R119_REL = D + "0.9.0_WK_IRPT_DASHBD~307/ACCOUNT_RECORD_READ_R119.json"
MAX_S3_READS = 400
NSD = "NO_START_DATE_AT_SOURCE"
CLASSES = {"NO_GROUP", "GROUP_NO_SERIES", "NO_START_DATE_AT_SOURCE", "SERIES_ENDED_AT_SOURCE", "UNMAPPED_ACCOUNT", "NO_FEED_ROW",
           "INCOMPLETE_WINDOW", "NO_EOD_VALUE", "RETURNED"}
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "delete_object", "delete_objects", "copy_object", "put_item", "update_item",
                "create_multipart_upload", "put_parameter", "invoke(", "start_execution")
VENDOR_TOKENS = ("requests.", "urllib.request", "http.client", "orionadvisor", "Authorization", "orion_session_jwt")
REC_KEYS = {"script", "extract", "silver_partitions", "feed_accounts", "roster_null_start", "feed_no_start_date", "a_minus_b_sha256",
            "a_minus_b_feed_class", "b_minus_a_sha256", "s60_account_sha256", "s60_in_roster_null_start", "s60_feed_class", "s60_in_difference",
            "verdict", "reads", "files_in_repo_private", "served_values_changed", "pushed", "deployed", "basis_words"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def recompute(extract, s60):
    """The extract: {'silver_partitions': int, 'accounts': {sha256: {'roster_null_start': bool, 'feed_class': word}}}."""
    acc = extract["accounts"]
    need(acc, "the extract holds no account")
    a = {h for h, v in acc.items() if v["roster_null_start"]}
    b = {h for h, v in acc.items() if v["feed_class"] == NSD}
    amb, bma = sorted(a - b), sorted(b - a)
    verdict = "NO_DIFFERENCE" if not amb and not bma else "DIFFERENCE_SHOWN"
    return {"silver_partitions": extract["silver_partitions"], "feed_accounts": len(acc), "roster_null_start": len(a), "feed_no_start_date": len(b),
            "a_minus_b_sha256": amb, "a_minus_b_feed_class": [acc[h]["feed_class"] for h in amb], "b_minus_a_sha256": bma,
            "s60_account_sha256": s60, "s60_in_roster_null_start": bool(acc.get(s60, {}).get("roster_null_start")),
            "s60_feed_class": acc[s60]["feed_class"] if s60 in acc else "NOT_IN_FEED", "s60_in_difference": s60 in set(amb) | set(bma),
            "verdict": verdict}


def no_identifiers(rec):
    """No run of 8 or more digits, except inside a sha256 value or a path / file field; no ISO date; no partition name."""
    rec = json.loads(json.dumps(rec))
    for outer, inner in (("extract", "path"), ("script", "file")):
        if isinstance(rec.get(outer), dict) and inner in rec[outer]:
            rec[outer][inner] = ""
    text = re.sub(r"[0-9a-f]{64}", "", json.dumps(rec))
    for m in re.finditer(r"\d{8,}", text):
        need(False, "a run of 8 or more digits in the record: %s" % m.group(0)[:3])
    need(re.search(r"\d{4}-\d{2}-\d{2}", text) is None, "a date is in the record")
    need("date=" not in text, "a partition name is in the record")


def script_clean(root, rel, want_sha):
    p = Path(root) / rel
    need(p.is_file(), "script %s is not a tracked file" % rel)
    b = p.read_bytes()
    need(sha(b) == want_sha, "script hash differs from the record")
    src = b.decode("ascii")
    for t in WRITE_TOKENS:
        need(t not in src, "script holds a write or invoke token: %s" % t)
    for t in VENDOR_TOKENS:
        need(t not in src, "script holds a vendor-call token: %s" % t)
    need("InflectionSilverReader" in src, "script must read the silver through InflectionSilverReader (GET-only, granted prefixes)")
    need("sha256" in src, "script must hash the ids (sha256) before anything is recorded")


def check(root, rec_rel=REC_REL):
    root = Path(root)
    rec = json.loads((root / rec_rel).read_bytes().decode("ascii"))
    need(set(rec) == REC_KEYS, "record keys differ from the whitelist: %s" % sorted(set(rec) ^ REC_KEYS))
    no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec["reads"]
    need(set(r) == {"s3_reads", "s3_writes", "dynamodb_writes", "vendor_calls", "secret_reads"}, "reads keys")
    for k in ("s3_writes", "dynamodb_writes", "vendor_calls", "secret_reads"):
        need(r[k] == 0, "reads.%s must be 0" % k)
    need(isinstance(r["s3_reads"], int) and 0 < r["s3_reads"] <= MAX_S3_READS, "reads.s3_reads must be 1..%d" % MAX_S3_READS)
    need(isinstance(rec["basis_words"], str) and len(rec["basis_words"]) >= 200, "basis_words (>= 200 characters) missing")
    script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    ex = rec["extract"]
    ep = Path(ex.get("path", ""))
    need(ep.is_file() and sha(ep.read_bytes()) == ex.get("sha256"), "the private extract is missing or its hash differs")
    extract = json.loads(ep.read_bytes().decode("utf-8"))
    for key in ("a_minus_b_sha256", "b_minus_a_sha256"):
        need(all(HEX64.match(h) for h in rec[key]), "%s must hold sha256 hex values only" % key)
    r119 = json.loads((root / R119_REL).read_bytes().decode("ascii"))
    s60 = r119["roles_sha256"]["missing_sha256"]
    need(rec["s60_account_sha256"] == s60, "s60_account_sha256 differs from the round-119 record's missing_sha256")
    want = recompute(extract, s60)
    for k, v in want.items():
        need(rec[k] == v, "%s: record %r recount %r" % (k, rec[k], v))
    need(all(c in CLASSES for c in rec["a_minus_b_feed_class"]) and rec["s60_feed_class"] in CLASSES | {"NOT_IN_FEED"}, "a class word outside the contract's set")


# ---- self-test ---------------------------------------------------------------------------------------------------------------
def build_good(td):
    accounts = {}
    for i in range(50):
        h = sha(("synthetic-account-%d" % i).encode())
        accounts[h] = {"roster_null_start": i < 5, "feed_class": NSD if 1 <= i < 5 else ("NO_GROUP" if i == 0 else "RETURNED")}
    s60 = sha(b"synthetic-account-0")                      # null start in the roster, classed NO_GROUP by the feed
    extract = {"silver_partitions": 1, "accounts": accounts}
    ex_path = Path(td) / "extract.json"
    ex_path.write_text(json.dumps(extract))
    live = Path(td) / "repo"
    (live / D / "0.9.0_WK_IRPT_DASHBD~321").mkdir(parents=True)
    (live / D / "0.9.0_WK_IRPT_DASHBD~307").mkdir(parents=True)
    (live / R119_REL).write_text(json.dumps({"roles_sha256": {"missing_sha256": s60}}))
    sp = live / D / "0.9.0_WK_IRPT_DASHBD~321" / "member_read.py"
    sp.write_bytes(b"import hashlib\nfrom inflection_account_dim import InflectionSilverReader\nreader = InflectionSilverReader()\nh = hashlib.sha256\n")
    rec = {"script": {"file": sp.relative_to(live).as_posix(), "sha256": sha(sp.read_bytes())},
           "extract": {"path": str(ex_path), "sha256": sha(ex_path.read_bytes())}, **recompute(extract, s60),
           "reads": {"s3_reads": 3, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
           "files_in_repo_private": False, "served_values_changed": False, "pushed": False, "deployed": False, "basis_words": "w" * 220}
    (live / REC_REL).write_text(json.dumps(rec))
    return live, rec, ex_path, extract, s60


def selftest(root):
    with tempfile.TemporaryDirectory() as td:
        live, rec, ex_path, extract, s60 = build_good(td)
        need(rec["verdict"] == "DIFFERENCE_SHOWN" and rec["s60_in_difference"] and rec["roster_null_start"] == 5 and rec["feed_no_start_date"] == 4,
             "selftest world drifted: %r" % {k: rec[k] for k in ("verdict", "roster_null_start", "feed_no_start_date")})
        sp_rel = rec["script"]["file"]
        good_script = (live / sp_rel).read_bytes()

        def trial(label, mutate=None, extract_mutate=None, script_bytes=None, r119=None, expect_fail=True):
            r = copy.deepcopy(rec)
            if mutate:
                mutate(r)
            if extract_mutate:
                e = copy.deepcopy(extract)
                extract_mutate(e)
                ex_path.write_text(json.dumps(e))
                r["extract"]["sha256"] = sha(ex_path.read_bytes())
            if script_bytes is not None:
                (live / sp_rel).write_bytes(script_bytes)
                r["script"]["sha256"] = sha(script_bytes)
            if r119 is not None:
                (live / R119_REL).write_text(json.dumps(r119))
            (live / REC_REL).write_text(json.dumps(r))
            try:
                check(live)
                got_fail, why = False, ""
            except Fail as exc:
                got_fail, why = True, str(exc)[:60]
            finally:
                ex_path.write_text(json.dumps(extract))
                (live / sp_rel).write_bytes(good_script)
                (live / R119_REL).write_text(json.dumps({"roles_sha256": {"missing_sha256": s60}}))
            need(got_fail == expect_fail, "selftest %s: expected %s" % (label, "FAIL" if expect_fail else "PASS"))
            print("selftest %-34s -> %s" % (label, ("FAIL (%s)" % why) if got_fail else "PASS"))

        trial("GOOD", expect_fail=False)
        trial("wrong roster null count", lambda r: r.update(roster_null_start=r["roster_null_start"] + 1))
        trial("wrong feed NSD count", lambda r: r.update(feed_no_start_date=r["feed_no_start_date"] - 1))
        trial("a_minus_b emptied", lambda r: r.update(a_minus_b_sha256=[], a_minus_b_feed_class=[]))
        trial("s60 membership flipped", lambda r: r.update(s60_in_roster_null_start=False))
        trial("s60 class changed", lambda r: r.update(s60_feed_class="GROUP_NO_SERIES"))
        trial("verdict NO_DIFFERENCE", lambda r: r.update(verdict="NO_DIFFERENCE"))
        trial("s60 hash not the R119 one", r119={"roles_sha256": {"missing_sha256": sha(b"another")}})
        trial("an id-like run in the record", lambda r: r.update(basis_words=r["basis_words"] + " 123456789"))
        trial("a date in the record", lambda r: r.update(basis_words=r["basis_words"] + " 2026-10-16"))
        trial("s3 write read as zero", lambda r: r["reads"].update(s3_writes=1))
        trial("extract changed after the record", extract_mutate=lambda e: e["accounts"][s60].update(feed_class="RETURNED"))
        trial("script with an Authorization", script_bytes=good_script + b"h = 'Authorization'\n")
        trial("script without sha256", script_bytes=b"from inflection_account_dim import InflectionSilverReader\n")
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        try:
            selftest(argv[2] if len(argv) > 2 else ROOT_DEFAULT)
        except Fail as exc:
            print("REASON: %s" % exc)
            print("selftest FAIL")
            return 1
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        need(cid == "DBI133-2-AC1", "unknown criterion %s" % cid)
        check(root)
    except FileNotFoundError as exc:
        print("REASON: no such file: %s" % Path(str(exc.filename)).name)
        print("%s FAIL" % cid)
        return 1
    except Fail as exc:
        print("REASON: %s" % exc)
        print("%s FAIL" % cid)
        return 1
    except Exception as exc:  # a crash is a FAIL with its type named, never a pass
        print("REASON: %s: %s" % (type(exc).__name__, str(exc)[:300]))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
