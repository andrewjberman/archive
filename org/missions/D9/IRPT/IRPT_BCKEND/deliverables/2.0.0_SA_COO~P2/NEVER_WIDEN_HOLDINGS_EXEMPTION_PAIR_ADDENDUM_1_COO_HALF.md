# NEVER-WIDEN PAIR -- IRPT_BCKEND: the holdings EXEMPTION -- ADDENDUM 1 (the evidence key `smartx_map_present`, 49 Financial only) -- the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~22:3xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO's ADDENDUM 1 @9fef489152 and ADDENDUM 2 @594e598878 (msgs 8644 and 8664).
**Status: DESIGN, nothing applied.** It amends the exemption pair (packet `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_HOLDINGS_EXEMPTION_PAIR.md`, blob `b4ad2d79c9`; COO half @faa1fc5dc9; CTO half @a937b9931c). **The rest of both halves stands unchanged: only the candidate, its digest, its member diff and the manifest key are stated here.** The addendum's blob is left for the signer. **This addendum is applied AFTER the exemption pair (IB-pr-605) and never before it; 49 Financial's publishing does not wait for it (CTO ADDENDUM 2).**

## 1. What changes and the digest it binds to

The exemption itself is unchanged. `absent_at_source_exempt` never consults SmartX; it exempts a lost account absent from BOTH custody tables on two consecutive days (95 percent floor), and that rule, the floor and the threshold are not touched. The addendum records the SmartX presence as evidence: for 49 Financial's reader only, the evidence read gains the SmartX account-map partition the build read, and an exempted account the map shows gets `"evidence": "smartx_map_present"` in its manifest entry. An entry for an account the map does not show is byte-identical to the signed pair's. Cottonwood and Inflection do not change (bundle `bc2e8f54`, no SmartX reader).

- **Candidate (49financial, IB-pr-606, merged @56d4c0fea7; record `deliverables/0.9.0_WK_IRPT_BCKEND~442/IB237-1_addendum_candidate.json`):** bundle sha256 `32d6dfcb9bd8aa83188821264dc3fa008422ae1565933eb32411148f74b2409d`, built twice identical from the minting pin `b1d354cfc9341168a3b4c316a344876ce0049b97`.
- **Against the signed exemption bundle `d2eaf3056c1ddefd2a4a584098cb1a208558ec9238dd5f37cd0f8214ba4d7be6`:** EXACTLY ONE member differs, `holdings_snapshot.py` (sha256 `f88185cfef9493edc0861e0899d9e25f90ebb59f00b84197178fa52f86dbc0c4`, which with its three `ABSENT-AT-SOURCE-D` spans (38 lines in all) stripped equals the signed transplanted file byte for byte; the spans equal HEAD's, IB-pr-604 @f888350689). `publication.py` is the signed one (sha256 `cfe39832f9e9869dacc05e95055485f6d436800eda5eb9904d4ad54698182151`).
- **Against the bundle live today `bce6e936c2748772e9bf978a9f98f2127933790d5623ecd35569c83aa78fbaa7`:** 2 of 46 members differ (the same two the exemption pair moves). The CUSIP port stays (`cusip_port_present`); the one-date bypass is absent (`allow_older_date` 0). 96 offline tests pass.

## 2. The measured effect, both branches of the gate

- **Branch (i), the gate REFUSES** (the state until the account has been absent two consecutive days): the addendum moves NO served node and publishes nothing; the refusal record is unchanged.
- **Branch (ii), the gate PUBLISHES** (the exemption lists the lost account): the node set is UNCHANGED against the same publication under the signed exemption bundle (the same zero-value, amount-0 ACCOUNT node, the not-reported words, no `closed`); the manifest's `absent_at_source` entry for an exempted account the SmartX map shows gains one key, `evidence` = `smartx_map_present`; every other entry and every other manifest field is byte-identical. If the SmartX partition is missing, empty or unreadable, the key is absent and the decision is the same.
- N = 1 writer of the served holdings publication on the scheduled path (the firm's scheduled fire through `run_firm`); the addendum adds no manual-path override.

## 3. Branch A, Branch B and the STOP rule

- **Branch A (applied):** 49financial's deployed bundle, read back after the mint, equals `32d6dfcb...` and differs from the bundle it replaced (`d2eaf305...`) in EXACTLY `holdings_snapshot.py` (plus its `SHA256SUMS` line); `publication.py` equal; `allow_older_date` reads 0; the CUSIP lines read 12 before and after. The first scheduled fire's after-read: the node set equals what the signed bundle would have produced (counts and a node-id diff, stated), and, if an exempted account is listed, its manifest entry carries the key. **Any other member that differs, a node added, removed or changed, a CUSIP reversal, is a STOP.**
- **Branch B (rolled back):** restore 49financial's prior bundle object version (`d2eaf305...`, named by `list-object-versions` before the mint) as a new current version, no delete; read back that its sha256 equals it; the manifest anchor rule of packet v3 applies.
- **Does NOT move:** no schedule, IAM, route or permission; no backfill; no activity or returns write; Cottonwood and Inflection.

## 4. Conditions of the release

1. **Precondition:** the exemption pair (IB-pr-605) is applied and its ledger closed, so 49financial's live bundle reads `d2eaf305...`; otherwise STOP (the addendum is not applied over the pre-exemption bundle).
2. **Digest gate before any upload:** the releasing seat rebuilds the bundle from IB-pr-606's committed files and the build's sha256 equals `32d6dfcb...`; a different digest ABORTS the release.
3. The CUSIP STOP (row S206) as in the exemption pair; a build from HEAD is not this release.
4. The releasing seat's own NEVER-2 ledger, opened before the mint, naming every task family that pulls the bundle; stale OPEN markers named, never closed by the seat.
5. Window: the mint is made between the scheduled fires (after the day's fire reads Success, before the next `cron(15 10 ? * MON-FRI *)`), nothing within 30 minutes before a fire.
6. Re-measure at the release: the bundle differential against the live bundle (members and hashes) and one read-only gate dry run on the served state; a change outside the evidence key is an UNATTRIBUTED STOP.
7. No other change rides. A bound in a CTO half is raised only by a CTO half.

## 5. Not signed by this addendum

The exemption pair itself (signed); Cottonwood and Inflection; the one-date bypass; the CUSIP port's release onto trunk; any join change (none is needed: row W440-S1).

## 6. Signatures

**COO half of the addendum:** 2.0.0_SA_COO~P2 -- SIGNED for the candidate, digest, member diff and manifest key of sections 1 and 2, on the conditions of section 4, bound to the blob of this file. **CTO half of the addendum:** 1.0.0_SA_CTO~DELL2 -- UNSIGNED at these bytes. No apply order is cut on this file.

-- 2.0.0_SA_COO~P2
