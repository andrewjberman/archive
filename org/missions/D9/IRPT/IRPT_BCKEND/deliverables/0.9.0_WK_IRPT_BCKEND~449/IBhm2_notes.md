# IB-hm-2 -- notes (worker 0.9.0_WK_IRPT_BCKEND~449, branch wk-IRPT_BCKEND-449, base 44518fb9a3)

**Convention.** `emit_hmac_list` (directory_runner.py) is the LAST stage of `run_firm`, called after `land()` inside a
`try` whose handler catches `Exception` and prints one `ERROR: hmac list stage failed: <class>` line. For each firm it
hashes two families of token forms with `HMAC-SHA256(key, form_utf8)` and writes lowercase hex, one per line, sorted,
unique, LF-terminated, ASCII, to one key (`--hmac-list-uri`, the firm's own bucket, outside the directory prefixes). The
key bytes are the UTF-8 `SecretString` of one Secrets Manager secret (`--hmac-secret-id`), read once per process. Raw
account keys are collected in process by `_entry` (`_HMAC_RAW_KEYS`, reset at the start of `run_firm`); a raw key `r`
gives `UPPER(r.strip())` and, when different, `UPPER(r with '-' removed)`; a minted `acc_<24 hex>` gives `UPPER(hex)`.
Empty input writes nothing (`skipped_empty`); no arguments skip (`skipped_no_args`); a run that does not upload skips
without reading the secret (`skipped_no_upload`). The stage prints only its OK, INFO and ERROR lines.

**Base test count.** At 44518fb9a3, before any edit, `pytest data/assets/scripts/gold/investor_reporting/tests -q
--continue-on-collection-errors`: 329 passed, 136 failed, 20 ERROR entries; three modules fail collection.

**After test count.** The same command after the change: 339 passed (329 plus the ten new tests), 136 failed, 20
ERROR entries. The failing and error sets are identical to base and every base-passing id still passes. The ten new
tests in `test_directory_hmac_list.py`: 10 of 10 passed.

**Criteria.** AC1 and AC2 were run before the commit (see IBhm2_criteria_output.txt). AC3 reads `HEAD~1..HEAD`, so it is
run after the commit and recorded by the amendment.

**Surprise rows filed** (INVESTIGATION_v1.md): IRPT_BCKEND-D2-W449-S1 (no status for upload-off with arguments), S2
(one URI cannot name one key per firm; main refuses several firms), S3 (the folder is not green at base).

**Not in this cell.** No AWS call, no secret, no dispatch, no grant change. The arguments are inert until a later cell
passes them.
