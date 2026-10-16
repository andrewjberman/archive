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
