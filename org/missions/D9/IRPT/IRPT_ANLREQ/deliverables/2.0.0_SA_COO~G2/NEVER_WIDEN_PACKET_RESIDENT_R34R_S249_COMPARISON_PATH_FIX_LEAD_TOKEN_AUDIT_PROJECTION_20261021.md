# Never-widen sign-off packet -- r34r: the resident r34q -> r34r at pin 32bb8d5a67 (the S249 fix so a Multi-Comp filing gets past the first hop, the retained-line lead token, and the audit source's plain-name projection)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-21. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO msg 11890 (replay offline on r34q, fix with a failing-first test, and log the refusal's leading constant token in the same release) and msg 11899 (r34r is the RecipeRefused fix plus `ticket_audit_source.py`; the IAM side is unblocked). The defect: run 7I (Multi-Comp, row S249) passed admission on r34q and stopped at the next hop, `retained_for_retry class=RecipeRefused code=-` three times.
**One move:** D1, the install of one new root on the resident host. SIX members change against the running r34q and none is added or removed; no IAM, Lambda, queue, table, schema or vendor-call path moves, and the registry file and the `tickets_table` binding do not move.

## 1. What ships

Package pin `32bb8d5a673d3e0dd3c6efc933b7f0db5206533a`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34r_build.py` (`org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`, the r34q builder shifted one root), BUILD ONLY, by worker `0.9.0_WK_IRPT_ANLREQ~357` (order AR-g-184, merged `d2d353b7d79`, record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~357/r65/RESIDENT_R34R_BUILD.json`) over the RUNNING r34q root (tarball sha256 `f757171891f3924458123168abe2ccbba87d4b5bc12821cfa0f59b0f38b9266b`). **323 members**: 317 identical to r34q, **6 changed**, 0 added, 0 removed. The files-from list is 50 lines (r34q's 49 plus `frozen_worker.py`).

| member | vs r34q | what changes |
|---|---|---|
| `ycharts/generate/frozen_worker.py` | changed | `prepare(..., upload=True)`: with `upload=False` the vendor upload is not built and `upload` is None; the result gains `comparison_keys` (the browser's order). The default call is unchanged (AR-g-182) |
| `ycharts/generate/resident_worker.py` | changed | `_opal_comparables` calls `prepare(upload=False)` and builds `{key, label, ticker}` from the REAL catalogue entries (key = the catalogue key, label = the entry's name, ticker only for an ETF) (AR-g-182) |
| `ycharts/generate/resident_main.py` | changed | `retained_reason` appends `lead=<token>` (an upper-case code, or up to six whole lower-case words, no value) for classes ending in Refused or Attention; any other class prints as before (AR-g-183; CTO msg 11890 item 2) |
| `ycharts/generate/ticket_audit_source.py` | changed | the ticket read projects `ticket_id, ticket_type, answers, created_at` with plain names and no longer reads `filer_user_type` (2.0.0_SA_COO~Y2 AR-y-487, trunk 11fb915f82d) |
| `reports/resident_bindings.json` | changed | `provenance` only: `package_pin`, `files_from_count` (50), `files_from_sha256`; the release checker proves every other key equals r34q's, `tickets_table` `opal-tickets` included |
| `SHA256SUMS` | changed | the package sums, replaced (322 lines) |

Everything else r34q shipped stays: the admission fix (`submission.py`), the registry file with the ACTIVE audit revision, FWD-10 Core, the price pages.

**Artifacts** (staged outside the repository at `C:/dev/irpt-release-r34r-g2`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34r.tar.gz`: sha256 `77ec08f5a591de5584abb71787eb74c86bcbd3167416f2b411befc750140b828`, 1,154,204 bytes, 323 members.
- Package sums `irpt-resident-0485393f3a-r34r.package.SHA256SUMS`: sha256 `8ccd674239ac1f0044b668076bb2dda4f1e1ff0118dee75e7937c3b745681189` (322 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34r.sh` `0c7dd0932f56f34fc7a3b6ee0e7e192862397676fcc5ae85a79825da168f7b37`; `install_r34.sh` `d124f8e973e22b8b11cf2a3b50af3f72954647a6a94acedc9b00b8a3365ab29c`; `pre_read_r34.sh` `0a1fefe0b2c010bfe794af9a9e0d48b881f9177bc40f491f8630801936bed5fb`; `rollback_r34.sh` `b71f95d3f37e7f8c2bd6912961cb5dd351df51b562903fb39007274440d3c30b`.
- V2 script `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh`, sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`, run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34r`.

**Verification before this packet.** (a) The worker's build and the issuer's rehearsal at the same pin produced the SAME tarball sha256 (fixed clock); builds identical 323 of 323. (b) The issuer's checker `checks/ar_release_r_checks.py`, written before the build and calibrated (positive on the rehearsal; negative: it refuses the r34q tarball offered as r34r, with the delta empty, four movers not the pinned source, the bindings unmoved and the extracted frozen-read check failing), re-run by the issuer on the official stage after the merge: `AR-RELR-record-OK`, `AR-RELR-tree-OK`, `AR-RELR-scripts-OK`. (c) Import smoke: `SMOKE live=86 imported=86 fail=0 note=0`. (d) Gate dry runs: 0, 31, 0, 33.

## 2. The S249 evidence (the replays, run on the extracted tarballs' OWN modules)

Run 7I's retained synthetic composition (`checks/fixtures/composition_7i_synthetic.json`) replayed through `FrozenCompositionWorker.prepare`: **`RecipeRefused: holdings row has no provider receipt`** (the run's four holdings are public ETFs priced from history, security-check reason `YFINANCE_HISTORY`, no `provider_receipt`; `prepare` also builds the VENDOR upload, which an Opal job never uses). A second defect sits behind it: `_opal_comparables` read `key`, `label`, `ticker` off catalogue entries that carry `name`, `security_type`, `source_id`, `vendor_id` and no key, so every model would have reached the producer with key None.

| check (`checks/ar_prepare_checks.py`, `checks/ar_reason_checks.py`, run with `--root <extracted tarball>`) | r34q | r34r |
|---|---|---|
| `frozen`: the real `prepare` over stubs that serve 7I's bytes; the default call still refuses; `upload=False` returns `upload` None and the keys | `AR-PREP-frozen-FAIL` (no upload option) | `AR-PREP-frozen-OK` |
| `worker`: the real `_opal_comparables`; `upload=False`; one `{key,label,ticker}` per chosen key, model and ETF cases | `AR-PREP-worker-FAIL` | `AR-PREP-worker-OK` |
| `reason`: `retained_reason` over 14 fixed exceptions | `AR-REASON-reason-FAIL` (6 of 14 differ) | `AR-REASON-reason-OK` |

The checkers were calibrated against reference fixes and 11 mutants (each fails). The admission replay (`ar_admission_replay.py`) still reads `AR-ADMIT-OK`. My AR-g-175 tests had faked `frozen` with the wrong shape, which is why 7I met the defects first; the new tests use the real shape and each failed before the code change.

## 3. The registry and the retention rows

No registry movement: the registry file in r34r is byte-equal to r34q's (the checker compares every revision's state and `policy_sha256` to r34q's, and to r34n's with the one tolerated exception, `irpt-dashbd-x10-v1`, PENDING_ENFORCEMENT in both trees). IB2's census of 2026-10-21T03:46Z (msg 11845; 2524 items, 0 rows under the dashbd and audit revisions, 11 under `irpt-anlreq-x10-v1`) therefore stands; r34r changes no hash a row could carry.

## 4. Blast radius

| what | BEFORE (r34q) | AFTER (r34r) |
|---|---|---|
| a Comparison or Multi-Comp filing after admission | RecipeRefused at the comparison read (no READY) | the comparison read builds no vendor upload; the producer receives one `{key,label,ticker}` per chosen comparable (replay) |
| an Overview filing | live | live, unchanged |
| the journal line for a failed poll or package | `class=X code=-` for sentence messages | adds ` lead=<token>` for classes ending in Refused or Attention; no value is printed |
| the audit's ticket read | projection with attribute names | plain-name projection (the granted attribute-restricted read; IB2 closed the ticket-read policy apply at 05:03Z) |
| retention rows, registry, lease, budget, tiers, packager | r34q | unchanged |

**Writers counted.** Each changed member has ONE writer for this release (the builder), the source files three owners on trunk (AR-g-182, AR-g-183, AR-y-487), each merged and verified on the full tree.

## 5. Apply protocol, in this order

0. Preconditions the GO names: both halves signed on this file's blob; no filing and no other IB2 act open on the host; outside 11:30Z-14:15Z; the gateway restart window 06:00Z to 06:55Z is not touched.
1. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34r-20261021`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34q`; the r34r root absent; the library and wrapper unmoved; queue 0 0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
4. V1: running root `0485393f3a-r34r`; the member checks MATCH; the package sums 322 of 322 OK; a census of the two roots (exactly 6 files differ, none only in either); the bindings (`package_pin`, `files_from_count` 50, `tickets_table` `opal-tickets`, `opal_map` pin and the packager alias unchanged); the three policy hashes unchanged from r34q; the imports; queue 0/0; no sign-in.
5. V2 INSIDE the service's own environment: `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34r`. No YCharts call.
6. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34q`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2. **The live proof is a separate act** (run 7J, the Multi-Comp filing, new holdings), one filing, never alongside another IB2 act; it reports the packager outcome and the audit outcome by name.

## 6. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34q`, which stays on the host; `0485393f3a-r34p`, `r34o` and `r34n` also stay.
- **The receipt:** the r34q receipt is kept by the install and copied back.
- **Queued messages and audit objects:** none are touched; an audit record written under the audit prefix is an additive object and stays.

## 7. Not claimed

- That run 7J passes: it is the next act after the install. The replays prove the packaged modules over run 7I's retained bytes, not the live producer's reads of the two model objects, the pricing tiers or the PDF.
- That the audit record is written: the first filing's audit outcome is read by name, not assumed (the grant for the ticket read is live; the write path was never exercised).
- That the live host, S3 objects, the lease row, the running root and receipt are as the build assumes (this is a build record; the host was NOT read by this seat).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-21, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34r`); the receipt and its r34q copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 4; the rollback is section 6.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
