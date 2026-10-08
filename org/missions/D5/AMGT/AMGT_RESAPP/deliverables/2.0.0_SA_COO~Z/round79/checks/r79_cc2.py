"""AMGT_RESAPP round 79 -- AMGT-cc-2: ONE served segment table with its period and currency labels (FWD-1).

  python r79_cc2.py --crit AC1|AC2|AC3 --where local

Round 78 built a reader of the stored Bloomberg segment table (`segment_table.read_segment_table`) and a pure function that
names a period column only where it ties to stored revenue (`segment_period.label_periods`); neither is served. This cell
builds the one function the adapter will call from `/thesis`:

  lib.research.api.segment_served.serve_segment_table(security_key, fiscal_year_figures, header_figures, client=None)

returning the block served under the key `segment_table`, with exactly these keys:
  status, rows, operating_income_rows, periods, period_note, currency, units, currency_note, reason, source
and each entry of `periods` exactly: period, label, fiscal_year, top_level_sum, note.

AC1 (build, planted objects behind a fake store client and planted figures; no network):
    F1 a column whose level-1 rows add up to a stored fiscal year's revenue is labelled with that year, the currency and
       the units are stated, and the rows are the reader's rows unchanged;
    F2 a column that ties to no stored year, and a column with no level-1 figure, are not labelled and each says why;
    F3 with no figures handed in, the table is still served: no column labelled, no currency, no units, a plain note;
    F4 nothing to show reads a plain reason and never raises: no stored table, a store that raises, arguments of the
       wrong type;
    F5 every answer carries exactly the ten keys, and every period entry exactly its five;
    F6 no served sentence uses a system word;
    F7 the store is read only through `segment_table.read_segment_table`, called once with the client handed in, and the
       arguments are left unchanged.
AC2 (build, the real neighbour; reads the store, writes nothing):
    S1 AMD_US_Equity serves its revenue rows with Period 1 labelled fiscal year 2025, in millions of USD;
    S2 8766_JP_Equity (its Period 1 ties to no stored year) serves its rows with Period 1 unlabelled and a plain note;
    S3 a name with no stored table (ZZZZ_US_Equity) reads the plain nothing-stored reason, and a stored name with no
       revenue lines (8306_JP_Equity) reads a different plain reason;
    S4 the denominator: every stored name is served without an exception, and its Period 1 is labelled exactly when this
       check's own sum of the level-1 rows is within 0.5 percent of a stored fiscal year's revenue (N of N printed).
AC3 (bound): the plant tests of the two modules this one stands on, and of the filing-text segment breakdown, pass.
Verdict: R79 CC2 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import ast
import copy
import io
import json
import subprocess
import sys

BUCKET = "opal-data-harvest"
PREFIX = "bloomberg/harvest/bronze/segments/"
TESTS = ("lib/research/api/tests/test_segment_table.py", "lib/research/api/tests/test_segment_period.py",
         "lib/research/api/tests/test_segment_breakdown.py")
KEYS = {"status", "rows", "operating_income_rows", "periods", "period_note", "currency", "units", "currency_note",
        "reason", "source"}
PERIOD_KEYS = {"period", "label", "fiscal_year", "top_level_sum", "note"}
BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
          "input ledger", "bronze")
STORE_CALLS = ("get_object", "get_paginator", "paginate", "list_objects_v2", "list_objects")
NONE_STORED = "No Bloomberg segment table has been stored for this name yet."
MARKER = -2.4245362661989844e-14
TOLERANCE = 0.005


class FakeStore:
    """A store client serving planted objects: the two calls the reader may make."""

    def __init__(self, objects, fail=False):
        self.objects = dict(objects)
        self.fail = fail

    def get_paginator(self, _name):
        return self

    def paginate(self, **kwargs):
        if self.fail:
            raise RuntimeError("planted listing failure")
        prefix = kwargs.get("Prefix", "")
        yield {"Contents": [{"Key": k, "Size": len(v)} for k, v in sorted(self.objects.items()) if k.startswith(prefix)]}

    def get_object(self, **kwargs):
        if self.fail:
            raise RuntimeError("planted read failure")
        return {"Body": io.BytesIO(self.objects[kwargs["Key"]])}


def _row(name, level, values):
    out = {"Metric Name": name, "Product Geographic Hierarchy Level": level}
    for i, v in enumerate(values, 1):
        out["Period %d Value" % i] = v
    return out


def _figure(year, value, mnemonic="SALES_REV_TURN", scope="fiscal_year_line_item", unit="MILLIONS"):
    return {"scope": scope, "fiscal_year": year, "mnemonic": mnemonic, "value": value, "unit": unit}


def _header(code):
    return [{"scope": "header", "fiscal_year": None, "mnemonic": "CRNCY", "value": "GBp"},
            {"scope": "header", "fiscal_year": None, "mnemonic": "EQY_FUND_CRNCY", "value": code}]


# Level-1 sums by column: 14.0, 12.0, 10.0, 1.0, none (the level-2 row is never counted).
TABLE = json.dumps({"security": "TEST US Equity", "pulled_at": "2026-10-07T11:51:13Z", "response": {
    "NAME": "TEST CO",
    "PG_REVENUE": [_row("Cloud", 1, [10.0, 9.0, 8.0, MARKER, MARKER]),
                   _row(chr(160) * 3 + "Hosting", 2, [6.0, 5.0, 4.0, 3.0, 2.0]),
                   _row("Devices", 1, [4.0, 3.0, 2.0, 1.0, MARKER])],
    "PG_OPERATING_INCOME": [_row("Cloud", 1, [2.0, 1.0, MARKER, MARKER, MARKER])]}}).encode("utf-8")
TABLE_KEY = PREFIX + "security_key=TEST_US_Equity/20261007T115113Z.json"
# 2025 ties to column 1, 2024 to column 2 (12.05 against 12.0 is inside 0.5 percent); 2023 misses column 3 (10.0 against 10.2).
FIGURES = [_figure("2025", 14.0), _figure("2024", 12.05), _figure("2023", 10.2),
           _figure("2025", 999.0, mnemonic="NET_INCOME"), _figure("2022", 1.0, scope="forecast")]


def _plain(text):
    return isinstance(text, str) and bool(text.strip()) and not any(w in text.casefold() for w in BANNED)


def _sentences(block):
    out = [block.get("reason"), block.get("period_note"), block.get("currency_note")]
    for p in block.get("periods") or []:
        if isinstance(p, dict):
            out.extend([p.get("note"), p.get("label")])
    return [s for s in out if s is not None]


def _period(block, n):
    for p in block.get("periods") or []:
        if isinstance(p, dict) and p.get("period") == n:
            return p
    return {}


def _load(clause):
    try:
        from lib.research.api import segment_served
    except Exception as err:  # noqa: BLE001 -- any import failure is the first clause of a build check
        clause("C0 lib.research.api.segment_served imports", False, str(err)[:160])
        return None, None
    fn = getattr(segment_served, "serve_segment_table", None)
    if not callable(fn):
        clause("C0 segment_served.serve_segment_table exists", False, "absent")
        return None, None
    return segment_served, fn


def _ac1(mod, fn, clause):
    from lib.research.api import segment_table

    store = FakeStore({TABLE_KEY: TABLE})
    reader = segment_table.read_segment_table("TEST_US_Equity", client=store)
    got = fn("TEST_US_Equity", copy.deepcopy(FIGURES), _header("EUR"), client=store)
    p1, p2, p3, p4, p5 = [_period(got, n) for n in range(1, 6)]
    clause("F1 a column that ties is labelled with its fiscal year; currency and units stated; rows unchanged",
           got.get("status") == "served" and got.get("rows") == reader.get("rows") and len(got.get("rows") or []) == 3
           and got.get("operating_income_rows") == reader.get("operating_income_rows")
           and got.get("source") == reader.get("source") and got.get("reason") is None
           and p1.get("fiscal_year") == "2025" and p1.get("label") == "Fiscal year 2025" and p1.get("note") is None
           and p1.get("top_level_sum") == 14.0 and p2.get("fiscal_year") == "2024"
           and got.get("currency") == "EUR" and got.get("units") == "millions"
           and _plain(got.get("currency_note")) and "EUR" in got.get("currency_note") and _plain(got.get("period_note")),
           "P1 %r; currency %r units %r" % (p1, got.get("currency"), got.get("units")))
    clause("F2 a column that ties to no year, and a column with no figure, are not labelled and each says why",
           p3.get("fiscal_year") is None and p3.get("label") == "Period 3" and p3.get("top_level_sum") == 10.0
           and _plain(p3.get("note")) and p4.get("fiscal_year") is None and _plain(p4.get("note"))
           and p5.get("fiscal_year") is None and p5.get("top_level_sum") is None and p5.get("label") == "Period 5"
           and _plain(p5.get("note")) and p5.get("note") != p3.get("note"),
           "P3 %r; P5 %r" % (p3, p5))

    bare = [fn("TEST_US_Equity", figures, header, client=store) for figures, header in ((None, None), ([], []))]
    clause("F3 with no figures the table is still served, no column labelled, no currency, no units",
           all(b.get("status") == "served" and b.get("rows") == reader.get("rows") and len(b.get("periods") or []) == 5
               and all(p.get("fiscal_year") is None and str(p.get("label")).startswith("Period ") for p in b.get("periods"))
               and b.get("currency") is None and b.get("units") is None and _plain(b.get("period_note"))
               and _plain(b.get("currency_note")) for b in bare),
           "period note %r" % (bare[0].get("period_note"),))

    nothing = []
    raised = None
    for args in (("ZZZZ_US_Equity", FIGURES, _header("USD"), FakeStore({})),
                 ("TEST_US_Equity", FIGURES, _header("USD"), FakeStore({}, fail=True)),
                 (None, "not a list", 7, FakeStore({})),
                 ("TEST_US_Equity", [None, 3, {"mnemonic": "SALES_REV_TURN"}], [None, "x"], FakeStore({TABLE_KEY: TABLE})),
                 ("TEST_US_Equity", FIGURES, _header("USD"), object())):
        try:
            nothing.append(fn(args[0], args[1], args[2], client=args[3]))
        except Exception as err:  # noqa: BLE001 -- the raise IS the failure being tested for
            raised = "%s: %s" % (type(err).__name__, str(err)[:80])
            nothing.append({})
    empties = [nothing[0], nothing[1], nothing[2], nothing[4]]
    clause("F4 nothing to show reads a plain reason and never raises",
           raised is None and all(n.get("status") == "none" and n.get("rows") == [] and n.get("periods") == []
                                  and n.get("currency") is None and _plain(n.get("reason")) for n in empties)
           and nothing[0].get("reason") == NONE_STORED and nothing[1].get("reason") != NONE_STORED
           and nothing[3].get("status") == "served" and _period(nothing[3], 1).get("fiscal_year") is None,
           "raised %r; reasons %r" % (raised, [n.get("reason") for n in empties][:2]))

    blocks = [got] + bare + nothing
    bad = [sorted(set(b) ^ KEYS) for b in blocks if set(b) != KEYS]
    bad_p = [sorted(set(p) ^ PERIOD_KEYS) for b in blocks for p in (b.get("periods") or [])
             if not isinstance(p, dict) or set(p) != PERIOD_KEYS]
    clause("F5 every answer carries exactly the ten keys and every period entry its five", not bad and not bad_p,
           "answers %d, off-shape %s %s" % (len(blocks), bad[:2], bad_p[:2]))

    used = sorted({w for b in blocks for s in _sentences(b) for w in BANNED if w in str(s).casefold()})
    clause("F6 no served sentence uses a system word", not used and all(isinstance(s, str) for b in blocks for s in _sentences(b)),
           "sentences read %d, words used %s" % (sum(len(_sentences(b)) for b in blocks), used))

    with open(mod.__file__, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    imports = sorted({a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
                     | {(n.module or "").split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)})
    store_calls = sorted({n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute) and n.attr in STORE_CALLS})
    calls = []
    real = segment_table.read_segment_table
    planted = copy.deepcopy(reader)
    sentinel = FakeStore({})

    def recorder(security_key, client=None):
        calls.append((security_key, client))
        return copy.deepcopy(planted)

    figures_in, header_in = copy.deepcopy(FIGURES), _header("EUR")
    figures_before, header_before = copy.deepcopy(figures_in), copy.deepcopy(header_in)
    segment_table.read_segment_table = recorder
    try:
        through = fn("TEST_US_Equity", figures_in, header_in, client=sentinel)
    except Exception as err:  # noqa: BLE001 -- a raise here is a FAIL of this clause
        through = {"error": "%s: %s" % (type(err).__name__, str(err)[:80])}
    finally:
        segment_table.read_segment_table = real
    clause("F7 the store is read only through read_segment_table, once, with the client handed in; arguments unchanged",
           "boto3" not in imports and "botocore" not in imports and not store_calls and len(calls) == 1
           and calls[0][0] == "TEST_US_Equity" and calls[0][1] is sentinel and through.get("rows") == reader.get("rows")
           and _period(through, 1).get("fiscal_year") == "2025"
           and figures_in == figures_before and header_in == header_before,
           "imports %s; store calls in the source %s; reader calls %d" % (imports, store_calls, len(calls)))


def _own_tie(rows, revenue):
    vals = [r["values"][0] for r in rows if r.get("level") == 1 and r["values"][0] is not None and abs(r["values"][0]) > 1e-6]
    if not vals:
        return False, None
    total = sum(vals)
    for value in revenue.values():
        if value > 0 and abs(total - value) <= TOLERANCE * value:
            return True, total
    return False, total


def _ac2(fn, clause):
    import boto3

    from lib.research.api import scoped_amgt, segment_table
    from lib.research.identity import crosswalk

    s3 = boto3.client("s3", region_name="us-east-1")

    def figures_of(name):
        block = scoped_amgt.read_model_block(name)
        return (scoped_amgt._figures(block, scoped_amgt.SCOPE_FISCAL_YEAR_LINE_ITEM), scoped_amgt._header_figures(block))

    def served(name):
        fiscal, header = figures_of(name)
        return fn(name, fiscal, header, client=s3), fiscal

    amd, _fiscal = served("AMD_US_Equity")
    reader = segment_table.read_segment_table("AMD_US_Equity", client=s3)
    p1 = _period(amd, 1)
    clause("S1 AMD serves its revenue rows with Period 1 labelled fiscal year 2025 in millions of USD",
           amd.get("status") == "served" and bool(amd.get("rows")) and amd.get("rows") == reader.get("rows")
           and p1.get("fiscal_year") == "2025" and p1.get("label") == "Fiscal year 2025" and amd.get("currency") == "USD"
           and amd.get("units") == "millions",
           "rows %d; P1 label %r sum %r; currency %r units %r" % (
               len(amd.get("rows") or []), p1.get("label"), p1.get("top_level_sum"), amd.get("currency"), amd.get("units")))

    odd, _fiscal = served("8766_JP_Equity")
    q1 = _period(odd, 1)
    clause("S2 a name whose Period 1 ties to no stored year serves its rows with Period 1 unlabelled and a plain note",
           odd.get("status") == "served" and bool(odd.get("rows")) and q1.get("fiscal_year") is None
           and q1.get("label") == "Period 1" and _plain(q1.get("note")),
           "8766_JP_Equity rows %d; P1 label %r sum %r note %r" % (
               len(odd.get("rows") or []), q1.get("label"), q1.get("top_level_sum"), q1.get("note")))

    never = fn("ZZZZ_US_Equity", [], scoped_amgt._header_figures(None), client=s3)
    bank, _fiscal = served("8306_JP_Equity")
    print("   never stored: %r" % (never.get("reason"),))
    print("   stored, no revenue lines: %r" % (bank.get("reason"),))
    clause("S3 a name with no stored table and a stored name with no revenue lines each read their own plain reason",
           never.get("status") == "none" and never.get("rows") == [] and never.get("reason") == NONE_STORED
           and bank.get("status") == "none" and bank.get("rows") == [] and _plain(bank.get("reason"))
           and bank.get("reason") != NONE_STORED)

    folders = set()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"][len(PREFIX):].split("/")
            if len(parts) == 2 and parts[0].startswith("security_key=") and parts[1].endswith(".json"):
                folders.add(parts[0][len("security_key="):])
    agree, with_rows, labelled, unlabelled, wrong = 0, 0, 0, [], []
    for folder in sorted(folders):
        name = crosswalk.security_key_from_slash_safe(folder)
        try:
            got, fiscal = served(name)
        except Exception as err:  # noqa: BLE001 -- the served function must never raise; a raise is a counted failure
            wrong.append("%s raised %s" % (name, type(err).__name__))
            continue
        rows = got.get("rows") or []
        stored_rows = segment_table.read_segment_table(name, client=s3).get("rows") or []
        if rows != stored_rows:
            wrong.append("%s (rows %d, the reader's %d)" % (name, len(rows), len(stored_rows)))
            continue
        if not rows:
            if got.get("status") == "none" and _plain(got.get("reason")) and set(got) == KEYS:
                agree += 1
            else:
                wrong.append(name)
            continue
        with_rows += 1
        revenue = {}
        for f in fiscal:
            value = f.get("value")
            if (f.get("mnemonic") == "SALES_REV_TURN" and f.get("scope") == "fiscal_year_line_item"
                    and isinstance(value, (int, float)) and not isinstance(value, bool)):
                revenue.setdefault(str(f.get("fiscal_year")), value)
        ties, _total = _own_tie(rows, revenue)
        is_labelled = _period(got, 1).get("fiscal_year") is not None
        labelled += is_labelled
        if not is_labelled:
            unlabelled.append(name)
        if is_labelled == ties and set(got) == KEYS and (is_labelled or _plain(_period(got, 1).get("note"))):
            agree += 1
        else:
            wrong.append("%s (labelled %s, own tie %s)" % (name, is_labelled, ties))
    print("   stored names %d; serving revenue rows %d; Period 1 labelled %d; Period 1 unlabelled %d %s; e.g. wrong %s"
          % (len(folders), with_rows, labelled, len(unlabelled), unlabelled[:6], wrong[:4]))
    clause("S4 every stored name is served, and its Period 1 is labelled exactly when its level-1 rows tie to a stored year",
           bool(folders) and agree == len(folders), "%d of %d" % (agree, len(folders)))


def _ac3(clause):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + list(TESTS),
                       capture_output=True, timeout=300)
    tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1].strip()
    print("   " + tail)
    clause("B1 the plant tests of the reader, the period labels and the filing-text breakdown pass",
           p.returncode == 0 and " passed" in tail and "failed" not in tail, "rc=%d" % p.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    def verdict():
        yes = bool(ok) and all(ok)
        print("R79 CC2 %s SERVED: %s" % (a.crit, "YES" if yes else "NO"))
        return 0 if yes else 1

    if a.crit == "AC3":
        _ac3(clause)
        return verdict()
    mod, fn = _load(clause)
    if fn is None:
        return verdict()
    try:
        if a.crit == "AC1":
            _ac1(mod, fn, clause)
        else:
            _ac2(fn, clause)
    except Exception as err:  # noqa: BLE001 -- a check that cannot finish is a FAIL with its cause, never a traceback
        clause("C9 the check ran to its end", False, "%s: %s" % (type(err).__name__, str(err)[:160]))
    return verdict()


if __name__ == "__main__":
    sys.exit(main())
