# TASK ORDER — ADVI_BDAPIMIG.P1-DURABLE

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<date>2026-06-29</date>
<priority>HIGH — sole 49f unfreeze path (Andrew declined the manual reseed band-aid; durable port IS the fix)</priority>

## Objective

Port cot's durable self-re-minting auto-login to the **49f BD box** so 49f re-mints its own
`.bd.identity` like cot does → bd_silver lands daily → the cookie-dead/silver-stale alarm storm goes
quiet because the underlying condition is gone (NOT by muting it). Rides ADVI_BDAPIMIG P1 as its
durable extension (no new project).

## Authorization + context

- **Andrew lifted the 49f login-automation hold** (COO session 2026-06-29) — the durable port (= BD
  login automation on 49f) is GO. Andrew chose **durable-port-only**: NO manual reseed band-aid, so
  this leg is the *sole* path that unfreezes 49f. 49f BD cookie is currently DEAD (bd-49f-keepalive
  401 since ~04:33Z; bd-49f-authtoken-absence ALARM; session secret 2.7d stale). 49f silver is 1td
  (not yet frozen) but Monday ingest needs a live cookie — your LEG2 live OTP test re-mints it.
- cot got this exact durable path Friday (61dc06e5d). You (0.6.2_AE) built it — this is the
  firm-parameterized port of your own work.
- CTO arch-gates the window_seconds firm-disambiguation + RAVCs the live-test evidence.

## Scope (CTO-authored, 1.0.0_SA_CTO 20260629T125806Z)

**LEG 0 — GROUND THE LIVE 49f BOX STATE FIRST** (repo does not carry 49f's on-box secret-ids.env;
0.7.0 baked it). Pull live 49f box config + confirm before changing anything: current BD_OTP_ADAPTER
value, whether a 49f gateway-token secret exists, device-trust capture state in
`blackdiamond/49f/session`, proxy secret present. **Report the delta-to-cot before LEG 1.**

**LEG 1 — PORT cot's durable auto-login to the 49f box** (the canonical .js already supports all of
this via env; this is wrapper+env+secret, NOT .js surgery):
  a. **Device-trust re-inject:** 49f wrapper sources `bd_device_registration` from
     `blackdiamond/49f/session` → exports `BD_DEVICE_REGISTRATION` (cot's run-bd-auto-login.sh fix,
     firm-swapped). FAIL-SAFE: absent token → unset → full-OTP (no regression).
  b. **Gateway-OTP adapter:** 49f secret-ids.env `BD_OTP_ADAPTER=gateway` + `BD_OTP_GATEWAY_URL` +
     `BD_OTP_GATEWAY_SECRET_ID=blackdiamond/49f/otp-gateway-token` (**49f-OWN token, NOT cot's**).
  c. **In-run retry:** `BD_MAX_LOGIN_ATTEMPTS=3` + backoff (49f currently pinned 1).
  d. **Resi-proxy stays ON** (`BD_PROXY_SECRET_ID` — 49f's datacenter IP is BD-blocked; 49f-specific
     delta cot does not have).

**LOAD-BEARING ARCH CONDITION (CTO arch-gates this):** 49f + cot read OTP from the SAME mailbox,
content-identical emails. 49f MUST set `BD_OTP_WINDOW_SECONDS` (~120 like cot) so the gateway returns
ONLY a code within [since, since+window] → a cot login and a 49f login cannot grab each other's code.
Confirm the gateway server honors per-firm window + 49f's token maps to the right mailbox/firm. **A
cross-firm code = a login that "succeeds" with the wrong firm's session = silent firm-sep break — this
is the gate (CLAUDE.md NEVER#1).**

**LEG 2 — LIVE ON-BOX OTP TEST:** one real BD login on the 49f box proving end-to-end self-re-mint
(gateway fetches 49f's code, device-trust checkbox sets bd_DeviceRegistration, `.bd.identity` captured
→ SM). Ground success on the cookie present + silver landing next runner, NOT self-report.

<compiler_tools_mandate>
- `comp-iam service bd-49f-runner` / the box role — confirm GetSecretValue on the 49f gateway-token +
  session secret BEFORE deploy.
- `comp-freshness bd` at accept — bd_silver PASS.
- `comp-pipescript deployed` — box script MATCH.
</compiler_tools_mandate>

<cross_domain_coordination>
49f BD box + 49f secrets + 49f OTP-gateway token only. FIRM-SEP (NEVER#1): the 49f run must NEVER
touch cot's secret / token / OTP code — the window_seconds disambiguation is exactly what guarantees
this; it is the arch-gate. Adjacent (same surface, do not collide): 0.7.0_AE is fixing the
freshness-PROBE semantic bug (200-no-token → emit 0) on the bd-cot/49f-freshness-probe Lambda — that
is a DIFFERENT file (the monitoring Lambda) from your box wrapper/env/secret work; coordinate if both
touch the 49f alarm topic.
</cross_domain_coordination>

<acceptance_criteria>
1. Live 49f BD login self-completes WITHOUT manual OTP.
2. `blackdiamond/49f/session` `captured_at` advances autonomously.
3. bd_silver transactions/realized/unrealized land on the next 02:00 runner (`comp-freshness bd` PASS).
4. Firm-sep PROVEN — the 49f run never touches a cot secret/code (NEVER#1); window_seconds confirmed by CTO arch-gate.
5. ≥24h with no manual reseed + the `opal-bd-49f-cookie-alerts` topic quiet.
6. RAVC to 2.0.0_SA_COO with LEG0 delta-to-cot report + LEG2 live-test evidence (cookie present + next-runner silver landing). CTO arch-gates the window_seconds disambiguation before LEG2 deploy.
</acceptance_criteria>
