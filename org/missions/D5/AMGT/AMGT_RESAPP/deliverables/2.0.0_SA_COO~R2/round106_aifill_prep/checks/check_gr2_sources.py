"""check_gr2_sources.py -- acceptance arms for AMGT-gr-2 (fetch a cited source and say what happened to it).

  PYTHONPATH=<repo root> python check_gr2_sources.py
Offline: every fetch goes through a stub transport. Imports lib.research.aifill.sources (new). The ruling (CTO, round-105 grounding pass): a citation that does not answer (404,
refused) grounds nothing; the CVO measured 78 web citations: 47 answered 200, 26 refused a script (403, paywall or bot wall), 2 were 404, 1 a TLS error, and 5 of the answers were PDFs.
"""
from __future__ import annotations

import os
import socket
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

PARA = "ASML named Roger Dassen chief financial officer in 2013 and he has led the finance function since then, through three product cycles and the 2018 Cymer integration. "
ARTICLE = "<html><head><title>  ASML   leadership \n page </title><style>.x{color:red}</style><script>var secret='SCRIPTSENTINEL';</script></head><body><nav>Home About</nav>" + \
          "".join("<p>%s Item %d &amp; more &#8212; done.</p>" % (PARA, i) for i in range(4)) + "<footer>Subscribe to our newsletter</footer></body></html>"


class Tr:
    def __init__(self, status=200, ctype="text/html; charset=utf-8", body=b"", exc=None):
        self.status, self.ctype, self.body, self.exc, self.calls = status, ctype, body, exc, []

    def __call__(self, url, headers, timeout):
        self.calls.append((url, dict(headers), timeout))
        if self.exc:
            raise self.exc
        return self.status, self.ctype, self.body


def main():
    from lib.research.aifill import sources as S

    arms = L.Arms("GR-2")
    fetch = S.fetch_source

    def ok_html():
        t = Tr(200, body=ARTICLE.encode("utf-8"))
        r = fetch("https://example.com/a", transport=t)
        return (r["status"] == "OK" and r["http_status"] == 200 and r["title"] == "ASML leadership page" and "Roger Dassen" in r["text"] and "SCRIPTSENTINEL" not in r["text"]
                and "color:red" not in r["text"] and "&amp;" not in r["text"] and "Item 2 & more" in r["text"] and r["chars"] == len(r["text"]) and r["url"] == "https://example.com/a"), {k: r[k] for k in ("status", "title", "chars")}
    arms.run("an answering page: OK, title cleaned, scripts and styles gone, entities decoded", ok_html)

    def http_arm(code, want):
        r = fetch("https://example.com/x", transport=Tr(code, body=b"<html>nope</html>"))
        return r["status"] == want and r["http_status"] == code and r["text"] == "", r["status"]

    for code, want in ((403, "REFUSED"), (401, "REFUSED"), (429, "REFUSED"), (404, "NOT_FOUND"), (410, "NOT_FOUND"), (500, "ERROR"), (301, "ERROR")):
        arms.run("HTTP %d -> %s, no text" % (code, want), lambda code=code, want=want: http_arm(code, want))

    def raising():
        for exc in (socket.timeout("timed out"), ConnectionError("reset"), ValueError("bad"), OSError("tls")):
            r = fetch("https://example.com/x", transport=Tr(exc=exc))
            if r["status"] != "ERROR" or type(exc).__name__ not in (r.get("note") or "") or r["http_status"] is not None:
                return False, (type(exc).__name__, r)
        return True, "four exceptions, none raised"
    arms.run("a transport that raises -> ERROR naming the exception class, never raises", raising)

    def pdf():
        a = fetch("https://example.com/r.pdf", transport=Tr(200, "application/pdf", b"%PDF-1.7 stuff"))
        b = fetch("https://example.com/r", transport=Tr(200, "text/html", b"%PDF-1.4 sneaky"))
        return a["status"] == "UNSUPPORTED" and b["status"] == "UNSUPPORTED" and a["text"] == "", (a["status"], b["status"])
    arms.run("a PDF (by type or by magic bytes) -> UNSUPPORTED", pdf)

    arms.run("a nearly empty page -> EMPTY", lambda: (fetch("https://example.com/e", transport=Tr(200, body=b"<html><body><p>Loading...</p></body></html>"))["status"] == "EMPTY", "ok"))

    def paywall():
        short = b"<html><head><title>Sub</title></head><body><p>To continue reading, please subscribe or sign in to your account to get unlimited access to every story and the full archive of this publication, plus newsletters and more perks every day of the week.</p></body></html>"
        r1 = fetch("https://example.com/p", transport=Tr(200, body=short))
        r2 = fetch("https://example.com/q", transport=Tr(200, body=b"<html><body><p>Just a moment... Verify you are human by completing the action below to proceed to the website. Cloudflare Ray ID and more words to pass the empty check easily here ok.</p></body></html>"))
        r3 = fetch("https://example.com/a", transport=Tr(200, body=ARTICLE.encode("utf-8")))
        return r1["status"] == "PAYWALL" and r2["status"] == "PAYWALL" and r3["status"] == "OK", (r1["status"], r2["status"], r3["status"])
    arms.run("a short page that asks to subscribe or verify -> PAYWALL; a long article with a footer 'Subscribe' stays OK", paywall)

    def bad_urls():
        t = Tr(200, body=ARTICLE.encode("utf-8"))
        got = [fetch(u, transport=t)["status"] for u in ("ftp://example.com/x", "javascript:alert(1)", "", "example.com/no-scheme", None)]
        return got == ["ERROR"] * 5 and t.calls == [], got
    arms.run("a non-http(s) url -> ERROR with no transport call", bad_urls)

    def headers():
        t = Tr(200, body=ARTICLE.encode("utf-8"))
        fetch("https://example.com/a", transport=t)
        url, hdr, timeout = t.calls[0]
        return len(t.calls) == 1 and "Opal" in hdr.get("User-Agent", "") and 0 < timeout <= 30 and "text/html" in hdr.get("Accept", ""), (hdr, timeout)
    arms.run("one transport call; a declared Opal user agent; a bounded timeout", headers)

    def trunc():
        big = ("<html><body>" + "".join("<p>%s</p>" % (PARA * 3) for _ in range(200)) + "</body></html>").encode("utf-8")
        r = fetch("https://example.com/big", transport=Tr(200, body=big), max_chars=5000)
        return r["status"] == "OK" and len(r["text"]) <= 5000 and r["chars"] == len(r["text"]), (r["status"], r["chars"])
    arms.run("max_chars bounds the text; chars equals its length", trunc)

    def charset():
        latin = "<html><head><meta charset='iso-8859-1'><title>Caf\xe9</title></head><body><p>" + ("Nestl\xe9 named a new chief executive officer today. " * 8) + "</p></body></html>"
        r = fetch("https://example.com/l", transport=Tr(200, "text/html; charset=iso-8859-1", latin.encode("latin-1")))
        junk = fetch("https://example.com/j", transport=Tr(200, "text/html", b"<html><body><p>" + bytes(range(128, 256)) * 3 + b"</p><div" + b" unclosed " * 40))
        return r["status"] == "OK" and "Nestl\xe9" in r["text"] and junk["status"] in ("OK", "EMPTY", "ERROR"), (r["status"], junk["status"])
    arms.run("a latin-1 page decodes; malformed bytes and tags never raise", charset)

    def titles():
        bad = ["Free Trial", "Subscribe to read", "Sign in", "Log in to continue", "Just a moment...", "Access Denied", "Attention Required! | Cloudflare", "404 Not Found", "Page not found", "Subscription required"]
        good = ["ASML names new chief financial officer", "Annual Report 2025", "Nestle - Board of Directors", "Quarterly results", ""]
        wrong = [t for t in bad if not S.is_paywall_title(t)] + [t for t in good if S.is_paywall_title(t)]
        return not wrong and S.is_paywall_title(None) is False, wrong
    arms.run("is_paywall_title: the CVO's 'Free Trial' and its kin, and no real headline", titles)

    def windows():
        para = lambda i: "Paragraph %d about unrelated shipping logistics and nothing else of interest to anyone." % i  # noqa: E731
        text = "\n".join([para(i) for i in range(40)] + ["Pablo Isla became chairman of Nestle in October 2025 after Paul Bulcke stepped down earlier than planned."] + [para(i) for i in range(40, 80)])
        short = S.select_windows("A short text.", ["anything"], 1000)
        got = S.select_windows(text, ["Pablo Isla chairman Nestle October 2025"], 600)
        return short == "A short text." and len(got) <= 600 and "Pablo Isla became chairman" in got, (len(got), got[:60])
    arms.run("select_windows keeps the paragraphs that mention the claim, within the bound", windows)

    def order():
        text = "\n".join(["alpha beta gamma delta epsilon first paragraph here", "unrelated filler text number one", "alpha beta gamma delta epsilon second paragraph here"] * 1 + ["filler two"] * 30)
        got = S.select_windows(text, ["alpha beta gamma delta epsilon"], 130)
        return got.index("first paragraph") < got.index("second paragraph"), got
    arms.run("select_windows preserves the order of the paragraphs it keeps", order)

    arms.run("default_transport exists and is callable (not called here)", lambda: (callable(S.default_transport), "ok"))

    def src_check():
        src = open(S.__file__, "rb").read()
        return src.isascii() and b"import anthropic" not in src and b"import boto3" not in src and b"import requests" not in src, "non-ASCII or a forbidden import"
    arms.run("the module is ASCII; no anthropic, boto3 or requests import", src_check)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
