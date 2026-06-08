# CMPAWS Wave-2 F1 Scorecard (node-level) — the 9 remaining classes

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-08 ~16:05Z
**Compiler:** `.tools/comp-aws` @ 2a604aa1e (property-complete, all 13 classes; CVO ran it)
**Method:** `CMPAWS_F1_CERT_METHODOLOGY.md` — existence vs LIVE re-pull; drift-class vs CVO
state-union (managed + data-source + §1.4 HCL-secondary); typing vs §3 schema. ARN-keyed.

## Node-level result — all 9 PASS (existence + typing + drift-class)

| Class | compiler | live | existence-F1 | declared | shadow (LIVE-no-DECL) | untyped | residual-false-shadow | node verdict |
|---|---|---|---|---|---|---|---|---|
| eventbridge | 92 | 92 | **1.00** | 78 | 14 | 0 | **0** | PASS |
| lambda | 171 | 171 | **1.00** | 137 | 34 | 0 | **0** | PASS |
| sns | 8 | 8 | **1.00** | 6 | 2 | 0 | **0** | PASS |
| sqs | 2 | 2 | **1.00** | 2 | 0 | 0 | **0** | PASS |
| dynamodb | 35 | 35 | **1.00** | 23 | 12 | 0 | **0** | PASS |
| cloudfront | 4 | 4 | **1.00** | 4 | 0 | 0 | **0** | PASS |
| secrets | 59 | 59 | **1.00** | 21 | 38 | 0 | **0** | PASS |
| kms | 2 | 2 | **1.00** | 2 | 0 | 0 | **0** | PASS |
| cloudwatch | 35 | 35 | **1.00** | 20 | 15 | 0 | **0** | PASS |

**Node-level headline (existence ∧ typing ∧ drift-class): ~1.00 for every class.** Existence matches the
live re-pull exactly (0 missing/hallucinated); 0 untyped (closed vocabulary total); 0 residual
false-shadow (no declared resource mis-flagged unmanaged — the §1.4 fixes hold across all classes).
**Brittleness = PASS by construction** (the global pure-discovery property verified on Wave-1 applies to
every class — same primitive).

## High-value LIVE-no-DECLARED surfaces (cataloged-as-findings, HELD — Andrew steer, not remediated)
- **secrets: 38 of 59 unmanaged** (64%) — console-created creds/keys (smartx creds, the openai-key fleet,
  etc.). The largest unmanaged surface + an exposure-attribution class. Cataloged.
- **lambda: 34 / 171 unmanaged** · **cloudwatch: 15 / 35** · **dynamodb: 12 / 35** · **eventbridge: 14 / 92**
  · **sns: 2 / 8**. Each = a real unmanaged-resource finding, typed + recorded.

## What this scorecard CERTIFIES vs what remains (honest scope)
- **CERTIFIED node-level** for all 9: existence-F1 1.00, typing-F1 1.00, drift-class provenance (0
  false-shadow), 0-untyped, brittleness-by-construction. This is the bulk of the AC1/AC3 bar
  (every live resource mapped to a typed node; LIVE-no-DECLARED surfaced categorically).
- **PENDING per-class deepening (the PROPERTY + EDGE F1):** the §3 per-class properties (e.g. dynamodb
  pitr/gsi, cloudwatch threshold/treat_missing_data, kms key-policy full-statement-set §1.5,
  cloudfront cache-behavior path→origin) + the typed EDGES per class need their hand-audit oracle to
  score against. EVENTING already has its edge oracle (v0.4 — D4 fan-out + EVENT_SOURCE origins +
  STARTS chain), so eventing is closest to full cert. The other 8 get their property/edge oracle next.
- A class is FULLY F1-certified only when node + property + edge all clear ≥95% (methodology §6). This
  scorecard banks the node layer (the hardest-to-fake + highest-value layer) for all 9 at once.

## Next
- Eventing: full cert (node ✓ here + edge oracle v0.4) — re-confirm post-MDPF_CADENCE-swap state.
- Per-class property/edge oracles → deepen each to full F1. Build order: eventing → the security-tie
  classes (kms key-policy §1.5, secrets, dynamodb pitr/del-protect) → cloudfront path-map → sns/sqs.
- AE fixes any named property/edge FP/FN per class.

— 3.0.0_SA_CVO
