#!/usr/bin/env python3
"""RT6 PACKAGER -- build irpt-directory-refresh's zip and PROVE it resolves a trading calendar.

WHY A PACKAGER AND NOT A COPY. `trading_calendar.py` is the estate's ONE frontier (CLAUDE.md) and
it lives at `lib/trading_calendar.py`. Copying it into `directory/` to make a flat build input
would be a SECOND DEFINITION of that frontier -- the same defect amendment H3 distinguished for
`ids.py`. Declaring it as a packaged member and RESOLVING IT FROM `lib/` at build time is a
DISTRIBUTION: one authority, and the zip carries a copy the way every zip does. This file is the
resolution step, and it prints where every member came from so a reader can see which is which.

WHAT IT PROVES, and the proof is not the hash. A zip whose bytes match is still a zip that may not
import: `resolve_calendar()` answers None on ImportError BY DESIGN and honestly, so a missing
calendar does not crash -- it silently turns the missed-trigger detector off (row W2-S48). The only
instrument that can see that is an EXTRACT-AND-IMPORT in the flat /var/task layout, in a fresh
interpreter, with the repo off sys.path, followed by actually CALLING the calendar rather than
merely importing it -- because expiry.py's own docstring warns that the import can succeed while
the first call fails.

NEGATIVE CONTROL, ALWAYS: the same build with trading_calendar.py withheld must report the
calendar UNRESOLVED. A probe that cannot return the failing case is a constant.

NO AWS CALL, NO UPLOAD, NO DEPLOY. Builds into .scratch/ and reads. ASCII only.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
OUT = os.path.join(REPO, ".scratch", "rt6-zips")
FUNCTION = "irpt-directory-refresh"

# The flat shared roots, IN ORDER, after the function's own source_dir. `lib` is here because the
# ONE trading-calendar frontier lives there and nowhere else.
SHARED_ROOTS = [
    os.path.join(REPO, "lib"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_authz"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_scope"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_keys"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_ids"),
]

ZIP_DATE = (2026, 9, 12, 0, 0, 0)

PROBE = (
    "import sys, os\n"
    "TASK = os.path.dirname(os.path.abspath(__file__))\n"
    "sys.path.insert(0, TASK)\n"
    "marks = [p for p in sys.path if 'investor-reporting' in p or 'wk-irpt' in p]\n"
    "assert not marks, 'the repository is on sys.path: %r' % marks\n"
    "import expiry\n"
    "cal = expiry.resolve_calendar()\n"
    "print('resolve_calendar ->', 'RESOLVED' if cal is not None else 'UNRESOLVED (None)')\n"
    "if cal is None:\n"
    "    print('CALENDAR-UNRESOLVED')\n"
    "else:\n"
    "    import datetime as dt\n"
    "    d = cal.expected_last_trading_day(dt.date(2026, 9, 12))\n"
    "    print('CALENDAR-OK expected_last_trading_day(2026-09-12) =', d)\n"
    "    print('  source:', getattr(cal, 'calendar_source', lambda: 'n/a')())\n"
    "import refresh\n"
    "print('refresh imported; put_manifest=%s last_manifest=%s'\n"
    "      % (hasattr(refresh, 'put_manifest'), hasattr(refresh, 'last_manifest')))\n"
)


def source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as fh:
        return json.load(fh)


def resolve(source_dir, name):
    p = os.path.join(source_dir, name.replace("/", os.sep))
    if os.path.isfile(p):
        return p, "source_dir"
    for root in SHARED_ROOTS:
        q = os.path.join(root, os.path.basename(name))
        if os.path.isfile(q):
            return q, os.path.relpath(root, REPO).replace(os.sep, "/")
    return None, None


def build(files, tag=""):
    sm = source_map()["functions"][FUNCTION]
    source_dir = os.path.join(REPO, sm["source_dir"].replace("/", os.sep))
    members, where, unresolved = {}, {}, []
    for name in files:
        path, origin = resolve(source_dir, name)
        if path is None:
            unresolved.append(name)
            continue
        members[name] = path
        where[name] = origin
    os.makedirs(OUT, exist_ok=True)
    zip_path = os.path.join(OUT, "%s%s.zip" % (FUNCTION, tag))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arc in sorted(members):
            info = zipfile.ZipInfo(arc, date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.create_system = 0
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(members[arc], "rb") as fh:
                zf.writestr(info, fh.read())
    with open(zip_path, "rb") as fh:
        sha = base64.b64encode(hashlib.sha256(fh.read()).digest()).decode("ascii")
    return zip_path, sha, members, where, unresolved


def probe(zip_path, label):
    tmp = tempfile.mkdtemp(prefix="rt6-import-")
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp)
        p = os.path.join(tmp, "_probe.py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(PROBE)
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        env.setdefault("IRPT_DIRECTORY_BUCKET_MAP", "{}")
        proc = subprocess.run([sys.executable, "-I", "_probe.py"], cwd=tmp, env=env,
                              capture_output=True, text=True, timeout=180)
        out = ((proc.stdout or "") + (proc.stderr or "")).strip()
        for line in out.splitlines():
            print("      %-14s %s" % (label, line[:130]))
        return "CALENDAR-OK" in out, out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("RT6 PACKAGER -- %s" % FUNCTION)
    print("repo: %s" % REPO)
    sm = source_map()["functions"][FUNCTION]
    files = sm.get("files") or []
    print("declared members: %d -- %s" % (len(files), ", ".join(files)))

    zip_path, sha, members, where, unresolved = build(files)
    print("resolved %d of %d:" % (len(members), len(files)))
    for name in sorted(members):
        print("    %-24s <- %s" % (name, where[name]))
    if unresolved:
        print("  UNRESOLVED (%d): %s" % (len(unresolved), ", ".join(unresolved)))
    print("zip: %s  sha256(b64)=%s" % (os.path.basename(zip_path), sha))

    print("  THE IMPORT-AND-CALL PROBE, flat layout, fresh interpreter, repo off sys.path:")
    ok, _out = probe(zip_path, "POSITIVE")

    # THE NEGATIVE CONTROL: withhold the calendar and the probe must say UNRESOLVED.
    neg_files = [f for f in files if f != "trading_calendar.py"]
    neg_path, _s, _m, _w, _u = build(neg_files, tag=".NEGATIVE-CONTROL")
    print("  NEGATIVE CONTROL -- the same build with trading_calendar.py withheld:")
    neg_ok, neg_out = probe(neg_path, "NEGATIVE-CTL")
    fires = (not neg_ok) and "CALENDAR-UNRESOLVED" in neg_out

    print("")
    print("=== SUMMARY ===============================================")
    print("  calendar RESOLVES in the flat layout : %s" % ok)
    print("  negative control FIRES               : %s" % fires)
    print("  sha256(b64)                          : %s" % sha)
    print("  %d of %d declared members resolved" % (len(members), len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
