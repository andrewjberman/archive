# NFRA_TRNSPT round 7 -- close record (2.0.0_SA_COO~T2, dell2, 2026-10-08)

Issuance `820c4ba8c5` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R7.md`, CTO round-6 analysis @57d1574255; rulings msgs 1480,
1482). `round-close-check --round 7`: MAY-CLOSE (2 orders, 0 judgment criteria).

| cell | order | merge | criteria |
|---|---|---|---|
| TR-c-7 (E1) | issuer act | this commit | census below |
| TR-g-7 (E2) | NFRA_TRNSPT.TO-TR-g7 | `ff7846f9f7` | AC1 R7-G7-CLASS-OK passed=2; AC2 R7-G7-GOLD-OK passed=1 |
| TR-h-7 (E3) | NFRA_TRNSPT.TO-TR-h7 | `4641939188` | AC1 R7-H7-MATCH-OK passed=14 |

Drain checks on the merged tree: transcripts tests `-k "outlook or mail or encrypted or completeness"` 115 passed, 0 failed (with
`test_eod_voice.py` ignored: an unrelated collection error, `ModuleNotFoundError: test_teams_chat_tenant`); `commit-gate.sh` clean on 6
files; Lambda bundle import `BUNDLE-IMPORT-OK files=61`.

## E1 -- the encrypted-attachment census (D2-S2 closed: not client feedback)

Record `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R7_E1_ENCRYPTED_CENSUS.json` (counts and recipient DOMAINS only). Window
2026-06-10..2026-10-09, the pull's own sender table, every listed message and attachment list fetched as the pull does.
- listed 395; author 395; author with encrypted-only attachments **368**; client test PASS **0**, FAIL **368**.
- FAIL recipient domains: ONE domain, `opalinvest.com` -- not in the client-domain table, Opal-internal YES (368 of 368).
- The 08-11 pair: both to `opalinvest.com` (internal).
- **Verdict:** not a data gap. The encrypted-only author mail is internal (to Opal), not client feedback, so the 08-11 pair correctly
  stays out. Under msg 1480 the ENCRYPTED_UNVERIFIED class would have landed **0** messages in these 120 days.
- A first run died on a gateway connection reset (WinError 10054) and kept nothing; the recorded run used per-request retries
  (`fetch_failed` absent from the counts = 0).

## E2 -- the ENCRYPTED_UNVERIFIED class (code and tests; NOT deployed)

`criterion.classify` gains `encrypted_only` and `admission_class` (FEEDBACK / ENCRYPTED_UNVERIFIED / None; `ingest` unchanged);
`pull.run` lands the class and counts `encrypted_unverified` (issuer accepted its `landed_dates` addition); the bronze sidecar records
the class; silver adds an `admission_class` column and holds such rows out; gold never emits one. Row NFRA_TRNSPT-D2-W1-S1 (the 19-column
silver pin) was resolved under amendment 1 (`1d490ae4c4`): the pin moved to 20. **The served Lambda does not carry this code**: a deploy
is a SERVED act with its own ledger and halves, not in this round; given E1 (0 qualifying messages in 120 days), it changes no landed
data when it ships.

## E3 -- FWD-4 matching within +/-1 day

The live record re-run from the round-6 inputs with `match_tolerance_days=1`: `R7_COMPLETENESS_RECORD_20261008.json` (this folder).
- The two suspected shifts: monday_meeting 2026-07-20 -> `here`, basis `bronze (+1 day: 2026-07-21)`; 2026-09-07 -> `here`, basis
  `bronze (+1 day: 2026-09-08)`.
- Counts (33 occurrences): **here 28, not_allowlisted 2, never_recorded 3** (asset_management_ic 2026-06-23, monday_meeting 2026-06-22,
  2026-09-21); research_meeting refused at series level. The 2-day negative is TR7-h7's test.

## Drain notes

- TR-g7's slot was re-seated once (the finished seat cannot resume). The re-seat's proof instance pins its `test_outlook_silver.py`
  artifact to `3d731bab5b`, which does not carry that change (the real commit is `07070c8622`); recorded here, not repaired.
- An issuer shell error while amending TR-g7 (an unquoted heredoc executed backticked words) ran `test_outlook_silver.py` as a shell
  script and one read-only pytest command; every line failed or was read-only, and the order file was restored from the branch before the
  amendment was redone with the Edit tool.
