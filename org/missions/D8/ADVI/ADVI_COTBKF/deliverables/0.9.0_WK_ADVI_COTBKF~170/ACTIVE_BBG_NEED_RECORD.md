# ACTIVE_BBG_NEED_RECORD -- CB-ch-2, round 86 (same figures as ACTIVE_BBG_NEED_RECORD.json)

Builder line (verbatim, `b1_request.py --build --names`, S3 read only, no vendor call):

`{"cells": 154024, "claim": "measured", "clipped_cusips": 681, "days_to_finish": 53, "emptied_cusips": 1, "finish_date": "2027-01-03", "funds_joined": 0, "held_back": 0, "priced_names": 1733, "securities": 1732, "skipped_one_dollar": 0, "total_return_names": 0, "unread_pulled": 0, "window_start": "2013-04-08"}`

| Figure | Value | Note |
|---|---|---|
| Active non-cash CUSIPs (need) | 3,366 | V2 sha256 5cef7ab0c9e10fe299cb757d4dba31792d069bad35f7250defa76e18773046ae; cash removes CASH and CFNCASH |
| In B1 request | 613 | |
| In failed-14 request | 14 | |
| NEW (no request yet) | 2,739 | 3,366 = 613 + 14 + 2,739 |
| NEW priced by the builder | 1,732 | 1,733 priced, 1 emptied by the active-window clip (06829D503) |
| NEW cells | 154,024 | |
| Day rate (history ceiling) | 5,858 cells/day, claim measured | one served ledger day, 2026-10-08; the research note's 23,432 is 4 x 5,858 |
| Days and finish, NEW alone | 27 trading days, 2026-11-24 | trading days from 2026-10-19 (first trading day after 2026-10-17) |
| Cells, NEW + B1 + failed-14 | 196,146 | 154,024 + 34,437 + 7,685 |
| Days and finish, all three | 34 trading days, 2026-12-04 | same counting rule |
| Slices | 27 files; largest 5,856 cells; sum 154,024 | one request file and one quote file per slice |
| NEW names not priced by this builder | 1,006 | no Commonwealth transaction; no window assigned (rule: not_priced_by_this_builder) |
| Value source | silver/holdings, 2026-10-12, column market_value | joined on account_id; 860 of 860 V2 keys present; 746 hold a named CUSIP |
| Baseline, active CUSIPs with a Bloomberg series | 0 of 3,366 | s3://opal-data-assets/bloomberg/ (8 objects, none a series); mdpf/global/silver/security_series/ absent |

Fire-day reading: the builder's own quote (drawer fire days) gives 2027-01-03 for NEW; the order's trading-day count gives 2026-11-24. The record states both; the issuer's rule is not established here.
