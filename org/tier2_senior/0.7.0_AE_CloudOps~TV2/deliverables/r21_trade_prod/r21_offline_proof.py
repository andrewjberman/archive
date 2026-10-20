"""TCKT_VNEXT TO-R21-RB1 start gate item 5: the OFFLINE PROOF, writing NOTHING (0.7.0_AE_CloudOps~TV2).

(1) the run script's body parser against a local stub of the Open body shape {expires_in, filename, url} and the four earlier shapes: each must read or
    refuse as designed, and a body with no url must refuse;
(2) a read-only GET of ONE existing residue object at its recorded version, under this seat's own read rights, returns the known file's SHA-256;
(3) the response waiter is registered BEFORE the Open press: the order of the two lines in the script is printed, and a stubbed page (a local http server,
    the page's button fetches a stub route that answers at once) is driven through the script's own open_and_capture(); an early response is still captured.
The only I/O is a local server on 127.0.0.1, a headless browser, and one s3:GetObject. Nothing is created, written or deleted anywhere.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

os.environ.setdefault("R20T_HEAD", "offline-proof-no-head")
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r21", str(HERE / "r21_trade_prod.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

U = "https://opal-data-cottonwood.s3.amazonaws.com/portal/cottonwood/state/ticket_attachments/trade-form/k/f.csv?X-Amz-Signature=STUB"
SHAPES = {
    "R21 shape {expires_in, filename, url}": ({"expires_in": 300, "filename": "f.csv", "url": U}, True),
    "earlier: data.url": ({"data": {"url": U, "filename": "f.csv", "expires_in": 300}}, True),
    "earlier: attachment.url": ({"attachment": {"url": U}}, True),
    "earlier: items[].download_url": ({"items": [{"download_url": U}]}, True),
    "no url": ({"ok": True, "filename": "f.csv"}, False),
    "non-S3 url": ({"url": "https://evil.example.com/x"}, False),
    "url of another bucket": ({"url": "https://opal-data-other.s3.amazonaws.com/portal/other/state/ticket_attachments/trade-form/k"}, False),
}


def part1():
    ok = True
    for name, (body, should_read) in SHAPES.items():
        url = m.find_url(body)
        reads = bool(url) and m.s3_ok(urlparse(url))
        good = reads == should_read
        ok = ok and good
        print("  %-38s key names %-48s -> %s (expected %s) %s" % (name, m.key_set(body), "READ" if reads else "REFUSED", "READ" if should_read else "REFUSED", "OK" if good else "FAIL"))
    return ok


def part2():
    import boto3
    known = hashlib.sha256(b"symbol,qty,px\r\nSYN1,100,12.34\r\n").hexdigest()
    key = "portal/cottonwood/state/ticket_attachments/trade-form/8b46f05593e643f0bb229023841d2a4a/tckt-r20-trade-synthetic.csv"
    ver = "U2wA9rMN_iqdUnci740XcsAfyvgsTK3h"
    body = boto3.client("s3", region_name="us-east-1").get_object(Bucket="opal-data-cottonwood", Key=key, VersionId=ver)["Body"].read()
    got = hashlib.sha256(body).hexdigest()
    print("  residue GET (own read rights, version %s...): %d bytes, sha256 %s; known file sha256 %s; equal=%s" % (ver[:8], len(body), got, known, got == known))
    return got == known


PAGE = b"""<!doctype html><html><body><button id="o" data-slot="stub-open">Open form</button><script>
document.getElementById('o').addEventListener('click', function(){ fetch('/api/scoped/tickets/TCK-STUB/attachment'); });
</script></body></html>"""
BODY = json.dumps({"expires_in": 300, "filename": "f.csv", "url": U}).encode()


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/attachment"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(BODY)))
            self.end_headers()
            self.wfile.write(BODY)   # answers at once, no delay
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(PAGE)))
            self.end_headers()
            self.wfile.write(PAGE)

    def log_message(self, *a):
        pass


def part3():
    src = (HERE / "r21_trade_prod.py").read_text(encoding="utf-8").splitlines()
    fn_start = next(i for i, ln in enumerate(src) if ln.startswith("def open_and_capture"))
    exp = next(i for i in range(fn_start, len(src)) if "page.expect_response(" in src[i])
    clk = next(i for i in range(fn_start, len(src)) if "click_locator.click()" in src[i])
    call = next(i for i, ln in enumerate(src) if "open_and_capture(pg, openbtn)" in ln)
    print("  script line order: line %d `%s`  <  line %d `%s`" % (exp + 1, src[exp].strip()[:60], clk + 1, src[clk].strip()))
    print("  the run's call site is line %d `%s`" % (call + 1, src[call].strip()[:60]))
    order_ok = exp < clk
    srv = HTTPServer(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    from playwright.sync_api import sync_playwright
    captured = None
    try:
        with sync_playwright() as pw:
            try:
                br = pw.chromium.launch(channel="msedge", headless=True)
            except Exception:  # noqa: BLE001
                br = pw.chromium.launch(headless=True)
            pg = br.new_page()
            pg.goto("http://127.0.0.1:%d/" % port)
            status, names, url = m.open_and_capture(pg, pg.locator("#o"))
            captured = (status, names, bool(url) and m.s3_ok(urlparse(url)))
            br.close()
    finally:
        srv.shutdown()
    print("  stubbed page, the stub route answers at once: captured status %s, key names %s, url read=%s" % captured)
    stub_ok = captured is not None and captured[0] == 200 and captured[1] == ["expires_in", "filename", "url"] and captured[2]
    return order_ok and stub_ok


if __name__ == "__main__":
    print("PART 1 -- the parser against stubbed Open body shapes")
    a = part1()
    print("PART 2 -- one read-only GET of an existing residue object at its version")
    b = part2()
    print("PART 3 -- the response waiter registered BEFORE the Open press")
    c = part3()
    print("OFFLINE-PROOF %s (parser=%s residue_get=%s listener_before_press=%s); nothing was written" % ("OK" if (a and b and c) else "FAIL", a, b, c))
    raise SystemExit(0 if (a and b and c) else 1)
