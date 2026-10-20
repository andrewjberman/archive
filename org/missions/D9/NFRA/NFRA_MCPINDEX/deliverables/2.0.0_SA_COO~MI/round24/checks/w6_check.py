"""w6_check.py <id>: the round-24 (workstream GATEWAY) criteria of cell MX-w-6, run from the repository root.
Ids: w6.AC1 (the traced serves set on a fixture), w6.AC2 (round-23 behavior unchanged: r1.AC1, r1.AC2 and the live routing table; the new
serves never add a pair the old one lacked, and drop one), w6.AC3 (pytest on tests/test_routing_serves.py). Prints a DENOMINATOR line,
one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9. The contract is decompositions/NFRA_MCPINDEX_DECOMP.round24-GATEWAY.md R24.3 (W6)."""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R24, "fixtures")
DELIV = os.path.normpath(os.path.join(R24, "..", ".."))
REPO = os.path.normpath(os.path.join(HERE, *([".."] * 9)))
R23 = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round23")
R22 = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round22")
H_CHECK = os.path.join(R23, "checks", "h_check.py")
PKG = os.path.join("workflows", "gateway_battery")
ROUTING_PY = os.path.join(PKG, "routing_table.py")
TEST_FILE = os.path.join(PKG, "tests", "test_routing_serves.py")
CENSUS = os.path.join(R22, "evidence", "GATEWAY_SURFACE_CENSUS_20261019_v2.json")
CATALOG = os.path.join(REPO, "infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
LIVE_TABLE = os.path.join(R23, "evidence", "ROUTING_TABLE_20261019.json")
OLD_SERVES = os.path.join(R23, "evidence", "GATEWAY_SERVES_20261019.json")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def fx(name):
    return os.path.join(FIX, name)


def run(args, timeout=240):
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


def line(out, prefix):
    for ln in out.splitlines():
        if ln.startswith(prefix):
            return ln.strip()
    return None


def pairs(lst):
    return sorted((x.get("vendor"), x.get("firm")) for x in lst or [])


def serves_run(tmp, tag):
    rt = os.path.join(tmp, "rt_%s.json" % tag)
    sv = os.path.join(tmp, "sv_%s.json" % tag)
    rc, so, se = run([ROUTING_PY, "--census", fx("w6_census.json"), "--catalog", fx("w6_catalog.yaml"), "--sources", fx("w6_sources.json"), "--out", rt, "--serves-out", sv])
    return rc, so, se, (jload(sv) if os.path.isfile(sv) else None), sv


def ac1(tmp):
    print("DENOMINATOR: fixture w6 -- 6 tools over 3 catalog rows of 3 vendors in 2 buckets: a coarse prefix over a two-vendor bucket (tW1, tW5), an exact prefix (tW2), "
          "a coarse prefix that carries the other vendor (tW3), no matching row (tW4), a source vendor no matched row has (tW6)")
    rc, so, se, doc, sv = serves_run(tmp, "a")
    arm("the emitter runs (rc 0 or 1, never 2 or a crash) and writes gateway_serves/1 for the six traced tools, and the SERVES line reads changed=5",
        rc in (0, 1) and doc is not None and doc.get("schema") == "gateway_serves/1" and [t.get("tool") for t in doc.get("tools", [])] == ["tW1", "tW2", "tW3", "tW4", "tW5", "tW6"]
        and line(so, "SERVES") == "SERVES tools=6 changed=5", "rc=%s %r %s" % (rc, line(so, "SERVES"), se[-200:]))
    by = {t.get("tool"): t for t in (doc or {}).get("tools", [])}
    t1 = by.get("tW1", {})
    arm("tW1 (coarse prefix over a two-vendor bucket, source vendor va): serves only va/fa; the catalog's vb/fb is REMOVED",
        (pairs(t1.get("serves")), pairs(t1.get("removed")), pairs(t1.get("added"))) == ([("va", "fa")], [("vb", "fb")], []), "got %r" % t1)
    t2 = by.get("tW2", {})
    arm("tW2 (exact prefix, matching vendor) is unchanged: serves va/fa, nothing added or removed",
        (pairs(t2.get("serves")), pairs(t2.get("removed")), pairs(t2.get("added"))) == ([("va", "fa")], [], []), "got %r" % t2)
    t3 = by.get("tW3", {})
    arm("tW3 (coarse prefix, source vendor vb): serves only vb/fb, ADDS vb/fb and REMOVES va/fa",
        (pairs(t3.get("serves")), pairs(t3.get("added")), pairs(t3.get("removed"))) == ([("vb", "fb")], [("vb", "fb")], [("va", "fa")]), "got %r" % t3)
    t4 = by.get("tW4", {})
    arm("tW4 (no catalog row matches): the unresolved rule is unchanged, serves vd/unresolved",
        (pairs(t4.get("serves")), pairs(t4.get("added")), pairs(t4.get("removed"))) == ([("vd", "unresolved")], [("vd", "unresolved")], []), "got %r" % t4)
    t5 = by.get("tW5", {})
    arm("tW5 (two sources): the union of the two traced sets, va/fa and vc/fc, with vb/fb REMOVED",
        (pairs(t5.get("serves")), pairs(t5.get("added")), pairs(t5.get("removed"))) == ([("va", "fa"), ("vc", "fc")], [], [("vb", "fb")]), "got %r" % t5)
    t6 = by.get("tW6", {})
    arm("tW6 (the matched row's vendor is not the source's vendor, and a row matched): contributes NOTHING, not an unresolved pair; the catalog's va/fa is REMOVED",
        (pairs(t6.get("serves")), pairs(t6.get("added")), pairs(t6.get("removed"))) == ([], [], [("va", "fa")]), "got %r" % t6)
    arm("counts tools=6 changed=5", (doc or {}).get("counts") == {"tools": 6, "changed": 5}, "got %r" % (doc or {}).get("counts"))
    rc2, so2, se2, doc2, sv2 = serves_run(tmp, "b")
    arm("two runs give the same bytes", doc is not None and doc2 is not None and open(sv, "rb").read() == open(sv2, "rb").read(), "differs or absent")


def h_check_pass(ident):
    rc, so, se = run([H_CHECK, ident], timeout=300)
    return rc == 0 and line(so, "RESULT:") == "RESULT: PASS", "rc=%s %r %s" % (rc, line(so, "RESULT:"), se[-200:])


def ac2(tmp):
    print("DENOMINATOR: round-23 r1.AC1 and r1.AC2 (the fixture serves arms and the three planted negatives), the live routing table (127 tools) and the live serves "
          "(old file %s)" % os.path.basename(OLD_SERVES))
    ok, why = h_check_pass("r1.AC1")
    arm("r1.AC1 (the routing table and the fixture serves arms) still prints RESULT: PASS", ok, why)
    ok, why = h_check_pass("r1.AC2")
    arm("r1.AC2 (planted link, code and display negatives, determinism, refusals) still prints RESULT: PASS", ok, why)
    sources = sorted(glob.glob(os.path.join(DELIV, "0.9.0_WK_NFRA_MCPINDEX~7[1-6]", "source_sets_*.json")))
    need = (CENSUS, CATALOG, LIVE_TABLE, OLD_SERVES)
    missing = [p for p in need if not os.path.isfile(p)]
    arm("the live inputs exist: the census, the catalog, the six source-set files, the committed routing table and the committed serves",
        not missing and len(sources) == 6, "missing=%r sources=%d" % (missing, len(sources)))
    if missing or len(sources) != 6:
        return
    rt = os.path.join(tmp, "live_rt.json")
    sv = os.path.join(tmp, "live_sv.json")
    rc, so, se = run([ROUTING_PY, "--census", CENSUS, "--catalog", CATALOG, "--sources"] + sources + ["--out", rt, "--serves-out", sv])
    arm("the live run prints the ROUTING line of round 23 (127 tools, 13 MISROUTED) and writes the serves",
        line(so, "ROUTING") == "ROUTING tools=127 pairs=199 routed_pairs=173 misrouted_tools=13 link=10 code=3 display=0 untraced=0" and os.path.isfile(sv),
        "rc=%s %r %s" % (rc, line(so, "ROUTING"), se[-200:]))
    arm("the live routing table is byte-identical to the committed round-23 table", os.path.isfile(rt) and open(rt, "rb").read() == open(LIVE_TABLE, "rb").read(), "differs or absent")
    if not os.path.isfile(sv):
        return
    new, old = jload(sv), jload(OLD_SERVES)
    old_by = {t["tool"]: set(pairs(t.get("serves"))) for t in old.get("tools", [])}
    new_by = {t["tool"]: t for t in new.get("tools", [])}
    sub = sorted(t for t, t_ in new_by.items() if not set(pairs(t_.get("serves"))) <= old_by.get(t, set()))
    arm("the same 127 tools, and for every tool the traced set is a SUBSET of the round-23 serves (it removes pairs, it adds none)",
        sorted(new_by) == sorted(old_by) and len(new_by) == 127 and not sub, "tools=%d old=%d not-subset=%r" % (len(new_by), len(old_by), sub[:5]))
    dropped = sorted(t for t, v in new_by.items() if v.get("current") and v.get("removed"))
    arm("at least one of the tools that carry serves today now has a REMOVED pair (the round-23 file removed none)", bool(dropped), "no tool with current serves has a removed pair")


def ac3(tmp):
    if not os.path.isfile(TEST_FILE):
        print("DENOMINATOR: test file %s absent" % TEST_FILE)
        arm("pytest on %s passes with at least 4 tests" % TEST_FILE, False, "file absent")
        return
    p = subprocess.run([sys.executable, "-m", "pytest", TEST_FILE, "-q", "-p", "no:cacheprovider", "--color=no"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum 4) file=%s" % (p.returncode, n, TEST_FILE))
    arm("pytest on %s passes with at least 4 tests" % TEST_FILE, p.returncode == 0 and n >= 4, "rc=%d passed=%d" % (p.returncode, n))


IDS = {"w6.AC1": ac1, "w6.AC2": ac2, "w6.AC3": ac3}


def main(argv):
    if len(argv) < 2 or argv[1] not in IDS:
        print("usage: w6_check.py %s" % "|".join(sorted(IDS)))
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
