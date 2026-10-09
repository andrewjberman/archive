# ADVI_FIRMBKTS -- round 2 pre-cut facts (2.0.0_SA_COO~F1, dell1, 2026-10-09 ~22:0xZ)

Read-only measurement taken WHILE BLOCKED on the round-1 analysis (the CVO's slug, then the CTO). This is not a cut:
round 2's rectangle is the analysis's enrichment list. Identity for every AWS read:
`arn:aws:iam::313476888478:user/cloudops-dell1-agent-user`.

## 1. F4 -- whom the fence admits (row ADVI_FIRMBKTS-D1-S1)

`get-bucket-policy` is READABLE today on all three firm buckets. Statement `DenyForeignFirmPrincipals` denies `s3:*`
to every principal whose ARN is NOT LIKE one of its admitted patterns:

| bucket | admitted patterns | firm glob | others |
|---|---:|---|---|
| `opal-data-inflection` | 7 | `role/*-inf-*` | `user/Andrew_Berman`, `user/Andrew_Berman_Console`, `user/Opal_Terminal`, `role/irpt-holdings-role`, `user/cloudops-dell2-agent-user`, `user/cloudops-dell1-agent-user` |
| `opal-data-cottonwood` | 7 | `role/*-cot-*` | the same six |
| `opal-data-49financial` | 21 | `role/*-49f-*` | the same six, plus three AWS service roles, `bd-exporter-ec2-role`, `opal-advi-stitch-landing-role`, `irpt-performance-adapter-role` and seven estate roles |

- PRD v1.3's F4 premise ("denies `s3:*` to every identity we hold") no longer holds: the repair it planned has
  landed (the admit list now carries named users and both CloudOps users). F4's first criterion, *an identity this
  estate holds performs a named `s3:*` act and succeeds*, is reachable as `user/cloudops-dell1-agent-user` (list and
  versioning reads succeeded).
- The negative arm is not yet exercised: a `role/*-cot-*` principal refused on `opal-data-inflection`. By the policy's
  text it is refused, but that is a DESIRED-plane read of an attached policy, not an exercised refusal.
- `opal-data-cottonwood` carries three more statements guarding `commonwealth/cottonwood/bronze/crm/` (reads and
  lists only for `Andrew_Berman_Console` and `cloudops-cot-restricted-breakglass-role`; writes only for the latter).
- Row IRPT_BCKEND-S107's exposure stands: the firm boundary is a substring glob over role NAMES.

## 2. F6 -- the router's rewrite targets (`infra/aws/lambda-edge/shared-advisor-router/index.mjs`)

- The bucket resolves in three branches (`:228-260`): `opal-capital` staff from `?firm=<slug>` as `opal-data-${slug}`;
  a mapped firm from `FIRM_BUCKET_MAP` (`../_shared/firm-config.mjs`); an unmapped firm as `opal-data-${firmId}`.
  Today 49 Financial maps to `opal-data-bd` (`:77-79`).
- `/api/scoped/advisor-intelligence/` rewrites (`:263-318`): `platinum/**` passes through to `/platinum/**`
  (summary.json under advisors/clients refused 401); `advisors/` -> `/gold/entities/`; `client_timeseries/{id}.json`
  -> `/gold/entities/clients/{id}/timeseries.json`; `views/`, `timeseries/`, `artifacts/`, `entities/` -> `/gold/...`;
  everything else -> `/gold/artifacts/`. Six of the seven branches carry `// LEGACY: ADVI_49PUSH`.
- DEC-6's target is `advi/{firm}/platinum/...`, one table in the router and one in the response guard, generated
  from the registry.

## 3. F7 -- 49 Financial's served keys at their new homes

- In `mapping.json`, `opal-data-bd` has 216 classes: 11 MOVE to `platinum`, 105 FAULT.
- `head_object` on the 11 canonical platinum addresses (each built by `address()` for its class's sample key):
  **0 of 11 present.** This is the gap LGIC_CANON carded at steps 10 and 16 (the `address()` home key 404s).
- So F6's flip has nothing to serve until F7's copy lands. The two are one cut: copy, compare on data-bearing leaves,
  then flip under never-widen sign-off (DEC-4).
