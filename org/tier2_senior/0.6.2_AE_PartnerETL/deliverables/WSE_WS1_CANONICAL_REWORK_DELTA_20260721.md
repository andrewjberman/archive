# WS-1 canonical-rework DELTA -- for CTO gate (BD_API_DESIGN.md conformance)

**Author:** 0.6.2_AE_PartnerETL · **Date:** 2026-07-21 · **For:** 1.0.0_SA_CTO (gate the reworked structure + landing/deploy shape)
**Trigger:** Andrew-direct 2026-07-21T213504Z @64fdd919c ("something like cot_bronze_ingest.py which pulls the model data through the rebalance endpoint every day") + CTO redirect-approval 213914Z.
**Grounded on:** `data/assets/docs/BD_API_DESIGN.md`, `data/cot/scripts/bronze/cot_bronze_ingest.py`, `infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py`.

## 1. The pattern shift (what changes)

| | OLD (my mirror, superseded) | NEW (canonical BD-REST) |
|---|---|---|
| Sibling | opal-assets-bd49f-daily-pull (DataMining->xlsx MONOLITH) | cot_bronze_ingest.py / bd-49f-runner (cookie-riding REST runner) |
| Auth | self-contained: RebalancerClient class mints its own bearer | DUMB about auth: reads the cot cookie the EXISTING session chain keeps fresh; mints the app token; auth-AWARE re-mint on 401 |
| HTTP | requests.Session + urllib3 Retry (layer dep) | stdlib urllib (cot_bronze_ingest convention; no requests layer needed) |
| Shape | one bespoke opal-assets Lambda | canonical firm-parameterized module (Model-B env) + CLI + lambda_handler |
| Session refresh | (n/a -- I minted inline) | RIDES cot-bd-session-trigger / bd-cot-keepalive / bd-cot-freshness-probe + the auto-login box -- a dead cookie self-heals, NOT my concern |

## 2. Canonical structure (mirrors cot_bronze_ingest.py)

- **Firm-parameterized (Model B):** `BD_S3_BUCKET`, `BD_FIRM_ID=cottonwood`, `BD_SESSION_SECRET_ID=blackdiamond/cot/session`, `REBAL_BASE=https://rebalancer.bdreporting.com` -- all env, defaults documented.
- **`load_bd_session()`** -> read `.bd.identity` (+ jar) from `blackdiamond/cot/session` (the cookie the chain keeps fresh). Fail-loud on empty.
- **`mint_rebalancer_bearer(cookie)`** -> `GET rebalancer.bdreporting.com/auth/token` (Cookie-authed) -> `{access_token}`. The Rebalancer-app analog of `get_datamining_token()` (each BD app mints its own; the DataMining bearer does NOT work here).
- **Auth-aware (bd-49f-runner classification, re-homed):** on a 401 mid-run, re-mint the bearer ONCE from the same cookie + retry; cookie-death is confirmed ONLY if the re-mint itself auth-fails -> stop LOUD (the chain + freshness alarm page). Transient 5xx -> linear backoff. No 401-storm.
- **`_already_landed(type, date)`** idempotence -> content-grounded (not bare existence), so a same-day double-invoke no-ops; fail-open to PULL on doubt.
- **Per-type ingest** -> land raw JSON; **bronze-complete stamp LAST** on full success.
- **`_assert_firm_separation()`** fail-closed (writes only under the cot scope; never blackdiamond/49f).
- **CLI** (`--type`, `--date`, `--backfill`) + **`lambda_handler`** -- runs as a Lambda daily AND hand-runnable, exactly like cot_bronze_ingest is CLI + SSM-run.

## 3. The 3 Rebalancer "types" (the model data, through the rebalance endpoint)

| type | endpoint | notes |
|---|---|---|
| `rebalancer_models` | POST /api/models/strategies/search | the roster (name<->id, per-model accountCount), RAW-COMPLETE |
| `rebalancer_accounts` | POST /api/accounts/search take=200 | the account book (strategyName per account = the assignment) |
| `rebalancer_model_detail` | GET /api/models/{id} | composition + blend children[].relativeAllocation; Opal-rooted TRANSITIVE closure |

## 4. CARRY-OVER (CTO-ratified, re-homed into the canonical runner -- NOT re-litigated)

- STRICT per-page byte-for-byte bronze pages (no estate paginated-JSON precedent -> strict pages, unambiguous 17a).
- Integrity manifest -> `meta/pulls/` (bronze is raw only).
- TWO fail-closed gates: pagination-integrity (rows==totalResultCount) + Sec.5 count-reconcile (296/14-Opal == roster).
- Transitive Opal model-detail closure; roster raw-complete; MODEL_DETAIL_SCOPE=all knob.
- Complete-stamp LAST; set-identity landing guard.

## 5. DECISIONS FOR YOUR GATE (recommendations flagged)

**(a) LANDING BUCKET.** cot_bronze_ingest lands to the FIRM bucket `opal-data-cot`; my PRD sec3 lands to the MONOLITH `opal-data-assets/blackdiamond/cottonwood/`. Andrew's redirect is about the PULL MECHANISM/FORMAT, not the bucket (he didn't touch it). **REC: keep the MONOLITH landing** (OPAL_CONSOLIDATION is the standing architecture; format is orthogonal to bucket). Env-parameterized so it repoints trivially if you rule firm-bucket.

**(b) DEPLOY SHAPE.** cot_bronze_ingest runs on the cot-exporter EC2 via SSM (heavy: xlsx + pandas + 900s datamining-run poll). The Rebalancer pull is LIGHTWEIGHT (JSON, ~26 calls, <120s, no xlsx/pandas) and cot-only (no Model-B firm-sharing -> no shared-script-pull rationale). **REC: a self-contained canonical Lambda** `cot-rebalancer-runner` whose lambda_function.py IS the canonical module + a CLI main() (faithful to "like cot_bronze_ingest" as a module, but Lambda-native since it doesn't need the EC2). Alternatives: bd-49f-runner-style (Lambda pulls a shared script from S3) or EC2/SSM -- both carry indirection this pull doesn't need.

**(c) FILE LOCATION / LANE.** cot_bronze_ingest lives in `data/cot/scripts/bronze/` (DS-lane, Rule 13). This is a BD-API-INFRA pull (AE/BD-box domain per BD_API_DESIGN.md) and Andrew assigned it to me (AE). **REC: AE-owned** under `infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/`. FLAG: if you'd rather the pull SCRIPT live in `data/cot/scripts/bronze/` (Rule-13 DS-lane) with an AE runner wrapper, say so.

**(d) STAMP SHAPE.** cot_bronze_ingest emits `bronze/{date}/_BRONZE_COMPLETE.json` (sentinel); my monolith design uses `meta/{date}-complete.json`. **REC: keep `meta/{date}-complete.json`** (monolith meta convention) -- but FLAG per your "changes the stamp shape" ask; align to whichever the WS-2 silver trigger expects.

**(e) THE EXISTING opal-assets-bd-rebalancer-daily-pull Lambda** (@fb885c8d3) is SUPERSEDED by this rework -- its endpoint logic + the 4 carry-overs migrate into the canonical runner; I retire the old dir on your GO.

## 6. Ask

Gate (a)-(e). On your GO I rebuild as the canonical `cot-rebalancer-runner`, re-run the 13-test suite re-homed, bring you the reworked code for the deploy-gate review, and re-sync WS-5 (0.7.0) on the adjusted TF (runner Lambda name/role/schedule unchanged in shape; the auth-is-external-chain simplifies the role -- no change to the S3/secret grants).
