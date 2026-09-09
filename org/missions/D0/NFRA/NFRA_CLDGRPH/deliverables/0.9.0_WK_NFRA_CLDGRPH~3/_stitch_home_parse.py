#!/usr/bin/env python3
"""E4-AC1 instrument -- parse the stitch-home record and grade it.

Takes the first fenced json object carrying a `home` key and requires:

  home                a member of the CLOSED two-value vocabulary
  owner               a serial (N.N.N_XX_Name[~slot])
  reason              non-empty and >= 200 chars -- this cell's whole output is
                      a decision, and a decision without a reason is a coin toss
                      with a serial attached
  producer            an object carrying tf_resource, schedule, s3_key and
                      vintage_now, each non-empty  -> PRODUCER_READ=true
  consumer            an object carrying file and lines
  rebuild_path_to_projection  == 0
  later_round_cells   for JOIN_PROJECTION: >= 1 entry, each with surface, lane,
                      verb and accept, and the lane must be a serial-shaped lane
                      id. For LOCAL_SCRATCH_DECLARED the list may be empty and
                      that is printed as the reason it is empty.

usage: _stitch_home_parse.py <record.md> [--label L]
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import json
import re
import sys

VOCAB = ("JOIN_PROJECTION", "LOCAL_SCRATCH_DECLARED")
SERIAL = re.compile(r"^[0-9]\.[0-9]\.[0-9]_[A-Z]{2}_[A-Za-z0-9_]+(~[A-Za-z0-9]+)?$")
PRODUCER_KEYS = ("tf_resource", "schedule", "s3_key", "vintage_now")
CELL_KEYS = ("surface", "lane", "verb", "accept")
MIN_REASON = 200


def first_block(path: str):
    txt = open(path, encoding="utf-8").read()
    for b in re.findall(r"```json\n(.*?)\n```", txt, re.S):
        try:
            d = json.loads(b)
        except Exception as ex:
            print("  BLOCK-UNPARSEABLE: %s" % ex)
            continue
        if isinstance(d, dict) and "home" in d:
            return d
    return None


def main() -> int:
    args = sys.argv[1:]
    label = "REAL"
    if "--label" in args:
        i = args.index("--label")
        label = args[i + 1]
        args = args[:i] + args[i + 2:]
    path = args[0]
    print("--- STITCH HOME PARSE [%s] %s ---" % (label, path))
    print("  VOCABULARY (closed, %d values): %s" % (len(VOCAB), ", ".join(VOCAB)))
    doc = first_block(path)
    if doc is None:
        print("  NO fenced json object carrying a `home` key in this file")
        print("STITCH_HOME=NONE NOT-RECORDED")
        print("PRODUCER_READ=false")
        return 0

    problems = []
    home = doc.get("home", "")
    if home not in VOCAB:
        problems.append("home %r is not in the closed vocabulary" % home)
    owner = str(doc.get("owner", ""))
    if not SERIAL.match(owner):
        problems.append("owner %r is not a serial" % owner)
    reason = str(doc.get("reason", "")).strip()
    if len(reason) < MIN_REASON:
        problems.append("reason is %d chars, under the %d-char floor"
                        % (len(reason), MIN_REASON))
    prod = doc.get("producer") or {}
    prod_ok = isinstance(prod, dict) and all(str(prod.get(k, "")).strip()
                                             for k in PRODUCER_KEYS)
    if not prod_ok:
        missing = [k for k in PRODUCER_KEYS
                   if not str((prod or {}).get(k, "")).strip()]
        problems.append("producer block incomplete: missing/empty %s" % missing)
    cons = doc.get("consumer") or {}
    if not (isinstance(cons, dict) and str(cons.get("file", "")).strip()
            and str(cons.get("lines", "")).strip()):
        problems.append("consumer block incomplete (needs file and lines)")
    rb = doc.get("rebuild_path_to_projection", None)
    if rb != 0:
        problems.append("rebuild_path_to_projection is %r, must be 0" % rb)

    cells = doc.get("later_round_cells") or []
    print("  OWNER=%s" % owner)
    print("  REASON_CHARS=%d (floor %d)" % (len(reason), MIN_REASON))
    for k in PRODUCER_KEYS:
        v = str((prod or {}).get(k, ""))
        print("  PRODUCER.%s = %s" % (k, (v[:150] + "...") if len(v) > 150 else v))
    print("  CONSUMER.file = %s" % cons.get("file", ""))
    print("  REBUILD_PATH_TO_PROJECTION = %r" % rb)
    for i, c in enumerate(cells, 1):
        miss = [k for k in CELL_KEYS if not str(c.get(k, "")).strip()]
        lane = str(c.get("lane", ""))
        lane_ok = bool(SERIAL.match(lane))
        if miss or not lane_ok:
            problems.append("later_round_cell %d: missing %s lane_ok=%s"
                            % (i, miss, lane_ok))
        print("  CELL %d  lane=%-22s verb=%-8s surface=%s"
              % (i, lane, c.get("verb", ""), str(c.get("surface", ""))[:70]))
    if home == "JOIN_PROJECTION" and len(cells) < 1:
        problems.append("home is JOIN_PROJECTION and NO later-round cell is named")
    if home == "LOCAL_SCRATCH_DECLARED" and not cells:
        print("  (no later-round cells: LOCAL_SCRATCH_DECLARED implies none)")
    print("  LATER_ROUND_CELLS=%d" % len(cells))

    for p in problems:
        print("  REJECTED -> %s" % p)
    if problems:
        print("STITCH_HOME=%s NOT-RECORDED (%d defect(s))" % (home or "NONE", len(problems)))
        print("PRODUCER_READ=%s" % ("true" if prod_ok else "false"))
        return 0
    print("STITCH_HOME=%s RECORDED" % home)
    print("PRODUCER_READ=true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
