"""y6_check.py <id>: the round-25 (workstream GATEWAY) criteria of cell MX-y-6 (cheatsheet.py gen-all --upload-manifest), run from the
repository root. Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. Ids: y6.AC1, y6.AC2, y6.AC3. ASCII only; python 3.9.
The contract is the Y6 SHEETS UPLOAD MANIFEST paragraph of decompositions/NFRA_MCPINDEX_DECOMP.round25-GATEWAY.md as restated in
section 1 of the task order NFRA_MCPINDEX.TO-MX-y-6.sheets-upload-manifest.md (the order's text wins where they differ).
Y6_PKG_DIR (optional) names the folder holding cheatsheet.py and tests/ (default workflows/gateway_battery); the issuer used it to
point the check at a scratch reference. Inputs: the round-24 w7 fixtures, planted into copies at run time."""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R25 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.normpath(os.path.join(R25, "..", "round24", "fixtures"))
PKG = os.environ.get("Y6_PKG_DIR") or os.path.join("workflows", "gateway_battery")
SCRIPT = os.path.join(PKG, "cheatsheet.py")
TESTS = os.path.join(PKG, "tests")
OK, BAD = [], []

FOLDER = "Opal Gateway Cheat Sheets"
NAME_RE = re.compile(r"^[A-Za-z0-9._-]+\.(md|json)$")
SHEETS_LINE = "SHEETS people=4 written=4 legacy=3 placeholder=1"
ALL12 = {"client_get_holdings", "etfs_get_fund_snapshot", "etfs_who_holds", "harvest_read", "news_for_security", "portal_get_macro",
         "news_market_mood", "news_search_articles", "schwab_list_files", "opal_discover", "whoami", "send_email"}
COMMON = {"whoami", "opal_discover"}
EXPECT = {
    "andrew": ALL12,
    "ellen": {"etfs_get_fund_snapshot", "etfs_who_holds", "news_for_security", "news_market_mood", "news_search_articles"} | COMMON,
    "frank": {"portal_get_macro", "news_market_mood", "news_for_security", "news_search_articles"} | COMMON,
    "gina": {"harvest_read"} | COMMON,
}
NET_WORDS = ("socket", "urllib", "http.client", "requests", "boto3", "ftplib", "smtplib", "subprocess", "upload_text_to_site(")


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def fx(name):
    return os.path.join(FIX, name)


def run(args, timeout=180):
    if args and args[0].endswith(".py") and not os.path.isfile(args[0]):
        return 98, "", "script absent: %s" % args[0]
    try:
        p = subprocess.run([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return 99, "", "%s: %s" % (type(exc).__name__, exc)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r", ""), p.stderr.decode("utf-8", "replace").replace("\r", "")


def jload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def jdump(o, p):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(o, fh, indent=1)


def text_of(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def line(out, prefix):
    for ln in out.splitlines():
        if ln.startswith(prefix):
            return ln.strip()
    return None


def pytest_count(testfile, minimum):
    if not os.path.isfile(testfile):
        print("DENOMINATOR: test file %s absent" % testfile)
        return False
    p = subprocess.run([sys.executable, "-m", "pytest", testfile, "-q", "-p", "no:cacheprovider", "--color=no"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum %d) file=%s" % (p.returncode, n, minimum, testfile))
    return p.returncode == 0 and n >= minimum


def stage(tmp, graded=None, roster=None, relevance=None):
    """Copy the w7 fixtures into <tmp>/in (optionally replacing graded, roster or relevance) and return the gen-all argv tail."""
    ind = os.path.join(tmp, "in")
    os.makedirs(ind, exist_ok=True)
    for n in ("w7_census.json", "w7_tiers.json", "w7_grants.json", "w7_graded.json", "w7_connect.md", "w7_roster.txt", "w7_relevance.json"):
        with open(fx(n), "rb") as src, open(os.path.join(ind, n), "wb") as dst:
            dst.write(src.read())
    if graded is not None:
        jdump(graded, os.path.join(ind, "w7_graded.json"))
    if relevance is not None:
        jdump(relevance, os.path.join(ind, "w7_relevance.json"))
    if roster is not None:
        with open(os.path.join(ind, "w7_roster.txt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(roster)
    p = os.path.join
    return ["--census", p(ind, "w7_census.json"), "--grants", p(ind, "w7_grants.json"), "--tier-decisions", p(ind, "w7_tiers.json"),
            "--graded", p(ind, "w7_graded.json"), "--connect", p(ind, "w7_connect.md"), "--roster", p(ind, "w7_roster.txt"),
            "--relevance", p(ind, "w7_relevance.json")]


def tree(root):
    got = []
    for d, _dirs, files in os.walk(root):
        for f in files:
            got.append(os.path.relpath(os.path.join(d, f), root).replace("\\", "/"))
    return sorted(got)


def snapshot(root, skip=("out_", "man_")):
    got = {}
    for rel in tree(root):
        if rel.startswith(skip):
            continue
        with open(os.path.join(root, rel), "rb") as fh:
            got[rel] = hashlib.sha1(fh.read()).hexdigest()
    return got


def gen_all(tmp, tag, manifest=True, manifest_path=None, **kw):
    """gen-all into <tmp>/out_<tag>, manifest at <tmp>/man_<tag>.json (or manifest_path); returns rc, stdout, stderr, out dir, manifest
    path and whether every file outside the out_* and man_* names is unchanged."""
    out = os.path.join(tmp, "out_" + tag)
    mpath = manifest_path or os.path.join(tmp, "man_%s.json" % tag)
    tail = stage(tmp, **kw)
    before = snapshot(tmp)
    argv = [SCRIPT, "gen-all"] + tail + ["--out-dir", out]
    if manifest:
        argv += ["--upload-manifest", mpath]
    rc, so, se = run(argv)
    return rc, so, se, out, mpath, before == snapshot(tmp)


def tools_in(sheet_text):
    return set(ln[4:].strip() for ln in sheet_text.splitlines() if ln.startswith("### "))


def graded_planted(edit):
    g = jload(fx("w7_graded.json"))
    first = [c for c in g["cases"] if c.get("verdict") in ("PASS", "EMPTY-CORRECT")]
    edit(first[0] if first else g["cases"][0])
    return g


def listed(man):
    return man.get("files") if isinstance(man, dict) and isinstance(man.get("files"), list) else []


# ------------------------------------------------------------------------------------------------ y6.AC1
def ac1(tmp):
    print("DENOMINATOR: gen-all over the round-24 w7 fixture roster (4 people: 1 profile, 3 legacy, 1 placeholder; 12 tool census) with and without --upload-manifest; 8 files expected (a sheet and an examples file per person)")
    rc0, so0, se0, out0, _m0, _s0 = gen_all(tmp, "p", manifest=False)
    n0 = len(tree(out0)) if os.path.isdir(out0) else 0
    arm("control: gen-all without the option is unchanged (SHEETS line, 8 files)", rc0 == 0 and line(so0, "SHEETS") == SHEETS_LINE and n0 == 8,
        "rc=%s %r %s" % (rc0, line(so0, "SHEETS"), se0[-200:]))
    rc, so, se, out, mpath, _same = gen_all(tmp, "a")
    arm("gen-all with --upload-manifest exits 0 and prints exactly the SHEETS line", rc == 0 and so.strip() == SHEETS_LINE, "rc=%s %r %s" % (rc, so[-200:], se[-200:]))
    have = rc == 0 and os.path.isfile(mpath)
    arm("the manifest file is written", have, "absent: %s" % mpath)
    man = jload(mpath) if have else {}
    arm("the manifest has exactly the keys schema, site, folder and files, with the contract values",
        have and sorted(man.keys()) == ["files", "folder", "schema", "site"] and man.get("schema") == "gateway_sheet_upload/1"
        and man.get("site") == "default" and man.get("folder") == FOLDER, "got %r" % sorted(man.keys()))
    files = listed(man)
    want = sorted(["%s.%s" % (p, e) for p in EXPECT for e in ("md", "examples.json")])
    names = [f.get("filename") for f in files]
    arm("it lists one entry per sheet and per examples file, sorted by filename", have and names == want, "got %r" % names)
    arm("every entry has exactly the keys filename, content and bytes", have and bool(files) and all(sorted(f.keys()) == ["bytes", "content", "filename"] for f in files))
    arm("every entry's content is the file written under --out-dir, verbatim, and bytes is its UTF-8 length",
        have and bool(files) and os.path.isdir(out) and all(os.path.isfile(os.path.join(out, f["filename"])) and f["content"] == text_of(os.path.join(out, f["filename"]))
                                                            and f["bytes"] == len(f["content"].encode("utf-8")) for f in files))
    arm("every filename matches [A-Za-z0-9._-]+.(md|json), every content is ASCII and every file is under 200000 bytes",
        have and bool(files) and all(NAME_RE.match(f["filename"]) and all(ord(c) < 128 for c in f["content"]) and f["bytes"] < 200000 for f in files))
    arm("the manifest lists exactly the files written under --out-dir (no more, no fewer)", have and os.path.isdir(out) and sorted(names) == tree(out))
    sheets = {f["filename"][:-3]: f["content"] for f in files if f.get("filename", "").endswith(".md")}
    arm("each listed sheet carries exactly the tools its person is admitted to (access unchanged by the manifest)",
        have and set(sheets) == set(EXPECT) and all(tools_in(sheets[w]) == EXPECT[w] for w in EXPECT), "got %r" % {w: sorted(tools_in(t)) for w, t in sheets.items()})
    arm("the sheets written with the option are byte-identical to those written without it",
        os.path.isdir(out0) and os.path.isdir(out) and tree(out0) == tree(out) and all(text_of(os.path.join(out0, f)) == text_of(os.path.join(out, f)) for f in tree(out0)))


# ------------------------------------------------------------------------------------------------ y6.AC2
def refusal_arm(why, tmp, tag, **kw):
    """The same inputs without the option succeed; with it, rc 2, one ERROR line, nothing written (no out dir content, no manifest)."""
    rcc, _soc, _sec, _outc, _mc, _sc = gen_all(tmp, tag + "c", manifest=False, **kw)
    rc, _so, se, out, mpath, same = gen_all(tmp, tag, **kw)
    errs = [ln for ln in se.splitlines() if ln.strip()]
    arm("refusal: %s -> rc 2, one ERROR line, nothing written (the same inputs without the option succeed)" % why,
        rcc == 0 and rc == 2 and len(errs) >= 1 and errs[0].startswith("ERROR:") and "usage:" not in se
        and not (os.path.isdir(out) and tree(out)) and not os.path.exists(mpath) and same, "control rc=%s; rc=%s %r out=%s man=%s" % (rcc, rc, se[-200:], os.path.isdir(out), os.path.exists(mpath)))


def ac2(tmp):
    print("DENOMINATOR: guards, determinism, write set and no-network over the same 4 person fixture; 4 refusals each with a control run without the option (an unsafe file name, a non-ASCII character, an oversize file, a missing manifest folder)")
    rc, so, se, out, mpath, same = gen_all(tmp, "a")
    have = rc == 0 and os.path.isfile(mpath)
    arm("the fixture run succeeds and writes the manifest", have, "rc=%s %s" % (rc, se[-200:]))
    rc2, _so2, _se2, out2, mpath2, _s2 = gen_all(tmp, "b")
    arm("two runs give byte-identical manifests and sheets",
        have and rc2 == 0 and os.path.isfile(mpath2) and text_of(mpath) == text_of(mpath2) and tree(out) == tree(out2)
        and all(text_of(os.path.join(out, f)) == text_of(os.path.join(out2, f)) for f in tree(out)))
    arm("nothing is written outside --out-dir and the manifest path (every other file under the work folder is byte-identical before and after the run)", have and same)
    if os.path.isfile(SCRIPT):
        src = text_of(SCRIPT)
        arm("the script never uploads, sends or reads a network: none of %s appears in it" % ", ".join(NET_WORDS), not [w for w in NET_WORDS if w in src], "found %r" % [w for w in NET_WORDS if w in src])
        arm("the script carries the folder name %r" % FOLDER, FOLDER in src)
    else:
        arm("the script exists", False, "absent: %s" % SCRIPT)
    rost = text_of(fx("w7_roster.txt"))
    rel = jload(fx("w7_relevance.json"))
    extra = dict([p for p in rel["people"] if p["who"] == "ellen@opalinvest.com"][0])
    extra["who"] = "bo+x@opalinvest.com"
    rel["people"] = rel["people"] + [extra]
    refusal_arm("an unsafe file name (a roster local part with a plus sign)", tmp, "u", roster=rost.rstrip("\n") + "\nbo+x@opalinvest.com\n", relevance=rel)
    refusal_arm("a non-ASCII character in a sheet", tmp, "n", graded=graded_planted(lambda c: c.update(question=c["question"] + " caf" + chr(233))))
    refusal_arm("a file of 200000 bytes or more", tmp, "o", graded=graded_planted(lambda c: c.update(question=c["question"] + " " + "x" * 250000)))
    rcm, _som, sem, outm, mm, _sm = gen_all(tmp, "m", manifest_path=os.path.join(tmp, "no_such_folder", "man.json"))
    errs = [ln for ln in sem.splitlines() if ln.strip()]
    arm("refusal: a manifest folder that does not exist -> rc 2, one ERROR line, nothing written",
        rcm == 2 and len(errs) >= 1 and errs[0].startswith("ERROR:") and "usage:" not in sem and not (os.path.isdir(outm) and tree(outm)) and not os.path.exists(mm),
        "rc=%s %r" % (rcm, sem[-200:]))


CHECKS = {
    "y6.AC1": ac1, "y6.AC2": ac2,
    "y6.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_cheatsheet_upload.py"), 5)),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: y6_check.py <%s>" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_y6_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
