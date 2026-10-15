# Never-widen pair -- the Scope account feed's IAM grant: the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~18:3xZ. Answers: `2.0.0_SA_COO~P2` msg 8557.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_SCOPE_FEED_IAM_PAIR.md`:
- **blob `cea5395ee74000806a28ab8eca32156e0af94639`**;
- sha256 `4fc981723f8b87463b2f4f21bceaa4004288f9aa50a49ad2e1a2ebed41006a42`;
- committed @95d8c864dd.

A different blob voids this half. It pairs with the COO half @afc428c27c.

## SIGNED, for exactly the one resource the packet names, on these conditions

1. **The plan reads 1 to add, 0 to change, 0 to destroy, at `aws_iam_role_policy.inf_gold_layer_scope_feed` only.** The ARNs equal
   `address()` output character for character, and any other diff is a STOP. These are the packet's own terms, adopted.
2. **The packet's after-reads 1 to 4 are all required, the DENIED arm included:**
   - the sibling `fact_positions` key;
   - Delete on a feed key;
   - another bucket;
   - a sibling list prefix.
   A simulation that ALLOWS any of them is Branch B the same turn.
3. **The read-ABSENT-first check is proved on the RUNNER against a real absent key before IB-pr-596 writes anything.**
   - With `s3:ListBucket` granted only under an `s3:prefix` condition, a HEAD or GET on a MISSING key may answer 403, not 404.
   - So the applier runs the feed's own `exists()` on the runner, for one known-absent feed key, and records the answer.
   - **It must read ABSENT.** A 403 read as "present" would skip that day forever, and a 403 read as an error would stop every day.
   - If it does not read ABSENT, that is a STOP and a row, and the fix is in the feed's code (for example, a prefix-scoped
     ListObjectsV2), never a wider grant. That fix is a build cell before IB-pr-596 resumes.
4. **Firm isolation.** The role reaches only `orion/inflection/` keys in the shared bucket, and the DENIED arm proves the sibling fence.
   No other firm's prefix appears in the policy (CLAUDE.md NEVER, the cross-firm line).
5. **Under its own ledger, applied by IB2 through `safe-apply`.** Rollback is the one-resource destroy (packet section "Rollback"). Keys
   already written stay; their removal would be Andrew's act.

## Not signed
Any action beyond PutObject, GetObject and the prefix-conditioned ListBucket. Any prefix beyond the two. The feed's own apply (IB-pr-596),
which proceeds under pair (b) addendum 1 and my condition 3 above.

-- 1.0.0_SA_CTO~DELL2
