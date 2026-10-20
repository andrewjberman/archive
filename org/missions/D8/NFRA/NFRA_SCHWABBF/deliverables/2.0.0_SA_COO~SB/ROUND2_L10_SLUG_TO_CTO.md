# NFRA_SCHWABBF round 2 -- L10 slug to 1.0.0_SA_CTO

**From:** `2.0.0_SA_COO~SB`, 2026-10-20 ~16:1xZ. **Round:** 2 (the firm-form rework, bronze side; decomposition `decompositions/NFRA_SCHWABBF_DECOMP_R2.md`, issuance `67998aecd3`).
`round-close-check --round 2`: 8 orders, 8 complete, proofs 8 of 8 valid, `verdict=MAY-CLOSE`.

## 1. What round 2 delivered (merged on `box/laptop`; NOTHING deployed, applied or moved)

| cell | merge | what exists |
|---|---|---|
| BF-z-2 | `87d44e203b` | the five round-1 master-form files restored to pre-round bytes (you verified by md5) |
| BF-k-2 | `ef38445985` | the key function pair in the firm form, `MASTER_FIRM` (registry-equal), parsers, master-filtering listers; 550 tests |
| BF-m-2 | `ef38445985` | the move tool to the firm form; live read-only plan on all three masters (below) |
| BF-r-2 | `ef38445985` | the two hand-parsing readers on the shared listing; 17 tests |
| BF-w-2 | `8360d83c35` | the puller lands `schwab/49financial/bronze/...`, index and guard filter by master; 9 tests |
| BF-t-2 | `e26bd321b2` | the trace oracle in the firm form; reads the registry, not the key function; 18 tests |
| BF-c-2 | `3d7a1d172f` | the converter, the conversion manifest, the set-identity guard and the runtime census read the firm form (master from the file name); four vendored twins byte-equal; 21 + 9 tests |
| BF-i-2 | `95b30c139f` | Terraform text only: per-master firm-prefix write entries for the 49F box, the converter's read of both firm prefixes, two event rules; 12 tests |

Merged-tree checks: 640 passed (`data/canonical/schwab/tests`), 122 passed (five converter-side files), `py_compile` clean, twins equal. Release plan: `deliverables/2.0.0_SA_COO~SB/RELEASE_PLAN_R2_FIRM_FORM.md` (pair COO half signed, CTO half owed).
FWD-1 is still not exercised: the cutover acts R0-R8 need the CloudOps lane, a change entry and the pair.

## 2. Rows

Investigation file: 26 rows, 0 defects. The two ARMED rows were `NFRA_SCHWABBF-W5-S2` and `-S3` (the conversion manifest and the set-identity guard read the master and date by path position; under the firm form the guard would have counted ZERO bronze without saying so). Disarmed same turn by ruling `b1ee3d5514` and fix `ffffebb8d0` (merged `3d7a1d172f`); their closure is the CVO's. Rows that bind the cutover: W3-S3 (a legacy-only file makes the new puller's guard exit 6 until the copy, so the puller upload follows the verified copy), W5-S5 (the converter's build-commit pin in `silver.tf` moves at release), W2-S7 (the RPS date axis no longer lists the unprefixed partitions). CVO watermark: none (LOCAL class, no judgment criteria).

## 3. DECISION FOR YOU: 1,245 stored 0824 objects have no master in their name

The live plan (read-only, 2026-10-20 ~16:0xZ) listed 21,813 keys (the brief: 21,782) and plans 20,568. The remaining **1,245**, all under `schwab/08242234/bronze/`, are named `CRS{YYYYMMDD}.{FEED}` with no `08242234.` prefix and no `.zip` (example `schwab/08242234/bronze/acc/20240116/CRS20240116.ACC`), 241 dates from **2023-01-17** to 2024-07-05, about 120 per feed (rld, rps, tcf, uln, ult, upn, ...). 0833 and 0840 have none. Dates before Schwab's served floor (2023-10-17) cannot be re-pulled.

PRD C-KEYFORM tells masters apart by the file-name master prefix, and FWD-4 wants no second form. These objects fit neither. They fire no converter event (suffix is not `.zip`) and no reader reads them today (`monolith_bronze_key` cannot name them).

- **Option A (my recommendation):** move them UNCHANGED into the firm folder (`schwab/49financial/bronze/<feed>/date=D/CRS{d8}.{FEED}`) and amend C-KEYFORM to say an unprefixed legacy member in that folder belongs to 0824, the only master that holds any. One form, nothing lost; readers still filter by prefix and so never see them, as today.
- **Option B:** leave them where they are and carve them out of FWD-4 ("every stored Schwab raw file"); the old prefix then survives R7 for them alone.
- **Option C:** rename them with the `08242234.` prefix on copy. That changes the vendor's name, which C-KEYFORM forbids, and they are not the vendor's `.zip` names to begin with.

I need your ruling before R4 (the release plan's second condition). Reply `A`, `B` or `C`. Either way a round-3 cell carries it (the move tool today counts them `unrecognized` and moves nothing).

## 4. Proposed round 3 (the enrichment list you analyse; a recommendation, not a cut)

R3-1 the ruling on the 1,245 (tool flag and C-KEYFORM line); R3-2 the `modules/opal_name` regeneration and the `secret_name` output (your msg 109913, its own Terraform cell); R3-3 retire-banners on the three dormant old-form writers; R3-4 FWD-2 (full backfill) and FWD-3 (held-days record) once the cutover is through; then the release acts. Silver, meta and `_ops` scope stays open at Andrew; the Alongside workstream is on its own lane.
