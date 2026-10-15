# R3-custodian-number (CB-ci-3, round 87) -- record

Counts only (the record is JSON beside this file). The links themselves are in the outside file `C:/dev/_cotbkf_match_20261015/R3_LINKS.csv` (sha256 in the record), not in the repository.

| Figure | Value | Denominator |
|---|---|---|
| R3 links, DETERMINISTIC | 88 | 88 Commonwealth accounts, 88 distinct account_ids |
| AMBIGUOUS (a custodian number held by two account_ids; not linked) | 1 Commonwealth account, 2 candidates | 1,533 crosswalk accounts |
| New links (served crosswalk NOT_MATCHED) | 86 | 88 deterministic links |
| New links to an active account (REVERSE_MATCH_V3 key) | 0 | 86 new |
| New links among the 219 reachable unmatched active accounts | 0 | 219 |
| Control: already MATCHED and linked | 2 | 88 deterministic links |
| Control: agree (current account = bd account_id) | 2 | 2 |
| Control: disagree | 0 | 2 |

Custodian numbers: 1,001 distinct non-blank in the three most recent fact_holdings partitions (date=2026-10-12, 10-13, 10-14; 94 partitions listed).

Reachable denominator: 387 unmatched active accounts (REVERSE_MATCH_V3 `none`), less 168 new clients after the migration = 219.

Against the research (87 new, 0 active, control 2 of 2): the control agrees (2 of 2) and the active yield is 0. New is 86, not 87: the research's figure includes one AMBIGUOUS Commonwealth account (two candidates, not linked by the rule). Both candidates are closed accounts outside the 860 active keys.

The value of R3 for the active 219 is zero on this measurement, as the order anticipated.
