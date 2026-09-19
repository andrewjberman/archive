# AMGT-rk-54 -- publication-links/v1 coverage MEASURE (2026-09-18)

Worker `0.9.0_WK_AMGT_RESAPP~54`. MEASURE ONLY -- no code edit, no producer run, no pool write. All
outputs below are the literal stdout of the five proof_of_spec invocations (AC1-AC4 are the
instruments, AC5 grades the JSON record built from them), re-run at THIS cell's FINAL, SETTLED cut
(see "the vintage race" note below -- the crosswalk population moved mid-session and these are the
post-settlement numbers, consistent with the delivered JSON and the proof_of_spec instance).

## THE VINTAGE RACE (read this first -- it changes every crosswalk-derived number below)

A first pass of AC2/AC5, run at spawn, read `crosswalk/v1/2026-09-15.json` (the vintage this order's
own text names, population 33). Before this record was finalized, a SECOND vintage
`crosswalk/v1/2026-09-19.json` landed live in the pool (`LastModified 2026-09-19T01:23:43Z`, written
by something other than this worker -- this cell makes no pool writes). `crosswalk.load_crosswalk()`
resolves the pool's LATEST object by `sorted(keys)[-1]` (`lib/research/identity/crosswalk.py:528`),
so a bare, unpinned call to it -- exactly what AC2/AC5's invocations make -- silently started
returning a DIFFERENT, larger population (36, not 33) partway through this cell's own run, with zero
code change on either side. Re-running the identical instrument twice after the new file settled
(no further arrivals) reproduces 36 both times -- STABLE now, but NOT stable across the session as a
whole. Filed as surprise rows `AMGT_RESAPP-Z-W54-S1` (validation names absent from the 09-15
vintage) and `AMGT_RESAPP-Z-W54-S2` (the race itself). All numbers below are the SETTLED, final
reading, at vintage `crosswalk/v1/2026-09-19.json`, population 36 (36 MEASURED + 60 UNRESOLVED = 96
total crosswalk records, up from 89 at the order's cited cut).

## AC1 -- pool association layer (paginated `list_objects_v2`, `Delimiter='/'` semantics via key-form split)

```
LINKS key_forms 3 objects 7
  form BA links 2
  form COST links 2
  form HD links 3
BODIES publishers 5 objects 7 [('barrons', 2), ('bbg', 2), ('ft', 1), ('sa', 1), ('wsj', 1)]
```
Denominator: 7 link objects (total), 7 body objects (total). 3 key forms present: BA, COST, HD.
0 `<malformed>` keys. Unaffected by the vintage race (this listing reads `publication-links/v1/`,
not the crosswalk).

## AC2 -- crosswalk identity -> pool links (36 of 36 MEASURED crosswalk records, vintage 2026-09-19.json)

```
ASML_NA_Equity aliases 3 links 0 states {}
BABA_US_Equity aliases 3 links 0 states {}
BBSE3_BZ_Equity aliases 3 links 0 states {}
BP/_LN_Equity aliases 3 links 0 states {}
BA_US_Equity aliases 3 links 2 states {}
COST_US_Equity aliases 3 links 2 states {}
ENEL_IM_Equity aliases 3 links 0 states {}
HSBA_LN_Equity aliases 3 links 0 states {}
HAL_US_Equity aliases 3 links 0 states {}
RMS_FP_Equity aliases 3 links 0 states {}
HD_US_Equity aliases 3 links 3 states {}
2317_TT_Equity aliases 3 links 0 states {}
ICICIBC_IN_Equity aliases 3 links 0 states {}
IMB_LN_Equity aliases 3 links 0 states {}
INTU_US_Equity aliases 3 links 0 states {}
9433_JP_Equity aliases 3 links 0 states {}
KMB_US_Equity aliases 3 links 0 states {}
KPN_NA_Equity aliases 3 links 0 states {}
992_HK_Equity aliases 3 links 0 states {}
NG/_LN_Equity aliases 3 links 0 states {}
NOVN_SW_Equity aliases 3 links 0 states {}
NU_US_Equity aliases 3 links 0 states {}
PBR_US_Equity aliases 3 links 0 states {}
RWE_GR_Equity aliases 3 links 0 states {}
RKT_LN_Equity aliases 3 links 0 states {}
ROG_SW_Equity aliases 3 links 0 states {}
SAP_GY_Equity aliases 3 links 0 states {}
SSE_LN_Equity aliases 3 links 0 states {}
ST_SP_Equity aliases 3 links 0 states {}
ULVR_LN_Equity aliases 3 links 0 states {}
VLO_US_Equity aliases 3 links 0 states {}
WALMEX*_MM_Equity aliases 3 links 0 states {}
ZURN_SW_Equity aliases 3 links 0 states {}
CAT_US_Equity aliases 2 links 0 states {}
CSL_AU_Equity aliases 2 links 0 states {}
6861_JP_Equity aliases 2 links 0 states {}
RECORDS measured 36 of 96 with_links 3 without_alias 0
```
Denominator: 36 of 96 crosswalk records are `RESOLUTION_MEASURED` (60 `UNRESOLVED`, all
`security-<hash>`-only with no `security_key`/company name). `with_links=3` (BA, COST, HD -- exactly
the read side's coverage figure, unchanged by the vintage race). `without_alias=0`: every MEASURED
record carries generic alias forms from `crosswalk.aliases()` (3 for the 33 original names, 2 for
CAT/CSL/6861), so "no lookup key" is NOT reproduced at this instrument's granularity.

## AC3 -- ingestion ledger (main tree, read-only URI)

```
LEDGER C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest/progress.sqlite3 bytes 282624 mtime 2026-09-15T04:58:26.531710Z
TABLE jobs rows 32
TABLE articles rows 84
TABLE article_objects rows 83
TABLE article_links rows 84
TABLE upload_outbox rows 167
JOBS by publisher, security_key, status:
   ('barrons', 'BA', 'auth_failed_after_refresh', 1)
   ('barrons', 'BA', 'complete_candidates', 2)
   ('barrons', 'BA', 'request_rejected', 1)
   ('bbg', 'BA', 'complete_candidates', 2)
   ('bbg', 'BA', 'error', 2)
   ('bbg', 'BA', 'insufficient_coverage', 1)
   ('ft', 'BA', 'complete_candidates', 1)
   ('sa', 'BA', 'complete_candidates', 1)
   ('sa', 'BA', 'new_articles', 1)
   ('wsj', 'BA', 'complete_candidates', 1)
   ('barrons', 'COST', 'complete_candidates', 2)
   ('barrons', 'COST', 'cooldown', 1)
   ('bbg', 'COST', 'complete_candidates', 1)
   ('bbg', 'COST', 'cooldown', 1)
   ('bbg', 'COST', 'insufficient_coverage', 1)
   ('bbg', 'COST', 'request_rejected', 1)
   ('ft', 'COST', 'complete_candidates', 1)
   ('sa', 'COST', 'complete_candidates', 1)
   ('wsj', 'COST', 'complete_candidates', 1)
   ('barrons', 'HD', 'complete_candidates', 1)
   ('barrons', 'HD', 'cooldown', 1)
   ('barrons', 'HD', 'error', 1)
   ('bbg', 'HD', 'complete_candidates', 1)
   ('bbg', 'HD', 'cooldown', 2)
   ('ft', 'HD', 'complete_candidates', 1)
   ('sa', 'HD', 'complete_candidates', 1)
   ('wsj', 'HD', 'complete_candidates', 1)
ARTICLES by publisher, security_key:
   ('barrons', 'BA', 5)
   ('bbg', 'BA', 9)
   ('ft', 'BA', 5)
   ('sa', 'BA', 10)
   ('wsj', 'BA', 5)
   ('barrons', 'COST', 5)
   ('bbg', 'COST', 5)
   ('ft', 'COST', 5)
   ('sa', 'COST', 5)
   ('wsj', 'COST', 5)
   ('barrons', 'HD', 5)
   ('bbg', 'HD', 5)
   ('ft', 'HD', 5)
   ('sa', 'HD', 5)
   ('wsj', 'HD', 5)
LINKS by security_key:
   ('BA', 34)
   ('COST', 25)
   ('HD', 25)
OUTBOX by status, error_code:
   ('pending', None, 167)
```
Denominator: jobs=32, articles=84, article_objects=83, article_links=84, upload_outbox=167 rows.
Jobs and articles exist ONLY for `BA`, `COST`, `HD` -- no other security_key appears in `jobs` or
`articles`, including `HAL` and `VLO` (both `pilot_securities` in config.json) and CAT/CSL/6861
(not pilots and never jobbed either). All 167 outbox rows are `pending`/no error -- fetched and
recorded, not yet uploaded (`automatic_uploads_enabled=false`). Unaffected by the vintage race (this
is a device-local SQLite file, not the pool crosswalk).

## AC4 -- harvester config + universe

```
CONFIG universe_source = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/universe.json"
CONFIG jobs_per_run = 1
CONFIG recurring_schedule_enabled = false
CONFIG automatic_uploads_enabled = false
CONFIG enabled_publishers = ["sa", "ft", "wsj", "bbg", "barrons"]
CONFIG articles_per_security = 5
CONFIG pilot_securities ['BA', 'COST', 'HD', 'HAL', 'VLO'] count 5
universe rc 0
UNIVERSE denominator 89 securities 89 pilot_keyed 5 ['BA', 'COST', 'HAL', 'HD', 'VLO'] security_hash_keyed 84
```
Denominator: universe command's own denominator = 89 securities -- a THIRD, INDEPENDENT denominator
(distinct from the 36-record crosswalk MEASURED population and the intake's 191-name chatter union;
also unaffected by the vintage race, since it reads `universe_source`'s worker-deliverables JSON, not
the pool crosswalk). 5 of 89 are pilot-keyed by company-name match; 84 are `security-<hash>`-keyed.
`universe_source` names a WORKER deliverables folder (`0.9.0_WK_AMGT_RESAPP~3/universe.json`) read by
production config -- the `C-PRODUCTION-HOME` class named in the order; recorded, not fixed.

## AC5 -- per-name table (36 MEASURED crosswalk records at the settled vintage, classes by subtraction from 36)

| security_key | class | links | jobs | articles |
|---|---|---|---|---|
| BA_US_Equity | COVERED | 2 | 13 | 34 |
| COST_US_Equity | COVERED | 2 | 10 | 25 |
| HD_US_Equity | COVERED | 3 | 9 | 25 |
| ASML_NA_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| BABA_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| BBSE3_BZ_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| BP/_LN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| ENEL_IM_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| HSBA_LN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| HAL_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| RMS_FP_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| 2317_TT_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| ICICIBC_IN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| IMB_LN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| INTU_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| 9433_JP_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| KMB_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| KPN_NA_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| 992_HK_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| NG/_LN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| NOVN_SW_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| NU_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| PBR_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| RWE_GR_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| RKT_LN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| ROG_SW_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| SAP_GY_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| SSE_LN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| ST_SP_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| ULVR_LN_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| VLO_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| WALMEX*_MM_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| ZURN_SW_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| CAT_US_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| CSL_AU_Equity | NEVER-JOBBED | 0 | 0 | 0 |
| 6861_JP_Equity | NEVER-JOBBED | 0 | 0 | 0 |

**Class counts: COVERED=3, STORED-NOT-KEYED=0, JOBBED-NOTHING-STORED=0, NEVER-JOBBED=33,
UNMEASURED=0. Sum = 36 = population.**

**Validation names (CAT, CSL, Keyence/6861):** at the SETTLED vintage (`crosswalk/v1/2026-09-19.json`)
all three ARE present -- `{"CAT_US_Equity": "NEVER-JOBBED", "CSL_AU_Equity": "NEVER-JOBBED",
"6861_JP_Equity": "NEVER-JOBBED"}` -- but at the order's OWN cited vintage
(`crosswalk/v1/2026-09-15.json`, population 33) none of the three existed under either resolution.
Both readings are filed as surprise rows (S1 for the 09-15 absence, S2 for the vintage race that
produced the 09-19 answer); this record's numbers are the settled, final (09-19) reading.

## The paragraph (CTO's L4 input)

The dominant cause over the 36 MEASURED crosswalk names (vintage crosswalk/v1/2026-09-19.json) is
INGESTION (NEVER-JOBBED), not association: 33 of 36 names never had a harvest job run for any of
their crosswalk aliases, because `__main__.py`'s `universe()` (`:12-36`) gates jobs to
`config.json`'s 5 `pilot_securities` by company-name match, and the ledger shows only 3 of those 5
(BA, COST, HD) ever actually ran a job -- `HAL_US_Equity` and `VLO_US_Equity`, though pilot-keyed by
the universe command, carry 0 job rows in `progress.sqlite3`'s `jobs` table. The second-largest class
is COVERED (3 of 36: BA_US_Equity, COST_US_Equity, HD_US_Equity), where jobs ran (`worker.py:57
run_job` -> `:102 client.articles(security, limit)`), articles were fetched (84 rows across
BA/COST/HD in the ledger's `articles` table) and links landed in the pool under the crosswalk's own
alias form (`catalog.py:74` builds `publication-links/v1/{security['key']}/{publisher}/{digest}.json`
from the job's security) -- but only 7 of those 84 ledger articles (2 BA, 2 COST, 3 HD) are present
as pool objects; the other 77 sit in `upload_outbox` at `status='pending'` because
`automatic_uploads_enabled` is false -- an upload-backlog finding orthogonal to this cell's per-name
classification, not itself a fifth class. STORED-NOT-KEYED and JOBBED-NOTHING-STORED are both 0 of
36 at this cut: no pool key form is unresolved against a crosswalk alias
(`unresolved_forms_in_pool=[]`), and no job ran that produced zero articles. Of the L3 intake's five
named no-lookup-key tickers (AAPL, NVDA, MSFT, JPM, TSLA): absent from all 96 crosswalk records under
either resolution (36 MEASURED + 60 UNRESOLVED) -- they are OUT OF THIS POPULATION entirely, not
merely lookup-key-empty within it, a different claim than the L3 framing implies. The three
C-VALIDATION-NAMES tickers (CAT, CSL, Keyence/6861) ARE present at this settled vintage, all classed
NEVER-JOBBED -- but were ABSENT at the order's own cited vintage (2026-09-15.json, population 33): a
new crosswalk build (`crosswalk/v1/2026-09-19.json`) landed live in the pool during this cell's own
execution window, adding exactly these three names and six others (33 -> 36), which is itself the
headline surprise for L4: the population this order's own text treats as fixed ("MEASURED = 33") is
not stable across a single MEASURE cell's runtime, because `crosswalk.load_crosswalk()` always
resolves whatever pool object currently sorts last, never a pinned vintage.

## Note on `without_alias`

The order's AC2 expectation reads `without_alias J` as "the count of names with NO lookup key (the
L3 claim about AAPL/NVDA/MSFT/JPM/TSLA...)". At the settled cut every one of the 36 MEASURED records
returns nonzero alias forms from `crosswalk.aliases()`, so `without_alias=0` measured on THIS
instrument -- `crosswalk.aliases()` always derives generic forms from the record's `security_key`
regardless of whether the pool ever resolves them, it does not read an `association_keys` field that
can be empty. The L3 claim is about a DIFFERENT population (AAPL/NVDA/MSFT/JPM/TSLA are not among
the 36 or the 60 UNRESOLVED, at either vintage checked). Recorded verbatim per the refusal clause:
the instrument ran exactly as written and printed 0; the mismatch with the L3 framing is a surprise
row, not a repair of the instrument.

## Controls

**Mutant (on this cell's own classification logic, the one piece of decision code it wrote):**
positive control exercises the five branches the classifier names in check order (ledger ABSENT ->
UNMEASURED; links>0 -> COVERED; no links but ledger articles/links>0 -> STORED-NOT-KEYED; no links/
articles but a job ran -> JOBBED-NOTHING-STORED; nothing -> NEVER-JOBBED) -- all five pass. The
mutant conflates "fetched" (ledger articles>0) with "COVERED" even when the pool holds 0 links for
the name -- exactly the ingestion/association confusion this task order exists to separate. On the
association-gap input (`MEASURED, 0 links, 5 articles, 5 ledger-links, 3 jobs`) the unmutated
classifier returns `STORED-NOT-KEYED`; the mutant returns `COVERED`. FIRED-AS-EXPECTED (diverged).

**Determinism:** the full build (AC1 pool listing, AC2 crosswalk join, AC3 ledger read, AC4 config/
universe, AC5 classification) run twice in sequence against the SETTLED pool (after the vintage race
above stopped moving): both runs produce byte-identical JSON records (excluding `measured_at`) --
population 36, classes {COVERED:3, NEVER-JOBBED:33, others 0}, validation_names identical. STABLE.
Separately documented: the SAME instrument run once BEFORE the 09-19 vintage landed and once AFTER
gave DIFFERENT answers (33 vs 36) with no code change -- that is not this cell's code being
nondeterministic, it is the live pool's unpinned "latest" pointer moving during the session, filed as
surprise row S2 rather than marked as a code defect.
