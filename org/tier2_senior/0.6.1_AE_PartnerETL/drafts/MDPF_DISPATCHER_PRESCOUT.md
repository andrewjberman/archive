# MDPF dispatcher pre-scout — ADHC_CDNCOHT pattern application

**Author:** 0.6.1_AE_PartnerETL
**Date:** 2026-05-26
**Trigger:** ws COO STANDBY-PREP dispatch 2026-05-26T~14:31Z per `/allocation #4` KEEP-EPHEMERAL discipline (terminal "standing by" forbidden)
**Anchor PRD:** `docs/architecture/ADHC_CDNCOHT.md` v0.1 (1a61f61c3); pattern v0.2 amend per ws CTO Path A 2026-05-26T~14:14Z post-CVO verdict `e45b4a21a`
**Pattern reference:** INF (`inf-pipeline-v1.7.67` / `b00e2733e`) + BD (`bd-v2.24.9` / `053bba6f7`) ships 2026-05-26 14:00-14:09Z

---

## §1 — Inventory MDPF infra surface

| Item | Path / identifier |
|---|---|
| Terraform module | `infra/aws/terraform/mdpf-pipeline/` (iam.tf + ec2.tf + lambdas.tf + alarms.tf) |
| EC2 instance | `aws_instance.mdpf_daily_runner` (decl in `mdpf-pipeline/ec2.tf`); single-instance daily runner pattern |
| EC2 instance role | `aws_iam_role.mdpf_runner` (name: `mdpf-daily-runner-ec2-role`); instance profile `mdpf-daily-runner-profile` |
| Lane policy | `aws_iam_role_policy.mdpf_runner` (Sid blocks: SmartXCredsReadWSB, MdpfFeederBucketRW, EtfsSilverReadWSD1, EtfsListScoped, BdReadWSD2WSE, BdListScoped, PlatinumMdpfScopedRW, PlatinumMdpfListScoped, JsonPortfoliosLegacyRW, InfEclipseReadLegacyEmit, OrionJwtReadStage0Bronze, InfEclipseListScoped, ChainFailedMetric, DispatchLogs) |
| Dispatcher script | `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh` — **LIVE** (252 lines; 4-stage DAG: Stage 0 orion bronze → Stage 1 parallel feeders WS-B/C/D.1/D.2 → Stage 2 WS-E → Stage 3 WS-A aggregate → Stage 3.5 legacy non_model_assets emit → Stage 4 rollup timeseries) |
| Dispatcher S3 location | `s3://opal-data-mdpf/code/` (synced into `/opt/mdpf/scripts/` at run start) |
| Bucket | `opal-data-mdpf` (per `local.mdpf_bucket`); platinum writes to `opal-data-portal-v2/platinum/mdpf/*` + `opal-data-portal-v2/json/portfolios/*` |
| Trigger | `mdpf-daily-trigger` Lambda → starts the EC2 → user-data fires dispatcher |
| Chain-failed metric | `MDPF/DailyChain.ChainFailed` (already wired; analog of INF's `Inflection/GoldChain.ChainFailed`) |

**MDPF gold-chain IS live** (contra PRD §6 framing "future MDPF dispatchers if applicable"). The dispatcher runs daily and emits platinum artifacts. COO ACK on 2026-05-26T13:57Z deferred MDPF scope from initial TO based on PRD framing; reality on disk is MDPF chain shipped + emitting since at least MDPF_ASSETS.018 (2026-05-19). **Re-affirming MDPF applicability is a scope-refinement candidate.**

## §2 — Equivalent of INF/BD `chain_exit==0` gate point

MDPF dispatcher uses a different exit-path mechanism than INF/BD:

- **INF / BD**: post-chain block placed inline after sentinel write, gated explicitly by `[ "$chain_exit" -eq 0 ]` (and `MODE=chain && DRY_RUN=0`)
- **MDPF**: linear execution; each stage fail-fasts via `CHAIN_STATUS="failed"; exit 1` (lines 189, 200, 211, 247); on success reaches `CHAIN_STATUS="complete"; exit 0` (lines 251-252); `trap 'finish "${CHAIN_STATUS:-failed}"' EXIT` (line 120) calls `finish()` on every exit; `finish()` differentiates via `[ "$CHAIN_STATUS" = "complete" ]` (line 107) for the CW metric value

**Two equivalent insertion points** for CF invalidation:

**Option A (inline, mirrors INF/BD):** between line 250 (`LAST_OUTPUT="All 4 stages complete..."`) and line 251 (`CHAIN_STATUS="complete"`). Pros: explicit "chain succeeded" placement; matches INF/BD shape. Cons: bypassed if a future refactor changes the exit path.

**Option B (inside `finish()`):** add a block after the CW metric block (line 113) gated on `[ "$CHAIN_STATUS" = "complete" ]`. Pros: trap-driven; centralized post-chain logic; survives future stage-flow refactors. Cons: invalidation runs during the trap-handler, slightly less explicit.

**Recommendation: Option B** (inside `finish()`). MDPF already centralizes post-chain logic in `finish()` via trap; adding the invalidation there matches the existing pattern + survives stage-flow changes. Sample block shape:

```bash
# ADHC_CDNCOHT.001-INTERIM.MDPF -- post-chain CloudFront invalidation
# Fires only on CHAIN_STATUS=complete. Path-scoping covers MDPF-emit
# surface: /api/general/json-tiered/* (CF behavior #14) + /json-tiered/*
# (CF behavior #15) -- where platinum/mdpf/ + json/portfolios/* surface.
# Failure -> WARN, chain log records it but trap-driven flow continues.
if [ "$CHAIN_STATUS" = "complete" ]; then
  CDNCOHT_DIST_ID="${CDNCOHT_DIST_ID:-EVTSA9VEHNZVH}"
  CDNCOHT_PATHS="${CDNCOHT_PATHS:-/api/general/* /json-tiered/*}"
  echo "[mdpf-dispatch] CDNCOHT invalidation distribution=${CDNCOHT_DIST_ID} paths=${CDNCOHT_PATHS}"
  _cdncoht_out=$("$AWS" cloudfront create-invalidation \
      --distribution-id "$CDNCOHT_DIST_ID" \
      --paths $CDNCOHT_PATHS \
      --query 'Invalidation.{Id:Id,Status:Status}' \
      --output text 2>&1) && _cdncoht_rc=0 || _cdncoht_rc=$?
  if [ "$_cdncoht_rc" -eq 0 ]; then
    echo "[mdpf-dispatch] CDNCOHT invalidation OK: $_cdncoht_out"
  else
    echo "[mdpf-dispatch] WARN: CDNCOHT invalidation FAILED (exit=$_cdncoht_rc) -- chain UNAFFECTED. $_cdncoht_out"
  fi
fi
```

## §3 — Effort estimate + STRUCTURAL DELTA (must read before dispatch)

**Effort if pattern applies straightforwardly: ~30-45min.** Mirrors INF/BD pattern: iam.tf addition + dispatcher block + S3 upload + terraform plan/apply + smoke invalidation. Single role single dispatcher.

### Structural delta vs INF/BD — surfaces TWO judgment calls for COO/CTO

**Delta A — different CF behavior surface; different path-scoping.**

MDPF writes platinum to `s3://opal-data-portal-v2/platinum/mdpf/*` + `s3://opal-data-portal-v2/json/portfolios/{aum-timeseries,non_model_assets}.json`. These surface via CloudFront behaviors **#14 + #15 + #16** (NOT #2/#3/#4/#12 like INF/BD):

- #14: `/api/general/json-tiered/*` → S3-opal-data-portal-v2-json (origin-response: `cache-control-injector`)
- #15: `/json-tiered/*` → S3-opal-data-portal-v2-json (direct, no L@E)
- #16: `/api/general/*` → S3-opal-data-portal-v2-json (origin-response: `cache-control-injector`)

So the MDPF invalidation must target a **different path set** than INF/BD: `/api/general/json-tiered/*` + `/json-tiered/*` (and possibly `/api/general/*` if the chain ever emits there). NOT `/api/scoped/advisor-intelligence/*`.

**Delta B — existing `cache-control-injector` L@E already bounds MDPF staleness to 5min.**

The cache-control-injector L@E (sibling to LEDGEH; deployed and live) already injects `Cache-Control: public, max-age=300, s-maxage=300` on `/json/` prefix URIs on behaviors #14 + #16. So MDPF's worst-case CDN staleness is **5 minutes**, NOT unbounded like the INF/BD pre-fix state was (18hr empirical anchor 2026-05-14).

**Implication:** the 18hr-staleness incident class (which justified INF/BD shipping urgently) **structurally cannot happen on MDPF**. Dispatcher-side invalidation would reduce 5min worst-case → ~30s — a real improvement but qualitatively smaller. Whether that justifies the ~30-45min ship + the small ongoing invalidation cost ($0.005 × 1 chain/day = ~$2/yr) is a COO/CTO judgment call, not an obvious operational unblock.

**Behavior #15 caveat (`/json-tiered/*` direct, no L@E):** the direct behavior does NOT have cache-control-injector. If consumers actually hit `/json-tiered/*` (vs the L@E-fronted `/api/general/json-tiered/*`), they ARE exposed to unbounded CDN cache duration. Worth a `comp-platinum reverse` check on whether portal components consume `/json-tiered/` directly vs through `/api/general/json-tiered/`. If they hit it directly, that IS the same toxic primitive INF/BD had — MDPF pattern application becomes urgency-equivalent to INF/BD.

### Suggested dispatch shape (if COO ratifies application)

If the structural deltas don't kill the application, a TO-001-INTERIM.MDPF would carry:

- Add `cloudfront:CreateInvalidation` Sid to `aws_iam_role_policy.mdpf_runner` (single statement, distribution-scoped to `EVTSA9VEHNZVH`)
- Add `finish()`-internal invalidation block per Option B above
- Path-scoping: `/api/general/json-tiered/* /json-tiered/*` (env override via `CDNCOHT_PATHS`)
- Upload dispatcher: `aws s3 cp infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh s3://opal-data-mdpf/code/scripts/` (verify exact target path; MDPF uses `code/scripts/` not `code/gold/`)
- Tag: `mdpf-pipeline-vX.Y.Z` (next-bump from latest)
- ACs analogous to AC1-AC5 from INF/BD TO

## §4 — Open questions for COO / CTO (pre-dispatch)

1. **Re-affirm MDPF applicability.** MDPF gold-chain IS live (vs PRD §6 "future" framing). Is dispatcher-side invalidation in scope for MDPF, given Delta B (cache-control-injector already bounds staleness to 5min on the L@E-fronted behaviors)?
2. **Behavior #15 direct path exposure.** Does any portal component consume `/json-tiered/*` directly (no L@E cache-bound), making MDPF urgency-equivalent to INF/BD pre-fix? `comp-platinum reverse` on `json/portfolios/aum-timeseries.json` + `platinum/mdpf/aggregate_aua/*.json` would settle this.
3. **AC4 path-scoping carry-over.** Per ws CTO v0.2 amend (post-CVO verdict `e45b4a21a`) — should MDPF use blanket-pattern (consistent with INF/BD v0.2 ratified scope) OR per-chain `output_paths`-derivation (the stricter v0.1 reading)? Recommend mirror-INF/BD blanket for consistency unless CTO directs otherwise.

## §5 — Standing

Pre-scout deliverable banked at this path per COO directive. No commit yet (drafts are uncommitted by convention; will commit if COO ratifies dispatch). Standing for next-TO dispatch — either MDPF TO if COO ratifies, OR a /allocation pivot, OR continued KEEP-EPHEMERAL standby.

— 0.6.1_AE_PartnerETL
