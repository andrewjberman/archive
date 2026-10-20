"""y3_check.py <id>: the round-25 (workstream GATEWAY) criteria of cell MX-y-3, run from the repository (or worktree) root.
Ids: y3.AC1 (the group-form links and the store vocabulary, in-process on fixtures), y3.AC2 (the doubled `dynamodb_dynamodb_` prefix is gone
from the four store rows and every id that names them, the scoped-API row names its store, the entries still load), y3.AC3 (pytest: the new
test file plus the four existing atom_decomposition files). Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL.
ASCII only; python 3.9. Y3_ROOT (default: the current directory) names the root that holds workflows/atom_decomposition.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round25-GATEWAY.md R25.3 (Y3) as AMENDED by the order's section 1 (the order wins)."""
import copy
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R25 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R25, "fixtures")
ROOT = os.environ.get("Y3_ROOT") or os.getcwd()
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
EMIT_PY = os.path.join(AD, "emit_catalog_v02.py")
NEW_TEST = os.path.join(AD, "tests", "test_group_links.py")
OLD_TESTS = ["tests/test_c_group.py", "tests/test_tool_index_and_harvest.py", "tests/test_depth_kinds.py", "tests/test_serves_map.py"]
BASELINE_PASSED = 72   # the four existing files at the round-25 base; the new file adds at least 8
NEW_MIN = 8
RENAMES = {
    "dynamodb_dynamodb_etf_classifications": "dynamodb_etf_classifications",
    "dynamodb_dynamodb_opal_keyword_intelligence": "dynamodb_opal_keyword_intelligence",
    "dynamodb_dynamodb_opal_news_articles": "dynamodb_opal_news_articles",
    "dynamodb_dynamodb_opal_news_trending_daily": "dynamodb_opal_news_trending_daily",
}
MEMBERS_COUNT = 4   # each old id is named 4 times in tool_index/members.yaml at the base (and 0 times in pending_members.yaml)
SCOPED = "published_analysis_scoped_api"
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def fx(name):
    return os.path.join(FIX, name)


def jload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def load_emitter():
    if not os.path.isfile(EMIT_PY):
        raise RuntimeError("emitter absent: %s" % EMIT_PY)
    sys.path.insert(0, AD)
    spec = importlib.util.spec_from_file_location("emit_catalog_v02_y3_under_test", EMIT_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ABSENT = {"claim": "absent", "reason": "fixture"}


def run_index(emit, members, link_groups, row_groups, tools, row_ids):
    """load_tool_index on a temp tool_index folder holding `members`; returns (entries by tool, errors)."""
    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "members.yaml"), "w", encoding="ascii") as fh:
            yaml.safe_dump({"members": members}, fh)
        with open(os.path.join(tmp, "measured.yaml"), "w", encoding="ascii") as fh:
            yaml.safe_dump({"tools": dict((t, {"history_depth": ABSENT}) for t in tools)}, fh)
        with open(os.path.join(tmp, "pending_members.yaml"), "w", encoding="ascii") as fh:
            yaml.safe_dump({"pending": []}, fh)
        saved = emit.TOOL_INDEX_DIR
        emit.TOOL_INDEX_DIR = tmp
        try:
            census = jload(fx("y3_census.json"))
            census["tools"] = [x for x in census["tools"] if x["tool"] in tools]   # only the tools this run holds an entry for
            census["n"] = len(census["tools"])
            kw = {}
            if link_groups is not None:
                kw["link_groups"] = link_groups
            if row_groups is not None:
                kw["row_groups"] = row_groups
            entries, errors, _c = emit.load_tool_index(set(row_ids), copy.deepcopy(census), row_keys={}, **kw)
        finally:
            emit.TOOL_INDEX_DIR = saved
    return dict((e["tool"], e) for e in entries), errors


def member(tool, index, links):
    return {"tool": tool, "member": "a", "index": index, "links": links, "freshness": ABSENT}


def ac1(tmp):
    rows_doc = jload(fx("y3_rows.json"))["rows"]
    row_ids = [r["entity"] for r in rows_doc]
    print("DENOMINATOR: fixture y3 -- %d catalog rows (two of group alpha, one of group beta, one without vendor and firm, one without a vendor), "
          "groups alpha, beta and an empty one; five tools in the census; the store words dynamodb, graph, amgt-scoped-api" % len(rows_doc))
    emit = load_emitter()
    # 1. the link-groups reader
    lg_path = fx("y3_link_groups.json")
    groups, errs = emit.load_link_groups([lg_path])
    arm("load_link_groups reads the fixture: three groups, no errors", sorted(groups) == ["g_alpha", "g_beta", "g_empty"] and errs == [],
        "groups=%r errs=%r" % (sorted(groups), errs))
    arm("a group holds exactly bucket, vendor and firm", all(set(v) == {"bucket", "vendor", "firm"} for v in groups.values()), repr(groups))
    base = jload(lg_path)

    def refused(doc, label, paths_extra=()):
        p = os.path.join(tmp, "lg_%s.json" % re.sub(r"\W+", "_", label))
        with open(p, "w", encoding="ascii") as fh:
            json.dump(doc, fh)
        g, e = emit.load_link_groups([p] + list(paths_extra))
        return bool(e)

    m1 = copy.deepcopy(base)
    m1["schema"] = "gateway_link_groups/0"
    arm("planted mutant refused: a wrong schema string", refused(m1, "schema"))
    m2 = copy.deepcopy(base)
    m2["groups"]["G_Upper"] = {"bucket": "opal-data-fixa", "vendor": "va", "firm": "fa"}
    arm("planted mutant refused: an upper-case group id", refused(m2, "upper"))
    m3 = copy.deepcopy(base)
    del m3["groups"]["g_alpha"]["firm"]
    arm("planted mutant refused: a group without its firm", refused(m3, "nofirm"))
    m4 = copy.deepcopy(base)
    m4["groups"]["g_beta"]["vendor"] = ""
    arm("planted mutant refused: an empty vendor", refused(m4, "emptyvendor"))
    arm("planted mutant refused: one group id named by two files", refused(base, "dup", paths_extra=[lg_path]))
    # 2. the row side
    sections = {"silver_datasets": [dict(r) for r in rows_doc[:3]], "portal_datasets": [dict(rows_doc[3])], "harvest_datasets": [dict(rows_doc[4])]}
    rg = emit.build_row_groups(sections)
    arm("build_row_groups keeps exactly the rows that carry bucket, vendor and firm, as (bucket, vendor, firm)",
        rg == {"row.a1": ("opal-data-fixa", "va", "fa"), "row.a2": ("opal-data-fixa", "va", "fa"), "row.b1": ("opal-data-fixb", "vb", "fb")}, repr(rg))
    # 3. the expansion
    members = [
        member("t_group", {"group": "g_alpha"}, [{"group": "g_alpha"}, "row.plain"]),
        member("t_lines", "row.a1", ["row.a1", "row.a2", "row.plain"]),
        member("t_dup", "row.a1", ["row.a1", {"group": "g_alpha"}, "row.b1", {"group": "g_beta"}]),
    ]
    entries, errors = run_index(emit, members, groups, rg, ["t_group", "t_lines", "t_dup"], row_ids)
    tg, tl, td = entries.get("t_group", {}), entries.get("t_lines", {}), entries.get("t_dup", {})
    arm("the group form loads with no error", errors == [] and tg != {}, "errors=%r" % errors[:3])
    arm("a group in links expands to the sorted entity ids of the rows with that key; a plain id stays: links row.a1, row.a2, row.plain",
        tg.get("links") == ["row.a1", "row.a2", "row.plain"], "got %r" % tg.get("links"))
    arm("an index written as {group: id} is the first sorted entity of the group", tg.get("index") == "row.a1", "got %r" % tg.get("index"))
    arm("the group form and the line-per-row form give the same index and links", (tg.get("index"), tg.get("links")) == (tl.get("index"), tl.get("links")),
        "group=%r lines=%r" % ((tg.get("index"), tg.get("links")), (tl.get("index"), tl.get("links"))))
    arm("an id a group expands to is skipped when the list already holds it: row.a1, row.a2, row.b1", td.get("links") == ["row.a1", "row.a2", "row.b1"], "got %r" % td.get("links"))
    ep, erp = run_index(emit, [member("t_dup", "row.a1", ["row.a1", "row.a1"])], groups, rg, ["t_dup"], row_ids)
    arm("a plain id stays exactly as written, a repeated plain id stays repeated (a per-link depth may name one row twice)",
        erp == [] and ep.get("t_dup", {}).get("links") == ["row.a1", "row.a1"], "errors=%r links=%r" % (erp[:2], ep.get("t_dup", {}).get("links")))
    e2, er2 = run_index(emit, members, groups, rg, ["t_group", "t_lines", "t_dup"], row_ids)
    arm("two runs give the same entries", json.dumps(entries, sort_keys=True) == json.dumps(e2, sort_keys=True) and er2 == [], "differs")
    # 4. refusals of the expansion
    _e, er = run_index(emit, [member("t_nogroup", "row.a1", [{"group": "g_nope"}, "row.a1"])], groups, rg, ["t_nogroup"], row_ids)
    arm("planted mutant refused: a group id no --link-groups file names (the error names the tool and the group)",
        any("t_nogroup" in x and "g_nope" in x for x in er), "errors=%r" % er[:3])
    _e, er = run_index(emit, [member("t_empty", "row.a1", ["row.a1", {"group": "g_empty"}])], groups, rg, ["t_empty"], row_ids)
    arm("planted mutant refused: a group that matches no catalog row (the error names the tool and the group)",
        any("t_empty" in x and "g_empty" in x for x in er), "errors=%r" % er[:3])
    e3, er3 = run_index(emit, [member("t_lines", "row.a1", ["row.a1", "row.a2"])], None, None, ["t_lines"], row_ids)
    arm("without --link-groups the line-per-row form works exactly as before", er3 == [] and e3.get("t_lines", {}).get("links") == ["row.a1", "row.a2"],
        "errors=%r" % er3[:3])
    # 5. the store vocabulary
    nb = emit.normalize_bucket
    arm("normalize_bucket admits the three store words exactly", nb("dynamodb") == "dynamodb" and nb("graph") == "graph" and nb("amgt-scoped-api") == "amgt-scoped-api",
        "got %r" % [nb("dynamodb"), nb("graph"), nb("amgt-scoped-api")])
    arm("normalize_bucket still keeps an S3 bucket name and still turns DynamoDB wording into the word",
        nb("opal-data-assets") == "opal-data-assets" and nb("none (DynamoDB us-east-1)") == "dynamodb")
    arm("planted mutant refused: a lookalike store word, a bare opal-data and a URL are not admitted",
        nb("amgt-scoped-apix") is None and nb("opal-data") is None and nb("s3://opal-data-assets") is None and nb("bucket-x") is None,
        "got %r" % [nb("amgt-scoped-apix"), nb("opal-data"), nb("s3://opal-data-assets"), nb("bucket-x")])
    sec = {"silver_datasets": [{"entity": "r_scoped", "bucket": "amgt-scoped-api"}, {"entity": "r_graph", "bucket": "graph"},
                               {"entity": "r_bad", "bucket": "amgt-scoped-apix"}], "portal_datasets": [], "harvest_datasets": []}
    se = emit.settle_row_buckets(sec, "opal-data-portal-v2")
    arm("settle_row_buckets accepts a scoped-API and a graph row and refuses a lookalike, naming it",
        len(se) == 1 and "r_bad" in se[0] and sec["silver_datasets"][0]["bucket"] == "amgt-scoped-api" and sec["silver_datasets"][1]["bucket"] == "graph", "errs=%r" % se)
    # 6. the command line
    absent = os.path.join(tmp, "no_such_link_groups.json")
    rc = emit.main(["--link-groups", absent])
    arm("emit_catalog_v02.main refuses a --link-groups file that does not exist with exit 2, before anything is read or written", rc == 2, "rc=%r" % (rc,))


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def scoped_ok(entries, emit):
    """The scoped-API row names its store: bucket amgt-scoped-api, table the route, and it settles to that bucket. Returns a problem list."""
    out = []
    data = entries.get(SCOPED)
    if not isinstance(data, dict):
        return ["%s is not a loaded entry" % SCOPED]
    if data.get("bucket") != "amgt-scoped-api":
        out.append("bucket is %r, not amgt-scoped-api" % data.get("bucket"))
    if data.get("table") != "/api/scoped/amgt":
        out.append("table is %r, not the route /api/scoped/amgt" % data.get("table"))
    sec = {"silver_datasets": [emit.silver_catalog_row(SCOPED, data)], "portal_datasets": [], "harvest_datasets": []}
    se = emit.settle_row_buckets(sec, "opal-data-portal-v2")
    if se or sec["silver_datasets"][0].get("bucket") != "amgt-scoped-api":
        out.append("the row does not settle to the store word: %r" % se)
    return out


def rename_problems(files, members_text, pending_text):
    out = []
    for old, new in RENAMES.items():
        if old + ".yaml" in files:
            out.append("%s.yaml is still a catalog entry" % old)
        if new + ".yaml" not in files:
            out.append("%s.yaml is absent" % new)
        if old in members_text or old in pending_text:
            out.append("%s is still named in a tool_index file" % old)
        n = members_text.count(new)
        if n != MEMBERS_COUNT:
            out.append("%s is named %d times in members.yaml, not %d" % (new, n, MEMBERS_COUNT))
        if pending_text.count(new) != 0:
            out.append("%s is named in pending_members.yaml" % new)
    return out


def unresolved_store_ids(members_text, stems):
    import yaml
    doc = yaml.safe_load(members_text) or {}
    seen = set()
    for m in doc.get("members") or []:
        if not isinstance(m, dict):
            continue
        for x in [m.get("index")] + list(m.get("links") or []):
            if isinstance(x, str) and x.startswith("dynamodb_"):
                seen.add(x)
    return sorted(x for x in seen if x not in stems), len(seen)


def ac2(tmp):
    ce = os.path.join(AD, "tool_index"), os.path.join(AD, "catalog_entries")
    print("DENOMINATOR: %d doubled-prefix store rows (four entries, each named %d times in members.yaml) and the scoped-API row %s, read from %s"
          % (len(RENAMES), MEMBERS_COUNT, SCOPED, AD))
    emit = load_emitter()
    files = set(os.path.basename(p) for p in glob.glob(os.path.join(ce[1], "dynamodb_*.yaml")))
    members_text = read_text(os.path.join(ce[0], "members.yaml"))
    pending_text = read_text(os.path.join(ce[0], "pending_members.yaml"))
    prob = rename_problems(files, members_text, pending_text)
    arm("the four store rows are files without the doubled prefix, and every id that names them moved with them (%d occurrences each)" % MEMBERS_COUNT, not prob, "; ".join(prob[:4]))
    entries, errors = emit.load_catalog_entries()
    arm("every catalog entry still loads with no error (the renamed files and the scoped-API row included)", errors == {}, "errors=%r" % sorted(errors)[:5])
    arm("the four renamed store rows are loaded entries", all(new in entries for new in RENAMES.values()), "missing %r" % [n for n in RENAMES.values() if n not in entries])
    sp = scoped_ok(entries, emit)
    arm("the scoped-API row names its store: bucket amgt-scoped-api, table /api/scoped/amgt, and it settles to that bucket", not sp, "; ".join(sp))
    sec = {"silver_datasets": [emit.silver_catalog_row(n, entries[n]) for n in sorted(RENAMES.values()) if n in entries], "portal_datasets": [], "harvest_datasets": []}
    se = emit.settle_row_buckets(sec, "opal-data-portal-v2")
    arm("the four store rows settle to the single word dynamodb", se == [] and [r["bucket"] for r in sec["silver_datasets"]] == ["dynamodb"] * 4, "errs=%r" % se)
    stems = set(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ce[1], "*.yaml")))
    unres, total = unresolved_store_ids(members_text, stems)
    arm("every dynamodb_ id that members.yaml names (%d) is a catalog entry" % total, not unres and total >= 4, "unresolved %r" % unres[:4])
    # planted mutants, made from the present data
    old = "dynamodb_dynamodb_opal_news_articles"
    mt = members_text.replace("dynamodb_opal_news_articles", old, 1)
    arm("planted mutant refused: one id put back to the doubled prefix", bool(rename_problems(files, mt, pending_text)))
    mf = set(files)
    mf.discard("dynamodb_etf_classifications.yaml")
    arm("planted mutant refused: a renamed file missing", bool(rename_problems(mf, members_text, pending_text)))
    me = copy.deepcopy(entries)
    me[SCOPED]["bucket"] = "opal-data-harvest"
    arm("planted mutant refused: the scoped-API row back on an S3 bucket", bool(scoped_ok(me, emit)))
    me2 = copy.deepcopy(entries)
    me2[SCOPED]["table"] = None
    arm("planted mutant refused: the scoped-API row without its route", bool(scoped_ok(me2, emit)))
    import yaml
    md = yaml.safe_load(members_text) or {}
    md.setdefault("members", []).append({"tool": "zz_probe", "member": "a", "index": "dynamodb_no_such_row", "links": ["dynamodb_no_such_row"]})
    mt2 = yaml.safe_dump(md)
    arm("planted mutant refused: a dynamodb_ link naming no entry", bool(unresolved_store_ids(mt2, stems)[0]))


def ac3(tmp):
    if not os.path.isfile(NEW_TEST):
        print("DENOMINATOR: test file %s absent" % NEW_TEST)
        arm("pytest on the new test file and the four existing atom_decomposition files passes with at least %d tests" % (BASELINE_PASSED + NEW_MIN), False, "file absent")
        return
    env = dict(os.environ)
    env["PYTHONPATH"] = AD
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "tests/test_group_links.py"] + OLD_TESTS,
                       cwd=AD, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    need = BASELINE_PASSED + NEW_MIN
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum %d = %d existing + %d new) files=5 in %s" % (p.returncode, n, need, BASELINE_PASSED, NEW_MIN, AD))
    arm("pytest on tests/test_group_links.py and the four existing files passes with at least %d tests" % need, p.returncode == 0 and n >= need,
        "rc=%d passed=%d" % (p.returncode, n))


IDS = {"y3.AC1": ac1, "y3.AC2": ac2, "y3.AC3": ac3}


def main(argv):
    if len(argv) < 2 or argv[1] not in IDS:
        print("usage: y3_check.py %s" % "|".join(sorted(IDS)))
        print("RESULT: FAIL")
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        try:
            IDS[argv[1]](tmp)
        except Exception as exc:  # noqa: BLE001
            arm("the check ran to its end", False, "%s: %s" % (type(exc).__name__, exc))
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if not BAD else "FAIL"))
    return 0 if not BAD else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
