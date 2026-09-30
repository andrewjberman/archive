"""AMGT_RESAPP round 48, AMGT-ww-1 -- capture the two NEVER-WIDEN limbs the halves grade on OUTPUT.

Limb 6: the served `/timeline` (and `/timeline/day`) OUTPUT must be byte-equal across the apply.
Limb 5: the served `/print` PDF OUTPUT must be byte-equal across the apply.
Either one moving is a ROLLBACK, not a note (CTO half s.2 condition 3).

READ-ONLY: `lambda:Invoke` of the DEPLOYED opal-amgt-scoped-api only. No AWS write call of any kind.

usage (repo root):  python <this> <out_dir>
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import sys
from pathlib import Path

import boto3

FUNCTION = "opal-amgt-scoped-api"
ROUTE_PREFIX = "/api/scoped/amgt"
REGION = "us-east-1"

# The four names the COO half's own limb-6 measurement used.
NAMES = ["AMD_US_Equity", "BA_US_Equity", "GOOGL_US_Equity", "1299_HK_Equity"]


def _event(path, query=None):
    return {
        "rawPath": path,
        "headers": {"x-firm-id": "opal"},
        "requestContext": {"http": {"method": "GET", "path": path}},
        "queryStringParameters": query,
    }


def _raw_invoke(client, path, query=None):
    """Return (status, content_type, body_bytes, error) -- the RAW served bytes, never re-serialised."""
    payload = json.dumps(_event(path, query)).encode("utf-8")
    resp = client.invoke(FunctionName=FUNCTION, Payload=payload)
    raw = resp["Payload"].read()
    if resp.get("FunctionError"):
        return None, None, b"", "%s %s" % (resp["FunctionError"], raw[:300].decode("utf-8", "replace"))
    parsed = json.loads(raw)
    headers = parsed.get("headers") or {}
    ctype = headers.get("Content-Type") or headers.get("content-type") or ""
    body = parsed.get("body") or ""
    blob = base64.b64decode(body) if parsed.get("isBase64Encoded") else body.encode("utf-8")
    return parsed.get("statusCode"), ctype, blob, None


def capture(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    client = boto3.client("lambda", region_name=REGION)
    sha = client.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]
    at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print("deployed CodeSha256 %s  captured_at %s" % (sha, at))

    rows = []
    for key in NAMES:
        for label, path, q in (
            ("timeline", "%s/security/%s/timeline" % (ROUTE_PREFIX, key), None),
            ("print_pdf", "%s/security/%s/print" % (ROUTE_PREFIX, key), None),
        ):
            status, ctype, blob, err = _raw_invoke(client, path, q)
            digest = hashlib.sha256(blob).hexdigest()
            slug = "%s.%s" % (key.replace("/", "_"), label)
            (out / (slug + ".bin")).write_bytes(blob)
            rows.append({
                "name": key, "route": label, "path": path, "status": status,
                "content_type": ctype, "bytes": len(blob), "sha256": digest, "error": err,
            })
            print("  %-16s %-10s status=%s bytes=%-8d sha256=%s%s"
                  % (key, label, status, len(blob), digest[:16], "  ERR=" + err if err else ""))

    # One /timeline/day read, on the name the halves name first.
    day = datetime.date.today().isoformat()
    path = "%s/security/%s/timeline/day/%s" % (ROUTE_PREFIX, NAMES[0], day)
    status, ctype, blob, err = _raw_invoke(client, path, None)
    digest = hashlib.sha256(blob).hexdigest()
    (out / ("%s.timeline_day.bin" % NAMES[0])).write_bytes(blob)
    rows.append({"name": NAMES[0], "route": "timeline_day", "path": path, "status": status,
                 "content_type": ctype, "bytes": len(blob), "sha256": digest, "error": err})
    print("  %-16s %-10s status=%s bytes=%-8d sha256=%s" % (NAMES[0], "tl_day", status, len(blob), digest[:16]))

    manifest = {"captured_at": at, "code_sha256": sha, "function": FUNCTION, "rows": rows}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("MANIFEST %s  (%d route reads)" % (out / "manifest.json", len(rows)))
    return manifest


if __name__ == "__main__":
    capture(sys.argv[1])
