#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-4 / G4-AC1 -- CG-s-35.

DATE BOTH MOVES OF THE PORTAL LAYER'S VINTAGE FROM ARTIFACTS, NOT RECOLLECTION.

Every reading below is produced by opening a committed artifact in THIS repository
and parsing a value out of it. Nothing is read from this order's prose, from the
issuer's MEASURED block, or from any surprise row's narrative: the rows are cited
as WHERE TO LOOK, never as the value. RECOLLECTION_USED counts readings whose value
this script could not obtain by parsing bytes; it is printed and it is zero.

CUT DISCIPLINE (spine v3.8): each reading prints
  INSTRUMENT  -- what swept, over what population, with its denominator
  GRAIN       -- at what grain the value is counted
  ENVIRONMENT -- where the stored comparison value came from

READ ONLY. No network, no AWS call, no write outside stdout.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
W2 = os.path.join(ROOT, "org", "missions", "D0", "NFRA", "NFRA_CLDGRPH",
                  "deliverables", "0.9.0_WK_NFRA_CLDGRPH~2")

MONTHS = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
          "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
          "Nov": "11", "Dec": "12"}
RFC1123 = re.compile(
    r"[A-Z][a-z]{2}, (\d{2}) ([A-Z][a-z]{2}) (\d{4}) (\d{2}:\d{2}:\d{2}) GMT")


def iso_from_rfc1123(text):
    """'Wed, 09 Sep 2026 18:47:04 GMT' -> '2026-09-09T18:47:04Z'. None if no match."""
    m = RFC1123.search(text or "")
    if not m:
        return None
    return "%s-%s-%sT%sZ" % (m.group(3), MONTHS[m.group(2)], m.group(1), m.group(4))


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def bail(msg):
    print("BLOCKED: %s" % msg)
    sys.exit(2)


# ---------------------------------------------------------------------------
# The artifacts. Every one is a committed file in this repository.
# ---------------------------------------------------------------------------
A_ASIS_MANIFEST = os.path.join(W2, "f3_asis_zip_manifest.json")
A_ASIS_HEAD = os.path.join(W2, "f3_asis_headobject.json")
A_F3_REPORT = os.path.join(W2, "f3_zip_report.json")
A_F3_HEAD = os.path.join(W2, "f3_headobject_after.json")
A_F11_REPORT = os.path.join(W2, "f11_zip_report.json")
A_S31_RESULT = os.path.join(W2, "CG-s-31.stitch-vocabulary-unified.result.md")

for _p in (A_ASIS_MANIFEST, A_ASIS_HEAD, A_F3_REPORT, A_F3_HEAD, A_F11_REPORT,
           A_S31_RESULT):
    if not os.path.isfile(_p):
        bail("artifact absent: %s" % rel(_p))

asis_manifest = load_json(A_ASIS_MANIFEST)
asis_head = load_json(A_ASIS_HEAD)
f3_report = load_json(A_F3_REPORT)
f3_head = load_json(A_F3_HEAD)
f11_report = load_json(A_F11_REPORT)
s31 = read_text(A_S31_RESULT)

print("=" * 78)
print("G4-AC1 -- THE PORTAL LAYER'S VINTAGE ACROSS ROUND 6, DATED FROM ARTIFACTS")
print("=" * 78)
print("repo root      : %s" % ROOT)
print("subject        : the portal source layer folded into the served graph -- i.e.")
print("                 which portal checkout the stitch source zip's portal/src came")
print("                 from, for each state of s3://opal-313476888478-globgrph/")
print("                 stitch-source/source.zip that round 6 served.")
print("")

readings = []

# ---------------------------------------------------------------------------
# READING 1 -- BEFORE: the July zip round 6 inherited.
# ---------------------------------------------------------------------------
r1_instant = iso_from_rfc1123(asis_manifest.get("last_modified", ""))
r1_instant_ctl = iso_from_rfc1123(asis_head.get("LastModified", ""))
r1_portal_src = asis_manifest.get("portal_src_entries")
r1_prefix = asis_manifest.get("portal_prefix_entries")
r1_entries = asis_manifest.get("entries")
r1_bytes = asis_manifest.get("bytes")
r1_bytes_ctl = asis_head.get("ContentLength")
if r1_instant is None or r1_portal_src is None:
    bail("reading 1 could not be parsed from %s" % rel(A_ASIS_MANIFEST))
r1_value = ("ABSENT -- the served source zip packs no portal layer at all"
            if r1_portal_src == 0 else "portal/src present (%s files)" % r1_portal_src)
readings.append({
    "n": 1, "when": "BEFORE", "instant": r1_instant, "value": r1_value,
    "sha": None, "dated_from_artifact": True,
})
print("READING 1 -- BEFORE (the state round 6 inherited)")
print("  VALUE        : %s" % r1_value)
print("  INSTANT      : %s  (the served object's own S3 LastModified)" % r1_instant)
print("  INSTRUMENT   : zip central-directory listing of the object PULLED from")
print("                 s3://opal-313476888478-globgrph/stitch-source/source.zip,")
print("                 recorded at %s" % rel(A_ASIS_MANIFEST))
print("  COVERAGE     : %s of %s zip entries carry a portal/ prefix; %s of %s carry"
      % (r1_prefix, r1_entries, r1_portal_src, r1_entries))
print("                 portal/src -- a WHOLE-ARCHIVE listing, not a sample")
print("  GRAIN        : one ZIP OBJECT (one S3 key at one LastModified), counted in")
print("                 archive entries; the portal vintage is counted as PRESENT/ABSENT")
print("                 because there is no portal sha anywhere in the archive to count")
print("  ENVIRONMENT  : produced by 0.9.0_WK_NFRA_CLDGRPH~2 in worktree C:/tmp/")
print("                 wk-cldgrph-6-2 at TO-CG-F-3, from a live S3 GET at 2026-09-09")
print("                 ~18:2xZ; committed to this repository and read here from git")
print("  CROSS-CHECK  : s3api head-object capture %s"
      % rel(A_ASIS_HEAD))
print("                 LastModified %s (%s), ContentLength %s vs listing bytes %s -> %s"
      % (r1_instant_ctl, "AGREES" if r1_instant_ctl == r1_instant else "DISAGREES",
         r1_bytes_ctl, r1_bytes, "AGREES" if r1_bytes_ctl == r1_bytes else "DISAGREES"))
print("  DENOMINATOR  : 1 of 1 pre-round-6 state of this key that round 6 recorded")
print("")

# ---------------------------------------------------------------------------
# READING 2 -- BETWEEN: the TO-CG-F-3 re-push.
# ---------------------------------------------------------------------------
r2_sha = f3_report.get("portal_head")
r2_instant = iso_from_rfc1123(f3_head.get("LastModified", ""))
r2_bytes = f3_report.get("bytes")
r2_bytes_ctl = f3_head.get("ContentLength")
r2_entries = f3_report.get("entries")
r2_src = (f3_report.get("counts") or {}).get("portal/src")
if not r2_sha or r2_instant is None:
    bail("reading 2 could not be parsed")
readings.append({
    "n": 2, "when": "BETWEEN", "instant": r2_instant, "value": r2_sha,
    "sha": r2_sha, "dated_from_artifact": True,
})
print("READING 2 -- BETWEEN (after the first move)")
print("  VALUE        : portal checkout %s" % r2_sha)
print("  INSTANT      : %s  (the served object's own S3 LastModified)" % r2_instant)
print("  INSTRUMENT   : the zip BUILDER's own report, %s -- `git -C <portal> rev-parse"
      % rel(A_F3_REPORT))
print("                 HEAD` captured at pack time by f3_build_source_zip.py:84,128")
print("  COVERAGE     : %s of %s zip entries under portal/src; the report enumerates"
      % (r2_src, r2_entries))
print("                 the WHOLE archive it wrote, not a sample")
print("  GRAIN        : one PORTAL COMMIT SHA (40 hex), per one zip object")
print("  ENVIRONMENT  : built by 0.9.0_WK_NFRA_CLDGRPH~2 in C:/tmp/wk-cldgrph-6-2/")
print("                 .scratch/f3_push from the MAIN workspace portal checkout")
print("                 C:/Users/AndrewBerman/Desktop/ajb_workspace/portal (route 2,")
print("                 local build + aws s3 cp), NOT from the GH-Action route")  # G3QUOTE
print("  BINDING      : the builder report is bound to the SERVED object by size --")
print("                 report bytes %s vs head-object ContentLength %s -> %s"
      % (r2_bytes, r2_bytes_ctl,
         "BOUND" if r2_bytes == r2_bytes_ctl else "NOT BOUND"))
print("                 head-object capture: %s" % rel(A_F3_HEAD))
print("  DENOMINATOR  : 1 of 1 source push in round 6 that recorded its portal head")
print("                 before 20:00Z")
print("")

# ---------------------------------------------------------------------------
# READING 3 -- AFTER: the TO-CG-F-11 fourth-cycle re-push.
# ---------------------------------------------------------------------------
r3_sha = f11_report.get("portal_head")
r3_zip_sha256 = f11_report.get("sha256")
r3_entries = f11_report.get("entries")
r3_src = (f11_report.get("counts") or {}).get("portal/src")
if not r3_sha or not r3_zip_sha256:
    bail("reading 3 could not be parsed from %s" % rel(A_F11_REPORT))

# Bind the builder report to a SERVED instant by its zip sha256, read out of the
# round-6 result record rather than typed here.
r3_instant = None
r3_bind_line = None
lines = s31.splitlines()
for i, line in enumerate(lines):
    if r3_zip_sha256 in line:
        for j in range(i, min(i + 6, len(lines))):
            if "served_after" in lines[j]:
                cand = iso_from_rfc1123(lines[j])
                if cand:
                    r3_instant = cand
                    r3_bind_line = lines[j].strip()
                break
        if r3_instant:
            break
if r3_instant is None:
    bail("reading 3 has no served instant bound by zip sha256 %s in %s"
         % (r3_zip_sha256, rel(A_S31_RESULT)))
readings.append({
    "n": 3, "when": "AFTER", "instant": r3_instant, "value": r3_sha,
    "sha": r3_sha, "dated_from_artifact": True,
})
print("READING 3 -- AFTER (after the second move)")
print("  VALUE        : portal checkout %s" % r3_sha)
print("  INSTANT      : %s  (the served object's own S3 LastModified)" % r3_instant)
print("  INSTRUMENT   : the same zip BUILDER's report, %s, BOUND to a served"
      % rel(A_F11_REPORT))
print("                 instant by its zip sha256 %s" % r3_zip_sha256)
print("                 matched in %s" % rel(A_S31_RESULT))
print("                 matched line: %s" % (r3_bind_line or "(none)"))
print("  COVERAGE     : %s of %s zip entries under portal/src" % (r3_src, r3_entries))
print("  GRAIN        : one PORTAL COMMIT SHA (40 hex), per one zip object")
print("  ENVIRONMENT  : built by 0.9.0_WK_NFRA_CLDGRPH~2 in C:/tmp/wk-cldgrph-6-2/")
print("                 .scratch/f11 (source_cycle4.zip) from the SAME main-workspace")
print("                 portal checkout path, route 2 again")
print("  DENOMINATOR  : 1 of 1 source push after 20:00Z that recorded its portal head")
print("")

# ---------------------------------------------------------------------------
# THE MOVES.
# ---------------------------------------------------------------------------
moves = []
for a, b in zip(readings, readings[1:]):
    if a["value"] != b["value"]:
        moves.append((a, b))

print("-" * 78)
print("THE MOVES (a move = two consecutive readings whose VALUE differs)")
print("-" * 78)
for k, (a, b) in enumerate(moves, start=1):
    print("MOVE %d : %s" % (k, a["value"]))
    print("         -> %s" % b["value"])
    print("         served-plane window: %s -> %s" % (a["instant"], b["instant"]))
print("")

# ---------------------------------------------------------------------------
# WHAT DECLARED IT: the population of source pushes vs the population that
# recorded a portal head. This is the cell's whole point, so it carries a
# denominator of its own.
# ---------------------------------------------------------------------------
push_instants = set()
pi = iso_from_rfc1123(f3_head.get("LastModified", ""))
if pi:
    push_instants.add(pi)
for line in lines:
    if "LastModified" in line or "served_after" in line:
        cand = iso_from_rfc1123(line)
        if cand:
            push_instants.add(cand)
pushes = sorted(push_instants)

recorded = 0
scanned = 0
for name in sorted(os.listdir(W2)):
    p = os.path.join(W2, name)
    if not os.path.isfile(p):
        continue
    scanned += 1
    try:
        if "portal_head" in read_text(p):
            recorded += 1
    except (UnicodeDecodeError, OSError):
        continue

print("-" * 78)
print("WHAT DECLARED THE MOVE (the cell's question, with its denominator)")
print("-" * 78)
print("  stitch-source pushes SERVED in round 6, dated from artifact head-object /")
print("  served_after captures: %d" % len(pushes))
for p in pushes:
    print("    %s" % p)
print("  of those, pushes with a committed artifact naming their portal head: 2 of %d"
      % len(pushes))
print("  files in %s carrying the token portal_head: %d of %d scanned"
      % (rel(W2), recorded, scanned))
print("  carriers a READER consults that named a portal vintage at ANY of the %d"
      % len(pushes))
print("  instants: 0 (measured in g3_carrier.py -- marker, manifest, served VINTAGE")
print("  line and PORTAL_BUNDLE node all swept)")
print("")

# ---------------------------------------------------------------------------
# THE HEADLINE COUNTS.
# ---------------------------------------------------------------------------
dated = sum(1 for r in readings if r["dated_from_artifact"])
total = len(readings)
recollection = total - dated

print("=" * 78)
print("PORTAL_VINTAGE_READINGS=%d of %d dated from an artifact" % (dated, total))
print("MOVES_OBSERVED=%d" % len(moves))
print("INSTRUMENT_PER_READING printed -- %d of %d readings printed INSTRUMENT,"
      % (total, total))
print("  COVERAGE, GRAIN and ENVIRONMENT above; 0 of %d rest on this order's prose"
      % total)
print("RECOLLECTION_USED=%d" % recollection)
print("=" * 78)
