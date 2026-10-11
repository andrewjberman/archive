"""IB-pr-456 readers of the accepted record at the base (ASCII). From the worktree root:
    python <this file> <out_json>
Starts from the IB-pr-453 list (deliverables/0.9.0_WK_IRPT_BCKEND~309/IB149-1_commentary_asked_member.json, 50 readers at 0bdd920114),
re-places each at the base by the same subtraction (universe: readers_universe_now.txt, the native-Grep file list of the same regexes at the base),
replaces the rows whose code moved, adds the rows the base added, and gives every row its function_or_surface and the ONE read the release pair
makes through it. The only production file that changed between 0bdd920114 and the base among the readers is resident_worker.py
(git diff --stat); acceptance.py and submission.py changed by the member itself. A reader row lists the code line of the READ."""
import json
import subprocess
import sys

OLD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~309/IB149-1_commentary_asked_member.json"
OUT = sys.argv[1]
G = "infra/aws/lambda/investor-reporting/"
old = json.loads(open(OLD, encoding="utf-8").read())["readers_of_the_accepted_record"]
HOST = ("resident host process (the dedicated always-on host: install-resident.sh -> resident_main.py, systemd irpt-analysis-resident.service); not a Lambda. "
        "The same module rides in the irpt-ycharts-generate zip but that function's handler never calls it")
ROUTE_READ = ("GET /api/scoped/investor-reporting/analysis/requests/{requestId} (operation analysis-request-read, Lambda irpt-status) for one request accepted before the release "
              "and one accepted with the member: look at the body, which must be exactly {identity, accepted_at} for both (owned_requests.py:243)")
ROUTE_HIST = ("GET /api/scoped/investor-reporting/analysis/requests (operation analysis-request-history, Lambda irpt-status): the rows for the same two requests, "
              "each row's key set unchanged and neither row naming commentary_requested")
INVOKE = ("a direct IAM invoke (this function has no route, schedule or event source) with {tenant, request_id} for one READY request accepted before the release "
          "and one with the member: look at status/reason in the answer, which must be the same OK shape for both")
OFFLINE = "no route reaches it: the offline arm named in replay.arms for this module, plus the repository's own test file for it, run against the built tree"
HOST_READ = ("no route reaches it (the host reads the table directly): the first job the host takes for a request accepted with the member; look at the READY receipt "
             "and the journal line IRPT_RESIDENT_READY_SIGNAL, or the offline arm named in replay.arms")

# (surface, read) by production file; tests are one row each
SURF = {
    "ycharts/generate/resident_worker.py": (HOST, HOST_READ),
    "ycharts/generate/frozen_worker.py": (HOST, OFFLINE + " (ycharts/generate/tests/test_frozen_worker.py)"),
    "ycharts/generate/publisher.py": (HOST, OFFLINE + " (ycharts/generate/tests/test_publisher.py)"),
    "ycharts/generate/publication_worker.py": (HOST, OFFLINE + " (ycharts/generate/tests/test_publication_worker.py)"),
    "ycharts/generate/current_authority.py": (HOST, OFFLINE + " (ycharts/generate/tests/test_permanent_authority_refusal.py)"),
    "reports/resident_installed.py": (HOST + "; also packaged in the irpt-status zip as a library", OFFLINE + " (reports/tests: test_status_installed.py)"),
    "ops/owned_requests.py": ("Lambda irpt-status (and the resident host through resident_installed)", ROUTE_READ + "; for the history method also: " + ROUTE_HIST),
    "ops/owned_status.py": ("Lambda irpt-status", "GET /api/scoped/investor-reporting/status/{jobId} (operation status-job) for the same two requests: look at the state and reason code, which must not depend on the member"),
    "ops/owned_report.py": ("Lambda irpt-status", "GET /api/scoped/investor-reporting/analysis/{jobId}/sections (analysis-report) and GET .../requests/{requestId}/original (analysis-request-original) for a ticketed request: look at the ticket binding answer, unchanged"),
    "ops/prospect_dates.py": ("Lambda irpt-status", "GET /api/scoped/investor-reporting/status/{jobId} for a prospect request: the date basis, unchanged (reached through owned_status)"),
    "ops/entry.py": ("Lambda irpt-status", ROUTE_READ),
    "reports/commentary_composition.py": ("Lambda irpt-commentary-composition-read-lambda", INVOKE),
    "reports/commentary_draft_store.py": ("Lambda irpt-commentary-draft-store-lambda", "a direct IAM invoke with op get_ref and {tenant, request_id} for one request accepted before the release and one with the member: look at status OK and commentary_ref, which must not depend on the member"),
    "ycharts/research/opal_packager.py": (HOST + " (the commentary_ready poll)", HOST_READ),
    "ycharts/research/runner.py": ("resident host process (the research runner role reads the table directly with its own client)", HOST_READ),
    "ycharts/generate/acceptance.py": ("Lambda irpt-ycharts-generate (accept, lookup, dispatch on the submit route); get also runs in irpt-status, irpt-commentary-draft-store-lambda, irpt-commentary-composition-read-lambda and the host",
                                       "the submit route POST /api/scoped/investor-reporting/analysis with and without the member (response {identity, stage, status}), then the stored record `analysis#<request_id>#1` read back with one live DynamoDB get-item of the requests table: the member is present only on the record sent with it"),
    "ycharts/generate/submission_service.py": ("Lambda irpt-ycharts-generate (POST /api/scoped/investor-reporting/analysis)",
                                               "the submit route POST /api/scoped/investor-reporting/analysis, one body without and one with the member: look at the response stage RECEIVED and, for a replay of the same request id with a different member, the refusal CHANGED_INPUTS_SAME_REQUEST_ID"),
}


def key_of(path):
    return path.replace(G, "")


rows = []
for r in old:
    path = r["code_line"].split(":")[0]
    row = {"reader": r["reader"], "code_line": r["code_line"], "kind": r["kind"]}
    if r["kind"] == "test":
        row["function_or_surface"] = "offline test suite (no function runs it)"
        row["read_the_pair_makes_through_it"] = "offline arm: run this test file against the built tree's modules (the test already reads the stored record); no route reaches it"
    else:
        s, rd = SURF[key_of(path)]
        row["function_or_surface"], row["read_the_pair_makes_through_it"] = s, rd
    rows.append(row)

# rows whose code moved at the base (resident_worker.py, 22 changed lines in IB-pr-455's worker half)
RW = G + "ycharts/generate/resident_worker.py"
moved = {
    "ResidentAssembly.execute reads the record": RW + ":649-704",
    "ResidentGenerationWorker.guard": RW + ":220-232",
    "ResidentGenerationWorker.mark_ready (the ONE member read today: ticket_id)": RW + ":333-343",
    "producer_for (the producer chosen from owner.principal_id)": RW + ":128-133",
    "ResidentGenerationWorker.run / run_opal read identity.revision, owner, composition_ref": RW + ":351,359,412-429,470-504",
    "DynamoAcceptance.get (returns the whole parsed record, no member filter)": G + "ycharts/generate/acceptance.py:68-71",
    "DynamoAcceptance.lookup (idempotent retry)": G + "ycharts/generate/acceptance.py:73-81,108-110",
    "DynamoAcceptance.dispatch": G + "ycharts/generate/acceptance.py:145-174",
}
seen = set()
for row in rows:
    for k, v in moved.items():
        if row["reader"].startswith(k.split(" (")[0]) and row["code_line"].split(":")[0] == v.split(":")[0]:
            row["code_line"] = v
            seen.add(k)
            row["moved_since_ib_pr_453"] = True
            break
assert seen == set(moved), sorted(set(moved) - seen)
for row in rows:
    if row["reader"].startswith("ResidentGenerationWorker.mark_ready"):
        row["reader"] = "ResidentGenerationWorker.mark_ready (reads ticket_id for the READY receipt; then calls signal_ready)"
# rows the base added
rows.insert(3, {"reader": "send_ready_if_ticketed (NEW at the base: the one rule for I3 reads ticket_id and commentary_requested, exactly True)",
                "code_line": RW + ":189-200", "kind": "worker", "moved_since_ib_pr_453": True, "added_since_ib_pr_453": True,
                "function_or_surface": SURF["ycharts/generate/resident_worker.py"][0],
                "read_the_pair_makes_through_it": ("no route reaches it, and the resident_worker.py in the irpt-ycharts-generate zip is the OLD one that does not hold this function (replay arm: the zip's resident_worker.py has no "
                                                   "send_ready_if_ticketed), so THIS release does not move it: the read is the host's first job for a request accepted with the member, journal line "
                                                   "IRPT_RESIDENT_READY_SIGNAL skipped=NO_TICKET or skipped=COMMENTARY_NOT_REQUESTED, or the offline tests ycharts/generate/tests/test_ready_signal_commentary_gate.py and test_ready_signal_ticket_gate.py")})
rows.append({"reader": "test_commentary_requested_member.py (NEW at the base: stubbed acceptance of a submission sent three ways; reads the record the transaction stored)",
             "code_line": G + "ycharts/generate/tests/test_commentary_requested_member.py:58-80", "kind": "test", "added_since_ib_pr_453": True,
             "function_or_surface": "offline test suite (no function runs it)",
             "read_the_pair_makes_through_it": "offline arm: run this test file against the built tree's modules; no route reaches it"})
prod = sum(1 for r in rows if r["kind"] != "test")
kinds = {}
for r in rows:
    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
diff = [
    "ADDED reader: resident_worker.py send_ready_if_ticketed (:189-200), the I3 rule IB-pr-455's worker half merged: it reads ticket_id AND commentary_requested (exactly True); called from signal_ready (:345-346) after mark_ready's READY write and from the redelivery path (:686-687). IB-pr-453 counted mark_ready's ticket_id read as 'the ONE member read today'; at the base the member is read here, and the gate is DORMANT until a record carries the member.",
    "MOVED (same readers, new lines, no change of what they read): ResidentAssembly.execute 635 -> 649-704, guard 208-216 -> 220-232, mark_ready 324-326 -> 333-343, producer_for 129-133 -> 128-133, run/run_opal -> 351,359,412-429,470-504; acceptance.get/lookup/dispatch -> :68-71, :73-81/108-110, :145-174 (two lines added at :122-123 shift what follows).",
    "ADDED test reader: ycharts/generate/tests/test_commentary_requested_member.py (the universe grows 45 -> 47 files; the second new file is docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json, placed NEITHER: it declares the member, it does not read a record). Two more new test files, test_ready_signal_commentary_gate.py and test_ready_signal_ticket_gate.py, exercise the gate but name none of the census terms, so by the same subtraction they sit OUTSIDE the universe and are not counted.",
    "GONE: none (every one of the 45 files of IB-pr-453 is still in the universe: set difference printed in readers_census.json).",
    "UNCHANGED: every other production reader file is byte-identical to IB-pr-453's base (git diff 0bdd920114..base over infra/aws/lambda/investor-reporting touches only resident_worker.py, acceptance.py and submission.py among the files that name the record).",
]
doc = {"base_commit": subprocess.run(["git", "rev-parse", "e7bb7e923a"], capture_output=True, check=True).stdout.decode().strip(),
       "readers": rows, "production_readers": prod, "readers_by_kind": kinds, "difference_from_ib_pr_453": diff}
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(doc, indent=1) + "\n")
print("readers=%d production=%d kinds=%s" % (len(rows), prod, kinds))
