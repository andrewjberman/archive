# Never-widen sign-off packet -- r34m (version 2): the resident r34l -> r34m at pin 7f1eab530c (the packager attaches the package at READY; analysis_ready goes out for every ticketed request; the submission schema admits commentary_requested)

**Supersedes** `NEVER_WIDEN_PACKET_RESIDENT_R34M_PACKAGE_AT_READY_20261020.md` (blob `2d6caef529`, CTO half signed @029cf79c9d, tarball `d9be3cea...`, never uploaded). This version changes the artifact (one more member) and the blast radius (section 2); it needs its own CTO half.
**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** PRD IRPT_ANLREQ v0.24 O5 and C-PACKAGER; CTO msg 11099 (gate met: ~V2 msg 11163); CTO msgs 11198 and 11199 (add the schema; print the diffs of the three differing contract schemas; say why each other stays; counts of what died of this); Andrew's relayed word (CTO msgs 11152 and 11168).
**One move:** D1, the install of one new root on the resident host. Six members change: four code or contract members, the bindings' provenance and the package sums. No IAM, Lambda, queue, table, schema-of-data or vendor-call path moves.
**Orders:** BUILD-ONLY `org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-y-438.resident-release-r34m-rebuild-with-the-submission-schema-six-movers.md` (record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~317/r58/RESIDENT_R34M_BUILD2.json`, merged `b019fd26cbc`); the first build `TO-AR-y-430` (merged `7f498fe48ec`) is superseded. Code merges: AR-y-417 `a732c5ef25a`, AR-y-423 `a2008503d59`.

## 0. The defect this version adds the fix for (measured)

Run 5B's request (REQ-84ca4dff...) was refused by the RUNNING resident twice (02:34:11Z, 02:49:12Z) with `SubmissionRefused CLOSED_COMPOSITION_REQUIRED`; the job stayed RECEIVED. IB2's read `irpt_anlreq_composition_refusal/A_COMPOSITION_REFUSAL.txt` (commit `8935704b41`): the resident journal says `COMPOSITION-REFUSED step=2 error_class=ValidationError` (step 2 is the schema step) both times; the repository's validator at trunk ADMITS the retained composition; the resident's own copy of the v1 contract schemas (inside the r34l tarball, taken from the base pin `0485393f3a`, 2026-10-07) does not. The issuer validated the same retained composition against the schema set INSIDE the running r34l tarball: exactly one error, `additionalProperties` at `browser` (`commentary_requested` unexpected), because the running copy of `AnalysisSubmissionRequest.schema.json` (git blob `a7370fcd237`, sha256 `a6f224cd...`) has `additionalProperties: false` and lacks the optional boolean that trunk's copy (blob `92cc5673589`, sha256 `1052343f...`) carries since IB-pr-455 (`74bbdbb322`, 2026-10-11). Against the schema set inside the r34m tarball of this version: `SCHEMA-ADMITS errors=0` (`check_schema_admits.py`; the same check on the r34l tarball prints `SCHEMA-REFUSES errors=1 additionalProperties@browser`).

**Counts (CTO msg 11198).** (a) Since when the portal sent the field: candidate commits carry `commentary_requested` from 2026-10-14 (AR-y-317); on the PROD branch the merge `45a3e18f` (2026-10-15 14:01:21 -0400, 18:01:21Z) added it and the revert `e0b43076` (14:21:19 -0400, 18:21:19Z) removed it again, 20 minutes later; `origin/PROD` now has 0 occurrences in `src/pages/TicketCenter/analysisRequest.ts` (tip `ba2c34127915`); DEV has 1 (merge `7d5ba57ec6` today). Whether the PROD branch of those 20 minutes was deployed was not measured. (b) The dead-letter requests: 7 distinct requests (IB2 `A_DLQ_INVENTORY.txt`), all accepted between 2026-10-07 18:07Z and 2026-10-09 14:59Z, before the field existed in any schema (2026-10-11): 0 of 7 can carry it. (c) Andrew's ticket `TCK-20261017-5af976ff` (not read here): filed through the PROD page after 2026-10-15 18:21Z, which sends no such field: 0 of Andrew's tickets sent it. So the refusal has not killed any request that was on PROD; it blocks every filing from the page version this round ships.

## 1. What ships

Package pin `7f1eab530cde4661e9a559bf45439ebdbf73dab2` (the issuer's scratch branch `scratch/r34m-pin`: the r34l pin C `2a3aaa2815` plus ONLY the three O5 files at their trunk blobs); base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; the schema member is taken at the pin through the builder's `--override`. Built twice, byte-identical (317 of 317), by worker `0.9.0_WK_IRPT_ANLREQ~317`; the issuer re-hashed the tarball and compared it member by member with the running r34l tarball (`e1466cb8...`): **317 members, 311 identical, 6 changed**, 0 added, 0 removed; the four content members equal the pin's git blobs.

| member | vs r34l | what changes |
|---|---|---|
| `docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json` | changed (blob `92cc5673589`, was `a7370fcd237`) | +4 lines, 0 removed: one optional property `commentary_requested` (type boolean, the caller's own statement that commentary was asked for; absent is read as not asked). `additionalProperties` stays false. Nothing else in the file moves. |
| `ycharts/generate/resident_worker.py` | changed (blob `43d2996f0c2a`) | AR-y-417: `analysis_ready` goes out for every request whose accepted record carries a ticket id (was: only when `commentary_requested` was exactly True). AR-y-423: after that send, the READY worker (and a redelivered READY) calls the packager port; a failure is printed `retained_for_retry` and recorded as the PACKAGER hop; the READY state is never touched. |
| `ycharts/research/opal_packager.py` | changed (blob `5342bcad219c`) | AR-y-423: `handle_ready` attaches the package WITHOUT the commentary (`pdf_ref` and `commentary_ref` both null together); a 409 whose stored package is the null pair and whose new payload is full is replaced by ONE re-POST with `prior_attached_at`; never a downgrade of a full package; one null beside one set is refused (`PACKAGE_PARTIAL_PAIR`). |
| `reports/resident_installed.py` | changed (blob `8aed9e5b4cdd`) | AR-y-423: the packager is built before the assembly and its `ready_package` is handed to every worker; the failure mark is shared. |
| `reports/resident_bindings.json` | changed | `provenance.package_pin` and `provenance.member_overrides` (the one override: the schema member, naming the pin); no other key moves (verified). |
| `SHA256SUMS` | changed | the package sums, replaced (316 lines) |

**The three contract schemas that differ between the r34l tarball and the pin (CTO msg 11199), 3 of 25 direct v1 schemas:**
1. `AnalysisSubmissionRequest.schema.json`: the +4 lines above. **Carried**: `RequestComposition.schema.json` references it (and `AnalysisUploadResult.schema.json`, which is identical), and `CompositionAdmission` validates every submission against `RequestComposition`.
2. `ExportBundle.schema.json` (+86 / -1): contract revision 1.1 -> 1.2, an ADDITIVE `filled_report_source` branch (IB-pr-557, 2026-10-15) for the export of a filled report, with its `anyOf` exclusivity branch. **Stays at the r34l bytes**: `RequestComposition` does not reference it (transitive references of `RequestComposition`: `AnalysisSubmissionRequest`, `AnalysisUploadResult`, itself), the resident does not validate an export bundle on this path, and the change belongs to another project's release.
3. `HoldingsSnapshot.schema.json` (+9 / -0): the optional ACCOUNT-node property `account_id` (IB-pr-493) and `multi_asset` enum members. **Stays at the r34l bytes**: not referenced by `RequestComposition`; additive and owned by another project.
The other two files that differ at the repository level (`responses/...` schemas and `routes.json`) are not `*.schema.json` direct children and are not read by the composition check.

**Held back on purpose (the pin is the r34l pin C plus the three files):** `ycharts/research/opal_producer.py` and `ycharts/research/layout_overview.py` stay at their r34l blobs (trunk's versions carry ~G2's paused price-page work), `lib/trading_calendar.py` and `overview_map.json` stay at pin C's blobs; the 41 files of `files_from_r34.txt` differ between pin C and trunk in exactly five (these two and the three O5 files).
**The cross-reference check** (`check_r34m_xref.py`): `R34M-XREF-OK missing=0 names=79` on this tarball; with one name removed from a sibling copy it reads `missing=1`.

**Artifacts** (staged OUTSIDE the repository at `C:/dev/irpt-release-r35f`; nothing uploaded; r35e holds the superseded first build):
- Tar `irpt-resident-0485393f3a-r34m.tar.gz`: sha256 `00e1d165266bc5c1ad36cafcbd1cb91b7bef05b4138aa82383adcd200142ce0b`, 1,132,736 bytes, 317 members.
- Package sums `irpt-resident-0485393f3a-r34m.package.SHA256SUMS`: sha256 `d40022bec8d93aef3256c949e396a59e2c2bf6ea6a6a31ba0dd5f47ab4d8d569`.
- Host scripts (`scripts/`): `resident_host_install_0485393f3a-r34m.sh` `d38ec0be5fd3e182f2ce9b779110d007322cafcb2f9cb418044054e2d53523c1`; `install_r34.sh` `14539b59d7d7d0d6c6e060530541ecf4fdcac66cd04ad8b97c75e8b25ad6a394`; `pre_read_r34.sh` `713163f186c53d873bfd4d692014cb52010b70c86c83e7ea83bdc247c4f66c07`; `rollback_r34.sh` `ac1a4f1c72b36db23573e6fe92eda6a4b8445ddff4ffc14f2e5cd866db5420bb`.
- V2 script: ~G2's `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh` (sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`), run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34m`; its checks cover members r34m does not change.
- Everything else (the lease, the budget, the resolve hop, the tiers, the packager binding, the swap pool, the report document) is unchanged.

**Verification before this packet (issuer's own reads).** (a) Tarball sha256 recomputed, 317 members, delta against r34l = the six; the four content members equal the pin blobs; the bindings differ at `provenance.package_pin` and `provenance.member_overrides` only. (b) Import smoke `SMOKE live=82 imported=82 fail=0 note=0`. (c) Gate dry runs: gate1 unchanged 0 / one-byte 31; gate2 unchanged 0 / one-byte 33. (d) The retained run-5B composition: `SCHEMA-REFUSES` on r34l, `SCHEMA-ADMITS` on this tarball. (e) The tests of AR-y-417 and AR-y-423 ran on trunk at their merges; they were NOT re-run on the pin tree.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34l) | AFTER (r34m) |
|---|---|---|
| a submission whose body carries `commentary_requested` (the portal's DEV form, every run) | refused at the composition check, step 2; the job never starts | admitted; the job starts |
| a submission without the field | admitted | the same |
| a request with a ticket id reaches READY, `commentary_requested` True | one `analysis_ready` message; the package attaches only when the commentary is ready | the same message AND one package attach at READY without the commentary; the commentary path later replaces it with all four refs |
| the same, False or absent | NO message, NO package | one `analysis_ready` message on the existing queue (its one consumer is the commentary function: CTO half of the first packet, known limit 1, accepted) and one package attach without the commentary |
| the ticket service's answer | (not called at READY) | one POST with `pdf_ref` and `commentary_ref` both null (the live service admits the null pair, ~V2 msg 11163) |
| a READY retry or redelivery | no package call | the attach again: `ALREADY_ATTACHED` when the ticket carries it; never a downgrade |
| the commentary path | attaches the full package | the same; a stored null package is replaced through `prior_attached_at` (ONE re-POST) |
| every other route, role, table, key, queue, tier, budget | unchanged | unchanged |

**Who gains: no principal class.** The schema change lets a field that the contract already names in trunk through the resident's check; it adds no write path and grants no read. **Writers counted.** The package is written to the ticket by `opal_packager._attach` only; `analysis_ready` by `send_ready_if_ticketed` only. A packager error never changes the READY state or the report.
**Known limits (named, not stops).** (1) The READY package carries the null pair until the commentary arrives; the page reads that as "Commentary not available" (live). (2) The V2 script is r34k's. (3) The two other differing schemas stay stale in the resident until their own projects release them.

## 3. Apply protocol, in this order

1. **No YCharts call and no `~Y2` run during the install or V2.** Apply outside the weekday 11:30Z-14:15Z band and outside 05:45Z-07:00Z on Tuesday 2026-10-20; never alongside run 5C, the r37 apply or run 6 (the CTO's order of IB2 acts: 5C, r34m, r37, run 6).
2. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34m-20261020`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
3. **Send every host script AS ROOT.** Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34l`; the r34m root absent; the six changed members at their r34l values; the queue 0 0).
4. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
5. V1: running root `0485393f3a-r34m`; the 4 content members at their built blobs; the package sums 316 of 316 OK; the imports; queue 0/0; no sign-in in the journal; `opal_pricing` and `ycharts_window_budget` as r34l.
6. **V2, INSIDE the service's own environment:** `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34m` (verify its sha256 first). Anything but `V2S OK`: rollback.
7. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34l`, list the tickets that already carry a package attached without the commentary (ticket ids only), close the ledger ROLLED-BACK, report. No retry.
8. The ledger closes at V2. **Live proof is a separate act:** run 6 files an unseeded staff request and reads four pointers on the ticket after READY; a plain filing WITH `commentary_requested` is the first request the resident can admit with the field.

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` restores `0485393f3a-r34l`, which stays on the host. After a rollback the resident refuses `commentary_requested` submissions again (the state of today).
- **A package already attached without the commentary:** stays on its ticket; after a rollback r34l does not call the packager at READY, and its commentary path meets a stored null package and refuses the attach with a 409 (r34l has no replace). The CTO accepted this hazard; the tickets are listed the same session.
- **The lease row, the count row, queued messages:** unchanged by r34m; a message received after a rollback is served by r34l.

## 5. Not claimed

- That the live host, S3 objects, running root and receipt are as the build assumes (this is a build record; they were NOT read).
- That the V2 script exercises the changed members: it does not; V1 and the later runs do.
- That the tests of the two O5 changes pass on the pin tree (they ran on trunk at their merges).
- That nothing else in the base-pin contract set blocks a request (the retained composition is admitted; other documents were not tried).
- That four pointers appear on a real ticket end to end: run 6 proves it.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34m`); the receipt and its r34l copy; the unit's ExecStart; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
