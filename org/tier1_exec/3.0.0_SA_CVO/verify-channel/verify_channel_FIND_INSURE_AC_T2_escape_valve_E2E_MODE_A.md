# /verify-channel Mode A — AC-T2 scraping_browser escape-valve E2E (AE~B v0.6.2)

**Trigger:** AE~B `20260528T~0443Z` VERIFY-CHANNEL SURFACE — AC-T2 escape-valve E2E GREEN (tag imo-pipeline-v0.6.2)
**Verifier:** 3.0.0_SA_CVO — independent read of the S3 artifact AE produced (verifier-≠-fixer; I did NOT re-invoke the Lambda)
**Self-validation flag:** AE~B's own Ship B artifact + own smoke; this is the independent CVO read AE invited.
**Verdict:** **PASS-mechanical + CONCERN-meaning (honest-limit DEFERRED)** — two axes, not collapsed.

## §1 — Mechanical axis: PASS (4-check)

Read `s3://opal-data-imo/corp/cambridge-investment-research/bronze/web-scrape/2026-05-28/`:
- **EXISTS:** `22e5b2ff093e080d.html` (87,886 B) + `.meta.json` (649 B) ✓
- **FRESH:** `fetched_at 2026-05-28T04:40:27Z`, S3 write 04:40:29Z — fresh, matches AE E2E report ✓
- **SCALED:** 87,886 B rendered DOM — non-trivial; the escape-valve rendered substantial content where direct-fetch hit `fallback-empty-body` (the exact acquisition-failure it remediates) ✓
- **NOT-FROZEN:** `content_hash a7247929167c170a` (distinct real render) ✓
- **Honest meta:** `fetch_method=scraping_browser1`, `fallback_trigger=fallback-empty-body`, `js_render_wait_ms=18032` (networkidle), `final_url=cir2login.b2clogin.com/...SAML/sso/login` recorded — the escape-valve connected, JS-rendered, followed the redirect, serialized DOM, wrote with honest provenance.

**The AC-T2 acquisition-failure-class remediation MECHANICALLY DELIVERS.** The 3-defect gate-mask cascade (credential→driver→glibc) is genuinely cleared; this is past "is it LIVE" to "it produced a real rendered artifact."

## §2 — Meaning axis (Step 3.5): CONCERN-meaning / UNTESTED, honest-limit DEFERRED

Content probe on the 87KB DOM: login/auth-dominated (b2clogin×30, password×36, SAML×4, sso×13, "Sign in"×4). The `ria`×23 matches are substring noise in login-portal context, NOT genuine RIA self-reference. **Zero scoreable AM signal** — the render is the B2C login wall (`final_url` confirms).

- **For Cambridge IR (auth-gated SPA) this is CORRECT behavior** — the public surface IS the login wall; the real content is behind auth and unreachable. The escape-valve faithfully captured what's publicly available.
- **But this fixture proves the RENDER MECHANISM, not the SIGNAL-EXTRACTION path.** "Does the escape-valve deliver SCOREABLE AM content for a public JS-SPA?" is UNTESTED — an auth-gated fixture has no public scoreable content by nature. Per Step 3.5 honest-limit: I CANNOT assert decision-useful content delivery from this fixture alone. The non-auth-gated SPA fixture probe (AE's own suggestion) is the next empirical step — I do NOT run it (would make me producer-not-verifier); routed as the next probe.

## §3 — Step 3.5 finding (meaningful, worth banking): auth-gated SPAs are a structural unrecoverable-signal tail

A subtle but real distinction the Cambridge IR anchor surfaces: the AC-T2 escape-valve fixes the **public-JS-SPA-render-failure** class (content exists publicly but needs JS-render to acquire). It does NOT — and cannot — fix the **auth-gated-SPA** class (no public content exists; signal is behind a login wall). Cambridge IR is the latter: the escape-valve "succeeds" mechanically (renders the login wall) but recovers no AM signal.

Implication for downstream scoring + the AC-T2 acquisition_failure_class taxonomy:
- Auth-gated SPAs should map to `wm_classification = null` (reason: `auth-gated-no-public-content`) or absent — NOT consume escape-valve "success" framing as if signal were recovered. A login-wall render with no AM signal correctly scores absent/null; it must NOT false-present (the `ria`×23 substring noise must not be mistaken for signal — confirm the score_web tokenizer doesn't match substrings).
- This is a known unrecoverable tail, distinct from the SPA-render-failure class AC-T2 was scoped for. Worth a one-line note in the AC-T2 spec: escape-valve effective for public-JS-SPA; auth-gated-SPA is a separate null-class tail (per-IMO Andrew sign-off path per §9 Q5, like BLOCKED-ROBOTS).

## §4 — Routing

- **AE 0.7~B (CC, verify lane):** PASS-mechanical confirmed independently; meaning-axis UNTESTED pending non-auth-gated SPA fixture (your suggested probe — the right next step). §3 auth-gated-tail observation for the AC-T2 taxonomy.
- **ws COO (primary per LD-0116):** AC-T2 escape-valve mechanically verified; recommend the non-auth-gated SPA fixture probe as the decision-useful confirmation before AC-T2 counts as fully closed; §3 auth-gated-tail = known-tail (not a defect).
- **Not a Stage-2 gate** — AC-T2 escape-valve is the acquisition-failure remediation, separate from the W1-classification gate (v0.7.3 re-verify). This verdict is informational to the AC-T2 closure, not blocking Stage 2.

— 3.0.0_SA_CVO 2026-05-28T05:18Z
