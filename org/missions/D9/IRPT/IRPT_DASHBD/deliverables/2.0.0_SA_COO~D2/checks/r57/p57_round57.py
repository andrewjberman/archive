"""IRPT_DASHBD round 57 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 3940: refresh the R45 release packet at the new source bytes.

Cell: DB-b-113 the R45 never-widen packet REFRESHED after DB-b-110 (the lots read cut, drained @5d339ced5b) and the docstring redaction
@354214c55f moved two staged members. The census is taken against the LIVE bundle's pins, the DELTA=0 evidence is one kit day run on the
live-pinned members and on HEAD's members with the five output hashes equal, and both halves read UNSIGNED.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB57-1-AC1  ~88/R45_REFRESH_CENSUS.json: base_codesha256 == oNgy4rnr; members_changed paths are EXACTLY the four (reporting-gold handler.py,
              account_return_daily.py, account_activity_lots.py and, by AMENDMENT 1, sources.json); each pin is a commit whose blob sha256 equals the recorded sha256 and HEAD's
              bytes; each carries base_sha256 (the live-pinned bytes) differing from sha256 and a non-empty commits_since_live_pin list;
              rollback.base_s3_version non-empty.
  DB57-1-AC2  ~88/R45_REFRESH_DELTA0.json: day 2026-10-08; members_at_head names the four members (the "new" run has all four at HEAD); thresholds_sha256 is the pinned thresholds file's for both runs; tables holds
              exactly the five outputs, each with rows > 0 and sha256_live == sha256_new; output_hash_equal is true.
  DB57-1-AC3  ~88/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH.md carries "## Supersedes", "## Branch A", "## Branch B", "## Rollback",
              "## Memory headroom", "## DELTA=0 evidence", "## COO half", "## CTO half", each half reading UNSIGNED.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
LIVE = "oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM="
MEMBERS = {
    "infra/aws/lambda/investor-reporting/reporting-gold/handler.py",
    "data/assets/scripts/gold/irpt_reporting/account_return_daily.py",
    "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py",
    "data/assets/scripts/gold/irpt_reporting/sources.json",
}
THRESHOLDS = "551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177"
TABLES = {"returns", "class", "account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB57"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB57-1-AC1":
        r = load(D + "88/R45_REFRESH_CENSUS.json")
        if r.get("base_codesha256") != LIVE:
            fail("base_codesha256 %r" % r.get("base_codesha256"))
        ms = r.get("members_changed") or []
        paths = [m.get("path") for m in ms]
        if len(paths) != len(MEMBERS) or set(paths) != MEMBERS:
            fail("members_changed %r, want exactly %r" % (paths, sorted(MEMBERS)))
        for m in ms:
            path = m["path"]
            out = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (m.get("pin"), path)], capture_output=True)
            if not m.get("pin") or out.returncode != 0:
                fail("pin %r does not resolve for %s" % (m.get("pin"), path))
            h = hashlib.sha256(out.stdout).hexdigest()
            if h != m.get("sha256") or hashlib.sha256((root / path).read_bytes()).hexdigest() != h:
                fail("pin blob / HEAD bytes / recorded sha256 differ for %s" % path)
            if not HEX64.match(str(m.get("base_sha256") or "")) or m.get("base_sha256") == h:
                fail("base_sha256 %r missing or equal to the new bytes for %s" % (m.get("base_sha256"), path))
            if not m.get("commits_since_live_pin"):
                fail("commits_since_live_pin empty for %s" % path)
        if not str((r.get("rollback") or {}).get("base_s3_version") or "").strip():
            fail("rollback.base_s3_version missing")
        print("OK: four members over oNgy4rnr, each pinned to HEAD bytes with its commits since the live pin")
    elif cid == "DB57-1-AC2":
        r = load(D + "88/R45_REFRESH_DELTA0.json")
        if r.get("day") != "2026-10-08":
            fail("day %r" % r.get("day"))
        if sorted(r.get("members_at_head") or []) != sorted(MEMBERS):
            fail("members_at_head %r, want the four members (AMENDMENT 1)" % r.get("members_at_head"))
        if r.get("thresholds_sha256") != THRESHOLDS:
            fail("thresholds_sha256 %r is not the pinned file's" % r.get("thresholds_sha256"))
        ts = r.get("tables") or {}
        if set(ts) != TABLES:
            fail("tables %r, want %r" % (sorted(ts), sorted(TABLES)))
        for name in sorted(ts):
            t = ts[name]
            a, b = str(t.get("sha256_live") or ""), str(t.get("sha256_new") or "")
            if not isinstance(t.get("rows"), int) or t["rows"] <= 0 or not HEX64.match(a) or a != b:
                fail("table %s: rows %r, live %r, new %r" % (name, t.get("rows"), a, b))
        if r.get("output_hash_equal") is not True:
            fail("output_hash_equal %r" % r.get("output_hash_equal"))
        print("OK: five tables hash equal between the live-pinned members and HEAD's on 2026-10-08")
    elif cid == "DB57-1-AC3":
        p = root / (D + "88/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH.md")
        if not p.is_file():
            fail("no packet")
        t = p.read_text(encoding="utf-8")
        for hd in ("## Supersedes", "## Branch A", "## Branch B", "## Rollback", "## Memory headroom", "## DELTA=0 evidence", "## COO half",
                   "## CTO half"):
            if hd not in t:
                fail("missing heading %r" % hd)
        for hd in ("## COO half", "## CTO half"):
            if "UNSIGNED" not in re.split(r"\n## ", t.split(hd, 1)[1], maxsplit=1)[0]:
                fail("%s not UNSIGNED" % hd)
        print("OK: packet sections present; both halves UNSIGNED")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
