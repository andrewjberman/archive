"""IB-pr-456 assembler (ASCII). From the worktree root:
    python <this file> <scratch_dir>
Reads: IB152-1_source_map_census.json, IB152-1_live_reads.json, IB152-1_live_configuration.json, IB152-1_replay.json, IB152-1_readers.json,
member_classes.json (this directory); <scratch>/live/<fn>.zip, <scratch>/zips/<fn>.1.zip and .2.zip (the two BUILD_ONLY builds per function),
the three closure limbs run on both zips of each function, and the moved-members probe. Writes IB152-1_release_read.json. Nothing is written
to AWS; no firm name, account id or bucket name is written."""
import base64
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

D = Path("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~312")
scratch = Path(sys.argv[1])
BASE = subprocess.run(["git", "rev-parse", "e7bb7e923a"], capture_output=True, check=True).stdout.decode().strip()
FNS = ["irpt-ycharts-generate", "irpt-status", "irpt-commentary-draft-store-lambda", "irpt-commentary-composition-read-lambda"]
Y2 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/signature_closure.py"
M285 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~285/"
IB455 = "74bbdbb322"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


def last(script, zp):
    r = subprocess.run([sys.executable, script, str(zp)], capture_output=True, timeout=120)
    return r.stdout.decode("utf-8", "replace").strip().splitlines()


def ascii_(s):
    return s.encode("ascii", "replace").decode("ascii")


census = load(D / "IB152-1_source_map_census.json")
live_reads = {x["function"]: x for x in load(D / "IB152-1_live_reads.json")["live_reads"]}
conf = {x["function"]: x for x in load(D / "IB152-1_live_configuration.json")["live_configuration"]}
replay = load(D / "IB152-1_replay.json")
readers = load(D / "IB152-1_readers.json")
classes = load(D / "member_classes.json")
repins = load(D / "candidate_repins.json")
smap = json.loads(subprocess.run(["git", "show", "e7bb7e923a:infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode("utf-8"))["functions"]
moved_all = json.loads(subprocess.run([sys.executable, str(D / "moved_members_probe.py"), str(scratch), "e7bb7e923a"] + FNS, capture_output=True, check=True).stdout.decode("utf-8"))
THREE = {"submission.py", "acceptance.py", "contracts/AnalysisSubmissionRequest.schema.json"}
PLACE = {"submission.py": "submission.py", "acceptance.py": "acceptance.py", "contracts/AnalysisSubmissionRequest.schema.json": "AnalysisSubmissionRequest.schema.json"}

functions = []
for fn in FNS:
    lr, cf, e = live_reads[fn], conf[fn], smap[fn]
    z1, z2, lz = (scratch / "zips" / (fn + ".1.zip")), (scratch / "zips" / (fn + ".2.zip")), (scratch / "live" / (fn + ".zip"))
    b1, b2, lb = z1.read_bytes(), z2.read_bytes(), lz.read_bytes()
    assert b64(lb) == lr["live_code_sha256"], fn
    mv = moved_all[fn]
    moved = []
    for m in mv["moved"]:
        c = classes[fn][m["member"]]
        commits = [{"commit": x["commit"], "subject": ascii_(x["subject"]), "is_ib_pr_455": x["commit"].startswith(IB455)} for x in m["owning_commits"]]
        moved.append({"member": m["member"], "repo_path": m["repo_path"], "live_sha": m["live_sha"], "built_sha": m["built_sha"], "live_blob_commit": m["live_blob_commit"],
                      "built_bytes_equal_base_blob": m["built_bytes_equal_base_blob"], "owning_commits": commits, "class": c["class"], "one_line": c["one_line"],
                      "is_one_of_the_three": c["is_one_of_the_three"], "owning_commits_not_ib_pr_455": [x["commit"] for x in commits if not x["is_ib_pr_455"]]})
        assert c["is_one_of_the_three"] == (m["member"] in THREE), (fn, m["member"])
    names_moved = {m["member"] for m in moved}
    packaged = {}
    for k, label in PLACE.items():
        if k == "contracts/AnalysisSubmissionRequest.schema.json" and not any(i.filename == k for i in zipfile.ZipFile(lz).infolist()):
            packaged[label] = "not_packaged"
        else:
            packaged[label] = "moves" if k in names_moved else "packaged_and_does_not_move"
    riders = [m["member"] for m in moved if not m["is_one_of_the_three"]]
    limbs = {}
    for side, zp in (("live", lz), ("built", z1)):
        limbs[side] = {"name": last(Y2, zp)[-1], "attribute": last(M285 + "signature_closure_attr.py", zp)[-1], "method": last(M285 + "method_call_limb_426.py", zp)[-1]}
    own = [r for r in repins["repins"] if r["function"] == fn]
    functions.append({
        "function": fn, "source_dir": e["source_dir"], "handler": cf["handler"],
        "live_code_sha256": lr["live_code_sha256"], "live_read_at_utc": lr["live_read_at_utc"], "live_last_modified": lr["live_last_modified"],
        "live_package_downloaded_sha256_equals_live_code_sha256": lr["downloaded_zip_equals_live_code_sha256"],
        "rollback_version_id": lr["rollback_version_id"], "rollback_version_is_the_latest_object": any(v["is_latest"] and v["version_id"] == lr["rollback_version_id"] for v in lr["versions"]),
        "artifact_object_versions_total": lr["versions_of_key"], "artifact_object_versions_same_size_as_live": lr["versions_of_key_same_size_as_live"],
        "map_artifact_sha256_equals_live_code_sha256": e.get("artifact_sha256") == lr["live_code_sha256"],
        "candidate_rows_repinned": [{"packaged_as": r["packaged_as"], "old_pin": r["old_pin"][:10], "new_pin": r["new_pin"][:10], "bytes_changed": r["bytes_changed"]} for r in own],
        "candidate_rows_repinned_note": ("none: this function's submission.py and acceptance.py are NATIVE members of its source_dir (no staged_from row pins them), "
                                         "so the builder reads them from the worktree, which is the base; only the staged schema row is re-pinned") if fn == "irpt-ycharts-generate" else "",
        "build": {"outcome": "BUILT", "built_sha256": b64(b1), "built_sha256_hex": hashlib.sha256(b1).hexdigest(), "built_bytes": len(b1), "built_twice_identical": b1 == b2 and b64(b1) == b64(b2),
                  "members_live": mv["members_live"], "members_built": mv["members_built"],
                  "command": "BAU_SOURCE_MAP_OVERRIDE=<candidate map: make_candidate_map.py e7bb7e923a> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting %s (TMPDIR in scratch, run twice)" % fn},
        "closure_limbs": limbs,
        "moved_members": moved, "changed_members_packaged": packaged, "riders": riders,
        "added_members": mv["added"], "removed_members": mv["removed"],
        "members_unchanged": mv["members_built"] - len(moved),
        "minimal_release": "RIDERS_MOVE_WITH_THEM" if riders else "ONLY_THE_CHANGED_MEMBERS_MOVE",
    })

# ---- AMENDMENT 1
G = "infra/aws/lambda/investor-reporting/"
after_read = {
    "function": "irpt-ycharts-generate",
    "proposal_for_the_CTO_to_rule_on": ("This is TEXT FOR A SENIOR SEAT TO RULE ON. It does not say that the CTO half's ordering condition (87d92b7c3b, condition 1) is lifted, and the "
                                        "worker cannot lift it. It proposes an after-read for THIS release (the minimal candidate AHxuDf7h...) that makes no vendor call at any step."),
    "steps": [
        {"step": "1. the package", "route_or_call": "aws lambda get-function-configuration, then ONE direct invoke of {\"irpt_import_census\": true} (generate_installed.py:500-505, import_census :483-497: imports only, no route, no write, no vendor call)",
         "what_is_read_back": "CodeSha256 equal to the built digest; failed == {} for every packaged top-level module", "through_which_reader": "generate_installed.import_census"},
        {"step": "2. a submission WITHOUT the member, accepted",
         "route_or_call": "POST /api/scoped/investor-reporting/analysis (operation analysis-requests; entry.py:97-138 -> generate_installed.RoutedSubmissionService.submit :250-253 -> SubmissionService.submit submission_service.py:103-167), one custody or prospect body, made by the principal on the Opal-producer allow list (resident_worker.py:121)",
         "what_is_read_back": "the response {identity, stage RECEIVED, status QUEUED}; then the stored record `analysis#<request_id>#1` by one DynamoDB get-item of the requests table: keys identity, owner, browser_sha256, composition_ref, accepted_at, acting_principal_id and NO commentary_requested; and GET /api/scoped/investor-reporting/analysis/requests/{requestId} (analysis-request-read, irpt-status) answering exactly {identity, accepted_at}",
         "through_which_reader": "DynamoAcceptance.get (acceptance.py:68-71, the same read the get-item makes) and OwnedRequestReader.read (owned_requests.py:245-254)"},
        {"step": "3. a submission WITH the member, accepted",
         "route_or_call": "the same route, a new request id, commentary_requested true, NO ticket_id (so the I3 gate, wherever it is installed, skips it as NO_TICKET: resident_worker.py:193-196)",
         "what_is_read_back": "the stored record carries commentary_requested == true exactly (and false when false is sent); analysis-request-read answers the same {identity, accepted_at} shape as step 2 (the member is not surfaced by any route); the response carries the new ingestion_gate_revision (the schemas digest)",
         "through_which_reader": "DynamoAcceptance.get; OwnedRequestReader.read"},
        {"step": "4. the replay fact (AMENDMENT 1 b)", "route_or_call": "the step 3 body again with commentary_requested dropped (or the step 2 body with it added), same request id",
         "what_is_read_back": "refused CHANGED_INPUTS_SAME_REQUEST_ID (IdempotencyConflict, public_reason_code INVALID_INPUT, acceptance.py:79-80); nothing written; the stored record byte-equal to step 3's",
         "through_which_reader": "DynamoAcceptance.lookup (acceptance.py:73-81) then DynamoAcceptance.get"},
        {"step": "5. a wrong-typed member refused", "route_or_call": "the same route, commentary_requested \"true\"", "what_is_read_back": "refused COMMENTARY_REQUESTED before any write (submission.py validate_public_request; entry.py:117-120 re-raises it as RequestRefused, reason INVALID_INPUT); no item added to either table",
         "through_which_reader": "validate_public_request (entry.py:118)"},
        {"step": "6. a request accepted BEFORE the apply", "route_or_call": "GET analysis-request-read and analysis-request-history (irpt-status) for one existing request",
         "what_is_read_back": "{identity, accepted_at} unchanged; the record by get-item byte-equal to the pre-apply read (no member added to a prior record)", "through_which_reader": "OwnedRequestReader.read and .history (owned_requests.py:245-254, :325+)"},
    ],
    "opal_producer_job_needed": False,
    "why": ("NOT NEEDED to exercise the changed members: acceptance, the member copy, the replay refusal and the queue send all finish inside this function's own code at the dispatch "
            "(submission_service.py:160-167); nothing it changes runs after that. BUT every accepted request is dispatched to the generation queue, and the resident host consumes it: a request "
            "submitted by any other principal is taken down the vendor branch (resident_worker.py:705 worker.run, session acquired at :361-369), which is the very path the CTO half forbids. "
            "A request whose owner principal is on the allow list is taken down the Opal branch instead (resident_worker.py:700-704 producer_for == OPAL -> run_opal), which the code states "
            "makes no vendor call and no session (resident_worker.py:466; ycharts/research/opal_producer.py:1) and goes RECEIVED -> CERTIFYING -> READY. So the steps above must be made by that "
            "principal, and the job that follows is an Opal-producer job: it reaches the host's reads of the accepted record (guard :220-232, producer_for :128-133), opal_producer.produce (reads the "
            "accepted holdings, renders, retains the PDF, persists an AnalysisReport v2), mark_ready (:333-343), send_ready_if_ticketed (:189-200, where the installed host package has it) and "
            "mark_i3_sent (durable_job.py:141). NOT READ by this worker: whether the host is running, whether its INSTALLED package has producer_for/run_opal (the resident_worker.py inside the "
            "irpt-ycharts-generate zip is the OLD one and has neither: replay arm), the allow-listed principal's profile row, and whether the generation queue has any other consumer."),
    "stays_unexercised": [
        {"what": "the queue-consumer entry job.lambda_handler and its consent gate", "code_line": G + "ycharts/generate/job.py:609-629 (IRPT_LIVE_YCHARTS_CALL checked at :617-618)",
         "why_only_a_vendor_generation_reaches_it": "it is packaged but is not this function's configured handler (generate_installed.lambda_handler, generate_installed.py:500); it is reached only by a consumer run holding the per-use word for a live vendor call"},
        {"what": "GenerationJob.run / resume / after_create: the vendor portfolio create, holdings upload, generate and read-back sequence", "code_line": G + "ycharts/generate/job.py:314-513",
         "why_only_a_vendor_generation_reaches_it": "every step is a vendor request; only a vendor generation executes them"},
        {"what": "Transport: the browserless REST replay of the vendor session (request, cookie rotation, persist)", "code_line": G + "ycharts/generate/transport.py:420-516",
         "why_only_a_vendor_generation_reaches_it": "it is the vendor HTTP client; no accepted-request, status or Opal path constructs it"},
        {"what": "ResidentGenerationWorker.run: session acquire and refresh, vendor download, refused-PDF keep, then mark_ready after a vendor receive", "code_line": G + "ycharts/generate/resident_worker.py:264-281,348-448 (keep_refused_pdf :307-331)",
         "why_only_a_vendor_generation_reaches_it": "reached from resident_worker.py:705 only when producer_for(record) is not OPAL; the Opal branch (:700-704) never enters it"},
        {"what": "CertifiedReportPublisher.publish vendor branch (retained vendor PDF, receipt binding, foreign-name check, build_publication, report schema)", "code_line": G + "ycharts/generate/publisher.py:234-260",
         "why_only_a_vendor_generation_reaches_it": "publish returns at :231-233 for an OPAL-kind document; the lines after it need a retained ORIGINAL_VENDOR_PDF and a vendor_artifact receipt"},
    ],
    "unexercised_but_not_vendor_gated": [
        {"what": "POST /api/scoped/investor-reporting/analysis/inputs (upload) and GET .../analysis/comparisons (catalogue)", "code_line": G + "reports/generate_installed.py:361-402,448-450",
         "why": "routes of this function that this release does not change; the after-read above does not call them"},
        {"what": "the dispatch recovery path (outbox PENDING page, lease expiry)", "code_line": G + "ycharts/generate/acceptance.py:145-197", "why": "reached only when a send fails or a lease lapses; the after-read makes a clean send"},
    ],
}
replay_branch = {
    "rule": "browser_sha256 is the digest of the validated submission (acceptance.py:117), so a replay of one request id whose validated body differs in ANY member, this one included, is refused by lookup (acceptance.py:79-80).",
    "what_a_caller_sees": ("LIVE today: a body naming commentary_requested is refused before lookup, UNKNOWN_OR_SERVER_OWNED_FIELD, whatever the request id. BUILT: the first submission with a given request id fixes "
                           "the member as sent (or absent); a second submission of that request id with the member added, dropped or changed is refused CHANGED_INPUTS_SAME_REQUEST_ID (public_reason_code "
                           "INVALID_INPUT), nothing is written and nothing is queued; the same body again is answered from the stored record exactly as today. A client that retries after a timeout "
                           "must therefore resend the SAME body: a form that adds the member to a request id it has already sent without it will be refused."),
    "arms": [a["name"] for a in replay["arms"] if "same_request_id_different_member" in a["name"] and a["function"] == "irpt-ycharts-generate"],
}

ENT = [
    "irpt-ycharts-generate: IB-pr-426 (one-tree rebuild) is merged and NOT applied; its CTO half (87d92b7c3b) is signed on an ORDERING condition (no apply while the resident host's vendor session is signed out) and on built digest MGQu5+58WxJ3pybmZx8cFdJ9nypEPvPGo66cCyiB1ts=, pinned at af64b4bca9, which does NOT contain IB-pr-455 (74bbdbb322 is not an ancestor of af64b4bca9, git merge-base --is-ancestor) -- so the minimal candidate here (built %s) is a different digest and is not that pair (the half's condition 5), and either apply changes what the other's live and rollback digests mean." % functions[0]["build"]["built_sha256"][:20] + "..",
    "irpt-ycharts-generate: the census statement that acceptance.py and submission_service.py must move together HOLDS at this base: the built acceptance.py requires acting_principal_id, the sole production caller of DynamoAcceptance.accept is submission_service.py:145-148, and the replay controls show a TypeError and 0 writes on EVERY new submission (with or without the member) when the two are split in either direction; the minimal candidate carries both (submission_service.py is a rider, commit 2f7cc7be42).",
    "irpt-status, irpt-commentary-draft-store-lambda, irpt-commentary-composition-read-lambda: that pairing does NOT hold for them, because none packages submission_service.py and a census of production callers of DynamoAcceptance.accept (native Grep over infra/aws/lambda/investor-reporting, tests excluded) finds exactly one caller of DynamoAcceptance.accept, submission_service.py:145 (the other `.accept(` hit, export/entry.py:364, is the export module's own async accept, not DynamoAcceptance); their acceptance.py is called through get only (replay: the packaged reader answers are identical with and without the member).",
    "all four: the acceptance.py a release packages also carries 2f7cc7be42 (IRPT_ANLREQ AR-y-37, acting_principal_id), which is not IB-pr-455's and is unreleased in every one of the four live packages; releasing the member releases that code (served in irpt-ycharts-generate, inert in the other three because nothing there calls accept).",
    "irpt-commentary-composition-read-lambda: its live acceptance.py and submission.py (pins 090c819803 and 03ea5980cc) also predate 1eed34a8c0 (IRPT_ANLREQ TO-AR-y-11, ticket_id), so a release of this member also releases ticket_id admission and recording in that package (inert there; no caller).",
    "irpt-ycharts-generate: the packaged AnalysisSubmissionRequest.schema.json moves the schemas digest generate_installed.ingestion_revision_for stamps as ingestion_gate_revision (generate_installed.py:94-101; replay arm), so every request accepted after the release carries a new ingestion_gate_revision, as the one-tree census found for the other contract files; owned_requests.py:190-191 checks it only as a non-empty string; the PORTAL readers' use of it is not read here (the portal submodule is not in this worktree).",
    "irpt-status: its map entry holds owned_requests.py and prospect_dates.py pinned at 361c44fa9d with an un-pin condition (the portal history reader that admits the new members on PROD; CTO ruling msg 4838, row IRPT_ANLREQ-D2-S45): the minimal candidate leaves both pinned, and a later one-tree re-release of this entry waits on that condition.",
    "irpt-commentary-draft-store-lambda: the map's artifact_sha256 for this entry (xyROb11e...) is NOT the live CodeSha256 (AsKY+KWLZ...) and its _build_note still reads DESIRED, not built; the minimal candidate still differs from the live package in exactly 2 of 16 members, so the live package was built from these pins; the entry's stale fields are a map-record matter (row filed).",
    "the worker gate (resident_worker.py send_ready_if_ticketed, merged at 0322231fc8) is in NONE of the four packages: the resident_worker.py in the irpt-ycharts-generate zip is pinned at the live bytes and has neither send_ready_if_ticketed nor producer_for (replay arm). This release therefore does not move the gate; the resident host's INSTALLED package was not read, so whether the gate is live on the host is not established here. The order of release stays SERVICE FIRST (this half, then the form).",
    "irpt-ycharts-generate: every accepted request is dispatched to the generation queue (submission_service.py:160-167) and consumed by the resident host; the CTO half's condition 1 (no accepted request while the host's vendor session is signed out) therefore applies to any after-read that submits, unless the submitter is on the Opal-producer allow list (AMENDMENT 1 a, above).",
    "irpt-ycharts-generate, AMENDMENT 1 b: a replay of one request id with a different, added or dropped member is refused CHANGED_INPUTS_SAME_REQUEST_ID on the built package (replay arms same_request_id_different_member); LIVE refuses the member outright.",
]

NOT_EX = [
    "the vendor generation and every branch only it reaches (job.py:314-513, transport.py:420-516, resident_worker.py:264-281,348-448, publisher.py:234-260): no vendor call of any kind was made; see after_read_with_no_vendor_call.stays_unexercised",
    "the readers that need a retained repository, a profile row or the host: OwnedJobStatusReader.read (status-job), OwnedAnalysisReader (sections, original, pdf), OwnedRequestReader.history, frozen_worker, publisher/publication_worker reads, current_authority.decide, resident_installed, opal_packager, research/runner: each is placed in readers_of_the_accepted_record_at_base with the read the pair would make; none was run in the replay (the replay ran OwnedRequestReader.read, commentary_composition.read_composition, commentary_draft_store.resolve_request, DynamoAcceptance get/lookup/accept and the real SubmissionService)",
    "the resident host's INSTALLED package, its queue consumers, its environment and whether it is running (host reads are outside this order's AWS reads)",
    "the live functions' event source mappings, resource policies and routes (only get-function and get-function-configuration were read); the live environment VALUES (names only were read)",
    "Terraform: no plan or apply, no S3 write; the module's s3_object_version and source_code_hash path is described in the packet, not run",
    "the portal and the form (the submodule is not in this worktree): nothing here reads a page, a portal reader or the ticket",
    "the DynamoDB tables themselves: the replay used in-memory fakes; the real transact_write_items condition behaviour and the real jobs-table lease were not exercised",
    "the repository's own pin test files against the built trees (the ~285 runner): not run here; the replay ran this cell's own probes",
]

CAND = scratch / "candidate_source_map.json"
doc = {
    "candidate_map": {"sha256": hashlib.sha256(CAND.read_bytes()).hexdigest(), "bytes": CAND.stat().st_size, "regenerated_byte_identical_by": "make_candidate_map.py e7bb7e923a <out> <repins>", "committed": False,
                      "why_not_committed": "it is a full copy of lambda-source-map.json, which names client firms and carries an account id in its bucket name; the committed diff is candidate_repins.json (7 rows) and the script regenerates the map", "rows_repinned": repins["rows_repinned"]},
    "to_id": "IRPT_BCKEND.TO-IB-pr-456", "serial": "0.9.0_WK_IRPT_BCKEND~312", "base_commit": BASE,
    "source_map_census": {"entries_scanned": census["entries_scanned"], "entries_packaging_a_changed_member": census["entries_packaging_a_changed_member"],
                          "functions_found": [x["function"] for x in census["functions_packaging"]], "near_misses_not_packaging": len(census["near_misses_not_packaging"]),
                          "how_found": ("make_source_map_census.py parsed the whole map at the base (%d function entries). For each entry it resolved every files[] name to the repo path it is packaged from "
                                        "(the staged_from row's repo_path where one packages that name, else source_dir/<name>) and tested it against the three repo paths; it tested every staged_from row's repo_path "
                                        "(equal to a member, or a directory containing one); and it tested whether source_dir is, or contains, a member's directory. 4 entries package a member by files[] and "
                                        "staged_from or source_dir; 0 entries are a near miss (a files[] basename equal to a member's but resolving elsewhere, or a source_dir match with no resolving files[] name). "
                                        "The issuer's lead of four names is confirmed as the whole set; the 'unnamed entry near map line 4030' is irpt-ycharts-generate itself (its files[] names "
                                        "contracts/AnalysisSubmissionRequest.schema.json, staged at pin 5be2acd7cc). Limit: a function whose package is not described by lambda-source-map.json (an Image function, a build outside "
                                        "build-and-upload.sh such as a Node bundle or the resident host package built by reports/build_resident_package.py) is not in this denominator; the 235 entries include every kind "
                                        "the map holds." % census["entries_scanned"]),
                          "census_file": "IB152-1_source_map_census.json"},
    "functions": functions,
    "entanglements": ENT,
    "readers_of_the_accepted_record_at_base": {"base_commit": BASE, "readers": readers["readers"], "production_readers": readers["production_readers"], "readers_by_kind": readers["readers_by_kind"],
                                               "total_rows": len(readers["readers"]), "difference_from_ib_pr_453": readers["difference_from_ib_pr_453"],
                                               "universe": {"files_now": 47, "files_ib_pr_453": 45, "added": ["ycharts/generate/tests/test_commentary_requested_member.py", "docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json"], "gone": [],
                                                            "regex": "DynamoAcceptance | analysis# | acceptance.(get|accept|lookup) | .acceptance | 'acceptance record' | 'accepted record' (native Grep over the worktree root, org/ excluded, workflows/ placed out as IB-pr-453 did); file list: readers_universe_now.txt"}},
    "replay": {"arms": replay["arms"], "arm_count": replay["arm_count"], "unexpected": replay["unexpected"], "harness": replay["harness"]},
    "amendment_1": {"a_after_read_with_no_vendor_call": after_read, "b_replay_fact_as_a_branch": replay_branch},
    "not_exercised": NOT_EX,
    "uploads_made": 0, "applies_made": 0, "real_source_map_edits": 0, "product_source_edits": 0, "vendor_calls_made": 0,
    "aws_calls_made": "reads only, through .tools/aws: lambda get-function-configuration, lambda get-function (the package link used once in memory and never written), s3api list-object-versions, head-object and get-object (read) on each function's own artifact key; 0 writes",
}
for f in functions:
    if f["function"] == "irpt-ycharts-generate":
        f["after_read_with_no_vendor_call"] = after_read
(D / "IB152-1_release_read.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
print("functions=%d readers=%d production=%d arms=%d" % (len(functions), len(readers["readers"]), readers["production_readers"], len(replay["arms"])))
for f in functions:
    print(f["function"], f["build"]["built_sha256"], f["build"]["built_twice_identical"], len(f["moved_members"]), f["riders"], f["minimal_release"], f["changed_members_packaged"], f["rollback_version_id"])
