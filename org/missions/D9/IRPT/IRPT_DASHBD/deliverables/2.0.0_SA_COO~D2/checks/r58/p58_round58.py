"""IRPT_DASHBD round 58 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADVI_COTBKF round-54 analysis @0ac41554df, section 3 row D2-W66-S1.

Cell: DB-b-114 the rule-24 record for the return_basis and method_version values the Cottonwood (positions-based, as-traded close, net of fees)
returns state: four postulates each answered, a word-boundary token census with its denominator, and ONE conclusion from a closed set naming
the two values the 107,316 measured rows are stamped with. The record decides whether a NEW value is needed; it lands no value.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB58-1-AC1  ~89/COTTONWOOD_VALUE_RULE24.json: postulates holds exactly mece, same_grain, intent_coherence, state_coherence, each with a
              non-empty finding and evidence [{file, line}]; token_census.files_scanned > 0 and tokens covers every current RETURN_BASIS
              member, every candidate and method_version, each with word-boundary hits and files as ints; conclusion is one of
              EXISTING_VALUES_SUFFICE / NEW_RETURN_BASIS_VALUE / NEW_METHOD_ROW / BOTH_NEW; stamp names return_basis and method_version;
              when the conclusion is EXISTING_VALUES_SUFFICE both stamp values are members the producer admits at HEAD.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
POSTULATES = {"mece", "same_grain", "intent_coherence", "state_coherence"}
CONCLUSIONS = {"EXISTING_VALUES_SUFFICE", "NEW_RETURN_BASIS_VALUE", "NEW_METHOD_ROW", "BOTH_NEW"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB58"))
        sys.exit(1)

    if cid != "DB58-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / (D + "89/COTTONWOOD_VALUE_RULE24.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    ps = r.get("postulates") or {}
    if set(ps) != POSTULATES:
        fail("postulates %r" % sorted(ps))
    for k in sorted(ps):
        ev = ps[k].get("evidence") or []
        if not str(ps[k].get("finding") or "").strip() or not ev:
            fail("postulate %s lacks a finding or evidence" % k)
        for e in ev:
            if not (root / str(e.get("file") or "")).is_file() or not isinstance(e.get("line"), int):
                fail("postulate %s evidence %r does not name a file and line" % (k, e))
    src = (root / PRODUCER).read_text(encoding="utf-8")
    m = re.search(r'^BASIS_TWR = "([^"]+)"', src, re.M)
    members = set(re.findall(r'^BASIS_[A-Z_]+ = "([^"]+)"', src, re.M))
    rows = set(int(x) for x in re.findall(r"^    (\d+): \{", src, re.M))
    if not m or not members or not rows:
        fail("could not read RETURN_BASIS members or METHOD_ROWS from the producer")
    tc = r.get("token_census") or {}
    toks = tc.get("tokens") or {}
    if not isinstance(tc.get("files_scanned"), int) or tc["files_scanned"] <= 0:
        fail("token_census.files_scanned %r" % tc.get("files_scanned"))
    need = set(members) | {"method_version"} | set(r.get("candidates") or [])
    for t in sorted(need):
        e = toks.get(t) or {}
        if not isinstance(e.get("hits"), int) or not isinstance(e.get("files"), int):
            fail("token_census lacks %r with int hits and files" % t)
    if r.get("conclusion") not in CONCLUSIONS:
        fail("conclusion %r" % r.get("conclusion"))
    st = r.get("stamp") or {}
    if "return_basis" not in st or "method_version" not in st:
        fail("stamp %r" % st)
    if r["conclusion"] == "EXISTING_VALUES_SUFFICE":
        if st["return_basis"] not in members or st["method_version"] not in rows:
            fail("stamp %r is not admitted by the producer at HEAD (members %r, rows %r)" % (st, sorted(members), sorted(rows)))
    print("OK: four postulates answered, census over %d files, conclusion %s, stamp %r" % (tc["files_scanned"], r["conclusion"], st))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
