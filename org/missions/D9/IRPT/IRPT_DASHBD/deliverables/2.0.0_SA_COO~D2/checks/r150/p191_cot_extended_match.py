"""IRPT_DASHBD round 150, workstream COTMATCH (issuer 2.0.0_SA_COO~D2) -- DB-b-325, C6d of the Cottonwood read path (Andrew-direct ruling a3ed via CTO msg 10288, rules msgs 10267, 10277): the EXTENDED MATCH. A worker reads the
Cottonwood CRM extract `Files.zip` (client data, ON THIS BOX, OUTSIDE the repo, never extracted into the repo) and writes a match table OUTSIDE the repo: for each of the 939 published Cottonwood accounts, the CRM household (and the
advisor field the CRM carries, if any) it links to, with the METHOD and a CONFIDENCE. Only HIGH with a certain join grants access (CTO rule). The repo receives a counts-only record and the worker's own matcher script (no data in it).
Claim label: "inferred", never measured. The checker re-runs the worker's script on the same inputs and compares the output hash (reproducibility), and re-reads the record for leaks.

  DBC191-1-AC1  the record: methods with their rules and counts, the confidence totals summing to the 939, the join counts reconciling with the sheet and the bridge, outputs named by sha256 and line count, no id
  DBC191-2-AC1  REPRODUCIBILITY: the script, re-run by the checker on the same inputs, writes a match table with the recorded sha256; and no published raw key appears in any committed file of the worker's folder

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = helper("r147/p151_pubapply.py", "p151_helper_191")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-325.cottonwood-extended-match-over-the-crm-extract.md"
LOCAL = "C:/opal-intake/work/"
ZIP = "C:/opal-intake/inbound/cottonwood-crm-files-zip/Files.zip"
RAW, DIRF = LOCAL + "cot_published_raw.txt", LOCAL + "cot_directory_latest.json"
SHEET = "C:/opal-intake/inbound/cottonwood-match/20261016T0225Z_cottonwood_account_household_match (1).csv"
PAIRS = "C:/opal-intake/inbound/cottonwood-match/dell1_desktop_20261017/Cottonwood_match_list_118_pairs.csv"
OUT = LOCAL + "cot_extended_match.csv"
CLAIM = "inferred from the CRM extract Files.zip (sha256 c66bae52) and the dell1 match sheet 20261016T0225Z (1)"
CONF = ("HIGH", "MEDIUM", "LOW", "UNMATCHED")
WORD = re.compile(r"^[a-z][a-z0-9_ -]{1,60}$")
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("sha256", "output_sha256", "script_sha256")


def count(x, lo=0):
    return is_int(x) and x >= lo


def check_record(rec):
    exp = {"claim", "worker", "inputs", "crm", "methods", "result", "join", "outputs", "script", "notes", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == CLAIM, "the claim label must read exactly: %s" % CLAIM)
    need(nes(rec["worker"]), "the worker named")
    i = rec["inputs"]
    need(isinstance(i, dict) and set(i) == {"files_zip_sha256_prefix", "published_raw_lines", "directory_entries", "sheet_rows", "pairs_rows"} and i["files_zip_sha256_prefix"] == "c66bae52"
         and i["published_raw_lines"] == 939 and count(i["directory_entries"], 1) and i["sheet_rows"] == 83 and i["pairs_rows"] == 118, "inputs: the zip prefix, 939 published keys, the directory, 83 sheet rows, 118 pairs")
    c = rec["crm"]
    need(isinstance(c, dict) and set(c) == {"tables", "household_id_spaces", "advisor_field_found", "advisor_field", "text_sources"}, "crm keys")
    need(isinstance(c["tables"], list) and len(c["tables"]) >= 3 and all(isinstance(x, str) and WORD.match(x) for x in c["tables"]), "crm.tables: table kinds as lowercase words, never a client-specific name")
    need(count(c["household_id_spaces"], 1) and isinstance(c["advisor_field_found"], bool), "crm: id spaces (a count) and whether an advisor field exists")
    need((c["advisor_field"] is None) == (not c["advisor_field_found"]) and (c["advisor_field"] is None or (isinstance(c["advisor_field"], dict) and set(c["advisor_field"]) == {"table", "column"} and nes(c["advisor_field"]["table"]) and nes(c["advisor_field"]["column"]))),
         "crm.advisor_field: {table, column} NAMES when found, else null")
    need(isinstance(c["text_sources"], list) and all(isinstance(x, str) and WORD.match(x) for x in c["text_sources"]), "crm.text_sources: kinds as lowercase words")
    ms = rec["methods"]
    need(isinstance(ms, list) and len(ms) >= 1, "methods: at least one")
    ids = set()
    for m in ms:
        need(isinstance(m, dict) and set(m) == {"id", "rule", "grants_access", "accounts_linked"} and re.fullmatch(r"M[A-Z0-9]{1,3}", str(m["id"])) and m["id"] not in ids and nes(m["rule"]) and len(m["rule"]) <= 400
             and isinstance(m["grants_access"], bool) and count(m["accounts_linked"]), "method keys: an id, a rule in words, grants_access, a count")
        ids.add(m["id"])
        need(not (m["grants_access"] and not re.search(r"certain|exact|deterministic|two independent|filed under (one|a single)", m["rule"], re.I)), "method %s grants access: its rule must say why the link is certain (exact, deterministic, two independent sources, or filed under one household)" % m["id"])
    r = rec["result"]
    need(isinstance(r, dict) and set(r) == {"published", "high", "medium", "low", "unmatched", "conflicts"} and r["published"] == 939 and all(count(r[k]) for k in ("high", "medium", "low", "unmatched", "conflicts"))
         and r["high"] + r["medium"] + r["low"] + r["unmatched"] == 939, "result: published 939 = HIGH + MEDIUM + LOW + UNMATCHED; conflicts counted")
    need(r["conflicts"] <= r["published"], "result.conflicts within the published")
    j = rec["join"]
    need(isinstance(j, dict) and set(j) == {"sheet_high_direct", "sheet_high_via_deterministic_pairs", "extended_high", "grant_ready_total", "left_out", "high_without_advisor"} and all(count(j[k]) for k in j),
         "join keys: counts")
    need(j["grant_ready_total"] == j["sheet_high_direct"] + j["sheet_high_via_deterministic_pairs"] + j["extended_high"] and j["grant_ready_total"] + j["left_out"] == 939,
         "join: grant_ready_total = sheet direct + sheet via pairs + extended HIGH, and grant_ready + left_out = 939 (CTO msg 10277: HIGH plus a certain join)")
    need(j["extended_high"] <= r["high"] and j["high_without_advisor"] <= j["grant_ready_total"], "join: extended HIGH within HIGH; high_without_advisor within grant_ready")
    o = rec["outputs"]
    need(isinstance(o, dict) and set(o) == {"match_table"} and isinstance(o["match_table"], dict) and set(o["match_table"]) == {"path", "output_sha256", "lines"} and o["match_table"]["path"] == OUT
         and re.fullmatch(r"[0-9a-f]{64}", str(o["match_table"]["output_sha256"])) and o["match_table"]["lines"] == 940, "outputs: the match table path, sha256, 940 lines (header + 939)")
    s = rec["script"]
    need(isinstance(s, dict) and set(s) == {"path", "script_sha256", "reproducible"} and nes(s["path"]) and s["path"].endswith(".py") and re.fullmatch(r"[0-9a-f]{64}", str(s["script_sha256"])) and s["reproducible"] is True,
         "script: a repo path, its sha256, reproducible true (two runs of the script wrote the same hash)")
    need(isinstance(rec["notes"], str) and 60 <= len(rec["notes"]) <= 3000 and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0, "extracted_to_repo": False}, "notes (words), and the reads block incl. extracted_to_repo false")
    return True


def run(root, cid):
    root = Path(root)
    serial = re.search(r"<issued_to>([^<]+)</issued_to>", (root / ORDER_REL).read_text(encoding="utf-8")).group(1).strip()
    rec = H.load(root, D + serial + "/COT_EXTENDED_MATCH_RECORD.json")
    check_record(rec)
    need(not H.digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(rec)[:2])
    if cid == "DBC191-1-AC1":
        print("OK: methods with their rules and counts, confidence totals summing to the 939, the join reconciling (sheet direct + via pairs + extended HIGH = grant ready), outputs named by sha256 and line count, no id")
        return True
    if cid == "DBC191-2-AC1":
        sp = root / rec["script"]["path"]
        need(sp.is_file() and hashlib.sha256(sp.read_bytes()).hexdigest() == rec["script"]["script_sha256"], "the script differs from the record's sha256")
        out = Path(OUT)
        need(out.is_file() and hashlib.sha256(out.read_bytes()).hexdigest() == rec["outputs"]["match_table"]["output_sha256"] and len(out.read_bytes().splitlines()) == 940, "the match table differs from the record")
        with tempfile.TemporaryDirectory() as td:
            tmp = str(Path(td) / "again.csv")
            r = subprocess.run([sys.executable, "-I", str(sp), "--zip", ZIP, "--raw", RAW, "--dir", DIRF, "--sheet", SHEET, "--pairs", PAIRS, "--out", tmp], capture_output=True, text=True, timeout=3600)
            need(r.returncode == 0 and Path(tmp).is_file(), "the script failed on a re-run (rc %s): %s" % (r.returncode, r.stderr[-200:].replace("\n", " | ")))
            need(hashlib.sha256(Path(tmp).read_bytes()).hexdigest() == rec["outputs"]["match_table"]["output_sha256"], "the re-run wrote a different match table: the script is not reproducible")
        raw = [x.strip() for x in Path(RAW).read_text(encoding="utf-8").splitlines() if x.strip()]
        sample = raw[:: max(1, len(raw) // 60)]
        hits = 0
        for p in (root / D / serial).rglob("*"):
            if p.is_file() and p.stat().st_size < 4_000_000 and p.suffix in (".json", ".md", ".txt", ".py", ".csv"):
                t = p.read_text(encoding="utf-8", errors="replace")
                hits += sum(1 for k in sample if k in t)
        need(hits == 0, "the worker's committed files carry %d published raw keys: an id leaked into the repo" % hits)
        print("OK: the script re-run by the checker wrote the recorded match table hash, and no sampled published key appears in the worker's committed files")
        return True
    raise Fail("unknown criterion %s" % cid)


def synthetic():
    return {"claim": CLAIM, "worker": "0.9.0_WK_IRPT_DASHBD~999",
            "inputs": {"files_zip_sha256_prefix": "c66bae52", "published_raw_lines": 939, "directory_entries": 271, "sheet_rows": 83, "pairs_rows": 118},
            "crm": {"tables": ["contacts", "activities", "crmhouseholds", "manualinsurance", "connections"], "household_id_spaces": 2, "advisor_field_found": True, "advisor_field": {"table": "crmhouseholds", "column": "advisor"}, "text_sources": ["activity notes"]},
            "methods": [{"id": "MA", "rule": "an exact account number cited in activity notes filed under one household at least twice and under no other", "grants_access": True, "accounts_linked": 300},
                        {"id": "MN", "rule": "a name match of the account holder to one contact", "grants_access": False, "accounts_linked": 400}],
            "result": {"published": 939, "high": 330, "medium": 400, "low": 9, "unmatched": 200, "conflicts": 4},
            "join": {"sheet_high_direct": 25, "sheet_high_via_deterministic_pairs": 3, "extended_high": 300, "grant_ready_total": 328, "left_out": 611, "high_without_advisor": 10},
            "outputs": {"match_table": {"path": OUT, "output_sha256": "a" * 64, "lines": 940}},
            "script": {"path": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~999/cot_extended_match.py", "script_sha256": "b" * 64, "reproducible": True},
            "notes": "Counts and words only; the extract was read in memory from the zip and nothing was extracted to the repo; the match table is outside the repo.", "reads": {"vendor_calls": 0, "secret_reads": 0, "extracted_to_repo": False}}


def selftest():
    rec = synthetic()
    check_record(rec)
    arms = {
        "claim": lambda r: r.update(claim="measured"),
        "zip prefix": lambda r: r["inputs"].update(files_zip_sha256_prefix="deadbeef"),
        "published": lambda r: r["inputs"].update(published_raw_lines=938),
        "tables few": lambda r: r["crm"].update(tables=["contacts"]),
        "tables client name": lambda r: r["crm"].update(tables=["contacts", "activities", "Smith Family"]),
        "advisor found without field": lambda r: r["crm"].update(advisor_field=None),
        "advisor field when not found": lambda r: r["crm"].update(advisor_field_found=False),
        "advisor field keys": lambda r: r["crm"]["advisor_field"].pop("column"),
        "method id": lambda r: r["methods"][0].update(id="alpha"),
        "method duplicate": lambda r: r["methods"][1].update(id="MA"),
        "grant without certainty": lambda r: r["methods"][1].update(grants_access=True),
        "method rule long": lambda r: r["methods"][0].update(rule="x" * 401),
        "confidence sum": lambda r: r["result"].update(unmatched=201),
        "published result": lambda r: r["result"].update(published=938),
        "conflicts": lambda r: r["result"].update(conflicts=940),
        "grant ready sum": lambda r: r["join"].update(grant_ready_total=329),
        "left out": lambda r: r["join"].update(left_out=610),
        "extended high": lambda r: r["join"].update(extended_high=331, grant_ready_total=359, left_out=580),
        "no advisor count": lambda r: r["join"].update(high_without_advisor=999),
        "output path": lambda r: r["outputs"]["match_table"].update(path="C:/dev/x.csv"),
        "output lines": lambda r: r["outputs"]["match_table"].update(lines=939),
        "output hash": lambda r: r["outputs"]["match_table"].update(output_sha256="zz"),
        "script path": lambda r: r["script"].update(path="x.txt"),
        "reproducible": lambda r: r["script"].update(reproducible=False),
        "extracted": lambda r: r["reads"].update(extracted_to_repo=True),
        "notes short": lambda r: r.update(notes="ok"),
        "extra key": lambda r: r.update(z=1),
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
    except Exception as e:  # a failed read or run is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
