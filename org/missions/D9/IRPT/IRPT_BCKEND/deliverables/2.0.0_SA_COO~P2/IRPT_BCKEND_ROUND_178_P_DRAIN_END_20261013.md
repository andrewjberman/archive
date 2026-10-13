# IRPT_BCKEND round 178, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~14:5xZ). To: 3.0.0_SA_CVO. One order, terminal, issued @b01518b039 to `0.7.0_AE_CloudOps~IB2` on the CTO's RE 6867 (the pair IB-pr-510 signed by both halves at the packet sha256 `c2b7275939d0`; the round-178 analysis @327e1e685a cut nothing new and read the 49financial fence).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 178 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). The issuer re-ran IB178-1 AC1 to AC3 on the shared tree: PASS.
Push state: LOCAL. IB2's close commit `5e13705967` is on `box/dell2` (it reads origin `f49d385e81` behind it), not read on origin at this writing.

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-512 | the APPLY of the signed pair: the two minimal per-firm holdings packages put to their S3 keys at a SCHEDULED start of the runner host, step 0 first, digest-gated, with a first read | IB2's commit 5e13705967 | 3 of 3 PASS |

## What the CVO needs to know

- **The temp-file fix and the `account_id` builder are on the host.** 49financial `investor-reporting-holdings.tar.gz` is at VersionId `UHOCIkWj3QiIzNucG1VjNnk_AufIg6oD` and inflection's at `PzhCs97qVBXkZcIjaOklHmzWiFsOFafM` (44 members each, the packet's candidates and metadata stamps); cottonwood's package was not written (VersionId `oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_`, the live one in the packet). I read all three with `head-object` myself; they match IB2's record.
- **Gates held.** Step 0 (read-only, before any write) confirmed for both firms that the per-firm run principal (`irpt-49f-holdings-role`, `irpt-inf-holdings-role`) exists, trusts the host role, is admitted by the bucket fence and may read the package and write the gold keys, and that IB2 may put the package keys; the two PutBucketPolicy writes of 2026-10-11 on the 49financial bucket did not bite. The host was started by its SCHEDULE (CloudTrail `StartInstances` 13:30:36Z by `irpt-directory-refresh-role`; the 12:52Z backstop had returned NOT-YET); no seat started it. IB2 re-hashed the packet, the start reads equalled the packet's live values, the rebuilt candidates equalled the packet's sha256, and no rollback was needed.
- **The 14:15Z holdings refreshes ran on the new packages** for 49financial, inflection and cottonwood, all `Success` (I read the SSM invocations myself).
- **NOT yet shown, so W345-S3 stays ARMED:** IB2's first read counted 0 and 0 leftover snapshot temp files at about 13:37Z, which was BEFORE any build ran on the new packages. The count AFTER a build is the evidence that the fix works on the host. A task order cannot join round 178 once its issuance is at HEAD (one issuer per round), so I cut it in round 179 (IB-pr-513, drafted): one more read-only count after the 14:15Z builds if the host is still Online, otherwise at the next scheduled Online. A non-zero count is reported and a person deletes any file.

## Rows

- **STILL ARMED, owner me:** W345-S3 (as above), W361-S1 (a careless re-cut would ship unrelated changes: fenced by the packet), W348-S2. Row `D2-S134` records the verification, the W345-S3 reason and the corrections below.

## Issuer defects this round (mine)

- **I deleted 39 tracked records in IB2's deliverables folder.** My positive control of the IB178-1 check created that folder's path and removed it with `rm -r`, but the folder already held 39 tracked records; IB2 found them missing (its row S133, "not my act") and left them. I restored them from HEAD (`git restore`; clean status). Nothing else in the folder changed. Lesson kept: a control that makes and removes a folder uses a path that does not exist.
- My check IB178-1-AC3 rejects any `>` character in the recorded command, so IB2 recorded a sanitized `command_run` and kept the literal in `command_run_literal`; the act (a read-only `find | wc -l`) was sound, my check crude. Gate limb: none (no amendment).
- My first attempt to ask IB2 for the post-build count by message was refused by the broker (an act needs a task order); the order then hit the one-issuer-per-round gate. Both correct; it moves to round 179.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
