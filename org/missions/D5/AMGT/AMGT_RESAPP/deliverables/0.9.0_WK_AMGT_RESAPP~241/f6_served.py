"""
f6_served.py -- F6's measure re-run on the peers the route SERVES (AMGT-av-5, DSGN FWD-8).

F6's method is deliverables/0.9.0_WK_AMGT_RESAPP~3/f6_remeasure.py (read only here): a peer set is the stale KPN
telecom copy when it overlaps the fixed 12-name KPN set at >= STALE_OVERLAP_THRESHOLD (6). That script scores a workbook's
CSC sheet; this one scores every covered name's served /security/<key>/peers members.

Overlap here = the number of served members that match an entry of the 12-name set, a member counting once. A member
matches an entry when its ticker equals the entry's root (scanner tickers carry no exchange: 'VZ', 'T'), or when the
member's matched company record is held under the entry's full Bloomberg form. A name serving no members is not scored
(it is not in N). WRONG = a served set at or over the threshold.

Run:    PYTHONPATH="$(pwd)" python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~241/f6_served.py
Prints: F6 WRONG n of N
Writes: f6_served.json beside this script (never ~3's f6_remeasure.json).
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F6_PATH = os.path.join(HERE, "..", "0.9.0_WK_AMGT_RESAPP~3", "f6_remeasure.py")
OUTPUT_PATH = os.path.join(HERE, "f6_served.json")
PREFIX = "/api/scoped/amgt"


def _load_f6():
    spec = importlib.util.spec_from_file_location("f6_remeasure", F6_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _norm(text):
    return re.sub(r"\s+", " ", str(text or "").strip()).upper()


def main():
    f6 = _load_f6()
    kpn = {_norm(e) for e in f6.KPN_STALE_SET}
    roots = {}
    for entry in kpn:
        roots.setdefault(entry.rsplit(" ", 1)[0], set()).add(entry)
    threshold = f6.STALE_OVERLAP_THRESHOLD

    from lib.research.api import scoped_amgt
    from lib.research.coverage import covered_universe

    keys = sorted(covered_universe.covered_security_keys())
    rows, no_members, non200 = [], [], []
    for key in keys:
        event = {"rawPath": "%s/security/%s/peers" % (PREFIX, key),
                 "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
                 "queryStringParameters": None}
        resp = scoped_amgt.handler(event)
        if resp.get("statusCode") != 200:
            non200.append("%s:%s" % (key, resp.get("statusCode")))
            continue
        members = (json.loads(resp.get("body") or "null") or {}).get("members") or []
        if not members:
            no_members.append(key)
            continue
        matched = []
        for member in members:
            ticker = _norm(member.get("ticker"))
            hit = bool(ticker) and ticker in roots
            if not hit:
                record_key = member.get("security_key") or (member.get("identity") or {}).get("security_key")
                form = _norm(((member.get("identity") or {}).get("bloomberg")) or "")
                hit = bool(form) and form in kpn
                if not hit and record_key:
                    from lib.research.identity import crosswalk
                    record = crosswalk.record_for(record_key) or {}
                    hit = _norm(record.get("bloomberg")) in kpn
            if hit:
                matched.append(member.get("ticker"))
        rows.append({"security_key": key, "members": len(members), "overlap": len(matched),
                     "matched": matched, "wrong": len(matched) >= threshold})
    wrong = [r for r in rows if r["wrong"]]
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"threshold": threshold, "kpn_set": sorted(kpn), "covered_names": len(keys),
                   "names_serving_members": len(rows), "names_serving_no_members": no_members, "non200": non200,
                   "wrong": [r["security_key"] for r in wrong], "rows": rows}, fh, indent=2, ensure_ascii=True)
        fh.write("\n")
    print("covered names %d; serving members %d; serving none %d; non-200 %d; max overlap %d (threshold %d)"
          % (len(keys), len(rows), len(no_members), len(non200), max([r["overlap"] for r in rows] or [0]), threshold))
    print("F6 WRONG %d of %d" % (len(wrong), len(rows)))
    return 0 if not non200 else 1


if __name__ == "__main__":
    sys.exit(main())
