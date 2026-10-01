"""Round 27 AC (IB-pr-272: CTO round-26 analysis rulings 1, 2 and 3) -- the read-only diagnosis record answers each question
with evidence a reader can open.

Usage: python p27_2_diagnosis.py <worktree root> <section> <criterion id>
  section nna    -- ruling 1: W97-S3's three 09-24 NNA rows (accounts 866, 769, 1096)
  section mirror -- ruling 2: why the ingest mirror and opal-assets-silver-orion did not move fact_positions past 2026-09-27
  section asof   -- ruling 3: whether Orion's positions endpoint accepts an as-of date, from its own documentation
Reads org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~99/ROUND27_DIAGNOSIS.json. Every section carries
`answer` (non-empty), `evidence` (a list of {"kind": "s3"|"log"|"file"|"doc", "ref": ...}), and its own required fields:
  nna:    `accounts` with keys 866, 769, 1096, each {"before": {...classification...}, "after": {...}, "household_id", "client_id"};
          `branch` in {"A", "B"}; if A, `same_household_or_client` true and `after` classes all INTERNAL
  mirror: `cause` (non-empty), `component` naming the stage that failed, `repair` (the proposed act, not performed)
  asof:   `accepts_as_of` in {"YES", "NO", "UNDETERMINED"}; `doc_ref` naming the file or document read; `calls_made` == 0
Every evidence ref of kind "s3" (s3://bucket/key) must HEAD 200; kind "file" must exist under the worktree.
Pass line: <criterion id> PASS. Base: FAIL (record absent).
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
section, cid = sys.argv[2], sys.argv[3]
REC = root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~99/ROUND27_DIAGNOSIS.json"


def fail(msg):
    print("%s FAIL: %s" % (cid, msg))
    sys.exit(1)


if not REC.exists():
    fail("record absent: %s" % REC)
d = json.loads(REC.read_text(encoding="utf-8")).get(section)
if not isinstance(d, dict):
    fail("section %r absent" % section)
if not str(d.get("answer") or "").strip():
    fail("section %r has no answer" % section)
ev = d.get("evidence")
if not isinstance(ev, list) or not ev:
    fail("section %r has no evidence list" % section)

if section == "nna":
    accts = d.get("accounts") or {}
    for a in ("866", "769", "1096"):
        row = accts.get(a)
        if not isinstance(row, dict) or not all(k in row for k in ("before", "after", "household_id", "client_id")):
            fail("account %s lacks before/after/household_id/client_id" % a)
    if d.get("branch") not in ("A", "B"):
        fail("branch %r not in A/B" % d.get("branch"))
    if d["branch"] == "A":
        if d.get("same_household_or_client") is not True:
            fail("branch A without same_household_or_client true")
        if any("INTERNAL" not in json.dumps(accts[a]["after"]).upper() for a in ("866", "769", "1096")):
            fail("branch A but an 'after' classification is not INTERNAL")
elif section == "mirror":
    for k in ("cause", "component", "repair"):
        if not str(d.get(k) or "").strip():
            fail("mirror lacks %s" % k)
elif section == "asof":
    if d.get("accepts_as_of") not in ("YES", "NO", "UNDETERMINED"):
        fail("accepts_as_of %r" % d.get("accepts_as_of"))
    if not str(d.get("doc_ref") or "").strip():
        fail("asof lacks doc_ref")
    if int(d.get("calls_made", -1)) != 0:
        fail("calls_made %r (the ruling reads documentation only)" % d.get("calls_made"))
else:
    fail("unknown section %r" % section)

s3 = None
checked = 0
for e in ev:
    kind, ref = e.get("kind"), str(e.get("ref") or "")
    if kind == "s3":
        if not ref.startswith("s3://"):
            fail("s3 evidence not an s3 uri: %r" % ref)
        if s3 is None:
            import boto3
            s3 = boto3.client("s3", region_name="us-east-1")
        b, k = ref[5:].split("/", 1)
        try:
            s3.head_object(Bucket=b, Key=k)
        except Exception as exc:  # noqa: BLE001
            fail("evidence %s does not read: %s" % (ref, str(exc)[:100]))
        checked += 1
    elif kind == "file":
        if not (root / ref.split(":")[0]).exists():
            fail("evidence file absent: %s" % ref)
        checked += 1
print("  section %s: answer present, %d evidence item(s), %d opened" % (section, len(ev), checked))
print("%s PASS" % cid)
