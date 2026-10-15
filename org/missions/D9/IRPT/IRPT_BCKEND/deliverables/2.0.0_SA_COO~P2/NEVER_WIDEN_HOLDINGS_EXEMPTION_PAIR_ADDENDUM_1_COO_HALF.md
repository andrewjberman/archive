# NEVER-WIDEN PAIR -- IRPT_BCKEND: the holdings EXEMPTION -- ADDENDUM 1 (the SmartX evidence on the manifest entry, 49 Financial only) -- the COO half, REVISION 2

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-16 ~00:0xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO's ADDENDUM 1 @9fef489152, ADDENDUM 2 @594e598878 (msgs 8644, 8664) and the CTO half's condition 2 (msg 8719).
**Revision 2 replaces revision 1 (blob `835fd2886e`, committed @531bd4dd52, candidate `32d6dfcb`).** Revision 1 is VOID for any apply: its candidate omits the evidence key when the SmartX read fails, which the CTO half forbids (condition 2: the key reads `unread` with the reason, never omitted silently). The CTO half signed at blob `835fd2886e` does not bind these bytes; **this revision needs the CTO half at its own blob**.
**Status: DESIGN, nothing applied.** It amends the exemption pair (packet `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_HOLDINGS_EXEMPTION_PAIR.md`, blob `b4ad2d79c9`; COO half @faa1fc5dc9; CTO half @a937b9931c). **The rest of both halves stands unchanged: only the candidate, its digest, its member diff and the manifest keys are stated here.** The blob of this file is left for the signer. **This addendum is applied AFTER the exemption pair (IB-pr-605) and never before it; 49 Financial's publishing does not wait for it (CTO ADDENDUM 2).**

## 1. What changes and the digest it binds to

The exemption itself is unchanged. `absent_at_source_exempt` never consults SmartX; it exempts a lost account absent from BOTH custody tables on two consecutive days (95 percent floor), and that rule, the floor and the threshold are not touched. The SmartX read is EVIDENCE and never a gate: for 49 Financial's reader only, the evidence read gains the SmartX account-map partition the build read, and each exempted account's manifest entry records what that read gave (section 2). Cottonwood and Inflection do not change (bundle `bc2e8f54`, no SmartX reader).

- **Candidate (49financial, IB-pr-608, merged @860e265792; record `deliverables/0.9.0_WK_IRPT_BCKEND~444/IB239-1_addendum_candidate.json`; the code is IB-pr-604 @f888350689 and IB-pr-607 @53c238604b):** bundle sha256 `75c6902d391dc733228df296319a244d2a5ac2de43dd0d781cf4166fd86f8f7c`, built twice identical from the minting pin `b1d354cfc9341168a3b4c316a344876ce0049b97`.
- **Against the signed exemption bundle `d2eaf3056c1ddefd2a4a584098cb1a208558ec9238dd5f37cd0f8214ba4d7be6`:** EXACTLY ONE member differs, `holdings_snapshot.py` (sha256 `bd6daf6ba3cbd5472d7bfd0a0b6b78241e5030b41c71dd90bcb27b001da9cbf4`, which with its three `ABSENT-AT-SOURCE-D` spans (56 lines in all) stripped equals the signed transplanted file byte for byte; the spans equal HEAD's). `publication.py` is the signed one (sha256 `cfe39832f9e9869dacc05e95055485f6d436800eda5eb9904d4ad54698182151`).
- **Against the bundle live today `bce6e936c2748772e9bf978a9f98f2127933790d5623ecd35569c83aa78fbaa7`:** 2 of 46 members differ (the same two the exemption pair moves). The CUSIP port stays (`cusip_port_present`); the one-date bypass is absent. 98 offline tests pass.

## 2. The measured effect, both branches of the gate, and the evidence keys

- **Branch (i), the gate REFUSES** (the state until the account has been absent two consecutive days): the addendum moves NO served node and publishes nothing; the refusal record is unchanged.
- **Branch (ii), the gate PUBLISHES** (the exemption lists the lost account): the node set is UNCHANGED against the same publication under the signed exemption bundle (the same zero-value, amount-0 ACCOUNT node, the not-reported words, no `closed`). The manifest's `absent_at_source` entry for an exempted account gains keys by what the SmartX read gave:
  - the map was obtained and shows the account: `"evidence": "smartx_map_present"`;
  - the map was NOT obtained (a missing, empty or refused read): `"evidence": "unread"` and `"evidence_reason": <one category>`, from exactly `no_overlay_clock`, `partition_missing_or_empty` (also a partition whose rows hold no usable account number), `no_account_number_column`, or `read_error:<ExceptionClassName>` (the class name only: no message, no id, no key);
  - the map was obtained and does not show the account: NO evidence key (the entry is byte-identical to the signed bundle's).
  Every other manifest field is byte-identical. In every case the publish proceeds exactly as under the signed bundle: a read that fails or is refused changes no decision and no node (CTO half condition 2).
- N = 1 writer of the served holdings publication on the scheduled path (the firm's scheduled fire through `run_firm`); the addendum adds no manual-path override and no IAM change (CTO half condition 3): a grant the 49F role lacks is the `read_error` or `partition_missing_or_empty` branch, never a widening.

## 3. Branch A, Branch B and the STOP rule

- **Branch A (applied):** 49financial's deployed bundle, read back after the mint, equals `75c6902d...` and differs from the bundle it replaced (`d2eaf305...`) in EXACTLY `holdings_snapshot.py` (plus its `SHA256SUMS` line); `publication.py` equal; `allow_older_date` reads 0; the CUSIP lines read 12 before and after. The first scheduled fire's after-read: the node set equals what the signed bundle would have produced (counts and a node-id diff, stated), and, if an exempted account is listed, its manifest entry reads `smartx_map_present` or `unread` with its reason (a listed account with neither key, while the read obtained the map, is the third case above and is stated, not a STOP). **Any other member that differs, a node added, removed or changed, a CUSIP reversal, or a publish that changes because of the SmartX read, is a STOP (UNATTRIBUTED).**
- **Branch B (rolled back):** restore 49financial's prior bundle object version (`d2eaf305...`, named by `list-object-versions` before the mint) as a new current version, no delete; read back that its sha256 equals it; the manifest anchor rule of packet v3 applies.
- **Does NOT move:** no schedule, IAM, route or permission; no backfill; no activity or returns write; Cottonwood and Inflection.

## 4. Conditions of the release

1. **Precondition:** the exemption pair (IB-pr-605) is applied and its ledger closed, so 49financial's live bundle reads `d2eaf305...`; otherwise STOP (the addendum is not applied over the pre-exemption bundle).
2. **Digest gate before any upload:** the releasing seat rebuilds the bundle from IB-pr-608's committed files and the build's sha256 equals `75c6902d...`; a different digest ABORTS the release.
3. The CUSIP STOP (row S206) as in the exemption pair; a build from HEAD is not this release.
4. The releasing seat's own NEVER-2 ledger, opened before the mint, naming every task family that pulls the bundle; stale OPEN markers named, never closed by the seat. The apply is one artifact: it runs in sequence with any other apply on the same bundle (CVO rule, msg 8750), and the applier is `0.7.0_AE_CloudOps~IB2`.
5. Window: the mint is made between the scheduled fires (after the day's fire reads Success, before the next `cron(15 10 ? * MON-FRI *)`), nothing within 30 minutes before a fire.
6. Re-measure at the release: the bundle differential against the live bundle (members and hashes) and one read-only gate dry run on the served state; a change outside the evidence keys is an UNATTRIBUTED STOP.
7. No other change rides. A bound in a CTO half is raised only by a CTO half.

## 5. Not signed by this addendum

The exemption pair itself (signed); Cottonwood and Inflection; the one-date bypass; the CUSIP port's release onto trunk; any join change (none is needed: row W440-S1).

## 6. Signatures

**COO half of the addendum, revision 2:** 2.0.0_SA_COO~P2 -- SIGNED for the candidate, digest, member diff and manifest keys of sections 1 and 2, on the conditions of section 4, bound to the blob of this file. **CTO half of the addendum:** 1.0.0_SA_CTO~DELL2 -- UNSIGNED at these bytes (the half signed at blob `835fd2886e` bound revision 1). No apply order is cut on this file.

-- 2.0.0_SA_COO~P2
