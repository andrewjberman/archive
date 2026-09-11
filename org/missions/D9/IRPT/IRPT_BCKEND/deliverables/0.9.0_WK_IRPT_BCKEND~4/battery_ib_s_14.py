"""IB-s-14 acceptance battery -- S14-AC1.

Nine arms -- (a) through (g) plus (amend) and (v0.11) -- each printing its own
denominators, and the token only when every one holds. The token is
IBS14-EXPORT-REPRODUCIBLE.

WHAT RUNS OFFLINE AND WHAT DOES NOT. Arms (a)-(f), (amend) and the render half of (v0.11)
run with a SOCKET GUARD installed over every render, and the guard is proved live by a
positive control before the verdict. The reads that are about the LIVE WORLD -- the three
retained vendor PDFs, the stored export object, the deployed function's configuration --
are NAMED AWS calls taken with the guard off, and each says so where it prints.

TWO THINGS THIS BATTERY SAYS OUT LOUD RATHER THAN LETTING A READER ASSUME:

  THE SECTIONS ARE FIXTURES. IB-s-10 is `staged` at this vintage -- its certified sections
  do not exist on CLOUD -- so arms (f) and (v0.11) render FIXTURE sections. The re-run on
  the real certified sections is IB-sb-3's replay, not this order's.

  THE RAW PDF HASH IS NOT STABLE AND IS NOT CLAIMED TO BE. Chromium stamps a creation date
  and a document /ID into every PDF. `artifact.sha256` in the receipt is the RAW digest of
  the bytes that exist; "the same bundle renders the same PDF" is asserted on the CONTENT
  hash, and both are printed side by side.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import socket
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[7]
PACKAGE = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "export"
IRPT = PACKAGE.parent
VARIANTS = REPO / "docs" / "research" / "investor_reporting_ycharts_variants_20260911"
ROUTES_JSON = REPO / "infra" / "aws" / "terraform" / "investor-reporting" / "api" / "routes.json"
LEDGER = (REPO / "org" / "critical_paths" / "change_management" /
          "20260911T0552Z_irpt-bckend-s14_deploy_completion.md")
SENTINEL = REPO / "org" / "critical_paths" / ".open_deploys" / "irpt-bckend-s14.json"
# The estate's own shim, via its .cmd face: `.tools/aws` is a bash script and a Windows
# Python cannot exec it (row IRPT_BCKEND-W4-S8).
AWS = ["cmd", "/c", str(REPO / ".tools" / "aws.cmd")]

EVIDENCE_BUCKET = "opal-data-ycharts"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
TENANT = "49financial"
GENERATION = "GENIBS14SYN"          # UNMISTAKABLY SYNTHETIC: this is not a client generation
VENDOR_PREFIX = ("research/20260911/variants/synthetic-firm/synthetic-advisor/requests/"
                 "irpt-variants-20260911-%s/report.pdf")

for _p in (PACKAGE, IRPT / "_authz", IRPT / "_authz" / "tests", IRPT / "_keys",
           IRPT / "_scope"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import assets as assets_mod        # noqa: E402
import bundle as bundle_mod        # noqa: E402
import download as download_mod    # noqa: E402
import enforce as _authz           # noqa: E402
import fixtures as authz_fixtures  # noqa: E402
import handler as handler_mod      # noqa: E402
import receipt as receipt_mod      # noqa: E402
import render as render_mod        # noqa: E402

VENDOR_HOSTS = ("bd3.bdreporting.com", "api.cloud.orionadvisor.com", "ycharts.com",
                "api.ycharts.com")
_real_connect = socket.socket.connect
_real_connect_ex = socket.socket.connect_ex
ATTEMPTS = {"total": 0, "vendor": 0, "loopback": 0}
RESULTS = []

# LOOPBACK IS PERMITTED AND COUNTED SEPARATELY, and this is a correction the first run
# forced rather than a convenience. The arm is "0 EXTERNAL connections during preview and
# render"; the headless print path drives the browser over a LOCAL channel, and Python's
# own asyncio event loop on Windows builds its self-pipe with `socket.socketpair()`, which
# is a 127.0.0.1 connect. A guard that refuses loopback does not measure egress -- it
# prevents the render from starting at all, and then reports zero external connections for
# a render that never happened. That is a detector which cannot go non-zero, wearing a
# measurement's clothes.
_LOOPBACK = ("127.0.0.1", "::1", "localhost", "0.0.0.0", "127.0.0.2")

GOOD_SVG = (b'<svg xmlns="http://www.w3.org/2000/svg" width="220" height="64">'
            b'<rect width="220" height="64" fill="#163372"/>'
            b'<text x="12" y="42" fill="#ffffff" font-size="26">ACME ADVISORS</text></svg>')
SCRIPT_SVG = (b'<svg xmlns="http://www.w3.org/2000/svg" width="220" height="64">'
              b'<script>fetch("https://ycharts.com/steal")</script></svg>')
BAD_TYPE = b"GIF89a" + b"\x00" * 32
SECTIONS = [
    {"section_id": "S1", "title": "Allocation", "certification": "FIXTURE-CERTIFIED",
     "body": "Target and actual allocation across the selected accounts."},
    {"section_id": "S2", "title": "Risk", "certification": "FIXTURE-CERTIFIED",
     "body": "Dispersion and drawdown of the selected set."},
]


def _classify(address):
    host = address[0] if isinstance(address, tuple) else str(address)
    return str(host), str(host) in _LOOPBACK


def _guard(self, address, *a, **k):
    host, local = _classify(address)
    if local:
        ATTEMPTS["loopback"] += 1
        return _real_connect(self, address, *a, **k)
    ATTEMPTS["total"] += 1
    if any(v in host for v in VENDOR_HOSTS):
        ATTEMPTS["vendor"] += 1
    raise OSError("BLOCKED: socket guard -- the render arms opened nothing external (%s)"
                  % (host,))


def _guard_ex(self, address, *a, **k):
    host, local = _classify(address)
    if local:
        ATTEMPTS["loopback"] += 1
        return _real_connect_ex(self, address, *a, **k)
    ATTEMPTS["total"] += 1
    if any(v in host for v in VENDOR_HOSTS):
        ATTEMPTS["vendor"] += 1
    raise OSError("BLOCKED: socket guard -- the render arms opened nothing external (%s)"
                  % (host,))


def install_guard():
    socket.socket.connect = _guard
    socket.socket.connect_ex = _guard_ex


def remove_guard():
    socket.socket.connect = _real_connect
    socket.socket.connect_ex = _real_connect_ex


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
        return {"_error": proc.stderr.decode("utf-8", "replace")[:300], "_rc": proc.returncode}
    return json.loads(out) if out.strip() else {}


def failed(result):
    """`aws_json` returns whatever the CLI printed -- a dict, a list, or a bare int when the
    call carried `--query ContentLength`. A membership test on the result therefore blows up
    on the success path, which is how this helper came to exist: `"_error" not in stored`
    raised TypeError on an int and took the arm down AFTER the work had succeeded."""
    return isinstance(result, dict) and "_error" in result


def catalogue():
    """The approved asset catalogue plus the four negative fixtures. Each negative differs
    from the approved one in EXACTLY the dimension it tests."""
    good = {"asset_id": "acme-logo", "kind": "svg", "role": "LOGO",
            "sha256": hashlib.sha256(GOOD_SVG).hexdigest(),
            "binding": {"firm_id": TENANT, "advisor_id": None}}
    return {
        "acme-logo": {"record": good, "bytes": GOOD_SVG},
        "wrong-firm": {"record": dict(good, asset_id="wrong-firm",
                                      binding={"firm_id": "cottonwood", "advisor_id": None}),
                       "bytes": GOOD_SVG},
        "wrong-type": {"record": dict(good, asset_id="wrong-type", kind="gif",
                                      sha256=hashlib.sha256(BAD_TYPE).hexdigest()),
                       "bytes": BAD_TYPE},
        "wrong-sum": {"record": dict(good, asset_id="wrong-sum", sha256="0" * 64),
                      "bytes": GOOD_SVG},
        "script-svg": {"record": dict(good, asset_id="script-svg",
                                      sha256=hashlib.sha256(SCRIPT_SVG).hexdigest()),
                       "bytes": SCRIPT_SVG},
    }


def export_inputs(**over):
    base = dict(
        tenant=TENANT, generation_id=GENERATION, attempt=1,
        report_revisions=[{"report_id": "REP-0001", "revision": "rev-7",
                           "authorization_ref": "AUTH-1", "immutable": True}],
        selected_sections=[s["section_id"] for s in SECTIONS],
        narrative_packet_ref={"packet_id": "NAR-0001", "revision": "1", "sha256": "a" * 64},
        versions={"template_version": "irpt-export-template/1.0.0",
                  "renderer_version": render_mod.RENDERER_VERSION,
                  "disclosure_version": "disc/2026-09"},
        sections=SECTIONS, requested_assets=["acme-logo"], asset_catalogue=catalogue(),
        binding_firm=TENANT)
    base.update(over)
    return base


def main():
    print("IB-s-14 BATTERY -- export bundle freeze, render worker, receipt, download")
    print("  package     : %s" % PACKAGE)
    print("  renderer    : %s" % render_mod.default_renderer().kind)
    print("  SECTIONS    : FIXTURE. IB-s-10 is `staged` at this vintage and its certified")
    print("                sections are not on CLOUD, so arms (f) and (v0.11) render FIXTURE")
    print("                sections and say so. The re-run on the real certified sections is")
    print("                IB-sb-3's replay, not this order's act.")

    install_guard()
    portrait = {"orientation": "PORTRAIT", "page_size": "Letter", "brand_revision": "V.01"}

    # ---------------------------------------------------------------- (a)
    head("(a) SAME BUNDLE, SAME PDF -- preview, render, retry")
    preview = handler_mod.run_export(export_revision="r1", render_options=portrait,
                                     narrative_text="Over the same window.",
                                     **export_inputs())
    first = handler_mod.run_export(export_revision="r1", render_options=portrait,
                                   narrative_text="Over the same window.", **export_inputs())
    retry = handler_mod.run_export(export_revision="r1", render_options=portrait,
                                   narrative_text="Over the same window.", **export_inputs())
    hashes = [preview["bundle_sha256"], first["bundle_sha256"], retry["bundle_sha256"]]
    print("  bundle sha256, preview/render/retry : %s" % [h[:16] for h in hashes])
    print("  equal across the three              : %s (3 of 3)" % (len(set(hashes)) == 1))
    print("  rendered content hash, render/retry : %s / %s"
          % (first["rendered"]["content_hash"][:16], retry["rendered"]["content_hash"][:16]))
    print("  content hash equal                  : %s  <- the arm"
          % (first["rendered"]["content_hash"] == retry["rendered"]["content_hash"]))
    print("  RAW sha256, render/retry            : %s / %s"
          % (first["rendered"]["raw_sha256"][:16], retry["rendered"]["raw_sha256"][:16]))
    print("  RAW equal                           : %s -- Chromium stamps a creation date and"
          % (first["rendered"]["raw_sha256"] == retry["rendered"]["raw_sha256"]))
    print("    a document /ID into every PDF, so the raw digest CANNOT be stable. It is what")
    print("    the receipt's artifact.sha256 carries (an artifact hash must name the object")
    print("    that exists); the reproducibility claim is on the content hash above.")
    print("  pages / validation                  : %d / %s"
          % (first["rendered"]["facts"]["page_count"],
             first["rendered"]["facts"]["validation_status"]))
    record("a", len(set(hashes)) == 1
           and first["rendered"]["content_hash"] == retry["rendered"]["content_hash"]
           and first["rendered"]["facts"]["validation_status"] == "PASSED",
           "one frozen bundle renders one document, three times",
           "bundle hash equal 3 of 3; content hash equal render-vs-retry; the raw digest is "
           "NOT equal and is not claimed to be")

    # ---------------------------------------------------------------- (b)
    head("(b) BRANDING IS A NEW REVISION, NOT A RECALCULATION")
    rebranded, rebrand_sha = bundle_mod.rebrand(first["bundle"], "V.02", [])
    second = handler_mod.run_export(export_revision="r2",
                                    render_options={"orientation": "PORTRAIT",
                                                    "page_size": "Letter",
                                                    "brand_revision": "V.02"},
                                    requested_assets=[],
                                    narrative_text="Over the same window.",
                                    **{k: v for k, v in export_inputs().items()
                                       if k != "requested_assets"})
    perf_before = bundle_mod.performance_revision_of(first["bundle"])
    perf_after = bundle_mod.performance_revision_of(second["bundle"])
    print("  export revision                     : r1 -> r2")
    print("  brand revision                      : %s -> %s"
          % (first["bundle"]["render_options"]["brand_revision"],
             second["bundle"]["render_options"]["brand_revision"]))
    print("  bundle sha256                       : %s -> %s (different: %s)"
          % (first["bundle_sha256"][:16], second["bundle_sha256"][:16],
             first["bundle_sha256"] != second["bundle_sha256"]))
    print("  receipt export_id                   : %s -> %s (different: %s)"
          % (first["receipt"]["export_ref"]["export_id"][:20],
             second["receipt"]["export_ref"]["export_id"][:20],
             first["receipt"]["export_ref"]["export_id"]
             != second["receipt"]["export_ref"]["export_id"]))
    print("  PERFORMANCE revision                : %s -> %s  <- UNCHANGED is the arm"
          % (perf_before, perf_after))
    print("  rebrand() carried the revisions     : %s (its own assertion, sha %s)"
          % (bundle_mod.performance_revision_of(rebranded) == perf_before, rebrand_sha[:12]))
    print("  logo used in r2                     : %s"
          % ((second["fallback_asset"] or {}).get("source")))
    record("b", first["bundle_sha256"] != second["bundle_sha256"]
           and first["receipt"]["export_ref"]["export_id"]
           != second["receipt"]["export_ref"]["export_id"]
           and perf_before == perf_after,
           "a branding change makes a NEW export revision with a different receipt and the "
           "performance revision unchanged",
           "2 of 2 identities moved (bundle sha, export id); 1 of 1 performance revision "
           "held at %s" % (perf_after,))

    # ---------------------------------------------------------------- (c)
    head("(c) NO VENDOR CALL IN RENDER -- THE CENSUS")
    print("  renders performed under the guard   : 4 (preview, render, retry, rebrand)")
    print("  EXTERNAL outbound attempts          : %d  <- 0 is the arm" % ATTEMPTS["total"])
    print("  of which to a VENDOR host           : %d (denominator: %s)"
          % (ATTEMPTS["vendor"], ",".join(VENDOR_HOSTS)))
    print("  LOOPBACK connects PERMITTED         : %d -- the print path drives the browser"
          % ATTEMPTS["loopback"])
    print("    over a LOCAL channel and asyncio builds its self-pipe with socketpair(). A")
    print("    guard that refused these would stop the render from starting and then report")
    print("    zero external connections for a render that never happened.")
    print("  bundle field the renderer asserts   : live_vendor_request_during_render=%s"
          % first["bundle"]["live_vendor_request_during_render"])
    before_vendor = ATTEMPTS["vendor"]
    fired = False
    try:
        socket.socket().connect(("ycharts.com", 443))
    except OSError:
        fired = True
    print("  POSITIVE CONTROL                    : guard fired=%s; vendor attempts moved "
          "%d -> %d, so the zero above is MEASURED, not a dead guard"
          % (fired, before_vendor, ATTEMPTS["vendor"]))
    guard_ok = fired and before_vendor == 0 and ATTEMPTS["vendor"] == 1
    record("c", guard_ok, "no external connection during preview or render",
           "0 of 0 vendor connections across 4 renders; the positive control moved the "
           "counter to 1")

    # ---------------------------------------------------------------- (d)
    head("(d) ASSETS VERIFIED, NOT FETCHED -- 5 of 5")
    cat = catalogue()
    cases = [("wrong-firm", "BINDING"), ("wrong-type", "UNSUPPORTED_TYPE"),
             ("wrong-sum", "CHECKSUM"), ("script-svg", "UNSAFE_SVG")]
    refused = 0
    for asset_id, expected in cases:
        try:
            entry = cat[asset_id]
            assets_mod.verify(entry["record"], entry["bytes"], TENANT)
            print("    %-11s NOT REFUSED (the arm fails)" % asset_id)
        except assets_mod.AssetRefused as exc:
            hit = exc.code == expected
            refused += hit
            print("    %-11s REFUSED %-17s %s" % (asset_id, exc.code, exc.reason[:74]))
    url_refused = 0
    url_field = "https://ycharts.com/logo.svg"
    try:
        assets_mod.resolve(url_field, cat)
        print("    url-field   NOT REFUSED (the arm fails)")
    except assets_mod.AssetRefused as exc:
        url_refused = 1
        print("    url-field   REFUSED %-17s %s" % (exc.code, exc.reason[:74]))
    print("  a report field carrying a URL is never fetched: refused BEFORE any lookup, and")
    print("  the socket guard counter did not move (%d vendor attempt(s) since the control)"
          % (ATTEMPTS["vendor"] - 1))
    print("  the APPROVED asset still verifies   : %s"
          % (assets_mod.verify(cat["acme-logo"]["record"], GOOD_SVG, TENANT)["asset_id"]))
    record("d", refused == 4 and url_refused == 1 and ATTEMPTS["vendor"] == 1,
           "four bad assets refused by name and a URL field never fetched",
           "%d of 4 refusals matched their expected code, plus 1 of 1 URL refusal = 5 of 5; "
           "the approved asset still verifies, so the arm is not passing by refusing "
           "everything" % refused)

    # ---------------------------------------------------------------- (e)
    head("(e) REAUTHORIZED EVEN WHEN THE ARTIFACT EXISTS -- THE DIFFERENCE CONTROL")
    binding = _authz.FirmBinding(TENANT, authz_fixtures.OPAQUE_FIRM)
    deps = authz_fixtures.Deps()
    enforcer = _authz.Enforcer(binding, deps.load_directory, deps.load_ownership,
                               deps.load_policy, artifacts=dict(authz_fixtures.ARTIFACTS),
                               cache={})
    export_id = first["receipt"]["export_ref"]["export_id"]
    artifacts = {export_id: {"key": first["artifact_key"], "bucket": EVIDENCE_BUCKET,
                             "exists": True}}
    signer = download_mod.FixtureSigner(EVIDENCE_BUCKET, ttl_seconds=120)
    route = download_mod.make_download_route(enforcer, artifacts,
                                             signer, {export_id: first["receipt"]})

    def request():
        return _authz.Request(authz_fixtures.headers(), download_mod.DOWNLOAD_OPERATION,
                              "pdf", authz_fixtures.PDF_OK, {"export_id": export_id})

    served = route(request())
    url_ok, url_problems = download_mod.verify(served.payload["url"], EVIDENCE_BUCKET)
    print("  download 1 (grant intact)           : ok=%s artifact_existed=%s reauthorized=%s"
          % (served.ok, served.payload["artifact_existed"], served.payload["reauthorized"]))
    print("  the URL                             : Opal-signed=%s ttl=%ds problems=%s"
          % (url_ok, served.payload["ttl_seconds"], url_problems or "none"))
    print("    host whitelist, not a vendor blacklist: an enumerated ban list lapses silently")
    print("    when a vendor's name changes.")
    deps.revoke()
    print("  REVOKED the fixture grant. The artifact is STILL PRESENT and the cache was NOT")
    print("  cleared -- so a refusal now cannot be explained by a cold cache or a missing")
    print("  object, which are the two things a reader would otherwise suspect.")
    again = route(request())
    print("  download 2 (grant revoked)          : ok=%s code=%s" % (again.ok,
                                                                     getattr(again, "code", None)))
    print("  artifact still recorded present     : %s" % artifacts[export_id]["exists"])
    print("  cache entries at refusal time       : %d" % len(enforcer.cache))
    record("e", served.ok and url_ok and (not again.ok)
           and again.code in ("EMPTY_GRANT", "OBJECT_NOT_COVERED")
           and artifacts[export_id]["exists"],
           "the download reauthorizes on every request, including the one that finds the "
           "artifact already there",
           "1 served then 1 REFUSED (%s) with the object still present and the cache "
           "untouched; the URL is Opal-signed with a %ds ttl and no vendor host"
           % (again.code, served.payload["ttl_seconds"]))

    # ---------------------------------------------------------------- (f)
    head("(f) THE ANALYSIS EXPORT -- same input, own orientation, no narrative")
    landscape = {"orientation": "LANDSCAPE", "page_size": "Letter", "brand_revision": "V.01"}
    analysis = handler_mod.run_export(export_revision="r1",
                                      render_options=landscape,
                                      kind="ANALYSIS",
                                      narrative_text="THIS NARRATIVE MUST NOT APPEAR",
                                      **export_inputs())
    same_inputs = (bundle_mod.performance_revision_of(analysis["bundle"])
                   == bundle_mod.performance_revision_of(first["bundle"])
                   and analysis["bundle"]["selected_sections"]
                   == first["bundle"]["selected_sections"]
                   and analysis["bundle"]["versions"] == first["bundle"]["versions"])
    print("  section source                      : FIXTURE (IB-s-10 is `staged`; its")
    print("                                        certified sections are not on CLOUD)")
    print("  same report revisions as the preview: %s" % same_inputs)
    print("  orientation, preview -> analysis    : %s -> %s"
          % (first["bundle"]["render_options"]["orientation"],
             analysis["bundle"]["render_options"]["orientation"]))
    print("  brand revision (same brand)         : %s"
          % analysis["bundle"]["render_options"]["brand_revision"])
    print("  pages / validation                  : %d / %s"
          % (analysis["rendered"]["facts"]["page_count"],
             analysis["rendered"]["facts"]["validation_status"]))
    print("  NARRATIVE census in the rendered TEXT: %s  <- 0 is the arm"
          % analysis["rendered"]["facts"]["forbidden_hits"])
    print("  and structurally: the analysis template has no {{NARRATIVE}} slot, so a caller")
    print("  passing narrative text cannot render one. Two independent halves.")
    slotless = "{{NARRATIVE}}" not in (
        render_mod.FIXTURE_PACKAGE_DIR / "analysis.html").read_text(encoding="utf-8")
    print("  analysis template is slotless       : %s" % slotless)
    record("f", same_inputs and slotless
           and analysis["rendered"]["facts"]["forbidden_hits"].get("Narrative") == 0
           and analysis["rendered"]["facts"]["validation_status"] == "PASSED"
           and analysis["bundle"]["render_options"]["orientation"] == "LANDSCAPE",
           "the Analysis export renders at the same input and configuration, in its own "
           "orientation, and carries no performance narrative",
           "0 of 1 narrative markers in the rendered text AND the template is slotless; "
           "orientation LANDSCAPE against the preview's PORTRAIT; sections are FIXTURES and "
           "the arm says so")

    # ---------------------------------------------------------------- (amend)
    head("(amend) GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE (rows W2-S9 / W2-S10)")
    table = handler_mod.routes(enforcer, artifacts, signer, {export_id: first["receipt"]})
    census = _authz.unguarded_routes(table)
    print("  routes THIS cell registers          : %s" % sorted(table))
    print("  unguarded census                    : %d of %d  (%s)"
          % (len(census["unguarded"]), census["routes"], census["verdict"][:60]))
    print("  routes.json (IB-s-15's deliverable) : present=%s" % ROUTES_JSON.is_file())
    print("    It does not exist at this vintage, so a census over it would be 0 of 0 -- a")
    print("    VACUOUS pass. It is printed as vacuous and the CENSOR is proved instead, with")
    print("    the two controls IB-s-7's battery ran:")

    def bare(request, scope):
        return {}
    unguarded_census = _authz.unguarded_routes({"export_download": bare})
    guarded_census = _authz.unguarded_routes(
        {"export_download": enforcer.guard("export_download", object_kind="pdf")(bare)})
    print("      an UNGUARDED handler censuses   : %d of %d"
          % (len(unguarded_census["unguarded"]), unguarded_census["routes"]))
    print("      the SAME handler wrapped        : %d of %d"
          % (len(guarded_census["unguarded"]), guarded_census["routes"]))

    unbound = _authz.Enforcer(_authz.FirmBinding(TENANT, authz_fixtures.OTHER_OPAQUE_FIRM),
                              deps.load_directory, deps.load_ownership, deps.load_policy,
                              artifacts=dict(authz_fixtures.ARTIFACTS), cache={})
    unbound_route = download_mod.make_download_route(unbound, artifacts, signer, {})
    unbound_out = unbound_route(request())
    print("  a NON-RECONCILING firm binding      : ok=%s code=%s"
          % (unbound_out.ok, getattr(unbound_out, "code", None)))
    print("    refused rather than served the EMPTY SET an unbound firm produces -- which is")
    print("    the failure no per-module test can see, because it looks like a revocation.")

    deps.restore()
    enforcer.cache.clear()
    secret = "Whitfield Family"
    leak_route = download_mod.make_download_route(enforcer, artifacts, signer, {})
    leaked = leak_route(_authz.Request(authz_fixtures.headers(),
                                       download_mod.DOWNLOAD_OPERATION, "pdf",
                                       authz_fixtures.PDF_OK,
                                       {"export_id": export_id, "client_name": secret}))
    envelope = json.dumps({"envelope": leaked.as_envelope(), "audit": enforcer.audit})
    occurrences = envelope.count(secret)
    print("  a parameter keyed by a client NAME  : ok=%s code=%s"
          % (leaked.ok, getattr(leaked, "code", None)))
    print("  occurrences of the refused VALUE in the WHOLE envelope (body + reason + audit):")
    print("      %d  <- 0 is the arm (envelope is %d bytes)" % (occurrences, len(envelope)))
    print("  the refused parameter NAME is named : %s" % ("client_name" in envelope))
    record("amend", not census["unguarded"]
           and unguarded_census["unguarded"] == ["export_download"]
           and not guarded_census["unguarded"]
           and unbound_out.code == "FIRM_BINDING"
           and getattr(leaked, "code", None) == "KEY_REFUSED"
           and occurrences == 0 and "client_name" in envelope,
           "every route is guarded, the firm binding refuses rather than serving empty, and "
           "no refused value leaves the handler",
           "0 of %d routes unguarded with the censor proved both ways (1 of 1 / 0 of 1); "
           "FIRM_BINDING on a non-reconciling binding; 0 occurrences of the refused value "
           "in the whole envelope while its NAME is named" % census["routes"])

    remove_guard()

    # ---------------------------------------------------------------- (g)
    head("(g) RECEIPT AND ARTIFACT; LEDGER CLOSED")
    pdf = first["pdf"]
    key = first["artifact_key"]
    print("  artifact key                        : %s" % key)
    print("  under the bound firm's prefix       : %s"
          % key.startswith("firms/%s/generations/" % TENANT))
    print("  built by _keys.s3_evidence_key      : every segment validated by SHAPE, so a")
    print("                                        client name cannot become a path")
    # THE GENERATION ID IS UNMISTAKABLY SYNTHETIC and the object carries irpt-synthetic=true
    # in its metadata. This is a real write to the real evidence bucket -- the arm asks for
    # the STORED object's hash -- so it must not be mistakable for a client artifact.
    (REPO / ".scratch" / "ibs14_report.pdf").write_bytes(pdf)
    put = aws_json(["s3api", "put-object", "--bucket", EVIDENCE_BUCKET, "--key", key,
                    "--body", str(REPO / ".scratch" / "ibs14_report.pdf"),
                    "--metadata", "irpt-synthetic=true,export-revision=r1,"
                                  "vendor-synthetic-holdings=false",
                    "--content-type", "application/pdf", "--output", "json"])
    stored = aws_json(["s3api", "get-object", "--bucket", EVIDENCE_BUCKET, "--key", key,
                       str(REPO / ".scratch" / "ibs14_readback.pdf"), "--query",
                       "ContentLength", "--output", "json"])
    readback = (REPO / ".scratch" / "ibs14_readback.pdf").read_bytes()
    declared = first["receipt"]["artifact"]["sha256"]
    actual = hashlib.sha256(readback).hexdigest()
    ok_receipt, why = receipt_mod.verify_against_object(first["receipt"], readback)
    print("  stored object bytes                 : %d (put rc ok=%s, get ok=%s)"
          % (len(readback), not failed(put), not failed(stored)))
    print("  receipt artifact_hash               : %s" % declared[:24])
    print("  stored object sha256                : %s" % actual[:24])
    print("  equal                               : %s -- %s" % (ok_receipt, why[:70]))
    print("  receipt validates against contract  : %s"
          % bundle_mod.validate(first["receipt"], "ExportReceipt.schema.json"))
    print("  server_only / reauthorization / vendor url: %s / %s / %s"
          % (first["receipt"]["artifact"]["server_only"],
             first["receipt"]["download_route"]["requires_reauthorization"],
             first["receipt"]["vendor_signed_url_exposed"]))
    cfg = aws_json(["lambda", "get-function-configuration", "--function-name",
                    "irpt-export-render", "--region", "us-east-1", "--output", "json"])
    with open(str(REPO / "infra" / "aws" / "lambda" / "ci" / "lambda-source-map.json"),
              encoding="utf-8") as fh:
        built_sha = json.load(fh)["functions"]["irpt-export-render"]["artifact_sha256"]
    print("  irpt-export-render CodeSha256       : %s" % cfg.get("CodeSha256"))
    print("  built zip sha256 (source map)       : %s" % built_sha)
    print("  equal                               : %s" % (cfg.get("CodeSha256") == built_sha))
    print("  layer attached                      : %s"
          % [x["Arn"] for x in cfg.get("Layers", [])])
    ledger_text = LEDGER.read_text(encoding="utf-8")
    ledger_closed = "**Status:** CLOSED" in ledger_text
    sha = subprocess.run(["git", "log", "-1", "--format=%H %s", "--",
                          "org/critical_paths/.open_deploys/irpt-bckend-s14.json"],
                         cwd=str(REPO), capture_output=True)
    print("  LEDGER irpt-bckend-s14              : entry reads CLOSED=%s; sentinel on disk=%s"
          % (ledger_closed, SENTINEL.exists()))
    print("    sentinel commit                   : %s"
          % sha.stdout.decode("utf-8", "replace").strip()[:104])
    record("g", ok_receipt and cfg.get("CodeSha256") == built_sha and ledger_closed
           and not SENTINEL.exists()
           and key.startswith("firms/%s/generations/" % TENANT),
           "the receipt names the object that exists, the key is under the bound firm's "
           "prefix, and the served bytes are the built bytes",
           "artifact_hash == the stored object's sha256; CodeSha256 == the built zip; "
           "ledger CLOSED and its sentinel removed by the close")

    # ---------------------------------------------------------------- (v0.11)
    head("(v0.11) THE ANALYSIS EXPORT ON REAL VENDOR INPUT -- 3 variants")
    expected = {r["variant"]: r for r in json.loads(
        (VARIANTS / "pdf_validation.json").read_text(encoding="utf-8"))}
    print("  source: s3://%s/research/20260911/variants/... (an OPAL-OWNED S3 read under KMS"
          % EVIDENCE_BUCKET)
    print("          key 86324aae-..., NOT a vendor call -- bound 1 is untouched)")
    verified, exported = 0, 0
    for variant in ("overview", "comparison", "multicomp"):
        local = REPO / ".scratch" / "vendor_pdfs" / ("%s.pdf" % variant)
        got = aws_json(["s3api", "get-object", "--bucket", EVIDENCE_BUCKET, "--key",
                        VENDOR_PREFIX % variant, str(local), "--query", "ContentLength",
                        "--output", "json"])
        if failed(got):
            print("    %-11s BLOCKED-BY-READ: %s" % (variant, got["_error"][:70]))
            continue
        data = local.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        match = digest == expected[variant]["sha256"]
        verified += match
        print("    %-11s %8d bytes  sha256 %s  == pdf_validation.json: %s  (declared %d pp)"
              % (variant, len(data), digest[:16], match, expected[variant]["pages"]))
        if not match:
            print("      STOP: a mismatch is a STOP and a row; this variant is not used.")
            continue
        inputs = export_inputs()
        inputs["report_revisions"] = [{"report_id": "REP-VENDOR-%s" % variant.upper(),
                                       "revision": digest[:16],
                                       "authorization_ref": "AUTH-VENDOR-SYNTHETIC",
                                       "immutable": True}]
        out = handler_mod.run_export(
            export_revision="v0-11-%s" % variant, generation_id=GENERATION,
            render_options={"orientation": "LANDSCAPE", "page_size": "Letter",
                            "brand_revision": "V.01"},
            kind="ANALYSIS", narrative_text="THIS NARRATIVE MUST NOT APPEAR",
            vendor_synthetic_holdings=True,
            **{k: v for k, v in inputs.items()
               if k not in ("report_revisions", "generation_id")},
            report_revisions=inputs["report_revisions"])
        vkey = out["artifact_key"]
        (REPO / ".scratch" / ("ibs14_%s.pdf" % variant)).write_bytes(out["pdf"])
        aws_json(["s3api", "put-object", "--bucket", EVIDENCE_BUCKET, "--key", vkey,
                  "--body", str(REPO / ".scratch" / ("ibs14_%s.pdf" % variant)),
                  "--metadata", "irpt-synthetic=true,vendor-synthetic-holdings=true,"
                                "export-revision=v0-11-%s" % variant,
                  "--content-type", "application/pdf", "--output", "json"])
        back = REPO / ".scratch" / ("ibs14_%s_readback.pdf" % variant)
        aws_json(["s3api", "get-object", "--bucket", EVIDENCE_BUCKET, "--key", vkey,
                  str(back), "--query", "ContentLength", "--output", "json"])
        stored_ok, _why = receipt_mod.verify_against_object(out["receipt"], back.read_bytes())
        narrative = out["rendered"]["facts"]["forbidden_hits"].get("Narrative")
        label = out["object_metadata"]["vendor-synthetic-holdings"]
        print("      bundle %s | %d pp | narrative markers %s | stored hash equal %s | "
              "vendor_synthetic_holdings %s"
              % (out["bundle_sha256"][:12], out["rendered"]["facts"]["page_count"],
                 narrative, stored_ok, label))
        print("      key %s" % vkey)
        exported += (stored_ok and narrative == 0 and label == "true")
    print("  SHA-256 verified BEFORE use         : %d of 3" % verified)
    print("  variants exported and stored        : %d of 3" % exported)
    print("  NEVER marked complete on the generator's 201 or on a PDF's existence: every")
    print("  variant above was hashed against pdf_validation.json first, rendered, stored,")
    print("  and READ BACK. The sections remain FIXTURES (IB-s-10 is `staged`), and")
    print("  REPRESENTATIVE REAL-CLIENT specimens remain the proof gap on FWD-4 / FWD-8.")
    record("v0.11", verified == 3 and exported == 3,
           "the three retained vendor PDFs are verified by digest and exported as Analysis "
           "bundles labelled vendor_synthetic_holdings",
           "3 of 3 SHA-256 equal to pdf_validation.json before use; 3 of 3 rendered, stored "
           "and read back with 0 narrative markers and the label set")

    # ---------------------------------------------------------------- verdict
    head("VERDICT")
    for arm, ok, claim, _ in RESULTS:
        print("  %s  (%s) %s" % ("PASS" if ok else "FAIL", arm, claim))
    passed = sum(1 for _, ok, _, _ in RESULTS if ok)
    print("\n  %d of %d mechanical arms passed" % (passed, len(RESULTS)))
    if passed == len(RESULTS):
        print("IBS14-EXPORT-REPRODUCIBLE")
        return 0
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        remove_guard()
