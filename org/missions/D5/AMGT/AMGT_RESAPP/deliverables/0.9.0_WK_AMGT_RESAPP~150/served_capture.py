"""AMGT_RESAPP round 39, AMGT-rn-5 -- capture the SERVED plane for BA_US_Equity.

FWD-30 was graded REALIZED on the IN-PROCESS producer (rm-4's `handler_rich_to_file.py`
patched `scoped_amgt.read_thesis_bundle`/`read_peer_set`/`read_model_block` and called
`handler()` directly -- never a deployed invoke). This script re-runs the comparison's
INPUT HALF against the DEPLOYED `opal-amgt-scoped-api` function, through `lambda:Invoke`,
using the SAME event shape `verify_after.py:71-76`/`:110-112` builds (`rawPath`,
`requestContext.http`, `queryStringParameters`, `x-firm-id` header) and the SAME function
name it invokes.

READ ONLY. No S3 write, no AWS write call of any kind -- `lambda invoke` and
`get_function_configuration` are both reads.

Routes invoked, for BA_US_Equity, matching the landed `tabsFixture.BA_US_Equity.json`'s
own top-level keys (`overlay`, `thesis`, `peers`, `rankings_live`) plus the `print`
leaf `exportCompare.harness.cjs --rich` needs a body for:
  GET /api/scoped/amgt/security/BA_US_Equity/overlay
  GET /api/scoped/amgt/security/BA_US_Equity/thesis
  GET /api/scoped/amgt/security/BA_US_Equity/peers
  GET /api/scoped/amgt/lead-panel/rankings/trending/chatter   (rankings_live's own producer
      read, per the landed fixture's `capture` field and the AMGT-rj-9 fixture-capture
      record: `read_rankings('trending','chatter')` -- INVESTIGATION_v1.md:5490)
  GET /api/scoped/amgt/security/BA_US_Equity/print?format=rich

Run (from the repo root):
  PYTHONPATH=<repo root> python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/
    0.9.0_WK_AMGT_RESAPP~150/served_capture.py
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import boto3

FUNCTION = "opal-amgt-scoped-api"
ROUTE_PREFIX = "/api/scoped/amgt"
REGION = "us-east-1"
SECURITY_KEY = "BA_US_Equity"

HERE = Path(__file__).resolve().parent
SERVED_DIR = HERE / "served"
LANDED_FIXTURE = (
    Path.cwd() / "portal" / "src" / "pages" / "SecurityAnalysis" / "__harness__"
    / "tabsFixture.BA_US_Equity.json"
)


def _event(path, query=None):
    return {
        "rawPath": path,
        "headers": {"x-firm-id": "opal"},
        "requestContext": {"http": {"method": "GET", "path": path}},
        "queryStringParameters": query,
    }


def _invoke(client, path, query=None):
    payload = json.dumps(_event(path, query)).encode("utf-8")
    response = client.invoke(FunctionName=FUNCTION, Payload=payload)
    raw = response["Payload"].read()
    if response.get("FunctionError"):
        return None, {
            "path": path, "query": query, "error": response["FunctionError"],
            "raw": raw[:500].decode("utf-8", "replace"),
        }
    parsed = json.loads(raw)
    headers = parsed.get("headers") or {}
    ctype = headers.get("Content-Type") or headers.get("content-type") or ""
    body = parsed.get("body") or ""
    status = parsed.get("statusCode")
    meta = {"path": path, "query": query, "status": status, "content_type": ctype}
    if status != 200:
        meta["body_head"] = (body if isinstance(body, str) else "")[:500]
        return None, meta
    if parsed.get("isBase64Encoded"):
        blob = base64.b64decode(body)
        text = blob.decode("utf-8", "replace")
    else:
        text = body
    try:
        obj = json.loads(text)
    except ValueError:
        obj = None
        meta["raw_text"] = text[:500]
    meta["bytes"] = len(text.encode("utf-8"))
    return obj, meta


def main():
    client = boto3.client("lambda", region_name=REGION)

    invoked_at = __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    code_sha = client.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]

    routes_meta = []

    overlay_path = "{0}/security/{1}/overlay".format(ROUTE_PREFIX, SECURITY_KEY)
    thesis_path = "{0}/security/{1}/thesis".format(ROUTE_PREFIX, SECURITY_KEY)
    peers_path = "{0}/security/{1}/peers".format(ROUTE_PREFIX, SECURITY_KEY)
    rankings_path = "{0}/lead-panel/rankings/trending/chatter".format(ROUTE_PREFIX)
    print_path = "{0}/security/{1}/print".format(ROUTE_PREFIX, SECURITY_KEY)

    overlay_obj, overlay_meta = _invoke(client, overlay_path)
    routes_meta.append(overlay_meta)
    thesis_obj, thesis_meta = _invoke(client, thesis_path)
    routes_meta.append(thesis_meta)
    peers_obj, peers_meta = _invoke(client, peers_path)
    routes_meta.append(peers_meta)
    rankings_obj, rankings_meta = _invoke(client, rankings_path, {"limit": "10"})
    routes_meta.append(rankings_meta)

    # The rich print body -- NOT parsed as JSON; captured to its own file.
    print_client = boto3.client("lambda", region_name=REGION)
    payload = json.dumps(_event(print_path, {"format": "rich"})).encode("utf-8")
    response = print_client.invoke(FunctionName=FUNCTION, Payload=payload)
    raw = response["Payload"].read()
    rich_meta = {"path": print_path, "query": {"format": "rich"}}
    rich_text = None
    if response.get("FunctionError"):
        rich_meta["error"] = response["FunctionError"]
        rich_meta["raw"] = raw[:500].decode("utf-8", "replace")
    else:
        parsed = json.loads(raw)
        rich_meta["status"] = parsed.get("statusCode")
        headers = parsed.get("headers") or {}
        rich_meta["content_type"] = headers.get("Content-Type") or headers.get("content-type") or ""
        body = parsed.get("body") or ""
        if parsed.get("isBase64Encoded"):
            rich_text = base64.b64decode(body).decode("utf-8", "replace")
        else:
            rich_text = body
        rich_meta["bytes"] = len(rich_text.encode("utf-8"))
    routes_meta.append(rich_meta)

    served = {
        "captured_at": invoked_at,
        "capture": (
            "SERVED plane (AMGT-rn-5): lambda:Invoke of the DEPLOYED opal-amgt-scoped-api, "
            "one invoke per route, for BA_US_Equity -- overlay/thesis/peers/print(format=rich) "
            "plus lead-panel/rankings/trending/chatter for rankings_live. Never the harness "
            "fixture, never the pool directly."
        ),
        "security_key": SECURITY_KEY,
        "overlay": overlay_obj,
        "thesis": thesis_obj,
        "peers": peers_obj,
        "rankings_live": rankings_obj,
        "_served": {
            "function": FUNCTION,
            "code_sha256": code_sha,
            "invoked_at": invoked_at,
            "routes": [m["path"] for m in routes_meta],
        },
    }

    SERVED_DIR.mkdir(parents=True, exist_ok=True)
    out_json = SERVED_DIR / "served_fixture.BA_US_Equity.json"
    out_json.write_text(json.dumps(served, indent=2, sort_keys=False), encoding="utf-8", newline="\n")

    out_rich = SERVED_DIR / "BA_US_Equity.rich.md"
    if rich_text is not None:
        out_rich.write_text(rich_text, encoding="utf-8", newline="\n")

    print("CodeSha256: {0}".format(code_sha))
    print("routes invoked ({0} of {0}):".format(len(routes_meta)))
    for m in routes_meta:
        status = m.get("status", "ERROR:" + str(m.get("error")))
        print("  {0}  status={1}".format(m["path"], status))
    print("wrote {0}".format(out_json))
    if rich_text is not None:
        print("wrote {0} bytes={1}".format(out_rich, len(rich_text.encode("utf-8"))))
    else:
        print("NOT WRITTEN: {0} (print/rich invoke failed: {1})".format(out_rich, rich_meta))

    any_fail = any((m.get("status") != 200) for m in routes_meta)
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
