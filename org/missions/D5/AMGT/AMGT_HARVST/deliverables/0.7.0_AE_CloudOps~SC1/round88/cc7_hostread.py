"""HVST-cc-7 host read, READ ONLY, run ON the opal-gateway instance (delivered by S3, pulled by SSM; Rule 12).

Prints ASCII lines: the unit state and MainPID, GET /health (status code only), a digest over /opt/opal-gateway/app (every
file's relative path and md5, __pycache__ excluded), the md5 of five named files, and the SERVED tool registry (app.server
imported, mcp._tool_manager.list_tools()): count, md5 of the sorted names, and the names. Writes nothing, restarts nothing,
prints no secret (only BIND_PORT is read from .env).
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import urllib.request

ROOT = "/opt/opal-gateway"
NAMED = ("app/server.py", "app/harvest_figures.py", "app/harvest_research.py", "app/harvest_identity.py", "app/config.py")


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sh(*cmd):
    return subprocess.run(list(cmd), capture_output=True, text=True).stdout.strip()


def main():
    print("HOSTREAD begin %s" % sh("date", "-u", "+%Y-%m-%dT%H:%M:%SZ"))
    print("UNIT %s" % sh("systemctl", "show", "opal-gateway.service", "-p", "ActiveState", "-p", "SubState", "-p", "MainPID", "-p", "ActiveEnterTimestamp").replace("\n", " | "))
    port = "8080"
    try:
        for line in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
            if line.startswith("BIND_PORT="):
                port = line.strip().split("=", 1)[1]
    except OSError:
        pass
    try:
        with urllib.request.urlopen("http://localhost:%s/health" % port, timeout=10) as r:
            print("HEALTH port=%s status=%s" % (port, r.status))
    except Exception as exc:  # noqa: BLE001
        print("HEALTH port=%s error=%r" % (port, exc))
    rows = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "app")):
        dn[:] = sorted(d for d in dn if d != "__pycache__")
        for f in sorted(fn):
            if f.endswith(".pyc"):
                continue
            p = os.path.join(dp, f)
            rows.append("%s %s" % (os.path.relpath(p, ROOT).replace(os.sep, "/"), md5_of(p)))
    rows.sort()
    print("APPTREE files=%d digest=%s" % (len(rows), hashlib.md5("\n".join(rows).encode("ascii")).hexdigest()))
    print("APPROWS " + ";".join(rows))
    for n in NAMED:
        p = os.path.join(ROOT, n)
        print("NAMED %s %s" % (n, md5_of(p) if os.path.exists(p) else "ABSENT"))
    os.chdir(ROOT)
    sys.path.insert(0, ROOT)
    try:
        from app import server
        names = sorted(t.name for t in server.mcp._tool_manager.list_tools())
        print("TOOLS count=%d names_md5=%s" % (len(names), hashlib.md5("\n".join(names).encode("ascii")).hexdigest()))
        print("TOOLNAMES " + " ".join(names))
    except Exception as exc:  # noqa: BLE001
        print("TOOLS error=%r" % (exc,))
    print("HOSTREAD end")


if __name__ == "__main__":
    main()
