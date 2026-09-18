"""IB-rt-8 acceptance battery -- RT8-AC1.

Seven arms -- (a) through (g) -- each printing its own denominators, and the token only when
every one holds. The token is IBRT8-EXPORT-RENDERS.

THE SUBJECT IS THE REAL ARTIFACT, NEVER A COPY THIS FILE WRAPS (bound 12). Arm (a) runs
against the DEPLOYED controller by `aws lambda invoke`; arm (c) reads the DEPLOYED layer and
the three DEPLOYED functions; arm (e) censuses the objects that exist in the bucket; arm
(f) reads the ledger entry and re-plans the three real roots; arm (g) reads the world for
whether four named objects are gone. Nothing here registers a handler with itself and then
measures it.

ARM (g) IS AN ADDENDUM ON ANDREW'S WORD (2026-09-11 13:48Z, VERBATIM "yes on synthetic
exports"), and IT DOES NOT PERFORM THE DELETE. The act was taken once, under its own
change-management ledger whose sentinel was committed BEFORE it; this arm VERIFIES the
result and is therefore re-runnable. A battery that deleted on every run would pass the
first time and fail the second, and its receipts would be its own claim rather than a
measurement.

ARM (e) CHANGED WITH THE WORLD. It read FIVE live objects and asserted 5 of 5 still headed
200; four of those are now gone by the same word. It now censuses what LIVES and re-runs the
four deleted keys from the COMMITTED RECORD, labelled a record -- the readers are pure
functions of (key, metadata), and whether the objects exist is arm (g)'s measurement.

THE RENDER RAN, AND IT READS SESSION-GATED. Andrew's word of 2026-09-11 ~14:5xZ ("Yes
ycharts runner may be started") turned the HUMAN-GATED arm into an act: the host was started,
`irpt-export-render-run` was sent, Chromium opened the REAL portal origin, and the print route
answered with a SIGN-IN SCREEN -- so the host half refused SESSION_ABSENT, which it is built
to do and never signs in around. The issuer's amendment names that branch, so SESSION-GATED is
the arm's own rule rather than a skip, and the host was returned to the state its root
declares. The battery does not start a host: it reads the RECORD of the act and reads the
WORLD for where the host ended up.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[7]
PACKAGE = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "export"
IRPT = PACKAGE.parent
LEDGER = (REPO / "org" / "critical_paths" / "change_management" /
          "20260911T1227Z_irpt-bckend-rt8_deploy_completion.md")
SENTINEL = REPO / "org" / "critical_paths" / ".open_deploys" / "irpt-bckend-rt8.json"
HERE = pathlib.Path(__file__).resolve().parent
DELETE_RECEIPTS = HERE / "RT8-g_delete_receipts.json"
RENDER_RECORD = HERE / "RT8-a_render_record.json"
DELETE_LEDGER = (REPO / "org" / "critical_paths" / "change_management" /
                 "20260911T1454Z_irpt-bckend-rt8-synthetic-delete_deploy_completion.md")
DELETE_SENTINEL = (REPO / "org" / "critical_paths" / ".open_deploys" /
                   "irpt-bckend-rt8-synthetic-delete.json")
AWS = ["cmd", "/c", str(REPO / ".tools" / "aws.cmd")]
TERRAFORM = str(REPO / ".tools" / "terraform.exe")

BUCKET = "opal-data-ycharts"
TENANT = "49financial"
SYNTHETIC_PREFIX = "firms/49financial/generations/GENIBS14SYN/"
PROOF_PREFIX = "firms/49financial/generations/GENRT8PROOF/"
GENERATION = "GENRT8PROOF"          # this cell's own proof generation, unmistakably synthetic
FUNCTION = "irpt-export-render"
LAYER = "irpt-common"
FUNCTIONS = ("irpt-performance-adapter", "irpt-narrative", "irpt-export-render")
ROOTS = ("export", "performance", "narrative")

for _p in (PACKAGE, IRPT / "_authz", IRPT / "_authz" / "tests", IRPT / "_keys"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def _load(path, name):
    """Load a module BY PATH, so sys.path order cannot decide which file answers.

    IT ALREADY DECIDED ONCE, WRONGLY. Round 2's sibling cell IB-rt-2 added
    `_authz/dispatch.py` beside this package's `export/dispatch.py`; both directories are on
    this battery's path, the later insert wins, and `import dispatch` silently resolved to the
    OTHER cell's module -- an AttributeError on HUMAN_GATED, which is the LUCKY failure. Had
    the two modules shared a function name with different semantics, the battery would have
    measured the wrong module and PASSED. A module name is not an identity; a path is.
    """
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


dispatch_mod = _load(PACKAGE / "dispatch.py", "irpt_export_dispatch")
exclusion_mod = _load(PACKAGE / "exclusion.py", "irpt_export_exclusion")
package_mod = _load(PACKAGE / "package.py", "irpt_export_package")
download_mod = _load(PACKAGE / "download.py", "irpt_export_download")
_authz = _load(IRPT / "_authz" / "enforce.py", "irpt_authz_enforce")
authz_fixtures = _load(IRPT / "_authz" / "tests" / "fixtures.py", "irpt_authz_fixtures")

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


# ROW W4-S23, THE RE-CUT BAR (round-2 ruling, IRPT_BCKEND_ROUND2_ANALYSIS.md): "0 EXTERNAL
# CONNECTIONS" IS UNACHIEVABLE against the portal as built -- the sign-in page this render
# reaches pulls webfonts from Google (2 of 12 requests, both foreign, 0 vendor). The number the
# bound actually protects is VENDOR calls, so the bar becomes "0 VENDOR connections" over an
# ENUMERATED vendor host list, with the foreign-but-not-vendor hosts printed on their own line.
#
# BAR TEXT, VERBATIM, BEFORE THIS EDIT (RT8-AC1(a), and this battery's own arm (a) print block):
#   "0 external connections during the render (host guard log, denominator printed)"
# BAR TEXT, VERBATIM, AFTER THIS EDIT:
#   "0 VENDOR connections during the render, over an enumerated vendor host list (host guard
#    log, denominator printed); foreign-but-not-vendor hosts (e.g. webfonts) are named, not
#    counted against the bar."
#
# The vendor list is the render record's OWN denominator string (guard["denominator"]), never
# retyped here -- a second copy of the enumeration is exactly the drift class row S32 warns about.
def vendor_bar_report(guard):
    """(ok, lines) for the re-cut bar. `guard` is the REAL network_guard dict from the committed
    render record (RT8-a_render_record.json) -- never a synthetic copy. ok is True iff 0 of the
    enumerated vendor hosts were reached and at least one request was measured."""
    total = guard.get("requests_total", 0)
    by_origin = guard.get("requests_by_origin") or {}
    denom = guard.get("denominator") or ""
    vendor_marker = "vendor hosts checked:"
    if vendor_marker in denom:
        vendor_hosts = tuple(h.strip() for h in
                              denom.split(vendor_marker, 1)[1].split(";", 1)[0].split(",")
                              if h.strip())
    else:
        vendor_hosts = ()
    vendor_hits = {h: by_origin.get(h, 0) for h in vendor_hosts if by_origin.get(h, 0)}
    foreign = list(guard.get("foreign_origins") or [])
    foreign_non_vendor = [o for o in foreign if o not in vendor_hosts]
    lines = [
        "  VENDOR LIST ENUMERATED (%d)      : %s" % (len(vendor_hosts), ", ".join(vendor_hosts)),
        "  FOREIGN, NOT VENDOR (%d)         : %s"
        % (len(foreign_non_vendor), ", ".join(foreign_non_vendor) or "none"),
        "  VENDOR %d of %d requests         : %s"
        % (len(vendor_hits), total,
           "0 VENDOR CONNECTIONS" if not vendor_hits else "VENDOR HIT: %s" % vendor_hits),
    ]
    ok = (not vendor_hits) and total > 0 and bool(vendor_hosts)
    return ok, lines


def invoke(payload, tag):
    """An invoke of the DEPLOYED function. The payload file and the response file are both
    under .scratch; the response is returned parsed, with an error surfaced rather than
    swallowed."""
    pay = REPO / ".scratch" / ("rt8_%s_in.json" % tag)
    out = REPO / ".scratch" / ("rt8_%s_out.json" % tag)
    pay.write_text(json.dumps(payload), encoding="utf-8", newline="")
    proc = subprocess.run(AWS + ["lambda", "invoke", "--function-name", FUNCTION,
                                 "--region", "us-east-1", "--payload",
                                 "file://%s" % pay.as_posix(), str(out), "--output", "json"],
                          capture_output=True)
    if not out.is_file():
        return {"_error": proc.stderr.decode("utf-8", "replace")[:400]}
    raw = json.loads(out.read_text(encoding="utf-8"))
    if "errorMessage" in raw:
        return {"_error": raw["errorMessage"], "_raw": raw}
    body = raw.get("body")
    return {"statusCode": raw.get("statusCode"),
            "body": json.loads(body) if isinstance(body, str) else body}


def submit_payload(pkg, revision, bundle_seed, **over):
    """One submit request. The PACKAGE'S FACTS TRAVEL WITH IT -- read at the counterpart's
    HEAD by this battery, which has the checkout, because a Lambda cannot read TypeScript in
    a submodule. The controller still enforces the version gate on whatever it is handed."""
    payload = {
        "action": "submit", "tenant": TENANT, "generation_id": GENERATION,
        "export_revision": revision,
        "report_revisions": [{"report_id": "REP-0001", "revision": bundle_seed,
                              "authorization_ref": "AUTH-1", "immutable": True}],
        "selected_sections": ["S1", "S2"],
        "narrative_packet_ref": {"packet_id": "NAR-0001", "revision": "1", "sha256": "a" * 64},
        "versions": {"template_version": "investor-reporting-render/1.0.0",
                     "renderer_version": "chromium-print/host/irpt-2.0.0",
                     "disclosure_version": "disc/2026-09"},
        "render_options": {"orientation": "LANDSCAPE", "page_size": "Letter",
                           "brand_revision": "V.01"},
        "report_kind": "performance",
        "package": {k: v for k, v in pkg.items() if k != "provenance"},
    }
    payload.update(over)
    return payload


def main():
    print("IB-rt-8 BATTERY -- the export worker renders")
    print("  controller : %s (DEPLOYED; every arm (a)/(c) read is an invoke)" % FUNCTION)
    print("  bound 12   : every subject below is the REAL artifact -- the deployed function,")
    print("               the deployed layer, the four objects that exist, the real roots.")

    # ---------------------------------------------------------------- (b) first: the package
    head("(b) THE REAL PACKAGE, VERSIONED")
    try:
        pkg = package_mod.load()
    except package_mod.PackageUnavailable as exc:
        print("  BLOCKED: %s" % exc)
        record("b", False, "the counterpart's package is readable", str(exc)[:120])
        pkg = None
    if pkg:
        prov = pkg["provenance"]
        print("  checkout that answered           : %s" % prov["checkout"])
        print("  its HEAD                         : %s" % prov["head"])
        print("    (portal/ is a GITLINK, so a linked worktree carries an EMPTY portal and the")
        print("     PRIMARY checkout is what answers -- printed, never assumed)")
        print("  package version                  : %s" % pkg["package_version"])
        print("  declared runtime                 : %s  <- why a Lambda cannot render it"
              % pkg["runtime"])
        print("  print entry point                : %s (PrintEntry.tsx present: %s)"
              % (pkg["print_route"], prov["print_entry_present"]))
        print("  templates                        : %s" % pkg["templates"])
        print("  supported contract versions      :")
        for name in sorted(pkg["supported_contracts"]):
            print("      %-20s %s" % (name, pkg["supported_contracts"][name]))
        contract_version = package_mod.contract_version_of(pkg)
        print("  contract_version for identity    : %s (exactly one, or the identity would be"
              % contract_version)
        print("                                     ambiguous and is REFUSED instead)")
        ok_supported = package_mod.assert_supported(pkg, "ExportBundle", contract_version)
        refusal = None
        try:
            package_mod.assert_supported(pkg, "ExportBundle", "investor-reporting/2")
        except package_mod.PackageRefused as exc:
            refusal = exc
        print("  an UNSUPPORTED version           : %s | %s"
              % (refusal.code if refusal else "NOT REFUSED (the arm fails)",
                 (refusal.reason if refusal else "")[:88]))
        census = package_mod.fixture_in_render_path()
        render_path = [m for m in census["modules_referencing_it"]
                       if m in ("render.py", "handler.py")]
        print("  FIXTURE RETIREMENT census        : file still on disk as round-1 history: %s"
              % census["fixture_file_present"])
        print("      modules mentioning it at all : %s" % census["modules_referencing_it"])
        print("      of those ON THE RENDER PATH  : %s  <- empty is the arm" % (render_path or "[]"))
        source_map = json.loads((REPO / "infra" / "aws" / "lambda" / "ci"
                                 / "lambda-source-map.json").read_text(encoding="utf-8"))
        packaged = source_map["functions"][FUNCTION]["files"]
        fixture_packaged = [f for f in packaged if "render_package" in f]
        print("      and in the ARTIFACT          : %s of %d packaged file(s)  <- 0 is the arm"
              % (len(fixture_packaged), len(packaged)))
        record("b", bool(ok_supported) and refusal is not None
               and refusal.code == package_mod.RENDER_PACKAGE_VERSION
               and not render_path and not fixture_packaged
               and pkg["runtime"] == "browser",
               "the counterpart's real package is read at its HEAD, an unsupported version is "
               "refused, and the fixture is off the render path",
               "package %s from %s@%s; RENDER_PACKAGE_VERSION on an unsupported version; 0 "
               "render-path modules and 0 of %d packaged files reference the fixture"
               % (pkg["package_version"], prov["checkout"].split("\\")[-1], prov["head"][:10],
                  len(packaged)))

    # ---------------------------------------------------------------- (a)
    head("(a) SUBMIT -> READY -> DOWNLOAD, ON THE SERVED SERVICE")
    t0 = time.time()
    first = invoke(submit_payload(pkg, "rt8-a", "b" * 64), "submit1")
    print("  [%.1fs] submit invoke              : statusCode=%s"
          % (time.time() - t0, first.get("statusCode") or first.get("_error", "")[:60]))
    ok_a = False
    body = first.get("body") or {}
    if first.get("statusCode") == 200:
        ident = body["identity"]
        print("  export_id (LOGICAL)              : %s" % ident["export_id"])
        print("  attempt_id (EXPLICIT)            : %s (attempt %d)"
              % (ident["attempt_id"], ident["attempt_number"]))
        print("  bundle_sha256                    : %s" % body["bundle_sha256"][:32])
        print("  contract_version                 : %s" % body["contract_version"])
        persisted = body.get("persisted") or {}
        print("  THE BUNDLE PERSISTED BEFORE RENDER:")
        print("      key                          : %s" % persisted.get("key"))
        print("      bytes / read-back equal      : %s / %s"
              % (persisted.get("bytes"), persisted.get("equal")))
        print("      metadata on the object       : %s" % persisted.get("metadata"))
        headed = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key",
                           persisted.get("key", ""), "--output", "json"])
        print("      head-object (independent)    : ContentLength=%s metadata=%s"
              % (headed.get("ContentLength"), headed.get("Metadata")))
        dispatch_rec = body.get("dispatch") or {}
        pre = dispatch_rec.get("preflight") or {}
        print("  THE DISPATCH DECISION            : %s (sent=%s)"
              % (dispatch_rec.get("decision"), dispatch_rec.get("sent")))
        print("      host                         : %s (%s) state=%s"
              % (pre.get("host", {}).get("host_name"), pre.get("host", {}).get("host_id"),
                 pre.get("host", {}).get("state")))
        print("      document exists              : %s" % pre.get("document_exists"))
        print("      reason, VERBATIM             :")
        for line in _wrap(pre.get("reason", ""), 68):
            print("        %s" % line)
        print("      OPERATOR ACT, verbatim       :")
        for act in (pre.get("operator_act") or []):
            print("        $ %s" % act)
        print("      the UNSENT request           : %s"
              % json.dumps(dispatch_rec.get("request", {}).get("Parameters", {}))[:150])
        # THE RENDER WAS RUN. Andrew's word of 2026-09-11 ~14:5xZ ("Yes ycharts runner may be
        # started") turned the HUMAN-GATED arm into an act, taken ONCE under its own ledger
        # and recorded here. The battery does NOT start a host: it reads the record of the act
        # and reads the WORLD for where the host ended up.
        render = json.loads(RENDER_RECORD.read_text(encoding="utf-8"))
        rmeta = render["_meta"]
        print("  THE RENDER, ON ANDREW'S WORD     : \"%s\"" % rmeta["word"])
        print("      source                       : %s" % rmeta["word_source"].split(";")[0])
        print("      host / document              : %s / %s" % (rmeta["host"], rmeta["document"]))
        for step in render["cycle"]:
            print("      [%s] %-10s rc=%s" % (step["at"], step["step"], step["rc"]))
        print("      SSM command status           : %s" % render["command"]["status"])
        print("      the refusal, VERBATIM        : %s"
              % render["command"]["stderr"].splitlines()[0][:150])
        guard = render["network_guard"] or {}
        print("  THE NETWORK GUARD -- A REAL BROWSER ON A REAL HOST, with its denominator:")
        print("      %s" % guard.get("denominator"))
        for origin, count in sorted((guard.get("requests_by_origin") or {}).items()):
            print("      %-34s %d request(s)%s"
                  % (origin, count,
                     "  <- FOREIGN" if origin in (guard.get("foreign_origins") or []) else ""))
        print("  THE RE-CUT BAR (row W4-S23): '0 external connections' is unachievable against")
        print("      the portal as built (the sign-in page fetches Google webfonts), so the bar")
        print("      the criterion actually protects is VENDOR calls, over an ENUMERATED list:")
        vendor_ok, vendor_lines = vendor_bar_report(guard)
        for line in vendor_lines:
            print(line)
        print("  RENDER ARM                       : SESSION-GATED -- the browser opened, reached")
        print("      the REAL portal origin and found a SIGN-IN SCREEN; render_export.cjs")
        print("      refuses SESSION_ABSENT by design and never signs in. An authenticated")
        print("      session for the host is IB-rtb-1's build item. The issuer's amendment")
        print("      names exactly this branch, so this is the arm's own rule, not a skip.")
        host_state = aws_json(["ec2", "describe-instances", "--instance-ids",
                               rmeta["host"].split("(")[-1].strip(") "),
                               "--region", "us-east-1", "--query",
                               "Reservations[].Instances[].State.Name", "--output", "json"])
        live_state = host_state[0] if isinstance(host_state, list) and host_state else None
        print("  THE HOST RETURNED TO ITS DECLARED STATE: record says %s, LIVE read says %s"
              % (render["final_instance_state"], live_state))
        print("      The word is a CYCLE, not a new resting state -- a host left running after")
        print("      a render is drift against aws_ec2_instance_state.runner, not a permission.")

        # THE DOWNLOAD HALF, on the real guarded route with the real authz library.
        enforcer, deps = _enforcer()
        artifacts = {ident["export_id"]: {"key": body["artifact_key"], "bucket": BUCKET,
                                          "exists": False}}
        signer = download_mod.FixtureSigner(BUCKET, ttl_seconds=120)
        route = download_mod.make_download_route(enforcer, artifacts, signer, {})
        served = route(_request(ident["export_id"]))
        url_ok, url_problems = download_mod.verify(served.payload["url"], BUCKET)
        print("  DOWNLOAD, reauthorized           : ok=%s Opal-signed=%s ttl=%ds problems=%s"
              % (served.ok, url_ok, served.payload["ttl_seconds"], url_problems or "none"))
        deps.revoke()
        again = route(_request(ident["export_id"]))
        print("  after a REVOKED grant            : ok=%s code=%s  (the artifact record is"
              % (again.ok, getattr(again, "code", None)))
        print("      untouched and the cache was not cleared -- only the grant moved)")
        deps.restore()
        ok_a = (persisted.get("equal") is True
                and not failed(headed) and headed.get("ContentLength")
                and dispatch_rec.get("decision") == dispatch_mod.HUMAN_GATED
                and dispatch_rec.get("sent") is False
                and served.ok and url_ok and not again.ok
                # THE RENDER HALF: the command RAN on the host, the guard MEASURED the
                # traffic, no vendor origin was touched, and the host is back where the
                # ycharts root declares it. The refusal itself is not a failure of this arm --
                # the amendment admits SESSION-GATED by name -- but a SILENT one would be.
                and render["command"]["status"] in ("Success", "Failed")
                and "SESSION_ABSENT" in render["command"]["stderr"]
                and vendor_ok  # the re-cut bar (row W4-S23): 0 VENDOR connections, enumerated
                and render["final_instance_state"] == "stopped"
                and live_state == "stopped")
    record("a", ok_a,
           "the served controller freezes and PERSISTS the bundle before any render, decides "
           "the dispatch, the download reauthorizes, and the RENDER RAN on the host and reads "
           "SESSION-GATED with its network denominator measured",
           "bundle persisted and read back equal, confirmed by an independent head-object; "
           "dispatch HUMAN_GATED with the operator act printed verbatim and 0 commands sent by "
           "the CONTROLLER; 1 download served and 1 refused after revocation; the OPERATOR "
           "cycle ran the document on i-0167fd745ad906a66, the browser reached the portal "
           "origin and refused SESSION_ABSENT, the guard measured 2 foreign of 12 requests "
           "with 0 vendor, and the host is back to stopped on a LIVE read")

    # ---------------------------------------------------------------- (c)
    head("(c) FIVE OF FIVE IN THE RUNTIME")
    caps = invoke({"action": "capabilities"}, "caps")
    cbody = caps.get("body") or {}
    print("  contracts_dir (in the Lambda)    : %s" % cbody.get("contracts_dir"))
    print("  contracts_available              : %s" % cbody.get("contracts_available"))
    for name in sorted(cbody.get("contracts", {})):
        row = cbody["contracts"][name]
        print("      %-20s available=%s  %s" % (name, row.get("available"),
                                                row.get("schema_id") or row.get("reason")))
    # THE VERSION IS READ FROM THE FUNCTIONS, NOT TYPED HERE. A battery that hardcodes a
    # layer version measures the number its author remembered; this reads the one the
    # deployed functions actually reference, and then asks the layer about itself.
    referencing, versions = [], set()
    arns_by_fn = {}
    for fn in FUNCTIONS:
        cfg = aws_json(["lambda", "get-function-configuration", "--function-name", fn,
                        "--region", "us-east-1", "--output", "json"])
        arns = [x["Arn"] for x in cfg.get("Layers", [])]
        arns_by_fn[fn] = arns
        hit = any(("layer:%s:" % LAYER) in a for a in arns)
        referencing.append(hit)
        for arn in arns:
            if ("layer:%s:" % LAYER) in arn:
                versions.add(arn.rsplit(":", 1)[-1])
    version = sorted(versions)[0] if len(versions) == 1 else None
    print("  layer version the functions use  : %s  (%d distinct value(s) across %d "
          "function(s) -- more than one would mean a partial re-point)"
          % (version or sorted(versions), len(versions), len(FUNCTIONS)))
    layer = aws_json(["lambda", "get-layer-version", "--layer-name", LAYER,
                      "--version-number", version or "0", "--output", "json"])
    print("  get-layer-version %s:%s   : CodeSha256=%s size=%s runtimes=%s"
          % (LAYER, version, (layer.get("Content") or {}).get("CodeSha256"),
             (layer.get("Content") or {}).get("CodeSize"),
             layer.get("CompatibleRuntimes")))
    built = json.loads((REPO / "infra" / "aws" / "lambda" / "layers" / "irpt-common"
                        / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
    published = (layer.get("Content") or {}).get("CodeSha256")
    print("  built layer sha256 (this cell)   : %s" % built["zip_sha256_base64"])
    print("  published layer sha256           : %s" % published)
    print("  equal                            : %s -- and THIS IS NOT THE ARM."
          % (published == built["zip_sha256_base64"]))
    print("      `irpt-common` is a SHARED surface: one S3 key and one terraform-managed")
    print("      layer version, written by more than one round-2 cell. IB-rt-3's ids.py and")
    print("      raw_keys.json are in the published artifact beside this cell's five")
    print("      contracts and key grammar, so the published digest is a UNION and cannot")
    print("      equal any single cell's local build. Asserting equality here would make a")
    print("      correct, merged layer read as a failure. Row IRPT_BCKEND-W4-S15 records the")
    print("      collision; what this arm asserts is the RUNTIME READ below.")
    print("  the layer also carries the shared key grammar and the firm registry:")
    for row in built.get("modules", []) + built.get("data", []):
        print("      %-34s @%s" % (row["packaged_as"], row["pin"][:10]))
    for fn in FUNCTIONS:
        print("      %-26s %s" % (fn, arns_by_fn[fn] or "NONE"))
    print("  functions referencing the layer  : %d of %d" % (sum(referencing), len(FUNCTIONS)))
    record("c", cbody.get("contracts_available") == "5 of 5"
           and str(cbody.get("contracts_dir")).startswith("/opt/python")
           and sum(referencing) == len(FUNCTIONS) and not failed(layer)
           and version is not None and published,
           "all five contracts are readable from the layer INSIDE the runtime and every "
           "function references the SAME published version",
           "%s read from %s INSIDE the runtime; layer version %s, ONE distinct value across "
           "%d of %d functions; the published digest %s is a UNION across concurrent cells "
           "and is printed rather than asserted equal to this cell's build"
           % (cbody.get("contracts_available"), cbody.get("contracts_dir"), version,
              sum(referencing), len(FUNCTIONS), str(published)[:16]))

    # ---------------------------------------------------------------- (d)
    head("(d) STABLE IDENTITY")
    retry = invoke(submit_payload(pkg, "rt8-a", "b" * 64), "submit2")
    changed = invoke(submit_payload(pkg, "rt8-a", "c" * 64), "submit3")
    rb, cb = retry.get("body") or {}, changed.get("body") or {}
    same = (body.get("identity", {}).get("export_id")
            == rb.get("identity", {}).get("export_id"))
    differs = (body.get("identity", {}).get("export_id")
               != cb.get("identity", {}).get("export_id"))
    print("  IDENTICAL INPUT, two submits:")
    print("      export_id  #1 / #2           : %s / %s"
          % (body.get("identity", {}).get("export_id"),
             rb.get("identity", {}).get("export_id")))
    print("      equal                        : %s  <- the arm (round 1 minted a NEW id here,"
          % same)
    print("                                     because it keyed on the ARTIFACT digest)")
    print("      bundle_sha256 #1 / #2        : %s / %s"
          % (str(body.get("bundle_sha256"))[:16], str(rb.get("bundle_sha256"))[:16]))
    print("      attempt_id  #1 / #2          : %s / %s"
          % (body.get("identity", {}).get("attempt_id"),
             rb.get("identity", {}).get("attempt_id")))
    print("      attempt number               : %s / %s (the retry rule: %s)"
          % (body.get("identity", {}).get("attempt_number"),
             rb.get("identity", {}).get("attempt_number"), rb.get("retry_reason")))
    print("  CHANGED INPUT:")
    print("      export_id                    : %s" % cb.get("identity", {}).get("export_id"))
    print("      differs from #1              : %s  <- the arm" % differs)
    print("      bundle_sha256                : %s" % str(cb.get("bundle_sha256"))[:16])
    print("  THE RAW DIGEST is not in either id: it stays in the receipt's artifact.sha256,")
    print("      where an artifact hash belongs. A print engine stamps a creation date and a")
    print("      document /ID into every PDF, so the raw digest CANNOT be a stable identity --")
    print("      measured in round 1: 25,231 bytes twice, two different sha256.")
    record("d", same and differs,
           "an identical-input retry is the SAME logical export and a changed input is a "
           "different one",
           "2 of 2 identical submits share one export_id; 1 of 1 changed submit differs; the "
           "attempt id is explicit and distinct in both")

    # ---------------------------------------------------------------- (e)
    head("(e) EXCLUSION PROVED -- and the population is SMALLER, BY ANDREW'S WORD")
    # BOTH SYNTHETIC GENERATIONS, not just the one the ruling named. This cell's own proof
    # submits write bundles under GENRT8PROOF, and an arm that censused only GENIBS14SYN
    # would have left its own objects outside the population it was proving clean.
    #
    # THIS ARM USED TO READ FIVE LIVE OBJECTS AND ASSERT 5 OF 5 STILL HEADED 200. Four of
    # them were deleted by arm (g) on Andrew's word, so it cannot read them live any more --
    # and the honest form is to say which half is live and which is a record, not to keep an
    # assertion that would now be false or to quietly drop the four from the denominator.
    rows = []
    for prefix in (SYNTHETIC_PREFIX, PROOF_PREFIX):
        listing = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix",
                            prefix, "--output", "json"])
        got = listing.get("Contents", []) if not failed(listing) else []
        print("  prefix %-58s %d object(s)" % (prefix, len(got)))
        rows.extend(got)
    inventory = []
    for row in rows:
        headed = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", row["Key"],
                           "--output", "json"])
        inventory.append({"Key": row["Key"], "Size": row["Size"],
                          "Metadata": headed.get("Metadata", {}),
                          "head_rc_ok": not failed(headed)})
    print("  LIVE INVENTORY, both synthetic generations : %d object(s)" % len(inventory))
    for row in inventory:
        print("      %-58s %7d  %s"
              % (row["Key"].split("exports/")[-1], row["Size"], row["Metadata"]))
    verdicts = [exclusion_mod.classify(r["Key"], r["Metadata"])[0] for r in inventory]
    print("  classification                   : %s" % verdicts)
    census_rows = exclusion_mod.census(inventory)
    print("  PER PRODUCTION READER (denominator %d object(s)):" % len(inventory))
    for row in census_rows:
        print("      %-14s admitted %d of %d, excluded %d"
              % (row["reader"], row["admitted"], row["objects"], row["excluded"]))
    ordinary = [{"Key": "firms/49financial/generations/GEN-0042/attempts/1/exports/r1/report.pdf",
                 "Metadata": {}}]
    control = exclusion_mod.census(ordinary)
    print("  THE CONTROL -- an ORDINARY export object, same readers:")
    for row in control:
        print("      %-14s admitted %d of %d  <- a filter that excludes everything is not a "
              "filter" % (row["reader"], row["admitted"], row["objects"]))
    after = [aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", r["Key"],
                       "--output", "json"]) for r in inventory]
    still = sum(1 for h in after if not failed(h))
    print("  NOTHING THIS ARM READS WAS TOUCHED BY IT: %d of %d live key(s) still head-object"
          % (still, len(inventory)))
    print("      200 AFTER the census. exclusion.py contains no delete_object, copy_object or")
    print("      put_object -- asserted by a test, not by this sentence. The four deletes are")
    print("      arm (g)'s, taken under their own ledger on Andrew's word, never here.")

    # THE FOUR DELETED KEYS, RE-RUN FROM THE COMMITTED RECORD. The readers are pure functions
    # of (key, metadata); the record supplies both. What the record CANNOT supply is whether
    # the objects exist -- that is arm (g)'s live 404, and it is not claimed here.
    recorded = json.loads(DELETE_RECEIPTS.read_text(encoding="utf-8"))
    gone_rows = [{"Key": k, "Metadata": (recorded["before"]["head"][k].get("Metadata") or {})}
                 for k in recorded["keys"]]
    gone_verdicts = [exclusion_mod.classify(r["Key"], r["Metadata"])[0] for r in gone_rows]
    gone_census = exclusion_mod.census(gone_rows)
    print("  THE FOUR DELETED KEYS, from the COMMITTED RECORD (%s):"
          % DELETE_RECEIPTS.name)
    print("      classification               : %s" % gone_verdicts)
    for row in gone_census:
        print("      %-14s admitted %d of %d" % (row["reader"], row["admitted"], row["objects"]))
    print("      THIS IS A RECORD, NOT A LIVE READ -- the objects are gone. Whether they are")
    print("      gone is measured in arm (g); what is measured HERE is only that the readers")
    print("      excluded them on the key and metadata they carried while they existed.")

    readers_ok = all(r["admitted"] == 0 for r in census_rows)
    control_ok = all(r["admitted"] == 1 for r in control if r["reader"] in
                     ("export_status", "download"))
    gone_ok = (len(gone_rows) == 4
               and all(v == exclusion_mod.EXCLUDED_BY_BOTH for v in gone_verdicts)
               and all(r["admitted"] == 0 for r in gone_census))
    record("e", len(inventory) >= 1
           and all(v == exclusion_mod.EXCLUDED_BY_BOTH for v in verdicts)
           and readers_ok and control_ok and gone_ok and still == len(inventory),
           "every production reader excludes the synthetic evidence -- the objects that live "
           "and the four the word removed",
           "LIVE: %d of %d objects EXCLUDED_BY_BOTH and %d of %d readers admit 0 of %d, with "
           "the control still admitting an ordinary object; RECORDED: 4 of 4 deleted keys "
           "EXCLUDED_BY_BOTH and %d of %d readers admit 0 of 4; %d of %d live keys still head "
           "200 after"
           % (len(verdicts), len(inventory), len(census_rows), len(census_rows),
              len(inventory), len(gone_census), len(gone_census), still, len(inventory)))

    # ---------------------------------------------------------------- (f)
    head("(f) LEDGERS AND PLANS")
    ledger_text = LEDGER.read_text(encoding="utf-8")
    closed = "**Status:** CLOSED" in ledger_text
    # --full-history OR THIS READS EMPTY. The sentinel was ADDED and DELETED inside a branch
    # that was merged, and `git log -- <path>` simplifies exactly that shape away: the file
    # never appears on the first-parent walk, so a plain log prints nothing and the arm would
    # report "no sentinel commit" about a sentinel that was committed and removed correctly.
    sha = subprocess.run(["git", "log", "-1", "--full-history", "--format=%H %s", "--",
                          "org/critical_paths/.open_deploys/irpt-bckend-rt8.json"],
                         cwd=str(REPO), capture_output=True)
    print("  LEDGER irpt-bckend-rt8           : entry reads CLOSED=%s; sentinel on disk=%s"
          % (closed, SENTINEL.exists()))
    print("      sentinel commit              : %s"
          % sha.stdout.decode("utf-8", "replace").strip()[:104])
    # THE YCHARTS ROOT IS PLANNED TOO, because this cell amended it. Its edit is a header
    # comment and one OUTPUT DESCRIPTION, and Terraform stores neither in state -- so the
    # honest thing to print is that the plan is clean AND that a clean plan does not prove the
    # description changed. The file is the evidence for the description; the plan is the
    # evidence that nothing ELSE moved, which is the part that could have gone wrong.
    ycharts = subprocess.run(
        [TERRAFORM, "-chdir=infra/aws/terraform/investor-reporting/ycharts", "plan",
         "-no-color", "-input=false", "-lock=false"], cwd=str(REPO), capture_output=True)
    ytext = ycharts.stdout.decode("utf-8", "replace")
    yclean = "No changes. Your infrastructure matches the configuration." in ytext
    print("      ycharts      plan             : %s (rc=%d) -- the root this cell amended;"
          % ("No changes" if yclean else "DRIFT", ycharts.returncode))
    print("      the amendment is a comment block and an output DESCRIPTION, which Terraform")
    print("      does not hold in state, so this line proves nothing ELSE moved -- not that")
    print("      the description changed. The file is the evidence for that.")
    converged = []
    for root in ROOTS:
        proc = subprocess.run(
            [TERRAFORM, "-chdir=infra/aws/terraform/investor-reporting/%s" % root, "plan",
             "-no-color", "-input=false", "-lock=false"], cwd=str(REPO), capture_output=True)
        text = proc.stdout.decode("utf-8", "replace")
        ok = "No changes. Your infrastructure matches the configuration." in text
        converged.append(ok)
        print("      %-12s plan             : %s (rc=%d)"
              % (root, "No changes" if ok else "DRIFT", proc.returncode))
        if not ok:
            # ASCII-ONLY OUT: terraform draws box rules with U+2500, and this console is
            # cp1252 -- printing the plan verbatim raised UnicodeEncodeError and took the
            # battery down AFTER it had measured the drift it was reporting.
            for line in text.splitlines()[-14:]:
                print("          %s" % line.encode("ascii", "replace").decode("ascii"))
    record("f", closed and not SENTINEL.exists() and all(converged) and yclean,
           "the ledger is closed with its sentinel committed and every root this cell touched "
           "re-plans clean",
           "1 of 1 entries CLOSED; %d of %d project roots report No changes, plus the ycharts "
           "root this cell amended" % (sum(converged), len(ROOTS)))

    # ---------------------------------------------------------------- (g)
    head("(g) THE FOUR SYNTHETIC EXPORTS DELETED ON ANDREW'S WORD")
    rec = json.loads(DELETE_RECEIPTS.read_text(encoding="utf-8"))
    meta, keys = rec["_meta"], rec["keys"]
    print("  THE WORD, VERBATIM               : \"%s\"" % meta["word"])
    print("      source                       : %s" % meta["word_source"])
    print("      it covers                    : %d key(s) in %s, and NOTHING else -- no other"
          % (len(keys), meta["bucket"]))
    print("                                     object, prefix or firm")
    print("  THE LEDGER                       : %s" % pathlib.Path(meta["ledger"]).name)
    print("      sentinel committed BEFORE    : %s" % meta["sentinel_commit"])
    print("  THE RECEIPTS (a receipt is a CLAIM; the 404 beside it is the MEASUREMENT):")
    live_gone, receipts_ok = 0, 0
    for row in rec["receipts"]:
        key, resp = row["key"], row["response"]
        headed = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", key,
                           "--output", "json"])
        gone = failed(headed) and ("404" in headed["_error"] or "Not Found" in headed["_error"])
        live_gone += 1 if gone else 0
        receipts_ok += 1 if resp.get("DeleteMarker") else 0
        print("      %-50s DeleteMarker=%s marker=%s"
              % (key.split("exports/")[-1], resp.get("DeleteMarker"),
                 str(resp.get("VersionId"))[:18]))
        print("      %-50s LIVE head-object -> %s"
              % ("", "404 Not Found" if gone else "STILL PRESENT (the arm fails)"))
    listing = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET,
                        "--prefix", rec["_meta"].get("prefix", SYNTHETIC_PREFIX),
                        "--output", "json"])
    remaining = [c["Key"] for c in listing.get("Contents", [])] if not failed(listing) else []
    unexpected = [k for k in remaining if k not in keys]
    print("  LIVE listing under %-36s : %d object(s) remaining, %d unexpected"
          % (SYNTHETIC_PREFIX, len(remaining), len(unexpected)))
    spare_key = rec["after"]["blast_radius_control"]["key"]
    spare = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", spare_key,
                      "--output", "json"])
    spare_ok = not failed(spare)
    print("  THE BLAST-RADIUS CONTROL         : an object the word does NOT cover --")
    print("      %s" % spare_key)
    print("      still head-object 200        : %s  <- a delete that removed everything would"
          % spare_ok)
    print("                                     be indistinguishable from this one without it")
    print("  THE GRAIN, STATED RATHER THAN IMPLIED:")
    for line in _wrap(meta["delete_grain"], 70):
        print("      %s" % line)
    g_closed = "**Status:** CLOSED" in DELETE_LEDGER.read_text(encoding="utf-8")
    print("  LEDGER irpt-bckend-rt8-synthetic-delete : CLOSED=%s; sentinel on disk=%s"
          % (g_closed, DELETE_SENTINEL.exists()))
    print("\n  %d of %d deleted, %d of %d remaining, %d unexpected objects"
          % (live_gone, len(keys), len(keys) - live_gone, len(keys), len(unexpected)))
    record("g", live_gone == 4 and receipts_ok == 4 and not unexpected and spare_ok
           and g_closed and not DELETE_SENTINEL.exists(),
           "the four synthetic exports named by Andrew's word are gone, and nothing else was "
           "touched",
           "4 of 4 delete receipts carry DeleteMarker=true and 4 of 4 keys now head 404; %d "
           "unexpected object(s) under the prefix; the uncovered control object still heads "
           "200; the deletion ledger is CLOSED with its sentinel committed before the act"
           % len(unexpected))

    # ---------------------------------------------------------------- verdict
    head("VERDICT")
    for arm, ok, claim, _ in RESULTS:
        print("  %s  (%s) %s" % ("PASS" if ok else "FAIL", arm, claim))
    passed = sum(1 for _, ok, _, _ in RESULTS if ok)
    print("\n  %d of %d mechanical arms passed" % (passed, len(RESULTS)))
    print("  RENDER STEP: RAN on i-0167fd745ad906a66 and reads SESSION-GATED; the")
    print("  network guard measured 2 foreign of 12 requests, 0 of them vendor.")
    if passed == len(RESULTS):
        print("IBRT8-EXPORT-RENDERS")
        return 0
    return 1


def _wrap(text, width):
    words, line, out = str(text).split(), "", []
    for word in words:
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def _enforcer():
    binding = _authz.FirmBinding(TENANT, authz_fixtures.OPAQUE_FIRM)
    deps = authz_fixtures.Deps()
    return _authz.Enforcer(binding, deps.load_directory, deps.load_ownership,
                           deps.load_policy, artifacts=dict(authz_fixtures.ARTIFACTS),
                           cache={}), deps


def _request(export_id):
    return _authz.Request(authz_fixtures.headers(), download_mod.DOWNLOAD_OPERATION,
                          "pdf", authz_fixtures.PDF_OK, {"export_id": export_id})


if __name__ == "__main__":
    sys.exit(main())
