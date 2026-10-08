# NFRA_TRNSPT round 8 -- close record (2.0.0_SA_COO~T2, dell2, 2026-10-08)

Issuance `cecfa091b1` (TR-k8, CTO ruling msg 1519) and addendum 1 `94a1cabe12` (TR-s8, round-7 analysis @117ee1fa17 E2); decomposition
`decompositions/NFRA_TRNSPT_DECOMP_R8.md`. `round-close-check --round 8`: MAY-CLOSE (2 orders, 0 judgment criteria). Branch: box/dell2
(the shared tree moved from CLOUD at 20:00:46Z, msg 1531).

| cell | order | merge | criteria |
|---|---|---|---|
| TR-k-8 (E1) | NFRA_TRNSPT.TO-TR-k8 | `5eaeb0744c` | AC1 R8-K8-NOTLAND-OK; AC2 R8-K8-REVERT-OK (6 files == 8394179dec, test_encrypted_class.py gone, BUNDLE-IMPORT-OK files=61) |
| TR-s-8 (E2) | NFRA_TRNSPT.TO-TR-s8 | `a7c0019d76` | AC1 R8-S8-ALL-OK files=29 rows=20473 failures=0; AC2 R8-S8-WIPE-OK 5 passed |

Drain on the merged tree: transcripts tests `-k "outlook or mail or internal_encrypted or completeness or research_fold"` 117 passed, 0
failed (`test_eod_voice.py` ignored: an unrelated collection error).

## E1 -- the class is reverted (no flag)

The five outlook modules and `test_outlook_silver.py` are byte-equal to `8394179dec` (the first parent of `ff7846f9f7`); the class work
stays recoverable at `ff7846f9f7`. The new fake-route test: an author email to `opalinvest.com` with one `.asc` octet-stream attachment
puts nothing under `/bronze/` (`ingest` 0, `not_landed_not_admitted` 1; the run record itself is always written). TR-k8's proof pins the
revert commit `603cbf62e4`, which carries the change (the analysis's criterion 3). The Lambda was never redeployed with the class.

## E2 -- FWD-5 first slice: the 29 Research transcripts as structured speech

`data/transcripts/scripts/teams/research_fold.py`: 29 of 29 files, 20,473 rows with the teams silver COLUMNS; speaker kept, text through
the mail wipe (name 14,153, id 25, residual flags 2,716; email, phone and theme 0); `start_utc`/`end_utc` None (the stored times are
derived from an operator-stated start, not observed). Nothing went to S3; the worker's local parquet sat in its worktree's `.scratch/`
and was deleted with the worktree.
- Row NFRA_TRNSPT-D2-W2-S2 (INERT): one utterance in `RT-20260409-1029.json` has a null speaker (the file names it UNATTRIBUTED);
  passed through as `None`. Issuer ruling: keep `None` (speaker unchanged).
- Criterion (3), the issuer's read-back (`R8_READBACK_ONE_TRANSCRIPT.json`, counts only): RT-20260803-1003 (2026-08-03) -> 207 rows,
  2 speakers, 207 speaker turns (rows per speaker 104 / 103), offsets on 207 of 207, wipe name 251, id 3, residual 72, 0 failures. Turns
  equal rows: each stored utterance is already one speaker turn.
- Residual flags (2,716) are capitalised words the wipe could not classify; a silver home for these rows would hold them out until
  resolved, as the mail silver does. The store's home is still undecided (PRD :154).
