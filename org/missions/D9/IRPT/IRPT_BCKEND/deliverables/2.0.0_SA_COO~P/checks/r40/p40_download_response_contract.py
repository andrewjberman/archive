"""Round 40 (IRPT_BCKEND ~P, CTO batch 211, row W101-S13) -- the export-download RESPONSE contract follows the server; the signed
link lives only in the response, never in the receipt.

Usage: python <this file> <repo_root> <criterion_id>
  IB40-1-AC1  docs/contracts/investor-reporting/v1/responses/export-download.response.schema.json, read as JSON, anywhere in its
              tree:
              - a `download_route` object schema whose properties include route, requires_reauthorization, url and expires_at,
                with url and expires_at REQUIRED, url constrained to https (a pattern starting ^https:// or format uri with an
                https pattern) and expires_at a date-time (format date-time, or a pattern ending in Z);
              - an object schema declaring `sha256` (pattern of 64 hex) and `byte_length` (type integer, minimum 0);
              and BOTH ExportReceipt.schema.json copies are byte-unchanged (blob e072d18e59 at the issuance base).
  IB40-1-AC2  infra/aws/lambda/investor-reporting/export/tests/test_download_response_contract.py names
              "export-download.response.schema.json" and "download_route"; at least 2 of its tests pass; and the whole export
              suite passes at least 190 (188 at the base, plus 2), 0 failed. Bounded at 110 s each.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = "docs/contracts/investor-reporting/v1/responses/export-download.response.schema.json"
RECEIPTS = ("infra/aws/lambda/investor-reporting/_contracts/ExportReceipt.schema.json",
            "docs/contracts/investor-reporting/v1/ExportReceipt.schema.json")
RECEIPT_BLOB = "e072d18e59038097190b9d9d3e44b97d0a8d5035"
TEST = "infra/aws/lambda/investor-reporting/export/tests/test_download_response_contract.py"


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB40"))
        sys.exit(1)

    if cid == "IB40-1-AC1":
        s = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
        routes = [d["properties"]["download_route"] for d in walk(s)
                  if isinstance(d.get("properties"), dict) and isinstance(d["properties"].get("download_route"), dict)]
        good_route = False
        for r in routes:
            props, req = r.get("properties") or {}, set(r.get("required") or [])
            if not {"route", "requires_reauthorization", "url", "expires_at"} <= set(props):
                continue
            if not {"url", "expires_at"} <= req:
                continue
            url, exp = props["url"], props["expires_at"]
            https = str(url.get("pattern", "")).startswith("^https://")
            dt = exp.get("format") == "date-time" or str(exp.get("pattern", "")).endswith("Z$")
            if https and dt:
                good_route = True
        if not good_route:
            fail("no download_route with route/requires_reauthorization/url/expires_at, url+expires_at required, url https, "
                 "expires_at a date-time")
        good_facts = False
        for d in walk(s):
            props = d.get("properties") if isinstance(d.get("properties"), dict) else {}
            sha, bl = props.get("sha256"), props.get("byte_length")
            if isinstance(sha, dict) and isinstance(bl, dict):
                if re.fullmatch(r"\^?\[0-9a-f\]\{64\}\$?", str(sha.get("pattern", ""))) and bl.get("type") == "integer" \
                        and bl.get("minimum") == 0:
                    good_facts = True
        if not good_facts:
            fail("no object declares sha256 (64 hex) and byte_length (integer, minimum 0)")
        for rp in RECEIPTS:
            blob = subprocess.run(["git", "hash-object", str(root / rp)], capture_output=True, text=True).stdout.strip()
            if blob != RECEIPT_BLOB:
                fail("%s changed (blob %s): ExportReceipt must stay as it is (batch 211)" % (rp, blob[:10]))
        print("OK: the response-only download_route and the integrity facts are declared; both ExportReceipt copies unchanged")
    elif cid == "IB40-1-AC2":
        t = root / TEST
        if not t.is_file():
            fail("no %s" % TEST)
        src = t.read_text(encoding="utf-8")
        for w in ("export-download.response.schema.json", "download_route"):
            if w not in src:
                fail("the test never names %r" % w)

        def run(target, floor):
            try:
                r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                                   cwd=str(root), capture_output=True, text=True, timeout=110)
            except subprocess.TimeoutExpired:
                fail("pytest exceeded 110 s on %s" % target)
            out = (r.stdout or "") + (r.stderr or "")
            bad = re.search(r"(\d+) (failed|error)", out)
            p = re.search(r"(\d+) passed", out)
            if bad or not p or int(p.group(1)) < floor:
                fail("%s: %s (floor %d)" % (target, bad.group(0) if bad else (p.group(0) if p else out[-200:]), floor))
            return int(p.group(1))
        n1 = run(TEST, 2)
        n2 = run("infra/aws/lambda/investor-reporting/export/tests", 190)
        print("OK: contract tests %d passed; export suite %d passed, 0 failed" % (n1, n2))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
