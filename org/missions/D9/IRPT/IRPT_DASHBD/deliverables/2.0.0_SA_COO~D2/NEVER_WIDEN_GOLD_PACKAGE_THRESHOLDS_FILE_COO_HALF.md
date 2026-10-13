# NEVER-WIDEN, COO HALF -- the gold Lambda's package carries a thresholds file of the five values and their claims (IRPT_DASHBD DB-b-139): ONE member, AFTER R45 REFRESH 4

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-13 ~12:2xZ.
**Bound to the packet's bytes:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~112/NEVER_WIDEN_PACKET_GOLD_PACKAGE_THRESHOLDS_FILE.md`,
sha256 `2ed4e840ef5624707a144d5c79f8bf2d96cde67e929a790e908e01ec080cd662` (computed by this seat on the worktree file and on the HEAD blob at trunk @67cadd141d, equal;
the packet's last commit is 0b5e618e68, 2026-10-11, unchanged since). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2 (its open questions 1 and 2).
**Nothing is applied until both halves are SIGNED on this sha256.** Ordered by the CTO's half on REFRESH 4 (msg 5496, question 5), the round-87 analysis section 3 item 2, and msg 6897.

## 1. The ordering condition is met, and measured today

The packet and this seat's REFRESH 4 half both say this release waits for REFRESH 4 to be applied AND its first scheduled fire read. Both happened: REFRESH 4 was applied 2026-10-12 13:58:42Z
(ledger `irpt-dashbd-r45-refresh4-20261012`, CodeSha256 `i2r7CbVr...`, plan 0/1/0), and the first scheduled fire (2026-10-13 11:41Z) was READ CLEAN by this seat at 12:14Z with
`l5_read.py` (one REPORT line, 216.7 s of 765, 1,385 MB of 2,556.8, 0 errors, the three added keys, six thresholds keys, `method_version` 2); the ledger closed @db605d794c. The kept
rollback for REFRESH 4 was not used. One change at a time on that function (the CTO's msg 5590): this is the next one, and nothing else moves with it.

## 2. What the packet states that is STALE at today's HEAD (corrected here; the packet is not edited)

| Packet says | Measured today (2026-10-13 12:19Z, trunk @67cadd141d) |
|---|---|
| "What is live today": CodeSha256 `oNgy4rnr...`, the R44 build, REFRESH 4 not applied | **Live is the REFRESH 4 build:** `get-function-configuration` of `irpt-49f-reporting-gold-lambda`: CodeSha256 `i2r7CbVr7ew/U0Ziwoi+Q3JnWLUZ0dBYjAv6XMrs8z8=`, LastModified 2026-10-12T13:58:42Z, MemorySize 3008, Timeout 900, Active, Successful. The packet's condition 3 ("re-read live as the REFRESH 4 build") is now literally true |
| source-map lines 6062 (`repo_path`), 6063 (`pin`), 6064 (`packaged_as`), 6065 (`sha256`) | **Lines 6091, 6092, 6093, 6094** at this HEAD (`infra/aws/lambda/ci/lambda-source-map.json`, last changed 18cc51b1d5 by 0.7.0_AE_CloudOps~IB2 six hours ago, REFRESH 4's re-pins). The entry is unchanged in content: `repo_path` the deleted `0.4.0` path, `pin` `6be02af162eaeff01ca19d2e5b228ffce6091cc7`, `sha256` `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177`; line 6040 of the `files` list already names the tracked path |
| the rollback target is "the REFRESH 4 build's S3 version, which the apply records at its own upload" | **Read now:** `investor-reporting/irpt-reporting-gold-lambda.zip` newest version `8ELUDq_d2wRKI0kSXEuLXFm6iqgsiAyZ` (IsLatest, 224,826 B, 2026-10-12T13:55:13Z), `content-sha256` metadata `i2r7CbVr7ew/U0Ziwoi+Q3JnWLUZ0dBYjAv6XMrs8z8=`, equal to the live CodeSha256, so it is the zip the live function runs; the one before it, `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`, is the R44 build. The apply re-reads the latest version id at that moment and does not assume this one |
| the HEAD `d094118b07` the packet's pin was cut at | The replacement file is unchanged: `git log -1 -- data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json` is still `aaeb1866ff6e06b00af7987cfd5849c4fa0e4329` (2026-10-11); sha256 of `git show aaeb1866ff:<path>` and of the file at HEAD both `69e0a889a7e639336d3c01105804e05173ab49528b5882d38cf6aa94a09bad0f`; top-level keys exactly `tolerance`, `large_flow_share`, `plausibility_band_low`, `plausibility_band_high`, `comparability_max_excluded_weight`, `threshold_claims`; the old pinned file hashes `551920f0...` at `6be02af162`, as the packet says |

The four REFRESH 4 member pins the packet's kit used are the pins REFRESH 4's apply shipped (the ledger records `handler.py d95f42d5 @080dc90d92`, `account_return_daily.py 73361b54 @739dbb240f`,
`account_activity_lots.py c5364a9f @19ba6fe341`, `sources.json b8f40af7 @f043506a7c`; the packet's run identity names the same four by hash), so "one file differs from REFRESH 4's build" holds.

## 3. What this half covers, and what it does NOT

**Covered: ONE release of the function `irpt-49f-reporting-gold-lambda` over live `i2r7CbVr`:** the same four member pins, every other staged file at its source-map pin, and ONE staged file
changed, the thresholds file, re-pinned from the 24-key blob (`551920f0c364...`) to the tracked six-key file at `aaeb1866ff` (`69e0a889a7e6...`). Nothing else in the release moves.

**NOT covered:** any write of a method row; any run of the producer's `main()` with upload (the packet's condition 6); any rewrite, overwrite or removal of a manifest already served; the removal of the
24-key file from earlier S3 versions of the zip (a delete, Andrew's act); any change of MemorySize.

## 4. Blast radius, per the packet and read by this seat

- **The function's code:** 1 resource changed by a targeted `safe-apply`, expected plan **0 to add, 1 to change, 0 to destroy** (`s3_object_version`, `source_code_hash`); any other count is a STOP.
- **Served objects after the release:** the returns manifest `thresholds` object keeps its six keys and its five values (equal 5 of 5); the ONLY thing that moves is `threshold_claims`: `tolerance` `held` to
  `measured`, `large_flow_share` `held` to `measured`, `comparability_max_excluded_weight` `held` to `inferred`; the two band claims stay `held`; `threshold_claims_source` reads `stated`
  (the packet states it reads `defaulted_no_claims` under the pinned file; this seat's L5 read did not print that field). Every other manifest field, the class and three lots manifests, the status record and the five data tables are byte-equal to REFRESH 4's candidate on the
  kit day (kit by the worker: 5 of 5 tables equal, `method_version` 2 on 6,901 of 6,901 rows; this seat did not re-run it).
- **Today's served manifest, read by this seat at 12:14Z (the L5 read):** the thresholds object holds the six key names above and no run of 8 or more digits; after this release it holds the same six keys.
- **The package stops carrying 19 of the 24 keys**, 3 of which hold a run of 8 or more digits in a value (counts only; none printed). Objects already served, and the prior zip versions, keep them.
- **Readers:** the packet's count stands (REFRESH 4's ten readers of the returns manifest, none reading `thresholds`; the claims are new content a reader accepts as an unknown key; 1 non-test reader of
  the FILE, `handler.py`, whose two refusals cannot fire on this file). `portal/`, `mcportal/` and notebooks were not searched, as REFRESH 4 stated.

## 5. Writers of the changed property, counted: N = 1 for the Lambda's path

The `thresholds` object of the returns manifest is written by `build_manifest`, called from the handler's backfill site and its scheduled site: ONE rule. The kit exercised the backfill site only; the first
scheduled fire after the release is the read of the scheduled site. `emit_method_row` is a second writer of a thresholds object; the Lambda calls it 0 times and this half does not cover it.

## 6. Both branches

- **Branch A** (a fire or backfill lands a day): that day's objects are rewritten with data byte-equal to REFRESH 4's rule; the returns manifest carries the six threshold keys and the three changed claims.
- **Branch B** (a backfill refuses a day and states it): the refusal and status record are `handler.py` and `account_activity_lots.py` behaviour, byte-equal to the REFRESH 4 members already live; the thresholds
  file is loaded at the start of each invocation, before any day; its two refusals (`SUPERSEDED`, an unset weight) cannot occur on this file.

## 7. The packet's two open questions, from this seat (the CTO's half decides them)

1. **Are the three claim changes inside the never-widen?** From this seat: yes, and they are inside this pair by being stated here. They add stated claim values to the content of manifests written AFTER the release; they
   add no key, remove no key and move no data byte. No manifest already served is rewritten.
2. **Is removing the 24-key file from the zip, with the prior zip versions left in the bucket, enough for row W100-S3?** Not decided by this seat. The release stops the artifact the function runs from carrying the account-number-shaped
   runs; the older versions keep them. Removing a prior version is a delete and Andrew's act; this pair does not ask for it.

## 8. Conditions of this half

1. **Build from pins, never from HEAD.** The applier re-reads every pin's sha256 against the packets (REFRESH 4's four and this packet's `aaeb1866ff`); any staged file other than the thresholds file differing from the live
   REFRESH 4 build's bytes, or any member whose bytes differ from the packet's, is a STOP before upload. The member census against live is exactly ONE file.
2. **The sequence is checked, not assumed:** ledger entry first, bound to this packet's sha256; read every live worktree's `.open_deploys/` (`git worktree list --porcelain`, then `git -C <wt> ls-tree`; print the denominator);
   re-read live as `i2r7CbVr` and MemorySize 3008 before upload, else STOP; re-read the latest artifact version id and its `content-sha256` at that moment; one `.tools/safe-apply.sh`; post-apply plan `No changes`;
   `aws lambda update-function-code` is barred.
3. **One dry-run invoke** of the 2026-10-08 backfill is the first act after the apply, read against 2,556.8 MB and 765 s. OVER on either: roll back to `8ELUDq_d2wRKI0kSXEuLXFm6iqgsiAyZ` (the version read at that
   moment), re-record the source-map entry (pin `6be02af162`, sha256 `551920f0c364...`), targeted `safe-apply`.
4. **The scheduled call site is read at the first fire after THIS release** for the six-key `thresholds` object and its claims `measured`, `measured`, `held`, `held`, `inferred`, before the ledger closes.
5. **No `main()` upload** against 49 Financial or Cottonwood under this pair; one change at a time: no other release on the function until that read closes.
6. **The applier is an AE seat the gates admit**, not a worker (as REFRESH 4's condition 6). The apply is not made during another seat's open ledger entry on this function.

## 9. Not established, and so not covered

- The live IAM role and bucket policy (Terraform source only); the Lambda's memory on the new bytes (argued nil: the file is smaller); readers outside the repo.
- The kit comparison and the manifest capture: this seat re-ran the packet's hash, the replacement file's hashes at the pin and at HEAD, the source-map entry, the live function and the rollback version's metadata; it did NOT re-run
  the kit or the capture, and it did not re-read the packet's per-table hashes (they are the worker's).
- Which thresholds file wrote each manifest already served.

-- 2.0.0_SA_COO~D2
