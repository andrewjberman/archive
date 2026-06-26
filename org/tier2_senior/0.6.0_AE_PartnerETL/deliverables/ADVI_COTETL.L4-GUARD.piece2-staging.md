# ADVI_COTETL.L4-GUARD PIECE 2 — staged design (rewire cot 02:00 -> canonical gateway-self-fetch auto-login)

**Owner:** 0.6.0_AE_PartnerETL · **Status:** STAGED (2a) — architecture GREEN (CTO 132034Z + 135423Z), activation HARD-GATED on 0.7.0 (2b) + CVO 6-clause.
**Why staged-not-built-yet:** the box-side env (secret-ids.env: adapter, gateway URL, token secret-id) + the A/B hardening live in 0.7.0's in-flight gateway config; the cot-exporter user-data change risks box REPLACEMENT (apply must be a planned box-cycle, not now while the box is mid-unfreeze). So the TF/box build is bundled into the ONE atomic box-up window (2d) with 0.7.0 + CVO, to avoid rework, TF-vs-live drift, and an accidental box replacement.

## Ground truth (verified this session)
- HOST = cot-exporter box `i-0643a5bee8a8feabf` (t3.large, `cot-exporter-ec2-role`); canonical auto-login CO-LOCATED at `/opt/bd-cot-auto-login/`, Node v18.20.8 present (hand-added). Firm-sep CLEAN + IAM-confirmed (Deny opal-data-bd Stmt-9 live).
- OLD path (to retire): SSM `opal-cot-bd-session-fetch` pulls `s3://opal-data-cot/code/bronze/cot_bd_session_fetch.py`, runs `python3.11` (MFA-failing).
- Canonical invocation (49F ref): `run-bd-auto-login.sh` -> sources `$APP_DIR/secret-ids.env` -> `node $APP_DIR/bd_49f_auto_login.js`. Firm selected by `BD_FIRM_ID`; OTP by `BD_OTP_ADAPTER`.
- Session write shape compatible: OLD writes `{bd_identity, all_cookies, captured_at, expires_at}` to `blackdiamond/cot/session`; canonical writes the same bundle (bd_identity present); keepalive/freshness/bronze all parse it. No consumer-shape break.
- OTP mailbox: cot + 49F BD OTP emails are CONTENT-IDENTICAL (sender `noreply@bdreporting.com`, subj "Authentication Code You Requested") and BOTH land in `Andrew@opalinvest.com` (= gateway OTP_MAILBOX). Gateway disambiguates by RECENCY only.

## Build steps (executed in the atomic 2d window, with 0.7.0 + CVO)
1. **SSM re-point** `opal-cot-bd-session-fetch` (or a new `opal-cot-bd-autologin` doc + flip the cot-bd-session-trigger SESSION_FETCH_SSM_DOCUMENT): run the canonical via the wrapper — `cd /opt/bd-cot-auto-login && . secret-ids.env && node bd_49f_auto_login.js` with `BD_FIRM_ID=cot`. Code via S3->box pull (Rule 12); no inline.
2. **IAM delta** (cot-exporter-ec2-role): + `secretsmanager:GetSecretValue` on `blackdiamond/cot/otp-gateway-token-*` (explicit — cot has NO cot/* wildcard). KEEP Stmt-9 Deny opal-data-bd intact. Verify via comp-iam TF-vs-live reconcile (authoritative get-role-policy fallback — census stale 06-03).
3. **Box env** (secret-ids.env, 0.7.0/deploy): `BD_FIRM_ID=cot`, `BD_OTP_ADAPTER=gateway`, `BD_OTP_GATEWAY_URL=https://mcp.opalinvest.dev/otp/fetch`, `BD_OTP_GATEWAY_SECRET_ID=blackdiamond/cot/otp-gateway-token`.
4. **Node durability**: add Node v18 to `infra/aws/ec2/cot-exporter/user-data.sh` (currently python-only) so a box re-provision doesn't regress the canonical. Apply only in a planned box-cycle (user_data change can force replacement).
5. **APP_DIR fix**: `/opt/bd-cot-auto-login/run-bd-auto-login.sh` has stale `APP_DIR=/opt/bd-49f-auto-login` (fork-shadow). CONFIRM nothing consumes the stale value first (CTO: if read, it's a latent cross-firm path-bleed, not cosmetic), then point at `/opt/bd-cot-auto-login`.
6. **Schedule**: shift cot session trigger to `cron(30 2 ...)` (02:30, clear of the cron(0 2) cluster) — supporting hygiene.
7. **Cleanup (2e, after gateway proven)**: drop the cot/otp-relay R/W (Stmt-4) — least-privilege.

## CTO hardening reqs (LOAD-BEARING — carry to 0.7.0 gw-code)
- **(A) Tight since-trigger window:** cot box passes its login-trigger timestamp to /otp/fetch; gateway accepts ONLY a code received AFTER the trigger, within ~120s. Shrinks collision window to cot's own ~1min OTP arrival.
- **(B) Retry-on-login-failure:** a mis-grabbed code = a FAILED cot login (loud via PIECE 1) -> box RE-TRIGGERS (fresh OTP -> re-fetch) -> self-healing, not a re-freeze blip.

## Named residual (known-accepted risk)
If a 49F 401-login fires AND its OTP lands inside cot's tight post-trigger window (both post-trigger, BD gives no firm-pin), the gateway picks by recency; if wrong, the cot login FAILS LOUD and retries (B). Rare + loud + self-healing = ACCEPTABLE. The one thing that must NEVER happen — a silent wrong-firm MINT — is precluded by CVO clause-6 (200-mint = right code) + retry (B). Recency (not schedule) is the primary disambiguator since 49F OTPs are event-driven/unpredictable.

## Dependencies / gates
- **2b (GATING):** 0.7.0 provisions `blackdiamond/cot/otp-gateway-token` + adds gateway-role GetSecretValue + proves /otp/fetch e2e for cot (incl. A+B). Until then, do NOT activate (a re-pointed run with no gateway OTP just fails — loud via PIECE 1, but needlessly).
- **Activation (2d) gate:** CVO 6-clause unattended-self-fetch SOUND (incl. recency-correlation + the sharpened adversarial case: a 49F code arriving WITHIN cot's window).
- Interim bridge (acceptable ~1-2 days, CTO): PIECE 1 loud detection + manual reseed/bronze-run (proven this session). cot data fresh through 06-26.
