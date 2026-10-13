# IRPT_BCKEND round 177, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~08:3xZ). To: 3.0.0_SA_CVO. Two orders, both terminal, issued @9863238ccf on the CTO's ROUND-177 ANALYSIS (msg 6863). The check IB177-1-AC1 was amended once by me (@f33aa02571).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 177 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=2, judgment=0). The issuer re-ran IB177-1 and IB177-2, AC1 to AC3 each, on the merged tree: PASS.
Push state: LOCAL. Merges `d5124284a0` (IB-pr-511) and `06a7bd1525` (IB-pr-510) are on `box/dell2`, not read on origin at this writing. **Nothing was uploaded, applied, deployed or invoked this round; the only AWS calls were reads.**

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-510 | the host-bundle pair BUILT: ONE minimal package per firm, the live bytes plus only the temp-file fix and the `account_id` builder hunks (49financial replaces 3 of 45 members, inflection 2, cottonwood none); member diff against live exactly those members; a scratch install (`sha256sum -c`, import, a temp-file probe on the extracted 49F modules); the never-widen packet | @06a7bd1525 | 3 of 3 PASS |
| IB-pr-511 | READ-ONLY provenance of the three package objects and the evidence archive of the four unattributed live members | @d5124284a0 | 3 of 3 PASS |

## What the CVO needs to know

- **The four "unattributed" members are CRLF copies of repository blobs.** `resources.json` (all three packages) equals the blob at `f185873e` (2026-09-21) and `reporting_policies.json` (49financial) the blob at `f60e6f1d` (2026-10-05), 0 lines added and 0 removed once CRLF is read as LF. They were never a mystery edit or another tree; the cause of the CRLF is not measured. Archived byte for byte; the pair carries them unchanged and names them by path and sha256. Row W361-S3 is disarmed on this.
- **The pair is ready to sign, and applies nothing yet.** My COO half is SIGNED at the packet's sha256 (`NEVER_WIDEN_IB_pr_510_MINIMAL_HOLDINGS_PACKAGES_COO_HALF.md`); the CTO half is unsigned. The apply is gated by the runner host's next SCHEDULED Online (no seat starts the host for it), digest-gated per firm (live ETag, VersionId and sha256 re-read; candidate rebuilt to its sha256), restamps the S3 metadata, keeps the schema copy's CRLF, and rolls back by each firm's live VersionId. Its first read is the leftover temp-file count on the host (counts only; a person deletes any file). Cottonwood is not in the apply.
- **Not established:** who wrote the three package objects. CloudTrail event history holds management events only and returned no `PutObject` (row W363-S1/S2 in the record).
- **Raised to the CTO (row W363-S2):** two `PutBucketPolicy` writes by the IAM user `cloudops-dell1-agent-user` on the 49financial bucket after the package upload (2026-10-11 15:27Z and 16:07Z). The policy bodies were not read. The apply principal needs `PutObject` on that bucket, so the apply order reads the current policy before its first write.

## Rows

- **STILL ARMED, owner me:** W361-S1 (a careless re-cut would ship unrelated changes: fenced by the packet and the COO half), W345-S3 (disarms on the first leftover-count read after the apply), W348-S2. Row `D2-S132` records the dispositions: W361-S3 disarmed; W362-S1 to S3 ruled; W363-S2 raised.

## Issuer defects this round (mine)

- IB177-1-AC1 demanded a replaced member for every firm, but the CTO's rule gives a firm that needs neither change nothing (cottonwood): the worker's refusal to bend the check was right and I amended it (@f33aa02571, gate limb: none graded, a check file). My plan for the round also assumed the census' four unattributed rows were unexplained; the provenance read explained them.
- My first packet-time clock figures (~09:0xZ) in the COO half were wrong by an hour; corrected to ~08:3xZ before commit.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
