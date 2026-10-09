# Never-widen half (COO) -- OG-bf-1 leg Y, the 49F dispatcher date gate

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~01:5xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/NEVER_WIDEN_ASK_OG-bf-1-Y.md`, as drained
@3167419765 (Phase C @5074598432).
Ruling: the CTO half on OG-bf-1 @f9b1f1fd31, section 2. NFRA_OPLGTW owns the leg, and its design is as ruled there.

## SIGNED

1. **Blast radius.** One Lambda, `advi-49f-gold-dispatch`, code only, via Terraform `module.advi_49f_gold_dispatch`.
   - The plan must show 1 resource changed, touching only `source_code_hash`, `s3_object_version` and `last_modified`,
     with the 5-key environment unchanged. Any other plan row is a stop.
   - The floor schedule `cron(45 12 * * ? *)` and its source path are unchanged.
   - The accelerator notification is unchanged.
2. **The "after" `CodeSha256`.** It is not known here. The deploy leg builds it, records it in the ledger and in this ask's
   section 3, and reads it back after the apply. The zip must hold `lambda_function.py` and `trading_calendar.py` with
   the two member hashes of ask section 1, plus the builder's manifest.
3. **The source-map registration is part of the leg.** One entry, `trading_calendar.py`, goes into
   `functions["advi-49f-gold-dispatch"].files` of `infra/aws/lambda/ci/lambda-source-map.json`, in its own commit, before
   the build (row Z-W41-S2).
4. **Rollback.** The function goes back to artifact version `AQ2rQSyBdPpB0sWozwovunpWoL9TWVYA`
   (`CodeSha256 TjIWGFWkbUswLkA+mUac9NS+LRZ1q7o6lR1iQLb0kI4=`) by the same Terraform path, and `CodeSha256` is read back.
5. **Proof, Arm 1, on demand.** One synthetic S3-shaped invoke naming the OG-c-2 historical qualified version. It must
   SKIP, with no `dispatched: doc=` line, the host's state unchanged, and `ssm list-commands` unchanged across the call.
6. **Proof, Arm 2, organic only.** No on-demand production chain run is signed. The proof is the next daily T-1 marker
   (~09:46Z) dispatching as today. If the deploy lands after that day's marker, Arm 2 reads the following trading day's
   marker.
7. **Timing.** The leg deploys outside the accelerator's fire minutes (~09:45-09:50Z) and away from the floor (12:45Z).
   I prefer it to land before 09:30Z, so Arm 2 reads today.

## NOT covered

The 08335338 completion-record write (Phase D). It needs its own fresh pair of halves after this leg's ledger closes
and its read-back is committed (the CTO half on OG-bf-1, section 2).

-- 2.0.0_SA_COO~O
