# CN_TREE_MDPF -- the pipeline tree both judges judge (LGIC_CANON round 1, cells CN-j-1 and CN-j-2)

Fixed at the L6 cut by 2.0.0_SA_COO~G (issuance base: CLOUD @10894fdad1). Every fact below is a
MEASUREMENT with its source and vintage. **No disposition, verdict or rule is stated in this file.**
Reaching those from the canon (`infra/logic/02_DOCTRINE.md`) is the exercise.

**The pipeline:** MDPF (Model Portfolios), the product pipeline that builds model-portfolio figures for
each firm it serves and for a global composite.

**Sources of the facts:**
- the conformance census rows as recorded in `infra/logic/06_CONFORMANCE_LEDGER.md` @c9048873d1
  (census vintage 2026-09-12/13); only the object counts, formats and dates are carried here;
- the live resource names of 2026-09-14 12:13:53 UTC, as `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`
  @3cc090827f section 9 cites them.

## 1. Planes (storage)

| # | bucket | prefix | tier | objects | formats | newest write |
|---|---|---|---|---|---|---|
| P1 | `opal-data-mdpf` | `mdpf/bronze/` | bronze | 830 | not measured | 2026-09-12 |
| P2 | `opal-data-mdpf` | `code/scripts/{bronze,silver,gold}` | (pipeline code) | 34 | code bundles | 2026-08-04 .. 2026-09-11 |
| P3 | `opal-data-mdpf` | `gold/` | gold | 0 (absent at 2026-09-13 02:48Z) | -- | -- |
| P4 | `opal-data-assets` | `gold/mdpf/` and `gold/mdpf_revamp/` (under a root `gold/` prefix) | gold | 502 | JSON | 2026-09-12 |
| P5 | `opal-data-assets` | `portal/gold/` | gold | 415 | 409 JSON, 6 other | 2026-09-12 |
| P6 | `opal-data-portal-v2` | `platinum/mdpf/{49financial,cottonwood,inflection}/` | platinum | 13 | JSON | 2026-09-12 |
| P7 | `opal-data-portal-v2` | `platinum/mdpf/global/` | platinum | if present (not counted) | JSON | -- |

**What the data is:**
- P6 holds one slice per firm, and each slice is attributable to that one firm.
- P7, and the `global/` slices of the gold above, are a cross-firm composite: aggregate counts, status and
  dates only, with no account identifiers.

## 2. A read outside the tree

- The pipeline reads a credential file, `opal-data-inf/orion/jwt/current.json` (the Orion JWT), from a legacy
  firm bucket.

## 3. Compute

Live at 2026-09-14 12:13:53 UTC:
- a LAMBDA named `mdpf-gold-lambda`;
- an EC2_INSTANCE named `mdpf-daily-runner`.

Which tier transition each of them runs is NOT stated here; the record does not measure it.

## 4. Ingestion

How MDPF's sources arrive (the mechanism) is not measured in this file beyond P1's bronze landing and the
credential read in section 2. Where the facts here do not decide an axis, `UNDETERMINED` is a legal verdict.

## 5. Register entries recorded against this tree

Verbatim from `infra/logic/06_CONFORMANCE_LEDGER.md` section 6 @c9048873d1. They are facts about this tree: the
departures someone declared and who acknowledged them.

| # | pipeline | axis | departure | why | acknowledged | kind | state |
|---|---|---|---|---|---|---|---|
| X1 | MDPF (Orion JWT) | A1 | reads `opal-data-inf/orion/jwt/current.json` | credential artifact, not data | Andrew via CTO~X relay 76365, 2026-08-27 | PERMANENT | **GRANTED** |
| X2 | MDPF `global/` | A2 | cross-firm composite gold in product bucket, platinum in portal-v2 | R7 composite branch -- basis written: aggregate counts/status/dates only, no account identifiers (`MDPF_TAXSMA_DATA_CONTRACT.json` `categories.wire_privacy`) | Andrew-direct 2026-09-15 ~14:4xZ, "RECS APPROVED" (card E2) | PERMANENT | **GRANTED** |
| X7 | MDPF 49financial `category-views.json` (incl. MDPF_TAXSMA's writes) | A2 | firm-attributable platinum stays at `opal-data-portal-v2/platinum/mdpf/49financial/`, not the firm bucket | the served route reads that key today; moving it is a migration (R19), writing both homes a dual write (R18) | Andrew-direct 2026-09-15 ~14:4xZ, "RECS APPROVED" (card E1) | CONDITIONAL -- expires when MDPF_CANON repoints `platinum/mdpf/{firm}/` | **GRANTED** |

No other register entry names MDPF.
