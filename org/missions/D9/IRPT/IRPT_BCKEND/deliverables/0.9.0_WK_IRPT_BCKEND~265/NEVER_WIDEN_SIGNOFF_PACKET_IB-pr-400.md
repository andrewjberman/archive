# Never-widen sign-off packet -- IB-pr-400 (release of IB-pr-393 + IB-pr-396): the holdings producer refuses a WORSE publication and keeps the last good one

Prepared by 0.9.0_WK_IRPT_BCKEND~265 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO msgs 2655, 2738, 2748; CVO msg 2744). Nothing here was uploaded, deployed, applied or written: BUILD_ONLY from a clean tree, offline replays, AWS reads only.
Files beside this packet: `IB102-4_release_census.json`, `IB102-4_release_replay.json`, `replay/replay_publish_gate.py` (the replay script), `replay/raw/gate_{built,prior,live}.json` (counts and hashes only, no id). Model: `..._IB-pr-389.md` (~200).

**READ THIS FIRST (row IRPT_BCKEND-D2-W265-S1, OBSERVATION, ARMED, disarm owner 2.0.0_SA_COO~P2).** The order says FWD-14's gate ships in `investor-reporting.tar.gz` (live `W2Wragr`). Measured, the scheduled holdings producer does not run that bundle.
`irpt-holdings-snapshot` (ENABLED, `cron(15 10 ? * MON-FRI *)` America/New_York) fires `irpt-holdings-refresh-lambda`, whose live `IRPT_HOLDINGS_BUNDLE_MAP` names THREE other objects, one per firm:
`s3://opal-data-<firm>/irpt/<firm>/code/gold/investor-reporting-holdings.tar.gz` (the standalone bundles `irpt_holdings_49f|inf|cot`, 44 members each, minted only by `--mint-bundle`). Each SSM command fetches that firm's object, verifies SHA256SUMS and runs `holdings_snapshot.py --firms <firm> --upload` from it
(`refresh_dispatch.py:65-75`). `investor-reporting.tar.gz` carries `holdings_snapshot.py` as one of its 12 members but none of its imports, so no scheduled fire executes that copy.
**A Branch A on the named key alone would read as released while the first scheduled fire still ran the ungated producer, and S392 would retire on a fire that cannot REFUSE.** This packet therefore states BOTH artifacts. The signers choose the set; the replay covers each.

## The pin and the builds

- **Release pin P: `6cbf2707cf4acccd2c9555ead458339350235745`** (branch `wk-IRPT_BCKEND-265`, box/dell2 after the round-102 drain). The code is `9af6811b61` (IB-pr-393, PRD v0.31 + v0.32) and `ce6e2a218e` (IB-pr-396, PRD v0.33), both in P.
- Built with the mint's own deterministic builder (`safe_deploy_core.build_bundle_payload` over `find_bundle(<name>)`), from a clean tree (porcelain 0 lines before and after), twice per artifact, byte-identical. No member of either bundle carries a DEPLOY-SERVE-HELD sentinel at P (`_serve_held_reason` over every `.py` member: none), so neither mint is refused by the hold.

| Artifact | Built sha256 | md5 (= the ETag a verified upload must echo) | bytes | live_before |
|---|---|---|---|---|
| ORDERED: `investor-reporting.tar.gz` (`mdpf` / `investor_reporting`) | `0d5959835432eba7be0154cbe1524a1b43abdd95c0cc0abf98069ce7216ab825` | `2562b15b40e677d3a912b729f897bf85` | 116,227 (12 members) | `W2WragrP52i8M7MfL22oXVPuHsTjyVLO` (2026-10-09T04:16:44Z, 112,861 bytes, ETag `5547fa5e6601c042beef7146c0064def`, sha256 `f6d48603a6496f78733312e49b0e279b0907288db3423575f735835e896a0118`, latest) |
| CONSUMER: `investor-reporting-holdings.tar.gz` x3 (`irpt_holdings_49f`, `_inf`, `_cot`) | `230d59e744cd9ab622e6c8d1e2c5237285cc590f58c39932e060330a401df278` (the same bytes for all three firms) | `daf12ecce111163b26ac1eece5212858` | 481,779 (44 members + SHA256SUMS) | 49financial `3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur` (2026-10-04T23:38:13Z, ETag `7a400c14...`); inflection `SuRm8tIYq9AKTbRD91SxTJp2Fh80CqCo` (2026-10-04T20:58:01Z, ETag `2b94e928...`); cottonwood `NZIQjid2En9Wbe8kM8ibfsIjxjDWKEoT` (2026-10-05T00:16:41Z, ETag `7a400c14...`) |

## Changed members and their owners

**ORDERED artifact: 1 of 12 changed versus `W2Wragr`, and it is FWD-14.** `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` (live `b4c1c984f6ad`, built `a9fe965f9e5a`; stamp `holdings-snapshot-sha256`). Owners: `9af6811b61` (`0.9.0_WK_IRPT_BCKEND~261`, IB-pr-393) and `ce6e2a218e` (`~263`, IB-pr-396).
The live blob equals the pre-393 file at `01e843ce2e`. No other member moved since `W2Wragr` (11 of 12 byte-identical). Non-FWD-14 changes: none.

**CONSUMER artifacts: 18 of 44 members changed versus the live per-firm bundle, 1 is FWD-14 and 17 are not.** Per firm the diff is the same 18 (inflection also differs in `systems.json`, live `e89058cbd1c4`). Owners are the commits since the live blob was minted:

| Member | Owner (latest) | FWD-14? |
|---|---|---|
| `holdings_snapshot.py` | `9af6811b61` + `ce6e2a218e` (~261, ~263); also `01e843ce2e` (`0.9.0_WK_MDPF_SECCLASS~51`, the e62/e56 port) | YES, plus a SECCLASS port inside the same file |
| `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` | `58772c1e86` (`0.9.0_WK_MDPF_STRATID~1`) | no |
| `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py` | `a85ecada1f` (`0.9.0_WK_MDPF_STRATID~2`) | no |
| `data/mdpf/scripts/gold/mdpf_category_registry.py` | `93de0c2336` (`~STRATID~2`) | no |
| `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json` | `01e843ce2e` (`0.9.0_WK_MDPF_SECCLASS~51`) | no |
| `infra/aws/lambda/investor-reporting/_ids/ids.py` | `11ba48fdc7` (`0.9.0_WK_IRPT_BCKEND~149`), `e962a5cb81` (`~141`) | no |
| `lib/trading_calendar.py` | `4b766e4e2d` (`0.9.0_WK_NFRA_CTLPLN~12`), `3d7fb62105` (`~NFRA_MCPINDEX~25`) | no |
| `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json` | `e15671f611` (`2.0.0_SA_COO~G`), `eb29bf7f37` (`4.0.0_SA_CRO`), LGIC_BLANKFIX workers | no |
| `infra/logic/registry/{exemptions,remediations,reporting_policies,resources,scopes,systems}.json` | `4.0.0_SA_CRO`, `0.9.0_WK_IRPT_ANLREQ~41` (`589aee38f0`), `0.9.0_WK_IRPT_DASHBD~52` (`5f962296ae`), `0.9.0_WK_MDPF_DEMQUE~2` | no |
| `data/firm_registry.json`, `docs/contracts/investor-reporting/v1/CurrencyAuthorities.json`, `.../schwab_account_codes.json` | `0.9.0_WK_NFRA_TRNSPT~3`, `0.0.0_AB_MSTR`, `0.9.0_WK_IRPT_BCKEND~66` (owner lists for these three are a superset: their live blob is not among the 40 latest commits of the path) | no |

**Flag: the consumer mint is not a pure FWD-14 release.** Its non-FWD-14 members move served output at two firms (replay below): the SECCLASS port and STRATID changes reclassify 87 of 154,473 nodes at 49financial and 236 of 17,840 at cottonwood (asset_class, asset_class_basis, sub_asset_class only); inflection is unchanged (0 of 36,232).
Whether those moves already hold their own signed halves is not in this cell; the signer reads them here before the consumer mint.

## What the release does

On an upload that captured the firm's index, `run_firm` compares the candidate with the publication served NOW (read by exact version) before `land()`. WORSE is any of SIX: reconcile difference above 0.01; any `multi_asset`; any class outside the six; a security classified at the prior and unclassified now;
an account lost; a source trading-day frontier older than the prior's. An account the firm's directory marks TERMINATED is LISTED, never refused (v0.32); where the firm's directory marks every entry UNKNOWN (cottonwood), account-lost is LISTED and never refuses by itself (v0.33), the other five still refuse.
A first publication is judged on the absolute conditions only. On WORSE: no `land()`, the index does not move, ONE refusal record per firm is written beside the manifest at `irpt/<firm>/platinum/holdings[_qa]/current/publish_refusal.json` (`address()` output), the run goes on to the next firm.
**The process exit stays 0 on a refusal** (`main()` returns 0 and prints `REFUSED: <firm> keeps its last good publication; <conditions>; record=<...>`), so the SSM command reads Succeeded: a refusal is read from the output line and the record, never from the command status.

## Writers of the changed properties

- **The ordered bundle object** `code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz`: 1 writer in code, `mint_bundle('mdpf','investor_reporting')` (`.tools/safe_deploy_core.py`). The observed `W2Wragr` put is attributed to no ledger entry (row IRPT_BCKEND-D2-W200-S1). N rules read: 1.
- **The three consumer objects** `irpt/<firm>/code/gold/investor-reporting-holdings.tar.gz`: 1 writer in code, `mint_bundle` via `--mint-bundle irpt_holdings_<short>` (`STANDALONE_BUNDLES`, never commit-routed; the only reference to the key is `.tools/safe_deploy_core.py:537,561`). The Terraform dispatch only READS them. N: 1.
- **The served index** `irpt/<firm>/platinum/holdings/current/manifest.json`: 1 writer, `HoldingsPublication.publish` (`publication.py:304`), reached through `land()`. This release adds a rule BEFORE that writer and no writer. N writers: 1; N rules read: 1 (the gate in `run_firm`).
- **The refusal record** `.../current/publish_refusal.json`: new key, 1 writer, `write_refusal_record`. No object exists at it today (all 3 firms, prod and QA, list-objects-v2).

## IAM read (never assumed)

The holdings writer role already covers `s3:PutObject` on the refusal record path at all 3 firms; **no grant is missing and the packet carries no IAM step.** Read 2026-10-09T07:3xZ (`iam list-role-policies`, `get-role-policy`, `s3api get-bucket-policy`, `get-object-lock-configuration`):

- Roles `irpt-49f-holdings-role`, `irpt-inf-holdings-role`, `irpt-cot-holdings-role`, inline policy statement `PublishOwnHoldings`: Allow `s3:PutObject`, `s3:GetObject`, `s3:GetObjectVersion` on `arn:aws:s3:::opal-data-<firm>/irpt/<firm>/{platinum,gold}/{holdings,holdings_qa}/*`. The refusal key matches `platinum/holdings/*` and `platinum/holdings_qa/*`, the same grant that lets the role write `current/manifest.json` beside it.
- Bucket policies: `DenyForeignFirmPrincipals` admits role names matching `*-49f-*`, `*-inf-*`, `*-cot-*` (the three roles match). The only write Deny that exists (cottonwood `DenyRestrictedWriteExceptBreakglass`) is scoped to `commonwealth/cottonwood/bronze/crm/*`. No Object Lock on any of the three buckets. The record is written without `IfMatch`/`IfNoneMatch`, so no extra action is needed.
- Not done: `iam:SimulatePrincipalPolicy` is AccessDenied to this reading identity, so no effective-permission simulation ran. The finding is the policy text plus the bucket policy. If the first refused fire cannot write the record, `run_firm` catches it, sets `refusal_record_error`, and the refusal still stands (the index does not move).

## Branch A (released)

0. **Ledger:** open `org/critical_paths/change_management/` entry BEFORE the first mint; it names every family that pulls a moved key: the ordered key is pulled by the directory refresh SSM commands (3 firms); the three consumer keys by the holdings dispatch (3 firms). Close it after the after-read.
1. **Decide the set (row W265-S1).** The scheduled fire needs step 3. Step 2 alone ships FWD-14 to no scheduled fire; it only keeps the ordered key honest (its `holdings_snapshot.py` is then the pin's, and the directory runner ignores it).
2. **Ordered key (the applier's path, DS lane):** `bash .tools/safe-deploy.sh data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` routes the member to `mint_bundle('mdpf','investor_reporting')`; head-object must show ETag `2562b15b40e677d3a912b729f897bf85` and every stamp; sha256 of the object `0d5959835432eba7be0154cbe1524a1b43abdd95c0cc0abf98069ce7216ab825`.
3. **Consumer keys:** `bash .tools/safe-deploy.sh --mint-bundle irpt_holdings_49f`, then `irpt_holdings_inf`, then `irpt_holdings_cot`; each must report `BUNDLE MINTED`, and head-object must show ETag `daf12ecce111163b26ac1eece5212858`. A firm whose mint fails is rolled back (Branch B) before the next fires: never leave the three firms on mixed behaviour past one fire.
4. **Before the first fire,** run the replay arm for the applier (below) against the bytes actually uploaded.
5. **Served effect:** on a fire where nothing is WORSE the firm publishes exactly what it publishes today (replay: nodes identical at 3 of 3 firms with the gate alone). A WORSE candidate is refused, the prior keeps serving, the record is written.
6. **Blast radius:** the 4 keys above plus, per firm, at most the one new `publish_refusal.json`. The served index changes only on a publishing fire, by the same two-tier write as today. The consumer mint additionally moves served classification at 49financial (87 nodes) and cottonwood (236 nodes), by the 17 non-FWD-14 members (see the flag).

## Branch B (rolled back)

- **Ordered key:** copy S3 version `W2WragrP52i8M7MfL22oXVPuHsTjyVLO` back over `code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz`; re-read: ETag `5547fa5e6601c042beef7146c0064def`, sha256 `f6d48603...0118`.
- **Consumer keys, per firm:** copy 49financial `3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur`, inflection `SuRm8tIYq9AKTbRD91SxTJp2Fh80CqCo`, cottonwood `NZIQjid2En9Wbe8kM8ibfsIjxjDWKEoT` back over each firm's key; re-read the ETag (`7a400c14...`, `2b94e928...`, `7a400c14...`). The packages have no other state; the next SSM run fetches whatever the key holds.
- **Never roll back through a WORSE window.** A rolled-back producer has no gate: the replay shows the live bundle publishes the worse candidate and moves the index (`worse_restored`, LIVE side). So: if a firm's `publish_refusal.json` is newer than its last index move (that firm is being protected right now), do not roll that firm back until the candidate is no longer WORSE or the signer accepts publishing it.
- No route, IAM, schedule, env or Terraform change to revert. No served key is written by this cell. A refusal record, once written, stays until overwritten; it names the served index version it was refused against, so a reader can tell it is stale once the index moves.

## The replay, and the arm for the applier (rerun before the ledger)

Recorded in `IB102-4_release_replay.json` (21 arms; trees extracted into separate empty directories, AWS reads only, writes captured in memory, scratch OUTSIDE the worktree and deleted). Trees: **built** (the consumer bundle at P), **live** (each firm's live consumer bundle), **prior** (the built tree with `holdings_snapshot.py` swapped for the live `W2Wragr` copy: FWD-14 isolated, which is exactly the ordered-artifact change).

- **Real inputs, FWD-14 isolated (ordered artifact): identical at 3 of 3 firms.** Same candidate nodes (sha256 equal) and same body apart from the run clock: 49financial 154,473 nodes / 7,620 accounts, cottonwood 17,840 / 859, inflection 36,232 / 862. Built gate = PUBLISHED, no condition, `new_unclassified` listed 0. The whole-revision hash differs only through `clocks.as_of_timestamp`, which is `datetime.now()` in the producer (`holdings_snapshot.py:2722`).
- **Real inputs, consumer artifact (live bundle versus built bundle):** inflection **identical** (0 of 36,232 nodes differ); 49financial **expected-diff** (87 nodes: `asset_class` 34, `asset_class_basis` 87, `sub_asset_class` 85); cottonwood **expected-diff** (236 nodes: `asset_class` 4, `asset_class_basis` 236, `sub_asset_class` 51). The difference is the 17 non-FWD-14 members (the gate does not touch nodes: the isolated arm above is identical). Built gate = PUBLISHED at all 3, so nothing is WORSE today.
- **QA worse/restored pair (3 firms, one run each): REFUSED, then PUBLISHED.** A classified security made unclassified: built REFUSED on `classified_security_lost` (1), index not moved, one refusal record; the restored candidate PUBLISHED and the index re-pointed. The live bundle publishes the worse candidate and moves the index (expected-diff).
- **An all-UNKNOWN firm losing an account: PUBLISHED and listed** (`account_lost_not_refused` = 1) at 3 of 3 firms; the landed revision is identical to the ungated tree's.
- **Negative controls (all verdict as expected):** an account the source records TERMINATED is listed, never refused (`closed_accounts_not_refused` = 1, PUBLISHED); a Monday candidate against Friday's served frontier is PUBLISHED (not stale); the gate stubbed to PUBLISHED publishes the same worse candidate and moves the index, so the REFUSED arm is the gate and not the fixture.
- Stop the apply if, against the uploaded bytes, the worse arm does not REFUSE with the index unmoved, or the restored arm does not PUBLISH, or a real-inputs arm is REFUSED for a firm whose served publication was not WORSE.
- To rerun against the uploaded bytes: extract each bundle into its own empty directory, then `python -I replay/replay_publish_gate.py run <tree> <scratch> <label> <firms>` once per tree (labels `built`, `prior`, `live_<short>`), and `python -I replay/replay_publish_gate.py compose <scratch> <out.json> <pin> built live` (merge the three `gate_live_*.json` into `gate_live.json` first). Run from a scratch directory outside the worktree; delete the scratch (it holds client node data) afterwards.

## The after-read

The first scheduled fire per firm after the mint (10:15 ET on the next trading day; the dispatch sends one SSM command per firm), read for each firm, never from the command status (a refusal exits 0):

- **PUBLISHED:** the command output prints `OK: <firm> business_date=<d> ...`; `current/manifest.json` has a new version whose `latest_date` is the fire's business date; no `publish_refusal.json` newer than that command.
- **REFUSED:** the output prints `REFUSED: <firm> keeps its last good publication; <condition(count)>; record=<...>`; `publish_refusal.json` exists with `refused_at` after the command started, `outcome` REFUSED, and `served.index_version` equal to the unchanged `current/manifest.json` version.
- Either answer is the proof the gate ran. **S392 retires then** (its manual read stands until the first scheduled fire is read, per PRD v0.31). A fire that prints neither line means the firm ran the old bundle (row W265-S1).
- Ledger: open before, close after. Rows to read with it: IRPT_BCKEND-D2-W265-S1 and IRPT_BCKEND-D2-W200-S1.
