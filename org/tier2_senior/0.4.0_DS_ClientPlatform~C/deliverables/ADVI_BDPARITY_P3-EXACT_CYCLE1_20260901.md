# ADVI_BDPARITY.P3-EXACT -- CYCLE 1 RECORD

**Seat:** `0.4.0_DS_ClientPlatform~C` | **Completed:** 2026-09-01T05:4xZ | **TO:** `ADVI_BDPARITY.P3-EXACT`
**Inputs, both PINNED:** cells `ADVI_BDPARITY_P2-2_CELLS_20260901.csv` @`e12a0b2960` (15,445 rows);
exclusion `ADVI_BDPARITY_P2-2_NOTCOMPARABLE_ACCOUNTS_20260901.csv` @`ecc18c543b` (64 accounts).
**Seated by:** `2.0.0_SA_COO` spawn (NOT Andrew-direct -- attribution corrected by that seat at 90756 s.0;
the words at this terminal were its `--say` hint).
**Class driven:** LARGE. **Disposition taken: NONE.** All mechanisms routed; no fix, no convention change.

---

## 0. THE STANDING SENTENCE FOR THIS CYCLE

> **The day-count residual is ONE-SIDED: 1,226 of 1,226 after exclusion, ZERO counterexamples in 15,376
> cells. We never link MORE days than BD. Only ever fewer.** The census published this residual as a
> RATE and omitted its SIGN; the sign was in the columns it shipped.

**And the lead, unchanged and reinforced:** the census is a TWO-WAY AUDIT and it is still finding more
on OUR side than on BD's.

---

## 1. THE EXCLUSION (2.0.0_SA_COO 90726 s.3(A), grain ruled at 90756 s.1)

Applied at ACCOUNT grain -- every cell of all 64 accounts -- per the ruled asymmetry: for P3's
consumer a false positive is a cell not driven this round (free), a false negative is tuning our
producer to reproduce a garbage figure that matches BD's (bakes a defect in behind a green class).

```
  exclusion set                                 64 accounts
  PRESENT in the compared table                 51        (13 already had EVERY cell withdrawn)
  CELLS WITHHELD                                69        <- the printed cost, per 90756 s.1
      by class    EXACT 42 | TIGHT 9 | LARGE 18
      by period   QTD 49 | YTD 19 | 1Y 1
  P3 POPULATION AFTER EXCLUSION            15,376 cells over 5,155 accounts
      (was 15,445 / 5,206 -- displacement 0.45% of cells)
```

**51 of the 69 withheld cells (61%) were EXACT or TIGHT.** That is the over-inclusion measured rather
than asserted: 51 agreeing cells withheld to be certain of not driving 18. **EXCLUDED IS NOT
CONDEMNED** -- any account the 114-row read labels legitimate returns to this population.

### 1a. The exclusion cross-check PASSED on a second instrument

| | |
|---|---|
| independent derivation | twr_daily, `\|r_net\| > 1.0`, FULL history, ALL accounts |
| denominators | 540 of 540 partitions, 3,058,096 rows, 8,632 accounts |
| result | 232 rows over 188 accounts |
| **`~Y`'s 64 contained in my 188** | **64 of 64. MISSING: ZERO.** |

Different code, different read path, different population -- corroboration under rule 22, not repetition.

---

## 2. MECHANISM 1 -- WITHDRAWN. My hypothesis died on its own pre-registered kill condition.

**Hypothesised:** the 1Y day-count asymmetry is the `1.0.0_SA_CTO` 85237 boundary defect (our linker's
1Y open a day late), unfixed in the census bytes.
**Pre-registered kill condition (90784 s.4):** *"if the 85237 correction IS in the census bytes, this
hypothesis is DEAD."*

Measured by CONTENT on every plane a run could have used (rule 22a -- never by filename):

```
  SERVED    s3://opal-data-49financial/_code/parity_period_returns.py   (s3api head-object, UTC)
            ETag 21e2c3ef8822f31fccbf680c21484137   41,544 B   2026-08-31T17:53:28Z
  WORKTREE  md5  21e2c3ef8822f31fccbf680c21484137   41,544 B   CR count 0
  COMMITTED git show 2762f02f6a:<path>  (BP1-6, the ruled 1Y-open fix)
            md5  21e2c3ef8822f31fccbf680c21484137   41,544 B
  NEGATIVE CONTROL  git show 5da9e7fffc:<path>  (the commit BEFORE BP1-6)
            md5  586dfcb52de527c854541c26c753cd5a   40,390 B   <- DIFFERS on digest AND size
```

**ALL THREE PLANES CARRY IDENTICAL BYTES, and the control CAN differ and does.** Source pinned at
`parity_period_returns.py:283-288 @2762f02f6a`. The deploy at 2026-08-31T17:53:28Z precedes the census.

> **HYPOTHESIS DEAD. The 1Y asymmetry is a different mechanism.**

**Two traps closed rather than assumed past:** (a) CR count 0, so the worktree digest is not an autocrlf
artifact; (b) an EARLIER deploy of this key (2026-08-30T02:44:30Z) carried ETag `586dfcb5...` = the
PRE-fix blob -- **reading that window-CLOSE frame alone would have inverted the answer.**

⚠ "Which plane did the census run on" is UNANSWERED and does not need answering, because all three are
byte-identical. That is the only shape in which an open wrong-object question is harmless.

---

## 3. MECHANISM 2 -- REAL AND SUBORDINATE. My prediction FAILED.

`0.4.0_DS_ClientPlatform~Y` @`16f1762977` localized the spot-check disagreement to an 87-day segment
`2025-08-28..2025-12-31` by nesting subtraction (`1Y > YTD > QTD`; only 1Y moved).

**I read the nesting PREMISE at source, which nobody had done and on which the whole localization
rests** -- `parity_period_returns.py:330-396 @2762f02f6a`: one `period_window` for all periods, the
same `daily` frame date-filtered, a geometric product over the slice; **the only period-conditional
branches in the function are `:320` and `:347`, BOTH `period == "SI"`.** QTD/YTD/1Y receive no
special-casing, so the products compose over disjoint date sets and the identity holds STRUCTURALLY.
*(A source read of a structural property, UNEXERCISED on data. No reserved word.)*

**Pre-registered prediction:** the segment-localized bucket carries *"a large majority"* of 1Y-LARGE.

```
  1Y LARGE (exclusion-applied)                        991
    A  QTD and YTD both non-LARGE -> segment-localized 331   33.4%
    B  QTD or YTD ALSO LARGE      -> not localized     614   62.0%
    incomplete                                          46
```

**33.4% IS NOT A LARGE MAJORITY. FALSIFIED AS WRITTEN, not rescued downward.**
⚠ **And I decline my own other pre-registered branch too** (*"if small, an n=3 artifact"*) -- 331 of 991
is not small. **The true verdict, REAL AND SUBORDINATE, was outside both branches I committed to.**
Pre-supplying an answer space that excludes the truth is the error; the remedy is to state the question
and not ship the options.

### 3a. The two mechanisms UNIFY arithmetically

```
  1Y window 252 days  -  YTD window 165 days  =  87 days   ==  exactly the localized segment
```

So the escalating rate (QTD 0.8% -> YTD 4.6% -> 1Y 18.4%) is **not three findings; it is ONE deficit
accumulating with window length**, the 87-day 2025 tail carrying a disproportionate share (236 -> 948
when only those days enter). **Mechanism 2 is a SPECIAL CASE of mechanism 3, and that is why bucket A
came in at 33% rather than 0% or 90% -- the failed prediction is EXPLAINED, not merely retracted.**

---

## 4. MECHANISM 3 -- THE ONE-SIDED DAY-COUNT DEFICIT (the cycle's result)

```
  ALL 15,376 cells, exclusion-applied
    our_days >  bd_days        0
    our_days == bd_days   14,150
    our_days <  bd_days    1,226
  BY PERIOD          nonzero    ours>bd
    QTD  n=5,089          42          0
    YTD  n=5,132         236          0
    1Y   n=5,155         948          0
```

### 4a. The discrimination check -- because 1,226-of-1,226 is exactly what a clamp would fake

- **(a) DATA-SIDE positive control:** our_days 211 distinct values, bd_days 197; max 252 on BOTH;
  per-period modes agree. Neither column constant, neither derived from the other.
- **(b) SOURCE-SIDE, decisive:** `parity_period_returns.py:374 @2762f02f6a` --
  `row["days_linked"] = int((~neutral).sum())`, computed from OUR frame ALONE. **`our_days` never sees
  `bd_days` anywhere in the function; the harness is structurally incapable of clamping.** The
  comparison CAN return `>`. It returns it zero times.

> **The one-sidedness is a property of the WORLD, not of the instrument.**

### 4b. The deficit is BIMODAL and the two halves want different fixes

```
  shortfall      n      EXACT  TIGHT  LARGE   LARGE share   median |delta|
     1 day     979       454    226    299       31%            0.89 bp
    2-5 days    86        10     10     66       77%       10,000.00 bp
    6-20 days   49         8      4     37       76%        9,988.97 bp
    21+ days   120        31     13     76       63%        9,337.78 bp
```

**A one-day shortfall barely moves the number (0.89 bp, 46% still EXACT) -- the signature of a
boundary/inclusive-exclusive CONVENTION difference. A multi-day shortfall is catastrophic (~10,000 bp
= 100%) -- the signature of an actual linking deficit.** Treating 1,226 as one mechanism points
remediation at the 979 benign cells and buries the 255 carrying the damage.
*(Independently derived at `3.0.0_SA_CVO` 90814 on the same table; two seats, same split.)*

---

## 5. THE UNSCOPED READ -- what every scoped instrument structurally could not see

Rule 22's coverage clause: a check scoped to the members cannot see a defect in what the members
SHARE. Run over the whole table rather than the parity cohort:

```
  twr_daily accounts (full history)          8,632
  the BD parity cohort                       5,309    <- 3,323 of our accounts are NOT in the census
  above |r_net|>1.0, cohort-scoped/in-window   114 rows /  64 accounts   (the census)
  above |r_net|>1.0, FULL population+history   232 rows / 188 accounts   (this scan)
  distinct dates carrying one                  111    (the census saw 35)
```

> **The gold defect is ~2-3x larger than the census could see. THE CENSUS IS NOT WRONG -- IT WAS
> SCOPED.** Its s.9 named the `|r_net|` bound as its limit. **The COHORT and the WINDOW were also
> limits and neither was named.**

### 5a. The metadata plane is CLEAN -- a negative result, reported as one

```
  PRIOR    2024-01-01..2025-08-27   288 of 540 partitions   written 2026-08-30   schema 11 -> 15
  SUSPECT  2025-08-28..2025-12-31    87 of 540              written 2026-08-30   schema 15/15/15
  CONTROL  2026-01-01..2026-08-28   165 of 540              written 2026-08-30 + 08-31
  boundary 2025-12-31 -> 2026-01-02 : sizes 261,351 -> 258,432, writes 04:59:55Z -> 05:00:07Z. SMOOTH.
  rebuild footprint: 539 of 540 partitions written 2026-08-30; 1 on 08-31 (terminal-day re-touch)
```

**No structural discontinuity at the segment boundary** -- so the mechanism is in the VALUES or the
LINKING, not producer shape. Eliminates a whole class from P3's search space, and corroborates `~Y`'s
corpus-clearing at POPULATION scale (540 partitions vs 271) on a different instrument.

---

## 6. THE LARGEST DATE CLUSTER IN HISTORY, AND THE `C` CLASS GETS ITS MECHANISM

```
  2025-07-25    39 blowup rows   <- LARGER than the census's top date (2026-01-26, 19)
  2026-01-26 19 | 2025-10-15 10 | 2024-11-01 7 | 2026-04-09 7 | 2024-08-28 7
```

**2025-07-25 is invisible to the census BY CONSTRUCTION: it precedes the 1Y window open by 34 days.**

Signature census on each clustered date's FULL blowup set:

| date | blowups | `cf_net == -bmv` (FULL SWEEP-OUT) | `cf_net == 0` (NO FLOW) | other |
|---|---|---|---|---|
| 2025-07-25 | 39 | **19** | 20 | 0 |
| 2026-01-26 | 19 | 0 | 19 | 0 |
| 2025-10-15 | 10 | 0 | 10 | 0 |
| 2026-04-09 | 7 | 0 | 7 | 0 |
| 2026-05-06 | 5 | 0 | 5 | 0 |
| **negative controls** | 2025-07-24: **0** | 2025-07-28: **0** | 2026-01-27: **0** | |

**On 2025-07-25 and nowhere else in the sample, 19 rows carry `cf_net == -bmv` EXACTLY -- a full
sweep-out of the entire opening balance recorded -- while `emv > 0` AND GREW.** Specimens:
bmv 1.03 -> emv 1.77, cf_net -1.03; bmv 3.46 -> emv 9.63, cf_net -3.46.

> **THAT IS THE `C` CLASS.** `3.0.0_SA_CVO` 90737 s.5 defined C as *"flow recorded, comparable to base,
> return still >100%"*, called it the most interesting class -- neither known mechanism -- and warned it
> must not be folded into A or B. `cf_net == -bmv` **is** a flow comparable to base.

**AND IT IS THE OPPOSITE DEFECT FROM A, WHICH IS WHY FOLDING THEM WOULD HAVE BEEN WRONG:**

```
  A  cf_net == 0      a flow HAPPENED and was NOT recorded              -> flow is MISSING
  C  cf_net == -bmv   a full outflow WAS recorded and the value ROSE    -> flow is SPURIOUS, or emv stale
```

**A per-date flow RE-INGEST fixes A. It would not fix C, and on a spurious-flow row it could make it
worse.** `1.0.0_SA_CTO` 90742 s.3 asked what the clustered dates have in common; **this says 2025-07-25
does not have the same thing in common as the others.**

---

## 7. P3's TARGET POPULATION, CHARACTERISED (cycle 2's material)

```
  1,506 both-sides-linked LARGE, over 919 accounts   (day counts AGREE; the number still differs)
    by period   1Y 671 | YTD 652 | QTD 183
    delta_bp    p10 -39.30  p25 -13.88  median +15.46  p75 +34.31  p90 +78.72
    sign        ours>BD 1,054 | ours<BD 452   (2.3:1, same direction as the day deficit)
    magnitude   |d|<100bp 1,345 | 100-1000bp 124 | >1000bp 47
```

**Mostly small-and-systematic with a thin violent tail.** This is the only major LARGE population with
no named mechanism, and it is cycle 2's target.

---

## 8. WHAT IS NOT CLAIMED

No reserved word ("proof / root cause / definitively / source-confirmed") is used anywhere above.
NOT established: why 2025-07-25 carries a sweep-out cluster; whether those 19 accounts are in the 5,309
cohort; that 111 dates is the whole population (`|r_net| > 1.0` remains an arbitrary bound and a milder
version of either defect is invisible to it); any diagnosis of WHY we under-link. The C-class
identification is a SIGNATURE MATCH against `3.0.0_SA_CVO`'s definition, **not** a dispositioning of the
census's 14 C rows, which remain that seat's and remain UNDISPOSITIONED.

**No convention change (P3-3 gate untouched at `1.0.0_SA_CTO`). No producer fix. No vendor call** --
everything above is landed bytes, git objects, one S3 head-object and one gold read.
**The per-DATE flow re-ingest stays UNCOVERED and unowned** (`1.0.0_SA_CTO` 90742); s.6 is input to
sizing it, **not** an absorption of it into P3.

---

## 9. CYCLE LEDGER (P3-1)

| # | class | mechanism | grounding | disposition | re-census delta |
|---|---|---|---|---|---|
| 1 | LARGE | M1 1Y-open boundary defect | `:283-288 @2762f02f6a` + 3-plane byte match + negative control | **WITHDRAWN** -- hypothesis dead on its own kill condition | none |
| 1 | LARGE | M2 87-day segment `2025-08-28..2025-12-31` | `~Y` @`16f1762977`; nesting premise read at `:330-396 @2762f02f6a` | **REAL, SUBORDINATE** (33.4% of 1Y-LARGE); special case of M3 | none |
| 1 | LARGE | M3 one-sided day-count deficit, bimodal | table @`e12a0b2960`; discrimination at `:374 @2762f02f6a` | **NAMED, ROUTED** -- 1-day limb is a CONVENTION question for the P3-3 gate | none |
| 1 | (producer) | M4 `cf_net == -bmv` spurious-flow, 2025-07-25 | gold twr_daily scan, 5 dates + 3 negative controls | **ROUTED** to the UNCOVERED item; NOT absorbed | none |

**Re-census delta this cycle: ZERO by design.** No disposition was taken, so no cell changed class.
Cycle 1 was a MECHANISM cycle; the TO's loop requires the mechanism before any fix, and three of the
four mechanisms are not this seat's to remedy.

## 10. COMPILER TOOLS

| tool | use | result |
|---|---|---|
| `comp-read` | `parity_period_returns.py` (696 lines), `advi_bdparity_w2_runner.py` | surfaced `period_window`'s RULED comment at `:284-285` -- the line that killed M1 -- and 69 qualifiers a grep would not have shown |
| `comp-find` | `--name '*BDPARITY*'` (128 hits/144,877 files); `'canonical/twr_daily'` (2,851 hits, banded) | located the TO, the P2-2 result, and the gold prefix; denominators printed |
| `comp-to` | set session TO_ID `ADVI_BDPARITY.P3-EXACT` | race-free per-session file |
| raw `aws s3api` | `head-object` on the served harness | the ONLY plane that could falsify M1; `s3api` for UTC, never `s3 ls` |
| `git show` by content | 3 commits + negative control | rule 22a -- deployed bytes vs BUILD INPUT, never by filename |

**Not run:** `comp-pipescript io/deployed/postdeps` and `comp-validate` -- this cycle deployed nothing,
ran no gold script and produced no served artifact; every read was analysis over landed bytes. They
bind on the cycle that takes a disposition.
