"""ADVI_INSURE.TO-A3-AE / INSA3AE-AC1 -- the act-(a) dispatch exercise.

Arms are transcribed FROM THE AC1 CRITERION TEXT, field by field, before any implementation was
consulted -- a harness transcribed from the implementation scores its own blind spot as a pass.

AC1 verbatim: "`lambda_handler` routes `{"leg":"insurance"}` to the insurance leg's run path and
leaves the reporting path byte-identical in behaviour; a bare/unknown event with no `q_start` fails
CLOSED with a NAMED reason. Exercised locally on the packaged bytes with THREE arms:
`{"leg":"insurance"}` -> insurance path entered (mocked HTTP, no live call); `{"q_start","q_end"}`
-> reporting path entered, insurance NOT entered; `{}` -> named refusal, no KeyError. Arms differ
on the field under test."

WHAT IS MOCKED AND WHY THAT KEEPS THE TEST HONEST: only the two EXTERNAL boundaries -- the HTTP
socket (`lambda_function._request`) and S3 (`lambda_function._s3`). The dispatch branch, the
pagination loop, the completeness verdict and the fail-closed refusals are the REAL code. A harness
that instead stubbed `run_insurance_leg` would prove only that a sentinel was reachable.

NO LIVE CALL IS POSSIBLE FROM THIS FILE: `_request` is replaced before any arm runs, and the
vehicle's own DRY_RUN gate is left at its fail-closed default besides.

Run:  python ADVI_INSURE.TO-A3-AE_dispatch_exercise.py
"""
from __future__ import annotations

import json
import os
import sys

LAMBDA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", "..",
    "infra", "aws", "lambda", "opal-assets", "opal-assets-bd49f-reporting-pull")
sys.path.insert(0, os.path.abspath(LAMBDA_DIR))

import lambda_function as veh  # noqa: E402
import insurance_leg  # noqa: E402

ATTESTED_TOTAL = 77
PAGE_LIMIT = 50


class Recorder:
    """Records every boundary crossing so an arm asserts on WHAT WAS CALLED, not on a return."""

    def __init__(self, pages):
        self.pages = pages
        self.http = []
        self.puts = []

    def request(self, method, path, cookie=None, token=None, body=None, raw=False):
        self.http.append({"method": method, "path": path, "body": body})
        if "session/token" in path or "datamining/auth/token" in path:
            return {"access_token": "t" * 66}
        if "RelationshipAccountDetailSearch" in path:
            offset = (body or {}).get("offset", 0)
            rows = self.pages.get(offset, [])
            payload = json.dumps({"data": rows, "total": ATTESTED_TOTAL}).encode()
            return payload if raw else json.loads(payload)
        if "insurancerelationshiplist" in path:
            return {"exportResultID": 282394, "resultGuid": "g-1"}
        if path.startswith("/request/api/offline/"):
            return insurance_leg.XLSX_MAGIC + b"fake-workbook"
        if path.startswith("/portfolioreporting/api/"):
            payload = json.dumps({"stub": "reporting", "path": path}).encode()
            return payload if raw else json.loads(payload)
        raise AssertionError("arm reached an unexpected path: %s" % path)

    # -- S3 stand-in -------------------------------------------------------
    def put_object(self, **kw):
        self.puts.append(kw)
        return {}

    def list_objects_v2(self, **kw):
        return {"KeyCount": 1}


def _rows(n, start=0):
    return [{"id": start + i, "name": "rel-%d" % (start + i), "accounts": []} for i in range(n)]


COMPLETE_PAGES = {0: _rows(PAGE_LIMIT), PAGE_LIMIT: _rows(ATTESTED_TOTAL - PAGE_LIMIT, PAGE_LIMIT)}
SHORT_PAGES = {0: _rows(PAGE_LIMIT), PAGE_LIMIT: []}


def install(pages):
    rec = Recorder(pages)
    veh._request = rec.request
    veh._s3 = rec
    insurance_leg.veh._request = rec.request
    insurance_leg.veh._s3 = rec
    return rec


def entered(rec):
    """Which leg did the handler actually reach, judged on the PATHS crossed."""
    ins = any("Relationship" in h["path"] or "insurance" in h["path"] for h in rec.http)
    rep = any("portfolioreporting" in h["path"] for h in rec.http)
    return ins, rep


RESULTS = []


def record(arm, passed, detail):
    RESULTS.append((arm, passed, detail))
    print("[%s] %s\n      %s" % ("PASS" if passed else "FAIL", arm, detail))


def arm1_insurance():
    rec = install(COMPLETE_PAGES)
    out = veh.lambda_handler({"leg": "insurance", "pull_date": "2026-08-28"}, None)
    ins, rep = entered(rec)
    d = out["detailsearch"]
    ok = (ins and not rep
          and d["completeness"] == "measured-complete"
          and d["rows_landed"] == ATTESTED_TOTAL
          and d["page_count"] == 2
          and d["attested_total"] == ATTESTED_TOTAL)
    record("ARM1 {'leg':'insurance'} -> insurance path entered, reporting NOT entered",
           ok,
           "insurance_entered=%s reporting_entered=%s pages=%d rows=%d attested=%s "
           "completeness=%s bronze_puts=%d"
           % (ins, rep, d["page_count"], d["rows_landed"], d["attested_total"],
              d["completeness"], len(rec.puts)))


def arm2_reporting():
    rec = install(COMPLETE_PAGES)
    accounts = [{"bd_account_id": 111, "schwab_account": "1234", "inception": "2024-01-01"}]
    out = veh.lambda_handler(
        {"q_start": "2026-04-01", "q_end": "2026-06-30", "accounts": accounts,
         "pull_date": "2026-08-28"}, None)
    ins, rep = entered(rec)
    ok = rep and not ins and out["count"] == 3
    record("ARM2 {'q_start','q_end'} -> reporting path entered, insurance NOT entered",
           ok,
           "reporting_entered=%s insurance_entered=%s landed=%d by_feed=%s"
           % (rep, ins, out["count"], json.dumps(out["by_feed"])))


def arm3_bare():
    install(COMPLETE_PAGES)
    try:
        veh.lambda_handler({}, None)
    except KeyError as e:
        record("ARM3 {} -> named refusal, NOT a KeyError", False,
               "REGRESSION: raised KeyError(%s) -- the pre-dispatch failure mode" % e)
        return
    except RuntimeError as e:
        msg = str(e)
        named = "REPORTING LEG REFUSED" in msg and "q_start" in msg
        record("ARM3 {} -> named refusal, NOT a KeyError", named,
               "RuntimeError, named=%s: %s" % (named, msg.split(".")[0]))
        return
    record("ARM3 {} -> named refusal, NOT a KeyError", False, "no exception raised at all")


def arm4_unknown_leg():
    install(COMPLETE_PAGES)
    try:
        veh.lambda_handler({"leg": "bogus"}, None)
    except RuntimeError as e:
        msg = str(e)
        record("ARM4 {'leg':'bogus'} -> named refusal (unknown leg)",
               "UNKNOWN LEG" in msg, msg.split(".")[0])
        return
    except KeyError as e:
        record("ARM4 {'leg':'bogus'} -> named refusal (unknown leg)", False,
               "REGRESSION: KeyError(%s)" % e)
        return
    record("ARM4 {'leg':'bogus'} -> named refusal (unknown leg)", False, "no exception raised")


def red_arm_short_pull():
    """THE RED ARM -- reachable from a DIFFERENT truth than the green ones.

    Reproduces the 2026-08-27 defect exactly: the server attests 77 and serves 50. The run MUST
    raise and the verdict MUST read `measured-short`. Without this arm the completeness control
    could be a constant that always says `measured-complete` and every green arm above would
    still pass."""
    rec = install(SHORT_PAGES)
    try:
        veh.lambda_handler({"leg": "insurance", "pull_date": "2026-08-28"}, None)
    except RuntimeError as e:
        msg = str(e)
        fired = "INCOMPLETE" in msg and "measured-short" in msg
        record("RED ARM: server attests 77, serves 50 -> run RAISES measured-short",
               fired, "%s | pages landed anyway=%d" % (msg.split(".")[0], len(rec.puts)))
        return
    record("RED ARM: server attests 77, serves 50 -> run RAISES measured-short", False,
           "*** CONTROL DID NOT FIRE -- a short pull returned success ***")


def main():
    print("=" * 78)
    print("ADVI_INSURE.TO-A3-AE / INSA3AE-AC1 -- act (a) dispatch exercise")
    print("subject: %s" % os.path.abspath(LAMBDA_DIR))
    print("DRY_RUN (vehicle default, unflipped) = %s" % veh.DRY_RUN)
    print("=" * 78)
    arm1_insurance()
    arm2_reporting()
    arm3_bare()
    arm4_unknown_leg()
    red_arm_short_pull()
    print("=" * 78)
    passed = sum(1 for _, p, _ in RESULTS if p)
    print("RESULT: %d of %d arms PASS" % (passed, len(RESULTS)))
    print("=" * 78)
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
