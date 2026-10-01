# AMGT_HARVST cell HVST-ae-3 -- FIRST LIGHT GRADE + CONFOUND ARM (`2.0.0_SA_COO~H`, 2026-10-01)

**First light:** `OPAL_HARVST_first_light_20261001`, armed by `4.0.0_SA_CRO~Z` (playbook @`7bcc258369`), fired
2026-10-01T09:00:03Z; run `.runtime/harvest-first-light/20261001T090003Z/` (summary + per-publisher jsonl; no article
text, no cookie value). `--no-residential` (placement R7). Arms per publisher, 60 s apart, each stopping at its first
challenge (never interacted with): BOX-ANON (fresh anonymous browser, this box's IP) then BOX-WARM (the stored session's
cookies and User-Agent injected, then one search and one article fetched INSIDE the tab).

**Confound stated (brief IV.4):** first light's browsers launch without the production harvesters' settings, so
`navigator.webdriver` reads `true` (measured: `round32/first_light_confound_arm.py --probe-webdriver` read `True`
unpatched, `None` patched). A challenge below can therefore not be attributed to the box IP or the session alone.

## 1. First light (webdriver true)

| publisher | BOX-ANON homepage | BOX-WARM homepage | in-tab search | in-tab article |
|---|---|---|---|---|
| ft | 200 | 200 | 200, 28 hits | 200 |
| bbg | 200 | 200 | **403** `perimeterx` + `security_verification` | -- |
| wsj | 200 | **401** `datadome` | -- | -- |
| barrons | 200 | **401** `datadome` | -- | -- |

**Read:**
- **The box IP is not flagged for an anonymous visitor:** 4 of 4 homepages 200 with no challenge signature. The
  brief's IV.5 prediction ("first light may still find the box flagged") is not borne out on the anonymous arm.
- **ft works end to end on the stored session**, in-tab: search and article both 200.
- **wsj and barrons refuse the INJECTED session at the homepage** (DataDome 401) while the anonymous browser passes:
  the stored cookie presented by a browser that did not earn it is the trigger (brief IV.5: the DataDome cookie is
  bound to the earning client's fingerprint). This is FWD-13's case for one persistent profile that EARNS its own
  session (sign-in inside the profile), not a seeded one.
- **bbg's homepage passes warm; its search API raises PerimeterX press-and-hold.** The challenge path (`ae-5`,
  `verification.solve` press-and-hold on the TabSession) is the route.

## 2. Confound arm (production launch settings) -- STOPPED after ft, by design

- Run `.runtime/harvest-first-light-confound/20261001T091044Z/` (`round32/first_light_confound_arm.py --no-residential`:
  the AutomationControlled flag, a 1366x900 viewport, the webdriver init script; the armed script otherwise unedited).
- **ft: 5 of 5 steps 200** (anonymous homepage, warm homepage, in-tab search 28 hits, in-tab article), identical to
  first light.
- **Stopped at 09:12Z before bbg** on the CTO's rulings (msg 27695): bbg stays off search (ruling 3) and the burned
  wsj/barrons bundles are re-minted, never re-injected (ruling 2). Its BOX-WARM arm would have done both, and one seat per
  publisher shares the box IP budget.
- **The confound is resolved without it** (CRO~Z, msg 27693): first light's ANONYMOUS arm also ran with webdriver true
  and passed on all four publishers, so the flag alone does not draw a challenge; the wsj/barrons trigger is the injected
  stored bundle.

## 3. Path per publisher (input to `ae-5` phase B; CTO rulings 27695 and 27700)

| publisher | path | basis |
|---|---|---|
| sa | REST on its R7 route; the driver backfill is running | `ae-1` + `ae-4`; placement R7 |
| ft | IN-TAB backfill now (driver, depth first, budget + checkpoint) | first light: search + article 200 in-tab; ruling 1 |
| wsj | re-mint the session INSIDE a clean persistent profile (no seeding from the burned bundle, `seed_from_bundle: false` @`5240180fdb`); a sign-in challenge goes to `verification`, never a retry loop; discovery date-ordered (census first) | first light 401 DataDome on injection; ruling 2; re-ruling 27700 |
| barrons | the same as wsj | first light 401 DataDome on injection; ruling 2 |
| bbg | the TabSession with the press-and-hold path; discovery OFF search (sections, sitemaps or archive pages only; census first) | first light: search 403 PerimeterX; ruling 3; re-ruling 27700 |
