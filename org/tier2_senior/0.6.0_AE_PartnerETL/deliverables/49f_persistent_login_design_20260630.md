# 49F / BD Persistent Login — Design (RE-AIMED v2: dedicated cookie-getter -> SM -> runner-reads -> OTP-fallback)

**Author:** 0.6.0_AE_PartnerETL (dedicated 49F AE) | **Date:** 2026-06-30
**Status:** PROPOSAL v2 for the ADVI_BREAKS / ADVI_BDAPIMIG durable phase. RE-AIMED per Andrew-direct via CTO (180855Z) — DROP consolidation; adopt the dedicated-auth-box -> SM-transfer -> runner-reads -> OTP-fallback doctrine (the inf pattern). NOT implemented.
**Gates:** apply HELD until 49F GREEN (tomorrow-AM penny-test) + Andrew-sequences; CVO re-certs the dedicated-box + SM-transfer threat model. v1 (consolidation) superseded by this.

## Problem (grounded)

49F BD session refreshes via the **bd-49f-auto-login** box (i-0fa1846f04ed7e337): a Playwright/Chromium browser that, **on every `.bd.identity` death (401)**, re-runs a FULL SS&C login + MFA cycle (OTP auto-read via Graph/otp-relay). Andrew never hand-enters the OTP, but a full MFA fires every refresh — fragility that produced the **3.5-day session dark gap (06-26..06-28)** (secret version history: 06-25 21:13Z -> [dark] -> 06-29 burst -> 06-30 00:02Z). Steady-state should be OTP-FREE; OTP should be a bounded fallback, not the refresh mechanism.

## The target architecture (Andrew-direct, the inf doctrine)

```
  [dedicated cookie-getter BOX]            (single-purpose auth tool; the ONLY box that logs in / runs a browser)
        | logs into BD (device-trusted -> NO MFA to the device-trust TTL; OTP only on TTL lapse)
        v
  [Secrets Manager TRANSFER LINE]          blackdiamond/49f/session (cookie) + blackdiamond/49f/device-registration (device-trust)
        | read-only
        v
  [BD INGESTION RUNNER]                     reads the cookie from SM; NEVER logs in; NO browser; NO login creds
        | mints DataMining bearer from the cookie -> pulls -> lands bronze -> silver-merge
        v
  opal-data-bd  (bronze/silver/served)
```

This is **exactly the inf pattern** (grounded): inf-exporter logs in -> writes JWT to SM `orion/jwt/current` -> the inf gold runner READS it (same for `orion/eclipse_jwt/current`, `smartx/jwt/current`). One persistent-login DOCTRINE across inf / 49F / cot: **dedicated-auth-box -> SM-transfer -> runner-reads -> OTP-fallback.**

## Why this is strictly better than consolidation (v1, dropped)

- **Better least-priv:** the ingestion runner holds NO login creds + runs NO browser — it only READS one scoped SM secret. Smaller attack surface than a login+pull box.
- **Auth isolated, single-surface:** one dedicated box owns login; SM is the rotatable / auditable / TTL'd transfer. RESOLVES the inf-vs-49F isolation tension (this is NOT consolidation; it PRESERVES the existing auth-box separation that today's snag-finding surfaced — the auth box correctly CANNOT run ingestion).
- **CVO threat model is CLEANER:** the ingestion box drops from auth-surface to SM-reader; the dedicated cookie-getter stays the only login surface (its CVO-certified least-priv posture is preserved + extended only by the device-trust secret).

## Part A (CORE, KEEP) — close the device-trust loop on the cookie-getter

The persistent-login engine is ~80% ALREADY BUILT in `bd_49f_auto_login.js`:
- injects the device-trust cookie pre-login if `BD_DEVICE_REGISTRATION` set (L290-297),
- checks "Remember My Device" before Continue (L414-438; multi-strategy + Kimi-vision fallback),
- persists the full cookie jar incl. `bd_DeviceRegistration` to the session secret (L475).

**Gap:** the orchestrator (`secret-ids.env`, instance.tf L87-104) never sets `BD_DEVICE_REGISTRATION` -> the inject is skipped -> the captured `bd_DeviceRegistration` is never re-fed -> full re-MFA every refresh (the dark-gap root).

**Fix (what the cookie-getter does before writing the cookie to SM):**
1. After a successful device-trusted login, extract `bd_DeviceRegistration` -> `PutSecretValue` to a DEDICATED durable secret `blackdiamond/49f/device-registration` (distinct lifetime from the volatile `.bd.identity` session).
2. On each login the orchestrator reads it -> sets `BD_DEVICE_REGISTRATION` -> the existing L290-297 inject presents it -> BD recognizes the device -> SKIPS MFA -> mints a fresh `.bd.identity` with NO OTP -> writes it to the SM transfer line.
3. **OTP = bounded fallback ONLY** when the device-trust TTL lapses (one MFA re-establishes it, re-captured to the device secret). The existing Graph/otp-relay adapter is retained for exactly this fallback, no longer steady-state.
4. IAM: add `secretsmanager:Get/PutSecretValue` on `blackdiamond/49f/device-registration-*` to the auth-box role (small, 49f-scoped).

## Part B (RE-AIMED) — the BD ingestion runner reads the cookie from SM (the ADVI_BDAPIMIG.P1 runner)

Today the 49F REST ingest has NO production runner (today's un-freeze ran provision local + silver-merge on bd-allocations ad-hoc). Build the dedicated ingestion runner that:
- READS the session cookie from `blackdiamond/49f/session` (the cot_bronze_ingest `load_bd_session` already does exactly this) — NEVER logs in, NO browser, NO login creds.
- Holds opal-data-bd code/template READ + forwardfill/silver WRITE + SM READ of the session line only.
- Runs the nightly bronze REST pull + silver-merge (replaces today's ad-hoc local path; documents 486228 + the provision as reproducible per CTO's process note).
- This is the ADVI_BDAPIMIG.P1 "productionize-runner" TO; same runner pattern serves Cottonwood (BD source-shared, firm-scoped buckets/secrets).

## Implementation steps (on GO: 49F GREEN + Andrew-sequences + CVO re-cert)
1. Create `blackdiamond/49f/device-registration` secret + the auth-box IAM Get/Put grant (TF, safe-apply).
2. Patch the cookie-getter orchestrator: read the device secret -> export `BD_DEVICE_REGISTRATION`; after a checked-Remember login, write the fresh `bd_DeviceRegistration` back.
3. Observe one device-trust cycle: a 2nd refresh skips MFA (log `Remember-My-Device checked=true`, no OTP fetch, fresh `.bd.identity`).
4. Stand up the dedicated BD ingestion runner (SM-reader; opal-data-bd RW; no login) = ADVI_BDAPIMIG.P1; move provision + nightly bronze REST + silver-merge onto it.
5. Wire the bronze nightly trigger via EventBridge (0.6.2 found the box built-in scheduler dead — same fix-class; ties the SI2/streak productionization).
6. Replicate the doctrine to Cottonwood (cot cookie-getter + cot ingestion runner already SM-mediated; add the device-trust loop).

## Open empirical questions (ground at implementation)
- BD device-trust TTL (how long before a forced re-OTP)?
- BD device-trust binding to IP/UA (box native AWS IP + fixed Playwright UA should be stable)?

## CVO re-cert scope (cleaner than v1)
- Dedicated cookie-getter: login surface unchanged + one new device-trust secret (Get/Put).
- Ingestion runner: NEW box, but auth-surface = SM-READER only (no creds/browser) — a REDUCTION in auth surface vs any consolidation. Firm-sep intact (blackdiamond/49f/* + opal-data-bd; zero cot, NEVER#1 clean). ROE: never log OTP/cred VALUES; device-trust token persisted same-class as the existing `.bd.identity`.

## Arch refinements (CTO 181328Z — endorsed v2 in direction; folded)
1. **Proactive re-mint, never fall to OTP in steady-state:** the cookie-getter must RE-MINT the device-trust + cookie BEFORE the TTL lapses — a pre-expiry alarm modeled on inf's cookie-age monitor (re-mint at ~T-7d). OTP-fallback is the bounded exception (TTL genuinely lapsed / device-trust revoked), NEVER a recurring steady-state event.
2. **SM least-priv ROLE SPLIT (firm-sep):** two distinct roles, never one. INGESTION runner role = `secretsmanager:GetSecretValue` READ-ONLY on `blackdiamond/49f/{session,device-registration}` ONLY (no write, no other firm). COOKIE-GETTER role = `secretsmanager:PutSecretValue` WRITE on those (no broad read). All scoped to `blackdiamond/49f/*`; cot uses its OWN line (`blackdiamond/cot/{session,device-registration}`) — the two firms NEVER share a secret (NEVER#1-clean).
3. **COT parity:** cot adopts the IDENTICAL doctrine on its own firm-scoped line (cot already SM-mediates the session via blackdiamond/cot/session + cot_bronze_ingest.load_bd_session; add the device-trust loop + the role split there too). The design covers both BD firms identically.

(Full CTO arch read is async/post-firefight; these 3 notes are folded for that read. Apply remains HELD per Andrew sequencing — fold the whole into ADVI_BDAPIMIG.)
