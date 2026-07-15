# OPAL_GLDRNS.B1 — G2 draft: the GO-flip injection (INF_AOR_FOLD_ACTIVE trigger→chain env forward)

**archetype:** IMPLEMENT (draft — NOTHING APPLIED)
**agent:** 0.4.0_DS_ClientPlatform~B · 2026-07-15 ~21:2xZ · per CTO 20:54:34Z ("G2 proceed; draft to me before apply")
**0.7.0 coordination:** MCP sent 20:51:56Z (they are DOWN per CTO 20:59:15Z — record lands for revival; deconfliction
trivially satisfied; pending-plan-stray discipline observed below).

## What it does

Makes Andrew's GO one motion: setting ONE TF env var flips the fold ON for the next chain run; unset (the
introduction state and the rollback) is byte-identically today's dark behavior. Mechanism = the existing
TF-managed PERF-ceiling export pattern (`lambda_function.py:452-462`), which already propagates
trigger-env → SSM dispatch_cmd → `orion-gold-dispatch.sh` → chain-step process env, where the deployed
dispatch (ff6b2ff87, deployed today) reads `${INF_AOR_FOLD_ACTIVE:-0}` as the semantic fold switch
(fold-vs-servicing OUTPUT only; chain entry is presence-gated and NOT touched by this).

## The exact hunk (infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py, after :462)

```python
    # OPAL_GLDRNS.B1 GO-flip (2026-07-15): propagate the AoR fold switch into the chain
    # env -- the same TF-managed pattern as the perf ceiling above. UNSET (the default,
    # and the state at introduction) -> empty export line -> the dispatch's own
    # `${INF_AOR_FOLD_ACTIVE:-0}` keeps the fold OFF (servicing basis). Andrew's GO
    # becomes ONE TF apply setting the var to "1". VALUE-PINNED: only the exact string
    # "1" is forwarded -- anything else (typo, whitespace, injection) forwards NOTHING
    # and the fold stays OFF. It gates fold-vs-servicing OUTPUT only; chain entry is
    # presence-gated in the dispatch (R5) and this variable never controls it.
    aor_fold_active = os.environ.get('INF_AOR_FOLD_ACTIVE', '')
    aor_export = (
        'export INF_AOR_FOLD_ACTIVE=1\n' if aor_fold_active == '1' else ''
    )
```

dispatch_cmd change: the format gains one slot — `'{}{}'.format(ceiling_export, aor_export)` in place of
`'{}'` (both export lines precede the dispatch invocation; order irrelevant, ceiling first for stability).

## TF (infra/aws/terraform/inf-pipeline/lambdas.tf)

- **AT INTRODUCTION: ZERO env change.** The var is NOT added to `environment_variables`. The only TF-visible
  change is the rebuilt `inf-pipeline/inf-gold-trigger.zip` artifact. The plan MUST show: env UNCHANGED
  (GOLD_INSTANCE_ID + PERF ceiling + the HOLD reason-string exactly as-is; `INF_GOLD_DISPATCH_RELEASE`
  stays ABSENT — the fail-closed chokepoint design in the module comments is untouched by construction).
- **AT ANDREW'S GO:** add `INF_AOR_FOLD_ACTIVE = "1"` to the env block + apply. One motion. Rollback = remove
  it + apply (empty export returns; dispatch default 0).

## Deploy vehicle + guards (nothing here executed yet)

1. Hermetic unit test FIRST (in the lambda dir): assert dispatch_cmd contains the export line iff env=="1",
   contains nothing on ""/absent/"true"/"0 "/junk (the value-pin proven both directions before any build).
2. Commit (owned-paths: infra/aws is AE-lane — **CTO TO RULE the landing lane**: (a) I commit under B1's
   Andrew-verbatim infra authorization with the audited bypass, or (b) you land the commit. Either way the
   hunk above is the content.)
3. build-and-upload inf-gold-trigger.zip -> `terraform plan` READ IN FULL for the whole inf-pipeline module
   (0.7.0's pending-plan strays discipline: any stray non-mine resource change in the plan = STOP, surface to
   CTO) -> `safe-apply` **-target module.inf_gold_trigger** -> 0-diff re-plan -> tag.
4. Post-deploy APPLIED-truth verify: `get-function` CodeSha256 changed; live env UNCHANGED (HOLD present,
   RELEASE absent, no AoR var); Door-5/Door-6/chokepoint re-checked (the G1 pattern).
5. **Honest exercise disclosure:** under the hold, the refusal fires BEFORE dispatch_cmd construction, so the
   export line cannot be exercised end-to-end until the gated release run — the hermetic test (step 1) is the
   pre-release evidence, and the release run's chain log (`INF_AOR_FOLD_ACTIVE=1` echoed by the dispatch's own
   INFO line at :453) is the exercised proof at the moment it matters. Claimed accordingly, never as
   "exercised" before then (Rule 22a).

## Why not other designs (considered, rejected)

- Env var directly on chain-step Lambdas: the fold consumers are EC2 chain scripts, not Lambdas — the env
  must ride the SSM dispatch; this IS the estate's existing pattern for exactly that (PERF ceiling precedent).
- Hand-editing the dispatch to default ON at release: couples the flip to a code deploy (not one motion,
  not one-motion-reversible, violates "flip at GO is one TF apply").
- Payload-driven flip (event field): any invoker could flip it; a TF env var is deliberate, audited, diffable.
