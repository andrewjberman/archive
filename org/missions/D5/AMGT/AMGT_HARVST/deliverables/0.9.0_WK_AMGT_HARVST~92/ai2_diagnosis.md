# ai-2 diagnosis -- what kills the ft session ~20-30 min after a renewal (0.9.0_WK_AMGT_HARVST~92, round 36)

Rows: Z-W92-S11 (driver `--no-sign-in` on a dead session) and Z-W92-S12 (the session dies again after a renewal).
Diagnosis budget: 25 ft page requests of the 30 allowed (probe 1: 15, probe 2: 10), in `ai2_probe.py`; the cookie reads
make no request.

## Finding

**ft's login cookie `FTSession_s` is a server-held token that the browser is never re-issued, and the server drops it
after a stretch with no page LOAD in the tab. The collector's requests are in-tab `fetch()` calls from one page that was
loaded once at launch, so the session ends ~10-40 minutes after the launch (or a renewal's re-seed) however many
requests are made. A tab that also loads an ft page every few minutes keeps it.**

## Evidence

1. **The cookie is never re-issued.** The profile jar's `FTSession_s` value hash is `cb5f7c9b` at every one of 25 reads
   from 20:08Z to 21:27Z, across fetches and navigations (`ai2_probe.jsonl`, `ai2_probe_fetchonly.jsonl`). In the earlier
   profiles the Chrome cookie row's `creation_utc` = `last_update_utc` (18:42:31Z) while `last_access_utc` ran to
   19:02:56Z: written once at the seed, read for 20 minutes, never rewritten. So nothing in the jar tells a worker the
   session is about to end, and a re-seed cannot be what kills it (the seed runs only on a page that loaded logged out;
   it never overwrites a live cookie).
2. **The deaths are not at a fixed age.** `events.jsonl` + the run records: renewal 16:45:19Z -> first logged-out page
   ~17:19-17:24 (34-39 min); renewal 17:26:11Z -> `auth_failed_after_refresh` 17:37:50 (<=12 min); renewal 18:42:18Z
   -> first locked page 19:00:07, `auth_failed_after_refresh` 19:03:20 (18-21 min). A fixed lifetime from sign-in
   would repeat; these do not.
3. **A tab that loads pages lives.** Probe 1 (renewed 20:06:37Z; one request per 4 min, alternating an in-tab `fetch()`
   and a navigation of the same article, so a page load at most every 8 min): `isUserLoggedIn` true on all 15 reads,
   20:08-21:00:31Z, 54 minutes; the profile was re-opened at 21:02:53Z and read logged in (56 minutes after the sign-in).
4. **A tab that only fetches dies at a low request rate.** Probe 2 (same cookie, same article, `fetch()` only, one per
   3 min after the launch's one page load at 21:02:53Z): logged in at 21:05:53, 08:54, 11:54, 14:55, 17:55, 20:55, 23:56,
   **logged out at 21:26:57Z, 24 minutes after the last page load, on request 10**. 80 minutes after the sign-in, 10 requests,
   one per 3 minutes: it is neither the sign-in's age (probe 1 passed 56 minutes) nor the request rate (0.33 per minute against
   the collector's ~3).

## What was not the cause

- A second session displacing the first: not observed. The cookie hash never changed and probe 1 held 54 minutes
  beside the same other drivers; a concurrent login elsewhere cannot be excluded by a probe, only by the run below.
- A re-seed over a live cookie: the seed is gated on a logged-out page (ah-3) and was never reached in a live session.
- Request rate: probe 2 died at 0.33 requests per minute.
- The renewal path itself: it produces a valid cookie (probes 1 and the run's first fetches read logged in); it only
  looks like the cause because every renewal restarts the clock of a tab that then only fetches.

## Fix

`tab_transport.TabSession.keepalive()`: when a contract names `session_keepalive_seconds` (ft: 300), `get()` loads the
tab's origin as a page (`goto(origin, wait_until="load")`) if that many seconds have passed since the last page load; a
failed load is swallowed (the request after it decides whether the session lives) and restarts the clock so it cannot loop.
`publishers._ensure_session` hands the contract value to the tab; every other publisher is unchanged (13 plants,
`test_ai2_ft_session.py`). The cadence, 5 minutes, sits inside the 8 minutes probe 1 held for 54 minutes.

Also (premise failure, row Z-W92-S15): the browser profile root follows the CHECKOUT the code runs from, not
`--runtime-root`, so a job run from a worktree against the main tree's runtime used the worktree's own ft profile.
`OPAL_HARVEST_PROFILE_ROOT` now names the profile root explicitly; unset it changes nothing.

## Run

See `ai2_run_log.txt`, `ai2_ft_longevity.json` and the closing section of this file.
