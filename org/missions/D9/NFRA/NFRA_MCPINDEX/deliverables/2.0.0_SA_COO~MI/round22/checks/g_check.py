"""g_check.py <id>: the round-22 (workstream GATEWAY) criteria, run from the repository root. Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL.
Ids: g1.AC1 g1.AC2 g1.AC3 g2.AC1 g2.AC2 g2.AC3 g4.AC1 g4.AC2 g4.AC3 g5.AC1 g5.AC2 g5.AC3. ASCII only; python 3.9.
Every arm drives the worker's CLI (workflows/gateway_battery/*.py) on the issuer's fixtures (round22/fixtures/) and compares to the contract in
decompositions/NFRA_MCPINDEX_DECOMP.round22-GATEWAY.md section R22.2."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.normpath(os.path.join(HERE, "..", "fixtures"))
PKG = os.path.join("workflows", "gateway_battery")
CENSUS_PY = os.path.join(PKG, "gateway_census.py")
COVER_PY = os.path.join(PKG, "index_coverage.py")
BATT_PY = os.path.join(PKG, "tool_battery.py")
SHEET_PY = os.path.join(PKG, "cheatsheet.py")
TESTS = os.path.join(PKG, "tests")

OK = []
BAD = []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def fx(name):
    return os.path.join(FIX, name)


def run(args, timeout=120):
    if args and args[0].endswith(".py") and not os.path.isfile(args[0]):
        return 98, "", "script absent: %s" % args[0]   # python's own rc for a missing file is 2, which an rc-2 arm would read as a refusal
    try:
        p = subprocess.run([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return 99, "", "%s: %s" % (type(exc).__name__, exc)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r", ""), p.stderr.decode("utf-8", "replace").replace("\r", "")


def jload(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def jdump(obj, path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1)


def first_line(out, prefix):
    for ln in out.splitlines():
        if ln.startswith(prefix):
            return ln.strip()
    return None


def pytest_count(testfile, minimum):
    if not os.path.isfile(testfile):
        print("DENOMINATOR: test file %s absent" % testfile)
        return False
    p = subprocess.run([sys.executable, "-m", "pytest", testfile, "-q", "-p", "no:cacheprovider", "--color=no"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum %d) file=%s" % (p.returncode, n, minimum, testfile))
    return p.returncode == 0 and n >= minimum


# ------------------------------------------------------------------------------------------------ g1: census
def g1_ac1(tmp):
    out = os.path.join(tmp, "census.json")
    rc, so, se = run([CENSUS_PY, "census", "--breakdown", fx("breakdown_sample.json"), "--out", out])
    print("DENOMINATOR: fixture breakdown channels=6 kinds bucket2 store1 integration1 native1 undeclared1; tools_distinct=9 pairs=10 segments=2 unindexed=4")
    arm("census rc 0", rc == 0, "rc=%s stderr=%s" % (rc, se[-200:]))
    want = "CENSUS channels=6 bucket=2 store=1 integration=1 native=1 undeclared=1 segments=2 tools=9 pairs=10 unindexed=4"
    arm("stdout line", first_line(so, "CENSUS") == want, "got %r" % first_line(so, "CENSUS"))
    got = jload(out) if os.path.isfile(out) else None
    arm("census JSON equals expected_census.json", got == jload(fx("expected_census.json")), "differs")


def g1_ac2(tmp):
    out = os.path.join(tmp, "grants.json")
    rc, so, se = run([CENSUS_PY, "grants", "--breakdown", fx("breakdown_sample.json"), "--out", out])
    print("DENOMINATOR: fixture holders: 3 named rows (andrew, alyssa) plus 1 population row; 4 channels hold")
    arm("grants rc 0", rc == 0, "rc=%s stderr=%s" % (rc, se[-200:]))
    arm("stdout line", first_line(so, "GRANTS") == "GRANTS principals=2 population_tools=1", "got %r" % first_line(so, "GRANTS"))
    got = jload(out) if os.path.isfile(out) else None
    arm("grants JSON equals expected_grants.json", got == jload(fx("expected_grants.json")), "differs")
    bad_files = {
        "error body": json.dumps({"error": "breakdown unreadable", "reason": "x"}),
        "empty channels": json.dumps({"read_at": "2026-10-19T15:00:00Z", "channels": []}),
        "not json": "this is not json",
        "channel without tools": json.dumps({"read_at": "x", "channels": [{"id": "a", "kind": "bucket"}]}),
    }
    for label, text in bad_files.items():
        p = os.path.join(tmp, "bad.json")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        for sub in ("census", "grants"):
            rc2, _, _ = run([CENSUS_PY, sub, "--breakdown", p, "--out", os.path.join(tmp, "bad_out.json")])
            arm("%s refused by %s (rc 2)" % (label, sub), rc2 == 2, "rc=%s" % rc2)


# ------------------------------------------------------------------------------------------------ g2: coverage gate
def cover(tmp, census=None, members=None, catalog=None, pending=None, channels=(), tag="o"):
    out = os.path.join(tmp, "cov_%s.json" % tag)
    args = [COVER_PY, "--census", census or fx("expected_census.json"), "--members", members or fx("members_min.yaml"),
            "--catalog", catalog or fx("catalog_min.yaml"), "--out", out]
    if pending:
        args += ["--pending", pending]
    for c in channels:
        args += ["--channel", c]
    rc, so, se = run(args)
    doc = jload(out) if os.path.isfile(out) else None
    return rc, so, se, doc


def refset(doc):
    return sorted((r.get("class"), r.get("subject")) for r in (doc or {}).get("refusals", []))


def g2_ac1(tmp):
    print("DENOMINATOR: green fixture census 6 channels, 9 tools; catalog rows under a census channel 4 (retired and unplaced rows excluded)")
    rc, so, se, doc = cover(tmp, pending=fx("pending_min.yaml"), tag="g")
    arm("green rc 0", rc == 0, "rc=%s stderr=%s" % (rc, se[-200:]))
    arm("green stdout", first_line(so, "COVERAGE") == "COVERAGE channels=6 tools=9 rows=4 refusals=0", "got %r" % first_line(so, "COVERAGE"))
    arm("green refusals empty", doc is not None and doc.get("refusals") == [], "refusals=%r" % (doc or {}).get("refusals"))
    rc, so, se, doc = cover(tmp, channels=("opal-data-harvest",), tag="h")
    arm("one channel scope", rc == 0 and first_line(so, "COVERAGE") == "COVERAGE channels=1 tools=2 rows=1 refusals=0", "got %r rc=%s" % (first_line(so, "COVERAGE"), rc))
    p = os.path.join(tmp, "bad.json")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("not json")
    rc, _, _, _ = cover(tmp, census=p, tag="b")
    arm("bad census input rc 2", rc == 2, "rc=%s" % rc)


def g2_ac2(tmp):
    import yaml  # noqa: WPS433
    print("DENOMINATOR: five planted arms over the green fixtures; each must refuse with EXACTLY the expected set")
    cat = yaml.safe_load(open(fx("catalog_min.yaml"), encoding="ascii"))
    mem = yaml.safe_load(open(fx("members_min.yaml"), encoding="ascii"))

    def write(obj, name):
        p = os.path.join(tmp, name)
        with open(p, "w", encoding="ascii", newline="\n") as fh:
            yaml.safe_dump(obj, fh)
        return p

    # P1 the PRD negative arm: a channel with no row and no (c) reason
    c1 = copy.deepcopy(cat)
    c1["silver_datasets"] = [r for r in c1["silver_datasets"] if r.get("bucket") != "opal-data-assets"]
    rc, so, _, doc = cover(tmp, catalog=write(c1, "c1.yaml"), tag="p1")
    arm("P1 channel with no row refuses", rc == 1 and refset(doc) == [("channel_no_row", "opal-data-assets")], "rc=%s refusals=%r" % (rc, refset(doc)))
    # P2 member b
    m2 = copy.deepcopy(mem)
    for e in m2["members"]:
        if e["tool"] == "harvest_read":
            e.clear()
            e.update({"tool": "harvest_read", "member": "b", "owner": "SOME_PROJECT"})
    rc, so, _, doc = cover(tmp, members=write(m2, "m2.yaml"), tag="p2")
    arm("P2 member b refuses", rc == 1 and refset(doc) == [("tool_member_b", "harvest_read")], "rc=%s refusals=%r" % (rc, refset(doc)))
    # P3 a row whose read_tool is not a census tool
    c3 = copy.deepcopy(cat)
    c3["harvest_datasets"].append({"entity": "ghost_row", "bucket": "opal-data-harvest", "read_tool": "ghost_tool", "retired": False})
    rc, so, _, doc = cover(tmp, catalog=write(c3, "c3.yaml"), tag="p3")
    arm("P3 row naming a non-census tool refuses", rc == 1 and refset(doc) == [("row_no_read_tool", "ghost_row")], "rc=%s refusals=%r" % (rc, refset(doc)))
    # P4 a census tool with no member entry
    m4 = copy.deepcopy(mem)
    m4["members"] = [e for e in m4["members"] if e["tool"] != "whoami"]
    rc, so, _, doc = cover(tmp, members=write(m4, "m4.yaml"), tag="p4")
    arm("P4 unclassified tool refuses", rc == 1 and refset(doc) == [("tool_unclassified", "whoami")], "rc=%s refusals=%r" % (rc, refset(doc)))
    # P5 a tool in the undeclared channel that is (a) with no index, and a (c) with no reason
    m5 = copy.deepcopy(mem)
    for e in m5["members"]:
        if e["tool"] == "stray_tool":
            e.clear()
            e.update({"tool": "stray_tool", "member": "a", "index": "none", "links": ["none"]})
        if e["tool"] == "send_email":
            e["reason"] = ""
    rc, so, _, doc = cover(tmp, members=write(m5, "m5.yaml"), tag="p5")
    want = sorted([("tool_a_unlinked", "stray_tool"), ("undeclared_tool", "stray_tool"), ("tool_c_no_reason", "send_email")])
    arm("P5 undeclared tool and empty (c) reason refuse", rc == 1 and refset(doc) == want, "rc=%s refusals=%r" % (rc, refset(doc)))
    arm("refusal records carry class, channel and subject", doc is not None and all(set(("class", "channel", "subject")) <= set(r) for r in doc["refusals"]), "shape")
    arm("denominator block present", doc is not None and set(("channels", "tools", "rows")) <= set(doc.get("denominator", {})), "denominator=%r" % (doc or {}).get("denominator"))


# ------------------------------------------------------------------------------------------------ g4: battery
SCOPE = ("opal-data-harvest", "opal-data-assets", "dynamodb", "ycharts", "m365")


def scope_args():
    a = []
    for c in SCOPE:
        a += ["--channel", c]
    return a


def grade(tmp, results_path, tag, census=None):
    out = os.path.join(tmp, "graded_%s.json" % tag)
    rc, so, se = run([BATT_PY, "grade", "--census", census or fx("expected_census.json"), "--cases", fx("cases_min.json"),
                      "--results", results_path, "--out", out] + scope_args())
    return rc, so, se, (jload(out) if os.path.isfile(out) else None)


def tool_row(doc, tool):
    for t in (doc or {}).get("tools", []):
        if t.get("tool") == tool:
            return t
    return {}


def g4_ac1(tmp):
    print("DENOMINATOR: fixture census 9 tools; 8 in scope (undeclared channel out); 9 cases; green results cover all 9")
    out = os.path.join(tmp, "plan.json")
    rc, so, se = run([BATT_PY, "plan", "--census", fx("expected_census.json"), "--cases", fx("cases_min.json"), "--out", out] + scope_args())
    arm("plan in scope rc 0", rc == 0 and first_line(so, "PLAN") == "PLAN tools=8 cases=9 tools_without_case=0", "rc=%s %r %s" % (rc, first_line(so, "PLAN"), se[-200:]))
    rc, so, se = run([BATT_PY, "plan", "--census", fx("expected_census.json"), "--cases", fx("cases_min.json"), "--out", os.path.join(tmp, "plan_all.json")])
    arm("plan over all channels flags the tool with no case", rc == 1 and first_line(so, "PLAN") == "PLAN tools=9 cases=9 tools_without_case=1", "rc=%s %r" % (rc, first_line(so, "PLAN")))
    rc, so, se, doc = grade(tmp, fx("results_min.json"), "g")
    arm("grade green rc 0", rc == 0, "rc=%s stderr=%s" % (rc, se[-200:]))
    want = "GRADE tools=8 PASS=6 EMPTY-CORRECT=0 REFUSED-CORRECT=1 PREVIEW-ONLY=1 FAIL=0"
    arm("grade stdout", first_line(so, "GRADE") == want, "got %r" % first_line(so, "GRADE"))
    arm("preview-only listed by name", first_line(so, "PREVIEW-ONLY TOOLS") == "PREVIEW-ONLY TOOLS: send_email", "got %r" % first_line(so, "PREVIEW-ONLY TOOLS"))
    arm("per-tool verdicts", tool_row(doc, "harvest_read").get("verdict") == "PASS" and tool_row(doc, "client_get_holdings").get("verdict") == "REFUSED-CORRECT"
        and tool_row(doc, "send_email").get("verdict") == "PREVIEW-ONLY", "tools=%r" % [(t.get("tool"), t.get("verdict")) for t in (doc or {}).get("tools", [])])
    want_doc = jload(fx("graded_min.json"))
    arm("graded file equals graded_min.json on cases, tools, counts, case_counts, preview_only and fails", doc is not None and all(doc.get(k) == want_doc.get(k) for k in ("cases", "tools", "counts", "case_counts", "preview_only", "fails")),
        "differs in %r" % [k for k in ("cases", "tools", "counts", "case_counts", "preview_only", "fails") if (doc or {}).get(k) != want_doc.get(k)])
    cs = {c.get("case_id"): c for c in (doc or {}).get("cases", [])}
    arm("per-case verdicts and the question carried", cs.get("C3", {}).get("verdict") == "EMPTY-CORRECT" and cs.get("C2", {}).get("question") == "Show the latest harvest rows for one ticker",
        "cases=%r" % cs.get("C3"))


def g4_ac2(tmp):
    print("DENOMINATOR: seven planted arms over the green results; each reads FAIL with its class and grade exits 1")
    res = jload(fx("results_min.json"))

    def variant(mutate, tag):
        r = copy.deepcopy(res)
        mutate(r)
        p = os.path.join(tmp, "res_%s.json" % tag)
        jdump(r, p)
        return grade(tmp, p, tag)

    def get(r, cid):
        return [x for x in r["results"] if x["case_id"] == cid][0]

    # G1 the PRD planted broken tool, through the plant subcommand
    pl = os.path.join(tmp, "planted.json")
    rc, so, se = run([BATT_PY, "plant", "--cases", fx("cases_min.json"), "--results", fx("results_min.json"), "--tool", "harvest_read", "--out", pl])
    arm("plant subcommand rc 0", rc == 0 and os.path.isfile(pl), "rc=%s %s" % (rc, se[-200:]))
    rc, so, se, doc = grade(tmp, pl, "g1")
    arm("G1 planted broken tool reads FAIL tool_error", rc == 1 and tool_row(doc, "harvest_read").get("verdict") == "FAIL"
        and tool_row(doc, "harvest_read").get("fail_class") == "tool_error" and "FAIL=1" in (first_line(so, "GRADE") or ""), "rc=%s %r %r" % (rc, first_line(so, "GRADE"), tool_row(doc, "harvest_read")))

    def m2(r):
        get(r, "C1")["source_check"]["agrees"] = False
    rc, so, se, doc = variant(m2, "g2")
    arm("G2 source disagrees", rc == 1 and tool_row(doc, "harvest_list").get("fail_class") == "source_disagrees", "rc=%s %r" % (rc, tool_row(doc, "harvest_list")))

    def m3(r):
        get(r, "C1")["source_check"] = None
    rc, so, se, doc = variant(m3, "g3")
    arm("G3 no source check is not a PASS", rc == 1 and tool_row(doc, "harvest_list").get("fail_class") == "source_unchecked", "rc=%s %r" % (rc, tool_row(doc, "harvest_list")))

    def m4(r):
        get(r, "C8")["sent"] = True
    rc, so, se, doc = variant(m4, "g4")
    arm("G4 a send is a FAIL", rc == 1 and tool_row(doc, "send_email").get("fail_class") == "sent", "rc=%s %r" % (rc, tool_row(doc, "send_email")))

    def m5(r):
        r["results"] = [x for x in r["results"] if x["case_id"] != "C5"]
    rc, so, se, doc = variant(m5, "g5")
    arm("G5 a case not run", rc == 1 and tool_row(doc, "schwab_query").get("fail_class") == "not_run", "rc=%s %r" % (rc, tool_row(doc, "schwab_query")))

    def m6(r):
        get(r, "C6")["rows"] = 0
    rc, so, se, doc = variant(m6, "g6")
    arm("G6 unexpected empty", rc == 1 and tool_row(doc, "mdpf_get_security_classification").get("fail_class") == "unexpected_empty", "rc=%s %r" % (rc, tool_row(doc, "mdpf_get_security_classification")))

    def m7(r):
        get(r, "C4")["status"] = "ok"
        get(r, "C4")["rows"] = 2
    rc, so, se, doc = variant(m7, "g7")
    arm("G7 an ungranted principal that is not refused", rc == 1 and tool_row(doc, "client_get_holdings").get("fail_class") == "not_refused", "rc=%s %r" % (rc, tool_row(doc, "client_get_holdings")))

    def m8(r):
        get(r, "C7")["status"] = "refused"
        get(r, "C7")["rows"] = None
    rc, so, se, doc = variant(m8, "g8")
    arm("G8 an unexpected refusal", rc == 1 and tool_row(doc, "ycharts_search").get("fail_class") == "unexpected_refusal", "rc=%s %r" % (rc, tool_row(doc, "ycharts_search")))
    # a tool in scope with no case at all
    out = os.path.join(tmp, "graded_all.json")
    rc, so, se = run([BATT_PY, "grade", "--census", fx("expected_census.json"), "--cases", fx("cases_min.json"), "--results", fx("results_min.json"), "--out", out])
    doc = jload(out) if os.path.isfile(out) else None
    arm("G9 a census tool with no case reads FAIL no_case", rc == 1 and tool_row(doc, "stray_tool").get("fail_class") == "no_case", "rc=%s %r" % (rc, tool_row(doc, "stray_tool")))


# ------------------------------------------------------------------------------------------------ g5: cheat sheet
def sheet(tmp, employee, graded, out_dir, roster=True, census=None, grants=None):
    args = [SHEET_PY, "gen", "--census", census or fx("expected_census.json"), "--grants", grants or fx("expected_grants.json"), "--graded", graded,
            "--employee", employee, "--connect", fx("connect_min.md"), "--out", out_dir]
    if roster:
        args += ["--roster", fx("roster_min.txt")]
    return run(args)


def g5_ac1(tmp):
    print("DENOMINATOR: fixture grants 2 principals (alyssa 2 tools in 2 channels; andrew 7 tools in 4 channels); roster 4 emails")
    gp = fx("graded_min.json")
    d1 = os.path.join(tmp, "s1")
    rc, so, se = sheet(tmp, "alyssa@opalinvest.com", gp, d1)
    arm("alyssa rc 0", rc == 0, "rc=%s %s" % (rc, se[-200:]))
    arm("alyssa SHEET line", first_line(so, "SHEET") == "SHEET employee=alyssa@opalinvest.com channels=2 tools=2 examples=3", "got %r" % first_line(so, "SHEET"))
    arm("ROSTER line beside the sheet count", first_line(so, "ROSTER") == "ROSTER employees=4 with_live_grant=2 without=2", "got %r" % first_line(so, "ROSTER"))
    sp = os.path.join(d1, "alyssa.md")
    text = open(sp, encoding="utf-8").read() if os.path.isfile(sp) else ""
    arm("sheet opens with the connect text", "CONNECT-FIXTURE-LINE" in text and "REFUSAL-FIXTURE-LINE" in text and text.find("CONNECT-FIXTURE-LINE") < text.find("### "), "no connect text before the first tool")
    arm("her tools and tested examples present", "### harvest_read" in text and "Show the latest harvest rows for one ticker" in text and "Show harvest rows for a date that has none" in text and "### whoami" in text and "Who am I signed in as" in text, "missing")
    arm("NEGATIVE ARM: no tool of a bucket she is not granted", text != "" and all(t not in text for t in ("client_get_holdings", "schwab_query", "ycharts_search", "send_email", "mdpf_get_security_classification", "harvest_list")), "a tool outside her grant is listed")
    d2 = os.path.join(tmp, "s2")
    rc, so, se = sheet(tmp, "andrew@opalinvest.com", gp, d2)
    arm("andrew SHEET line", rc == 0 and first_line(so, "SHEET") == "SHEET employee=andrew@opalinvest.com channels=4 tools=7 examples=6", "rc=%s got %r" % (rc, first_line(so, "SHEET")))
    atext = open(os.path.join(d2, "andrew.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(d2, "andrew.md")) else ""
    arm("sending tool is named PREVIEW-ONLY, never given an example", "### send_email" in atext and "PREVIEW-ONLY" in atext and "Draft an email to myself without sending it" not in atext, "send_email handling")
    arm("a refused-only tool carries no example", "### client_get_holdings" in atext and "Show another firm's holdings" not in atext, "refused case question shown")
    ex = os.path.join(d2, "andrew.examples.json")
    exd = jload(ex) if os.path.isfile(ex) else None
    arm("examples.json lists exactly the sheet's examples", isinstance(exd, list) and len(exd) == 6 and all(set(("tool", "question", "case_id")) <= set(x) for x in exd), "examples=%r" % exd)


def g5_ac2(tmp):
    print("DENOMINATOR: determinism over two runs; employee with no live grant; a planted FAIL tool; no roster")
    gp = fx("graded_min.json")
    a, b = os.path.join(tmp, "r1"), os.path.join(tmp, "r2")
    sheet(tmp, "andrew@opalinvest.com", gp, a)
    sheet(tmp, "andrew@opalinvest.com", gp, b)
    same = True
    for name in ("andrew.md", "andrew.examples.json"):
        pa, pb = os.path.join(a, name), os.path.join(b, name)
        same = same and os.path.isfile(pa) and os.path.isfile(pb) and open(pa, "rb").read() == open(pb, "rb").read()
    arm("a second run reproduces the same bytes", same, "the two runs differ or a file is absent")
    rc, so, se = sheet(tmp, "bob@opalinvest.com", gp, os.path.join(tmp, "r3"))
    arm("employee with no live grant: rc 2 and NO LIVE GRANT", rc == 2 and "NO LIVE GRANT" in (so + se) and not os.path.isfile(os.path.join(tmp, "r3", "bob.md")), "rc=%s" % rc)
    gp2 = fx("graded_fail_min.json")
    d4 = os.path.join(tmp, "r4")
    rc, so, se = sheet(tmp, "alyssa@opalinvest.com", gp2, d4)
    text = open(os.path.join(d4, "alyssa.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(d4, "alyssa.md")) else ""
    arm("a FAIL tool is flagged KNOWN ISSUE and carries no example", rc == 0 and "KNOWN ISSUE" in text and "Show the latest harvest rows for one ticker" not in text, "rc=%s" % rc)
    rc, so, se = sheet(tmp, "alyssa@opalinvest.com", gp, os.path.join(tmp, "r5"), roster=False)
    arm("no roster: said absent, not zero", rc == 0 and "ROSTER not supplied (claim: absent)" in so, "got %r" % first_line(so, "ROSTER"))


CHECKS = {
    "g1.AC1": lambda t: g1_ac1(t), "g1.AC2": lambda t: g1_ac2(t), "g1.AC3": lambda t: print("") or arm("pytest", pytest_count(os.path.join(TESTS, "test_gateway_census.py"), 6)),
    "g2.AC1": lambda t: g2_ac1(t), "g2.AC2": lambda t: g2_ac2(t), "g2.AC3": lambda t: print("") or arm("pytest", pytest_count(os.path.join(TESTS, "test_index_coverage.py"), 6)),
    "g4.AC1": lambda t: g4_ac1(t), "g4.AC2": lambda t: g4_ac2(t), "g4.AC3": lambda t: print("") or arm("pytest", pytest_count(os.path.join(TESTS, "test_tool_battery.py"), 6)),
    "g5.AC1": lambda t: g5_ac1(t), "g5.AC2": lambda t: g5_ac2(t), "g5.AC3": lambda t: print("") or arm("pytest", pytest_count(os.path.join(TESTS, "test_cheatsheet.py"), 6)),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: g_check.py <%s>" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_g_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
