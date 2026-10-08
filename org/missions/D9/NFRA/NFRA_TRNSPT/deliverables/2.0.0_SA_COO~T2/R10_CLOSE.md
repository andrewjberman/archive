# NFRA_TRNSPT round 10 -- close record (2.0.0_SA_COO~T2, dell2, box/dell2, 2026-10-08)

Issuance `2c39c4fc74` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R10.md`, CTO round-9 analysis @9c6c91c505). TR-q10 merged
`6cd69560aa` (AC1 `R10-Q10-READ-OK 4 passed`); drain 127 passed, 0 failed.

## The analysis's criteria

- (2) a held-out row is never returned -- `test_held_out_row_never_returned` PASS; live: 4,555 held-out rows skipped, 0 examined.
- (3) a company named in no meeting returns empty with its reason -- `test_unnamed_company_empty_with_reason` PASS; live control
  `Zyxwvutco`: count 0, reason "no stored non-held-out turn mentions 'Zyxwvutco' (stored text is wiped)".
- (1) one real covered company from S3, counts only, no file opened by the caller (`R10_COMPANY_READ.json`): **NVIDIA** (+NVDA) -> 8 turns
  in 5 of 29 meetings, 2 speakers; 15,918 non-held-out rows scanned.

## FINDING -- the wipe removes company names (row NFRA_TRNSPT-D2-S5)

Whole-word counts in the unwiped `research_transcripts/structured/*.json` against the stored, searchable rows:

| company | raw utterances | stored matches |
|---|---|---|
| Microsoft | 67 | 0 |
| NVIDIA | 32 | 8 |
| Apple | 24 | 0 |
| Broadcom | 15 | 0 |
| Exxon | 6 | 0 |

The mail wipe (`outlook/wipe.py`), applied to transcript text by the issuer's round-8 ruling, treats capitalised company names as person
names (14,153 `name` replacements over 20,473 rows). The read works, but FWD-5's ACCEPT ("what was said about one company") is not met
for most companies. The remedy is a CTO ruling: a company-preserving transcript wipe (or a securities allowlist), then a re-fold and a
re-write of the 29 silver objects (a SERVED act via the laptop, as in round 9).
