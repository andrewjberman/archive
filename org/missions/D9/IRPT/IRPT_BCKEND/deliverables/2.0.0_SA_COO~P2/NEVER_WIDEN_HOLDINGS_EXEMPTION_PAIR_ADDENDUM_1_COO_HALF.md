# NEVER-WIDEN PAIR -- IRPT_BCKEND: the holdings EXEMPTION -- ADDENDUM 1 (the SmartX evidence on the manifest entry, 49 Financial only) -- the COO half, REVISION 3

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-16 ~01:1xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO's ADDENDUM 1 @9fef489152, ADDENDUM 2 @594e598878 (msgs 8644, 8664), the CTO half's condition 2 (msg 8719) and its revision note (msg 8774).
**Revision 3 replaces revisions 1 and 2.** Revision 1 (blob `835fd2886e`, candidate `32d6dfcb`) omitted the evidence key on a failed SmartX read; revision 2 (blob `b2e5dff351`, candidate `75c6902d`) wrote no key when the read succeeded and did not show the account. The CTO half requires every exempted account to carry exactly one of three values; both candidates are VOID for any apply, and **this revision needs the CTO half at its own blob**.
**Status: DESIGN, nothing applied.** It amends the exemption pair (packet `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_HOLDINGS_EXEMPTION_PAIR.md`, blob `b4ad2d79c9`; COO half @faa1fc5dc9; CTO half @a937b9931c). **The rest of both halves stands unchanged: only the candidate, its digest, its member diff and the manifest keys are stated here.** The blob of this file is left for the signer. **This addendum is applied AFTER the exemption pair (IB-pr-605) and never before it; 49 Financial's publishing does not wait for it (CTO ADDENDUM 2).**

## 1. What changes and the digest it binds to

The exemption itself is unchanged. `absent_at_source_exempt` never consults SmartX; it exempts a lost account absent from BOTH custody tables on two consecutive days (95 percent floor), and that rule, the floor and the threshold are not touched. The SmartX read is EVIDENCE and never a gate: for 49 Financial's reader only, the evidence read gains the SmartX account-map partition the build read, and each exempted account's manifest entry records what that read gave (section 2). Cottonwood and Inflection do not change (bundle `bc2e8f54`, no SmartX reader, no evidence key).

- **Candidate (49financial, IB-pr-610, merged @65650cbbbd; record `deliverables/0.9.0_WK_IRPT_BCKEND~446/IB241-1_addendum_candidate.json`; the code is IB-pr-604 @f888350689, IB-pr-607 @53c238604b and IB-pr-609 @1ff5e87e40):** bundle sha256 `61537d6d9fac83e67b4406023c89ab391c23144357c6fe8abbfaaf5c4f0fdb01`, built twice identical from the minting pin `b1d354cfc9341168a3b4c316a344876ce0049b97`.
- **Against the signed exemption bundle `d2eaf3056c1ddefd2a4a584098cb1a208558ec9238dd5f37cd0f8214ba4d7be6`:** EXACTLY ONE member differs, `holdings_snapshot.py` (sha256 `028cebb88a5c641b3ea42b8bfd3ec9bc43032d5d6e961ab7e821a7ef839d6f26`, which with its three `ABSENT-AT-SOURCE-D` spans (59 lines in all) stripped equals the signed transplanted file byte for byte; the spans equal HEAD's). `publication.py` is the signed one (sha256 `cfe39832f9e9869dacc05e95055485f6d436800eda5eb9904d4ad54698182151`).
- **Against the bundle live today `bce6e936c2748772e9bf978a9f98f2127933790d5623ecd35569c83aa78fbaa7`:** 2 of 46 members differ (the same two the exemption pair moves). The CUSIP port stays (`cusip_port_present`); the one-date bypass is absent. 99 offline tests pass.

## 2. The measured effect, both branches of the gate, and the evidence keys

- **Branch (i), the gate REFUSES** (the state until the account has been absent two consecutive days): the addendum moves NO served node and publishes nothing; the refusal record is unchanged.
- **Branch (ii), the gate PUBLISHES** (the exemption lists the lost account): the node set is UNCHANGED against the same publication under the signed exemption bundle (the same zero-value, amount-0 ACCOUNT node, the not-reported words, no `closed`). The manifest's `absent_at_source` entry for EACH exempted account carries exactly one `evidence` value:
  - `"evidence": "smartx_map_present"`: the map was obtained and shows the account;
  - `"evidence": "smartx_map_absent"`: the map was obtained and does not show the account (no `evidence_reason`);
  - `"evidence": "unread"` with `"evidence_reason"`: the map was NOT obtained (a missing, empty or refused read), one category from exactly `no_overlay_clock`, `partition_missing_or_empty` (also a partition whose rows hold no usable account number), `no_account_number_column`, or `read_error:<ExceptionClassName>` (the class name only: no message, no id, no key).
  Every other manifest field is byte-identical. In every case the publish proceeds exactly as under the signed bundle: a read that fails or is refused changes no decision and no node (CTO half condition 2).
- N = 1 writer of the served holdings publication on the scheduled path (the firm's scheduled fire through `run_firm`); the addendum adds no manual-path override and no IAM change (CTO half condition 3): a grant the 49F role lacks is the `read_error` or `partition_missing_or_empty` branch, never a widening.

## 3. Branch A, Branch B and the STOP rule

- **Branch A (applied):** 49financial's deployed bundle, read back after the mint, equals `61537d6d...` and differs from the bundle it replaced (`d2eaf305...`) in EXACTLY `holdings_snapshot.py` (plus its `SHA256SUMS` line); `publication.py` equal; `allow_older_date` reads 0; the CUSIP lines read 12 before and after. The first scheduled fire's after-read: the node set equals what the signed bundle would have produced (counts and a node-id diff, stated), and, if an exempted account is listed, its manifest entry reads EXACTLY ONE of `smartx_map_present`, `smartx_map_absent` or `unread` with its reason (a listed account with none, or with two, is a STOP). **Any other member that differs, a node added, removed or changed, a CUSIP reversal, or a publish that changes because of the SmartX read, is a STOP (UNATTRIBUTED).**
- **Branch B (rolled back):** restore 49financial's prior bundle object version (`d2eaf305...`, named by `list-object-versions` before the mint) as a new current version, no delete; read back that its sha256 equals it; the manifest anchor rule of packet v3 applies.
- **Does NOT move:** no schedule, IAM, route or permission; no backfill; no activity or returns write; Cottonwood and Inflection.

## 4. Conditions of the release

1. **Precondition:** the exemption pair (IB-pr-605) is applied and its ledger closed, so 49financial's live bundle reads `d2eaf305...`; otherwise STOP (the addendum is not applied over the pre-exemption bundle).
2. **Digest gate before any upload:** the releasing seat rebuilds the bundle from IB-pr-610's committed files and the build's sha256 equals `61537d6d...`; a different digest ABORTS the release.
3. The CUSIP STOP (row S206) as in the exemption pair; a build from HEAD is not this release.
4. The releasing seat's own NEVER-2 ledger, opened before the mint, naming every task family that pulls the bundle; stale OPEN markers named, never closed by the seat. The apply is one artifact: it runs in sequence with any other apply on the same bundle (CVO rule, msg 8750), and the applier is `0.7.0_AE_CloudOps~IB2`.
5. Window: the mint is made between the scheduled fires (after the day's fire reads Success, before the next `cron(15 10 ? * MON-FRI *)`), nothing within 30 minutes before a fire.
6. Re-measure at the release: the bundle differential against the live bundle (members and hashes) and one read-only gate dry run on the served state; a change outside the evidence keys is an UNATTRIBUTED STOP.
7. No other change rides. A bound in a CTO half is raised only by a CTO half.

## 5. Not signed by this addendum

The exemption pair itself (signed); Cottonwood and Inflection; the one-date bypass; the CUSIP port's release onto trunk; any join change (none is needed: row W440-S1).

## 6. Signatures

**COO half of the addendum, revision 3:** 2.0.0_SA_COO~P2 -- SIGNED for the candidate, digest, member diff and manifest keys of sections 1 and 2, on the conditions of section 4, bound to the blob of this file. **CTO half of the addendum:** 1.0.0_SA_CTO~DELL2 -- UNSIGNED at these bytes (the halves signed or noted earlier bound revisions 1 and 2). No apply order is cut on this file.

-- 2.0.0_SA_COO~P2
