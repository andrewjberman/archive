# The resolve hop's WAF back-off: the design, drafted while AQ2's lookup read is out (issuer 2.0.0_SA_COO~G2, 2026-10-16)

STATUS: a DRAFT held for the CTO's branch. CTO msg 9429: if AQ2's ONE cookieless lookup answers CLEAN, the issuer cuts this change in its own cell and pair; if it is still challenged, NOTHING is cut and the pattern goes to the CTO. Nothing here is built, ordered or committed to a worker. Claim words: CODE = read at HEAD; INFERRED = said so.

## What the code already knows

- CODE (`ycharts/generate/resident_worker.py` lines 860-864, written from the CTO's batch 262 and the 2026-10-05 probes): "The YCharts firewall window measured on 2026-10-05 lies in (122, 373] s: a redelivery 122 s later was challenged (batch 97 item 4), and after 6 requests a 7th 373 s after the first answered (WAF-PROBE-20261005T1254Z-W330). 390 s clears the window." The generation hop's read-back already waits 390 s on the same challenge (`READ_BACK_RELEASE_VISIBILITY_S`).
- CODE (lines 858, 877, 978-989): a resolve hop RETRY is re-sent with `VisibilityTimeout = RESOLVE_RETRY_VISIBILITY_S = 60` for every cause, at most `RESOLVE_MAX_RECEIVES = 4` receives (strictly below the queue's maxReceiveCount 5), then `_end_exhausted_resolve`. So a WAF challenge is retried at 60 s, 60 s, 60 s: three more tries, all INSIDE the measured (122, 373] s window, the one spacing known to be challenged. That is the shape SET 2 showed (four challenged receives, then exhaustion).
- CODE (`intake/upload_resolution.py` line 24): `REDRIVE_SECONDS = 960`. The client re-dispatches a still-RESOLVING row only after 960 s, which is the 900 s receive plus margin; a back-off whose total stays at or under 900 s cannot be doubled by a client re-dispatch.

## The change (the smallest that matches CTO msg 9429)

Only the `RETRY` branch of the resolve poll (`resident_worker.py` lines 978-989) changes. For a RETRY whose detail code ends with `:WAF_CHALLENGE`, the visibility timeout is taken from a growing schedule by receive count instead of the flat 60 s:

- `RESOLVE_WAF_BACKOFF_S = (150, 300, 450)`; receive 1 re-releases for 150 s, receive 2 for 300 s, receive 3 for 450 s, receive 4 is `RESOLVE_MAX_RECEIVES` and ends the row as today (`RESOLVE_RETRY_EXHAUSTED`). Total back-off 150 + 300 + 450 = 900 s = the CTO's 15-minute cap, under `REDRIVE_SECONDS` (960) and the queue's receive limit. Attempts fall at t = 0, 150, 450 and 900 s: the second and later attempts are spaced past or at the measured window's edge (the 450 s and 900 s attempts clear it; the 150 s attempt sits at its lower edge and is the one most likely challenged again).
- Every other RETRY cause keeps 60 s (a 503, a timeout, the BUSY class keeps its own re-send path).
- The journal line for a RETRY gains the delay it chose (`... code=PROVIDER_READ_UNAVAILABLE:WAF_CHALLENGE visibility=150`), so the class and the spacing are named on each retry (CTO msg 9429 item 2).
- No new state, no new message field, no change to `_end_exhausted_resolve`, to the door's lookup (it stays sessionless, batch 72 item 12) or to the lease.

## Tests on both sides (the cell's criteria, written as issuer checks dry-run at the base before the cut)

1. A RETRY with code ending `:WAF_CHALLENGE` at receive counts 1, 2 and 3 sets `VisibilityTimeout` 150, 300 and 450 and prints `visibility=`; at receive 4 it ends the row (`RESOLVE_RETRY_EXHAUSTED`) and deletes the message (unchanged).
2. A RETRY with any other code (`STATUS_503`, `BODY`, a timeout) still sets 60 at every receive; the BUSY class still takes its re-send path.
3. A code that merely CONTAINS `WAF_CHALLENGE` in the middle (not at the end) takes 60 (no loose match); a missing or non-string code takes 60.
4. The back-off total equals 900 and is at most `REDRIVE_SECONDS`, and `RESOLVE_MAX_RECEIVES` stays below the queue's maxReceiveCount of 5 (an assertion test, so a later edit that breaks the margin fails).
Mutants the issuer's check must fail: a flat 150 for every cause; the schedule applied to every RETRY cause; a loose substring match; a schedule that sums past 960.

## Named, not claimed

- That the challenge is rate/window-based: the 2026-10-05 measurement says so for the generation hop; SET 2 is consistent (the retries at 60 s were inside the window). The sessionless lookup's challenge could also key on the host's address; AQ2's read prints the address and ONE lookup's answer. If that lookup is challenged, this change does not apply.
- That the fifth upload of a SET is always the one challenged: SET 2 had the challenge at lookup number 5; SET 1 did not.
- A filer's upload now shows RESOLVING for up to 15 minutes before it ends in NEEDS_CORRECTION on a persistent challenge (it was about 3 minutes). That is the CTO's cap.
- Cell, pair, build and apply follow the r34 pattern: a worker cell on `resident_worker.py` and its test, a new resident release (r34f, own names), the CTO's pair, AQ2's apply with V2 in the service's own environment. Not started.
