"""IRPT_BCKEND round 183 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB183-1  IB-pr-517  the comparison catalogue serves Opal's five canonical models (UST, ST, INT, LT, ULT) in that order; Ultra Short-Term is added keyed by Opal's own model identity (namespace OPAL), with no YCharts mapping; the YCharts path refuses an entry that has no mapping and says so
    AC1  the served list: five model entries in the canonical order, named, no ticker, no vendor member; templates.json counts 5 and the new entry has no security_id
    AC2  admission: all five entries pass _admitted_comparison for every permitted firm; the four existing pins are unchanged; the new entry is OPAL/UST and an altered copy of it is refused (the negative arm)
    AC3  the YCharts path: recipe.comparison_security_ids returns the ids of mapped entries and refuses an unmapped one with COMPARISON_NO_VENDOR_MAPPING naming the key; the catalogue test file and the new test file pass
"""
import json
import os
import subprocess
import sys
from pathlib import Path

R = "infra/aws/lambda/investor-reporting"
BASE_PINS = {
    "opal_long_term": "5229433d0a1e10f33aea10b3b01cdc12a1d7e950262f89ab08869f7542b0b5eb",
    "opal_short_term": "9a183f6afaf7fe8fbfb4464bafac860ed5ed2ddca4676f3dcc2c13aa77675ebd",
    "opal_intermediate_term": "9392552c7db401a131e3aecc6cb255cd8f4c7d3c55e54d43cb1aaed979f5f300",
    "opal_ultra_long_term": "b797ca667d6417333fc777abbcc722c7e2606383c0e342ea6aaa443ec06f1917",
}
ORDER_KEYS = ["opal_ultra_short_term", "opal_short_term", "opal_intermediate_term", "opal_long_term", "opal_ultra_long_term"]
ORDER_LABELS = ["Opal Ultra Short-Term", "Opal Short-Term", "Opal Intermediate-Term", "Opal Long-Term", "Opal Ultra Long-Term"]
CID = ""
ROOT = Path(".")


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB183"))
    sys.exit(1)


def setup():
    for p in ("/ycharts/generate", "/_scope", "/_ids", "/_keys", "/_authz", ""):
        sys.path.insert(0, str(ROOT / (R + p)))
    sys.path.insert(0, str(ROOT / "lib"))


def templates():
    return json.loads((ROOT / R / "ycharts/generate/templates.json").read_text(encoding="utf-8"))


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell != "IB183-1" or arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    setup()
    t = templates()
    entries = t["comparison_catalog"]["entries"]
    if arm == "AC1":
        import comparison_catalogue as cc
        served = [e for e in cc.build_catalogue(tenant="FIRMX")["entries"] if e.get("name_source") == "model_catalogue"]
        if [e["label"] for e in served] != ORDER_LABELS or [e["key"] for e in served] != ORDER_KEYS:
            fail("served model entries must read %s in order, read %s" % (ORDER_LABELS, [e["label"] for e in served]))
        for e in served:
            if sorted(e) != ["key", "label", "name_source", "ticker"] or e["ticker"] is not None:
                fail("a served model entry must carry exactly key, label, ticker (null) and name_source: %s" % sorted(e))
        if t["_meta"]["denominators"].get("comparison_catalog_entries") != 5 or len(entries) != 5:
            fail("_meta.denominators.comparison_catalog_entries and the entries array must both read 5")
        new = [e for e in entries if e.get("key") == "opal_ultra_short_term"]
        if len(new) != 1 or "security_id" in new[0]:
            fail("opal_ultra_short_term must be present once with no security_id (no YCharts mapping)")
        print("OK: five model entries in canonical order; the new one has no YCharts id")
    elif arm == "AC2":
        import maintained_sources as ms
        owner_firms = sorted(ms._comparison_firms())
        if len(owner_firms) != 3:
            fail("expected three permitted firms, read %s" % owner_firms)
        for e in entries:
            for firm in owner_firms:
                for pc in ("FIRM_ADVISOR", "FIRM_OPERATIONS", "OPAL_GLOBAL"):
                    try:
                        ms._admitted_comparison(e, {"firm_id": firm}, {"principal_class": pc})
                    except Exception as x:
                        fail("%s not admitted for %s/%s: %s" % (e.get("key"), firm, pc, type(x).__name__))
        for k, v in BASE_PINS.items():
            if ms._COMPARISON_POLICY_SHA256.get(k) != v:
                fail("the pin of the existing key %s changed" % k)
        if "opal_ultra_short_term" not in ms._COMPARISON_POLICY_SHA256:
            fail("no pin for opal_ultra_short_term")
        new = [e for e in entries if e["key"] == "opal_ultra_short_term"][0]
        c = new["candidate"]
        if c.get("namespace") != "OPAL" or c.get("vendor_id") != "UST" or c.get("security_type") != "model_portfolio":
            fail("the new candidate must read namespace OPAL, vendor_id UST, security_type model_portfolio")
        altered = json.loads(json.dumps(new))
        altered["candidate"]["name"] = altered["candidate"]["name"] + " X"
        try:
            ms._admitted_comparison(altered, {"firm_id": owner_firms[0]}, {"principal_class": "FIRM_ADVISOR"})
        except Exception as x:
            if type(x).__name__ != "MaintainedSourceUnauthorized":
                fail("an altered entry must be refused with MaintainedSourceUnauthorized, got %s" % type(x).__name__)
        else:
            fail("an altered copy of the new entry was admitted (the pin does not bind it)")
        print("OK: five entries admitted for 3 firms x 3 principal classes; four old pins unchanged; altered copy refused")
    else:
        import recipe
        try:
            ids = recipe.comparison_security_ids({"a": {"security_id": "P:1"}, "b": {"namespace": "OPAL"}}, ["a"])
        except Exception as x:
            fail("a mapped entry must return its id: %s" % type(x).__name__)
        if ids != ["P:1"]:
            fail("comparison_security_ids(['a']) must return ['P:1'], read %r" % (ids,))
        try:
            recipe.comparison_security_ids({"a": {"security_id": "P:1"}, "b": {"namespace": "OPAL"}}, ["a", "b"])
        except recipe.EnvelopeRefused as x:
            text = " ".join(str(a) for a in x.args)
            if "COMPARISON_NO_VENDOR_MAPPING" not in text or "b" not in text:
                fail("the refusal must carry COMPARISON_NO_VENDOR_MAPPING and name the key: %s" % text)
        except Exception as x:
            fail("an unmapped entry must raise EnvelopeRefused, got %s" % type(x).__name__)
        else:
            fail("an unmapped entry was not refused")
        gen = ROOT / R / "ycharts/generate"
        newtest = gen / "tests/test_comparison_opal_model.py"
        if not newtest.is_file() or newtest.read_text(encoding="utf-8").count("def test_") < 3:
            fail("tests/test_comparison_opal_model.py must exist with at least 3 tests")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "tests/test_comparison_catalogue.py", "tests/test_comparison_opal_model.py"],
                           cwd=str(gen), capture_output=True, text=True, env=env, timeout=110)
        if r.returncode != 0:
            fail("pytest rc %s: %s" % (r.returncode, (r.stdout + r.stderr)[-300:]))
        print("OK: the YCharts path refuses an unmapped entry and says so; tests pass: %s" % r.stdout.strip().splitlines()[-1])
    print("%s PASS" % CID)


main()
