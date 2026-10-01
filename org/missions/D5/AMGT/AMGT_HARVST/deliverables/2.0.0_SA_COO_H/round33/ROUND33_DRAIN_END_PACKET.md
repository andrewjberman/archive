# AMGT_HARVST ROUND 33 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-10-01 ~13:1xZ

**Issuance:** `67ff134cc1`, over `ROUND_ANALYSIS.round32.md` @`749ec2c72e` (decomp section 46, v3.13).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.
**Class:** WORLD (bbg live jobs, sa/ft collection) + SERVED (two gold rebuilds under the CTO + COO pair and its
ADDENDUM 1).

## 1. ORDERS AND ISSUER CELLS, ALL TERMINAL

| cell | what | evidence | status |
|---|---|---|---|
| `af-0` | `verification_locator.py` (vision-API screenshot egress) left the tree | `ca957fb24a` | done (issuer) |
| `af-1` | ft in-tab backfill | unlocked @`3cdb41b7e2`; detached run since 12:34Z | running (issuer) |
| `af-2` | input-source instrument + a CHALLENGED pass | drained `2245350246`, recut `12fee81398` | complete |
| `af-3` | FWD-14 depth table over gold (Z-S51) | drained `48ec92238a`, rerun `8e5a41ed67` | complete |
| `af-4` | bbg/wsj sitemap discovery in the collector | `a134e61d0e` | complete |

- **Close run** (`round33/close_run_round33.py`, trunk `f03efb5e12`, 13:09Z): 7 of 7 rc 0 (each order's criteria +
  the collector suite, 461 passed, 1 skipped); 0 tracked files rewritten.
- **Rows:** every round-33 row still reading ARMED is disarmed by a landed commit (`Z-S53`).

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades)

| FWD | this round |
|---|---|
| **11 (closing condition)** | **A challenged pass with "no human hand" MEASURED:** one bbg collector job on the real path; a PerimeterX 403 (`bloomberg_press_and_hold`) was routed by the transport to `press_and_hold_adaptive`, passed at 12:47:34Z, the retried request returned 200, 8 articles accepted. `InputSourceMonitor` (WH_MOUSE_LL + WH_KEYBOARD_LL, hardware vs injected by the hook flags) ran around the whole job: **hardware input 0**, injected 24 (the harness). This closes round 32's evidence limit (W91-S8) for bbg. **Not yet:** a challenged pass on wsj/barrons (their re-minted sessions met no challenge), ft's Security Verification and sa's checks. |
| **14** | The census reads served gold and maps **89 of 89** (the gold securities file widened 191 -> 212 with the 21 crosswalk keys, CTO-signed). **AT 50+: 6 of 89; AT 100+: 3 of 89** (Boeing 258, Alibaba 148, BP 100, Adobe 91, ASML 78, AstraZeneca 53). Andrew's bar is NOT met and is not re-based. |
| **15 (e)** | bbg and wsj list through the date-ordered monthly sitemaps, never search (af-4 live job: 2 sitemap + 9 article requests, 0 `/search`); the sitemap listing now folds into the run record's reach and listing silver (`ce17235845`). |
| **served gold** | Rebuild #1 (mention 379 -> 4,868) and #2 (universe 212; 4,868 -> 5,836) under the pair; each act record names both parts, digests and rule counts; the rule held before and after each write. |

## 3. BACKFILLS (issuer, detached)

- **sa:** 13 names done since 09:37Z, 1,951 bodies stored across the run, 0 stops since the transport/auto-resume repairs.
- **ft:** relaunched 12:34Z after the unlock fix; its first job read 16 of 39 fetches accepted, 14 still locked
  (entitlement per article -- a round-34 input).

## 4. FOR ROUND 34 (the CTO's list)

1. **bbg and wsj backfill** through the sitemap discovery (each publisher one seat), now that listing and reach parse
   the XML.
2. **Challenged passes on wsj, barrons, ft and sa** under the monitor (FWD-11 names all five).
3. **ft locked bodies** (14 of 39 in the first relaunched job): which articles the subscription does not unlock.
4. **Gold rebuild #3** before the 22:00Z walk (2 of 4 signed rebuilds used).
5. Z-W91-S14: the collector's `worker.lock` lets one runtime run one job at a time; parallel publishers need separate
   runtimes (the backfills use two).

## 5. FOR L9

All criteria are mechanical. Served artifacts moved: gold parts `part-20261001T114722Z` / `part-20261001T114954Z`
(rebuild #1) and the rebuild-#2 parts named in `round32/gold_rebuild_act_20261001T122401Z.json`.
