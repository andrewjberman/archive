# PER-DOCUMENT ROWS -- MX-s-14 amendment A2, the AC1/AC2/AC3 predicates on the other 3 BD documents (PHASE A cut)

Written by 0.9.0_WK_NFRA_MCPINDEX~17 for the L9 reader. `proof-of-spec-check.py` refuses an acceptance row whose id is not
in the task order's expected set (AC1,AC2,AC3), so these rows live beside the proof instance, which grades the transaction
document as written.

Live reads, 2026-09-29 ~07:1xZ (ssm describe-document / get-document `$LATEST`, events describe-rule):

| document | AC1 predicate: Default==Latest; playwright refs=0; BD_PASSWORD refs=0; merge refs>=1 | AC2 predicate: rule ENABLED, 1 target | AC3 predicate: successful scheduled run after the PHASE B GO |
| --- | --- | --- | --- |
| opal-bd-allocation-download | FAIL: Default 3, Latest 4; playwright 1, BD_PASSWORD 2, merge 2 (served, unedited) | allocation rule ENABLED cron(0 22 ? * MON-FRI *) read; target count not re-read | not computable before PHASE B (slot 22:00Z) |
| opal-bd-realized-download | FAIL: Default 2, Latest 2; playwright 1, BD_PASSWORD 2, merge 2 | not re-read (MX-i-5 dead proof read ENABLED; no rule changed) | not computable before PHASE B (slot 21:45Z) |
| opal-bd-unrealized-download | FAIL: Default 2, Latest 2; playwright 1, BD_PASSWORD 2, merge 2 | not re-read (same) | not computable before PHASE B (slot 21:38Z) |

The AC1 FAILs are the served, unedited documents by design (PHASE A). Offline on the EDITED command lists: playwright 0,
BD_PASSWORD 0, merge 2 for all three. AC3 rides each document's next scheduled weekday fire after PHASE B.
