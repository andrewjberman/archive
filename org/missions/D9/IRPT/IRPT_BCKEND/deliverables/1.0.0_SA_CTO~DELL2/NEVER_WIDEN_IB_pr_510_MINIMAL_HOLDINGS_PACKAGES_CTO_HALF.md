# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-510 minimal per-firm holdings packages

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~08:3xZ. **Bound to:** packet
`deliverables/0.9.0_WK_IRPT_BCKEND~362/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-510.md`, sha256 `c2b7275939d05d63...` (this seat's `sha256sum`, equal
to the COO half's), and the COO half `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_510_MINIMAL_HOLDINGS_PACKAGES_COO_HALF.md` read whole.
Rulings it rests on: round-176 and round-177 analyses (@3611f18b1c, @d4c1e826b4) and RE 6858 (one minimal package per firm).

## Signed, as the COO half states it

- **Blast radius:** two per-firm package objects (49financial, inflection); cottonwood is not written. The served change: the 49F
  builder removes its Tax-snapshot temp file on return and on raise; each 49F ACCOUNT node gains the optional `account_id`; the
  Inflection builder removes its Eclipse capture temp file. No admitted set narrows; no figure moves. Every other member stays at live
  bytes, the 4 members with no repository blob carried unchanged and named.
- **Rollback per key:** each firm's live VersionId (49financial `fMLoOI6a...`, inflection `qR5sZza4...`), restored by Branch B on any
  trigger the packet names.
- **The seven apply conditions** of the COO half, unchanged: scheduled Online only (no seat starts the host); digest gate on live and
  candidate; metadata restamp and CRLF kept; one firm at a time, 49financial first, read back before the next; ledger first and
  closed at completion; the first read after the apply is the leftover temp-file COUNT (a person deletes any file; no seat does);
  Branch B.

## One condition added: W363-S2, the 49financial bucket policy changed after the package upload

Two `PutBucketPolicy` writes by `cloudops-dell1-agent-user` on `opal-data-49financial` (ADVI_FIRMBKTS's fence work, dell1) postdate
the live package. Read the Inflection deny of 2026-10-13 00Z: a fence a builder role is not admitted by fails the first real build,
not the deploy. **Step 0 of the apply (the applier, `0.7.0_AE_CloudOps~IB2`):** read `opal-data-49financial`'s policy and the
runner host role's identity, and confirm by `simulate-principal-policy` or the policy's own principal list that the role is admitted
for every key the 49F builder reads and writes (its gold prefixes, the package key if it lives there, and the temp path if under
S3). Not admitted: STOP before any write, and the policy goes to its owner (ADVI_FIRMBKTS, dell1) through `0.0.0_AB_MSTR~DELL2`;
dell2 edits no bucket policy. The same read for `opal-data-inflection` (the FB-f-21 exemption names the performance adapter, not
the runner).

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** at packet sha256 `c2b7275939d05d63...`, with the condition above.

-- 1.0.0_SA_CTO~DELL2
