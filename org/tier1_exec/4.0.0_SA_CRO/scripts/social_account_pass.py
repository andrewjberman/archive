#!/usr/bin/env python
"""
social_account_pass.py -- resolve social_account for the AMGT_RESAPP universe by
reading each company's OWN SITE, using the ir_domain already held.

AUTHORITY: Andrew's Bright Data grant. Read-only, SEARCH/FETCH only, no landing.

WHY THE COMPANY'S OWN SITE AND NOT SERP (plan s.16/s.20). Bright Data's
search_engine returns Google redirect stubs with NO HOST. A social handle IS a
URL, so a stub carries none of the information this key needs -- the blog half
died on exactly this. Reading the company's own domain is also STRONGER evidence
than any search ranking: a handle linked from the company's own site is published
by the company about itself.

THE EVIDENCE MODEL, stated honestly rather than dressed as two tests.
    PRIMARY   the link was found on the registrable domain already resolved as
              this company's ir_domain. This is STRUCTURAL -- true by
              construction for every link collected -- so it is the COLLECTION
              METHOD, not a discriminating test, and it is not claimed as one.
    FLAG      the handle text carries a distinctive token of the company name.
              RECORDED, NEVER REQUIRED: a legitimate handle need not contain the
              name ('nestle_global' does, 'ThisIsCostco' does not). Records where
              it fails are marked so a reviewer can look, which is the whole
              value of a flag that is not a gate.

THE MEASURED LIMIT, from the shape probe (s.20 + the fallback probe):
    astrazeneca.com  5 platforms     costco.com  3 platforms     adobe.com  0
    Adobe's root carries no social links AND NO NAV PATHS TO FOLLOW -- the whole
    navigation is client-rendered, so a fallback page has nothing to follow. That
    miss is STRUCTURAL and NAMED, not random: this pass cannot see a
    client-rendered footer, and says so per record instead of implying absence.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir_domain_bulk_pass import name_tokens  # noqa: E402  -- one token rule

IR_PASS = os.path.join("org", "tier1_exec", "4.0.0_SA_CRO", "deliverables",
                       "IDENTITY_IR_DOMAIN_PASS_20260913_Z.json")

PLATFORMS = {
    "x.com": "x", "twitter.com": "x", "linkedin.com": "linkedin",
    "facebook.com": "facebook", "instagram.com": "instagram",
    "youtube.com": "youtube", "tiktok.com": "tiktok", "weibo.com": "weibo",
}
# Share widgets and platform chrome. A "tweet this" button is a link to the
# PLATFORM, never to the company's account, and it appears on most corporate
# pages -- so without this the most common capture would be noise.
NOT_AN_ACCOUNT = re.compile(
    r"^(share|sharer|intent|home|hashtag|search|login|signup|privacy|tos|"
    r"terms|help|about$|watch|results|feed|explore|dialog|playlist)", re.I)
# A BARE NUMERIC IS A PLATFORM ID, NOT AN ACCOUNT NAME. Found by inspecting
# the flagged records rather than the count: Celsius captured "2471716".
# It cannot be corroborated against a company name by anyone, ever.
BARE_NUMERIC = re.compile(r"^\d+$")


def cfg_token():
    p = os.path.join(os.path.expanduser("~"), ".claude.json")
    return json.load(open(p, encoding="utf-8"))["mcpServers"]["brightdata"]["url"].split("token=")[1]


EP = None
SID = None
_id = [1]


def rpc(payload, sid=None):
    h = {"Content-Type": "application/json",
         "Accept": "application/json, text/event-stream"}
    if sid:
        h["mcp-session-id"] = sid
    req = urllib.request.Request(EP, data=json.dumps(payload).encode(),
                                 method="POST", headers=h)
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = r.read().decode("utf-8", "replace")
        return ([json.loads(ln[5:].strip()) for ln in raw.splitlines()
                 if ln.startswith("data:")] or [None])[0], r.headers.get("mcp-session-id")


MIN_PAGE_BYTES = 400   # below this there is no page to have failed to find
                       # links in -- Copa returned 52 bytes and was booked
                       # as "no social links", which reads as an absence.


def scrape(url, retry=True):
    """
    Returns the untrusted body, or None for "nothing usable arrived".

    RETRIES ONCE. A transient failure and a dead host are byte-identical on
    this tool, and six major companies (Netflix, Spotify, Unilever, KPN,
    Nubank, CCB) came back empty on the first full run -- every one of them
    certainly publishes social accounts. The estate banked "retry once
    before recording an absence" earlier the same session, on this exact
    tool, and this pass shipped without it.
    """
    _id[0] += 1
    try:
        res, _ = rpc({"jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
                      "params": {"name": "scrape_as_markdown",
                                 "arguments": {"url": url}}}, SID)
    except Exception:
        return None                      # transport failure, distinct from empty
    r = res.get("result", {}) if res else {}
    t = "".join(c.get("text", "") for c in r.get("content", []))
    body = t.split("_BEGIN=====", 1)[-1].split("=====UNTRUSTED", 1)[0].strip()
    if len(body) < MIN_PAGE_BYTES and retry:
        time.sleep(2)
        return scrape(url, retry=False)
    return body if len(body) >= MIN_PAGE_BYTES else None


def extract(body: str) -> dict:
    found = {}
    for m in re.finditer(r"https?://(?:www\.)?([a-z0-9.-]+)/([^)\s\"'>]+)",
                         body, re.I):
        plat = PLATFORMS.get(m.group(1).lower())
        if not plat:
            continue
        handle = m.group(2).split("?")[0].split("#")[0].strip("/")
        if plat == "linkedin":
            if not handle.startswith("company/"):
                continue
            handle = handle[len("company/"):]
        if not handle or len(handle) > 60 or NOT_AN_ACCOUNT.match(handle):
            continue
        if BARE_NUMERIC.match(handle):
            continue
        found.setdefault(plat, set()).add(handle)
    return {k: sorted(v)[:3] for k, v in found.items()}


def main() -> int:
    global EP, SID
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--exclude-done", default="",
                    help="path to a prior output JSON; folders it RESOLVED are "
                         "carried forward and not re-fetched. Folders it left "
                         "UNRESOLVED are retried, because an instrument limit "
                         "is not an answer. Carried from the sibling passes on "
                         "purpose -- this is the fifth time in one session that "
                         "a guard existed in one pass and not its neighbour.")
    ap.add_argument("--out", default="")
    ap.add_argument("--sleep", type=float, default=0.3)
    args = ap.parse_args()

    ir = json.load(open(IR_PASS, encoding="utf-8"))
    held = [(r["folder"], r["company_name"], r["ir_domain"]["value"])
            for r in ir["records"] if r["ir_domain"]["value"]]
    total = len(ir["records"])

    carried = []
    if args.exclude_done:
        prior = json.load(open(args.exclude_done, encoding="utf-8"))
        done = {r["folder"] for r in prior["records"]
                if r["social_account"]["status"] == "INFERRED"}
        carried = [r for r in prior["records"] if r["folder"] in done]
        retry_n = len(prior["records"]) - len(done)
        held = [h for h in held if h[0] not in done]
        print("CARRIED        %d already-RESOLVED folder(s), not re-fetched" % len(done))
        print("RETRIED        %d folder(s) the instrument could not read -- a "
              "limit is not an answer" % retry_n)

    targets = held[:args.limit] if args.limit else held

    print("SOURCE         %s" % IR_PASS)
    print("DENOMINATOR    %d universe | %d with a held ir_domain | %d this batch"
          % (total, len(held), len(targets)))
    print("               A name with NO ir_domain cannot be read here at all.")
    if args.dry_run:
        print("MODE           DRY RUN -- zero calls\n")
        for folder, nm, dom in targets:
            print("  %-42s -> https://www.%s/" % (folder[:42], dom))
        return 0

    EP = "https://mcp.brightdata.com/mcp?token=" + cfg_token()
    _, SID = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                  "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                             "clientInfo": {"name": "opal-cro", "version": "1.0"}}})
    rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, SID)
    print("MODE           LIVE\n")

    out = list(carried)
    calls, empties = 0, 0
    # SEED FROM CARRIED, or a resume reports the carried names as failures.
    resolved = sum(1 for r in carried
                   if r['social_account']['status'] == 'INFERRED')
    consecutive = 0
    for i, (folder, nm, dom) in enumerate(targets, 1):
        body = scrape("https://www." + dom + "/")
        calls += 1
        # THE GUARD THAT DID NOT TRAVEL, CARRIED THIS TIME ON PURPOSE. Both
        # sibling passes needed it and the second one shipped without it.
        if body is None:
            consecutive += 1
            out.append({
                "folder": folder, "company_name": nm, "ir_domain": dom,
                "social_account": {
                    "value": None, "status": "UNRESOLVED",
                    "evidence": ("NOT ASKED / NO PAYLOAD -- the fetch of "
                                 "https://www.%s/ returned nothing. A transient "
                                 "failure and a dead host are byte-identical on "
                                 "this tool, so THIS IS NOT A FINDING that the "
                                 "company publishes no social accounts." % dom),
                    "resolved_at": datetime.datetime.utcnow()
                                   .strftime("%Y-%m-%dT%H:%MZ"),
                }})
            print("  [%2d] %-34s NO PAYLOAD" % (i, folder[:34]))
            if consecutive >= 3:
                print("\n  STOPPING: 3 consecutive empty payloads. The rest "
                      "would record absences that were never really asked.")
                break
            continue
        consecutive = 0

        found = extract(body)
        toks = name_tokens(nm)
        flagged = {}
        for plat, handles in found.items():
            for h in handles:
                hn = re.sub(r"[^a-z0-9]+", "", h.lower())
                flagged.setdefault(plat, []).append(
                    {"handle": h, "handle_carries_company_name":
                     any(t in hn for t in toks)})

        if found:
            resolved += 1
            status, value = "INFERRED", flagged
            note = ("ACCEPTED -- %d platform(s) linked from the company's own "
                    "domain %s: %s." % (len(found), dom,
                                        ", ".join(sorted(found))))
        else:
            empties += 1
            status, value = "UNRESOLVED", None
            note = ("REFUSED -- the page at https://www.%s/ returned %d bytes "
                    "and carried NO social links. Measured cause for at least "
                    "one company (Adobe): the navigation and footer are "
                    "CLIENT-RENDERED, so a markdown scrape cannot see them and "
                    "no fallback page can be followed either. THIS IS A LIMIT "
                    "OF THE INSTRUMENT, not evidence the company has no "
                    "accounts." % (dom, len(body)))

        out.append({
            "folder": folder, "company_name": nm, "ir_domain": dom,
            "body_bytes": len(body),
            "social_account": {
                "value": value, "status": status, "evidence": note,
                "resolved_at": datetime.datetime.utcnow()
                               .strftime("%Y-%m-%dT%H:%MZ"),
            }})
        print("  [%2d] %-34s %-22s %s"
              % (i, folder[:34], ",".join(sorted(found)) or "-- none --",
                 "%d bytes" % len(body)))
        if args.sleep:
            time.sleep(args.sleep)

    print("\nCALLS          %d" % calls)
    print("RESOLVED       %d of %d attempted" % (resolved, len(out)))
    print("NO LINKS       %d  <- instrument limit (client-rendered), NOT an "
          "absence" % empties)
    print("NO PAYLOAD     %d" % (len(out) - resolved - empties))

    if args.out:
        json.dump({
            "artifact": "social_account PASS -- read from each company's OWN site",
            "author": "4.0.0_SA_CRO~Z",
            "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"),
            "method": "scrape the registrable domain already resolved as this "
                      "company's ir_domain, and collect links to known social "
                      "platforms. NOT SERP: Bright Data's search_engine returns "
                      "hostless Google redirect stubs (plan s.16).",
            "evidence_model": "PRIMARY is structural -- the link was published on "
                              "the company's own domain. The handle-carries-the-"
                              "name check is a RECORDED FLAG, never a gate: a "
                              "legitimate handle need not contain the name.",
            "status_note": "INFERRED, not MEASURED: no account page was visited "
                           "to confirm it is operated by this company.",
            "known_limit": "a client-rendered footer is invisible to a markdown "
                           "scrape, and such a site also exposes no nav path to "
                           "follow. Records with zero links say so.",
            "denominator": {
                "universe": total, "with_held_ir_domain": len(held),
                "attempted": len(out), "resolved": resolved,
                "no_links_instrument_limit": empties,
                "no_payload": len(out) - resolved - empties, "calls": calls,
            },
            "records": out,
        }, open(args.out, "w", encoding="utf-8", newline="\n"),
            indent=2, ensure_ascii=True)
        print("WROTE          %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
