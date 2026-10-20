"""w7_check.py <id>: the round-24 (workstream GATEWAY) criteria of cell MX-w-7 (cheatsheet.py gen-all), run from the repository root.
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. Ids: w7.AC1, w7.AC2, w7.AC3. ASCII only; python 3.9.
The contract is the W7 SHEETS BATCH paragraph of decompositions/NFRA_MCPINDEX_DECOMP.round24-GATEWAY.md as restated in section 2 of the
task order NFRA_MCPINDEX.TO-MX-w-7.sheets-batch.md (the order's text wins where they differ)."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R24, "fixtures")
PKG = os.path.join("workflows", "gateway_battery")
SCRIPT = os.path.join(PKG, "cheatsheet.py")
TESTS = os.path.join(PKG, "tests")
OK, BAD = [], []

PLACEHOLDER_PREFIX = "PLACEHOLDER SHEET: your role is not recorded yet, so this sheet shows the tools of these buckets: "
ALL12 = {"client_get_holdings", "etfs_get_fund_snapshot", "etfs_who_holds", "harvest_read", "news_for_security", "portal_get_macro",
         "news_market_mood", "news_search_articles", "schwab_list_files", "opal_discover", "whoami", "send_email"}
DENIED = {"client_get_holdings", "schwab_list_files", "send_email"}
COMMON = {"whoami", "opal_discover"}
EXPECT = {
    "andrew": ALL12,
    "ellen": {"etfs_get_fund_snapshot", "etfs_who_holds", "news_for_security", "news_market_mood", "news_search_articles"} | COMMON,
    "frank": {"portal_get_macro", "news_market_mood", "news_for_security", "news_search_articles"} | COMMON,
    "gina": {"harvest_read"} | COMMON,
}


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
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def jdump(o, p):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(o, fh, indent=1)


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


def stage(tmp, relevance=None, roster=None, tiers=None):
    """Copy the fixtures into <tmp>/in (optionally replacing relevance, roster or the tier-decisions path) and return the argv tail."""
    ind = os.path.join(tmp, "in")
    os.makedirs(ind, exist_ok=True)
    for n in ("w7_census.json", "w7_tiers.json", "w7_grants.json", "w7_graded.json", "w7_connect.md", "w7_roster.txt", "w7_relevance.json"):
        shutil.copyfile(fx(n), os.path.join(ind, n))
    if relevance is not None:
        jdump(relevance, os.path.join(ind, "w7_relevance.json"))
    if roster is not None:
        with open(os.path.join(ind, "w7_roster.txt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(roster)
    p = lambda n: os.path.join(ind, n)  # noqa: E731
    return ["--census", p("w7_census.json"), "--grants", p("w7_grants.json"), "--tier-decisions", tiers or p("w7_tiers.json"),
            "--graded", p("w7_graded.json"), "--connect", p("w7_connect.md"), "--roster", p("w7_roster.txt"), "--relevance", p("w7_relevance.json")]


def snapshot(root, skip=("out_",)):
    """path -> sha1 of every file under root, outside the out_* folders."""
    got = {}
    for d, _dirs, files in os.walk(root):
        for f in files:
            rel = os.path.relpath(os.path.join(d, f), root).replace("\\", "/")
            if rel.startswith(skip):
                continue
            with open(os.path.join(d, f), "rb") as fh:
                got[rel] = hashlib.sha1(fh.read()).hexdigest()
    return got


def gen_all(tmp, tag, **kw):
    """Runs gen-all into <tmp>/out_<tag>; returns rc, stdout, stderr, out dir and whether everything outside the out_* folders is unchanged."""
    out = os.path.join(tmp, "out_" + tag)
    tail = stage(tmp, **kw)
    before = snapshot(tmp)
    rc, so, se = run([SCRIPT, "gen-all"] + tail + ["--out-dir", out])
    return rc, so, se, out, before == snapshot(tmp)


def tools_of(sheet_path):
    if not os.path.isfile(sheet_path):
        return None
    with open(sheet_path, encoding="utf-8") as fh:
        return set(ln[4:].strip() for ln in fh.read().splitlines() if ln.startswith("### "))


def text_of(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def tree(root):
    got = []
    for d, _dirs, files in os.walk(root):
        for f in files:
            got.append(os.path.relpath(os.path.join(d, f), root).replace("\\", "/"))
    return sorted(got)


# ------------------------------------------------------------------------------------------------ w7.AC1
def ac1(tmp):
    print("DENOMINATOR: gen-all over a 4 person fixture roster (a profile person with a mixed-case email, two legacy persons with a role, one legacy placeholder person) on a 12 tool census; 12 expected tool names for the profile person")
    rc, so, se, out, _same = gen_all(tmp, "a")
    arm("gen-all exits 0 and prints the SHEETS line", rc == 0 and line(so, "SHEETS") == "SHEETS people=4 written=4 legacy=3 placeholder=1", "rc=%s %r %s" % (rc, line(so, "SHEETS"), se[-200:]))
    names = tree(out) if os.path.isdir(out) else []
    want = sorted(["%s.%s" % (p, e) for p in EXPECT for e in ("md", "examples.json")])
    arm("one sheet and one examples file per roster person, named by the lowercased local part", names == want, "got %r" % names)
    for who in ("andrew", "ellen", "frank", "gina"):
        got = tools_of(os.path.join(out, who + ".md"))
        arm("%s lists exactly the expected tools" % who, got == EXPECT[who], "got %r" % (sorted(got) if got is not None else None))
    cdir = os.path.join(tmp, "gen_out")
    ind = os.path.join(tmp, "in")
    rc2, so2, se2 = run([SCRIPT, "gen", "--census", os.path.join(ind, "w7_census.json"), "--grants", os.path.join(ind, "w7_grants.json"), "--graded", os.path.join(ind, "w7_graded.json"),
                         "--employee", "andrew@opalinvest.com", "--connect", os.path.join(ind, "w7_connect.md"), "--out", cdir])
    arm("the existing gen is unchanged", rc2 == 0 and line(so2, "SHEET ") == "SHEET employee=andrew@opalinvest.com channels=8 tools=12 examples=10", "rc=%s %r" % (rc2, line(so2, "SHEET ")))


# ------------------------------------------------------------------------------------------------ w7.AC2
def ac2(tmp):
    print("DENOMINATOR: legacy rule, placeholder rule, tier choice, examples, determinism, write set and 3 refusals over the same 4 person fixture; every arm needs written files (a failing run cannot pass)")
    rc, so, se, out, _same = gen_all(tmp, "a")
    have = rc == 0 and os.path.isfile(os.path.join(out, "ellen.md"))
    arm("the fixture run succeeds and writes the sheets", have, "rc=%s %s" % (rc, se[-200:]))
    legacy = {}
    for who in ("ellen", "frank", "gina"):
        legacy[who] = tools_of(os.path.join(out, who + ".md"))
    arm("no sheet of a person without a profile lists a client_*, Schwab or Black Diamond tool, or a sender",
        have and all(s is not None and not (s & DENIED) and not any(t.startswith(("client_", "schwab_", "blackdiamond_")) for t in s) for s in legacy.values()),
        "got %r" % {k: sorted(v & DENIED) for k, v in legacy.items() if v})
    arm("the profile person keeps every tool the grant carries, including the data-grant tools", have and tools_of(os.path.join(out, "andrew.md")) == ALL12)
    arm("the news bucket is by tool-name prefix across channels, and a bucket not chosen is left out",
        have and "news_for_security" in legacy["ellen"] and "news_for_security" not in legacy["gina"] and "harvest_read" not in legacy["ellen"])
    texts = {w: text_of(os.path.join(out, w + ".md")) for w in ("andrew", "ellen", "frank", "gina") if os.path.isfile(os.path.join(out, w + ".md"))}
    ph = [ln for ln in texts.get("frank", "").splitlines() if ln.startswith("PLACEHOLDER SHEET")]
    tested = [i for i, ln in enumerate(texts.get("frank", "").splitlines()) if ln.startswith("Tested ")]
    arm("the placeholder person has the exact placeholder line after the Tested line; nobody else has one",
        len(ph) == 1 and ph[0] == PLACEHOLDER_PREFIX + "portal, news." and tested and texts["frank"].splitlines().index(ph[0]) > tested[0]
        and all("PLACEHOLDER SHEET" not in texts.get(w, "x") for w in ("andrew", "ellen", "gina")) and len(texts) == 4, "got %r" % ph)
    ex = os.path.join(out, "ellen.examples.json")
    exs = jload(ex) if os.path.isfile(ex) else []
    arm("the examples list holds only PASS questions of tools on the sheet",
        have and exs != [] and all(e.get("tool") in legacy["ellen"] and e.get("question", "").startswith("Fixture question") for e in exs)
        and not any(e.get("tool") in ("news_search_articles", "send_email") for e in exs), "got %r" % exs[:2])
    rc2, so2, se2, out2, _s2 = gen_all(tmp, "b")
    same = have and rc2 == 0 and tree(out) == tree(out2) and all(text_of(os.path.join(out, f)) == text_of(os.path.join(out2, f)) for f in tree(out))
    arm("two runs give byte-identical files", same)
    arm("nothing is written outside --out-dir (every file outside the out folders is byte-identical before and after the run, and the out folder holds the 8 files)", have and _same and len(tree(out)) == 8)
    rel = jload(fx("w7_relevance.json"))
    for p in rel["people"]:
        if p["who"] == "ellen@opalinvest.com":
            p["tier"] = "standard"
    rc3, so3, se3, out3, _s3 = gen_all(tmp, "t", relevance=rel)
    t3 = tools_of(os.path.join(out3, "ellen.md"))
    arm("a legacy person's tier from the relevance file picks that tier's admit set (standard admits the sender, still not the data-grant tools)",
        rc3 == 0 and t3 is not None and "send_email" in t3 and not (t3 & {"client_get_holdings", "schwab_list_files"}), "rc=%s got %r" % (rc3, sorted(t3) if t3 else None))
    short = jload(fx("w7_relevance.json"))
    short["people"] = [p for p in short["people"] if p["who"] != "gina@opalinvest.com"]
    badb = jload(fx("w7_relevance.json"))
    badb["people"][1]["buckets"] = ["etfs", "not-a-bucket"]
    for tag, kw, why in (("m", {"relevance": short}, "a roster person with no relevance entry"), ("u", {"relevance": badb}, "an unknown bucket name")):
        rcr, sor, ser, outr, _sr = gen_all(tmp, tag, **kw)
        errs = [ln for ln in ser.splitlines() if ln.strip()]
        arm("refusal: %s -> rc 2, one ERROR line, nothing written (the same inputs without the defect succeed)" % why,
            have and rcr == 2 and len(errs) >= 1 and errs[0].startswith("ERROR:") and "usage:" not in ser and not (os.path.isdir(outr) and tree(outr)), "rc=%s %r" % (rcr, ser[-200:]))
    rcu, sou, seu, outu, _su = gen_all(tmp, "x", tiers=os.path.join(tmp, "in", "absent_tiers.json"))
    errs = [ln for ln in seu.splitlines() if ln.strip()]
    arm("refusal: an unreadable tier-decisions file -> rc 2, one ERROR line, nothing written",
        have and rcu == 2 and len(errs) >= 1 and errs[0].startswith("ERROR:") and "usage:" not in seu and not (os.path.isdir(outu) and tree(outu)), "rc=%s %r" % (rcu, seu[-200:]))


CHECKS = {
    "w7.AC1": ac1, "w7.AC2": ac2,
    "w7.AC3": lambda t: arm("pytest", pytest_count(os.path.join(TESTS, "test_cheatsheet_batch.py"), 5)),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: w7_check.py <%s>" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_w7_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
