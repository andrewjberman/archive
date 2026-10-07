"""AMGT_RESAPP round 78 -- AMGT-bb-1: the segments reader (round-77 analysis ruling 3, FWD-1).

  --crit AC1|AC2|AC3 --where local

The cell builds `lib.research.api.segment_table.read_segment_table(security_key, client=None)`, a reader of the NEWEST
usable stored Bloomberg segments object for a name. It returns
  {status, rows, operating_income_rows, periods, period_note, currency, currency_note, reason, source}
where a row is {segment, level, values} and `values` holds five entries, each a number or None.

AC1 (build, the seam against the real store; reads only):
    C1 AMD_US_Equity serves revenue rows: every row a clean segment name (no leading, trailing or non-breaking space),
       an integer level and five values each a number or None; no value sits between 0 and 1e-6 in size (the
       missing-period marker is served as None); the source object is the newest stored object that carries the table;
    C2 BP/_LN_Equity serves rows (its folder is written slash-safe);
    C3 8306_JP_Equity (stored, no revenue lines) and a name never stored each read rows [] and a plain reason, and the
       two reasons differ;
    C4 the denominator: every stored name is read without an exception, and it serves revenue rows exactly when its
       newest usable object carries revenue lines (N of N printed, with the served and the reason counts);
    C5 a served table states its periods and currency plainly: five period labels, a period note, a currency note, and
       `currency` None (the stored object carries neither a fiscal period nor a currency).
AC2 (build, planted objects behind a fake store client; no network):
    F1 a newer object holding only refused fields is not chosen over an older one that carries the table;
    F2 a non-breaking-space indent is stripped, the level is kept, a near-zero marker is None and a true 0.0 stays 0.0;
    F3 a table of share-capital lines, and a table under one repeated heading, each read rows [] with a reason that
       does not call the source a filing;
    F4 a store read that raises reads rows [] and a reason, never an exception;
    F5 a slash name is found under its slash-safe folder.
AC3 (build): the plant tests in lib/research/api/tests/test_segment_table.py pass.
Verdict: R78 BB1 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys

BUCKET = "opal-data-harvest"
PREFIX = "bloomberg/harvest/bronze/segments/"
TEST = "lib/research/api/tests/test_segment_table.py"
BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
          "input ledger", "bronze")
NBSP = chr(160)
MARKER = -2.4245362661989844e-14


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


def _body(security, response, pulled_at="2026-10-07T11:51:13Z"):
    return json.dumps({"security": security, "pulled_at": pulled_at, "response": response}).encode("utf-8")


def _row(name, level, values):
    out = {"Metric Name": name, "Product Geographic Hierarchy Level": level}
    for i, v in enumerate(values, 1):
        out["Period %d Value" % i] = v
    return out


def _plain(reason):
    return isinstance(reason, str) and bool(reason.strip()) and not any(w in reason.casefold() for w in BANNED)


def _rows_ok(rows):
    for row in rows:
        seg, vals = row.get("segment"), row.get("values")
        if not isinstance(seg, str) or not seg or seg != seg.strip() or NBSP in seg:
            return False, "segment %r" % (seg,)
        if not isinstance(row.get("level"), int) or isinstance(row.get("level"), bool):
            return False, "level %r" % (row.get("level"),)
        if not isinstance(vals, list) or len(vals) != 5:
            return False, "values %r" % (vals,)
        for v in vals:
            if v is None:
                continue
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                return False, "value %r" % (v,)
            if v != 0 and abs(v) < 1e-6:
                return False, "near-zero marker served %r" % (v,)
    return True, "%d row(s)" % len(rows)


def _usable(response):
    errors = response.get("__field_errors__") or {}
    if "PG_REVENUE" in errors:
        return False
    return ("PG_REVENUE" in response or "PG_OPERATING_INCOME" in response) or not errors


def _ac1(fn, clause):
    import boto3

    from lib.research.identity import crosswalk

    s3 = boto3.client("s3", region_name="us-east-1")
    listed = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"][len(PREFIX):].split("/")
            if len(parts) == 2 and parts[0].startswith("security_key=") and parts[1].endswith(".json"):
                listed.setdefault(parts[0][len("security_key="):], []).append(obj["Key"])
    expect = {}
    for folder, keys in listed.items():
        name = crosswalk.security_key_from_slash_safe(folder)
        chosen, has_rows = None, False
        # AMENDMENT 1 (row Z-W289-S1): among the five newest, an object that carries a segment list wins over a newer object
        # that carries none (a pull of other fields into the same folder); only when none carries one is the newest
        # error-free object taken.
        bodies = []
        for key in sorted(keys, reverse=True)[:5]:
            response = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8")).get("response") or {}
            bodies.append((key, response))
        with_table = [(k, r) for k, r in bodies if "PG_REVENUE" not in (r.get("__field_errors__") or {})
                      and ("PG_REVENUE" in r or "PG_OPERATING_INCOME" in r)]
        fallback = [(k, r) for k, r in bodies if _usable(r)]
        pick = (with_table or fallback or [(None, {})])[0]
        chosen, has_rows = pick[0], bool(pick[1].get("PG_REVENUE"))
        expect[name] = (chosen, has_rows)

    amd = fn("AMD_US_Equity", client=s3)
    ok, detail = _rows_ok(amd.get("rows") or [])
    src = (amd.get("source") or {}).get("object")
    clause("C1 AMD serves clean revenue rows from the newest object that carries the table",
           bool(amd.get("rows")) and ok and src == expect.get("AMD_US_Equity", (None,))[0],
           "%s; source %s" % (detail, str(src).rsplit("/", 1)[-1]))
    bp = fn("BP/_LN_Equity", client=s3)
    clause("C2 a slash name serves rows", bool(bp.get("rows")) and _rows_ok(bp.get("rows") or [])[0],
           "%d row(s)" % len(bp.get("rows") or []))
    none_a, none_b = fn("8306_JP_Equity", client=s3), fn("ZZZZ_US_Equity", client=s3)
    print("   stored, no revenue lines: %r" % (none_a.get("reason"),))
    print("   never stored: %r" % (none_b.get("reason"),))
    clause("C3 two kinds of nothing each read their own plain reason",
           not none_a.get("rows") and not none_b.get("rows") and _plain(none_a.get("reason")) and _plain(none_b.get("reason"))
           and none_a.get("reason") != none_b.get("reason"))
    agree, served, reasoned, wrong = 0, 0, 0, []
    for name, (_chosen, has_rows) in sorted(expect.items()):
        try:
            got = fn(name, client=s3)
        except Exception as err:  # noqa: BLE001 -- the reader must never raise; a raise is a counted failure
            wrong.append("%s raised %s" % (name, type(err).__name__))
            continue
        rows = got.get("rows") or []
        served += bool(rows)
        reasoned += (not rows and _plain(got.get("reason")))
        if bool(rows) == has_rows and _rows_ok(rows)[0] and (rows or _plain(got.get("reason"))):
            agree += 1
        else:
            wrong.append(name)
    print("   stored names %d; serving revenue rows %d; reading a plain reason %d; e.g. wrong %s"
          % (len(expect), served, reasoned, wrong[:4]))
    clause("C4 every stored name reads as its newest usable object says", bool(expect) and agree == len(expect),
           "%d of %d" % (agree, len(expect)))
    periods = amd.get("periods")
    clause("C5 a served table states its periods and currency plainly",
           isinstance(periods, list) and len(periods) == 5 and _plain(amd.get("period_note"))
           and _plain(amd.get("currency_note")) and amd.get("currency") is None,
           "periods %r currency %r" % (periods, amd.get("currency")))


def _ac2(fn, clause):
    good = _body("TEST US Equity", {"NAME": "TEST CO", "PG_REVENUE": [
        _row("Cloud", 1, [10.0, 9.0, 8.0, MARKER, MARKER]),
        _row(NBSP * 3 + "Hosting", 2, [6.0, 0.0, MARKER, MARKER, MARKER]),
        _row("Devices", 1, [4.0, 3.0, 2.0, 1.0, 0.5])],
        "PG_OPERATING_INCOME": [_row("Cloud", 1, [2.0, 1.0, MARKER, MARKER, MARKER])]})
    probe = _body("TEST US Equity", {"NAME": "TEST CO", "__field_errors__": {"SEGMENT_NAME": "BAD_FLD"}},
                  pulled_at="2026-10-08T09:00:00Z")
    base = PREFIX + "security_key=TEST_US_Equity/"
    older, newer = base + "20261007T115113Z.json", base + "20261008T090000Z.json"
    got = fn("TEST_US_Equity", client=FakeStore({older: good, newer: probe}))
    clause("F1 a newer object of refused fields is not chosen", bool(got.get("rows"))
           and (got.get("source") or {}).get("object") == older, str((got.get("source") or {}).get("object")).rsplit("/", 1)[-1])
    by_name = {r.get("segment"): r for r in got.get("rows") or []}
    hosting, cloud = by_name.get("Hosting") or {}, by_name.get("Cloud") or {}
    clause("F2 indent stripped, level kept, the marker None, a true zero kept",
           hosting.get("level") == 2 and hosting.get("values") == [6.0, 0.0, None, None, None]
           and cloud.get("values") == [10.0, 9.0, 8.0, None, None]
           and [r.get("segment") for r in got.get("operating_income_rows") or []] == ["Cloud"],
           "Hosting %r" % (hosting.get("values"),))
    capital = _body("CAP US Equity", {"NAME": "CAP CO", "PG_REVENUE": [
        _row("Ordinary shares outstanding", 1, [5.0, 5.0, 5.0, 5.0, 5.0]),
        _row("Treasury shares", 1, [1.0, 1.0, 1.0, 1.0, 1.0]),
        _row("Share capital", 1, [2.0, 2.0, 2.0, 2.0, 2.0])]})
    one = _body("ONE US Equity", {"NAME": "ONE CO", "PG_REVENUE": [
        _row("Total", 1, [5.0, 5.0, 5.0, 5.0, 5.0]), _row("Total", 1, [1.0, 1.0, 1.0, 1.0, 1.0])]})
    r_cap = fn("CAP_US_Equity", client=FakeStore({PREFIX + "security_key=CAP_US_Equity/20261007T115113Z.json": capital}))
    r_one = fn("ONE_US_Equity", client=FakeStore({PREFIX + "security_key=ONE_US_Equity/20261007T115113Z.json": one}))
    print("   share capital: %r" % (r_cap.get("reason"),))
    print("   one heading: %r" % (r_one.get("reason"),))
    clause("F3 share-capital lines and one repeated heading are refused with a reason that names no filing",
           all(not r.get("rows") and _plain(r.get("reason")) and "filing" not in r.get("reason").casefold()
               for r in (r_cap, r_one)))
    try:
        failed = fn("TEST_US_Equity", client=FakeStore({}, fail=True))
        clause("F4 a store read that raises reads a reason", not failed.get("rows") and _plain(failed.get("reason")),
               repr(failed.get("reason")))
    except Exception as err:  # noqa: BLE001 -- the raise IS the failure being tested for
        clause("F4 a store read that raises reads a reason", False, "raised %s" % type(err).__name__)
    slash = PREFIX + "security_key=BP-SLASH-_LN_Equity/20261007T115120Z.json"
    r_slash = fn("BP/_LN_Equity", client=FakeStore({slash: good}))
    clause("F5 a slash name is found under its slash-safe folder", bool(r_slash.get("rows"))
           and (r_slash.get("source") or {}).get("object") == slash)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC3":
        if not os.path.isfile(TEST):
            clause("C1 the plant test file exists", False, TEST)
            return verdict(a, ok)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST], capture_output=True,
                           timeout=100)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 every plant case passes", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    try:
        from lib.research.api import segment_table
    except ImportError as err:
        clause("C0 lib.research.api.segment_table imports", False, str(err))
        return verdict(a, ok)
    fn = getattr(segment_table, "read_segment_table", None)
    if not callable(fn):
        clause("C0 segment_table.read_segment_table exists", False, "absent")
        return verdict(a, ok)
    if a.crit == "AC1":
        _ac1(fn, clause)
    else:
        _ac2(fn, clause)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB1 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
