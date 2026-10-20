"""y4_check.py <id>: the round-25 (workstream GATEWAY) criteria of cell MX-y-4, run from the repository root.
Ids: y4.AC1 (the three new link rules on a fixture of 16 tools), y4.AC2 (round-23/24 behavior unchanged: the r1 fixtures byte for byte, the three --plant
modes, the live round-24 table differing ONLY in the pairs the rules route, the serves untouched), y4.AC3 (pytest on tests/test_routing_links.py).
Prints a DENOMINATOR line, one line per arm, then RESULT: PASS|FAIL. ASCII only; python 3.9.
Y4_PKG_DIR (default workflows/gateway_battery) names the folder that holds routing_table.py and tests/ (a reference copy may be pointed at).
The contract is decompositions/NFRA_MCPINDEX_DECOMP.round25-GATEWAY.md R25.3 (Y4) plus the order's section 1 clarifications."""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R25 = os.path.normpath(os.path.join(HERE, ".."))
FIX = os.path.join(R25, "fixtures")
DELIV = os.path.normpath(os.path.join(R25, "..", ".."))
REPO = os.path.normpath(os.path.join(HERE, *([".."] * 9)))
R22 = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round22")
R23 = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round23")
R24 = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round24")
PKG = os.environ.get("Y4_PKG_DIR") or os.path.join("workflows", "gateway_battery")
ROUTING_PY = os.path.join(PKG, "routing_table.py")
TEST_FILE = os.path.join(PKG, "tests", "test_routing_links.py")
CATALOG = os.path.join(REPO, "infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
LIVE_CENSUS = os.path.join(R24, "evidence", "census_prospective_20261020.json")
LIVE_TABLE = os.path.join(R24, "evidence", "ROUTING_TABLE_20261020b.json")
LIVE_SERVES = os.path.join(R24, "evidence", "GATEWAY_SERVES_20261020b.json")
CATALOG_MD5 = "2bfc456e20600cdfacb6c7a6070961fb"
OK, BAD = [], []

FIXTURE_LINE = "ROUTING tools=16 pairs=16 routed_pairs=9 misrouted_tools=7 link=7 code=0 display=0 untraced=0"
LIVE_LINE = "ROUTING tools=127 pairs=209 routed_pairs=196 misrouted_tools=7 link=4 code=3 display=0 untraced=0"
CORRECTED_LINE = "ROUTING tools=127 pairs=209 routed_pairs=199 misrouted_tools=4 link=1 code=3 display=0 untraced=0"
FLIPPED = {  # the pairs the three rules route on the live round-24 inputs, by tool
    "harvest_get_research": {"harvest_amgt_harvest_silver_research_report", "harvest_research-continuation"},
    "mdpf_get_model_composition": {"opal_data_mdpf_feeds_model_composition"},
    "mdpf_get_security_classification": {"dynamodb_dynamodb_etf_classifications"},
}
STILL = {  # still MISROUTED live: the source names are env-var or function names, not the table
    "harvest_get_published_analysis": "published_analysis_scoped_api",
    "news_keyword_intelligence": "dynamodb_dynamodb_opal_keyword_intelligence",
    "news_search_articles": "dynamodb_dynamodb_opal_news_articles",
    "news_trending_topics": "dynamodb_dynamodb_opal_news_trending_daily",
}
TABLE_OF = {  # the table each news store source resolves to (the catalog rows' own table field)
    "news_keyword_intelligence": "opal-keyword-intelligence",
    "news_search_articles": "opal-news-articles",
    "news_trending_topics": "opal-news-trending-daily",
}
FX_ROUTED = ["tC1", "tI1", "tS1", "tS2", "tS3", "tT1", "tT3", "tT5", "tW1"]
FX_MISROUTED = ["tC2", "tI2", "tS4", "tS5", "tT2", "tT4", "tW2"]


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
    with open(p, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def jdump(doc, p):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")


def rbytes(p):
    with open(p, "rb") as fh:
        return fh.read()


def line(out, prefix):
    for ln in out.splitlines():
        if ln.startswith(prefix):
            return ln.strip()
    return None


def verdicts(doc):
    return {t["tool"]: (t["verdict"], t["class"]) for t in (doc or {}).get("tools", [])}


def fixture_run(tmp, tag):
    out = os.path.join(tmp, "fx_%s.json" % tag)
    rc, so, se = run([ROUTING_PY, "--census", fx("y4_census.json"), "--catalog", fx("y4_catalog.yaml"), "--sources", fx("y4_sources.json"), "--out", out])
    return rc, so, se, (jload(out) if os.path.isfile(out) else None), out


def ac1(tmp):
    print("DENOMINATOR: fixture y4 -- 16 tools over 9 catalog rows: store rows against store and integration sources (tS1 exact name, tS2 underscore for hyphen, "
          "tS3 a source table field, tS4 another name, tS5 an s3-only tool, tI1 integration with a table field, tI2 without), a templated prefix (tT1..tT5), "
          "twin prefixes (tW1 same bucket, tW2 another bucket), controls tC1 (exact) and tC2 (mismatch)")
    rc, so, se, doc, out = fixture_run(tmp, "a")
    arm("the script runs (rc 0 or 1, never 2 or a crash), writes gateway_routing_table/1 for the 16 tools and prints the expected ROUTING line (9 routed pairs, link=7)",
        rc in (0, 1) and doc is not None and doc.get("schema") == "gateway_routing_table/1" and len(doc.get("tools", [])) == 16 and line(so, "ROUTING") == FIXTURE_LINE,
        "rc=%s %r %s" % (rc, line(so, "ROUTING"), se[-200:]))
    v = verdicts(doc)
    arm("rule (i) store and integration sources: tS1 (exact name), tS2 ('_' for '-'), tS3 (the source table field) and tI1 (integration with a table field) are ROUTED",
        all(v.get(t) == ("ROUTED", None) for t in ("tS1", "tS2", "tS3", "tI1")), "got %r" % {t: v.get(t) for t in ("tS1", "tS2", "tS3", "tI1")})
    arm("rule (i) negatives: a store source of another name (tS4), a store-word row on an s3-only tool (tS5) and an integration with no matching name or table (tI2) stay MISROUTED link",
        all(v.get(t) == ("MISROUTED", "link") for t in ("tS4", "tS5", "tI2")), "got %r" % {t: v.get(t) for t in ("tS4", "tS5", "tI2")})
    arm("rule (ii) templated prefix: a <firm> segment stands for one path segment (tT1 one segment, tT3 a shorter source prefix, tT5 deeper literal) -> ROUTED",
        all(v.get(t) == ("ROUTED", None) for t in ("tT1", "tT3", "tT5")), "got %r" % {t: v.get(t) for t in ("tT1", "tT3", "tT5")})
    arm("rule (ii) negatives: another literal segment (tT2) and a wildcard that would have to span two segments (tT4) stay MISROUTED link",
        all(v.get(t) == ("MISROUTED", "link") for t in ("tT2", "tT4")), "got %r" % {t: v.get(t) for t in ("tT2", "tT4")})
    arm("rule (iii) twin prefixes: 'research-dossier' against 'research_dossier' in the same bucket (tW1) is ROUTED; the same prefixes in another bucket (tW2) stay MISROUTED link",
        v.get("tW1") == ("ROUTED", None) and v.get("tW2") == ("MISROUTED", "link"), "got %r" % {t: v.get(t) for t in ("tW1", "tW2")})
    arm("controls: the exact pair (tC1) stays ROUTED and the mismatched pair (tC2) stays MISROUTED link",
        v.get("tC1") == ("ROUTED", None) and v.get("tC2") == ("MISROUTED", "link"), "got %r" % {t: v.get(t) for t in ("tC1", "tC2")})
    arm("the verdict sets are exactly the 9 routed and the 7 misrouted tools",
        sorted(t for t, x in v.items() if x[0] == "ROUTED") == FX_ROUTED and sorted(t for t, x in v.items() if x[0] == "MISROUTED") == FX_MISROUTED,
        "routed=%r" % sorted(t for t, x in v.items() if x[0] == "ROUTED"))
    shapes = [sorted((p.get("row_source") or {}).keys()) for t in (doc or {}).get("tools", []) for p in t.get("pairs", [])]
    arm("every pair's row_source keeps exactly the keys bucket and prefix (the catalog's table field does not leak into the output)",
        bool(shapes) and all(s == ["bucket", "prefix"] for s in shapes), "got %r" % shapes[:3])
    rc2, so2, se2, doc2, out2 = fixture_run(tmp, "b")
    arm("two runs give the same bytes", doc is not None and doc2 is not None and rbytes(out) == rbytes(out2), "differs or absent")
    for kind in ("link", "code", "display"):
        po = os.path.join(tmp, "pl_%s.json" % kind)
        prc, pso, pse = run([ROUTING_PY, "--census", fx("y4_census.json"), "--catalog", fx("y4_catalog.yaml"), "--sources", fx("y4_sources.json"), "--out", po, "--plant", kind, "--tool", "tS1"])
        pd = jload(po) if os.path.isfile(po) else {}
        pv = verdicts(pd).get("tS1")
        arm("--plant %s on the store tool tS1 is read back as MISROUTED %s (rc 0 and the PLANT line; a store row the new rule routes is never the planted row)" % (kind, kind),
            prc == 0 and pv == ("MISROUTED", kind) and line(pso, "PLANT") == "PLANT kind=%s tool=tS1 verdict=MISROUTED class=%s" % (kind, kind),
            "rc=%s %r %r %s" % (prc, line(pso, "PLANT"), pv, pse[-150:]))


def r1_files():
    return [os.path.join(R23, "fixtures", n) for n in ("r1_census.json", "r1_catalog.yaml", "r1_sources.json")]


def ac2(tmp):
    print("DENOMINATOR: the round-23 r1 fixtures (table and serves byte for byte against the base outputs stored as y4_r1_base_*), the three --plant modes on r1's tS1, "
          "the live round-24 inputs (127 tools, catalog md5 %s) against the committed ROUTING_TABLE_20261020b.json and GATEWAY_SERVES_20261020b.json, and a "
          "corrected copy of the news store sources" % CATALOG_MD5)
    census, cat, src = r1_files()
    t1 = os.path.join(tmp, "r1_t.json")
    s1 = os.path.join(tmp, "r1_s.json")
    rc, so, se = run([ROUTING_PY, "--census", census, "--catalog", cat, "--sources", src, "--out", t1, "--serves-out", s1])
    arm("the r1 fixtures: the ROUTING and SERVES lines of round 23 (7 tools, link=1 code=1 display=1 untraced=1; 6 serves tools, changed=2)",
        line(so, "ROUTING") == "ROUTING tools=7 pairs=8 routed_pairs=7 misrouted_tools=3 link=1 code=1 display=1 untraced=1" and line(so, "SERVES") == "SERVES tools=6 changed=2",
        "rc=%s %r %r %s" % (rc, line(so, "ROUTING"), line(so, "SERVES"), se[-150:]))
    arm("the r1 routing table and serves are byte-identical to the base outputs",
        os.path.isfile(t1) and os.path.isfile(s1) and rbytes(t1) == rbytes(fx("y4_r1_base_table.json")) and rbytes(s1) == rbytes(fx("y4_r1_base_serves.json")), "differs or absent")
    for kind in ("link", "code", "display"):
        po = os.path.join(tmp, "r1pl_%s.json" % kind)
        prc, pso, pse = run([ROUTING_PY, "--census", census, "--catalog", cat, "--sources", src, "--out", po, "--plant", kind, "--tool", "tS1"])
        pv = verdicts(jload(po) if os.path.isfile(po) else {}).get("tS1")
        arm("r1: --plant %s on tS1 still fires (rc 0, PLANT line, MISROUTED %s)" % (kind, kind),
            prc == 0 and pv == ("MISROUTED", kind) and line(pso, "PLANT") == "PLANT kind=%s tool=tS1 verdict=MISROUTED class=%s" % (kind, kind), "rc=%s %r %r" % (prc, line(pso, "PLANT"), pv))
    sources = sorted(glob.glob(os.path.join(DELIV, "0.9.0_WK_NFRA_MCPINDEX~7[1-6]", "source_sets_*.json")))
    need = (CATALOG, LIVE_CENSUS, LIVE_TABLE, LIVE_SERVES)
    missing = [p for p in need if not os.path.isfile(p)]
    arm("the live inputs exist: the prospective census, the catalog, the six source-set files, the committed round-24 routing table and serves",
        not missing and len(sources) == 6, "missing=%r sources=%d" % (missing, len(sources)))
    if missing or len(sources) != 6:
        return
    md5 = hashlib.md5(rbytes(CATALOG)).hexdigest()
    arm("the tracked catalog is the round-24 candidate (md5 %s), so the committed table is the base the delta is read against" % CATALOG_MD5, md5 == CATALOG_MD5, "md5=%s" % md5)
    rt = os.path.join(tmp, "live_rt.json")
    sv = os.path.join(tmp, "live_sv.json")
    rc, so, se = run([ROUTING_PY, "--census", LIVE_CENSUS, "--catalog", CATALOG, "--sources"] + sources + ["--out", rt, "--serves-out", sv])
    arm("the live run prints the ROUTING line with link=4 (was 7) and routed_pairs=196 (was 192); code stays 3", line(so, "ROUTING") == LIVE_LINE and os.path.isfile(rt),
        "rc=%s %r %s" % (rc, line(so, "ROUTING"), se[-150:]))
    if not os.path.isfile(rt):
        return
    old, new = jload(LIVE_TABLE), jload(rt)
    by_old = {t["tool"]: t for t in old["tools"]}
    by_new = {t["tool"]: t for t in new["tools"]}
    changed = sorted(n for n in by_new if by_new[n] != by_old.get(n))
    arm("exactly the tools harvest_get_research, mdpf_get_model_composition and mdpf_get_security_classification differ from the committed table; the same 127 tools",
        sorted(by_new) == sorted(by_old) and len(by_new) == 127 and changed == sorted(FLIPPED), "changed=%r" % changed)
    ok = True
    why = ""
    for name, rows in FLIPPED.items():
        a, b = by_old.get(name), by_new.get(name)
        if not a or not b:
            ok, why = False, "missing %s" % name
            break
        flipped = {p["row"] for p, q in zip(a["pairs"], b["pairs"]) if p != q and p["verdict"] == "MISROUTED" and q["verdict"] == "ROUTED" and p["class"] == "link" and q["class"] is None}
        same_rest = all(a[k] == b[k] for k in ("tool", "channel", "declared_vendors", "source_set")) and len(a["pairs"]) == len(b["pairs"]) \
            and all(p == q for p, q in zip(a["pairs"], b["pairs"]) if p["row"] not in rows)
        if flipped != rows or not same_rest or (b["verdict"], b["class"]) != ("ROUTED", None):
            ok, why = False, "%s flipped=%r same_rest=%s" % (name, sorted(flipped), same_rest)
            break
    arm("in those tools only the four expected pairs flipped MISROUTED link -> ROUTED; the source sets, declared vendors and every other pair are unchanged", ok, why)
    oc, nc = old["counts"], new["counts"]
    arm("the counts differ only in link (7 -> 4) and routed_pairs (192 -> 196)",
        {k for k in nc if nc[k] != oc.get(k)} == {"link", "routed_pairs"} and (oc["link"], nc["link"], oc["routed_pairs"], nc["routed_pairs"]) == (7, 4, 192, 196), "old=%r new=%r" % (oc, nc))
    still = {n: next((p for p in by_new[n]["pairs"] if p["row"] == r), None) for n, r in STILL.items()}
    arm("the four pairs whose source names are env-var or function names stay MISROUTED link (published analysis, keyword intelligence, news articles, trending daily)",
        all(p is not None and p["verdict"] == "MISROUTED" and p["class"] == "link" for p in still.values()), "got %r" % {n: (p or {}).get("verdict") for n, p in still.items()})
    arm("the live serves are byte-identical to the committed GATEWAY_SERVES_20261020b.json (the new link rules never touch the serves rule)",
        os.path.isfile(sv) and rbytes(sv) == rbytes(LIVE_SERVES), "differs or absent")
    fixed = []
    for i, path in enumerate(sources):
        doc = jload(path)
        for entry in doc.get("tools", []):
            if entry.get("tool") in TABLE_OF:
                for s in entry.get("sources", []):
                    if s.get("kind") == "store":
                        s["table"] = TABLE_OF[entry["tool"]]
        out = os.path.join(tmp, "fixed_%d.json" % i)
        jdump(doc, out)
        fixed.append(out)
    crt = os.path.join(tmp, "corr_rt.json")
    crc, cso, cse = run([ROUTING_PY, "--census", LIVE_CENSUS, "--catalog", CATALOG, "--sources"] + fixed + ["--out", crt])
    cdoc = jload(crt) if os.path.isfile(crt) else {}
    cv = verdicts(cdoc)
    arm("with a table field on the three news store sources the live run prints link=1 (only the published-analysis row left) and the three news tools are ROUTED",
        line(cso, "ROUTING") == CORRECTED_LINE and all(cv.get(t) == ("ROUTED", None) for t in TABLE_OF), "rc=%s %r %r" % (crc, line(cso, "ROUTING"), {t: cv.get(t) for t in TABLE_OF}))


def ac3(tmp):
    if not os.path.isfile(TEST_FILE):
        print("DENOMINATOR: test file %s absent" % TEST_FILE)
        arm("pytest on %s passes with at least 6 tests" % TEST_FILE, False, "file absent")
        return
    p = subprocess.run([sys.executable, "-m", "pytest", TEST_FILE, "-q", "-p", "no:cacheprovider", "--color=no"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    m = re.search(r"(\d+) passed", out)
    n = int(m.group(1)) if m else 0
    print("DENOMINATOR: pytest rc=%d passed=%d (minimum 6) file=%s" % (p.returncode, n, TEST_FILE))
    arm("pytest on %s passes with at least 6 tests" % TEST_FILE, p.returncode == 0 and n >= 6, "rc=%d passed=%d" % (p.returncode, n))


IDS = {"y4.AC1": ac1, "y4.AC2": ac2, "y4.AC3": ac3}


def main(argv):
    if len(argv) < 2 or argv[1] not in IDS:
        print("usage: y4_check.py %s" % "|".join(sorted(IDS)))
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
