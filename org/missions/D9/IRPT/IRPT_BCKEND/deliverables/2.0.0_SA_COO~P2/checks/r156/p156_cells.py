"""IRPT_BCKEND round 156 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one BUILD order with its release read, nothing released:
  IB156-1  IB-pr-460  the commentary draft store's persist answer carries `ticket_id` on a first OK persist when the accepted
                      record has one, and is absent otherwise (PRD v0.45, signed @83e8664d75; CTO msg 6033); and the release
                      read for that one function: what would move, every rider named, the replay.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB156-1-AC1  BUILD (FAILS at base): the cell's own test file passes and writes the answers file: a first persist for a record
               WITH a ticket id carries the member equal to the record's; WITHOUT one the answer's key set is exactly today's;
               a replay, a refusal and get_ref carry no ticket_id.
  IB156-1-AC2  SEAM (FAILS at base): the release read: the function built twice identically from a minimal candidate map beside
               its live package; EVERY moved member named with its owning commits and whether it is this change; the riders;
               replay arms (no ticket id: identical on live and built; with one: expected-diff; a negative control); the one
               consumer named with the read through it.
  IB156-1-AC3  CONTROL (PASSES at base and after): the EXISTING test file is byte-identical to the base's and still passes. It
               pins the exact key set of every answer for records with no ticket id, so it passing unchanged is the proof that
               such an answer is equal to today's.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

R = "infra/aws/lambda/investor-reporting/reports/"
MOD = R + "commentary_draft_store.py"
OLD_TEST = R + "tests/test_commentary_draft_store.py"
OLD_TEST_SHA256 = "b3c192b636ce0d45c8a5d5814a32b5e503ae47eab25181ee591f1fd1d9d3785a"
NEW_TEST = R + "tests/test_commentary_draft_store_ticket_id.py"
ANSWERS = R + "tests/commentary_draft_store_answers.json"
D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~316/"
OUT, PACKET = D + "IB156-1_release_read.json", D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-460.md"
B64 = re.compile(r"^[A-Za-z0-9+/]{43}=$")
REF = {"artifact_id", "sha256", "version_id"}
FN = "irpt-commentary-draft-store-lambda"


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
        print("%s FAIL" % (cid or "IB156"))
        sys.exit(1)

    if cid == "IB156-1-AC1":
        if not (root / NEW_TEST).is_file():
            fail("no %s" % NEW_TEST)
        ok, tail = pytest(root, [NEW_TEST])
        if not ok:
            fail("the cell's tests: %s" % tail[:160])
        f = root / ANSWERS
        if not f.is_file():
            fail("no %s" % ANSWERS)
        a = json.loads(f.read_text(encoding="utf-8"))
        need = {"first_persist_with_ticket_id", "first_persist_without_ticket_id", "replay", "refusal", "get_ref", "record_ticket_id"}
        if set(a) != need:
            fail("the answers file must hold exactly %s" % sorted(need))
        w, wo = a["first_persist_with_ticket_id"], a["first_persist_without_ticket_id"]
        if set(wo) != {"status", "commentary_ref"} or set(wo["commentary_ref"]) != REF or wo.get("status") != "OK":
            fail("the answer for a record with no ticket id is not exactly {status, commentary_ref{artifact_id, sha256, version_id}}")
        if set(w) != {"status", "commentary_ref", "ticket_id"} or w["ticket_id"] != a["record_ticket_id"] or not isinstance(w["ticket_id"], str) or not w["ticket_id"]:
            fail("the answer for a record with a ticket id must carry ticket_id equal to the record's, and nothing else new")
        for k in ("replay", "refusal", "get_ref"):
            if "ticket_id" in a[k]:
                fail("%s carries ticket_id" % k)
        if set(a["replay"]) != {"status", "reason"} or set(a["refusal"]) != {"status", "reason"}:
            fail("a replay and a refusal must be exactly {status, reason}")
        print("OK: %s; with a ticket id the answer carries it; without, the key set is today's; replay, refusal and get_ref carry none" % tail[:40])
    elif cid == "IB156-1-AC2":
        f = root / OUT
        if not f.is_file():
            fail("no %s" % OUT)
        a = json.loads(f.read_text(encoding="utf-8"))
        if a.get("function") != FN or not re.match(r"^[0-9a-f]{10,40}$", str(a.get("base_commit") or "")):
            fail("function must be %s and base_commit stated" % FN)
        if not B64.match(str(a.get("live_code_sha256") or "")) or not a.get("rollback_version_id"):
            fail("live_code_sha256 and rollback_version_id")
        b = a.get("build") or {}
        if b.get("outcome") != "BUILT" or not B64.match(str(b.get("built_sha256") or "")) or b.get("built_twice_identical") is not True:
            fail("build must be BUILT with built_sha256 and built_twice_identical true")
        mv = a.get("moved_members")
        if not isinstance(mv, list) or not mv or any(not m.get("member") or not isinstance(m.get("owning_commits"), list) or m.get("class") not in ("served", "inert")
                                                     or not m.get("one_line") or not isinstance(m.get("is_this_change"), bool) or not m.get("serves") for m in mv):
            fail("moved_members must list each member with owning_commits, class, one_line, is_this_change and serves")
        if not any(m["member"].endswith("commentary_draft_store.py") and m["is_this_change"] for m in mv):
            fail("commentary_draft_store.py is not among the moved members as this change")
        if a.get("riders") != [m["member"] for m in mv if not m["is_this_change"]]:
            fail("riders must be exactly the moved members that are not this change")
        arms = (a.get("replay") or {}).get("arms")
        if not isinstance(arms, list) or any(x.get("verdict") not in ("identical", "expected-diff") or not x.get("name") for x in arms):
            fail("replay.arms must each read identical or expected-diff")
        if not any(x.get("record_has_ticket_id") is False and x.get("verdict") == "identical" for x in arms) \
                or not any(x.get("record_has_ticket_id") is True and x.get("verdict") == "expected-diff" for x in arms) \
                or not any(x.get("negative_control") for x in arms):
            fail("the replay needs: no ticket id identical, with one expected-diff, and a negative control")
        c = a.get("consumer") or {}
        if not c.get("name") or ":" not in str(c.get("code_line") or "") or not c.get("read_the_pair_makes_through_it") or not c.get("on_the_new_member"):
            fail("consumer needs name, code_line, on_the_new_member and read_the_pair_makes_through_it")
        for k in ("uploads_made", "applies_made", "real_source_map_edits", "vendor_calls_made", "functions_invoked"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not (root / PACKET).is_file() or not isinstance(a.get("not_exercised"), list):
            fail("the packet and not_exercised are required")
        print("OK: %s built twice identically; %d moved member(s), %d rider(s); %d replay arm(s); consumer %s" % (
            FN, len(mv), len(a["riders"]), len(arms), c["name"]))
    elif cid == "IB156-1-AC3":
        b = (root / OLD_TEST).read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(b).hexdigest() != OLD_TEST_SHA256 and hashlib.sha256((root / OLD_TEST).read_bytes()).hexdigest() != OLD_TEST_SHA256:
            fail("the existing test file was changed: it pins today's answers and must stay byte-identical")
        ok, tail = pytest(root, [OLD_TEST])
        if not ok:
            fail("the existing tests: %s" % tail[:160])
        print("OK: the existing test file is unchanged and passes: %s" % tail[:40])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
