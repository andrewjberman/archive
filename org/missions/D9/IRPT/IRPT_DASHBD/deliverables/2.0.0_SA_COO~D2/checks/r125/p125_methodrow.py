"""IRPT_DASHBD round 125, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-256, the `dim_return_method` CLAIMS READ (CTO analysis @4285776c5c ruling 4, row IRPT_DASHBD-D2-S78): which
producer may write `threshold_claims_source`, and where. The producer's method row carries claim columns (CLAIM_COLUMNS, `threshold_claims_source` among them); the served 49 Financial
rows are method_version 1 (2026-10-01) and 2 (2026-10-03); the scheduled reporting-gold function writes five gold prefixes and not this one. A READ of the repo and of S3: no write, no grant.

  DB-b-256 (~209) the served rows' columns, the producer's claim columns, the claim columns missing from the served rows, every call site of emit_method_row, whether a scheduled function
                  reaches one, and which Terraform names the prefix.                         DB125-3-AC1

Definitions (the checker recounts every list):
  served_versions = for each object method_version=N/data.parquet under the firm's dim_return_method prefix (49 Financial, from address()): {method_version, columns (sorted parquet column
  names), claim_columns_present (the producer's claim columns among them, sorted)};  producer_claim_columns = sorted(CLAIM_COLUMNS) of account_return_daily.py (THRESHOLD_VALUES each + "_claim",
  plus threshold_claims_source);  missing_in_newest = producer_claim_columns minus the newest served version's columns, sorted;
  call_sites = sorted "relpath::function" of every call to emit_method_row (an ast scan) in .py files under data/assets/scripts/gold/irpt_reporting and infra/aws/lambda/investor-reporting,
  excluding any path with a /tests/ segment and the def itself;  scheduled_function_call_sites = the call_sites under infra/aws/lambda;
  terraform_files_naming_prefix = sorted .tf files under infra/aws/terraform/investor-reporting whose uncommented text contains "dim_return_method" ;
  reporting_gold_write_list_has_prefix = whether the uncommented `irpt_rg_gold_write_arns` list of the reporting-gold locals.tf mentions dim_return_method.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import ast
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~209/RD_METHOD_ROW_READ_R125.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~209/method_row_read_r125.py"
PRODUCER_REL = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
SCAN_DIRS = ("data/assets/scripts/gold/irpt_reporting", "infra/aws/lambda/investor-reporting")
TF_DIR = "infra/aws/terraform/investor-reporting"
GOLD_LOCALS_REL = "infra/aws/terraform/investor-reporting/reporting-gold/locals.tf"
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("cottonwood", "inflection", "orion/", "eclipse/", "opal-data-cottonwood", "opal-data-inflection")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item", "update_item",
                "write_table", "write_to_dataset", ".to_parquet(", "emit_method_row(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "call_sites", "scheduled_function_call_sites", "terraform_files_naming_prefix")


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


def is_tracked(root, rel):
    return subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel], capture_output=True, text=True).returncode == 0


def uncommented(text):
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))


# ------------------------------------------------------------------------------------------------ the recount (pure parts)
def claim_columns_of(src):
    tree = ast.parse(src)
    tv = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "THRESHOLD_VALUES" for t in n.targets):
            tv = ast.literal_eval(n.value)
    need(tv, "THRESHOLD_VALUES not found in the producer")
    return sorted([v + "_claim" for v in tv] + ["threshold_claims_source"])


def call_sites_of(rel, src):
    """['rel::function'] for each call to emit_method_row inside a function (module level: '<module>')."""
    tree = ast.parse(src)
    out = []

    def visit(node, fn):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit(ch, ch.name)
                continue
            if isinstance(ch, ast.Call):
                f = ch.func
                nm = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
                if nm == "emit_method_row":
                    out.append("%s::%s" % (rel, fn))
            visit(ch, fn)
    visit(tree, "<module>")
    return sorted(set(out))


def write_list_has_prefix(locals_text):
    t = uncommented(locals_text)
    m = re.search(r"irpt_rg_gold_write_arns\s*=\s*\[(.*?)\n\s*\]", t, re.S)
    need(m is not None, "no irpt_rg_gold_write_arns list in the reporting-gold locals.tf")
    return "dim_return_method" in m.group(1)


def recount(root):
    root = Path(root)
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    claims = claim_columns_of((root / PRODUCER_REL).read_text(encoding="utf-8"))
    s3 = boto3.client("s3")
    addr = opal_naming.address("irpt", FIRM, "gold", "dim_return_method", "method_version=1", "data.parquet")
    bucket, key = addr[len("s3://"):].split("/", 1)
    pre = key.split("method_version=", 1)[0]
    r = s3.list_objects_v2(Bucket=bucket, Prefix=pre)
    versions = []
    for o in r.get("Contents", []):
        m = re.fullmatch(re.escape(pre) + r"method_version=(\d+)/data\.parquet", o["Key"])
        if not m:
            continue
        schema = pq.read_schema(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()))
        cols = sorted(schema.names)
        versions.append({"method_version": int(m.group(1)), "columns": cols, "claim_columns_present": sorted(set(cols) & set(claims))})
    versions.sort(key=lambda v: v["method_version"])
    need(versions, "no served method row listed")
    newest_cols = set(versions[-1]["columns"])
    sites = []
    for d in SCAN_DIRS:
        for p in sorted((root / d).rglob("*.py")):
            rel = p.relative_to(root).as_posix()
            if "/tests/" in rel or "/__pycache__/" in rel:
                continue
            txt = p.read_text(encoding="utf-8", errors="replace")
            if "emit_method_row" in txt:
                sites += call_sites_of(rel, txt)
    sites = sorted(set(sites))
    tfs = sorted(p.relative_to(root).as_posix() for p in (root / TF_DIR).rglob("*.tf") if "dim_return_method" in uncommented(p.read_text(encoding="utf-8", errors="replace")))
    return {"served_versions": versions, "producer_claim_columns": claims, "missing_in_newest": sorted(set(claims) - newest_cols), "call_sites": sites,
            "scheduled_function_call_sites": [s for s in sites if s.startswith("infra/aws/lambda/")], "terraform_files_naming_prefix": tfs,
            "reporting_gold_write_list_has_prefix": write_list_has_prefix((root / GOLD_LOCALS_REL).read_text(encoding="utf-8"))}


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
KEYS = ("served_versions", "producer_claim_columns", "missing_in_newest", "call_sites", "scheduled_function_call_sites", "terraform_files_naming_prefix", "reporting_gold_write_list_has_prefix")


def check_record(rec, truth, analysis_text, tracked, analysis_sha):
    exp = {"firm", *KEYS, "who_may_write", "words", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and nes(rec["words"]) and rec["claim"] in CLAIMS, "firm, words or claim")
    for k in KEYS:
        need(rec[k] == truth[k], "%s: record %s, recount %s" % (k, json.dumps(rec[k])[:200], json.dumps(truth[k])[:200]))
    w = rec["who_may_write"]
    need(isinstance(w, dict) and set(w) == {"producer_function", "entry_point", "grant_needed", "options", "words"} and nes(w["producer_function"]) and nes(w["entry_point"]) and nes(w["grant_needed"])
         and isinstance(w["options"], list) and len(w["options"]) >= 2 and all(isinstance(o, dict) and set(o) == {"id", "words"} and nes(o["id"]) and nes(o["words"]) for o in w["options"])
         and nes(w["words"]), "who_may_write block: the producer function, its entry point, the grant a writer needs, at least two options {id, words}")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and an.get("sha256") == analysis_sha and tracked, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    low = analysis_text.lower()
    need(not [t for t in FOREIGN if t in low], "the script names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the script holds a write call")
    return True


def run(root, cid):
    need(cid == "DB125-3-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root)
    check_record(rec, truth, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    print("OK: method-row read: %d served versions (newest lacks %d of %d claim columns); %d call site(s) of emit_method_row, %d in a scheduled function; %d Terraform file(s) name the prefix; "
          "reporting-gold write list has it: %s; every list equals the recount" % (len(truth["served_versions"]), len(truth["missing_in_newest"]), len(truth["producer_claim_columns"]),
                                                                              len(truth["call_sites"]), len(truth["scheduled_function_call_sites"]), len(truth["terraform_files_naming_prefix"]),
                                                                              truth["reporting_gold_write_list_has_prefix"]))
    return True


def selftest():
    import copy
    src = 'THRESHOLD_VALUES = ("a", "b")\n'
    assert claim_columns_of(src) == ["a_claim", "b_claim", "threshold_claims_source"]
    code = "def main():\n    emit_method_row(1)\n\ndef other():\n    x = mod.emit_method_row(2)\n\ndef emit_method_row(s):\n    return 1\n\nemit_method_row(3)\n"
    assert call_sites_of("f.py", code) == ["f.py::<module>", "f.py::main", "f.py::other"]
    assert write_list_has_prefix("locals {\n  irpt_rg_gold_write_arns = [\n    \"a/dim_return_method/*\",\n  ]\n}\n") is True
    assert write_list_has_prefix("locals {\n  irpt_rg_gold_write_arns = [\n    # dim_return_method\n    \"a/b/*\",\n  ]\n}\n") is False
    truth = {"served_versions": [{"method_version": 1, "columns": ["a"], "claim_columns_present": []}], "producer_claim_columns": ["a_claim"], "missing_in_newest": ["a_claim"],
             "call_sites": ["x.py::main"], "scheduled_function_call_sites": [], "terraform_files_naming_prefix": [], "reporting_gold_write_list_has_prefix": False}
    rec = {"firm": FIRM, **copy.deepcopy(truth), "who_may_write": {"producer_function": "emit_method_row", "entry_point": "main --method-row-only", "grant_needed": "PutObject on the one prefix",
           "options": [{"id": "A", "words": "w"}, {"id": "B", "words": "w"}], "words": "w"}, "words": "w", "analysis": {"file": ANALYSIS_REL, "tracked": True, "sha256": "a" * 64},
           "reads": {"s3_reads": 3, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured", "files_in_repo": False, "served_values_changed": False,
           "pushed": False, "deployed": False}

    def grade(r, t="x = 1", tr=truth):
        try:
            return check_record(r, tr, t, True, "a" * 64)
        except Fail:
            return False
    assert grade(copy.deepcopy(rec)) is True
    for name, f in (("versions", lambda r: r["served_versions"][0].update(columns=["b"])), ("claims", lambda r: r.update(producer_claim_columns=[])), ("missing", lambda r: r.update(missing_in_newest=[])),
                    ("sites", lambda r: r.update(call_sites=[])), ("scheduled", lambda r: r.update(scheduled_function_call_sites=["y"])), ("tf", lambda r: r.update(terraform_files_naming_prefix=["z.tf"])),
                    ("grant flag", lambda r: r.update(reporting_gold_write_list_has_prefix=True)), ("one option", lambda r: r["who_may_write"].update(options=[{"id": "A", "words": "w"}])),
                    ("flag", lambda r: r.update(pushed=True)), ("writes", lambda r: r["reads"].update(s3_writes=1)), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="id 1234567890"))):
        r = copy.deepcopy(rec)
        f(r)
        assert grade(r) is False, "red arm %s passed" % name
    assert grade(copy.deepcopy(rec), t="s3.put_object()") is False and grade(copy.deepcopy(rec), t="opal-data-cottonwood") is False
    print("selftest: the ast scans, the write-list reader, one green and fourteen red record arms behave")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
