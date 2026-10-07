"""AMGT_RESAPP round 77 -- cell AMGT-ba-6 (CTO round-76 ruling 7): a share-capital or equity-structure table, and a
table whose rows carry one repeated label, is REFUSED as a driver chart or a segment breakdown; the name then
reads a plain reason.

The cell builds `lib/research/filings/table_class.py`:
  driver_refusal(thesis_driver, passage_text=None) -> a plain reason, or None when the driver is kept
  segment_refusal(rows)                            -> a plain reason, or None when the rows are kept
Both read only what they are handed; neither takes a security key.

  AC1  the two specimens are refused, the business tables beside them are kept, planted tables decide the class
  AC2  every reason is plain words; the module is stdlib-only at module scope and names no company
  AC3  the seam: the rule over the DEPLOYED /thesis of every covered name (read-only), refused names printed

  python r77_ba6.py --crit AC1|AC2|AC3 [--where local]
Prints PASS / FAIL clause lines and `R77 BA6 <crit> SERVED: YES|NO`; exit 0 on YES.
"""
import argparse
import ast
import concurrent.futures
import importlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "r77_groupB_fixture.json")
MODULE = "lib.research.filings.table_class"
FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate",
          "stage", "input ledger")
COMPANY_WORDS = ("asml", "petrobras", "pbr", "boeing", "alibaba", "baba")
STDLIB_OK = {"__future__", "re", "typing", "collections", "itertools", "functools", "dataclasses", "enum", "string",
             "unicodedata"}

_OK = [True]


def clause(name, passed, detail=""):
    print(("PASS " if passed else "FAIL ") + name + ((" " + str(detail)) if detail != "" else ""))
    if not passed:
        _OK[0] = False


def verdict(crit):
    print("R77 BA6 %s SERVED: %s" % (crit, "YES" if _OK[0] else "NO"))
    return 0 if _OK[0] else 1


def load_module():
    try:
        return importlib.import_module(MODULE)
    except Exception as err:  # noqa: BLE001 -- an absent or broken module is the FAIL this check reports
        clause("the module %s imports" % MODULE, False, "%s: %s" % (type(err).__name__, err))
        return None


def plain(reason):
    low = str(reason).lower()
    return (isinstance(reason, str) and 20 <= len(reason) <= 220 and reason[0].isupper() and reason.rstrip().endswith(".")
            and all(ord(ch) < 128 for ch in reason) and not any(word in low for word in BANNED)
            and "_" not in reason)


def fixture_names():
    with open(FIXTURE, encoding="utf-8") as handle:
        return json.load(handle)


def rows_of(entry):
    return ((entry.get("segment_breakdown") or {}).get("rows")) or []


def first_passage(entry):
    points = ((entry.get("thesis_driver_chart") or {}).get("points")) or []
    return points[0].get("passage_text") if points else None


def crit_ac1(mod):
    fx = fixture_names()
    names = fx["names"]
    print("   fixture: deployed %s captured %s" % (fx["function_code_sha256"][:8], fx["captured_at"]))
    asml, pbr, ba, baba = (names[k] for k in ("ASML_NA_Equity", "PBR_US_Equity", "BA_US_Equity", "BABA_US_Equity"))
    r = mod.driver_refusal(asml["thesis_driver"], first_passage(asml))
    clause("C1 the share-count driver is refused (ASML NA: %r, unit %r)" % (asml["thesis_driver"]["series"][:40],
                                                                             asml["thesis_driver"]["unit"]), bool(r), repr(r))
    r = mod.segment_refusal(rows_of(asml))
    clause("C2 the share-capital rows are refused as segments (ASML NA: %d rows)" % len(rows_of(asml)), bool(r), repr(r))
    r = mod.segment_refusal(rows_of(pbr))
    clause("C3 rows under one repeated label are refused as segments (PBR: %d rows, labels %s)" % (
        len(rows_of(pbr)), sorted({x["segment"] for x in rows_of(pbr)})), bool(r), repr(r))
    r = mod.driver_refusal(ba["thesis_driver"], first_passage(ba))
    clause("C4 control: a business driver is kept (BA: %r)" % ba["thesis_driver"]["series"][:40], r is None, repr(r))
    r = mod.segment_refusal(rows_of(ba))
    clause("C5 control: business segments are kept (BA: %d rows, %d labels)" % (
        len(rows_of(ba)), len({x["segment"] for x in rows_of(ba)})), r is None, repr(r))
    r = mod.segment_refusal(rows_of(baba))
    clause("C6 control: business segments are kept (BABA: %d rows)" % len(rows_of(baba)), r is None, repr(r))
    for series in (pbr["thesis_driver"], baba["thesis_driver"]):
        r = mod.driver_refusal(series, None)
        clause("C7 control: a non-share driver with no chart is not refused (%r)" % series["series"][:40], r is None, repr(r))
    # Planted tables decide the class, with no company in them.
    one = [{"segment": "Widgets", "text": "R77 PLANT Widgets revenue was 10 in 2025.", "cite": "plant"} for _ in range(3)]
    clause("C8 plant: three rows under one real label are refused", bool(mod.segment_refusal(one)), repr(mod.segment_refusal(one)))
    clause("C9 plant: one row alone is not a repeated label", mod.segment_refusal(one[:1]) is None, repr(mod.segment_refusal(one[:1])))
    clause("C10 plant: no rows is not a refusal", mod.segment_refusal([]) is None, repr(mod.segment_refusal([])))
    two = [{"segment": "Widgets", "text": "R77 PLANT Widgets revenue was 10.", "cite": "plant"},
           {"segment": "Gadgets", "text": "R77 PLANT Gadgets revenue was 12.", "cite": "plant"}]
    clause("C11 plant: two rows under two labels are kept", mod.segment_refusal(two) is None, repr(mod.segment_refusal(two)))
    equity = [{"segment": "Treasury shares", "text": "R77 PLANT Treasury shares: 5 (2024) and 6 (2025).", "cite": "plant"},
              {"segment": "Authorized share capital", "text": "R77 PLANT Authorized share capital: 100 ordinary shares.", "cite": "plant"},
              {"segment": "Major holders", "text": "R77 PLANT Major holders: Holder A 6.8% of the shares.", "cite": "plant"}]
    clause("C12 plant: three share-capital rows under three labels are refused", bool(mod.segment_refusal(equity)), repr(mod.segment_refusal(equity)))
    plant_driver = {"series": "R77 PLANT ordinary shares outstanding", "unit": "number of shares", "resolution": "cited",
                    "points": [{"period": "2024", "value": 10, "span": [0, 2]}, {"period": "2025", "value": 9, "span": [3, 5]}]}
    clause("C13 plant: a share-count driver is refused", bool(mod.driver_refusal(plant_driver, None)), repr(mod.driver_refusal(plant_driver, None)))
    plant_ok = dict(plant_driver, series="R77 PLANT units delivered", unit="units per year")
    clause("C14 plant: a units driver is kept", mod.driver_refusal(plant_ok, None) is None, repr(mod.driver_refusal(plant_ok, None)))
    clause("C15 a missing driver is not a refusal", mod.driver_refusal(None, None) is None and mod.driver_refusal({}, None) is None, "")


def crit_ac2(mod):
    names = fixture_names()["names"]
    asml, pbr = names["ASML_NA_Equity"], names["PBR_US_Equity"]
    reasons = {
        "share-count driver": mod.driver_refusal(asml["thesis_driver"], first_passage(asml)),
        "share-capital segments": mod.segment_refusal(rows_of(asml)),
        "one-label segments": mod.segment_refusal(rows_of(pbr)),
    }
    for kind, reason in reasons.items():
        clause("C1 the %s reason is plain words" % kind, plain(reason), repr(reason))
    seg = [reasons["share-capital segments"], reasons["one-label segments"]]
    clause("C2 the two segment reasons differ, so a reader can tell the classes apart", all(seg) and seg[0] != seg[1], "")
    path = getattr(mod, "__file__", "") or ""
    with open(path, encoding="utf-8") as handle:
        source = handle.read()
    tree = ast.parse(source)
    top = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            top.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            top.add((node.module or "").split(".")[0])
    clause("C3 the module imports only the standard library at module scope (the Lambda imports it)", top <= STDLIB_OK, sorted(top - STDLIB_OK))
    nested = sorted({n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} |
                    {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
    clause("C4 no import anywhere in the module reaches the filing fetch stack, a vendor or the network",
           not any(re.search(r"(fetch|document|battery|analyze|boto|requests|urllib|anthropic|fitz)", name) for name in nested), nested)
    low = source.lower()
    named = [word for word in COMPANY_WORDS if re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", low)]
    clause("C5 the rule names a class, not a company", not named, named)
    clause("C6 the module is ASCII", all(ord(ch) < 128 for ch in source), "")


def crit_ac3(mod):
    import boto3
    from botocore.config import Config

    from lib.research.coverage.covered_universe import covered_security_keys

    keys = sorted(covered_security_keys())
    lam = boto3.client("lambda", region_name=os.environ.get("AWS_REGION", "us-east-1"),
                       config=Config(max_pool_connections=12, read_timeout=120, retries={"max_attempts": 3}))
    sha = lam.get_function_configuration(FunctionName=FN)["CodeSha256"]

    def get(key):
        event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, key), "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        out = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
        try:
            return key, out.get("statusCode"), json.loads(out.get("body") or "{}")
        except ValueError:
            return key, out.get("statusCode"), {}

    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        served = list(pool.map(get, keys))
    read = [x for x in served if x[1] == 200]
    print("   deployed %s; covered names %d; /thesis read 200 on %d" % (sha[:8], len(keys), len(read)))
    clause("C1 every covered name's /thesis was read", len(read) == len(keys) and len(keys) > 0, "%d of %d" % (len(read), len(keys)))
    charts, with_rows, driver_refused, segment_refused, errors = [], [], {}, {}, []
    for key, _code, body in read:
        chart = body.get("thesis_driver_chart") or {}
        rows = ((body.get("segment_breakdown") or {}).get("rows")) or []
        try:
            if chart.get("status") == "SERVED" and chart.get("source") == "filing":
                charts.append(key)
                points = chart.get("points") or []
                reason = mod.driver_refusal(body.get("thesis_driver"), points[0].get("passage_text") if points else None)
                if reason:
                    driver_refused[key] = reason
            if rows:
                with_rows.append(key)
                reason = mod.segment_refusal(rows)
                if reason:
                    segment_refused[key] = reason
        except Exception as err:  # noqa: BLE001 -- the rule must not raise on any served shape
            errors.append("%s: %s: %s" % (key, type(err).__name__, err))
    clause("C2 the rule raised on no served shape", not errors, errors[:3])
    print("   filing driver charts served today: %d %s; refused %d %s" % (len(charts), charts, len(driver_refused), sorted(driver_refused)))
    print("   segment breakdowns served today: %d; refused %d %s" % (len(with_rows), len(segment_refused), sorted(segment_refused)))
    for key in sorted(set(driver_refused) | set(segment_refused)):
        print("     %s: driver %r; segments %r" % (key, driver_refused.get(key), segment_refused.get(key)))
    clause("C3 the share-count driver is refused on the served bytes (ASML NA)", "ASML_NA_Equity" in driver_refused, "")
    clause("C4 the business driver is kept on the served bytes (BA)", "BA_US_Equity" in charts and "BA_US_Equity" not in driver_refused, "")
    clause("C5 the share-capital and one-label breakdowns are refused (ASML NA, PBR)",
           {"ASML_NA_Equity", "PBR_US_Equity"} <= set(segment_refused), sorted(segment_refused))
    kept = [k for k in ("BA_US_Equity", "BABA_US_Equity", "HD_US_Equity") if k in with_rows and k not in segment_refused]
    clause("C6 control: the business breakdowns are kept (BA, BABA, HD)", len(kept) == 3, kept)
    clause("C7 bound: fewer than half of the served breakdowns are refused", len(segment_refused) * 2 < max(1, len(with_rows)),
           "%d of %d" % (len(segment_refused), len(with_rows)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    mod = load_module()
    if mod is not None:
        missing = [name for name in ("driver_refusal", "segment_refusal") if not callable(getattr(mod, name, None))]
        if missing:
            clause("the module exports driver_refusal and segment_refusal", False, missing)
        else:
            try:
                {"AC1": crit_ac1, "AC2": crit_ac2, "AC3": crit_ac3}[a.crit](mod)
            except Exception as err:  # noqa: BLE001 -- an instrument error is a FAIL with its cause, never a traceback
                clause("the check ran to the end", False, "%s: %s" % (type(err).__name__, err))
    return verdict(a.crit)


if __name__ == "__main__":
    sys.exit(main())
