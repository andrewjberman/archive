# NEVER-WIDEN SIGNOFF PACKET -- IRPT_BCKEND IB-pr-528 (round 189, workstream ~P)

Order: IRPT_BCKEND.TO-IB-pr-528 (issued by 2.0.0_SA_COO~P2; CTO round-189 analysis item 2: "First check: FDRXX on Inflection resolves on the canonical branch. The packet counts what moves per firm against IB-pr-526's upper bounds, split by layer, as a never-widen packet. The apply waits for the pair.").
Worker: 0.9.0_WK_IRPT_BCKEND~375. Record: IB189-2_cash_rule_by_layer.json (same folder).
Scope: the holdings cash rule (build order IB-pr-527: a canonical etf-classifications row whose sub_asset_class is Cash serves the cash class). This packet is for the rule's LATER RELEASE. READ ONLY. Nothing was invoked, written, uploaded, applied, deployed, signed in, or sent to a vendor. Object bodies were read into scratch outside the worktree and counted; no holding value, account identifier or holding name is written here.

Base commit (worker HEAD before the first commit): 1d3605e19c5be48cbc0079705829b68e74b30b76.

## What the rule moves, and the cash definition

The cash definition is the sub-class Cash only: sub_asset_class trimmed and lower-cased equals cash, on a canonical row. Money Market and T-Bill sub-classes are NOT moved. The canonical table holds 365 cash-sub rows, 22 Money Market rows and 11 T-Bill rows; the last two stay fixed_income as the table serves them. The fallback layer (the bd-securities answer, basis NAME_ALIAS) is not changed by the rule: its cash-sub holdings stay as served.

## Counts per firm (newest ACCEPTED served snapshot; the upper bound is IB-pr-526's)

| firm | newest served date | SECURITY nodes | would move (upper bound) | canonical branch (blast radius) | fallback branch (stays as served) | upper bound delta |
|---|---|---|---|---|---|---|
| 49financial | 2026-10-12 | 124,441 | 32 | 32 | 0 | 0 |
| cottonwood | 2026-10-08 | 15,455 | 253 | 38 | 215 | 0 |
| inflection | 2026-10-12 | 34,273 | 841 | 774 | 67 | 0 |

The blast radius of the canonical-only rule is the canonical-branch column: 844 nodes across the three firms. Nothing else changes: not the sub-class, the basis, the weights or the totals (per the IB-pr-527 contract, which keeps sub, basis and class_source). The would-move column is an upper bound only; it includes the fallback layer, which the rule does not touch.

## The FDRXX check (CTO item 2)

The canonical row for FDRXX is found: fixed_income, sub Cash. Inflection's newest accepted snapshot holds 757 SECURITY nodes with display symbol FDRXX, all served fixed_income with sub Cash. The rule therefore reaches them on the canonical branch: resolves_on_canonical_branch is true and rule_scope is canonical_only.

## Branch A -- the act (the release, NOT run)

(a) The holdings producer that carries the rule is released. At the base commit no code carries the name apply_cash_rule: the rule is the IB-pr-527 build and is not in this tree. The release replaces the producer's deployed bytes with the rule-bearing build; its release mechanics belong to the release order and are not read here.
(b) Each firm's next scheduled fire re-publishes that firm's holdings through the publish gate below.

What was READ for Branch A: data/assets/scripts/gold/investor_reporting/holdings_snapshot.py (the publication runner, which writes the firm bucket and the platinum index) and infra/aws/terraform/investor-reporting/holdings/lambda.tf (the read-side Lambda irpt-holdings: artifact investor-reporting/irpt-holdings.zip, handler entry.lambda_handler). What was NOT read: the schedule and deploy target of the publication runner, and any live Lambda configuration. The scheduled fire times are not stated here.

## Branch B -- rollback

(a) Publication: the served manifest of each firm is object current/manifest.json. Its version served NOW, by a list-object-versions READ of that one named key (IsLatest), is:
- 49financial: daFZJt6f7G9.CXj3MJftFYV.DNUOVFQh (last modified 2026-10-13T14:20:49Z)
- cottonwood: lQMhNnImgj0ikICMdhFeasBGJKSbl55s (last modified 2026-10-09T14:18:11Z)
- inflection: MLSPlfHHsZa7mSnXEzorRkR9zgs2Q68u (last modified 2026-10-13T14:18:39Z)
Restoring the prior manifest version returns the prior publication: the key carries prior versions (14, 15 and 15 listed), and each dated object is named by its content revision. A new dated publication itself is not removed by that restore.
(b) Code: the rollback anchor of the producer is named at the release by a list-object-versions read of its bundle key; it is not named here.
What cannot be undone: a fire that has already published a date stays in the bucket as its own revision, and any reader that has already fetched a served page has the prior bytes.

## The publish gate

A rule-bearing candidate still meets the publish gate's six conditions: reconcile_difference, multi_asset, class_outside_six, classified_security_lost, account_lost and source_frontier_older. On WORSE the index does not move and one refusal record per firm is written beside the manifest. The rule adds no new condition. Cash is one of the six admitted classes, so the moved nodes are not outside the six.

Cottonwood: current/publish_refusal.json was last modified 2026-10-13T14:17:45Z (head-object read; the body was not read). The order states that Cottonwood's candidates have been refused since that time on one lost account; that cause is not verified here. The rule reaches Cottonwood's page only after that is resolved, and until then its served page stays at the 2026-10-08 publication.

## Layer fact

The fallback branch's cash-sub holdings stay as served: 49financial 0, cottonwood 215 (206 Black Diamond-prefixed identifiers, 6 CUSIP-shaped, 3 other shape), inflection 67 (no ticker-shaped display symbol). The rule does not change the bd-securities answer for money-market, sweep or cash-reserve names that have no canonical row.

## Signatures

COO half: 2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes.
CTO half: 1.0.0_SA_CTO -- UNSIGNED at these packet bytes.
The packet's own sha256 is left for the signers and is not computed here. Both halves are signed at these packet bytes before Branch A may run.

## What this packet did not measure

The publication runner's schedule and deploy target; the live configuration of any Lambda; the bucket versioning and IAM policy; the cause of the Cottonwood refusal (body not read); the fallback table (bd-securities); any holding value. Surprise rows IRPT_BCKEND-D2-W375-S1 to S4 carry the open definitional and locational points.
