"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the round-60 G enrichment (CTO msg 11977). READ ONLY, offline, no AWS.
Needs a python with pytest and jsonschema (the repository's producer tests import them), not `-I`.

    python ar_enrich_checks.py etfkey [--root <lambda tree root>]
    python ar_enrich_checks.py asof [--root <lambda tree root>]
    python ar_enrich_checks.py tests189 [--root <lambda tree root>]
    python ar_enrich_checks.py tests190 [--root <lambda tree root>]

`etfkey` (cell AR-g-189): an ETF typed in the form's "Other ETFs" field is admitted by the REAL door (`maintained_sources.resolve_comparison_fields`
over a classification table naming IWM), which drops `key` from the retained catalogue entry (the key is the dict key). The REAL
`ResidentGenerationWorker._opal_comparables` must then return ticker "IWM" for it (and None for a model), and the REAL producer, given those
comparables, must chart the ETF priced from the held readers, report it at 100 percent in its class, and state no gap. At base the ticker is None
(measured, `etf_typed_measure.py`) and the ETF is a nameless line-less "other" comparable.
`asof` (cell AR-g-190): page 60's allocation rows print each model's OWN as-of date. The positioning object's `portfolios.<code>.data_as_of`
(LT 2026-08-18, ULT 2026-10-08 here) is the row's date; a portfolio with no `data_as_of` falls back to the file's `data_as_of` (2026-10-19); a
`data_as_of` that is present and not a YYYY-MM-DD day is a ModelSourceRefused. `read_allocation` keeps its file-level "as_of" and gains
"as_of_by_code".
`tests189` / `tests190`: the owned test files pass and at least the baseline plus the new tests ran.
Prints one RESULT line: AR-ENRICH-<arm>-OK or AR-ENRICH-<arm>-FAIL <why>. ASCII only.
"""
import copy
import gzip
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
TREE = "infra/aws/lambda/investor-reporting"
TESTS = {"tests189": (["reports/tests/test_compare_ports.py"], 7),
         "tests190": (["ycharts/research/tests/test_model_source.py", "ycharts/research/tests/test_compare_producer.py"], 68)}
PORTFOLIO_DATES = {"LT": "2026-08-18", "ULT": "2026-10-08"}


def fail(arm, why):
    print("AR-ENRICH-%s-FAIL %s" % (arm, why))
    sys.exit(1)


def paths(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    here = os.path.join(base, "ycharts/research")
    sys.path[:0] = [os.path.join(here, "tests"), here, os.path.join(base, "ycharts/session"), os.path.join(base, "ycharts/generate"),
                    os.path.join(base, "ycharts/extract"), os.path.join(base, "reports"), os.path.join(base, "lib"), os.path.join(base, "ops"), os.path.join(base, "intake"),
                    os.path.join(base, "_scope"), os.path.join(base, "_ids"), os.path.join(base, "_keys"), os.path.join(base, "_authz"), base]
    return base


def arm_etfkey(root):
    paths(root)
    import types
    import maintained_sources as ms
    import resident_worker as rw
    import test_opal_producer as tp
    import test_compare_producer as tc
    owner = {"firm_id": "F1", "principal_id": "P1", "principal_class": "OPAL_GLOBAL", "advisor_id": None, "home_firm_id": "F1"}
    catalogue = {"maintainer": "2.0.0_SA_COO~Y", "candidate_version": ms.COMPARISON_CANDIDATE_VERSION, "entries": []}
    table = {"IWM": {"name": "iShares Russell 2000 ETF"}}
    ms.resolve_prospect_owner = lambda headers: owner
    try:
        out = ms.resolve_comparison_fields({}, {"content_sha256": "0" * 64}, ["IWM"], get_catalogue=lambda: catalogue,
                                           authorize_input=lambda o, i: True, read_classifications=lambda: table)
    except Exception as exc:  # noqa: BLE001
        fail("etfkey", "the door raised %s: %s" % (type(exc).__name__, str(exc)[:100]))
    etf_entry = out["comparison_catalog"]["IWM"]
    model_entry = {"mapping_evidence": "OPAL_MODEL", "name": "Opal Long-Term", "namespace": "YCHARTS", "security_type": "model_portfolio",
                   "source_id": "opal_long_term", "vendor_id": "P:2"}
    prepared = {"comparison_keys": ["opal_long_term", "IWM"], "comparisons": [model_entry, etf_entry]}
    shell = types.SimpleNamespace(
        frozen=types.SimpleNamespace(prepare=lambda principal, request_id, **kw: copy.deepcopy(prepared)),
        store=types.SimpleNamespace(tenant="49financial"))
    try:
        got = rw.ResidentGenerationWorker._opal_comparables(shell, {"firm_id": "49financial", "principal_id": "p"}, "REQ-x")
    except Exception as exc:  # noqa: BLE001
        fail("etfkey", "_opal_comparables raised %s: %s" % (type(exc).__name__, str(exc)[:100]))
    want = [{"key": "opal_long_term", "label": "Opal Long-Term", "ticker": None},
            {"key": "IWM", "label": "iShares Russell 2000 ETF", "ticker": "IWM"}]
    if got != want:
        fail("etfkey", "the door's own ETF entry %s gives %r, want %r" % (sorted(etf_entry), got, want))
    clf = tp.FakeClassifier()
    clf.rows["IWM"] = {"ticker": "IWM", "asset_class": "equity", "sub_asset_class": "Fixture Small Blend", "name": "iShares Russell 2000 ETF"}
    mp = json.loads((tc.MAPS / "multi_map.json").read_text(encoding="utf-8"))
    stores = tp.make_stores(classifier=clf, map=mp, pricing=True, as_of=tc.AS_OF, price_readers=tc._readers(), comparables=got,
                            model_bytes=tc._model_bytes())
    try:
        tp.op.produce(tp.REQ, tp.FIRM, stores)
    except Exception as exc:  # noqa: BLE001
        fail("etfkey", "the producer raised %s: %s" % (type(exc).__name__, str(exc)[:120]))
    sections = {s["section_id"]: s for s in stores["reports"].persisted[0]["report"]["sections"]}
    problems = []
    chart = tc._value(sections, "opal.compare.chart")
    if [line["name"] for line in chart] != ["Your portfolio", "Opal Long-Term", "iShares Russell 2000 ETF"]:
        problems.append("chart lines %r" % ([line["name"] for line in chart],))
    returns = tc._value(sections, "opal.compare.returns")
    if returns["gaps"] != []:
        problems.append("returns gaps %r" % (returns["gaps"],))
    alloc = tc._value(sections, "opal.compare.allocation")
    rows = {r["Name"]: r for r in alloc["rows"]}
    if rows.get("iShares Russell 2000 ETF", {}).get("Equity") != 100.0 or alloc["gaps"] != []:
        problems.append("allocation rows %r gaps %r" % (rows.get("iShares Russell 2000 ETF"), alloc["gaps"]))
    if problems:
        fail("etfkey", "; ".join(problems))
    print("AR-ENRICH-etfkey-OK")


def _positioning(per_portfolio, file_date="2026-10-19"):
    import test_compare_producer as tc
    portfolios = {}
    for code, alloc in tc.ALLOC.items():
        entry = {"code": code, "allocation": dict(zip(tc.ALLOC_KEYS, alloc))}
        if code in per_portfolio:
            entry["data_as_of"] = per_portfolio[code]
        portfolios[code] = entry
    return gzip.compress(json.dumps({"data_as_of": file_date, "portfolios": portfolios}).encode("utf-8"))


def _bytes_with(positioning):
    import test_compare_producer as tc
    import model_source as msrc
    base = tc._model_bytes()

    def get(key):
        return positioning if key == msrc.POSITIONING_KEY else base(key)
    return get


def arm_asof(root):
    paths(root)
    import model_source as msrc
    import test_opal_producer as tp
    import test_compare_producer as tc
    problems = []
    doc = msrc.read_allocation(_bytes_with(_positioning(PORTFOLIO_DATES)))
    if doc.get("as_of") != "2026-10-19":
        problems.append("the file-level as_of is %r" % (doc.get("as_of"),))
    if doc.get("as_of_by_code") != {"LT": "2026-08-18", "ULT": "2026-10-08"}:
        problems.append("as_of_by_code is %r" % (doc.get("as_of_by_code"),))
    mixed = msrc.read_allocation(_bytes_with(_positioning({"LT": "2026-08-18"})))
    if mixed.get("as_of_by_code") != {"LT": "2026-08-18", "ULT": "2026-10-19"}:
        problems.append("a portfolio without data_as_of should take the file's date, got %r" % (mixed.get("as_of_by_code"),))
    try:
        msrc.read_allocation(_bytes_with(_positioning({"LT": "2026-13-45"})))
        problems.append("a malformed per-portfolio data_as_of was not refused")
    except msrc.ModelSourceRefused:
        pass
    clf = tp.FakeClassifier()
    clf.rows["IWM"] = {"ticker": "IWM", "asset_class": "equity", "sub_asset_class": "Fixture Small Blend", "name": "iShares Russell 2000 ETF"}
    mp = json.loads((tc.MAPS / "multi_map.json").read_text(encoding="utf-8"))
    stores = tp.make_stores(classifier=clf, map=mp, pricing=True, as_of=tc.AS_OF, price_readers=tc._readers(), comparables=tc.ENTRIES,
                            model_bytes=_bytes_with(_positioning(PORTFOLIO_DATES)))
    try:
        tp.op.produce(tp.REQ, tp.FIRM, stores)
    except Exception as exc:  # noqa: BLE001
        fail("asof", "the producer raised %s: %s" % (type(exc).__name__, str(exc)[:120]))
    sections = {s["section_id"]: s for s in stores["reports"].persisted[0]["report"]["sections"]}
    alloc = tc._value(sections, "opal.compare.allocation")
    rows = {r["Name"]: r for r in alloc["rows"]}
    for name, day in (("Opal Long-Term", "2026-08-18"), ("Opal Ultra Long-Term", "2026-10-08")):
        basis = rows.get(name, {}).get("Basis")
        if basis != "Model positioning as of %s" % day:
            problems.append("%s basis is %r, want the model's own date %s" % (name, basis, day))
    if problems:
        fail("asof", "; ".join(problems))
    print("AR-ENRICH-asof-OK")


def arm_tests(arm, root):
    files, minimum = TESTS[arm]
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + files
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    found = re.findall(r"(\d+) passed", run.stdout)
    passed = int(found[-1]) if found else 0
    if run.returncode != 0 or passed < minimum:
        print("AR-ENRICH-%s-FAIL rc=%d passed=%d (want rc 0 and at least %d): %s" % (arm, run.returncode, passed, minimum,
              " ".join(run.stdout.strip().splitlines()[-2:])[:200]))
        sys.exit(1)
    print("AR-ENRICH-%s-OK passed=%d" % (arm, passed))


def main():
    arms = ("etfkey", "asof", "tests189", "tests190")
    if len(sys.argv) < 2 or sys.argv[1] not in arms:
        print("usage: ar_enrich_checks.py %s [--root <root>]" % "|".join(arms))
        sys.exit(2)
    root = REPO
    if "--root" in sys.argv:
        root = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    arm = sys.argv[1]
    if arm.startswith("tests"):
        arm_tests(arm, root)
    else:
        {"etfkey": arm_etfkey, "asof": arm_asof}[arm](root)


if __name__ == "__main__":
    main()
