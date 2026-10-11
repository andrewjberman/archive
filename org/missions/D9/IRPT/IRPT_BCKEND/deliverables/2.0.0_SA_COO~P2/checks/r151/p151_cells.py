"""IRPT_BCKEND round 151 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one BUILD order, nothing released:
  IB151-1  IB-pr-455  the submission's closed set admits the optional boolean `commentary_requested` and refuses any other type;
                      acceptance copies it into the accepted record only when sent (IRPT_YCDGEN PRD v0.13, signed; CTO msg 5863).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB151-1-AC1  BUILD (FAILS at base): validate_public_request admits the member as true or false, refuses every other type with
               one refusal code, and still refuses an unknown member; the cell's own test file passes.
  IB151-1-AC2  SEAM (FAILS at base): the public contract declares the member as an optional boolean in a still-closed object,
               and the record acceptance writes carries the member exactly when the submission sent it (read through the
               module's own fake-free path: the record built for a planted submission, by the cell's test helper).
  IB151-1-AC3  CONTROL (PASSES at base and after): a submission WITHOUT the member validates to exactly what it validated to
               before, and the existing acceptance and submission tests still pass.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

G = "infra/aws/lambda/investor-reporting/ycharts/generate/"
SUB, ACC = G + "submission.py", G + "acceptance.py"
TEST = G + "tests/test_commentary_requested_member.py"
SCHEMA = "docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json"
EXISTING = [G + "tests/test_acceptance_actor.py", G + "tests/test_prospect_submission.py", G + "tests/test_ready_signal_commentary_gate.py"]
BASE = {"request_id": "idem-0001", "client_id": "CL-1", "account_ids": ["A-1"], "snapshot_id": "SNAP-1", "variant": "auto",
        "comparison_keys": [], "report_title": None, "prepared_for": "A Reader"}


def load(root):
    sys.path.insert(0, str(root / G))
    spec = importlib.util.spec_from_file_location("submission_under_check", str(root / SUB))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pytest(root, files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + [str(root / f) for f in files],
                       cwd=str(root), capture_output=True, text=True, timeout=110)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    return r.returncode == 0 and " passed" in tail and "failed" not in tail, tail


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB151"))
        sys.exit(1)

    m = load(root)
    if cid == "IB151-1-AC1":
        for v in (True, False):
            try:
                out = m.validate_public_request(dict(BASE, commentary_requested=v))
            except Exception as exc:  # noqa: BLE001
                fail("commentary_requested=%r is refused: %s" % (v, getattr(exc, "code", exc)))
            if out.get("commentary_requested") is not v:
                fail("commentary_requested=%r is not returned as sent" % (v,))
        codes = set()
        for v in ("true", "false", 1, 0, None, [], {}, 1.0):
            try:
                m.validate_public_request(dict(BASE, commentary_requested=v))
            except m.SubmissionRefused as exc:
                codes.add(exc.code)
                continue
            fail("commentary_requested=%r (type %s) was admitted" % (v, type(v).__name__))
        if len(codes) != 1:
            fail("the wrong types are refused with %d different codes: %s" % (len(codes), sorted(codes)))
        try:
            m.validate_public_request(dict(BASE, commentary_requested=True, commentary="yes"))
            fail("an unknown member beside it was admitted")
        except m.SubmissionRefused as exc:
            if exc.code != "UNKNOWN_OR_SERVER_OWNED_FIELD":
                fail("an unknown member is refused with %s" % exc.code)
        if not (root / TEST).is_file():
            fail("no %s" % TEST)
        ok, tail = pytest(root, [TEST])
        if not ok:
            fail("the cell's tests: %s" % tail[:160])
        print("OK: true and false admitted and returned; 8 wrong types refused with %s; unknown member still refused; %s" % (sorted(codes)[0], tail[:40]))
    elif cid == "IB151-1-AC2":
        s = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
        p = (s.get("properties") or {}).get("commentary_requested")
        if not isinstance(p, dict) or p.get("type") != "boolean":
            fail("%s does not declare commentary_requested as a boolean" % SCHEMA)
        if s.get("additionalProperties") is not False or "commentary_requested" in (s.get("required") or []):
            fail("the schema must stay closed and the member must stay optional")
        f = root / G / "tests" / "commentary_requested_records.json"
        if not f.is_file():
            fail("no tests/commentary_requested_records.json (the three records the cell's test writes through acceptance)")
        r = json.loads(f.read_text(encoding="utf-8"))
        if set(r) != {"sent_true", "sent_false", "not_sent"}:
            fail("the records file must hold exactly sent_true, sent_false, not_sent")
        if r["sent_true"].get("commentary_requested") is not True or r["sent_false"].get("commentary_requested") is not False \
                or "commentary_requested" in r["not_sent"]:
            fail("the accepted record does not carry the member exactly when it was sent")
        if set(r["sent_true"]) - {"commentary_requested"} != set(r["not_sent"]):
            fail("the record with the member differs from the record without it by more than the member")
        print("OK: the contract declares an optional boolean in a closed object; the record carries it when sent (true, false) and not otherwise")
    elif cid == "IB151-1-AC3":
        out = m.validate_public_request(dict(BASE))
        if "commentary_requested" in out or out != BASE:
            fail("a submission without the member no longer validates to itself")
        ok, tail = pytest(root, [f for f in EXISTING if (root / f).is_file()])
        if not ok:
            fail("the existing tests: %s" % tail[:160])
        print("OK: a submission without the member validates to itself; existing tests: %s" % tail[:60])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
