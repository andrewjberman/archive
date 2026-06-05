# /verify-channel (Mode B PRE-EXECUTION) — ADHC_GLDINC build-PRD pre-propagate gate

**archetype:** VALIDATE
**Agent:** 3.0.0_SA_CVO · 2026-06-05 ~1707Z · Class-1 NOVEL-PRD pre-propagate gate (Andrew APPROVED 46e7f5285, build-GO; COO decomposing)
**Scope:** PRE-EXECUTION (production untouched by design). Components (a) commits + (b) PRD + (c) AC-coverage + (e) Constitution-drift apply; (d) end-to-end artifact trace = N/A (nothing built — pre-build by design).

## Verdict: **CLEAN — PERMIT build /drive. No blocking conditions.** One watch-note (§4a boundary).

This is among the best-gated build-PRDs reviewed — the PRD has the VERIFIER'S OWN discipline baked into its safety gates.

## §2 5-gate soundness (genuinely structural, not aspirational)
| Gate | Structural? | Evidence |
|---|---|---|
| 1 Dual-run parity (oracle stays primary+serving; incremental→shadow `_parity/` prefix, never served key; value-for-value on REAL prod data N≥5 nightlies pre-cutover; WRITE-SCOPED shadow reads real oracle inputs) | YES | §4.1-2. No blind swap; apples-to-apples parity. |
| 2 Phased one-at-a-time lowest-risk-first (P1=watermark plumbing-proof ZERO correctness change; each phase independently dev'd+validated+revertible-one-flip) | YES | §2.2 |
| 3 Reconcile-correctness explicit gate (DS-owned; phase doesn't ship until reconcile proven; restatement trigger on frozen-period late data) | YES | §2.3, §5 |
| 4 Checkpoint primitive first (P0 standalone low-risk) | YES | §2.4 |
| 5 Cost-model drives sizing (output of min Σ runtime×rate, not fixed target) | YES | §2.5, §7 |

## AC-coverage (known failure modes — all covered)
- Incrementalization drift → dual-run value-for-value parity. A_03 76GB memory floor → §3 stateful per-pair cum-unit store (the binding-constraint structural drop). Freeze-baseline correctness → reconcile gate + restatement trigger. **Epsilon-masking** → the float epsilon is EMPIRICALLY-DERIVED-THEN-FROZEN; "any loosening is a re-review event; an epsilon that has to grow is a signal of a real divergence, not a tolerance to widen" (§4.2) — this is the Step-3.5 anti-completion-pressure-erosion defense built INTO the PRD. **Reconcile-path-unexercised** → §4a: they identified that a forward N-night window won't hit historical reconcile-trigger dates (injection/rebaseline/reassignment), so steady-state parity FALSELY PASSES the reconcile path → closed via scoped single-date carve-out. That is "sharpest-test-binds / what degeneracy would my coarse test miss" written into the design.
- **Asymmetric-fail** (incremental more-correct than buggy oracle) = human-review not auto-abandon; oracle is reference, not assumed infallible (§4.2). Sophisticated.

## Step 3.5 (decision-useful + completion-pressure erosion)
- Anti-erosion defense is IN the PRD (frozen-epsilon-re-review). One residual knob to watch at each phase RAVC2: the N≥5-consecutive-clean-nightlies could be pressured down ("ship faster"). MITIGATED structurally — each per-phase production CUTOVER is separately Andrew-gated, so Andrew sees the actual N + parity log + reconcile proof as the RAVC2 closure evidence. Not a pre-propagate blocker.

## Production protection (why CLEAN despite touching prod pipelines)
Oracle stays serving throughout; shadow never writes served keys; per-phase cutover separately Andrew-gated ("approval of the PLAN ≠ blanket cutover"); revertible one-flip; oracle not decommissioned until post-cutover grace window. The BUILD lane (checkpoint primitive, dual-run harness, parity oracle) is production-untouched by construction.

## (e) Constitution-drift subscan: GREEN (CORROBORATE)
PRD explicitly honors Rule 1/18 (Terraform/safe-apply infra), Rule 17 (tier discipline), ds-commit-gate per .py, and NFRA cost-discipline (validate-on-scheduled-nightlies C1, no ad-hoc c6i runs). No authority/mandate drift. axis_constitution_coherence GREEN.

## WATCH-NOTE (not blocking) — §4a is the ONE carved exception to no-ad-hoc-gold-run
§4a scoped single-date reconcile-parity carve-out runs ONE reconcile-trigger date through both paths on a RIGHT-SIZED SMALL BOX (never c6i.16xlarge). Andrew-approved as-recommended + correctly bounded (single date + small box + reconcile-validation-only). This is the one sanctioned exception to `feedback_no_adhoc_gold_runs_validate_on_scheduled_nightly`. The build lane MUST hold that boundary — single-date small-box ONLY, never expand to a full c6i run "while we're at it." Flagging so the boundary is explicit on the record; not a gate condition (Andrew already scoped it).

## Routing
PERMIT — CLEAN, build /drive unblocked. Each per-phase production cutover re-verifies separately (Andrew-gated; the N-night parity log + reconcile proof + cost-model update IS the phase RAVC2 = a verify-channel surface per phase). CC COO+CTO informational.

— 3.0.0_SA_CVO
