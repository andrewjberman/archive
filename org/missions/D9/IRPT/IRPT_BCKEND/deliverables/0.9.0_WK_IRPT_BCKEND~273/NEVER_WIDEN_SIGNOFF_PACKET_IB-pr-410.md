# Never-widen sign-off packet -- IB-pr-410: the 49F holdings bundle with dell1's e56 CUSIP fallback, IB-pr-403's SmartX CUSIP ids and the ticker= fact that keeps SmartX nodes classified

Prepared by 0.9.0_WK_IRPT_BCKEND~273 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed, applied or written: BUILD_ONLY, offline replays, AWS reads only.
Files beside this packet: `IB111-1_49f_bundle_census.json`, `IB111-1_49f_bundle_replay.json`, `IB111-1_49f_analysis.json` (counts only), `compose_410.py`. Scripts reused unchanged: ~266's `extract_bundle.py` / `narrow_pack.py`, ~269's `replay_driver_cached.py` / `cmp_members.py`, ~265's `replay_publish_gate.py`.
Order: `IRPT_BCKEND.TO-IB-pr-410`; CTO ruling D1-S8 AMENDMENT 2 @b58f09e1b8; rows `IRPT_BCKEND-D2-W269-S1` (disposed by D2-S53), `IRPT_BCKEND-D2-W269-S2`. **This packet SUPERSEDES `0.9.0_WK_IRPT_BCKEND~269/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-406.md`**: its artifact (sha256 `f8bd6f667d3820ca7318a8360d5801e8d80dc73f7412f9eff907034610b08819`) is the build the FWD-14 gate REFUSES and is no longer the one to sign.

## The fix, and what it does on real 49F inputs

**Fix** (`holdings_49f.py`, commit `9b7256a99f`): every SmartX model-asset SECURITY node whose row has a ticker carries the classification fact `ticker=<ticker>`, whether its `security_id` is a CUSIP or a TICKER. `holdings_snapshot.fill_display_from_facts` reads the symbol from that fact (`:803`), so `display.symbol` stays and `classify_security` keeps asking the table by symbol first. IB-pr-403's CUSIP rule, its `cusip_basis` fact and its listing are unchanged. Tests: `test_smartx_cusip_node_keeps_ticker_for_display_symbol`, `test_smartx_cusip_node_keeps_ticker_even_when_security_id_has_no_ticker_namespace`; IB-pr-403's three `smartx_cusip` tests still pass (5 of 22 selected by `-k smartx_cusip`; the 49F and SmartX suites 49 passed).

**Replay, same real inputs and served index for every tree** (business_date 2026-10-08, 156,281 node ids on every tree, identical `source_set_revision_sha256`; `IB111-1_49f_bundle_replay.json`, 9 arms, 3 negative controls). The gate is read, not assumed:

| | Base (IB-pr-402 bytes) | Built (this packet) | ~269 build (negative control) |
|---|---|---|---|
| gate outcome | PUBLISHED, conditions none, `new_unclassified` 0 | **PUBLISHED, conditions none, `new_unclassified` 0** | **REFUSED, `classified_security_lost` 53**, `new_unclassified` 5 |
| puts | 195 | 204 | 1 (the refusal record) |
| SmartX class state, base -> candidate | | classified -> classified **116,815 of 116,815**; classified -> unclassified **0** | classified -> classified 102,923; classified -> unclassified **13,892** |

`fwd14_gate_unchanged` **identical** (outcome, conditions and listed counts equal; `evaluate_publish_gate` is byte-identical in both members). `smartx_class_parity` **identical**: 0 SmartX nodes classified on base and unclassified on built; no `asset_class`, `sub_asset_class` or `asset_class_basis` moves on any of the 116,815 SmartX nodes (the ~269 build moved 20,499 class values); `display.symbol` equal on base and built for 116,815 of 116,815.

## What is released, and from what

- **Base = IB-pr-402's built 49F bytes**, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` (md5/ETag `01387cef54b9e15e10023f05029e357d`, 468,666 bytes). **The live object is those bytes**: version `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`, LastModified 2026-10-09T10:27:33Z, read by `get-object` today, sha256 equal (the version IB-pr-404 landed). Control: ~266's packer over the unpatched extracted live tree reproduces this sha256.
- **Built = `47be54d6479fdb849477a41b7cffa089319f2f18d38069b3384393fec192dda5`**, md5 (= the ETag a verified upload must echo) `1e8ff3096af151f91b96c4e8a3712e4a`, 469,537 bytes, 45 members (python 3.12, LF). Packed twice, byte-identical. Pin `9b7256a99f0fc76e7c37988b4eb48c4f44491d3e`. S3 user metadata the upload would carry: `members-sha256=96925f389381e64beeeb31ebf61eecdd5335fddf30cce0335300b455979bfd62,member-count=44`.
- **Two members move** (42 of 45 byte-identical to the base; `SHA256SUMS` is the regenerated manifest; read member by member from both tars with `cmp_members.py`):
  - `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py`: the live (narrow) member + the diff of `01e843ce2e` to that file ONLY (`e56_holdings_snapshot.diff` sha256 `2334c941...597fff`) -> sha256 `a9fe965f9e5ada7fe9b2278e2e596c32d48ae96e43df90ec90a22211e921ec62`, git blob `e39636c5a8`. dell1's member; the tree's copy is untouched, the member is composed only here.
  - `data/assets/scripts/gold/investor_reporting/holdings_49f.py`: the live member (blob `3ee9637a62`) + the diff of `dfa9b72cc9` to that file ONLY (`ab133dcc...1a3`) + this order's fix (`6c675c4c...bc6c`) -> sha256 `401a36ff675a4e0637b4e1de6baa2aeca5a1e64ec473336fac950f65b8f8f08d`, git blob `b0f8bc0add` (= the blob of commit `9b7256a99f`'s file). Applied cleanly, no conflict.
- Key (ONE): `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz`. Inflection and cottonwood keys are untouched.

## Blast radius

- **ONE S3 key, two members.** Writers of the served index: 1 (`HoldingsPublication.publish` via `land()`); rules read: 1 (the FWD-14 gate, unchanged code).
- Served change, on real 49F inputs (156,281 nodes both sides, same ids): **116,902 nodes differ, 39,379 byte-equal.**
  - **116,777 SmartX model-asset nodes newly carry a CUSIP `security_id`** (38 keep the source id with "no CUSIP in source" listed); all 116,815 SmartX nodes gain the `ticker=` fact; their class, sub-class, basis and `display.symbol` do not move.
  - **Custody (e56): 87 SECURITY nodes with a CUSIP id change (of 7,412), 32 newly classified, 0 lost** (the only class moves in the whole candidate).
  - 32,054 of 32,054 nodes the changes do not reach are byte-equal to base.
- Producer cost (row W269-S2, runtime, not repeated here): every SmartX symbol now hits the table, so the uncached CUSIP-key fallback is not exercised on them (symbol hit 116,777, symbol miss 0). With misses memoised the built run made 124,553 table lookups (1,934 distinct) against base 124,250 (1,782); the ~269 build made 241,330. What e56 still asks uncached is the custody CUSIP misses (about 300 more lookups than base, 152 more distinct keys); the scheduled fire runs the uncached code and its wall time is NOT measured here (the three replays ran in parallel on a laptop: base 569.6 s, built 575.6 s, ~269 build 379.9 s before it refused).
- No new put key class: `holdings/current` and `holdings/date=<d>`; no IAM step. Puts rise 195 -> 204 because the SmartX drill files carry the new facts.

## The landing path (the 402 packet's: digest-gated, NEVER a mint)

`safe-deploy.sh --mint-bundle` builds from the tree and ships more members; do not use it.

0. **Ledger:** open an `org/critical_paths/change_management/` entry BEFORE the upload; it names the one key and every family that pulls it (`irpt-holdings-refresh-lambda`, the 49F SSM command). Close it after the after-read.
1. **Precheck:** `bash .tools/aws s3api head-object --bucket opal-data-49financial --key irpt/49financial/code/gold/investor-reporting-holdings.tar.gz` -> ETag must be `01387cef54b9e15e10023f05029e357d` and `VersionId` the version IB-pr-404 landed (read today: `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`). Anything else is a STOP.
2. **Rebuild** in empty directories outside the worktree, python 3.12 (3.14 writes different gzip bytes): `get-object --version-id <that version>` -> `extract_bundle.py` (~266) -> apply the three diffs named above (`git diff 01e843ce2e^ 01e843ce2e`, `git diff dfa9b72cc9^ dfa9b72cc9`, `git diff 9b7256a99f^ 9b7256a99f`, each to its ONE file, `git -c core.autocrlf=false -c core.eol=lf apply`) -> `py -3.12 -I narrow_pack.py <repo> <tree> out.tar.gz` (~266, no member argument).
3. **Digest gate:** sha256 `47be54d6...dda5` and md5 `1e8ff309...712e4a`. A different digest is a STOP and a row; never upload other bytes.
4. **Upload** with the mint's call shape: `aws s3 cp out.tar.gz s3://opal-data-49financial/<key> --metadata members-sha256=96925f389381e64beeeb31ebf61eecdd5335fddf30cce0335300b455979bfd62,member-count=44`; `head-object` must echo ETag = built md5 and both metadata values.
5. Rerun the replay (`replay_driver_cached.py`, `compose_410.py`) against the UPLOADED bytes before the first fire; stop the apply if `fwd14_gate_unchanged` is not `identical`.

## Branch A (released)

Steps 0-5, then the after-read. With these bytes the first fire PUBLISHES (replay: conditions none, `new_unclassified` 0); the served index gains 116,777 CUSIP ids on SmartX model assets and 32 newly classified custody securities, and nothing else moves in class.

## Branch B (rolled back)

Copy back **the version IB-pr-404 landed, read at apply time** (`head-object` of the key just before the upload: today `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`, ETag `01387cef54b9e15e10023f05029e357d`, metadata `members-sha256=f3247ea2964f9daae8d8439431cbbfae99108d39c50774b234821462c1d5d036`, `member-count=44`, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901`; **re-read it at apply**):
`aws s3api copy-object --bucket opal-data-49financial --key irpt/49financial/code/gold/investor-reporting-holdings.tar.gz --copy-source "opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz?versionId=irUPjpfrDLoM2zhnhunbBtIG9fP275kI"`, then `head-object` (the copy writes a NEW version id; the ledger records it). The next fire then runs the base bytes.

## The after-read

A refused fire exits 0 and the SSM command reads Succeeded either way: read the output line and the record, never the SSM status. After the first 10:15 ET fire after the upload:
- PUBLISHED (expected): `OK: 49financial business_date=<d> ...`; `current/manifest.json` has a new version at the fire's business date; no `publish_refusal.json` newer than the command.
- REFUSED (the ~269 build's outcome; would mean other bytes ran or the inputs moved): `REFUSED: 49financial keeps its last good publication; classified_security_lost(<n>)...`. Stop and roll back (Branch B).
- Either line proves the gate ran; neither means the old bundle ran (check the key's version).

## Who signs

This pair is ~P2's COO half (`2.0.0_SA_COO~P2`), dell1 `2.0.0_SA_COO~M1`'s COO half for the e56 member (via MSTR), and the CTO half (`1.0.0_SA_CTO`).

## The red list (CTO ADDENDUM 18, row D2-S46)

ADDENDUM 18's list is the nine `_contracts` tests red at ~272's pin (`IB110-1_red_list.json`): `test_owned_request_contracts.py::test_public_routes_are_declared_against_the_installed_status_handler`; `test_upload_contract.py::test_route_denominators_are_measured_and_upload_is_declared_against_generate`; `tests/test_seam_paired.py::test_the_consumer_fixture_source_is_named_and_non_empty`; `::test_every_declared_route_has_a_response_contract_whose_refs_resolve`; and `::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[...]` for `analysis-request-original`, `custody-report-persist`, `custody-report-read`, `export-receipt`, `submit-export`. Targets: `infra/aws/lambda/investor-reporting/_contracts/`, `docs/contracts/investor-reporting/`, and the five operations above. Re-run at this cell's base (`pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/`): **4 failed, 194 passed** -- the `seam_paired` route-contract test and the control tests for `analysis-request-original`, `custody-report-persist`, `custody-report-read` (a subset of the nine; the base moved since ~272 -- row `IRPT_BCKEND-D2-W273-S1`). This cell's changed paths against its base are 2 (`data/assets/scripts/gold/investor_reporting/holdings_49f.py`, `.../tests/test_holdings_49f.py`) plus this folder; the packaged members' sources are the two `holdings_*.py` files. **Intersection with any target path or red operation name: none; STOP = no.** No 49F holdings test is on the red list.

## Replay (`IB111-1_49f_bundle_replay.json`, 9 arms, 3 negative controls)

Base, built and the ~269 build extracted into separate empty directories outside the worktree and driven by ~265's `replay_publish_gate.py run` (python -I) through ~269's `replay_driver_cached.py`; real inputs, real served index, writes captured in memory, nothing put anywhere. Verdicts: `fwd14_gate_unchanged` **identical**; `fwd14_gate_fixture_arms_unchanged` identical; `smartx_class_parity` **identical**; `symbol_miss_cusip_fallback` expected-diff (the fallback is present on built, absent on base; 116,777 symbol hits, 0 misses on the SmartX nodes, so it fires on none of them); `real_49financial_nodes` expected-diff; `custody_cusip_nodes_e56_fallback` expected-diff (32 newly classified, 0 lost); negative controls: `negative_control_mutant_gate_stubbed` (the gate arms discriminate), `negative_control_untouched_nodes_and_no_cusip_nodes` (32,054 of 32,054 untouched nodes byte-equal; 38 of 38 no-CUSIP SmartX nodes keep class), `negative_control_269_build_unfixed_403_still_refuses` (REFUSED, `classified_security_lost` 53; 13,892 SmartX nodes lose their class on that build, 0 on the fixed one). The client data used stays outside the repo and is deleted; the files here hold counts only.
