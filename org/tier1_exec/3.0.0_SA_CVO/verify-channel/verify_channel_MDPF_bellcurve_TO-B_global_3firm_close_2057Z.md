# /verify-channel Mode A — MDPF bell-curve footer TO-B GLOBAL slice + 3-firm close — 2026-06-01T2057Z

**VERDICT: GLOBAL current-artifact PASS ; DURABLE CERT = CONDITIONAL (gated on AE EC2 docker redeploy). 3-firm TO-B set: 49F PASS + inflection PASS + global PASS-now/CONDITIONAL-durable.**
**Requester:** DS~B `[AC3 global ready for cert]` 2054Z (per AE ask) — completes the 3-firm set for cert; I certed inflection slice (`bf244cac1`) + corroborated 49F (`ce1424df4`).
**Surface:** SERVED `s3://opal-data-portal-v2/json/portfolios/account-distribution.json` (the default/unscoped account-distribution = consumer's no-firm-selected bell-curve). Independent artifact read, not DS~B self-report.

## GLOBAL current artifact — PASS (4-check + Step 2.5)
1. **EXISTS + FRESH:** present, generated_at 2026-06-01T20:54:40Z (head-object LastModified 20:54:43Z). ✓
2. **VALUES + ARITH:** TOTAL funded 6838 / active 6840 / `excluded_unfunded_count` 2; active − funded = 2 = excl, EXACT. period=202605 (May, the latest FUNDED period — correctly skips the 202606 June $0-shell). ✓
3. **by_model RECONCILE (Step 2.5 aggregate-identity, the sharp test):** 5 models, SUM(by_model) excl=2 / funded=6838 / active=6840 == totals to the unit. NOT identity-masked — walked per-model. ✓
4. **SCALE/identity sense:** global funded 6838 == 49F funded 6838 EXACTLY (incl by_model). This is a **legitimate identity, not a degenerate collapse**: `json/portfolios/account-distribution.json` is the default SmartX book, and the SmartX book IS 49Financial (producer sources `SMARTX_ALLOC_KEY`; inflection sourced separately from `INF_BUCKET` to `json/mdpf/inflection/`). There is no `json/mdpf/global/account-distribution.json` — "global" = SmartX-default-view = 49F. So global≠all-firms-sum by design; the "3 firms" label is loose (global is the SmartX default, which coincides with 49F). Honest-limit: I infer this from the source key + the exact numeric+by_model identity; confident, but flagging the loose "global" naming.

## Step 3.5 — decision-useful
The default bell-curve renders the SmartX (49F) account-size distribution; firm-scoped views (`json/mdpf/{49financial,inflection}/`) render their books. Each scope shows its real distribution; the LD-0012-class cross-scope-subtraction garbage (old inflection 6639 = global 7039 − dist 400) is structurally eliminated for ALL THREE firms (49F excl=2, inflection excl=5, global/SmartX excl=2 — all accounts-grain, plausible-small 0.03%/1.23%/0.03%). Meaningful + correct grain.

## DURABILITY — CONDITIONAL (the binding axis; ship-attestation != deploy-attestation)
DS~B's own flag, structurally confirmed as the correct verifier posture: the served 6838@202605 is correct NOW because the **corrected producer was run directly** to emit it — but the **EC2 daily exporter (~14:16Z) runs a DIVERGED old bundled `smartx-workspace/scripts` copy** lacking the latest-funded-period selection. The next daily run re-selects 202606 (June $0-shell) and **re-overwrites to the anomalous 7025@June** until AE redeploys the EC2 docker (AE lane, on COO go).
- This is `[[feedback-s3-pull-dispatcher-no-auto-propagate]]` / `[[feedback-ship-attestation-vs-deploy-attestation-distinct]]`: a fix run-to-S3-once is NOT the same as the RUNTIME running the fixed code. The artifact is correct; the regenerating runtime is NOT yet fixed.
- **Verifier-conservative:** I do NOT issue a clean durable cert. **Durable cert fires when (a) AE's EC2 docker redeploy lands AND (b) a post-deploy daily run regenerates 6838@202605 (the correct latest-funded period) from the RUNTIME** — at which point the artifact's correctness is durable, not transient.

## 3-FIRM TO-B ROLL-UP
| firm | path | funded | active | excl | by_model reconcile | CVO verdict |
|---|---|---|---|---|---|---|
| inflection | json/mdpf/inflection/ | 400 | 405 | 5 | SUM=5 (IntTerm 3 + INT/LTC 2) ✓ | PASS (bf244cac1) |
| 49financial | json/mdpf/49financial/ | 6838 | 6840 | 2 | SUM=2 (Long Term) ✓ | PASS (ce1424df4) |
| global/SmartX | json/portfolios/ | 6838 | 6840 | 2 | SUM=2 (Long Term) ✓ | PASS-now / CONDITIONAL-durable |

## Routing
**→ DS~B (CC COO+CTO+AE+DE).** GLOBAL current artifact PASS; AC3 data-correct on all 3 firms NOW. **DURABLE TO-B cert is CONDITIONAL on AE EC2 docker redeploy** — re-verify global post-deploy daily-run (confirm RUNTIME emits 6838@202605, not the 7025@June clobber). Until then the served global is transient-correct. No CVO fix (verifier≠fixer; EC2 redeploy = AE lane on COO go). Per closure discipline this is the DATA-layer; portal visual smoke (Andrew) remains the separate FE gate for MDPF close.
