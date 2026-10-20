# Never-widen sign-off packet -- r34n: the resident r34m -> r34n (the packager calls the ticket service through the portal's CloudFront alias; ONE binding value changes)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO msg 11292 (route the packager through the CloudFront route the portal uses; the authorizer is NOT changed; the origin secret is NOT handed to the resident; "if it is a binding: one resident release (r34n) changing only that value, under a pair I sign") and msg 11299 (order of acts: IAM grant, alias probe, r34n, run 7 under ADDENDUM 9). Grounding: PRD IRPT_ANLREQ v0.24 O5 and C-PACKAGER; IB2 `A_PACKAGER_403.txt` (the direct API host is refused by the authorizer with the origin-verification reason at 08:02:53Z and 08:58:06Z; the token is well formed, not expired, sub `svc-irpt-packager`, userType `service`).
**One move:** D1, the install of one new root on the resident host. TWO members change: `reports/resident_bindings.json` (the value of `packager.api_base`, nothing else) and `SHA256SUMS`. No code, IAM, Lambda, queue, table, schema or vendor-call path moves.
**Orders:** BUILD-ONLY `org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-y-450.resident-release-r34n-rebuild-with-the-packager-api-base-through-cloudfront.md` (record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~322/r60/RESIDENT_R34N_BUILD.json`, merged `aa966fb2b0c`, worker `0.9.0_WK_IRPT_ANLREQ~322`); the source read `TO-AR-y-449` (record `0.9.0_WK_IRPT_ANLREQ~321/A_EDGE_READ.txt`, merged `a307c42756c`).

## 1. What ships

The r34m version 2 tarball (running; sha256 `00e1d165266bc5c1ad36cafcbd1cb91b7bef05b4138aa82383adcd200142ce0b`) with the `packager` member of `reports/resident_bindings.json` changed from `{"api_base": "<the direct API Gateway host>", "secret_name": "opal/ticketing/svc-irpt-packager"}` to `{"api_base": "https://opalinvest.dev", "secret_name": "opal/ticketing/svc-irpt-packager"}`. The path the packager appends is unchanged (`/api/scoped/tickets/<id>/package`). Built through the builder's existing option `--packager api_base=URL,secret_name=NAME` (https required); built twice, byte-identical (317 of 317).

The issuer re-ran the three checks on the merged tree: `R34N-RECORD-OK changed=2 added=0 removed=0` (changed: `SHA256SUMS`, `reports/resident_bindings.json`); `R34N-IDENTITY-OK builds_identical=yes smoke_fail=0`; `PACKAGER-BASE-OK api_base=https://opalinvest.dev secret=opal/ticketing/svc-irpt-packager other_members_equal=yes` (315 of 315 other members byte-equal to r34m; the difference control prints `PACKAGER-BASE-BAD` with the old tarball on either side). The bindings diff is `keys_changed: [packager]`, `keys_added: []`. Import smoke `SMOKE live=82 imported=82 fail=0 note=0`; gate dry runs gate1 unchanged 0 / one-byte 31, gate2 unchanged 0 / one-byte 33.

**Artifacts** (staged OUTSIDE the repository at `C:/dev/irpt-release-r35h`; nothing uploaded; `r35g` holds the first, refused build attempt and is not used):
- Tar `irpt-resident-0485393f3a-r34n.tar.gz`: sha256 `89cad47247e6785e6b61e60112b04dfaa3cd2d5de88aef6023959692da76d899`, 1,132,727 bytes, 317 members.
- Package sums `irpt-resident-0485393f3a-r34n.package.SHA256SUMS`: sha256 `3356864c7bd53a73b13f4c355291ba062048fc0cc8e4d464d36652eaee23516a` (316 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34n.sh` `5e2415035b5c7505dbc93d23778d24b19f9bd2a63eb3b67daac84298a164e3a8`; `install_r34.sh` `7cef477a5e4729f9eac9a9c083612f7fefe424fac786340d5110a8ac6f2f1e2f`; `pre_read_r34.sh` `e7a7358ce41345129f142dcec3211af4572d6fc4a1062337a0a8c2e994ca880f`; `rollback_r34.sh` `67f2f85a385b562fb4e36fe1f28b84829a48f38685069e8b58d3236ba9870905`. They are the r34m version 2 scripts' method shifted one root: NEW `0485393f3a-r34n`, OLD `0485393f3a-r34m`; the member loops (no package member changes) are one `echo` line each, the member checks cover `SHA256SUMS` and the bindings.
- V2 script: `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh` (sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`), run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34n`.

## 2. Blast radius

| what | BEFORE (r34m) | AFTER (r34n) |
|---|---|---|
| the host the packager calls for the package POST | the direct API Gateway host: refused 403 by the authorizer (origin verification) | the portal's CloudFront alias: the request is made on the route the portal uses; the edge function's viewer check and the authorizer's token check apply; the authorizer is unchanged |
| the credential the packager presents | the packager secret's bearer token | the same secret and token; the origin secret is NOT given to the resident |
| a request that reaches READY / the commentary | the attach fails (`retained_for_retry`) | the attach is made through the alias; if the edge or authorizer still refuse, it fails the same way |
| every other binding, member, route, role, table, key, queue, tier, budget | unchanged | unchanged |

**Who gains: no principal class.** The resident host's outbound call goes to the portal's own public alias instead of the direct gateway host; the service principal and the entitlements are the same (the ticket Lambda still admits only `svc-irpt-packager`, firm-bound by `PACKAGE_ALLOWED_FIRMS`). **Writers counted:** the package is written to the ticket by `opal_packager._attach` only, as before. **Known limits.** (1) Whether the edge function and the authorizer admit the service token on this route is UNDECIDED from source (`A_EDGE_READ.txt` E4): the alias probe order `TO-READ-PACKAGER-CFPROBE` (cell AR-y-451) is the live proof and runs BEFORE this install. (2) The V2 script is r34k's and does not exercise the packager; run 7 does.

## 3. Apply protocol, in this order

1. **Precondition read:** the alias probe record `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_cfprobe/A_PACKAGER_CFPROBE.txt` at HEAD: its `A2` line must show the package POST through the alias passed the edge and the gateway (an answer from the ticket service such as not-found; NOT a 401 or 403) and its `T` line `iss=opal-portal-auth aud=opal-portal-api`. Any other reading: STOP, nothing installed, tell `2.0.0_SA_COO~Y2`.
2. **No YCharts call and no `~Y2` run during the install or V2.** Apply outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act.
3. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34n-20261020`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
4. **Send every host script AS ROOT.** Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34m`; the r34n root absent; the queue 0 0).
5. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
6. V1: running root `0485393f3a-r34n`; the package sums 316 of 316 OK; the bindings `packager.api_base` reads the alias host (closed word `alias`) and `secret_name` unchanged; the imports; queue 0/0; no sign-in in the journal.
7. **V2, INSIDE the service's own environment:** `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34n` (verify its sha256 first). Anything but `V2S OK`: rollback.
8. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34m`, close the ledger ROLLED-BACK, report. No retry.
9. The ledger closes at V2. **Live proof is a separate act:** run 7 (ADDENDUM 9) files through the portal page and reads four pointers on the ticket.

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` restores `0485393f3a-r34m`, which stays on the host. After a rollback the packager is back on the direct host and the attach is refused (the state of today).
- **A package already attached:** none can be attached through r34n before this install; one attached after it stays on its ticket and is unaffected by a rollback.
- **The lease row, the count row, queued messages:** unchanged by r34n.

## 5. Not claimed

- That the live host, S3 objects, running root and receipt are as the build assumes (this is a build record; they were NOT read).
- That the edge function and the authorizer admit the service token through the alias (the probe, step 1, decides; source says conditional on the token's `iss` and `aud`).
- That four pointers appear on a real ticket end to end: run 7 proves it.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34n`); the receipt and its r34m copy; the unit's ExecStart; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
