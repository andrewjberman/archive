# IRPT_DASHBD round 51, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~15:4xZ)

For `3.0.0_SA_CVO`. The issuer re-graded the order in its worktree and again at box/dell2 after the drain. round-close-check: orders=1, complete 1,
verdict MAY-CLOSE.

| order | worker | risk | criterion (issuer re-grade at HEAD) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-104` lots status key via `address()` | ~79 | WORLD | DB51-1-AC1 PASS (88/88; 1 of 1 firm key equal) | @98ae364e98 |

- **The change.** The typed `LOTS_STATUS_KEY` is gone. `_lots_status_location(firm)` builds the bucket and key from
  `address('irpt', firm, 'gold', 'account_activity_daily', '_status', 'lots_not_computed.json')`, as laptop 4.0.0_SA_CRO ruled (MSTR msg 3555).
- **The key's bytes are unchanged** for the one firm the handler serves, 49financial:
  `irpt/49financial/gold/account_activity_daily/_status/lots_not_computed.json`, before and after. A mutant control (the pre-edit handler) FAILs
  the check.
- **No deploy.** The change rides the next gold release with DB-b-97 under its own pair (CTO ADDENDUM 16 item 1). Both changes are in `handler.py`,
  so that release's census should show one changed member.
