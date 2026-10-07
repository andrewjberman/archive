# Never-widen pair -- IRPT_DASHBD FWD-8: the split Black Diamond pull (DB-b-45, run on the laptop)

**Packet author:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~23:5xZ | **Halves:** `1.0.0_SA_CTO~DELL2` and `2.0.0_SA_COO~D2` (laptop CTO
ruling msg 106630, relayed by 0.0.0_AB_MSTR~DELL2 msg 1145: "It is dell2's project and a read-only pull into a new partition, so the
halves are 1.0.0_SA_CTO~DELL2's and 2.0.0_SA_COO~D2's; no laptop CTO half is added.")

## The act

ONE run of `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~25/bd_split_pull.py . run --go` at the pin the GO names
(dell2 CLOUD at or after @35a0fc34d4; on origin in `q/dell2/seat-work-2240/r2` @eaae449ef2), by laptop seat `0.7.0_AE_CloudOps~I`, and at
most one `sweep --go` of its FAILED set. Authority: Andrew's per-use word, record
`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261007_211xZ_DELL2_GO_WITH_YOUR_REC_TWO_PORTAL_LANDINGS_BD_VENDOR_PULL.md`
@5ef6d33141: ONE split, read-only pull, 2,299 accounts, 2,299 calls, 4,598 date ranges. Nothing wider.

## Blast radius

- **Vendor:** Black Diamond `performancePeriod` POSTs, READ only: 2,299 calls (one per account, two ranges each), plus at most one retry
  per call and one sweep of the FAILED set, under round 14's ruling (`aggregate_rps` 2, workers 2 -> 6, `failed_cap` 105, abort on 3
  consecutive failures or any unexpected 4xx). Bearer mints through the 49F sign-in, one at a time.
- **Writes:** ONLY new objects under
  `s3://opal-data-assets/blackdiamond/49financial/bronze/reporting_performance/pull=split20261007/acct=<bd_internal_id>.json`
  (builder output, `lib/opal_naming.py address()`), one per account; the runner refuses if any object is already there. No existing key,
  no other prefix, no served table, no other firm's tree.
- **Not touched:** the round-14 `pull=20261004` prefix, every gold table, every IAM grant, every schedule.
- **Writers of the named property:** one rule (the runner's landing) on one path; printed: 1.

## Rollback per key

Each landed key is new and read by nothing yet; rollback is deleting `pull=split20261007/acct=<id>.json`, by key, under the issuer's
word. Nothing else changed, so nothing else rolls back.

## Branches (read from the round-19 analysis @b402b7b2e3 section 2, stated before the word was spent)

- **## BRANCH A** -- the split figures tie Opal's within 0.35 pp on most of the 2,299 closure segments: BD's closure-day booking is the
  cause of the closure residue.
- **## BRANCH B** -- they do not tie: the gap is not the closure day, and the residue read widens.
Either branch moves FWD-8's grade. The run itself has two outcomes as well: landed (+ FAILED <= 105, swept once) or ABORTED by a rule,
with every call recorded; an abort lands nothing further and is reported, not retried beyond the one sweep.

## After-read (the issuer's, on dell2)

`p27_pull_run.py` DB27-1-AC1 on the returned `SPLIT_PULL_RUN.json` (counts close, abort null) and DB27-1-AC2 (the S3 listing under the
new prefix equals the record's landed count). Then the tie-out cell is cut.

## CTO half -- 1.0.0_SA_CTO~DELL2

UNSIGNED. Signing means: the blast radius above is the whole act; the writes are only new keys under one new prefix; the run is bounded by
Andrew's word and the runner's refusals.

## COO half -- 2.0.0_SA_COO~D2

**SIGNED 2026-10-07 ~23:5xZ.** I have read Andrew's word at the record above and the runner's refusals (`--go`; plan re-derived; exactly
2,299 requests, 4,598 ranges, 0 unmapped; nothing landed under the prefix; round-14 ruling unchanged). The plan is graded VALID
(DB26-3-AC1, AC2) and merged @35a0fc34d4. The act may touch only the vendor reads and the new keys named above; rollback is per key. The
dell2 abort @e39ea3dcca made 0 vendor calls, so this run is the first and only use of the word.
