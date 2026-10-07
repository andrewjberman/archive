# irpt-ycharts-generate release (IB-pr-357 + X-1): equality read and rider census -- ~P2's owed rows

**By:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~21:0xZ | **For:** the one pair (CTO ruling msg 1085). Deployer is `2.0.0_SA_COO~Y2`;
the draft is @ad75873357. **Read at:** dell2 CLOUD HEAD 49020c6afa.

## 1. A build at HEAD ships NONE of the fixes: four staged rows hold old blobs

`lambda-source-map.json` stages the four files that carry tonight's changes at old pins. `build-and-upload.sh` packages each
`staged_from` blob at its row's pin, never at HEAD.

| packaged member | repo path | staged pin | blob at pin | blob at HEAD | carries |
|---|---|---|---|---|---|
| served.py | _authz/served.py | 0642c9d004 | a9b14d7813cc | 7cc704129f91 | IB-pr-357 (the F1 fix) |
| generate_installed.py | reports/generate_installed.py | 3f29017cfc | f761837e870f | d878d10731f4 | IB-pr-358 (the reader on the upload door) |
| uploads.py | intake/uploads.py | 3f29017cfc | f88bdb902789 | 47f89e0b4660 | IB-yr-631 (the X-1 admit) |
| interactive_access.py | _scope/interactive_access.py | 3f29017cfc | bba07a3f4eeb | c28d9a74c9af | IB-pr-354 (the allowedFirmIds carry) |

`upload_resolution.py` is staged at 3f29017cfc, and that blob equals HEAD (b2edc1b17aff); it carries nothing.

**Consequence:** the ruling's premise ("any build of irpt-ycharts-generate ships both") does not hold at the bytes. The release needs
the four rows re-pinned, each with its sha256, in ONE source-map commit; that commit is the pin. The export release (IB-pr-349) hit
the same trap and was caught by the same census.

## 2. Rider census: what a re-pin of the four rows carries besides the named changes

`git log <pin>..HEAD -- <path>` per row:

| row | commits carried | named in the pair? |
|---|---|---|
| served.py | db8161f46e IB-pr-357; **cd9a61bb0c IB-pr-326** (the guarded path's enforcer_for refusals answer public_reason_for) | 357 yes; **326 is a RIDER** |
| generate_installed.py | d3b71b79c6 IB-pr-358 | yes |
| uploads.py | a241bfa396 IB-yr-631; **ee8c6e6d97 IB-pr-340 amendment 1** (uploads refusals InputAccessDenied / InputUnavailable) | 631 yes; **340 am. 1 is a RIDER** |
| interactive_access.py | c101699a71 IB-pr-354 | yes |

Both riders are drained and graded:
- **IB-pr-326:** on the wire it changes only a refusal's public reason code.
- **IB-pr-340 am. 1:** it names two upload refusals by class.

Neither widens access. The pair either names them or the re-pin excludes them (the latter is not clean: each shares its file with a
named change).

## 3. Census at HEAD, before any re-pin

`release-census.py irpt-ycharts-generate --pin HEAD`: built 100 members, live 114, `changed_members=20`.
- **Six members changed:** canonical_profile_reads.py, loaders.py, maintained_sources.py, publication_worker.py, publisher.py,
  served.py (the last at its pinned blob, which is still newer than live).
- **14 `fixtures/har/*` members REMOVED.** E-Y4 leg (1), "0 fixtures/har in the deployed zip", holds at HEAD.

The pair's census must be re-taken at the re-pin commit.

## 4. Equality read for the other functions that package the changed files (msg 1018 row (1))

- **served.py:** eight functions package it, each at its own staged pin: irpt-performance-adapter f9a00f732c, irpt-directory-search,
  irpt-export-render, irpt-holdings and irpt-49f-reporting-read-lambda d8d8e7d868, irpt-narrative f6c6b56f40, irpt-status 0642c9d004,
  irpt-ycharts-generate 0642c9d004. Only irpt-ycharts-generate's row is re-pinned by this release. The other seven keep their pinned
  blob, so this release changes none of them, and IB-pr-357 does not reach them.
- **interactive_access.py:** the census at HEAD f4307c366d showed it changed in none of irpt-status, irpt-export-render or
  irpt-performance-adapter.

## 5. Owed

- **The re-pin commit** (four rows, each sha256 verified equal to the HEAD blob), then this census re-taken at it.
- **The pair** names the two riders, IB-pr-326 and IB-pr-340 amendment 1.
