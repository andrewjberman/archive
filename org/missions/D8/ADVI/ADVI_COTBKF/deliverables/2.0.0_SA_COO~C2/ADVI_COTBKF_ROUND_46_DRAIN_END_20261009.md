# L8 drain end -- ADVI_COTBKF round 46

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~15:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB46at1-AC2)

Round 46 was cut as one issuance @7de6f36196 on `1.0.0_SA_CTO~DELL2` ADDENDUM 19 @47529c9d9e (msg 3547). It was spawned after round
45's drain, because both rounds edit the same census file.

| order | item | worker | state |
|---|---|---|---|
| CB-at-1 | the cot price writer resolves every repo-file input beside itself first, then at the repo root; records the resolution in its output's parquet metadata; the census prints each path | ~73 | complete @8bd569d91e (test alone first, 14a6fd3343), drained @5878ac20bc |

## The real runs, by the issuer

```
pytest data/cot/scripts/gold/tests: 43 passed
deployed mirror today: code/gold/lib/ticker_overrides.py present (VersionId .t5WA_bRvThzpfzz.MiBGPgPbQluupEy, 65,983 B)
```

The worker's run also gave the silver suite 749 passed, 11 skipped (no-split-literals test green). The new test failed 4/4 at the base
with `ModuleNotFoundError: lib.ticker_overrides`, and gives 4 passed now.

## What the round delivered

- **One resolver, `resolve_repo_file`, covers every repo-file input.** It tries beside the module first, then the repo path.
  - The table goes into the output parquet's schema metadata under `opal_input_resolution`, with no other schema change.
  - The census (`--source-firm-only`) prints `INPUT name=.. role=.. path=.. how=.. firm=..` per key. A key without the metadata prints
    `INPUT-RESOLUTION absent` and counts as NOT-CLEAN; today's 38 keys do.
- **The repo-file inputs found:**
  - `scopes.json` (registry): beside-only.
  - `ticker_overrides` (config): repo path `data/cot/scripts/gold/lib/ticker_overrides.py`.
  - The writer reads no other repo file.

**Rows (all INERT), each a fact the redeploy cell must carry:**
- **W73-S1:** the base writer's "repo root" (`parents[3]`) was actually `data/`, so its repo-file firm stamp could never have resolved.
  Fixed.
- **W73-S2:** `scopes.json` stays beside-only, because round 42's test (h) forbids a repo registry path in the writer. So IN THE REPO
  every firm reads `absent`. A repo-root fallback for the registry needs the CTO to lift test (h).
- **W73-S3:** an unresolved `ticker_overrides` now degrades to EMPTY overrides plus a WARN, where the base raised an import error. Its
  757 overrides and 1 correction would be dropped silently.
  - **Issuer measurement:** the deployed mirror carries it at `code/gold/lib/ticker_overrides.py`, but the new resolver looks for
    `ticker_overrides.py` BESIDE the writer (`code/gold/ticker_overrides.py`).
  - **The redeploy must ship `ticker_overrides.py` beside the writer** (registry first, per ADDENDUM 18), or the overrides silently
    vanish in production. This is carried to that cell's pair, not to this round.

**ARMED:** 0.

**Round-close check:** REFUSED until CB46at1-AC2 is graded.

**Next:**
- Round 48's sweep (~75) is spawned on this drain.
- ONE writer redeploy cell (rounds 46 and 48 together, registry first, `ticker_overrides.py` beside) is cut when round 48 drains.
