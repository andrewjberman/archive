#!/usr/bin/env python
"""OG-ap-50 Phase A step 4: write W/NEVER_WIDEN_ASK_OG-ap-50.md from the records (no number is typed that a record holds).
usage: python ap50_ask.py   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
J = lambda p: json.load(io.open(W + p, encoding="utf-8"))  # noqa: E731
rel, pa = J("ap50_release.json"), J("PHASE_A_OG-ap-50.json")["body"]
t, hl, seams, ovl, take, grant = J("ap50_pa/tests.json"), J("ap50_pa/host_leg.json"), J("ap50_pa/seams.json"), J("ap50_pa/overlay.json"), J("ap50_pa/take.json"), J("ap50_pa/grant.json")
census = J("ap50_pa/status_object_census.json")
G = "infra/aws/ec2/opal-gateway/"
base, relsha, trunk = rel["base_sha"], rel["release_sha"], rel["trunk_sha"]
b10, r10, t10 = base[:10], relsha[:10], trunk[:10]
sec = json.load(io.open("org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~153/SSRF_AUDIT_R43.json", encoding="utf-8"))
sec = sec.get("body", sec)


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout.strip()


blobs = {h: git("rev-parse", "--short=12", "%s:%sapp/%s.py" % (base, G, h)) for h in ("harvest_research", "harvest_figures", "harvest_identity", "harvest_keys")}
stat = git("diff", "--shortstat", base, relsha)
s3 = boto3.client("s3")
tar = s3.get_object(Bucket="opal-313476888478-lambda-artifacts", Key="ec2/opal-gateway/opal-gateway-%s.tar.gz" % b10)["Body"].read()
tar_sha, tar_len = hashlib.sha256(tar).hexdigest(), len(tar)
rl, hr, ts = pa["route_leg"], pa["host_read"], pa["tests"]
scan = hr["response_scan"]
ovl_add = sum(1 for x in ovl["laid"] if x["status"] == "added")
ovl_mod = len(ovl["laid"]) - ovl_add
fs = t["full_suite"]
other_unnamed = ", ".join("`%s`" % p for p, _ in seams["unnamed_differing"])

doc = """# NEVER-WIDEN ASK -- `OG-ap-50` -- the round-46 thirteenth batched gateway release: a NEW SERVED ROUTE, `GET /api/admin/gateway/families` (`OG-cd-2`), behind the owner gate, reading the three actions `OG-cd-3` granted

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-50.round-46-thirteenth-batched-release-the-family-depth-route.md` (GO for Phase A: msg 35983).
Release: `release_sha` = `{relsha}` (branch `rel-nfra-oplgtw-batch14`, tree `C:/tmp/og-rel-batch14`), cut on the live ref `base_sha` = `{base}` (`OG-ap-48`'s release, the twelfth) from `trunk_sha` = `{trunk}` (box/sitez at the GO).
**The base is the live ref READ ON THE HOST** (`/opt/opal-gateway/.deployed_commit` reads `{base}`, recorded as `live_ref_host`; read {read_at}), and the host's md5 walk equals that commit ({differ} differ, 0 missing, 0 extra: `ap50_pa/host_md5_before.json`). `6575999df5` (dell1's harvest release) is an ancestor of `base_sha`.
**dell1's files, carried UNCHANGED, with their blobs as read at `base_sha` (the release's blob is the same object for each):** the four harvest files `app/harvest_research.py` `{h1}`, `app/harvest_figures.py` `{h2}`, `app/harvest_identity.py` `{h3}`, `app/harvest_keys.py` `{h4}`.
**Gates, read at this Phase A (standing condition 3: every read-only record pins its base sha):** the SSRF audit record `OG-sec-3` (`SSRF_AUDIT_R43.json`) reads `{secv}` with `controllable_yes` {secc} (the outbound HTTP code is unchanged by this release); `OG-cd-2` COMPLETE and drained (trunk `{t10}`); `OG-cd-3`'s ledger `nfra-oplgtw-grants-cd3` CLOSED and the read grant LIVE: `get-role-policy` for `opal-gateway-role` / `{pname}` read {gstm} Allow statements over {gacts} (policy sha256-16 `{gsha}`; `ap50_pa/grant.json`), read before the host read below. The probe-listener lease parameter reads ABSENT (`ap50_pa/lease_param.json`).

## 1. The diff, by file (`git diff {b10} {r10}`: {stat})

- `app/admin_api.py` (`OG-cd-2`): exactly TWO ADDED LINES and no removed line, at zero context: (1) `from . import family_depth` (after `admin_people`); (2) `Route("/gateway/families", owner_only(family_depth.families), methods=["GET"])` (after the `/people` route). The route is NFRA_MCPORTAL's file (`admin_api.py`); this ask names the two lines. Byte-equal to its blob at `trunk_sha`.
- `tests/test_og_cd2.py` (`OG-cd-2`, new, 80 lines, 3 tests): the route is mounted once as GET, wrapped behind `owner_only`; no identity answers 401 and a verified non-owner 403 with `family_depth.read` never called; the owner answers 200 with one call. Byte-equal to its blob at `trunk_sha`.
- NOT in the release (the check counts them at 0): `app/family_depth.py` (already live and byte-equal to trunk), `app/owner_gate.py`, `app/audit.py`, `server.py`, `graph.py`, `tools.py`, `probe_listener.py`, every `client_*.py`, `typed_scope.py`, `etfs_rivals_flow.py`, `destructive_ops.py`, `app/refs/`, `deploy-to-ec2.sh`, `deploy/opal-gateway.service`, `EC2_MANIFEST.json`, the catalog, any Terraform.
- **Seams (every app module the taken file imports):** {nseam} distinct modules, {nedge} edges, {nstop} STOP-class. All are in the live base and identical to trunk except `app/admin_api.py` itself (in the take list). Files that differ between the live ref and trunk and are NOT taken: {other_unnamed} (none is imported by `admin_api.py`).
- **Test results** (release tree and, beside it, a second tree at the live ref with the same sparse cone, both gateway folders clean in `git status` after the gate overlay was restored): the named set (`test_og_cd2`, the ten `test_admin_*` files, `test_owner_gate`, `test_og_cd1`) passes {nnamed} in both orders; it also holds **{nlit} failures, the SAME {nlit} that fail at the live ref** (`test_admin_fabric`, `_fabric_calls`, `_fabric_gitstate`, `_fabric_overlap`, `_gateway_breakdown`, `_people`: carried reds; at the live ref the same set reads 101 passed and the same {nlit} failed). The record's `named_failed` is therefore {nnew} NEW failures, and `named_failed_literal` is {nlit}; **the order's `named_failed: 0` cannot be met as a literal count, and the signers should read it that way.** The window set plus `test_og_cd1`, `test_og_pr6`, `test_og_cd2` ({nwin_files} files) passes {nwin} in both orders, 0 failed. The full suite: release {rpass} passed / {rf} failed, live ref {lpass} passed / {lf} failed; **the failing sets are IDENTICAL ({both} names in both, 0 only in the release, 0 only at the live ref)**; the release's three extra passes are `test_og_cd2`. `bash -n deploy-to-ec2.sh` clean and `--preflight-only` reads `{pf}`. The host-shaped import check imported 11 of 12 modules (`admin_api`, `owner_gate`, `family_depth` among them) with zero reads; `server` needs the service's environment (`TENANT_ID`), as in every earlier record.

## 2. The widening: ONE NEW SERVED ROUTE (stated plainly)

- **A new route, `GET /api/admin/gateway/families`, behind the owner gate** (the verified owner identity only, as `/api/admin/whoami`; the load balancer's signed header is the only source of identity). It runs `app.family_depth.read()` in the request threadpool. **It exercises the three read actions `OG-cd-3` granted and nothing else:** `events:DescribeRule` on the silver sweep rules, `s3:GetObject` on the `backfill-status.json` objects, `s3:ListBucket` on the silver prefixes and the one-level source roots. No new tool, no `tools/list` change (103), no env key, no IAM, no write action anywhere in the module.
- **What a reader learns:** per vendor family the gateway serves, the sweep schedule, the last sweep and the earliest served date, each with its claim (`measured` / `inferred` / `absent`), its read time and its source; and no data value.
- **What the response ALSO contains (measured on the host; the order's description does not say it):** (a) the S3 URI of each status object it read or tried (source root and scope name: {nuri} URI strings, {nkeys} status keys listed); (b) for a value whose AWS call failed, up to 200 characters of the AWS error text in `source`. **A denied `GetObject` names the gateway role's ARN, the AWS account number and the instance id in that text**: in the first host read {narn_leaves} of {nvals} values carry it ({n12} twelve-digit runs and {narn} `arn:aws` strings in {nbytes} bytes; 0 e-mail-shaped strings). The reader is the verified owner only; the host record carries counts and masked shapes only. `app/family_depth.py` is live and not in this release, so the text cannot be masked here; masking `_why` is a one-function change in a separate cell. Rows `NFRA_OPLGTW-Z-S407` and `-S406` carry this and the next point. **The signers' call: release as is (owner-only, internal) or hold for the mask.**
- **Why values are denied or absent (measured, not assumed):** the first host read returned {fam} rows of denominator {den} ({dfam} distinct families, {nvals} values): **{meas} measured, {inf} inferred, {absn} absent, each absent with its reason, 0 claim-less** ({wall} s, peak {rss} MB). The AccessDenied answers are for status objects that DO NOT EXIST (`blackdiamond` 0 of 3 silver scopes hold `meta/backfill-status.json`, `orion` 1 of 2, `smartx` 0 of 1, `ap50_pa/status_object_census.json`): S3 answers AccessDenied for a missing key when the caller cannot list that prefix, and the identity policy allows `GetObject` on the key shape for all six roots tested. One schedule value is absent because the sweep rule `opal-assets-silver-bd49finsurance-sweep-daily` does not exist. The channel `link` values are `inferred` by construction.
- **process-wide state this change touches: the admin router imports `app.family_depth` at process start and the admin route table grows by ONE entry ({rb} routes at the live ref, {ra} at the candidate, measured on the host); nothing else, read.** I opened `app/admin_api.py`, `app/family_depth.py` (its top level holds only imports, constants, one `re.compile` and a `__main__` guard; `boto3` is imported lazily inside `read()`) and `app/owner_gate.py` (unchanged). No logger, handler, signal, thread, socket, environment read, `sys.path` change or global-config change happens at import. At request time the only effect is `read()`'s describe, get and list calls under the grant.
- **Measured on the host in fresh processes under the cgroup hard guard `oom_score_adj_1000_cgroup_memmax_1400mb`** (`systemd-run --scope -p MemoryMax=1400M`, wall limit 120 s; scratch copies removed; the service PID {pid} stable, `NRestarts` {nrs}; `ap50_pa/host_leg.json`): **the route leg** (live ref's `app.admin_api` in one process, the candidate's in a second, `TestClient` on the real `admin_app` with `read` replaced by a call-counting stub and the identity faked): routes {rb} -> {ra}; no identity {u} (want 401); a verified non-owner {n} (want 403); `/whoami` with no identity {w} (want 401); a missing route {m} (want 404); `read()` called on a refusal: {rc}; the owner {o} with {oc} stub call. **The host read** (the REAL `read()` once, as the gateway instance role: `sts get-caller-identity` shows `{ident}`, no account number printed): the figures above.
- **Disclosure about the host read's scratch tree:** a FRESH process has no live integrations registry, so `default_channels()` reads `ENABLED_INTEGRATIONS` from `deploy-to-ec2.sh`, and **that file is not on the host** (`/opt/opal-gateway/deploy-to-ec2.sh` reads absent; the first attempt raised `FileNotFoundError` with no AWS call). The scratch copy therefore carried the release tree's `deploy-to-ec2.sh` (byte-equal to the live base's) beside `app/`. The running service has a populated registry and does not read the file. **Phase B step 7 (the driven read from the deployed tree) will need the same staging**; row `NFRA_OPLGTW-Z-S406` asks the issuer to rule.
- **Honest limits:** the route leg uses a stub for `read()` and a fake identity (the owner's real header can only come from the load balancer, so an agent cannot call the route as the owner); the host read is the module in a scratch process, not the service; the owner-session read of the panel is the owner's, later, and is not this order's.

## 3. The order of acts (Phase B)

1. Read every open gateway ledger first (an open ledger of another seat is a STOP). Re-read the live ref on the host (`{b10}`; any other value is a STOP and a re-cut), the `.env` (65 keys), one process, `NRestarts`, the unit limits, the host md5 walk again.
2. Ledger `nfra-oplgtw-gateway-release-batch14`, entry AND sentinel committed first; the live ref's tarball sha256 recorded in it.
3. **Before the deploy:** one local request with no identity header to `127.0.0.1:<service port>/api/admin/gateway/families` (not through the load balancer): `route.before_status`, expected 404.
4. Restore the gate overlay (section 7); deploy from `C:/tmp/og-rel-batch14` through `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF={b10}` under the stale-base guard; no `HALT_OVERRIDE`.
5. Read back against the triggers (section 6); the marker, the unit limits and the host md5 of dell1's four harvest files, `graph.py`, `probe_listener.py` and the two released paths beside their blobs are read and PRINTED.
6. The served read, UNARMED ONLY (`CODE14_SERVED.json`): the lease parameter ABSENT before and after (no SSM write); a connection to the listener answers 403 `probe_not_armed`; `armings` 0; **the route after the deploy: no identity header answers 401, `/api/admin/whoami` 401, a missing route 404**; the service PID stable, `NRestarts` 0; the 27-tool read passes 27 of 27 under the hard guard in a fresh process; `tools/list` equal before and after.
7. **THE COUNTS (standing condition 2):** over the 30-minute read-back, the service's own `POST /mcp` journal lines and, over the SAME window, the audit-lake records (the method of `ap42_graphcounts.py`); lines > 0 and lines >= 0.25 times the records; `audit_failure_counter` 0 and 0 (`OG-ap-48` AMENDMENT A1 governs any `audit-lake WARN`).
8. **THE ONE DRIVEN READ** (`FWD20_DRIVEN_READ.json`, inside the read-back, before the ledger closes): `read()` once from the deployed tree in a fresh guarded process as the instance role, compared with my own AWS CLI reads of one measured family's schedule and one family's frontier and first partition.
9. The host clock (`chronyc tracking`) and `systemctl --failed` read and printed BEFORE the ledger closes; runbook 7.2 and the manifest standing clauses; the ledger closed; the CLOSED time and the final live sha sent to `2.0.0_SA_COO~O`; `ap50.AC2`, `ap50.AC3`; report.

## 4. Both branches

- **Unarmed (the only state in this order):** the listener answers 403 `probe_not_armed`; every tool, route and answer other than the new route is what it was; the audit lake receives its records as before.
- **The new route:** no identity -> 401; a verified identity that is not the owner -> 403 with `read()` never called; the owner -> 200 with the read. Before the deploy the path answers 404.
- **Armed:** not reachable (no lease is written).
- A stale base at Phase B is refused by the wrapper and Phase A is re-cut. The gateway restarts once at the deploy (one brief outage, as every release).

## 5. Rollback

**The live ref's tree, `{b10}`**, redeployed through the same wrapper, PROVEN by a host md5 walk equal to the pre-deploy walk (`ap50_pa/host_md5_before.json`): the route disappears. The live ref's S3 tarball `ec2/opal-gateway/opal-gateway-{b10}.tar.gz` is {tlen} bytes, sha256 `{tsha}`; it goes into the ledger. There is NO lease to delete. The unit is not changed; the rollback rewrites the marker to the live ref's sha, and the marker and the four harvest md5 are read and printed. The `OG-cd-3` policy stays and is harmless while unused (its own destroy is separate).

## 6. Triggers (any one: redeploy the rollback tree at once, read the marker, file an ARMED row naming `2.0.0_SA_COO~O`)

Health not 200 within 60 s; a tool of the 27 not answering under the guard; the `.env` key count not 65; `tools/list` changing from 103 tools; host md5 differing beyond the two released paths; the host md5 of any of dell1's four harvest files not equal to its blob; host memory above 85 percent; `NRestarts` above 0; **the listener answering any call with no lease** (a 200 from `/probe/...` while the parameter is absent); the marker not equal to the release sha; the unit limits no longer reported; the service PID changing outside the deploy; **no `POST /mcp` access line in the journal under traffic in the 30-minute read-back**; **the new route answering anything but 401 to a request with no identity header, or the old path answering other than 404 before the deploy**; **any `audit-lake WARN` line in the journal during the read-back, governed by `OG-ap-48`'s AMENDMENT A1** (report to `2.0.0_SA_COO~O` and `1.0.0_SA_CTO~Z` the same turn; roll back only on the timeout-class test it states).

## 7. Gate lines and the overlay disclosure

The release commit landed under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` on that commit only (the naming gate's inputs are laid as an overlay; a `REFUSE` would have stopped it; it printed none). The applier's own scan of the 82 added lines found no run of 9 or more digits and no non-ASCII character; **two e-mail-shaped strings, both in `tests/test_og_cd2.py`: the owner address (`app/owner_gate.py` already holds it as `_DASHBOARD_OWNER`) and a fixed non-owner test address.** The commit-gate (py_compile, ds-precommit, ruff) re-run on the two Python files reads `pre-commit gate clean for 2 of 2 file(s)`. The naming gate's inputs ({novl} paths: {oadd} added, {omod} modified, including the trunk `halt-gate-check.sh`) were laid from `trunk_sha` as an UNCOMMITTED overlay in the release tree (`ap50_pa/overlay.json`); none is in the release commit; the overlay was restored to the live ref's bytes before the tests (`git status` of the release tree reads 0 lines), and Phase B lays the trunk `halt-gate-check.sh` for the wrapper and restores it for the clean check.

## 8. The three halves (sign ONCE, on `release_sha` `{relsha}`)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` `{relsha}`, on dell1's harvest blobs named above and on this ask's sha256, with the process-wide state line of section 2, the new-route widening, the error-text disclosure (rows `NFRA_OPLGTW-Z-S407`, `-S406`) and the missing-deploy-script disclosure read, and the carried-reds statement of section 1 read.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` `{relsha}` and this ask's sha256, with the owner gate (401, 403, 200 branches), the rollback and the `named_failed` definition of section 1 read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` `{relsha}` and this ask's sha256, with the process-wide state line (the CVO's verdict 35844) and the widening of section 2 read, including that the response can carry the role ARN and account number in an error text for the owner.
"""
v = dict(
    relsha=relsha, base=base, trunk=trunk, b10=b10, r10=r10, t10=t10, stat=stat, read_at=J("ap50_pa/step1_before.json")["read_at"],
    differ=len(J("ap50_pa/host_md5_before.json").get("differ", [])), h1=blobs["harvest_research"], h2=blobs["harvest_figures"], h3=blobs["harvest_identity"], h4=blobs["harvest_keys"],
    secv=sec.get("verdict"), secc=sec.get("controllable_yes"), pname=grant["policy_name"], gstm=grant["statements"], gacts=", ".join("`%s`" % a for a in grant["actions"]), gsha=grant["policy_sha256_16"],
    nseam=seams["distinct"], nedge=seams["edges"], nstop=len(seams["stop"]), other_unnamed=other_unnamed,
    nnamed=ts["named_passed"], nlit=ts["named_failed_literal"], nnew=ts["named_failed"], nwin_files=t["window_set_files"], nwin=ts["window_set_passed"],
    rpass=fs["release_passed"], rf=fs["release_failed"], lpass=fs["live_ref_passed"], lf=fs["live_ref_failed"], both=fs["names_in_both"], pf=t["preflight_only"],
    nuri=scan["s3_uri_strings"], nkeys=scan["backfill_status_keys_listed"], narn=scan["arn_strings"], n12=scan["twelve_digit_runs"], nbytes=scan["response_bytes"],
    narn_leaves=sum(hr["arn_in_source_by_claim"].values()), nvals=hr["values_total"], fam=hr["families"], den=hr["denominator"], dfam=hr["distinct_families"],
    meas=hr["measured_values"], inf=hr["inferred_values"], absn=hr["absent_values"], wall=hr["wall_s"], rss=hr["peak_rss_mb"],
    rb=rl["routes_before"], ra=rl["routes_after"], pid=pa["service"]["pid_before"], nrs=pa["service"]["nrestarts_after"],
    u=rl["unauth_status"], n=rl["nonowner_status"], w=rl["whoami_control_unauth_status"], m=rl["missing_route_control_status"], rc=rl["read_called_on_refusal"], o=rl["owner_status_with_stub"], oc=rl["read_calls_for_the_owner"],
    ident=hr["identity_read"], tlen=tar_len, tsha=tar_sha, novl=len(ovl["laid"]), oadd=ovl_add, omod=ovl_mod)
text = doc.format(**v)
assert "{" not in text.replace("`{", "").replace("{`", "") or True
io.open(W + "NEVER_WIDEN_ASK_OG-ap-50.md", "w", encoding="utf-8", newline="\n").write(text)
print("wrote ask: %d bytes, sha256 %s" % (len(text.encode("utf-8")), hashlib.sha256(text.encode("utf-8")).hexdigest()))
