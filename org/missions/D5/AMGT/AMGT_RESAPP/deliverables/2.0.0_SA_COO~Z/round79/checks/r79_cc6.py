"""AMGT_RESAPP round 79 -- AMGT-cc-6, the adapter cell: every hookup of the round, read through the handler.

  python r79_cc6.py --crit AC1 --where local|deployed
  python r79_cc6.py --crit AC2 --where local
  python r79_cc6.py --crit AC3 --where local

AC1 (build) the round's hookups are served. `--where local` runs the handler in-process on the tree; `--where deployed`
invokes the function (GET-shaped direct invokes, read only) and is the line the redeploy's list carries.
  H1 segment table (cc-2): /thesis for AMD_US_Equity carries `segment_table`, status served, 6 rows, the first column
     named fiscal year 2025, currency USD;
  H2 a name whose first column ties to no stored year (8766_JP_Equity) serves its rows with that column unnamed and a
     note saying why; a name with no stored table (HD_US_Equity) reads a plain reason that is not the read-failed one;
  H3 research-note sections (cc-4): /thesis for ASML_NA_Equity carries `dossier_sections`, five entries in the fixed
     order, the first served with the stored text;
  H4 a name whose notes hold none of the five (AMD_US_Equity) serves five absent entries, each with a plain reason;
  H5 Seeking Alpha column (cc-3): GET /freshness?view=page (the page's own request) carries `seeking_alpha` with a
     state and a sentence on every covered row (95 of 95); every state is read, checked or no_record (unreadable is
     accepted with `--where local` only, for a box that cannot list the records); a row that is not `read` carries no
     date and is not flagged stale; a `read` row carries a compact stamp; no served Seeking Alpha date is 2026-09-11;
  K1 GET /freshness (the default body) keeps every other field it served before, carries the three added fields and
     no longer carries the two retired ones.
  L1-L3 (`--where local` only: the wiring, which no served body can show)
     L1 one build of the view asks the record reader once;
     L2 a page request answered from a stored snapshot asks it not at all;
     L3 a record read that fails writes no snapshot (the write is made against a recording stand-in, never the store).

  DEPLOYED, H5 and K1: the freshness route reads a STORED SNAPSHOT that only the scheduled event
  {"amgt_scheduled_action": "refresh_freshness_snapshot"} re-writes. Until that event has run on the new code the
  stored snapshot is the old code's and H5 and K1 read NO. They are meaningful only after the redeploy's snapshot
  event; H5 prints the snapshot's stamp so the reader can see which one answered. This check never sends that event.
  LOCAL, H5 and K1: the stored snapshot is set aside in memory so the tree's own view answers (nothing is written).

AC2 (bound) the round-78 served shape still holds on the tree: r78_bb17.py --crit AC1 --where local reads YES.
AC3 (bound) lib/research/api/tests/ and lib/research/freshness/tests/ pass, apart from the failures named in
     KNOWN_BASE_FAILURES (printed), and no fewer tests pass than at the draft.
Verdict: R79 CC6 <crit> SERVED: YES|NO (exit 0|1). Read-only: no store write, no vendor, web or model call.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
D = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/"

TABLE_NAME = "AMD_US_Equity"
UNTIED_NAME = "8766_JP_Equity"
NO_TABLE_NAME = "HD_US_Equity"
NOTES_NAME = "ASML_NA_Equity"
NO_SECTIONS_NAME = "AMD_US_Equity"
FIELD_ORDER = ("company_description", "why_we_own", "positives", "negatives", "special_items")
NOTES_OPEN = "COMPANY DESCRIPTION:What started as a failing joint venture"
SEGMENT_READ_FAILED = "The Bloomberg segment table for this name could not be read just now."
NOTES_READ_FAILED = "The research notes for this company could not be read just now."

COVERED_AT_THE_DRAFT = 95
STATES = ("read", "checked", "no_record")
PILOT_DAY = "20260911"
COMPACT = re.compile(r"^[0-9]{8}T[0-9]{6}Z$")
SA_KEYS = ("state", "sentence", "last_read", "newest_job_finished_at", "newest_job_status")

# The default /freshness body as served before this cell (read at the draft, scoped_amgt.py blob afe19b30ce43).
ROW_KEYS_BEFORE = ("covered", "reason", "name", "security_key", "security_key_basis", "source", "last_refreshed",
                   "per_input", "pack", "rot")
DENOMINATORS_KEPT = ("names", "covered_names", "covered_names_added", "covered_read_error", "universe_denominators",
                     "security_key_basis", "with_something_landed", "never_refreshed", "bloomberg_bronze_objects_listed",
                     "bright_data_serp_objects_listed", "pack_objects_listed", "vendor_inputs")
READS_KEPT = ("universe", "bloomberg_bronze", "bright_data_serp", "packs", "lists")
TOP_KEPT = ("rows", "denominators", "rot", "reads", "generated_at")
RETIRED = (("denominators", "seeking_alpha_bronze_objects_listed"), ("reads", "seeking_alpha_bronze"))
ADDED = (("denominators", "seeking_alpha_job_record_objects_listed"), ("denominators", "seeking_alpha_states"),
         ("reads", "seeking_alpha_job_record"))

KNOWN_BASE_FAILURES = ("lib/research/api/tests/test_harvest_prefixes.py::test_ii_registry_hash_matches",)
PASSED_AT_THE_DRAFT = 860
TEST_DIRS = ("lib/research/api/tests/", "lib/research/freshness/tests/")


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _reader(where):
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(event):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        def raw(event):
            return scoped_amgt.handler(event)

    def body(path, query=None):
        event = {"rawPath": PREFIX + path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
                 "queryStringParameters": query}
        try:
            r = raw(event)
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
        except Exception as err:  # noqa: BLE001 -- a read that fails is a FAIL line, never a crash of the check
            return "%s: %s" % (type(err).__name__, str(err)[:120]), {}

    return body


def _d(value):
    return value if isinstance(value, dict) else {}


def _l(value):
    return value if isinstance(value, list) else []


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _has_day(value):
    text = str(value or "")
    return len(text) >= 8 and text[:4].isdigit()


class _Recorder:
    """A stand-in store client that records a write and never makes one."""

    def __init__(self):
        self.puts = []

    def put_object(self, **kwargs):
        self.puts.append(kwargs.get("Key"))
        return {"ETag": "recorded-not-written"}


class _Refusing:
    """A stand-in store client whose listing fails."""

    def get_paginator(self, _name):
        raise RuntimeError("the check made this listing fail")

    def get_object(self, **_kwargs):
        raise RuntimeError("the check made this read fail")


def _thesis_clauses(body, clause):
    code_t, th_table = body("/security/%s/thesis" % TABLE_NAME)
    st = th_table.get("segment_table")
    periods = _l(_d(st).get("periods"))
    p1 = _d(periods[0]) if periods else {}
    clause("H1 the thesis serves the Bloomberg segment table with its first column named and its currency",
           isinstance(st, dict) and st.get("status") == "served" and len(_l(st.get("rows"))) == 6
           and p1.get("fiscal_year") == "2025" and st.get("currency") == "USD",
           "%s http %s; segment_table %s; status %r; rows %d; first column %r %r; currency %r units %r" % (
               TABLE_NAME, code_t, "present" if isinstance(st, dict) else "ABSENT", _d(st).get("status"),
               len(_l(_d(st).get("rows"))), p1.get("label"), p1.get("fiscal_year"), _d(st).get("currency"),
               _d(st).get("units")))

    code_u, th_untied = body("/security/%s/thesis" % UNTIED_NAME)
    su = _d(th_untied.get("segment_table"))
    u1 = _d(_l(su.get("periods"))[0]) if _l(su.get("periods")) else {}
    code_n, th_none = body("/security/%s/thesis" % NO_TABLE_NAME)
    sn = th_none.get("segment_table")
    untied_ok = (su.get("status") == "served" and bool(_l(su.get("rows"))) and u1.get("label") == "Period 1"
                 and u1.get("fiscal_year") is None and _text(u1.get("note")))
    none_ok = (isinstance(sn, dict) and sn.get("status") == "none" and not _l(sn.get("rows"))
               and _text(sn.get("reason")) and sn.get("reason") != SEGMENT_READ_FAILED)
    clause("H2 a first column that ties to no year is served unnamed with its note, and no stored table reads a plain reason",
           untied_ok and none_ok,
           "%s http %s status %r rows %d first column %r year %r note %r; %s http %s status %r reason %r" % (
               UNTIED_NAME, code_u, su.get("status"), len(_l(su.get("rows"))), u1.get("label"), u1.get("fiscal_year"),
               u1.get("note"), NO_TABLE_NAME, code_n, _d(sn).get("status"), _d(sn).get("reason")))

    code_a, th_notes = body("/security/%s/thesis" % NOTES_NAME)
    ds = th_notes.get("dossier_sections")
    fields = [_d(e).get("field") for e in _l(ds)]
    first = _d(_l(ds)[0]) if _l(ds) else {}
    clause("H3 the thesis serves the five research-note sections in the fixed order, the first with its stored text",
           isinstance(ds, list) and len(ds) == 5 and tuple(fields) == FIELD_ORDER and first.get("status") == "served"
           and str(first.get("text") or "").startswith(NOTES_OPEN),
           "%s http %s; dossier_sections %s; fields %s; first status %r; text opens %r" % (
               NOTES_NAME, code_a, "present (%d)" % len(ds) if isinstance(ds, list) else "ABSENT", fields,
               first.get("status"), str(first.get("text") or "")[:len(NOTES_OPEN)]))

    da = th_table.get("dossier_sections") if NO_SECTIONS_NAME == TABLE_NAME else body(
        "/security/%s/thesis" % NO_SECTIONS_NAME)[1].get("dossier_sections")
    entries = [_d(e) for e in _l(da)]
    reasons = [e.get("reason") for e in entries]
    clause("H4 a name whose notes hold none of the five serves five absent entries, each with a plain reason",
           isinstance(da, list) and len(entries) == 5 and all(e.get("status") == "absent" and e.get("text") is None for e in entries)
           and all(_text(r) and r != NOTES_READ_FAILED for r in reasons),
           "%s dossier_sections %s; statuses %s; first reason %r" % (
               NO_SECTIONS_NAME, "present (%d)" % len(entries) if isinstance(da, list) else "ABSENT",
               [e.get("status") for e in entries], reasons[0] if reasons else None))


def _page_clauses(code, page, where, clause, note):
    rows = [r for r in _l(page.get("rows")) if isinstance(r, dict)]
    stamp = page.get("snapshot") if page.get("snapshot") is not None else page.get("snapshot_fallback")
    note("freshness page http %s; rows %d; view made %s; answered from %s %s" % (
        code, len(rows), page.get("generated_at"), "the stored snapshot" if page.get("snapshot") is not None
        else "no stored snapshot (the view was worked out now)", json.dumps(stamp, sort_keys=True)[:260]))
    allowed = STATES + (("unreadable",) if where == "local" else ())
    states, shaped, off_state, flagged, dated, pilot, bad_stamp, worded = {}, 0, [], [], [], [], [], []
    for row in rows:
        key = row.get("security_key")
        sa = row.get("seeking_alpha")
        state = _d(sa).get("state")
        states[state] = states.get(state, 0) + 1
        if isinstance(sa, dict) and all(k in sa for k in SA_KEYS) and _text(sa.get("sentence")) and _text(state):
            shaped += 1
        if state not in allowed:
            off_state.append((key, state))
        stamp_served = _d(row.get("per_input")).get("seekingalpha")
        rule = _d(_d(row.get("inputs")).get("seekingalpha"))
        if state != "read":
            if rule.get("state") == "stale" or "seekingalpha" in _l(row.get("stale_inputs")):
                flagged.append((key, state))
            if _has_day(stamp_served) or _d(sa).get("last_read") is not None or rule.get("day") is not None:
                dated.append((key, state, stamp_served))
        elif not (isinstance(stamp_served, str) and COMPACT.match(stamp_served)
                  and stamp_served == re.sub(r"[-:]", "", str(_d(sa).get("last_read") or ""))):
            bad_stamp.append((key, stamp_served, _d(sa).get("last_read")))
        served_dates = (str(stamp_served or ""), str(_d(sa).get("last_read") or "").replace("-", ""),
                        str(rule.get("day") or "").replace("-", ""))
        if any(v.startswith(PILOT_DAY) for v in served_dates):
            pilot.append((key, stamp_served))
        if "not collected" in str(_d(sa).get("sentence") or "").lower():
            worded.append(key)
    note("Seeking Alpha states over %d rows: %s" % (len(rows), json.dumps(states, sort_keys=True, default=str)))
    clause("H5a every covered row carries a Seeking Alpha state and its sentence",
           len(rows) == COVERED_AT_THE_DRAFT and shaped == len(rows) and not worded,
           "%d of %d rows (covered names at the draft %d); sentences saying not collected %d" % (
               shaped, len(rows), COVERED_AT_THE_DRAFT, len(worded)))
    clause("H5b every state is one of %s" % ", ".join(allowed), bool(rows) and not off_state,
           "off the list %d %s" % (len(off_state), off_state[:3]))
    clause("H5c a row that is not read carries no date and is not flagged stale; a read row carries a compact stamp",
           bool(rows) and shaped == len(rows) and not flagged and not dated and not bad_stamp,
           "flagged stale %d %s; dated %d %s; read rows without the compact stamp of their date %d %s" % (
               len(flagged), flagged[:3], len(dated), dated[:3], len(bad_stamp), bad_stamp[:3]))
    clause("H5d no served Seeking Alpha date is the pilot's 2026-09-11", bool(rows) and shaped == len(rows) and not pilot,
           "rows dated 2026-09-11: %d %s" % (len(pilot), [p[0] for p in pilot][:5]))


def _default_clause(code, view, clause):
    den, reads = _d(view.get("denominators")), _d(view.get("reads"))
    rows = [r for r in _l(view.get("rows")) if isinstance(r, dict)]
    lost = [k for k in TOP_KEPT if k not in view] + ["denominators." + k for k in DENOMINATORS_KEPT if k not in den] \
        + ["reads." + k for k in READS_KEPT if k not in reads]
    row_lost = sorted(set(k for r in rows for k in ROW_KEYS_BEFORE if k not in r))
    row_extra = sorted(set(k for r in rows for k in r if k not in ROW_KEYS_BEFORE + ("seeking_alpha",)))
    parts = {"denominators": den, "reads": reads}
    still = ["%s.%s" % pk for pk in RETIRED if pk[1] in parts[pk[0]]]
    missing = ["%s.%s" % pk for pk in ADDED if pk[1] not in parts[pk[0]]]
    counts = _d(den.get("seeking_alpha_states"))
    covered = sum(1 for r in rows if r.get("covered"))
    uncovered_with = sum(1 for r in rows if not r.get("covered") and r.get("seeking_alpha") is not None)
    summed = sum(v for v in counts.values() if isinstance(v, int) and not isinstance(v, bool))
    record = _d(reads.get("seeking_alpha_job_record"))
    clause("K1 the default freshness body keeps every other field, carries the three added and not the two retired",
           bool(rows) and not lost and not row_lost and not row_extra and not still and not missing
           and sorted(counts) == ["checked", "no_record", "read", "unreadable"] and summed == covered and not uncovered_with,
           "http %s; rows %d (covered %d); fields lost %s; row fields lost %s, unexpected %s; retired still served %s; "
           "added not served %s; state counts %s; rows not covered that carry the field %d; record read finished %r, objects listed %r" % (
               code, len(rows), covered, lost, row_lost, row_extra, still, missing, json.dumps(counts, sort_keys=True),
               uncovered_with, record.get("read_completed"), record.get("objects_listed")))


def _local_freshness(body, clause, note):
    """The tree's own view through the handler, with the stored snapshot set aside in memory; then the wiring."""
    from lib.research.api import served_cache
    from lib.research.freshness import snapshot as fs

    try:
        from lib.research.freshness import collector_read
    except Exception as err:  # noqa: BLE001
        collector_read = None
        note("lib.research.freshness.collector_read does not import: %s: %s" % (type(err).__name__, err))
    calls = {"n": 0, "fail": False}
    real_reader = getattr(collector_read, "seeking_alpha_by_security", None)
    real_snapshot_read = fs.read_freshness_snapshot

    def counted(covered_keys, client=None):
        calls["n"] += 1
        return real_reader(covered_keys, client=_Refusing() if calls["fail"] else client)

    def no_snapshot(_client, *_a, **_k):
        return None, {"object": None, "generated_at": None, "age_hours": None,
                      "reason": "this check set the stored snapshot aside to read the tree's own view"}

    if real_reader is not None:
        collector_read.seeking_alpha_by_security = counted
    try:
        fs.read_freshness_snapshot = no_snapshot
        served_cache.clear()
        code, page = body("/freshness", {"view": "page"})
        after_build = calls["n"]
        _page_clauses(code, page, "local", clause, note)
        code_d, view = body("/freshness")
        _default_clause(code_d, view, clause)
        # A complete view is held for a minute, so the second request builds nothing; an incomplete one is built again.
        clause("L1 one build of the view asks the record reader once",
               real_reader is not None and after_build == 1 and calls["n"] in (1, 2),
               "calls after the first build %d; after the second request %d (1 when the view was held, 2 when built again)" % (
                   after_build, calls["n"]))

        held = copy.deepcopy(view)
        held.pop("snapshot_fallback", None)
        before = calls["n"]

        def held_snapshot(_client, *_a, **_k):
            return held, {"object": "held in memory by this check", "generated_at": held.get("generated_at"),
                          "age_hours": 0.0, "reason": None}

        fs.read_freshness_snapshot = held_snapshot
        served_cache.clear()
        code_s, page_s = body("/freshness", {"view": "page"})
        clause("L2 a page request answered from a stored snapshot asks the record reader not at all",
               real_reader is not None and before >= 1 and calls["n"] == before and page_s.get("snapshot") is not None
               and len(_l(page_s.get("rows"))) == len(_l(page.get("rows"))),
               "http %s; calls before %d, after %d; answered from a snapshot %s; rows %d" % (
                   code_s, before, calls["n"], page_s.get("snapshot") is not None, len(_l(page_s.get("rows")))))

        recorder = _Recorder()
        calls["fail"] = True
        fs.read_freshness_snapshot = no_snapshot
        served_cache.clear()
        try:
            failed_view = fs.build_freshness_snapshot()
            written = fs.write_freshness_snapshot(recorder, view=failed_view)
            raised = None
        except Exception as err:  # noqa: BLE001
            failed_view, written, raised = {}, {}, "%s: %s" % (type(err).__name__, str(err)[:100])
        covered_rows = [r for r in _l(failed_view.get("rows")) if isinstance(r, dict) and r.get("covered")]
        unreadable = sum(1 for r in covered_rows if _d(r.get("seeking_alpha")).get("state") == "unreadable"
                         and not _has_day(_d(r.get("per_input")).get("seekingalpha")))
        clause("L3 a record read that fails writes no snapshot, and every covered row reads unreadable with no date",
               real_reader is not None and raised is None and written.get("written") is False and not recorder.puts
               and bool(covered_rows) and unreadable == len(covered_rows),
               "raised %s; written %r; writes attempted %d; unreadable with no date %d of %d covered rows; said %r" % (
                   raised, written.get("written"), len(recorder.puts), unreadable, len(covered_rows), written.get("reason")))
    finally:
        fs.read_freshness_snapshot = real_snapshot_read
        if real_reader is not None:
            collector_read.seeking_alpha_by_security = real_reader
        served_cache.clear()


def ac1(where):
    body = _reader(where)
    results = []

    def clause(name, cond, detail=""):
        results.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    def note(text):
        print("   " + text)

    _thesis_clauses(body, clause)
    if where == "local":
        _local_freshness(body, clause, note)
    else:
        code, page = body("/freshness", {"view": "page"})
        _page_clauses(code, page, where, clause, note)
        code_d, view = body("/freshness")
        _default_clause(code_d, view, clause)
        note("L1-L3 (the wiring) are read on the tree only: run --where local")
    ok = bool(results) and all(results)
    print("R79 CC6 AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def ac2():
    root = _root()
    check = D + "round78/checks/r78_bb17.py"
    p = subprocess.run([sys.executable, check, "--crit", "AC1", "--where", "local"], cwd=root, capture_output=True,
                       env=dict(os.environ, PYTHONPATH=root))
    out = p.stdout.decode("utf-8", "replace")
    lines = [ln for ln in out.splitlines() if ln.startswith(("PASS ", "FAIL "))]
    for ln in lines:
        print("   " + ln[:150])
    last = [ln for ln in out.splitlines() if ln.strip()][-1:] or [""]
    ok = p.returncode == 0 and last[0].strip() == "R78 BB17 AC1 SERVED: YES"
    print("%s B1 the round-78 served shape still reads YES on the tree rc=%d; clauses passing %d of %d; %s" % (
        "PASS" if ok else "FAIL", p.returncode, sum(1 for ln in lines if ln.startswith("PASS ")), len(lines), last[0][:120]))
    print("R79 CC6 AC2 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def ac3():
    root = _root()
    p = subprocess.run([sys.executable, "-m", "pytest"] + list(TEST_DIRS) + ["-q", "-p", "no:cacheprovider", "--color=no", "-rfE"],
                       cwd=root, capture_output=True, env=dict(os.environ, PYTHONPATH=root))
    out = p.stdout.decode("utf-8", "replace")
    failed = sorted(set(re.findall(r"^FAILED (\S+)", out, re.M)))
    errors = sorted(set(re.findall(r"^ERROR (\S+)", out, re.M)))
    passed = re.findall(r"(\d+) passed", out)
    passed_n = int(passed[-1]) if passed else 0
    tail = [ln for ln in out.splitlines() if ln.strip()][-1:] or ["no output"]
    new = [f for f in failed if f not in KNOWN_BASE_FAILURES]
    print("   " + tail[0].strip("= ")[:150])
    print("   failures allowed, known at the draft and another cell's to repair: %s" % list(KNOWN_BASE_FAILURES))
    ok = p.returncode in (0, 1) and not new and not errors and passed_n >= PASSED_AT_THE_DRAFT
    print("%s B1 both test folders pass apart from the allowed failures rc=%d; passed %d (at the draft %d); failed %s; of them not allowed %s; errors %s" % (
        "PASS" if ok else "FAIL", p.returncode, passed_n, PASSED_AT_THE_DRAFT, failed, new, errors))
    print("R79 CC6 AC3 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    sys.path.insert(0, _root())
    if a.crit == "AC1":
        return ac1(a.where)
    return ac2() if a.crit == "AC2" else ac3()


if __name__ == "__main__":
    sys.exit(main())
