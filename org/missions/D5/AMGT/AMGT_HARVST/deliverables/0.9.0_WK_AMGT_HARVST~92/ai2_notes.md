# ai-2 progress notes (0.9.0_WK_AMGT_HARVST~92)

- 20:06Z one renewal through auth.SessionManager.refresh (ai2_renew.py); 20:08Z probe holds the main tree's ft profile at
  one request / 4 min (ai2_probe.py, ai2_probe.jsonl). 20:32Z: logged in, 8 requests, FTSession_s value hash unchanged
  (the server never re-issues it on fetch or navigation).
- Premise failure: the browser profile root follows the CHECKOUT, not --runtime-root (tab_transport.default_profile_root);
  OPAL_HARVEST_PROFILE_ROOT added so a worktree job can use the main tree's profile.
- Earlier-run evidence (events.jsonl): renewals 16:45, 17:26, 18:42Z; first logged-out page ~35, <=12, ~18 min later.
