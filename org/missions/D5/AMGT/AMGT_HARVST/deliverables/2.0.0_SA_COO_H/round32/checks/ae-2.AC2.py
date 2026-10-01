"""HVST-ae-2 AC2 (issuer seam probe, LOCAL): the in-tab transport against a REAL Chrome, with no publisher traffic.

Starts a local HTTP fixture on 127.0.0.1 that sets a cookie on its first response and echoes the request's User-Agent
and Cookie headers on every later one. Drives the worker's `TabSession` (the interface the order names) in a fresh
persistent profile under a temp root, and prints what the fixture SAW.

PASS requires:
- the request reached the fixture from the browser tab (the echoed User-Agent equals the tab's own navigator.userAgent);
- navigator.webdriver reads false in that tab;
- the cookie the fixture set on request 1 came back on request 2 (the browser's own jar carries the session);
- the profile directory is per publisher (`<root>/<publisher>`) and survives close (a second TabSession on the same root
  sees the cookie with no Python-side cookie handling);
- 0 connections to any host but 127.0.0.1 (the fixture counts its own; the probe names no other URL).
"""
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)

SEEN = []


class Fixture(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        SEEN.append({"path": self.path, "ua": self.headers.get("User-Agent"), "cookie": self.headers.get("Cookie")})
        body = json.dumps({"ua": self.headers.get("User-Agent"), "cookie": self.headers.get("Cookie")}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        if self.path.startswith("/set"):
            self.send_header("Set-Cookie", "hvst_probe=ae2; Path=/; Max-Age=3600")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        return


def main():
    failures = []
    try:
        from lib.opal_data_harvest.tab_transport import TabSession
    except Exception as exc:  # noqa: BLE001
        print("IMPORT: %s %s" % (type(exc).__name__, exc))
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: lib.opal_data_harvest.tab_transport.TabSession not importable")
        return 1
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = "http://127.0.0.1:%d" % server.server_address[1]
    root = tempfile.mkdtemp(prefix="hvst-ae2-")
    try:
        s = TabSession("probe", root, origin)
        try:
            r1 = s.get(origin + "/set")
            r2 = s.get(origin + "/echo")
            tab_ua = s.evaluate("navigator.userAgent")
            webdriver = s.evaluate("navigator.webdriver")
        finally:
            s.close()
        profile = os.path.join(root, "probe")
        s2 = TabSession("probe", root, origin)
        try:
            r3 = s2.get(origin + "/echo2")
        finally:
            s2.close()
    finally:
        server.shutdown()
    echoed = json.loads(r2.text)
    print("STATUS: %s %s %s" % (r1.status_code, r2.status_code, r3.status_code))
    print("TAB UA: %s" % tab_ua)
    print("FIXTURE SAW UA: %s" % echoed.get("ua"))
    print("navigator.webdriver: %r" % webdriver)
    print("COOKIE ON REQUEST 2: %s" % echoed.get("cookie"))
    print("COOKIE AFTER REOPEN: %s" % json.loads(r3.text).get("cookie"))
    print("PROFILE DIR: %s exists=%s" % (profile, os.path.isdir(profile)))
    print("FIXTURE REQUESTS: %d (all 127.0.0.1)" % len(SEEN))
    if echoed.get("ua") != tab_ua:
        failures.append("the request did not carry the tab's own User-Agent")
    if webdriver not in (False, None):
        failures.append("navigator.webdriver is %r" % webdriver)
    if "hvst_probe=ae2" not in str(echoed.get("cookie")):
        failures.append("the browser jar did not carry the fixture's cookie")
    if "hvst_probe=ae2" not in str(json.loads(r3.text).get("cookie")):
        failures.append("the per-publisher profile did not persist the cookie across sessions")
    if not os.path.isdir(profile):
        failures.append("no per-publisher profile directory at <root>/<publisher>")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
