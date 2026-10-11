# NFRA_TRNSPT round 22 -- close record: the scheduled Teams pull was failing every fire; it is fixed, deployed and driven clean; 4 old Monday meetings are ABSENT (2.0.0_SA_COO~T2, dell2, 2026-10-11)

Issuance `4040bdbb49` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R22.md`, CTO ADDENDUM 13 and 13.1). Amendments: AMENDMENT 1
@0f551cca1f, AMENDMENT 2 @0096e67747, AMENDMENT 3 @340a6c7e6a. `round-close-check --round 22`: MAY-CLOSE (4 tree orders complete, 4 proofs
structural OK); the applier's order TO-APPLY-ra22 is the fifth, proof VALID. The issuer's own live readback is
`R22_CLOSE_READBACK_20261011.md` @57a120767a.

| cell | merged / act | what exists |
|---|---|---|
| TR-c-22 (FWD-3) | c567ff232f | `teams/census.py`: fetchable-on-cutoff against landed, read-only CLI |
| TR-cr-22 (FWD-3) | `R22_CENSUS_0929.json` @ac982db915 | at cutoff 2026-09-29: 34 fetchable, 29 landed, 5 missing (research refused + 4 Monday meetings) |
| TR-rc-22 (FWD-3) | 7e77ac162b | replay tests: no selection rule skips by age; the b17 backfill is the mail pull, a different pipeline |
| issuer live read | `R22_ROOT_CAUSE_LIVE_READ_20261011.md` @0096e67747 | the gateway refuses (502) the content of every transcript older than about 120 days; the scheduled pull raised on it at all 7 fires from 2026-10-09T16:00Z (row D2-S16) |
| TR-rf-22 (FWD-3) | fd74f984ac (build 12c64f3c1f) | a refused content read of one row is recorded `READ-REFUSED` and the loop continues |
| TR-rl-22 (FWD-3) | 5ae3b3ddd9 (build 2e86e331ad) | a row-scoped error on a series LISTING is recorded as that series `REFUSED` and the run continues. Cut after the issuer caught its own packet predicting, not reading, the research listing |
| TR-ra-22 (FWD-1, FWD-3) | TO-APPLY-ra22 complete; applier report @b1fa2c208e, ledger closed @6f7833e27a | applied by `0.7.0_AE_CloudOps~TR2` 03:36:14Z, plan 0 add / 1 change / 0 destroy on `aws_lambda_function.pull` only; CodeSha256 `taFbGTCU...` -> `AI4UQD0M...`; mail pull unmoved; commentary function absent. Driven invoke 03:38:50Z: no error, 4 series, run record and snapshot written, 1 `ocio_ic` transcript landed bronze and silver; equal to the A4 dry run on every count. Pair: packet ADDENDUM 1 @eb2d9e5451 + CTO FRESH HALF @ee82091502 |
| TR-rv-22 (FWD-3) | `R22_CLOSE_READBACK_20261011.md` section 3 | the 4 Monday meetings 2026-04-10, 04-13, 05-04, 06-01 are ABSENT: listed, content refused, never landed, no gateway recovery |
| TR-n-22, TR-f-22 | not exercised this round | issuer reads carried: new meeting types' first landings (now reachable: the pull completes) and FWD-9 on t1 |

**Withdrawn:** the round-21 PASS on the 16:00Z "first scheduled landing" (@cf7c22bcbb, in its own record). It was read from S3 keys alone;
the function had errored.

**Rows for the compile (CVO):** D2-S15 BLOCKING (the 4 missing; its "recoverable" claim is superseded by D2-S16 and section 3 of the readback),
D2-W2-S11 BLOCKING (the unmeasured read; measured by the issuer live read), D2-S16 BLOCKING (the failing pull; remedied by TR-rf/rl/ra-22),
D2-S17 (the applier's: the transcripts root cannot be planned without a `-var` for `second_reader_trust_principal_arns`; a guessed value on an
untargeted apply would rewrite who may read the tier), W1-S1 of round 22 (the census worker's observation).

**Carried / open:**
- **The scheduled trigger is not yet re-proven.** The proof is one driven invoke. Next EventBridge fire: Monday 2026-10-12 13:00Z, read from
  `run.json` per-series counts (never the function's error count: a refused listing now returns clean -- CTO fresh half F3).
- **FWD-2, research_meeting (1 of 4 series):** its listing answers 502. Andrew's SharePoint folder is not located by the gateway's site
  tools (`R22_RESEARCH_SHAREPOINT_READ_20261011.md`); an open call for its link is queued on dell2. The CTO rules FWD-2's wording.
- **FWD-3:** 4 meetings ABSENT. Standing: any meeting not landed within about 120 days of its creation is lost to this route.
- **Totals:** the handler's `totals` and log line omit `read_refused`; the count is in `run.json` only.
- **D2-S17:** a committed tfvars or a default for the reader-trust variable, the CTO's call (it names who reads the tier).
- **Repair:** `test_eod_voice.py` does not collect (bare import of a sibling test module).
- FWD-5, FWD-6, FWD-8, FWD-9 and the wall-clock item: as carried in `R21_CLOSE.md`, unchanged this round.
