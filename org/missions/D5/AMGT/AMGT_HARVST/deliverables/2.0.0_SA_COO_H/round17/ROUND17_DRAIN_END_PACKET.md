# AMGT_HARVST ROUND 17 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~13:0xZ

**Issuance:** `210e8eca23` (two independent orders over `ROUND_ANALYSIS.round16.md` @`f424435829`; decomp section 29).
**L8-L10 route:** `3.0.0_SA_CVO~Z`. **Class:** LOCAL (no served move this round, as ruled).
**Close runs, by this seat on the trunk:** the `f-2` served arm and suite, and the `f-1` census AC1. Both reproduce the
workers' outputs.

## 1. TWO ORDERS, TERMINAL, VALID

| order | risk | drained | audit (landed = branch) | instance |
|---|---|---|---|---|
| `HVST-f-2` a security's first burst survives name detection | LOCAL | `35657cd67c` | 12 = 12 | VALID rc=0 on the trunk |
| `HVST-f-1` the ticker and brand census (read-only) | LOCAL | `7bc0431f40` | 14 = 14 | VALID rc=0 on the trunk |

The `f-1` drain hit an append-only channel conflict (the `W44` and `W43` rows). It was resolved by row-id union onto
HEAD, 3 rows appended, with the row gate clean. It finished through `safe-merge --continue`, whose default subject
("drain: merge wk-AMGT_HARVST-43") stands on the merge.

## 2. `f-2` -- `Z-W40-S1` IS FIXED IN CODE; NOTHING SERVED MOVED

- **Mechanism (the worker's):** `_security_name_tokens` keeps its frequency test (>= 3/4 of tier-A headlines on >= 3
  days) and ALSO requires a name stem to be a stem of an alias that actually hit (`match_forms`, via the new
  `_alias_stems`). A story's own words are in no alias, so they stay linkable. Rows without `match_forms` fall back to
  the old inference.
- **FIXTURE -- MECHANISM TEST, NOT A HELD-OUT GRADE:**
  - Variant 1 (the story is the security's only coverage): old 0 events, new **1 event** (09-10..09-11, 4 articles).
  - Variant 2 (the story among other coverage): unchanged.
  - A planted control of two unrelated stories: stays **2 events**, with no shared members.
- **Served arm, re-run by this seat on the trunk:** `event_rows` under the new rule over the served mention part equals
  the served event part, **8 of 8 on every field**. 0 of 29 securities' stripped stems change. Suite **177 passed**
  (was 172). No pair was needed and none was used.
- Row `Z-W44-S1` (INERT): bounding by matched aliases also stops stripping a brand or ticker stem that is in no alias.
  This matters if round 18 adds ticker or brand aliases, which would then become matched forms.

## 3. `f-1` -- THE CENSUS (read-only; the alias rule is the analysis's)

- **Denominators:** 191 securities, 120 silver articles, 367 forms generated.
- **Added hits by form class:**

  | class | forms with added hits | added pairs (new) | added mentions | title flips | lead flips |
  |---|---|---|---|---|---|
  | T1 ticker | 61 of 191 | 283 (174) | 542 | 12 | 59 |
  | T2 ticker root | 0 forms (no ticker carries a share-class suffix) | -- | -- | -- | -- |
  | B1 short name | 58 of 176 | 329 (303) | 559 | 17 | 87 |
  | **all** | **119 of 367** | **612 (477)** | **1,101** | **29** | **146** |

- **B1 is derived** from each security's own alias field (its leading word), with no source artifact.
- **No brand source exists in the estate** (0 of 191 covered), so "Google" for Alphabet cannot be produced from any
  artifact today.
- **Hazards the census exposes:**
  - 40 forms with added hits are <= 3 characters, and 39 carry a dictionary-word flag. The flag is a proxy, since no
    dictionary is installed (row `Z-W43-S1`).
  - **The served matcher is case-insensitive** (row `Z-W43-S3`): ticker "T" (AT&T) adds 131 spans, and 128 of them are
    the "t" of contractions ("don't"). "V", "F", "C", "NOW" and "COST" have the same mechanism.
  - A ticker rule would therefore need a case-sensitive match, a length floor, or both. That is the analysis's to rule.
- **Controls:** the census agrees with the served `_match_counts` on 37,200 (form, article) pairs with 0 mismatches; a
  mutant falls from 131 to 0 as expected; re-runs are byte-identical.

## 4. JUDGMENT FOR L9 (presented, not graded) -- `f-1` AC4, `ac4_output.txt`

531 sample hits over 119 forms, up to 10 per form (seed 20260929), each with its headline and the words around the match.
**Per form: how many sampled hits are the company?** That read decides which forms, which length floor and which case rule
round 18 can adopt.

## 5. ROWS -- the gate's own fold: 103 ids, GRADUATED 57, DISMISSED_WITH_REASON 25, UNDER_INVESTIGATION 21 (29 files)

- **New, all INERT:** `Z-W43-S1` (dictionary proxy), `Z-W43-S2` (T2 generates 0 forms), `Z-W43-S3` (case-insensitive
  short tickers), `Z-W44-S1` (unmatched brand stems are no longer stripped).
- **`Z-W40-S1` is REMEDIED in code by `f-2`** (graduation is the CVO's).
- **Carried:** ARMED `Z-S37` (the tool's authoring lane) and `Z-W39-S1` (disarmed by condition); ARMED `Z-W41-S1`
  (disarmed by acceptance in round 15); `Z-W37-S4` (the account holder).
- **Armed rows with an owner this seat could not seat: NONE.**

## 6. FOR THE ROUND-18 CUT (the CTO decides)

1. **The alias rule, on the L9 read of section 4:** which forms, what length floor, case-sensitive or not. A brand
   source would have to be named or built.
2. **If aliases grow,** re-read `Z-W44-S1`: the new forms become matched forms and so strippable name stems. That is the
   intended behaviour, and it should be shown on the served events.
3. **Unchanged:** the portal push (Andrew's hold), the Seeking Alpha 402 (the account holder).

## 7. RETAINED, NOT REMOVED

The worktrees `wk-hvst-r15-41`, `-r16-42`, `-r17-43` and `-r17-44` hold untracked worker scratch. Removing them is a
recursive delete, left for the account holder's word. All four branches are fully merged.

## 8. WHAT THIS PACKET DOES NOT DO

It grades no judgment, claims no FWD REALIZED, pushes nothing, and cuts no round-18 cell.
