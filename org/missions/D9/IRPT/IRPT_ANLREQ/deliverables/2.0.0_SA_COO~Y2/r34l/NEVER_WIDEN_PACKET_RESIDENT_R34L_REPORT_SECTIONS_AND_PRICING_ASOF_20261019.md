# Never-widen sign-off packet -- r34l: the resident r34k -> r34l at pin 2a3aaa2815 (the report document lists no section for an entry the report does not show, and counts them; the pricing as-of follows the trading-calendar frontier)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-19. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO msg 10696 (Andrew's 13:43Z defect: the report page shows about 425 empty "text" cards), ruling `RULING_REPORT_425_TEXT_CARDS_DROP_BUILDER_ONLY_SECTIONS_20261019.md` and its ADDENDUM 1 (@msg 10759: also drop NOT_IN_THIS_VERSION and count them in one disclosure); ~G2 msg 10711 and row S163 / CTO msg 10257 (the pricing as-of rides the next release that touches the resident); pause record items 3-4 (r34l is one of the two ships that end the pause); CTO msg 11011 (ship the producer-only pin).
**One move:** D1, the install of one new root on the resident host. Four members change: two code members, the bindings' provenance and the package sums. No IAM, Lambda, queue, table, schema or vendor-call path moves.
**Order:** `org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-y-406.resident-release-r34l-build-only-two-movers.md` (BUILD ONLY; amendments `5fdddb24b3`, `7536f901bd`, `003fae44dd`), build record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~306/r56/RESIDENT_R34L_BUILD_PINC.json`, merged `055f227cdb`.

## 1. What ships

Package pin `2a3aaa2815874f8efaed622065676332ec41808d` (the issuer's scratch branch `scratch/r34l-pin-c`); base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built twice, byte-identical (317 of 317), by worker `0.9.0_WK_IRPT_ANLREQ~306` with ~G2's r34 tools (five pinned unchanged) over the RUNNING r34k root (tarball sha256 `64f5567dddbd7e96a955410e7e12c5fb3f319551fbe9ce1527cdefdfe8f18a0c`). **317 members**: 313 identical to r34k, **4 changed**, 0 added, 0 removed. The issuer re-hashed the tarball and its three code members against the pin's git blobs (below).

| member | vs r34k | what changes |
|---|---|---|
| `ycharts/research/opal_producer.py` | changed (blob `cdad54df852c`, was `4b5380495c`) | AR-y-404 (`4050bbd629`) and AR-y-408 (`298adde070`): the report document's `sections[]` lists no section for an entry whose method is BUILDER_ONLY or whose reason is NOT_IN_THIS_VERSION and whose status is not VALUE; a VALUE entry is never dropped; ONE last disclosure `NOT_SHOWN` ("%d report elements that this version of the report does not produce are not listed.") counts the dropped entries; `run.json` entries are unchanged. 13 lines added, 1 removed against r34k. |
| `reports/resident_installed.py` | changed (blob `e78cf73b9b`, was `f6f62fc4e8`) | AR-g-161 (`87c9948811`, ~G2): the pricing as-of is the trading-calendar frontier `prev_trading_day(expected_last_trading_day(day))`, not the weekday rule (4 lines added, 6 removed). 0 delivered or queued reports are affected (G2's `ASOF_COUNT_20261017.md`). |
| `reports/resident_bindings.json` | changed | only `provenance` (the verifier proves no other key moved) |
| `SHA256SUMS` | changed | the package sums, replaced (316 lines) |

**Held back on purpose (the pin is a scratch commit that puts these at the r34k bytes):** (a) `lib/trading_calendar.py` at blob `72178007dd` (DASHBD's `f25618c0b4` rides its own pair; `resident_installed.py` calls only `prev_trading_day` and `expected_last_trading_day`, both defined there: checked in the built tarball); (b) `ycharts/research/layout_overview.py` and the overview map `overview_map.json`, ~G2's price-page work AR-g-163..166, paused by the CTO.
**A defect the build gates did not catch, and the check added for it.** The first pin (B) took `opal_producer.py` from trunk, where it also carries AR-g-166's price-table code reading `layout_overview.PRICE_TABLE`; with the layout held back that raises AttributeError at report time. The driver's delta check and the import smoke both PASSED that tarball (the read is inside a function). Found by running the 404 and 408 tests on the pin-B tree (11 failed; 11 pass at pin C). The order now carries criterion AR406-y-AC3 (`check_r34l_xref.py`): every `lo.<NAME>` the built producer reads is defined in the built layout. At pin C: `R34L-XREF-OK missing=0 names=21`; on the pin-B tarball (difference control): `R34L-XREF-BAD missing=1 PRICE_TABLE`.

**Artifacts** (staged OUTSIDE the repository at `C:/dev/irpt-release-r35d`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34l.tar.gz`: sha256 `e1466cb8a0465572e4e0f9a42d79e193313c8afea5fbc2f3370a9ec015a33b6c`, 1,131,211 bytes, 317 members.
- Package sums `irpt-resident-0485393f3a-r34l.package.SHA256SUMS`: sha256 `d5aa71aa6614baa9dc49c897e3b1d1f7ab25e830defc726127fbc9d89c1f8057`.
- Host scripts (`scripts/`): `resident_host_install_0485393f3a-r34l.sh` `e4b73ff0c60b9f31c7d534e05304dab54a55d1cfb4f4e45b335c329f39c59e1d`; `install_r34.sh` `6a1bba36beef2cac0fc06a0496ee9d313c62e0f1f8dd1eb24df64033a66ef092`; `pre_read_r34.sh` `3a5b01064c0bec81f58aa21b84aa8318de61d3dac804b4a3111e59cfc41170dd`; `rollback_r34.sh` `53c0de5b488addc8b0c150b9e28c618caf21b2fc5c51bdae421e20ea4beeee1d`.
- V2 script: ~G2's `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh` (sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`), run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34l` (the script reads that variable); its checks cover members r34l does not change.
- Everything else (the lease, the budget, the resolve hop, the price transport, the door's resolver, the tiers, the packager binding, the swap pool) is unchanged.

**Verification before this packet (issuer's own reads).** (a) Tarball sha256 recomputed `e1466cb8...a33b6c`, 317 members; the members `opal_producer.py` (`cdad54df85`), `layout_overview.py` (`82f0b4744f`, equal to r34k's) and `resident_installed.py` (`e78cf73b9b`) equal the git blobs at the pin. (b) Import smoke over the built tree: `SMOKE live=82 imported=82 fail=0 note=0`. (c) AC3 above. (d) On a detached checkout of the pin: `test_opal_producer_builder_only_sections.py` + `test_opal_producer_not_in_this_version.py` 11 passed; `reports/tests` files `test_generate_installed`, `test_generate_installed_custody`, `test_resident_installed`, `test_status_installed*` 50 passed. The `ycharts/research` suite at the pin fails 30 tests: 26 are the price-page tests and 4 are counts of ~G2's held-back price elements (156 vs 158, 26 vs 9, the holdings table); none is a test of a shipped behaviour. (e) Gate dry runs: gate1 unchanged 0, one-byte 31; gate2 unchanged 0, one-byte 33.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34k) | AFTER (r34l) |
|---|---|---|
| a NEW Opal report's document `sections[]` | one section per layout entry (about 425 cards; 280 builder-only, 144 not-in-this-version) | one section per entry that has a value or a reason other than builder-only / NOT_IN_THIS_VERSION; the dropped ones are counted in ONE final `NOT_SHOWN` disclosure |
| `run.json` entries of a new report | all entries | the SAME |
| a report that was already stored or is queued | its sections as stored | unchanged (no stored report is rewritten) |
| the report's own as-of date | latest `as_of_date` among its sections (`export/narrative_submit.py:42`) | the same: only entries without a value are dropped, and a VALUE entry is never dropped |
| the pricing as-of of a priced report on a Saturday, Sunday or holiday | the weekday rule: Saturday gives Friday | the calendar frontier: Saturday gives Thursday's close, the T-1 trading day (the same rule the door's checker uses since r34k) |
| every other route, role, table, key, queue, tier, budget | unchanged | unchanged |

**Who gains: no principal class.** The change decides which entries a new report prints; it grants no read to a principal. **Writers counted.** Each changed member has ONE writer (the builder). `sections[]` is written by `opal_producer.py` only; its reader named by the brief is the portal's "Open report" (`GET .../analysis/{requestId}/sections`); other readers were not enumerated (section 5).

**Known limits (named, not stops).** (1) The portal's "Open report" is not changed here; a person sees fewer cards, but a report with only pricing-off entries still shows the cards that carry a reason other than NOT_IN_THIS_VERSION (the 144 vendor-not-available kind are kept as cards by the CTO's ruling). (2) The pricing as-of change moves a date on weekend runs; it changes no stored report. (3) Pin B's producer on trunk still reads `PRICE_TABLE`: trunk is not releasable as a whole until ~G2's guard (TO-AR-g-170, row S216) lands; this release does not depend on it.

## 3. Apply protocol, in this order

1. **No YCharts call and no `~Y2` window runs during the install or V2.** The GO says so in terms. Apply outside the weekday 11:30Z-14:15Z band.
2. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34l-20261019`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
3. **Send every host script AS ROOT.** Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34k`; the r34l root absent; the four changed members at their r34k values; the queue 0 0).
4. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
5. V1: running root `0485393f3a-r34l`; the 4 changed members at their built value (`opal_producer.py` blob `cdad54df85`, `resident_installed.py` blob `e78cf73b9b`); the package sums 316 of 316 OK; the imports; queue 0/0; no sign-in in the journal; `opal_pricing` enabled with the tiers `estate, yfinance, ycharts` and `ycharts_window_budget` (6, 390).
6. **V2, INSIDE the service's own environment:** `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34l` (verify its sha256 before sending). Anything but `V2S OK`: rollback.
7. **Gate:** anything but `V2S OK` (or an install that did not print its success line): send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34k`, close the ledger ROLLED-BACK, report. No retry.
8. The ledger closes at V2. **Live proof is a separate act:** run 4 (`IRPT_ANLREQ.TO-RUN-COMMENTARY-E2E-4`, under the signed pair ADDENDA 1-4) reads, for one fresh synthetic Multi-Comp request, `sections[]` with 0 BUILDER_ONLY and 0 NOT_IN_THIS_VERSION entries, the `NOT_SHOWN` disclosure last, and the VALUE sections present.

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's failure branch) restores `0485393f3a-r34k`, which stays on the host.
- **The receipt:** the r34k receipt is kept by the install and copied back.
- **The lease row, the count row, queued messages:** unchanged by r34l; a message received after a rollback is served by r34k.

## 5. Not claimed

- That the live host, S3 objects, running root and receipt are as the build assumes (this is a build record; they were NOT read).
- That the V2 script (written for r34k) exercises the four changed members: it does not; V1 and run 4 do.
- That the PDF printer or any reader other than the portal's "Open report" and the status route is indifferent to fewer sections: the as-of reader (`narrative_submit.py:42`) and the recipe checks (`recipe.py:417-426`, an empty or shorter array is valid) were read; no other consumer was enumerated.
- That the 144 vendor-not-available cards are acceptable to a person: they stay (CTO ruling).
- That trunk HEAD is releasable: it is not until TO-AR-g-170 lands.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-19, on this packet's bytes at the commit that carries it. The write set: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34l`); the receipt and its r34k copy; the unit's ExecStart; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
