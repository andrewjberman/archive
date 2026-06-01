# BMKAUD LEG-1 smartx-model-monthly-pull RETIREMENT — WS-5 zero-consumer NOD — 2026-06-01T1552Z

**NOD: GRANTED — sidecars consumer-free, LEG-1 retirement safe.** (Corroboration gate for CTO; destroy still held for Andrew apply-ratify.)
**Ask:** AE `[WS-5 NOD ASK]` 1550Z — CTO gated the smartx-model-monthly-pull full-retirement destroy on my explicit WS-5 zero-consumer nod.
**Verifier≠fixer:** independent corroboration (my own repo-wide grep + lambda-source reads), not a trust of AE's grep.

## Independent zero-consumer evidence
Repo-wide grep for `_smartx_model_monthly` / `_smartx_model_daily` / `smartx_model_{monthly,daily}.json` → 26 files, ALL classify as NON-consumer:
- **Producer (being removed):** `data/smartx/scripts/pull_smartx_model_monthly_performance.py` (WRITES both sidecars), `infra/aws/terraform/smartx-pipeline/model-perf-pull.tf` (its infra), `lambda-source-map.json` (its entry).
- **Docs/logs/TOs:** ~20 `*.md` (session logs, ws-charter, WS-4 ledger/census, briefs, YALP_MDSRC B1-B4 TOs, lineage-map) + my own WS-5 verify logs.
- **One-off verify scaffold:** `docs/briefs/b1_e2e_verify.py` (brief verification script, not a live pipeline node).
- **My runtmp:** `.runtmp/*` (evidence/invoke artifacts).
- **ZERO live reader code** under `infra/aws/lambda/**/*.py`, `data/*/scripts/{gold,silver,bronze}/**`, or `portal/src/**`.

Corroborating cross-checks (mine, from WS-5):
- Benchmark producer `yang-model-portfolio-benchmarks` reads `data.pkl → return_daily` only (full source read in pre-stage) — never the sidecars; deployed pure-yang (CodeSha256 IYrvZ0zN==revert).
- Peer producer `yang-generate-peer-performance` reads the uploaded xlsx only — never the sidecars.
- Component-3: `portal-proxy.ts` has ZERO `_smartx_*` references — FE never resolves them.
- Schedule already DISABLED (`f38353b0f`); sidecars frozen (last write 13:36Z, in the 20260601T1445Z evidence snapshot).

## NOD
The 2 sidecars (`_smartx_model_monthly.json`, `_smartx_model_daily.json`) are **consumer-free**; `smartx-model-monthly-pull` is a true orphan (WS-4 Finding #1). LEG-1 retirement (remove lambda + `model-perf-pull.tf` 8 resources + source-map entry + producer script) is **SAFE** — the destroy removes the sidecars' only writer; no reader exists anywhere. CTO gate-1 cleared on this nod. Destroy applies only on Andrew apply-ratify (reversible plan: 0add/0change/8destroy). Optionally delete the 2 stale frozen sidecar S3 objects post-destroy (cosmetic; they're already unconsumed).
