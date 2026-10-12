"""IB-pr-460 assembler (ASCII). From the worktree root:
    python <this file> <scratch_dir>
Reads this directory's IB156-1_live_reads.json, IB156-1_live_configuration.json, IB156-1_replay.json, IB156-1_consumer_arm.json,
candidate_repins.json, <scratch>/live/<fn>.zip, <scratch>/zips/<fn>.1.zip and .2.zip (the two BUILD_ONLY builds), <scratch>/moved.json (the
moved-members probe), <scratch>/build1.log. Writes IB156-1_release_read.json and NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-460.md. Nothing is
written to AWS; no firm name, account id or bucket name is written. The packet recommends nothing on timing."""
import base64
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

D = Path("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~316")
scratch = Path(sys.argv[1])
FN = "irpt-commentary-draft-store-lambda"
BASE = subprocess.run(["git", "rev-parse", "7bd08ac698"], capture_output=True, check=True).stdout.decode().strip()
PIN = subprocess.run(["git", "rev-parse", "b7da10ca46"], capture_output=True, check=True).stdout.decode().strip()
STORE_PATH = "infra/aws/lambda/investor-reporting/reports/commentary_draft_store.py"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, check=True).stdout.decode("utf-8", "replace").strip()


lr = load(D / "IB156-1_live_reads.json")["live_reads"][0]
cf = load(D / "IB156-1_live_configuration.json")["live_configuration"][0]
replay = load(D / "IB156-1_replay.json")
cons = load(D / "IB156-1_consumer_arm.json")
repins = load(D / "candidate_repins.json")
mv = load(scratch / "moved.json")[FN]
lz, z1, z2 = scratch / "live" / (FN + ".zip"), scratch / "zips" / (FN + ".1.zip"), scratch / "zips" / (FN + ".2.zip")
lb, b1, b2 = lz.read_bytes(), z1.read_bytes(), z2.read_bytes()
assert b64(lb) == lr["live_code_sha256"]
assert len(mv["moved"]) == 1 and mv["moved"][0]["member"] == "commentary_draft_store.py"
assert not replay["unexpected"] and replay["arm_count"] == len(replay["arms"])

L, B = zipfile.ZipFile(lz), zipfile.ZipFile(z1)
names = sorted(i.filename for i in B.infolist() if not i.filename.endswith("/"))
unchanged = [n for n in names if L.read(n) == B.read(n)]
stayed = {n: (L.read(n) == B.read(n)) for n in ("acceptance.py", "submission.py")}
assert all(stayed.values())
closure = [ln.strip() for ln in (scratch / "build1.log").read_text(encoding="utf-8", errors="replace").splitlines() if "import-closure" in ln][-1]

m0 = mv["moved"][0]
live_subject = git("log", "--format=%s", "-1", m0["live_blob_commit"])[:160]
commits = [{"commit": c["commit"], "subject": c["subject"].encode("ascii", "replace").decode("ascii"), "is_ib_pr_460": c["commit"].startswith("b7da10ca46")} for c in m0["owning_commits"]]
moved = [{
    "member": m0["member"], "repo_path": m0["repo_path"], "live_sha": m0["live_sha"], "built_sha": m0["built_sha"], "live_blob_commit": m0["live_blob_commit"],
    "live_blob_commit_subject": live_subject.encode("ascii", "replace").decode("ascii"), "built_bytes_equal_pin_blob": m0["built_bytes_equal_base_blob"],
    "owning_commits": commits, "class": "served",
    "one_line": ("On a first persist that answers status OK the answer gains a third member, ticket_id, equal to the accepted record's ticket_id when that is a non-empty string; "
                 "for a record with none (absent, empty, null or not a string) the answer is byte-identical to live's. A replay, every refusal and get_ref are unchanged. resolve_request keeps its "
                 "two-value return (it now wraps _resolve_record, which holds the same single requests.get read and also yields the ticket id). The only owning commit is IB-pr-460's (b7da10ca46); "
                 "no earlier unreleased commit touches this path since the live blob (%s). Classed served: the function's answer changes for a record with a ticket id." % m0["live_blob_commit"]),
    "is_this_change": True,
    "serves": [{"commit": "b7da10ca46", "serves": "IRPT_BCKEND TO-IB-pr-460 (round 156, cell IB-pr-460), Part A: PRD ADDENDUM v0.45, the commentary draft store's persist answer names the request's ticket"}],
}]
riders = [m["member"] for m in moved if not m["is_this_change"]]

consumer_arm = {
    "function": FN, "name": "consumer: the drafter's own make_draft_store, given today's two-member first-persist answer and then the built three-member answer, returns the same three keys for put and the same ref for get_ref",
    "verdict": "identical" if cons["same"] and cons["persist_returns_exactly_the_stored_fields"] else "UNEXPECTED", "record_has_ticket_id": True, "negative_control": False,
    "members": ["data/transcripts/scripts/commentary/lambda_handler.py"],
    "detail": "offline: lambda_handler.make_draft_store over a fake lambda client (no AWS call); persist_draft returned %s for both answers; existing_draft returned the ref for both; payload ops %s (IB156-1_consumer_arm.json)." % (
        cons["built_three_member_answer"]["persist_draft_returns"] and sorted(cons["built_three_member_answer"]["persist_draft_returns"]), cons["built_three_member_answer"]["payload_ops"])}
arms = replay["arms"] + [consumer_arm]
assert consumer_arm["verdict"] == "identical"

consumer = {
    "name": "the commentary drafter (outlook-global-commentary-draft-lambda), data/transcripts/scripts/commentary/lambda_handler.py make_draft_store, by direct RequestResponse invoke of this function",
    "code_line": "data/transcripts/scripts/commentary/lambda_handler.py:122-125,135-138",
    "on_the_new_member": ("Ignores it today. invoke() returns doc.get('commentary_ref') only (line 125) after checking status == OK (line 122); persist_draft (lines 135-138) then requires and copies the three _STORED_FIELDS "
                          "(line 73: artifact_id, sha256, version_id) and returns nothing else. No line of the drafter reads ticket_id from this function's answer. Offline arm: IB156-1_consumer_arm.json shows put and get_ref returning identical values for today's answer and the built answer."),
    "read_the_pair_makes_through_it": ("The offline arm above, run now (it persists nothing and invokes nothing). In the world, the one read through the drafter is passive and persists nothing of its own making: the drafter's record "
                                       "for its next organic run, which ends at stage draft_stored (a first persist, the answer carrying ticket_id when the request's record has one) or draft_exists (get_ref, unchanged), "
                                       "read from its result and its log lines that name request ids only. If no such run occurs the drafter's live behaviour on the new member stays unexercised; no draft is persisted to make one."),
}
who = {
    "invoke_policy": "irpt-commentary-draft-store-invoke-policy: lambda:InvokeFunction on this one function and nothing else (infra/aws/terraform/investor-reporting/export/commentary_draft_store.tf:121-135)",
    "attached_to_role": "outlook-global-commentary-draft-role (the commentary drafter's role), attached by aws_iam_role_policy_attachment.commentary_draft_store_invoke (infra/aws/terraform/transcripts/commentary.tf:256-259; role name from data/transcripts/scripts/commentary/NAMES.json role.name)",
    "resource_based_permission": "none declared: the store's Terraform file holds no aws_lambda_permission, so no other principal is granted by a resource policy there",
    "source": "Terraform read only, at the pin; the live attachment and the live resource policy were not read (not_exercised)",
}

NOT_EX = [
    "a LIVE first persist with a record that carries a ticket_id: it writes an artifact to S3 and rows to the requests table as svc-commentary; no draft is persisted to test a release unless a seat can say whose request it is",
    "the live record shape of ticket_id: whether any accepted record in the requests table carries one is not established here (IB154-1 read, finding 13); the offline fakes plant a synthetic id",
    "the real DynamoDB conditional update, the real ArtifactRepository and S3: the replay used in-memory fakes of the request, ref and artifact ports and the unit tests used the repository's own fakes",
    "the drafter's live behaviour (its role, its DRAFT_STORE_FUNCTION value, its environment): only its committed code was run, against a fake lambda client",
    "the live invoke-policy attachment and the function's live resource policy (only get-function and get-function-configuration were read); the live environment VALUES (names only were read)",
    "Terraform: no plan or apply, no S3 write; the module's s3_object_version and source_code_hash path is described in the packet, not run",
    "the map entry's own record: its artifact_sha256 is not the live CodeSha256 and its _build_note still reads DESIRED (row IRPT_BCKEND-D2-W312-S1); this read does not change it",
    "the drafter edit that would READ ticket_id: another seat's cell, after this function's release; nothing here reads, copies or posts the member",
]

live_digest, built_digest = lr["live_code_sha256"], b64(b1)
doc = {
    "function": FN, "to_id": "IRPT_BCKEND.TO-IB-pr-460", "serial": "0.9.0_WK_IRPT_BCKEND~316", "base_commit": BASE, "pin": PIN,
    "live_code_sha256": live_digest, "live_read_at_utc": lr["live_read_at_utc"], "live_last_modified": lr["live_last_modified"],
    "live_package_downloaded_sha256_equals_live_code_sha256": lr["downloaded_zip_equals_live_code_sha256"],
    "rollback_version_id": lr["rollback_version_id"],
    "rollback_version_is_the_latest_object": any(v["is_latest"] and v["version_id"] == lr["rollback_version_id"] for v in lr["versions"]),
    "artifact_object_versions_total": lr["versions_of_key"], "artifact_object_versions_same_size_as_live": lr["versions_of_key_same_size_as_live"],
    "live_configuration_names_only": cf,
    "candidate_map": {"sha256": repins["candidate_map_sha256"], "rows_repinned": repins["rows_repinned"], "committed": False,
                      "equals_the_real_map_byte_for_byte": True,
                      "why": ("commentary_draft_store.py is a NATIVE member of the function's source_dir (reports/): no staged_from row pins it (candidate_repins.json store_member), so there is NO row to re-pin; "
                              "the builder reads it from the worktree at the pin. The candidate map is therefore the real map at the pin, byte-equal (sha256 above); acceptance.py, submission.py and keys.py stay at their live pins. "
                              "The full map is not committed (it names client firms and an account id); make_candidate_map.py regenerates it."),
                      "row_filed": "IRPT_BCKEND-D2-W316-S1"},
    "build": {"outcome": "BUILT", "built_sha256": built_digest, "built_sha256_hex": hashlib.sha256(b1).hexdigest(), "built_bytes": len(b1), "built_twice_identical": b1 == b2 and b64(b1) == b64(b2),
              "members_live": mv["members_live"], "members_built": mv["members_built"], "closure_gate_line": closure,
              "command": "BAU_SOURCE_MAP_OVERRIDE=<candidate map: make_candidate_map.py b7da10ca46> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting %s (TMPDIR in scratch, run twice)" % FN,
              "build_only_skips": "build-and-upload.sh:657-666: after every gate and the zip, BUILD_ONLY=1 prints the digest and continues; the s3 cp, the head-object verify and write_sha_to_map (lines 668-710) are not reached; the summary at 733-736 says 'nothing uploaded, source map untouched'"},
    "moved_members": moved, "riders": riders, "added_members": mv["added"], "removed_members": mv["removed"], "members_unchanged": len(unchanged),
    "acceptance_py_and_submission_py_stayed_at_their_live_pins": {"acceptance.py": stayed["acceptance.py"], "submission.py": stayed["submission.py"], "basis": "built member bytes equal the live member bytes (zip member compare)",
        "what_would_ride_if_they_were_not": ("a re-pin of the two staged rows to the round-152 base (e7bb7e923a) would move both: acceptance.py would carry 74bbdbb322 (IB-pr-455, commentary_requested copy) and 2f7cc7be42 (AR-y-37, "
                                             "acting_principal_id required keyword), submission.py would carry 74bbdbb322; both inert in this package because nothing packaged calls accept or lookup (round-152 read, "
                                             "0.9.0_WK_IRPT_BCKEND~312 member_classes.json). Not applicable to this candidate: neither is re-pinned.")},
    "replay": {"arms": arms, "arm_count": len(arms), "unexpected": [], "harness": replay["harness"] + "; consumer arm: replay/consumer_arm_460.py"},
    "consumer": consumer, "who_may_invoke": who, "not_exercised": NOT_EX,
    "uploads_made": 0, "applies_made": 0, "real_source_map_edits": 0, "vendor_calls_made": 0, "functions_invoked": 0,
    "aws_calls_made": "reads only, through .tools/aws: lambda get-function-configuration, lambda get-function (the package link used once in memory and never written), s3api list-object-versions, head-object and get-object (read) on the function's own artifact key; 0 writes",
}
(D / "IB156-1_release_read.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

# ------------------------------------------------------------------ packet
out = []
w = out.append
w("# Never-widen sign-off packet -- IB-pr-460: what a release of the draft store's `ticket_id` answer would move, for `%s`\n" % FN)
w("Prepared by 0.9.0_WK_IRPT_BCKEND~316 for 2.0.0_SA_COO~P2 on TO-IB-pr-460 (round 156; PRD ADDENDUM v0.45; CTO msgs 6024 and 6033). Base `%s`; pin `%s` (Part A: the change, its tests and the answers file). "
  "Nothing was uploaded, deployed or applied: BUILD_ONLY from the committed pin in this worktree against a candidate map (the real map, byte-equal: no row pins the changed member; `candidate_repins.json` is its committed diff, empty, and "
  "`make_candidate_map.py` regenerates the map, sha256 `%s...`; the full copy is not committed because it names client firms and carries an account id; `lambda-source-map.json` untouched), AWS READS only through the `.tools/aws` shim, "
  "offline replays with in-memory fakes and synthetic ids. This packet does NOT say which ratified outcome any change serves beyond the `serves` column, and it recommends nothing on timing.\n" % (BASE[:10], PIN[:10], repins["candidate_map_sha256"][:16]))
w("## Read this first\n")
w("1. **One member moves: `commentary_draft_store.py` (1 of %d), owned by this cell's commit alone.** No rider. The other %d members are byte-identical to the live package, `acceptance.py` and `submission.py` among them (they stay at their live pins: %s)." % (
    mv["members_built"], len(unchanged), "yes, member bytes equal"))
w("2. **Digests.** Live `%s` (read %s UTC; the downloaded package hashes to it). Built `%s` (%d bytes), twice, byte-identical: %s. Rollback S3 version `%s` (content sha256 equals the live digest by bytes; %s)." % (
    live_digest, lr["live_read_at_utc"], built_digest, len(b1), doc["build"]["built_twice_identical"], lr["rollback_version_id"],
    "it is the LATEST object" if doc["rollback_version_is_the_latest_object"] else "an earlier object"))
w("3. **Replay: %d arms, 0 unexpected.** A first persist for a record with no usable ticket id (no key, empty, null, integer, list) answers byte-identically on live and built. For a record with one, live answers `status` and `commentary_ref`; built adds `ticket_id` equal to the record's. A replay, six refusals and `get_ref` are identical. `requests.get` is called once per persist on both." % len(arms))
w("4. **The one consumer ignores the member**: the drafter reads `commentary_ref` only (`lambda_handler.py:125`) and copies three keys (`:135-138`); an offline arm shows identical results for the old and the new answer.")
w("5. **Two facts that differ from the order's expectation**: no staged row pins `commentary_draft_store.py` (it is native to `source_dir`), so the candidate re-pins 0 rows (row `IRPT_BCKEND-D2-W316-S1`); and the map entry's `artifact_sha256` is not the live digest (row `IRPT_BCKEND-D2-W312-S1`, unchanged by this read).\n")
w("## `%s`\n" % FN)
w("| | |\n|---|---|")
w("| live CodeSha256 | `%s` (read %s; LastModified %s) |" % (live_digest, lr["live_read_at_utc"], lr["live_last_modified"]))
w("| built (twice, byte-identical: %s) | `%s` (%d bytes) |" % (doc["build"]["built_twice_identical"], built_digest, len(b1)))
w("| rollback S3 version | `%s` (%d versions of the key, %d the same size as live) |" % (lr["rollback_version_id"], lr["versions_of_key"], lr["versions_of_key_same_size_as_live"]))
w("| members live / built / moved / added / removed / unchanged | %d / %d / 1 / %d / %d / %d |" % (mv["members_live"], mv["members_built"], len(mv["added"]), len(mv["removed"]), len(unchanged)))
w("| candidate rows re-pinned | 0 (the changed member is native to `source_dir`; `acceptance.py`, `submission.py` and `keys.py` stay at the live pins `283f7e7700`) |")
w("| riders | none |")
w("| live configuration (names only) | handler `%s`, %s, %d MB, %d s, role `%s`, layers none, environment variable names: %s |" % (
    cf["handler"], cf["runtime"], cf["memory"], cf["timeout"], cf["role_name"], ", ".join("`%s`" % x for x in cf["environment_variable_names"])))
w("| import-closure gate (build) | %s |" % closure)
w("| who may invoke | %s, attached to `outlook-global-commentary-draft-role` (`transcripts/commentary.tf:256-259`); no resource-based permission is declared |\n" % "`irpt-commentary-draft-store-invoke-policy` (`lambda:InvokeFunction` on this one function)")
w("**Every moved member (1): owning commits and class**\n")
w("- `commentary_draft_store.py` (THIS CHANGE; live `%s...`, built `%s...`; live blob = commit `%s`, built bytes = the pin blob: %s) -- **served**. %s" % (
    m0["live_sha"][:12], m0["built_sha"][:12], m0["live_blob_commit"], m0["built_bytes_equal_base_blob"], moved[0]["one_line"]))
for cm in commits:
    w("    - `%s` %s  -- serves: %s" % (cm["commit"], cm["subject"], moved[0]["serves"][0]["serves"]))
w("")
w("**acceptance.py and submission.py.** Not moved. " + doc["acceptance_py_and_submission_py_stayed_at_their_live_pins"]["what_would_ride_if_they_were_not"] + "\n")
w("**Branch A** -- release forward, then the module's Terraform path.\n")
w("1. No source-map row needs to land for the changed member (it is native to `source_dir`; the builder reads it from the tree the build runs in). The build must run from a tree whose `commentary_draft_store.py` is the blob of `%s` (sha256 `%s`) and whose staged rows are the ones in the map today; otherwise this read is re-run. The entry's deploy fields are rewritten by `record-terraform-deploy.sh` at the apply." % (PIN[:10], m0["built_sha"]))
w("2. `bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting %s`; the object's `content-sha256` metadata must read `%s`. A different digest stops the apply." % (FN, built_digest))
w("3. `safe-apply` of the root `infra/aws/terraform/investor-reporting/export` on `module.irpt_commentary_draft_store.aws_lambda_function.this` only; the module takes the object's own VersionId and `content-sha256`, so the plan must show `s3_object_version` and `source_code_hash` and nothing else on the function. Role, environment, handler, runtime, memory and timeout are not changed by this build (Terraform not planned by this order). A change-management ledger entry is opened at the start and closed at completion.\n")
w("**Branch B** -- redeploy the rollback version, re-read at apply: S3 version `%s` of the function's own artifact key (content sha256 `%s`), through the same Terraform path, pinning the function to that version. The rollback version is RE-READ AT APPLY (`list-object-versions` and `head-object` on that one key), because a later upload makes today's reading stale. After it the CodeSha256 must read `%s`. Branch B writes nothing to any record; a draft persisted while the built code ran keeps whatever answer it already returned (the answer is not stored).\n" % (
    lr["rollback_version_id"], live_digest, live_digest))
w("## After-read proposed (nothing is persisted)\n")
w("1. `lambda get-function-configuration`: CodeSha256 equals `%s`; handler, runtime, memory, timeout, role name and environment NAMES equal the table above." % built_digest)
w("2. One direct invoke of `{\"op\": \"get_ref\"}` (a refused shape: status REFUSED, reason INVALID_REQUEST; it reads no table and writes nothing). It shows the built package imports and answers. It does not reach the new member.")
w("3. If a seat can say whose request it is: one direct invoke of `op get_ref` with that request's `{tenant, request_id}` answers the same body as the same invoke before the apply and carries no `ticket_id` (contract). It persists nothing.")
w("4. The drafter's record for its next organic run, as in the consumer section of the json. **What then stays unexercised:** the new member on a live first persist, which needs a persist (a write to S3 and the requests table as svc-commentary) and no draft is persisted for a test.\n")
w("## The consumer\n")
w("- **%s**, `%s`." % (consumer["name"], consumer["code_line"]))
w("- On the new member: " + consumer["on_the_new_member"])
w("- The read through it: " + consumer["read_the_pair_makes_through_it"] + "\n")
w("## The replay (offline; live zip against built zip; `IB156-1_replay.json`)\n")
w("%d arms; verdicts: %s; negative controls: %d. Harness `replay/run_replay_460.py` over `replay/probe_460.py` and `replay/consumer_arm_460.py`: boto3 is never imported, every port is an in-memory fake, every socket connect is refused, AWS is never called by the replay, every id is synthetic, one tree per `python -I` process. Verdicts are computed from the probe outputs; a comparison that does not come out as stated would read UNEXPECTED (unexpected: 0).\n" % (
    len(arms), {v: sum(1 for x in arms if x["verdict"] == v) for v in ("identical", "expected-diff")}, sum(1 for x in arms if x["negative_control"])))
for x in arms:
    w("- **%s** %s%s -- %s" % (x["verdict"], "[NEGATIVE CONTROL] " if x["negative_control"] else "", x["name"], x["detail"]))
w("\n## What is NOT exercised\n")
for x in NOT_EX:
    w("- " + x)
w("\n## Rows and state\n")
w("Row filed by this worker: `IRPT_BCKEND-D2-W316-S1` in `org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md`. Uploads 0, applies 0, real source-map edits 0, vendor calls 0, functions invoked 0. Scratch packages are outside the worktree and are deleted file by file at the end of the order. Commits are LOCAL on branch `wk-IRPT_BCKEND-316`; nothing is pushed.")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-460.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("release read written; moved=%d riders=%d arms=%d built=%s twice=%s" % (len(moved), len(riders), len(arms), built_digest, doc["build"]["built_twice_identical"]))
