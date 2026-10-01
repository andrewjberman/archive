"""AMGT_RESAPP round 51, AMGT-zz-8 -- capture the two NEVER-WIDEN limbs the halves grade on OUTPUT.

Limb 6: the served `/print` and `/timeline` OUTPUT on AMD, BA, GOOGL and 1299 HK, captured before and
        byte-equal after. A timeline move is ATTRIBUTED against any AMGT_HARVST data write between the
        captures before it is a ROLLBACK, so /print is graded strict on all four and /timeline strict on
        1299 HK, the other three standing as the attribution comparands.
Limb 7: "a lead-list row's `rank`, `score` or order moves against the pre-apply capture of the SAME
        GENERATION." This CANNOT be graded on raw bytes: zz-5 deliberately adds `name`, `name_source`
        and `places_moved` to every row, so the raw body MUST move and a byte comparison would report a
        violation for the act working as designed. So each axis is captured twice over:
          - the raw bytes (recorded, never the limb's oracle), and
          - a FIELD-SCOPED PROJECTION in served order: (i, ticker, security_key, rank, rank_sort, score)
            plus the body's `generation_id`.
        The projection is what limb 7 is graded on. If `generation_id` MOVES between the captures the
        comparison is VOID for that axis rather than passing quietly -- a new generation is entitled to
        rerank, and reading that as "no move" would be the limb answering a question it cannot see.

All four lead-panel axes are swept, because AC1's population is the four (66 rows), not the single
trending/chatter axis this seat captured in round 50.

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

# Limb 6's four names.
NAMES = ["AMD_US_Equity", "BA_US_Equity", "GOOGL_US_Equity", "1299_HK_Equity"]
STRICT_TIMELINE = {"1299_HK_Equity"}

# Limb 7's population: the four lead-panel axes zz_8_served.py --what rows sweeps.
AXES = [("trending", "chatter"), ("trending", "price"), ("breakout", "chatter"), ("breakout", "price")]

# The fields limb 7 names, plus the identity needed to line rows up. NOT name/name_source/places_moved:
# those are exactly what the act is supposed to add.
ROW_FIELDS = ("ticker", "security_key", "rank", "rank_sort", "score")


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
    """(generation_id, [row-projection], note) -- limb 7's oracle. Never the raw bytes."""
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


def capture(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    client = boto3.client("lambda", region_name=REGION)
    sha = client.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]
    at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print("deployed CodeSha256 %s  captured_at %s" % (sha, at))

    rows = []

    def record(name, label, path, query=None, limb=None, strict=True, project=False):
        status, ctype, blob, err = _raw_invoke(client, path, query)
        digest = hashlib.sha256(blob).hexdigest()
        slug = "%s.%s" % (name.replace("/", "_"), label)
        (out / (slug + ".bin")).write_bytes(blob)
        row = {
            "name": name, "route": label, "path": path, "query": query, "limb": limb,
            "strict": strict, "status": status, "content_type": ctype,
            "bytes": len(blob), "sha256": digest, "error": err,
        }
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
            named = 0
            pm_int = 0
            try:
                doc = json.loads(blob.decode("utf-8"))
                for r in (doc.get("rows") or []):
                    if isinstance(r, dict):
                        named += 1 if r.get("name") else 0
                        pm_int += 1 if isinstance(r.get("places_moved"), int) else 0
            except ValueError:
                pass
            row["named"] = named
            row["places_moved_int"] = pm_int
        rows.append(row)
        extra = ""
        if project:
            extra = "  gen=%s rows=%s named=%d pm_int=%d proj=%s" % (
                str(row.get("generation_id"))[:28], row.get("row_count"), row["named"], row["places_moved_int"],
                (row.get("projection_sha256") or "NONE")[:16])
        print("  %-16s %-14s limb=%-4s strict=%-5s status=%s bytes=%-8d sha256=%s%s%s"
              % (name, label, limb, strict, status, len(blob), digest[:16], extra,
                 "  ERR=" + err if err else ""))

    # ---- Limb 6 ----
    for key in NAMES:
        record(key, "print", "%s/security/%s/print" % (ROUTE_PREFIX, key), None, limb="6", strict=True)
        record(key, "timeline", "%s/security/%s/timeline" % (ROUTE_PREFIX, key), None,
               limb="6", strict=(key in STRICT_TIMELINE))

    # ---- Limb 7: all four axes, projection-graded ----
    for mv, sj in AXES:
        record("rankings_%s_%s" % (mv, sj), "rows",
               "%s/lead-panel/rankings/%s/%s" % (ROUTE_PREFIX, mv, sj),
               None, limb="7", strict=True, project=True)

    total_named = sum(r.get("named", 0) for r in rows if r.get("limb") == "7")
    total_rows = sum(r.get("row_count") or 0 for r in rows if r.get("limb") == "7")
    total_pm = sum(r.get("places_moved_int", 0) for r in rows if r.get("limb") == "7")
    print("  LEAD-LIST TOTALS across the four axes: rows %d, named %d, places_moved int %d"
          % (total_rows, total_named, total_pm))

    manifest = {
        "captured_at": at, "code_sha256": sha, "function": FUNCTION,
        "axes": ["%s/%s" % (m, s) for m, s in AXES],
        "row_fields_graded": list(ROW_FIELDS),
        "lead_list_totals": {"rows": total_rows, "named": total_named, "places_moved_int": total_pm},
        "rows": rows,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    print("MANIFEST %s  (%d route reads)" % (out / "manifest.json", len(rows)))
    return manifest


if __name__ == "__main__":
    capture(sys.argv[1])
