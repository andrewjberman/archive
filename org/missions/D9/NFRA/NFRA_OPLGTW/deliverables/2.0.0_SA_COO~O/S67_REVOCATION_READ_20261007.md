# Row Z-S67 -- what revoked the scoped concierge's gateway session at the r28 restart

By: `2.0.0_SA_COO~O`, 2026-10-07 23:2xZ. For `1.0.0_SA_CTO~Z` msgs 31448 and 31452. Three read-only reads, by this seat's own
AWS identity. Counts, times, status codes and generation numbers only: no address, id, email, token hash or principal
is in this file or was printed.

## Verdict

**The restart did not cut a request. The session was revoked on the NEW process, 8 seconds after it came up, during a
burst of token refreshes: 20 requests to `POST /token` in 11 seconds, 15 of them refused.** A drain before the restart
does not prevent that. The cause is on the reconnect side: more than one request presented the same refresh token.

## Read 1 -- the session's records (`gateway-access-state-table`, 22:39Z)

| Event in the concierge's revoked family | Time (1 s resolution) |
|---|---|
| generation 31 issued | 21:27:07Z |
| generation 31 consumed | 21:49:12Z |
| generation 32 issued | 21:49:12Z (never consumed) |
| family revoked, reason `refresh_token_reuse` | 21:49:12Z |

Gap between the last rotation and the revocation: 0 s. Rotations in this family ran a median 1,806 s apart (n = 30); this
one came 1,325 s after the previous. Families revoked in the hour of r26: 0; of r27: 0; of r28: 1 (29 families, 519 records).

## Read 2 -- the host's journal, 21:48:50Z to 21:49:40Z (one SSM command `54f14c72`, 23:1xZ)

403 journal lines, 187 access lines. The host program printed counts only.

- **The stop was graceful and took one second:** 21:49:02 `Stopping`, `Shutting down`; 21:49:03 `Finished server process`,
  `Started`; 21:49:04 `Uvicorn running`. (The same lines as `OG-dr-1`'s read, SSM `99d3aced`.)
- **Access lines per second:** 1 at 21:48:54, then none until 21:49:04; 7, 24, 16, 5, 29, 27, 31, 8, 11, 13, 7, 4 in the
  seconds 21:49:05 to 21:49:16. That is the clients coming back together.
- **`POST /token`, per second, with status codes:**

| second | requests | 200 | 400 | distinct connections |
|---|---|---|---|---|
| 21:49:05 | 3 | 2 | 1 | 3 |
| 21:49:06 | 1 | 0 | 1 | 1 |
| 21:49:07 | 1 | 1 | 0 | 1 |
| 21:49:08 | 1 | 0 | 1 | 1 |
| 21:49:09 | 2 | 1 | 1 | 2 |
| 21:49:11 | 1 | 0 | 1 | 1 |
| **21:49:12** | **4** | **1** | **3** | **2** |
| 21:49:13 | 1 | 0 | 1 | 1 |
| 21:49:14 | 3 | 0 | 3 | 2 |
| 21:49:15 | 3 | 0 | 3 | 2 |
| total | 20 | 5 | 15 | |

In the second the family was revoked, four token requests arrived: one answered 200 (a rotation) and three answered 400.
After it, 7 more requests were refused and none succeeded.

## Read 3 -- this box (22:4xZ)

`opal-gateway-bbg` is configured once, in the user-level `~/.claude.json` (0 mentions in the repo's `.mcp.json`), so every
Claude session of this Windows user holds it. 12 `claude.exe` processes were running. There is one
`~/.claude/.credentials.json`.

## What is shown, and what is not

- **Shown:** the stop was graceful; the rotation and the revocation happened in one second on the new process; token
  requests arrived in a burst from several connections; refusals began in the first second.
- **INFERRED:** that the three 400s at 21:49:12 were the concierge's own sessions presenting generation 31 after the
  first one had rotated it. The journal does not say which family a request belonged to, and this read printed no
  identifier to join on. The source address in the journal is the load balancer's, so "distinct client processes" is
  NOT readable from it: distinct connections (2 in that second) is the nearest count.
- **Not explained:** the 400s at 21:49:05 to 21:49:11, before the concierge's revocation. They belong to some family and
  may be other sessions' refusals of other kinds; they were not classified.
- **A second route exists and was not excluded:** `app/server.py:367-382` answers 503 at a 30 s budget while the work
  still commits (row Z-W35-S1). No 503 was counted on `/token` in this window, so it does not fit this event.

## What follows

1. **`OG-dr-1`'s drain is not the remedy for this event.** Its changes (a bounded graceful stop, stop-then-start with the
   result printed) are built on branch `wk-NFRA_OPLGTW-30-35` @47dd5053b2 and are NOT drained. Whether they ship as
   hygiene is the CTO's.
2. **The exposure is the number of sessions sharing one sign-in.** Up to twelve sessions (the count at 22:4xZ; the count at
   21:49Z was not read) with one refresh token reconnect together after any restart; the first to refresh rotates the token and any other that still holds the old one is
   reuse by the server's rule.
3. **Remedies, for the CTO's ruling, none built:** a client-side one (the Bloomberg concierge's sign-in held by ONE
   session, not by every session on the box; that is a configuration of the box and Andrew's or the integrator's to
   change), or the server-side grace the CTO has already weighed, now with a measured case: a replay in the same second.
4. **Until one lands,** every gateway restart can sign the concierge out, and the release form's 12-hour bar before the
   07:00 America/New_York send stands.
