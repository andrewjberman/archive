# Orion Advisor Login Flow — Selector Spec
**Project:** ADVI_INFLEC W2.6
**Author:** 0.7.0_AE_CloudOps
**Date:** 2026-04-24
**Method:** orion-inspector.py automated scan (2 probe runs)
**Output base:** `.frontend-dev-results/orion-20260424T202639Z/` + `orion-probe-20260424T202915Z/`

---

## Flow Architecture

Orion login is a **two-step single-URL flow** — the page URL stays at
`https://login.orionadvisor.com/` throughout. Step 1 collects username,
Step 2 renders the password form in-place after "Continue".

```
https://login.orionadvisor.com/
  Step 1: username input -> Continue
  Step 2: password input -> Log In
  Step 3: OTP challenge (if triggered) -- selectors TBD (need real creds)
  Step 4: post-login dashboard / export page
```

---

## Stage 1: Username Step

**URL:** `https://login.orionadvisor.com/`
**Page title:** `Login`

| Element | Selector | Notes |
|---------|----------|-------|
| Username input | `#Username` | `type="text"` `class="oat-input-simple"` |
| Continue button | `#btn_userName` | `class="oat-btn oat-btn-primary btn-lrg default-button"` — disabled until input |

**Playwright snippet:**
```typescript
await page.fill('#Username', username);
await page.click('#btn_userName');
await page.waitForLoadState('networkidle');
```

---

## Stage 2: Password Step

**URL:** `https://login.orionadvisor.com/` (same URL, in-place form swap)
**Detection:** `#password` visible after Continue click

| Element | Selector | Notes |
|---------|----------|-------|
| Password input | `#password` | `type="password"` |
| Submit button | `#submit` | text="Log In" |
| Error indicator | `#passwordError` | `class="oat-help-text"` — has `hidden=""` attr on success, attr removed on failure. Check: `await page.locator('#passwordError').isVisible()` |
| Username (hidden) | `#UserName` `[name="UserName"]` | Pre-filled with username from step 1 |
| CSRF token | `[name="__RequestVerificationToken"]` | Rotates each request |

**reCAPTCHA:** `<div id="captcha" class="mb-24">` is present.
- Site key: `6LcAGXAdAAAAALblSqUeyH1zQndg6MAtsTuBPl9s` (v2)
- Container: `#captcha`
- Risk: may activate on repeated failures, new IP, or suspicious UA.
  With valid creds from consistent IP, typically does not challenge.
  If triggered, `orion_export.ts` should detect and surface to OTP relay flow.

**Playwright snippet:**
```typescript
await page.fill('#password', password);
await page.click('#submit');
await page.waitForLoadState('networkidle');

// Detect login failure
if (await page.locator('#passwordError').isVisible()) {
    throw new Error('Orion login failed: invalid password');
}
```

---

## Stage 3: OTP Challenge (TBD)

**Status:** Selectors not yet captured — requires valid credentials to reach this page.

**Known from BRONZERUN PRD:**
- OTP is delivered via email or authenticator (frequency: may be per-session or per-new-IP)
- OTP relay flow: Playwright detects OTP page → writes `state.json` = WAITING_FOR_OTP
  → Lambda → Slack → Andrew replies with `/orion-otp 123456`
  → Lambda writes OTP to `s3://opal-data-inf/otp/current.txt`
  → Playwright polls S3 every 5s, reads OTP, fills form, submits

**Likely selectors (to be confirmed on first real login run):**
```typescript
// Detection — check for any of these:
const OTP_SELECTORS = [
    'input[type="tel"]',
    'input[autocomplete="one-time-code"]',
    '#AuthCode', '#Code', '#otp', '#verificationCode',
    '[name="code"]', '[name="otp"]', '[name="AuthCode"]',
    '[placeholder*="code" i]', '[placeholder*="verif" i]',
];

// Submit button likely:
// '#btn_mfa', '#submit', 'button:has-text("Verify")', 'button:has-text("Submit")'
```

**Action needed:** Populate `orion/credentials` in Secrets Manager and run
`python .tools/orion-inspector.py` with valid creds. The inspector will capture
stage-04/05 JSON with OTP page elements. Update this spec with confirmed selectors.

---

## Stage 4: Post-Login / Export Page (TBD)

Unknown — dependent on completing OTP. To be captured on first live run.

**Expected from BRONZERUN PRD:**
- 3 export targets: Transactions CSV, AUM/Household CSV, Accounts CSV (SlickGrid)
- Export URLs and trigger selectors TBD
- Post-export file paths go to `s3://opal-data-inf/bronze/orion/{YYYY-MM-DD}/`

---

## Known Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| reCAPTCHA v2 triggers | HIGH | Valid creds + consistent IP + realistic timing in Playwright; detect `iframe[src*="recaptcha"]` presence |
| OTP frequency unknown | MEDIUM | S3 polling relay handles any OTP; worst case = every session |
| Password page element IDs change | LOW | IDs (`#password`, `#submit`) are stable OAT design-system elements |
| Session cookie expiry | LOW | Fresh login on each run; no session persistence needed |

---

## orion_export.ts Implementation Notes

1. Launch with `{ headless: false }` — reCAPTCHA is more likely to pass with visible browser
2. Credential fetch: `SecretsManager.getSecretValue('orion/credentials')` at runtime
3. OTP detection: check for any `OTP_SELECTORS` match after login submit; if found, trigger S3 relay
4. Add `page.waitForTimeout(1000)` between form fills to mimic human cadence
5. Screenshot at every stage transition to `s3://opal-data-inf/otp/debug/{date}/stage{N}.png`

---

## Scan Artifacts

```
.frontend-dev-results/
  orion-20260424T202639Z/          -- Stage 1 clean load (no creds)
    stage-01-login-page.{png,html,json}
    selector-spec.md
  orion-probe-20260424T202915Z/    -- Stages 1-5 with dummy creds
    stage-01-login-page.{png,html,json}
    stage-02-username-filled.{png,html,json}
    stage-03-password-filled.{png,html,json}
    stage-04-post-submit.{png,html,json}  <-- PASSWORD PAGE SELECTORS
    stage-05-otp-or-post-auth.{png,html,json}
    selector-spec.md
```
