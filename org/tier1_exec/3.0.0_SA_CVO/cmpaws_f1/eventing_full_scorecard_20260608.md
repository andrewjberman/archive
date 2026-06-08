# CMPAWS Eventing Full F1 Scorecard (node + property + edge) — first Wave-2 full cert

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-08 ~16:30Z
**Compiler:** `.tools/comp-aws` @ 2a604aa1e (CVO ran) · **Oracle:** eventing-hand-audit-fixture v0.4 (+ v0.5 corrections below)
**Method:** existence vs live; typing/provenance vs state-union; EDGES vs hand-audited oracle + live event_pattern adjudication.

## VERDICT: CERTIFIED at 1.00 (EV-EDGE-1 fixed + CVO re-verified).
**Update ~16:33Z:** AE fixed EV-EDGE-1 (commit db2122239 — one EMITS_TO per pinned resource-id). CVO
re-verified independently: EMITS_TO 92→95; opal-inf-ec2-state-change-monitor now has 4 EMITS_TO (its
4 pinned instances i-04373615/i-081ae6/i-083ad9/i-0ed5af); opal-data-inf out-degree = 4 (inf-silver-chain
+ inf-assets-trigger + mdpf-daily-refresh-trigger + inf-otp-state-change) — exactly my v0.5 correction.
**Eventing edge-F1 → 1.00. Eventing fully CERTIFIED at 1.00** (node/typing/provenance/properties/edges
all 1.00, brittleness PASS, 0-untyped). First Wave-2 class certified at full marks.

| Axis | Result |
|---|---|
| **Node existence** | 1.00 — 92 EVENT_RULE = live 92; classification 8 event-pattern / 84 scheduled = oracle exactly (post-MDPF_CADENCE-swap) |
| **EVENT_SOURCE** | 70 nodes typed (CLOUDTRAIL_API 2, SCHEDULED 67, CUSTOM 1); origin-totality holds — 92 EMITS_TO = 1 origin per rule, 0 untyped |
| **Typing** | 1.00 — 0 untyped (EVENT_RULE + EVENT_SOURCE all typed) |
| **Provenance** | 1.00 — 78 DECLARED / 14 LIVE-no-DECLARED, 0 residual false-shadow vs state-union |
| **Properties** | event_pattern/schedule/state/event_bus present + correct (mdpf-daily-refresh-trigger post-swap verified: schedule=null, event_pattern=opal-data-inf sentinel ✓) |
| **Edges — TRIGGERS** | 8/8 correct on my hand-audited event-pattern rules (all targets match) |
| **Edges — EMITS_TO typing** | correct on all 8 (the compiler RESOLVED 3 of my oracle's unknowns/assumptions, see corrections) |
| **Edges — EMITS_TO completeness** | **~0.98 — EV-EDGE-1 finding (below)** |
| **Brittleness** | PASS (global pure-discovery, by construction) |

## EV-EDGE-1 (named edge FN for AE — push eventing edge-F1 to 1.00)
**A resource-bound rule that pins N concrete resources should emit N EMITS_TO edges (source fan-in); the
compiler emits exactly 1 per rule.** Anchor: `opal-inf-ec2-state-change-monitor`'s live event_pattern pins
**4 instance-ids** (i-081ae6aafb394fb1a, i-083ad9ae297f88e9f, i-0ed5afded2ebd4ed4, i-04373615f03fbf9a9,
state=stopped) — so it should have **4 EMITS_TO edges** (one EC2_INSTANCE → rule each, the D4 fan-out
applied to the source side), but the compiler emits 1 (i-081ae6 only). ~3 EMITS_TO FN. Same class would
hit any multi-pinned-resource rule. Fix: emit one EMITS_TO per pinned resource id in the event_pattern.

## Compiler corrected MY oracle (cert working both ways — oracle v0.4→v0.5 corrections)
The live event_patterns are authoritative; the compiler read them correctly and exposed 3 oracle errors I'm fixing:
1. `opal-inf-ec2-state-change-monitor`: my oracle guessed EVENT_SOURCE{AWS_SERVICE, aws.ec2}; ACTUAL = RESOURCE-BOUND to 4 EC2_INSTANCEs (pattern pins instance-id). Oracle → 4 EC2_INSTANCE sources. (The compiler's typing is right; only its edge *count* is the EV-EDGE-1 gap.)
2. `inf-otp-state-change`: my oracle had "?"; ACTUAL = S3:opal-data-inf (otp/state.json sentinel). So **opal-data-inf EMITS_TO out-degree = 4** (inf-silver-chain + inf-assets-trigger + mdpf-daily-refresh-trigger + inf-otp-state-change), not the 3 in v0.4.
3. `exec-summary-trigger`: my oracle had "?"; ACTUAL = EVENT_SOURCE{CUSTOM, bd-pipeline.gold-chain, chain-complete}.

## Disposition
Eventing **CERTIFIED** at the full headline (node 1.00 / typing 1.00 / provenance 1.00 / properties ✓ /
TRIGGERS 1.00 / EMITS_TO-typing 1.00 / edge-completeness ~0.98 / brittleness PASS / 0-untyped). EV-EDGE-1
is the one named edge FN (multi-pinned EMITS_TO fan-in) → AE fix pushes to 1.00. Oracle corrected to v0.5
(my 3 errors the compiler caught). First Wave-2 class fully certified.

— 3.0.0_SA_CVO
