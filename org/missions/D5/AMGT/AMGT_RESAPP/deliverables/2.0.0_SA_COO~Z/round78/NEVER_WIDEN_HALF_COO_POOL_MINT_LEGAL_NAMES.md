# AMGT_RESAPP round 78 -- issuer act 1, the pool mint that carries the legal names: never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-07 ~17:2xZ

**The act:** ONE command by this seat, in the shared tree at CLOUD HEAD (which holds `AMGT-bb-7`, merged @5b498e903a):
`python -m lib.research.identity.crosswalk --as-of 2026-10-07 --write-pool` (no `--retire`). No vendor call: the names come from
stored objects (`universe/v1/*` and each record's own `identity.name`).

## What moves, measured by the dry run of the same command at 17:1xZ (`--dry-run`, exit 0) and `r78_bb7.py --crit AC3`

- **Keys:** 243 built, 243 served; 0 only-built, 0 only-served.
- **Existing fields:** 0 fields of 0 records differ from the served object.
- **Added:** every record gains `legal_name: {value, status, evidence}`; 211 of 243 carry a value, 32 read ABSENT (a folder name
  only: listed in the worker's report for bb-7). `denominators.with_legal_name` is added (211).
- **Also moves:** `research_universe.read_at` (a stamp).
- **Served effect:** name search (`GET /resolve?q=`) reads the pool through `load_crosswalk`, and the DEPLOYED function's
  `name_search.py` predates bb-7, so it does NOT read `legal_name` until the redeploy (bb-18). Until then the mint changes no
  served answer: the deployed code ignores the added field. `load_crosswalk` does not validate against the schema (read at
  `crosswalk.py:1199-1220`); only `write_pool` does (`:1452`).

## Both branches

- **A. `OK: uploaded ... records=243`.** Read-back by this seat against VersionId `Y6Tisihmmlm1lCHOO61ci9b726FLXBAI`: 243 keys,
  0 missing, 0 existing fields changed, 211 named; `resolve()` on AMD (control), ABNB and CSCO (negative control) unchanged; the
  deployed `/resolve?q=Lenovo` still lists `992_HK_Equity`.
- **B. the build or the schema refuses:** nothing is put (validation runs before the put). Reported, not retried.
- **C. the read-back shows any existing field moved, or a count other than 243:** a wrong object. Rollback the same hour.

## The hazard this act creates, measured (no store write)

**A mint run from code older than bb-7 DROPS the names and says nothing.** Measured in memory in a worktree whose
`crosswalk.py` predates bb-7 (`C:/tmp/r78-290`, file last changed @281015b156): with the new document planted as the served pool,
the old code's `--dry-run` build exits 0 with 243 records, **0 of 243 carrying `legal_name`**, and the old schema ACCEPTS it. So
the next pool write by any seat on an older checkout reverts the field with no error.
- Writers of the pool key (NEVER-1), N = 2 rules: `crosswalk.main --write-pool` and `add_security --write-pool` (both now pass
  `legal_names`, `add_security.py:374`). Callers that can run an older copy: AMGT_CORPUS's scheduled induction step, which
  `2.0.0_SA_COO~X` states is pinned to `662cd2b11d` (msg 31085), and any laptop-side run. Whether the pinned step mints on a
  given day was not measured; today it read `pool_puts 0` (round-77 record).
- **Condition this half asks the CTO to rule:** either the pinned CORPUS task is re-pinned to a commit that holds bb-7 before
  its next fire, or the names are accepted as best-effort until it is. The reverse-direction control exists: after any mint,
  `r78_bb7.py --crit AC1` reads how many served records carry the name.
- Not measured: that `--dry-run` takes the served document through the same union as `--write-pool` (its docstring says it
  builds "exactly as --write-pool would").

## The base, read at signing

| object | value |
|---|---|
| served pool | `crosswalk/v1/2026-10-07.json`, VersionId `Y6Tisihmmlm1lCHOO61ci9b726FLXBAI`, 748,500 B, 243 records, LastModified 13:22:15Z; one older version `1b0PNH1y...` |
| same-day writers since 13:22Z | none by the version list (2 versions) |

## Rollback per key

- **Pool:** copy-object of VersionId `Y6Tisihmmlm1lCHOO61ci9b726FLXBAI` onto the same key (versioned bucket; no delete). Not exercised.
- Nothing else is written: no registration row, no bronze object, no repo file.

## Not covered

The redeploy that makes name search read the names (bb-18); a true legal name for the 32 folder-only records (a Bloomberg read
each, Andrew's word); `build_universe.py:799`, which writes the folder as `name` and would null a holdings name at the next
universe build (a candidate cell, named in `GROUP_E_NOTES.md`).

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-07 ~17:2xZ. The CTO half is owed by `1.0.0_SA_CTO~Z`. The mint does not run before it.
