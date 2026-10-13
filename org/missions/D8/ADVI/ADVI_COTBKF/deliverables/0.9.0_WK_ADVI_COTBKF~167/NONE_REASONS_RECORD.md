# NONE_REASONS_RECORD -- round 84, CB-cf-1, 0.9.0_WK_ADVI_COTBKF~167

Of the 273 reasonless none rows: NEW_CLIENT_AFTER_MIGRATION 152 (41 with a CUSIP-overlap candidate), MISMATCH_NO_IDENTIFIER 89 (all with a candidate), OTHER 32 (NO_CANDIDATE_OVERLAP 32; LINKED_NOT_RECORDED 0), NO_COMMONWEALTH_HOUSEHOLD 0 (no household key exists on the target side). Migration date 2026-06-23. 496 other rows byte-equal. REVERSE_MATCH_V2.csv: 769 rows, sha256 993858e306b2d9d5955d7c77dfd2a9c7ec620ec42ea6c048cfda83a6a5a1d065.

- List commit: 9442dec344bcc75358d5898e3f7b8dafec59c2d4 at 2026-10-13T23:04:24Z (NONE_REASON_LIST.md, written before any classification read); population sentence corrected in b8de2ba3580bdf7113fe1a483add6761d67e089d at 2026-10-13T23:07:53Z (before any classification read)
- Counts by code (sum 273): NO_COMMONWEALTH_HOUSEHOLD 0, NEW_CLIENT_AFTER_MIGRATION 152, MISMATCH_NO_IDENTIFIER 89, OTHER 32
- Accounts with a CUSIP-overlap candidate, by code: NO_COMMONWEALTH_HOUSEHOLD 0, NEW_CLIENT_AFTER_MIGRATION 41, MISMATCH_NO_IDENTIFIER 89, OTHER 0
- Unchanged rows: 496, byte-equal: True. Diff control: 1 mutant row changed, 1 reported.
- File: C:/dev/_cotbkf_active_set_20261013/REVERSE_MATCH_V2.csv, 769 rows, 82451 bytes, sha256 993858e306b2d9d5955d7c77dfd2a9c7ec620ec42ea6c048cfda83a6a5a1d065

## Not established
- Household join: none. The 273 target keys appear in neither crosswalk.csv nor account_links.csv (0 of 273), and no Black Diamond-side household identifier exists in the holdings read. account_links client_line is shared by 183 values across Commonwealth rows but joins to no Black Diamond key. NO_COMMONWEALTH_HOUSEHOLD is therefore assigned to 0 rows.
- Key space: the 273 target keys are 71-character tokens; the 457 matched keys are 11-character raw ids. The holdings partitions (account_id) and the crosswalk carry raw ids only, so no partition read joins a target (0 of 273 in silver and in gold). Tying the tokens to the raw holdings needs the salt, which this worker did not use or open.
- Migration date 2026-06-23 is a choice: the first day after the last Commonwealth Trade_Date (2026-06-22). The Black Diamond silver start (2026-06-08) would give different NEW_CLIENT counts; not computed.
- NEW_CLIENT_AFTER_MIGRATION uses the earliest held_from of the account black_diamond windows in the active-set file, not a partition read (see key space). A window starts on the first date its security appears on the Black Diamond side.
- Snapshot CUSIPs are the CUSIPs of windows with held_to open. 130 of 273 accounts have no open window carrying a CUSIP, so the candidate test is void for them; their non-candidate classification rests on that absence.
- A candidate is a Commonwealth account with a pre-migration transaction (Trade_Date before 2026-06-23) in a CUSIP the account holds. Shared fund CUSIPs count. Because the target key appears in no crosswalk or account_links row, every candidate is unjoined by key; MISMATCH_NO_IDENTIFIER therefore means CUSIP-overlap candidate with no key join available, not evidence that the crosswalk tried and failed.
- Identifiers that would settle a match (holder name, tax identifier, account title) are absent from every column of crosswalk.csv and account_links.csv and from the holdings columns read.
- The 14 crosswalk-current raw accounts outside the 769 were read at the 2026-10-12 snapshot: 239 rows across 14 accounts; the only non-zero-units rows (3) are cash-equivalent; none holds a non-cash unit. They are not among the 769.
- OTHER sub-codes are counted here only; the CSV carries reason OTHER for all 32 rows, as the list requires a code, not a sub-code, in the file.
- Gold canonical holdings were not filtered on its source column (the record states the BD side of that table is not established per row).
- The crosswalk reason_code column (for example NO_CURRENT_ACCOUNT_HOLDS_POSITIONS, CLOSED_BEFORE_CURRENT_HISTORY) is a Commonwealth-side reason not in the closed list and was not used.
- Account-level counts only. No account key, number or value appears in this record or in the report. Raw downloads sit under the worktree .scratch folder (gitignored, never committed).

