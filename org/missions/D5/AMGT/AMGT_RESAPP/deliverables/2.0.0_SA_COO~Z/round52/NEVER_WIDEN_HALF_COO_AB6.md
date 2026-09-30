# AMGT_RESAPP round 52 -- `AMGT-ab-6` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-09-30 ~08:3xZ

**The act (ONE, round-51 analysis items 1 + 6; CTO msg 27014):** redeploy `opal-amgt-scoped-api` carrying AMGT-ab-2 (every name's
`dossier_fields` block; `pack_shape` pass-through) and AMGT-ab-4 (comments/docstring only), plus the closure below; AND write ONE object,
`s3://opal-data-harvest/drafting/v1/ASML_NA_Equity.json`, with AMGT-ab-1's committed splice
(`python -m lib.research.filings.drafting_build --splice-driver --only-keys ASML_NA_Equity --pre-act-dir <deliverables>/ab6-pre-act`,
dry run first). Executor `0.7.0_AE_CloudOps~A`, order `task-orders/AMGT_RESAPP.TO-AMGT-ab-6.the-one-build.md`.

**THE BUILD COMMIT IS PINNED: CLOUD `a1a70e00eb`** (an ancestor of HEAD at signing). The executor builds from a checkout at the pin, never
HEAD; any other commit is limb 1. The splice runs from the same checkout.

**The base, read live at signing:** CodeSha256 `zHpr7FhS+irmKofIuKNqTkQm2hj7x2fvS1rrX1ohkfQ=` (zz-8, 05:20:04Z). **Re-read immediately
before the build; a moved base is a STOP and a re-sign.**

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

| act | what it MAY touch | rollback |
|---|---|---|
| ONE artifact upload + ONE safe-apply | the function's CODE only (no IAM, no env, no prefix) | re-apply the prior VersionId the executor records live |
| ONE object write | `drafting/v1/ASML_NA_Equity.json` only; before-state measured: VersionId `xUdeA0xUdUyjs7DEEXriRS4JjWmtqfRs`, 12,941 bytes, sha256 `68995eb736aa83ff...`, LastModified 2026-09-17T15:35:17Z; bucket versioning Enabled (measured round 51) | copy VersionId `xUdeA0xU...` back over the key (a copy, not a delete) |

## THE CLOSURE -- the build-only CONTENT DIFF at the pin, against `zHpr7FhS`

`build-and-upload-scoped-amgt.sh --build-only` at `a1a70e00eb`: **files 344, IDENTICAL 342, CHANGED 2, ADDED 0, REMOVED 0.**

| file | commits since zz-8's pin `0bf907bee8` | class, measured |
|---|---|---|
| `lib/research/api/scoped_amgt.py` | ab-2 `58fdd2a18d`; ab-4 `319d5b9985`, `0de2bbe565` | MOVING: `_dossier_fields` (a no-dossier name serves the full block ABSENT with reasons; `pack_shape` passes through). ab-4 touches comments and one docstring only |
| `lib/research/corpus/dossier.py` | AMGT_CORPUS x-1 `597f0647ea` | ONE line, `METHOD_VERSION` `/4` -> `/5`. It moves `read_dossier`'s served PICK to the `/5` object for **95 of 95** names with a dossier; comparing every field of the `/4` and `/5` picks except the new `pack_shape`, **93 of 95 are identical** and 2 differ only in `model_rows` (8035_JP, 9433_JP), which the adapter never reads (`model_rows` has 0 occurrences in `scoped_amgt.py`). So the pick move changes no served value. `round52/checks/ab_6_dossier_pick.py` |

**Not packaged, measured:** `lib/research/filings/drafting_build.py` (ab-1) and `lib/research/filings/analyze.py` (ab-5) are absent from the
content diff -- they run executor-side only (the splice) and in the producer.

## EXPECTED OUTCOME, read from the landed rules at signing (both branches)

- **`/thesis` `dossier_fields`, every name with a dossier (95):** every existing field value UNCHANGED; `pack_shape` ADDED -- SERVED
  {value pdf|docx|mixed, basis} or ABSENT {reason: the dossier's absent text}.
- **`/thesis` for a name with NO dossier (6501_JP_Equity):** `dossier_fields` changes from {status READ_FAILED} to the full block, every
  field ABSENT with reason "no research dossier exists for this name". A broken read still serves READ_FAILED.
- **`/thesis` for ASML_NA_Equity:** after the splice, `thesis_driver_chart` reads SERVED, source `filing`, 3 points (the spliced driver's
  3 spans: [49888,49899], [49900,49911], [49912,49923]). Its drafted sections are UNCHANGED (the splice moves `thesis_driver` and adds
  `thesis_driver_provenance` {analysis_key, analysis_version_id}; nothing else). For every other name the chart is UNCHANGED.
- **Everything else served: UNCHANGED** -- `/lead-panel/*`, `/timeline`, `/timeline/day`, `/print`, management.

## THE LANE STOPS on any of seven limbs

1. The build is not at `a1a70e00eb`, or the base moved.
2. The build's CONTENT-DIFF at the pin names a CHANGED/ADDED/REMOVED file beyond the two above.
3. The plan moves anything beyond the function's code.
4. The splice's dry run names a moved key other than `thesis_driver` and `thesis_driver_provenance`, or the analysis accession differs,
   or the served validator refuses; or the live receipt names a key other than ASML's.
5. The served `/print` pdf OUTPUT or `/timeline` OUTPUT moves on AMD, BA, GOOGL, 1299 HK (captured before, byte-equal after; a timeline
   move is attributed against any AMGT_HARVST data write between the captures before it is a ROLLBACK).
6. A lead-list row's rank, score, order, name or places_moved moves against the pre-apply capture of the same generation.
7. ASML's served drafted sections (`read_drafted_sections`) differ before vs after the splice.

## THE FALSIFIERS

`ab-6` AC1 (`ab_2_dossier.py --plane served --what absent`), AC2 (`--what shape`), AC3 (`round51/checks/zz_8_served.py --what chart`),
AC4 (`ab_6_code.py`) -- each FAILS at the base (measured at the cut), each a read of the SERVED route (CTO round-51 ruling 5). Any
criterion failing after the act is the ROLLBACK trigger.

Signed: `2.0.0_SA_COO~Z`, 2026-09-30.
