"""AMGT_RESAPP round 41, AMGT-rp-1 -- capture the SERVED plane for ANY coverage-list security key.

GENERALISED from `0.9.0_WK_AMGT_RESAPP~150/served_capture.py` (rn-5's BA_US_Equity capture): same
routes, same event shape, same `lambda:Invoke` of the deployed `opal-amgt-scoped-api`, same READ-ONLY
standing (no S3 write, no AWS write call of any kind) -- parameterised on `security_key` and on the
output directory so a sweep can call it once per coverage-list name into a fresh temp directory
outside the repository (BOUNDS 1/3 of this cell's own task order).

Routes invoked, matching rn-5's set:
  GET /api/scoped/amgt/security/{key}/overlay
  GET /api/scoped/amgt/security/{key}/thesis
  GET /api/scoped/amgt/security/{key}/peers
  GET /api/scoped/amgt/lead-panel/rankings/trending/chatter   (rankings_live's own producer read)
  GET /api/scoped/amgt/security/{key}/print?format=rich

Run (from the repo root, via sweep.py -- not usually invoked directly):
  PYTHONPATH=<repo root> python -c "from capture_lib import capture; capture('BA_US_Equity', '/tmp/x')"
"""
from __future__ import annotations

import base64
import datetime
import json
import re
from pathlib import Path

import boto3


def _filename_slug(security_key):
    """A security_key can carry characters that are not safe as a bare filename (the
    coverage list measured 2 of 89 keys with a literal '/', e.g. 'BP/_LN_Equity' --
    a landed-model-block display value copied through unescaped). This slug is used
    ONLY for the on-disk file name; the JSON payload's own `security_key` field
    always carries the value verbatim."""
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", security_key)

FUNCTION = "opal-amgt-scoped-api"
ROUTE_PREFIX = "/api/scoped/amgt"
REGION = "us-east-1"


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


def capture(security_key, out_dir):
    """Invoke every route for `security_key` against the deployed function, write
    `served/served_fixture.<key>.json` and `served/<key>.rich.md` under `out_dir`
    (created if needed). Returns (routes_meta, rich_text, served_dict)."""
    out_dir = Path(out_dir)
    served_dir = out_dir / "served"
    served_dir.mkdir(parents=True, exist_ok=True)

    client = boto3.client("lambda", region_name=REGION)
    invoked_at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    code_sha = client.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]

    routes_meta = []

    overlay_path = "{0}/security/{1}/overlay".format(ROUTE_PREFIX, security_key)
    thesis_path = "{0}/security/{1}/thesis".format(ROUTE_PREFIX, security_key)
    peers_path = "{0}/security/{1}/peers".format(ROUTE_PREFIX, security_key)
    rankings_path = "{0}/lead-panel/rankings/trending/chatter".format(ROUTE_PREFIX)
    print_path = "{0}/security/{1}/print".format(ROUTE_PREFIX, security_key)

    overlay_obj, overlay_meta = _invoke(client, overlay_path)
    routes_meta.append(overlay_meta)
    thesis_obj, thesis_meta = _invoke(client, thesis_path)
    routes_meta.append(thesis_meta)
    peers_obj, peers_meta = _invoke(client, peers_path)
    routes_meta.append(peers_meta)
    rankings_obj, rankings_meta = _invoke(client, rankings_path, {"limit": "10"})
    routes_meta.append(rankings_meta)

    # The rich print body -- NOT parsed as JSON; captured to its own file.
    payload = json.dumps(_event(print_path, {"format": "rich"})).encode("utf-8")
    response = client.invoke(FunctionName=FUNCTION, Payload=payload)
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
            "SERVED plane (AMGT-rp-1, generalised from rn-5's served_capture.py): lambda:Invoke of "
            "the DEPLOYED opal-amgt-scoped-api, one invoke per route, for {0} -- overlay/thesis/peers/"
            "print(format=rich) plus lead-panel/rankings/trending/chatter for rankings_live. Never the "
            "harness fixture, never the pool directly."
        ).format(security_key),
        "security_key": security_key,
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

    slug = _filename_slug(security_key)
    out_json = served_dir / "served_fixture.{0}.json".format(slug)
    out_json.write_text(json.dumps(served, indent=2, sort_keys=False), encoding="utf-8", newline="\n")

    out_rich = served_dir / "{0}.rich.md".format(slug)
    if rich_text is not None:
        out_rich.write_text(rich_text, encoding="utf-8", newline="\n")

    return {
        "routes_meta": routes_meta,
        "served_fixture_path": str(out_json),
        "rich_path": str(out_rich) if rich_text is not None else None,
        "rich_bytes": len(rich_text.encode("utf-8")) if rich_text is not None else 0,
        "code_sha256": code_sha,
    }
