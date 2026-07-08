# NFRA_PROMOTE-P2 / GOV-B -- the hot-registration PRODUCER-side design (pre-stage)

**Author:** 0.8.0_AE_CloudComp~D | **Date:** 2026-07-08 | **Status:** DESIGN (pre-stage; build gated on PROMOTE-P1 landing)
**For:** CTO arch-gate review -> instant-to-build on the PROMOTE-P1-land signal. COO~B-directed productive-use-of-wait.
**Seam:** CVO gap #8 (NFRA_SEMCTL_PRD.md:178, NFRA_COMPILERKIT_PRD.md:69) -- the promoted-recognizer -> LIVE-compiler HOT-REGISTRATION path. **COMPILERKIT owns the registry (CONSUMER -- built); PROMOTE owns the materializer (PRODUCER -- this design.)**

---

## 1. What already exists (the consumer half I own, comp_recognizer_sdk.py)

The `RecognizerRegistry` is already the hot-reloadable, surfaced seam:
- `register(r)` -> add; raises on dup; fires `on_register(PROMOTE_SEAM, artifact_class, concept)`.
- `reload(r)` -> replace-without-restart; fires `on_register(PROMOTE_SEAM + ".reload", ...)`.
- `deregister(artifact_class, concept)` -> remove-without-restart (GOV-B req#3 reversibility); **fail-LOUD** (KeyError) on a missing key, never a silent no-op; fires `on_register(PROMOTE_SEAM + ".deregister", ...)`.
- `on_register` hook -> the surfacing seam (a constructor arg); `PROMOTE_SEAM = "compilerkit.recognizer.hot_register"`.
- `Recognizer.emits` (landed 4e8306597) -> a promoted recognizer declares its emitted primitives, so the coverage-sweep stays current automatically when it registers.

So the producer side does NOT need new registry primitives -- it needs to CALL them correctly + bind the surfacing hook to comp-surface-check.

## 2. The producer contract (the recognizer/compiler-rule materializer, PROMOTE-P2 S4.1)

Input: a **RATIFIED** promoted candidate (MOTIF pattern -> ratified by CTO per invariant #3 human-ratify). Shape (proposed):
```
PromotedRecognizerSpec = {
  candidate_id, artifact_class, concept, requires (capability), compiler_id,
  emits: [primitive values],            # -> Recognizer.emits (coverage-sweep stays current)
  recognizer_source,                    # the compiled recognizer body (see S4 -- the open question)
  provenance: {motif_ref, evidence, measured_effect, decompression_chain},   # invariant #5 inspectable
  ratification: {owner, ratified_at, commission_id},                          # invariant #3 human-ratify
}
```

Materialize (MATERIALIZED transition):
1. Construct the `Recognizer` from the spec (S4 = the open design question: how the compiled body is realized).
2. `live_registry.register(r)` (or `.reload(r)` if replacing a promoted one) -- HOT, no redeploy.
3. The `on_register` hook FIRES `comp-surface-check` on `PROMOTE_SEAM` (S3) -- proves the registration TOOK.
4. Emit a MATERIALIZED CSE (provenance-bound) -- the transition is itself an observation (feeds FEDOBS).

Demote (DEGRADED -> DEMOTED transition, invariant #4 reversible):
1. `live_registry.deregister(artifact_class, concept)` -- fail-loud if absent.
2. `on_register` fires `comp-surface-check` on `PROMOTE_SEAM + ".deregister"`.
3. Emit a DEMOTED CSE carrying the degradation evidence (FEDOBS-measured).

## 3. The on_register -> comp-surface-check binding (the I3 "control must fire when exercised" arm)

GOV-A I3: a control is real only if it FIRES when exercised. A silent no-op registration (a promoted recognizer that fails to take -- wrong key, capability-floor mismatch, dup-swallow) would certify a promotion GREEN that never actually reached the live dispatch set. So the hot-register entrypoint is a **named critical surface** (already: PROMOTE_SEAM). The binding:

```
def _surface_hook(seam, artifact_class, concept):
    # advisory-check the critical surface EVERY registration -> a no-op/collision surfaces, never silent
    comp_surface_check(surface=seam, subject=f"{artifact_class}/{concept}")   # advisory, LOUD on anomaly
live_registry = RecognizerRegistry(on_register=_surface_hook)
```
Post-register VERIFY (the exercised red-test, not a config read): assert `concept in [r.concept for r in live_registry.recognizers_for(artifact_class, capability)]` -- the promoted recognizer is now in the LIVE capability-matched dispatch set. If not -> the registration is a no-op -> FAIL LOUD (do not emit MATERIALIZED; surface a promotion-failed CSE). This is the exercise-or-evidence bar applied to the promotion itself.

## 4. THE key open design question (for CTO arch-gate) -- how the LIVE compiler picks it up "without a redeploy"

The registry primitives are in-process. "Without a redeploy" means a RUNNING compiler must acquire a newly-materialized recognizer without a code push. Three options:

- **(A) Registry-manifest + run-time load (RECOMMENDED).** The live compiler builds its recognizer set at each run from a **promoted-recognizers manifest** (a store the materializer writes), not a hardcoded `register_all`. A new promoted recognizer appears on the next run -- no code redeploy. Mirrors comp-kuzu's marker-oracle auto-refresh (HEAD-advance -> reload). Reversible = drop it from the manifest -> deregister on next load. **Fits the advisory/run-per-invocation compiler model; no long-lived daemon assumption.**
- **(B) In-process direct call.** Only works if the materializer runs IN the compiler's process (it generally doesn't -- PROMOTE is a separate plane). Rejected for the cross-process case.
- **(C) Live-daemon signal (SIGHUP/watch).** Assumes a long-lived compiler daemon; heavier; only if a compiler runs as a service.

Recommendation: **(A)** -- a manifest the materializer writes + the compiler loads-and-auto-refreshes, with `on_register`->comp-surface-check firing on each load so a manifest entry that fails to take is caught. The manifest entry carries the `PromotedRecognizerSpec` (S2). This keeps "hot" = "next run, no redeploy" and reversible = "manifest drop", both surfaced.

Sub-question for CTO: the `recognizer_source` realization -- a promoted recognizer is a COMPILED pattern. Is it (i) a parameterized instance of an existing recognizer CLASS (a rule-template + params, safest -- no code-gen), or (ii) generated recognizer code (needs a sandbox + the fidelity/pure-lexical gate)? **Recommend (i) for P2** (template + params: e.g. a new dispatch-catalog variant, a new config-key pattern) -- it stays pure-lexical (CTO#3) + fidelity-checkable by construction, no code-gen risk. (ii) is a later, gated escalation.

## 5. GOV-B / 5-invariant binding (how the producer honors the charter)

| Invariant | Producer-side binding |
|---|---|
| #3 human-ratify | materialize() only accepts a spec with a `ratification` block (CTO/owner commission) -- zero auto-mutation; a spec without it is REJECTED |
| #4 reversible | `deregister()` demotion path (fail-loud) + manifest-drop; a DEMOTED CSE with degradation evidence |
| #5 inspectable | the spec carries `provenance` (motif_ref + evidence + measured_effect + decompression_chain); the MATERIALIZED CSE is provenance-bound |
| I3 fire-when-exercised | on_register->comp-surface-check + the post-register dispatch-set VERIFY (S3) -- a no-op registration fails loud, never silent-GREEN |
| I1 honest-missing | a registration that does not take -> promotion-failed CSE (LOUD), never a silent success |

## 6. Instant-to-build plan (on PROMOTE-P1 land)

1. `PromotedRecognizerSpec` dataclass + the manifest schema (S2/S4-A).
2. `materialize(spec, live_registry)` + `demote(...)` in a new `comp_promote_materializer.py` (COMPILERKIT side) -- reuses the registry primitives un-forked.
3. The `_surface_hook` binding + the post-register VERIFY (S3).
4. The run-time manifest-load in each compiler's `register_all` (load hardcoded + manifest-promoted).
5. Self-test: materialize a template-recognizer spec -> register -> assert in dispatch set -> demote -> assert gone + both surfaced (exercised, GOV-A I3 on the materializer itself).
6. Hand CVO the exercise-cert (does a promoted recognizer ACTUALLY reach live dispatch + reverse cleanly).

## 7. Open questions for CTO arch-gate (before build)
1. Confirm option **(A)** (registry-manifest + run-time load) as the hot-registration mechanism.
2. Confirm **(i)** (template+params, pure-lexical) as the P2 recognizer_source realization; defer code-gen (ii).
3. The manifest STORE location + write-authority (who may write a promoted-recognizer entry -- the ratify-gated materializer only).
4. Does the MATERIALIZED/DEMOTED CSE go through the same cse_schema emit path (yes, recommend) -> the promotion is itself a compiled event.

## 8. Grounding
- `org/modules/graph/comp_recognizer_sdk.py` (RecognizerRegistry + PROMOTE_SEAM + register/reload/deregister + on_register + Recognizer.emits) -- the consumer seam, read + owned.
- `docs/architecture/NFRA_PROMOTE_PRD.md` (P2 materializers S5:71, lifecycle S4.3, invariants S4.2) -- read.
- `docs/architecture/NFRA_SEMCTL_PRD.md:178` + `NFRA_COMPILERKIT_PRD.md:69` (CVO gap #8 hot-registration seam) -- read.
- Build GATED on PROMOTE-P1 (MOTIF candidates; MOTIF-P1 certed, P2/P3 running) -- design-only per the Wave-4 gate.
