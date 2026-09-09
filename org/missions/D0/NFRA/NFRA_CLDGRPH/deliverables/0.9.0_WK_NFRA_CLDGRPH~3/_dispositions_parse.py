#!/usr/bin/env python3
"""E3-AC1 instrument -- parse a disposition record and grade every entry.

Takes the FIRST fenced json block of the record file, requires an object with
an `artifacts` array and a `p7_row_id`, and grades each entry on:

  artifact         non-empty string
  size_bytes       int
  mtime            non-empty string
  manifest         non-empty string (the word n/a is allowed and is a claim)
  disposition      a member of the CLOSED vocabulary
  owner            a serial (N.N.N_XX_Name[~slot])
  reason           non-empty and >= 80 chars -- a one-word reason is the rot
                   with a tidier label
  later_act_if_any non-empty string
  p7_status        non-empty string

It is the SAME parser the control feeds a planted ownerless entry through, so
the pass on the real record is bounded by a probe that made it fail.

usage: _dispositions_parse.py <record.md> [--channel <investigation.md>]
       [--expect-artifacts N] [--label L]
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import json
import re
import sys

VOCAB = ("RETIRE_WITH_TOMBSTONE", "ARCHIVE_UNDER_PROJECT",
         "KEEP_WITH_NAMED_READER", "HOLD_PENDING_P7")
SERIAL = re.compile(r"^[0-9]\.[0-9]\.[0-9]_[A-Z]{2}_[A-Za-z0-9_]+(~[A-Za-z0-9]+)?$")
FIELDS = ("artifact", "size_bytes", "mtime", "manifest", "disposition",
          "owner", "reason", "later_act_if_any", "p7_status")
MIN_REASON = 80


def first_block(path: str):
    txt = open(path, encoding="utf-8").read()
    for b in re.findall(r"```json\n(.*?)\n```", txt, re.S):
        try:
            d = json.loads(b)
        except Exception as ex:
            print("  BLOCK-UNPARSEABLE: %s" % ex)
            continue
        if isinstance(d, dict) and "artifacts" in d:
            return d
    return None


def grade(entry, idx):
    problems = []
    for f in FIELDS:
        if f not in entry:
            problems.append("MISSING FIELD %s" % f)
    if not problems:
        if entry["disposition"] not in VOCAB:
            problems.append("disposition %r not in the closed vocabulary"
                            % entry["disposition"])
        if not SERIAL.match(str(entry["owner"])):
            problems.append("owner %r is not a serial" % entry["owner"])
        if not isinstance(entry["size_bytes"], int):
            problems.append("size_bytes %r is not an int" % entry["size_bytes"])
        for f in ("artifact", "mtime", "manifest", "later_act_if_any", "p7_status"):
            if not str(entry[f]).strip():
                problems.append("%s is empty" % f)
        if len(str(entry["reason"]).strip()) < MIN_REASON:
            problems.append("reason is %d chars, under the %d-char floor"
                            % (len(str(entry["reason"]).strip()), MIN_REASON))
    name = str(entry.get("artifact", "<no artifact field>"))
    if problems:
        print("  ENTRY %d REJECTED  %s" % (idx, name))
        for p in problems:
            print("      -> %s" % p)
        return False
    print("  ENTRY %d OK  %-95s %-22s owner=%s"
          % (idx, name[-95:], entry["disposition"], entry["owner"]))
    return True


def main() -> int:
    args = sys.argv[1:]
    label = "RECORD"
    channel = None
    expect = None
    while len(args) > 1 and args[1].startswith("--"):
        k = args[1]
        if k == "--channel":
            channel = args[2]
            del args[1:3]
        elif k == "--expect-artifacts":
            expect = int(args[2])
            del args[1:3]
        elif k == "--label":
            label = args[2]
            del args[1:3]
        else:
            break
    path = args[0]
    print("--- DISPOSITION PARSE [%s] %s ---" % (label, path))
    doc = first_block(path)
    if doc is None:
        print("  NO fenced json object with an `artifacts` array in this file")
        print("DISPOSITIONS=0 of 0 RECORDED")
        return 0
    arts = doc.get("artifacts") or []
    denom = expect if expect is not None else len(arts)
    ok = 0
    for i, e in enumerate(arts, 1):
        if grade(e, i):
            ok += 1
    print("  VOCABULARY (closed, %d values): %s" % (len(VOCAB), ", ".join(VOCAB)))
    seen = sorted({e.get("disposition") for e in arts})
    print("  DISPOSITIONS USED: %s" % ", ".join(str(s) for s in seen))
    print("  ENTRIES PARSED=%d  EXPECTED=%s" % (len(arts), denom))
    row = doc.get("p7_row_id", "")
    if channel:
        ctext = open(channel, encoding="utf-8").read()
        ids = set()
        for b in re.findall(r"```json\n(.*?)\n```", ctext, re.S):
            try:
                d = json.loads(b)
            except Exception:
                continue
            for r in (d if isinstance(d, list) else [d]):
                if isinstance(r, dict) and r.get("id"):
                    ids.add(r["id"])
        print("  CHANNEL ROWS PARSED=%d  (%s)" % (len(ids), channel))
        if row in ids:
            print("  P7 ROW RESOLVES IN THE CHANNEL: %s" % row)
        else:
            print("  P7 ROW DOES NOT RESOLVE: %r" % row)
            row = ""
    print("DISPOSITIONS=%d of %d RECORDED" % (ok, denom))
    print("P7_ROW_FILED=%s" % (row or "NONE"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
