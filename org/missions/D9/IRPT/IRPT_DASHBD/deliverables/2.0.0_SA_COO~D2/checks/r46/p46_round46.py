"""IRPT_DASHBD round 46 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 12 item 5 (msg 3371, @77e60c3d2b): DB-b-90 and DB-b-91
release TOGETHER as ONE gold Lambda release after yIAQjspL, under one never-widen pair; the member census against live yIAQjspL shows
exactly the members those two orders own, else STOP.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB46-1-AC1  ~69/R44_RELEASE_CENSUS.json: base_codesha256 == the yIAQjspL value; members_changed is a list whose path set is EXACTLY
              {account_activity_lots.py, reporting-gold handler.py}; each member's pin is a commit at HEAD whose blob sha256 equals the
              member's sha256 and equals the bytes at HEAD; rollback.base_s3_version is a non-empty string.
  DB46-1-AC2  ~69/NEVER_WIDEN_PACKET_R44_RELEASE.md carries the headings "## Branch A", "## Branch B", "## Rollback", "## COO half",
              "## CTO half", and each half's section reads UNSIGNED.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~69/"
BASE = "yIAQjspL0nPX6tJOHxD+Dv0REVoZyBNRkhmHQxUVuEE="
MEMBERS = {"data/assets/scripts/gold/irpt_reporting/account_activity_lots.py",
           "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB46"))
        sys.exit(1)

    if cid == "DB46-1-AC1":
        p = root / (D + "R44_RELEASE_CENSUS.json")
        if not p.is_file():
            fail("no census")
        r = json.loads(p.read_bytes().decode("utf-8"))
        if r.get("base_codesha256") != BASE:
            fail("base_codesha256 %r" % r.get("base_codesha256"))
        ms = r.get("members_changed")
        if not isinstance(ms, list) or {m.get("path") for m in ms} != MEMBERS or len(ms) != len(MEMBERS):
            fail("members_changed paths %r, want exactly %r" % ([m.get("path") for m in ms or []], sorted(MEMBERS)))
        for m in ms:
            pin, path, sha = str(m.get("pin") or ""), m["path"], str(m.get("sha256") or "")
            out = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (pin, path)], capture_output=True)
            if not pin or out.returncode != 0:
                fail("pin %r for %s does not resolve" % (pin, path))
            h = hashlib.sha256(out.stdout).hexdigest()
            if h != sha or hashlib.sha256((root / path).read_bytes()).hexdigest() != sha:
                fail("%s: pin blob %s / HEAD bytes differ from recorded %s" % (path, h[:12], sha[:12]))
        if not str((r.get("rollback") or {}).get("base_s3_version") or "").strip():
            fail("rollback.base_s3_version missing")
        print("OK: census = exactly the two members over base yIAQjspL; pins equal HEAD bytes")
    elif cid == "DB46-1-AC2":
        p = root / (D + "NEVER_WIDEN_PACKET_R44_RELEASE.md")
        if not p.is_file():
            fail("no packet")
        t = p.read_text(encoding="utf-8")
        for h in ("## Branch A", "## Branch B", "## Rollback", "## COO half", "## CTO half"):
            if h not in t:
                fail("missing heading %r" % h)
        for h in ("## COO half", "## CTO half"):
            sec = re.split(r"\n## ", t.split(h, 1)[1], maxsplit=1)[0]
            if "UNSIGNED" not in sec:
                fail("%s does not read UNSIGNED" % h)
        print("OK: packet sections present; both halves UNSIGNED")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
