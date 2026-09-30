"""AMGT_RESAPP round 52, AMGT-ab-6 -- capture the never-widen limbs the halves grade on OUTPUT.

Adapted from round 51's zz8-captures/capture_limbs_6_7.py. The limb NUMBERS moved this round, and
one limb is new:

Limb 5: the served `/print` and `/timeline` OUTPUT on AMD, BA, GOOGL and 1299 HK, captured before and
        byte-equal after. A `/print` move on a name whose NEWEST MODEL BLOCK STAMP moved between the
        captures is attributed to CORPUS y-4 before it is a ROLLBACK (CTO half condition 1), and a
        `/timeline` move is attributed to any AMGT_HARVST data write the same way. So this script also
        records, per name, the newest `derived/model_block/<key>/<ts>/model_block.json` timestamp --
        WITHOUT it the attribution the CTO half grants cannot be exercised and a y-4 unit-label change
        would read as this build's rollback trigger.

Limb 6: "a lead-list row's `rank`, `score`, ORDER, `name` or `places_moved` moves against the pre-apply
        capture of the SAME GENERATION." Graded on a FIELD-SCOPED PROJECTION, never raw bytes.
        NOTE the difference from round 51: `name` and `places_moved` were what zz-5 was ADDING then, so
        zz-8 deliberately EXCLUDED them from its projection. They are landed and stable now and this
        round's half names them, so they are IN the graded set here. Order is graded by the row index
        `i` carried in the projection. If `generation_id` MOVES the comparison is VOID for that axis
        rather than passing quietly -- a new generation is entitled to rerank.

Limb 7: "ASML's served drafted sections (`read_drafted_sections`) differ before vs after THE SPLICE."
        The oracle is the `/thesis` response's drafting block (the adapter merges
        `read_drafted_sections(resolved_key)` into the /thesis bundle at :2315 of the pin). Limb 7 is
        graded ACROSS THE SPLICE, not across the build, so this script is run at THREE points and the
        limb-7 comparison is post-apply/pre-splice vs post-splice.

Also captured, as the AC baselines and their negative control: `/thesis` for 6501_JP (AC1),
AZN_LN / ADBE_US / AMD_US (AC2) and ASML (AC3's chart + limb 7).

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

# Limb 5's four names.
NAMES = ["AMD_US_Equity", "BA_US_Equity", "GOOGL_US_Equity", "1299_HK_Equity"]
STRICT_TIMELINE = {"1299_HK_Equity"}

# Limb 6's population: the four lead-panel axes.
AXES = [("trending", "chatter"), ("trending", "price"), ("breakout", "chatter"), ("breakout", "price")]

# The fields THIS round's half names, plus the identity needed to line rows up. `name` and
# `places_moved` are IN this round (they were the act under test in round 51, they are stable now).
ROW_FIELDS = ("ticker", "security_key", "rank", "rank_sort", "score", "name", "places_moved")

# /thesis reads: limb 7 (ASML) and the AC baselines.
THESIS_NAMES = ["ASML_NA_Equity", "6501_JP_Equity", "AZN_LN_Equity", "ADBE_US_Equity", "AMD_US_Equity"]

# The drafting block limb 7 grades -- the keys read_drafted_sections merges into the /thesis bundle.
DRAFTING_KEYS = ("drafted_sections", "drafting_status", "drafting_source", "drafting_reason")

# Limb 5's attribution comparand.
MODEL_BLOCK_PREFIX = "derived/model_block/"
STAMP_NAMES = NAMES + ["ASML_NA_Equity"]


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


def _projection(blob):
    """(generation_id, [row-projection], note) -- limb 6's oracle. Never the raw bytes."""
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


def _drafting_block(blob):
    """Limb 7's oracle -- the drafting keys of the /thesis bundle, canonicalised."""
    try:
        doc = json.loads(blob.decode("utf-8"))
    except ValueError as exc:
        return None, "body not parseable as JSON: %r" % (exc,)
    return {k: doc.get(k) for k in DRAFTING_KEYS}, None


def _chart(blob):
    """AC3's read -- thesis_driver_chart source and points_count, recorded beside limb 7."""
    try:
        doc = json.loads(blob.decode("utf-8"))
    except ValueError:
        return None
    ch = doc.get("thesis_driver_chart")
    if not isinstance(ch, dict):
        return {"status": None, "source": None, "points_count": None}
    pts = ch.get("points")
    return {
        "status": ch.get("status"),
        "source": ch.get("source"),
        "points_count": len(pts) if isinstance(pts, list) else ch.get("points_count"),
    }


def _dossier_fields_digest(blob):
    """AC1/AC2's baseline -- the dossier_fields block, recorded so the act's move is visible."""
    try:
        doc = json.loads(blob.decode("utf-8"))
    except ValueError:
        return None
    df = doc.get("dossier_fields")
    if not isinstance(df, dict):
        return {"present": False, "raw": repr(df)[:120]}
    ps = df.get("pack_shape")
    return {
        "present": True,
        "status": df.get("status"),
        "keys": sorted(df.keys()),
        "pack_shape": ps,
        "sha256": hashlib.sha256(json.dumps(df, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
    }


def model_block_stamps():
    """Newest `derived/model_block/<key>/<ts>/` per name -- limb 5's attribution comparand.
    The bucket is DERIVED from the adapter's own pool reader, never typed here."""
    from lib.research.coverage import pool_reader

    bucket = pool_reader.POOL_BUCKET
    client = boto3.client("s3", region_name=REGION)
    out = {"bucket": bucket, "prefix": MODEL_BLOCK_PREFIX, "newest": {}}
    for key in STAMP_NAMES:
        base = "%s%s/" % (MODEL_BLOCK_PREFIX, key)
        stamps = []
        for page in client.get_paginator("list_objects_v2").paginate(
            Bucket=bucket, Prefix=base, Delimiter="/"
        ):
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

    def record(name, label, path, query=None, limb=None, strict=True, project=False, thesis=False):
        status, ctype, blob, err = _raw_invoke(client, path, query)
        digest = hashlib.sha256(blob).hexdigest()
        slug = "%s.%s" % (name.replace("/", "_"), label)
        (out / (slug + ".bin")).write_bytes(blob)
        row = {
            "name": name, "route": label, "path": path, "query": query, "limb": limb,
            "strict": strict, "status": status, "content_type": ctype,
            "bytes": len(blob), "sha256": digest, "error": err,
        }
        extra = ""
        if project:
            gen, proj, note = _projection(blob)
            row["generation_id"] = gen
            row["projection_note"] = note
            row["row_count"] = None if proj is None else len(proj)
            if proj is not None:
                (out / (slug + ".projection.json")).write_text(
                    json.dumps({"generation_id": gen, "rows": proj}, indent=2, sort_keys=True),
                    encoding="utf-8", newline="\n")
                row["projection_sha256"] = hashlib.sha256(
                    json.dumps(proj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
            extra = "  gen=%s rows=%s proj=%s" % (
                str(row.get("generation_id"))[:28], row.get("row_count"),
                (row.get("projection_sha256") or "NONE")[:16])
        if thesis:
            block, note = _drafting_block(blob)
            row["drafting_note"] = note
            if block is not None:
                (out / (slug + ".drafting.json")).write_text(
                    json.dumps(block, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
                row["drafting_sha256"] = hashlib.sha256(
                    json.dumps(block, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
                sec = block.get("drafted_sections")
                row["drafted_section_count"] = len(sec) if isinstance(sec, list) else None
                row["drafting_status"] = block.get("drafting_status")
            row["chart"] = _chart(blob)
            row["dossier_fields"] = _dossier_fields_digest(blob)
            extra = "  draft=%s secs=%s chart=%s/%s df=%s" % (
                (row.get("drafting_sha256") or "NONE")[:16], row.get("drafted_section_count"),
                (row.get("chart") or {}).get("source"), (row.get("chart") or {}).get("points_count"),
                (row.get("dossier_fields") or {}).get("status"))
        rows.append(row)
        print("  %-16s %-10s limb=%-4s strict=%-5s status=%s bytes=%-8d sha256=%s%s%s"
              % (name, label, limb, strict, status, len(blob), digest[:16], extra,
                 "  ERR=" + err if err else ""))

    # ---- Limb 5 ----
    for key in NAMES:
        record(key, "print", "%s/security/%s/print" % (ROUTE_PREFIX, key), None, limb="5", strict=True)
        record(key, "timeline", "%s/security/%s/timeline" % (ROUTE_PREFIX, key), None,
               limb="5", strict=(key in STRICT_TIMELINE))

    # ---- Limb 6: all four axes, projection-graded ----
    for mv, sj in AXES:
        record("rankings_%s_%s" % (mv, sj), "rows",
               "%s/lead-panel/rankings/%s/%s" % (ROUTE_PREFIX, mv, sj),
               None, limb="6", strict=True, project=True)

    # ---- Limb 7 + the AC baselines ----
    for key in THESIS_NAMES:
        record(key, "thesis", "%s/security/%s/thesis" % (ROUTE_PREFIX, key), None,
               limb=("7" if key == "ASML_NA_Equity" else "AC"), strict=(key == "ASML_NA_Equity"),
               thesis=True)

    stamps = model_block_stamps()
    print("  MODEL BLOCK newest stamps (limb 5 attribution comparand), bucket %s:" % stamps["bucket"])
    for k, v in sorted(stamps["newest"].items()):
        print("    %-16s %s  (%d stamp dirs)" % (k, v["newest_stamp"], v["stamp_count"]))

    bad = [r for r in rows if r["status"] != 200 or r["error"]]
    print("  ROUTE READS: %d, all status 200: %s" % (len(rows), "YES" if not bad else "NO -- %s" % bad))

    manifest = {
        "captured_at": at, "code_sha256": sha, "last_modified": str(cfg["LastModified"]),
        "function": FUNCTION,
        "axes": ["%s/%s" % (m, s) for m, s in AXES],
        "row_fields_graded": list(ROW_FIELDS),
        "drafting_keys_graded": list(DRAFTING_KEYS),
        "model_block_stamps": stamps,
        "all_200": not bad,
        "rows": rows,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    print("MANIFEST %s  (%d route reads)" % (out / "manifest.json", len(rows)))
    return manifest


if __name__ == "__main__":
    capture(sys.argv[1])
