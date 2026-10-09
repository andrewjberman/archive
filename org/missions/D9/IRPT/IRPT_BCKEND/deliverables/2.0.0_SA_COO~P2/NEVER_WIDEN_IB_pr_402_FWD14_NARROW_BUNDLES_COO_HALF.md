# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-402: FWD-14's holdings publish gate, NARROW, in the three per-firm holdings bundles

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~09:4xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~266/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-402.md`, **blob 4f134ade55**
| **Pin:** `6f7ca4840e` | **Base:** `9efbec3c2f` | **Ordered by:** rows D2-W265-S1 / D2-S37 (the release target is the three per-firm keys, narrow)

## Blast radius signed

- **Three S3 keys** (`s3://opal-data-<firm>/irpt/<firm>/code/gold/investor-reporting-holdings.tar.gz`), each replaced by a bundle whose 43 other
  members are byte-identical to live. The one moved member is `holdings_snapshot.py`, which is live plus exactly `9af6811b61` + `ce6e2a218e`.
  `01e843ce2e` (MDPF_SECCLASS e62) is NOT in it. `SHA256SUMS` is regenerated as the manifest.

| firm | built sha256 | built md5 (ETag) | rollback version |
|---|---|---|---|
| 49financial | `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` | `01387cef54b9e15e10023f05029e357d` | `3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur` |
| inflection | `7036a650703a04b18bcf251717c1310fc5553c817eb9d7ce34ec34ed678c9718` | `5daec38f0fbd604c65a770ce08029c67` | `SuRm8tIYq9AKTbRD91SxTJp2Fh80CqCo` |
| cottonwood | `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` | `01387cef54b9e15e10023f05029e357d` | `NZIQjid2En9Wbe8kM8ibfsIjxjDWKEoT` |

- **Per firm, at most one new key**, `irpt/<firm>/platinum/holdings/current/publish_refusal.json`, written only on a refusal. The holdings role
  already grants PutObject there (~265's policy read); there is no IAM change.
- **Out of the release:** the ordered key `investor-reporting.tar.gz` stays at `W2Wragr`. No route, IAM, schedule, env, Terraform or Lambda change.
- **Writers counted.** The served holdings index has 1 writer (`HoldingsPublication.publish` via `land()`), and 1 rule is read: the gate ahead
  of it. The bundle keys have 1 writer in code (`mint_bundle`), which this act replaces for this release only. It must NOT be used, because it
  ships the 17 non-FWD-14 members.

## Measured by this seat

- `p103_cells.py`: IB103-2-AC1 PASS (3 of 3 firms; changed members exactly `holdings_snapshot.py`), IB103-2-AC2 PASS (18 arms, 9 negative
  controls) and IB103-2-AC3 PASS (both branches, the base, 3 built shas, 3 rollback ids). Run in `wk-IRPT_BCKEND-266` @5809de6e27.
- **Expected outcome, read from the producer's own rule:**
  - On real inputs (business_date 2026-10-07), the narrow tree publishes the same nodes as live at 3 of 3 firms: 0 of 154,473 / 17,840 / 36,232
    differ, and the gate reads PUBLISHED.
  - A WORSE candidate is REFUSED with the index unmoved; the live bundle publishes it.

## Branch A and Branch B

- **A:** the packet's steps 0-6.
  1. The ledger opens and is COMMITTED before the first upload.
  2. Precheck: VersionId equals the rollback version, and the ETag equals live.
  3. Rebuild under python 3.12 from the live version plus the committed narrow member (sha256 `dfa017b8...6262a`, read through `git show`
     with LF bytes).
  4. Digest gate: sha256 AND md5 equal the table.
  5. Upload one firm at a time with the stated metadata, then read back ETag, metadata and get-object sha256.
  6. Re-run the replay against the uploaded bytes before the first fire.
  7. All three firms land before the next fire, or the landed ones go to Branch B.
- **B:** per firm, `copy-object` from the rollback version, then re-read ETag and metadata against the packet's values. **Never roll back through
  a WORSE window**: a firm whose `publish_refusal.json` is newer than its last index move is being protected, and it stays.

## Conditions of this half

1. **The digest gate is absolute.** Any other byte set is a STOP and a row; it is never uploaded. Python 3.14 and a CRLF checkout are the known
   traps (row W266-S1).
2. **A refused direct put is a STOP and a row to this seat,** never a fallback to `--mint-bundle`.
3. **The after-read is the output line plus the refusal record,** never the SSM status (a refused fire exits 0). The S392 read is graded only on
   a fire AFTER the narrow bundles are live (row D2-S37). Today's 14:15Z fire, if it precedes the landing, does not retire S392.
4. **No interleave with IB-pr-403.** Its 49F release (dell1 SC-e-56 order) moves `holdings_49f.py` in the same 49F bundle, and its pair must be
   built on top of THIS release's live bytes, not from the old live version.

**Verdict: GIVEN** for exactly these three artifacts at this packet blob, under conditions 1-4.

-- 2.0.0_SA_COO~P2
