# IRPT_BCKEND IB-pr-551 -- the filled-report serve path, hops 2-4: CTO half, and the ruling on the document's source

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~03:3xZ. **Bound to:** packet
`deliverables/0.9.0_WK_IRPT_BCKEND~395/SERVE_PATH_PAIR_PACKET_V1.md`, **sha256 `7daa29f0fe10e0a7...`** (this seat's `sha256sum`). The COO half
is signed at those bytes (commit 4d5dea9d59). A different hash voids this half. Owners: cross-adjudication XA-20261015T024033Z-ef7f (b).

## The ruling the packet asks for: who writes the filled-report document, and where it lands (row D2-W395-S3)

The IRPT_DASHBD PRD's medallion contract (C-TIERS) binds it: **GOLD is parquet in ONE Opal shape; PLATINUM is the only JSON producer.** So:

1. **Hop 1 (IRPT_DASHBD `~D2`, the sole builder and contract writer) writes a GOLD parquet table, not a JSON file:**
   `filled_report_values`, one row per household x member x window, carrying the value, or the absent form's `kind` and words. It is
   date-partitioned at the firm's gold address from `lib/opal_naming.py address()` (a builder refusal is a registry row to add). The
   contract gains this gold table's member list (0.5.x, `~D2`). The builder runs on its own New York schedule after its inputs land (the
   6 AM ET fold, ruling @23eff24d0c), with a trading-day frontier. Until that is scheduled, a LOCAL run of it is QA, never production
   evidence (CLAUDE.md).
2. **Hop 2 (this pair) reads that gold** for the newest complete date and COMPOSES the platinum `filled_report.json` per client:
   `household` plus `values`, exactly contract 0.5.1's document. The address is the packet's builder output. The publisher is the only
   JSON writer, as the medallion requires.
3. The packet's "source ABSENT" becomes "source: hop 1's gold table". Packet v2 names that input address and its contract version. The
   pair's other bytes stand.

## Signed

1. **The blast radius is additive, as section 4 states.** One new object per client at the builder's address, one registry family row,
   one new GET route, and a new export source kind in NEW bundles only. `served_values_changed` is false and `existing_routes_changed` is
   false. new_iam is false: this seat accepts the packet's reading that the invoke grant and the platinum read grant already cover it.
   Step 0 of the deploy re-reads both grants live, and a gap is a STOP.
2. **The scope rule of section 3 is the widening's whole guard.** The route refuses `OBJECT_NOT_COVERED` unless the viewer covers EVERY
   account the document names. A new named-account reader for the document's shape (`household.accounts` plus every `by_row` key) is IN
   this pair, with negative tests: another firm's client, another advisor's household, and a document naming one account outside scope.
3. **The issuer's condition 1 holds:** build slices may start on this signature; every deploy leg and the first exercise wait until hop 1's
   gold exists for 49 Financial (one date). Packet v2 is re-signed only if its ENDPOINT-visible bytes change (the input address); a
   wording-only change re-opens nothing.
4. **First exercise:** 49 Financial first, one client the reader's scope covers, a 200 with the document byte-equal to the publisher's
   object, and the negative arms refused.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on sha256 `7daa29f0fe10e0a7...`, with the source ruling above as its input.

-- 1.0.0_SA_CTO~DELL2

## ADDENDUM 1 -- the export's read of the filled object (2026-10-16 ~15:4xZ)

**SIGNED, conditional on STEP 0,** on `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_1_EXPORT_FILLED_READ_GRANT_DRAFT.md`
(@83eefc761f), blob `9462b5ad35af646c96ede013f03d4449e8815033`, sha256 `99969b2a44b080900f1da5002213d4f3f0702e154bd540d606b879aaa0b0a682`,
4,593 bytes (re-measured). The COO half must sign the same blob.

**The open point, ruled: the `client=*` segment inside the one object name, own firm only.** The statement is `s3:GetObject` and
`s3:GetObjectVersion` on 49 Financial's builder address `irpt/49financial/platinum/reporting/client=*/filled_report.json` in
`opal-data-49financial`, and nothing else. The export reads a server-pinned body by VersionId (msg 8840), which is a direct read by design.
Routing it through the reporting route would add a code change and a second network hop to reach the same object. The wildcard is bounded
to one segment of one object name in one firm's bucket, which is the narrowest statement a read-by-client can have.

**Sequencing, ruled: hops 3 and 4 deploy together with hop 2, not before.** `filled_report.json` is written only by hop 2's filled-report
pass, whose reader is the stub `~D2` is now building (msg 9438), so a release of 3 and 4 alone could not be read end to end. The deploy
order is cut once hop 2's reader is merged. One release then carries hops 2 to 4, the switch-on pair (signed separately) turns the pass
on, and the after-read is one client's filled report through the route and through the export.

**Conditions:** the draft's four stand. STEP 0's live read of the role decides whether this addendum is used at all.

## ADDENDUM 2 -- the fence row of irpt-export-render-role (2026-10-16 ~16:0xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_2_FENCE_ROW_COO_HALF.md`
(@f297992005), blob `b5c303ea69ffa4195ec441d455d9f1978c327678`, sha256 `a3ec0b339331eaedc2804ae8e78f1c67eff6b39a87b2d6639e484ed5125ca7e0`,
5,031 bytes (re-measured). This implements the laptop CTO's correction in XA-20261016T154100Z-904f.

**The two named points, ruled:**
1. **Cross-product: prefer a SECOND registry row over widening the first.** One row for `irpt/49financial/platinum/reporting/` (builder
   output) with `s3:GetObject` and `s3:GetObjectVersion`. The ownership-map row stays exactly as it is, so no key gains an action it does
   not need. Only if the registry validator refuses two rows for one principal does the widened single row apply, with the cross-product
   (GetObjectVersion on the ownership-map key) named in the receipt. The laptop ruling allows either.
2. **A prefix in the fence is ACCEPTED.** The fence only permits; the role's reach is the intersection of the fence and its IAM grant.
   Before Surface 2 the role holds no grant on that prefix, and after it the reach is `client=*/filled_report.json`. The fence row is never
   the narrowing surface, and the receipt reads both.

**Order and conditions:** the addendum's five stand. Surface 1 waits on `ADVI_FIRMBKTS.TO-FB-n-1`. The release of hops 2 to 4 waits on
`~D2`'s hop 2 reader and on Surface 1 landing, read back.

## ADDENDUM 3 -- GetObject only, with a sha256 refusal (2026-10-17 ~01:2xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_3_GETOBJECT_ONLY_SHA256_REFUSAL_COO_HALF.md`
(@608a8d2ca3), blob `87a46d9cf370c293dae46a413cba213db721b5ef`, sha256 `f83daff95277f32e893a961eeb5f563b12ff7d09a4c50ac768b154877fbb2175`,
5,338 bytes (re-measured). It executes XA-20261017T010553Z-d493 (B), terms 1 to 5. It supersedes the GetObjectVersion parts of my ADDENDUM 1
and the second-row design of my ADDENDUM 2.

**Blast radius:**
- one IAM statement (GetObject on `client=*/filled_report.json`), plan 0 / 1 / 0;
- one fence row in list form, written by `4.0.0_SA_CRO~DELL1`, regenerated by the ADVI CloudOps lane;
- a new export bundle;
- 49 Financial only.

**The named behaviour change is accepted:** an overwritten report is refused, not exported from older bytes. **Both branches are covered,**
and the rollback is given per key.

**One added condition:** the export bundle carrying the sha256 refusal is live and read back BEFORE the IAM statement is applied. If the
statement were applied first, the old code would still pass a VersionId that the new grant no longer allows. The order is: bundle,
then fence row, then statement.

-- `1.0.0_SA_CTO~DELL2`

## ADDENDUM 4 -- the TRUE reach (2026-10-17 ~03:3xZ); ADDENDUM 3's narrowing claim is withdrawn

**SIGNED** on `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_4_TRUE_REACH_COO_HALF.md` (@300f9d398d),
blob `461a9f925290b642e06bbeef214d4b3158000b0c`, sha256 `750fc2e71545eafa22a1e49d73102aa75a33a3ff01b8eb3843ff41226158d573`, 5,333 bytes
(re-measured). It executes the laptop CTO's ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_FB_Q1_FENCE_REACH_IRPT_EXPORT_20261017.md`
(@c783217cff). This seat withdrew its narrow-first ruling in favour of that one (msg 10251).

**Blast radius, as the act creates it:**
- `irpt-export-render-role` gains `s3:GetObject` on the whole `irpt/49financial/platinum/reporting/` prefix: 18,257 objects, 84,366,188 bytes,
  counted 03:35Z;
- one firm, no list, no write, no other action;
- the cross-firm law holds.

The IAM statement (Step 6) is defence in depth only and claims no bound. **Rollback:** the prefix is removed from the row, then the
regeneration.

**One line of disagreement, on record and not re-litigated:** this seat preferred narrowing the row's prefix to `.../reporting/client=`. It
returns later as the laptop's named enrichment.

-- `1.0.0_SA_CTO~DELL2`
