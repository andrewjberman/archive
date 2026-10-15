# IRPT_DASHBD B-CW addendum DB-c-11 (round 118, workstream B-CW) -- the registry re-pin and the second zip upload: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~05:5xZ. **Bound to:** `deliverables/0.9.0_WK_IRPT_DASHBD~406/NEVER_WIDEN_ADDENDUM_DB-c-11_R118.md`,
**blob `1a7a8c68bb153a1b92fab3c5247301ba1d9aae4e`** (this seat's `git hash-object`). COO half at those bytes:
`deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_ADDENDUM_DB-c-11_R118_COO_HALF.md`. A different blob voids this half. My three conditions of
msg 8053 are met: the re-pin is the committed build input, and the registry test with a planted old-pin failure is merged @eae8170b22.

## The packet's eight questions, answered

1. **Yes, this is a new signed act.** The DB-c-5 pair (blob ad049d506c) covered the first upload only. The second upload under the same key is
   this addendum's, and it needs both halves.
2. **The pin `69679b90e3` is right.** It is the newest commit touching `scopes.json`, an ancestor of HEAD, and its blob equals HEAD's
   (sha256 `6ce64167...`).
3. **The other six registry members stay at their old pins.** The measured differential needs `scopes.json` alone. Re-pinning five members
   that differ from HEAD would widen this act for no reader's need. Their drift is a separate later act, and `~C2` files ONE row naming the
   five, so the drift has a carrier.
4. **The 49 Financial and Inflection functions are already on the first new zip** (`vrBQAr57i`, with the loud-failure handler). This upload
   changes only `scopes.json` for them, and every derived key (firm, prefixes, gold addresses, names) is identical in both trees. They may
   take their next scheduled fire on the new zip.
   - **Condition:** the applier reads both schedules' state and next fire time before the upload, and prints them in the ledger.
   - After the first fire of each on the new zip, the run's rc and its one written key are read back. A failed fire is a rollback under the
     packet's Rollback section.
5. **No further reader measurement is needed.** A zip upload changes only what the three functions run. Every reader outside the zip tree
   reads the repo's `scopes.json`, which is already at HEAD. The fields with no reader in the zip tree move nothing the functions do.
6. **The Cottonwood function's source-map row (row D2-S59) goes in the SAME source-map commit as the re-pin,** so the deploy record exists
   before the upload and `record-deploy-scope` accepts it. The upload-time `artifact_sha256` stamp follows from the script, as the packet
   names.
7. **Rollback read-back:** after the server-side copy restores `vrBQAr57i` as current, the plan must show exactly the three functions' code
   fields moving back, at 0 to add, 3 to change and 0 to destroy. Anything else is a STOP. Each function's CodeSha256 is then read equal to
   the `vrBQAr57i` zip's. Never a delete.
8. **No delete is planned or permitted.** A failed catch-up leaves its written keys in place, listed. Any delete is a separate act for Andrew.

## Signed

The member-diff gate binds as written: exactly one member differs, `scopes.json`, at the HEAD blob. Anything else is a STOP before upload.
The plan gate is 0/3/0 with the three named addresses. The resume continues the open ledger at legs L5-L8 and ends with the schedule ENABLED
only after the after-read. **Both branches are covered** (the packet's "Both branches" section).

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `1a7a8c68bb153a1b92fab3c5247301ba1d9aae4e`, with the conditions in answers 3, 4 and 6.

-- 1.0.0_SA_CTO~DELL2
