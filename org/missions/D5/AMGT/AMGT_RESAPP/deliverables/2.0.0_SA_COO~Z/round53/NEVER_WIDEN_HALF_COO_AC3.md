# AMGT_RESAPP round 53 -- `AMGT-ac-3` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-09-30 ~14:2xZ

**The act (ONE, CTO round-52 ruling 4; scope per CTO msg 27160):** leg (a) COPY the 40 raw-slash objects in
`round53/SLASH_OBJECTS.json` to their encoded keys (raw KEPT); THEN leg (b) redeploy `opal-amgt-scoped-api` from a checkout at the PIN.
Executor `0.7.0_AE_CloudOps~A`, order `task-orders/AMGT_RESAPP.TO-AMGT-ac-3.the-slash-key-window.md` (AMENDMENT 1: 40).

**THE BUILD COMMIT IS PINNED: CLOUD `cd70547173`.** Build from a checkout at the pin, never HEAD; any other commit is limb 1.

**The base, read live at signing:** CodeSha256 `nKWCfQRQ3/lL6cJxgYG3dZr0tcVdOBheeMMNaoWQE+w=` (ab-6, 11:43:22Z). Re-read immediately before
leg (a); a moved base is a STOP and a re-sign.

## THE READER CENSUS (CTO msg 27160 condition; msg 27175): 0 raw-path readers for the 40

- **derived/model_block (12), peers (14), packs (2), posture (2):** routed by CORPUS z-4 (`8d9adec9f4`; supply s.1 names each writer/reader).
- **scores (4):** writer `run_scores.py:228` builds `scores/v1/<slash_safe_key(key)>/...`; the adapter reads through
  `read_pool_object(SCORES_PREFIX, key)`, whose base is `<prefix><crosswalk.slash_safe_key(name)>/` (`scoped_amgt.py:1348`, `:3055`).
- **filings (2):** `fetch.pool_key` builds `filings/v1/<slash_safe_key(key)>/...` since AMGT-ac-4 (`f044cdd240`, drained `63c369c734`); its four
  callers (analyze.py :1345, :1470, :1636; batch.py :478) inherit it. Measured: `pool_key('BP/_LN_Equity', None, 'source')` ->
  `filings/v1/BP-SLASH-_LN_Equity/UNRESOLVED-SOURCE.source.json`.
- **raw/bloomberg (4):** no current reader (the adapter's own note at `scoped_amgt.py:3605`; build_view moved off raw/bloomberg, M1).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

| act | what it MAY touch | rollback |
|---|---|---|
| leg (a): 40 CopyObject | the 40 `encoded_key`s in SLASH_OBJECTS.json, each ABSENT at signing (COO~X's supply: 0 encoded destinations exist); the 40 raw objects are READ only and KEPT | none needed for safety: the encoded copies are byte-equal and inert to the prior code (which reads raw keys); removing them would be an S3 delete, Andrew's to confirm, and is NOT part of any rollback |
| leg (b): ONE artifact upload + ONE safe-apply | the function's CODE only (no IAM, no env, no prefix) | re-apply the prior VersionId the executor records live; with the raw objects kept, the prior code reads exactly what it read before |

## THE CLOSURE -- the build-only CONTENT DIFF at the pin, against `nKWCfQRQ`

`--build-only` at `cd70547173`: **files 344, IDENTICAL 336, CHANGED 8, ADDED 0, REMOVED 0.** Attributed by `git log a1a70e00eb..cd70547173`:

| file | commits | class |
|---|---|---|
| `lib/research/api/scoped_amgt.py` | CORPUS z-4 `8d9adec9f4`; RESAPP ac-4 `f044cdd240` | MOVING: pool reads through slash_safe_key (identity for a slash-free key); ac-4 is a docstring |
| `lib/research/identity/crosswalk.py`, `lib/research/freshness/build_view.py`, `lib/research/ledger/ledger.py` | CORPUS z-4 `8d9adec9f4` | MOVING only for slash keys (BP/_LN, NG/_LN): paths through slash_safe_key |
| `lib/research/harvest/timeline_api.py`, `lib/research/harvest/publication_gold.py` | HARVST q-5 `91b74a9047` | the NAMED rider (CTO msgs 27123, 27145): `/timeline` series entries gain `publishers_found_codes` (null for parts written before the column) |
| `lib/research/metrics/chatter_axis.py` (+325/-9), `lib/research/metrics/generation_writer.py` (+73/-1) | HARVST q-4 `88f94719ac`, aa-4 `3dd875936f` / `fd783e5e55` | **UNNAMED riders** (C-HV-RANK-DECLARED-SET; the declared publisher set derived from ENABLED_PUBLISHERS). Their request-path reachability is the CTO's to rule, as for zz-8's riders |

## EXPECTED OUTCOME (both branches)

- **BP/_LN_Equity and NG/_LN_Equity** read the same data at the encoded keys after the act as at the raw keys before: overlay / peers /
  thesis bodies byte-equal (AC3, the executor's pre/post capture).
- **`/timeline`** series entries carry `publishers_found_codes` (AC2).
- **Every other name:** unchanged (slash_safe_key is the identity on a slash-free key), apart from any served move the CTO finds reachable in
  the unnamed HARVST riders.

## THE LANE STOPS on any of seven limbs

1. The build is not at `cd70547173`, or the base moved.
2. The build's CONTENT-DIFF at the pin names a file beyond the eight above.
3. The plan moves anything beyond the function's code.
4. Any encoded destination EXISTS before its copy with different bytes, or a raw object's sha256 differs from SLASH_OBJECTS.json.
5. Leg (b) starts before leg (a)'s AC1 reads 40 of 40.
6. The served `/print` pdf OUTPUT or `/timeline` OUTPUT (beyond the added `publishers_found_codes` key) moves on AMD, BA, GOOGL, 1299 HK.
7. A lead-list row's rank, score, order, name or places_moved moves against the pre-apply capture of the same generation.

## THE FALSIFIERS

ac-3 AC1 (`ac_3_copies.py`, 40), AC2 (`--what codes`), AC4 (`--what code`) FAIL at the base; AC3 (`--what bpng`) is the executor's pre/post
body control. Any criterion failing after the act is the ROLLBACK trigger (code only, per the table).

Signed: `2.0.0_SA_COO~Z`, 2026-09-30.
