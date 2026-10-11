# LGIC_CANON -- round 5 drain end: FWD-5 run clean (2.0.0_SA_COO~B1, dell1, 2026-10-09)

**Issuance:** @dcea6794eb, on `ledger/ROUND_ANALYSIS.round5.md` (`1.0.0_SA_CTO~DELL1`, msg 3013) and its ADDENDUM 1 (msg 3029).
**Orders:** 3 of 3 complete, each re-proved by the issuer before its merge; slots torn down.

| cell | item | merge | the issuer's re-run |
|---|---|---|---|
| `CN-q-1` | R1: step 13 on today's tools; remaining RAISEs get registry rows | @59e4f31a3d | 183 wave names (184 rows minus the wave's 1 plant): `CENSUS: COMPLETE 175 judged + 0 carded + 8 ruled`, 0 RAISE; `PASS-R5-STEP13`. Registry diff: rows added only (`name_rulings.json` #119-#126) |
| `CN-q-2` | R2: portal paths derived from the scope | @21e9ac9480 | first pass: 1 derived, 7 carded to Andrew (the measurement that produced ADDENDUM 1); `PASS-R5-PATHS` |
| `CN-q-3` | PART A (ADDENDUM 1): core + `tenant.pages`; PART B: the FWD-5 run | @a923041120 | A: 49financial `derived=8 carded=0`; `--check` live `firms=4 pages=35 graded_firms=3 skipped_firms=1 stops=0 OK`, planted page STOPs; `PASS-R5-PATHS2`. B: `steps=16 units=17 reached=15 carded=2`; `PASS-R5-RUN` |

**Registry act by `4.0.0_SA_CRO`:** `tenant.pages` for the three client firms, `scopes.json` @a15fb36a4c (read from firmAccess.ts on portal
DEV and PROD, identical): 49financial `["/trade-submission"]`, inflection `[]`, cottonwood `["/attribution","/factor-tilts","/trade-submission"]`.

**Amendments (issuer's, each re-run before its commit):**
- CN-q-1 AMENDMENT 1 @4854282496: the wave's self-declared plant (R-0184, a fictional IAM role) leaves step 13's population, and its
  ruling row was removed. A registry row for a fictional name would write fiction into the estate registry.
- CN-q-3 AMENDMENT 1 @b1e26111f8: ADDENDUM 1's work, drafted as a new cell, was refused by the gate (one issuance per round) and
  folded into the unspawned CN-q-3 as PART A.
- CN-q-3 AMENDMENT 2 @5e9f957f39: the run arm counted 16 units while the order splits step 14 into 14a/14b (17) -- the issuer's
  defect (row S32). Row S31 ruled: `--check` grades client firms and prints `SKIP demo` (ADDENDUM 1 scope).

## The FWD-5 run (CN-q-3 PART B, `deliverables/0.9.0_WK_LGIC_CANON~1/CANON_RUN_R5.md` + `.json`)

On the `LGIC_LGCTFM` practice wave `20260918T011619Z-8db9eb1` (49financial), every step a READ or a pure call:

```
  checklist steps ............ 16   (17 units: step 14 split into 14a and 14b)
  REACHED .................... 15   (1-9, 11, 12, 13, 14a, 14b, 15)
  CARDED ...................... 2   (10, 16 -- both firm-bucket, owner ADVI_FIRMBKTS: the router repoint)
  reached + carded ........... 17   == units
  live_acts .................. []   routes hash 0de2f0f6def5ee0583c9637886a4fed6e7ccf763 before == after
```

- **Step 13 REACHED:** 0 unresolved on the wave's names; `census --all-roots` `completed=86 stopped=0`.
- **Step 14a REACHED:** `python lib/opal_portal_paths.py 49financial` derives all 8 pages from the core and `tenant.pages`, 0 carded,
  with no prompt. Checklist step 14's portal-paths sub-bullet and the INPUTS row read DERIVED (CN-q-2).
- **Step 14b REACHED by read:** the partner table exists and is ACTIVE; `grade` reads OUT-OF-PATTERN, the departure register entry
  X8 declares for exactly this table.
- **Carded only inside the carve-out:** steps 10 and 16 (the legacy tier-first platinum keys are still the served ones; the
  `address()` home key 404s until ADVI_FIRMBKTS's router repoint lands).

**Hygiene on the combined trunk:** `pytest lib/tests` 214 passed; `.tools/naming-gate.py --self-test` PASS; every r5 arm PASS.
`round-close-check --round 5`: orders 3, judgment 0, `verdict=MAY-CLOSE`.

## Rows for the round-5 analysis

- **D1-W2-S1:** a stored-file path's answer now sits in `name_rulings.json` (the census reads only that file by (name, type));
  two answers also exist in `key_rulings.json` and can drift. For the registry owner.
- **D1-W3-S30:** three places in the checklist still call the portal paths SOVEREIGN (the INPUTS count line, the step-14 trailer, the
  STOP list) -- outside CN-q-2's grant.
- **D1-W1-S33:** committed generated views lag the registry for other scopes; checklist Step 4 and Step 14 wording predates PART A.
- **D1-W1-S31** (ruled, demo skip) and **D1-W1-S32** (resolved by AMENDMENT 2).
