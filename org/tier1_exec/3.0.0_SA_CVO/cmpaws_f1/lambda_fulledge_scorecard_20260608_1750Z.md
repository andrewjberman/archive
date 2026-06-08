# NFRA_COMPAWS — Lambda full-edge cert

**CVO:** 3.0.0_SA_CVO (independent — compiler + live re-pull + state-union)
**Build:** comp-aws @ 07833813d | **Derive:** `.runtmp/comp_v2.json` (snapshot 17:33:50Z)
**Methodology:** `CMPAWS_F1_CERT_METHODOLOGY.md` — headline-F1 ≥0.95 ∧ 0-untyped ∧ brittleness-pass

## LAMBDA — **CERTIFIED (full-headline 1.00)**

**Existence — 1.00.** 171 nodes vs 171 live at snapshot. Live re-pull at 17:50Z shows 172; the delta (`cw-bd-session-trigger`) has **LastModified 17:43:47Z — created ~10 min AFTER the derive snapshot (17:33Z)**. Freshness artifact, NOT an enumeration miss: plain Zip/python3.11/Active function, no exclusion path; a re-derive would include it. Existence F1 at snapshot = 1.00.

**Typing — 1.00.** 0 untyped.

**Properties — 1.00.** runtime / memory / timeout / role complete. 4 nodes have null `runtime` (opal-news-ai-sentiment, news-semantic-clustering, ycharts-session-capture, yfinance-aapl-test) — all verified `PackageType=Image` against live, so null runtime is **correct** (container lambdas have no managed runtime), not a property gap.

**Provenance — 1.00.** 137 DECLARED / 34 LIVE-no-DECLARED, all drift-classed.

**Edges — 1.00:**
- `ASSUMES` (lambda → execution role): 171 — every lambda emits exactly one; **0 orphan, 0 non-IAM target**.
- inbound `TRIGGERS` (→ lambda): 105 — all resolve; sources 98 eventbridge + 7 s3 (event-notification). 0 dangling.
- outbound capability (`READS`/`WRITES`/`READS_SECRET`/`PUBLISHES_TO`/`SENDS_TO`/`ENCRYPTS_WITH`/`LOGS_TO`): **0 cross-wire** — confirms EDGE-CROSSWIRE-1 is EC2-role-only; lambda's capability projection is clean. Wildcard-capability edges are the established GRANT-projection ruling (brittleness-exempt).

**Brittleness:** deterministic — ASSUMES/TRIGGERS derive from config (role + event-source), not heuristics; capability layer is GRANT-projection. Re-derive stable.

**Verdict:** node ∧ typing ∧ property ∧ provenance ∧ edge all 1.00. **CERTIFIED full-headline.**

---

## Tally after this cert
**Full-headline CERTIFIED (6/13):** S3, EC2, eventbridge, dynamodb, kms, **lambda**.
**At-gate w/ finding:** secrets (0.996, EDGE-CROSSWIRE-1 → AE).
**Node+property certified, full-edge pending AE edge family:** IAM (typed-principal), sns (typed-endpoint), sqs (DLQ-linkage), cloudwatch (MONITORS), cloudfront (OAC/OAI).
