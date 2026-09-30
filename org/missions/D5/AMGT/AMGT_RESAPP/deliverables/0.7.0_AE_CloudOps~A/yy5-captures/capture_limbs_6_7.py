"""AMGT_RESAPP round 50, AMGT-yy-5 -- capture the two NEVER-WIDEN limbs the halves grade on OUTPUT.

Limb 6: the served `/print` OUTPUT and `/timeline` OUTPUT on AMD, BA, GOOGL and 1299 HK, captured
        before and byte-equal after. An AMD/BA/GOOGL TIMELINE move is ATTRIBUTED against any
        AMGT_HARVST data write after the capture before it is a ROLLBACK (COO half limb 6; CTO half
        condition 4 records that HARVST l-2's event put moved only 992_HK, AMZN and HD, so none of
        the four captured names has a changed event and the ROLLBACK rule applies as written).
        Strict byte-equality is therefore graded on /print for all four and on /timeline for 1299 HK;
        the other three timelines are captured as the attribution comparands.
Limb 7: the served `/lead-panel/rankings/trending/chatter` rows and `/lead-panel/timeseries/trending/
        chatter` series, equal across the act, `generated_at` excepted.

WHY THE TICKERS ARE PINNED: the timeseries route takes `?tickers=`, and round 49's AC2 derived that
list from the FIRST FIVE rankings rows. Re-deriving it on the after-run would make the comparison
measure the ranking's own drift instead of the function's behaviour -- a moved ranking would change
the tickers asked, and the series would differ for a reason limb 7 does not name. So the before-run
writes the list it used into the manifest and the after-run is given the SAME list via --tickers.

Derived from this seat's round-49 capture_limbs_4_5_6.py (limbs renumbered; the timeseries arm is NEW
here, because round 49's limb 6 graded rankings only and round 50's limb 7 adds the series).

`/timeline/day/{date}` is captured as a NON-LIMB comparand only: the COO half's expected-outcome names
it among the routes that stay unchanged, but no limb grades it, so a move there is a finding to report,
never a rollback trigger. Its date is drawn from each name's own /timeline body, so the read is
reproducible across both runs.

READ-ONLY: `lambda:Invoke` of the DEPLOYED opal-amgt-scoped-api only. No AWS write call of any kind.

usage (repo root):  python <this> <out_dir> [--tickers T1,T2,...]
"""
from __future__ import annotations

import argparse
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

# The four names the COO half's limb 6 names.
NAMES = ["AMD_US_Equity", "BA_US_Equity", "GOOGL_US_Equity", "1299_HK_Equity"]

# Limb 6 grades STRICT timeline byte-equality on this one only; the others are attribution comparands.
STRICT_TIMELINE = {"1299_HK_Equity"}

# Round 49 AC2's unheld control, kept so the pinned list matches the established read.
UNHELD = "ZZZNOTHELD US"


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


def _scrub(node):
    """Drop every `generated_at` at ANY depth -- limb 7 excepts the field, not one position of it."""
    if isinstance(node, dict):
        return {k: _scrub(v) for k, v in node.items() if k != "generated_at"}
    if isinstance(node, list):
        return [_scrub(v) for v in node]
    return node


def _normalise(blob):
    """Return (normalised_bytes, note). A body that is not JSON is itself the finding, not an error."""
    try:
        doc = json.loads(blob.decode("utf-8"))
    except ValueError as exc:
        return None, "body not normalisable as JSON: %r" % (exc,)
    return json.dumps(_scrub(doc), sort_keys=True, separators=(",", ":")).encode("utf-8"), None


def _first_date(node, depth=0):
    """The first value under a key named `date` that looks like YYYY-MM-DD, for the /timeline/day read."""
    if depth > 8:
        return None
    if isinstance(node, dict):
        value = node.get("date")
        if isinstance(value, str) and len(value) == 10 and value[4] == "-" and value[7] == "-":
            return value
        for item in node.values():
            found = _first_date(item, depth + 1)
            if found:
                return found
    elif isinstance(node, list):
        for item in node:
            found = _first_date(item, depth + 1)
            if found:
                return found
    return None


def capture(out_dir, pinned_tickers=None):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    client = boto3.client("lambda", region_name=REGION)
    sha = client.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]
    at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print("deployed CodeSha256 %s  captured_at %s" % (sha, at))
    print("tickers: %s" % ("PINNED (given)" if pinned_tickers else "DERIVED from rankings rows 1-5"))

    rows = []

    def record(name, label, path, query=None, limb=None, strict=True, normalise=False):
        status, ctype, blob, err = _raw_invoke(client, path, query)
        digest = hashlib.sha256(blob).hexdigest()
        slug = "%s.%s" % (name.replace("/", "_"), label)
        (out / (slug + ".bin")).write_bytes(blob)
        row = {
            "name": name, "route": label, "path": path, "query": query, "limb": limb,
            "strict": strict, "status": status, "content_type": ctype,
            "bytes": len(blob), "sha256": digest, "error": err,
        }
        if normalise:
            norm, note = _normalise(blob)
            if norm is not None:
                (out / (slug + ".normalised.json")).write_bytes(norm)
                row["sha256_normalised"] = hashlib.sha256(norm).hexdigest()
            else:
                row["sha256_normalised"] = None
                row["normalise_note"] = note
                print("  NOTE %s: %s" % (slug, note))
        rows.append(row)
        print("  %-16s %-14s limb=%-4s strict=%-5s status=%s bytes=%-8d sha256=%s%s%s"
              % (name, label, limb, strict, status, len(blob), digest[:16],
                 "  norm=" + (row.get("sha256_normalised") or "NONE")[:16] if normalise else "",
                 "  ERR=" + err if err else ""))
        return blob

    # ---- Limb 6: /print strict on all four; /timeline strict on 1299 HK only ----
    for key in NAMES:
        record(key, "print", "%s/security/%s/print" % (ROUTE_PREFIX, key), None, limb="6", strict=True)
        timeline_blob = record(key, "timeline", "%s/security/%s/timeline" % (ROUTE_PREFIX, key), None,
                               limb="6", strict=(key in STRICT_TIMELINE))
        # NON-LIMB comparand: one /timeline/day read per name, dated from that name's own timeline.
        day = None
        try:
            day = _first_date(json.loads(timeline_blob.decode("utf-8")))
        except ValueError:
            pass
        if day:
            record(key, "timeline_day", "%s/security/%s/timeline/day/%s" % (ROUTE_PREFIX, key, day),
                   None, limb=None, strict=False)
        else:
            print("  %-16s %-14s limb=-    SKIPPED -- no date found in its /timeline body" % (key, "timeline_day"))
            rows.append({"name": key, "route": "timeline_day", "limb": None, "strict": False,
                         "skipped": "no date in /timeline body"})

    # ---- Limb 7: rankings rows, then the series over the PINNED tickers ----
    rankings_blob = record("rankings", "trending_chatter",
                           "%s/lead-panel/rankings/trending/chatter" % ROUTE_PREFIX,
                           None, limb="7", strict=True, normalise=True)

    if pinned_tickers:
        tickers = list(pinned_tickers)
    else:
        try:
            doc = json.loads(rankings_blob.decode("utf-8"))
        except ValueError:
            doc = {}
        tickers = [str(r.get("ticker")) for r in (doc.get("rows") or [])[:5] if r.get("ticker")] + [UNHELD]
    print("  tickers asked (%d): %s" % (len(tickers), ",".join(tickers)))

    record("timeseries", "trending_chatter",
           "%s/lead-panel/timeseries/trending/chatter" % ROUTE_PREFIX,
           {"tickers": ",".join(tickers)}, limb="7", strict=True, normalise=True)

    manifest = {
        "captured_at": at,
        "code_sha256": sha,
        "function": FUNCTION,
        "tickers": tickers,
        "tickers_source": "PINNED (given on the command line)" if pinned_tickers else "DERIVED from rankings rows 1-5",
        "rows": rows,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    print("MANIFEST %s  (%d route reads)" % (out / "manifest.json", len(rows)))
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--tickers", default="", help="comma list; PIN the before-run's list on the after-run")
    a = ap.parse_args()
    pinned = [t for t in a.tickers.split(",") if t] or None
    capture(a.out_dir, pinned)
    return 0


if __name__ == "__main__":
    sys.exit(main())
