"""IRPT_DASHBD round 85 (issuer 2.0.0_SA_COO~D2) -- the issuer's own cell: round 84's counts get a tracked producer.

Cell DB-b-163: the scripts that produced FLOW_DAYS_FIRST_INVESTED.json are tracked in the worker's folder, hold no client literal,
compile, and a re-run of the tracked copies reproduces the record's counts; RULE.md is unchanged.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB85-1-AC1  ~131/PRODUCERS.json: scripts (1 or more) each {file (exists under the worker's producers/ folder), sha256 (equals the
              file's bytes)}; every script compiles and holds no run of 8 or more digits; rerun {from_tracked_copies true,
              counts_equal_record true, classes (equal to the record's classes)}; rule_sha256 equals RULE.md's bytes AND the
              record's rule.sha256; client_literals 0.
"""
import hashlib
import json
import py_compile
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(rb"\d{8,}")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB85"))
        sys.exit(1)

    if cid != "DB85-1-AC1":
        fail("unknown criterion %r" % cid)
    folder = root / (M + "0.9.0_WK_IRPT_DASHBD~131")
    p = folder / "PRODUCERS.json"
    if not p.is_file():
        fail("no record 0.9.0_WK_IRPT_DASHBD~131/PRODUCERS.json")
    r = json.loads(p.read_bytes().decode("utf-8"))
    rec = json.loads((folder / "FLOW_DAYS_FIRST_INVESTED.json").read_bytes().decode("utf-8"))
    sc = r.get("scripts") or []
    if not sc:
        fail("no script listed")
    for s in sc:
        f = folder / "producers" / str(s.get("file") or "")
        if not str(s.get("file") or "").endswith(".py") or not f.is_file():
            fail("script %r is not a file under producers/" % s.get("file"))
        b = f.read_bytes()
        if hashlib.sha256(b).hexdigest() != s.get("sha256"):
            fail("script %r: sha256 does not equal its bytes" % s.get("file"))
        if RUN.search(b):
            fail("script %r holds a run of 8 or more digits" % s.get("file"))
        try:
            py_compile.compile(str(f), doraise=True, cfile=str(Path(sys.argv[0]).with_suffix(".tmp.pyc")))
        except py_compile.PyCompileError as e:
            fail("script %r does not compile: %s" % (s.get("file"), str(e)[:120]))
        finally:
            tmp = Path(sys.argv[0]).with_suffix(".tmp.pyc")
            if tmp.exists():
                tmp.unlink()
    rr = r.get("rerun") or {}
    if rr.get("from_tracked_copies") is not True or rr.get("counts_equal_record") is not True or rr.get("classes") != rec.get("classes"):
        fail("rerun must be from the tracked copies and reproduce the record's classes: %r against %r" % (rr.get("classes"), rec.get("classes")))
    rule = hashlib.sha256((folder / "RULE.md").read_bytes()).hexdigest()
    if r.get("rule_sha256") != rule or (rec.get("rule") or {}).get("sha256") != rule:
        fail("RULE.md's bytes are not the ones the record and this record name")
    if r.get("client_literals") != 0:
        fail("client_literals %r" % r.get("client_literals"))
    print("OK: %d tracked script(s), each at its recorded bytes and compiling; a re-run of the tracked copies reproduces the classes %s; the rule is unchanged"
          % (len(sc), rec.get("classes")))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
