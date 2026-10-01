# AMGT_HARVST ROUND 32 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-10-01 ~11:1xZ (the Friday round)

**Issuance:** `a1eb58cd75`, over `ROUND_ANALYSIS.round31.md` @`309b2da963` + PRD v0.13 (decomp section 45, v3.12).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.
**Class:** WORLD (sa and ft collection, Secrets-free in-profile sign-ins, bbg/wsj/barrons challenge run) + SERVED
(one gold mention rebuild, a measured DELTA=0, CTO-accepted without a pair, msgs 27574/27580).

## 1. FOUR ORDERS + ONE ISSUER CELL, ALL TERMINAL

| order | FWD | drained | status |
|---|---|---|---|
| `ae-1` sa wrong-object repair | 12 | A `05198fa747`, B `176defa91c` | complete |
| `ae-2` one browser identity | 13 | `594d7be519` | complete |
| `ae-4` site Z backfill driver | 15 | A `4732ca8c57`, B `c591280ff9` | complete |
| `ae-5` challenge path + renewal | 11 (+15 e) | A `021cf42819`, B `7b959b3910` | complete |
| cell `ae-3` first light | -- | grade `e0deed6998` | graded (issuer) |

- **Close run** (`round32/close_run_round32.py`, trunk `220a74350a`, 11:08:55Z): 12 of 12 rc 0 (every criterion of
  the four orders + the collector suite, 442 passed, 1 skipped); 0 tracked files rewritten. Commit `eae320125c`.
- **Rows:** every round-32 row still reading ARMED is disarmed by a landed commit or ruled (`Z-S52`).

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades)

| FWD | this round |
|---|---|
| **12 (DONE WHEN a-d exercised)** | The sa leg takes the body from the listing (no `/articles/{news_id}`), page cap 200. 38 of 85 stored sa rows (33 keys) were the wrong object (listing-discovered, raw article capture, title unequal to the listing); quarantined by one object `seeking-alpha/harvest/silver/quarantine/date=2026-10-01/20261001T064759Z.json`; re-check 0 of 85 outside the quarantine (AC2); 0 of 33 keys in gold (AC3). The mention rebuild was a verified DELTA=0 (379 rows, digest equal to the signing dry run; daily WITH = WITHOUT the keys). |
| **13** | `TabSession`: one persistent per-publisher Chrome profile, requests in-tab, no User-Agent override, no REST cookie write-back; wired into `publishers.py` for every `"transport": "tab"` publisher (bbg, wsj, ft, barrons; sa stays REST, R7). Real-Chrome seam probe: the server saw the tab's own UA, `navigator.webdriver` false, the profile cookie persisted. |
| **15** | The driver: budget printed first, sa first, checkpoint/resume, `--stop-file`, `--clear-stop`, bounded `--auto-resume-transient` for transport-class stops only. **Depth (silver since 2026-01-01, universe keys): 11 of 89 names with any, 6 at 50+, 1 at 100+ (Andrew's bar is NOT met and is not re-based); sa distinct 20 -> 528.** The sa run continues detached (9 of 89 names done at 11:15Z, 0 stops since 09:37Z). Date-ordered discovery: wsj and bbg monthly SITEMAPS reach 2026-01 (census, never search). |
| **11 (closing condition)** | One unattended run, validation security BA: **bbg press-and-hold met and PASSED** (`press_and_hold_adaptive`, HTTP 200 after), wsj and barrons met no challenge; 3 articles each; each in its own main-tree profile. wsj and barrons sessions re-minted INSIDE clean profiles (the stored bundles were burned: first light 401 DataDome on injection); a deliberately staled barrons session renewed itself in-profile (hash changed, status 200). **Not yet:** ft's Security Verification and sa's checks were not met in this run; FWD-11 names all five. See section 4 for the evidence limit on "no human hand". |

## 3. FIRST LIGHT (cell ae-3) -- `round32/FIRST_LIGHT_GRADE.md`

The box IP is clean (anonymous homepages 200 on all four); ft passes in-tab; bbg's search raises PerimeterX; wsj and
barrons refuse the injected stored bundle. The confound arm (production launch settings) was stopped after ft on the
CTO's rulings 27695; the anonymous arm already resolves the confound (webdriver true, all passed).

## 4. ROWS, ISSUER REPAIRS AND ONE EVIDENCE LIMIT

- **Issuer repairs, each with a negative control:** `254ea37cf6` (sa silver empty struct), `3669bd0f0a` (no-response
  retry, <= 2), `5240180fdb` (`TabResponse.raise_for_status`; no seeding of burned bundles), `6039cefc48` (sa account
  once per job; transport-class auto-resume), `791616d9b6` + `3cdb41b7e2` (seed adds only the bundle cookies a profile
  lacks), `220a74350a` (no path in `verification` posts a screenshot to an external vision API; row W91-S4).
- **EVIDENCE LIMIT (row W91-S8, ruled):** the box's last-input clock ticks every 2-3 min with no human present (the agent
  harness is a candidate source), so `operator_input_detected` cannot tell a human hand from harness input. AC2 holds for
  the short leg windows it records; FWD-11's "no human hand" is carried INFERRED until an input-source instrument exists.
- **ft in-tab backfill:** the first live ft run (09:54-10:45Z) fetched 145 articles, 133 locked: the subscriber bundle
  was never seeded (fixed `3cdb41b7e2`). ft then answered 429; ft traffic is paused, a one-article unlock re-probe runs
  12:02Z, and the ft run relaunches only on an unlocked 200.

## 5. FOR ROUND 33 (the CTO's list)

1. ft: in-tab backfill after the unlock re-probe; ft's Security Verification on the challenge path (FWD-11).
2. bbg and wsj backfill through `discovery` (monthly sitemaps) -- the `publishers.py` hookup to `discovery.discover` is
   the issuer's next act (the collector's `bloomberg()` still lists by search).
3. An input-source instrument for FWD-11's "no human hand" (row W91-S8).
4. FWD-14's census population and key (row Z-S51: universe keys and gold keys share 0).
5. **The served gold rebuild** for the page (mention + daily over the new depth): a SERVED move with CTO+COO halves from
   a serializing dry run, targeted before the 18:00 ET walk.

## 6. FOR L9

All criteria are mechanical. Served artifact moved: `article_security_mention` part-20261001T064839Z (DELTA=0).
Disposable worktrees `wk-hvst-r32-90..92` (the `~91` census profile, 80 MB, sits untracked inside one); removal needs
Andrew's word.
