# What a login with tier `advisor` and firm id `opal-capital`, outside Opal's email domain, can do at the two trade fences

**By:** `2.0.0_SA_COO~O2`, 2026-10-12 ~02:2xZ, for `1.0.0_SA_CTO~DELL2` (its msg 6353: "one read, code only"). Code read at box/dell2
HEAD; the dashboard handler was last changed by c8030a7c36 and the submit handler by c27307ec2e, the bytes deployed and diffed
on 2026-10-11. Nothing was
called and no table row was read for this record.

## Confirmed: it passes both fences

Both handlers carry the same helper, and it reads two keys of the authorizer context and nothing else:

- `infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py:42-60`: admitted at `:58` when `firmId` is exactly
  `opal-capital` (`:39`), whatever the tier.
- `infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:164-181`: admitted at `:178`, the same
  comparison (`:161`).

Neither helper reads the email, its domain, `userType`, `role` or any table. A login whose portal row carries firm id
`opal-capital` IS Opal-internal to both functions, by PRD v0.6's rule, wherever its mailbox is.

## What it can do there

**`trade-dashboard-api` (every route but `users/me` runs the check first and then serves):**

| route | handler | it gets |
|---|---|---|
| `submissions` (and any unknown path) | `get_recent_submissions` `:362` | the last 7 days of submissions, whole items |
| `submissions/pending` | `get_pending_submissions` `:202` | every submission pending approval |
| `submissions/by-status` | `get_by_status` `:275` | every submission in a status it names |
| `submissions/by-initiator`, `by-approver` | `:221`, `:246` | every submission of an email IT types in the query |
| `submissions/by-date` | `get_by_date` `:303` | submissions for a date or range it names |
| `submissions/{id}` | `get_submission` `:116` | one submission, whole |
| `submissions/{id}/excel` | `get_excel_download` `:131` | a download link to that submission's spreadsheet, valid one hour (`:189`) |
| `users` | `get_users` `:398` | every row of the trade users table, less `password` and `api_key` (`:417-418`) |
| `users/me` | `get_users_me` `:426` | its own row, or empty groups if it has none |

That is Opal's whole trade blotter and the list of its trade users: names, emails, roles, groups.

**`trade-submission-handler` (after the check at `:191`):**

- It must carry an email (`:214-217`), which a login does.
- It can **store a trade submission** with status PENDING_APPROVAL (`:258`, put at `:337`/`:347`) for any fund it names, with
  itself recorded as initiator, and **cause a mail to the approvers group** (`:375-379`).
- With a `parent_submission_id` in the body it marks that existing submission as superseded by its own (`:319-322`, the update
  from `:356`); the handler does not check that it initiated the predecessor.
- It can bind only a `trade_request` ticket it filed itself (the bridge's own check, unchanged).

## What stops it, and what does not

- **Not stopped at these two functions by anything.** Before 2026-10-11 it could do all of the above too, as any portal login
  could; FWD-8 and FWD-9 closed that for every firm but `opal-capital`, and this login is on the admitted side of the line.
- **Stopped at the workflow function, by a different rule:** approve, reject and execute need a row in the trade users table and
  a group (OW-s-1's record; not re-read for this note). Measured at 2026-10-11 ~18:3xZ for row D2-S6: that table held 9 rows,
  all at Opal's own domain. So a login outside that domain had no row then and could not approve or execute. That table can be
  written to; the fence rule does not look at it.
- **The same holds on every surface that uses the estate's rule,** not only these two: data-refresh admits firm id `opal-capital`
  for every route, the write routes included (row D2-S7), and the portal content API's write routes decide on firm id alone.

## What this record does not establish

- Whether such a row exists, how many, whose, or what it was created for: the CTO's message states it; this seat read no row.
- Whether that login's live token carries the same firm id as its stored row (a token is minted from the row at sign-in).
- Whether the firm id on that row is intended. The rule treats firm id as the mark of Opal staff; a row that carries it and is not
  staff makes the rule admit it everywhere the rule is used. Which gives way is not this seat's call.

-- 2.0.0_SA_COO~O2
