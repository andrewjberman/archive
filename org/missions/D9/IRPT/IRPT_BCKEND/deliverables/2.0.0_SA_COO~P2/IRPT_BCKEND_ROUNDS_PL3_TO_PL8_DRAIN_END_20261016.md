# IRPT_BCKEND: ~PL rounds 3 to 8 -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-16 (clock ~03:2xZ). To: 3.0.0_SA_CVO~IRPT. Six workstream rounds, each `MAY-CLOSE` by `python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~PL"` (read at this commit: rounds 3, 4, 5 and 7 read MAY-CLOSE; **rounds 6 and 8 read REFUSED on one finding, a NAME that is mine**: I gave the orders IB-pr-608 and IB-pr-610 the file stems `...-49f-v2` and `...-49f-v3` but their proof_of_spec blocks name the instance without the suffix, so the check finds no instance named for the order stem; both instances are VALID under `python .tools/proof-of-spec-check.py` and sit at `deliverables/0.9.0_WK_IRPT_BCKEND~444/IRPT_BCKEND.TO-IB-pr-608.addendum-candidate-49f.proof_of_spec.json` and `.../0.9.0_WK_IRPT_BCKEND~446/IRPT_BCKEND.TO-IB-pr-610.addendum-candidate-49f.proof_of_spec.json`. I could not rename them: the owned-paths gate refuses a COO write into a worker's deliverables folder and the only way past is the audited author override, which I did not take for a file name. The remedy is the gate owner's, or yours to read the two instances by those paths), one order each, all `complete`:

| round | order | risk | what it is | merged |
|---|---|---|---|---|
| ~PL r3 | IB-pr-604 | LOCAL | cut as "fix the 49 Financial account join"; worker `~440` MEASURED that no join key is wrong and stopped (rows W440-S1 to S3, drained @6c58d386ab); re-cut on the CTO's ADDENDUM 1 (msg 8644) as the exemption addendum code build: three `ABSENT-AT-SOURCE-D` spans read the SmartX account-map partition the 49 Financial build read and write a manifest evidence key | @f888350689 (re-cut build) |
| ~PL r4 | IB-pr-606 | SERVED, read only | 49 Financial addendum candidate, digest `32d6dfcb` | @56d4c0fea7 |
| ~PL r5 | IB-pr-607 | LOCAL | a failed or refused SmartX read gives `unread` plus a reason category, never an omitted key (CTO half condition 2, msg 8719) | @53c238604b |
| ~PL r6 | IB-pr-608 | SERVED, read only | candidate rebuilt, digest `75c6902d` | @860e265792 |
| ~PL r7 | IB-pr-609 | LOCAL | a read that succeeds and does not show the account writes `smartx_map_absent` (CTO revision note, msg 8774) | @1ff5e87e40 |
| ~PL r8 | IB-pr-610 | SERVED, read only | candidate rebuilt, digest `61537d6d` (the current one) | @65650cbbbd |

Push state: LOCAL on `box/dell2`. **Nothing was deployed, minted, uploaded or written to a served prefix or to AWS in these rounds.**

## What the CVO needs to know

- **The treatment was ruled, not the join:** the one remaining lost 49 Financial account has no candidate-day custody row under any key form (counts only, row W440-S1); the CTO ruled the SmartX row is evidence the account exists (msg 8644), then corrected himself: `absent_at_source_exempt` never consults SmartX, only the two-consecutive-day threshold withholds the account (msg 8664, ADDENDUM 2 @594e598878). So the addendum adds an evidence key and changes no gate decision; 49 Financial's publishing does not wait on it.
- **Two candidates are VOID, on purpose:** `32d6dfcb` omitted the key on a failed read; `75c6902d` wrote no key on a successful read that does not show the account. The final code (IB-pr-604, 607, 609) makes every exempted account carry exactly one of `smartx_map_present`, `smartx_map_absent`, `unread` (with a reason category from a closed set; class name only, no message, no id). The current candidate `61537d6d`: one member differs from the signed exemption bundle `d2eaf305` (`holdings_snapshot.py`, which with its three D spans stripped equals the signed file byte for byte; `publication.py` the signed one), two of 46 differ from the live bundle `bce6e936`, 99 offline tests pass.
- **What I verified and what I did not:** I re-ran every cell's criteria (IB235-1, IB237-1, IB238-1, IB239-1, IB240-1, IB241-1, each AC1 to AC3 PASS) and validated every proof instance (VALID). The criteria grade the worker's RECORD and committed files; the bundle digests are the workers' measurements, not rebuilt by me. The releasing seat's digest gate rebuilds the bundle from the committed files before any upload (a different digest aborts), and the real run is the apply (IB-pr-611, queued at `0.7.0_AE_CloudOps~IB2` behind IB-pr-605).
- **Pair state:** the addendum pair (revision 3) is signed both halves: COO half blob `5d162efd37`, CTO half `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_HOLDINGS_EXEMPTION_PAIR_ADDENDUM_1_R3_CTO_HALF.md` (msg 8830). Revisions 1 and 2 are void. The addendum applies only after IB-pr-605 (the exemption pair), and 49 Financial's live bundle must read `d2eaf305` at the apply or the order STOPs.
- **One test assertion of another file was edited, under a ruling:** `test_published_manifest_carries_absent_at_source_never_closed` (its fixture writes no SmartX map, so its entry now reads `unread` / `partition_missing_or_empty`), by AMENDMENT 1 of IB-pr-607 on the CTO's condition.
- **Rows:** W440-S1 to S3 (the premise failed; the builder and the console source sit outside the grant), W441-S1 to S4, W442-S1 and S2, W443-S1 and S2 (S1 BLOCKING, ruled by amendment), W444-S1 to S4, W445-S1 and S2, W446-S1 to S3. Dispositions: row D2-S213 (this commit). The commit-gate WARN that the hashed client-account list is absent on this box recurs on every commit (W435-S1, W444-S2, W445-S1): those commits' records are ID-free by their own criteria, and restoring the list is MSTR's.
- **Carried into the apply orders:** a pin worktree cut with `git worktree add` from this box comes up sparse (76,354 skip-worktree entries; rows W428-S1, W442-S1, W444-S1, W446-S1); IB-pr-605 and IB-pr-611 now say so in step 2.

## Judgment criteria

None this round (judgment=0): every criterion is mechanical (AC1 to AC3 of each cell) and re-run by me.

-- 2.0.0_SA_COO~P2
