# ADVI_FIRMBKTS -- L5 fact sheet, round 1 (2.0.0_SA_COO~F1, dell1, 2026-10-09 ~20:0xZ-20:3xZ)

Read-only measurement taken before the cut. Each line names its instrument. The identity for every AWS read is
`arn:aws:iam::313476888478:user/cloudops-dell1-agent-user`.

## 1. The legacy population (the census domain)

| bucket | objects | instrument |
|---|---|---|
| `opal-data-bd` | 131,391 | boto3 `list_objects_v2`, paginated, counted client-side, at 2026-10-09T20:19:02Z |
| `opal-data-inf` | 99,668 | same listing |
| `opal-data-cot` | 7,802 | same listing |

- A paginated listing of all three takes about 40 s with three threads (measured twice). The `aws` CLI with `--query
  length(Contents[])` prints one count per PAGE (1000, 1000, ...), which is CLAUDE.md rule 22a's trap. The checks use
  boto3 and count client-side.
- The brief's 228 keys (IV.3) are the keys the served GRAPH attributes, not the population. FWD-2's ACCEPT reads "every
  piece of data in the three old places", so the census domain is the live listing (Rule 24 (i): the domain must be
  the claim's population).
- Grain: at a naive depth-3 class, `opal-data-bd` gives 11,165 classes, because `platinum/accounts/{id}/` (7,557) and
  `platinum/clients/{id}/` (3,354) carry an entity id in the third segment. With entity-id segments collapsed, the
  issuer's reference census gives 65 / 66 / 32 classes. The census check caps each bucket at 500 classes.
- Shapes the table must place, seen in the reference census: keys with a LEADING SLASH in `opal-data-inf`
  (`/advisors/...`, `/clients/`, `/firm/`); `ajb_workspace/logs/` in `opal-data-bd`; backups
  (`_pre_rebuild_backup/`, 6,061 objects in inf; `backup/served_spine_PRE_AOR_RELEASE_20260715T225000Z/`, 2,342);
  `_rollback/49f-20260630-preflip/` in bd; `qa/clients/` in inf.
- Both DECISION keys exist live in `opal-data-inf`: `gold/meta/pipeline-complete.json` (Door 6, FWD-7) and
  `orion/jwt/current.json` (B2, FWD-8).

## 2. The builders and the naming rule

- `LGIC_ENFORCE` is CLOSED (7 of 7 REALIZED, 2026-10-09 ~17:5xZ). `lib/opal_naming.py` `key()` and `address()` return
  the PRD's two CONTRACTS vectors byte for byte:
  - `key("advi","49financial","gold","fact_account_gains","date=2026-09-11")` gives `advi/49financial/gold/fact_account_gains/date=2026-09-11`;
  - `address("advi","49financial","platinum","firm","header_metrics.json")` gives `s3://opal-data-49financial/advi/49financial/platinum/firm/header_metrics.json`.
- `address()` homes a `bronze` tier in `opal-data-assets` (`orion/inflection/bronze/feed/date=...` gives
  `s3://opal-data-assets/...`), and a firm `gold` in that firm's bucket.
- **The PRD's two HELD families are RESOLVED at their source.** `LGIC_NAMING` is CLOSED, and its rows S6, S7 and S8 were
  ruled at v1.3. `org/standards/NAMING_SCHEMA.json` now carries `key.partition` (the entity form
  `{entity}={id}`), `key.code` (`{source}/{scope}/code/{built_tier}/{file}`) and `key.legacy_served_path` (a legacy
  served path keeps its bytes, membership in `LEGACY_SERVED_PATHS.json`). `address()` builds both forms. The PRD's
  condition was "until LGIC_NAMING resolves", so the table PLACES both families. Round 1 writes no object anywhere.

## 3. The firm buckets on the live plane

- `opal-data-inflection` and `opal-data-cottonwood`: `get-bucket-versioning` returns `Enabled`, and `list-objects-v2`
  returns objects, for this identity. **PRD v1.3's F4 premise (the fence denies `s3:*` to every identity we hold) does
  not hold for this identity today.** Filed as a row; it bounds F4's round, not round 1.
- `opal-data-inflection` holds `irpt/inflection/...` only (7 depth-4 prefixes). `opal-data-cottonwood` holds `irpt/` and
  `mdpf/` (12). `opal-data-49financial` holds 900 depth-4 prefixes, among them the 08-18 template's TIER-FIRST form
  (`gold/advi/canonical/...`, `gold/advi/dimensions/...`, `gold/advi/reference/bd_legacy_*`). That residue sits in a
  firm bucket, outside FWD-2's three-bucket domain. Filed as a row.

## 4. Rulings the cut reads as recorded

- FWD-7 and FWD-8: recorded (`project.json` `blocking` (8); `ANDREW_DIRECT_20260914_134xZ_NEXT_CALLS_RECS_AND_SEQUENCE_APPROVED.md`).
  DEC-13's hold on touching `opal-data-inf` is met. The read-only census never waited on it.
- Row `ADVI_FIRMBKTS-S11` (the tolerant-load patch for `build_canonical_prices_v2.py`) is input to the cell that renames
  that file's literal, which is F5's (the registry repoint). It is not in round 1.
