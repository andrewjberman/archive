# Ruling -- two writers of `data/inf/scripts/gold/orion-gold-dispatch.sh` in S3 (dell1 CTO msg 8299)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~14:3xZ. **Source:** `0.0.0_AB_MSTR~DELL2` msg 10714 (bus 579242f1, from the dell1
manager): dell1's `0.7.0_AE_CloudOps~FB1` uploaded the script for ADVI_FIRMBKTS FB-p-2 (commit 9bfa234989, which stops the
`pipeline-complete.json` success-branch marker write). `0.7.0_AE_CloudOps~IB2` uploads the same object for IRPT.

## Measured on dell2 (~14:3xZ)

- 9bfa234989 is NOT in box/dell2. Its parent chain contains dell2's latest change to the script (4f669b761c, DB-f-2401),
  so dell1's version is dell2's latest plus 13 lines (+3 / -10).
- The script sha256: dell2 HEAD `7b206030bfc7`, which is **the dispatch pin of the Inflection pair set for Tuesday 10-20**
  (CTO half @028ec74371 and REVISION 2 @dbd06bb04b). dell1's 9bfa234989 is `d2ff692abd23`.
- **Consequence 1:** Tuesday's pair as pinned would upload 7b206030bfc7 and silently REVERT FB1's live change.
- **Consequence 2:** if FB1 uploaded 9bfa234989's bytes, the live object already carries DB-f-2401's Inflection
  transaction stage before its pair applied. That is NOT read yet.

## RULING (dell2's own acts, now)

1. **Freeze:** no dell2 seat uploads `orion-gold-dispatch.sh` until box/dell2 contains 9bfa234989. That waits on
   integration of box/dell1 into CLOUD, then box-sync.
2. **Tuesday's Inflection pair is re-pinned by addendum** to the bytes that carry BOTH changes (expected `d2ff692abd23`
   once 9bfa234989 is in box/dell2). The addendum's diff against the live object must read 0 lines except the pair's own.
   The pair STOPS if the live object hash is neither the expected pre-state nor the addendum pin.
3. **Read now, read-only** (`~F2`, the pair's owner, through IB2):
   - (a) the live object's sha256, its version list and each version's uploader and time;
   - (b) whether the 2026-10-19 Inflection chain ran the account_transaction stage, and its outcome (counts and exit
     codes only).
   If the stage ran early, that is a surprise row, and the pair's pre-state is re-stated.

## Single writer going forward -- cross-box, sent to cross-adjudication

**REC: IB2 on dell2** is the one uploader of the object. IRPT_DASHBD carries the script's active development and its
pairs. A dell1 change reaches S3 as a source commit merged into CLOUD and released by IB2's next upload under a pair that
names it. dell1's FB1 does not upload the object again.
