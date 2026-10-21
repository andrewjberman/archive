"""u3_check.py <id>: the round-27 (workstream GATEWAY) criteria of cell MX-u-3 (cheatsheet.py gen-all --platform-labels), run from the
repository root. Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. Ids: u3.AC1, u3.AC2, u3.AC3. ASCII only; python 3.9.
The contract is the U3 SHEETS LABELS SECTION paragraph of decompositions/NFRA_MCPINDEX_DECOMP.round27-GATEWAY.md as restated in
section 1 of the task order NFRA_MCPINDEX.TO-MX-u-3.sheets-labels.md (the order's text wins where they differ).
U3_PKG_DIR (optional) names the folder holding cheatsheet.py and tests/ (default workflows/gateway_battery); the issuer used it to
point the check at a scratch reference. Inputs: the round-24 w7 fixtures, the round-27 u3_labels.json and the frozen round-25 outputs
u3_base/ (what gen-all wrote on the w7 fixtures before this cell), planted into copies at run time."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R27 = os.path.normpath(os.path.join(HERE, ".."))
FIX7 = os.path.normpath(os.path.join(R27, "..", "round24", "fixtures"))
FIX = os.path.join(R27, "fixtures")
BASE = os.path.join(FIX, "u3_base")
PKG = os.environ.get("U3_PKG_DIR") or os.path.join("workflows", "gateway_battery")
SCRIPT = os.path.join(PKG, "cheatsheet.py")
TESTS = os.path.join(PKG, "tests")
OK, BAD = [], []

SHEETS_LINE = "SHEETS people=4 written=4 legacy=3 placeholder=1"
HEADING = "## Platform labels"
MISSING = "platform label not recorded in the labels file"
FIVE = ["client_get_allocation", "client_get_fees", "client_get_holdings", "client_get_transactions", "client_resolve_account"]
NET_WORDS = ("socket", "urllib", "http.client", "requests", "boto3", "ftplib", "smtplib", "subprocess", "upload_text_to_site(")


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def read(p):
    with open(p, encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def jload(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def jdump(o, p):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(o, fh, indent=1)


def run(args, timeout=180):
    if args and args[0].endswith(".py") and not os.path.isfile(args[0]):
        return 98, "", "script absent: %s" % args[0]
    try:
        p = subprocess.run([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return 99, "", "%s: %s" % (type(exc).__name__, exc)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r", ""), p.stderr.decode("utf-8", "replace").replace("\r", "")


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


def tree(root):
    got = []
    for d, _dirs, files in os.walk(root):
        for f in files:
            got.append(os.path.relpath(os.path.join(d, f), root).replace("\\", "/"))
    return sorted(got)


def snapshot(root, skip=("out_", "man_")):
    got = {}
    for rel in tree(root):
        if not rel.startswith(skip):
            got[rel] = read(os.path.join(root, rel))
    return got


def stage(tmp, labels, grants=None):
    """Copy the w7 fixtures into <tmp>/in; labels is a dict written as in/u3_labels.json (or None); grants optionally replaced."""
    ind = os.path.join(tmp, "in")
    os.makedirs(ind, exist_ok=True)
    for n in ("w7_census.json", "w7_tiers.json", "w7_grants.json", "w7_graded.json", "w7_connect.md", "w7_roster.txt", "w7_relevance.json"):
        with open(os.path.join(FIX7, n), "rb") as src, open(os.path.join(ind, n), "wb") as dst:
            dst.write(src.read())
    if grants is not None:
        jdump(grants, os.path.join(ind, "w7_grants.json"))
    if labels is not None:
        jdump(labels, os.path.join(ind, "u3_labels.json"))
    p = os.path.join
    return ["--census", p(ind, "w7_census.json"), "--grants", p(ind, "w7_grants.json"), "--tier-decisions", p(ind, "w7_tiers.json"),
            "--graded", p(ind, "w7_graded.json"), "--connect", p(ind, "w7_connect.md"), "--roster", p(ind, "w7_roster.txt"),
            "--relevance", p(ind, "w7_relevance.json")], os.path.join(ind, "u3_labels.json")


def gen_all(tmp, tag, option=True, manifest=False, labels=None, grants=None, labels_path=None):
    """gen-all into <tmp>/out_<tag>; returns rc, stdout, stderr, out dir, manifest path, and whether every file outside out_* and man_* is unchanged."""
    out = os.path.join(tmp, "out_" + tag)
    mpath = os.path.join(tmp, "man_%s.json" % tag)
    tail, lpath = stage(tmp, labels if labels is not None else (jload(os.path.join(FIX, "u3_labels.json")) if option else None), grants)
    before = snapshot(tmp)
    argv = [SCRIPT, "gen-all"] + tail + ["--out-dir", out]
    if option:
        argv += ["--platform-labels", labels_path or lpath]
    if manifest:
        argv += ["--upload-manifest", mpath]
    rc, so, se = run(argv)
    return rc, so, se, out, mpath, before == snapshot(tmp)


def andrew_all_five():
    g = jload(os.path.join(FIX7, "w7_grants.json"))
    for p in g["principals"]:
        if p["who"].lower() == "andrew@opalinvest.com":
            p["by_channel"]["opal-data-assets"] = list(FIVE)
    return g


def no_client_grants():
    g = jload(os.path.join(FIX7, "w7_grants.json"))
    for p in g["principals"]:
        p["by_channel"] = dict((ch, [t for t in tl if not t.startswith("client_")]) for ch, tl in p["by_channel"].items() if [t for t in tl if not t.startswith("client_")])
    return g


def expected_section(labels, tools):
    """The contract's section for the client_ tools a sheet lists, written independently of the script."""
    by = {}
    for it in labels["items"]:
        by.setdefault(it["tool"], []).append(it)
    lines = []
    for t in sorted(tools):
        rows = sorted(by.get(t, []), key=lambda x: x["adapter"])
        if not rows:
            lines.append("- %s: %s" % (t, MISSING))
        elif len(rows) == 1:
            lines.append("- %s: platform: %s | omit: %s" % (t, rows[0]["platform_meaning"], rows[0]["omit_means"]))
        else:
            for r in rows:
                lines.append("- %s [%s]: platform: %s | omit: %s" % (t, r["adapter"], r["platform_meaning"], r["omit_means"]))
    return "\n" + HEADING + "\n\n" + "\n".join(lines) + "\n"


def same_tree(a, b):
    return os.path.isdir(a) and os.path.isdir(b) and tree(a) == tree(b) and all(read(os.path.join(a, f)) == read(os.path.join(b, f)) for f in tree(a))


# ------------------------------------------------------------------------------------------------ u3.AC1
def ac1(tmp):
    labels = jload(os.path.join(FIX, "u3_labels.json"))
    print("DENOMINATOR: gen-all over the round-24 w7 fixtures (4 people; only the profile person lists a client_ tool) against the frozen round-25 outputs, then a planted grants copy listing all five client_ tools, with the 6 item hand-made u3_labels.json (client_get_holdings answered by two adapters)")
    rc0, so0, se0, out0, _m0, _s0 = gen_all(tmp, "p", option=False)
    base_files = tree(BASE)
    arm("control: gen-all without the option writes exactly the frozen round-25 files (8 files, byte for byte) and the SHEETS line",
        rc0 == 0 and so0.strip() == SHEETS_LINE and same_tree(out0, BASE) and len(base_files) == 8, "rc=%s %r %s" % (rc0, so0.strip(), se0[-200:]))
    rc, so, se, out, _mp, _same = gen_all(tmp, "a")
    arm("with --platform-labels the command exits 0 and prints exactly the SHEETS line", rc == 0 and so.strip() == SHEETS_LINE, "rc=%s %r %s" % (rc, so[-200:], se[-200:]))
    have = rc == 0 and os.path.isdir(out)
    got = {}
    if have:
        for f in tree(out):
            got[f] = read(os.path.join(out, f))
    held = dict((f, read(os.path.join(BASE, f))) for f in base_files)
    arm("the sheets and examples files of people who list no client_ tool, and every examples file, are byte-identical to the frozen outputs",
        have and all(got.get(f) == held[f] for f in held if f != "andrew.md"), "differs: %r" % [f for f in held if f != "andrew.md" and got.get(f) != held[f]])
    arm("the profile person's sheet is the frozen sheet plus exactly the section for client_get_holdings (one line per adapter, sorted by adapter)",
        have and got.get("andrew.md") == held["andrew.md"] + expected_section(labels, ["client_get_holdings"]), "got tail %r" % (got.get("andrew.md") or "")[-400:])
    # a planted grants copy: the profile person lists all five client_ tools
    rcn, _son, _sen, outn, _mn, _sn = gen_all(tmp, "n", option=False, grants=andrew_all_five())
    rc5, so5, se5, out5, _m5, _s5 = gen_all(tmp, "f", grants=andrew_all_five())
    five_ok = rcn == 0 and rc5 == 0 and os.path.isdir(out5)
    plain = read(os.path.join(outn, "andrew.md")) if rcn == 0 else None
    sheet5 = read(os.path.join(out5, "andrew.md")) if five_ok else None
    arm("all five client_ tools listed: the sheet is the plain sheet plus the exact section (tools sorted, a tool with two adapters on two lines sorted by adapter)",
        five_ok and sheet5 == plain + expected_section(labels, FIVE), "got tail %r" % (sheet5 or "")[-500:])
    arm("the section is the last thing in the sheet, the heading appears exactly once, and the sheet is ASCII with no CR",
        five_ok and sheet5.count(HEADING) == 1 and sheet5.rstrip("\n").splitlines()[-1].startswith("- client_") and all(ord(c) < 128 for c in sheet5) and "\r" not in sheet5)
    # the file's own order does not matter
    rev = copy.deepcopy(labels)
    rev["items"] = list(reversed(rev["items"]))
    rcr, _sor, _ser, outr, _mr, _sr = gen_all(tmp, "r", labels=rev, grants=andrew_all_five())
    arm("a labels file listing its items in reverse order gives the same sheets", five_ok and rcr == 0 and same_tree(out5, outr))
    # a listed tool the file does not describe
    miss = copy.deepcopy(labels)
    miss["items"] = [it for it in miss["items"] if it["tool"] != "client_get_fees"]
    rcm, _som, _sem, outm, _mm, _sm = gen_all(tmp, "m", labels=miss, grants=andrew_all_five())
    arm("a listed client_ tool with no item in the file gets the line '- <tool>: %s'" % MISSING,
        rcm == 0 and read(os.path.join(outm, "andrew.md")) == plain + expected_section(miss, FIVE) and ("- client_get_fees: " + MISSING) in read(os.path.join(outm, "andrew.md")))
    # a grants copy with no client_ tool anywhere: no sheet changes
    rcz, _soz, _sez, outz, _mz, _sz = gen_all(tmp, "z0", option=False, grants=no_client_grants())
    rcy, _soy, _sey, outy, _my, _sy = gen_all(tmp, "z1", grants=no_client_grants())
    arm("sheets that list no client_ tool carry no section: with the option and no client_ tool granted anywhere every file equals the run without it",
        rcz == 0 and rcy == 0 and same_tree(outz, outy) and HEADING not in "".join(read(os.path.join(outy, f)) for f in tree(outy)))


# ------------------------------------------------------------------------------------------------ u3.AC2
def refusal_arm(why, tmp, tag, labels=None, labels_path=None):
    """The same inputs without the option succeed; with it, rc 2, one ERROR line, nothing written (no out dir content, no manifest)."""
    rcc, _soc, _sec, _outc, _mc, _sc = gen_all(tmp, tag + "c", option=False)
    rc, _so, se, out, mpath, same = gen_all(tmp, tag, manifest=True, labels=labels, labels_path=labels_path)
    errs = [ln for ln in se.splitlines() if ln.strip()]
    arm("refusal: %s -> rc 2, one ERROR line, nothing written (the same inputs without the option succeed)" % why,
        rcc == 0 and rc == 2 and len(errs) >= 1 and errs[0].startswith("ERROR:") and "usage:" not in se
        and not (os.path.isdir(out) and tree(out)) and not os.path.exists(mpath) and same, "control rc=%s; rc=%s %r out=%s man=%s" % (rcc, rc, se[-200:], os.path.isdir(out), os.path.exists(mpath)))


def mutated(edit):
    d = jload(os.path.join(FIX, "u3_labels.json"))
    edit(d)
    return d


def ac2(tmp):
    print("DENOMINATOR: regression against the frozen round-25 outputs, determinism, the manifest, the write set and 8 refusals (each with a control run without the option) on the w7 fixtures and the hand-made u3_labels.json")
    rc0, so0, _se0, out0, _m0, _s0 = gen_all(tmp, "p", option=False, manifest=True)
    arm("regression: gen-all without the option but with --upload-manifest still writes exactly the frozen round-25 sheets",
        rc0 == 0 and so0.strip() == SHEETS_LINE and all(read(os.path.join(out0, f)) == read(os.path.join(BASE, f)) for f in tree(BASE)) and tree(out0) == tree(BASE))
    rc, so, se, out, mpath, same = gen_all(tmp, "a", manifest=True, grants=andrew_all_five())
    have = rc == 0 and os.path.isfile(mpath)
    arm("both options together exit 0 and print exactly the SHEETS line", rc == 0 and so.strip() == SHEETS_LINE, "rc=%s %r %s" % (rc, so[-200:], se[-200:]))
    man = jload(mpath) if have else {}
    files = man.get("files") if isinstance(man.get("files"), list) else []
    by = dict((f.get("filename"), f) for f in files)
    arm("the upload manifest carries the sheets as written, the Platform labels section included, and its bytes are the UTF-8 length",
        have and "andrew.md" in by and HEADING in by["andrew.md"].get("content", "") and by["andrew.md"]["content"] == read(os.path.join(out, "andrew.md"))
        and by["andrew.md"].get("bytes") == len(by["andrew.md"]["content"].encode("utf-8")) and sorted(by) == tree(out))
    rc2, _so2, _se2, out2, mpath2, _s2 = gen_all(tmp, "b", manifest=True, grants=andrew_all_five())
    arm("two runs give byte-identical sheets and manifests", have and rc2 == 0 and same_tree(out, out2) and read(mpath) == read(mpath2))
    arm("nothing is written outside --out-dir and the manifest path (every other file under the work folder is byte-identical before and after the run)", have and same)
    if os.path.isfile(SCRIPT):
        src = read(SCRIPT)
        arm("the script reads no network and uploads nothing: none of %s appears in it" % ", ".join(NET_WORDS), not [w for w in NET_WORDS if w in src], "found %r" % [w for w in NET_WORDS if w in src])
    else:
        arm("the script exists", False, "absent: %s" % SCRIPT)
    refusal_arm("a wrong schema string", tmp, "s", labels=mutated(lambda d: d.update(schema="gateway_platform_labels/0")))
    refusal_arm("an item without platform_meaning", tmp, "f", labels=mutated(lambda d: d["items"][0].pop("platform_meaning")))
    refusal_arm("an item naming a tool outside the client_ tools", tmp, "t", labels=mutated(lambda d: d["items"][0].update(tool="whoami")))
    refusal_arm("a non-ASCII character in a text field", tmp, "n", labels=mutated(lambda d: d["items"][0].update(omit_means=d["items"][0]["omit_means"] + " caf" + chr(233))))
    refusal_arm("a line break inside a text field", tmp, "l", labels=mutated(lambda d: d["items"][0].update(platform_meaning="first part\nsecond part of the meaning text")))
    refusal_arm("two items for one (tool, adapter)", tmp, "d", labels=mutated(lambda d: d["items"].append(dict(d["items"][0])) or d))
    refusal_arm("an items value that is not a list", tmp, "i", labels=mutated(lambda d: d.update(items={"x": 1})))
    refusal_arm("a labels file that does not exist", tmp, "x", labels_path=os.path.join(tmp, "no_such_labels.json"))


CHECKS = {
    "u3.AC1": ac1, "u3.AC2": ac2,
    "u3.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_cheatsheet_labels.py"), 6)),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: u3_check.py <%s>" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_u3_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
