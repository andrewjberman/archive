"""Serve the locally built rivalfunds page the way the gateway does, for a look before anything deploys.

    python serve_local.py <page dir: .../platinum/page/date=<D>> [port]

Routes (the gateway's shape, read from rivalfunds_view.py): /rivalfunds/<D> -> index.html; /rivalfunds/<D>/audit ->
audit.html; /rivalfunds/<D>/chart/<FUND> -> charts/<FUND>.json. Binds 127.0.0.1 only; reads local files only.
"""
import http.server
import pathlib
import re
import sys

PAGE = pathlib.Path(sys.argv[1]).resolve()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
DAY = re.search(r"date=(\d{4}-\d{2}-\d{2})", str(PAGE)).group(1)


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p = self.path.split("?")[0].rstrip("/")
        m = re.fullmatch(rf"/rivalfunds/{DAY}/chart/([A-Z0-9]{{1,8}})", p)
        if p in ("", "/rivalfunds", f"/rivalfunds/{DAY}"):
            f, ct = PAGE / "index.html", "text/html; charset=utf-8"
        elif p == f"/rivalfunds/{DAY}/audit":
            f, ct = PAGE / "audit.html", "text/html; charset=utf-8"
        elif m:
            f, ct = PAGE / "charts" / f"{m.group(1)}.json", "application/json"
        else:
            f, ct = None, None
        if not f or not f.exists():
            self.send_response(404)
            self.end_headers()
            return
        b = f.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass


print(f"serving {PAGE} at http://127.0.0.1:{PORT}/rivalfunds/{DAY}", flush=True)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
