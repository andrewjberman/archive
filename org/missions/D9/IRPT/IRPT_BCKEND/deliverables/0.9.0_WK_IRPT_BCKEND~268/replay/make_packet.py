"""Scratch: writes NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-405.md from the census and replay JSON (so every number in the packet is read, not typed)."""
import json
from pathlib import Path

D = Path("C:/dev/wk-irpt-bckend-268/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~268")
c = json.loads((D / "IB106-1_release_census.json").read_text())
r = json.loads((D / "IB106-1_release_replay.json").read_text())
PIN = c["pin"]
arts = {a["function"]: a for a in c["artifacts"]}
st = arts["irpt-status"]
rows = c["candidate_map"]["irpt_status_staged_from_rows_repinned"]
alt = c["candidate_map"]["minimal_alternative_built_sha256"]
ident = sum(1 for a in r["arms"] if a["verdict"] == "identical")
diff = sum(1 for a in r["arms"] if a["verdict"] == "expected-diff")
neg = sum(1 for a in r["arms"] if a["negative_control"])


def short(s, n=12):
    return s[:n]


L = []
w = L.append
w("# Never-widen sign-off packet -- IB-pr-405: the owned request read returns the persist inputs; svc-custody-statement reads it for cottonwood only\n")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~268 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO msg 3088, IRPT_DASHBD ADDENDUM 9.2 (2)). Nothing here was uploaded, deployed, applied or written: "
  "BUILD_ONLY from a clean tree, offline replays, AWS reads only (2026-10-09 ~11:0xZ). Files beside this packet: `IB106-1_release_census.json`, "
  "`IB106-1_release_replay.json`, `replay/` (the scripts and the raw outcomes of both sides). Model: `0.9.0_WK_IRPT_BCKEND~262/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md`.\n")
w("**READ THIS FIRST.**\n")
w("1. **The artifacts below are built at a CANDIDATE source map, not the real one.** `infra/aws/lambda/ci/lambda-source-map.json` pins irpt-status's `served.py`, "
  "`entry.py` and `owned_report.py` to older commits, so a build at the real map does not carry this change; the map is outside this order's grant. The builds use "
  "`BAU_SOURCE_MAP_OVERRIDE` with a scratch copy in which ONLY irpt-status's `staged_from` rows listed under Branch A step 1 are re-pinned to the pin. "
  "**The applier commits those seven rows (a map edit), rebuilds at the REAL map, and compares the printed sha256 to the table: ABORT if different.** (Row IRPT_BCKEND-D2-W268-S1.)")
w("2. **The irpt-status release is wide, and most of it is other cells' pending work.** Live irpt-status is behind the real map already (AR-y-22's `/original` route and TO-AR-y-11's `ticket_id` "
  "are staged but not live), and the persisted-report half of `report_index` needs the retention stack the packaged zip lacks (`retention.py` has no policy-revision support, `repository.py` "
  "does not list CUSTODY_REPORT, the packaged registry has no `irpt-custody-x10-v1` row). The candidate therefore also re-pins `retention.py`, `repository.py`, `composition.py` and "
  "`reporting_policies.json`; they carry the IB-pr-386 service-principal rules and the AR-t-12 writer into irpt-status. **%d of %d members change versus live; 3 are this cell's.** The table under "
  "\"What moves\" names each member's owner. (Row IRPT_BCKEND-D2-W268-S2, ARMED.)" % (st["changed_member_count_vs_live"], st["built_members"]))
w("3. **Only irpt-status needs a deploy.** The other seven functions package `served.py` too, at the old pin, so their built zips do not change (5 of 7 are byte-identical to their live zips; "
  "irpt-narrative and irpt-ycharts-generate differ from live for reasons that are not this release). They are in the census so the signer sees the whole set.")
w("4. **Not replayed:** whether the gateway/edge admits the svc-custody-statement token on `GET .../analysis/requests/{requestId}` (outside the zip). The retention service in the replay is a double. "
  "Both are the after-read's first checks. (Row IRPT_BCKEND-D2-W268-S3.)\n")
w("## What changed in code (commits `1cb1c965f3`, `9489a0fed0`)\n")
w("- **Route and operation extended:** `GET /api/scoped/investor-reporting/analysis/requests/{requestId}`, operation `analysis-request-read` (served by irpt-status). No new route. "
  "The new member is **opt-in**, `?include=persist_inputs` (a comma list with `comparisons` and `composition`), like the two existing includes: a caller that does not ask gets `{identity, accepted_at}` key for key.")
w("- **`persist_inputs`** (`OwnedAnalysisReader.persist_inputs`, `ops/owned_report.py`; `ops/entry.py` merges it), exactly four members, each read from the record the read already loads:")
w("  - `artifact_id` = `composition_ref.artifact_id` of the accepted record (`ART-<64 hex>`, the retained request `custody-report-persist` takes);")
w("  - `composition_sha256` = `composition_ref.sha256`;")
w("  - `retention_policy` = `composition_ref.retention_ref.policy_revision` (read, never typed; the runner's DB41-3-AC1 compares it to `irpt-custody-x10-v1`, and the registry registers REQUEST_COMPOSITION under `irpt-x10-v1`, row IRPT_DASHBD-W61-S3);")
w("  - `report_index` = `{report_id, revision, retention_ref}` of the persisted CUSTODY_REPORT row, found by the repository's own identity formula over the artifact's stored owner and one consistent prefix query (`Limit` 2) on the same table; `null` when none is persisted; more than one revision is refused, never chosen.")
w("- **Re-authorized per request** through the read's existing path: `_materialize` (owner binding, the current grant via `authorize_current`, the retained composition reference), the report row bound to owner, tenant and retention chain with `require_live(accepted=True)`, then `_final` (record unchanged, retention `require_live`). Another firm and a non-owner are refused (replay arms below).")
w("- **svc-custody-statement** (`_authz/served.py`): `SVC_CUSTODY_STATEMENT_OPERATIONS` gains the ONE operation `analysis-request-read` (now 4). Its firm stays the registry's cottonwood (`_svc_custody_statement_firm`), it is never `internal` (no any-firm or ALL reach, `selected_tenant` of another firm is FIRM_BINDING), and a sibling owned read (`analysis-request-history`) is still refused. "
  "Because the grant is the operation, svc can also make the plain read of a cottonwood request; as an OPAL_GLOBAL principal it reads any owner's cottonwood request, as every Opal reader does.")
w("- **No IAM change:** `irpt-status-role` already allows `dynamodb:Query` and `GetItem` on `irpt-requests` (policy `irpt-status-policy`, Sid `ReadJobLeasesCheckpointsAndRequestRevisions`, read 2026-10-09). No route, schedule, environment or layer change.")
w("- **Tests:** `ops/tests/test_persist_inputs.py` (11) and `_authz/tests/test_svc_custody_statement.py` (the `persist_inputs` tests): e.g. `test_persist_inputs_owner_reads_all_four_members`, `test_persist_inputs_other_firm_is_refused_before_any_read`, "
  "`test_persist_inputs_non_owner_in_the_same_firm_is_refused`, `test_svc_custody_statement_persist_inputs_read_cottonwood_admitted`, `test_svc_custody_statement_persist_inputs_other_firm_claim_refused`.\n")
w("## The pin and the builds\n")
w("- **Release pin P: `%s`** (branch `wk-IRPT_BCKEND-268`). The code is `1cb1c965f3` and `9489a0fed0`; every later commit on the branch is deliverables only. The candidate-map rows point at P." % PIN)
w("- BUILD_ONLY from a clean tree (`git status --porcelain` 0 lines before and after every build), each function built twice (%d builds), **byte-identical between runs: %s**, rc %d. Command: `%s`. Zips kept only in scratch; nothing uploaded; the real source map untouched." % (
    c["build_only"]["builds"], "YES" if c["build_only"]["byte_identical_between_runs"] else "NO", c["build_only"]["rc"], c["build_only"]["command"]))
w("- Live read with `aws lambda get-function` (the downloaded zip's sha256 equals the reported CodeSha256 for all 8) and `aws s3api list-object-versions` (latest version = the rollback version).\n")
w("| Function | Built sha256 (base64, = the BUILD_ONLY line) | built bytes | live_before (CodeSha256) | Rollback S3 version | Deploy? |")
w("|---|---|---|---|---|---|")
for fn in ["irpt-status", "irpt-performance-adapter", "irpt-directory-search", "irpt-narrative", "irpt-ycharts-generate", "irpt-export-render", "irpt-holdings", "irpt-49f-reporting-read-lambda"]:
    a = arts[fn]
    w("| `%s` | `%s` | %d | `%s` (%s) | `%s` | %s |" % (fn, a["built_sha256"], a["built_bytes"], a["live_before"], a["live_last_modified"][:19] + "Z", a["s3_rollback_version"],
                                                      "**YES**" if a["deploy_needed"] else "no (built %s live)" % ("=" if a["built_sha256"] == a["live_before"] else "differs from, for reasons outside this release,")))
w("\nMinimal alternative for irpt-status (rows 1-3 only: `served.py`, `entry.py`, `owned_report.py`): built sha256 `%s`. With it `persist_inputs` answers three members and `report_index` null, "
  "but is **expected to refuse whenever a report IS persisted** (reasoned from the packaged `retention.py`, whose `reference()` takes no policy revision; not replayed). Not recommended: the runner's read after its own persist would refuse.\n" % alt)
w("## What moves in irpt-status (10 members versus live)\n")
w("| Member | Live blob | Built blob | Class | Owners since the live blob (latest first) |")
w("|---|---|---|---|---|")
for m in st["changed_members"]:
    own = "; ".join(o[:110] for o in (m.get("owners_since_live_latest_first") or [])[:3]) or (m.get("note") or "")
    w("| `%s` | `%s` | `%s` | %s | %s |" % (m["member"], m["live_sha256_prefix"], m["built_sha256_prefix"], m["classification"], own))
w("")
w("Everything else in the zip (%d of %d members) is byte-identical to live." % (st["built_members"] - st["changed_member_count_vs_live"], st["built_members"]))
w("The `irpt-x10-v1` policy row is byte-equal at both registry pins (so no retained record's `policy_sha256` moves); the `irpt-ycdgen-research-v1` row changes state PENDING_ENFORCEMENT to ACTIVE and its firms to three (YCD-a-7), and `irpt-custody-x10-v1` and `irpt-anlreq-x10-v1` are added.\n")
w("## Blast radius\n")
w("- **Functions touched:** `irpt-status` only (Lambda code). **Served output:** `analysis-request-read` gains an opt-in member; every other irpt-status route answers as the pinned stack makes it (the AR-y-22 `analysis-request-original` operation is installed in the handler: replay arm `installed_handler_composes`). "
  "**Authorization reach:** svc-custody-statement gains one operation, bound to cottonwood; no other subject, firm or operation. **No** IAM, route, schedule, table, environment or layer change; no data written.")
w("- **Carried with it (other cells' pending changes, named in the table):** TO-AR-y-11 (`acceptance.py`, `submission.py`: `ticket_id` in the accepted record), AR-y-22 (`entry.py`, `owned_report.py`, `pdf_link.py`: the `/original` link), IB-pr-369/YCD-l-6/IB-pr-386/AR-t-12 (the retention stack), E8/YCD-a-7/AR-t-12 (registry rows). "
  "Each is already staged in the real map or in a function that serves it live; the signer reads this release as carrying them.")
w("- **Writers of the changed property:** the Lambda code object of `irpt-status` has one writer, the Terraform apply of `infra/aws/terraform/investor-reporting/ops/lambda.tf` (`module.irpt_status`, source `investor-reporting/irpt-status.zip`). N writers = 1; N rules read = 1 (the build + apply path).\n")
w("## Branch A (released)\n")
w("0. **Ledger:** open `org/critical_paths/change_management/` BEFORE the first act; it names every task family or function that pulls the moved key (`investor-reporting/irpt-status.zip`: the irpt-status function only); close it after the after-read.")
w("1. **Commit the map rows** (an edit to `infra/aws/lambda/ci/lambda-source-map.json`, `functions.irpt-status.staged_from`, the applier's/issuer's act): set `pin` and `sha256` of exactly these rows to the values in the last two columns (the same values are in `replay/candidate_map_rows.json`):\n")
w("| packaged_as | repo_path | pin before | pin after | sha256 after |")
w("|---|---|---|---|---|")
for d in rows:
    w("| `%s` | `%s` | `%s` | `%s` | `%s` |" % (d["packaged_as"], d["repo_path"], d["pin_before"][:10], d["pin_after"], d["sha256_after"]))
w("")
w("2. **Rebuild at the REAL map from a clean tree** (P or a descendant whose map, `_authz/`, `ops/` and `reports/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status`; the printed sha256 must be `%s`. ABORT if different." % arts["irpt-status"]["built_sha256"])
w("3. **Upload and deploy:** the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-status.zip`), then the Terraform path of the function (`safe-apply` on the ops root; never `aws lambda update-function-code`). Expected plan: one in-place update of `module.irpt_status.aws_lambda_function.this` (`source_code_hash`), no IAM/route/env change.")
w("4. **Before the first real call,** run the replay arm below against the bytes actually uploaded.")
w("5. **Served effect:** owner and firm users see the same answers as today for every route they use (replay: the existing-caller arms are identical); the runner reads `?include=persist_inputs` as svc-custody-statement for cottonwood.\n")
w("## Branch B (rolled back)\n")
w("- `irpt-status`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `%s` of `investor-reporting/irpt-status.zip` (its CodeSha256 is the `live_before` value `%s`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and that version still the latest." % (st["s3_rollback_version"], st["live_before"]))
w("- The other seven functions: nothing to roll back (not deployed by this release). Their current rollback versions are in the table.")
w("- Revert the seven map rows with their commit. No other state: no table row, IAM, schedule or environment is written. If the svc-custody-statement read has already been used, nothing it did persists (it is a read).\n")
w("## The replay (%d arms: %d identical, %d expected-diff, %d negative controls)\n" % (len(r["arms"]), ident, diff, neg))
w("Recorded in `IB106-1_release_replay.json`; harness `replay/run_side.py` (the REAL irpt-status modules of one extracted zip in the flat layout, `entry.build_owned_entry` and `served.lambda_entry`, offline doubles for storage only), raw outcomes of both sides in `replay/raw/`. Synthetic fixtures, no client data.\n")
w("| arm | verdict | negative control |")
w("|---|---|---|")
for a in r["arms"]:
    w("| %s | %s | %s |" % (a["name"], a["verdict"], "yes" if a["negative_control"] else "no"))
w("\n**Arm for the applier (rerun against the uploaded bytes):** extract the live irpt-status zip (after the upload, `aws lambda get-function` Code.Location) into an EMPTY directory outside the worktree, then `python -I replay/run_side.py <dir> built <out.json>` and compare to `replay/raw/replay_built.json` arm by arm (the `static` block and every `arms.*` outcome). "
  "STOP if the `svc_cottonwood_include_persist_inputs` arm is not admitted with four members, if any `other_firm_*`, `non_owner_*` or `svc_claims_*` arm answers data, or if `ctl_retention_dead_owner_include_persist_inputs` answers data (the harness would then not be reaching the retention check).\n")
w("## The after-read\n")
w("1. One `GET /api/scoped/investor-reporting/analysis/requests/{requestId}?include=persist_inputs` as svc-custody-statement (cottonwood request): expect `data.persist_inputs` with exactly `artifact_id`, `composition_sha256`, `retention_policy`, `report_index`. A 403 from the gateway/edge instead of the Lambda answer means the edge does not admit the svc token on this GET route (row W268-S3): that is outside this cell and is read first.")
w("2. The same request as an ordinary advisor of another firm: refused. The same without `include`: `{identity, accepted_at}` as before. CloudWatch shows no `TypeError` or `KeyError` in the `irpt-status` log group.")
w("3. Until the apply, every one of these is UNEXERCISED against the live service; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.\n")
w("## Rows\n")
w("`IRPT_BCKEND-D2-W268-S1` (the source map pins the three members; candidate map used; OBSERVATION, INERT), `IRPT_BCKEND-D2-W268-S2` (irpt-status carries other cells' pending changes and needs the retention stack; OBSERVATION, ARMED, disarm owner 2.0.0_SA_COO~P2), "
  "`IRPT_BCKEND-D2-W268-S3` (the published contract does not name `include=persist_inputs` or the member; edge admission unverified; OBSERVATION, INERT). Related, not this cell's: `IRPT_BCKEND-D2-S43`, `IRPT_DASHBD-W61-S2/S3`.")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-405.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("packet bytes", len("\n".join(L)))
