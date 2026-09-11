"""IB-rt-8 acceptance battery -- RT8-AC1.

Six arms -- (a) through (f) -- each printing its own denominators, and the token only when
every one holds. The token is IBRT8-EXPORT-RENDERS.

THE SUBJECT IS THE REAL ARTIFACT, NEVER A COPY THIS FILE WRAPS (bound 12). Arm (a) runs
against the DEPLOYED controller by `aws lambda invoke`; arm (c) reads the DEPLOYED layer and
the three DEPLOYED functions; arm (e) censuses the FOUR OBJECTS THAT EXIST in the bucket; arm
(f) reads the ledger entry and re-plans the three real roots. Nothing here registers a
handler with itself and then measures it.

THE RENDER ARM IS HUMAN-GATED AND SAYS SO, WITH THE RECORD VERBATIM. RT8-AC1 (a) admits that
as the arm's own rule. What is gated is exactly one step -- a browser opening the
counterpart's print route -- and every step around it is taken on the served service and
printed.

ASCII only. Python 3.12.
"""
from __future__ import annotations

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

import dispatch as dispatch_mod    # noqa: E402
import download as download_mod    # noqa: E402
import enforce as _authz           # noqa: E402
import exclusion as exclusion_mod  # noqa: E402
import fixtures as authz_fixtures  # noqa: E402
import package as package_mod      # noqa: E402

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
        print("  RENDER ARM                       : HUMAN-GATED -- admitted by RT8-AC1 (a) as")
        print("      the arm's own rule. The record above is the operator's act, executable")
        print("      rather than described. The render itself (a browser opening the print")
        print("      route) is the ONE step not taken; every step around it ran on the served")
        print("      service. See infra/aws/ec2/investor-reporting-export/README.md for why")
        print("      no reachable host may be started by this cell.")
        print("  0 EXTERNAL CONNECTIONS DURING THE RENDER: no render ran, so there is no host")
        print("      guard log to read. THIS IS PRINTED AS VACUOUS, never as a pass (bound 12).")
        print("      The guard exists in the host half and writes render_guard.json beside the")
        print("      PDF with its own denominator; it is measured at the operator's run.")

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
                and served.ok and url_ok and not again.ok)
    record("a", ok_a,
           "the served controller freezes and PERSISTS the bundle before any render, decides "
           "the dispatch, and the download reauthorizes -- the render step reads HUMAN-GATED",
           "bundle persisted and read back equal, confirmed by an independent head-object; "
           "dispatch HUMAN_GATED with the operator act printed verbatim and 0 commands sent; "
           "1 download served and 1 refused after revocation")

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
    head("(e) EXCLUSION PROVED -- and nothing moved, nothing deleted")
    # BOTH SYNTHETIC GENERATIONS, not just the one the ruling named. This cell's own proof
    # submits write bundles under GENRT8PROOF, and an arm that censused only GENIBS14SYN
    # would have left its own objects outside the population it was proving clean.
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
    print("  INVENTORY, both synthetic generations : %d object(s)" % len(inventory))
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
    print("  0 DELETES ISSUED                 : all %d key(s) still head-object 200 AFTER the"
          % still)
    print("      battery. This cell has no writer on them: exclusion.py contains no")
    print("      delete_object, copy_object or put_object, asserted by a test. Deletion is")
    print("      Andrew's word and is CARRIED on the instance, not taken here.")
    readers_ok = all(r["admitted"] == 0 for r in census_rows)
    control_ok = all(r["admitted"] == 1 for r in control if r["reader"] in
                     ("export_status", "download"))
    ruling_four = [r for r in inventory if "GENIBS14SYN" in r["Key"]]
    record("e", len(ruling_four) == 4
           and all(v == exclusion_mod.EXCLUDED_BY_BOTH for v in verdicts)
           and readers_ok and control_ok and still == len(inventory),
           "the four synthetic objects are inventoried, every production reader excludes "
           "them, and none was moved or deleted",
           "%d of %d objects EXCLUDED_BY_BOTH predicates (the ruling's 4 under GENIBS14SYN "
           "plus this cell's own proof bundles under GENRT8PROOF); %d of %d readers admit 0 "
           "of %d; the control shows the readers still admit an ordinary object; %d of %d "
           "keys still head 200 after"
           % (len(verdicts), len(inventory), len(census_rows), len(census_rows),
              len(inventory), still, len(inventory)))

    # ---------------------------------------------------------------- (f)
    head("(f) LEDGERS AND PLANS")
    ledger_text = LEDGER.read_text(encoding="utf-8")
    closed = "**Status:** CLOSED" in ledger_text
    sha = subprocess.run(["git", "log", "-1", "--format=%H %s", "--",
                          "org/critical_paths/.open_deploys/irpt-bckend-rt8.json"],
                         cwd=str(REPO), capture_output=True)
    print("  LEDGER irpt-bckend-rt8           : entry reads CLOSED=%s; sentinel on disk=%s"
          % (closed, SENTINEL.exists()))
    print("      sentinel commit              : %s"
          % sha.stdout.decode("utf-8", "replace").strip()[:104])
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
    record("f", closed and not SENTINEL.exists() and all(converged),
           "the ledger is closed with its sentinel committed and all three roots re-plan clean",
           "1 of 1 entries CLOSED; %d of %d roots report No changes"
           % (sum(converged), len(ROOTS)))

    # ---------------------------------------------------------------- verdict
    head("VERDICT")
    for arm, ok, claim, _ in RESULTS:
        print("  %s  (%s) %s" % ("PASS" if ok else "FAIL", arm, claim))
    passed = sum(1 for _, ok, _, _ in RESULTS if ok)
    print("\n  %d of %d mechanical arms passed" % (passed, len(RESULTS)))
    print("  RENDER STEP: HUMAN-GATED, record printed verbatim in arm (a).")
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
