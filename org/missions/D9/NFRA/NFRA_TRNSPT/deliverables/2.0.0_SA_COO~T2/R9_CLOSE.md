# NFRA_TRNSPT round 9 -- close record (2.0.0_SA_COO~T2, dell2, box/dell2, 2026-10-08)

Issuance `623a05b7e9` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R9.md`, CTO round-8 analysis @08ff07562f, ruling msg 1542).

| cell | carrier | result |
|---|---|---|
| TR-w-9 | NFRA_TRNSPT.TO-TR-w9, merged `01e971915c` | AC1 `R9-W9-WRITE-OK 3 passed`; drain 123 passed, 0 failed |
| TR-x-9 (SERVED) | laptop `NFRA_TRNSPT.TO-RUN-x9` @f2f40005b3 by `0.7.0_AE_CloudOps` (msg 1566), run from `01e971915c` | 29 objects written 2026-10-08T20:41Z |

**Why the laptop wrote it:** the transcripts key grants the Dell users Decrypt and DescribeKey only (`DellAgentUsersDecryptOnly`); an
SSE-KMS put needs GenerateDataKey. Routed through `0.0.0_AB_MSTR~DELL2` (msgs 1554, 1555, 1566). The prefix held 0 objects before the
write (measured 20:2xZ; positive controls: silver 58, bronze 1,938).

## The analysis's three criteria, read back by the issuer from S3 (dell2 decrypts)

Record `R9_READBACK_STORED.json` (this folder; counts and keys only).
1. **Address:** 29 keys under `s3://opal-data-transcripts/teams/transcripts/silver/research_meeting/date=<YYYY-MM-DD>/<id>.parquet`, equal
   to `research_fold.write_all(..., apply=False)` (the builder's `address()` output): TRUE. No registry row was needed.
2. **Rows:** 20,473 stored; **held_out 4,555, not held out 15,918**.
   - Reconciled against the analysis's 2,716 (msg 1567, item 1): 2,716 is the count of DISTINCT residual-flagged words that
     `wipe_blocks` returns (its flag list is de-duplicated). `held_out` is a per-row flag (a row drew at least one residual flag), so
     4,555 rows carry the 2,716 words. The difference is 1,839 rows. Row NFRA_TRNSPT-D2-W1-S2.
3. **Wipe on the stored bytes:** re-running `wipe_blocks` on every stored non-held-out row finds name 0, id 0, email 0, phone 0.

The laptop's own counts-and-keys file (msg 1566) has not arrived at this close; the issuer's read-back above is the grading artifact.

## Rows this round

- NFRA_TRNSPT-D2-W1-S2 (INERT): held_out rows 4,555 vs the 2,716 flag count (above).
- NFRA_TRNSPT-D2-S4 (INERT, `e312c474a0`, CTO msg 1567 item 2): a second producer (Teams chat-assist; probable owner NFRA_CTLPLN, unconfirmed)
  wrote 71 `teams/transcripts/bronze/chat_messages/` and 4 `teams/transcripts/state/chat_assist/` objects into this bucket on 2026-10-08.
