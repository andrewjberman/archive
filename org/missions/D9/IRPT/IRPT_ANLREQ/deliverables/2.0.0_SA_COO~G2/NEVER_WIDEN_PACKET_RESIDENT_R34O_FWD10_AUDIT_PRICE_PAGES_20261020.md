# Never-widen sign-off packet -- r34o: the resident r34n -> r34o at pin 3f1961ceab (FWD-10 Core: the comparison section; the audit record's live wiring; the Overview price pages, never released before)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** PRD IRPT_ANLREQ v0.25 FWD-10 and contract C-MODEL-SOURCE (CTO msg 11442: decompose and issue FWD-10 as one round); `2.0.0_SA_COO~Y2` msg 11518 (this seat builds the next resident release and it carries their audit wiring AR-y-467 and AR-y-469); the model-read grant is LIVE (IB2 `A_AFTER_MODELGRANT_R2.txt`, 18:47Z, pair at blob 640730617653).
**One move:** D1, the install of one new root on the resident host. 11 members change and 6 are added (below); bindings change in two places (the Overview map pin and the provenance). No IAM, Lambda, queue, table or schema moves in this packet; the tiers (`estate, yfinance, ycharts`), the budget (6 calls, 390 s), the packager `api_base` (`https://opalinvest.dev`) and the producer list are r34n's.

## 1. What ships

Package pin `3f1961ceab12c934b2510e2047589351ba3539e6`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34o_build.py` (`org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`) over the RUNNING r34n root (tarball sha256 `89cad47247e6785e6b61e60112b04dfaa3cd2d5de88aef6023959692da76d899`), BUILD ONLY, by worker `0.9.0_WK_IRPT_ANLREQ~332` (order AR-g-176, merged `565f271beb2`, record `deliverables/0.9.0_WK_IRPT_ANLREQ~332/r61/RESIDENT_R34O_BUILD.json`). **323 members**: 306 identical to r34n, **11 changed**, **6 added**, 0 removed. The files-from list is 47 lines (r34n's 41, plus six).

| member | vs r34n | what changes |
|---|---|---|
| `ycharts/research/layout_overview.py` | changed (LIVE) | the Opal layout: the Overview price pages (series forms, text, per-holding price table; rounds 57 and 59, never released) and the five comparison elements (window, chart, returns, risk, allocation; round 60 AR-g-174) |
| `ycharts/research/opal_producer.py` | changed (LIVE) | the producer: the price stage, its guard, the comparison stage (AR-g-175), appended after the last page only when the request has comparables AND pricing is on |
| `ycharts/research/overview_map.json` | changed | the Overview map re-pointed for the price pages (round 57); its sha256 is pinned in the bindings |
| `ycharts/generate/resident_worker.py` | changed (LIVE) | `run_opal` hands the producer the request's comparables for a comparison or multicomp record, resolved through the same guarded frozen read the vendor job uses (AR-g-175) |
| `reports/resident_installed.py` | changed (LIVE) | the Opal stores gain `model_bytes` (S3 `get_object` for exactly the two model keys, any other key refused); the audit ports `audit_source` and `audit_put` when `IRPT_TICKETS_TABLE` is set (AR-g-175; AR-y-469) |
| `ycharts/research/opal_packager.py` | changed (LIVE) | the packager records the audit after each successful attach (AR-y-467, AR-y-469); with no audit ports it records AUDIT_PORTS_UNWIRED |
| `ycharts/generate/ticket_confirmation.py` | changed | changed on the pin since r34m's, outside round 60 (not read here beyond the diff being in the pinned source); rides the pin |
| `ops/owned_report.py` | changed | changed on the pin since r34m's, outside round 60 (not read here beyond the diff being in the pinned source); rides the pin |
| `lib/trading_calendar.py` | changed | ONE ADDED function, `first_trading_day_on_or_after` (round 132 IRPT_DASHBD, FWD-5); no existing function moved (diff: +1 doc line, +13 lines); its sha256 is also in the bindings' `members_added` |
| `ycharts/research/model_source.py` | ADDED (LIVE) | the Opal model data reader: S3 bytes injected, both objects (plain series, gzip positioning) read and refused by name (AR-g-171) |
| `ycharts/research/model_code_map.json` | ADDED | the catalogue key to model code map (UST, ST, INT, LT, ULT) |
| `ycharts/research/comparables.py` | ADDED (LIVE) | the comparison record: common window, rebased paths cut at the window end, returns, risk figures, side-by-side allocation (AR-g-173) |
| `ycharts/generate/ticket_audit_source.py` | ADDED | the ticket item reader for the audit (AR-y-469); imported lazily inside `make_packager` when `IRPT_TICKETS_TABLE` is set, so the import smoke cannot see it; listed by hand |
| `reports/analysis_audit.py` | ADDED | the AnalysisAudit.v1 record, its validation and its one write (AR-y-467); imported lazily by the packager; needs `jsonschema` at run time (see section 5) |
| `_contracts/AnalysisAudit.v1.schema.json` | ADDED | the schema `analysis_audit.py` validates against |
| `reports/resident_bindings.json` | changed | `opal_map.sha256` (the new Overview map, `661adac1ef...`), `provenance.package_pin`, `files_from_count` (47), `files_from_sha256`, and `members_added` (only the `lib/trading_calendar.py` sha256); the builder and the release checker prove no other key moved |
| `SHA256SUMS` | changed | the package sums, replaced (322 lines) |

**Two movers are not the round-60 work and are named here because the release carries them unseparated.** (1) The Overview price pages and the price-table code (layout, producer, map) are in the same files as the comparison section, and FWD-10 needs the price stage for the portfolio's path, so they cannot ship apart. Andrew-direct "no performance work until Fidelity" (call 6af6, held XA-2064) stands for new price work; your msg 11442 superseded it for FWD-10 only, and this release makes the already-merged round-57/59 price pages reachable for any request with pricing on (the resident's `opal_pricing` is already enabled in r34n). (2) `lib/trading_calendar.py`: an additive function by another seat.

**Artifacts** (staged outside the repository at `C:/dev/irpt-release-r34o-g2`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34o.tar.gz`: sha256 `c1e3ab21de0511e951c0e727f3d358c1ecfb94fc5f0078963ced2f97cb359b2a`, 1,153,061 bytes, 323 members.
- Package sums `irpt-resident-0485393f3a-r34o.package.SHA256SUMS`: sha256 `3121acf74e02fca872a35cd37f8b09e9047e767e551a3a7e0ff59fd034da5d55` (322 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34o.sh` `6ff2229e5c421e9502ef07052f4630db032a8750563f8d0ce08a798c40893c26`; `install_r34.sh` `5ae1a2dd67175ff233bd34793c01c5decf2ea3b4c4839339c2c05635e3cd0349`; `pre_read_r34.sh` `23bc44375695ea148d37497ca470cd4a82af953b96bb1e4bee3386241505d511`; `rollback_r34.sh` `5803fd9bf9e1036b5866ea8d8d32412940f6bc0a78c1b7eea537a60960fb0976`.
- V2 script `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh`, sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`, run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34o`; its offline test re-run by the issuer today: `V2S-R34K-TEST-OK 30 cases`.

**Verification before this packet.** (a) The worker's build and the issuer's own earlier rehearsal at the same pin produced the SAME tarball sha256 (fixed clock), builds identical 323 of 323. (b) The issuer's release checker `checks/ar_release_checks.py`, written before the build and calibrated on the rehearsal with mutants, re-run by the issuer on the official stage: `AR-REL-record-OK`, `AR-REL-tree-OK`, `AR-REL-scripts-OK`. The tree arm reads the tarball with its own code: every shared member equals r34n except the 11, each mover and addition equals `git show 3f1961ceab:<source>`, the bindings carry the pin, and the lazy imports the smoke cannot see (`ticket_audit_source`, `analysis_audit` with its schema, `model_source`, `comparables`) import in a fresh `-I` interpreter over the extracted tree. (c) Import smoke over the built tree: `SMOKE live=86 imported=86 fail=0 note=0`. (d) Gate dry runs (an unchanged copy passes, a one-byte copy refuses): 0, 31, 0, 33.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34n) | AFTER (r34o) |
|---|---|---|
| an Opal Overview with pricing on | no price pages, no price table | the price pages and the per-holding price table (price levels from the estate, yfinance, then ycharts tiers; same lease and budget as r34n) |
| an Opal Comparison or Multi-Comp report | the vendor-shaped sections only | the same, plus ONE comparison section after the last page when the request has comparables and pricing is on: window, cumulative-return chart, returns, risk, allocation; a part Opal cannot fill reads `not available for <name>: <reason>` |
| reads of the model objects | none | `s3:GetObject` on `json/benchmarks/model_portfolio_timeseries.json` and `json/positioning/positioning_data.json` of `opal-data-portal-v2` by the host role (grant live); `model_bytes` refuses any other key |
| the packager's audit record | none | when `IRPT_TICKETS_TABLE` is set: one DynamoDB GetItem on the ticket table and one S3 put of the audit JSON to the product bucket per attach (Y2's IAM pair AR-y-468 applies FIRST); when unset: AUDIT_PORTS_UNWIRED recorded, nothing written |
| a request with no comparables, or pricing off | -- | unchanged: no compare element, no extra read |
| lease, budget, resolve hop, tiers, packager `api_base`, producer list | r34n | unchanged |

**Writers counted.** Each changed or added member: ONE writer (the builder, for this release). The bindings file and the package sums: ONE (the builder).

## 3. Apply protocol, in this order

0. Preconditions the GO names: Y2's IAM pair for the audit (AR-y-468) is applied if the service environment sets `IRPT_TICKETS_TABLE`; no YCharts window run is in flight; the model grant stays as it is.
1. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34o-20261020` first; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34n`; the r34o root absent; the library and wrapper unmoved; the 9 changed package members at their r34n value, the 6 additions ABSENT; queue 0/0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
4. V1: running root `0485393f3a-r34o`; the 17 changed or added members at their built value; the package sums 322 of 322 OK; the imports; queue 0/0; no sign-in in the journal; `opal_pricing` enabled with the tiers `estate, yfinance, ycharts` and the budget (6, 390).
5. V2 INSIDE the service's own environment: `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34o`. No YCharts call.
6. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34n`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2. **The live proof is a separate act** (the one real run, `FWD10_ONE_REAL_RUN_PLAN_20261020.md`, orchestrated by `2.0.0_SA_COO~Y2`).

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34n`, which stays on the host.
- **The receipt:** the r34n receipt is kept by the install and copied back.
- **Queued messages:** none are touched; a message received after a rollback is served by r34n, which has no comparison section and no price pages.

## 5. Not claimed

- That `jsonschema` is importable on the resident host: `analysis_audit.validate` raises ValidationUnavailable without it and no audit write follows (the attach itself is not blocked by the audit's absence); this release does not install it. Y2's V2 or first attach reads it.
- That the comparison reads well to a person, or that the numbers equal an independent recomputation on the live objects: that is the one real run and the CVO's L9, after the install.
- That the live host, S3 objects, the lease row, the running root and receipt are as the build assumes (this is a build record; they were NOT read).
- That the yang job keeps the two model keys where they are today (a moved key makes the reader refuse in words; one constant in `model_source.py`).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34o`); the receipt and its r34n copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
