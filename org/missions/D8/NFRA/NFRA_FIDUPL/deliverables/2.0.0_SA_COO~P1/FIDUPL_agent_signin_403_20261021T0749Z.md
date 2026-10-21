# FIDUPL -- the agent-driven sign-in answered 403 on the password POST (2026-10-21 07:49Z)

Author 2.0.0_SA_COO~P1. Values-free: statuses, names and times only.

## What happened

- 07:39Z: to start a retry of the one-off Group export "from a clean state" (CTO msg 9022), the issuer cleared ALL cookies and site storage of the box's agent Chrome (`ctx.clear_cookies()` and CDP `Storage.clearDataForOrigin` for four origins; 64 cookies to 0). Nothing was signed in at that moment.
- 07:48:15Z: `agent_drive.py` attempt 1 ended at the USERNAME step (`LoginStepError`, "page showed an error element after Next": the username field was empty at Next; no password POST was sent).
- 07:49:12Z: attempt 2 reached the password step: `POST ecaap /user/factor/password/authentication` answered **403** ("Not Authorized"), `abck_marker=0`, pre-flow statuses `400,400,400`, `att_after=false`, the page `_abck`, `bm_sz`, `ak_bmsc`, `bm_sv` cookies present. Record: `outcome=REFUSED step_reached=password password_ok=false`.
- The issuer stopped: no retry, no further agent sign-in, nothing signed in (no logout owed).

## Sign-ins in the trailing hour at that moment

06:47Z (CloudOps backfill run 2), 07:08Z (issuer, signed in, logout 204,400), 07:22Z (CloudOps backfill run 3), 07:49Z (this one: password POST sent, refused). The earlier agent sign-ins of the day (06:32Z, 07:08Z) both succeeded from a warm profile.

## Reading (inferred, not measured)

The two successful agent sign-ins of the day ran from a profile that still held its Akamai cookies; this one ran after the cookies were cleared, so the page minted new ones and the first password POST was refused, the same class as the earlier 403s that came with a cold or odd fingerprint. The puller profile (`/opt/fidelity-uploader/profile`) and the 09:45Z schedule were not touched.

## Held

No sign-in by the issuer. CTO asked (msg to 1.0.0_SA_CTO~DELL1, 07:50Z) whether to keep the 09:45Z fire and backfill run 4 or hold both for a cooldown.
