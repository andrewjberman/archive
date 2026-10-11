"""pytest plugin for the IB-pr-426 replay.

(1) Refuse every network connect and every name resolution but localhost (the offline guarantee); the number refused is printed
    as OFFLINE-GUARD-ATTEMPTS=<n> at session end.
(2) Record which of the named CALL SITES the run executed (sys.monitoring LINE events). Env SITES_OUT=<json path> and
    SITES=<file.py>::<source substring or @line>;;<file.py>::... name the sites.
ASCII only.
"""
import json
import linecache
import os
import socket
import sys

ATTEMPTS = []


def _refuse(self, *a, **k):
    ATTEMPTS.append(str(a)[:80])
    raise OSError("OFFLINE-GUARD: network connect refused")


socket.socket.connect = _refuse
socket.socket.connect_ex = _refuse
socket.create_connection = lambda *a, **k: (_ for _ in ()).throw(OSError("OFFLINE-GUARD"))
_real_getaddrinfo = socket.getaddrinfo


def _no_dns(host, *a, **k):
    if host in (None, "localhost", "127.0.0.1", "::1", ""):
        return _real_getaddrinfo(host, *a, **k)
    ATTEMPTS.append("dns")
    raise OSError("OFFLINE-GUARD: name resolution refused")


socket.getaddrinfo = _no_dns

SITES = [tuple(s.split("::", 1)) for s in os.environ.get("SITES", "").split(";;") if s]
HITS = {s: 0 for s in SITES}
if SITES:
    mon = sys.monitoring
    TOOL = mon.PROFILER_ID
    mon.use_tool_id(TOOL, "sites426")

    def on_line(code, line):
        fn = os.path.basename(code.co_filename)
        mine = [s for s in SITES if s[0] == fn]
        if not mine:
            return mon.DISABLE
        text = linecache.getline(code.co_filename, line)
        hit = False
        for s in mine:
            if (s[1].startswith("@") and str(line) == s[1][1:]) or (not s[1].startswith("@") and s[1] in text):
                HITS[s] += 1
                hit = True
        return None if hit else mon.DISABLE

    mon.register_callback(TOOL, mon.events.LINE, on_line)
    mon.set_events(TOOL, mon.events.LINE)


def pytest_sessionfinish(session, exitstatus):
    print("OFFLINE-GUARD-ATTEMPTS=%d" % len(ATTEMPTS))
    if SITES and os.environ.get("SITES_OUT"):
        with open(os.environ["SITES_OUT"], "w", encoding="utf-8") as fh:
            json.dump({"%s::%s" % k: v for k, v in HITS.items()}, fh, indent=1)
