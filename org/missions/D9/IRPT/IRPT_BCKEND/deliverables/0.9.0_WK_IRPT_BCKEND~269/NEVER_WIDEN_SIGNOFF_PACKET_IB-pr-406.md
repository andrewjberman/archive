# Never-widen sign-off packet -- IB-pr-406: the 49F holdings bundle with dell1's e56 CUSIP fallback and IB-pr-403's SmartX CUSIP ids

Prepared by 0.9.0_WK_IRPT_BCKEND~269 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed, applied or written: BUILD_ONLY, offline replays, AWS reads only.
Files beside this packet: `IB107-1_49f_bundle_census.json`, `IB107-1_49f_bundle_replay.json`, `IB107-1_49f_gate_analysis.json`, `IB107-1_49f_class_transitions.json` (counts only), `replay_driver_cached.py`, `compose_406.py`, `class_transitions.py`, `cmp_members.py`.
Order: CTO ruling D1-S8 AMENDMENT 2 @b58f09e1b8 (msg 3107). Row: `IRPT_BCKEND-D2-W269-S1` (BLOCKING), `IRPT_BCKEND-D2-W269-S2`.

## READ THIS FIRST: the built bytes are NOT releasable as the order is cut

**On real 49F inputs the built bundle's own FWD-14 publish gate REFUSES the candidate; the base publishes it.** Same served index, same business date (2026-10-08), same 155,019 node ids, same gate code (`evaluate_publish_gate` is byte-identical in both members).

| | Base (IB-pr-402 bytes) | Built (this packet) |
|---|---|---|
| gate outcome | PUBLISHED, conditions none, `new_unclassified` 0 | **REFUSED, `classified_security_lost` 53**, `new_unclassified` 6 |
| landed | 193 puts, index moves | 1 put (the refusal record); index does not move |

Landed as built, **49F's served holdings would stop moving**: every scheduled fire would REFUSE and write `publish_refusal.json`; the prior publication would keep serving, getting older. The blast radius is therefore not "no served change": it is a standing freeze of one firm's holdings publication until the bundle is rolled back (Branch B) or fixed.

**Mechanism (measured, counts only; `IB107-1_49f_class_transitions.json`).** IB-pr-403 replaces a SmartX model-asset node's TICKER `security_id` with a CUSIP one. `holdings_snapshot.fill_display` takes a node's `display.symbol` from a TICKER-namespaced `security_id` (or a `ticker=` fact); with a CUSIP id it gets neither, so on built **`display.symbol` is absent on 115,412 of 115,412** nodes that gained a CUSIP. `classify_security` (e56) then asks the canonical table with no symbol, asks it again for `CUSIP:<id>` -- the table answers for **1 of 115,412** -- and the bd-securities fallback answers by name:

- SmartX model-asset nodes, class state base -> built: classified -> classified 101,520; **classified -> unclassified 13,892**; unclassified -> classified 0. Of the 101,520 that stay classified, `asset_class_basis` moves TABLE -> NAME_ALIAS (101,519) and the class VALUE changes for 6,689 (structured -> alternatives 6,506; fixed_income -> equity 183).
- The gate's rule applied to the built candidate against the base nodes as the served stand-in names 53 CUSIP keys that are classified on custody nodes and unclassified on a SmartX node of the same CUSIP: exactly the 53 the real run reported.

The e56 fallback itself works where the order meant it to: **87 custody SECURITY nodes with a CUSIP id change (of 7,532), 32 of them newly classified, 0 lost**. So the defect is the interaction, not e56. **Inferred, NOT tested here:** e56 alone, or IB-pr-403 with the ticker kept visible to display/classification (for example a `ticker=` fact beside the CUSIP id), would not remove the ticker-table hits. One edit to IB-pr-403's holdings_49f.py (owner: its cell) and a rebuild would be the route; this packet does not make it (not in the grant).

If the pair signs anyway, sign knowing the above; the sections below describe the act exactly as the 402 packet's landing path does it.

## What is released, and from what

- **Base = IB-pr-402's built 49F bytes**, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` (md5/ETag `01387cef54b9e15e10023f05029e357d`, 468,666 bytes). Rebuilt from the rollback version `3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur` plus ~266's narrow member (python 3.12, LF): the digest equals the base. **The live object is those bytes**: version `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`, LastModified 2026-10-09T10:27:33Z, read by `get-object`, sha256 equal.
- **Built = `f8bd6f667d3820ca7318a8360d5801e8d80dc73f7412f9eff907034610b08819`**, md5 (= the ETag a verified upload must echo) `99b6a24b0145fdd26790b1ce0a6abb7c`, 469,452 bytes, 45 members. Packed twice, byte-identical.
- **Two members move** (the other 42 of 45 are byte-identical to the base; `SHA256SUMS` is the regenerated manifest):
  - `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py`: narrow member (`dfa017b8...6262a`) + the diff of `01e843ce2e` to that file ONLY -> sha256 `a9fe965f9e5ada7fe9b2278e2e596c32d48ae96e43df90ec90a22211e921ec62`, git blob `e39636c5a8` (the 402 packet's control reproduced: the blob of `ce6e2a218e`'s file).
  - `data/assets/scripts/gold/investor_reporting/holdings_49f.py`: the base member (blob `3ee9637a62`) + the diff of `dfa9b72cc9` to that file ONLY -> sha256 `5f1061e30edd813160e802ee9307c7a26548837fb744ef2c8a832417dca1a310`, blob `0eecfb976c`. Applied cleanly, no conflict.
- Pin `776d8300716e572ea95f13ecd8281e594c0443cb`. S3 user metadata the upload would carry: `members-sha256=5e1fb6cae18de61e7ab8bdce48bc083d2ef88fd06b80448f90826c6db0122307,member-count=44`.
- Key: `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz`. Inflection and cottonwood keys are untouched.

## Blast radius

- **ONE S3 key, two members.** Verified by reading both tars member by member: changed = `holdings_49f.py`, `holdings_snapshot.py`, `SHA256SUMS`.
- Served change, on real 49F inputs (business_date 2026-10-08, 155,019 nodes both sides, same ids):
  - **115,412 SmartX model-asset nodes newly carry a CUSIP** (38 keep the source id with "no CUSIP in source" listed; 0 ambiguous).
  - **Newly classified: 32** (custody nodes, via e56's `CUSIP:<id>`); **0 SmartX nodes** newly classified; **13,892 SmartX nodes lose their class**; 6,689 change class value.
  - 115,537 of 155,019 nodes differ (115,450 SmartX + 87 custody); the other 39,482 are byte-equal.
  - **But the candidate is REFUSED by the gate, so none of this is served**; what moves is "49F stops publishing".
- Writers of the served index: 1 (`HoldingsPublication.publish` via `land()`). N rules read: 1 (the FWD-14 gate, unchanged code).
- Producer cost, measured: with the canonical table's misses uncached, the same real run took **3,907.5 s on built against 443.4 s on base** (laptop, one sequential DynamoDB GetItem per CUSIP-key miss; 115,412 of them). With misses memoised in the replay driver (2,047 distinct keys) 330.7 s. Row W269-S2. The scheduled fire runs the uncached code.
- Plus, per fire, one `irpt/49financial/platinum/holdings/current/publish_refusal.json` (already covered by the holdings role's `PublishOwnHoldings`; no IAM step).

## The landing path (the 402 packet's: digest-gated, NEVER a mint)

`safe-deploy.sh --mint-bundle` builds from the tree and ships more members; do not use it.

0. **Ledger:** open `org/critical_paths/change_management/` entry BEFORE the upload; it names the one key and every family that pulls it (`irpt-holdings-refresh-lambda`, the 49F SSM command). Close it after the after-read.
1. **Precheck:** `bash .tools/aws s3api head-object --bucket opal-data-49financial --key irpt/49financial/code/gold/investor-reporting-holdings.tar.gz` -> ETag must be `01387cef54b9e15e10023f05029e357d` and `VersionId` the version IB-pr-404 landed (read now: `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`). Anything else is a STOP.
2. **Rebuild** in empty directories outside the worktree, python 3.12 (3.14 writes different gzip bytes): `get-object --version-id <that version>` -> `extract_bundle.py` (~266) -> lay the two built members over it (`git show <commit carrying this folder>` for the diffs in the census, applied with `-c core.autocrlf=false -c core.eol=lf`) -> `py -3.12 -I narrow_pack.py <repo> <tree> out.tar.gz` (~266, no member argument).
3. **Digest gate:** sha256 `f8bd6f66...b08819` and md5 `99b6a24b...b7c`. A different digest is a STOP and a row; never upload other bytes.
4. **Upload** with the mint's call shape: `aws s3 cp out.tar.gz s3://opal-data-49financial/<key> --metadata members-sha256=5e1fb6cae18de61e7ab8bdce48bc083d2ef88fd06b80448f90826c6db0122307,member-count=44`; `head-object` must echo ETag = built md5 and both metadata values.
5. Rerun the replay (`replay_driver_cached.py`, `compose_406.py`) against the UPLOADED bytes before the first fire; stop the apply if `fwd14_gate_unchanged` is not `identical`.

## Branch A (released)

Steps 0-5, then the after-read. **With these bytes the first fire REFUSES** (above); the release does not deliver the CUSIP or the e56 classifications to the served surface. Do not take Branch A until the REFUSED outcome is answered (fix and rebuild, or the signers accept a frozen 49F publication for a stated period).

## Branch B (rolled back)

Copy back **the version IB-pr-404 lands, read at apply time** (`head-object` of the key just before the upload: today `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`, ETag `01387cef54b9e15e10023f05029e357d`, metadata `members-sha256=f3247ea2964f9daae8d8439431cbbfae99108d39c50774b234821462c1d5d036`, `member-count=44`, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901`):
`aws s3api copy-object --bucket opal-data-49financial --key irpt/49financial/code/gold/investor-reporting-holdings.tar.gz --copy-source "opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz?versionId=<that version>"`, then `head-object` (the copy writes a NEW version id; the ledger records it). If a fire has already REFUSED, the key is being protected, not harmed: rolling back lets the next fire publish; check `publish_refusal.json` against the index before and after.

## The after-read

A refused fire exits 0 and the SSM command reads Succeeded either way: read the output line and the record, never the SSM status. After the first 10:15 ET fire after the upload:
- PUBLISHED: `OK: 49financial business_date=<d> ...`; `current/manifest.json` has a new version at the fire's business date; no `publish_refusal.json` newer than the command.
- REFUSED: `REFUSED: 49financial keeps its last good publication; classified_security_lost(<n>)...; record=<...>`; `publish_refusal.json` with `refused_at` after the command started and `served.index_version` equal to the unchanged manifest version. **This is the outcome the replay predicts.**
- Either line proves the gate ran; neither means the old bundle ran (check the key's version).

## Who signs

This pair is ~P2's COO half (`2.0.0_SA_COO~P2`), dell1 `2.0.0_SA_COO~M1`'s COO half for the e56 member (via MSTR), and the CTO half (`1.0.0_SA_CTO`).

## Replay (`IB107-1_49f_bundle_replay.json`, 8 arms, 2 negative controls)

Base and built extracted into separate empty directories outside the worktree and driven by ~265's `replay_publish_gate.py run` (python -I) through `replay_driver_cached.py`; real inputs, real served index, writes captured in memory, nothing put anywhere. Verdicts: `fwd14_gate_unchanged` **FAIL** (not the order's `identical`: PUBLISHED vs REFUSED, recorded as the world is); `fwd14_gate_fixture_arms_unchanged` identical; `negative_control_mutant_gate_stubbed` expected-diff; `symbol_miss_cusip_fallback` expected-diff (115,412 symbol misses, 1 CUSIP-key hit, 0 newly classified on SmartX); `real_49financial_nodes` expected-diff; `negative_control_untouched_nodes_and_no_cusip_nodes` expected-diff (32,037 of 32,037 untouched nodes byte-equal; 38 of 38 no-CUSIP SmartX nodes keep class); `custody_cusip_nodes_e56_fallback` expected-diff (32 newly classified, 0 lost); `smartx_model_asset_classification_moves` **FAIL** (13,892 lose their class). The client data used stays outside the repo and is deleted; the files here hold counts only.
