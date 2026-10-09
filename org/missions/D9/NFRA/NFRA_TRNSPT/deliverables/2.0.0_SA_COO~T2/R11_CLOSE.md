# NFRA_TRNSPT round 11 -- close record (2.0.0_SA_COO~T2, dell2, box/dell2, 2026-10-08)

Issuance `7fa942c9ba` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R11.md`, CTO round-10 analysis @8ce4b5098e, ruling msg 1608).

| cell | carrier | result |
|---|---|---|
| TR-a-11 (E1) | NFRA_TRNSPT.TO-TR-a11, merged `9f8dddcb9b` (three seats) | AC1 `R11-A11-LIST-OK version=1 tokens=6697 source_rows=5207`; AC2 `R11-A11-GATE-OK 5 passed`; drain 145 passed, 0 failed |
| TR-b-11 (E2, SERVED) | laptop `NFRA_TRNSPT.TO-RUN-b11` @40e54f5a06 by `0.7.0_AE_CloudOps` (msgs 1705, 1741), from `9f8dddcb9b` | 29 objects rewritten 21:50Z as new versions (priors retained; prior VersionIds in the laptop file @38acf0c577) |

## E1 -- the securities allowlist

Source: the served security master, DynamoDB `etf-classifications` (the canonical per-security table), snapshotted by the issuer at the cut
(`data/transcripts/scripts/teams/securities_source_20261008.json`: 11,172 rows read, 5,207 equities with a name; ticker and name only).
`securities_allowlist.json` v1: 6,787 tokens (6,697 distinct lower-cased), every ticker plus each issuer's distinctive name word.
- **ARMED row D2-W1-S3, disarmed by issuer ruling (amendment 1, `6d53f93adf`):** 556 name tokens that are also person-dictionary words
  were excluded, so a bare person name equal to an issuer word is still wiped (`test_colliding_person_name_still_wiped`, "Allison").
  Stated loss: "Apple" is a dictionary name and is wiped. The AC1 check was amended to match (`f8d33113db`, row D2-W1-S4).
- The mail wipe (`outlook/wipe.py`) is unchanged; the research fold widens `Assets.allow`.

## E2 -- read back on the STORED bytes (`R11_READBACK_STORED.json`, counts only)

1. **The five-company re-probe; Microsoft > 0 is the arm -- MET:**

   | company | raw utterances | stored, round 10 | stored, round 11 |
   |---|---|---|---|
   | Microsoft (+MSFT) | 67 | 0 | **49** (16 meetings) |
   | NVIDIA (+NVDA) | 32 | 8 | 29 (13 meetings) |
   | Broadcom (+AVGO) | 15 | 0 | 10 (3 meetings) |
   | Exxon (+XOM) | 6 | 0 | 3 (3 meetings) |
   | Apple (+AAPL) | 24 | 0 | 0 -- the ruled loss |

   (Raw counts include held-out rows; the read returns non-held-out rows only.)
2. **The re-wipe and an independent PII sweep at 0:** `verify_stored` re-wipe name 0, id 0, email 0, phone 0; an independent regex sweep
   of the 16,829 non-held-out stored rows (not the wipe): email addresses 0, phone-shaped numbers 0, digit runs of 8+ 0.
3. **held_out:** 3,644 rows (round 9: 4,555; delta -911 -- company names no longer draw residual flags).

The laptop's own result (msg 1741) agrees: 29 rewritten, 20,473 / 3,644 / 0.

## Rows

D2-W1-S3 (ARMED, disarmed by the amendment), D2-W1-S4 (resolved by `a3a11edf07`), both on TR-a11's branch.
