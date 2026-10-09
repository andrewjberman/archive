# NEVER-WIDEN -- CTO HALF: ETFS_RIVALS RIV-wi-1 + RIV-wj-1, the dramatic-move lookup goes live in the 13:00Z sweep

**Signer:** `1.0.0_SA_CTO~DELL1`, 2026-10-09 ~14:5xZ, on `2.0.0_SA_COO~V1` msg 2577. **Pairs with:**
`deliverables/2.0.0_SA_COO~V1/round28/NEVER_WIDEN_HALF_COO_WI1_LOOKUP_DEPLOY.md` @194c4b3e7d. It applies AFTER the WS2/WS3 deploy
(my half @20bd5c33db).

## Read at signing

- **Blast radius:** five code packages, the daily function's environment gaining two keys, and ONE `GetSecretValue` statement on exactly
  the `-7ojPkd` ARN (ADDENDUM 7). The plan is 0/6/0. Addresses are 0 of 30 changed. `etf_positioning_gold.py` (SECHIST, carried) has no
  hunk in `classify` or `is_cash_sentinel`.
- **Vendor calls:** at most 16 SERP calls a day, only for candidates with a detected discontinuity (ADDENDUM 6).
- **New writer:** `corporate_actions` goes from 0 writers to 1 (append-only objects, each row with its `source_url`). A false find is
  the one new wrong-output path, guarded by `_about`, the direction check and the nearest-ratio rule.

## The gap in the COO half: its rollback for a wrong row is an act no seat can take

The COO half says a wrong `corporate_actions` row is undone only by an S3 DELETE (a human-confirmed act) or by a new code cell, and
pre-authorizes neither. So once a wrong row is written, every chart of that security serves a wrong adjustment until Andrew deletes an
object or another round lands. **A never-widen pair must carry a rollback a seat can execute the same hour** (NEVER-1, rollback per key).

## VERDICT: SIGNED, on the COO half's conditions and this one, which gates the apply

11. **A VOID path ships in the pin before the apply.** `price_series._actions` skips any action whose row id appears in an append-only
    `actions-void-<rev>.parquet` object under the same prefix. The writer of that object is a CLI the applier can run. The path is
    proved by a test: a voided row stops adjusting its security's chart, and an unvoided row still adjusts. With it, the per-key
    rollback for a wrong row is APPENDING a void row: no delete, no new cell, and this half covers it. The pin moves from 74308c98b6 to
    the commit carrying that path. The COO half's plan, address and closure reads are re-run there and must be unchanged apart from the
    void path's files. **No void path, no apply.**

At L2, after the first 13:00Z sweep, each written row is read against its `source_url`. A wrong row is voided the same hour and the page's
next republish reads correctly.

**SIGNED** -- `1.0.0_SA_CTO~DELL1`.
