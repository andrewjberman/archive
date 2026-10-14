"""IRPT_DASHBD round 108 (issuer 2.0.0_SA_COO~D2) -- the issuance for 1.0.0_SA_CTO~DELL2's ROUND-108 ANALYSIS (@4d26563910; the CVO graded DB107-1-J1 PASS, so the 49 Financial thread is done but for the disclosure gate).

  DB-b-211 (~171)  the Inflection adapter's first tables: account_dim and the household key, read from Inflection's own silver prefixes only, with counts and the schema hash
                   against the gold contract; a private dry-run table; nothing written to S3.                                                           DB108-1-AC1
  DB-b-212 (~172)  two reads that decide Inflection's coverage words: whether Orion's returns include dividends (measured against one account's transactions) and whether
                   Eclipse tax lots are populated (else NO_LOTS in plain words); counts and words only.                                                   DB108-2-AC1

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers on synthetic arms
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P6 = load_mod("p106", "r106/p106_round106.py")
P5 = P6.P5
P = P5.P
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D = P.D
PRIV = P.PRIV
Fail = P.Fail
DIM_CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_DIM_CONTRACT.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_dim.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_inflection_account_dim.py"
DRY_DIR = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~171/"
ALLOWED_PREFIXES = ("s3://opal-data-assets/orion/inflection/", "s3://opal-data-assets/eclipse/inflection/")
# another firm's bucket, key prefix or master id must appear nowhere in the module (CLAUDE.md cross-firm rule)
FOREIGN = ("cottonwood", "49financial", "49f_", "opal-data-49", "orion/4698", "eclipse/4698", "/4698/")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects")
ORION_DIV = ("YES", "NO", "NOT_ESTABLISHED")


def schema_hash_of(root, module_rel):
    code = ("import hashlib, importlib.util\nspec = importlib.util.spec_from_file_location('m', %r)\nm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
            "print(hashlib.sha256('\\n'.join(sorted('%%s:%%s' %% (x.name, x.type) for x in m.ARROW_SCHEMA)).encode()).hexdigest())\n") % str((root / module_rel).resolve())
    o = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, cwd=str(root))
    return o.returncode, o.stdout.strip(), o.stderr.strip()[-200:]


def foreign_hits(src):
    low = src.lower()
    return [t for t in FOREIGN if t in low]


def write_hits(src):
    return [t for t in WRITE_TOKENS if t in src]


def s3_literals(src):
    return sorted(set(re.findall(r"s3://[A-Za-z0-9._/\-=]+", src)))


# ---------------------------------------------------------------- DB108-1-AC1 (the Inflection adapter's first tables)
def check_dim(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_R108.json")
    need((root / DIM_CONTRACT_REL).is_file(), "the account_dim gold contract %s must exist" % DIM_CONTRACT_REL)
    dc = json.loads((root / DIM_CONTRACT_REL).read_bytes().decode("utf-8"))
    need(P.HEX64.fullmatch(str(dc.get("schema_hash") or "")), "the gold contract carries no schema_hash")
    m = r.get("module") or {}
    need(m.get("file") == MODULE_REL and (root / MODULE_REL).is_file() and m.get("sha256") == sha(root / MODULE_REL) and m.get("tracked") is True, "module: the tracked file %s hashed as recorded" % MODULE_REL)
    src = (root / MODULE_REL).read_text(encoding="utf-8")
    need(not foreign_hits(src), "the adapter names another firm's place (%s): Inflection's own prefixes only" % foreign_hits(src))
    need(not write_hits(src), "the adapter holds a write call (%s): nothing is written to S3 in this round" % write_hits(src))
    lits = s3_literals(src)
    need(all(any(x.startswith(p) for p in ALLOWED_PREFIXES) for x in lits), "every s3:// literal of the adapter must sit under %s (found %s)" % (list(ALLOWED_PREFIXES), lits))
    t = r.get("tests") or {}
    need(t.get("file") == TEST_REL and (root / TEST_REL).is_file() and is_int(t.get("passed")) and t["passed"] >= 6 and t.get("failed") == 0 and t.get("mutant_failed") is True, "tests: %s, 6 or more passing, none failing, a failing mutant" % TEST_REL)
    q = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", str((root / TEST_REL).resolve())], capture_output=True, text=True, cwd=str(root))
    need(q.returncode == 0, "the test file does not pass when the checker runs it")
    rc, h, err = schema_hash_of(root, MODULE_REL)
    need(rc == 0 and h == dc["schema_hash"], "the adapter's ARROW_SCHEMA hash %s must equal the gold contract's schema_hash (C-ADAPTERS: the same schema hash) %s" % (h[:12], err))
    need(r.get("schema_hash") == dc["schema_hash"], "the record's schema_hash must equal the contract's")
    sp = r.get("source_prefixes")
    need(isinstance(sp, list) and sp and all(isinstance(x, str) and any(x.startswith(p) for p in ALLOWED_PREFIXES) for x in sp), "source_prefixes must list the Inflection prefixes read, each under %s" % list(ALLOWED_PREFIXES))
    dr = r.get("dry_run") or {}
    pth = str(dr.get("path") or "").replace("\\", "/")
    need(pth.startswith(DRY_DIR) and pth.endswith(".parquet") and Path(pth).is_file(), "dry_run.path must be a private .parquet under %s" % DRY_DIR)
    need(not pth.startswith(str(root.resolve()).replace("\\", "/").rstrip("/") + "/"), "the dry-run table is inside the repo: client data never goes there")
    need(dr.get("sha256") == sha(pth), "dry_run.sha256 must equal the file's bytes")
    import hashlib
    import pyarrow.parquet as pq
    tb = pq.read_table(pth)
    ph = hashlib.sha256("\n".join(sorted("%s:%s" % (f.name, f.type) for f in tb.schema)).encode()).hexdigest()
    need(ph == dc["schema_hash"], "the dry-run table's own schema hash must equal the contract's")
    rows = tb.to_pylist()
    accounts = {x["account_id"] for x in rows}
    households = {x["household_id"] for x in rows if x.get("household_id")}
    need(len(rows) == len(accounts) and len(accounts) > 0, "one row per account: %d rows, %d accounts" % (len(rows), len(accounts)))
    need(r.get("accounts") == len(accounts) and r.get("households") == len(households) and len(households) > 0, "accounts and households must equal the checker's recount from the dry-run table (%d, %d)" % (len(accounts), len(households)))
    need(all(x["firm"] == "inflection" for x in rows), "every row's firm must be inflection")
    need(nes(r.get("household_key_source")) and isinstance(r.get("absent_fields"), list) and nes(r.get("coverage_words")), "household_key_source (words), absent_fields (a list) and coverage_words (words) are required")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0 and is_int(rd.get("s3_reads")), "reads: vendor_calls, s3_writes, dynamodb_writes and secret_reads 0, s3_reads an integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not P.long_digit_runs({k: v for k, v in r.items() if k != "dry_run"}), "the record holds a run of 8 or more digits")
    print("OK: Inflection account_dim adapter: %d accounts in %d households recounted from the private dry-run table, schema hash equal to the gold contract, %d Inflection prefix(es), no write call, no other firm named, %d tests pass"
          % (len(accounts), len(households), len(sp), t["passed"]))


# ---------------------------------------------------------------- DB108-2-AC1 (the two coverage reads)
def check_reads(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~172/COVERAGE_READS_R108.json")
    od = r.get("orion_dividends") or {}
    need(od.get("answer") in ORION_DIV, "orion_dividends.answer must be one of %s" % list(ORION_DIV))
    need(nes(od.get("method")) and is_int(od.get("transactions_checked")) and is_int(od.get("dividend_flows")) and nes(od.get("basis_words")), "orion_dividends: method (words), transactions_checked, dividend_flows (integers) and basis_words")
    need(od["answer"] == "NOT_ESTABLISHED" or od["transactions_checked"] > 0, "an answer other than NOT_ESTABLISHED must rest on transactions actually checked")
    need(nes(od.get("account_ref")) and re.fullmatch(r"[0-9a-f]{64}", str(od.get("account_ref_sha256") or "")), "the account sampled is named only by account_ref_sha256 (a sha256 of its id), never by number")
    el = r.get("eclipse_lots") or {}
    need(isinstance(el.get("populated"), bool) and isinstance(el.get("tables_checked"), list) and el["tables_checked"] and all(nes(x) for x in el["tables_checked"]) and is_int(el.get("rows_with_lot_fields")), "eclipse_lots: populated (bool), tables_checked (a list of table names) and rows_with_lot_fields (an integer)")
    if el["populated"]:
        need(el["rows_with_lot_fields"] > 0, "lots reported populated but zero rows carry lot fields")
    else:
        need("NO_LOTS" in str(el.get("coverage_member") or "") and nes(el.get("lots_words")) and "NO_LOTS" not in str(el.get("lots_words")), "lots not populated: coverage_member must name NO_LOTS and lots_words must be plain words with no code token")
    sc = r.get("script") or {}
    need(nes(sc.get("file")) and (root / sc["file"]).is_file() and sc.get("sha256") == sha(root / sc["file"]) and sc.get("tracked") is True, "script: the tracked read script hashed as recorded")
    ssrc = (root / sc["file"]).read_text(encoding="utf-8")
    need(not foreign_hits(ssrc) and not write_hits(ssrc), "the read script names another firm's place or holds a write call")
    need(all(any(x.startswith(p) for p in ALLOWED_PREFIXES) for x in s3_literals(ssrc)), "every s3:// literal of the read script must sit under %s" % list(ALLOWED_PREFIXES))
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0 and is_int(rd.get("s3_reads")), "reads: vendor_calls, s3_writes, dynamodb_writes and secret_reads 0, s3_reads an integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not P.long_digit_runs({k: v for k, v in r.items() if k != "orion_dividends"}) and not P.long_digit_runs({k: v for k, v in od.items() if k != "account_ref_sha256"}), "the record holds a run of 8 or more digits")
    print("OK: Orion returns include dividends: %s (%d transactions checked, %d dividend flows); Eclipse lots populated: %s (%d rows carry lot fields across %d table(s))"
          % (od["answer"], od["transactions_checked"], od["dividend_flows"], el["populated"], el["rows_with_lot_fields"], len(el["tables_checked"])))


# ---------------------------------------------------------------- self test
def selftest():
    n = 0

    def arm(name, cond):
        nonlocal n
        n += 1
        if not cond:
            print("SELFTEST FAIL: %s" % name)
            sys.exit(1)

    arm("foreign: another firm's bucket in the source is found", foreign_hits('B = "opal-data-cottonwood"') == ["cottonwood"] and foreign_hits("x = 1") == [])
    arm("foreign: the Orion master prefix is another place", "orion/4698" in foreign_hits('s3://opal-data-assets/orion/4698/silver/'))
    arm("write tokens are found", write_hits("c.put_object(Bucket=b)") == ["put_object"] and write_hits("c.get_object(Bucket=b)") == [])
    arm("s3 literals are listed and checked against the allowed prefixes", s3_literals('a = "s3://opal-data-assets/orion/inflection/silver/fact_assets/"') == ["s3://opal-data-assets/orion/inflection/silver/fact_assets/"])
    arm("an Inflection Orion prefix is allowed and a Cottonwood one is not", any("s3://opal-data-assets/orion/inflection/silver/x".startswith(p) for p in ALLOWED_PREFIXES) and not any("s3://opal-data-cottonwood/irpt/".startswith(p) for p in ALLOWED_PREFIXES))
    root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(".").resolve()
    dc = json.loads((root / DIM_CONTRACT_REL).read_bytes().decode("utf-8"))
    cw = root / "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_account_dim.py"
    if cw.is_file():
        rc, h, _e = schema_hash_of(root, "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_account_dim.py")
        arm("the method reproduces the gold contract's schema hash from the Cottonwood adapter (so a same-schema Inflection adapter will match)", rc == 0 and h == dc["schema_hash"])
    print("SELFTEST OK: %d arms" % n)


FNS = {"DB108-1-AC1": check_dim, "DB108-2-AC1": check_reads}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
        return
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid in FNS, "unknown criterion %r" % cid)
        FNS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB108"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, ImportError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
