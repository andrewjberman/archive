"""DSGN_IRPTV1 round 24 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 5447 on row DSGN_IRPTV1-D2-S18.

Cell: IV-e-110 when the Holdings securities table lists less than the total card, the table says in a sentence how much sits in sleeves
it does not itemise and names the producer's two reasons (cash only, or detail withheld).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV110-AC1  ~60/UNLISTED_SLEEVES.json: sentence {text, where {file, line}}; reasons_named has exactly two entries; amount_rule
             (a sentence: the card less the listed rows, from the served nodes); cases holds at least one case with sentence_shown
             true (the listed rows fall short of the card) and one with sentence_shown false (they sum to it); test {id, passes true,
             mutant {what, failed true}}; screenshots: 1 or more existing files in the worker's folder, each in screenshots_read;
             lint_errors 0; typecheck_errors 0; suite_after.new_failing_ids == []; product_files_changed non-empty; portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV24"))
        sys.exit(1)

    if cid != "IV110-AC1":
        fail("unknown criterion %r" % cid)
    folder = root / "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~60"
    p = folder / "UNLISTED_SLEEVES.json"
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    s = r.get("sentence") or {}
    w = s.get("where") or {}
    if not str(s.get("text") or "").strip() or not str(w.get("file") or "").strip() or not w.get("line"):
        fail("sentence lacks its text or where")
    rn = r.get("reasons_named")
    if not isinstance(rn, list) or len(rn) != 2 or any(not str(x).strip() for x in rn):
        fail("reasons_named %r, want exactly two" % (rn,))
    if not str(r.get("amount_rule") or "").strip():
        fail("no amount_rule")
    shown = [c.get("sentence_shown") for c in (r.get("cases") or [])]
    if True not in shown or False not in shown:
        fail("cases want one with the sentence shown and one without; got %r" % shown)
    t = r.get("test") or {}
    mu = t.get("mutant") or {}
    if not str(t.get("id") or "").strip() or t.get("passes") is not True or not str(mu.get("what") or "").strip() or mu.get("failed") is not True:
        fail("the test lacks an id, a pass, or a failing mutant")
    shots = r.get("screenshots") or []
    if not shots or any(not (folder / str(x)).is_file() for x in shots) or sorted(r.get("screenshots_read") or []) != sorted(shots):
        fail("screenshots: one or more existing files, each in screenshots_read")
    if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
        fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
    if (r.get("suite_after") or {}).get("new_failing_ids") != []:
        fail("suite_after.new_failing_ids %r" % (r.get("suite_after") or {}).get("new_failing_ids"))
    if not r.get("product_files_changed") or not HEX.match(str(r.get("portal_commit") or "")):
        fail("product_files_changed empty or portal_commit missing")
    print("OK: the table states what it does not itemise (%s:%s), naming two reasons; shown when short, absent when whole; %d screenshot(s) read"
          % (w["file"], w["line"], len(shots)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
