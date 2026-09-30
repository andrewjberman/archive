"""AMGT_RESAPP round 53, AMGT-ac-3 -- capture the never-widen limbs the halves grade on OUTPUT.

THE LIMB NUMBERS MOVED AGAIN this round, and one of them changed SHAPE. Round 52's limbs 5/6 are
round 53's limbs 6/7, and limb 6 is no longer a plain byte-equality:

Limb 6: "The served `/print` pdf OUTPUT or `/timeline` OUTPUT (BEYOND THE ADDED `publishers_found_codes`
        KEY) moves on AMD, BA, GOOGL, 1299 HK."
        `/print` is graded on raw bytes. `/timeline` CANNOT be: AC2 is precisely that every series
        entry GAINS `publishers_found_codes` (HARVST q-5), so the raw body MUST move and a byte
        comparison would report a limb-6 violation for the act working as designed -- the same trap
        round 51 hit on the lead-list rows. So `/timeline` is captured twice over:
          - the raw bytes (recorded, never the limb's oracle), and
          - a PROJECTION with every `publishers_found_codes` key removed RECURSIVELY, plus the
            volatile render keys dropped. That projection is limb 6's oracle for `/timeline`.
        The capture also counts, per name, how many series entries carry the key -- so the SAME
        capture that clears the limb also evidences the change the act intends.

Limb 7: "A lead-list row's `rank`, `score`, ORDER, `name` or `places_moved` moves against the
        pre-apply capture of the SAME GENERATION." Projection-graded, never raw bytes; a moved
        `generation_id` makes the axis VOID rather than passing quietly.

ATTRIBUTION: the newest `derived/model_block/<key>/<ts>/` stamp per name is recorded, as in round 52,
so a `/print` move can be attributed to a concurrent block write before it is read as a rollback.

READ-ONLY: `lambda:Invoke` of the DEPLOYED opal-amgt-scoped-api, plus S3 LIST on the model-block pool.
No AWS write call of any kind.

usage (repo root):  python <this> <out_dir>
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

import boto3

sys.path.insert(0, os.getcwd())

FUNCTION = "opal-amgt-scoped-api"
ROUTE_PREFIX = "/api/scoped/amgt"
REGION = "us-east-1"

NAMES = ["AMD_US_Equity", "BA_US_Equity", "GOOGL_US_Equity", "1299_HK_Equity"]
AXES = [("trending", "chatter"), ("trending", "price"), ("breakout", "chatter"), ("breakout", "price")]
ROW_FIELDS = ("ticker", "security_key", "rank", "rank_sort", "score", "name", "places_moved")

# The key AC2 ADDS. Limb 6 grades /timeline "beyond" it, so it is removed before comparing.
ADDED_KEY = "publishers_found_codes"
VOLATILE = ("generated_at", "read_at", "served_at", "request_id")

MODEL_BLOCK_PREFIX = "derived/model_block/"
# AMZN is AC2's own name; carried here so the found-codes evidence and the limb share one capture.
STAMP_NAMES = NAMES + ["AMZN_US_Equity"]


def _event(path, query=None):
    return {
        "rawPath": path,
        "headers": {"x-firm-id": "opal"},
        "requestContext": {"http": {"method": "GET", "path": path}},
        "queryStringParameters": query,
    }


def _raw_invoke(client, path, query=None):
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


def _strip(o, drop):
    """Remove every key in `drop` at any depth -- limb 6's /timeline oracle."""
    if isinstance(o, dict):
        return {k: _strip(v, drop) for k, v in o.items() if k not in drop}
    if isinstance(o, list):
        return [_strip(v, drop) for v in o]
    return o


def _timeline_projection(blob):
    """(projection_sha, series_len, entries_carrying_the_added_key, note)."""
    try:
        doc = json.loads(blob.decode("utf-8"))
    except ValueError as exc:
        return None, None, None, "body not parseable as JSON: %r" % (exc,)
    ser = doc.get("series") or []
    carrying = sum(1 for e in ser if isinstance(e, dict) and ADDED_KEY in e)
    proj = _strip(doc, set(VOLATILE) | {ADDED_KEY})
    sha = hashlib.sha256(json.dumps(proj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return sha, len(ser), carrying, None


def _rows_projection(blob):
    try:
        doc = json.loads(blob.decode("utf-8"))
    except ValueError as exc:
        return None, None, "body not parseable as JSON: %r" % (exc,)
    rows = doc.get("rows") or []
    proj = []
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            proj.append({"i": i, "NON_DICT_ROW": repr(r)[:80]})
            continue
        item = {"i": i}
        for f in ROW_FIELDS:
            item[f] = r.get(f)
        proj.append(item)
    return doc.get("generation_id"), proj, None


def model_block_stamps():
    from lib.research.coverage import pool_reader

    bucket = pool_reader.POOL_BUCKET
    client = boto3.client("s3", region_name=REGION)
    out = {"bucket": bucket, "prefix": MODEL_BLOCK_PREFIX, "newest": {}}
    for key in STAMP_NAMES:
        base = "%s%s/" % (MODEL_BLOCK_PREFIX, key)
        stamps = []
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=base, Delimiter="/"):
            stamps += [p["Prefix"][len(base):].rstrip("/") for p in (page.get("CommonPrefixes") or [])]
        out["newest"][key] = {"newest_stamp": max(stamps) if stamps else None, "stamp_count": len(stamps)}
    return out


def capture(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    client = boto3.client("lambda", region_name=REGION)
    cfg = client.get_function_configuration(FunctionName=FUNCTION)
    sha = cfg["CodeSha256"]
    at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print("deployed CodeSha256 %s  LastModified %s  captured_at %s" % (sha, cfg["LastModified"], at))

    rows = []

    def record(name, label, path, limb, strict=True, kind=None):
        status, ctype, blob, err = _raw_invoke(client, path)
        digest = hashlib.sha256(blob).hexdigest()
        slug = "%s.%s" % (name.replace("/", "_"), label)
        (out / (slug + ".bin")).write_bytes(blob)
        row = {"name": name, "route": label, "path": path, "limb": limb, "strict": strict,
               "status": status, "content_type": ctype, "bytes": len(blob), "sha256": digest, "error": err}
        extra = ""
        if kind == "timeline":
            psha, slen, carrying, note = _timeline_projection(blob)
            row.update({"timeline_projection_sha256": psha, "series_len": slen,
                        "entries_carrying_found_codes": carrying, "projection_note": note})
            extra = "  proj=%s series=%s carrying=%s" % ((psha or "NONE")[:16], slen, carrying)
        elif kind == "rows":
            gen, proj, note = _rows_projection(blob)
            row.update({"generation_id": gen, "projection_note": note,
                        "row_count": None if proj is None else len(proj)})
            if proj is not None:
                (out / (slug + ".projection.json")).write_text(
                    json.dumps({"generation_id": gen, "rows": proj}, indent=2, sort_keys=True),
                    encoding="utf-8", newline="\n")
                row["projection_sha256"] = hashlib.sha256(
                    json.dumps(proj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
            extra = "  gen=%s rows=%s proj=%s" % (str(gen)[:28], row.get("row_count"),
                                                  (row.get("projection_sha256") or "NONE")[:16])
        rows.append(row)
        print("  %-26s %-9s limb=%-3s status=%s bytes=%-8d sha256=%s%s%s"
              % (name, label, limb, status, len(blob), digest[:16], extra, "  ERR=" + err if err else ""))

    # ---- Limb 6 ----
    for key in NAMES:
        record(key, "print", "%s/security/%s/print" % (ROUTE_PREFIX, key), limb="6")
        record(key, "timeline", "%s/security/%s/timeline" % (ROUTE_PREFIX, key), limb="6", kind="timeline")
    # AC2's own name, carried so the found-codes evidence rides the same capture
    record("AMZN_US_Equity", "timeline", "%s/security/AMZN_US_Equity/timeline" % ROUTE_PREFIX,
           limb="AC2", strict=False, kind="timeline")

    # ---- Limb 7 ----
    for mv, sj in AXES:
        record("rankings_%s_%s" % (mv, sj), "rows",
               "%s/lead-panel/rankings/%s/%s" % (ROUTE_PREFIX, mv, sj), limb="7", kind="rows")

    stamps = model_block_stamps()
    print("  MODEL BLOCK newest stamps (attribution comparand), bucket %s:" % stamps["bucket"])
    for k, v in sorted(stamps["newest"].items()):
        print("    %-16s %s  (%d stamp dirs)" % (k, v["newest_stamp"], v["stamp_count"]))

    bad = [r for r in rows if r["status"] != 200 or r["error"]]
    print("  ROUTE READS: %d, all status 200: %s" % (len(rows), "YES" if not bad else "NO -- %s" % bad))

    manifest = {"captured_at": at, "code_sha256": sha, "last_modified": str(cfg["LastModified"]),
                "function": FUNCTION, "axes": ["%s/%s" % (m, s) for m, s in AXES],
                "row_fields_graded": list(ROW_FIELDS),
                "timeline_graded_modulo": [ADDED_KEY] + list(VOLATILE),
                "model_block_stamps": stamps, "all_200": not bad, "rows": rows}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    print("MANIFEST %s  (%d route reads)" % (out / "manifest.json", len(rows)))
    return manifest


if __name__ == "__main__":
    capture(sys.argv[1])
