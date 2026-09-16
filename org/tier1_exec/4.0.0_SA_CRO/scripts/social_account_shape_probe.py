"""
Shape probe for social_account: read the company's OWN site (the ir_domain we
already hold) and extract the social links it publishes.

WHY NOT SERP. Bright Data's search_engine returns Google redirect stubs with no
host (plan s.16), which is exactly what made it useless for the blog half. A
social handle IS a URL, so a stub carries none of the information needed.

WHY THIS IS STRONGER EVIDENCE ANYWAY. A handle linked FROM the company's own
domain is published by the company about itself -- the same domain-equality
identity constraint the blog rule uses, and far better than any search ranking.
"""
import json
import os
import re
import urllib.request

cfg = os.path.join(os.path.expanduser("~"), ".claude.json")
tok = json.load(open(cfg, encoding="utf-8"))["mcpServers"]["brightdata"]["url"].split("token=")[1]
EP = "https://mcp.brightdata.com/mcp?token=" + tok

PLATFORMS = {
    "x.com": "x", "twitter.com": "x", "linkedin.com": "linkedin",
    "facebook.com": "facebook", "instagram.com": "instagram",
    "youtube.com": "youtube", "tiktok.com": "tiktok", "weibo.com": "weibo",
}


def rpc(p, sid=None):
    h = {"Content-Type": "application/json",
         "Accept": "application/json, text/event-stream"}
    if sid:
        h["mcp-session-id"] = sid
    req = urllib.request.Request(EP, data=json.dumps(p).encode(),
                                 method="POST", headers=h)
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = r.read().decode("utf-8", "replace")
        return ([json.loads(ln[5:].strip()) for ln in raw.splitlines()
                 if ln.startswith("data:")] or [None])[0], r.headers.get("mcp-session-id")


_, SID = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
              "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                         "clientInfo": {"name": "opal-cro", "version": "1.0"}}})
rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, SID)

_id = [1]


def scrape(url):
    _id[0] += 1
    res, _ = rpc({"jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
                  "params": {"name": "scrape_as_markdown",
                             "arguments": {"url": url}}}, SID)
    t = "".join(c.get("text", "") for c in res["result"]["content"])
    return t.split("_BEGIN=====", 1)[-1].split("=====UNTRUSTED", 1)[0].strip()


for folder, domain in [("AstraZeneca AZN", "astrazeneca.com"),
                       ("Adobe ADBE US", "adobe.com"),
                       ("NEG CONTROL", "opal-no-such-host-xyz.com")]:
    body = scrape("https://www." + domain + "/")
    found = {}
    for m in re.finditer(r"https?://(?:www\.)?([a-z0-9.-]+)/([^)\s\"'>]+)", body, re.I):
        host, path = m.group(1).lower(), m.group(2)
        plat = PLATFORMS.get(host)
        if not plat:
            continue
        handle = path.split("?")[0].strip("/")
        if plat == "linkedin" and not handle.startswith("company/"):
            continue
        if handle and len(handle) < 60:
            found.setdefault(plat, set()).add(handle)
    print("%-18s %-24s body=%-7d platforms=%d"
          % (folder[:18], domain, len(body), len(found)))
    for plat in sorted(found):
        vals = sorted(found[plat])[:3]
        print("    %-10s %s" % (plat, ", ".join(vals)))
    if not found and body:
        print("    (no social links on the root page -- a footer may be "
              "client-rendered; that is a finding, not a gap)")
