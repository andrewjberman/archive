"""IB-pr-426 never-widen packet writer. From the worktree root:
    python <this file> <deliverables_dir> <scratch_dir>
Reads IB124-1_generate_census.json and IB124-1_replay.json from <deliverables_dir>, the live function configuration (AWS read through the
.tools/aws shim) and the real source map entry at HEAD, and writes NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-426.md there. Counts and digests come
from the two json files; the Terraform facts are the ones read from infra/aws/terraform/investor-reporting/ycharts/generate.tf. ASCII only.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ddir = Path(sys.argv[1])
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
C = json.loads((ddir / "IB124-1_generate_census.json").read_text(encoding="utf-8"))
R = json.loads((ddir / "IB124-1_replay.json").read_text(encoding="utf-8"))
real = json.loads(subprocess.run(["git", "show", "HEAD:infra/aws/lambda/ci/lambda-source-map.json"], cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8"))["functions"]["irpt-ycharts-generate"]
cfg = json.loads(subprocess.run(["bash", ".tools/aws", "lambda", "get-function-configuration", "--function-name", "irpt-ycharts-generate", "--output", "json"],
                                cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8"))
layers = [re.sub(r"arn:aws:lambda:[a-z0-9-]+:\d+:layer:", "", lay["Arn"]) for lay in cfg.get("Layers", [])]
env_names = sorted(cfg.get("Environment", {}).get("Variables", {}))
TF_ENV = sorted(["IRPT_YCHARTS_BASE", "IRPT_YCHARTS_SESSION_SECRET_ID", "IRPT_EVIDENCE_BUCKET", "IRPT_JOBS_TABLE", "IRPT_REQUESTS_TABLE", "IRPT_GENERATION_QUEUE_URL",
                 "IRPT_GENERATE_TIMEOUT_S", "IRPT_FIRM_DESTINATION_POLICY", "IRPT_FIRM_REGISTRY", "IRPT_DIRECTORY_BUCKET_MAP"])
def same(a, b):
    return "equal" if a == b else "DIFFERENT"


moved = C["moved_members"]
served = [m for m in moved if m["class"] == "served"]
inert = [m for m in moved if m["class"] == "inert"]
arms = R["arms"]
exp_arms = [a for a in arms if a["verdict"] == "expected-diff"]
L = []
w = L.append

w("# Never-widen sign-off packet -- IB-pr-426: irpt-ycharts-generate rebuilt from ONE commit")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~285 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO~DELL2 (CTO half), on TO-IB-pr-426 and its AMENDMENT 1 (row `IRPT_BCKEND-D2-W285-S1`; CTO msgs 4621, 4657; row `IRPT_ANLREQ-D2-S39`). "
  "Nothing here was uploaded, deployed or applied: BUILD_ONLY from a committed tree in this worktree, offline replays against SYNTHETIC data with in-memory fakes, AWS reads only through the `.tools/aws` shim (the live zip, the function configuration, the S3 object versions). "
  "This packet does not say which ratified outcome any change serves; the issuer reads the ENDPOINT against the census.")
w("")
w("## Read this first")
w("")
w("1. **One pin, one build.** The pin is `%s` (the commit this worktree was cut from; it contains the `performance/` restoration `c267b71edb`). EVERY member of the function, staged (%d rows) or native (%d), is that commit's blob: checked by bytes against `git show` for all %d. Built twice, byte-identical. Built **%s**, live **%s**." % (
    C["pin"], C["pin_checks"]["staged_rows"], C["pin_checks"]["native_members"], C["members_built"], C["built_sha256"], C["live_before"]))
w("2. **%d of %d members move; %d are served, %d inert.** No member is added or removed (%d built, %d live). The two inert members are %s." % (
    len(moved), C["members_built"], len(served), len(inert), C["members_built"], C["members_live"], " and ".join("`%s`" % m["member"] for m in inert)))
w("3. **The method-call limb reads 4 on the build and the SAME 4 on the live package** (AMENDMENT 1: the bar is nothing new against live). They are listed below with their reasons. Each reason is a READING OF THE SOURCE for the injected object, which is not in this package; where a replay arm reached the call line it says so, and what it proves is the call shape against a fake, not the injected object. The name and attribute limbs read 0 on both zips.")
w("4. **The source map is NOT edited** (outside this order's grant). The zip was built from `%s` via `BAU_SOURCE_MAP_OVERRIDE`. For the record step: the real map's `artifact_sha256` (`%s`), `deployed_code_sha256` (`%s`), `last_deployed_at` (`%s`) and `deploy_ledger` (`%s`) for this entry are ONE RELEASE BEHIND: they name the build that release 6b replaced, not the live `%s`." % (
    C["candidate_map"], real["artifact_sha256"], real["deployed_code_sha256"], real["last_deployed_at"], real["deploy_ledger"], C["live_before"]))
w("5. **The acceptance pair moves together** (`acceptance.py` and `submission_service.py`); one without the other raises `TypeError` on every new submission (negative-control arms below read it).")
w("6. **What rides, said plainly.** One commit means the 23 staged members that lagged arrive with every commit in between, and the three native members (`acceptance.py`, `durable_job.py`, `submission_service.py`) with theirs. The table below names every owning commit. The packaged schema directory is digested into `ingestion_revision`, so **every request accepted after the apply records a different `ingestion_gate_revision`** (replay: live `%s...`, built `%s...`); `destination_revision` is unchanged." % (
    next(a for a in arms if a["name"].startswith("composition"))["detail"].split("live ")[1][:20], next(a for a in arms if a["name"].startswith("composition"))["detail"].split("built ")[1][:20]))
w("")
w("## Digests, rollback and the closure limbs")
w("")
w("| item | value |")
w("|---|---|")
w("| function | `irpt-ycharts-generate` (handler `generate_installed.lambda_handler`) |")
w("| pin | `%s` |" % C["pin"])
w("| built sha256 (CodeSha256 form) | `%s` (hex `%s`, %d bytes), built twice identical: %s |" % (C["built_sha256"], C["built_sha256_hex"], C["built_bytes"], C["built_twice_identical"]))
w("| live CodeSha256 before | `%s` (last modified %s); the live zip read from AWS hashes to it: %s |" % (C["live_before"], C["live_last_modified"], C["live_zip_is_live"]))
w("| rollback S3 version | `%s` of `s3://<the lambda-artifacts bucket the order names>/investor-reporting/irpt-ycharts-generate.zip` (bucket and key as in the real map entry's `artifact_s3_bucket` and `artifact_s3_key`); its `content-sha256` metadata equals the live digest: %s |" % (C["rollback_version"], C["rollback_is_live"]))
w("| members | %d built, %d live; %s |" % (C["members_built"], C["members_live"], C["member_count_note"]))
w("| name limb (built / live) | %d / %d mismatched |" % (C["built_signature_mismatched"], C["live_signature_mismatched"]))
w("| attribute limb (built / live) | %d / %d mismatched of %d attribute calls checked |" % (C["built_attribute_mismatched"], C["live_attribute_mismatched"], C["built_attribute_checked"]))
w("| method limb (built / live) | %d / %d mismatched of %d / %d method calls checked |" % (C["built_method_mismatched"], C["live_method_mismatched"], C["built_method_checked"], C["live_method_checked"]))
w("")
w("Last lines of the instruments (each run at its own path on the zip's bytes):")
for side in ("built", "live"):
    for limb in ("name", "attribute", "method"):
        w("- %s %s: `%s`" % (side, limb, C["limb_last_lines"][side][limb]))
w("")
w("### The four carried method-call sites (live carries the same four; compared by module and call text, never by line)")
w("")
w("| module | call | in live | reason (one sentence) | basis |")
w("|---|---|---|---|---|")
for s in C["method_mismatch_sites"]:
    w("| `%s` | `%s` | %s | %s | %s |" % (s["module"], s["call"], s["in_live"], s["reason"], s["reason_basis"]))
w("")
w("## Every moved member (%d): owning commits and class" % len(moved))
w("")
w("`owning_commits` = `git log <old pin>..%s -- <repo path>`: the commits between the live blob and the built blob on that path (the live bytes were checked equal to the old pin's blob for every row: %s). Old pin: the real map row for a staged member, `66207bce7d` (release 6b) for a native one." % (C["pin"][:10], all(m["live_bytes_equal_old_pin_blob"] for m in moved)))
w("")
w("| member | repo path | old pin | owning commits | class | one line |")
w("|---|---|---|---|---|---|")
for m in moved:
    oc = m["owning_commits"]
    commits = ", ".join("`%s`" % c["commit"] for c in oc) if len(oc) > 3 else "; ".join("`%s` %s" % (c["commit"], c["subject"][:70].replace("|", "/")) for c in oc)
    w("| `%s` | `%s` | `%s` | %s | **%s** | %s |" % (m["member"], m["repo_path"], m["old_pin"], commits, m["class"], m["one_line"]))
w("")
w("`served` = the change can alter an answer, a record or a call the function makes (a handler, a code path a route reaches, a schema the function validates or writes, a registry or policy file it reads at runtime). `inert` only where the reason is stated; when unsure it is `served`. The three resident-side members (`resident_worker.py`, `resident_main.py`, `durable_job.py`) are classed served because the package carries them and whether any process runs them from this artifact was not read (`install-resident.sh` installs from a package root with a SHA256SUMS file); the Lambda's own handler, `generate_installed.lambda_handler`, does not run the resident loop.")
w("")
w("## Branch A -- source-map entry landed first, then the build, then the module's Terraform path")
w("")
w("1. The apply amendment lands the candidate entry (`%s`, only the `irpt-ycharts-generate` entry; every `staged_from` row at `%s`, sha256 recomputed from `git show`) into `infra/aws/lambda/ci/lambda-source-map.json`. Order matters: the build reads the map. The entry's `artifact_sha256`, `deployed_code_sha256`, `last_deployed_at` and `deploy_ledger` are then rewritten by `record-terraform-deploy.sh` at the apply (today they are one release behind, point 4 above)." % (C["candidate_map"], C["pin"][:10]))
w("2. Build and upload: `bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-ycharts-generate` from the landed map; the object's `content-sha256` metadata must read `%s` (the two BUILD_ONLY builds here were byte-identical at this tree). A different digest stops the apply." % C["built_sha256"])
w("3. The module's Terraform path: `safe-apply` of the root `infra/aws/terraform/investor-reporting/ycharts` on `module.irpt_ycharts_generate.aws_lambda_function.this` only. The module takes `s3_object_version` and `source_code_hash` from the object (`modules/yang-lambda/main.tf` lines 38-39: the object's own VersionId and `content-sha256` metadata), so the plan must show those two attributes and nothing else on the function. Role, layers, environment, handler, runtime, memory and timeout are unchanged (section below). A change-management ledger entry in `org/critical_paths/change_management/` is opened at the start and closed at completion; both never-widen halves are signed before the apply.")
w("4. After-reads: the section below.")
w("")
w("## Branch B -- redeploy the rollback version, re-read at apply")
w("")
w("Redeploy S3 version `%s` (content-sha256 metadata `%s`, the digest live today) through the same Terraform path, pinning the function to that object version. The rollback version is RE-READ AT APPLY (`head-object` and, if the latest object is not the live one, `list-object-versions` on that one key) because a later upload would make today's reading stale. After the rollback the function's CodeSha256 must read `%s`. Branch B leaves any record the built code wrote (a request accepted with `acting_principal_id`, an `i3_sent_at` marker, a retained ANALYSIS_COMMENTARY artifact) in place; those are additive fields and rows the live code does not read (not read for every reader: the acceptance-record reader census is inherited from `2.0.0_SA_COO~Y2`'s report, 19 readers, 0 with a closed key set, and was not re-run here)." % (
    C["rollback_version"], C["live_before"], C["live_before"]))
w("")
w("## After-reads proposed for the applier (one per served change)")
w("")
w("- **Every change:** `aws lambda get-function-configuration` reads CodeSha256 `%s` and the same handler, runtime, memory, timeout, layers and environment names; then one direct invoke of the import census (`{\"irpt_import_census\": true}`, `generate_installed.import_census`: imports only, no route, no write, no vendor call) answers `failed: {}` for every packaged top-level module." % C["built_sha256"])
w("- **The acceptance pair (the read `2.0.0_SA_COO~Y2`'s census suggests):** one fresh accepted request through the real submission path: its acceptance record carries `acting_principal_id` equal to the verified submitter's principal id; one request accepted BEFORE the apply reads back byte-equal (no field added). The same fresh record carries `ingestion_gate_revision` `%s` and an unchanged `destination_policy_revision`." % next(a for a in arms if a["name"].startswith("composition"))["detail"].split("built ")[1][:80].split(" ")[0])
w("- **served.py:** one direct invoke naming `analysis-request-read` from the svc-custody-statement subject answers UNSUPPORTED_OPERATION where live answered NOT_AUTHORIZED (replay arm); every other operation unchanged.")
w("- **loaders.py, ids.py, custodian_key_seam.json:** the import census above; the firm directory pointer is read only on a request, so no additional read is proposed without a request.")
w("- **Registry, policy and schema files (`lib/opal_naming.py`, `infra/logic/registry/*`, `org/standards/NAMING_SCHEMA.json`):** the import census and the fresh accepted request above (it binds `ingestion_gate_revision` and `destination_policy_revision`); `destination_policy_revision` must read the unchanged X10 digest `e0046398...`.")
w("- **owned_requests.py, repository.py, retention.py, durable_job.py, resident_worker.py, resident_main.py:** no read is proposed against the Lambda, because no route of this function reaches them (replay arms exercise them against fakes). If a process runs them from this artifact the applier reads that process's own first poll line (`IRPT_RESIDENT_POLL`, `IRPT_RESIDENT_PACKAGE outcome=`).")
w("")
w("## Role, routes, layers, environment: unchanged, read from Terraform")
w("")
w("Read from `infra/aws/terraform/investor-reporting/ycharts/generate.tf` (the file is not touched by this order) and compared with the live configuration:")
w("")
w("| attribute | Terraform | live | |")
w("|---|---|---|---|")
w("| handler | `generate_installed.lambda_handler` | `%s` | %s |" % (cfg["Handler"], same("generate_installed.lambda_handler", cfg["Handler"])))
w("| runtime / memory / timeout | python3.12 / 512 / 900 | %s / %s / %s | %s |" % (cfg["Runtime"], cfg["MemorySize"], cfg["Timeout"], same((("python3.12", 512, 900)), (cfg["Runtime"], cfg["MemorySize"], cfg["Timeout"]))))
w("| role | `irpt-ycharts-generate-role` (inline policies `irpt-ycharts-generate`, `irpt-ycharts-generate-custody-factory-policy`) | `%s` | %s |" % (cfg["Role"].split("/")[-1], same("irpt-ycharts-generate-role", cfg["Role"].split("/")[-1])))
w("| layers | `irpt-common` (latest version by name), `AWSSDKPandas-Python312:16` | %s | %s |" % (", ".join("`%s`" % lay for lay in layers), same(["AWSSDKPandas-Python312:16"], [lay for lay in layers if lay.startswith("AWSSDK")])))
w("| environment variable NAMES (%d) | %s | %s | %s |" % (len(TF_ENV), ", ".join("`%s`" % n for n in TF_ENV), ("same %d names" % len(env_names)) if env_names == TF_ENV else str(env_names), same(TF_ENV, env_names)))
w("| absent on purpose | `IRPT_LIVE_YCHARTS_CALL` (its absence is what makes `job.lambda_handler` refuse a vendor call); `IRPT_ANALYSIS_READY_QUEUE_URL` is not set by Terraform | `IRPT_LIVE_YCHARTS_CALL` present: %s; `IRPT_ANALYSIS_READY_QUEUE_URL` present: %s | %s |" % (
    "IRPT_LIVE_YCHARTS_CALL" in env_names, "IRPT_ANALYSIS_READY_QUEUE_URL" in env_names, same(False, "IRPT_LIVE_YCHARTS_CALL" in env_names)))
w("| routes / schedules / event source mappings | none created by this root (`NO ROUTE, NO SCHEDULE, NO EVENT SOURCE MAPPING IS CREATED HERE`); the three routes are declared in `docs/contracts/investor-reporting/v1/routes.json` | event source mappings on the function: 0 | equal |")
w("")
w("Values of the environment variables are not printed here (a queue URL carries an account id). This build changes none of the above and the apply changes only the object version and `source_code_hash` of the function.")
w("")
w("## The replay (offline; live zip against built zip; `IB124-1_replay.json`)")
w("")
w("%d arms, every verdict `identical` or `expected-diff` (%d expected-diff, %d identical), %d negative controls. Harness: `replay/run_replay_426.py` (runs the probes in this directory's `replay/`, the unchanged ~272 binding-case runner, and the repository's own pin test files against each zip's modules). boto3 is replaced by an in-memory fake before any packaged module is imported; every socket connect and every name resolution but localhost is refused; AWS is never called by the replay; every id is synthetic; no client data is read. %d test ids ran on each tree; the built tree regresses none that passes on live." % (
    len(arms), len(exp_arms), sum(a["verdict"] == "identical" for a in arms), sum(a["negative_control"] for a in arms), R["tests_run_per_tree"]))
w("")
w("| # | arm | verdict | control | members named |")
w("|---|---|---|---|---|")
for i, a in enumerate(arms, 1):
    w("| %d | %s | %s | %s | %s |" % (i, a["name"].replace("|", "/")[:170], a["verdict"], "NEGATIVE CONTROL" if a["negative_control"] else "", ", ".join("`%s`" % m for m in a["members"]) or "-"))
w("")
w("Carried method sites exercised by an arm: `publication .lookup(1)` (arm: carried method site publication), `publisher .validate(2)` x2 (arm: carried method sites publisher), `resident_worker .renew(ttl=900)` (arm: carried method site resident_worker). All three: the call line was reached on both zips and the result is identical on live and built; the callee is a fake shaped like the injected object (detail in each arm).")
w("")
w("Each `expected-diff` arm, with its deciding facts, is in `IB124-1_replay.json` (`detail`). In short: composition (ingestion_revision moves), contract schemas (new history shape valid, legacy invalid; `retained_ref`, `persist_inputs`, `covered_account_ids` appear; `multi_asset` leaves the holdings asset_class enum), packaged registry (new ACTIVE policy `irpt-anlreq-x10-v1`; research policy widened to three firms with a new policy digest; `lookup('4698')`), the svc-custody-statement operation, the loader pointer, the acceptance pair (the record gains `acting_principal_id`), the resident arms (I3 send, `i3_sent_at`, package poll, five-key runtime) and the pin tests that pass only on built.")
w("")
w("## What is NOT exercised")
w("")
w("- **No live call of any kind.** No request was made to the deployed function, no vendor call, no write to any AWS resource. The vendor path of the function is behind `job.lambda_handler`'s per-use consent sentence, which the environment does not set.")
w("- **The real injected objects** behind the four carried method sites (the retained `ReportRepository.validate`, the operation-fenced transport) are not in this package; the arms use fakes shaped like them.")
w("- **PDF text extraction and certification** (PyMuPDF is not on the replay box: the replay reads `BackendUnavailable` from `foreign_firm_names` on both zips; whether the Lambda's layers carry it was not read): `foreign_firm_names` and `build_publication` are stand-ins in the publisher arm; tests that need a real PDF fail identically on both trees.")
w("- **Real DynamoDB, S3 and SQS semantics** (conditional expressions beyond the in-memory fakes, KMS, versions, queue visibility): the arms use in-memory fakes.")
w("- **The Lambda-side route reach of the history reader, the repository and retention service-subject paths, and the resident loop:** exercised through the repository's pin tests and fakes, not through a deployed route.")
w("- **Any request from a real principal**, including the allow-listed Opal producer principal: `producer_for` is read with synthetic principals only.")
w("- **The 409 binding-case runner** builds `entry.ENTRY`; the upload route exists only in `generate_installed.build_boundary` and is replayed by the route arm instead.")
w("")
w("## Rows and state")
w("")
w("- Row `IRPT_BCKEND-D2-W285-S1` (the method limb reads 4 on the build and the same 4 on live) stays as filed; AMENDMENT 1 ruled it. Any further row is listed in the worker report.")
w("- `git status --short` after each of the two BUILD_ONLY builds showed no tracked change. The candidate map writer, the closure tools, the census writer, the replay harness and this writer are in this directory.")
(ddir / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-426.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("packet written: %d lines, %d bytes" % (len(L), len("\n".join(L))))
