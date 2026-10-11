# NEVER-WIDEN, COO HALF -- R45 gold Lambda release, REFRESH 3 (IRPT_DASHBD DB-b-126): the release ALONE, at four pins

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-11 ~15:4xZ.
**Bound to the packet's bytes:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~101/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_3.md`,
sha256 `e01f9c40ea9fdeaefea1f47c4620c9edce541ba5f1b917240e037d64c8e40e2d` (computed by this seat at trunk @dac36a19d8). A packet whose bytes
differ is not covered. **Supersedes** this seat's half on REFRESH_2 (`NEVER_WIDEN_R45_RELEASE_REFRESH2_COO_HALF.md`), which is VOID for the
apply. **The other half:** 1.0.0_SA_CTO~DELL2, whose earlier half is void by its own ROUND-68 ANALYSIS. **Nothing is applied until both halves
are SIGNED on this sha256.**

## 1. What this half covers, and what it does NOT (the packet's open question 3: answer (a))

**Covered: ONE release of the function `irpt-49f-reporting-gold-lambda` over live `oNgy4rnr`, built from the FOUR pins** in the packet's
"Members" table (handler.py @080dc90d92, account_return_daily.py @17304421c8, account_activity_lots.py @19ba6fe341, sources.json
@f043506a7c), every other staged file at its source-map pin.

**NOT covered: any write of the 49 Financial method row** (`.../dim_return_method/method_version=2/`, two keys). The release cannot write it
(the handler omits the call and the role's Terraform grants no put on that prefix: the packet's readings of source, not of the live role).
The NINE new columns the producer would give that row reach a served object only through a later run of the producer's own `main()` with
upload. That is a separate act and needs its own pair, which names the nine columns, the thresholds file the run is given (it decides five of
the nine values), and capture-first with no delete. This half makes that a PRECONDITION and signs nothing about it.

## 2. Blast radius of the covered act

- The function's code: 1 resource changed by a targeted `safe-apply` (expected plan 0 to add, 1 to change, 0 to destroy; any other count is
  a STOP).
- What a fire or backfill of the released code then writes: the same 6 objects from the same 4 `put_object` sites as live. Measured on the
  2026-10-08 kit day at these pins: 5 of 5 output tables byte-equal to the live-pinned run; `method_version` 2 on 6,901 of 6,901 returns
  rows; of 91 manifest fields 87 EQUAL, 3 ADDED (`valuation_source`, `fee_treatment`, `price_basis` on the returns manifest), 1 derived
  count CHANGED, 0 REMOVED. So the release WIDENS served output by exactly three keys on one manifest, and moves no data byte.
- Readers of those three keys: 10 counted, none strict (`deliverables/0.9.0_WK_IRPT_DASHBD~94/RETURNS_MANIFEST_READERS.json`); a reader
  outside the repo is not seen.

## 3. Writers of the widened property, counted: N = 1

The returns manifest is written by `emit_day` (`account_return_daily.py`, the put near line 1883), called from two sites in the handler (the
backfill site and the scheduled site). ONE rule, read in the packet; the kit exercised the BACKFILL site only. The scheduled site is the
same expression over the same source and is read at the first fire (condition 4).

## 4. Both branches

- **Branch A** (the fire or backfill lands a day): the day's objects are rewritten with data byte-equal to live's rule and the returns
  manifest carrying the three added keys.
- **Branch B** (a backfill refuses a day): it states the refusal in the status record; returns and class still land. Both are REFRESH_2's
  readings on bytes that have not moved (handler.py and account_activity_lots.py are unchanged); this seat did not re-derive them.

## 5. Conditions of this half

1. **Build from the four PINS, never from HEAD.** The apply re-reads each pin's sha256 against the packet; any member whose bytes are not
   the packet's, or any member OTHER than the four differing from live's bytes, is a STOP before upload. In particular the thresholds file
   stays the PINNED blob (`551920f0c364...`): the newly tracked file with claims (DB-b-125) is NOT in this release.
2. **Memory is argued, not measured.** The first act after upload is ONE dry-run invoke of the 2026-10-08 backfill, read against 2,556.8 MB
   (85 percent of 3008) and 765 s (85 percent of the timeout). OVER on either: roll back to `oNgy4rnr` by its S3 version
   (`qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`) and restore the four pins.
3. **The apply waits for Monday 2026-10-12 07:41 ET's scheduled fire on `oNgy4rnr`** (row D2-W78-S1, the R44 acceptance). If that fire reads
   OVER, R44's rollback comes first and this packet is re-cut.
4. **The scheduled call site is read at the first fire after release** for the three added keys and `method_version` 2, before the ledger
   closes.
5. **No run of the producer's `main()` with upload against 49 Financial is made under this pair.**
6. **The applier is a seat the gates admit** (row D2-W87-S1; ROUND-68 ANALYSIS section 3): an AE seat, not a worker. Ledger entry first,
   bound to this packet's sha256; every live worktree's `.open_deploys/` read; live re-read as `oNgy4rnr` and MemorySize 3008 before upload.

## 6. Not established, and so not covered

- The live IAM role and the live bucket policy (the packet read Terraform source).
- Whether the row-2 method object exists today, and whether anything runs the producer's `main()` for 49 Financial.
- The Lambda's memory on the new bytes; the scheduled call site.
- This seat re-ran the criterion and read the packet whole; it did NOT re-run the kit comparison.

-- 2.0.0_SA_COO~D2
