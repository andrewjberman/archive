# NFRA_TRNSPT round 16 -- close record: household optional; two served runs carried to round 17 (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `4ad5e91ea0` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R16.md`, CTO msg 2205). TR-h16 merged `2d3bcce249`:
`R16-H16-OK 4 passed`; drain on the merged tree `data/transcripts/scripts/tests/` 367 passed, 0 failed (with `test_eod_voice.py` ignored: it
fails to import `test_teams_chat_tenant`, LDO-001's file from `f9ba6ba8a8`, not this project's); `round-close-check --round 16` MAY-CLOSE.

- **TR-h-16 (row D2-S7):** `ticket_client.py` omits `answers.household` when the context has none; the title is always "Draft commentary --
  <firm> (<report_type>)", never built from household, at most 300 characters (contract v0.2 @20784c5462, section 8).
- **TR-a-16 (the Apple re-write) and TR-b-16 (the ONE 365-day backfill): NOT RUN, carried to round 17 as issuer acts.** Both were routed to
  laptop `0.7.0_AE_CloudOps` (msgs 2211, 2220; MSTR relayed with GO, msg 2223). Laptop `1.0.0_SA_CTO` frame 24e5ac25 item (3), relayed by
  `0.0.0_AB_MSTR~DELL2` msg 2229 (Andrew-direct ~02:5xZ, the Dells run their own scripts), moved both to `0.7.0_AE_CloudOps~DELL2` and stood the
  laptop down; they are reissued only after MSTR relays the laptop's stand-down, so neither runs twice. The pair follows the executor: COO half
  amended `1bb934be65`; CTO half AMENDMENT 1 (msg 2232) adds condition 6, a simulate of kms:GenerateDataKey/Encrypt and s3:PutObject first.
- **Baseline read at 02:52Z** (counts only, issuer read): Research silver 29 objects, all last modified 2026-10-08T21:50Z, Apple 0 turns,
  Microsoft 49 / 16 meetings, verify_stored re-wipe 0 over 20,473 rows (held_out 3,644) -- identical to `R11_READBACK_STORED.json`, so no
  re-write has landed. analysis_commentary: bronze 20 keys / 5 dates, silver 5 keys / 5 dates (2026-07-06..2026-10-01), gold 0.
- **Vendor hold ended:** LAW EDIT 4d77a9c3ea (egress open except Bloomberg; MSTR msg 2240); CTO ruled it ends the Kimi call (msg 2252; PRD v0.3
  ADDENDUM 1 @1a298a7f6c). Open call dell2-20261009T015641Z-1889 is answered by that ruling.
- **New BLOCKING row D2-S8** (`4d6e134c7d`): `commentary.tf` omits five env names `lambda_handler._live_ports()` reads and the svc-commentary
  secret read. CTO agreed (msg 2259): a round-17 cell completes it, the composition read stays in the apply pair, addresses from `address()`.

Round 17 rectangle (proposed to the CTO): TR-c-17 commentary.tf completion (row D2-S8); TR-a-17 and TR-b-17 the two carried runs on
`0.7.0_AE_CloudOps~DELL2`; then the Lambda's never-widen pair on the merged bytes.
