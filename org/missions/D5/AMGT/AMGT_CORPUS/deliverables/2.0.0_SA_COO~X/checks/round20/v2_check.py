"""AMGT_CORPUS round 20 -- the issuer's checker for CRPS-v-2's evidence file (read-only).

  python v2_check.py structure <evidence.json> -> 'v2 outcomes N of 6 rows_valid V signed_out_void S disarm_refused D population P'
                                                  then VALID/INVALID
  python v2_check.py quotes    <evidence.json> -> 'v2 fence_quotes_verbatim N of 6'

The file: {"prd", "run_at", "population": {"source", "denominator"}, "deployed_function": {"name", "code_sha256"},
"portal": {"dev_commit", "base"}, "signed_out_control": {"command", "exit_code", "void_line"}, "walk": {"stamp", "command",
"disarm_line"}, "outcomes": [6 rows]}. A row: id, fence_quote (VERBATIM from the PRD), served {instrument, numerator,
denominator, excerpt, state met|unmet}, page {security, tab, shot, reads (words: what the page shows), state
met|unmet|unmeasurable, reason when unmeasurable}, and owner + exercising_act (the word "wait" refuses it) when either half is
not met.
"""
import json
import os
import re
import sys

PRD = "org/missions/D5/AMGT/AMGT_CORPUS/prd/AMGT_CORPUS_PRD.md"
WANT = ["FWD-10", "FWD-11", "FWD-12", "FWD-15", "FWD-16", "FWD-18"]
OWNERS = {"AMGT_CORPUS", "AMGT_RESAPP", "DSGN_AMGTV1"}


def norm(text):
    return re.sub(r"\s+", " ", str(text or "")).strip()


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def row_ok(r):
    s, p = r.get("served") or {}, r.get("page") or {}
    if r.get("id") not in WANT or not norm(r.get("fence_quote")):
        return False
    if not (norm(s.get("instrument")) and is_int(s.get("numerator")) and is_int(s.get("denominator")) and s["denominator"] > 0
            and norm(s.get("excerpt")) and s.get("state") in ("met", "unmet")):
        return False
    if not (norm(p.get("security")) and norm(p.get("tab")) and norm(p.get("reads")) and p.get("state") in ("met", "unmet", "unmeasurable")):
        return False
    if p["state"] == "unmeasurable" and not norm(p.get("reason")):
        return False
    if p["state"] != "unmeasurable" and "ui-walk" not in norm(p.get("shot")):
        return False
    if s["state"] == "met" and p["state"] == "met":
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
        print("v2 fence_quotes_verbatim %d of 6" % sum(1 for r in rows if norm(r.get("fence_quote")) and norm(r.get("fence_quote")) in prd))
        return 0
    ids = [r.get("id") for r in rows]
    valid = sum(1 for r in rows if row_ok(r))
    so = doc.get("signed_out_control") or {}
    void = so.get("exit_code") == 3 and "WALK VOID" in norm(so.get("void_line"))
    disarm = "REFUSED" in norm((doc.get("walk") or {}).get("disarm_line"))
    pop = (doc.get("population") or {}).get("denominator")
    covered = len(set(ids) & set(WANT))
    print("v2 outcomes %d of 6 rows_valid %d signed_out_void %s disarm_refused %s population %s" % (covered, valid, void, disarm, pop))
    ok = covered == 6 and valid == 6 and len(ids) == 6 and void and disarm and is_int(pop) and pop > 0
    ok = ok and bool(norm((doc.get("portal") or {}).get("dev_commit"))) and bool(norm((doc.get("deployed_function") or {}).get("code_sha256")))
    print("VALID" if ok else "INVALID")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
