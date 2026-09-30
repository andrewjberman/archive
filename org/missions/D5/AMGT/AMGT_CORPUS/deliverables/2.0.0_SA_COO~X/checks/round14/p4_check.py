"""AMGT_CORPUS round 14 -- the issuer's checker for CRPS-p-4's evidence file (read-only).

  python p4_check.py structure <evidence.json> -> 'p4 outcomes N of 6 rows_valid V entry_named E deployed_read D' then VALID/INVALID
  python p4_check.py quotes    <evidence.json> -> 'p4 fence_quotes_verbatim N of 6'

The file: {"prd", "run_at", "entry": {"slug", "status_read"}, "deployed_function": {"name", "code_sha256", "last_modified"},
"outcomes": [6 rows]}. A row: id, fence_quote, instrument, output_excerpt, denominator, state (met / unmet / unmeasurable),
reason when unmeasurable, and exercising_act (the word "wait" refuses it) + owner when not met.
"""
import json
import os
import re
import sys

PRD = "org/missions/D5/AMGT/AMGT_CORPUS/prd/AMGT_CORPUS_PRD.md"
WANT = ["FWD-10", "FWD-11", "FWD-12", "FWD-15", "FWD-16", "FWD-18"]
STATES = {"met", "unmet", "unmeasurable"}
OWNERS = {"AMGT_CORPUS", "AMGT_RESAPP", "DSGN_AMGTV1"}


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip()


def row_ok(r):
    if not (r.get("id") in WANT and norm(r.get("fence_quote")) and norm(r.get("instrument"))
            and norm(r.get("output_excerpt")) and norm(r.get("denominator")) and r.get("state") in STATES):
        return False
    if r["state"] == "unmeasurable" and not norm(r.get("reason")):
        return False
    if r["state"] == "met":
        return True
    act = norm(r.get("exercising_act"))
    return bool(act) and not re.search(r"\bwait", act, re.I) and r.get("owner") in OWNERS


def main(mode, path):
    if not os.path.exists(path):
        print("MISSING %s" % path)
        return 1
    doc = json.load(open(path, encoding="utf-8"))
    rows = doc.get("outcomes") or []
    if mode == "quotes":
        prd = norm(open(PRD, encoding="utf-8").read())
        print("p4 fence_quotes_verbatim %d of 6" % sum(1 for r in rows if norm(r.get("fence_quote")) and norm(r.get("fence_quote")) in prd))
        return 0
    ids = [r.get("id") for r in rows]
    valid = sum(1 for r in rows if row_ok(r))
    entry = doc.get("entry") or {}
    fn = doc.get("deployed_function") or {}
    entry_named = bool(norm(entry.get("slug")) and norm(entry.get("status_read")))
    deployed_read = bool(norm(fn.get("name")) and norm(fn.get("code_sha256")))
    covered = len(set(ids) & set(WANT))
    print("p4 outcomes %d of 6 rows_valid %d entry_named %s deployed_read %s" % (covered, valid, entry_named, deployed_read))
    print("VALID" if covered == 6 and valid == 6 and len(ids) == 6 and entry_named and deployed_read else "INVALID")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
