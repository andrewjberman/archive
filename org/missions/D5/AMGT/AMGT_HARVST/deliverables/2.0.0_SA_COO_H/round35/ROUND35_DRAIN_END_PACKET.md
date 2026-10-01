# AMGT_HARVST round 35 -- drain-end packet (L8 input) -- `2.0.0_SA_COO~H`, 2026-10-01 ~19:4xZ

Round-34 analysis @6cbef26707 -> issuance @33bace02e0 (decomposition section 48). 3 of 3 cells terminal.

## 1. Cells

| cell | result | merged | check at the base |
|---|---|---|---|
| `HVST-ah-1` `~91` | **A**: `challenge_capture.py`, hooked in `verification.py` once the control is located and before it is operated. It saves the rendered DOM (page + frames, sanitizer `ah1-sanitizer-v1`), at most once per publisher per hour; a failure never alters `solve()`. Live in the drivers from @9f3de64c5f; 3 bbg captures so far (16:24, 17:36, 18:46Z). **B**: the 16:24Z capture is the planted fixture. The collector's own TabSession (headless, hosts locked to 127.0.0.1) runs `solve()` on it and holds for 12.03-12.21 s against the 12 s constant. A static page never clears, so the test proves the control was OPERATED, not that a server accepted the hold | @9f3de64c5f + @caed8abbf3 | `ah-1.AC2.output.txt` PASS (check fix @83b90f37a7: colour-safe) |
| `HVST-ah-2` `~90` | `load_window_grade.py` VOIDs every minute with hardware input, whole windows without per-minute buckets, and unmonitored minutes; verdicts are INSUFFICIENT (< 24 clean hours), NOT-MET, MET-BY-ABSENCE and MET | @6e3e68dd84 + @6b315b0d92 (re-land after an exit-5 merge) | `ah-2.AC2.output.txt` PASS |
| `HVST-ah-3` `~92` | the ft "locked" bodies were a **dead session**: the ASML job ran logged in for ~150 fetches, then logged out for ~266. A barrier on a logged-out page now raises AuthExpired and the login cookies are re-seeded. **Premium-labelled teasers** (a tier the account does not hold) are skipped before the fetch. After both fixes: 63 body fetches, 1 locked (2%, was 91%), 23 stored, 49 Premium skipped, 1 renewal | @a78b06d3e6 + @9b14622a78 | `ah-3.AC2.output.txt` PASS (1 job of 2: see section 3) |

## 2. FWD-11 per publisher (CTO ruling msg 27860)

The limb-2a grade comes from the ah-2 grader over windows 1 and 2, through 19:31Z.

| pub | (1) robust auth | (2a) captcha at load | (2b) planted fixture |
|---|---|---|---|
| bbg | r33 | INSUFFICIENT: 987 requests, 14 challenges presented, 13 passed, 5 in void minutes; clean_hours 0 | **PASS** (real capture; control operated 12 s) |
| wsj | MET (r34) | INSUFFICIENT: 884 requests, 0 challenges | none captured (0 challenges at load) |
| barrons | MET (r34) | INSUFFICIENT: 52 requests (no driver run) | none |
| ft | not graded | INSUFFICIENT: 1,061 requests, 0 challenges | none |
| sa | not graded | INSUFFICIENT: 493 requests, 0 challenges | none |

**Why clean_hours is 0 everywhere (a measured value).** A person used the console in every clock hour since monitoring
began: the last hardware minutes were 16:24Z, 17:42Z and 18:xxZ (80 void minutes in window 2, 156,307 hardware events).
The grader counts a clock hour clean only when none of its minutes is void, so FWD-11 (2a) needs the box left
untouched; no code change moves it. bbg's 1 unpassed challenge is a `bot_check` attempt with no matching
`challenge_passed` in its run span, under the grader's stated rule. Which hour it fell in is read from the grader's
JSON, not assumed.

## 3. Depth (FWD-14) and the ft driver

| pub | pairs | new stored | note |
|---|---|---|---|
| sa | 22 of 89 | 3,166 | upload ~12 s per article dominates |
| bbg | 32 of 89 | 451 | sitemap listing |
| wsj | 52 of 89 | 158 | sitemap listing |
| ft | 3 of 89 | 62 (+23 in the ah-3 run) | driver OFF since 16:1xZ (ah-3 held ft) |

52 names have new items; 15 of them gained 50 or more new, 14 gained 100 or more. Andrew (19:2xZ, direct): "this pace
is fine" -- pacing unchanged. Gold rebuild #3 runs at 20:00Z (signed pair).

**ft driver stays OFF (rows Z-W92-S11, S12 ARMED -> issuer row Z-S55):**
- S11: the driver passes `--no-sign-in`, which refuses a dead saved session at fetch 1.
- S12: the ft session dies ~20-30 min after each renewal, so a job ends `auth_failed_after_refresh` and ft cools down for 60 min.

## 4. Proposed for round 36 (the CTO decides)

1. **ft session longevity (S12):** find why the session dies ~20-30 min after renewal, and let the driver renew in-job (S11).
2. **FWD-11 (2a):** an unattended window of 24 clean hours. This is an operator condition (no console input), not code.
3. **(2b) for wsj/barrons/ft/sa:** these need a challenge presented at load. None has been in ~2,500 requests; until one is, (2b) cannot be met for them, and MET-BY-ABSENCE applies only to (2a).
4. **barrons driver run;** **sa upload speed** (left as is: Andrew is content with the pace).

Rows this round: Z-W90-S9, Z-W91-S17, Z-W92-S11..S14; disposition Z-S55.
