#!/usr/bin/env python3
"""POSN_ASTTAX.TO-V9-1 V9-AC11 -- the FIVE-PATH VERIFY.

Resolves the task order's <FIVE_PATH_VERIFY_AUTHENTICATED> placeholder.

WHAT THIS IS, AND THE ONE THING IT IS NOT
-----------------------------------------
The criterion asks for an AUTHENTICATED five-path verify. On this device that half
is BLOCKED: every committed portal credential fixture returns mfaRequired=true from
POST /auth/login, and satisfying a second factor is CREDENTIAL-EQUIVALENT and is
NOT authorized by any standing ruling (the fixture file says so itself). So this
instrument runs the authenticated arm's OWN QUESTION on two planes that do not
need a bearer, and it labels the gap rather than papering it:

  ARM A  EDGE ENVELOPE (live, unauthenticated, before/after).
         One GET per behavior through https://opalinvest.dev. Records status,
         content-type, byte length and body sha256.
         PROVES: the five behaviors still exist, still bind their edge functions
         and still answer in the same envelope before and after.
         DOES NOT PROVE: anything about the rewrite. auth-validator-edge is a
         VIEWER-REQUEST function and shared-advisor-router is ORIGIN-REQUEST, so
         an unauthenticated probe is refused BEFORE the router runs. Stated here
         because an identical-before/after on this arm would otherwise read as
         evidence about code it never reached.

  ARM B  DEPLOYED-BYTES INVOKE (before/after, the discriminating arm).
         Invokes the PUBLISHED Lambda version directly with a synthetic
         CloudFront origin-request event -- the same event shape the edge
         delivers -- and reads back the rewritten uri / origin / refusal status.
         This exercises the DEPLOYED ARTIFACT, not the committed source, and it
         is run against BOTH the prior version and the new one with byte-identical
         payloads, so the four Advisor Intelligence rewrites are compared
         version-to-version rather than asserted.
         DOES NOT PROVE: that S3 then serves the object, nor the end-to-end
         served bytes through the real edge.

ARM B is the substitute oracle for the authenticated arm's real question ("does
the router still rewrite behaviors 1-4 identically, and does it now admit the two
new leaves"). It is weaker than a bearer in exactly one direction: it bypasses the
auth gate, so it says nothing about authorization. It is stronger in another: it
grades deployed bytes at a named version rather than a session's luck.

Usage:
  python five_path_verify.py --phase before --version 25 --out <path>
  python five_path_verify.py --phase after  --version 26 --out <path>
  python five_path_verify.py --compare <before.json> <after.json>
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HOST = "https://opalinvest.dev"
FUNCTION = "shared-advisor-router"
# Native Windows Python cannot exec the bash shim .tools/aws (WinError 2); the
# estate ships .tools/aws.cmd beside it for exactly this caller. Payload goes via
# fileb:// and never through argv -- aws.cmd truncates a multi-line argv value at
# the first newline and still returns rc=0.
AWS_SHIM = os.path.join(".tools", "aws.cmd" if os.name == "nt" else "aws")

# The five behaviors, one probe each. Behavior binding was resolved against the
# LIVE distribution config with CloudFront first-match-wins semantics, never assumed.
PROBES = [
    ("AI-1", "/api/scoped/advisor-intelligence/artifacts/*/*",
     "/api/scoped/advisor-intelligence/artifacts/snapshots/aua_by_region.json"),
    ("AI-2", "/api/scoped/advisor-intelligence/artifacts/*",
     "/api/scoped/advisor-intelligence/artifacts/clients_tab.json"),
    ("AI-3", "/api/scoped/advisor-intelligence/entities/*/*",
     "/api/scoped/advisor-intelligence/entities/accounts/z0925724581/aua_timeseries.json"),
    ("AI-4", "/api/scoped/advisor-intelligence/*.json",
     "/api/scoped/advisor-intelligence/views/firm_composition.json"),
    ("SAT-registry", "/api/scoped/satellites/*", "/api/scoped/satellites/registry.json"),
    ("SAT-holdings", "/api/scoped/satellites/*", "/api/scoped/satellites/holdings.json"),
    ("SAT-characteristics", "/api/scoped/satellites/*", "/api/scoped/satellites/characteristics.json"),
    ("SAT-unlisted", "/api/scoped/satellites/*", "/api/scoped/satellites/nope.json"),
]

# TO-7-AE's discriminating control: a path NO behavior claims falls to the default
# and answers in a DIFFERENT envelope (403/xml) than a claimed-but-unauthenticated
# scoped route (401/json). Without it, "401 everywhere" cannot tell a live behavior
# from a missing one.
NO_BEHAVIOR_CONTROL = ("CTRL-no-behavior", "*DEFAULT* /*", "/api/scoped/zzz-no-such-behavior/x.json")


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- ARM A
def edge_get(path, querystring=""):
    url = HOST + path + (("?" + querystring) if querystring else "")
    req = urllib.request.Request(url, headers={"User-Agent": "opal-posn-b5-verify"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return {"status": r.status, "content_type": r.headers.get("Content-Type"),
                    "bytes": len(body), "sha256": sha256_hex(body)}
    except urllib.error.HTTPError as e:
        body = e.read()
        return {"status": e.code, "content_type": e.headers.get("Content-Type"),
                "bytes": len(body), "sha256": sha256_hex(body)}
    except Exception as e:
        return {"status": "ERR", "content_type": None, "bytes": 0,
                "sha256": None, "error": repr(e)[:200]}


def arm_a():
    rows = []
    for name, pattern, path in PROBES + [NO_BEHAVIOR_CONTROL]:
        qs = "firm=cot"
        r = edge_get(path, qs)
        r.update({"probe": name, "behavior": pattern, "path": path, "querystring": qs})
        rows.append(r)
        time.sleep(0.2)
    return rows


# ---------------------------------------------------------------- ARM B
def cf_event(uri, firm_id, querystring=""):
    """The origin-request event shape the edge delivers, with the headers
    auth-validator-edge injects downstream of a real login."""
    headers = {
        "x-firm-id": [{"key": "X-Firm-Id", "value": firm_id}],
        "x-user-tier": [{"key": "X-User-Tier", "value": "internal"}],
        "host": [{"key": "Host", "value": "opalinvest.dev"}],
    }
    return {"Records": [{"cf": {"request": {
        "method": "GET", "uri": uri, "querystring": querystring, "headers": headers,
        "origin": {"s3": {"domainName": "opal-data-portal-v2.s3.us-east-1.amazonaws.com",
                          "region": "us-east-1", "authMethod": "origin-access-identity",
                          "path": "", "customHeaders": {}}},
    }}}]}


def invoke(version, payload):
    fn = FUNCTION + ":" + str(version)
    pf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="ascii")
    json.dump(payload, pf)
    pf.close()
    of = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    of.close()
    try:
        p = subprocess.run(
            [AWS_SHIM, "lambda", "invoke", "--function-name", fn,
             "--payload", "fileb://" + pf.name.replace("\\", "/"),
             "--cli-read-timeout", "60", of.name.replace("\\", "/")],
            capture_output=True, text=True, timeout=120)
        with open(of.name, "rb") as fh:
            raw = fh.read()
        if p.returncode != 0:
            return {"invoke_rc": p.returncode, "error": (p.stderr or "")[:400]}
        try:
            return {"invoke_rc": 0, "result": json.loads(raw.decode("utf-8"))}
        except Exception:
            return {"invoke_rc": 0, "raw": raw.decode("utf-8", "replace")[:400]}
    finally:
        for f in (pf.name, of.name):
            try:
                os.unlink(f)
            except OSError:
                pass


def summarize(res):
    """Collapse a router return into the fields that decide the criterion."""
    if "result" not in res:
        return res
    r = res["result"]
    if not isinstance(r, dict):
        return {"shape": "UNEXPECTED", "value": str(r)[:200]}
    if "status" in r:  # a generated response = a refusal
        body = r.get("body", "")
        try:
            err = json.loads(body).get("error")
        except Exception:
            err = body[:80]
        return {"outcome": "REFUSED", "status": r.get("status"), "error": err}
    origin = ((r.get("origin") or {}).get("s3") or {}).get("domainName")
    return {"outcome": "REWRITTEN", "uri": r.get("uri"), "origin": origin}


def arm_b(version):
    rows = []
    identities = [("opal-capital+firm=cot", "opal-capital", "firm=cot"),
                  ("49financial", "49financial", "")]
    for name, pattern, path in PROBES:
        for ident_label, firm_id, qs in identities:
            ev = cf_event(path, firm_id, qs)
            out = summarize(invoke(version, ev))
            out.update({"probe": name, "behavior": pattern, "path": path,
                        "identity": ident_label})
            rows.append(out)
    return rows


# ---------------------------------------------------------------- compare
def key_a(r):
    return r["probe"]


def key_b(r):
    return (r["probe"], r["identity"])


def compare(before, after):
    bf = {r["probe"]: r for r in before["arm_a"]}
    af = {r["probe"]: r for r in after["arm_a"]}
    print("")
    print("ARM A -- EDGE ENVELOPE, live, UNAUTHENTICATED, before vs after")
    print("  (proves the behavior still exists and binds; proves NOTHING about the rewrite --")
    print("   the auth gate is viewer-request and refuses ahead of this origin-request router)")
    print("")
    hdr = "  {:20} {:8} {:8} {:7} {:7} {:9} {}".format(
        "probe", "st.bef", "st.aft", "B.bef", "B.aft", "hash", "VERDICT")
    print(hdr)
    ok_a = True
    for name, _p, _path in PROBES + [NO_BEHAVIOR_CONTROL]:
        b, a = bf.get(name, {}), af.get(name, {})
        same = (b.get("status") == a.get("status") and b.get("sha256") == a.get("sha256"))
        if not same:
            ok_a = False
        print("  {:20} {:8} {:8} {:7} {:7} {:9} {}".format(
            name, str(b.get("status")), str(a.get("status")), str(b.get("bytes")),
            str(a.get("bytes")), "IDENTICAL" if b.get("sha256") == a.get("sha256") else "DIFFERS",
            "SAME" if same else "CHANGED"))
    ctrl_b = bf.get("CTRL-no-behavior", {})
    reg_b = bf.get("SAT-registry", {})
    disc = (ctrl_b.get("status") != reg_b.get("status")
            or ctrl_b.get("content_type") != reg_b.get("content_type"))
    print("")
    print("  CONTROL (does ARM A discriminate a live behavior from a missing one?): {}".format(
        "FIRES -- claimed route {} {} vs no-behavior {} {}".format(
            reg_b.get("status"), reg_b.get("content_type"),
            ctrl_b.get("status"), ctrl_b.get("content_type")) if disc
        else "DOES NOT FIRE -- the arm cannot tell the two apart"))

    print("")
    print("ARM B -- DEPLOYED BYTES, router invoked directly at a named version")
    print("  before = v{}   after = v{}".format(before["version"], after["version"]))
    print("")
    bb = {key_b(r): r for r in before["arm_b"]}
    ab = {key_b(r): r for r in after["arm_b"]}
    print("  {:20} {:22} {:34} {:34} {}".format(
        "probe", "identity", "BEFORE", "AFTER", "VERDICT"))

    def render(r):
        if not r:
            return "(missing)"
        if r.get("outcome") == "REFUSED":
            return "REFUSED {} {}".format(r.get("status"), r.get("error"))
        if r.get("outcome") == "REWRITTEN":
            return "-> {}".format(r.get("uri"))
        return str(r)[:34]

    findings = []
    for k in sorted(set(list(bb.keys()) + list(ab.keys()))):
        b, a = bb.get(k), ab.get(k)
        rb, ra = render(b), render(a)
        expect_change = k[0] in ("SAT-holdings", "SAT-characteristics")
        changed = rb != ra
        if expect_change:
            verdict = "CHANGED-AS-SPECIFIED" if changed else "DID-NOT-MOVE"
        else:
            verdict = "IDENTICAL" if not changed else "UNEXPECTED-CHANGE"
        findings.append((k, verdict))
        print("  {:20} {:22} {:34} {:34} {}".format(k[0], k[1], rb[:34], ra[:34], verdict))

    print("")
    bad = [k for k, v in findings if v in ("UNEXPECTED-CHANGE", "DID-NOT-MOVE")]
    print("  ARM B denominator: {} of {} comparisons".format(len(findings), len(findings)))
    print("  ARM B rows outside the signed bound: {}".format(len(bad)))
    for k, v in findings:
        if v in ("UNEXPECTED-CHANGE", "DID-NOT-MOVE"):
            print("     OUTSIDE: {} {} -> {}".format(k[0], k[1], v))
    print("")
    print("  ARM A verdict: {}".format("all probes identical before/after" if ok_a
                                       else "AT LEAST ONE PROBE CHANGED"))
    print("")
    print("BLOCKED AND NOT CLAIMED: the end-to-end AUTHENTICATED fetch (a real bearer through")
    print("the edge, served S3 bytes compared to the object). Every committed fixture is")
    print("MFA-gated; satisfying the second factor is credential-equivalent and unauthorized.")
    return 0 if (ok_a and not bad) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["before", "after"])
    ap.add_argument("--version")
    ap.add_argument("--out")
    ap.add_argument("--compare", nargs=2)
    a = ap.parse_args()
    # NO ARGUMENTS = re-render the verdict from the two committed captures.
    # The task order names this instrument as `python <FIVE_PATH_VERIFY_AUTHENTICATED>`
    # with NO arguments, so the bare invocation has to be the one that produces the
    # criterion's table. The captures are committed beside this file, which also makes
    # the table re-derivable by a later reader without re-touching the live plane.
    if not (a.compare or a.phase):
        here = os.path.dirname(os.path.abspath(__file__))
        a.compare = [os.path.join(here, "five_path_verify.BEFORE.json"),
                     os.path.join(here, "five_path_verify.AFTER.json")]
    if a.compare:
        with open(a.compare[0]) as f:
            b = json.load(f)
        with open(a.compare[1]) as f:
            c = json.load(f)
        return compare(b, c)
    rec = {"phase": a.phase, "version": a.version,
           "read_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "arm_a": arm_a(), "arm_b": arm_b(a.version)}
    with open(a.out, "w") as f:
        json.dump(rec, f, indent=2)
    print("OK: {} phase recorded at v{} -> {}".format(a.phase, a.version, a.out))
    print("  ARM A rows: {}   ARM B rows: {}".format(len(rec["arm_a"]), len(rec["arm_b"])))
    for r in rec["arm_a"]:
        print("   EDGE {:20} {} {} {}B".format(r["probe"], r["status"], r["content_type"], r["bytes"]))
    for r in rec["arm_b"]:
        print("   INVK {:20} {:22} {}".format(
            r["probe"], r["identity"],
            r.get("uri") or "REFUSED {} {}".format(r.get("status"), r.get("error")) if r.get("outcome")
            else str(r)[:80]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
