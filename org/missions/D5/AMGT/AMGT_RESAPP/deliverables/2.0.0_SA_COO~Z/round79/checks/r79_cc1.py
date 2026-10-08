"""AMGT_RESAPP round 79 -- AMGT-cc-1: the segments reader finds a stored table however many later pulls sit above it.

  python r79_cc1.py --crit AC1|AC2|AC3 --where local

Round 78 built `lib.research.api.segment_table.read_segment_table`; it reads the FIVE newest objects of a name's folder and
chooses among those, so five newer objects without a segment list would hide a stored table behind the sentence "no revenue
by business line" (round-78 analysis, enrichment item 1). This cell walks newest first, stops at the first object that
carries a segment list, reads at most MAX_READ = 20 bodies, and says so in plain words when it stopped with objects unread.

AC1 (build, planted objects behind a fake store client; no network):
    P1 a table under six newer objects that carry no segment list is served, from the table's own object;
    P2 the reader stops at the first object that carries a table: eight objects, the newest carries it, ONE body read;
    P3 MAX_READ is 20;
    P4 MAX_READ + 3 newer objects with no segment list above a table: rows [], bodies read equal MAX_READ, no source, and
       a plain reason that states the number, says the older ones were not looked at, and is none of the three older
       sentences (nothing stored / no business-line table / no revenue by business line);
    P5 a folder read to its end keeps its round-78 answers: three error-free objects with no segment list read the
       no-revenue sentence with the newest as source; three objects of refused fields read the no-table sentence.
AC2 (build, the seam against the real store; reads only):
    S1 AMD_US_Equity serves revenue rows from the newest stored object that carries the table, and the reader read exactly
       as many bodies as it takes to reach that object;
    S2 the denominator: every stored name is read without an exception, serves revenue rows exactly when the newest object
       of its WHOLE folder that carries a table has revenue lines, and reads no more bodies than it takes to reach that
       object (N of N printed, with the deepest folder and the most bodies any name needed).
AC3 (bound): the seventeen round-78 plant cases are all still in lib/research/api/tests/test_segment_table.py and the file
    passes.
Verdict: R79 CC1 <CRIT> SERVED: YES|NO (exit 0|1). AC2 reads the store; nothing is written.
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
N_STATED = 20
BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
          "input ledger", "bronze")
OLD_REASONS = (
    "No Bloomberg segment table has been stored for this name yet.",
    "Bloomberg's stored segment data for this name holds no business-line table yet.",
    "Bloomberg's stored table for this name has no revenue by business line.",
)
R78_TESTS = (
    "test_served_table", "test_newer_probe_is_skipped",
    "test_newer_error_free_object_without_table_does_not_hide_stored_table", "test_revenue_field_error_is_skipped",
    "test_marker_and_true_zero", "test_indent_stripped_level_kept", "test_share_capital_refused",
    "test_one_heading_refused", "test_nothing_no_object", "test_nothing_objects_none_usable",
    "test_nothing_no_revenue_lines", "test_nothing_no_key", "test_nothing_read_failed",
    "test_garbled_object_reads_failed_not_raise", "test_slash_name_found_in_slash_safe_folder",
    "test_other_names_folder_not_read", "test_reasons_use_plain_words",
)


class FakeStore:
    """A store client serving planted objects: the two calls the reader may make. It counts the bodies read."""

    def __init__(self, objects):
        self.objects = dict(objects)
        self.reads = []

    def get_paginator(self, _name):
        return self

    def paginate(self, **kwargs):
        prefix = kwargs.get("Prefix", "")
        yield {"Contents": [{"Key": k, "Size": len(v)} for k, v in sorted(self.objects.items()) if k.startswith(prefix)]}

    def get_object(self, **kwargs):
        self.reads.append(kwargs["Key"])
        return {"Body": io.BytesIO(self.objects[kwargs["Key"]])}


class Counting:
    """The real store client, with the bodies read counted."""

    def __init__(self, inner):
        self.inner = inner
        self.gets = 0

    def get_paginator(self, name):
        return self.inner.get_paginator(name)

    def get_object(self, **kwargs):
        self.gets += 1
        return self.inner.get_object(**kwargs)


def _body(response, pulled_at="2026-10-07T11:51:13Z"):
    return json.dumps({"security": "TEST US Equity", "pulled_at": pulled_at, "response": response}).encode("utf-8")


def _row(name, level, values):
    out = {"Metric Name": name, "Product Geographic Hierarchy Level": level}
    for i, v in enumerate(values, 1):
        out["Period %d Value" % i] = v
    return out


def _plain(reason):
    return isinstance(reason, str) and bool(reason.strip()) and not any(w in reason.casefold() for w in BANNED)


def _carries(response):
    errors = response.get("__field_errors__") or {}
    return "PG_REVENUE" not in errors and ("PG_REVENUE" in response or "PG_OPERATING_INCOME" in response)


GOOD = _body({"NAME": "TEST CO", "PG_REVENUE": [_row("Cloud", 1, [10.0, 9.0, 8.0, 7.0, 6.0]),
                                                _row("Devices", 1, [4.0, 3.0, 2.0, 1.0, 0.5])]})
OTHER = _body({"NAME": "TEST CO", "PX_LAST": 1.0})
PROBE = _body({"NAME": "TEST CO", "__field_errors__": {"SEGMENT_NAME": "BAD_FLD"}})
BASE = PREFIX + "security_key=TEST_US_Equity/"


def _stamp(day, hour=0):
    return BASE + "202611%02dT%02d0000Z.json" % (day, hour)


def _ac1(mod, clause):
    fn = mod.read_segment_table
    table_key = _stamp(1)
    six = {_stamp(2 + i): OTHER for i in range(6)}
    store = FakeStore(dict(six, **{table_key: GOOD}))
    got = fn("TEST_US_Equity", client=store)
    clause("P1 a table under six newer objects with no segment list is served",
           got.get("status") == "served" and len(got.get("rows") or []) == 2
           and (got.get("source") or {}).get("object") == table_key,
           "status %r rows %d source %s bodies read %d reason %r" % (
               got.get("status"), len(got.get("rows") or []), str((got.get("source") or {}).get("object")).rsplit("/", 1)[-1],
               len(store.reads), got.get("reason")))

    eight = {_stamp(1 + i): GOOD for i in range(8)}
    store = FakeStore(eight)
    got = fn("TEST_US_Equity", client=store)
    clause("P2 the reader stops at the first object that carries a table",
           got.get("status") == "served" and store.reads == [_stamp(8)], "bodies read %d" % len(store.reads))

    cap = getattr(mod, "MAX_READ", None)
    clause("P3 MAX_READ is %d" % N_STATED, cap == N_STATED and not isinstance(cap, bool), "MAX_READ %r" % (cap,))

    cap_n = cap if isinstance(cap, int) and not isinstance(cap, bool) and 0 < cap < 500 else N_STATED
    deep = {_stamp(1, 0): GOOD}
    for i in range(cap_n + 3):
        deep[_stamp(2 + i // 24, i % 24)] = OTHER
    store = FakeStore(deep)
    got = fn("TEST_US_Equity", client=store)
    reason = got.get("reason")
    clause("P4 objects left unread are said to be unread, never called no revenue",
           got.get("status") == "none" and not got.get("rows") and got.get("source") is None and _plain(reason)
           and reason not in OLD_REASONS and str(cap_n) in reason and "not looked at" in reason
           and len(store.reads) == cap_n,
           "bodies read %d of %d; reason %r" % (len(store.reads), len(deep), reason))

    three_other = {_stamp(1 + i): OTHER for i in range(3)}
    three_probe = {_stamp(1 + i): PROBE for i in range(3)}
    s_other, s_probe = FakeStore(three_other), FakeStore(three_probe)
    r_other, r_probe = fn("TEST_US_Equity", client=s_other), fn("TEST_US_Equity", client=s_probe)
    clause("P5 a folder read to its end keeps its round-78 answers",
           r_other.get("reason") == OLD_REASONS[2] and (r_other.get("source") or {}).get("object") == _stamp(3)
           and r_probe.get("reason") == OLD_REASONS[1] and r_probe.get("source") is None
           and len(s_other.reads) == 3 and len(s_probe.reads) == 3,
           "no list: %r; refused fields: %r" % (r_other.get("reason"), r_probe.get("reason")))


def _ac2(mod, clause):
    import boto3

    from lib.research.identity import crosswalk

    fn = mod.read_segment_table
    cap = getattr(mod, "MAX_READ", None)
    cap_n = cap if isinstance(cap, int) and not isinstance(cap, bool) and cap > 0 else N_STATED
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
        chosen, has_rows, needed = None, False, None
        ordered = sorted(keys, reverse=True)
        for i, key in enumerate(ordered[:cap_n]):  # the WHOLE folder, up to the reader's own stated limit
            response = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8")).get("response") or {}
            if _carries(response):
                chosen, has_rows, needed = key, bool(response.get("PG_REVENUE")), i + 1
                break
        expect[name] = (chosen, has_rows, needed if needed is not None else min(len(ordered), cap_n), len(ordered))

    amd_expect = expect.get("AMD_US_Equity", (None, False, 0, 0))
    client = Counting(s3)
    amd = fn("AMD_US_Equity", client=client)
    src = (amd.get("source") or {}).get("object")
    clause("S1 AMD serves its rows from the newest object that carries the table and reads no body past it",
           bool(amd.get("rows")) and src is not None and src == amd_expect[0] and client.gets == amd_expect[2],
           "source %s; bodies read %d, needed %d, in the folder %d" % (
               str(src).rsplit("/", 1)[-1], client.gets, amd_expect[2], amd_expect[3]))

    agree, served, wrong = 0, 0, []
    for name, (_chosen, has_rows, needed, _count) in sorted(expect.items()):
        client = Counting(s3)
        try:
            got = fn(name, client=client)
        except Exception as err:  # noqa: BLE001 -- the reader must never raise; a raise is a counted failure
            wrong.append("%s raised %s" % (name, type(err).__name__))
            continue
        rows = got.get("rows") or []
        served += bool(rows)
        if bool(rows) == has_rows and (rows or _plain(got.get("reason"))) and client.gets <= needed:
            agree += 1
        else:
            wrong.append("%s (rows %d, bodies read %d, needed %d)" % (name, len(rows), client.gets, needed))
    print("   stored names %d; serving revenue rows %d; deepest folder %d object(s); most bodies needed %d; MAX_READ %r; "
          "e.g. wrong %s" % (len(expect), served, max([e[3] for e in expect.values()] or [0]),
                             max([e[2] for e in expect.values()] or [0]), cap, wrong[:4]))
    clause("S2 every stored name reads as its whole folder says and reads no body it does not need",
           bool(expect) and agree == len(expect), "%d of %d" % (agree, len(expect)))


def _ac3(clause):
    if not os.path.isfile(TEST):
        clause("B1 the round-78 plant test file exists", False, TEST)
        return
    with open(TEST, encoding="utf-8") as handle:
        text = handle.read()
    missing = [name for name in R78_TESTS if ("def %s(" % name) not in text]
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST],
                       capture_output=True, timeout=300)
    tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1].strip()
    print("   " + tail)
    clause("B1 the seventeen round-78 plant cases are all still there and the file passes",
           not missing and p.returncode == 0 and " passed" in tail and "failed" not in tail,
           "rc=%d; round-78 cases present %d of %d %s" % (p.returncode, len(R78_TESTS) - len(missing), len(R78_TESTS),
                                                        missing[:3] if missing else ""))


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
        print("R79 CC1 %s SERVED: %s" % (a.crit, "YES" if yes else "NO"))
        return 0 if yes else 1

    if a.crit == "AC3":
        _ac3(clause)
        return verdict()
    try:
        from lib.research.api import segment_table
    except Exception as err:  # noqa: BLE001 -- any import failure is the first clause of a build check
        clause("C0 lib.research.api.segment_table imports", False, str(err)[:160])
        return verdict()
    if not callable(getattr(segment_table, "read_segment_table", None)):
        clause("C0 segment_table.read_segment_table exists", False, "absent")
        return verdict()
    try:
        if a.crit == "AC1":
            _ac1(segment_table, clause)
        else:
            _ac2(segment_table, clause)
    except Exception as err:  # noqa: BLE001 -- a check that cannot finish is a FAIL with its cause, never a traceback
        clause("C9 the check ran to its end", False, "%s: %s" % (type(err).__name__, str(err)[:160]))
    return verdict()


if __name__ == "__main__":
    sys.exit(main())
