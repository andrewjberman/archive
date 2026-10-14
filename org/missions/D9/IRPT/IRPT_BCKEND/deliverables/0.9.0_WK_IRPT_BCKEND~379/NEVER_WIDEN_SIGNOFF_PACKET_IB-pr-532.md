# NEVER-WIDEN SIGNOFF PACKET -- IRPT_BCKEND IB-pr-532 (round 191, workstream ~P)

Order: IRPT_BCKEND.TO-IB-pr-532 (issued by 2.0.0_SA_COO~P2; CTO round-191 analysis item 2 at 10401d0134: the never-widen packet and the COO half for ONE release of the holdings producer, carrying both changes, movers counted per firm and per change from the producer's own rules on each firm's newest candidate).
Worker: 0.9.0_WK_IRPT_BCKEND~379. Record: IB191-1_release_counts.json (same folder). Surprise rows: IRPT_BCKEND-D2-W379-S1 to S3 (INVESTIGATION_v1.md).
Scope: READ ONLY. Nothing was invoked, written, uploaded, applied, deployed, signed in, or sent to a vendor. The producer's publish path was not entered. Candidates were built in memory from read-only inputs; no holding value, account identifier or holding name is written here.

Base commit (worker HEAD before the first commit): 49467335d288d5c0012fe339c4cafcb74bd43fb5.

## Change set

Change 1, the IR cash rule on both layers: the canonical branch (merge dff35d95da, IB-pr-527) and the bd-securities fallback branch (merge 1464de48be, IB-pr-529). Both call apply_cash_rule on the return of classify_security. The rule changes asset_class only, to cash, where sub_asset_class trimmed and lower-cased equals cash.

Change 2, the publish-gate exemption repair: merge 4db49e0a27 (IB-pr-530). directory_marks_no_closures ignores carried-forward entries, so a lost account is listed rather than refused where the firm's own source marks every entry UNKNOWN.

Producer file: data/assets/scripts/gold/investor_reporting/holdings_snapshot.py, blob 3a19dcf5912798f7d94e9756ae04f64dd2ce7ea0 at 49467335d2. The blob at the release pin is to be re-read at the release; it is not the same claim as this packet until it is.

## Counts per firm (measured 2026-10-14, candidate business date 2026-10-12 for all three)

| firm | candidate nodes | canonical movers | fallback movers | total | vs round 189 (canonical, fallback) | gate before | gate after | lost accounts listed |
|---|---|---|---|---|---|---|---|---|
| 49financial | 156,521 | 32 | 0 | 32 | 0, 0 | PUBLISHED | PUBLISHED | 0 |
| cottonwood | 17,966 | 38 | 211 | 249 | 0, -4 | REFUSED (account_lost) | PUBLISHED | 1 |
| inflection | 36,702 | 774 | 67 | 841 | 0, 0 | PUBLISHED | PUBLISHED | 0 |

Public canonical symbols per firm (the record lists them): 49financial SNOXX, SNSXX, SNVXX, SWVXX; cottonwood FDRXX, SWVXX, VUSXX; inflection FDRXX, SPAXX.

Cash-sub SECURITY nodes that read cash with the rule and without it: 49financial 33 and 1; cottonwood 253 and 4; inflection 843 and 2.

## Branch A -- the act (NOT run)

Branch A is `bash .tools/safe-deploy.sh --mint-bundle` of each firm's standalone bundle: irpt_holdings_49f, irpt_holdings_cot and irpt_holdings_inf. Bundle key shape: s3 bucket of the firm, then irpt/<firm>/code/gold/investor-reporting-holdings.tar.gz. The current version id and sha256 per firm, from the census and re-read today (version ids and last-modified by head-object, sha256 carried from the census):
- 49financial: version UHOCIkWj3QiIzNucG1VjNnk_AufIg6oD, last modified 2026-10-13T13:35:24Z, sha256 f945da680596607ed152c4bc321c06b2b2b98908383279b67a4fb16758de8534.
- cottonwood: version oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_, last modified 2026-10-09T10:29:07Z, sha256 3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901.
- inflection: version PzhCs97qVBXkZcIjaOklHmzWiFsOFafM, last modified 2026-10-13T13:36:08Z, sha256 8709a0d5fd7b44e24cec91905837323d56091f59d6efaecdef7af7ea53c965c7.

The schedule the change rides: irpt-holdings-snapshot, cron(15 10 ? * MON-FRI *), America/New_York, ENABLED (scheduler read today). The FIRST scheduled fire after the mint is the first fire to carry the change; it is the first fire whose after-read is due in the release ledger. --mint-bundle opens no change-management ledger, so the releasing seat opens its own NEVER-2 ledger.

## Branch B -- rollback

Rollback: copy the prior bundle object version back over the same key (copy-object with CopySource VersionId), the prior version read at the release by list-object-versions on that one key. Per firm, the manifest version served NOW, by list-object-versions of the one named current/manifest.json key (IsLatest, read today, unchanged):
- 49financial: daFZJt6f7G9.CXj3MJftFYV.DNUOVFQh, last modified 2026-10-13T14:20:49Z.
- cottonwood: lQMhNnImgj0ikICMdhFeasBGJKSbl55s, last modified 2026-10-09T14:18:11Z.
- inflection: MLSPlfHHsZa7mSnXEzorRkR9zgs2Q68u, last modified 2026-10-13T14:18:39Z.

Restoring the bundle restores the code for the next scheduled fire. The manifest version above is the publication a reader is served until a fire publishes again.

What cannot be undone: a fire that has already published a date stays in the bucket as its own revision, and any reader that has already fetched a page holds the prior bytes.

## Blast radius per firm and per change

Nothing else changes: not the sub-class, the basis, the weights or the totals; the rule's own contract keeps sub and basis. Per firm:
- 49financial: the cash rule moves 32 canonical nodes (4 public symbols) and no fallback node. The exemption repair changes no gate outcome (PUBLISHED before and after, no lost account).
- cottonwood: the cash rule moves 38 canonical and 211 fallback nodes (249). The exemption repair turns a REFUSED candidate into a PUBLISHED one: the single account_lost condition is listed, one lost account (count only, never an identifier), and no other condition differs.
- inflection: the cash rule moves 774 canonical and 67 fallback nodes (841). No gate outcome changes.

The 49financial 2026-10-08 gap is a key the release must not widen or hide. The served index holds 10 dates, latest 2026-10-12, and 2026-10-08, a trading day, is absent: its 2026-10-09 scheduled fire was killed on the SSM execution timeout and no later fire replays a date. The release does not backfill 2026-10-08. A page that asks for 2026-10-08 on 49financial has no row before and after the release.

## The releasing seat's own NEVER-2 ledger

The releasing seat opens its own change-management entry at the start of the release, under org/critical_paths/change_management/, naming every leg:
1. the mint of irpt_holdings_49f, irpt_holdings_cot and irpt_holdings_inf (each a leg);
2. the FIRST scheduled fire's after-read per firm: each firm's current/manifest.json latest_date after the fire, and for cottonwood a business date past 2026-10-08 with its lost account listed (listed count 1 at this measurement);
3. the rule's after-read: FDRXX and the other Cash-sub holdings read Cash in the published page;
4. the 49financial 2026-10-08 gap, unchanged after the release.

The after-read states what to read; the value is measured then, not predicted here.

## Stop rule (both branches)

The release stops, and this packet is re-cut, unless at the release the counts match this packet: the per-firm canonical and fallback movers, the lost-account count, and the gate outcome and conditions before and after. A differing count means a different candidate. Cottonwood's fallback already differs from the round-189 figure (211 against 215; surprise row IRPT_BCKEND-D2-W379-S2), so its release count is compared with this packet, not with 215. Any condition other than account_lost that differs between the two gate runs also stops the release.

## Premises re-grounded

- 49financial served index: 10 dates, latest 2026-10-12, 2026-10-08 absent. Held.
- cottonwood served latest 2026-10-08; publish_refusal object present (last modified 2026-10-13T14:17:45Z). Held.
- The CTO expectation for Cottonwood, that the repaired exemption lists its lost account and publishes, is measured: listed 1, PUBLISHED. Held.
- Round-189/190 counts: 49financial and inflection equal; cottonwood canonical equal, fallback differs (see the stop rule).
- The layer of each mover is not on the node or in the census; it was read by re-running the producer's classifier (surprise row IRPT_BCKEND-D2-W379-S1).

## Signatures

COO half: 2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes.
CTO half: 1.0.0_SA_CTO -- UNSIGNED at these packet bytes.
The packet's own sha256 is left for the signers and is not computed here. Both halves are signed at these packet bytes before Branch A may run.

## What this packet did not measure

The release pin of the producer blob; bundle member contents beyond the census; the bundle sha256 values (carried from the census, not recomputed); any Lambda or SSM configuration beyond the census; the IAM policies; the cause of the Cottonwood refusal (body not read); the business-date discrepancy between the cutoff and the source date (surprise row IRPT_BCKEND-D2-W379-S3); any holding value.
