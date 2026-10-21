# Never-widen sign-off packet -- r34q: the resident r34p -> r34q at pin 21cb4e857d (the S245 admission fix so Comparison and Multi-Comp filings pass the replay, the tickets_table binding, and the registry with the NEW ACTIVE revision irpt-anlreq-audit-x10-v1)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-21. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** the CTO's reply to my msg 11789 (r34q carries `submission.py`, 02:55Z), msg 11639 (a revision that has rows is never edited; the audit family returns as a NEW revision; the packet carries a measured census), msg 11843 (ship with the dashbd move tolerated; the packet carries the shipped dashbd state, the census of both revisions, and the checker rule). The defect: run 7H (Multi-Comp, row S245) stopped at P1 on r34p with `CLOSED_COMPOSITION_REQUIRED` because the resident replays the frozen composition through `CompositionAdmission`, step 3 calls `validate_public_request`, and the packaged `ycharts/generate/submission.py` (the base pin's) does not list `commentary_requested`.
**One move:** D1, the install of one new root on the resident host. SEVEN members change against the running r34p and none is added or removed; no IAM, Lambda, queue, table, schema or vendor-call path moves.

## 1. What ships

Package pin `21cb4e857df85da3e0d3e14c83cb4c78c9a94b83`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34q_build.py` (`org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`, the r34p builder shifted one root, plus `--tickets-table` on my release builder), BUILD ONLY, by worker `0.9.0_WK_IRPT_ANLREQ~354` (order AR-g-181, merged `535aead683f`, record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~354/r64/RESIDENT_R34Q_BUILD.json`) over the RUNNING r34p root (tarball sha256 `4991c7bcba0f01cb47b06bfa8c4e30f3fe47a6cbd6e9b9f479d1d39b77b49ea4`). **323 members**: 316 identical to r34p, **7 changed**, 0 added, 0 removed. The files-from list is 49 lines.

| member | vs r34p | what changes |
|---|---|---|
| `ycharts/generate/submission.py` | changed | trunk's copy at the pin (PUBLIC_FIELDS lists `commentary_requested`): the S245 fix |
| `infra/logic/registry/reporting_policies.json` | changed | trunk's registry at the pin: adds the revision `irpt-anlreq-audit-x10-v1` (ACTIVE, enforcement_ref `e3788d3f8a359b0253f45137f8ff3b1cfa075c2d`, 2.0.0_SA_COO~Y2 AR-y-485); `irpt-anlreq-x10-v1` keeps its r34n hash `8edbe84b05765c36`; `irpt-dashbd-x10-v1` carries IRPT_BCKEND's FILLED_REPORT family (df2468cbc8f, state PENDING_ENFORCEMENT) |
| `reports/analysis_audit.py` | changed | the audit module at the pin (Y2 AR-y-473/483) |
| `reports/resident_installed.py` | changed | reads the optional binding `tickets_table` and wires the audit ports when set (Y2 AR-y-483/484); unset leaves the ports unwired |
| `reports/build_resident_package.py` | changed | the lambda tree's builder copy at the pin (Y2 AR-y-484; a different file from my release builder) |
| `reports/resident_bindings.json` | changed | adds `tickets_table` = `opal-tickets`; `provenance` moves (`package_pin`, `files_from_count` 49, `files_from_sha256`); the release checker proves every other key equals r34p's (`opal_map` pin, packager, tiers, budget) |
| `SHA256SUMS` | changed | the package sums, replaced (322 lines) |

Everything else r34p shipped stays: FWD-10 Core (comparison section, model reader), the Overview price pages, the retention behaviour of r34n.

**Artifacts** (staged outside the repository at `C:/dev/irpt-release-r34q-g2`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34q.tar.gz`: sha256 `f757171891f3924458123168abe2ccbba87d4b5bc12821cfa0f59b0f38b9266b`, 1,153,401 bytes, 323 members.
- Package sums `irpt-resident-0485393f3a-r34q.package.SHA256SUMS`: sha256 `81fe6d38d3c9f69b838406a95c1c1947252428b681389f48507ca8f0507edc73` (322 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34q.sh` `62e59a1371ee4e263f1d4fee0ab52294ae04a30c9daec3f194f613371a27bc2d`; `install_r34.sh` `49e86cf98f88641f57736a23beffa138828bd58fb1b928da98029ea360c42ff7`; `pre_read_r34.sh` `1bc51f491ed3689c3182ca068e4b5fd94b6f3caacc117c221e6a90af927eec72`; `rollback_r34.sh` `2ac568e6517ad33c95581c676af87bad9443cb52c45739054344c7280813e026`.
- V2 script `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh`, sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`, run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34q`.

**Verification before this packet.** (a) The worker's build and the issuer's rehearsal at the same pin produced the SAME tarball sha256 (fixed clock); builds identical 323 of 323. (b) The issuer's checker `checks/ar_release_q_checks.py`, written before the build and calibrated (positive on the rehearsal; negative: it refuses the r34p tarball offered as r34q, with the delta empty, five movers not the pinned source, the bindings unmoved, the audit revision absent and the admission replay failing at step 3), re-run by the issuer on the official stage after the merge: `AR-RELQ-record-OK`, `AR-RELQ-tree-OK`, `AR-RELQ-scripts-OK`. (c) Import smoke: `SMOKE live=86 imported=86 fail=0 note=0`. (d) Gate dry runs: 0, 31, 0, 33.

## 2. The S245 evidence (the admission replay)

`checks/ar_admission_replay.py` replays the five steps of `CompositionAdmission.validate` (canonical, schema, compose, bindings, portfolio) on run 7H's retained synthetic composition (`checks/fixtures/composition_7h_synthetic.json`) through a tarball's OWN modules in a fresh interpreter. **r34o and r34p tarballs: `AR-ADMIT-FAIL step=3 ... CLOSED_COMPOSITION_REQUIRED`. The r34q tarball: `AR-ADMIT-OK`** (also the r34p tarball with trunk's `submission.py` swapped in). Overview filings never call admission (the Opal Overview path does not), which is why run 7F passed on r34p; Comparison and Multi-Comp reach it through `self.frozen.prepare()`.

## 3. The shipped registry and the census (CTO msg 11843)

**(1) The shipped file's revision states**, read from the r34q tarball with its own `lib/opal_naming.reporting_policy()` in a fresh `-I` interpreter:

| revision | state | policy_sha256 (first 16) | vs r34n/r34p |
|---|---|---|---|
| `irpt-anlreq-x10-v1` | ACTIVE | `8edbe84b05765c36` | equal |
| `irpt-dashbd-x10-v1` | **PENDING_ENFORCEMENT** | `244a20425ba40cde` | moved (r34n: `301c58e24ff0feda`); IRPT_BCKEND's FILLED_REPORT family |
| `irpt-anlreq-audit-x10-v1` | ACTIVE | `2b4f91d3feda649b` | new |

While the dashbd revision is PENDING_ENFORCEMENT, `retention.py:61-63` refuses every reserve, so no row can carry its hash.

**(2) The IB2 census** (read only, 2026-10-21T03:46Z, order `IRPT_ANLREQ.TO-READ-RETENTION-CENSUS-R34Q`, msg 11845, record `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_retention_census_r34q/A_CENSUS_R34Q.txt`): table `irpt-requests`, paginated scan to the end, **2524 items scanned**, 721 retention rows. Rows under `irpt-dashbd-x10-v1`: `301c58e24ff0feda` **0**, `244a20425ba40cde` **0**. Rows under `irpt-anlreq-audit-x10-v1` `2b4f91d3feda649b`: **0**. Any other hash under these two revisions: **0**; any other spelling of a revision containing audit or dashbd: **0**. Control `irpt-anlreq-x10-v1` `8edbe84b05765c36`: 11 rows (10 at the r34p census plus one reserved since), and its hash is unchanged in r34q, so all 11 stay valid.

**(3) The checker's rule as built** (`r34q_build.py` and `ar_release_q_checks.py`): every revision r34n carried must keep its `policy_sha256` in the packaged registry, with ONE tolerated exception, `irpt-dashbd-x10-v1`, and only while its state reads PENDING_ENFORCEMENT in both trees; a moved ACTIVE revision, or any other moved revision, fails. `irpt-anlreq-audit-x10-v1` must be the only addition and ACTIVE. The release printed `NOTE registry revisions moved but tolerated: ['irpt-dashbd-x10-v1']`.

## 4. Blast radius

| what | BEFORE (r34p) | AFTER (r34q) |
|---|---|---|
| a Comparison or Multi-Comp filing at the resident's admission replay | refused at step 3 (CLOSED_COMPOSITION_REQUIRED) | passes the five steps (replay on run 7H's composition) |
| an Overview filing | live | live, unchanged |
| the audit record | ports unwired (`IRPT_TICKETS_TABLE` unset on the host; address refused by name) | wired through the binding `tickets_table` = `opal-tickets`; the audit address resolves; writes go to `opal-data-irpt` under `irpt/<firm>/platinum/analysis_audit/` (the resident role holds `irpt-audit-write-policy`, applied by IB2, closed 2026-10-21T03:03Z) |
| the 11 existing retention rows of `irpt-anlreq-x10-v1` | valid | valid (hash unchanged) |
| rows under the dashbd and audit revisions | none | none (census) |
| lease, budget, tiers, packager `api_base`, producer list | r34p | unchanged |

**Writers counted.** Each changed member has ONE writer for this release (the builder). The registry file's three revisions are written by three owners on trunk (IRPT_ANLREQ x10, IRPT_BCKEND dashbd, IRPT_ANLREQ audit); the release copies the file and does not edit it.

## 5. Apply protocol, in this order

0. Preconditions the GO names: both halves signed on this file's blob; no filing and no other IB2 act open on the host; the gateway restart window 06:00Z to 06:55Z is not touched.
1. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34q-20261021`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34p`; the r34q root absent; the library and wrapper unmoved; queue 0 0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
4. V1: running root `0485393f3a-r34q`; the registry member MATCH; the package sums 322 of 322 OK; a census of the two roots (exactly 7 files differ, none only in either); the bindings (`package_pin`, `files_from_count` 49, `tickets_table` `opal-tickets`, the `opal_map` pin and the packager alias unchanged); the three policy hashes above printed on the host; the imports; queue 0/0; no sign-in.
5. V2 INSIDE the service's own environment: `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34q`. No YCharts call.
6. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34p`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2. **The live proof is a separate act** (run 7I, the Multi-Comp filing), one filing, never alongside another IB2 act.

## 6. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34p`, which stays on the host; `0485393f3a-r34o` and `0485393f3a-r34n` also stay.
- **The receipt:** the r34p receipt is kept by the install and copied back.
- **Queued messages and audit objects:** none are touched; an audit record written under the audit prefix is an additive object and stays.

## 7. Not claimed

- That run 7I passes: it is the next act after the install. The admission replay proves the packaged modules, not the live bindings, queue or host.
- That the resident role can read the `opal-tickets` table: not measured by this seat; a failed audit read or put is recorded as an audit refusal and the attach stands (as for r34p), so the first filing's audit outcome is read, not assumed.
- That the dashbd revision stays PENDING_ENFORCEMENT: when its owner flips it ACTIVE, rows can start to carry its hash and a resident whose registry differs is refused; the flip then needs its own release and census.
- That the live host, S3 objects, the lease row, the running root and receipt are as the build assumes (this is a build record plus a read-only census; the host was NOT read by this seat).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-21, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34q`); the receipt and its r34p copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 4; the rollback is section 6.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
