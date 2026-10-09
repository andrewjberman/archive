# Never-widen sign-off packet -- IB-pr-417: the 49F holdings bundle with dell1's e56 CUSIP fallback, IB-pr-403's SmartX CUSIP ids, the ticker= fact, and IB-pr-414's publish-gate memory fix

Prepared by 0.9.0_WK_IRPT_BCKEND~279 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed, applied or written: BUILD_ONLY, the memory harness and offline replays, AWS reads only.
Files beside this packet: `IB117-2_49f_bundle_census.json`, `IB117-2_49f_bundle_memory.json`, `IB117-2_49f_bundle_replay.json`, `compose_417.py`. Scripts reused unchanged: ~266's `extract_bundle.py` / `narrow_pack.py`, ~269's `replay_driver_cached.py` / `cmp_members.py`, ~265's `replay_publish_gate.py`, ~276's `mem_harness.py`.
Order: `IRPT_BCKEND.TO-IB-pr-417`; CTO ADDENDUM 19.1 and ADDENDUM 20 (@c3fd5df57a); rows D2-S56 (49F producer SIGKILLed on the 4 GiB box), `IRPT_BCKEND-D2-W276-S1`. **This packet SUPERSEDES `0.9.0_WK_IRPT_BCKEND~273/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-410.md`** (built `47be54d6479fdb849477a41b7cffa089319f2f18d38069b3384393fec192dda5`): that bundle's 49F producer peaks at 4.06e9 B on the memory harness, above the limit, so it is no longer the one to sign. IB-pr-413 applies THIS bundle once the pair signs.

## What changes against IB-pr-410, and why

IB-pr-410's two members, with ONE added diff: `3f2bdda578` (IB-pr-414) to `holdings_snapshot.py` ONLY. `holdings_49f.py` is IB-pr-410's member unchanged (sha256 `401a36ff...f8f08d`). The added diff changes the FWD-14 publish-gate code (`served_publication` folds the served publication's batches into keyed sets; `evaluate_publish_gate` reads them) and nothing of e56 or CUSIP; the candidate nodes the build produces are byte-equal to IB-pr-410's (156,281 of 156,281).

## Memory and time (one harness, run_firm on the real 49F inputs, business date 2026-10-08, writes captured in memory and discarded; sequential, alone, no memoisation; `IB117-2_49f_bundle_memory.json`)

| tree | peak working set (B) | wall (s) | table lookups |
|---|---|---|---|
| **this bundle** | **3,137,327,104** | **468.7** (cpu 349.0) | 123,315 |
| live 404 bundle (negative control) | 4,000,243,712 | 453.7 | 123,005 |
| IB-pr-410 members | 4,062,478,336 | 456.8 | 123,315 |

- Limit: 0.85 x 4 GiB = 3,650,722,201 B. This bundle is **0.859 of the limit** (0.731 of 4 GiB); the live bundle and IB-pr-410's both read ABOVE the limit (the order's negative control: the served-node list form peaks above the fixed bundle in 2 of 2 trees).
- Wall: 468.7 s against the 2 x 380.2 s = 760.4 s bound (pre-404 wall, ~276's census); the shared machine ran at similar load for all three trees (455 to 469 s).
- Comparability with the 4 GiB t3.medium is NOT measured on the box (no RSS was recorded there); the number that binds is the limit line, as in ~276's census.

## Replay, same real inputs and served index for every tree (`IB117-2_49f_bundle_replay.json`, 5 arms, 2 negative controls)

| arm | verdict | detail in counts |
|---|---|---|
| `fwd14_gate_vs_b410` | **identical** | gate PUBLISHED, conditions none, `new_unclassified` 0, uploaded, on BOTH trees; the whole decision (served node count 154,473 both) byte-equal; 5 of 5 fixture arms equal; candidate nodes sha256 equal |
| `smartx_class_parity` | **identical** | 116,815 SmartX nodes: classified -> classified 116,815, classified -> unclassified **0**; 0 differ from IB-pr-410's in class, sub-class or basis; `display.symbol` equal on 116,815 |
| `real_49financial_nodes_vs_b410` | identical | 156,281 nodes, 0 differ |
| `negative_control_served_node_list_form_peaks_above_fix` | expected-diff | the memory table above |
| `negative_control_mutant_gate_stubbed` | expected-diff | with the gate stubbed to PUBLISHED the worse fixture candidate publishes; the real gate refuses it |

## What is released, and from what

- **Base = the LIVE 49F bytes**, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` (md5/ETag `01387cef54b9e15e10023f05029e357d`, 468,666 bytes), version `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`, LastModified 2026-10-09T10:27:33Z, read by `get-object` and `head-object` today (2026-10-09 17:45Z): sha256 equal, version unchanged. Control: ~266's packer over the unpatched extracted live tree reproduces this sha256.
- **Built = `fe4000cbd31aaee971793854ad6cf26bc7b2d9a37a484e953896a09084f02f2e`**, md5 (= the ETag a verified upload must echo) `8b482c8db26c2e913aeee72023bacc7e`, 470,165 bytes, 45 members (python 3.12, LF). Packed twice, byte-identical. Pin `4b008d1521c0ded196623ce7323879aefd866b2a`. S3 user metadata the upload would carry: `members-sha256=73f33c3c59b77528c6eaaa56799e9c55f570a7adac23a0c6bcd12e66fe343a81,member-count=44`. Control 2: the same packer over IB-pr-410's member set reproduces `47be54d6...dda5`.
- **Two members move** (42 of 45 byte-identical to the base; `SHA256SUMS` is the regenerated manifest; read member by member with `cmp_members.py` over the live tree and the tree extracted from the BUILT tar):
  - `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py`: the live (narrow) member + the diff of `01e843ce2e` (dell1's e56; `2334c941...597fff`) + the diff of `3f2bdda578` (IB-pr-414; `ddd81013...16b6e`), each to that file ONLY -> sha256 `24c6ea6e1b8db2914a721a003768ca005878a1e3c9b12b5f1865171c69b5a42b` (equal to ~276's fix member). The tree's copy is untouched; the member is composed only here.
  - `data/assets/scripts/gold/investor_reporting/holdings_49f.py`: IB-pr-410's member, live + the diff of `dfa9b72cc9` (`ab133dcc...1a3`) + the diff of `9b7256a99f` (`6c675c4c...bc6c`) -> sha256 `401a36ff675a4e0637b4e1de6baa2aeca5a1e64ec473336fac950f65b8f8f08d`. Applied cleanly, no conflict.
- Key (ONE): `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz`. Inflection and cottonwood keys are untouched.

## Blast radius

- **ONE S3 key, two members.** Writers of the served index: 1 (`HoldingsPublication.publish` via `land()`); rules read: 1 (the FWD-14 gate, decisions unchanged on real inputs).
- **Served change, in counts** (real 49F inputs, 156,281 nodes both sides, same ids): **116,902 nodes differ, 39,379 byte-equal.**
  - **116,777 SmartX model-asset nodes newly carry a CUSIP `security_id`** (38 keep the source id); all 116,815 SmartX nodes gain the `ticker=` fact; their class, sub-class, basis and `display.symbol` do not move.
  - **Custody (e56): 87 SECURITY nodes with a CUSIP id change (of 7,412), 32 newly classified, 0 lost** (IB-pr-410's count; this bundle's candidate is byte-equal to IB-pr-410's).
  - The memory fix moves no served byte of its own: 0 of 156,281 candidate nodes differ from IB-pr-410's build.
- No new put key class: `holdings/current` and `holdings/date=<d>`; no IAM step. Puts rise as IB-pr-410 stated (the SmartX drill files carry the new facts).
- Producer cost on the harness: table lookups 123,315 (IB-pr-410's count); wall 468.7 s.

## The landing path (digest-gated, NEVER a mint)

`safe-deploy.sh --mint-bundle` builds from the tree and ships more members; do not use it.

0. **Ledger:** open an `org/critical_paths/change_management/` entry BEFORE the upload; it names the one key and every family that pulls it (`irpt-holdings-refresh-lambda`, the 49F SSM command). Close it after the after-read.
1. **Precheck:** `bash .tools/aws s3api head-object --bucket opal-data-49financial --key irpt/49financial/code/gold/investor-reporting-holdings.tar.gz` -> ETag must be `01387cef54b9e15e10023f05029e357d` and `VersionId` the version IB-pr-404 landed (read today: `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`). Anything else is a STOP.
2. **Rebuild** in empty directories outside the worktree, python 3.12 (3.14 writes different gzip bytes): `get-object --version-id <that version>` -> `extract_bundle.py` (~266) -> apply the four diffs named above (`git diff 01e843ce2e^ 01e843ce2e` and `git diff 3f2bdda578^ 3f2bdda578` to `holdings_snapshot.py`; `git diff dfa9b72cc9^ dfa9b72cc9` and `git diff 9b7256a99f^ 9b7256a99f` to `holdings_49f.py`; each to its ONE file, `git -c core.autocrlf=false -c core.eol=lf apply`) -> `py -3.12 -I narrow_pack.py <repo> <tree> out.tar.gz` (~266, no member argument).
3. **Digest gate:** sha256 `fe4000cb...2f2e` (full: `fe4000cbd31aaee971793854ad6cf26bc7b2d9a37a484e953896a09084f02f2e`) and md5 `8b482c8db26c2e913aeee72023bacc7e`. A different digest is a STOP and a row; never upload other bytes.
4. **Upload** with the mint's call shape: `aws s3 cp out.tar.gz s3://opal-data-49financial/<key> --metadata members-sha256=73f33c3c59b77528c6eaaa56799e9c55f570a7adac23a0c6bcd12e66fe343a81,member-count=44`; `head-object` must echo ETag = built md5 and both metadata values.
5. Rerun the replay (`replay_driver_cached.py`, `compose_417.py`) and the memory harness against the UPLOADED bytes before the first fire; stop the apply if `fwd14_gate_vs_b410` is not `identical` or the peak reads at or above 3,650,722,201 B.

## Branch A (released)

Steps 0-5, then the after-read. With these bytes the first fire PUBLISHES (replay: conditions none, `new_unclassified` 0) and the 49F producer fits the memory limit on the harness (0.859 of it); the served index gains 116,777 CUSIP ids on SmartX model assets and 32 newly classified custody securities, and nothing else moves in class.

## Branch B (rolled back)

Copy back **the live 404 version, read at apply time** (`head-object` of the key just before the upload: today `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`, ETag `01387cef54b9e15e10023f05029e357d`, metadata `members-sha256=f3247ea2964f9daae8d8439431cbbfae99108d39c50774b234821462c1d5d036`, `member-count=44`, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901`; **re-read it at apply**):
`aws s3api copy-object --bucket opal-data-49financial --key irpt/49financial/code/gold/investor-reporting-holdings.tar.gz --copy-source "opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz?versionId=irUPjpfrDLoM2zhnhunbBtIG9fP275kI"`, then `head-object` (the copy writes a NEW version id; the ledger records it). The next fire then runs the 404 bytes (which the 4 GiB box killed once: row D2-S56), so Branch B is a rollback of the apply, not a fix.

## The after-read

A refused fire exits 0 and the SSM command reads Succeeded either way: read the output line and the record, never the SSM status. After the first 10:15 ET fire after the upload:
- PUBLISHED (expected): `OK: 49financial business_date=<d> ...`; `current/manifest.json` has a new version at the fire's business date; no `publish_refusal.json` newer than the command; the SSM command is not SIGKILLed.
- REFUSED: `REFUSED: 49financial keeps its last good publication; classified_security_lost(<n>)...`. Stop and roll back (Branch B).
- Either line proves the gate ran; neither means the old bundle ran (check the key's version).

## Who signs

This pair is ~P2's COO half (`2.0.0_SA_COO~P2`), dell1 `2.0.0_SA_COO~M1`'s COO half for the e56 member (via MSTR), and the CTO half (`1.0.0_SA_CTO`).

## The red list (CTO ADDENDUM 18, row D2-S46)

ADDENDUM 18's list is the nine `_contracts` tests red at ~272's pin: `test_owned_request_contracts.py::test_public_routes_are_declared_against_the_installed_status_handler`; `test_upload_contract.py::test_route_denominators_are_measured_and_upload_is_declared_against_generate`; `tests/test_seam_paired.py::test_the_consumer_fixture_source_is_named_and_non_empty`; `::test_every_declared_route_has_a_response_contract_whose_refs_resolve`; and `::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[...]` for `analysis-request-original`, `custody-report-persist`, `custody-report-read`, `export-receipt`, `submit-export`. Targets: `infra/aws/lambda/investor-reporting/_contracts/`, `docs/contracts/investor-reporting/`, and the five operations above. Re-run at this cell's base (`py -3.12 -m pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/`, 2026-10-09 ~17:3xZ): **2 failed, 198 passed** -- `test_seam_paired.py::test_every_declared_route_has_a_response_contract_whose_refs_resolve` and `::test_control_...[analysis-request-original]`, both on the list. The packaged members' sources are exactly two files: `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` and `.../holdings_49f.py` (the bundle's changed members, from the census). **Intersection with any target path (`_contracts/`, `docs/contracts/investor-reporting/`) or red operation name: none; STOP = no.** No 49F holdings test is on the red list.

## Supersession

This packet supersedes IB-pr-410's (`0.9.0_WK_IRPT_BCKEND~273/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-410.md`). IB-pr-410's bundle is not to be applied; IB-pr-413 is re-pointed to this one by amendment once the pair signs. The client data used stays outside the repo and is deleted file by file; the files here hold counts, sha256 and reason codes only.
