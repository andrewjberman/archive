# Black Diamond Login Mechanism — Analysis & Record (self-re-minting vision login + OTP gateway)

**Author:** 0.6.2_AE_PartnerETL · **Domain:** ADVI_BDAPIMIG / Black Diamond auth · **Type:** analysis / record of a LIVE mechanism
**Grounded @ `27a229d17`** (working tree, 2026-07-14). Citations are `file:line` at that vintage. This is an *as-it-stands*
record: it describes the mechanism as it exists in code today, names what is **code-grounded** vs what would need a **live
exercise** to confirm, and records the doc-drift it found rather than papering over it. Companion to
`SCHWAB_AUTO_PULL_DESIGN.md` (same directory) — the two are deliberate opposites on the one axis that matters most.

> **Grounding provenance:** the component map below was assembled by a dedicated read-only search pass over the repo this
> session (44 tool calls), reading actual file contents; every mechanism claim carries a `file:line`. Runtime/live-AWS
> claims (alarms firing, a login actually succeeding) are labelled as such and were **not** independently exercised for
> this doc — they are the mechanism as coded and deployed-by-Terraform, not a live-fire verification.

---

## 0. What it is, and why it's the reference point

Black Diamond (BD) has **no standing human session**. Where the Schwab pull rides a session a person established and
re-establishes when it lapses, BD **re-mints its own session from scratch on a schedule** — a headless browser logs in,
clears MFA by fetching its own one-time code, captures the resulting session cookie, and writes it back to Secrets
Manager for the data runners to consume. Nothing human is in the daily loop.

The interesting part — and the reason Andrew names it as the reference for "OTP fallback via Kimi-enabled graphapi email
access" — is the **two-part autonomy**:

1. **Vision-driven login (the "Kimi-enabled" part).** The login driver is a Playwright/Chromium bot that doesn't rely on
   brittle CSS selectors to know what screen it's on. It screenshots each step and asks **Kimi-VL** (a vision-language
   model) to classify the screen — LOGIN vs MFA vs LOGGED_IN — then acts, in a perceive→act loop. DOM heuristics are a
   fallback, not the primary signal.

2. **Graph-API OTP fetch through a capability gateway (the "graphapi email access" part).** When BD demands an emailed
   6-digit code, the box does **not** touch a mailbox. It POSTs to an internal OTP gateway holding a *capability bearer*;
   the gateway — using **Andrew's own delegated Microsoft 365 token, held server-side** — reads the shared OTP mailbox via
   Microsoft Graph and returns **only** a code whose receipt time falls inside a tight recency window. That window is the
   entire firm-separation guarantee for the shared mailbox.

This pattern — *a box that self-re-mints, fetching its OTP from a locked-down Graph gateway with a recency-bounded read* —
is the portable design any pipeline needs when it must remove the human-in-the-loop. It is **not** wired into the Schwab
box today (see `SCHWAB_AUTO_PULL_DESIGN.md` §3); BD is where it lives and works.

---

## 1. End-to-end flow

```
   EventBridge cron (per firm, staggered)             49f-fees 22:20Z · 49f-main 00:00Z · cot 02:00Z
   bd-49f-session-daily / cot-bd-session-daily              (min gap 1h40m; each mint hard-capped ~25min)
            |  invokes
            v
   session-trigger Lambda  --> StartInstances (transient auto-login EC2 box) --> wait SSM-Online
            |  SSM RunCommand: doc opal-{firm}-bd-session-fetch
            v  on the box:
   run-bd-auto-login.sh
     - source secret-ids.env (secret-id POINTERS, never values)
     - pull prior device-trust token from SM blackdiamond/<firm>/session -> export BD_DEVICE_REGISTRATION
     - node bd_49f_auto_login.js
            |
            v
   bd_49f_auto_login.js  (Playwright + Kimi-VL)
     - smGet creds + Kimi key from Secrets Manager
     - launch headless Chromium (NATIVE AWS IP; stealth args)
     - inject bd_DeviceRegistration cookie (skip MFA if BD trusts the device)
     - perceive->act loop: screenshot -> Kimi-VL classifyState (DOM fallback) -> act
         LOGIN -> type creds
         MFA_OTP -> click "email code", getOtpCode(), type code, check "Remember My Device"
         LOGGED_IN
     - success oracle = the .bd.identity cookie is PRESENT (not a vision verdict)
     - smPut fresh {bd_identity, all_cookies[], device-trust, captured_at} -> SM blackdiamond/<firm>/session
       (persist is BOUND TO rc: a failed write forces rc=1 LOUD)
            |
   getOtpCode() (adapter = gateway) -----------------> POST https://mcp.opalinvest.dev/otp/fetch
            |   Authorization: Bearer <firm capability token>       (Starlette gateway on EC2 behind ALB)
            |   body {sender, subject, since, pattern, window_seconds}
            |                                                v
            |                                   otp.fetch_otp():
            |                                     - get_token(OTP_MAILBOX)  [Andrew's DELEGATED M365 token, server-held]
            |                                     - Graph GET /me/messages ?$filter=receivedDateTime ge {since}
            |                                     - accept ONLY receipt in [since, since+window]   <-- firm disambiguation
            |                                     - pin sender + subject substring, regex the body
            |<---------------------------------- return { "code": "######" }  (Cache-Control: no-store; code never logged)
            v
   on SSM Success: EventBridge stops the box + invokes the bronze runner on the fresh cookie -> silver -> gold
```

---

## 2. Component inventory (path → role)

**Login driver + wrappers**
| Path | Role |
|---|---|
| `infra/aws/ec2/bd-49f-auto-login/bd_49f_auto_login.js` (559 ln) | The canonical, firm-parameterized Playwright + Kimi-VL login driver. Single source of truth; the same filename is deployed to the cot box for parity. |
| `infra/aws/ec2/bd-49f-auto-login/run-bd-auto-login.sh` | 49f SSM wrapper: sources env, re-injects device-trust from SM, runs node, propagates rc. |
| `infra/aws/ec2/bd-cot-auto-login/run-bd-auto-login.sh` | cot wrapper (same shape, `BD_FIRM_ID=cot`, cot session secret). |
| `infra/aws/ec2/bd-49f-auto-login/package.json` | Playwright `^1.47.0`, postinstall `playwright install chromium`. |
| `bd-49f-auto-login/secret-ids.env`, `bd-cot-auto-login/secret-ids.env` | Per-firm secret-id **pointers** + tunables (adapter, window, attempts). No secret values. |

**OTP gateway (the Graph mailbox read)**
| Path | Role |
|---|---|
| `infra/aws/ec2/m365-mcp-gateway/app/otp.py` | `/otp/fetch` logic: delegated-token mailbox read, sender/subject pin, `[since, since+window]` recency guard, returns only the code (`fetch_otp` :81; window at :107,:128-131). |
| `.../m365-mcp-gateway/app/server.py:436-493` | `/otp/fetch` (:438) + `/otp/health` (:481) HTTP handlers; static bearer gate, `no-store`. |
| `.../m365-mcp-gateway/app/token_broker.py` | Per-user **delegated** MSAL token cache, Fernet-encrypted at rest, silent-refresh — holds Andrew's M365 session server-side. Never an app-only tenant token (:1-7). |
| `.../m365-mcp-gateway/app/config.py:161-174` | `OTP_BEARER` (per-firm capability bearers), `OTP_MAILBOX` (Andrew's mailbox, injected at deploy), `OTP_WINDOW_SECONDS`. |
| `infra/aws/terraform/m365-mcp-gateway/{main.tf,alb.tf,secrets-iam.tf,otp-liveness.tf}` | Gateway host + ALB at `mcp.opalinvest.dev`, per-firm bearer secrets, 6h liveness probe. |

**Infra: trigger chains, runners, alarms, secrets**
| Path | Role |
|---|---|
| `infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf` | 49f re-auth chain: EventBridge cron → session-trigger Lambda → StartInstances → SSM mint → on-Success stop box + invoke runner. |
| `infra/aws/terraform/bd-pipeline/bd-49f-interim.tf` | Keepalive (15m) + freshness probe (1h) + all 49f staleness alarms + runners. |
| `infra/aws/terraform/bd-pipeline/secrets.tf` | `blackdiamond/49f/{credentials,session,otp-relay,otp-gateway-token}` SM containers. |
| `infra/aws/terraform/cot-pipeline/{ssm.tf,eventbridge.tf,ec2.tf}` | cot session-fetch SSM doc (gateway path), `cron(0 2)` chain, cot-exporter EC2. |
| `infra/aws/terraform/bd-49f-auto-login/{main.tf,instance.tf,iam.tf}` | The 49f transient auto-login EC2 box + least-priv role. |
| `data/black_diamond/API/AUTHENTICATION.md` | BD OIDC/session model, cookie TTLs, firm-sep — **partly stale, see §9**. |

---

## 3. The login driver — vision perceive→act, with a hard success oracle

`bd_49f_auto_login.js` (`main()` :269, `attemptLogin()` :325):

- **Launch:** headless Chromium with stealth args (:338), **native AWS IP** — the BrightData residential proxy was
  dropped 2026-06-25 (Andrew-direct); the box role has no BrightData grant, so native-IP is structurally enforced
  (`bd-49f-auto-login/secret-ids.env:34-37`, `terraform/bd-49f-auto-login/instance.tf:5-8`). BD runs Cloudflare
  bot-management on the login flow (`__cf_bm`, ~30min), which is why login is on-box only and "has NOT been tested
  off-box" (`AUTHENTICATION.md:57-61`).
- **Perceive→act loop** (:380): each step screenshots, then `classifyState` (:97) asks **Kimi-VL** (key from
  `BD_KIMI_SECRET_ID=astn/kimi/api-key`) which screen this is, with a DOM heuristic fallback `classifyByDom` (:142).
  It drives `LOGIN → MFA_OTP → LOGGED_IN`.
- **Success oracle is a cookie, not the model.** `hasIdentity` (:371) checks for the `.bd.identity` cookie's presence.
  Vision decides *what to do*; the cookie decides *whether it worked*. A vision model saying "looks logged in" never
  substitutes for the actual session artifact existing.
- **Retry/backoff:** `BD_MAX_LOGIN_ATTEMPTS=3`, `BD_LOGIN_BACKOFF_MS=5000` (secret-ids.env).
- **SM-direct:** the JS reads its own secrets (`smGet` :42) and writes its own output (`smPut` :537-543); the wrapper
  never touches a secret *value*, only pointers.

---

## 4. The OTP gateway — the load-bearing part

This is the mechanism Andrew wants recorded as a reference. It has three properties that make it safe to point an
autonomous box at a shared mailbox.

### 4.1 The box holds a capability, not mailbox access
`getOtpCode()` with `BD_OTP_ADAPTER=gateway` (`bd_49f_auto_login.js:222-256`): the box POSTs to
`BD_OTP_GATEWAY_URL=https://mcp.opalinvest.dev/otp/fetch` with `Authorization: Bearer <gwToken>` where
`gwToken = smGet(BD_OTP_GATEWAY_SECRET_ID)` — a per-firm token (`blackdiamond/49f/otp-gateway-token`,
`blackdiamond/cot/otp-gateway-token`). **The box never sees a mailbox, a Graph scope, or Andrew's credentials.** It
holds one narrow capability: "ask the gateway for a code." Request body (:243): `{sender, subject, since,
pattern:'Authorization code:\s*(\d{6})', window_seconds}`. Polls up to 30×10s (:245-254).

### 4.2 The gateway reads Graph as Andrew, delegated — never app-only
Handler `otp_fetch` (`server.py:438-477`) validates the bearer in constant time (`otp.check_bearer`,
`hmac.compare_digest`, no early exit — `otp.py:56-72`), then `otp.fetch_otp(...)`:
- Mints the **delegated** token for the fixed OTP mailbox via `get_token(OTP_MAILBOX)` (`otp.py:109`), raising
  `NeedsLogin` if Andrew's delegated refresh has lapsed. `token_broker.py` holds a per-user, Fernet-encrypted,
  silent-refreshing MSAL cache; the comment is explicit: *"the gateway never holds an app-only tenant-wide token —
  Graph enforces per-user scope"* (`token_broker.py:1-7`).
- Graph query: `GET /me/messages`, `$top=15`, `$orderby=receivedDateTime desc`, `$filter=receivedDateTime ge {since}`
  (`otp.py:113-120`).
- Returns **only** `{"code": "######"}` with `Cache-Control: no-store` (`server.py:477`); the code is **never logged**
  — `audit_fetch` records only `found`/`outcome` (`otp.py:145`).

### 4.3 The recency window IS the firm-separation guarantee
Both firms' OTP emails land in **one shared mailbox** and are content-identical, so sender+subject cannot tell them
apart. Disambiguation is **temporal**: `until_dt = since_dt + timedelta(seconds=eff_window)` (`otp.py:107`), and the
loop skips any message received after `until_dt` (`otp.py:128-131`) — it accepts only a code within `[since,
since+window]`. Both firms send `BD_OTP_WINDOW_SECONDS=120` (`bd-cot-auto-login/secret-ids.env:15`,
`bd-49f-auto-login/secret-ids.env:28`), and the mint schedules are staggered ≥1h40m apart (§7). A login started at
T only accepts a code emailed in `[T, T+120s]`, so a cot login and a 49f login cannot grab each other's code.

> **This is the same class of guard as CLAUDE.md NEVER#1 (firm-sep):** a cross-firm code = a login that "succeeds"
> with the wrong firm's session = a silent firm-separation break. The window is what makes the shared mailbox safe.
> It is a *timing* control, so it depends on the stagger holding — worth an explicit note for anyone changing cadence.

### 4.4 Adapter seam (know the history so you don't reintroduce a removed one)
`BD_OTP_ADAPTER` selects the source (`bd_49f_auto_login.js:193`):
- `gateway` — the live/durable path, both firms (above).
- `relay` (:195-221) — an interim CVO-operated bridge reading a code from a transient SM secret, freshness-gated by
  `loginStart`, consume-once + clear. Retained **inert** as a one-line revert.
- **Removed:** the old app-only Graph `Mail.Read` app-registration adapter was deleted 2026-06-25 (:257-259) —
  *do not reintroduce it.* The delegated-as-Andrew model replaced it precisely so the gateway never holds a
  tenant-wide app token.

---

## 5. Device-trust — skip the OTP when BD already trusts the box

- **Capture** (`bd_49f_auto_login.js:526`): after login, the driver finds the `bd_DeviceRegistration` cookie (or any
  `/device|trust|remember/i` cookie) and persists it into the session secret as `bd_device_registration` (:537-543).
  During MFA it checks "Remember My Device" via three verifying strategies — label-text click / force-check / vision
  (:478-495).
- **Re-inject** (two layers): the wrapper sources the token back from `blackdiamond/<firm>/session` and exports
  `BD_DEVICE_REGISTRATION` (49f `run-bd-auto-login.sh:44-56`, reading the explicit `BD_SESSION_SECRET_ID`, **not**
  cot's default — firm-sep note at :37-39). The JS injects it as a pre-login cookie
  `ctx.addCookies([{name:'bd_DeviceRegistration',...}])` (:349-355) so BD skips the OTP screen entirely.
- **Fail-safe:** absent token → full-OTP procurement, no regression. Device-trust is an optimization on top of a login
  that always works without it.

---

## 6. The session artifact `.bd.identity`

- **What it is:** the Black Diamond IdentityServer (idsrv) OIDC session cookie, scoped to the parent domain
  `.bdreporting.com`, one of ~9 cookies in the jar (`AUTHENTICATION.md:31-42`). One login authenticates all sibling
  apps (DataMining `bd3`, Billing). Per-app opaque bearers are minted from the cookie jar via
  `GET /datamining/auth/token` (`AUTHENTICATION.md:63-97`).
- **Persistence, bound to rc:** the JS writes `{bd_identity, all_cookies[], bd_device_registration,
  bd_device_cookie_name, captured_at}` to SM `blackdiamond/<firm>/session` (:537-543). A failed `smPut` forces
  `rc=1` LOUD (:530-548) — a stale secret can never return a false green. Home is Secrets Manager only (no S3 for the
  cookie).
- **Consumption:** the bd runners / keepalive / freshness Lambdas read `BD_SESSION_SECRET_ID=blackdiamond/49f/session`
  (`bd-49f-interim.tf:140,316`; `bd-49f-session-chain.tf:172`); cot bronze reads `blackdiamond/cot/session`
  (`cot-pipeline/ssm.tf:119`).

---

## 7. Deployment + trigger chains (event-driven, collision-free by construction)

- **Boxes:** 49f auto-login on transient EC2 `i-0fa1846f04ed7e337` (t3.medium, AL2023, SSM-managed, no keypair, IMDSv2,
  ephemeral public IP — `terraform/bd-49f-auto-login/instance.tf:51-57`); cot login runs on the cot-exporter EC2
  `i-0643a5bee8a8feabf` (`cot-pipeline/ec2.tf:44-53`); the OTP gateway on `aws_instance.gw` behind an ALB at
  `mcp.opalinvest.dev` (`m365-mcp-gateway/main.tf:148`).
- **Code deploy (Rule 12):** repo → S3 → SSM pull; Playwright browsers install post-boot, not at launch.
- **Chains (NOT a box cron):**
  - 49f: `bd-49f-session-daily` `cron(0 0 * * ? *)` → `bd-49f-session-trigger` → StartInstances → wait Online → SSM doc
    `opal-bd-49f-session-fetch` (runs the wrapper, timeout 1500s) → mint. On SSM `Success`,
    `bd-49f-session-complete` → stop box + invoke `bd-49f-runner` on the fresh cookie
    (`bd-49f-session-chain.tf:184,205-215`). A second `bd-49f-fees-session-daily` `cron(20 22 ? * MON-FRI *)` (:243).
  - cot: `cot-bd-session-daily` `cron(0 2 * * ? *)` → `cot-bd-session-trigger` → SSM `opal-cot-bd-session-fetch`
    (gateway path) → bronze run (`cot-pipeline/eventbridge.tf:45`, `ssm.tf:63-69`).
- **Collision-free by construction:** scheduled mints are 49f-fees 22:20Z, 49f-main 00:00Z, cot 02:00Z — min gap
  1h40m, each mint hard-capped ~25min (`bd-49f-session-chain.tf:32-39`). Combined with the 120s OTP window (§4.3), two
  firms' logins cannot overlap and cannot cross-grab codes. The old fixed `cron(0 2)` box runners are **disabled**,
  superseded by the chain (`bd-49f-interim.tf:618-627,759-768`).

---

## 8. Firm separation + freshness guarding

**Firm-sep (NEVER#1) — enforced at two layers:**
- **Code:** `bd_49f_auto_login.js:280-283` — every firm-bound secret-id must start with `blackdiamond/<firm>/`, else
  `process.exit(3)` fail-closed. Debug screenshots are firm-prefixed (:394).
- **Infra:** separate boxes, separate IAM roles with zero grants on the other firm's secrets/buckets, and an explicit
  `Deny` on `opal-data-cot` in the 49f runner roles (`bd-49f-interim.tf:549-558,714-722`). Each firm holds its own
  gateway bearer secret.
- **The one shared resource** is the OTP mailbox (`bd-49f-auto-login/secret-ids.env:18`), made safe by the recency
  window, not by mailbox routing (§4.3).

**Freshness / liveness (code-grounded; live-firing not exercised for this doc):**
- `bd-49f-keepalive` Lambda `rate(15 min)` GET `/auth/keepalive`, 401 → SNS; absence alarm `bd-49f-keepalive-absence`
  (no datapoint 2h → breaching) (`bd-49f-interim.tf:130-209`).
- `bd-49f-freshness-probe` `rate(1 hour)` emits `AuthTokenOK` + per-table `TradingDayLag`; absence alarm
  `bd-49f-authtoken-absence` (no datapoint 3h) (:306-398).
- Per-table `bd-49f-silver-stale-<table>` (**trading-day-aware** — NEVER#1), `bd-49f-runner-errors`,
  `bd-49f-bronze-sentinel-stale`, all → SNS `opal-bd-49f-cookie-alerts` (:411-464).
- Gateway-side: `m365-otp-liveness` Lambda `rate(6 hours)` GETs `/otp/health`, alerts on `needs_login` (Andrew's
  delegated refresh lapsed) (`m365-mcp-gateway/otp-liveness.tf:71-116`; handler `server.py:480-493`). **This is the
  single point of freshness that a purely-autonomous OTP box still has:** if Andrew's delegated M365 refresh dies, the
  gateway cannot read the mailbox and every firm's login stalls at MFA. It fails loud, but it is the human-shaped
  dependency that remains.
- **Retired:** `bd-49f-authtoken-dead` (dead-cookie pager) retired 2026-07-02 — the re-auth-at-ETL chain makes
  cookie-death structurally irrelevant (:363-379).

---

## 9. Smell pass — drift found while grounding (recorded, not fixed)

These are map-vs-territory gaps the grounding surfaced. Recorded here per "a stale record says something false with
authority"; none is changed by this doc (they are not in my authoring lane), but they are named so nobody trusts the
stale surface.

1. **`AUTHENTICATION.md:44-49` (dated 2026-07-08) is behind the code.** It still says login is performed by
   `cot_bd_session_fetch.py`. The **deployed** SSM doc `opal-cot-bd-session-fetch` was rewired to run
   `run-bd-auto-login.sh → bd_49f_auto_login.js` (gateway self-fetch), explicitly replacing the MFA-failing
   `cot_bd_session_fetch.py` (`cot-pipeline/ssm.tf:52-63`). The legacy `data/cot/scripts/bronze/cot_bd_session_fetch.py`
   still exists in-repo. → Doc should be corrected by the cot lane owner.
2. **`terraform/bd-49f-auto-login/instance.tf:96-113` user-data bakes `BD_OTP_ADAPTER=graph` + TODO placeholders**,
   whereas the deployed/repo `secret-ids.env` uses `BD_OTP_ADAPTER=gateway`. The comment (:67-70) says the running box's
   env is kept in sync via SSM config-sync with the S3 copy as source-of-truth, so this is *expected* drift — but a
   bootstrap that names a **removed** adapter is a trap for the next reader. → Worth a one-line correction.
3. **No cot copy of the JS to diff against.** `bd-cot-auto-login/` holds only the wrapper + `secret-ids.env`; the
   canonical JS lives only under `bd-49f-auto-login/` and is deployed to cot's `/opt/bd-cot-auto-login/`. No cot-specific
   divergence exists, but there is nothing in-repo to diff the cot on-box JS against. → Parity is by-convention, not
   by-artifact.
4. **The 06-29 ADVI_BDAPIMIG TO's auth premises are stale/wrong for BD.** That TO referenced an "LMS SSO gateway",
   `sws-gateway.schwab.com`, `LMS_ClientId=SDD`, and Windows Credential Manager as part of the BD port. **None of those
   are in the BD stack** — they belong to the *Schwab* SI2 REST discovery (Windows Credential Manager `SDDSecure` is the
   Schwab puller's auth; see `SCHWAB_AUTO_PULL_DESIGN.md` §3). The BD OTP path is the m365 gateway, full stop. → If that
   TO is revived, its auth section needs a rewrite against this record.
5. **`OTP_MAILBOX` literal is intentionally out-of-band** (injected via gateway `.env` at deploy, not in repo). The
   mechanism is fully grounded; the mailbox address is deliberately not committed. Not a defect — noted so a reader
   doesn't hunt for it in the repo.

---

## 10. The two mechanisms side by side (why this record exists)

| Axis | Schwab Auto Pull | Black Diamond |
|---|---|---|
| Session origin | **Human-established**, standing SDD session (refresh token in Windows Cred Mgr) | **Self-re-minted** every run by a headless login |
| Auth in the daily path | None — rides the token | Full login: creds + MFA + device-trust |
| MFA / OTP | N/A (no login) | Kimi-VL vision loop + **Graph OTP via capability gateway**, recency-windowed |
| Freshness single-point | The human session; FATALs loud when it dies | Andrew's **delegated M365 refresh** at the gateway; FATALs loud (`/otp/health`) |
| Firm-sep for the shared resource | Master-scoped keyspace + observe-from-vendor quarantine | 120s OTP recency window + schedule stagger + code fail-closed guard |
| When you'd port the other's design | Port BD's self-re-mint to remove the human from Schwab | (already autonomous) |

The BD mechanism is the **existence proof** that an Opal pipeline can fully remove the human from an MFA-gated vendor
login, safely, with firm-separation intact. That is what makes it the reference point — and what a future Schwab
"remove the human" effort would adopt.

---

## Appendix — grounding notes

Component map assembled by a read-only search pass this session; every mechanism claim carries `file:line @ 27a229d17`.
Not independently exercised for this doc: a live BD login end-to-end, live alarm state, and the delegated-token refresh
health — those are the mechanism as coded + Terraform-deployed, and would each need a live exercise (a real mint / a
CloudWatch read / an `/otp/health` call) to move from `deployed` to `exercised`. The §9 drift items are the map-vs-code
gaps found in passing; they are outside my authoring lane and are recorded for the owning lanes to correct.
