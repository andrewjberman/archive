# Never-widen sign-off packet -- r34t: the resident r34s -> r34t at pin c17477bc32 (typed ETF as a priced comparable, each model's own date, the left-out line, the Risk Info tables, the C-SWAP model leg)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-21. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO msgs 11977 and 11980 (the FWD-10 enrichment: a typed ETF reaches the comparison stage; page 60 prints each model's own as-of date; a kept row left out of the figures is named on the page; page 21's Risk Info tables are fixed; all in r34t) and the other COO's C-SWAP model leg (rulings msgs 11456 and following; trunk `3dac9960e2b`, release needs `deliverables/2.0.0_SA_COO~Y2/swap_leg/SWAP_LEG_RELEASE_NEEDS_20261021.md`).
**One move:** D1, the install of one new root on the resident host. NINE members change against the running r34s and TWO are added, none removed; no IAM, Lambda, queue, table, schema or registry moves. One new OPTIONAL binding `opal_swap_model` ships `{"enabled": true}`, and the files-from list gains one line (51).

## 1. What ships

Package pin `c17477bc32023d5e02776460d1814e138e9ddf65`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34t_build.py` (`org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`, the r34s builder shifted one root), BUILD ONLY, by worker `0.9.0_WK_IRPT_ANLREQ~384` (order AR-g-194, merged `732397f507`, record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~384/r67/RESIDENT_R34T_BUILD.json`) over the RUNNING r34s root (tarball sha256 `fa950681774268d2108eb7ca141ec150213d0d6e482dad498d13870a90d87b14`). **325 members**: 314 identical to r34s, **9 changed**, **2 added**, 0 removed.

| member | vs r34s | what changes |
|---|---|---|
| `ycharts/generate/resident_worker.py` | changed | `_opal_comparables`: a typed ETF's ticker is the catalogue key (the door drops the entry's `key`, so the ticker was null and the ETF an empty line; measured offline) (AR-g-189) |
| `ycharts/research/model_source.py` | changed | `read_allocation` also returns each model's own `data_as_of` (`as_of_by_code`, fallback to the file's date, a malformed one refused); the file-level `as_of` is unchanged (AR-g-190) |
| `ycharts/research/opal_producer.py` | changed | the allocation rows take each model's own date (AR-g-190); the swap stage composes an optional model classify and a proposals port behind the store keys (AR-y-494) |
| `ycharts/research/layout_overview.py` | changed | one line `Left out of all figures: <ticker>, <reason>.` on the Top 10 Holdings page for each kept holding the swap pass left out (AR-g-191); the Overview's six Risk Info tables (Alpha, Beta, Sharpe, Sortino, Max Drawdown, Monthly VaR) print as tables (AR-g-192) |
| `ycharts/research/swap_pass.py` | changed | the `proposals` port and the model-classification fields in the swap record (AR-y-492) |
| `reports/resident_installed.py` | changed | the optional binding `opal_swap_model` (exactly `{"enabled": bool}`, else `SWAP_MODEL_BINDING_INVALID`); when enabled and the swap-pool binding is present, the swap store gains the model classify and proposals ports built over the resident's secrets client; enabled without a secrets client refuses at install (AR-y-494) |
| `reports/build_resident_package.py` | changed | the bindings dict carries `opal_swap_model` (a package member; not executed on the host) |
| `reports/resident_bindings.json` | changed | adds `opal_swap_model` `{"enabled": true}`; provenance (`package_pin`, `files_from_count` 51, `files_from_sha256`, `members_added`); every other key equals r34s's |
| `SHA256SUMS` | changed | the package sums, replaced (324 lines) |
| `ycharts/research/swap_model.py` | ADDED | the model adapter (AR-y-493): classifies a held symbol the classifier lacks, inside the pool's vocabulary, and proposes same-class tickers; opens no connection, reads no secret itself |
| `etf_classification_model.py` | ADDED | at the package ROOT, the classifier module `swap_model` imports by bare name (from `v2_portal/_shared`) |

Everything else r34s shipped stays: the portfolio path, the presentation fixes, the admission and comparison-read fixes, the registry and bindings.

**Artifacts** (staged outside the repository at `C:/dev/irpt-release-r34t-g2`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34t.tar.gz`: sha256 `35a4f044c2bcae4d567c57132b833c101ab1872d9880bafd45cb0a4afe6af21d`, 1,166,418 bytes, 325 members.
- Package sums `irpt-resident-0485393f3a-r34t.package.SHA256SUMS`: sha256 `3bb68876ab589aeef1899d6617c1299949a0469b1a710012130c049d8ed67e39` (324 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34t.sh` `cbf6ac60dfea7dfbd0aa0122cf86d9c16b7db17c0d5dc45f15b6cd8e30dceae1`; `install_r34.sh` `35ed22127f95f07cf0d5c46450a05cd1356784928c17bb7c5f5ac4494d7be0bf`; `pre_read_r34.sh` `fa34f0b7f37ecd678a35e92a035be9c2313ab89df2a4397d9b60031cfb5629a9`; `rollback_r34.sh` `40116cb93551fc2a011c07eb5b532b5d59ec795c80623394c9018f36745a50ea`.
- V2 script `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh`, sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`, run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34t`.

**Verification before this packet.** (a) The worker's build and the issuer's rehearsal at the previous pin produced a tarball whose members differ from it only in `reports/resident_bindings.json` (the package pin) and `SHA256SUMS` (which sums that file) (the rehearsal ran at pin d458b8111e, sha256 `fcc15e8cef51...`, the official build at pin c17477bc32; the issuer compared the two trees member by member). (b) The issuer's checker `checks/ar_release_t_checks.py`, written before the build and calibrated (positive on the rehearsal; negative: it refuses the r34s tarball offered as r34t and a record missing a mover), re-run by the issuer on the official stage after the merge: `AR-RELS-record-OK`, `AR-RELS-tree-OK`, `AR-RELS-scripts-OK`. (c) Import smoke: `SMOKE live=87 imported=87 fail=0 note=0`. (d) Gate dry runs: 0, 31, 0, 33. (e) The cells' own gates, run by the issuer on the full tree after the merges: `ar_enrich_checks.py` etfkey OK, asof OK, tests189 7, tests190 75; `ar_enrich2_checks.py` excl OK, p21 OK, tests191 10, tests192 61; the instrument for run 7M offline OK; and the drain run of `ycharts/research/tests`, `test_resident_main.py`, `test_frozen_worker.py` and `test_compare_ports.py`: 804 passed. The other COO re-ran its swap-leg criteria (67, 11 and 64 tests; every check's mutants fire).

## 2. The evidence for each change

- **Typed ETF (measured).** `etf_typed_measure.py` runs the tree's REAL door (`resolve_comparison_fields`, a classification table naming VNQ) and the exact `_opal_comparables` mapping: the retained entry has no `key`, the ticker is null, and `_compare_stage` takes the empty "other" branch (`ETF_TYPED_PATH_MEASUREMENT_20261021.md`). After the fix the same real door gives ticker `VNQ`, the REAL producer charts the ETF from the held readers and reports it 100 percent in its class. The checker was calibrated against the reference fix and mutants.
- **Per-model dates.** The positioning object carries `data_as_of` per model (Short-Term 2026-10-08, Long-Term 2026-08-18) beside the file's 2026-10-19; page 60 printed the file's date for every model (run 7K read).
- **Left-out line and Risk Info tables.** Run 7L (an Overview with the unknown ZQXWVK kept) was READY and the report did not name the left-out row; the Overview map's six Risk Info table elements name both columns and a statistic, the producer took the scalar path, and a scalar printed "The kept answer is not a readable table." (reproduced offline with the real map; five of six on a ten-year synthetic history, six on run 7L). Both fixed failing-first with the REAL producer on the REAL maps.
- **C-SWAP model leg** (the other COO's cells, offline-proved): see its release-needs file for the vendor path.

## 3. Blast radius

| what | BEFORE (r34s) | AFTER (r34t) |
|---|---|---|
| a Multi-Comp with a typed ETF | an empty line, nothing priced | the ETF priced through the holdings' tiers (estate, yfinance, then YCharts as the last tier), classified, in the chart, returns, risk and allocation tables |
| page 60 allocation rows | every model "as of" the file's date | each model's own date |
| an Overview or Multi-Comp with a kept unknown holding | silent | one line naming the ticker and the reason, no amount |
| the Overview's page 21 | six "not a readable table" lines | tables with a row per period |
| an UNRESOLVED holding the classifier lacks | left out, named `NOT_ANALYSED` | **NEW: the Kimi model (`kimi-k3`, Moonshot, `POST api.moonshot.ai/v1/chat/completions`, no tools key so no web search) is asked for a class from the pool's vocabulary, and a proposals call widens the pool; every candidate is class-checked and Yahoo-priced and the longest history wins; below 0.80 confidence the swap record flags `low_confidence`; an answer outside the vocabulary is refused (the holding stays left out)**. Only the held symbol and the class pair are sent, never a firm, amount or account. |
| IAM, queues, tables, schema, registry | r34s | unchanged: the resident role already reads the estate Kimi key (`resident.tf` Sid `ReadTheEstateKimiKey`; simulated `allowed` 10:19Z by the other COO); the model leg adds no table read |
| run.json, the lease, the budget, the tiers, the pool binding | r34s | unchanged; `opal_swap_model` is new and optional |

**Writers counted.** Each changed member has ONE writer for this release (the builder). The sources have two owners on trunk (this seat's AR-g-189 to AR-g-192; the other COO's AR-y-492 to AR-y-494 for `opal_producer.py`, `swap_pass.py`, `resident_installed.py`, `build_resident_package.py`, `swap_model.py`), each merged and verified on the full tree.

## 4. Apply protocol, in this order

0. Preconditions the GO names: both halves signed on this file's blob; no filing and no other IB2 act open on the host; **outside 11:30Z-14:15Z and 06:00Z-06:55Z** (CTO msg 11991: the install starts at or after 14:15Z).
1. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34t-20261021`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34s`; the r34t root absent; the library and wrapper unmoved; queue 0 0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
4. V1: running root `0485393f3a-r34t`; the member checks MATCH; the package sums 324 of 324 OK; a census of the two roots (exactly 9 files differ, 2 only in r34t, none only in r34s); the bindings (`package_pin`, `files_from_count` 51, `tickets_table` `opal-tickets`, `opal_swap_model` `{"enabled": true}`, `opal_map` pin and the packager alias unchanged); the three policy hashes unchanged from r34s; the imports (including `swap_model` and `etf_classification_model`); queue 0/0; no sign-in.
5. V2 INSIDE the service's own environment: `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34t`. No YCharts call, no model call.
6. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34s`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2. **The live proofs are separate acts**, one at a time: run 7M (a Multi-Comp: two Opal models and one typed ETF) read by this seat against independent recomputation, then the other COO's run 7N (an Overview with BREIT and, if kept, ZQXWVK).

## 5. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34s`, which stays on the host; `r34r`, `r34q`, `r34p`, `r34o` and `r34n` also stay. Setting `opal_swap_model` to `false` is not needed for rollback (the r34s root has no such binding).
- **The receipt:** the r34s receipt is kept by the install and copied back.
- **Queued messages and audit objects:** none are touched.

## 6. Not claimed

- That run 7M or run 7N passes, or that the typed ETF's history is held by the estate or yfinance tier (the YCharts tier is last and is a vendor call only if both miss).
- That the model leg classifies any given real name correctly: the offline proofs use fakes for every model call; the live proof is run 7N.
- That the live host, S3 objects, the lease row, the running root and receipt are as the build assumes (this is a build record; the host was NOT read by this seat).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-21, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34t`); the receipt and its r34s copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
