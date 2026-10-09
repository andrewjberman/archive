"""AMGT_RESAPP round-85 -- NU's stored draft repaired in place (CTO~DELL1 msg 2442; NEVER_WIDEN_ROUND85_JJ2_CTO_HALF.md ADDENDUM 2).

  python r85_repair.py --crit AC1 --draft <local repaired NU drafting JSON>

--exclude-section NAME (round 86): drop a section from every count, e.g. company_description, which R5 empties.

Grades a LOCAL repaired copy of drafting/v1/NU_US_Equity.json BEFORE it is written, against the CURRENT stored draft and NU's stored
filing excerpt (the latest silver `filing_source` row's excerpt text), both read only:
    K1 the same number of sentences as the stored draft (38 at the cut) -- any drop is a STOP;
    K2 0 glued sentence boundaries and 0 sentences stating one fact twice in a row (r85_sentences' own S1/S2 rules);
    K3 every kept sentence's text is a verbatim substring of NU's stored filing excerpt (whitespace collapsed, both sides);
    K4 citations intact: each sentence keeps the stored sentence's `evidence` list, in order.
Verdict: R85 REPAIR AC1: YES|NO (exit 0|1). On the current stored draft itself: NO (K2: 25 glued, 14 restated; K3 fails on the
paraphrases).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

KEY = "NU_US_Equity"
BUCKET = "opal-data-harvest"
HERE = os.path.dirname(os.path.abspath(__file__))


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _norm(t):
    return re.sub(r"\s+", " ", t or "").strip()


EXCLUDE = set()


def _sentences(doc):
    return [s for sec in doc.get("sections") or [] if (sec.get("section") or "") not in EXCLUDE for s in sec.get("sentences") or []]


def _stored_draft():
    import boto3

    obj = boto3.client("s3", region_name="us-east-1").get_object(Bucket=BUCKET, Key="drafting/v1/%s.json" % KEY)
    return json.loads(obj["Body"].read())


def _excerpt():
    from lib.research.harvest import store as hs

    rows = hs.silver_latest("sec", "filing_source", ("security_key", "accession"))
    rows = list(rows.values()) if isinstance(rows, dict) else list(rows)
    mine = [r for r in rows if r.get("security_key") == KEY]
    row = max(mine, key=lambda r: str(r.get("fetched_at")))
    obj = json.loads(row["object_json"])
    return obj.get("accession"), (obj.get("excerpt") or {}).get("text") or ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--draft", required=True)
    ap.add_argument("--exclude-section", action="append", default=[])
    a = ap.parse_args()
    EXCLUDE.update(a.exclude_section)
    if EXCLUDE:
        print("   sections excluded from every count: %s" % sorted(EXCLUDE))
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    for p in (root, HERE):
        if p and p not in sys.path:
            sys.path.insert(0, p)
    import r85_sentences as rs

    new = _sentences(json.load(open(a.draft, encoding="utf-8")))
    old = _sentences(_stored_draft())
    accession, excerpt = _excerpt()
    ex = _norm(excerpt)
    print("   stored draft sentences %d; repaired %d; excerpt accession %s, %d chars" % (len(old), len(new), accession, len(excerpt)))
    k1 = say(len(new) == len(old), "K1 sentences kept: %d of %d" % (len(new), len(old)))
    texts = [s.get("text") or "" for s in new]
    restated = sum(1 for t in texts if rs.restated(t))
    glued = sum(1 for t in texts if rs.GLUE_RE.search(t))
    k2 = say(restated == 0 and glued == 0, "K2 restated %d of %d, glued %d of %d" % (restated, len(texts), glued, len(texts)))
    not_verbatim = [i for i, t in enumerate(texts) if not _norm(t) or _norm(t) not in ex]
    for i in not_verbatim[:5]:
        print("   NOT VERBATIM [%d]: %s" % (i, texts[i][:140].encode("ascii", "replace").decode()))
    k3 = say(bool(texts) and not not_verbatim, "K3 sentences that are a verbatim substring of the stored filing: %d of %d" % (
        len(texts) - len(not_verbatim), len(texts)))
    moved = [i for i, (n, o) in enumerate(zip(new, old)) if (n.get("evidence") or []) != (o.get("evidence") or [])]
    k4 = say(len(new) == len(old) and not moved, "K4 citations intact: %d of %d sentences keep their evidence list%s" % (
        min(len(new), len(old)) - len(moved), len(old), (" (moved %s)" % moved[:5]) if moved else ""))
    ok = k1 and k2 and k3 and k4
    print("R85 REPAIR AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
