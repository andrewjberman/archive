# OPAL_ASSETS -- G5 convergence row-shape SPEC

**Author:** `0.8.0_AE_CloudComp` (sole lane, Andrew-direct) | **Date:** 2026-07-13
**For:** `2.0.0_SA_COO` (GO 040239Z: "spec the G5 convergence row-shape NOW") | **CC (align/gate):** `0.7.0_AE_CloudOps~A` (base table+emitter owner), `1.0.0_SA_CTO~B` (schema arch-gate), `0.4.0_DS_ClientPlatform` (P0-B)
**Builds on:** the CTO-base schema design (`org/tier1_exec/1.0.0_SA_CTO/deliverables/OPAL_ASSETS_P0A_SCHEMA_DESIGN_20260713.md`, authored under my serial during the identity mix-up, disclosed as CTO input) + `~A`'s G6 contract (`be910e7b7`) + my G4 fold design (`c509e1c9d`) + DS's 3 notes (adopted).

> **archetype:** IMPLEMENT (forward-design) | **Scope guard:** the both-masters custody dimension is **POST-G2** -- it needs `~A`'s `08335338` backfill (executing now, ~6,932 files, ~3h) + the new CBUGL parser. This spec designs the SHAPE so P2 lands as a **value change, never a schema migration.**

---

## 0. What G5 is

G5 = **the convergence**: the ONE daily DynamoDB bucket becomes the single honest source per cohort per day, carrying (a) the base 14-cohort freshness stamp (`~A`'s table), (b) the folded per-partner ETF **ownership** (G4), and (c) the **custody dimension** (both Schwab masters, POST-G2). This spec locks the row shape so the interim (today) and the full (post-G2, post-served-cutover) states are the **same schema at different values** -- the never-widen guarantee at the row level.

## 1. The converged row (superset of the base row -- additive only)

Base row (from the CTO-base design, `~A`'s table): `{cohort(PK), bucket_date(SK), value, as_of, state, staleness_trading_days, source_masters(L), partial?, ownership?, provenance...}`. G5 adds/finalizes:

| Attribute | Interim (today) | Full (post-G2) | Migration? |
|---|---|---|---|
| `source_masters` (L of S) | `["08242234"]` (49F), `[]`+`expected_masters` (cohort-8), `[]` (ETFs) | cohort-8 -> `["08335338","08242234"]`; 49F ownership entries gain `08335338` | **NONE** -- list grows, shape fixed |
| `ownership` (L of M `{firm_id, held, ownership_pct, source_masters(L), as_of, state, partial?}`) | 49F entry `partial="08242234-only"`, `state=rolled_forward@06-24`; inflection `fresh@own` | 49F `partial` DROPS (attr absent), `held` = both-masters account-deduped | **NONE** -- `partial` removal + `held` revalue |
| `custody` (M, cohort-8 only: `{present_masters(L), missing_masters(L), deduped_by_account(bool)}`) | `{present:["08242234"], missing:["08335338"], deduped:false}` -> cohort-8 `state=incomplete/99` | `{present:["08335338","08242234"], missing:[], deduped:true}` -> cohort-8 `state` from real vintage | **NONE** -- values flip, keys fixed |

**Load-bearing property:** every interim->full change above is a VALUE change on a FIXED key set. No `aws_dynamodb_table` attribute change, no GSI change, no item-count change. This is the never-widen forward-compat guarantee -- P2 does not migrate the table, it repopulates values. (CTO~B's forward-compat criterion, satisfied structurally.)

## 2. `as_of` -- the section-3d invariant, carried EVERYWHERE

Every `as_of` in the converged row -- the top-level cohort `as_of` AND each `ownership[].as_of` AND (post-G2) the custody present/missing sides -- is that element's **OWN-field** vintage, **never a cross-partner/cross-master min**. A stale ownership entry ages on its own `source_as_of` (49F: 06-24); a fresh one (inflection: 07-10) sits beside it with its own. The row NEVER smears a single as_of across heterogeneous-vintage sub-parts. (PRD 3d; `~A`'s G6 contract; the mdpf per-partner gate discipline, verbatim.)

## 3. Cohort-8 (`49f_schwab_custody`) -- the convergence's headline

- **Interim (now):** `state=incomplete`, `staleness=99`, `value` ABSENT (no fake number), `custody.missing_masters=["08335338"]`. The row is HONEST-about-the-gap and self-describes what it's waiting on. **No sovereign read to produce it** -- absence is the truth, stamped explicitly (DS note 1: it is a real row, not an omission).
- **Post-G2 (both-masters):** when `~A`'s `08335338` CBUGL pull + parser land the Schwab BD positions, cohort-8's custody value = `08335338` CBUGL positions **deduped by account** against the `08242234` RPS book (PRD 3c D1=SPLIT: all 4 Opal ETFs live in `08335338` ~22K rows AND `08242234` RPS carries ~$153M DIVZ -- so the leg is avgcap(`08242234`) + CBUGL(`08335338`) DEDUPED BY ACCOUNT, never summed). `state` flips off `incomplete` to its real vintage; `custody.deduped_by_account=true`.
- **Boundary I hold:** I do NOT pull `08335338` -- that is `~A`'s sovereign-scoped G2 lane. G5 consumes whatever `~A`'s converged custody artifact serves, Opal-side. If the dedup requires a data read I'd have to originate, I STOP and surface (invariant-1).

## 4. G4 ownership in the converged shape

The `ownership` nested list (CTO-base pick, endorsed for G5): both-masters custody at P2 adds/updates ENTRIES in the same list -- it does not add items or attributes. `partial="08242234-only"` on the 49F entry during interim; its removal (P2 dedup) = attribute absent = **G4 DONE** (PRD AC4). Canonical held-source per partner = `opal-data-etfs/daily` (COO-ratified; inflection `source_artifact=opal-data-inf/gold/canonical/holdings`, 49F `=opal-data-bd/schwab/silver/rps` i.e. the `08242234` side) -- one source per partner, no mdpf-target-weight double-source.

## 5. DS's 3 notes -- carried into G5 (binding on P0-B too)

1. **Census = ALWAYS 14 rows** (explicit missing/incomplete rows). A day with <14 rows = writer failure, structurally distinct from data absence.
2. **rolled_forward / carried values = VERBATIM copy** of value+as_of from the last fresh observation (never re-derived) -- applies to cohort tops AND ownership entries.
3. **Upsert visibility:** `first_written_at = if_not_exists(...)` + `emitted_at = :now` on every (cohort, bucket_date) UpdateItem -- a re-write is visible without breaking idempotency.

## 6. Served cutover = P2, GATED (not in this spec's build)

G5-full's promotion onto the ModelPortfolios / AUM served surface rides **NEVER#2 never-widen co-sign (CTO+COO+Andrew)** + **NEVER#4 served-artifact verification** (a verified DELTA=0 promote needs no hold; any served AUM figure change needs the co-sign on record -- PRD AC6). This spec designs the SHAPE the cutover would serve; it does **not** authorize or perform the cutover. The bucket runs ALONGSIDE today's surface until the co-sign.

## 7. Open items for the CTO~B gate

- `custody` map on cohort-8: nested map (this spec) vs promoting `present/missing_masters` to top-level attrs. Recommend nested map (keeps the 14-item invariant; cohort-8-only).
- `expected_masters` informational field (CTO-base open item): I recommend **keeping** it on `incomplete` cohorts -- it's what makes the row self-describe its gap; drops to redundant once `source_masters` carries both at P2 (harmless to leave).
- Trigger for the emitter: S3-event off the platinum write (CTO-base's actual recommendation) vs `cron(30 15 * * ? *)` -- S3-event removes the missed-run staleness window; `~A` owns the emitter so it's `~A`'s call, flagged for consistency with my fold's re-run visibility.

## 8. Compiler Tools

| Tool | Call | Result |
|---|---|---|
| `comp-glob` | `**/*avgcap*` / `**/*rps_recon*` | located the fold source + confirmed sovereign-diagnostic vs served-artifact distinction |
| (Opal-side S3) | `aws s3 cp` `opal-data-etfs/daily/{49financial,inflection}` | grounded the ownership fold shape + per-partner own-field `source_as_of` (49F 06-24, inflection 07-10) |

No sovereign bucket touched; forward-design only (no apply, no TF, no IAM). Both-masters dimension explicitly POST-G2.
