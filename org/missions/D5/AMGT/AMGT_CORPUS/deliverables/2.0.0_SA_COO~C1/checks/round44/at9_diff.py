"""AMGT_CORPUS round 44, CRPS-at-9 (row D1-S2; CTO ruling msg 3213) -- the /10 re-write's diff of EVERY dossier field, all names,
against /7 (served before 19:51Z) and /9 (served since). Issuer's file. READ-ONLY: S3 reads and in-memory builds; nothing written.

  PYTHONPATH=. python at9_diff.py --pre     the /10 candidate built IN MEMORY by the current code (dossier.build), real fitz asserted
  PYTHONPATH=. python at9_diff.py --post    the WRITTEN /10 objects (read_dossier with METHOD_VERSION at /10)

Per name and field of doc["fields"] (every field the dossier carries), the candidate is classed:
  SAME        equal to /7 and to /9
  GAIN9       equal to /9, not to /7   (expected: exactly the 12 /9 gains of evidence/r42_ar2_changes_whole_20261009.txt)
  RESTORE7    equal to /7, not to /9   (expected: the PDF reads /9 lost -- cases on 8035 JP, BZLFY, HEI, SNPS, TSM, V)
  BOTH-DIFFER equal to neither, where /7 == /9 (a field that moved for no reason: must be 0)
  ALL-DIFFER  equal to neither, where /7 != /9 (listed and read)
Prints `at9 fitz <real|STUB> version <v>`, then the RESTORE7 / BOTH-DIFFER / ALL-DIFFER lines, then
`at9 names <n> fields <f> same <s> gain9 <g> restore7 <r> both_differ <b> all_differ <a> cases_restored <c>/6` and `at9 build <0|1>/1`
(build = fitz real, both_differ 0, all_differ 0, the GAIN9 set equal to the 12, cases restored on all 6).
"""
import json
import os
import sys

import fitz  # noqa: F401  -- deliberately REAL: a stub here is the very defect this act repairs

from lib.research.corpus import dossier
from lib.research.harvest import store

HERE = os.path.dirname(os.path.abspath(__file__))
PRE12 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "evidence", "r42_ar2_changes_whole_20261009.txt")
CASE_NAMES = ("8035_JP_Equity", "BZLFY_US_Equity", "HEI_US_Equity", "SNPS_US_Equity", "TSM_US_Equity", "V_US_Equity")


def _read(key, client, method):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = method
    try:
        return dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = current


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _gain12():
    t = open(PRE12, encoding="utf-8").read()
    return {tuple(blk.split("\n", 1)[0].split()[1:3]) for blk in t.split("=== ")[1:]}


def main():
    mode = "--post" if "--post" in sys.argv else "--pre"
    real = hasattr(fitz, "open") and hasattr(fitz, "Document")
    ver = getattr(fitz, "VersionBind", None) or getattr(fitz, "__version__", None) or getattr(fitz, "version", None)
    print("at9 fitz %s version %s mode %s method %s" % ("real" if real else "STUB", ver, mode, dossier.METHOD_VERSION))
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    counts = {"SAME": 0, "GAIN9": 0, "RESTORE7": 0, "BOTH-DIFFER": 0, "ALL-DIFFER": 0}
    gain9, restored_cases = set(), set()
    n = 0
    for key in keys:
        try:
            d7 = _read(key, client, "amgt-corpus-dossier/7")
            d9 = _read(key, client, "amgt-corpus-dossier/9")
            cand = dossier.build(key, client=client) if mode == "--pre" else _read(key, client, dossier.METHOD_VERSION)
        except LookupError as exc:
            print("UNREAD %s %s" % (key, str(exc)[:80]))
            continue
        n += 1
        f7, f9, fc = d7.get("fields") or {}, d9.get("fields") or {}, cand.get("fields") or {}
        for name in sorted(set(f7) | set(f9) | set(fc)):
            a, b, c = _canon(f7.get(name)), _canon(f9.get(name)), _canon(fc.get(name))
            if c == a and c == b:
                cls = "SAME"
            elif c == b:
                cls = "GAIN9"
                gain9.add((key, name))
            elif c == a:
                cls = "RESTORE7"
                if name == "cases" and key in CASE_NAMES:
                    restored_cases.add(key)
            elif a == b:
                cls = "BOTH-DIFFER"
            else:
                cls = "ALL-DIFFER"
            counts[cls] += 1
            if cls in ("RESTORE7", "BOTH-DIFFER", "ALL-DIFFER"):
                print("%s %s %s" % (cls, key, name))
    expected = _gain12()
    for k in sorted(expected - gain9):
        print("GAIN-MISSING %s %s" % k)
    for k in sorted(gain9 - expected):
        print("GAIN-EXTRA %s %s" % k)
    print("at9 names %d fields %d same %d gain9 %d restore7 %d both_differ %d all_differ %d cases_restored %d/6" % (
        n, sum(counts.values()), counts["SAME"], counts["GAIN9"], counts["RESTORE7"], counts["BOTH-DIFFER"],
        counts["ALL-DIFFER"], len(restored_cases)))
    build = int(real and counts["BOTH-DIFFER"] == 0 and counts["ALL-DIFFER"] == 0 and gain9 == expected
                and len(restored_cases) == 6)
    print("at9 build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main())
