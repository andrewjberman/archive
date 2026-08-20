# WIRING PLAN (PROPOSAL) -- precondition-token on the deploy code-artifact put

**Author:** 0.7.0_AE_CloudOps · **To:** 1.0.0_SA_CTO (owner of the deploy-mechanics law, Rules 13/14,
safe-deploy) · **Date:** 2026-08-20 · **Status:** PROPOSAL. **THIS PLAN APPLIES NOTHING.** It is
delivered so that switching the token check on -- Andrew's worded act under the no-gates law -- is
cheap to give, never to pre-empt it. No live path is edited by the C10-PRECOND TO.

## P5 assertion -- no activation, stated and true

`.tools/safe_deploy_core.py` and `.tools/safe-deploy.sh` are BYTE-UNCHANGED by this TO.
- `safe_deploy_core.py` blob sha at HEAD: **5276193e00fd70b67bef1b33198b65fb0a97c9be** (working tree
  clean; `git status --porcelain` empty for both files).
- No global write gate is installed. Nothing is armed. The `put_if_precondition` capability lives
  only in this deliverable dir and is imported by nothing on any live path.

## The bounded class (S0 denominator)

The deploy code-artifact put = safe-deploy's `aws s3 cp` of gold/silver code to the firm trees'
`.../code/` prefixes (Rule 13; PIPELINE_MAP bd/inf/cot/mdpf). Ground-read:

- **2 put PRIMITIVES**, invoked at **5 dispatch sites**:
  - `deploy_file` (`safe_deploy_core.py:524`): `aws s3 cp` (`:549`, UNCONDITIONAL) then a
    `head-object` ETag verify (`:556`). Dispatched at `:1217` (primary) and `:1248` (second target).
  - `mint_bundle` (`:637`): `aws s3 cp --metadata` (`:665`, UNCONDITIONAL) then a `head-object`
    ETag + metadata-echo verify (`:672`). Dispatched at `:975` and `:1164`.
- **2/2 primitives carry a post-put ETag verify today; 0/2 carry an ATOMIC precondition.** The put
  is last-writer-wins; the verify is a separate check-then-act read that confirms "my bytes landed"
  but not "I did not clobber a writer who landed between my read and my put." That interleaving
  window is exactly what the token closes -- and there is a MEASURED incident in this class
  (2026-07-13: a hung `aws s3 cp --quiet` reported success while S3 kept the old artifact; the
  upload-verify existed on 1 of 4 call sites -- CLAUDE.md Git section).

## The proposed change, per primitive (NOT applied)

For each primitive, replace the unconditional `aws s3 cp` + separate head-object with one
atomically-bound `put_if_precondition`:

1. **Token source.** Before the write, take a live token: `read_precondition_token(bucket, key,
   read_window_seconds)`. Both primitives already resolve key-exists-vs-first-mint under the
   S3-membership guard (Rule 13: key-exists=update enforced, 404=loud skip/first-mint) -- the SAME
   distinction the token needs (ETAG for update, PRECOND_ABSENT for first mint). `read_window`
   is DECLARED (the deploy's own bounded window, e.g. the safe-deploy step budget), never defaulted.
2. **The bound write.** `put_if_precondition(bucket, key, body, token)`:
   - update -> `If-Match: <token ETag>` (write iff the object has not moved since the read);
   - first mint -> `If-None-Match: '*'` (write iff still absent).
   This requires switching the primitive from the `aws s3 cp` CLI (which does NOT expose the
   conditional-write parameters) to `boto3.put_object(IfMatch=/IfNoneMatch=)`. That is a real code
   change to `safe_deploy_core.py`, in scope for the ACTIVATION act, not for this build.
3. **The verify step SUBSUMES the current one.** `put_if_precondition`'s verifying re-read replaces
   the existing post-put `head-object`: it confirms the stored ETag equals the put's ETag AND -- the
   thing the current verify cannot do -- refuses to call a put COMMITTED if the store does not
   corroborate it (the hung-cp / m4 class). `mint_bundle`'s metadata-echo check is retained
   alongside (it is orthogonal to the ETag binding).
4. **Rejection handling.** A 412 returns (gate=TRANSACTION, reason=PRECONDITION_CHANGED); the deploy
   STOPS and surfaces (a refused code put fails LOUD TOWARD INACTION -- the safe direction, and the
   reason this class was chosen first over a served key, whose refusal would strand a publish).

## Rung 4 is load-bearing (CTO arch condition 1)

The binding is S3's OWN conditional write -- a native platform feature (Build Ladder rung 4). NO lock
table, NO second store, NO DynamoDB. If any future implementation needs one to work, that is the
mechanism failing its own premise: `put_if_precondition` raises `StopAndSurface` on a runtime that
does not honour the parameter (the probe's ABSENT verdict), rather than degrading into an
unconditional put. Runtime support MUST be proven on the DEPLOYED runtime before activation
(`infra/aws/globgrph/probe_ifmatch_cas.py`, the SUPPORTED verdict; the dev box is not the runtime).

## The activation marker requirement (the no-gates law)

**No wiring lands without an inline `# andrew-asked: <verbatim + date>` marker at each edited call
site.** Switching the token check on for ANY class is Andrew's worded act; CTO/COO cannot gate it
into existence and neither can this plan. The plan's job is to make that word cheap: the capability
is built, exercised on the real plane, and ready to wire the moment he says so.

## The second class (base's nomination), reachable by config

`put_if_precondition(bucket, key, body, token)` is class-agnostic. Base's served-key nomination is
the right SECOND class and stays reachable as a config choice -- a later, SEPARATE Andrew-worded
activation, with its own failure-direction analysis (a refused served put fails toward a stranded
publish, so it wants its own guardrails). Not in scope here.

## Sequence to activation (for CTO to route, when/if Andrew words it)

1. base's spec cert of the Precondition_Token object (S5 sec.1) + the Rule-24 record.
2. CTO arch gate on the object + this wiring plan.
3. Andrew's word to activate on the deploy code-artifact class (the `# andrew-asked` marker).
4. The code change to `safe_deploy_core.py` (cp -> boto3 conditional put) through the normal
   commit -> gate -> push cycle; probe SUPPORTED on the deployed runtime as a precondition of the
   change; same-window rollback ready (revert the primitive to the byte-identical cp).
