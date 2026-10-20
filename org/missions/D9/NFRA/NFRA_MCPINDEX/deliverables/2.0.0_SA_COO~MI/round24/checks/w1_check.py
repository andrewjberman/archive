"""w1_check.py <id>: the round-24 (workstream GATEWAY) criteria of cell MX-w-1, run from the repository root.
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. Ids: w1.AC1 (the fixture grade), w1.AC2 (planted negatives,
refusals, determinism, listing only), w1.AC3 (the unit tests). ASCII only; python 3.9; standard library only.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round24-GATEWAY.md section R24.3, W1 SOURCE COMPARE.
The script directory is workflows/gateway_battery unless the environment names another (W1_PKG_DIR); the issuer uses that to try a reference."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R24, "fixtures")
PKG = os.environ.get("W1_PKG_DIR") or os.path.join("workflows", "gateway_battery")
SCRIPT = os.path.join(PKG, "source_compare.py")
TESTFILE = os.path.join(PKG, "tests", "test_source_compare.py")
OK, BAD = [], []

NAMES = ["tA", "tB", "tC", "tD", "tE", "tG", "tH", "tJ", "tK", "tN"]
ENTRY_KEYS = ["agrees", "answer_as_of", "case_ids", "instrument", "reason", "source", "source_dates", "tool"]
FORBIDDEN = ("get_object", "download_file", "put_object", "delete_object", "copy_object", "upload_file", "write_object")


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


def compare(tmp, tag, cases=None, results=None, routing=None, fake=None, census=None):
    """Run the script on the fixtures (or the given paths); return (rc, stdout, stderr, out path, parsed doc or None)."""
    out = os.path.join(tmp, "sc_%s.json" % tag)
    args = [SCRIPT, "--census", census or fx("w1_census.json"), "--routing", routing or fx("w1_routing.json"),
            "--results", results or fx("w1_results.json"), "--cases", cases or fx("w1_cases.json"),
            "--fake", fake or fx("w1_fake.json"), "--out", out]
    rc, so, se = run(args)
    doc = None
    if os.path.isfile(out):
        try:
            doc = jload(out)
        except ValueError:
            doc = None
    return rc, so, se, out, doc


def by_tool(doc):
    return dict((t.get("tool"), t) for t in (doc or {}).get("tools", []) if isinstance(t, dict))


# ------------------------------------------------------------------------------------------------ w1.AC1
def w1_ac1(tmp):
    print("DENOMINATOR: 12 fixture census tools; 12 cases and 12 results (tF has an error result, tI has no case); 10 tools reach the output "
          "(tA tB tC tD tE tG tH tJ tK tN); expected counts agrees=2 disagrees=1 unreadable=7")
    rc, so, se, out, doc = compare(tmp, "g")
    arm("a disagreement makes rc 1 and the file is written", rc == 1 and doc is not None, "rc=%s %s" % (rc, se[-200:]))
    arm("stdout line", line(so, "SOURCE") == "SOURCE tools=10 agrees=2 disagrees=1 unreadable=7", "got %r" % line(so, "SOURCE"))
    doc = doc or {}
    arm("schema and counts", doc.get("schema") == "gateway_source_compare/1" and doc.get("counts") == {"tools": 10, "agrees": 2, "disagrees": 1, "unreadable": 7},
        "got %r %r" % (doc.get("schema"), doc.get("counts")))
    tools = doc.get("tools", [])
    names = [t.get("tool") for t in tools if isinstance(t, dict)]
    arm("one entry per tool with an ok result, sorted by name; an error-only tool and a tool with no result are absent", names == NAMES, "got %r" % names)
    arm("every entry has exactly the contract keys", bool(tools) and all(isinstance(t, dict) and sorted(t.keys()) == ENTRY_KEYS for t in tools),
        "got %r" % [sorted(t.keys()) for t in tools if isinstance(t, dict) and sorted(t.keys()) != ENTRY_KEYS][:1])
    arm("every entry has an instrument and a reason that are strings", bool(tools) and all(isinstance(t.get("instrument"), str) and t["instrument"].strip() and isinstance(t.get("reason"), str) for t in tools))
    t = by_tool(doc)
    a = t.get("tA", {})
    arm("tA: the first ok result with an as_of, both listing pages read, the date found",
        (a.get("case_ids"), a.get("answer_as_of"), a.get("source"), a.get("source_dates"), a.get("agrees")) ==
        (["A-1", "A-2"], "2026-10-16", {"kind": "s3", "bucket": "bkt-a", "prefix": "gold/a/"}, ["2026-10-15", "2026-10-16"], True), "got %r" % a)
    b = t.get("tB", {})
    arm("tB: the answer date is not among the listed dates -> false", (b.get("answer_as_of"), b.get("source_dates"), b.get("agrees")) == ("2026-10-17", ["2026-10-14", "2026-10-15"], False), "got %r" % b)
    c = t.get("tC", {})
    arm("tC: keys with no date token -> null with an undated reason", c.get("agrees") is None and c.get("source_dates") == [] and "undated" in str(c.get("reason")).lower(), "got %r" % c)
    arm("tD, tE, tJ: a store, an integration and a graph source are not read here -> null naming the kind",
        all(t.get(n, {}).get("agrees") is None and t.get(n, {}).get("source", {}).get("kind") == k and k in str(t.get(n, {}).get("reason")).lower() and "not read here" in str(t.get(n, {}).get("reason")).lower()
            for n, k in (("tD", "store"), ("tE", "integration"), ("tJ", "graph"))), "got %r" % [(n, t.get(n)) for n in ("tD", "tE", "tJ")])
    g = t.get("tG", {})
    arm("tG: the source whose bucket and prefix the answer_source string names is chosen (not the first), a YYYYMMDD key counts as a date",
        (g.get("source"), g.get("source_dates"), g.get("agrees")) == ({"kind": "s3", "bucket": "bkt-g2", "prefix": "p2/"}, ["2026-10-16"], True), "got %r" % g)
    h = t.get("tH", {})
    arm("tH: a result with no as_of -> null with a reason that names as_of", h.get("agrees") is None and h.get("answer_as_of") is None and "as_of" in str(h.get("reason")).lower(), "got %r" % h)
    k = t.get("tK", {})
    arm("tK: an empty listing -> null with an empty reason", k.get("agrees") is None and k.get("source_dates") == [] and "empty" in str(k.get("reason")).lower(), "got %r" % k)
    n = t.get("tN", {})
    arm("tN: a routing entry with no source -> source null, null, reason names the missing source", n.get("source") is None and n.get("agrees") is None and "no source" in str(n.get("reason")).lower(), "got %r" % n)


# ------------------------------------------------------------------------------------------------ w1.AC2
def w1_ac2(tmp):
    print("DENOMINATOR: 3 planted inputs (a shifted answer date, a dated listing, a dropped disagreement), 4 refusals (unknown tool, missing routing entry, missing fake file, unreadable results), determinism over 2 runs, no object read or write in the script")
    res = jload(fx("w1_results.json"))
    # 1. a planted answer date that is not in the listing flips tA true -> false
    r1 = copy.deepcopy(res)
    for r in r1["results"]:
        if r["case_id"] == "A-1":
            r["as_of"] = "2026-10-02"
    p1 = os.path.join(tmp, "r_shift.json")
    jdump(r1, p1)
    rc, so, se, out, doc = compare(tmp, "shift", results=p1)
    arm("planted: tA's answer date moved off the listing reads false, and the counts follow",
        rc == 1 and by_tool(doc).get("tA", {}).get("agrees") is False and line(so, "SOURCE") == "SOURCE tools=10 agrees=1 disagrees=2 unreadable=7", "rc=%s %r %r" % (rc, line(so, "SOURCE"), by_tool(doc).get("tA", {}).get("agrees")))
    # 2. a planted dated listing flips tC null -> true
    fk = jload(fx("w1_fake.json"))
    fk["bkt-c|gold/c/"] = [{"Contents": [{"Key": "gold/c/date=2026-10-16/part-0.parquet"}], "IsTruncated": False}]
    p2 = os.path.join(tmp, "f_dated.json")
    jdump(fk, p2)
    rc, so, se, out, doc = compare(tmp, "dated", fake=p2)
    arm("planted: a dated listing under tC turns null into true", rc == 1 and by_tool(doc).get("tC", {}).get("agrees") is True and line(so, "SOURCE") == "SOURCE tools=10 agrees=3 disagrees=1 unreadable=6",
        "rc=%s %r" % (rc, line(so, "SOURCE")))
    # 3. no disagreement: exit 0
    r3 = copy.deepcopy(res)
    r3["results"] = [r for r in r3["results"] if r["case_id"] != "B-1"]
    p3 = os.path.join(tmp, "r_nob.json")
    jdump(r3, p3)
    rc, so, se, out, doc = compare(tmp, "nob", results=p3)
    arm("no disagreement -> exit 0 and the stdout line says so", rc == 0 and line(so, "SOURCE") == "SOURCE tools=9 agrees=2 disagrees=0 unreadable=7", "rc=%s %r" % (rc, line(so, "SOURCE")))
    # 4. unknown tool in the results -> exit 2, nothing written
    cs = jload(fx("w1_cases.json"))
    cs["cases"].append({"case_id": "Z-1", "tool": "tZ", "question": "What is the latest data for fixture tool tZ today", "args": {}, "expect": "nonempty", "source_hint": "fixture"})
    p4c = os.path.join(tmp, "c_z.json")
    jdump(cs, p4c)
    r4 = copy.deepcopy(res)
    r4["results"].append({"case_id": "Z-1", "status": "ok", "rows": 1, "as_of": "2026-10-16", "error_text": None, "sent": False, "source_check": None})
    p4r = os.path.join(tmp, "r_z.json")
    jdump(r4, p4r)
    rc, so, se, out, doc = compare(tmp, "z", cases=p4c, results=p4r)
    arm("a result for a tool that is not in the census exits 2 and writes nothing", rc == 2 and not os.path.isfile(out), "rc=%s exists=%s %s" % (rc, os.path.isfile(out), se[-160:]))
    # 5. missing routing entry -> exit 2
    rt = jload(fx("w1_routing.json"))
    rt["tools"] = [t for t in rt["tools"] if t["tool"] != "tA"]
    p5 = os.path.join(tmp, "rt_nota.json")
    jdump(rt, p5)
    rc, so, se, out, doc = compare(tmp, "nort", routing=p5)
    arm("a tool with results but no routing entry exits 2 and writes nothing", rc == 2 and not os.path.isfile(out), "rc=%s exists=%s" % (rc, os.path.isfile(out)))
    # 6. missing fake file, unreadable results -> exit 2
    rc, so, se, out, doc = compare(tmp, "nofake", fake=os.path.join(tmp, "absent_fake.json"))
    arm("a --fake file that does not exist exits 2", rc == 2 and not os.path.isfile(out), "rc=%s" % rc)
    bad = os.path.join(tmp, "r_bad.json")
    with open(bad, "w", encoding="utf-8") as fh:
        fh.write("{not json")
    rc, so, se, out, doc = compare(tmp, "badres", results=bad)
    arm("an unreadable results file exits 2", rc == 2 and not os.path.isfile(out), "rc=%s" % rc)
    # 7. determinism
    rc1, so1, se1, out1, d1 = compare(tmp, "d1")
    rc2, so2, se2, out2, d2 = compare(tmp, "d2")
    same = os.path.isfile(out1) and os.path.isfile(out2) and open(out1, "rb").read() == open(out2, "rb").read() and so1 == so2
    arm("two runs on the same input give the same bytes and the same stdout", bool(same) and rc1 == rc2 == 1, "rc=%s,%s" % (rc1, rc2))
    # 8. the script lists, it never gets or writes an object
    text = ""
    if os.path.isfile(SCRIPT):
        with open(SCRIPT, encoding="utf-8") as fh:
            text = fh.read()
    arm("the script holds no object read or write call (listing only)", bool(text) and not any(tok in text for tok in FORBIDDEN) and "list_objects_v2" in text,
        "script absent" if not text else "found %r" % [tok for tok in FORBIDDEN if tok in text])


CHECKS = {
    "w1.AC1": w1_ac1,
    "w1.AC2": w1_ac2,
    "w1.AC3": lambda t: arm("pytest", pytest_count(TESTFILE, 6)),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: w1_check.py <%s>" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_w1_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
