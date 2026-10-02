# HVST-aj-5 path finding -- the bbg article 403 (job 20261002T065754Z-bbg-4f3bfa12bd, signature bloomberg_press_and_hold)

Line numbers are at CLOUD 4720f6975a (the base of this worktree, before the aj-5 edits).

## The path the driver's per-name shape takes

1. `backfill_driver.py:172-179` (`Collector.run_job`) spawns `python -m lib.opal_data_harvest run --harvest-grammar
   --retrieval-mode backfill --new-only --no-sign-in --security-json ... --publishers bbg --max-jobs 1`. `--no-sign-in` is
   why the run record reads `signed_in` false (`worker.py:449` default; it flips true only at `worker.py:694` and `:708`,
   both refresh branches that `--no-sign-in` refuses).
2. `contracts.json:72-79` gives bbg `"transport": "tab"`, so `publishers.py:357-362` builds a `TabSession` and
   `publishers.py:392` wraps it in a `PacedSession`; `tab_transport.py:69` sets `solves_challenges = True`.
3. `Publisher.bloomberg` (`publishers.py:797-799`) takes `_tab_listing()` (`publishers.py:670-684`, true for a built tab
   session on a publisher in `discovery.ROUTES`), i.e. `_bloomberg_sitemap` (`publishers.py:701-745`): monthly news
   sitemaps through `discovery.discover` (`discovery.py:84`), then each article by `self.session.get(url)`
   (`publishers.py:732`). That is where the 403 arrived.
4. `transport.request_kind` (`transport.py:153-161`) labels a URL "listing" when its path holds `/news`; every bbg article URL
   is `/news/articles/...`, so an ARTICLE fetch is recorded `request_kind: "listing"`. The "listing" label is a
   substring match, not evidence of a listing request.
5. `PacedSession.get` (`transport.py:275-327`): a 403 whose body matches a bot-check signature is classed `bot_check`
   (`_attempt_class`, `:400-410`); with `solved` false and `_routes_challenges()` true (`:373-378`: inner
   `solves_challenges` and bbg in `verification.CHALLENGE_PUBLISHERS`) it calls `route_bot_check` (`:292-303`), which
   calls `verification.solve` (`verification.py:393-397`, `solve` at `:342`). The solve therefore IS reached in this shape.

## Why no event and no capture exist for the failed job

- The only solve outcome the transport recorded was `challenge_passed`, on success (`transport.py:308-309`). A solve that
  did not pass raised `ChallengeFailed` (`verification.py:398-399`) with NO event at all, and the attempts row for it is the
  one appended at `transport.py:299-301`, identical in every field the run record keeps (`request_kind`, status, `class`,
  `signature`) to the row of a request that never reached a solve. The run record cannot tell the two apart.
- `challenge_presented` did not exist yet: aj-1 (`ed10da285e`) committed 2026-10-02T03:14:41-04:00 = 07:14:41Z, after this
  job (06:57:54Z start, 403 at ~06:59:52Z).
- The capture fires only from `solve()`'s `on_control` hook (`verification.py:358-361`, called by `_solve_press_and_hold`
  at `:308` only once the PRESS & HOLD control is located), and `challenge_capture.capture` refuses a second capture inside
  an hour (`challenge_capture.py:99-111`, `:121`). A solve that never located the control (`acted` false, path "none",
  `verification.py:366-374`, `:381`) captures nothing, and bbg's 06:38Z capture already held the hour.

## Finding

The code at the base routes this 403 into `verification.solve()` (`transport.py:292-303`), so "reached no solve()" is not
what the code does for a tab-transport bbg leg; the missing solve record is a recording gap (a failed solve emitted no event,
and its capture was cap-bound and control-bound), and the run record's attempts row is identical either way. What the
records cannot establish is WHY the solve did not pass; aj-5 now records the outcome of every solve, captures the failure
regardless of the cap, and retries once. Rows AMGT_HARVST-Z-W90-S13 (the premise difference), -S14 (the mislabel), -S15 (retry gated on an
unpassed solve) and -S16 (grader definitions the order left open) are filed.
