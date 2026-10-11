"""IB-pr-456 packet writer (ASCII). From the worktree root:
    python <this file>
Reads IB152-1_release_read.json and writes NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-456.md in this directory. Every number comes from the json. The packet does NOT say which
ratified outcome any change serves and does NOT recommend an order of release among the functions."""
import json
from pathlib import Path

D = Path("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~312")
R = json.loads((D / "IB152-1_release_read.json").read_text(encoding="utf-8"))
smap = json.loads(__import__("subprocess").run(["git", "show", "e7bb7e923a:infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode("utf-8"))["functions"]
conf = {x["function"]: x for x in json.loads((D / "IB152-1_live_configuration.json").read_text(encoding="utf-8"))["live_configuration"]}
A1 = R["amendment_1"]
F = {f["function"]: f for f in R["functions"]}
out = []
w = out.append

AFTER = {
    "irpt-ycharts-generate": "AMENDMENT 1 (a) below: the steps, the Opal-producer question and what stays unexercised.",
    "irpt-status": ("(1) get-function-configuration reads the built CodeSha256 and the same handler, runtime, memory, timeout, role name and environment NAMES as the table above. "
                    "(2) Through OwnedRequestReader.read (owned_requests.py:245-254): GET /api/scoped/investor-reporting/analysis/requests/{requestId} (analysis-request-read) for one request accepted BEFORE the apply answers exactly {identity, accepted_at}, byte-equal to the same read taken before the apply. "
                    "(3) Through OwnedRequestReader.history (owned_requests.py:325+): GET .../analysis/requests (analysis-request-history), the rows for the same request unchanged. "
                    "(4) Through OwnedJobStatusReader.read (owned_status.py:33-37): GET .../status/{jobId} for the same request, state and reason unchanged. "
                    "No record carries the member until irpt-ycharts-generate accepts one, so a WITH-the-member read through this function is a read of the later moment when such a record exists: the same three routes for that request must answer the same shapes (replay arm: the answer does not depend on the member)."),
    "irpt-commentary-draft-store-lambda": ("(1) get-function-configuration reads the built CodeSha256 and the same handler, runtime, memory, timeout, role name and environment NAMES. (2) This function has no route, schedule or event source: ONE direct invoke "
                                           "with op get_ref and {tenant, request_id} for a request accepted before the apply answers the same body as the same invoke taken before the apply. Through commentary_draft_store.resolve_request (commentary_draft_store.py:112-125). "
                                           "A request with the member exists only after irpt-ycharts-generate accepts one; the same invoke for it must answer the same shape (replay arm)."),
    "irpt-commentary-composition-read-lambda": ("(1) get-function-configuration reads the built CodeSha256 and the same handler, runtime, memory, timeout, role name and environment NAMES. (2) This function has no route, schedule or event source: ONE direct invoke "
                                                "with {tenant, request_id} for a READY request accepted before the apply answers status OK with the same request_ref and a composition of the same sha256 as before the apply. Through commentary_composition.read_composition (commentary_composition.py:131-175). "
                                                "A request with the member exists only after irpt-ycharts-generate accepts one; the same invoke for it must answer the same shape (replay arm)."),
}

w("# Never-widen sign-off packet -- IB-pr-456: what a release of `commentary_requested` would move, function by function\n")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~312 for 2.0.0_SA_COO~P2 on TO-IB-pr-456 (round 152; CTO msg 5863) and its AMENDMENT 1 (CTO msg 5904). Base `%s` (contains IB-pr-455, merged @0322231fc8). "
  "Nothing was uploaded, deployed or applied: BUILD_ONLY from a committed tree in this worktree against a candidate map (the real map with only 7 staged rows re-pinned to the base: `candidate_repins.json` is its committed diff and `make_candidate_map.py` regenerates it byte for byte, sha256 `%s`; the full copy is not committed because it names client firms and carries an account id; `lambda-source-map.json` untouched), AWS READS only through the `.tools/aws` shim, offline replays with in-memory fakes and synthetic ids. "
  "This packet does NOT say which ratified outcome any change serves, and it does NOT recommend an order of release among the functions: the issuer reads the ENDPOINT against this census.\n" % (R["base_commit"], R["candidate_map"]["sha256"][:16] + "..."))
w("## Read this first\n")
c = R["source_map_census"]
w("1. **%d of the %d map entries package a changed member**, found by subtraction over the whole map (`IB152-1_source_map_census.json`): %s. The issuer's lead of four names is the whole set; the unnamed entry near map line 4030 is `irpt-ycharts-generate` itself. Near misses: %d." % (
    c["entries_packaging_a_changed_member"], c["entries_scanned"], ", ".join("`%s`" % n for n in c["functions_found"]), c["near_misses_not_packaging"]))
w("2. **Every function's minimal candidate BUILT, twice, byte-identically.** Per function: %s." % "; ".join(
    "`%s` live `%s`, built `%s`, %d of %d members move, riders %s, **%s**" % (f["function"], f["live_code_sha256"], f["build"]["built_sha256"], len(f["moved_members"]), f["build"]["members_live"],
                                                                         f["riders"] or "none", f["minimal_release"]) for f in R["functions"]))
w("3. **Only `irpt-ycharts-generate` has riders.** Its submission.py and acceptance.py are native members of its source_dir, so a build reads them (and every other native member) from the tree: the candidate re-pins only the one staged row (the schema), and two native members that are not IB-pr-455's differ from live and ride with it: `durable_job.py` (3acafb3f45) and `submission_service.py` (2f7cc7be42). In the other three the staged rows are re-pinned to the base and nothing else differs from live.")
w("4. **Two of the changed members carry EARLIER unreleased commits that are not IB-pr-455's**: `acceptance.py` carries 2f7cc7be42 (IRPT_ANLREQ AR-y-37, `acting_principal_id`) in all four functions, and in `irpt-commentary-composition-read-lambda` also 1eed34a8c0 (AR-y-11, `ticket_id`); `submission.py` there carries 1eed34a8c0 too.")
w("5. **%d readers of the accepted record at this base (%d production)**, against IB-pr-453's 50: one production reader added (the I3 rule `send_ready_if_ticketed`), one test added, none gone. Section 'Readers'." % (
    R["readers_of_the_accepted_record_at_base"]["total_rows"], R["readers_of_the_accepted_record_at_base"]["production_readers"]))
w("6. **Replay: %d arms, %d unexpected.** A submission WITHOUT the member is accepted and recorded identically by live and built in all four functions (the full record differs by one key, `acting_principal_id`, which is AR-y-37's)." % (R["replay"]["arm_count"], len(R["replay"]["unexpected"])))
w("7. **Closure limbs** (signature, attribute, method-call) on the built zips: signature and attribute read 0 mismatched on all four; the method-call limb reads 0 on three and **4 on `irpt-ycharts-generate`, the SAME 4 on the live package** (publication:114 `.lookup`, publisher:191 and :258 `.validate`, resident_worker:137 `.renew`; carried, compared by module and call text; the one-tree packet gave their reasons). Last lines per function in the json.\n")

w("## Per function\n")
for f in R["functions"]:
    n = f["function"]
    e = smap[n]
    cf = conf[n]
    w("### `%s`\n" % n)
    w("| | |\n|---|---|")
    w("| live CodeSha256 | `%s` (read %s; LastModified %s) |" % (f["live_code_sha256"], f["live_read_at_utc"], f["live_last_modified"]))
    w("| built (twice, byte-identical: %s) | `%s` (%d bytes) |" % (f["build"]["built_twice_identical"], f["build"]["built_sha256"], f["build"]["built_bytes"]))
    w("| rollback S3 version (content sha256 equals the live digest; %s) | `%s` (%d versions of the key, %d the same size as live) |" % (
        "it is the LATEST object" if f["rollback_version_is_the_latest_object"] else "an earlier object", f["rollback_version_id"], f["artifact_object_versions_total"], f["artifact_object_versions_same_size_as_live"]))
    w("| live package downloaded once; its sha256 equals the live CodeSha256 | %s |" % f["live_package_downloaded_sha256_equals_live_code_sha256"])
    w("| map `artifact_sha256` equals the live CodeSha256 | %s |" % f["map_artifact_sha256_equals_live_code_sha256"])
    w("| members live / built / moved / added / removed | %d / %d / %d / %d / %d |" % (f["build"]["members_live"], f["build"]["members_built"], len(f["moved_members"]), len(f["added_members"]), len(f["removed_members"])))
    w("| the three changed members | %s |" % "; ".join("`%s`: %s" % (k, v) for k, v in f["changed_members_packaged"].items()))
    w("| candidate rows re-pinned | %s |" % ("; ".join("`%s` %s -> %s" % (r["packaged_as"], r["old_pin"], r["new_pin"]) for r in f["candidate_rows_repinned"])))
    if f["candidate_rows_repinned_note"]:
        w("| note | %s |" % f["candidate_rows_repinned_note"])
    w("| riders | %s |" % (", ".join("`%s`" % r for r in f["riders"]) or "none"))
    w("| minimal release | **%s** |" % f["minimal_release"])
    w("| live configuration (names only) | handler `%s`, %s, %d MB, %d s, role `%s`, layers %s, environment variable names: %s |" % (
        cf["handler"], cf["runtime"], cf["memory"], cf["timeout"], cf["role_name"], cf["layers"] or "none", ", ".join("`%s`" % x for x in cf["environment_variable_names"])))
    w("| closure limbs (built) | %s ; %s ; %s |" % (f["closure_limbs"]["built"]["name"], f["closure_limbs"]["built"]["attribute"], f["closure_limbs"]["built"]["method"]))
    w("| closure limbs (live) | %s ; %s ; %s |\n" % (f["closure_limbs"]["live"]["name"], f["closure_limbs"]["live"]["attribute"], f["closure_limbs"]["live"]["method"]))
    w("**Every moved member (%d): owning commits and class**\n" % len(f["moved_members"]))
    for m in f["moved_members"]:
        w("- `%s` (%s; live `%s...`, built `%s...`; live blob = commit `%s`, built bytes = the base blob: %s) -- **%s**. %s" % (
            m["member"], "one of the three" if m["is_one_of_the_three"] else "RIDER", m["live_sha"][:12], m["built_sha"][:12], m["live_blob_commit"], m["built_bytes_equal_base_blob"], m["class"], m["one_line"]))
        for cm in m["owning_commits"]:
            w("    - `%s` %s%s" % (cm["commit"], cm["subject"], "" if cm["is_ib_pr_455"] else "  **[NOT IB-pr-455's]**"))
    w("")
    tfdir = "/".join(e["tf_file"].split("/")[:-1])
    w("**Branch A** -- source-map entry landed first, then the build, then the module's Terraform path.\n")
    w("1. The apply amendment lands the re-pinned rows (`candidate_repins.json`, the rows for `%s`; the candidate map is the whole map with only those rows changed) into `infra/aws/lambda/ci/lambda-source-map.json`. The build reads the map, so this comes first. "
      "%s" % (n, "The native members are read from the tree the build runs in; the build must run from a tree whose `acceptance.py`, `submission.py`, `submission_service.py` and `durable_job.py` are the base's, or the census is re-read (a later tree can move more members). " if n == "irpt-ycharts-generate" else "")
      + "The entry's deploy fields are rewritten by `record-terraform-deploy.sh` at the apply.")
    w("2. `bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting %s`; the object's `content-sha256` metadata must read `%s`. A different digest stops the apply." % (n, f["build"]["built_sha256"]))
    w("3. `safe-apply` of the root `%s` on `%s` only; the module takes the object's own VersionId and `content-sha256`, so the plan must show `s3_object_version` and `source_code_hash` and nothing else on the function. Role, layers, environment, handler, runtime, memory and timeout are not changed by this build (Terraform not read or planned by this order). A change-management ledger entry is opened at the start and closed at completion.\n" % (tfdir, e["tf_resource"]))
    w("**Branch B** -- redeploy the rollback version, re-read at apply: S3 version `%s` of the function's own artifact key (content sha256 `%s`), through the same Terraform path, pinning the function to that version. The rollback version is RE-READ AT APPLY (`list-object-versions` and `head-object` on that one key), because a later upload makes today's reading stale. After it the CodeSha256 must read `%s`. Branch B leaves any record the built code wrote in place.\n" % (
        f["rollback_version_id"], f["live_code_sha256"], f["live_code_sha256"]))
    w("**After-read proposed through each reader:** %s\n" % AFTER[n])

w("## AMENDMENT 1 (a) -- an after-read for `irpt-ycharts-generate` with NO vendor call (text for the CTO to rule on)\n")
a = A1["a_after_read_with_no_vendor_call"]
w(a["proposal_for_the_CTO_to_rule_on"] + "\n")
w("| step | route or call | what is read back | through which reader |\n|---|---|---|---|")
for s in a["steps"]:
    w("| %s | %s | %s | %s |" % (s["step"], s["route_or_call"], s["what_is_read_back"], s["through_which_reader"]))
w("\n**Opal-producer job needed: %s.** %s\n" % (str(a["opal_producer_job_needed"]).lower(), a["why"]))
w("**What stays UNEXERCISED under this after-read (vendor-only):**\n")
for s in a["stays_unexercised"]:
    w("- %s -- `%s`. Why only a vendor generation reaches it: %s." % (s["what"], s["code_line"], s["why_only_a_vendor_generation_reaches_it"]))
w("\nAlso unexercised, not vendor-gated:\n")
for s in a["unexercised_but_not_vendor_gated"]:
    w("- %s -- `%s`: %s." % (s["what"], s["code_line"], s["why"]))
w("\n## AMENDMENT 1 (b) -- the replay fact, as a branch of the release\n")
b = A1["b_replay_fact_as_a_branch"]
w(b["rule"] + "\n")
w("**What a caller sees.** " + b["what_a_caller_sees"] + "\n")
w("Replay arms that show it on the built package (live refuses the member outright, so live and built differ): %s.\n" % "; ".join("`%s`" % x for x in b["arms"]))
w("## Entanglements (stated, not resolved)\n")
for i, x in enumerate(R["entanglements"], 1):
    w("%d. %s" % (i, x))
w("\n## Readers of the accepted record at the base (%d rows, %d production; IB-pr-453 counted 50)\n" % (R["readers_of_the_accepted_record_at_base"]["total_rows"], R["readers_of_the_accepted_record_at_base"]["production_readers"]))
rd = R["readers_of_the_accepted_record_at_base"]
w("Universe: %s. By kind: %s.\n" % (rd["universe"]["regex"], rd["readers_by_kind"]))
w("**Difference from IB-pr-453:**\n")
for x in rd["difference_from_ib_pr_453"]:
    w("- " + x)
w("\n| reader | code line | kind | runs in | the one read the pair makes through it |\n|---|---|---|---|---|")
for r in rd["readers"]:
    if r["kind"] == "test":
        continue
    w("| %s | `%s` | %s | %s | %s |" % (r["reader"], r["code_line"].replace("infra/aws/lambda/investor-reporting/", ""), r["kind"], r["function_or_surface"], r["read_the_pair_makes_through_it"]))
w("\nThe %d test readers are in the json, each with the offline arm 'run this test file against the built tree'.\n" % sum(1 for r in rd["readers"] if r["kind"] == "test"))
w("## The replay (offline; live zip against built zip; `IB152-1_replay.json`)\n")
w("%d arms; verdicts: %s; negative controls: %d. Harness `replay/run_replay_456.py` over `replay/probe_456.py`: boto3 is never imported, every client is an in-memory fake, every socket connect is refused, AWS is never called by the replay, every id is synthetic, one tree per `python -I` process. Verdicts are computed from the probe outputs; a comparison that does not come out as stated would read UNEXPECTED (unexpected: %d).\n" % (
    R["replay"]["arm_count"], {v: sum(1 for x in R["replay"]["arms"] if x["verdict"] == v) for v in ("identical", "expected-diff")}, sum(1 for x in R["replay"]["arms"] if x["negative_control"]), len(R["replay"]["unexpected"])))
for x in R["replay"]["arms"]:
    w("- **%s** %s%s -- %s" % (x["verdict"], "[NEGATIVE CONTROL] " if x["negative_control"] else "", x["name"], x["detail"]))
w("\n## What is NOT exercised\n")
for x in R["not_exercised"]:
    w("- " + x)
w("\n## Rows and state\n")
w("Rows filed by this worker are listed in the final report and in `org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md` under the ids `IRPT_BCKEND-D2-W312-S<k>`. Uploads 0, applies 0, real source-map edits 0, product source edits 0, vendor calls 0. Scratch packages are outside the worktree and are deleted at the end of the order. Commits are LOCAL on branch `wk-IRPT_BCKEND-312`; nothing is pushed.")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-456.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("packet written: %d lines" % len(out))
