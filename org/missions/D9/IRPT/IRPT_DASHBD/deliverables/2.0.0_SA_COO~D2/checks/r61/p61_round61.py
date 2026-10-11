"""IRPT_DASHBD round 61 (issuer 2.0.0_SA_COO~D2) -- the R45 never-widen packet, SECOND refresh (1.0.0_SA_CTO~DELL2 msgs 3940, 3999, 4029).

Cell: DB-b-117 the R45 packet at the bytes after DB-b-115 (the handler passes src): four members from their live pins, one kit day on HEAD's
four members against the live-pinned run with the five output hashes equal, EVERY manifest the run writes compared field by field against
the live one, halves UNSIGNED.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB61-1-AC1  ~92/R45_REFRESH2_CENSUS.json: base_codesha256 == oNgy4rnr; members_changed paths are EXACTLY the four; each pin is a commit
              whose blob sha256 equals the recorded sha256 and HEAD's bytes; each carries base_sha256 differing from sha256 and a non-empty
              commits_since_live_pin list; rollback.base_s3_version non-empty.
  DB61-1-AC2  ~92/R45_REFRESH2_DELTA0.json: day 2026-10-08; members_at_head names the four; thresholds_sha256 is the pinned file's; tables
              holds exactly the five outputs, each rows > 0 and sha256_live == sha256_new; output_hash_equal is true.
  DB61-1-AC3  the same record's manifests: a non-empty list of {manifest, fields: [{field, live, new, verdict}]} with verdict in EQUAL /
              ADDED / CHANGED / REMOVED, including the returns manifest with method_version EQUAL at 2; no field REMOVED; every CHANGED
              field named in expected_changes with a reason; and ~92/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_2.md carries "## Supersedes",
              "## Branch A", "## Branch B", "## Rollback", "## Memory headroom", "## DELTA=0 evidence", "## Manifest comparison",
              "## COO half", "## CTO half", each half reading UNSIGNED.
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
        print("%s FAIL" % (cid or "DB61"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB61-1-AC1":
        r = load(D + "92/R45_REFRESH2_CENSUS.json")
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
    elif cid == "DB61-1-AC2":
        r = load(D + "92/R45_REFRESH2_DELTA0.json")
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
    elif cid == "DB61-1-AC3":
        r = load(D + "92/R45_REFRESH2_DELTA0.json")
        ms = r.get("manifests") or []
        if not ms:
            fail("manifests empty")
        exp = {(e.get("manifest"), e.get("field")) for e in (r.get("expected_changes") or []) if str(e.get("reason") or "").strip()}
        seen_mv = False
        for m in ms:
            fs = m.get("fields") or []
            if not m.get("manifest") or not fs:
                fail("manifest entry %r has no name or no fields" % m.get("manifest"))
            for f in fs:
                v = f.get("verdict")
                if v not in ("EQUAL", "ADDED", "CHANGED", "REMOVED"):
                    fail("%s.%s verdict %r" % (m["manifest"], f.get("field"), v))
                if v == "REMOVED":
                    fail("%s.%s is REMOVED against the live manifest" % (m["manifest"], f.get("field")))
                if v == "EQUAL" and f.get("live") != f.get("new"):
                    fail("%s.%s reads EQUAL but live %r != new %r" % (m["manifest"], f.get("field"), f.get("live"), f.get("new")))
                if v == "CHANGED" and (m["manifest"], f.get("field")) not in exp:
                    fail("%s.%s is CHANGED and not in expected_changes with a reason" % (m["manifest"], f.get("field")))
                if "return" in str(m["manifest"]).lower() and f.get("field") == "method_version":
                    if v != "EQUAL" or f.get("new") != 2:
                        fail("returns manifest method_version: verdict %r, live %r, new %r" % (v, f.get("live"), f.get("new")))
                    seen_mv = True
        if not seen_mv:
            fail("no returns manifest with a method_version field among %r" % [m.get("manifest") for m in ms])
        p = root / (D + "92/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_2.md")
        if not p.is_file():
            fail("no packet")
        t = p.read_text(encoding="utf-8")
        for hd in ("## Supersedes", "## Branch A", "## Branch B", "## Rollback", "## Memory headroom", "## DELTA=0 evidence", "## Manifest comparison",
                   "## COO half", "## CTO half"):
            if hd not in t:
                fail("missing heading %r" % hd)
        for hd in ("## COO half", "## CTO half"):
            if "UNSIGNED" not in re.split(r"\n## ", t.split(hd, 1)[1], maxsplit=1)[0]:
                fail("%s not UNSIGNED" % hd)
        print("OK: %d manifest(s) compared field by field, none REMOVED; packet sections present; both halves UNSIGNED" % len(ms))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
