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

---

# THE ACT RAN (2026-10-07 13:15:47Z) -- BRANCH A: `OK: uploaded`, 242 records; C2 read (a); the act stands

Everything above was written before the put. C1 is answered above (branch a). This section is the act.

## C3 -- timing

`2.0.0_SA_COO~X` reported the 13:00Z AMGT_CORPUS fire READ (msg 30936, 13:14Z: `already_current 0 pulled 96 rc 0`, ended 13:13Z,
the induction step `pool_puts 0`), on its statement @bcffc028d5 that the fire reads the pool crosswalk. The put ran after that
read. `2.0.0_SA_COO~X` was told the time first (this seat's msg at 13:15:05Z).

## The base, re-read at 13:15:22Z, immediately before

6 keys under `crosswalk/v1/`, newest `2026-09-29.json`, ONE version `cFEovcK7Oye9K7PFrckMAbELVJW_xj02` (599,016 B);
`2026-10-07.json` absent; `universe/v1/` 3 keys, newest `2026-10-06.json`; `registrations.json` 71 rows; `lib/research/identity`
clean in the shared tree at fde4a80cc5.

## The put

`python -m lib.research.identity.crosswalk --as-of 2026-10-07 --write-pool`, started 13:15:47Z, rc 0, done 13:15:49Z:
`OK: uploaded s3://opal-data-harvest/crosswalk/v1/2026-10-07.json ContentLength=745570 document-sha256=4c965620...c0efc5 schema-version=1 records=242 MEASURED=242 UNRESOLVED=0`

## Read-back of the WRITTEN object (not the run's own line)

| read | value | predicted in the read @2568bc92a2 |
|---|---|---|
| object | 745,570 B, **VersionId `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib`**, LastModified 13:15:52Z, metadata sha matches the run's | -- |
| records | 242 | 242 |
| added keys | `BE_US_Equity`, `DG_US_Equity`, `ED_US_Equity`, `GEV_US_Equity`, `MRNA_US_Equity` | the same five |
| served keys missing | 0 | 0 |
| fields changed on the 237 | `provenance` 231, `source_row` 191, `raw_identifier` 158; no other field | the same three counts |
| `raw_identifier` pattern (old = new + " Equity") | 158 of 158 | 158 of 158 |
| `source_row.folder` changes | 0 | 0 |
| keys under the prefix | 7, newest `crosswalk/v1/2026-10-07.json` | -- |

Every number equals the prediction. The object is the one the pair signed.

## C2 -- the served read through the live route, before and after (same script, same name)

`POOL_REMINT_C2_BEFORE_20261007.json` (12:32:47Z, pool 2026-09-29, 237) and `POOL_REMINT_C2_AFTER_20261007.json` (13:16:19Z,
pool 2026-10-07, 242), by `checks/r77_pool_remint_c2_read.py` on `2317_TT_Equity`:

| read | before | after |
|---|---|---|
| `/overlay` status | 200 | 200 |
| peer identities (key, resolution), 13 | -- | the SAME list, 13 of 13 |
| the peers block, sha256 | `c10b919f...` | EQUAL |
| `resolve("2602335D_US_Equity")`, `MSFT_US_Equity`, `PLTR_US_Equity` | MEASURED, `<root> US Equity` | MEASURED, `<root> US` |
| `resolve("BE_US_Equity")`, `GEV_US_Equity` | UNRESOLVED | **MEASURED**, `<root> US Equity` |
| control `AMD_US_Equity` | MEASURED, `AMD US Equity` | MEASURED, `AMD US` |
| negative control `CSCO_US_Equity` (in neither object) | UNRESOLVED | UNRESOLVED |

Branch (a) of C2: 200 both times, the same peer keys and resolutions, and the only differences are the `raw_identifier` form and
the two added names becoming keyed. No peer that was keyed is now unkeyed.

**One limit, stated:** the served peers block is byte-EQUAL, so the deployed route did not show even the `raw_identifier` change
on this name's peers. Either that block is built from a stored peer set, or a warm container still holds the earlier pool; this
read does not say which, and a cold start was not forced. The pool-side `resolve()` reads are from this seat's process, on the new
object. The peers block of a name that has one of the five added names as a peer was not read (no covered name was searched for
one).

## Rollback target for the NEXT same-day put (ba-23)

`crosswalk/v1/2026-10-07.json` VersionId `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib` is the object to restore by copy-object if ba-23's put
is wrong. The 2026-09-29 object is untouched (one version, `cFEovcK7...`).
