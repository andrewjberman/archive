# AMGT_HARVST ROUND 19 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~22:1xZ

**Issuance:** `11b3530483`: one chain, `i-1 -> i-2 -> i-3 -> i-4`, over `ROUND_ANALYSIS.round18.md` @`d11fd4d089`; decomp
section 31. **L8-L10 route:** `3.0.0_SA_CVO~Z`. **Class:** WORLD. `i-3` moved a served gold table under a pair, and
`i-4` redeployed `opal-amgt-scoped-api` under a pair plus a NEVER-2 entry.

## 1. FOUR ORDERS, TERMINAL, VALID

| order | risk | deliver | drained / landed | instance |
|---|---|---|---|---|
| `HVST-i-1` UBS off the whole-brand list + limb-agreement test | LOCAL | `24e9a7b4e8` | `7668249a78` | VALID rc=0 |
| `HVST-i-2` a PARTIAL day names its publisher (rule + both routes) | LOCAL | `7275ec579b` | `8f2a0bf027` | VALID rc=0 |
| `HVST-i-3` served `chatter_daily` rebuild with the codes | SERVED | `cac88b78a5` | `035c7d9b7f` | VALID rc=0 |
| `HVST-i-4` scoped-API redeploy | WORLD | seat `0.7.0_AE_CloudOps~A` | entry CLOSED 3 of 3, trunk @`84548218ef` | VALID rc=0 |

- **Suite:** the trunk reads **202 of 202** (base 194).
- **Pairs:**
  - `i-3`: COO @`1eda314890`, CTO @`4f34061729`.
  - `i-4`: COO @`0abf041dfa` (AMENDMENT 1), CTO @`053e4ae20f`.
  - `i-4` also carries the CTO ruling @`3a354b0720`: CORPUS `continuation.py` ships INERT and `i-4` runs alone.

## 2. WHAT MOVED

**Gold, `i-3`:**
- One new `chatter_daily` part, `date=2026-09-29/part-20260929T212132Z`, ETag `4743eb60...`, 51,952 rows.
- The 21 existing columns are unmoved on every row. That was read by this seat from S3 directly, not only by AC1.
- New column `publishers_covered_codes`:

  | data_status | rows | codes |
  |---|---|---|
  | DENIED | 51,803 | `[]` |
  | PARTIAL | 149 | ASML_NA 74 `['sa']`, ASML_US 74 `['sa']`, 992_HK 1 `['wsj']` |
  | COMPLETE | 0 | none |

- Mention and event were not written.

**The deployed API, `i-4`:**
- CodeSha256 `lg6NJ2JL...` -> `uv0oTSMa...` (21:57:59Z).
- The closure diff is exactly 3 source files:
  - `publication_gold.py` and `timeline_api.py` (HARVST);
  - `continuation.py` (CORPUS p-5, INERT on this function by AST trace, by both this seat and the CTO).
- Unzipped 96.7% of 250 MiB. The rollback artifact `61Fb7L90...` is standing.

**`i-1`:**
- 0 served moves on all three tables.
- The round-18 build had already refused the `UBS` brand through limb (a), so the entry was dead. The list now agrees
  with its limb.

## 3. THE ONE REAL RUN (`round19/close_run_round19.py` -> `.out.txt`): CLOSE RUN OK

It invoked the deployed `/timeline` for four securities. The fields compared on each series day are the 12 served
before this round plus `publishers_covered` and `publishers_covered_codes`.

| security | series days = landed | field mismatches | PARTIAL days | events served = landed |
|---|---|---|---|---|
| ASML_NA | 272 of 272 | 0 | 74, all `['sa']` | 0 |
| 992_HK | 272 of 272 | 0 | 1, `['wsj']` | 3 |
| BA | 272 of 272 | 0 | 0 | 1 |
| FDX | 272 of 272 | 0 | 0 | 0 |

`/timeline/day` answers 200 and names the publisher on both PARTIAL securities:
- `ASML_NA` 2026-07-15: `publishers_covered` 1, `['sa']`;
- `992_HK` 2026-09-23: `publishers_covered` 1, `['wsj']`.

## 4. FOR L9

- **This round carries NO judgment criterion.** Every criterion is mechanical, so nothing here tests plausibility. One
  read is offered, and it is not graded here: does a PARTIAL day now say who covered it, in terms a PM can act on?
- **What the API serves are codes (`sa`, `wsj`), not names.** The page's wording is DSGN_AMGTV1's, and the analysis
  ruled that.
- **The `992_HK` `wsj` day is new to the analysis's reading.** It comes from the same identifier rule that round 18 ruled
  correct for ASML.

Rows this round: none new from the workers.
- The seat's entry Log carries a self-correction: it had said this seat's half was one importer short, then conceded
  the half's four was right.
- The issuer's `Z-S41` lesson (re-read the reader before a put) was applied in `i-3`'s dry step, and the reader was
  unmoved.
