# AMGT_HARVST round 37 -- drain-end packet (L8 input) -- `2.0.0_SA_COO~H`, 2026-10-02 ~18:5xZ

The round-36 analysis @e38e50aa55 led to issuance @f45007adc7 (decomposition section 50). Four amendments followed:
- 1: aj-5 @4720f6975a, CTO 28278 plus ruling 8.
- 2: aj-6 @ce1886a63d, CTO 28484.
- 3: aj-7 @cedca01272, CTO 28509.
- 4: aj-8 @bff0ce863a, CTO 28525.

Re-points on Andrew-direct:
- aj-4 went to NopeCHA @dc610be2d3 (~13:08Z). Its step 2 then went back to Andrew's hand (~16:47Z, option B).
- aj-6 went to Ocilar @acec34f084 (~13:3xZ), then back to the NopeCHA extension @bd232ecca9 (~16:47Z, option A).

**8 of 8 orders are terminal.** The mid-round packet @2789aedd64 covered aj-1, aj-2 and aj-3.

## 1. Cells

| cell | result | merged | check |
|---|---|---|---|
| `HVST-aj-1` `~90` | Grader bands anchor on the presentation; requests counted only inside the monitor windows | @fdd7442696 | `aj-1.AC2.output.txt` PASS |
| `HVST-aj-2` issuer act | Monitor window3 from 06:52:23Z; pid 22892 still ALIVE at 18:4xZ | -- | `aj-2.AC2.output.txt` PASS |
| `HVST-aj-3` issuer act | Ordinary barrons backfill inside window3; 89 of 89 pairs, finished 11:36Z | -- | `aj-3.AC2.output.txt` PASS |
| `HVST-aj-4` `~92` | **CANCELLED.** Andrew's hand-solved ft sign-in (FTSession_s 17:01Z) got a 401 at 17:25:05Z, 24m04s later, despite 6 `keepalive_page_load` events ~3.3 min apart, all logged_in | @1e6610290e; flip @6e4e127a1e | AC1 PASS; AC2 FAIL |
| `HVST-aj-5` `~92` | bbg solve outcomes recorded, plus a failure-capture bundle and one bounded retry; limb 2a graded per run | @7b3800219d; close @42a0cc9f14 | `aj-5.AC2.output.txt` PASS |
| `HVST-aj-6` `~90` | **CANCELLED.** The Ocilar route is built (@67cc4ecbcc) but answers 503 (hcaptcha "coming"). The NopeCHA extension 0.6.1 loaded on the ft profile; the hCaptcha was presented at 18:07:12Z and NOT cleared in 150 s; no FTSession_s | @4b333e54ac; flip @2a3d75c5f9 | AC1 PASS 15/15; AC2 FAIL (4) |
| `HVST-aj-7` `~90` | `title` (verbatim) and `published_precision` join the gold mention schema | @385f4a76cc | `aj-7.AC2.issuer_grade.txt` PASS |
| `HVST-aj-8` `~90` | barrons silver dict titles unwrapped; 149 of 149 re-derived, 0 others moved | @2268853761; close @757b50b6ad | `aj-8.AC2.issuer_grade.txt` PASS |

## 2. ONE REAL RUN at close -- limb 2a over all three monitor windows

`python -m lib.opal_data_harvest.load_window_grade --json` ran at 18:38Z (rc 0). The output is
`close_load_window_grade_20261002T1838Z.json` in this folder. The rule is per_challenge_guard_band, at grain per_run,
with a 2 min band; requests are counted inside the monitor windows; 3 windows.

| pub | windowed requests | grader verdict | window pass rate |
|---|---|---|---|
| bbg | 3,245 | MET | 0.9286 |
| wsj | 1,872 | MET-BY-ABSENCE | -- |
| barrons | 544 | MET-BY-ABSENCE | -- |
| ft | 775 | MET-BY-ABSENCE | -- |
| sa | 743 | MET-BY-ABSENCE | -- |

These are the GRADER's verdicts. `3.0.0_SA_CVO~Z` grades limb 2a on them; this seat does not.

## 3. Served gold -- rebuild #5 under the NEW signed pair, @ee94bac02d

The pair is COO @5d7992b7d4 and CTO @b69262724d. The act ran at 16:29Z with as_of 2026-10-02 and universe round33.
VERIFY read the written parts, and the rule held:

| table | before | after | verify |
|---|---|---|---|
| article_security_mention | 14,375 | **23,691** | gone 0, pre-existing changed 0, added 9,316; titled 23,691 of 23,691 |
| chatter_daily | 58,300 | 58,300 | gone 0; changed 33,986 = 33,980 by an added mention + 6 coverage-only (all inside the CTO's four bounds); other 0 |

The served `/timeline/day` headline now reads from this gold. That is RESAPP am-1, drained by `2.0.0_SA_COO~Z`
@6436cc930a.

## 4. FWD-11 per publisher

| pub | (1) robust auth | (2a) grader | (2b) |
|---|---|---|---|
| bbg | r33 | MET | PASS-FIXTURE |
| wsj | MET (r34) | MET-BY-ABSENCE | OPEN (no sample) |
| barrons | MET (r34) | MET-BY-ABSENCE | OPEN (no sample) |
| ft | **NOT MET** | MET-BY-ABSENCE | OPEN (no sample) |
| sa | not graded | MET-BY-ABSENCE | OPEN (no sample) |

**ft limb (1) has no working route today.** Every route was measured this round:

| route | result | row |
|---|---|---|
| NopeCHA Token API | discontinued (error 19) | Z-W92-S18 |
| NopeCHA hCaptcha recognition | 400 "outdated format"; the current API reference names no hCaptcha | Z-S66 |
| NopeCHA browser extension | loaded and running; did not clear the challenge in 150 s | Z-W90-S21 |
| Ocilar | 503, hcaptcha "coming"; re-check `HVST-RECHECK-OCILAR-1` due 2026-11-01 | Z-W92-S19 |
| hand-solved session plus keep-alive | died at 24 min (aj-4) and 75 min (ai-2) | Z-W92-S20 |

ft stays OFF (STOP_FT). The unpacked extension persisted in the ft profile's Secure Preferences. It is inert, because
both ft launchers keep Playwright's default `--disable-extensions`.

## 5. Depth and drivers (18:4xZ)

| pub | pairs | stored | driver |
|---|---|---|---|
| sa | 68 of 89 | 8,570 | running (pid 31676) |
| bbg | **89 of 89** | 1,239 | finished 18:35:08Z, not interrupted |
| barrons | **89 of 89** | 149 | finished 11:36Z |
| wsj | not re-read this round (r36: 84 of 89, 371) | -- | -- |
| ft | 3 of 89 (r36) | 62 | OFF (STOP_FT) |

The bbg raw outbox has 1,237 uploaded and **2 pending** on `SilverRowError`. One is `TD7VMGKGCTIZ00`, the known
Z-W91-S19 row (mixed int/str `duration`). The other, `THSVU1KIJH9O00`, is new and its shape is not yet read. 10 of 25
upload passes returned rc=2, but the rows behind them landed on later passes: only these 2 remain pending.

## 6. Proposed for round 38 (the CTO decides)

1. **The FWD-11 ft limb is an ENDPOINT question.** No solver route works (section 4). Options:
   - (a) qualify it as an essential wait until the Ocilar re-check on 2026-11-01, which needs Andrew's word;
   - (b) a new solver vendor, which needs Andrew's word for each one;
   - (c) accept ft at the depth it has.
   Hand-solved sessions do not hold.
2. **HARVST v0.14, FWD-16 and FWD-17** (CTO 28634, @82d1cb21e2): cut after `3.0.0_SA_CVO~Z` re-signs. The
   ratified-text half is STALE and the notifier withholds.
3. **2 stranded bbg rows** (`SilverRowError`): one coercion cell, or accept 2 of 1,239.
4. **A gold refresh after #5.** Silver keeps growing (sa 8,570 stored, bbg 1,239). Under CLAUDE.md a production
   pipeline must be scheduled, so make gold a scheduled producer rather than another ad-hoc pair.
5. **(2b) for wsj, barrons, ft and sa:** no challenge has been presented at load, so no sample exists.
6. **NopeCHA renewal on 2026-10-31** is Andrew's money call: both NopeCHA routes fail on hCaptcha.

## 7. Rows this round (17 since 06:30Z)

- BLOCKING (INERT):
  - Z-S66, NopeCHA has no hCaptcha;
  - Z-W92-S18, Token API discontinued;
  - Z-W92-S19, Ocilar 503;
  - Z-W92-S20, the session dies under keep-alive;
  - Z-W90-S17, barrons dict titles, fixed by aj-8;
  - Z-W90-S21, the extension did not solve.
- BLOCKING ARMED: Z-S64, bbg 2a on live traffic. It is disarmed by Z-S65.
- OBSERVATION: Z-S63, Z-W90-S12 to S16, and Z-W90-S18 to S20.
