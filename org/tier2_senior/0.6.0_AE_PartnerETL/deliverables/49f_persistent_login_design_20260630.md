# 49F BD Persistent Login — Design Proposal (no re-OTP per refresh)

**Author:** 0.6.0_AE_PartnerETL (dedicated 49F AE) | **Date:** 2026-06-30
**Status:** PROPOSAL for the ADVI_BREAKS durable phase (Andrew-sovereign direction 2026-06-30; COO carrying as a follow-on TO; gated on CTO arch + CVO re-cert). NOT yet implemented.
**Andrew direction (verbatim intent):** "log in on the box responsible for ingestion, so we don't need to OTP every single time... we already proved this with the Schwab box, 0.0.1_UA built that system."

## Problem (grounded)

Today the 49F BD session refreshes via the **bd-49f-auto-login** box (i-0fa1846f04ed7e337): a Playwright/Chromium browser that, **on every `.bd.identity` death (401)**, re-runs a FULL SS&C login + MFA cycle (OTP auto-read from email via Microsoft Graph / otp-relay). Andrew does not hand-enter the OTP, but it still runs a full MFA every refresh — and that fragility produced the observed **3.5-day session dark gap (06-26..06-28)** before the burst-recovery 06-29 (secret version history: 06-25 21:13Z -> [dark] -> 06-29 14:15/15:20/22:21Z -> 06-30 00:02Z). The auth box is also auth-ONLY (CVO-certified least-priv: no opal-data-bd access), separate from any ingestion box.

## Key finding: the persistent-login mechanism is ~80% ALREADY BUILT

`infra/aws/ec2/bd-49f-auto-login/bd_49f_auto_login.js` already:
- **Injects the device-trust cookie pre-login** if `BD_DEVICE_REGISTRATION` is set (L290-297: "so BD recognizes the device + skips MFA").
- **Checks "Remember My Device"** before Continue (L414-438; multi-strategy + Kimi-vision fallback; logs `device-trust: Remember-My-Device checked=`).
- **Persists the full cookie jar** incl. `bd_DeviceRegistration` to the session secret (L475).

The "trusted device" path is the same pattern Schwab uses (and the BD MFA screen offers "Remember My Device" — L97).

## The gap (why we still re-MFA every time)

The orchestrator's `secret-ids.env` (TF `instance.tf` user_data, L87-104) **never sets `BD_DEVICE_REGISTRATION`**. So:
- On each login the `if (process.env.BD_DEVICE_REGISTRATION)` inject is SKIPPED -> BD sees an unrecognized device -> full MFA.
- The `bd_DeviceRegistration` cookie IS captured into the session bundle each run, but it is **never read back out and re-fed** into the next login. The trust loop is open.

## Proposed fix (two parts)

### Part A — Close the device-trust loop (the no-re-OTP core)
1. **Persist the device-trust token to its OWN durable secret**, separate from the volatile `.bd.identity` session (which dies often). E.g. `blackdiamond/49f/device-registration`. After a successful MFA login where "Remember My Device" was checked, extract `bd_DeviceRegistration` from the jar and `PutSecretValue` there. (Distinct lifetime: the device trust is long-lived; the session cookie is short-lived.)
2. **Re-inject on every login:** orchestrator reads that secret -> sets `BD_DEVICE_REGISTRATION` -> the existing L290-297 inject presents it -> BD recognizes the device -> **skips MFA** -> mints a fresh `.bd.identity` with NO OTP.
3. **Re-OTP only when the device trust itself expires** (BD device-trust TTL — to be observed empirically; typically weeks-months). At that point one MFA re-establishes it, captured back into the device secret.
4. IAM: add `secretsmanager:PutSecretValue` + `GetSecretValue` on `blackdiamond/49f/device-registration-*` to the auth role (small, firm-scoped, 49f-only).

### Part B — Consolidate login + ingestion on one box (Andrew's "log in on the ingestion box")
The 49F REST ingest currently has NO dedicated production runner (today's un-freeze ran provision local + silver-merge on bd-allocations ad-hoc). Rather than maintain a separate auth-only box + a separate ingest box, make ONE box hold the durable (device-trusted) session AND run the ingest:
- Grant that box: opal-data-bd code/template READ + forwardfill/silver WRITE (for ingest) IN ADDITION to the 49f secret RW (for auth) + boto3/pandas/pyarrow/openpyxl.
- This collapses the auth-box/ingest-box split — but it CROSSES the CVO-certified "auth box has no data bucket" least-priv boundary (iam.tf L8-15). **Requires CVO re-cert** of the widened scope (Andrew-sovereign direction authorizes the direction; CVO certifies the bounded implementation). This is also the natural home for the ADVI_BDAPIMIG.P1 "productionize-runner" TO.

## Boundary / governance notes
- **Firm-sep intact:** all grants stay `blackdiamond/49f/*` + `opal-data-bd` (49F's own plane) — zero cot, NEVER#1 clean.
- **ROE preserved:** never log/persist OTP or credential VALUES (the device-trust token is a device-binding cookie, not a credential — same persist-class as the `.bd.identity` session already persisted).
- **Net effect:** session refresh becomes OTP-free for the device-trust lifetime -> eliminates the recurring dark-gap fragility -> durable 49F session (closes the "durable session unproven" item from my launch mandate).

## Implementation steps (on GO + CTO arch + CVO re-cert)
1. Add `blackdiamond/49f/device-registration` secret + the auth-role IAM grant (TF, safe-apply).
2. Patch the orchestrator (`run-bd-auto-login.sh` / secret-ids.env): read the device secret -> export `BD_DEVICE_REGISTRATION`; after a checked-Remember login, write the fresh `bd_DeviceRegistration` back to the device secret.
3. Observe one device-trust cycle: confirm a 2nd refresh skips MFA (log `Remember-My-Device checked=true` + no OTP fetch + fresh `.bd.identity`).
4. (Part B) Provision the consolidated login+ingest box (deps + opal-data-bd IAM) = the ADVI_BDAPIMIG runner; move provision + nightly bronze REST + silver-merge onto it (replaces today's ad-hoc local/bd-allocations path; documents 486228 + the provision as reproducible per CTO's process note).
5. Wire the bronze nightly trigger (EventBridge — note 0.6.2 found the box's built-in scheduler dead; same fix-class).

## Open empirical questions (to ground at implementation)
- BD device-trust TTL (how long before a re-OTP is forced)?
- Does BD bind device-trust to IP/UA (the box's native AWS IP + the fixed Playwright UA should be stable)?
