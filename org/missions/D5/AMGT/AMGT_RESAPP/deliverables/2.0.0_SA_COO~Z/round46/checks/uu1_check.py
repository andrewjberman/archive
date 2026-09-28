"""AMGT_RESAPP round 46 -- the issuer's checker for AMGT-uu-1's evidence files (read-only).

  python uu1_check.py structure <dir>  -> 'outcomes N of 31 rows_valid V duplicates D' + 'basis_rows R complete C', then VALID/INVALID
  python uu1_check.py quotes    <dir>  -> 'fence_quotes_verbatim N of 31'
<dir> holds FWD_EVIDENCE_ROUND46.json and BASE_CASE_BASIS.json.
"""
import json
import os
import re
import sys

PRD = "org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md"
STATES = {"met", "unmet", "unmeasurable"}
N = 31
BASIS_FIELDS = ("security_key", "consensus_eps", "consensus_eps_basis", "trailing_median_pe", "trailing_median_pe_basis",
                "window", "base_value", "px_last", "ratio_to_px_last", "currency")


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip()


def load(path):
    if not os.path.exists(path):
        print("MISSING %s" % path)
        print("INVALID")
        sys.exit(1)
    return json.load(open(path, encoding="utf-8"))


def structure(d):
    doc = load(os.path.join(d, "FWD_EVIDENCE_ROUND46.json"))
    rows = doc.get("outcomes") or []
    ids = [r.get("id") for r in rows]
    want = ["FWD-%d" % i for i in range(1, N + 1)]
    valid = sum(1 for r in rows if r.get("id") in want and norm(r.get("fence_quote")) and norm(r.get("instrument"))
                and norm(r.get("output_excerpt")) and r.get("state") in STATES
                and (r.get("state") != "unmeasurable" or norm(r.get("reason"))))
    covered = len(set(ids) & set(want))
    print("outcomes %d of %d rows_valid %d duplicates %d" % (covered, N, valid, len(ids) - len(set(ids))))
    basis = load(os.path.join(d, "BASE_CASE_BASIS.json"))
    brow = basis.get("rows") or []
    complete = sum(1 for r in brow if all(k in r and r[k] not in (None, "") for k in BASIS_FIELDS))
    print("basis_rows %d complete %d (served base SERVED on the live plane per the file: %s)" % (
        len(brow), complete, basis.get("served_base_served_count")))
    ok = (covered == N and valid == N and len(ids) == N and brow and complete == len(brow)
          and basis.get("served_base_served_count") == len(brow))
    print("VALID" if ok else "INVALID")
    return 0 if ok else 1


def quotes(d):
    doc = load(os.path.join(d, "FWD_EVIDENCE_ROUND46.json"))
    prd = norm(open(PRD, encoding="utf-8").read())
    rows = doc.get("outcomes") or []
    hit = sum(1 for r in rows if norm(r.get("fence_quote")) and norm(r.get("fence_quote")) in prd)
    print("fence_quotes_verbatim %d of %d" % (hit, N))
    return 0 if hit == N and len(rows) == N else 1


if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]
    sys.exit(structure(path) if mode == "structure" else quotes(path))
