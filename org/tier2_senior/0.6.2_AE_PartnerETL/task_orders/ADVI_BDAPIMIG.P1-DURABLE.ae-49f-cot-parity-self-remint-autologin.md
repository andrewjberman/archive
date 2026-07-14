# TASK ORDER — ADVI_BDAPIMIG.P1-DURABLE

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>superseded-pending-D1a-verify</status>
<date>2026-06-29</date>
<priority>HIGH — sole 49f unfreeze path (Andrew declined the manual reseed band-aid; durable port IS the fix)</priority>

> **SUPERSEDED-BY-D1a, CONDITIONAL (CTO RULING 173520Z; COO executed same window).** The world moved
> under this TO: Andrew ordered the daily BD REST pattern for BOTH masters into the MONOLITH (~03:4xZ
> 07-14); 0.7.0's D1a REST vehicle is LIVE in probe mode. THE RULING: this TO CLOSES only when D1a
> Apply B lands AND its first scheduled pull VERIFIES on the live listing. Until that event: ZERO new
> investment in legacy-box auto-login (build-on-the-replaced); the legacy bd-49f flow stays at its
> current hand-run cadence serving its current consumers; if D1a slips materially OR the legacy feed
> degrades before Apply B verifies, COO RE-OPENS this TO -- the supersede is conditional, not a bet.
> Lineage: 0.6.2 hygiene surface 173100Z -> COO fork routing 173219Z -> CTO ruling 173520Z.
> **Assignee does nothing here; the close-or-reopen event is COO-watched on the D1a verify.**

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

---

## LEG0 GROUNDING — BANKED 2026-06-30T21:01Z (0.6.2_AE) — Andrew-HELD; resume when sequenced

COO HELD LEG1 (mutation) 2026-06-30T21:03Z: ADVI_BDAPIMIG is Andrew-HELD (Part A + B folded into
BDAPIMIG until Andrew sequences it). Read-only LEG0 grounding done during inf-warm-standby gaps;
LEG1 (start box + deploy wrapper/env) NOT executed. All findings grounded on live AWS + cot repo ref.

**49f box:** bd-49f-auto-login `i-0fa1846f04ed7e337` (transient, was STOPPED at grounding, last
launch 16:34Z 06-30). cot reference = `infra/aws/ec2/bd-cot-auto-login/{secret-ids.env,run-bd-auto-login.sh}`
(canonical firm-agnostic wrapper: APP_DIR self-locating + device-trust re-inject keyed off BD_FIRM_ID).

**Delta-to-cot (LEG1 port targets, when un-held):**
- BD_FIRM_ID cot -> 49f; deploy the SAME canonical wrapper (S3->box, Rule 12); set BD_OTP_ADAPTER=gateway
  (49f current value UNREAD — box was stopped); BD_OTP_GATEWAY_SECRET_ID -> blackdiamond/49f/otp-gateway-token
  (EXISTS); BD_MAX_LOGIN_ATTEMPTS 1->3 (+BD_LOGIN_BACKOFF_MS=5000); BD_OTP_RELAY_SECRET_ID ->
  blackdiamond/49f/otp-relay (EXISTS, revert-parity).
- **BD_OTP_WINDOW_SECONDS ~120 = the CTO ARCH-GATE** (firm-disambig; 49f + cot share the mailbox; a
  cross-firm code = silent firm-sep break, NEVER#1). BDAPIMIG-phase CTO gate, not tonight.

**Live secrets:** blackdiamond/49f/{session,credentials,otp-relay,otp-gateway-token} all EXIST.
session last-changed ~00:15Z 06-30 (FRESHER than the TO's "2.7d stale" written 06-29 — re-ground
session/device-trust state on-box when BDAPIMIG runs).

**IAM (live get-role-policy bd-49f-auto-login-role):** GetSecretValue = blackdiamond/49f/* + astn/kimi/*
(covers gateway-token+session+relay); PutSecretValue = session-* (fresh-cookie writeback). =>
**LEG1a/b IAM precondition SATISFIED — no IAM change needed** (except possibly a proxy grant, below).

**>>> LOAD-BEARING (COO-elevated 21:03Z) — PROXY-GAP HYPOTHESIS, ground FIRST in BDAPIMIG-design: <<<**
NO `blackdiamond/49f/proxy` secret exists AND no proxy ARN in the box role. The TO LEG1d presumes
"resi-proxy stays ON (49f datacenter IP BD-blocked)" — but there is no backing secret/grant.
HYPOTHESIS (Rule-22, UNVERIFIED): if the 49f IP is BD-blocked with no proxy wired, login fails ->
session dies -> feeds freeze == this may be the MECHANISM of the systemic 49f session-death (the
~3.5-day dark gap), i.e. the actual durable-fix target. GROUND BEFORE BUILDING: (1) verify the
BD-IP-block claim; (2) confirm proxy presence/mechanism (a to-be-created secret + IAM grant? a URL
env? or block-claim stale?). Do NOT treat as fact until source/live-grounded.
