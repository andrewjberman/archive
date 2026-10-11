"""LGIC_ENFORCE round 22 (follow-up cell, row D1-S1) -- the issuer's fixed check (2.0.0_SA_COO~B1).

Run from the root of the worktree under test:  python <this file> ruled
Prints one PASS-*/FAIL-* verdict line last; exits 0 only on PASS.

`ruled` runs `python lib/opal_naming.py census --names <file>` over a names file holding the three names that carry
name_rulings.json rows (calculated-group IAM_GROUP, astn/kimi/api-key SECRET, restricted-prefix-get-put-list IAM_POLICY) plus
one unruled name that RAISEs (zzqx-unruled-r22-lambda LAMBDA):
  arm A, with a --not-judged card for the unruled name only: rc 0; each ruled name prints a line starting `CENSUS RULED`
         that names it and cites `name_rulings.json#<row index>`, the row that holds it; the unruled name prints
         `CENSUS CARDED`; and a totals line reports ruled=3.
  arm B, with NO card: rc 3, STOPPED on the unruled name (the loud stop is unchanged; a ruled name never stops the run).
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
RULED = [("IAM_GROUP", "calculated-group"), ("SECRET", "astn/kimi/api-key"), ("IAM_POLICY", "restricted-prefix-get-put-list")]
UNRULED = ("LAMBDA", "zzqx-unruled-r22-lambda")


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def census(names_path, nj_path=None):
    args = [sys.executable, "lib/opal_naming.py", "census", "--names", names_path]
    if nj_path:
        args += ["--not-judged", nj_path]
    p = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=600)
    return p.returncode, ((p.stdout or b"") + (p.stderr or b"")).decode("utf-8", "replace").replace("\r\n", "\n")


def row_index():
    rows = json.load(open(os.path.join(ROOT, "infra/logic/registry/name_rulings.json"), encoding="utf-8"))["name_rulings"]
    return {(r["type"], r["name"]): i for i, r in enumerate(rows)}


def arm_ruled():
    idx = row_index()
    for t, n in RULED:
        need((t, n) in idx, "name_rulings.json carries no row for %s %s (the check's premise)" % (t, n))
    need(UNRULED not in idx, "the unruled control has a ruling row")
    tmp = tempfile.mkdtemp(prefix="r22-")
    names = os.path.join(tmp, "names.tsv")
    with open(names, "w", encoding="utf-8", newline="\n") as fh:
        for t, n in RULED + [UNRULED]:
            fh.write("%s\t%s\n" % (t, n))
    nj = os.path.join(tmp, "nj.json")
    with open(nj, "w", encoding="utf-8", newline="\n") as fh:
        json.dump([{"name": UNRULED[1], "plane": "names", "card": "r22 control: an unruled RAISE stays carded"}], fh)
    rc, out = census(names, nj)
    for ln in out.splitlines():
        if re.match(r"^CENSUS (RULED|CARDED|RAISE)|ruled", ln):
            print("A: " + ln[:200])
    need(rc == 0, "arm A: rc=%d (want 0)" % rc)
    for t, n in RULED:
        need(re.search(r"^CENSUS RULED .*%s.*name_rulings\.json#%d\b" % (re.escape(n), idx[(t, n)]), out, re.M),
             "arm A: no `CENSUS RULED ... name_rulings.json#%d` line for %s" % (idx[(t, n)], n))
    need(re.search(r"^CENSUS CARDED .*%s" % re.escape(UNRULED[1]), out, re.M), "arm A: the unruled name is not CARDED")
    need(re.search(r"\bruled=3\b", out), "arm A: no totals line reporting ruled=3")
    rc, out = census(names)
    print("B: rc=%d last=%r" % (rc, (out.strip().splitlines() or [""])[-1][:160]))
    need(rc == 3 and re.search(r"^CENSUS: STOPPED .*%s" % re.escape(UNRULED[1]), out, re.M),
         "arm B: without a card the unruled name did not STOP the run (rc=%d)" % rc)
    return "PASS-R22-RULED"


def main():
    if (sys.argv[1:] or [""])[0] != "ruled":
        print("usage: check_en_r22.py ruled")
        return 2
    try:
        verdict = arm_ruled()
    except Fail as exc:
        print("FAIL-R22-RULED: %s" % exc)
        return 1
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
