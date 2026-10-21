# Never-widen sign-off packet -- r34s: the resident r34r -> r34s at pin 5fd1e793f2 (the Multi-Comp portfolio path from the common window start, and the report presentation fixes)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-21. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO msgs 11929 and 11932 (FWD-10 is not realized while the portfolio row fails to reproduce under the resident's own formula; proceed with the fix cells, failing-first). The defect: run 7J (Multi-Comp on r34r) served a portfolio row that differs from independent recomputation (`deliverables/2.0.0_SA_COO~G2/FWD10_READ_RUN7J_20261021.md`).
**One move:** D1, the install of one new root on the resident host. FIVE members change against the running r34r and none is added or removed; no IAM, Lambda, queue, table, schema or vendor-call path moves, and the registry file, the `tickets_table` binding and the files-from list do not move.

## 1. What ships

Package pin `5fd1e793f2fe7e3eabdac88d178c411c3d51ab0b`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34s_build.py` (`org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`, the r34r builder shifted one root), BUILD ONLY, by worker `0.9.0_WK_IRPT_ANLREQ~365` (order AR-g-188, merged `af7e16202a1`, record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~365/r66/RESIDENT_R34S_BUILD.json`) over the RUNNING r34r root (tarball sha256 `77ec08f5a591de5584abb71787eb74c86bcbd3167416f2b411befc750140b828`). **323 members**: 318 identical to r34r, **5 changed**, 0 added, 0 removed.

| member | vs r34r | what changes |
|---|---|---|
| `ycharts/research/portfolio_series.py` | changed | adds `buy_and_hold_from(series_by_ticker, amounts, start_ms)`: the filed amounts applied at `start_ms` (AR-g-185); `buy_and_hold` is unchanged |
| `ycharts/research/opal_producer.py` | changed | `_price_stage` returns its per-symbol series and amounts as a fourth value; `_compare_stage` re-applies the filed amounts at the common window start (the largest first timestamp among the comparables that carry a series) instead of cutting a path whose weights were set at the start of the 10-year price window (AR-g-185); run.json is unchanged |
| `ycharts/research/layout_overview.py` | changed | no false "Not available: no row of this section has a value." line; the n/a period columns explained in words; the comparison elements `el cmp` with a keep-together page-style rule; the literal `{portfolio_name}` in element labels printed as `Your portfolio` (AR-g-186) |
| `reports/resident_bindings.json` | changed | `provenance.package_pin` only (the files-from list is unchanged, so the count and sha256 do not move); the release checker proves every other key equals r34r's |
| `SHA256SUMS` | changed | the package sums, replaced (322 lines) |

Everything else r34r shipped stays: the admission and comparison-read fixes, the lead token, the audit projection, the registry and bindings.

**Artifacts** (staged outside the repository at `C:/dev/irpt-release-r34s-g2`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34s.tar.gz`: sha256 `fa950681774268d2108eb7ca141ec150213d0d6e482dad498d13870a90d87b14`, 1,155,397 bytes, 323 members.
- Package sums `irpt-resident-0485393f3a-r34s.package.SHA256SUMS`: sha256 `fce2a5b9f31b14138fa5d08faa9630b5ea7921e1aa5e985ebf85f7284ea7c3fc` (322 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34s.sh` `ac2663c612b5a0c9f0232c8a5305bb3d9a6628e944c9c8f22d8dcfd3dc31fe94`; `install_r34.sh` `bc002da4715368159f4a3f8ecf97e37ec70d27682cf02350da7c87cb473663bc`; `pre_read_r34.sh` `8de0d54bc83a2d51445edaf0ddaa5853ec97dd12b44805f073d82726a96c5936`; `rollback_r34.sh` `9f44317de0edb618b27b16ff76a659d52495cbe2511825efd826cd4292bb08bb`.
- V2 script `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh`, sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`, run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34s`.

**Verification before this packet.** (a) The worker's build and the issuer's rehearsal at the same pin produced the SAME tarball sha256 (fixed clock); builds identical 323 of 323. (b) The issuer's checker `checks/ar_release_s_checks.py`, written before the build and calibrated (positive on the rehearsal; negative: it refuses the r34r tarball offered as r34s, with the delta empty, three movers not the pinned source, the bindings unmoved and the shipped source lacking `buy_and_hold_from`), re-run by the issuer on the official stage after the merge: `AR-RELS-record-OK`, `AR-RELS-tree-OK`, `AR-RELS-scripts-OK`. (c) Import smoke: `SMOKE live=86 imported=86 fail=0 note=0`. (d) Gate dry runs: 0, 31, 0, 33. (e) The cells' own gates, run by the issuer on the full tree after the merges: portfolio `AR-WINDOW-portfolio-OK`, window tests 76 passed; `AR-GAPNOTE-gaps-OK`, `AR-GAPNOTE-placeholder-OK`, gapnote tests 85 passed; and the drain run of `ycharts/research/tests`, `test_compare_ports.py`, `test_resident_main.py` and `test_frozen_worker.py`: 741 passed.

## 2. The evidence for the defect and the fix

**The defect, MEASURED by exact reproduction.** 7J's portfolio row (1M -0.5286, 3M 0.7512, YTD 10.6642, 1Y 13.3749, chart maximum 151.8645) equals, to three decimals, the filed amounts (44 SPY, 26 AGG, 15 IWM, 15 EFA) applied at 2016-10-20 (the start of the 10-year price window, `PRICE_HISTORY_YEARS`), by the resident's own reader and formula, then cut and rebased at the common window start 2024-04-30, by which date SPY had drifted to 60.1 percent. The independent recomputation with the amounts applied AT the window start gives YTD 8.83, 1Y 11.12 and maximum drawdown -13.60 against the page's 10.66, 13.37 and -15.94. The Opal model rows matched exactly (8 of 8 returns, drawdown, monthly std dev, allocation).

**The fix, by the checker the cell was written against** (`checks/ar_window_checks.py`, the REAL producer on a Multi-Comp whose holdings were priced over a history that starts 60 months before the models' first observation, with strong pre-window drift; expected value from the checker's own arithmetic): at the base the served "Your portfolio" line ends at 157.4417 against the 151.6101 the window-start amounts give (FAIL); at the pin it passes. The checker was calibrated against a reference fix and three mutants (window start ignored, start at the wrong date, amounts ignored), each of which fails.

**Run 7f's Overview sample reproduces exactly** under the resident's formula (the same read: all five portfolio cells and the chart maximum and minimum), and its caption states its semantics ("buy-and-hold from the accepted amounts"); r34s does not change the Overview's path (the change is in `_compare_stage`, which runs only with comparables).

## 3. Blast radius

| what | BEFORE (r34r) | AFTER (r34s) |
|---|---|---|
| a Multi-Comp's "Your portfolio" returns, risk and chart | the filed weights drifted from the 10-year window start | the filed amounts bought at the common window start and held |
| a Comparison with one ETF comparable | the same drift | the same fix (the common window start is that comparable's own first observation or the portfolio's) |
| an Overview (no comparables) | its documented path (amounts at the first common date) | unchanged |
| the comparison section's text | a false "no row has a value" sentence in three sections, a bare `n/a` for 3Y/5Y/10Y, a stranded heading | no false sentence, the n/a periods named in words, the elements kept together on a page |
| Overview element labels | the raw `{portfolio_name}` printed | `Your portfolio` |
| run.json, the registry, the bindings, the lease, the budget, the tiers | r34r | unchanged (bindings: `package_pin` only) |

**Writers counted.** Each changed member has ONE writer for this release (the builder), the source files two owners on trunk (AR-g-185, AR-g-186), each merged and verified on the full tree.

## 4. Apply protocol, in this order

0. Preconditions the GO names: both halves signed on this file's blob; no filing and no other IB2 act open on the host (Y2's residue-delete order, if running, closed first); outside 11:30Z-14:15Z and 06:00Z-06:55Z.
1. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34s-20261021`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34r`; the r34s root absent; the library and wrapper unmoved; queue 0 0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
4. V1: running root `0485393f3a-r34s`; the member checks MATCH; the package sums 322 of 322 OK; a census of the two roots (exactly 5 files differ, none only in either); the bindings (`package_pin`, `files_from_count` 50, `tickets_table` `opal-tickets`, `opal_map` pin and the packager alias unchanged); the three policy hashes unchanged from r34r; the imports; queue 0/0; no sign-in.
5. V2 INSIDE the service's own environment: `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34s`. No YCharts call.
6. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34r`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2. **The live proof is a separate act** (run 7K, the Multi-Comp filing, new holdings), one filing, never alongside another IB2 act; its PDF is read by the issuer against independent recomputation (the portfolio row must reproduce, the false sentence and the raw placeholder must be gone).

## 5. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34r`, which stays on the host; `r34q`, `r34p`, `r34o` and `r34n` also stay.
- **The receipt:** the r34r receipt is kept by the install and copied back.
- **Queued messages and audit objects:** none are touched.

## 6. Not claimed

- That run 7K passes: it is the next act after the install. The producer-level checks prove the packaged modules over synthetic prices, not the live price tiers, the PDF's page breaks (the `.cmp` rule is proven in the HTML; the next PDF is the proof) or the risk table's Sharpe, Sortino and alpha, which the issuer has not independently recomputed.
- That the Overview's buy-and-hold-from-the-first-common-date semantics read as intended to a person: it is a spec call, not a reproduction failure (the CTO has the record).
- That the live host, S3 objects, the lease row, the running root and receipt are as the build assumes (this is a build record; the host was NOT read by this seat).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-21, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34s`); the receipt and its r34r copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
