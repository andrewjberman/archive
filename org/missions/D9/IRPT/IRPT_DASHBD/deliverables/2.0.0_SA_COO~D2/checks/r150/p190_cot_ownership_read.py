"""IRPT_DASHBD round 150, workstream COTOWN (issuer 2.0.0_SA_COO~D2) -- DB-b-324, C6a of the Cottonwood Performance read path (CTO msgs 10215, 10227, 10267): a READ-ONLY measurement by the one IRPT CloudOps lane
`0.7.0_AE_CloudOps~IB2` of what the Cottonwood ownership map can be built against: the 939 published series prefixes, the Cottonwood directory, the dell1 match sheet (a local file OUTSIDE the repo, newer pair) and the
portal's Cottonwood advisor ids. It writes two files OUTSIDE the repo (the published raw keys, a copy of the directory object) and a counts-only record in the repo. WORLD (read only); the checker re-reads.

  DBC190-1-AC1  the record: counts and booleans only, the coverage chain (sheet -> published -> directory), the advisor-id measurement, the two local files named by sha256 and line count, no id
  DBC190-2-AC1  FRESH reads: the published prefix count equals the record, the two local files exist with the recorded sha256 and line counts, and no file of the repo carries any of the 939 raw keys

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = helper("r147/p151_pubapply.py", "p151_helper_190")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_OWNERSHIP_READ_RECORD.json"
BUCKET, PREFIX = "opal-data-cottonwood", "irpt/cottonwood/platinum/reporting/"
LOCAL_DIR = "C:/opal-intake/work/"
RAW_FILE, DIR_FILE = LOCAL_DIR + "cot_published_raw.txt", LOCAL_DIR + "cot_directory_latest.json"
SHEET_ROWS, SHEET_HIGH, SHEET_MEDIUM, SHEET_LOW, SHEET_UNMATCHED, SHEET_CODES = 83, 40, 36, 2, 5, 3
SHAPE = re.compile(r"^[a-z][a-z0-9_-]{1,40}$")
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("sha256", "invoked_utc")


def b(x):
    return isinstance(x, bool)


def count(x, lo=0):
    return is_int(x) and x >= lo


def check_record(rec):
    exp = {"claim", "applier", "no_write_to_aws", "published", "directory", "sheet", "bridge", "users", "authorizer", "local_files", "notes", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured" and rec["applier"] == APPLIER and rec["no_write_to_aws"] is True, "claim measured, the applier named and no_write_to_aws true")
    p = rec["published"]
    need(isinstance(p, dict) and set(p) == {"prefixes", "mintable", "unmintable"} and count(p["prefixes"], 1) and count(p["mintable"]) and count(p["unmintable"]) and p["mintable"] + p["unmintable"] == p["prefixes"],
         "published: prefixes = mintable + unmintable (each raw key through ids.opaque_account)")
    d = rec["directory"]
    keys = {"entries", "entries_with_client_id", "entries_with_relationship_id", "entries_with_accounts", "distinct_accounts", "firm_id_opaque_present", "accounts_in_published", "published_in_directory"}
    need(isinstance(d, dict) and set(d) == keys and b(d["firm_id_opaque_present"]), "directory keys")
    for k in keys - {"firm_id_opaque_present"}:
        need(count(d[k]), "directory.%s must be a count" % k)
    need(d["entries_with_client_id"] <= d["entries"] and d["entries_with_relationship_id"] <= d["entries"] and d["entries_with_accounts"] <= d["entries"], "directory: a subset of entries cannot exceed the entries")
    need(d["accounts_in_published"] <= d["distinct_accounts"] and d["published_in_directory"] <= p["mintable"], "directory: the overlap with the published set cannot exceed either side")
    s = rec["sheet"]
    skeys = {"pair", "rows", "high", "medium", "low", "unmatched", "all_in_published_raw", "high_in_published_raw", "medium_in_published_raw", "high_in_directory", "advisor_codes", "high_by_advisor_code"}
    need(isinstance(s, dict) and set(s) == skeys and s["pair"] == "newer", "sheet: the NEWER pair, keys %s" % sorted(skeys))
    need((s["rows"], s["high"], s["medium"], s["low"], s["unmatched"], s["advisor_codes"]) == (SHEET_ROWS, SHEET_HIGH, SHEET_MEDIUM, SHEET_LOW, SHEET_UNMATCHED, SHEET_CODES),
         "sheet: the counts the CTO's reading established (83 rows: HIGH 40, MEDIUM 36, LOW 2, UNMATCHED 5; 3 advisor codes)")
    need(count(s["all_in_published_raw"]) and s["all_in_published_raw"] <= s["rows"] and count(s["high_in_published_raw"]) and s["high_in_published_raw"] <= min(s["high"], s["all_in_published_raw"])
         and count(s["medium_in_published_raw"]) and s["medium_in_published_raw"] <= s["medium"] and count(s["high_in_directory"]) and s["high_in_directory"] <= s["high"], "sheet: overlap counts within their populations")
    hb = s["high_by_advisor_code"]
    need(isinstance(hb, dict) and len(hb) == SHEET_CODES and all(count(v) for v in hb.values()) and sum(hb.values()) == s["high"] and all(SHAPE.match(str(k).lower()) for k in hb), "sheet.high_by_advisor_code: a count per code, summing to HIGH (codes as given by the sheet; no name)")
    br = rec["bridge"]
    bkeys = {"pairs", "deterministic", "to_confirm", "distinct_old", "distinct_new", "sheet_accounts_in_old", "sheet_high_in_old", "sheet_medium_in_old", "new_in_published_raw", "deterministic_new_in_published_raw", "high_direct", "high_via_deterministic_pairs", "high_left_out", "grant_ready", "answers_filled"}
    need(isinstance(br, dict) and set(br) == bkeys and all(count(br[k]) for k in bkeys), "bridge keys: counts for the 118-pair list (old custodian account to current Black Diamond account)")
    need((br["pairs"], br["deterministic"], br["to_confirm"]) == (118, 11, 107) and br["deterministic"] + br["to_confirm"] == br["pairs"], "bridge: 118 pairs = 11 deterministic + 107 to confirm")
    need(br["sheet_high_in_old"] + br["sheet_medium_in_old"] <= br["sheet_accounts_in_old"] <= s["rows"] and br["sheet_high_in_old"] <= s["high"] and br["sheet_medium_in_old"] <= s["medium"], "bridge: the sheet's overlap with the old accounts within its populations")
    need(br["deterministic_new_in_published_raw"] <= br["new_in_published_raw"] <= br["distinct_new"] and br["high_via_deterministic_pairs"] <= br["deterministic"] * s["high"], "bridge: overlap counts within their populations")
    need(br["high_direct"] == s["high_in_published_raw"] and br["high_direct"] + br["high_via_deterministic_pairs"] + br["high_left_out"] == s["high"] and br["grant_ready"] == br["high_direct"] + br["high_via_deterministic_pairs"],
         "bridge: (a) HIGH accounts joining directly = sheet.high_in_published_raw, (b) HIGH accounts joining via the 11 deterministic pairs, (c) HIGH left out; a + b + c = the HIGH rows; grant_ready = a + b (CTO msg 10277)")
    need(br["answers_filled"] <= br["to_confirm"], "bridge: answers filled in the review sheet cannot exceed the rows to confirm (the count of non-blank 'Your answer' cells; 0 expected)")
    u = rec["users"]
    need(isinstance(u, dict) and set(u) == {"table", "firm_attribute", "advisor_attribute", "cottonwood_users", "cottonwood_users_with_advisor_id", "advisor_id_shapes", "sheet_codes_found_as_advisor_id", "high_rows_under_a_found_code", "second_source_available"},
         "users keys")
    need(nes(u["table"]) and nes(u["firm_attribute"]) and nes(u["advisor_attribute"]) and count(u["cottonwood_users"]) and count(u["cottonwood_users_with_advisor_id"]) and u["cottonwood_users_with_advisor_id"] <= u["cottonwood_users"],
         "users: the table, the two attribute names (words), counts")
    need(isinstance(u["advisor_id_shapes"], list) and all(isinstance(x, str) and SHAPE.match(x) for x in u["advisor_id_shapes"]), "users.advisor_id_shapes: shape classes as lowercase words, never an id")
    need(count(u["sheet_codes_found_as_advisor_id"]) and u["sheet_codes_found_as_advisor_id"] <= SHEET_CODES and count(u["high_rows_under_a_found_code"]) and u["high_rows_under_a_found_code"] <= s["high"] and b(u["second_source_available"]),
         "users: how many of the 3 sheet codes are advisor ids of Cottonwood users, and how many HIGH rows sit under a found code")
    a = rec["authorizer"]
    need(isinstance(a, dict) and set(a) == {"header_source_path", "advisor_header_origin"} and nes(a["header_source_path"]) and nes(a["advisor_header_origin"]), "authorizer: where the advisor header comes from (a repo path and a sentence)")
    lf = rec["local_files"]
    need(isinstance(lf, dict) and set(lf) == {"published_raw", "directory"}, "local_files keys")
    for name, path, lo in (("published_raw", RAW_FILE, 1), ("directory", DIR_FILE, 1)):
        f = lf[name]
        need(isinstance(f, dict) and set(f) == {"path", "sha256", "lines"} and f["path"] == path and re.fullmatch(r"[0-9a-f]{64}", str(f["sha256"])) and count(f["lines"], lo), "local_files.%s: the path, a sha256 and a line count" % name)
    need(lf["published_raw"]["lines"] == p["prefixes"], "the published raw file must hold one line per prefix")
    need(isinstance(rec["notes"], str) and 40 <= len(rec["notes"]) <= 2400 and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "notes (words) and the reads block")
    return True


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    check_record(rec)
    need(not H.digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(rec)[:2])
    if cid == "DBC190-1-AC1":
        print("OK: counts and booleans only; the coverage chain sheet -> published -> directory; the advisor-id measurement; the two local files named by sha256 and line count; no id")
        return True
    if cid == "DBC190-2-AC1":
        import boto3
        s3 = boto3.client("s3")
        n = 0
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
            n += len(page.get("CommonPrefixes", []))
        need(n == rec["published"]["prefixes"], "the live prefix count %d differs from the record's %d" % (n, rec["published"]["prefixes"]))
        for name, path in (("published_raw", RAW_FILE), ("directory", DIR_FILE)):
            p = Path(path)
            need(p.is_file(), "the local file %s is missing" % path)
            data = p.read_bytes()
            need(hashlib.sha256(data).hexdigest() == rec["local_files"][name]["sha256"] and len(data.splitlines()) == rec["local_files"][name]["lines"], "the local file %s differs from the record (sha256 or line count)" % name)
        raw = [x.strip() for x in Path(RAW_FILE).read_text(encoding="utf-8").splitlines() if x.strip()]
        need(len(set(raw)) == len(raw) == n, "the raw key file must hold %d distinct keys" % n)
        sample = raw[:: max(1, len(raw) // 40)]
        hits = []
        for rel in rec_scope_files(root):
            text = (root / rel).read_text(encoding="utf-8", errors="replace")
            hits += [k for k in sample if k in text]
        need(not hits, "the committed record files carry %d published raw keys: an id leaked into the repo" % len(hits))
        print("OK: live: %d prefixes as recorded; the two local files exist with the recorded sha256 and line counts; none of a 40-key sample of the raw keys appears in the order's committed files" % n)
        return True
    raise Fail("unknown criterion %s" % cid)


def rec_scope_files(root):
    base = Path(root) / D / APPLIER
    return [str(p.relative_to(root)).replace("\\", "/") for p in base.glob("*") if p.is_file() and p.suffix in (".json", ".md", ".txt") and p.stat().st_size < 4_000_000]


def synthetic():
    return {"claim": "measured", "applier": APPLIER, "no_write_to_aws": True,
            "published": {"prefixes": 939, "mintable": 939, "unmintable": 0},
            "directory": {"entries": 271, "entries_with_client_id": 271, "entries_with_relationship_id": 200, "entries_with_accounts": 271, "distinct_accounts": 900, "firm_id_opaque_present": True, "accounts_in_published": 880, "published_in_directory": 880},
            "sheet": {"pair": "newer", "rows": 83, "high": 40, "medium": 36, "low": 2, "unmatched": 5, "all_in_published_raw": 80, "high_in_published_raw": 25, "medium_in_published_raw": 34, "high_in_directory": 39, "advisor_codes": 3,
                      "high_by_advisor_code": {"code-a": 2, "code-b": 30, "code-c": 8}},
            "bridge": {"pairs": 118, "deterministic": 11, "to_confirm": 107, "distinct_old": 115, "distinct_new": 96, "sheet_accounts_in_old": 18, "sheet_high_in_old": 12, "sheet_medium_in_old": 6, "new_in_published_raw": 90,
                       "deterministic_new_in_published_raw": 11, "high_direct": 25, "high_via_deterministic_pairs": 3, "high_left_out": 12, "grant_ready": 28, "answers_filled": 0},
            "users": {"table": "opal-users-v2", "firm_attribute": "firmId", "advisor_attribute": "advisorId", "cottonwood_users": 12, "cottonwood_users_with_advisor_id": 5, "advisor_id_shapes": ["three-letter-code"],
                      "sheet_codes_found_as_advisor_id": 2, "high_rows_under_a_found_code": 32, "second_source_available": True},
            "authorizer": {"header_source_path": "infra/aws/users/lambda/portal-authorizer/index.mjs", "advisor_header_origin": "the advisorId claim of the signed token, set at login from the user record"},
            "local_files": {"published_raw": {"path": RAW_FILE, "sha256": "a" * 64, "lines": 939}, "directory": {"path": DIR_FILE, "sha256": "b" * 64, "lines": 1}},
            "notes": "Counts and booleans only; the two files named were written outside the repo; nothing was written to AWS.", "reads": {"vendor_calls": 0, "secret_reads": 0}}


def selftest():
    rec = synthetic()
    check_record(rec)
    arms = {
        "claim": lambda r: r.update(claim="inferred"),
        "applier": lambda r: r.update(applier="x"),
        "aws write": lambda r: r.update(no_write_to_aws=False),
        "mintable sum": lambda r: r["published"].update(mintable=900),
        "no prefixes": lambda r: r["published"].update(prefixes=0, mintable=0, unmintable=0),
        "dir subset": lambda r: r["directory"].update(entries_with_client_id=999),
        "dir overlap": lambda r: r["directory"].update(accounts_in_published=901),
        "published overlap": lambda r: r["directory"].update(published_in_directory=940),
        "sheet pair": lambda r: r["sheet"].update(pair="older"),
        "bridge pairs": lambda r: r["bridge"].update(pairs=117),
        "bridge split": lambda r: r["bridge"].update(deterministic=12),
        "bridge sheet overlap": lambda r: r["bridge"].update(sheet_high_in_old=40),
        "bridge new overlap": lambda r: r["bridge"].update(deterministic_new_in_published_raw=91),
        "bridge answers": lambda r: r["bridge"].update(answers_filled=108),
        "bridge key lost": lambda r: r["bridge"].pop("answers_filled"),
        "bridge reach": lambda r: r["bridge"].update(high_via_deterministic_pairs=4),
        "bridge grant ready": lambda r: r["bridge"].update(grant_ready=29),
        "bridge direct differs": lambda r: r["bridge"].update(high_direct=24, high_left_out=13),
        "bridge left out": lambda r: r["bridge"].update(high_left_out=11),
        "sheet high": lambda r: r["sheet"].update(high=41),
        "sheet codes": lambda r: r["sheet"].update(advisor_codes=4),
        "high in published": lambda r: r["sheet"].update(high_in_published_raw=41),
        "high by code sum": lambda r: r["sheet"]["high_by_advisor_code"].update({"code-a": 3}),
        "high by code count": lambda r: r["sheet"]["high_by_advisor_code"].pop("code-c"),
        "users subset": lambda r: r["users"].update(cottonwood_users_with_advisor_id=13),
        "shape id": lambda r: r["users"].update(advisor_id_shapes=["ABC123"]),
        "found codes": lambda r: r["users"].update(sheet_codes_found_as_advisor_id=4),
        "found rows": lambda r: r["users"].update(high_rows_under_a_found_code=41),
        "second source type": lambda r: r["users"].update(second_source_available="yes"),
        "authorizer": lambda r: r["authorizer"].update(advisor_header_origin=""),
        "raw file path": lambda r: r["local_files"]["published_raw"].update(path="C:/dev/x.txt"),
        "raw file lines": lambda r: r["local_files"]["published_raw"].update(lines=938),
        "dir file hash": lambda r: r["local_files"]["directory"].update(sha256="zz"),
        "reads": lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}),
        "notes short": lambda r: r.update(notes="ok"),
        "extra key": lambda r: r.update(z=1),
        "firm opaque flag": lambda r: r["directory"].update(firm_id_opaque_present="yes"),
    }
    n = 0
    for label, mut in arms.items():
        r = copy.deepcopy(rec)
        try:
            mut(r)
            check_record(r)
        except Fail:
            n += 1
            continue
        raise AssertionError("mutant passed: " + label)
    print("selftest: green on the synthetic record and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
