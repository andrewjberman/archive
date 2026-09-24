"""AMGT_RESAPP.TO-AMGT-rm-7 AC2 -- the verify-after on the DEPLOYED function.

Two modes, one file, because the BEFORE reads and the AFTER reads must be taken by
the SAME instrument or the comparison is between two scripts rather than two states:

    python verify_after.py --capture-before   # immediately before the apply
    python verify_after.py                    # immediately after the apply (AC2)

THREE COMPARANDS ARE COMPUTED FOR EVERY PDF AND ALL THREE ARE PRINTED. Which one
GRADES L2 is --l2-comparand, so the issuer's ruling is a one-word change and never a
re-run. Why there are three, in the order they were found to be insufficient:

  raw          sha256 of the served bytes. The order's original L2. UNUSABLE: the
               renderer stamps a wall-clock /CreationDate, so two IDENTICAL requests
               four seconds apart already differ (measured 2026-09-24, 77862 bytes
               both, one differing span, no deploy involved). Always false, and the
               order made a different sha the ROLLBACK trigger. Row Z-S254.

  normalised   sha256 after replacing /CreationDate, /ModDate, /ID with fixed text.
               Fixes the stamp, and is what issuer amendment 2 (b) mandates. ALSO
               UNUSABLE ACROSS THIS PARTICULAR DEPLOY: rl-10 sets
               PdfPages(metadata={"CreationDate": None}), which REMOVES the entry
               rather than fixing it (render_pack.py:295 and its own comment). So the
               BEFORE pdf has the field and the AFTER pdf does not, and dropping those
               bytes shifts every xref offset after them. Measured by simulating that
               exact shape: fab9a93f... -> 9895fc74..., SURVIVES False.

  content      sha256 over page count plus each page's DECODED CONTENT STREAM -- the
               drawing program itself, text and vector chart operators alike. Carries
               no file-level metadata and no byte offsets, so neither hazard reaches
               it. Exercised on all three arms: identical across two live invokes that
               differ in the stamp; identical across the metadata strip that moved the
               file 77862 -> 77388; and DIFFERENT for CAT_US_Equity, so "equal" is
               still free to fail. This is the default.

  content is NOT a weaker test of the property L2 exists to protect. A moved figure, a
  changed number or a dropped section all move the content stream. Only metadata and
  byte offsets are excluded -- which is precisely what the pin changes and precisely
  what a DELTA=0 claim should not be hostage to.

The print leaf ignores the firm. handler() computes firm_id only to pass the edge
gate, and the print branch calls _print_pack(requested, identity=identity, fmt=...)
with no firm argument. The header is supplied because _firm_id() fails closed with a
401 when it is absent.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
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
COMPARANDS = ("content", "normalised", "raw")
SHA_FIELD = {"content": "sha_content", "normalised": "sha_norm", "raw": "sha_raw"}


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
    return re.sub(rb"/ID\s*\[[^\]]*\]", b"/ID[NORMALISED]", out)


def _content_digest(blob):
    """Page count + each page's decoded content stream. No metadata, no xref offsets.

    Returns None rather than raising if the body is not a parseable PDF, so a
    non-pdf response is reported as such instead of crashing the verify.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        reader = PdfReader(io.BytesIO(blob))
        hasher = hashlib.sha256()
        hasher.update("pages={0}".format(len(reader.pages)).encode("ascii"))
        for page in reader.pages:
            contents = page.get_contents()
            data = contents.get_data() if contents is not None else b""
            hasher.update(hashlib.sha256(data).digest())
        return hasher.hexdigest()
    except Exception:
        return None


def _invoke(client, security_key, query):
    payload = json.dumps(_event(security_key, query)).encode("utf-8")
    response = client.invoke(FunctionName=FUNCTION, Payload=payload)
    raw = response["Payload"].read()
    if response.get("FunctionError"):
        return {"error": response["FunctionError"], "raw": raw[:500].decode("utf-8", "replace")}
    parsed = json.loads(raw)
    headers = parsed.get("headers") or {}
    ctype = headers.get("Content-Type") or headers.get("content-type") or ""
    body = parsed.get("body") or ""
    blob = base64.b64decode(body) if parsed.get("isBase64Encoded") else body.encode("utf-8")
    is_pdf = "pdf" in ctype
    return {
        "status": parsed.get("statusCode"),
        "content_type": ctype,
        "bytes": len(blob),
        "sha_raw": hashlib.sha256(blob).hexdigest(),
        "sha_norm": hashlib.sha256(_normalise(blob)).hexdigest(),
        "sha_content": _content_digest(blob) if is_pdf else None,
        "has_creationdate": bool(re.search(rb"/CreationDate", blob)) if is_pdf else None,
        "first_line": "" if is_pdf else blob.decode("utf-8", "replace").split("\n")[0].strip(),
        "body_head": body[:300] if "json" in ctype else "",
    }


def _reads(client):
    return {
        "ba_default": _invoke(client, "BA_US_Equity", None),
        "ba_rich": _invoke(client, "BA_US_Equity", {"format": "rich"}),
        "ba_xml": _invoke(client, "BA_US_Equity", {"format": "xml"}),
        "cat_default": _invoke(client, "CAT_US_Equity", None),
    }


def _code_sha(client):
    return client.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]


def _show(label, read):
    print("  {0}".format(label))
    if "error" in read:
        print("    FunctionError: {0}".format(read["error"]))
        print("    {0}".format(read["raw"]))
        return
    print("    status={0} content-type={1} bytes={2}".format(
        read["status"], read["content_type"], read["bytes"]))
    print("    sha raw        = {0}".format(read["sha_raw"]))
    print("    sha normalised = {0}".format(read["sha_norm"]))
    print("    sha content    = {0}".format(read["sha_content"]))
    if read.get("has_creationdate") is not None:
        print("    /CreationDate present = {0}".format(read["has_creationdate"]))
    if read.get("first_line"):
        print("    first line     = {0!r}".format(read["first_line"][:120]))
    if read.get("body_head"):
        print("    body           = {0}".format(read["body_head"]))


def capture_before(client):
    print("=== BEFORE READS (pre-apply) ===")
    code_sha = _code_sha(client)
    print("  CodeSha256 BEFORE = {0}".format(code_sha))
    reads = _reads(client)
    for name in ("ba_default", "ba_rich", "ba_xml", "cat_default"):
        _show(name, reads[name])
    with open(BEFORE_PATH, "w", encoding="utf-8", newline="\n") as handle:
        json.dump({"code_sha256": code_sha, "reads": reads}, handle, indent=2)
        handle.write("\n")
    print("")
    print("WROTE {0}".format(BEFORE_PATH))
    print("Paste CodeSha256 BEFORE and all three shas into the NEVER-2 entry.")
    return 0


def verify_after(client, comparand):
    if not os.path.exists(BEFORE_PATH):
        print("REFUSED: {0} is absent. Run --capture-before immediately before the apply;".format(BEFORE_PATH))
        print("         an AFTER read with no BEFORE read is not a comparison.")
        return 2

    with open(BEFORE_PATH, encoding="utf-8") as handle:
        before = json.load(handle)

    after_code = _code_sha(client)
    after = _reads(client)
    b = before["reads"]
    failures = []

    print("=== AFTER READS (post-apply) ===")
    for name in ("ba_default", "ba_rich", "ba_xml", "cat_default"):
        _show(name, after[name])

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
    field = SHA_FIELD[comparand]
    for name in COMPARANDS:
        key = SHA_FIELD[name]
        mark = "  <-- GRADED" if name == comparand else ""
        print("  {0:<11} BEFORE {1}".format(name, ba_b.get(key)))
        print("  {0:<11} AFTER  {1}   EQUAL={2}{3}".format(
            name, ba_a.get(key), ba_b.get(key) == ba_a.get(key), mark))
    print("  /CreationDate present BEFORE={0} AFTER={1}  (rl-10 removes it; that is expected)".format(
        ba_b.get("has_creationdate"), ba_a.get("has_creationdate")))

    if ba_a.get("status") != 200 or "application/pdf" not in (ba_a.get("content_type") or ""):
        failures.append("L2: default path is not 200 application/pdf")
    if ba_a.get(field) is None or ba_b.get(field) is None:
        failures.append("L2: the {0} comparand is unavailable on one side".format(comparand))
    elif ba_b.get(field) != ba_a.get(field):
        failures.append("L2: the pdf default CHANGED on the {0} comparand -- ROLLBACK trigger".format(comparand))

    print("")
    print("=== L2 negative control: CAT must differ from BA ===")
    cat_a = after["cat_default"]
    print("  BA  {0} = {1}".format(comparand, ba_a.get(field)))
    print("  CAT {0} = {1}".format(comparand, cat_a.get(field)))
    differs = cat_a.get(field) != ba_a.get(field)
    print("  DIFFERENT: {0}   (if False, 'equal' could not fail and L2 would be vacuous)".format(differs))
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
    print("=== VERDICT (L2 graded on: {0}) ===".format(comparand))
    if failures:
        for item in failures:
            print("  FAIL: {0}".format(item))
        print("  RESULT: FAIL -- {0} failed check(s) across L1/L2/L3".format(len(failures)))
        return 1
    print("  OK: L1 code moved; L2 pdf default DELTA=0 on the {0} comparand with a live".format(comparand))
    print("      negative control; L3 rich served as text/markdown and xml refused 400.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="rm-7 verify-after on the deployed function")
    parser.add_argument("--capture-before", action="store_true",
                        help="take the BEFORE reads and write before_reads.json")
    parser.add_argument("--l2-comparand", choices=COMPARANDS, default="content",
                        help="which comparand GRADES L2 (all three are always printed)")
    args = parser.parse_args()

    client = boto3.client("lambda", region_name=REGION)
    if args.capture_before:
        return capture_before(client)
    return verify_after(client, args.l2_comparand)


if __name__ == "__main__":
    sys.exit(main())
