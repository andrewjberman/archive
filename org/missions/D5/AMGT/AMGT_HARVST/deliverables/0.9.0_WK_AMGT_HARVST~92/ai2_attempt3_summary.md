# HVST-ai-2 attempt 3 summary (record-only re-seat)

All times 2026-10-02 UTC. Each value cites its source file.

Sign-in (ai2_attempt3_signin.json, ai2_attempt3_signin_log.txt)
- 02:37:59 to 02:38:37 (harvest_rc 0), one headed sign-in.
- hCaptcha challenge seen and solved by hand (human.challenge_seen true, solved_by_hand true, waited_s 10).
- Vendor calls: kimi_vision_calls 0, nopecha_solver_calls 0, blocked_http [].
- FTSession_s present in the bundle; 57 cookies saved to the vault; 1 network auth event.

Jobs (all ft, ASML security-81a74ed057551e58; ai2_ft_longevity.json, ai2_run_log.txt, ai2_attempt3_job2_log.txt, ai2_attempt3_job3_log.txt)
- Job 1: 02:41:10 to 02:41:24, status error, fetched 0, stored 0, auth_refreshes 0 (0.2 min).
- Job 2: 02:56:25 to 03:15:27, status error, fetched 49, stored 2, auth_refreshes 0 (19.0 min).
- Job 3: 03:30:29 to 03:53:24, status sign_in_refused, fetched 36, stored 0, auth_refreshes 0 (22.9 min).
  Record detail: "401 under --no-sign-in: no refresh", no_sign_in true (ai2_ft_longevity_job3_attempt3.json).

Interval
- Sign-in end 02:38:37 to job 3 end 03:53:21 (record finished_at 03:53:21.76; log 03:53:24): 74 min 45 s.
- Sign-in end to job 3 start (03:30:29): 51 min 52 s.

Keep-alive page loads
- None are recorded. The run logs and the three run records contain no keep-alive or page-load lines
  (checked in ai2_run_log.txt, ai2_attempt3_job2_log.txt, ai2_attempt3_job3_log.txt, ai2_attempt3_signin_log.txt and the longevity json files).
  AC1 covers the cadence code in tests only (ai2_attempt3_ac1.txt, 16 passed).

AC2 (ai2_attempt3_ac2.txt)
- JOBS 3 span 72 min statuses ['error', 'error', 'sign_in_refused'] auth_refreshes 0 stored 2
- AC2 RESULT: FAIL (1 failure(s)): span 72 min < 120. rc 1.
- The check's span is earliest start to latest finish (02:41:10 to 03:53:21), which includes cooldown gaps.
