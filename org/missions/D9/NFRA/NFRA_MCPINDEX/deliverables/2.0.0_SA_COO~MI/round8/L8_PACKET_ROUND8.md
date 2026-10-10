# NFRA_MCPINDEX round 8 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-10 ~22:4xZ)

Addressed to `3.0.0_SA_CVO~Z`.
- **Source:** PRD v0.7 (ADMITTED @3c7ff0684b). Issuance @b0d8580aab: 4 cells in ONE issuance. Battery
  `deliverables/2.0.0_SA_COO~MI/round8/checks/`.
- **State:** 4 of 4 orders are drained and issuer-graded on box/sitez. `round-close-check.py --round 8` reads MAY-CLOSE
  (3 proofs structurally OK at the 22:3xZ read; MX-r-9 flips on its applier's proof commit). Round 7 stays open on
  MX-s-19 alone, which is event-gated on the 2026-10-13 runs.

## 1. Orders -- graded on box/sitez (issuer re-run after each drain)

| order | risk | status | mechanical (issuer re-grade) | judgment owed at L9 |
|---|---|---|---|---|
| MX-d-7 (discover states the TRUE as-of) | WORLD | complete @9f51c11617, drained @e9545d6823 | d7.AC1 3/3 tests; AC2 3/3 stated as-of == served (claim measured); AC3 routing 24/27 (floor 24); proof VALID | none |
| MX-c-6 (the 29 need entries) | WORLD | complete @5a7edfb8ab, drained @dc3435a65f | c6.AC1 29/29 entries, 0 violations; AC2 3/3 tests; AC3 4/4 tool sets, 15 named, 0 unknown; proof VALID | **J2** (via MX-r-9) |
| MX-d-8 (discover answers needs, in her words) | WORLD | complete @182203f735, drained @4b29d72cc3 | d8.AC1 present 9/9, routed 9/9 first try, original 24/27; AC2 3/3 named tests; proof VALID | none |
| MX-r-9 (the release) | WORLD | LIVE d3c31e972e since 2026-10-09 19:42Z, labels repaired 2026-10-10 21:50Z; ledger CLOSED 4/4 @3cc6f5e6ec | r9.AC1 PASS (30 of 30 sentinels scanned); r9.AC2 PASS 3/3 (ssm 1c43624e); r9.AC3 PASS 9/9 + 3/3 (ssm a334d45a) -- all re-run by the issuer after the 21:50Z restart | **J1**, **J2** |

## 2. The one real run of the outcome (FWD-11, the thread), 2026-10-10 ~22:4xZ

Through this seat's opalgateway MCP session (an admitted Opal principal), against the served host:
- `opal_discover("how did the growth model do against its benchmark last quarter")`: catalogued true, one match, need
  **E-13** "Model performance by period versus its benchmark", SERVED, op_class read, `next_tool`
  `mdpf_get_model_benchmarks`, retires W6 and C2.
- `mdpf_get_model_benchmarks()`: `data_as_of` **2026-10-09**, generated 2026-10-10T11:06:04Z,
  `opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json`; 5 models (UST, ST, INT, LT, ULT), each with
  index and ETF benchmark bases; the caveat says "model-design returns, never realized" and the basis note says "name
  the basis". 2026-10-09 is the T-1 trading day for a Saturday read.
- Example, 1Q, ULT: model -0.82, index benchmark +1.51 (spread -2.33), ETF benchmark +1.36 (spread -2.18).
- **Noted for J1:** no model is named "growth". Discover routed on the need anyway. The answer has to name one of the 5
  models, or ask which one; it must not supply a growth figure. That is part of what J1 judges, from her own words.
- The opalinvest.dev page comparison is J1's proof. It is not done here.

## 3. Judgment criteria

- **J1 (FWD-11, PRD v0.7:213-220):** Alyssa, in her own words, asks how a model did against its benchmark for a
  period. Discover names the tool, states the true as-of, and the figure matches opalinvest.dev. Proof: her transcript
  beside the served `data_as_of` and the page. **NOT RUN: HELD at Andrew.** `0.0.0_AB_MSTR~Z` put the Alyssa booking
  to him at 21:27Z (msgs 33019/33020/33034); the precondition (AC2 + AC3 PASS, ledger closed) is met.
- **J2 (FWD-12, PRD v0.7:222-229; FWD-18, :270-275):** subtract the served catalog's needs from her two briefs, with
  nothing missing (denominator 29); and the count of C1-C8 and W1-W6 a SERVED entry answers (denominator 14). Served
  catalog: `app/refs/DATA_CATALOG.yaml` on the host, md5 7e9e40bb185f266aa293a7d29ad67e6d (= release d3c31e972e); need
  map `deliverables/2.0.0_SA_COO~MI/ALYSSA_WORKFLOWS_INDEX_INPUT_MAP_20261009.md`.

## 4. Rows this round, and the issuer's rulings

| row | in-file | ruled by |
|---|---|---|
| Z-W28-S1, S2 (MX-d-7) | OBSERVATION/INERT | Z-S86 at the d-7 drain |
| Z-W28-S3, Z-W29-S2 (commits refused on stale worktree bases) | BLOCKING/ARMED | Z-S86: DISARMED; each branch merged the index fix ac148d7eb9 before its close |
| Z-W29-S1 (emitter rewrites the census dir) | OBSERVATION/ARMED | Z-S86 |
| Z-W28-S4..S6 (MX-d-8) | OBSERVATION/INERT | Z-S87: confirmed; S4's word folds are a later catalog enrichment |
| Z-W28-S7, S8 (PHASE A pins, suite baseline) | OBSERVATION | Z-S89 |
| Z-S90 (.env equality as a rule) | OBSERVATION/ARMED | Z-S91 (A3): DISARMED |
| Z-S92 (artifacts mislabelled) | BLOCKING/ARMED | Z-S95 @b0d9d6a69b: DISARMED; both CTO read-backs re-measured by the issuer (ssm e80b1708) |
| Z-S93 (repair evidence), Z-S94 (2 orphaned dashboard assets) | OBSERVATION/INERT | Z-S95; S94 is NFRA_OPLGTW's deploy surface, told to 2.0.0_SA_COO~O |

## 5. Carried to the round-8 L10 slug (enrichment candidates)

1. **Deploy procedure:** a release's deploy tree HEAD must BE the deploy-only commit (Z-S92's cause:
   `deploy-to-ec2.sh` names and stamps from `rev-parse HEAD`). The wrapper's manifest auto-commit fails in a sparse tree
   (`commit_gate_runner.py:96`, ModuleNotFoundError `comp_constants_cli`); seen on both MX-r-9 runs.
2. **Catalog word folds** (Z-W28-S4): move her phrasings into E-9/E-19 example text.
3. **An unknown model name** (section 2): decide whether discover or the tool answer asks which model when a named model
   does not exist.
4. **Round 9 (FWD-19 readers)** is cut after this round's L10, per `1.0.0_SA_CTO~Z`'s ruling
   (`ledger/CTO_RULING_ROUND9_AFTER_ROUND8_DRAIN_20261009.md`, call 9c9d).
