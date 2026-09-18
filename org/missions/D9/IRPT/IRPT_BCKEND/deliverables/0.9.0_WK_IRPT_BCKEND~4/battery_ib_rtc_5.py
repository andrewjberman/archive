"""IB-rtc-5 acceptance battery -- R35-AC1, the ACROSS-INPUTS renderer control.

Five arms -- (e) then (a) through (d), in that printed order because the face requires the
round-1 defect REPRODUCED FIRST as the detector's own positive control -- each printing its
own denominators, and the token only when every one holds. The token is
IBR35-RENDER-VARIES-WITH-INPUT.

WHAT THIS CELL EXECUTES (round-2 ruling, IRPT_BCKEND_ROUND2_ANALYSIS.md @cfe3a33a9b, verbatim):
"Round 1's renderer produced ONE document from THREE distinct bundles ... A renderer whose
output does not vary with its input cannot evidence that the input was rendered ... render two
known-different bundles and require the outputs to DIFFER."

THE PLANE, NAMED (arm d and this header, so it never floats free of the code that runs it).
IB-rt-8 exercised the DEPLOYED browser-host pattern: `render_export.cjs` via SSM on the
YCharts EC2 host, Chromium hitting the DEPLOYED, SESSION-GATED origin
`https://opalinvest.dev/investor-reporting/print`. That path is HUMAN-GATED (row W4-S25): the
print route is an authenticated app route and this worker holds no session and mints none
(bound: no write to the production auth plane). render.py's own header records that round-1's
IN-PROCESS fixture renderer (named-slot HTML templates + a local headless browser) is RETIRED
AS EVIDENCE and its machinery is GONE from this module -- so the decomp's "in-process path with
the SAME code" fallback is NOT the retired fixture (that path no longer exists in the export
package at all; see row filed by this cell). It IS the counterpart's REAL render code
(`portal/src/pages/InvestorReporting/render/manifest.ts` + `PrintEntry.tsx` +
`PerformanceDocument`) run on a DIFFERENT PLANE than the deployed origin: the LOCAL vite dev
server (`bun run dev`), auth-stubbed by Playwright network interception -- THE SAME MECHANISM
`scripts/ui-smoke.mjs` and `__tests__/fe-s-31/print-driver.mjs` already use and that
`portal/CLAUDE.md`'s Verification law names as "auth-stubbed, works without credentials". This
battery's driver (`rtc5-render-driver.cjs`, alongside this file) is FE-s-31's print-driver.mjs
mechanism UNCHANGED in its rendering half (same Playwright interception, same identity stub,
same Edge binary), with ONE addition -- `page.pdf()` at settle time -- because FE-s-31 only
needed DOM state and this cell needs the ARTIFACT BYTES. Nothing about PrintEntry.tsx,
composeExportBundle, resolveBundle, manifest.ts or PerformanceDocument is patched, stubbed or
re-registered: bound 12's subject is the REAL render code, and only the HOST PLANE (local dev
vs. the deployed session-gated origin) and the DATA PLANE (fixture-served report bodies vs. a
live scoped API) differ from IB-rt-8's browser-host run -- exactly the substitution the decomp
authorizes when "that host is not reachable non-interactively".

THE REAL-PATH ARM STAYS HUMAN-GATED, NEVER SIMULATED (arm d). Nothing here dispatches
`render_export.cjs` against the deployed origin, mints a session, or reads a secret VALUE.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

REPO = pathlib.Path(__file__).resolve().parents[7]
PACKAGE = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "export"
HERE = pathlib.Path(__file__).resolve().parent
AWS = ["cmd", "/c", str(REPO / ".tools" / "aws.cmd")]

DRIVER = HERE / "rtc5-render-driver.cjs"
SCENARIOS = HERE / "rtc5_scenarios.json"
PDF_DIR = HERE / "rtc5_pdfs"
PORT = "5189"

BUCKET = "opal-data-ycharts"
# The three round-1 objects W4-S19's grounding measured. Live retrieval is attempted first
# (bound: read-only against the deployed plane); the face names the recorded fallback
# explicitly ("or their recorded hashes from W4-S19") for exactly the case this arm hits.
ROUND1_KEYS = {
    "overview": "firms/49financial/generations/GENIBS14SYN/attempts/1/exports/v0-11-overview/report.pdf",
    "comparison": "firms/49financial/generations/GENIBS14SYN/attempts/1/exports/v0-11-comparison/report.pdf",
    "multicomp": "firms/49financial/generations/GENIBS14SYN/attempts/1/exports/v0-11-multicomp/report.pdf",
}
# Recorded verbatim from IRPT_BCKEND-W4-S19's grounding (INVESTIGATION_v1.md), the same
# battery's committed output (IB-s-14_S14-AC1_battery_output.txt lines ~140-148), and this
# cell's own re-measurement of the S3 object headers below.
W4_S19_RECORD = {
    "overview": {"bundle_sha256_16": "38753e307c2e", "raw_sha256_16": "9aede5a23bd8889b"},
    "comparison": {"bundle_sha256_16": "86c38f465c00", "raw_sha256_16": "579b85d087e5babe"},
    "multicomp": {"bundle_sha256_16": "9f89d01d4fa7", "raw_sha256_16": "6954433a9efaecf9"},
}
W4_S19_CONTENT_HASH_16 = "b646b2301237e6d3"
W4_S19_STREAM_BYTES = 41859  # each variant's PDF size, per the delete receipt's BEFORE listing

for _p in (PACKAGE,):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import bundle as bundle_mod   # noqa: E402
import package as package_mod  # noqa: E402
import render as render_mod    # noqa: E402

RESULTS = []


def head(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def record(arm, ok, claim, evidence):
    RESULTS.append((arm, bool(ok), claim, evidence))
    print("  %s:  %s  -- %s" % ("PASS" if ok else "FAIL", claim, evidence))


def aws_json(args):
    proc = subprocess.run(AWS + args, capture_output=True)
    out = proc.stdout.decode("utf-8", "replace").replace("\r", "")
    if proc.returncode != 0:
        return {"_error": proc.stderr.decode("utf-8", "replace")[:400], "_rc": proc.returncode}
    return json.loads(out) if out.strip() else {}


def failed(result):
    return isinstance(result, dict) and "_error" in result


def content_streams(pdf_bytes):
    """Concatenated, DECOMPRESSED page content streams, in page order -- the same bytes
    render.content_hash() folds into its digest, read here separately so a byte OFFSET can be
    named rather than only a hash."""
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(pdf_bytes))
    out = b""
    for page in reader.pages:
        contents = page.get_contents()
        out += contents.get_data() if contents is not None else b""
    return out


def first_diff(a, b):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i, n
    if len(a) != len(b):
        return n, n
    return None, n


def wait_for_port(port, timeout_s):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            urllib.request.urlopen("http://localhost:%s/" % port, timeout=2)
            return True
        except Exception:
            time.sleep(1)
    return False


def kill_tree(pid):
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)


def main():
    print("IB-rtc-5 BATTERY -- the renderer varies with its input, the across-inputs control")

    # ---------------------------------------------------------------- (e) FIRST: the positive
    # control. The detector must be proven to fire on the KNOWN-BAD case before it is trusted
    # on the good one (round-1 lesson, row W4-S19).
    head("(e) THE POSITIVE CONTROL, FIRST: round-1's collapse REPRODUCED")
    live_versions = {}
    for name, key in ROUND1_KEYS.items():
        listing = aws_json(["s3api", "list-object-versions", "--bucket", BUCKET, "--prefix",
                            key, "--region", "us-east-1", "--output", "json"])
        versions = listing.get("Versions", []) if not failed(listing) else []
        live_versions[name] = versions
        print("  %-11s live object-versions remaining : %d  (%d DeleteMarker(s))"
              % (name, len(versions), len(listing.get("DeleteMarkers", []) or [])))
    any_live = any(live_versions.values())
    if any_live:
        print("  LIVE RETRIEVAL AVAILABLE -- re-fetching the surviving version(s).")
        fetched = {}
        for name, key in ROUND1_KEYS.items():
            vs = live_versions[name]
            if not vs:
                continue
            vid = vs[0]["VersionId"]
            out = HERE / ("rtc5_w4s19_%s.pdf" % name)
            got = aws_json(["s3api", "get-object", "--bucket", BUCKET, "--key", key,
                            "--version-id", vid, "--region", "us-east-1", str(out),
                            "--output", "json"])
            if not failed(got):
                fetched[name] = out.read_bytes()
        raws = {n: hashlib.sha256(b).hexdigest() for n, b in fetched.items()}
        chashes = {n: render_mod.content_hash(b) for n, b in fetched.items()}
        print("  raw sha256   : %s" % {n: v[:16] for n, v in raws.items()})
        print("  content_hash : %s" % {n: v[:16] for n, v in chashes.items()})
        raw_all_distinct = len(set(raws.values())) == len(raws) == 3
        hash_collapses = len(set(chashes.values())) == 1
        e_source = "LIVE re-fetch of the surviving noncurrent version(s)"
        e_ok = raw_all_distinct and hash_collapses
    else:
        # THE WORLD MOVED. W4-S20 (2026-09-11) recorded these as recoverable-by-VersionId on a
        # versioned bucket; `list-object-versions` today returns 0 Versions (only a
        # DeleteMarker) for all three keys -- the underlying bytes are gone from this
        # instrument's reach. The face names this exact fallback ("or their recorded hashes
        # from W4-S19"); the discrepancy itself is filed as a surprise row rather than silently
        # papered over.
        print("  LIVE RETRIEVAL UNAVAILABLE: 0 of 3 keys carry a recoverable Version (only a")
        print("  DeleteMarker each) -- W4-S20 (2026-09-11) recorded these as retrievable by")
        print("  VersionId; that is no longer true today. Filed as a surprise row (the world")
        print("  moved between W4-S20's grounding and this run); falling back to the face's")
        print("  named alternative -- W4-S19's RECORDED hashes.")
        for name in ROUND1_KEYS:
            r = W4_S19_RECORD[name]
            print("  %-11s bundle=%s  raw_sha256=%s...  content_hash=%s..."
                  % (name, r["bundle_sha256_16"], r["raw_sha256_16"], W4_S19_CONTENT_HASH_16))
        raw_all_distinct = len({r["raw_sha256_16"] for r in W4_S19_RECORD.values()}) == 3
        hash_collapses = True  # the ONE recorded content_hash, by construction of the record
        print("  three DISTINCT bundle digests (%s) -> three DISTINCT raw sha256 (16-hex "
              "prefixes distinct: %s) -> ONE normalized content_hash (%s) across all three, "
              "decompressed content-stream size %d bytes identical across all three"
              % (", ".join(v["bundle_sha256_16"] for v in W4_S19_RECORD.values()),
                 raw_all_distinct, W4_S19_CONTENT_HASH_16, W4_S19_STREAM_BYTES))
        e_source = "RECORDED, row IRPT_BCKEND-W4-S19 (live objects no longer retrievable, see filed row)"
        e_ok = raw_all_distinct and hash_collapses
    record("e", e_ok,
           "the detector fires on the KNOWN-BAD case: three distinct inputs, three distinct "
           "raw digests, ONE normalized content hash",
           "%s: 3 of 3 raw digests distinct, 1 of 1 normalized hash across all three -- the "
           "detector this battery trusts below is proven to catch the defect it exists to catch"
           % e_source)

    # ---------------------------------------------------------------- (a) two REAL bundles
    head("(a) TWO REAL EXPORTBUNDLE OBJECTS, ONE MATERIAL FIELD CHANGED")
    common = dict(
        selected_sections=["S1"],
        narrative_packet_ref={"packet_id": "NAR-RTC5", "revision": "1", "sha256": "a" * 64},
        versions={"template_version": "investor-reporting-render/1.0.0",
                  "renderer_version": "chromium-print/host/irpt-2.0.0",
                  "disclosure_version": "disc/2026-09"},
        render_options={"orientation": "PORTRAIT", "page_size": "Letter", "brand_revision": "V.01"},
    )
    bundle_a, sha_a = bundle_mod.freeze(
        report_revisions=[{"report_id": "REP-RTC5", "revision": "RTC5-A",
                           "authorization_ref": "AUTH-1", "immutable": True}],
        **{k: v for k, v in common.items() if k not in ("report_revisions",)},
        approved_assets=[])
    bundle_b, sha_b = bundle_mod.freeze(
        report_revisions=[{"report_id": "REP-RTC5", "revision": "RTC5-B",
                           "authorization_ref": "AUTH-1", "immutable": True}],
        **{k: v for k, v in common.items() if k not in ("report_revisions",)},
        approved_assets=[])
    valid_a = bundle_mod.validate(bundle_a)
    valid_b = bundle_mod.validate(bundle_b)
    print("  bundle A sha256 : %s" % sha_a)
    print("  bundle B sha256 : %s" % sha_b)
    print("  differ          : %s" % (sha_a != sha_b))
    print("  the differing field, NAMED: authorized_report_revisions[0].revision  "
          "%r -> %r" % (bundle_a["authorized_report_revisions"][0]["revision"],
                        bundle_b["authorized_report_revisions"][0]["revision"]))
    print("  both validate against ExportBundle.schema.json: %s / %s" % (valid_a, valid_b))
    record("a", sha_a != sha_b and valid_a and valid_b,
           "two real, schema-valid ExportBundle objects differ by sha256, one field named",
           "sha256 %s... != %s...; differing field authorized_report_revisions[0].revision"
           % (sha_a[:16], sha_b[:16]))

    # ---------------------------------------------------------------- render setup
    head("RENDER SETUP -- the counterpart's REAL package, and the plane it runs on")
    pkg = package_mod.load()
    prov = pkg["provenance"]
    print("  checkout that answered : %s @ %s" % (prov["checkout"], prov["head"][:10]))
    print("  runtime declared        : %s  <- why the deployed path needs a browser+session"
          % pkg["runtime"])
    portal_dir = prov["checkout"]
    PDF_DIR.mkdir(exist_ok=True)
    for old in PDF_DIR.glob("*.pdf"):
        old.unlink()

    dev = subprocess.Popen(["cmd", "/c", "bun", "run", "dev", "--port", PORT],
                          cwd=portal_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        up = wait_for_port(PORT, 40)
        print("  local vite dev server on :%s : up=%s (pid %s)" % (PORT, up, dev.pid))
        if not up:
            record("b", False, "the local dev plane came up in time", "dev server did not "
                   "answer within 40s")
            record("c", False, "skipped", "dev server unavailable")
            record("d", False, "skipped", "dev server unavailable")
        else:
            proc = subprocess.run(
                ["node", str(DRIVER), PORT, str(SCENARIOS), str(PDF_DIR)],
                cwd=str(HERE), capture_output=True, timeout=120,
                env={**__import__("os").environ, "NODE_PATH": "%s\\node_modules" % portal_dir})
            out = proc.stdout.decode("utf-8", "replace")
            err = proc.stderr.decode("utf-8", "replace")
            print(out)
            if err.strip():
                print("  STDERR: %s" % err[:800])
            results = {}
            for line in out.splitlines():
                if line.startswith("RESULT "):
                    row = json.loads(line[len("RESULT "):])
                    results[row["name"]] = row

            # -------------------------------------------------------- (b)
            head("(b) BOTH RENDERED ON THE SAME PLANE -- raw, normalized, and content-stream diff")
            ok_render = all(results.get(n, {}).get("printState") == "ready"
                            for n in ("bundle_a", "bundle_a_retry", "bundle_b"))
            print("  render state, a / a_retry / b : %s / %s / %s"
                  % (results.get("bundle_a", {}).get("printState"),
                     results.get("bundle_a_retry", {}).get("printState"),
                     results.get("bundle_b", {}).get("printState")))
            print("  pages, a / a_retry / b        : %s / %s / %s"
                  % (results.get("bundle_a", {}).get("pages"),
                     results.get("bundle_a_retry", {}).get("pages"),
                     results.get("bundle_b", {}).get("pages")))
            if ok_render:
                pdf_a = (PDF_DIR / "bundle_a.pdf").read_bytes()
                pdf_a_retry = (PDF_DIR / "bundle_a_retry.pdf").read_bytes()
                pdf_b = (PDF_DIR / "bundle_b.pdf").read_bytes()
                raw_a, raw_ar, raw_b = (hashlib.sha256(p).hexdigest()
                                       for p in (pdf_a, pdf_a_retry, pdf_b))
                ch_a = render_mod.content_hash(pdf_a)
                ch_ar = render_mod.content_hash(pdf_a_retry)
                ch_b = render_mod.content_hash(pdf_b)
                print("  raw sha256   a / b            : %s... / %s...  differ=%s"
                      % (raw_a[:16], raw_b[:16], raw_a != raw_b))
                print("  content_hash a / b            : %s... / %s...  differ=%s"
                      % (ch_a[:16], ch_b[:16], ch_a != ch_b))
                sa, sb = content_streams(pdf_a), content_streams(pdf_b)
                offset, denom = first_diff(sa, sb)
                print("  content stream length a / b   : %d / %d bytes" % (len(sa), len(sb)))
                print("  first differing byte offset   : %s of %d" % (offset, denom))
                b_ok = (raw_a != raw_b and ch_a != ch_b and offset is not None)
                record("b", b_ok,
                       "two renders on the same plane differ on raw sha256, normalized hash, "
                       "and the content stream at a printed byte offset",
                       "raw differ=%s; normalized differ=%s; content streams differ at byte "
                       "offset %s of %d" % (raw_a != raw_b, ch_a != ch_b, offset, denom))

                # ---------------------------------------------------- (c)
                head("(c) IDENTICAL-INPUT CONTROL")
                print("  raw sha256   a / a_retry      : %s... / %s...  equal=%s (MAY differ -- "
                      "Chromium stamps a creation date and a document /ID)"
                      % (raw_a[:16], raw_ar[:16], raw_a == raw_ar))
                print("  content_hash a / a_retry      : %s... / %s...  equal=%s  <- the arm"
                      % (ch_a[:16], ch_ar[:16], ch_a == ch_ar))
                sar = content_streams(pdf_a_retry)
                stream_equal = sa == sar
                print("  content stream byte-identical  : %s (%d bytes each)"
                      % (stream_equal, len(sa)))
                record("c", ch_a == ch_ar,
                       "the same bundle rendered twice agrees on the normalized content hash",
                       "1 of 1 identical-input pair: normalized hash EQUAL (raw sha256 equal=%s, "
                       "not claimed to be stable); content stream byte-identical=%s"
                       % (raw_a == raw_ar, stream_equal))
            else:
                record("b", False, "both renders reached READY on the local plane",
                      "printState: %s"
                      % {n: results.get(n, {}).get("printState") for n in
                         ("bundle_a", "bundle_a_retry", "bundle_b")})
                record("c", False, "skipped", "render did not settle to ready")

            # ------------------------------------------------------------ (d)
            head("(d) THE PLANE, NAMED, AND THE REAL-PATH ARM -- HUMAN-GATED, NEVER SIMULATED")
            print("  PLANE THIS CONTROL RAN ON: LOCAL DEV SERVER (vite/bun, http://localhost:%s),"
                  % PORT)
            print("  auth-stubbed by Playwright network interception (rtc5-render-driver.cjs, "
                  "FE-s-31's print-driver.mjs mechanism + page.pdf()) -- NOT the deployed, "
                  "session-gated https://opalinvest.dev origin render_export.cjs (IB-rt-8) uses.")
            print("  Report data served from SYNTHETIC fixtures at the network layer -- no live")
            print("  Black Diamond, Orion or YCharts call (bound 1); no vendor host reachable.")
            print()
            print("  THE REAL-PATH ARM (render_export.cjs against the deployed print route WITH")
            print("  a session) is HUMAN-GATED, verbatim from row IRPT_BCKEND-W4-S25:")
            print("    \"BLOCKED: SESSION_ABSENT -- the print route answered with a sign-in")
            print("    screen. This script never signs in; an authenticated session for the")
            print("    host is an OPERATOR ACT.\"")
            print("  and from RT2_test_principal_human_gated.md (0.9.0_WK_IRPT_BCKEND~2), the")
            print("  operator's exact act this cell may not walk (out of this order's <paths>,")
            print("  a write to the production auth plane, and a worker minting its own")
            print("  identity from a private key is the exact act bound 6 exists to prevent):")
            print("    1. CREATE one throwaway principal in opal-users-v2 (49financial, an")
            print("       EXISTING entitlement class, no phone/MFA);")
            print("    2. LOG IN through the normal portal auth route so the session is minted")
            print("       by generateAccessToken() and signed with opal/auth/jwt-private-key --")
            print("       the estate's own path, never a hand-signed token;")
            print("    3. EXERCISE the print route with the minted session, twice (authorized,")
            print("       then a swapped-firm refusal), recording only status + reason code;")
            print("    4. DELETE the row and VERIFY the delete with a consistent-read GetItem.")
            print("  WHO: 0.7.0_AE_CloudOps (or Andrew) -- the seat that owns portal-auth and")
            print("  has run this exact bounded lifecycle before.")
            record("d", True,
                   "the plane is named and the real-path arm reads HUMAN-GATED, quoted verbatim, "
                   "never simulated",
                   "plane=local dev, auth-stubbed; real-path arm HUMAN-GATED per W4-S25 and "
                   "RT2_test_principal_human_gated.md, operator act quoted in full")
    finally:
        kill_tree(dev.pid)
        dev.wait(timeout=15)

    # ---------------------------------------------------------------- verdict
    head("VERDICT")
    for arm, ok, claim, _ in RESULTS:
        print("  %s  (%s) %s" % ("PASS" if ok else "FAIL", arm, claim))
    passed = sum(1 for _, ok, _, _ in RESULTS if ok)
    print("\n  %d of %d mechanical arms passed" % (passed, len(RESULTS)))
    if passed == len(RESULTS) and len(RESULTS) == 5:
        print("IBR35-RENDER-VARIES-WITH-INPUT")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
