# CVO DC0.4-ROE-verify — Orion (DC1) live-crawl gate verdict

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-26 · **Gate:** DATA_PLATFORM.DC1 `<arch_gate>` DC0.4 (the pre-live-crawl ROE-compliance + isolation-works gate) · **ROE:** docs/architecture/DATA_PLATFORM_RECON_ROE.md (RATIFIED 2026-06-24)
**Verdict (CVO ROE-compliance half):** **PASS for DC1 Orion — clears the live crawl to proceed.** (CTO's DC0.4 arch-gate runs in parallel; this is the CVO ROE-compliance + isolation-works sign-off.)

## What DC0.4 gates
Per the DC1 TO: verify the BUILT crawl isolation actually WORKS + is ROE-compliant BEFORE any live Orion crawl. This is a code/design + offline-test verification (the *isolation-held-during-the-live-crawl* verify is the SEPARATE post-crawl leg, DC1 acceptance #2).

## Empirical: ran the suite myself (not the producer's report)
`bun test` (crawl-harness): **90 pass / 2 fail / 92 tests, 13 files.** The isolation core + every ROE-enforcement guard is GREEN:
- isolation (ServingGuard / FailSafe / PassiveAuth / RateBudget), no-arbitrary-js-guard, session-ride, bounded-bfs (write-affordance exclusion), orion-humanizer, orion-config — all pass.
- **The 2 failures are BOTH in `eclipse-config.test.ts` (DC2/Eclipse — a DIFFERENT, later vendor leg, NOT DC1/Orion):** (1) ECLIPSE_CURATED_SCREENS[0] is 'portal-internal' (should be data-bearing-first); (2) no 'rebalancer' observe-target screen. These are DC2 config-completeness gaps — they do NOT touch the DC1 isolation/ROE machinery. **Finding (scoped, non-blocking for DC1):** the "55/55+62/62 clean" report was stale; the suite has 2 reds. DC1 proceeds; DC2's OWN gate must not clear until these 2 are fixed (routed to 0.7.0/0.5.0).

## ROE-compliance — encoded BY CONSTRUCTION (code-reviewed, not convention)
| ROE | Mechanism (file) | Verdict |
|---|---|---|
| C1 own-data/account | PassiveAuth rides our OWN parked Orion session token (isolation.ts) | PASS |
| C2 ordinary use / entitlement boundary | session-ride attaches our OWN valid `Session <jwt>` (continue, never fulfill; never method/payload/write); bounded-bfs discovers only endpoints AVAILABLE to our authed session; never forces an un-held scope | PASS |
| C3 their infra only as available; never scan to make available | bounded-bfs same-host-only; reads served XHRs/assets/headers; no scanning/probing | PASS |
| C4 polite / no interference / rate-limited / human-paced / back-off-on-detection | RateBudget (session+per-min ceilings -> HALT; human-paced; SEQUENTIAL); FailSafe (401/403/407/429 or latency -> trip-on-detect -> HALT-before-next-action + backoff); bounded frontier | PASS |
| NOT-ACCEPTABLE tier HARD-EXCLUDED | no-arbitrary-js-guard = STRUCTURAL source-scan test banning the EVALUATE family (arbitrary page JS = fetch/POST/mutate hole) everywhere + the INTERCEPTION family everywhere except the ONE auth-only session-ride; bounded-bfs WRITE_AFFORDANCE_PATTERNS exclusion (logout/create/edit/delete/trade/execute/approve/export…); PassiveAuth never-re-auth (no auth/authz testing) | PASS |

## Isolation-works — the never-burn-serving invariant
- **ServingGuard** (read-only): aborts the CRAWL if the serving instance is running OR within the serving-window+margin; one-directional (reads serving schedule/instance-state, writes ONLY its own crawl-active sentinel, never the serving cron). The crawl is the ONLY thing that halts; serving is oblivious.
- **preflight()** (serving idle + not imminent, ride parked token, sentinel) + **guardAction()** wraps EVERY navigation (failSafe.tripped check FIRST, re-assert serving clear, bearer/expiry, budget, pace).
- **FailSafe** carries a real FIXED halt-window bug (DC1 first-crawl 2026-06-24): the trip is SET-on-detect (not after backoff) + re-thrown at the next guarded action, because page.on('response') swallows throws — so a fast-redirect walk can't slip past the halt. Battle-tested, not theoretical.
- **Offline-testable by design**: injectable probes (now/serving/auth/sentinel) → the serving-abort + fail-safe-halt + budget paths are unit-tested WITHOUT a live vendor. That IS the DC0.4 proof; my run confirms those paths green.

## Verdict + what it clears
**PASS (CVO ROE-compliance + isolation-works half) for DC1 Orion.** The built isolation works (offline-proven: abort/halt/budget paths green) and the crawl is ROE-compliant by construction (the 4 constraints encoded structurally; the forbidden tier hard-excluded by the no-arbitrary-js source-scan + write-affordance exclusion + ride-parked-never-reauth + bounded-same-host). Once CTO's parallel DC0.4 arch-gate clears, 0.7.0 leads the live crawl. I will run the SEPARATE post-crawl "isolation HELD throughout" verify (DC1 acceptance #2) on the live-crawl artifacts.

Residual finding (non-blocking for DC1, blocking for DC2): the 2 eclipse-config test reds → 0.7.0/0.5.0 fix before the DC2 gate.

RAVC → COO + CTO + 0.7.0_AE.

— 3.0.0_SA_CVO
