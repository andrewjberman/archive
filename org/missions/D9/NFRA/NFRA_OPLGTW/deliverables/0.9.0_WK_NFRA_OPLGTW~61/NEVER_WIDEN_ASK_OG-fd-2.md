# NEVER-WIDEN ASK -- OG-fd-2 (round-36 E2): the per-family releases of the per-family DLQ drain, with each family's drift named

To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`. From: `0.9.0_WK_NFRA_OPLGTW~61`. Source and offline tests only: no package rebuilt, no deploy,
no queue read. Rows: `NFRA_OPLGTW-Z-W61-S1`, `-S2`. The releases are later orders; this file is what each is signed against.

## 1. What this order changed (source, committed `b2538131ea`)

`run_sweep` now writes its DLQ drain dict into the backfill-status section it already writes, as ONE added key `dlq_drain`:
`drained`, `family`, `other_family_returned`, `unattributed`, `truncated`, `messages` (id + body, capped at 25),
`messages_total`, `messages_capped`. No existing key changes; the guard and counts keys are asserted unchanged in the tests.
Sites: `mirror_conversion.py run_sweep` (orion, eclipse, blackdiamond), `etf_conversion.py run_sweep` (3 trees, via
`mc.dlq_drain_record`), `schwab_runtime.py run_sweep` (the drain now runs BEFORE the lanes so each lane's fold carries it; its drain
output also gains `message_ids`). Tests: `test_fd2_ac01`, `test_fd2_ac02`, plus an etf leg; 78 passed, 10 skipped across the three suites.
Any release of OG-fd-1's drain therefore also ships this record, so it is read after the fact (row Z-S100) from the first fire.

smartx and bd49finsurance hold no DLQ read (`grep drain_dlq|DLQ_URL` over both package dirs and the sources: 0 hits), so neither has a
drain change to ship and neither is exposed to row Z-S91. They are in the census because they are in `silver.tf local.silver_families`.

## 2. The census (denominator: `silver.tf local.silver_families` = 7; schwab is live, so 6 follow)

Measured by `FD2_DRIFT.json` (same folder): each BUILD_MANIFEST `vendored_modules` file at source `4c7e933975` (before this order's source
change) against the package copy, CRLF-normalised, lines added plus removed. `drift_owner` is the author of the newest commit on the
package path (the order's definition); `newest_source_commit_in_drift` names who moved the SOURCE ahead, because for most families the
package path's newest commit is a vendoring that was itself partial (row `-S1`).

| family | drift_lines | without the drain code | drift_owner (package path) | newest source commit in the drift |
|---|---|---|---|---|
| orion | 359 | 282 | `0.9.0_WK_NFRA_MCPINDEX~7` @`878fd82986` | `0.9.0_WK_NFRA_OPLGTW~58` @`12a92ffa49` |
| eclipse | 475 | 398 | `0.9.0_WK_NFRA_MCPINDEX~7` @`878fd82986` | `0.9.0_WK_NFRA_OPLGTW~58` @`12a92ffa49` |
| blackdiamond | 375 | 298 | `0.9.0_WK_MDPF_STRATID~5` @`82e0a49ed2` | `0.9.0_WK_NFRA_OPLGTW~58` @`12a92ffa49` |
| etf | 101 | 19 | `0.9.0_WK_NFRA_MCPINDEX~7` @`878fd82986` | `0.9.0_WK_NFRA_OPLGTW~58` @`12a92ffa49` |
| smartx | 0 | 0 | `0.7.0_AE_CloudOps` @`07a8d69eee` | none (no differing file) |
| bd49finsurance | 2 | 2 | `0.7.0_AE_CloudOps` @`7d0ab9cdac` | `0.9.0_WK_NFRA_OPLGTW~39` @`47c3c75f11` (silver_registry.py) |

The drain code (OG-fd-1 + this order) accounts for the difference between the two number columns; the rest is drift the rebuild would also ship.

## 3. Per family: alone or with drift, blast radius, rollback

Rollback for every family: re-point the function to the prior code. Live prior `CodeSha256` was READ now (`get-function-configuration`,
one resource each, 2026-10-13T17:2xZ) and must be re-read at release time. None of the six functions carries `OPAL_BUILD_COMMIT`
(`silver_build_commit` holds schwab only), so the prior PIN is "UNPINNED (no OPAL_BUILD_COMMIT env)" for all six and the prior
code identity is the CodeSha256 plus the package-path commit that built it. The release should record the prior S3 object version of
`opal-assets/opal-assets-silver-<family>.zip` before uploading.

- **etf** -- ships the drain change PLUS 19 lines of other drift (mirror_conversion.py 17 differing lines;
  silver_registry.py 2: the third schwab master 08403355, inert to etf). Closest to "drain alone". Blast radius: the etf converter's code
  (`etf_conversion.py`, `mirror_conversion.py`, `silver_registry.py`), 3 silver trees. Prior CodeSha256
  `hosvkcI2IaY+NBmxqio98+dEqWmXIjBpBQqEpkA30nU=` (LastModified 2026-09-27T10:35:46Z, package built at `878fd82986`).
- **orion** -- ships the drain change AND 282 lines of drift, 256 of them in `mirror_conversion.py`: the package copy is a HYBRID
  (`878fd82986` patched the Z-S3/Z-S25 fixes into a stale copy; it equals no source commit) so a rebuild replaces it with the source's current text (11 commits in that file's history), plus mirror_schemas.py (11) and silver_registry.py (15). Not drain-alone. Blast radius: the
  orion converter's code, i.e. orion bronze->silver for all feeds. Prior CodeSha256 `dO6YMv6Gi477d6/g4Jbx/WLPro60rXwtFm7hA97ne0Y=`
  (2026-09-27T10:35:46Z, built at `878fd82986`).
- **eclipse** -- same shape as orion, 398 lines of drift besides the drain. Not drain-alone. Blast radius: the eclipse converter's code.
  Prior CodeSha256 `QsoUUJUhw2lDaga37HU2gKo1VqZwHreRNbeZpRvE2Bg=` (2026-09-27T10:35:46Z, built at `878fd82986`).
- **blackdiamond** -- ships the drain change AND 298 lines of drift that includes work its own manifest note calls held: rebalancer_schemas.py (111) and
  rebalancer_conversion.py (77), and `opal_strategy_matcher.py` (91 lines), which `82e0a49ed2` added to BUILD_MANIFEST but the package dir
  never received (MISSING_IN_PACKAGE; `vendor-manifest.sh` copies every manifest entry unconditionally, so a rebuild ships it). The
  bd49finsurance manifest note records the same coupling (3F-S5/S7 rebalancer work riding a blackdiamond rebuild). Not drain-alone.
  Blast radius: the blackdiamond converter's code (cottonwood xlsx and the rebalancer path). Prior CodeSha256
  `DZl5N5IoyMTwGZI1Dl/D+40Ldd+ZzkbF60M6JFwD3Pw=` (2026-09-27T10:35:46Z, built at `878fd82986`).
- **smartx** -- no drain code, so NO release is needed for this cell; nothing to sign. Drift 0. Prior CodeSha256
  `aHX6HfHnISKRRVlZL9k56kz9K4KNfGrrPJovmqO/5yQ=` (2026-07-20T19:23:28Z) for the record.
- **bd49finsurance** -- no drain code, so NO release is needed for this cell. Drift 2 lines (inert). Prior CodeSha256
  `BWz0P6TXSxMKM+ZL4KzFuyh9lOCzrPXJ5cHqMYv4ZcE=` (2026-08-30T08:06:05Z).

## 4. The decision this puts to the CTO and issuer

Row Z-S91 (a sweep deleting another family's record) stays open for orion, eclipse, blackdiamond and etf until their releases land.
Two ways to release a family: (a) vendor everything the manifest lists and accept the drift in section 3, or (b) a drain-only package
(vendor only the drain-bearing module(s) over the live copy), which needs the vendored files to stay mutually consistent and is a build
choice the release order must make explicit. etf fits (a) with 19 lines of drift; orion, eclipse and blackdiamond need a per-family signature that
names their drift, because (a) ships hundreds of lines no order has graded.
