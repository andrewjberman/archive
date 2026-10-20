"""y1_check.py <id>: the round-25 (workstream GATEWAY) criteria of cell MX-y-1, run from the repository root.
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. Ids: y1.AC1 (probes and the by-key rule on the fixtures),
y1.AC2 (planted negatives, refusals, determinism, the round-24 behavior unchanged without --probes, listing only), y1.AC3 (the unit tests).
ASCII only; python 3.9; standard library only.
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round25-GATEWAY.md section R25.3, Y1 SOURCE COMPARE BY CLASS.
The script directory is workflows/gateway_battery unless the environment names another (Y1_PKG_DIR); the issuer uses that to try a reference."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R25 = os.path.normpath(os.path.join(HERE, ".."))
R24 = os.path.normpath(os.path.join(R25, "..", "round24"))
FIX = os.path.join(R25, "fixtures")
FIX24 = os.path.join(R24, "fixtures")
PKG = os.environ.get("Y1_PKG_DIR") or os.path.join("workflows", "gateway_battery")
SCRIPT = os.path.join(PKG, "source_compare.py")
TESTFILE = os.path.join(PKG, "tests", "test_source_compare_classes.py")
OK, BAD = [], []

NAMES = ["dA", "gA", "gB", "iA", "sA", "uA", "uB", "uC", "uD", "xA"]
ENTRY_KEYS = ["agrees", "answer_as_of", "case_ids", "instrument", "reason", "source", "source_dates", "tool"]
FORBIDDEN = ("get_object", "download_file", "put_object", "delete_object", "copy_object", "upload_file", "write_object")
STDOUT_FULL = "SOURCE tools=10 agrees=5 disagrees=3 unreadable=2"


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


def rbytes(p):
    with open(p, "rb") as fh:
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


def compare(tmp, tag, probes="__default__", cases=None, results=None, routing=None, fake=None, census=None):
    """Run the script on the y1 fixtures (or the given paths); probes: a path, None for no --probes, or the default fixture file."""
    out = os.path.join(tmp, "sc_%s.json" % tag)
    args = [SCRIPT, "--census", census or fx("y1_census.json"), "--routing", routing or fx("y1_routing.json"),
            "--results", results or fx("y1_results.json"), "--cases", cases or fx("y1_cases.json"),
            "--fake", fake or fx("y1_fake.json"), "--out", out]
    if probes == "__default__":
        probes = fx("y1_probes.json")
    if probes is not None:
        args += ["--probes", probes]
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


def mutated(tmp, tag, name, edit):
    """Write a deep copy of fixture `name` after `edit(obj)` and return its path."""
    obj = copy.deepcopy(jload(fx(name)))
    edit(obj)
    path = os.path.join(tmp, "%s_%s" % (tag, name))
    jdump(obj, path)
    return path


# ------------------------------------------------------------------------------------------------ y1.AC1
def y1_ac1(tmp):
    print("DENOMINATOR: 10 fixture tools with an ok result (dA dated s3; gA gB graph, iA integration, sA store, each with a probe; uA uB uC uD undated s3; xA graph with no probe); "
          "expected counts agrees=5 disagrees=3 unreadable=2")
    rc, so, se, out, doc = compare(tmp, "g")
    arm("a disagreement makes rc 1 and the file is written", rc == 1 and doc is not None, "rc=%s %s" % (rc, se[-200:]))
    arm("stdout line", line(so, "SOURCE") == STDOUT_FULL, "got %r" % line(so, "SOURCE"))
    doc = doc or {}
    arm("schema and counts", doc.get("schema") == "gateway_source_compare/1" and doc.get("counts") == {"tools": 10, "agrees": 5, "disagrees": 3, "unreadable": 2},
        "got %r %r" % (doc.get("schema"), doc.get("counts")))
    tools = doc.get("tools", [])
    names = [t.get("tool") for t in tools if isinstance(t, dict)]
    arm("one entry per tool with an ok result, sorted by name", names == NAMES, "got %r" % names)
    arm("every entry has exactly the round-24 keys, string instrument and reason", bool(tools) and all(isinstance(t, dict) and sorted(t.keys()) == ENTRY_KEYS and isinstance(t.get("instrument"), str)
                                                                                                         and t["instrument"].strip() and isinstance(t.get("reason"), str) for t in tools),
        "got %r" % [sorted(t.keys()) for t in tools if isinstance(t, dict) and sorted(t.keys()) != ENTRY_KEYS][:1])
    t = by_tool(doc)
    pr = dict((p["tool"], p) for p in jload(fx("y1_probes.json"))["probes"])
    ga = t.get("gA", {})
    arm("gA (graph probe, values equal after trim): true, source is the first source (graph), instrument and reason are the probe's, no source dates",
        (ga.get("agrees"), ga.get("source"), ga.get("instrument"), ga.get("reason"), ga.get("source_dates"), ga.get("answer_as_of"), ga.get("case_ids")) ==
        (True, {"kind": "graph", "bucket": "graph", "prefix": ""}, pr["gA"]["instrument"], pr["gA"]["fact"], [], "2026-10-16", ["gA-1"]), "got %r" % ga)
    arm("gB (graph probe, values differ): false", t.get("gB", {}).get("agrees") is False and t.get("gB", {}).get("reason") == pr["gB"]["fact"], "got %r" % t.get("gB"))
    arm("iA (integration probe, equal after case folding): true", t.get("iA", {}).get("agrees") is True and t.get("iA", {}).get("source", {}).get("kind") == "integration", "got %r" % t.get("iA"))
    arm("sA (store probe, values differ): false", t.get("sA", {}).get("agrees") is False and t.get("sA", {}).get("source", {}).get("kind") == "store", "got %r" % t.get("sA"))
    xa = t.get("xA", {})
    arm("xA (graph source, no probe): null and the round-24 reason that names the kind and says it is not read here",
        xa.get("agrees") is None and "graph" in str(xa.get("reason")).lower() and "not read here" in str(xa.get("reason")).lower(), "got %r" % xa)
    ua = t.get("uA", {})
    arm("uA (undated s3, the answer's object key is in the listing): true with the reason 'object key present in the listing'",
        ua.get("agrees") is True and ua.get("reason") == "object key present in the listing" and ua.get("source") == {"kind": "s3", "bucket": "bkt-u", "prefix": "pa/"}, "got %r" % ua)
    ub = t.get("uB", {})
    arm("uB (undated s3, the answer's object key is not in a non-empty listing): false with a reason", ub.get("agrees") is False and isinstance(ub.get("reason"), str) and ub["reason"].strip() != "", "got %r" % ub)
    uc = t.get("uC", {})
    arm("uC (undated s3, the answer carries no object key): null with the round-24 undated reason", uc.get("agrees") is None and "undated" in str(uc.get("reason")).lower(), "got %r" % uc)
    ud = t.get("uD", {})
    arm("uD (undated s3, the key lies below the listed level, an s3:// answer string): the key's own directory is listed and the key found -> true",
        ud.get("agrees") is True and ud.get("reason") == "object key present in the listing", "got %r" % ud)
    da = t.get("dA", {})
    arm("dA (dated s3): the round-24 date rule still decides", da.get("agrees") is True and str(da.get("reason")).startswith("answer date") and da.get("source_dates") == ["2026-10-15", "2026-10-16"], "got %r" % da)


# ------------------------------------------------------------------------------------------------ y1.AC2
def y1_ac2(tmp):
    print("DENOMINATOR: round-24 behavior without --probes on the 12-tool round-24 fixtures (bytes and stdout against the frozen y1_r24_expected files); "
          "2 planted flips (a probe answer value, a removed listing key); 8 refusals (absent probes file, wrong schema, class outside graph|integration|store, unknown tool, class that does not match the tool's first source kind, two probes for one tool, a probe for a tool with no ok result, an empty probe field); determinism over 2 runs; no object read or write in the script")
    out24 = os.path.join(tmp, "r24.json")
    rc, so, se = run([SCRIPT, "--census", os.path.join(FIX24, "w1_census.json"), "--routing", os.path.join(FIX24, "w1_routing.json"), "--results", os.path.join(FIX24, "w1_results.json"),
                      "--cases", os.path.join(FIX24, "w1_cases.json"), "--fake", os.path.join(FIX24, "w1_fake.json"), "--out", out24])
    exp_json, exp_out = os.path.join(FIX, "y1_r24_expected.json"), os.path.join(FIX, "y1_r24_expected.stdout")
    same_bytes = os.path.isfile(out24) and rbytes(out24) == rbytes(exp_json)
    same_out = so == rbytes(exp_out).decode("utf-8", "replace").replace("\r", "")
    arm("without --probes the round-24 fixtures give the same output bytes, the same stdout and rc 1 as the frozen round-24 run", rc == 1 and same_bytes and same_out,
        "rc=%s bytes_equal=%s stdout_equal=%s %s" % (rc, same_bytes, same_out, se[-120:]))
    # planted flips
    p1 = mutated(tmp, "flip", "y1_probes.json", lambda o: o["probes"][0].update(answer_value="13"))
    rc, so, se, out, doc = compare(tmp, "flip", probes=p1)
    arm("planted: gA's answer value moved off the probe value reads false and the counts follow",
        rc == 1 and by_tool(doc).get("gA", {}).get("agrees") is False and line(so, "SOURCE") == "SOURCE tools=10 agrees=4 disagrees=4 unreadable=2", "rc=%s %r %r" % (rc, line(so, "SOURCE"), by_tool(doc).get("gA", {}).get("agrees")))
    f1 = mutated(tmp, "nokey", "y1_fake.json", lambda o: o.update({"bkt-u|pa/": [{"Contents": [{"Key": "pa/other.csv"}], "IsTruncated": False}]}))
    rc, so, se, out, doc = compare(tmp, "nokey", fake=f1)
    arm("planted: the answer's key removed from a non-empty listing turns uA true -> false", rc == 1 and by_tool(doc).get("uA", {}).get("agrees") is False and line(so, "SOURCE") == "SOURCE tools=10 agrees=4 disagrees=4 unreadable=2",
        "rc=%s %r" % (rc, line(so, "SOURCE")))

    # refusals: exit 2 and no output file
    def refused(tag, label, probes_path=None, results=None):
        rc, so, se, out, doc = compare(tmp, tag, probes=probes_path, results=results) if probes_path is not None else (None,) * 5
        # the script's own refusal text is required: an argparse "unrecognized arguments" error also exits 2 and must not pass these arms
        arm(label, rc == 2 and not os.path.isfile(out) and "REFUSED:" in (se or ""), "rc=%s exists=%s %s" % (rc, os.path.isfile(out), (se or "")[-140:]))

    refused("absent", "a --probes file that does not exist exits 2 and writes nothing", os.path.join(tmp, "absent_probes.json"))
    refused("schema", "a probes file with another schema string exits 2", mutated(tmp, "schema", "y1_probes.json", lambda o: o.update(schema="gateway_source_probes/0")))
    refused("cls", "a probe class outside graph, integration, store exits 2", mutated(tmp, "cls", "y1_probes.json", lambda o: o["probes"][0].update(**{"class": "s3"})))
    refused("tool", "a probe for a tool that is not in the census exits 2", mutated(tmp, "tool", "y1_probes.json", lambda o: o["probes"][0].update(tool="zzNotATool")))
    refused("kind", "a probe whose class does not match the tool's first source kind exits 2", mutated(tmp, "kind", "y1_probes.json", lambda o: o["probes"][0].update(**{"class": "store"})))
    refused("dup", "two probes for one tool exit 2", mutated(tmp, "dup", "y1_probes.json", lambda o: o["probes"].append(copy.deepcopy(o["probes"][0]))))
    res_no_xa = mutated(tmp, "noxa", "y1_results.json", lambda o: o.update(results=[r for r in o["results"] if r["case_id"] != "xA-1"]))
    probe_xa = mutated(tmp, "pxa", "y1_probes.json", lambda o: o["probes"].append({"tool": "xA", "class": "graph", "instrument": "i", "fact": "f", "value": "1", "answer_value": "1"}))
    refused("noresult", "a probe for a tool with no ok result exits 2", probe_xa, results=res_no_xa)
    refused("empty", "a probe with an empty field exits 2", mutated(tmp, "empty", "y1_probes.json", lambda o: o["probes"][0].update(fact="  ")))
    # determinism and listing only
    rc1, so1, se1, out1, d1 = compare(tmp, "d1")
    rc2, so2, se2, out2, d2 = compare(tmp, "d2")
    same = os.path.isfile(out1) and os.path.isfile(out2) and rbytes(out1) == rbytes(out2) and so1 == so2
    arm("two runs on the same input give the same bytes and the same stdout", bool(same) and rc1 == rc2 == 1, "rc=%s,%s" % (rc1, rc2))
    text = ""
    if os.path.isfile(SCRIPT):
        with open(SCRIPT, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    arm("the script holds no object read or write call (listing only) and has a --probes option", bool(text) and not any(tok in text for tok in FORBIDDEN) and "list_objects_v2" in text and "--probes" in text,
        "script absent" if not text else "found %r" % [tok for tok in FORBIDDEN if tok in text])


CHECKS = {
    "y1.AC1": y1_ac1,
    "y1.AC2": y1_ac2,
    "y1.AC3": lambda t: arm("pytest", pytest_count(TESTFILE, 8)),
}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: y1_check.py <%s>" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    with tempfile.TemporaryDirectory(prefix="mx_y1_") as tmp:
        CHECKS[cid](tmp)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
