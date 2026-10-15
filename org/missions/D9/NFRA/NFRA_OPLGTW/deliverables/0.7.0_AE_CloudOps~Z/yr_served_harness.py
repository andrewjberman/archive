#!/usr/bin/env python
"""OG-yr-1 Phase B step 5: the SERVED /yearinreview read, through the INSTALLED code on the host.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python. Uploaded to S3 and pulled by the
host, never inlined into an SSM command (cloud-ops Rule 12).

WHAT `md5_served_host` IS, because three md5s are in play and only one is the oracle (order A3): it is
the md5 of the RESPONSE BODY that app.yearinreview_view.yearinreview_page returns to an admitted
caller -- not a hash of a file I chose to read. load_page() reads
/opt/opal-gateway/app/static/yearinreview/index.html, so the number is the installed page as served.
`md5_file_host` is the same page hashed off the disk and is reported beside it: the two agreeing is the
evidence that the serving path adds and drops nothing.

THE AUDIT SINK IS STUBBED, AND THAT IS A BOUND, NOT A CONVENIENCE. audit.log_call -> audit._emit ->
_s3_client.put_object whenever AUDIT_S3_BUCKET is set, which it is in prod. This order's BOUNDS say
"no object written to any bucket", so calling the live handler with the real sink attached would
breach the order it is proving. log_call is replaced by a recorder; the verdict it WOULD have written
is captured and returned instead. Nothing else is replaced -- _allowed(), tools._is_opal_user and the
host's real YEARINREVIEW_VIEW_ALLOWED_EMAILS all run as installed, and the gate is what this release
changed.

_viewer IS STUBBED PER ARM, and that is the same stand-in the order names ("an Opal stand-in identity
is served 200, an #EXT# guest 403"). The identity WALL is the ALB authenticate-oidc default action
plus identity.py, exercised live by the unauthenticated public GET recorded separately -- not by this
process, which has no ALB in front of it.

NOTHING SENSITIVE IS PRINTED: no .env value, no person's address, no tenant or object id, and not one
roster entry. The three probe addresses are synthetic and are never written to any store; the live
roster is reported only as a COUNT.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import traceback
import urllib.request

ROOT = "/opt/opal-gateway"
PAGE_REL = "app/static/yearinreview/index.html"
UNTIL = b'"until": "2026-10-11"'

# The three arms. OPAL is deliberately NOT a roster member: on the superseded owner-only gate it was a
# 403, so a 200 here is the widening itself and not the roster answering.
OPAL = "yr1.served.probe@opalinvest.com"
GUEST = "yr1_served_probe_example.com#EXT#@opalinvest.com"
OUTSIDER = "yr1.served.probe@example.invalid"


def md5_bytes(raw: bytes) -> str:
    return hashlib.md5(raw).hexdigest()


def md5_path(path: str) -> str:
    with open(path, "rb") as fh:
        return md5_bytes(fh.read())


def tree_md5(rel: str) -> dict:
    """Every file under ROOT/rel, path relative to ROOT -> md5. __pycache__ and .pyc are excluded: they
    are build products of the host's own interpreter and were never in the artifact."""
    out = {}
    base = os.path.join(ROOT, rel)
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".pyc"):
                continue
            full = os.path.join(dirpath, fn)
            key = os.path.relpath(full, ROOT).replace(os.sep, "/")
            try:
                out[key] = md5_path(full)
            except OSError as exc:
                out[key] = "UNREADABLE:%s" % type(exc).__name__
    return out


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    out = {"body": {}}
    body = out["body"]

    # ---- the file on disk, and the data date in the installed bytes -----------------------------
    page = os.path.join(ROOT, PAGE_REL)
    with open(page, "rb") as fh:
        raw = fh.read()
    body["md5_source"] = "0d828b51d433a24f7e2ef2e6ea7967ee"   # order A3: the checked-out form the deploy tars
    body["md5_file_host"] = md5_bytes(raw)
    body["page_bytes_host"] = len(raw)
    body["page_crlf_host"] = raw.count(b"\r\n")

    # ---- /health on the loopback -----------------------------------------------------------------
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=10) as resp:
            body["health_status"] = resp.status
            body["health_body"] = resp.read(200).decode("utf-8", "replace").strip()
    except Exception as exc:
        body["health_status"] = None
        body["health_body"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])

    # ---- the three arms, through the installed handler -------------------------------------------
    import asyncio

    from starlette.requests import Request

    from app import tools
    from app import yearinreview_view as yv

    audit_rows = []

    def _recorder(email, tool, args, outcome, detail="", **kw):
        # The verdict the real sink would have written, kept in-process: no bucket object, no local JSONL.
        audit_rows.append((tool, outcome, detail))

    yv.audit.log_call = _recorder                                    # type: ignore[assignment]

    def _req() -> Request:
        scope = {"type": "http", "method": "GET", "path": "/yearinreview", "raw_path": b"/yearinreview",
                 "headers": [], "query_string": b"", "server": ("ssm-harness", 80), "scheme": "http",
                 "root_path": ""}
        return Request(scope)

    roster = yv._cfg.YEARINREVIEW_VIEW_ALLOWED_EMAILS or ()
    body["roster_size_live"] = len(roster)
    body["opal_probe_on_roster"] = OPAL in roster       # must be false, or the 200 proves nothing

    arms = {}
    for label, who in (("opal", OPAL), ("guest", GUEST), ("outsider", OUTSIDER)):
        yv._viewer = (lambda w: (lambda request: w))(who)            # type: ignore[assignment]
        before = len(audit_rows)
        resp = asyncio.run(yv.yearinreview_page(_req()))
        served = resp.body or b""
        arms[label] = {
            "status": resp.status_code,
            "body_bytes": len(served),
            "body_md5": md5_bytes(served),
            "serves_page": b"<title>Opal Year One Review</title>" in served,
            "carries_until": UNTIL in served,
            "audit_verdict": list((audit_rows[before:] or [(None, None, None)])[-1][1:]),
            "is_opal_user_predicate": tools._is_opal_user(who),
        }
    body["arms"] = arms

    opal_arm = arms["opal"]
    body["md5_served_host"] = opal_arm["body_md5"]
    body["contains_until_2026_10_11"] = bool(opal_arm["carries_until"])
    body["opal_user_admitted"] = bool(opal_arm["status"] == 200 and opal_arm["serves_page"]
                                      and not body["opal_probe_on_roster"])
    body["guest_refused"] = bool(arms["guest"]["status"] == 403 and not arms["guest"]["serves_page"]
                                 and arms["guest"]["body_bytes"] < 400)
    body["outsider_refused"] = bool(arms["outsider"]["status"] == 403
                                    and not arms["outsider"]["serves_page"])
    body["served_equals_file"] = body["md5_served_host"] == body["md5_file_host"]
    body["served_equals_source"] = body["md5_served_host"] == body["md5_source"]

    # ---- the registry, which this release does not touch ------------------------------------------
    try:
        names = [t.name for t in tools.mcp._tool_manager.list_tools()]
    except Exception:
        names = [t.name for t in asyncio.run(tools.mcp.list_tools())]
    body["registry_count"] = len(names)
    body["registry_instrument"] = "app.tools.mcp._tool_manager.list_tools()"

    # ---- the running bytes, per file, for the local parity diff -----------------------------------
    body["tree_md5"] = {}
    for rel in ("app", "deploy", "dashboard"):
        body["tree_md5"].update(tree_md5(rel))
    body["tree_md5_files"] = len(body["tree_md5"])

    body["audit_rows_captured"] = len(audit_rows)
    body["audit_sink_stubbed"] = True
    print("YR_SERVED_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("YR_SERVED_JSON")
        print(json.dumps({"body": {"verdict": "FAIL", "fatal": traceback.format_exc()[-1500:]}}, indent=1))
        sys.exit(1)
