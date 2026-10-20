"""Read the r34n build record and grade it (READ ONLY: nothing is built, uploaded or run).

usage: python -I check_r34m_record.py <RESIDENT_R34N_BUILD.json> [--identity]

No flag: prints R34N-RECORD-OK changed=<n> added=<n> removed=<n> only when delta_vs_r34m.changed is exactly the two
expected members, added and removed are empty, the artifact has a 64-hex sha256 and an integer member count.
--identity: prints R34N-IDENTITY-OK builds_identical=yes smoke_fail=0 only when two_builds.files_compared equals
two_builds.identical and the import smoke line reads fail=0.
Anything else prints R34N-RECORD-BAD <why> (or R34N-IDENTITY-BAD <why>) and exits 1. ASCII only.
"""
import json
import os
import re
import sys

EXPECT = sorted(["SHA256SUMS", "reports/resident_bindings.json"])


def bad(prefix, why):
    print("%s %s" % (prefix, why))
    return 1


def load(path):
    if not os.path.isfile(path):
        return None, "record absent: %s" % path
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh), ""
    except (OSError, ValueError) as exc:
        return None, "record unreadable: %s" % exc


def check_record(rec):
    delta = rec.get("delta_vs_r34m")
    if not isinstance(delta, dict):
        return "no delta_vs_r34m block"
    changed = sorted(delta.get("changed") or [])
    added = delta.get("added")
    removed = delta.get("removed")
    if changed != EXPECT:
        return "changed is %s, want exactly %s" % (changed, EXPECT)
    if added != [] or removed != []:
        return "added %s removed %s, want none" % (added, removed)
    art = rec.get("artifact") or {}
    sha = art.get("sha256")
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
        return "artifact sha256 is not 64 hex: %r" % (sha,)
    count = art.get("member_count")
    if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
        return "artifact member_count is not a positive integer: %r" % (count,)
    return ""


def check_identity(rec):
    two = rec.get("two_builds") or {}
    compared, same = two.get("files_compared"), two.get("identical")
    if not isinstance(compared, int) or compared != same or compared <= 0:
        return "two_builds files_compared %r identical %r" % (compared, same)
    smoke = rec.get("import_smoke") or []
    line = smoke[0] if smoke else ""
    if " fail=0 " not in line + " ":
        return "import smoke line is %r, want fail=0" % (line,)
    return ""


def main(argv):
    if not argv or argv[0].startswith("--"):
        print("usage: check_r34m_record.py <record.json> [--identity]")
        return 2
    identity = "--identity" in argv[1:]
    prefix = "R34N-IDENTITY-BAD" if identity else "R34N-RECORD-BAD"
    rec, err = load(argv[0])
    if rec is None:
        return bad(prefix, err)
    why = check_identity(rec) if identity else check_record(rec)
    if why:
        return bad(prefix, why)
    if identity:
        print("R34N-IDENTITY-OK builds_identical=yes smoke_fail=0")
    else:
        delta = rec["delta_vs_r34m"]
        print("R34N-RECORD-OK changed=%d added=%d removed=%d" % (len(delta["changed"]), len(delta["added"]), len(delta["removed"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
