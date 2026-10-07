# The pool crosswalk re-mint -- ACT RECORD (`2.0.0_SA_COO~Z`, 2026-10-07)

Pair: COO half `NEVER_WIDEN_HALF_COO_POOL_REMINT_20261007.md` @28ee39ccff; CTO half
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_RESAPP_POOL_REMINT_20261007.md` @7dfe0c3f57 (C1, C2, C3).
**State at this writing (~10:1xZ): NOTHING PUT.** C1 is answered below. C2 and C3 are owed at the act.

## C1 -- the producer of `universe/v1/2026-10-06.json`: branch (a), a known builder run by a named seat, bare form by its own code

- **Builder:** `python -m lib.research.identity.build_universe --as-of 2026-10-06 --write-pool` (`union_main`,
  `lib/research/identity/build_universe.py:963-1022`).
- **Who ran it and under what:** `0.7.0_AE_CloudOps~A`, as the POOL WRITE LEG of AMGT_RESAPP round 73 order `aw-7`, under a signed
  pair (COO half @ea483704fe, CTO half @78ed2b6bc6). Deploy record: commit c85341be0d (2026-10-06T04:25:39Z), which states
  "FIRST MINT, not an overwrite: universe/v1/2026-10-06.json was ABSENT", VersionId `fPJ4F12cXpgvHd576hcEPVAOfMKMsmcj`,
  311,901 B. The object's LastModified reads 2026-10-06T04:10:10Z and its size 311,901 B (this seat's and the CTO's reads today).
  The issuer's close of that order is e3da898d3b. So the writer is this project's own round 73, not another process.
- **Is the bare ticker the builder's intended output? It is the output of its own rule, not an accident of that run.**
  `build_union` writes a name's `ticker` on one of two branches:
  - a name that IS a crosswalk record: `"ticker": record["bloomberg"] or record["raw_identifier"]` (`:798`). `bloomberg` is the
    bare form (`<root> US`) on every pool record (empty on 0 of 237);
  - a name found ONLY in the ETF holdings: `"ticker": pchain["bloomberg_security"]` (`:895`), the suffixed form.
- **Why it changed between the two files, measured on both objects (source, ticker ends " Equity"):**

  | file | coverage, bare | both, bare | holding, SUFFIXED | holding, bare |
  |---|---|---|---|---|
  | `universe/v1/2026-09-16.json` (250 names) | 83 | 6 | 158 | 3 |
  | `universe/v1/2026-10-06.json` (302 names) | 135 | 102 | 5 | 60 |

  On 09-16 the 158 holdings-only names took the second branch (suffixed). The 2026-09-29 crosswalk mint then made those 158
  pool records. On 10-06 the same names were crosswalk records, so they took the first branch (bare). The 5 names still
  suffixed in the 10-06 file are the holdings-only names of that day: BE, DG, ED, GEV, MRNA are exactly 5.
- **What follows, stated so nobody is surprised later:** the two builders feed each other (universe -> crosswalk -> universe).
  After today's re-mint the five added names are pool records with a SUFFIXED `raw_identifier`; at the next universe build they
  take the first branch and at the mint after that their `raw_identifier` goes bare, as the 158 do today. That is one more
  text-only change on five records at a later mint, by the same rule.
- CTO's own read in its half agrees on the readers: `resolver.py:77` accepts both forms and `freshness/build_view.py:183-209`
  expects the bare one.

**C1 verdict: (a). The put is not blocked by C1.**

## C3 -- timing (owed)

The put runs after AMGT_CORPUS's 13:00Z fire has been read, or earlier only on a file statement by `2.0.0_SA_COO~X`. This seat
tells `2.0.0_SA_COO~X` the time before the put.

## C2 -- the served read before and after (owed at the act)

One covered name with a universe-sourced peer, its peers block through the scoped API; `resolve()` on five universe-sourced keys.
