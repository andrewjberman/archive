"""ADVI_COTBKF TO-CB-cv-1 AC2 (issuer's check): is the completion report one well-formed row per FWD-1..FWD-9?

Reads org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~189/COMPLETION_REPORT.json (repo-relative; run from the repo root).
Prints one line:
  REPORT-SHAPE rows=<n> ids_ok=<bool> grades_ok=<bool> artifacts_ok=<bool> grade_read_ok=<bool> acts_ok=<bool>
Rules: ids_ok = exactly FWD-1..FWD-9, each once; grades_ok = every grade is REALIZED or NOT_REALIZED; artifacts_ok = every row has an
artifact {kind in s3_key_version | commit | file_at_commit, ref, version_or_commit} with a non-empty ref; grade_read_ok = every row names the file
and locator the grade was read from; acts_ok = every NOT_REALIZED row has a non-empty act and act_owner. Counts only; reads the record only.
A missing file raises (the criterion FAILS where the record does not exist).
"""
import json
import sys

P = sys.argv[1] if len(sys.argv) > 1 else "org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~189/COMPLETION_REPORT.json"
d = json.load(open(P, encoding="utf-8"))
rows = d.get("rows") or []
want = ["FWD-%d" % i for i in range(1, 10)]
ids_ok = sorted(r.get("fwd", "") for r in rows) == sorted(want)
grades_ok = bool(rows) and all(r.get("grade") in ("REALIZED", "NOT_REALIZED") for r in rows)


def art_ok(r):
    a = r.get("artifact") or {}
    return a.get("kind") in ("s3_key_version", "commit", "file_at_commit") and bool(str(a.get("ref", "")).strip()) \
        and bool(str(a.get("version_or_commit", "")).strip())


def read_ok(r):
    g = r.get("grade_read") or {}
    return bool(str(g.get("file", "")).strip()) and bool(str(g.get("locator", "")).strip())


artifacts_ok = bool(rows) and all(art_ok(r) for r in rows)
grade_read_ok = bool(rows) and all(read_ok(r) for r in rows)
acts_ok = bool(rows) and all(r.get("grade") == "REALIZED" or (str(r.get("act", "")).strip() and str(r.get("act_owner", "")).strip()) for r in rows)
print("REPORT-SHAPE rows=%d ids_ok=%s grades_ok=%s artifacts_ok=%s grade_read_ok=%s acts_ok=%s"
      % (len(rows), ids_ok, grades_ok, artifacts_ok, grade_read_ok, acts_ok))
