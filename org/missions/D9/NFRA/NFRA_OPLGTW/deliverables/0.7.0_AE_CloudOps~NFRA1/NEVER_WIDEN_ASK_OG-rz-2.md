# NEVER-WIDEN ASK -- `OG-rz-2` -- resize the gateway host from `t4g.small` to `t4g.large`, THEN one batched release (`OG-rz-1` memory limits, `OG-ms-1` Schwab master `08403355`)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rz-2.round-46-resize-the-gateway-host-to-t4g-large.md` (GO for Phase A: msgs 36088 and 36115, amendment A1). Phase A applies and deploys NOTHING.
Release: `release_sha` = `13917ef993` (branch `rel-nfra-oplgtw-batch15`, tree `C:/tmp/og-rel-batch15`), cut on the live ref `base_sha` = `6d1b5dcb64` (`OG-ap-50`'s release) from `trunk_sha` = `9095ce68f3`. Instance change: branch `rz2-instance-type-nfra1`, commit `62514569a6`, `main.tf` blob `1cf3c199cb2c`.
**The base is the live ref READ ON THE HOST** (`/opt/opal-gateway/.deployed_commit` reads `6d1b5dcb64`, read 2026-10-19T19:59:07Z) and the host's md5 walk equals it (0 differ, 0 missing, 0 extra: `rz2_pa/host_md5_before.json`).

## 1. The two acts, in THIS order (one ledger `nfra-oplgtw-gateway-resize-t4g-large`, legs `instance`, `release`, `read-back`)

1. **`instance`:** `infra/aws/terraform/opal-gateway/main.tf` line 172, `instance_type` `t4g.small` -> `t4g.large`, applied through `safe-apply` TARGETED at `aws_instance.gw`. The plan reads **`0 to add, 1 to change, 0 to destroy`, an in-place update, `replace` False** (`RZ2_PLAN.json`; the attribute is `instance_type`; `public_dns` and `public_ip` print as known after apply, which is Terraform's generic note for a stop/start; see section 4). AWS stops the instance, changes the type and starts it.
2. **`release`:** only AFTER the host reads `running`, `/health` 200 and the marker unchanged on the new size, ONE code release (section 2) deployed through `infra/aws/ec2/safe-ec2-deploy.sh` under the stale-base guard. **The limits must not be released before the resize:** `MemoryMax=6400M` on a 2 GiB host would invite the kernel OOM killer.

## 2. The diff, by file (`git diff 6d1b5dcb64 13917ef993`: 10 files changed, 158 insertions(+), 27 deletions(-))

Ten files taken whole from trunk, each byte-equal to trunk's blob (checked: 10 of 10), and for nine of them the live ref's file equals the file just before the worker's merge, so the whole-file take brings ONLY the worker's change; the tenth, `scopes.json`, is the one exception (section 3, point 6).
- `OG-rz-1` (merge `97ec4f8c60`): `deploy/opal-gateway.service`: `MemoryHigh` 1200M -> **5600M**, `MemoryMax` 1400M -> **6400M** (the comments updated: about 1792 MB of the 8 GiB host left to the system daemons); `tests/test_og_un1.py` (the test bounds); `deploy/NFRA_OPLGTW_CONTRACT.json`: `target_instance_type` `t4g.small` -> `t4g.large`.
- `OG-ms-1` (merge `9095ce68f3`; worker commit `0be402e218` plus the adapter amendment `a844325b8e`): Schwab master `08403355` ("TaxSMA", the "0840" account family) registered in `MASTERS` (`app/data_entitlement.py`), the audit set (`app/schwab_audit.py`), BOTH copies of the contract (`deploy/NFRA_OPLGTW_CONTRACT.json` and `org/standards/NFRA_OPLGTW_CONTRACT.json`, byte-equal to each other: the master name, the four `silver` data prefixes and the `meta/complete/` completion prefix), the naming registry copy `infra/logic/registry/scopes.json` (staged as `app/refs/scopes.json`), `app/client_adapter_schwab.py` (its own alias-master set, so the CLIENT tools keep refusing 0840), `tests/test_og_ms1.py` (new) and `tests/test_account_ref.py`.
- NOT in the release: `app/admin_api.py` and every other gateway file, `deploy-to-ec2.sh`, the unit file's other lines, `EC2_MANIFEST.json`, any Terraform in the release (the instance change is applied by `safe-apply`, not shipped).
- **Tests** (release tree and, beside it, a second tree at the live ref, both clean): the named files (`test_og_ms1`, `test_og_un1`, `test_account_ref`) pass 12 in both orders; the window set plus those three (23 files) passes 87 in both orders, 0 failed; the full suite fails the SAME 74 names in both trees (0 only in the release, 0 only at the live ref; release 1131 passed against 1126). `bash -n deploy-to-ec2.sh` clean and `--preflight-only` reads PREFLIGHT OK; the host-shaped import check imported 11 of 12 modules with zero reads (`server` needs the service environment, as in every record).

## 3. The widening, stated plainly

1. **The host gets four times the memory** (2 GiB to 8 GiB) and the service's cgroup limits rise to `MemoryHigh` 5600M and `MemoryMax` 6400M. A runaway request can now hold up to 6.4 GB before the kernel kills the service (it was 1.4 GB); about 1.8 GB stay for the daemons. It costs more per hour (the larger instance type).
2. **Downtime:** the gateway is DOWN for every user for the whole stop/start (section 5), and restarts once more at the release.
3. **A new Schwab master, `08403355`, becomes known to the gateway.** Registering it changes NO grant: a grant names its masters explicitly, so no principal can read this master until a grant names it (`OG-ms-2`, a separate order and halves, adds it to one grant). What the registration does: `parse_scope` accepts the master in a grant; the catalog and the audit set know it; the contract's data prefixes include its four `silver` tables and its completion markers.
4. **Measured on the master (read-only):** `08403355` is the ONLY `0840` prefix under `schwab/`; its four `silver` datasets each hold an object at the latest complete date (2026-10-16); the completion markers number 764. **The live reader-role read** (`simulate-principal-policy`): `gateway-schwab-read-role` is ALLOWED `GetObject` and `ListBucket` on the master's `silver/dim_balance/` and is `explicitDeny` on `meta/complete/` by design; `gateway-schwab-catalog-read-role` is ALLOWED on `meta/complete/` and `explicitDeny` on `silver/` by design. The existing master `08335338` reads identically. **No IAM change is needed.**
5. **The CLIENT tools keep refusing 0840** (the adapter's own `_ALIAS_MASTERS`); the Schwab data tools take a master only from a grant.
6. **`scopes.json` brings three other seats' registry hunks with it.** The staged registry copy is byte-equal to `infra/logic/registry/scopes.json` (`client_core.py` says so), so it is taken whole from trunk. Of its five hunks live-to-trunk, two are `OG-ms-1`'s (the master row and the master list); the other three are other seats' registry commits: a new FIRM row `alongside` (the Fidelity domain, `bucket_provisioned` false, so inert) and `alongside` added to two `separated_from` lists. They add registry rows the client firm lookup can read; nothing is granted. The alternative (apply only the two `OG-ms-1` hunks to the live bytes) would make the staged copy differ from the repo's, so I did not choose it; **the halves may choose it instead**, and the release is then re-cut.
7. `lib/opal_naming.py` differs between the live ref and trunk (a small change) and the deploy stages it from the release tree; **this release does not take it**, so the host keeps the live ref's naming module with the newer registry. The registry shapes in the three extra hunks already exist in other rows, and the tests above pass with that pair.

## 4. The public address

**An Elastic IP is attached** to the instance (`describe-addresses`), so the public address does NOT change on stop/start (`RZ2_BEFORE.json`: `eip_attached` True, `public_ip_changes_on_stop_start` False). Terraform's "known after apply" for the address is its generic note. Estate residual (counts and names only): 19 surfaces name the egress address, all repo files (records and inboxes), **0 security-group rules and 0 WAF IP sets**. A VENDOR-SIDE allowlist (a vendor that admits only a listed source address) cannot be read from here: **NOT CLAIMED**. Because the address is unchanged, that residual only matters if the association were lost; Phase B reads `describe-addresses` again after the start.

## 5. Downtime and the window

The gateway is DOWN for every user during the stop/start; the other boxes and sessions must be told the window. The duration is **UNKNOWN**: no stop/start of this instance is on record (the host reads up 31 days); Phase B measures it (first failed health read to first 200). **Proposed window: 2026-10-20 from 06:00Z to 06:45Z** (02:00 to 02:45 ET, off-hours; Alyssa's session was 19:00Z today), `0.0.0_AB_MSTR~Z` told in one message before the stop. The issuer sets the window.

## 6. The order of acts (Phase B)

1. Open the ledger (entry AND sentinel); re-read the live ref (`6d1b5dcb64`; any other value is a STOP and a re-cut), the unit limits (1200M and 1400M), target health, the `.env` (65 keys) and the host md5; any change since Phase A re-cuts Phase A once. Tell `0.0.0_AB_MSTR~Z` the window.
2. `instance` leg: `safe-apply` targeted; read `describe-instances` until `running` and the target group healthy; `describe-addresses` still associated; the downtime in seconds.
3. `release` leg: re-read the marker and `/health`; restore the gate overlay; deploy `C:/tmp/og-rel-batch15` through the wrapper with `DEPLOY_BASE_REF=6d1b5dcb64`; the service restarts once; read back against the triggers.
4. 30-minute read-back, UNARMED ONLY: `/health` 200; marker equals the release; host memory total at least 7,000 MB; the unit's live limits 5600M and 6400M; `tools/list` 103; 27 of 27 under the hard guard; `NRestarts` 0 after the deploy's own restart; **the large-reply test, ONE call at a time, never concurrent:** `mdpf_get_aggregate_aua` (about 743 KB) and `opal_discover` (about 585 KB) each complete, with `MemoryCurrent` before and after each recorded as counts and the peak below `MemoryHigh`; the dual count (journal `POST /mcp` lines against audit-lake records over ONE window); `audit_failure_counter` 0. Then `RZ2_SERVED.json`, the clock and failed units BEFORE the close, the ledger closed.

## 7. Rollback, in the SAFE order

**FIRST redeploy the live ref's tarball** (`opal-gateway-6d1b5dcb64b.tar.gz`, 922315 bytes, sha256 `e7cd9de1617a`, in the ledger) through the wrapper, so the limits return to 1200M and 1400M; **THEN** apply `t4g.small` (revert the `main.tf` line, targeted `safe-apply`). The reverse order would put `MemoryMax=6400M` on a 2 GiB host. **One more dependency:** if `OG-ms-2` has already added `08403355` to a grant, rolling the release back makes the older code reject that grant, so that grant is reverted FIRST (a tombstone revoke of the new revision, never a delete) before the tarball is redeployed. There is no lease to delete.

## 8. Triggers (any one: stop, and roll back in the order of section 7)

The plan reads anything other than `0 to add, 1 to change, 0 to destroy` at the apply, or names a replacement; the instance not `running` within 10 minutes of the apply; the target group not healthy 5 minutes after `running`; the Elastic IP no longer associated; health not 200 within 60 s of the deploy's restart; the marker not equal to the release; the unit limits not 5600M and 6400M; host memory total below 7,000 MB; `tools/list` not 103; a tool of the 27 not answering under the guard; the `.env` key count not 65; host md5 differing beyond the ten released paths; `NRestarts` above 0 after the deploy's own restart; either large reply failing or the peak reaching `MemoryHigh`; no `POST /mcp` access line under traffic in the 30-minute read-back; any `audit-lake WARN` line, governed by `OG-ap-48`'s AMENDMENT A1.

## 9. process-wide state this change touches: the host instance type and memory (stop/start), the service's cgroup limits `MemoryHigh` and `MemoryMax` (the unit file), the staged registry copy `app/refs/scopes.json`, and the Schwab master registry (`MASTERS`, the audit set, the contract); two service restarts (the stop/start and the release); nothing else, read

I read the unit file diff, the contract diff, `app/data_entitlement.py` and `app/schwab_audit.py` diffs, `main.tf` line 172 and the plan. No logger, handler, signal, environment key or listener is added; no arming and no SSM parameter write; no IAM, security group, load balancer, listener or Elastic IP change.

## 10. Gate lines and the overlay disclosure

The release commit landed under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` on that commit only (the naming gate's inputs are laid as an UNCOMMITTED overlay; a `REFUSE` would have stopped it; it printed none). The overlay (274 paths: 257 added, 17 modified: `rz2_pa/overlay.json`) was restored to the release's own bytes (not the live ref's, because the release deliberately changes `scopes.json`) and the release tree's `git status` reads 0 lines. The IAM simulation as the identity that applies (`RZ2_IAM.json`): `ec2:StopInstances`, `ec2:StartInstances`, `ec2:ModifyInstanceAttribute` and `ec2:DescribeInstances` all allowed. The instance edit sits on its own branch, not on `box/sitez`, so an untargeted apply of this root by another seat cannot resize the live gateway before the signed window.

## 11. The three halves (sign ONCE, on `release_sha` `13917ef993`, the `main.tf` blob `1cf3c199cb2c` and this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

Sign or refuse on sections 1 to 5, the `scopes.json` choice of section 3 point 6, the window of section 5 and the process-wide state line of section 9.

### COO half (`2.0.0_SA_COO~O`)

Sign or refuse on the same, the rollback order and its `OG-ms-2` dependency (section 7) and the triggers (section 8); the issuer sets the window.

### CVO half (`3.0.0_SA_CVO~Z`)

Sign or refuse on the same, including that the raised limits are released only after the resize, that the registered master grants no one access by itself, and that three other seats' registry hunks ride in `scopes.json`.
