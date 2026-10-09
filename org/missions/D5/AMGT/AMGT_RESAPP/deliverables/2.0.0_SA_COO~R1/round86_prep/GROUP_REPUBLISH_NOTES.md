# AMGT_RESAPP round-86 PREP -- the crosswalk same-key republish with `research_universe` (CTO~DELL1 round-85 analysis R1)

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~14:2xZ. READ-ONLY: S3 read only, no write, no commit.

## 1. The research-folder "argument" is not a flag -- it is the device's research library

`crosswalk.main` has NO research-folder CLI flag. Every path (`--write-pool`, `--out`, `--dry-run`, `--disclosure`) calls
`_research_folders_for_disclosure()` (`lib/research/identity/crosswalk.py:1606`), which reads `lib.research.corpus.library.library_root()`
and `list_folders(root)`; ANY failure returns `(None, None)` silently and `build_crosswalk` then writes
`research_universe = {"absent": "no research_folders argument given ..."}` (`crosswalk.py:975-990`).

`library_root()` looks, in order, at env `OPAL_RESEARCH_LIBRARY_ROOT`, env `OneDriveCommercial` + `Shared - Documents\Asset
Management\Research`, then `~\OneDrive - Opal Capital\Shared - Documents\Asset Management\Research` (`lib/research/corpus/library.py:25-75`).

**Measured on dell1:** `LibraryAbsentError` -- no env var, and `C:\Users\Test\OneDrive - Opal Capital\...\Research` does not exist. So
every crosswalk build on dell1 publishes `research_universe` absent. That is why jj-4 (run on dell1) published it absent.
**2026-10-07.json was built on the laptop:** `research_universe.source` = `C:\Users\Opal Bloomberg\OneDrive - Opal Capital\Shared -
Documents\Asset Management\Research`, `folders` 97, `read_at` 2026-10-07T17:18:12Z.

**So the republish must run where the library is** (the laptop, or any box with the OneDrive Research folder synced), or with
`OPAL_RESEARCH_LIBRARY_ROOT` pointed at a synced copy of that folder. Copying 97 from 10-07 forward would be a stale read, not a
measurement -- the disclosure field is a live folder count with its own `read_at`. Before the put, `--disclosure` prints
`research_folders_live`, a free pre-check that the library is readable.

## 2. The same-key rewrite needs no code change

Row D1-W341-S2 said `--write-pool` is put-if-absent by date. The code says otherwise: `write_pool` (`crosswalk.py:1517-1600`) heads the
key and, when the existing object's `document-sha256` differs, puts with `IfMatch: <its ETag>` (an optimistic, versioned overwrite);
only a NEW key is put with `IfNoneMatch: *`. An identical document is not rewritten. So re-running
`python -m lib.research.identity.crosswalk --as-of 2026-10-09 --write-pool` on a box whose library reads re-writes TODAY's key as a new
version of `crosswalk/v1/2026-10-09.json` -- the CTO's "same-key rewrite" path -- with no new flag. The rollback is the same mechanism:
a re-put of the prior VersionId's bytes (the bucket is versioned); never a delete. The union-first carry (`_carry_served`) keeps every
served record.

## 3. Every top-level field, 2026-10-07.json vs 2026-10-09.json

| field | 10-07 | 10-09 | |
|---|---|---|---|
| `as_of` | 2026-10-07 | 2026-10-09 | expected change |
| `coverage_source`, `identity_universe`, `key_conventions`, `registrations_source`, `schema_version` | -- | -- | same |
| `records` | 243 | 243 | same count (C1) |
| `research_universe` | {source, read_at, folders: 97} | {absent: ...} | **the regression** |
| `denominators.research_folders_live` | 97 | MISSING | the regression's denominator |
| `denominators.with_issuer_cik` | MISSING | 204 | expected (jj-3) |
| `coverage_vintage.snapshot_stale_against_live` | true | MISSING | rides the library read (computed only when folders are known) |
| every other `denominators.*` / `coverage_vintage.*` key | -- | -- | same |

## 4. The widened check -- `round85_prep/checks/r85_crosswalk.py` C5 (C1-C4 unchanged)

`--reference <key>` turns on C5: every top-level field of the reference, and every key one level inside a top-level object, is in the
graded list with an equal value or named in `--admit` (both values printed); keys the graded list adds must be admitted too; and
`research_universe.folders >= 1`. Without `--reference`, C1-C4 grade exactly as before.

Dry-run on today's latest key (`--reference crosswalk/v1/2026-10-07.json --admit as_of,denominators.with_issuer_cik`):
`C5 ... 6 not admitted ['coverage_vintage.snapshot_stale_against_live', 'denominators.research_folders_live',
'research_universe.absent', 'research_universe.folders', 'research_universe.read_at', 'research_universe.source']; research_universe
folders None` -> `R85 CROSSWALK AC1: NO`. Positive control: 10-07 graded against itself -> C5 PASS (0 not admitted, folders 97).
A correct republish is admitted with `--admit as_of,denominators.with_issuer_cik,research_universe.read_at,research_universe.folders,
denominators.research_folders_live` only if the folder count changed; equal values need no admission.
