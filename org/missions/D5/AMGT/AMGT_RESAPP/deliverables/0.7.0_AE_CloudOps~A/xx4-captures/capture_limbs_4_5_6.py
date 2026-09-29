"""AMGT_RESAPP round 49, AMGT-xx-4 -- capture the three NEVER-WIDEN limbs the halves grade on OUTPUT.

Limb 4: the served `/print` PDF OUTPUT must be byte-equal on AMD, BA, GOOGL and 1299 HK across the apply.
Limb 5: the served `/timeline` OUTPUT must be byte-equal on 1299 HK. A move on AMD, BA or GOOGL is
        ATTRIBUTED against any AMGT_HARVST data write after the capture before it is a ROLLBACK
        (round 48 AMENDMENT 1 @95a081df7b, CTO msg 26679) -- so those three are captured too, as the
        attribution comparands, not as strict-equality arms.
Limb 6: the served `/lead-panel/rankings/trending/chatter` rows must be equal across the apply,
        `generated_at` excepted.

Derived from this seat's round-48 capture_limbs_5_6.py, which covered limbs 5 and 6 of that round; the
rankings read is new here because round 49's limb 6 grades it.

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

# The four names both halves name for limbs 4 and 5.
NAMES = ["AMD_US_Equity", "BA_US_Equity", "GOOGL_US_Equity", "1299_HK_Equity"]

# Limb 5 grades STRICT byte-equality on this one only; the others are attribution comparands.
STRICT_TIMELINE = {"1299_HK_Equity"}


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

    def record(name, label, path, query=None, limb=None, strict=True):
        status, ctype, blob, err = _raw_invoke(client, path, query)
        digest = hashlib.sha256(blob).hexdigest()
        slug = "%s.%s" % (name.replace("/", "_"), label)
        (out / (slug + ".bin")).write_bytes(blob)
        rows.append({
            "name": name, "route": label, "path": path, "query": query, "limb": limb,
            "strict": strict, "status": status, "content_type": ctype,
            "bytes": len(blob), "sha256": digest, "error": err,
        })
        print("  %-16s %-12s limb=%-4s strict=%-5s status=%s bytes=%-8d sha256=%s%s"
              % (name, label, limb, strict, status, len(blob), digest[:16],
                 "  ERR=" + err if err else ""))

    # Limb 4 (/print, strict on all four) and limb 5 (/timeline, strict on 1299 HK only).
    for key in NAMES:
        record(key, "print_pdf", "%s/security/%s/print" % (ROUTE_PREFIX, key), None, limb="4", strict=True)
        record(key, "timeline", "%s/security/%s/timeline" % (ROUTE_PREFIX, key), None,
               limb="5", strict=(key in STRICT_TIMELINE))

    # Limb 6: the rankings rows. generated_at is excepted, so store a normalised copy beside the raw one.
    path = "%s/lead-panel/rankings/trending/chatter" % ROUTE_PREFIX
    status, ctype, blob, err = _raw_invoke(client, path, None)
    (out / "rankings.trending_chatter.bin").write_bytes(blob)
    norm = None
    try:
        doc = json.loads(blob.decode("utf-8"))
        doc.pop("generated_at", None)
        if isinstance(doc.get("rows"), list):
            for r in doc["rows"]:
                if isinstance(r, dict):
                    r.pop("generated_at", None)
        norm = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")
        (out / "rankings.trending_chatter.normalised.json").write_bytes(norm)
    except Exception as exc:          # a body that is not JSON is itself the finding; record it
        print("  NOTE: rankings body not normalisable as JSON: %r" % (exc,))
    rows.append({
        "name": "rankings", "route": "trending_chatter", "path": path, "query": None, "limb": "6",
        "strict": True, "status": status, "content_type": ctype, "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "sha256_normalised": hashlib.sha256(norm).hexdigest() if norm is not None else None,
        "error": err,
    })
    print("  %-16s %-12s limb=6    strict=True  status=%s bytes=%-8d sha256=%s  norm=%s"
          % ("rankings", "trending_chat", status, len(blob),
             hashlib.sha256(blob).hexdigest()[:16],
             hashlib.sha256(norm).hexdigest()[:16] if norm is not None else "NONE"))

    manifest = {"captured_at": at, "code_sha256": sha, "function": FUNCTION, "rows": rows}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("MANIFEST %s  (%d route reads)" % (out / "manifest.json", len(rows)))
    return manifest


if __name__ == "__main__":
    capture(sys.argv[1])
