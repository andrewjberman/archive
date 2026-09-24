"""AMGT_RESAPP.TO-AMGT-rm-7 AC2 -- the verify-after on the DEPLOYED function.

Two modes, one file, because the BEFORE reads and the AFTER reads must be taken by
the SAME instrument or the comparison is between two scripts rather than two states:

    python verify_after.py --capture-before   # immediately before the apply
    python verify_after.py                    # immediately after the apply (AC2)

WHY L2 IS GRADED ON A NORMALISED SHA AND NOT THE RAW ONE (row AMGT_RESAPP-Z-S254).
The order's AC2 asks that the default path's body sha256 be EQUAL before and after,
"a different sha is the ROLLBACK trigger". The served PDF is NOT byte-deterministic:
it carries a render-time /CreationDate, so two IDENTICAL requests four seconds apart
already differ. Measured on the deployed function 2026-09-24, no deploy involved:
77862 bytes both times, sha256 f29a7918... and b734929c..., differing in EXACTLY ONE
span of those 77862 bytes -- "/CreationDate (D:20260924145119Z)" against
"(D:20260924145123Z)". Raw equality is therefore always FALSE and would roll back a
correct deploy.

So this script prints BOTH and is explicit about which one grades:
  RAW sha        -- printed for the ledger, never graded, expected to differ
  NORMALISED sha -- /CreationDate, /ModDate and /ID replaced by fixed text; this is
                    the DELTA=0 the order actually wants, and it was exercised: the
                    two nondeterministic bodies above normalise to the SAME digest
                    fab9a93f5b4bbc68db79dba266a02422411b43ec7f55ca496474bc5199b3ba0e.

The normalisation touches ONLY those three PDF metadata fields. Any real change to
the rendered document -- a moved figure, a changed number, a dropped section --
still moves the normalised digest, which is what keeps this a DELTA=0 test rather
than a way of passing. The CAT_US_Equity negative control proves that on every run:
it must read DIFFERENT from BA on both comparands, so "equal" is a comparison that
is free to fail.

The print leaf ignores the firm. handler() computes firm_id only to pass the edge
gate, and the print branch calls _print_pack(requested, identity=identity, fmt=...)
with no firm argument (lib/research/api/scoped_amgt.py). The header is supplied
because _firm_id() fails closed with 401 when it is absent.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys

import boto3

FUNCTION = "opal-amgt-scoped-api"
ROUTE_PREFIX = "/api/scoped/amgt"
REGION = "us-east-1"
HERE = os.path.dirname(os.path.abspath(__file__))
BEFORE_PATH = os.path.join(HERE, "before_reads.json")

RICH_MIN_BYTES = 20 * 1024


def _event(security_key, query):
    path = "{0}/security/{1}/print".format(ROUTE_PREFIX, security_key)
    return {
        "rawPath": path,
        "headers": {"x-firm-id": "opal"},
        "requestContext": {"http": {"method": "GET", "path": path}},
        "queryStringParameters": query,
    }


def _normalise(blob):
    """Replace ONLY the render-time PDF metadata. Everything else is compared."""
    out = re.sub(rb"/CreationDate\s*\([^)]*\)", b"/CreationDate(NORMALISED)", blob)
    out = re.sub(rb"/ModDate\s*\([^)]*\)", b"/ModDate(NORMALISED)", out)
    out = re.sub(rb"/ID\s*\[[^\]]*\]", b"/ID[NORMALISED]", out)
    return out


def _invoke(client, security_key, query):
    payload = json.dumps(_event(security_key, query)).encode("utf-8")
    response = client.invoke(FunctionName=FUNCTION, Payload=payload)
    raw = response["Payload"].read()
    if response.get("FunctionError"):
        return {
            "error": response["FunctionError"],
            "raw": raw[:500].decode("utf-8", "replace"),
        }
    parsed = json.loads(raw)
    headers = parsed.get("headers") or {}
    ctype = headers.get("Content-Type") or headers.get("content-type") or ""
    body = parsed.get("body") or ""
    blob = base64.b64decode(body) if parsed.get("isBase64Encoded") else body.encode("utf-8")
    text_head = ""
    if "pdf" not in ctype:
        text_head = blob.decode("utf-8", "replace").split("\n")[0].strip()
    return {
        "status": parsed.get("statusCode"),
        "content_type": ctype,
        "bytes": len(blob),
        "sha_raw": hashlib.sha256(blob).hexdigest(),
        "sha_norm": hashlib.sha256(_normalise(blob)).hexdigest(),
        "first_line": text_head,
        "body_head": body[:300] if "json" in ctype else "",
    }


def _reads(client):
    return {
        "ba_default": _invoke(client, "BA_US_Equity", None),
        "ba_rich": _invoke(client, "BA_US_Equity", {"format": "rich"}),
        "ba_xml": _invoke(client, "BA_US_Equity", {"format": "xml"}),
        "cat_default": _invoke(client, "CAT_US_Equity", None),
    }


def _code_sha(client_lambda):
    return client_lambda.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]


def _show(label, read):
    print("  {0}".format(label))
    if "error" in read:
        print("    FunctionError: {0}".format(read["error"]))
        print("    {0}".format(read["raw"]))
        return
    print("    status={0} content-type={1} bytes={2}".format(
        read["status"], read["content_type"], read["bytes"]))
    print("    sha256 raw       = {0}".format(read["sha_raw"]))
    print("    sha256 normalised= {0}".format(read["sha_norm"]))
    if read.get("first_line"):
        print("    first line       = {0!r}".format(read["first_line"][:120]))
    if read.get("body_head"):
        print("    body             = {0}".format(read["body_head"]))


def capture_before(client, client_lambda):
    print("=== BEFORE READS (pre-apply) ===")
    code_sha = _code_sha(client_lambda)
    print("  CodeSha256 BEFORE = {0}".format(code_sha))
    reads = _reads(client)
    for name in ("ba_default", "ba_rich", "ba_xml", "cat_default"):
        _show(name, reads[name])
    payload = {"code_sha256": code_sha, "reads": reads}
    with open(BEFORE_PATH, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    print("")
    print("WROTE {0}".format(BEFORE_PATH))
    print("Paste CodeSha256 BEFORE and the four raw+normalised shas into the NEVER-2 entry.")
    return 0


def verify_after(client, client_lambda):
    if not os.path.exists(BEFORE_PATH):
        print("REFUSED: {0} is absent. Run --capture-before immediately before the apply;".format(BEFORE_PATH))
        print("         an AFTER read with no BEFORE read is not a comparison.")
        return 2

    with open(BEFORE_PATH, encoding="utf-8") as handle:
        before = json.load(handle)

    after_code = _code_sha(client_lambda)
    after = _reads(client)

    print("=== AFTER READS (post-apply) ===")
    for name in ("ba_default", "ba_rich", "ba_xml", "cat_default"):
        _show(name, after[name])

    b = before["reads"]
    failures = []

    print("")
    print("=== L1: the code moved ===")
    print("  CodeSha256 BEFORE = {0}".format(before["code_sha256"]))
    print("  CodeSha256 AFTER  = {0}".format(after_code))
    moved = after_code != before["code_sha256"]
    print("  MOVED: {0}".format(moved))
    if not moved:
        failures.append("L1: CodeSha256 did not move -- the deploy did not land")

    print("")
    print("=== L2: the pdf default is unchanged (DELTA=0) ===")
    ba_b, ba_a = b["ba_default"], after["ba_default"]
    print("  BEFORE raw        = {0}".format(ba_b.get("sha_raw")))
    print("  AFTER  raw        = {0}".format(ba_a.get("sha_raw")))
    print("  raw EQUAL         = {0}   (NOT GRADED -- /CreationDate makes this false always)".format(
        ba_b.get("sha_raw") == ba_a.get("sha_raw")))
    print("  BEFORE normalised = {0}".format(ba_b.get("sha_norm")))
    print("  AFTER  normalised = {0}".format(ba_a.get("sha_norm")))
    norm_equal = ba_b.get("sha_norm") == ba_a.get("sha_norm")
    print("  normalised EQUAL  = {0}   <-- THIS IS L2".format(norm_equal))
    if ba_a.get("status") != 200 or "application/pdf" not in (ba_a.get("content_type") or ""):
        failures.append("L2: default path is not 200 application/pdf")
    if not norm_equal:
        failures.append("L2: the pdf default CHANGED -- this is the ROLLBACK trigger")

    print("")
    print("=== L2 negative control: CAT must differ from BA ===")
    cat_a = after["cat_default"]
    print("  BA  normalised = {0}".format(ba_a.get("sha_norm")))
    print("  CAT normalised = {0}".format(cat_a.get("sha_norm")))
    differs = cat_a.get("sha_norm") != ba_a.get("sha_norm")
    print("  DIFFERENT: {0}   (if this were False, 'equal' could not fail and L2 would be vacuous)".format(differs))
    if not differs:
        failures.append("CONTROL: CAT and BA read the same -- L2 proves nothing this run")

    print("")
    print("=== L3: rich is served ===")
    rich = after["ba_rich"]
    ctype_ok = "text/markdown" in (rich.get("content_type") or "")
    size_ok = (rich.get("bytes") or 0) > RICH_MIN_BYTES
    head = rich.get("first_line") or ""
    heading_ok = head.startswith("#")
    names_security = "BA" in head
    print("  status        = {0} (want 200)".format(rich.get("status")))
    print("  content-type  = {0} (want text/markdown) -> {1}".format(rich.get("content_type"), ctype_ok))
    print("  bytes         = {0} (want > {1}) -> {2}".format(rich.get("bytes"), RICH_MIN_BYTES, size_ok))
    print("  first line    = {0!r}".format(head[:120]))
    print("  markdown head = {0}; names the security = {1}".format(heading_ok, names_security))
    if rich.get("status") != 200:
        failures.append("L3: format=rich did not return 200")
    if not ctype_ok:
        failures.append("L3: format=rich is not text/markdown")
    if not size_ok:
        failures.append("L3: format=rich body is not larger than 20 KB")
    if not heading_ok:
        failures.append("L3: format=rich first line is not a Markdown heading")
    if not names_security:
        failures.append("L3: format=rich first line does not name the security")

    print("")
    print("=== L3 refusal arm: an unknown format is refused ===")
    xml = after["ba_xml"]
    print("  status = {0} (want 400)".format(xml.get("status")))
    print("  body   = {0}".format(xml.get("body_head")))
    if xml.get("status") != 400:
        failures.append("L3: format=xml did not return 400")

    print("")
    print("=== VERDICT ===")
    if failures:
        for item in failures:
            print("  FAIL: {0}".format(item))
        print("  RESULT: FAIL -- {0} failed check(s) across L1/L2/L3".format(len(failures)))
        return 1
    print("  OK: L1 code moved; L2 pdf default DELTA=0 on the normalised comparand with a")
    print("      live negative control; L3 rich served as text/markdown and xml refused 400.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="rm-7 verify-after on the deployed function")
    parser.add_argument("--capture-before", action="store_true",
                        help="take the BEFORE reads and write before_reads.json")
    args = parser.parse_args()

    client = boto3.client("lambda", region_name=REGION)
    if args.capture_before:
        return capture_before(client, client)
    return verify_after(client, client)


if __name__ == "__main__":
    sys.exit(main())
