# Never-widen sign-off packet -- IB-pr-402: FWD-14's holdings publish gate, NARROW, in the three per-firm holdings bundles

Prepared by 0.9.0_WK_IRPT_BCKEND~266 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. It supersedes the consumer-bundle leg of `..._IB-pr-400.md` (~265), which this packet narrows. Nothing here was uploaded, deployed, applied or written: BUILD_ONLY, offline replays, AWS reads only.
Files beside this packet: `IB103-2_narrow_bundle_census.json`, `IB103-2_narrow_bundle_replay.json`, `narrow_pack.py` (packer), `compose_narrow.py` (replay compose step), `extract_bundle.py`, `holdings_snapshot.narrow.py.txt` (the one narrow member, LF bytes).
Order: row `IRPT_BCKEND-D2-W265-S1` and its disposition `IRPT_BCKEND-D2-S37`: the scheduled producer `irpt-holdings-refresh-lambda` runs three per-firm bundles, and a fresh mint from HEAD would also ship 17 non-FWD-14 members (87 nodes reclassified at 49financial, 236 at cottonwood). This release ships none of them.

## What is released, and from what

- **Base commit: `9efbec3c2fd8867151f6f903dad796716ae2c577`.** Its `holdings_snapshot.py` blob (`98d4ae8218cb...`) is byte-equal to the live member of all three firm bundles (sha256 `55a5ac985aa2170b6d2170637497cfdbb61f24db13492bfe44057265cb75a2aa`).
- **Patch: the diffs of `9af6811b61` (IB-pr-393) and `ce6e2a218e` (IB-pr-396) to that one file, applied in that order to the live bytes.** Both applied cleanly (hunks at offset -17: the 17 lines `01e843ce2e` added ahead of them, which the live member lacks). `01e843ce2e` (MDPF_SECCLASS e62) is NOT applied; no other commit is. Control: narrow member + the `9efbec3c2f..01e843ce2e` diff reproduces git blob `e39636c5a8`, `ce6e2a218e`'s file, so the narrow member is the live member plus exactly the two commits. Narrow member sha256 `dfa017b824c1aba5c1107e53ef4811edaba93b2b7903c140208e41ab8866262a` (LF; the box git config has `core.autocrlf=true`, so apply with `-c core.autocrlf=false -c core.eol=lf` and read the committed file with `git show <commit>:<path>`, not a CRLF checkout).
- **Pin: `6f7ca4840e79d94ab2359e0409c9a80ac3d4b3c8`** (worktree HEAD of `wk-IRPT_BCKEND-266` when built; contains both FWD-14 commits).

| Firm | Key | rollback version (`live_before`) | live ETag / bytes | **Built sha256** | built md5 (= the ETag a verified upload must echo) | built bytes |
|---|---|---|---|---|---|---|
| 49financial | `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz` | `3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur` | `7a400c1482044ab80b45e5878b8f4ad5` / 465,247 | `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` | `01387cef54b9e15e10023f05029e357d` | 468,666 |
| inflection | `s3://opal-data-inflection/irpt/inflection/code/gold/investor-reporting-holdings.tar.gz` | `SuRm8tIYq9AKTbRD91SxTJp2Fh80CqCo` | `2b94e928cf3c070977fa28bf796763fd` / 465,015 | `7036a650703a04b18bcf251717c1310fc5553c817eb9d7ce34ec34ed678c9718` | `5daec38f0fbd604c65a770ce08029c67` | 468,435 |
| cottonwood | `s3://opal-data-cottonwood/irpt/cottonwood/code/gold/investor-reporting-holdings.tar.gz` | `NZIQjid2En9Wbe8kM8ibfsIjxjDWKEoT` | `7a400c1482044ab80b45e5878b8f4ad5` / 465,247 | `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` | `01387cef54b9e15e10023f05029e357d` | 468,666 |

49financial and cottonwood are the same bytes (their live bundles are too). The S3 user metadata each upload carries (as the live objects do): 49financial and cottonwood `members-sha256=f3247ea2964f9daae8d8439431cbbfae99108d39c50774b234821462c1d5d036,member-count=44`; inflection `members-sha256=0b1a3bf7077865054a330ba9360521425f6299bb1bb970766023d2011d70a093,member-count=44`.
Each live version was read by `s3api get-object --version-id` and was still the current version when read (`list-object-versions`, 2026-10-09T09:0xZ). Live md5 equals each ETag above.

## Blast radius

- **Three S3 keys, one member each.** Each key's object is replaced by a bundle whose 43 other members and their bytes are identical to live; the one moved member is `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py`; `SHA256SUMS` (regenerated, one line changed) is its manifest, not a second change. Verified by reading both tars member by member: changed members = `holdings_snapshot.py` + `SHA256SUMS`, at 3 of 3 firms.
- The ordered key `code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` is OUT of this release (no scheduled fire runs its `holdings_snapshot.py`; row W265-S1). It stays at `W2WragrP52i8M7MfL22oXVPuHsTjyVLO`.
- Plus, per firm, at most one NEW key `irpt/<firm>/platinum/holdings/current/publish_refusal.json`, written only on a refusal (the holdings role's `PublishOwnHoldings` already covers it: ~265's IAM read; no IAM step here).
- **Served output moves nowhere by this release.** On real inputs the narrow tree publishes the same nodes as the live bundle at 3 of 3 firms (0 of 154,473 / 17,840 / 36,232 nodes differ). Writers of the served index: 1 (`HoldingsPublication.publish` via `land()`); this release adds a rule before it. N rules read: 1.
- Writers of the three bundle keys: 1 in code (`mint_bundle`, via `--mint-bundle irpt_holdings_<short>`, which builds from the TREE and so would ship the 17 members); this packet's landing path replaces that writer for this act only.

## The landing path (NOT a mint from the tree)

`safe-deploy.sh --mint-bundle irpt_holdings_<short>` builds from the working tree and ships 18 changed members; do not use it for this release. The path that ships exactly the built bytes: rebuild them from the live version plus the committed narrow member, check the digest, then upload that file with the mint's own upload call shape.

0. **Ledger:** open `org/critical_paths/change_management/` entry BEFORE the first upload; it names the three keys and every family that pulls them (the holdings dispatch `irpt-holdings-refresh-lambda`, 3 firms, one SSM command each). Close it after the after-read.
1. **Precheck, per firm:** `bash .tools/aws s3api head-object --bucket opal-data-<firm> --key irpt/<firm>/code/gold/investor-reporting-holdings.tar.gz` -> `VersionId` must equal the rollback version above and ETag the live ETag. Anything else is a STOP (the live bundle moved since this packet).
2. **Rebuild, per firm, in empty directories outside the worktree** (python 3.12; **python 3.14 (zlib-ng) writes different gzip bytes and fails the digest**):
   `aws s3api get-object --bucket opal-data-<firm> --key <key> --version-id <rollback version> live.tar.gz`; `python -I extract_bundle.py live.tar.gz <empty live dir>`; `git show <the commit carrying this folder>:org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~266/holdings_snapshot.narrow.py.txt > narrow.py` (sha256 must be `dfa017b8...6262a`);
   `py -3.12 -I narrow_pack.py <repo root> <live dir> out.tar.gz data/assets/scripts/gold/investor_reporting/holdings_snapshot.py narrow.py`. The control (same command with no member arguments) reproduces the live tar.gz byte for byte, at 3 of 3 firms; run it once to show the packer is the live producer's.
3. **Digest gate:** sha256 and md5 of `out.tar.gz` must equal the table. A different digest is a STOP and a row; never upload a different byte set.
4. **Upload, one firm at a time** (the mint's own call shape): `aws s3 cp out.tar.gz s3://opal-data-<firm>/<key> --metadata members-sha256=<...>,member-count=44` (values above). `head-object` must then show ETag = built md5 and both metadata values echoed; `get-object` of the new version must hash to the built sha256. If a hook or policy refuses the direct put, that is a row for 2.0.0_SA_COO~P2, not a reason to mint from the tree.
5. **Do all three before the next fire, or roll the landed ones back (Branch B):** never leave the firms on mixed behaviour past one fire.
6. **Before the first fire,** rerun the replay for the applier against the uploaded bytes (below).

## Branch A (released)

Steps 0-6 above for the three keys, then the after-read. The first scheduled fire per firm (`irpt-holdings-snapshot`, ENABLED, `cron(15 10 ? * MON-FRI *)` America/New_York) runs the gated producer. A fire where nothing is WORSE publishes exactly what it publishes today (replay: nodes identical at 3 of 3 firms). A WORSE candidate is refused, the prior publication keeps serving, one record is written. S392 retires on the first fire read per the after-read below, not before.

## Branch B (rolled back)

Per firm, copy the `live_before` version back over the key and re-read the ETag:
`aws s3api copy-object --bucket opal-data-<firm> --key <key> --copy-source "opal-data-<firm>/<key>?versionId=<rollback version>"` (metadata is copied with the object), then `head-object`.

- 49financial: rollback version `3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur`; re-read ETag must be `7a400c1482044ab80b45e5878b8f4ad5`, metadata `members-sha256=099096b1560e926dd330ab2a2e1b900796daa49bf9b694409ed5fac0577055f4`, `member-count=44`.
- inflection: rollback version `SuRm8tIYq9AKTbRD91SxTJp2Fh80CqCo`; ETag `2b94e928cf3c070977fa28bf796763fd`, `members-sha256=7a02292cee4eab318c10a05a7b35d4bfc0e4589b63bfb51689572ed42a6e60d6`.
- cottonwood: rollback version `NZIQjid2En9Wbe8kM8ibfsIjxjDWKEoT`; ETag `7a400c1482044ab80b45e5878b8f4ad5`, `members-sha256=099096b1560e926dd330ab2a2e1b900796daa49bf9b694409ed5fac0577055f4`.

The copy writes a NEW version id (the key then serves the old bytes under it); the rollback version ids above name the bytes, and the ledger records the new id. **Never roll back through a WORSE window:** the live producer has no gate and publishes a worse candidate (replay `worse_restored`, LIVE side). If a firm's `publish_refusal.json` is newer than its last index move, that firm is being protected now; do not roll it back until the candidate is no longer WORSE or the signer accepts publishing it. No route, IAM, schedule, env or Terraform change to revert; the dispatch Lambda is not touched.

## The replay (`IB103-2_narrow_bundle_replay.json`, 18 arms, 9 negative controls)

Trees extracted into separate empty directories; ~265's `replay_publish_gate.py run` drives each tree's own `run_firm` (AWS reads only, writes captured in memory); `compose_narrow.py` pairs narrow with live per firm. Real inputs, business_date 2026-10-07.

- **`real_<firm>_live_vs_built`: identical at 3 of 3.** Same candidate nodes (sha256 equal) and same stable body; narrow gate PUBLISHED, no condition, `new_unclassified` 0; puts 192/192, 31/31, 55/55. 49financial 154,473 nodes / 7,620 accounts, cottonwood 17,840 / 859, inflection 36,232 / 862; node diff changed 0, only-in-one-side 0. The whole-revision hash differs only through `clocks.as_of_timestamp` (`datetime.now()`), excused by the order.
- **`fx_<firm>_worse_restored`: expected-diff at 3 of 3** (QA pair). Narrow: a classified security made unclassified is REFUSED (`classified_security_lost`), index not moved, one refusal record; the restored candidate PUBLISHES and re-points. Live bundle: the worse candidate is published and the index moves.
- `fx_<firm>_all_unknown_loses_account`: PUBLISHED and listed (`account_lost_not_refused` 1), landed revision identical to the live bundle's, at 3 of 3.
- Negative controls (9): `closed_account_not_refused` (TERMINATED listed, never refused), `monday_not_stale` (Monday vs Friday's frontier PUBLISHES), `mutant_gate_stubbed` (gate stubbed to PUBLISHED publishes the same worse candidate and moves the index, so the REFUSED arm is the gate and not the fixture), each at 3 firms.
- **Rerun against the uploaded bytes** (the applier, before the first fire): extract each uploaded bundle (`get-object` by the new version id) into its own empty directory, then from a scratch directory outside the worktree `python -I replay_publish_gate.py run <tree> <scratch> narrow_<short> <firm>` (~265's script; ~4-9 minutes per firm), the same for the rollback version as `live_<short>`, then `python -I compose_narrow.py <repo> <scratch> <out.json> <pin>`. Stop the apply if a `real_` arm is not identical, the worse arm does not REFUSE with the index unmoved, or the restored arm does not PUBLISH. Delete the scratch afterwards (it holds client node data).

## The after-read

A refused fire exits 0 (`main()` returns 0), so the SSM command reads Succeeded either way: **read the output line and the refusal record, never the SSM status.** Per firm, after the first scheduled fire after the upload (10:15 ET on the next trading day):

- **PUBLISHED:** the output prints `OK: <firm> business_date=<d> ...`; `current/manifest.json` has a new version whose `latest_date` is the fire's business date; no `publish_refusal.json` newer than the command.
- **REFUSED:** the output prints `REFUSED: <firm> keeps its last good publication; <condition(count)>; record=<...>`; `irpt/<firm>/platinum/holdings/current/publish_refusal.json` exists with `refused_at` after the command started, `outcome` REFUSED, and `served.index_version` equal to the unchanged `current/manifest.json` version.
- Either line proves the gate ran. A fire that prints neither means that firm ran the old bundle (check the key's version against the table).
- Ledger closed after the after-read. Rows to read with it: `IRPT_BCKEND-D2-W265-S1`, `IRPT_BCKEND-D2-S37`, `IRPT_BCKEND-D2-W266-S1`.
