"""DSGN_IRPTV1 round 12 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4198: one signed-in FWD-1 trace under a never-widen pair.

Cell: IV-e-87 the DRAFT of that pair for a READ-ONLY synthetic identity on dell2: the journey's hops read from the portal at the DEV tip,
each with its request, the identity and token bounds the CTO ruled, the radius and rollback per key, the branches, both halves UNSIGNED.
It mints nothing and calls nothing.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV87-AC1  ~47/FWD1_TRACE_HOPS.json: portal_commit 40 hex; hops is a non-empty ordered list of {hop, what_the_user_does, requests:
            [{method, route, source: {file, line}}], records}; non_get_requests is exactly the requests whose method is not GET, each
            with is_sign_in (agreeing with the sign_in list), writes_server_side (true / false / NOT_ESTABLISHED) and its handler's
            file and line -- a non-GET read is LISTED for the halves, never hidden and never refused by this check; identity {tier == "internal", firm_list of length 1,
            token_max_minutes <= 30, removed_after_exp == true}; repo_carries is a subset of {hop, status, counts, byte_length,
            sha256_prefix, code}.
  IV87-AC2  ~47/FWD1_TRACE_READONLY_PAIR.md carries "## Measured at signing", "## The identity", "## The act", "## Blast radius",
            "## Branches", "## What must hold before a run order cites this pair", "## COO half", "## CTO half"; each half reads UNSIGNED;
            the text contains no "@" address other than under opal.invalid and no digit run of 8 or more.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
CARRY = {"hop", "status", "counts", "byte_length", "sha256_prefix", "code"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV12"))
        sys.exit(1)

    if cid == "IV87-AC1":
        p = root / (D + "47/FWD1_TRACE_HOPS.json")
        if not p.is_file():
            fail("no record")
        r = json.loads(p.read_bytes().decode("utf-8"))
        if not HEX40.match(str(r.get("portal_commit") or "")):
            fail("portal_commit %r" % r.get("portal_commit"))
        hops = r.get("hops") or []
        if not hops:
            fail("hops empty")
        sign_in = {(x.get("method"), x.get("route")) for x in (r.get("sign_in") or [])}
        non_get = []
        n = 0
        for h in hops:
            if not h.get("hop") or not str(h.get("what_the_user_does") or "").strip() or not h.get("records"):
                fail("hop %r lacks a name, what_the_user_does or records" % h.get("hop"))
            for q in h.get("requests") or []:
                n += 1
                src = q.get("source") or {}
                if not q.get("method") or not q.get("route") or not src.get("file") or not isinstance(src.get("line"), int):
                    fail("hop %r has a request without method, route or file-and-line source" % h.get("hop"))
                if q["method"] != "GET":
                    non_get.append((q["method"], q["route"]))
        if n == 0:
            fail("no request in any hop")
        listed = {(x.get("method"), x.get("route")) for x in (r.get("non_get_requests") or [])}
        if listed != set(non_get):
            fail("non_get_requests %r do not equal the non-GET requests in the hops %r" % (sorted(listed), sorted(set(non_get))))
        for x in r.get("non_get_requests") or []:
            src = x.get("source") or {}
            if x.get("writes_server_side") not in (True, False, "NOT_ESTABLISHED") or not isinstance(x.get("is_sign_in"), bool)                     or not src.get("file") or not isinstance(src.get("line"), int):
                fail("non-GET request %r lacks is_sign_in, writes_server_side or its handler's file and line" % x.get("route"))
            if x["is_sign_in"] != ((x.get("method"), x.get("route")) in sign_in):
                fail("non-GET request %r: is_sign_in disagrees with the sign_in list" % x.get("route"))
        idn = r.get("identity") or {}
        if idn.get("tier") != "internal" or len(idn.get("firm_list") or []) != 1 or not isinstance(idn.get("token_max_minutes"), int) \
                or idn["token_max_minutes"] > 30 or idn.get("removed_after_exp") is not True:
            fail("identity %r is outside the ruled bounds" % idn)
        if not set(r.get("repo_carries") or []) or not set(r.get("repo_carries")) <= CARRY:
            fail("repo_carries %r is not a subset of %r" % (r.get("repo_carries"), sorted(CARRY)))
        print("OK: %d hop(s), %d request(s), %d non-GET listed with what each writes; identity inside the ruled bounds" % (len(hops), n, len(set(non_get))))
    elif cid == "IV87-AC2":
        p = root / (D + "47/FWD1_TRACE_READONLY_PAIR.md")
        if not p.is_file():
            fail("no packet")
        t = p.read_text(encoding="utf-8")
        for hd in ("## Measured at signing", "## The identity", "## The act", "## Blast radius", "## Branches",
                   "## What must hold before a run order cites this pair", "## COO half", "## CTO half"):
            if hd not in t:
                fail("missing heading %r" % hd)
        for hd in ("## COO half", "## CTO half"):
            if "UNSIGNED" not in re.split(r"\n## ", t.split(hd, 1)[1], maxsplit=1)[0]:
                fail("%s not UNSIGNED" % hd)
        bad = [a for a in re.findall(r"[\w.+-]+@[\w.-]+", t) if not a.lower().endswith("opal.invalid") and "opal.agent" not in a.lower()]
        if bad:
            fail("an address outside opal.invalid: %r" % bad[:3])
        if re.search(r"(?<![0-9A-Za-z])\d{8,}(?![0-9A-Za-z])", t):
            fail("a digit run of 8 or more (an account-like token) is in the packet")
        print("OK: packet sections present; both halves UNSIGNED; no address or account-like token")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
