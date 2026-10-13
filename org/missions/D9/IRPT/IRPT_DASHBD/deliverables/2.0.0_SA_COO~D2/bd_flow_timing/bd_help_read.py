"""READ-ONLY (Andrew-direct card 5, 2026-10-13): read Black Diamond's own help text on how external cash flows are timed in time-weighted return, using the stored signed-in
49F session (Secrets Manager blackdiamond/49f/session). GET only; the cookie jar never leaves this process; only cookies whose domain is .bdreporting.com are sent, and only to
*.bdreporting.com hosts. Modes (argv[1]):
  fetch <url>            print status, redirect chain hosts, title, and up to 25 link texts
  search <query>         try the docs host's search page and print result titles + URLs
  grep <url> <regex>     print the paragraphs/sentences of the page text that match the regex (vendor help text; no client data is on these pages)
"""
import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse, urljoin, quote

AWS = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() + "/.tools/aws"  # derived, not typed
UA = "Mozilla/5.0 (opal-agent read-only)"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def load_jar():
    out = subprocess.run(["bash", AWS, "secretsmanager", "get-secret-value", "--secret-id", "blackdiamond/49f/session", "--query", "SecretString", "--output", "text"],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        print("READ REFUSED")
        sys.exit(2)
    obj = json.loads(out.stdout.strip())
    return [c for c in (obj.get("all_cookies") or []) if isinstance(c, dict) and (c.get("domain") or "").startswith(".bdreporting.com")]


JAR = None


def cookie_for(host):
    if not host.endswith("bdreporting.com"):
        return ""
    return "; ".join("%s=%s" % (c["name"], c["value"]) for c in JAR)


def get(url, max_hops=8):
    hops = []
    opener = urllib.request.build_opener(NoRedirect)
    for _ in range(max_hops):
        host = urlparse(url).hostname or ""
        headers = {"User-Agent": UA, "Accept": "text/html"}
        ck = cookie_for(host)
        if ck:
            headers["Cookie"] = ck
        try:
            r = opener.open(urllib.request.Request(url, headers=headers), timeout=30)
            return r.status, url, hops, r.read(3_000_000).decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                nxt = urljoin(url, e.headers["Location"])
                hops.append(urlparse(url).netloc + urlparse(url).path)
                url = nxt
                continue
            return e.code, url, hops, ""
        except Exception as e:  # noqa: BLE001
            return -1, url, hops, str(e)[:120]
    return -2, url, hops, ""


def text_of(body):
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"(?s)<br\s*/?>|</p>|</li>|</h\d>|</tr>", "\n", body)
    return html.unescape(re.sub(r"<[^>]+>", " ", body))


def main():
    global JAR
    JAR = load_jar()
    mode = sys.argv[1]
    if mode == "fetch":
        st, final, hops, body = get(sys.argv[2])
        t = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
        print("GET %s -> %s final=%s hops=%s title=%r len=%d" % (sys.argv[2], st, urlparse(final).netloc + urlparse(final).path, hops, t.group(1).strip()[:90] if t else None, len(body)))
        seen = set()
        for h, txt in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', body, re.I | re.S):
            txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", txt)).strip()
            if txt and h not in seen and len(txt) < 100:
                seen.add(h)
                print("   %-60s %s" % (txt[:60], urljoin(final, h)[:110]))
                if len(seen) >= 25:
                    break
    elif mode == "search":
        base = sys.argv[3] if len(sys.argv) > 3 else "https://docs.bdreporting.com"
        for path in ("/search?query=%s", "/search?q=%s", "/collection?query=%s"):
            url = base + path % quote(sys.argv[2])
            st, final, hops, body = get(url)
            t = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
            print("GET %s -> %s final=%s title=%r len=%d" % (url, st, urlparse(final).netloc + urlparse(final).path, t.group(1).strip()[:80] if t else None, len(body)))
            if st == 200 and "SignIn" not in final:
                seen = set()
                for h, txt in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', body, re.I | re.S):
                    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", txt)).strip()
                    if txt and h not in seen and 8 < len(txt) < 140 and re.search(r"article|docs|collection", h, re.I):
                        seen.add(h)
                        print("   %-70s %s" % (txt[:70], urljoin(final, h)[:120]))
                        if len(seen) >= 20:
                            break
                break
    elif mode == "grep":
        st, final, hops, body = get(sys.argv[2])
        t = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
        print("GET %s -> %s final=%s title=%r" % (sys.argv[2], st, urlparse(final).netloc + urlparse(final).path, t.group(1).strip()[:90] if t else None))
        txt = re.sub(r"[ \t]+", " ", text_of(body))
        paras = [p.strip() for p in re.split(r"\n\s*\n|\n", txt) if p.strip()]
        n = 0
        for p in paras:
            if re.search(sys.argv[3], p, re.I):
                print("  >", p[:700])
                n += 1
                if n >= 12:
                    break
        print("matching paragraphs:", n, "of", len(paras))


main()
