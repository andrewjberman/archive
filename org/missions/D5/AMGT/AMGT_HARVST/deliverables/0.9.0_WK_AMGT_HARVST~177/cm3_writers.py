# -*- coding: utf-8 -*-
"""HVST-cm-3 (AMGT_HARVST round 98, PATHKEY-WRITERS-2) -- READ-ONLY re-run of the round-96 writer census (HVST-ck-4,
ck4_writers.py) after the pull_enqueue deploy (HVST-cl-1/cl-2), grading the result: 0 raw-spelling writers.
Copied from ck4_writers.py; the changes are the output name, this header, the Lambda classification (verified at run
time by verify_lambda_copy, not read from the round-96 table), the negative control (a token generated at run time),
and the WRITER-CHANGED / WRITER-NEW / WRITER-GONE comparison against ck4_writers.out.

Run from the root of the worktree, in the foreground:  python -B -u <this file>
(-B: no bytecode is written into the shared checkout.)
It reads the SHARED checkout C:/Dev/ajb_workspace by absolute path, changes no file there, and writes its output to
cm3_writers.out next to this file (newline="\\n"). Discovery mode (--discover) prints the occurrence groups only.

Method, stated so a reader can check it:
  1. PREFIX: the literal leading path of every path-component key template the gateway reads, parsed from the
     gateway module ASTs (harvest_research.py P_*, harvest_figures.py MODEL/FYE, harvest_identity.py KEYED
     path-component rows and the packs/ ledger literal, harvest_published.py ADMISSION_PREFIX). Nothing is typed.
  2. SCAN: one walk of the shared checkout. Every file of the listed extensions is read (denominator printed per
     extension). A LITERAL occurrence is a line holding the prefix literal. A NAME occurrence is a line holding a
     module constant whose value is that prefix (the indirection a literal scan cannot see), resolved per use.
  3. CLASSIFY: each occurrence is classed from its enclosing function (ast) and file kind. The VERDICT tables record
     what each function was READ to do (the key it builds, the call that puts it, the schedule register).
     A function absent from the tables that performs an S3 write call prints class=WRITER spelling=unknown.
  4. ADDENDUM: writers whose key is an f-string placeholder (derived/{ENGINE}/...) carry no literal the scan can
     match; each is listed here with its file:line, read by hand, and printed as its own occurrence.
  5. NEWEST: read-only S3 list calls (list_objects_v2 pages only; no get, put, delete or copy) under each prefix for
     the two measured slash keys, RAW and CANONICAL spelling, printing the newest LastModified.
  6. CONTROLS: a reader that must be found (positive) and a literal that exists nowhere (negative), by the same scan.
"""
import ast
import collections
import datetime
import os
import re
import secrets
import subprocess
import sys
import time

SHARED = "C:/Dev/ajb_workspace"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cm3_writers.out")
ROUND96_OUT = os.path.join(HERE, "..", "0.9.0_WK_AMGT_HARVST~173", "ck4_writers.out")
DISCOVER = "--discover" in sys.argv

GW_REL = "infra/aws/ec2/opal-gateway/app/"
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
TEXT_EXTS = {".py", ".sh", ".ps1", ".js", ".ts", ".tsx", ".tf", ".yaml", ".yml", ".json", ".md"}
MAX_BYTES = 2 * 1024 * 1024
# the negative control: generated at run time, never typed in any file (ZZ_NO_SUCH_ + 16 hex + _ZZ/v1/)
NEG_TOKEN = "ZZ_NO_SUCH_" + secrets.token_hex(8) + "_ZZ/v1/"
LAMBDA_REL = "infra/aws/lambda/research/pull_enqueue/lambda_function.py"
LAMBDA_TEST_REL = "infra/aws/lambda/research/pull_enqueue/test_cl1_status_key_canonical.py"
LAMBDA_FIXTURE_REL = "infra/aws/ec2/opal-gateway/tests/fixtures/cj2_continuation_keys.txt"
LAMBDA_EXTRA_KEYS = ["BP/_LN_Equity", "NG/_LN_Equity"]
LAMBDA_REFUSAL_PROBES = [None, 5, "", "NVDA\u00e9_US_Equity", " BP/_LN_Equity", "BP-SLASH-_LN_Equity"]
WRITER_LINE_RE = re.compile(r"^WRITER (\S+) (\S+):(\d+) (\S+) spelling=(\S+)")
RECORD_TREES = ("org/missions/", "org/tier1_exec/", "org/tier0_exec/", "org/surprise_channel/",
                "org/critical_paths/", ".runtmp/", ".scratch/")
PRODUCT_ROOTS = ("lib/", "integrations/", "infra/", "workflows/")
# S3 write APIs and the repository's own writers of an S3 key (a generic 'write' or 'put' is not a write site here)
S3_WRITE_CALLS = {"put_object", "upload_file", "upload_fileobj", "copy_object", "gold_put", "write_pool",
                  "write_document", "write_pool_object", "s3_put_if_absent", "_write_status", "_write_ledger_raw",
                  "bronze_write", "_put"}
READ_CALLS = {"get_object", "list_objects_v2", "list_objects", "get_paginator", "paginate", "head_object",
              "_list_json", "read_json", "read_parquet", "read", "read_text", "load", "fetch_pool_json",
              "_live_listing", "_live_prefix", "list_keys", "newest_part", "_json_under", "_read_all", "served_names",
              "filed_names", "keyed_population", "newer", "latest_stamp_under"}
NAME_RE = re.compile(r"^_?[A-Z][A-Z0-9_]*PREFIX$|^P_[A-Z][A-Z0-9_]*$")

SCHED_CLI = "none-registered: CLI module, no scheduler register names it (infra/aws/terraform/harvest/*schedule*.tf, .tools/*schedule*, org/devices)"
SCHED_PIPE = "none-registered: called from pipeline code paths only; no scheduler register names it"
SCHED_QUEUE = "queue-driven: SQS consumer drain loop (infra/aws/terraform/harvest/sqs.tf); no scheduler register"
SCHED_EVENT = "event-driven: Lambda invoked per request on the internal tier route; never scheduled"
SCHED_READ = "not a writer"

# (rel, line) -> (class, spelling, schedule, basis): a line-level verdict wins over the function's verdict.
VERDICT_LINES = {
    ("lib/research/peers/engine.py", 1325): ("OTHER", "-", "-", "log message text, no key construction"),
    ("lib/research/peers/engine.py", 1427): ("OTHER", "-", "-", "batch summary print, no key construction"),
    ("lib/research/peers/engine.py", 1503): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/management/enrich.py", 237): ("OTHER", "-", "-", "message text"),
    ("lib/research/management/enrich.py", 980): ("OTHER", "-", "-", "SKIP-POOL print text"),
    ("lib/research/management/enrich.py", 1091): ("OTHER", "-", "-", "SKIP-POOL print text"),
    ("lib/research/management/enrich.py", 1178): ("OTHER", "-", "-", "SKIP-POOL print text"),
    ("lib/research/management/enrich.py", 1221): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/management/enrich.py", 1222): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/management/enrich.py", 1229): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/management/enrich.py", 1231): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/management/enrich.py", 1238): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/management/enrich.py", 1244): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/management/enrich.py", 1345): ("OTHER", "-", "-", "SKIP-POOL print text"),
    ("lib/research/management/officer_plan.py", 88): ("OTHER", "-", "-", "plan text naming an excluded aggregate"),
    ("lib/research/management/fwd7_plan.py", 97): ("OTHER", "-", "-", "argparse help text"),
    ("lib/research/filings/batch.py", 505): ("OTHER", "-", "-", "help text"),
    ("lib/research/filings/analyze.py", 2069): ("OTHER", "-", "-", "summary print, no key construction"),
    ("lib/research/scores/run_scores.py", 145): ("OTHER", "-", "-", "message text"),
    ("integrations/bloomberg/research/management_posture_batch.py", 294): ("OTHER", "-", "-", "print text"),
    ("integrations/bloomberg/research/management_posture_batch.py", 298): ("OTHER", "-", "-", "print text"),
    ("integrations/bloomberg/research/management_posture_batch.py", 163): ("READER", "-", SCHED_READ, "newest object read (list + get_object)"),
    ("integrations/bloomberg/research/management_posture_batch.py", 177): ("READER", "-", SCHED_READ, "served-names listing (list only)"),
    ("integrations/bloomberg/research/management_posture_batch.py", 178): ("READER", "-", SCHED_READ, "served-names listing (list only)"),
    ("integrations/bloomberg/research/management_posture_batch.py", 218): ("READER", "-", SCHED_READ,
        "served-names listing of cmd_management (list only); its writes are at :256 via management_enrich.write_pool_object"),
    ("integrations/bloomberg/research/management_posture_batch.py", 276): ("READER", "-", SCHED_READ,
        "served-names listing of cmd_posture (list only); its writes run inside posture_judge.run(write_pool=...)"),
    ("lib/research/posture/judge.py", 450): ("READER", "-", SCHED_READ, "fetch of the R-1 peer set (fetch_pool_json), read"),
    ("lib/research/api/scoped_amgt.py", 7975): ("OTHER", "-", "-", "route table text"),
    ("lib/research/api/scoped_amgt.py", 7976): ("OTHER", "-", "-", "route table text"),
    ("infra/aws/ec2/opal-gateway/app/harvest_identity.py", 536): ("READER", "-", SCHED_READ,
        "branch on the live prefix of a coverage read (_live_prefix)"),
    ("infra/aws/ec2/opal-gateway/app/harvest_published.py", 86): ("READER", "raw", SCHED_READ,
        "admission address of a read: the caller's key is concatenated as typed (read only)"),
    ("lib/research/print/render_pack.py", 82): ("OTHER", "-", "-", "template key constant read by the renderer"),
    ("lib/opal_data_harvest/uploads.py", 165): ("WRITER", "canonical", SCHED_CLI,
        "publication-links branch of the uploader; put_object at :201; the key is the outbox key from catalog.store (opaque identity, no slash)"),
    ("lib/opal_data_harvest/uploads.py", 180): ("WRITER", "canonical", SCHED_CLI,
        "publication-links branch of the uploader; put_object at :201; the key is the outbox key from catalog.store (opaque identity, no slash)"),
}

# (rel, function) -> (class, spelling, schedule, basis)
VERDICTS = {
    ("lib/research/peers/engine.py", "pool_key"): ("WRITER", "canonical", SCHED_CLI,
        "pool key slash_safe_key(security_key) at :1181; put_object in write_pool_object (:1189) via run_batch (:1353) and main (:1533)"),
    ("lib/research/management/enrich.py", "management_key"): ("WRITER", "canonical", SCHED_CLI,
        "management key slash_safe_key(security_key) at :778; write_document -> crosswalk.write_pool (:918-921); callers batch.py:176, proxy_officers.py:375"),
    ("lib/research/management/enrich.py", "pool_key"): ("WRITER", "canonical", SCHED_CLI,
        "the _pool aggregate key (POOL_NAME; no security key in the path, so the spelling question is vacuous, counted canonical by identity); write_pool_object (:1190-1195)"),
    ("lib/research/filings/analyze.py", "write_outputs"): ("WRITER", "canonical", SCHED_CLI,
        "drafting key slash_safe_key(security_key) at :1946; crosswalk.write_pool at :1958; callers batch.run_group and analyze.main"),
    ("lib/research/filings/fetch.py", "pool_key"): ("WRITER", "canonical", SCHED_CLI,
        "filings .analysis.json key slash_safe_key at :482; written by analyze.write_outputs (:1939-1941) and reverify_stored_thesis_driver (:1775, write_pool at :1830); persist() writes no filings/v1 object (:486-499)"),
    ("lib/research/filings/drafting_build.py", "_drafting_pool_key"): ("WRITER", "canonical", SCHED_CLI,
        "drafting key slash_safe_key at :606; put via _rebuild_pool (:695), _splice_driver_pool (:816), _hold_unspanned_pool (:949)"),
    ("lib/research/filings/drafting_build.py", "_newest_analysis_key"): ("READER", "raw", SCHED_READ,
        "listing of filings/v1 under the caller's key as typed (list only, :630)"),
    ("lib/research/posture/judge.py", "pool_key"): ("WRITER", "canonical", SCHED_CLI,
        "posture key slash_safe_key at :250; put_object in write_pool_object (:303) with read-back (:310); callers judge.run and management_posture_batch.cmd_posture"),
    ("lib/research/scores/run_scores.py", "run"): ("WRITER", "canonical", SCHED_CLI,
        "scores key slash_safe_key at :336; crosswalk.write_pool at :340; the dry-run branch (:337-339) writes nothing"),
    ("lib/research/ledger/ledger.py", "_ledger_key"): ("WRITER", "canonical", SCHED_PIPE,
        "packs input_ledger key slash_safe_key at :72; put_object in _write_ledger_raw (:86-94); callers record_run and rerun"),
    ("integrations/bloomberg/research/pull_consumer.py", "_write_status"): ("WRITER", "canonical", SCHED_QUEUE,
        "packs status key slash_safe_key at :58; get_object read-modify-write (:61) then put_object (:68)"),
    ("lib/opal_data_harvest/catalog.py", "store"): ("WRITER", "canonical", SCHED_CLI,
        "publication-links key from security['key'] (:74) = the rank identity key 'security-<hash>' (opaque; 0 of 242 identity records carry '/'); staged to the outbox, uploaded by uploads.run"),
    ("lib/opal_data_harvest/uploads.py", "run"): ("WRITER", "canonical", SCHED_CLI,
        "put_object of the outbox key (:201); the spelling is inherited from catalog.store (opaque identity key, no slash)"),
    ("integrations/bloomberg/research/management_posture_batch.py", "cmd_management"): ("WRITER", "canonical", SCHED_CLI,
        "drives management_enrich.write_pool_object (:256) and the per-name writes; the keys are built in enrich.py (management_key, pool_key)"),
    ("integrations/bloomberg/research/management_posture_batch.py", "cmd_posture"): ("WRITER", "canonical", SCHED_CLI,
        "drives posture_judge.run(write_pool=...) (:287); the keys are built in judge.py (pool_key)"),
}

# READ-ADDENDUM: writers whose key the literal scan cannot match (the prefix is built from a constant in an f-string),
# each read by hand at the cited line of the shared checkout.
ADDENDUM = [
    dict(prefix="derived/model_block/", rel="integrations/bloomberg/research/model_block_pull.py", line=1811,
         fn="stage_derive", cls="WRITER", spelling="canonical", schedule=SCHED_CLI,
         basis="f-string derived/{ENGINE}/{slash_safe_key(sec_key)}/{stamp}/model_block.json with ENGINE='model_block' (:90); put via s3_put_if_absent (:654-668)"),
    dict(prefix="derived/model_block_fye/", rel="integrations/bloomberg/research/derive_fye_fixed.py", line=131,
         fn="derive_one", cls="WRITER", spelling="canonical", schedule=SCHED_CLI,
         basis="f-string derived/{ENGINE}/{slash_safe_key(sec_key)}/{stamp}/model_block_fye.json with ENGINE='model_block_fye' (:39); put via s3_put_if_absent (:82-94)"),
]


def emit_factory():
    state = {"fh": None, "lines": []}

    def emit(line):
        state["lines"].append(line)
        if state["fh"] is not None:
            state["fh"].write(line + "\n")
        else:
            print(line)
    return emit, state


emit, EMIT_STATE = emit_factory()


def is_record_json(rel):
    return rel.startswith(RECORD_TREES) or "/deliverables/" in rel


def leading_literal(value):
    """The fixed leading path of a template: text before the first %, refused when it is a security_key= partition."""
    lead = value.split("%")[0]
    if "security_key=" in lead:
        return None
    return lead


# ----------------------------------------------------------------------------------------- 1. PREFIX (read, not typed)
def gateway_prefixes():
    """{literal: {'name', 'template' (DIR|FILE|ROOT|CC|RAW), 'sources': [rel:line]}} from the gateway ASTs."""
    found = collections.OrderedDict()

    def add(literal, name, template, src):
        if literal is None or not literal.endswith("/"):
            return
        ent = found.setdefault(literal, {"name": name, "template": template, "sources": []})
        ent["sources"].append(src)

    rel = GW_REL + "harvest_research.py"
    tree = ast.parse(open(os.path.join(SHARED, rel), encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("P_MANAGEMENT", "P_FILINGS", "P_DRAFTING", "P_PEERS", "P_SCORES", "P_POSTURE"):
            val = node.value.value
            tmpl = "FILE" if val.endswith(".json") else "DIR"
            add(leading_literal(val), node.targets[0].id, tmpl, "%s:%d" % (rel, node.lineno))
    rel = GW_REL + "harvest_figures.py"
    tree = ast.parse(open(os.path.join(SHARED, rel), encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("MODEL_PREFIX", "FYE_PREFIX"):
            add(leading_literal(node.value.value), node.targets[0].id, "DIR", "%s:%d" % (rel, node.lineno))
    rel = GW_REL + "harvest_identity.py"
    tree = ast.parse(open(os.path.join(SHARED, rel), encoding="utf-8").read())
    tmpl_name = {"_DIR": "DIR", "_FILE": "FILE", "_ROOT": "ROOT", "_CC": "CC"}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "KEYED":
            for elt in node.value.elts:
                literal, tmpl = elt.elts[0].value, elt.elts[1].id
                if tmpl in tmpl_name:
                    add(leading_literal(literal), "KEYED", tmpl_name[tmpl], "%s:%d" % (rel, elt.lineno))
    for sub in ast.walk(tree):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str) and "input_ledger.json" in sub.value:
            add(leading_literal(sub.value), "_ledger", "DIR", "%s:%d" % (rel, sub.lineno))
    rel = GW_REL + "harvest_published.py"
    tree = ast.parse(open(os.path.join(SHARED, rel), encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "ADMISSION_PREFIX":
            add(leading_literal(node.value.value), "ADMISSION_PREFIX", "RAW", "%s:%d" % (rel, node.lineno))
    return found


# ----------------------------------------------------------------------------------------- 2. SCAN
def walk_files():
    for dp, dns, fns in os.walk(SHARED):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            yield dp, fn


def is_product_def(rel):
    return rel.startswith(PRODUCT_ROOTS) and "/deliverables/" not in rel and "/checks/" not in rel \
        and "/tests/" not in rel and "/layers/" not in rel and "/build/" not in rel and "/fixtures/" not in rel


def scan(literals, want_names, prefix_names):
    """One pass over the shared checkout.
    literals: prefix literals to match as lines. want_names: True in pass 1 (collect constant definitions).
    prefix_names: {NAME} whose uses are collected in pass 2."""
    denom = collections.Counter()
    excluded = collections.Counter()
    skipped_big = 0
    lit_hits = collections.defaultdict(list)     # literal -> [(rel, line, ext, text)]
    name_uses = collections.defaultdict(list)    # NAME -> [(rel, line, text)]
    defs_all = []                                # (rel, NAME, literal-or-None) for product-tree module constants
    name_re = re.compile(r"\b(" + "|".join(sorted(map(re.escape, prefix_names))) + r")\b") if prefix_names else None
    for dp, fn in walk_files():
        ext = os.path.splitext(fn)[1].lower()
        if ext not in TEXT_EXTS:
            continue
        full = os.path.join(dp, fn)
        rel = os.path.relpath(full, SHARED).replace("\\", "/")
        try:
            if os.path.getsize(full) > MAX_BYTES:
                skipped_big += 1
                continue
        except OSError:
            continue
        if ext == ".json" and is_record_json(rel):
            excluded[ext] += 1
            continue
        denom[ext] += 1
        try:
            with open(full, encoding="utf-8", errors="replace", newline="") as fh:
                text = fh.read()
        except OSError:
            continue
        for idx, line in enumerate(text.split("\n"), 1):
            if literals and ("ZZ_NO_SUCH" in line or any(lit in line for lit in literals)):
                for lit in literals:
                    if lit in line:
                        lit_hits[lit].append((rel, idx, ext, line.strip()))
            if ext == ".py":
                if want_names and is_product_def(rel):
                    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:os\.environ\.get\([^,]*,\s*)?[\"']([^\"']+)[\"']", line)
                    if m and NAME_RE.match(m.group(1)):
                        defs_all.append((rel, m.group(1), m.group(2)))
                if name_re is not None and name_re.search(line) and not any(lit in line for lit in literals):
                    for mm in name_re.finditer(line):
                        name_uses[mm.group(1)].append((rel, idx, line.strip()))
    return denom, excluded, skipped_big, lit_hits, name_uses, defs_all


def is_prefix(lit, prefixes):
    return lit in prefixes


# ----------------------------------------------------------------------------------------- 3. CLASSIFY
_text_cache = {}


def file_text(rel):
    if rel not in _text_cache:
        try:
            with open(os.path.join(SHARED, rel), encoding="utf-8", errors="replace") as fh:
                _text_cache[rel] = fh.read()
        except OSError:
            _text_cache[rel] = ""
    return _text_cache[rel]


HARVEST_REF = re.compile(r"opal-data-harvest|HARVEST_BUCKET|POOL_BUCKET|mbp\.BUCKET|hstore\.|harvest_read|"
                         r"lib\.research\.harvest|harvest_typed|crosswalk\.write_pool")
_harvest_cache = {}


def harvest_addressed(rel):
    """True when the file names the harvest bucket or its store (it can address the census prefixes there)."""
    if rel not in _harvest_cache:
        if rel.startswith("lib/opal_data_harvest/"):
            _harvest_cache[rel] = True          # the harvester stages objects and uploads them to the harvest bucket
        else:
            _harvest_cache[rel] = bool(HARVEST_REF.search(file_text(rel)))
    return _harvest_cache[rel]


def parse_py(rel):
    try:
        return ast.parse(file_text(rel))
    except (SyntaxError, ValueError):
        return None


def py_structure(tree):
    funcs, docs = [], []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append((node.lineno, node.end_lineno, node.name, node))
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                docs.append((first.lineno, first.end_lineno))
    return funcs, docs


def call_names(node):
    names = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            f = sub.func
            if isinstance(f, ast.Attribute):
                names.add(f.attr)
            elif isinstance(f, ast.Name):
                names.add(f.id)
    return names


def is_test_path(rel):
    base = rel.rsplit("/", 1)[-1]
    return "/tests/" in rel or rel.startswith("tests/") or base.startswith("test_") or "/test_" in rel


def is_scratch_path(rel):
    return rel.startswith((".scratch", ".runtmp", "tmp/")) or "/.scratch" in rel or "/.runtmp/" in rel


def lead(value):
    """The fixed leading path of a constant's value (a template such as 'peers/v1/%s/' -> 'peers/v1/')."""
    return value.split("%")[0]


def resolve_name(name, use_rel, prefix_defs, all_defs):
    """A name use -> the LEADING prefix literal it carries, or None (not a prefix constant), or 'UNRESOLVED'."""
    same = [lit for (drel, dname, lit) in all_defs if drel == use_rel and dname == name]
    if same:
        return lead(same[0]) if lead(same[0]) in PREFIX_SET else None
    cands = sorted(set(lead(lit) for (drel, dname, lit) in prefix_defs if dname == name))
    if len(cands) == 1:
        return cands[0]
    if not cands:
        return None
    hit = set()
    text = file_text(use_rel)
    for (drel, dname, lit) in prefix_defs:
        if dname == name and re.search(r"\b%s\b" % re.escape(os.path.basename(drel)[:-3]), text):
            hit.add(lead(lit))
    return hit.pop() if len(hit) == 1 else "UNRESOLVED"


PREFIX_SET = set()


def classify(rows, prefix_defs, all_defs):
    """rows: dicts(prefix, rel, line, ext, via, text). Returns classified dicts."""
    out = []
    by_file = collections.defaultdict(list)
    for r in rows:
        by_file[r["rel"]].append(r)
    for rel, frows in by_file.items():
        ext = frows[0]["ext"]
        for r in frows:
            if ext == ".md":
                out.append(dict(r, cls="DOC", fn="-", spelling="-", schedule="-", basis="docs file (.md)"))
            elif ext == ".json":
                out.append(dict(r, cls="OTHER", fn="-", spelling="-", schedule="-", basis="config/data JSON, not code"))
            elif ext != ".py":
                cls, basis = "OTHER", "%s file, not a python I/O site" % ext
                txt = r.get("text", "")
                if ext in (".ts", ".tsx", ".js") and (txt.startswith("*") or txt.startswith("//")):
                    cls, basis = "DOC", "portal comment"
                elif ext in (".yaml", ".yml"):
                    basis = "catalog/register entry (yaml), not a writer"
                elif ext == ".tf":
                    basis = "terraform (IAM, route or scheduler text), not a writer"
                out.append(dict(r, cls=cls, fn="-", spelling="-", schedule="-", basis=basis))
            else:
                out.append(classify_py(r, rel, prefix_defs, all_defs))
    return out


_CW = {}


def crosswalk_module():
    """lib/research/identity/crosswalk.py, imported from the shared checkout (read only; -B writes no bytecode)."""
    if "mod" not in _CW:
        if SHARED not in sys.path:
            sys.path.insert(0, SHARED)
        from lib.research.identity import crosswalk
        _CW["mod"] = crosswalk
    return _CW["mod"]


def _outcome(fn, value):
    """('ok', value), or ('raise', 'ValueError') for any ValueError (a subclass such as SlashSafeKeyError is a
    ValueError, as pytest.raises(ValueError) reads it), or ('raise', <other class name>) -- a NameError is never a refusal."""
    try:
        return ("ok", fn(value))
    except Exception as exc:  # noqa: BLE001 -- the refusal kind is the observable
        return ("raise", "ValueError" if isinstance(exc, ValueError) else type(exc).__name__)


def verify_lambda_copy():
    """pull_enqueue ships its OWN stdlib copy of crosswalk.slash_safe_key (_slash_safe_key). Verified here, at run
    time, from the Lambda and the crosswalk as they stand in the shared checkout -- not from the round-96 table:
      (a) the copy's def line; the call site in lambda_handler that builds the packs status key, on the same line as
          the 'packs/%s/status.json' literal; the put_object call(s) in lambda_handler;
      (b) equality with crosswalk.slash_safe_key over the measured keys (the fixture, as the test's own comparison)
          and the test's refusal probes (outcome compared: value, or refusal).
    Returns (spelling, basis). spelling is 'canonical' only when every check holds; otherwise 'unknown'."""
    if "verdict" in _CW:
        return _CW["verdict"]
    tree = ast.parse(file_text(LAMBDA_REL))
    copy_def = handler = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "_slash_safe_key":
            copy_def = node
        if isinstance(node, ast.FunctionDef) and node.name == "lambda_handler":
            handler = node
    if copy_def is None or handler is None:
        _CW["verdict"] = ("unknown", "UNVERIFIED: %s has no module-level _slash_safe_key or no lambda_handler" % LAMBDA_REL)
        return _CW["verdict"]
    status_lines = [n.lineno for n in ast.walk(handler) if isinstance(n, ast.Constant)
                    and isinstance(n.value, str) and "packs/%s/status.json" in n.value]
    call_lines = [n.lineno for n in ast.walk(handler) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Name) and n.func.id == "_slash_safe_key"]
    put_lines = [n.lineno for n in ast.walk(handler) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and n.func.attr == "put_object"]
    site_ok = any(s in call_lines for s in status_lines)
    # the copy's own module-level constant (_SLASH_SAFE_TOKEN) travels with the def; nothing else is imported
    consts = [n for n in tree.body if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "_SLASH_SAFE_TOKEN" for t in n.targets)]
    ns = {"ascii": ascii}
    mod = ast.Module(body=consts + [copy_def], type_ignores=[])
    ast.fix_missing_locations(mod)
    exec(compile(mod, LAMBDA_REL, "exec"), ns)
    copy_fn = ns["_slash_safe_key"]
    cw = crosswalk_module()
    fixture = [ln for ln in file_text(LAMBDA_FIXTURE_REL).splitlines() if ln.strip()]
    keys = fixture + LAMBDA_EXTRA_KEYS
    key_mism = [k for k in keys if _outcome(copy_fn, k) != _outcome(cw.slash_safe_key, k)]
    # the test's assertion: BOTH sides raise ValueError on a refusal (test_refusals_match_crosswalk)
    probe_mism = [repr(p) for p in LAMBDA_REFUSAL_PROBES
                  if not (_outcome(copy_fn, p) == ("raise", "ValueError") and
                          _outcome(cw.slash_safe_key, p) == ("raise", "ValueError"))]
    probe_kinds = [_outcome(cw.slash_safe_key, p)[1] for p in LAMBDA_REFUSAL_PROBES]
    ok = site_ok and bool(put_lines) and not key_mism and not probe_mism and bool(consts)
    basis = ("stdlib COPY of crosswalk.slash_safe_key: def _slash_safe_key at %s:%d (module constant _SLASH_SAFE_TOKEN "
             "at %s:%d); call site in lambda_handler at %s:%d builds the packs status key (site_ok=%s); put_object at %s; "
             "equality with lib/research/identity/crosswalk.py slash_safe_key over %d keys (%d fixture + %d extra; fixture "
             "%s; the test's own comparison is %s::test_slash_safe_key_equals_crosswalk_over_every_measured_key) "
             "key_mismatches=%d; refusal probes %d, crosswalk outcomes [%s] (the test's is %s::test_refusals_match_crosswalk) "
             "probe_mismatches=%d"
             % (LAMBDA_REL, copy_def.lineno, LAMBDA_REL, consts[0].lineno if consts else -1,
                LAMBDA_REL, status_lines[0] if status_lines else -1, site_ok,
                ",".join(str(x) for x in put_lines) or "NONE", len(keys), len(fixture), len(LAMBDA_EXTRA_KEYS),
                LAMBDA_FIXTURE_REL, LAMBDA_TEST_REL, len(key_mism), len(LAMBDA_REFUSAL_PROBES),
                ",".join(probe_kinds), LAMBDA_TEST_REL, len(probe_mism)))
    if ok:
        _CW["verdict"] = ("canonical", basis)
    else:
        _CW["verdict"] = ("unknown", "UNVERIFIED (not canonical): " + basis + " ; probe_mismatch_values=" + ",".join(probe_mism))
    return _CW["verdict"]


def classify_py(r, rel, prefix_defs, all_defs):
    ln = r["line"]
    if is_test_path(rel):
        return dict(r, cls="TEST", fn="-", spelling="-", schedule="-", basis="test module")
    if is_scratch_path(rel):
        return dict(r, cls="OTHER", fn="-", spelling="-", schedule="-",
                    basis="untracked scratch copy (git ls-files: none); not a served or scheduled module")
    if not harvest_addressed(rel):
        return dict(r, cls="OTHER", fn="-", spelling="-", schedule="-",
                    basis="out of scope: this file never addresses the harvest bucket (no opal-data-harvest, HARVEST_BUCKET, POOL_BUCKET, mbp.BUCKET or harvest store reference)")
    tree = parse_py(rel)
    if tree is None:
        return dict(r, cls="OTHER", fn="?", spelling="unknown", schedule="unknown", basis="file does not parse")
    funcs, docs = py_structure(tree)
    src_lines = file_text(rel).split("\n")
    stripped = src_lines[ln - 1].strip() if ln - 1 < len(src_lines) else ""
    if stripped.startswith("#"):
        return dict(r, cls="DOC", fn="-", spelling="-", schedule="-", basis="comment line")
    if any(s <= ln <= e for s, e in docs):
        return dict(r, cls="DOC", fn="-", spelling="-", schedule="-", basis="docstring")
    if (rel, ln) in VERDICT_LINES:
        cls, spelling, schedule, basis = VERDICT_LINES[(rel, ln)]
        best = next(((s, e, n, nd) for s, e, n, nd in funcs if s <= ln <= e), None)
        return dict(r, cls=cls, fn=best[2] if best else "<module>", spelling=spelling, schedule=schedule, basis=basis)
    best = None
    for s, e, name, node in funcs:
        if s <= ln <= e and (best is None or s >= best[0]):
            best = (s, e, name, node)
    if best is None:
        return dict(r, cls="OTHER", fn="<module>", spelling="-", schedule="-",
                    basis="module-level constant or literal; its use sites are classified at their own lines")
    fn, node = best[2], best[3]
    if (rel, fn) == (LAMBDA_REL, "lambda_handler"):
        spelling, basis = verify_lambda_copy()
        return dict(r, cls="WRITER", fn=fn, spelling=spelling, schedule=SCHED_EVENT, basis=basis)
    if (rel, fn) in VERDICTS:
        cls, spelling, schedule, basis = VERDICTS[(rel, fn)]
        return dict(r, cls=cls, fn=fn, spelling=spelling, schedule=schedule, basis=basis)
    calls = call_names(node)
    if calls & S3_WRITE_CALLS:
        return dict(r, cls="WRITER", fn=fn, spelling="unknown", schedule="unknown",
                    basis="UNVERIFIED: enclosing function performs an S3 write call and has no verdict")
    if calls & READ_CALLS:
        return dict(r, cls="READER", fn=fn, spelling="-", schedule="-",
                    basis="auto: enclosing function performs read calls and no S3 write call")
    return dict(r, cls="OTHER", fn=fn, spelling="-", schedule="-",
                basis="auto: no S3 I/O call in the enclosing function (message, route, helper or constant)")


# ----------------------------------------------------------------------------------------- 4. NEWEST
def seg(template, key):
    """The key segment exactly as the gateway's harvest_identity._segment builds it (DIR, FILE, ROOT, CC; RAW = key)."""
    if template == "DIR":
        return "%s/" % key
    if template == "FILE":
        return key
    if template == "ROOT":
        return "%s/" % key.split("_")[0]
    if template == "CC":
        return "%s/" % (key[:-len("_Equity")] if key.endswith("_Equity") else key)
    return key


def newest(client, bucket, prefix, counter):
    count, newest_dt = 0, None
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        counter["requests"] += 1
        for obj in page.get("Contents", []) or []:
            count += 1
            lm = obj["LastModified"]
            if newest_dt is None or lm > newest_dt:
                newest_dt = lm
    stamp = newest_dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if newest_dt else "none"
    return count, stamp


# ----------------------------------------------------------------------------------------- MAIN
def shared_head():
    """The shared checkout's HEAD, read with git rev-parse (read only). A failed read is printed as UNREAD."""
    try:
        res = subprocess.run(["git", "-C", SHARED, "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                             timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        return "UNREAD(%s)" % type(exc).__name__
    val = res.stdout.strip()
    return val if res.returncode == 0 and val else "UNREAD(rc=%d)" % res.returncode


def parse_round96(path):
    """The round-96 WRITER lines of ck4_writers.out -> ({(prefix, file, function): {(line, spelling)}}, n_lines)."""
    sites = collections.defaultdict(set)
    n = 0
    with open(path, encoding="utf-8", newline="") as fh:
        for line in fh.read().split("\n"):
            m = WRITER_LINE_RE.match(line)
            if m:
                n += 1
                sites[(m.group(1), m.group(2), m.group(4))].add((int(m.group(3)), m.group(5)))
    return sites, n


def main():
    global PREFIX_SET
    t0 = time.time()
    out_fh = None
    if not DISCOVER:
        out_fh = open(OUT_PATH, "w", encoding="utf-8", newline="\n")
        EMIT_STATE["fh"] = out_fh
    gw = gateway_prefixes()
    literals = list(gw.keys())
    PREFIX_SET = set(literals)
    emit("# cm3_writers.py -- HVST-cm-3 read-only writer census, re-run after the pull_enqueue deploy (AMGT_HARVST round 98, PATHKEY-WRITERS-2)")
    emit("# shared checkout: %s (HEAD %s read at the run; read by absolute path, nothing written there)" % (SHARED, shared_head()))
    emit("# run: %s UTC; python %s" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                       sys.version.split()[0]))
    for lit, ent in gw.items():
        emit("PREFIX %s literal=%s template=%s source=%s" % (ent["name"], lit, ent["template"], ", ".join(ent["sources"])))
    emit("PREFIX-SET n=%d (the 8 named by the cell, plus the coverage, publication-link and admission templates the gateway reads)"
         % len(literals))

    scan_lits = literals + [NEG_TOKEN]
    denom, excluded, skipped_big, lit_hits, _, defs_all = scan(scan_lits, True, set())
    prefix_defs = [(rel, name, lit) for (rel, name, lit) in defs_all if any(lit.startswith(p) for p in PREFIX_SET)]
    prefix_names = set(name for (_, name, _) in prefix_defs)
    _, _, _, _, name_uses, _ = scan([], False, prefix_names)

    for ext in sorted(denom):
        emit("SCAN-DENOM ext=%s files=%d" % (ext, denom[ext]))
    emit("SCAN-DENOM total_files=%d skipped_over_2MiB=%d json_record_trees_excluded=%d (records: org/missions, org/tier1_exec, "
         "org/tier0_exec, deliverables, .runtmp, .scratch)" % (sum(denom.values()), skipped_big, excluded.get(".json", 0)))
    emit("SCAN-NAMES prefix_constants=%d names=%s" % (len(prefix_defs), ", ".join(sorted(prefix_names))))

    rows = []
    for lit in literals:
        for rel, ln, ext, txt in lit_hits.get(lit, []):
            rows.append(dict(prefix=lit, rel=rel, line=ln, ext=ext, via="literal", text=txt))
    unresolved, resolved = 0, 0
    for name, uses in name_uses.items():
        for rel, ln, txt in uses:
            lit = resolve_name(name, rel, prefix_defs, defs_all)
            if lit is None:
                continue
            if lit == "UNRESOLVED":
                unresolved += 1
                lit = "UNRESOLVED:" + name
            else:
                resolved += 1
            ext = os.path.splitext(rel)[1].lower()
            rows.append(dict(prefix=lit, rel=rel, line=ln, ext=ext, via="name:" + name, text=txt))
    emit("SCAN-NAME-USES resolved=%d unresolved=%d (an unresolved use is printed as OTHER)" % (resolved, unresolved))
    # the negative control is not a census prefix
    neg_n = len(lit_hits.get(NEG_TOKEN, []))
    rows = [r for r in rows if r["prefix"] in PREFIX_SET or r["prefix"].startswith("UNRESOLVED:")]

    classified = classify(rows, prefix_defs, defs_all)
    for a in ADDENDUM:
        classified.append(dict(prefix=a["prefix"], rel=a["rel"], line=a["line"], ext=".py", via="read-addendum",
                               text="", cls=a["cls"], fn=a["fn"], spelling=a["spelling"], schedule=a["schedule"],
                               basis=a["basis"]))
    classified.sort(key=lambda c: (c["prefix"], c["rel"], c["line"]))

    if DISCOVER:
        grp = collections.Counter()
        for c in classified:
            grp[(c["rel"], c["fn"], c["prefix"], c["cls"], c["via"])] += 1
        for k, v in sorted(grp.items()):
            print("DISC %s | %s | %s | %s | %s | n=%d" % (k[0], k[1], k[2], k[3], k[4], v))
        print("DISC rows=%d neg=%d elapsed=%.1f" % (len(rows), neg_n, time.time() - t0))
        return

    counts = collections.Counter()
    per_prefix_writers = collections.defaultdict(list)
    for c in classified:
        counts[c["cls"]] += 1
        emit("OCCURRENCE %s %s:%d class=%s function=%s via=%s basis=%s" %
             (c["prefix"], c["rel"], c["line"], c["cls"], c["fn"], c["via"], c["basis"]))
        if c["cls"] == "WRITER":
            per_prefix_writers[c["prefix"]].append(c)
            emit("WRITER %s %s:%d %s spelling=%s schedule=%s" %
                 (c["prefix"], c["rel"], c["line"], c["fn"], c["spelling"], c["schedule"]))

    # NEWEST: read-only lists (list_objects_v2 pages), RAW and CANONICAL spelling of the two measured slash keys
    sys.path.insert(0, SHARED)
    from lib.research.harvest import store as hstore
    crosswalk = crosswalk_module()
    bucket = hstore.HARVEST_BUCKET
    client = hstore._default_client()
    counter = collections.Counter()
    for lit, ent in gw.items():
        for raw_key in ("BP/_LN_Equity", "NG/_LN_Equity"):
            can_key = crosswalk.slash_safe_key(raw_key)
            raw_pfx = lit + seg(ent["template"], raw_key)
            can_pfx = lit + seg(ent["template"], can_key)
            raw_n, raw_new = newest(client, bucket, raw_pfx, counter)
            can_n, can_new = newest(client, bucket, can_pfx, counter)
            emit("NEWEST %s %s raw_n=%d raw_newest=%s canonical_n=%d canonical_newest=%s" %
                 (lit, raw_key, raw_n, raw_new, can_n, can_new))
            emit("NEWEST-LISTED %s raw=s3://%s/%s canonical=s3://%s/%s" % (lit, bucket, raw_pfx, bucket, can_pfx))

    # controls
    pos = [c for c in classified if c["prefix"] == "peers/v1/" and c["rel"].endswith("harvest_research.py")
           and c["cls"] == "READER"]
    if pos:
        emit("CONTROL-POSITIVE reader_found prefix=peers/v1/ file=%s class=READER" % pos[0]["rel"])
    else:
        emit("CONTROL-POSITIVE NOT-FOUND prefix=peers/v1/ (no READER occurrence in harvest_research.py)")
    emit("CONTROL-NEGATIVE-2 token=%s occurrences=%d" % (NEG_TOKEN, neg_n))
    for rel, ln, ext, txt in lit_hits.get(NEG_TOKEN, []):
        emit("CONTROL-NEGATIVE-2-HIT %s:%d ext=%s class=%s text=%s" %
             (rel, ln, ext, "DOC" if ext == ".md" else "CODE-OR-CONFIG", txt[:170]))

    for lit in literals:
        if not per_prefix_writers.get(lit):
            emit("NO-WRITER %s: searched the shared checkout (%d files of the listed extensions, the literal and the name "
                 "scan of its constants, and the f-string placeholder forms read by hand); no writer in the repository. "
                 "A writer outside the repository is invisible to this census." % (lit, sum(denom.values())))

    writers = [c for c in classified if c["cls"] == "WRITER"]
    raw_w = sum(1 for c in writers if c["spelling"] == "raw")
    can_w = sum(1 for c in writers if c["spelling"] == "canonical")
    unk_w = sum(1 for c in writers if c["spelling"] not in ("raw", "canonical"))
    # round-98 vs round-96: a site is (prefix, file, function); its spelling(s) are compared, its line is printed
    old_sites, old_n = parse_round96(ROUND96_OUT)
    new_sites = collections.defaultdict(set)
    for c in writers:
        new_sites[(c["prefix"], c["rel"], c["fn"])].add((c["line"], c["spelling"]))
    n_changed = n_new = n_gone = 0
    for key in sorted(set(old_sites) & set(new_sites)):
        o_sp = set(s for _, s in old_sites[key])
        n_sp = set(s for _, s in new_sites[key])
        if o_sp != n_sp:
            for line, sp in sorted(new_sites[key]):
                n_changed += 1
                emit("WRITER-CHANGED %s %s:%d was=%s now=%s" % (key[0], key[1], line, ",".join(sorted(o_sp)), sp))
    for key in sorted(set(new_sites) - set(old_sites)):
        for line, sp in sorted(new_sites[key]):
            n_new += 1
            emit("WRITER-NEW %s %s:%d %s spelling=%s" % (key[0], key[1], line, key[2], sp))
    for key in sorted(set(old_sites) - set(new_sites)):
        for line, sp in sorted(old_sites[key]):
            n_gone += 1
            emit("WRITER-GONE %s %s:%d %s spelling=%s" % (key[0], key[1], line, key[2], sp))
    emit("WRITER-DIFF round96_writer_lines=%d round96_sites=%d now_writer_lines=%d now_sites=%d changed=%d new=%d gone=%d "
         "(site = prefix, file, function; a line move alone is not a change)"
         % (old_n, len(old_sites), len(writers), len(new_sites), n_changed, n_new, n_gone))
    emit("# class counts: %s ; elapsed=%.1fs" % (dict(counts), time.time() - t0))
    emit("CENSUS-WRITERS prefixes=%d occurrences=%d writers=%d raw_writers=%d canonical_writers=%d "
         "unknown_writers=%d files_scanned=%d gets=%d" %
         (len(literals), len(classified), len(writers), raw_w, can_w, unk_w, sum(denom.values()), counter["requests"]))
    if out_fh is not None:
        out_fh.close()


if __name__ == "__main__":
    main()
