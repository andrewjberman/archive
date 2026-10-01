# AMGT_HARVST ROUND 29 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~17:0xZ

**Issuance:** `201bc76e9b`, three orders over `ROUND_ANALYSIS.round28.md` @`c907537920` (decomp section 41).
**Re-cuts:**
- `094fcb2a4a` (section 42): PRD v0.9 `C-HV-TRUST-TOKEN` and Andrew-direct ~12:5xZ, carried into the orders. New order files
  were refused (ONE ISSUER PER ROUND).
- `54435d12fd`: sa joins batch 1 (CTO msg 27212).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.
**Class: WORLD** (`ab-2`'s mention rebuild and `ab-3`'s batch-1 collection) **plus LOCAL code.**

## 1. THREE ORDERS, ALL TERMINAL

| order | class | pair | drained | status |
|---|---|---|---|---|
| `ab-1` live wsj reach, `p-2` test, hold seed; A1 pre-floor skip; A2 `C-HV-TRUST-TOKEN`; A3 newest token first | LOCAL | -- | `7fc6ad1cbb` | complete, VALID (`da63b88ccd`) |
| `ab-2` mention rebuild for the 11 bbg story ids | WORLD | `9548acfffb` / `8522f36154` | `a9c5fc9ea8` | complete, VALID (`df1fa5d0aa`) |
| `ab-3` A0: a 402 keeps its body and gets one fresh-session retry | LOCAL | -- | `ffe564672b` | part of `ab-3` |
| `ab-3` phase A: batch 1 collection | WORLD | `6b3b243c4e` / `2fa1940cad` | `2c9c337f92` (record) | **withdrawn** after its act (`d5b427852f`); phase B not run |

- **Close run** (`round29/close_run_round29.py`, at trunk `d5b427852f`): **5 of 5 re-runs rc 0**; 0 tracked files were rewritten.
  `ab-3` is withdrawn and excluded.
- **The collector suite on the trunk:** 317 passed, 1 skipped (253 at `6caac02338`, 0 regressed).

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades)

| FWD | this round |
|---|---|
| **2** | **The 11 bbg story-id articles are on the mention plane** (`ab-2`). `part-20260930T134616Z` holds 379 rows (358 kept, 21 new, all bbg on the 11 story ids), 44,376 bytes, equal to the serializing dry run. There are 0 pairs on the 11 empty rows. The day route lists the 2 in-window 992_HK pairs (2026-08-13, 2026-09-01). **9 of the 11 are 2015-2019** (row `Z-S46`) and reach no page day. The `/timeline` series waits on a paired daily rebuild. |
| **7 / 3 / 1** | **Collection now follows Andrew's rules in code** (`ab-1`, `ab-3` A0): Secrets credentials; the NEWEST stored token first; a 429 is backed off in-job (5 attempts / 120 s) and keeps the token; expiry only after backoff; every attempt is in the run record; a dated pre-floor hit is not fetched (3 recorded bbg pages: 17 fetches become 4); a 402 keeps its body and gets one fresh sign-in. The live wsj path dates hits from `timestamp`, so a wsj backfill bound-stops at the floor. |
| **9 / 7 / 1** | **Batch 1 reached 0 names** (`ab-3` phase A, below). The re-based ceiling stays DEFAULT: 13,500 pages for the other 180 names over {bbg, wsj, sa}. FWD-7's declared set stays `[]`. |

**`ab-3` phase A, the act** (12 run records, 14 jobs, pending 0, so no upload):

| publisher | first request | refusal body (runtime `rejected_bodies/`) | class |
|---|---|---|---|
| bbg (2317_TT) | 403 | -- | the press-and-hold repair failed |
| wsj (2317_TT) | 401 | 652 B: a DataDome captcha page (`geo.captcha-delivery.com`, "Please enable JS and disable any ad blocker") | **bot check** |
| barrons (992_HK) | 401 after one repair | -- | bot check (Dow Jones, the same stack as wsj) |
| ft (992_HK) | 403 | 65,536 of 270,934 B: "Security Verification" interstitial | **bot check** |
| sa (10 names) | none | -- | `contract_unavailable`: "Security lacks a resolved Seeking Alpha symbol" |

- **The finding:** on the stored tokens, every requesting publisher met a BOT CHECK. None of these refusals was token expiry.
- **The CTO half's condition (ii)** ("an interactive challenge is Andrew's login, never bypassed or retried") stopped the bbg
  and wsj legs after name 1. The worker read the challenges that way; the issuer confirms it.
- **So the backfill cannot proceed** on the collector's REST transport as it stands. The route past bot checks is the CTO's
  call. The candidates, none of them chosen here:
  - an Andrew-run headed session;
  - a different transport;
  - pacing.
- **sa was never requested.** The issuer copied the security files from the GOLD universe, which carries no SA symbol,
  instead of the collector's resolved securities. The account check is still unmeasured.

## 3. ROWS THIS ROUND

- **Issuer rows:**
  - `Z-S46`, pre-floor fetches: disarmed by `ab-1` A1. Its count is corrected by `Z-W81-S6` to 13 of 17 article hits.
  - `Z-S47`, the sa probe was vacuous: an issuer cut-time miss.
- **Worker rows, all OBSERVATION and INERT unless noted:**
  - `Z-W81-S1`..`S4`: `S1` and `S2` are ruled inside `Z-W76-S1`.
  - `Z-W81-S5`, `S6`.
  - `Z-W81-S7` (ARMED): disarmed by `ab-1` A3.
  - `Z-W81-S8`..`S10`: accepted as recorded.
  - `Z-W83-S1`, `S2`: the sa symbol, and 0 names reached.
- **Carried rows:** `Z-W76-S1` and `S2` are disarmed by `ab-1`. `Z-W37-S4`'s standing (the sa 402) stays OPEN, because the
  probe never requested.
- **Issuer defects, named:**
  - The probe name and the security files were chosen without checking sa symbol resolution.
  - `ab-1`'s proof instance was pinned PENDING-THIS-COMMIT across three amendment commits; it was repinned by the worker
    @`e5d7e34367`.
  - Three new order files were cut into a round that already had its issuance; the gate refused them, and they were re-cut as
    amendments.
- **Incident fact:** `wk-hvst-r24..r28` were removed (26 of 26) on Andrew's word, card 2. The branches are kept.

## 4. FOR ROUND 30 (the CTO's list; not cut here)

1. **The collection route past bot checks** (bbg press-and-hold, Dow Jones DataDome, the ft security verification). This is
   Andrew's login under condition (ii). It gates batch 1, and therefore FWD-7, FWD-9 and the schedule re-arm.
2. **sa batch 1 on resolved securities** (the collector's own universe objects) with a REAL account check, which settles
   `Z-W37-S4`. sa made no request this round, so it may be the one publisher that can proceed now.
3. **The paired daily rebuild** that serves the new mention snapshot (the `/timeline` series) and `publishers_found_codes`
   on the route (after RESAPP round 53).

## 5. FOR L9

- All criteria are mechanical.
- The served artifact is `article_security_mention` `part-20260930T134616Z`.
- `ab-3`'s evidence: `~83/ab3_runs.json` and the 12 run records.
- **Disposable worktrees:** `wk-hvst-r29-81`, `-82`, `-83`. Their removal needs Andrew's word; card 2 covered r24-r28 only.
