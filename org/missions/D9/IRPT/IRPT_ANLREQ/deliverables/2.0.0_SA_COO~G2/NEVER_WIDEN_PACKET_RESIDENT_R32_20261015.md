# Never-widen sign-off packet -- r32: the resident r31 -> r32 at pin 26d720a980 (the ENGINE lane's merged cells, the commentary revision, run 3's producer address)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-15. **Applier:** a CloudOps seat named by the CTO.
**Authority:** CTO msg 8377 (the ENGINE lane), msg 8568 (ADDENDUM 2 of `CTO_RULING_DELL2_ANLREQ_PROD_PROMOTE_RELEASE_AFTER_FWD1_WINDOW2_20261015.md`:
`irpt-anlreq-x10-v1` and run 3's address ride ONE resident release), msg 8630 (SPY and BIL), msg 8647 (PRD v0.16); `~Y2` msg 8566 and 8570 (the address
`fwd1-staff-r41b@opal.invalid`). **Ledger:** `irpt-resident-r32-20261015`. **One move:** D1, the install of one new root on the resident host. No IAM, Lambda,
queue, table or schema moves. No vendor call. **Scope:** this is the RESIDENT leg only. The accept stamps and the upload door run in the `irpt-ycharts-generate`
Lambda and are a separate leg (`R32_LEGS_FINDING_20261015.md`).

## 1. What ships

Package pin `26d720a980ba7792e87141e2bd97a5781f8bb190`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r32_build.py` over the tools at that pin, BUILD ONLY. **310 members**: 284 identical to r31, **15 changed**
(including `SHA256SUMS` and the bindings), **11 added**, 0 removed. Two builds under one fixed clock are identical 310 of 310.
The verifier `ar_g92_checks.py verify` (independent of the builder) recomputed every number below and passed.

| member | vs r31 | in the resident's runtime (static import walk) |
|---|---|---|
| `intake/portfolio.py` | changed | LIVE |
| `intake/uploads.py` | changed | LIVE |
| `reports/build_resident_package.py` | changed | not reachable |
| `reports/generate_installed.py` | changed | not reachable |
| `reports/resident_bindings.json` | changed | not reachable |
| `reports/resident_installed.py` | changed | LIVE |
| `ycharts/generate/acceptance.py` | changed | LIVE |
| `ycharts/generate/normalized_input.py` | changed | LIVE |
| `ycharts/generate/prospect_submission.py` | changed | not reachable |
| `ycharts/generate/resident_worker.py` | changed | LIVE |
| `ycharts/generate/submission_service.py` | changed | not reachable |
| `ycharts/research/layout_overview.py` | changed | LIVE |
| `ycharts/research/opal_producer.py` | changed | LIVE |
| `ycharts/research/runner.py` | changed | LIVE |
| `ycharts/generate/ticket_confirmation.py` | ADDED | not reachable |
| `ycharts/research/comparison_map.json` | ADDED | not reachable |
| `ycharts/research/multi_map.json` | ADDED | not reachable |
| `ycharts/research/portfolio_series.py` | ADDED | LIVE |
| `ycharts/research/price_adapter_bbg.py` | ADDED | LIVE |
| `ycharts/research/price_adapter_demque.py` | ADDED | not reachable |
| `ycharts/research/price_adapter_ycharts.py` | ADDED | not reachable |
| `ycharts/research/price_adapter_yfinance.py` | ADDED | LIVE |
| `ycharts/research/price_source.py` | ADDED | LIVE |
| `ycharts/research/swap_replacement.py` | ADDED | not reachable |
| `ycharts/research/tr_level.py` | ADDED | LIVE |

Reachable modules: 74 in r32, 69 in r31. Compiled: 127 of 127 Python members.

**The bindings** gain `opal_map_comparison` and `opal_map_multicomp` (relative paths, pinned by content, verified by the installer's own loader against the shipped files: report types
OVERVIEW, COMPARISON, MULTI) and `opal_pricing` shipped **OFF** (`enabled` false, tiers `estate`, `yfinance`); the provenance block changes; every other key is unchanged.

**The producer list** reads exactly `("andrew@opalinvest.com", "fwd1-staff-r41b@opal.invalid")`: r41a (run 1) leaves, r41b (run 3) enters.

**Artifacts** (staged outside the repository; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r32.tar.gz`: sha256 `3338a5c73c8bf0bb050850507ba9707a079055e803858321c8864ee8bb3a3f1f`, 1,087,615 bytes, 310 members.
- Package sums `irpt-resident-0485393f3a-r32.package.SHA256SUMS`: sha256 `8a473acc405fb41dfba1af5d5bd9f2956aa38208aac43fa79d2f7fd96751afb5`.
- Host install script `resident_host_install_0485393f3a-r32.sh`: sha256 `5adc8d0b6ae1a6d04b182cda11d5d758b8549084f722b90e5990fc0b59d0d0d6`; `install_r32.sh` `39f1326c96610d60d2a2a494ddc54e10d480df104f2df9bb747bd4994d871e53`; `pre_read_r32.sh` `9f6523cf84a8f3216ab312c2a7072b0fb468d89eec12a48e5cd9788ac4e1ccba`; `rollback_r32.sh` `a5b74ea1c35b29631f31a780240359a3d5d41891335bc754e3b726efd041c487`.
- The capture library and wrapper are unchanged (`a1c28801...`, `55ddb8f7...`).

## 2. Blast radius, by branch (read from the code at the pin)

| what changes | BEFORE (r31) | AFTER (r32) |
|---|---|---|
| a job for `fwd1-staff-r41a@opal.invalid` | Opal producer | YCharts producer (r41a leaves the list) |
| a job for `fwd1-staff-r41b@opal.invalid` | YCharts producer | Opal producer |
| a job for `andrew@opalinvest.com` | Opal producer | the same |
| any other principal | YCharts producer, unless its record carries `ticket_confirmed` True | the same (the stamp is written by the Lambda leg, not by r32) |
| an Opal job whose record has no `report_variant` | the Overview map | the Overview map (absent = overview) |
| an Opal job whose record has `report_variant` comparison or multicomp | the Overview map (silently wrong) | its own pinned map; if the pin is absent or differs the job refuses `OPAL_MAP_BINDING_REQUIRED` / `PINNED_FILE_*` (the shipped pins are verified) |
| an Opal job's report: figures that need only the portfolio's series | NOT_AVAILABLE (pricing off) | unchanged while `opal_pricing` is off; the code is present and unreachable until a bindings edit enables it |
| the Opal page's multi-column statistics (Periodic Return, Drawdown) | `STATISTIC_UNKNOWN:None` | worked out per column, `n/a` where the series is too short; unchanged while pricing is off (the elements read NOT_IN_THIS_VERSION) |
| the package attach (commentary read-back) | refused: `ANALYSIS_COMMENTARY` unregistered | registered under `irpt-anlreq-x10-v1` |
| a priced run, if a later bindings edit enables it | -- | SPY and BIL named as the benchmark and the risk-free proxies in words; an unpriced one leaves its statistics INPUT_MISSING |

**Writers of the touched properties, counted.** The producer list has ONE writer (`resident_worker.py`); the bindings have ONE writer (the builder, for this release). The in-flight
jobs at the install are not touched: the installer reads the queue empty first (`0 0`) and restores the library and receipt if it is not.

## 3. Apply protocol, in this order

1. Both halves at HEAD naming this file's blob.
2. Before-read: `pre_read_r32.sh` (fail-closed: the running root must be `0485393f3a-r31`, exit 40; the unit must carry no `IRPT_ANALYSIS_READY_QUEUE_URL`; the r32 root absent; the library and wrapper unmoved; every changed member at its r31 value, every added member ABSENT; the queue 0/0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r32.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM` (exits 31 and 33, dry-run: unchanged copy rc 0, one byte changed rc 31 and 33); it then runs the host script, which stages the tar, checks 26 members, keeps the r31 root and library, installs, polls, and ROLLS BACK ITSELF to r31 on a failed start.
4. V1: running root `0485393f3a-r32`; every changed or added member at its built value; the package sums 309 of 309 OK; the Opal imports (`price_source`, `portfolio_series`, `tr_level`, the adapters, `layout_overview`, `opal_producer`); the producer list line; queue 0/0; no sign-in in the journal.
5. The ledger closes at V1.

**Live proof is a separate act** (FWD-1 run 3 under `~Y2`'s addendum with the new address).

## 4. Rollback, per key

- **The root:** `rollback_r32.sh` (or the install's own failure branch) restores `0485393f3a-r31`, which stays on the host; its readers are the r31 values of the changed members and ABSENT for the added ones.
- **The receipt:** `cutover_receipt.0485393f3a-r31.json` is kept by the install and copied back.
- **The library:** unchanged bytes before and after; the kept copy `ycharts_session.js.before-0485393f3a-r32` restores it.
- **Queued messages:** none are touched; a job picked up after a rollback is served by r31.

## 5. Not claimed

- The behaviour of the Lambda leg (stamps, door), the portal form, or any live Opal report.
- That the BBG history or Yahoo hold SPY and BIL; pricing is OFF in this release.
- That `price_adapter_ycharts.py`, `price_adapter_demque.py` and `swap_replacement.py` are used: they are not reachable.
- The live host, S3 objects, running root and receipt were NOT read (this is a build record).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-15, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r32`); the receipt
and its r31 copy; the unit's ExecStart; the kept library copy. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO

(not signed)
