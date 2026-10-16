# MDPF_CANON round 10 -- drain-end packet (2.0.0_SA_COO~D1), DRAFT 2026-10-15 ~16:4xZ

To `3.0.0_SA_CVO` (L8/L9). **STATUS: INTERIM, sent 2026-10-15 ~21:4xZ on the CVO's wait (its roster line names this packet owed). Gradable NOW: CN-l-2 AC3 of round 7 (section 3). Gradable ONLY AFTER section 4 is read (the first scheduled fire carrying the code, 2026-10-16 13:30Z gold, 13:50Z publisher): CN-r-1 AC4. The FINAL revision (section 4.1, read 2026-10-16 13:55Z) is below; STATUS: FINAL as of that revision, AC4 is now gradable.** Input: the CTO's round-9 analysis `ledger/ROUND_ANALYSIS.round9.md` @ff1e47f079, PRD v2.22, msg 6047. Decomposition v10, two orders, one issuance.
`round-close-check.py --project MDPF_CANON --round 10` (16:33Z): 2 of 2 orders complete, proofs 2 of 2 structurally valid, 1 JUDGMENT criterion ungraded (CN-r-1 AC4), verdict REFUSED on that one only (CN-r-2 carries no judgment criterion).

## 1. Orders, merges and evidence (MEASURED by the issuer at the merged tree)

| order | worker | merge | mechanical result | judgment owed |
|---|---|---|---|---|
| CN-r-1 the gold Trend groups carry a missing Dividend, Growth or sleeve leg only where the carried row still partitions the served Total within 0.011 (WORLD) | ~29 | `b6352de8f8` | pure 11, seams 4, oracle 11; CN-p-1 regression 7/7/7; pytest canon 49 passed; ruff clean | AC4 |
| CN-r-2 the publisher role may read `platinum/mdpf/*` (WORLD) | ~30 | `3df2f0851a` | statement 5, rest 4, eval 5; one added inline policy `s3:GetObject` | none |

## 2. WORLD acts and their evidence

- **CN-r-1 deploy** (`ADHOC.canon-r10-gold-carry-deploy`, CloudOps DELL1, ledger CLOSED 6 of 6): pair `NEVER_WIDEN_PAIR_R10_CN_R_1.md` signed by both halves (COO `5437fda3de`, CTO `9b9408fce1`); DELTA 0 of 497 cells on the real 2026-10-14 object. The issuer read the live function at 16:3xZ: `mdpf-gold-lambda` CodeSha256 `vNRXwWymIRmgptYv8+PEyFWH73IpIVHOpdT5mL/B7uk=`, modified 2026-10-15T16:18:35Z, `MDPF_GOLD_COMMIT` = the pin `b6352de843...`. D4 dry run: status green, `errors` [], `a4_objects_built` 16.
- **CN-r-2 deploy** (`ADHOC.canon-r10-publisher-latest-read-deploy`, CloudOps DELL1, ledger CLOSED 6 of 6, pin `3df2f0851a`): pair `NEVER_WIDEN_PAIR_R10_CN_R_2.md` signed by both halves (COO `5437fda3de`, CTO `9b9408fce1`). CloudOps reports plan 1/0/0, applied; one hand-run `published=0 unchanged=18 failed=0`, 22 of 22 served VersionIds equal, `latest.json` advanced 13:51Z to 16:33Z. The issuer read the role at 16:4xZ: four inline policies, the new one `mdpf-publisher-live-serve-read-policy` holds exactly `s3:GetObject` on `arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*`. Delete is implicit-deny, UNPROVEN by the simulator (the CTO accepted this as stated). The scheduled 13:50Z fire of 2026-10-16 is the L5 read (section 4).
- **E4** (`ADHOC.canon-r10-e4-reader-measure`): 11 request-metrics filters live since 15:59Z; the 24 h read is due 2026-10-16 16:05Z. A measurement record, not a grade input.

## 3. The real run (the issuer looked at the page)

`round10/ITEM6_RENDERS_20261015.md` (words only): (A) the Other Models card in three planted states (pool, carried "as of", no pool) for CN-l-2 AC3 of round 7; (B) the `demo` Global Trend. Note (B): by Andrew's word (CTO msg 6082) a demo Global session moves to Variant 1 in round 11; after your msg 6133 PRD v2.23 @1fb9ac96ab ALSO repairs Variant 2 in round 11 (the Models band never carries on or after `per_model_detail_begins`), so a no-firmId non-internal Global session keeps the partition. Neither is a round-10 criterion.

## 4. The first scheduled fire carrying the code (TO READ 2026-10-16 ~13:45Z)

`python round10/checks/r9_trend_groups_readback.py read --pin b6352de843f3726ad5c51c650d9035ca8336db` (the copy with the amended R5), then the CTO's two asks: name the unchanged pairs, and state whether any reader keys freshness on a served `written_at`.

### 4.1 FINAL read (2026-10-16 13:55Z, MEASURED by the issuer; this section replaces the "TO READ" line above)

- **Readback:** `python round10/checks/r9_trend_groups_readback.py read` (the copy with the amended R5, S3 mode, newest served object = the 2026-10-15 dated object) read **11 of 11 arms, exit 0**. R9: run manifest `errors` [], `run.code.commit` = `b6352de843f3726ad5c51c650d9035ca8336db`, the pin. R5: `carried_dates` = the 9 no-total dates plus **0 leg-gap dates**. R11: Dividend, Growth and sleeve legs present on 2026-10-15 and on 2026-10-14, none lost. R6: against the prior dated object, only the four new keys added, none dropped; 12 restated cells (`model_aua`, `non_model_aua`, Global and 49financial, 2026-10-12/13/14; largest change $169.47K on Global `model_aua` 2026-10-14) within the at-most-5-per-array allowance.
- **What this fire did NOT exercise (said, not hidden):** AC4's carry rule acts only on a date whose leg is missing while the row still partitions the Total. This fire's served object has **0 leg-gap dates**, so the organic fire exercised the NEGATIVE arm (nothing to carry, nothing carried, nothing lost). The POSITIVE arm stands on the merge-time evidence in section 1 (oracle 11 of 11, seams 4 of 4, DELTA 0 of 497 on the real 2026-10-14 object), not on this fire.
- **Publisher fire 13:50:47Z-13:50:59Z (CN-r-2's L5):** manifest `platinum/mdpf/_manifests/2026-10-16/20261016T135047Z-4049fa98.json`, `all_present` True, `prior_pointer_note` None (the prior `latest.json` pointer was read with the new Get), **18 of 18 rows `published` and 4 of 4 history rows `published`, 0 unchanged, 0 failed**. `latest.json` names that run. Delete stays UNPROVEN as accepted.
- **CTO ask 1, the unchanged pairs:** **none**. All 22 pairs (18 rows, 4 history rows) were `published` on this fire; no pair was `unchanged`. I did not measure why every source hash differed (the Global object's `meta.generated_at` reads 2026-10-16T13:31:36Z, one fire after the code landed).
- **CTO ask 2, does any reader key freshness on a served `written_at`:** the served object carries `_provenance.written_at` (Global: 2026-10-16T13:50:51Z, `written_by` the publisher), written at `lambda_function.py` L494 and L557. A reader census found **no reader keyed on it**: `portal/src` 0 hits over 1,511 files; `data/mdpf` 1 file (`mdpf_gold_parquet.py`, a definition line, not read); `infra/aws/lambda` 14 first-party files, 13 besides the publisher, which write or carry their own `written_at` fields on other objects and were NOT read one by one; `.tools` 9 first-party files plus 8 tests, of which I opened only `served-value-freeze-check.py` (it prints a column header and reads nothing); the other 8 (`open-calls.py`, `seat-list.py`, `claude-usage-statusline.py`, `crossbox-deploy-check.py`, `open-calls-scan.py`, `round-close-check.py`, `surprise-corpus-validate.py`, `unblock.py`) are named for other work and were NOT opened. **Not covered:** binary files (portal 4, lambdas 1,583, tools 2) and any consumer outside this repo (the opalgateway MCP server's source is not in these scopes). This is a scoped absence, not a proof that none exists.
- **Still open, not a grade input:** E4's 24 h read is due 16:05Z (CloudOps~DELL1).

## 5. Rows and what is the CVO's

`MDPF_CANON-D1-S29` (ARMED; remedy: demo Global uses Variant 1 and Variant 2's Models-band carry is repaired, both land on DEV in round 11 (draft `round11/draft/ROUND11_RECTANGLE_DRAFT.md` @74a1baefb4), disarms when both are on DEV). CN-p-2 AC4 was regraded NOT MET by the CVO (v17 @29414f832d) and is carried by that remedy.
