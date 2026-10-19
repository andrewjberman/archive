# IBcw1 notes -- 0.9.0_WK_IRPT_BCKEND~456 on IRPT_BCKEND.TO-IB-cw-1

**Verdict: UNDETERMINED.** The order's STOP clause applies: the replay did not reproduce the six. Read at worktree HEAD e7bf14ca0f (branch wk-IRPT_BCKEND-456). Read-only throughout: no --upload, no --local-out, no S3 put, no AWS write, no Lambda invoke, no SSM command. Clients appear only as 12-hex hashes of the opaque client key.

## 1. Stage order, source read to entry set
File: data/assets/scripts/gold/investor_reporting/directory_runner.py at e7bf14ca0f.

1. :431 FirmCOT.load calls read_fact("fact_allocations", business_date); this is the only source table read (no advisor or ownership map).
2. :790 and :796 build_cot takes data["allocations"] and iterates its records.
3. :800-802 rid = _s(Relationship ID); a blank or NaN spelling becomes the sentinel "0".
4. :803-806 THE ROUTING: a sentinel row goes to ungrouped (:804); any other row is appended to by_rel[rid] (:806).
5. :824-833 one relationship entry per by_rel key; client_raw = rid.
6. :834-841 one account-only entry per ungrouped row; client_raw = AccountID.
7. :859 BUILDERS table maps "cottonwood" to build_cot; :1243 run_firm calls it.
8. :974-977 source_raw_keys_cot = non-sentinel Relationship IDs union AccountIDs (stripped by _raw_ids, :953-960); :980-982 source_client_ids mints the opaque client keys.
9. :1275-1276 carry_forward_removed runs against the previous served entries; :997-999 held = a previous key absent from the build and present in the source.
10. :1288-1293 refusal text; :1291-1292 raises only when upload or local_out is set; a dry run records carry_info refused and main fails it.

The drop stage is :803-806: the account's account-level key is not emitted once its row carries a real Relationship ID. Line 803 sha256 (stripped, at HEAD): ded1b3d1aaea212c6c47a76f3cb4bd33128e8bd8957d6e45198d467849815198.

## 2. Parked link (checked first)
- The parked item: the Cottonwood ownership map (the account-to-advisor link) at s3 opal-data-cot platinum/cottonwood/ownership_map.json, 107 bytes, advisors=0, per the probe in investigation row IRPT_BCKEND-W144-S1 (INVESTIGATION_v1.md, heading at line 19695).
- used_by_build: false. directory_runner.py has no reference to ownership_map, platinum or an advisor map; FirmCOT.load (:431) reads fact_allocations only. The "advisory" hits at :477-480 are UNKNOWN constants, not reads.

## 3. Replay (rc=1)
Command: python data/assets/scripts/gold/investor_reporting/directory_runner.py --firms cottonwood --as-of 2026-10-14 --dry-run. Raw stdout kept outside the repository. Lines, ids masked:
- OK: firm=cottonwood bucket=opal-data-cot entries=260 valid=260 of 260 as_of=2026-10-14 source_completion=2026-10-14 uploaded=False
- CARRIED: held_in_source 11, previous_as_of 2026-10-12, previous directory key investor-reporting/directory/2026-10-12/directory.json
- ERROR: REFUSED: BUILD_DROPS_SOURCE_ENTRY: 11 previous client(s) are still in the source snapshot but missing from this build; nothing is landed.

The premise was 6 (ruling part (a), row IRPT_BCKEND-D2-S239). Today's replay refuses 11.

## 4. Bisect (after the STOP point, reads only, aggregates only)
Scratch script outside the repository; printed counts and 12-hex hashes only.
- Source keys 1087. Build 258 entries (251 unique client keys, 7 duplicated keys); 2 previous entries carried TERMINATED (absent from the build and from the source), giving the 260 the replay reports.
- Previous served directory (as_of 2026-10-12): 271 entries = 220 relationship + 51 account-level; 11 duplicated client keys.
- Gone from the build: 16 entries. Held in source: 14 entries = 11 unique keys, all account-level in the previous directory.
- For 11 of 11 held keys, the account's alloc rows carry a non-sentinel Relationship ID (8 keys with one row, 3 with two; 0 mixed); 11 of 11 accounts are still present in a current entry's account_ids. They were re-keyed from account level to relationship level, not removed.
- Control: 28 of 28 retained account-level keys have sentinel-only rows; 0 regrouped.
- Whitespace: 0 of 864 AccountID values and 0 of 224 Relationship ID values carry surrounding whitespace, so the strip-based source mint and the build mint agree.
- Held keys, 12-hex hashes of the opaque client key (11 unique): 0d67b0367f1c, 23a70853e5e5, 37f25b195dea, 3d7cc5f6a7de, 4bd43c85dc13, 68c79182651a, 70800f44a454, 91af2d199d7e, c0181547ec24, eae34753da55, fcf4d1947b4f.

Shared attributes, held 11 against the control of 28 account-level retained keys:
- Non-sentinel Relationship ID on the account's rows: held 11 of 11; control 0 of 28.
- Account still present in the current build: held 11 of 11.
- Account Market Value above zero on some row: held 11 of 11; control 26 of 28.
- Two or more alloc rows: held 3 of 11; control 7 of 28.

## 5. Verdict reasoning
- The six cannot be reproduced read-only, so the verdict for the six is UNDETERMINED.
- Today's 11 are a re-key, not a removal: each account is still served under a relationship entry, and the 10-14 source assigns it a Relationship ID that the 10-12 directory lacks. The guard compares client-level keys (:997-999), so the re-key reads as a drop.
- Whether any of the six 10-14 clients is among these 11 needs the 10-12 source and the 10-14 served state, neither read here.
- The findings contract (dropped_count 6, six distinct ids) cannot be filled honestly from 11 keys, so no findings file and no proof instance were written; the order's refusal clause says to write nothing further beyond the notes.

## 6. Surprise rows filed (INVESTIGATION_v1.md, appended)
- IRPT_BCKEND-D2-W456-S1, class BLOCKING, hazard INERT: the replay refuses 11, not 6.
- IRPT_BCKEND-D2-W456-S2, class OBSERVATION, hazard INERT: the re-key mechanism at :803-806.
- IRPT_BCKEND-D2-W456-S3, class OBSERVATION, hazard INERT: duplicated account-level client keys (11 in the 2026-10-12 directory, 7 in today's build); the per-row emission at :834-841 is the probable cause, not verified.

## 7. Criteria
AC1 and AC2 run before the commit fail on the missing findings file; AC3 is run after the commit. The proof instance was not written (STOP).
