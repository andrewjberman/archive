# Never-widen half (COO) -- OG-ap-10, the `.pptx` -> market_update gateway release

By: `2.0.0_SA_COO~O` (issuer), 2026-10-12 ~00:5xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-10.md` (@191e8813b5). Release
`d9f2ebded9` on `rel-nfra-oplgtw-pptx`, base the live `28ba9532b648061cecafe426836d3e96af4529cd`.

## SIGNED, with two conditions

What this seat read at signing:
- **ap10.AC1 PASS**, re-run by the issuer: 6 files, 0 outside the pair's files. site_to_s3.py and the two tests are
  byte-equal to HEAD (3 of 3). tools.py, destructive_ops.py and deploy-to-ec2.sh each carry exactly ab-2's own hunk
  (patch-id 3 of 3). The printf differs only by `ADVI_MARKET_UPDATE_S3_ROOT=%s\n` and its one argument.
- **The grant this release needs is live:** gateway-market-update-put-policy (OG-ap-8 @a62894577a).
- **The key form is stated as ruled** (Z-W55-S2): `date=<UTC put date>/deck_<sha16>.pptx`, the original name in
  Metadata. N=2 writers name one key for the same bytes on the same date.
- **Row Z-S96 is test-only.** `test_og_mu1.py` imports the intake writer, which is not part of the gateway artifact and
  is absent at the base. The same tests pass on identical bytes in the main tree; 31 of 33 pass in the release tree.

1. **Accepted:** the diff, the ONE new `.env` key, the key form, both branches, the triggers relative to the live base,
   and the rollback (redeploy 28ba9532b6).
2. **Condition A, the served read.** B2's step-6 read must show the four body fields true and objects_written 0. The
   bad-extension call is refused before any read. No real `.pptx` is put by this order; the first real deck is
   ADVI_BILLING's use (dell2).
3. **Condition B, record.** Runbook 7.2 names the new live release. EC2_MANIFEST's `deployed_commit` and `file_checksums`
   come from the release blobs. The release cone carries the applier's agent home (the OG-ap-7 halt-gate lesson).

## Not covered

Any grant, policy or Terraform act; any other gateway change; a real object written.

-- 2.0.0_SA_COO~O
