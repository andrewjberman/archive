> ⛔ **SUPERSEDED IN ONE PLACE, AND IT IS SECTION 3.** Read
> `WIP_IB-rt-9_coldstart2_blocked.md` (same folder) FIRST. **The "one deploy that is owed" below
> CANNOT BE TAKEN** -- all three Terraform roots carry a committed, unapplied
> `handler -> entry.lambda_handler` flip and the `entry` module is in no zip, so the apply that
> lands the `ids.py` fix takes three live functions down (row `IRPT_BCKEND-W3-S26`, measured
> 2026-09-11 ~23:3xZ by extract-and-import, 3 of 3). Section 5's "next free id is W3-S26" is also
> spent: the next free id is **`W3-S31`**. Everything else below still holds.

# WIP HAND-OFF -- IRPT_BCKEND.TO-IB-rt-9, stopped at a managed wind-down

**Written for a SUCCESSOR who has none of my context.** Read this before you read the task
order, because three of its sentences are no longer true and this file says which.

| | |
|---|---|
| Order | `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rt-9.ycharts-session-broker-on-the-fixed-cloud-chain.md` |
| Status | `pending` -- **NOT flipped, and it must not be flipped until arms (b)-(f) pass in one run** |
| Worker | `0.9.0_WK_IRPT_BCKEND~3` |
| Worktree | `C:\tmp\wk-irpt-2-3` (branch `wk-irpt_bckend-2-3`, cut at `684e7eb90a`) |
| My commits | `d3397434d5`, `f83f73ce6c`, plus the commit carrying this file. **LOCAL. Never pushed.** |
| Why it stopped | Managed wind-down: `0.0.0_AB_MSTR` via `2.0.0_SA_COO~B`, 2026-09-11 17:30Z -- *"let all agents know that they need to let their workers finish but prepare for a reboot"*. No ledger, no apply, no publish, no deploy for the rest of that session. |

---

## 1. WHAT IS DONE AND MUST NOT BE RE-DONE

### 1.1 Arm (a) -- THE CUTOVER, EVERY READER. **COMPLETE and PASSING, 0 failures.**

Re-run it before you touch anything else; it takes about 40 seconds and it is the only arm
whose result you can trust without reading code:

```
timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rt_9.py
```

Saved output: `.../deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-rt-9_RT9-AC1_arm_a_output.txt`.
Deciding lines:

```
a1 readers migrated or retired: 4 of 4
a2 legacy any-non-403 probes remaining: 0
a3 new predicate correct on every recorded case: 14 of 14   (old predicate wrong on 10)
a4 END TO END: every probe 400 -> verdict=STALE, SessionFresh=[0.0]
```

What changed in the tree:

- **`infra/aws/lambda/ycharts-session-probe/lambda_function.py` -- REWRITTEN.** The retired
  predicate was `rec["auth_ok"] = rec.get("status") is not None and rec.get("status") != 403`.
  It is replaced by (i) `classify()`, a POSITIVE allowlist -- authenticated iff 200 AND not a
  challenge/login page AND the body parses as the contracted JSON, everything else a named
  member of a closed 13-member refusal vocabulary -- and (ii) `read_session()` / `evaluate()`,
  which REQUIRE the v0.9 versioned bundle with an integer `fence`, re-read the fence after
  probing, and return `SUPERSEDED` (not `STALE`) when it advanced mid-probe. The legacy
  capture invocation is removed. Every outbound call is behind an injected seam
  (`secrets=`, `cloudwatch=`, `fetch=`) and `boto3` is imported inside the handler, so
  importing the module reaches nothing.
- **`infra/aws/lambda/ycharts-session-capture/index.mjs` -- RETIRED IN SOURCE.** The handler
  returns 410 with a `RETIRED` record; the legacy capture body is preserved verbatim beneath
  it as `legacyCaptureHandler`, unreachable. The header says why in full.
- **`infra/aws/terraform/investor-reporting/ycharts/iam.tf` -- HEADER COMMENT ONLY** (W4-S21).
  It names the export root's cross-root `aws_iam_role_policy.render_host_export_evidence` on
  `irpt-ycharts-runner-role`, declared at `infra/aws/terraform/investor-reporting/export/iam.tf:194`.
  **The policy is deliberately NOT moved** -- a cross-root move of an inline policy on a live
  role is a destroy-and-create, and the gap between them is a window where the render host
  cannot write its evidence. No resource changed; a plan of this root must still read
  `No changes` from this edit alone.
- **`infra/aws/lambda/ci/lambda-source-map.json`** -- `ids.py` added to `irpt-export-render`,
  `irpt-status` and `irpt-ycharts-generate`. See section 3.

### 1.2 The two arm-(a) checks that FAILED FIRST, and why you should not "fix" them again

Both first failures were MY instruments, not the world. They are already corrected in
`battery_ib_rt_9.py` and the corrections are commented in place. Do not re-widen them:

- **a1** first counted every code file CONTAINING the string `ycharts/session/current` and got
  7 -- including a COMMENT in `tests/fakes.js`, a data literal in a research script, and this
  worker's own `battery_ib_s_8.py`. The discriminator between a READER and a MENTION is not
  the secret name; it is whether the file calls a Secrets Manager read API. 4 resolve, 3 only
  mention.
- **a2** first fired on 2 lines and both were wrong: the new probe's own DOCSTRING quoting the
  retired predicate (recording a defect is not committing it), and
  `ycharts_session.js:272`, `if (status === 403) ... authenticated: false`, which is the
  CORRECT direction. The detector is now directional (only a NEGATIVE 403 comparison) and
  reads comment/string-stripped source, and it carries a positive AND a negative control.

---

## 2. WHAT REMAINS, IN ORDER

`RT9-AC1` needs arms (a) through (f) to pass **in one run** of `battery_ib_rt_9.py`.

> **THE ACCEPTANCE TOKEN IS DELIBERATELY ABSENT FROM THE BATTERY'S OUTPUT IN EVERY FORM,
> INCLUDING NEGATED.** `RT9-AC1`'s `<expect>` is graded as a REGEX over that output, so a line
> reading `<token>: NOT ASSERTED` would MATCH and the criterion would read PASS on a run that
> proved one arm of six. Add the token to the final line ONLY in the same edit that makes all
> six arms pass. This is the single easiest way to turn this hand-off into a false green.

**(b) FENCING** -- two capture attempts on the fixture: 1 wins, 1 refuses, the published
version unchanged by the loser (printed). The mechanism already exists and is not yours to
build: `infra/aws/ec2/investor-reporting-ycharts/ycharts_session.js`, `acquireLease` (the
conditional DynamoDB update that `ADD fence_token :one`, ~line 379) and `persistSession`
(the fenced write that throws `FenceError`, ~line 771-815). The fakes are in
`infra/aws/ec2/investor-reporting-ycharts/tests/fakes.js` and `battery_ib_s_8.py` already
drives them -- read that battery first.

**(c) ROTATION** -- publish a new version, the replay transport's next invocation uses it, the
old version is refused. `ReplayTransport` is at
`infra/aws/lambda/investor-reporting/ycharts/generate/transport.py:426`.

**(d) EVICTION / SELF-HEALING** -- on the generation job with the replay transport: a 401
mid-job -> ONE broker refresh -> resume at the checkpoint, with the no-resubmit difference
control; a repeat eviction -> `retryable/attention`. The rule is already written and tested:
`transport.resume_allowed(prior_generation, session, refreshes_used)` at `transport.py:202` --
`refreshes_used == 1` EXACTLY, and the session must be genuinely new and verified three ways.
Arm (d) exercises it through the job, it does not re-derive it.

**(f) NOTHING LEFT THE MACHINE** -- 0 external connections across the whole battery, with the
guard log and its denominator. `battery_ib_s_9.py` has the egress guard this should reuse.

**(e) ABSORBED, STOPPED, CONVERGED -- DO THIS LAST AND ONLY WITH ROOM TO FINISH.**
The research root `infra/aws/terraform/investor-reporting/ycharts-research-20260911/` is
absorbed into the ycharts root: a plan showing its resources moving under the ycharts root's
state, `state mv` under a change-management ledger, then the research root deleted from the
tree; host STOPPED (`describe-instances`); the ycharts root's post-apply plan `No changes`;
ledgers CLOSED, sentinels committed. **NEVER-2: open the ledger only with the room to close it
in-session.** My own row `IRPT_BCKEND-W3-S4` is the pattern -- commit the OPEN sentinel BEFORE
the act, commit the CLOSE before the grading reads it. `safe-apply.sh`, never bare terraform.

---

## 3. THE ONE DEPLOY THAT IS OWED, AND IT IS YOUR FIRST ACT

**Row `IRPT_BCKEND-W3-S25`.** `infra/aws/lambda/investor-reporting/_scope/resolve.py:81`
carries `import ids as _ids` at module scope (IB-rt-3's typed identifiers,
`_ids/ids.py`), and `lambda-source-map.json` declared `ids.py` in ZERO of the three functions
that ship `resolve.py`: `irpt-export-render`, `irpt-status`, `irpt-ycharts-generate`.
`enforce.py` fails transitively because it imports `resolve`.

Measured in the `/var/task` layout with the repo stripped from `sys.path`:

```
before:  import closure in the /var/task layout: 6 of 8 OPEN
         [enforce: ModuleNotFoundError, resolve: ModuleNotFoundError]
after :  import closure in the /var/task layout: 9 of 9 CLOSED
```

I fixed the DECLARATION (commit `d3397434d5`). **I did not deploy** -- the wind-down forbade
it. `artifact_sha256` is therefore still the LIVE value and
`registered == S3 content-sha256 == live CodeSha256 == hiVUThOsWCSe304UfRug466Oqv6tqvL/8fjKskUUpoo=`,
read live 2026-09-11. The three live functions serve OLDER bytes and work today.

**The armed part:** the next rebuild-and-deploy of any of those three -- by anyone, for any
reason -- would build, upload, register, match its hash three ways and then die at cold start
on `ModuleNotFoundError`. **`CodeSha256` equality cannot see this, by construction:** a hash
certifies bytes, and nothing in the deploy path ever imports them. The only instrument that
catches it is an extract-and-import in the flat layout with the repo off `sys.path`. Mine is
`.scratch/verify_ycharts_inputs.py` in my worktree (scratch, not committed) -- rewrite it or
lift it, but run something like it before you register any hash.

Per W3-S18: print `artifact_sha256 == S3 content-sha256 == live CodeSha256` for every function
you deploy.

---

## 4. THREE SENTENCES IN THE TASK ORDER THAT ARE NOT TRUE

1. **"`irpt-ycharts-generate` declares 25 build inputs of which 7 have never existed in the
   tree: register the truth (a build input absent from the tree is REMOVED, never invented)."**
   **DO NOT DO THIS.** Row `IRPT_BCKEND-W3-S24`. Measured: **26 declared, 26 resolve, 0
   absent** (27 after my `ids.py` addition). The 8 that do not sit under the entry's own
   `source_dir` are FLAT-PACKAGED shared libraries -- every module lands at `/var/task`, so a
   shared library is declared by basename and resolved from its home package at build time.
   The "7" is what a naive `does source_dir/<name> exist` check returns. Removing them would
   strip `enforce`, `gate`, `keys`, `resolve` and `firm_registry.json` out of the zip -- the
   exact failure in section 3, self-inflicted, and GREEN at every deploy-time rung.

2. **"arm (a) reads 4 of 4 ... with the probe's predicate replaced by a fence read"** -- done,
   see section 1. Nothing about arm (a) is left.

3. **W3-S23 is satisfied.** The amendment's grant of
   `infra/aws/lambda/ycharts-session-probe/` and `infra/aws/lambda/ycharts-session-capture/`
   was used and is spent. Note the grant does **NOT** include
   `infra/aws/terraform/ycharts-pipeline/`, which is where the legacy Lambdas' EventBridge
   rules, ECR repo and IAM live. I did not touch it. If retiring the capture properly needs a
   Terraform change there, that is a BLOCKING row, not an override.

**Trigger state, measured live 2026-09-11, not asserted from the `.tf`:**

```
aws events describe-rule --name ycharts-session-capture-schedule -> DISABLED  rate(72 hours)
aws events describe-rule --name ycharts-session-probe-schedule   -> ENABLED   cron(0 */6 * * ? *)
```

The probe's schedule is ENABLED and the LIVE probe still runs the OLD non-403 predicate every
6 hours (`LastModified 2026-05-22`). The rewrite is in the tree, not in the world. That is not
an emergency -- the old predicate is over-permissive, so it does not false-ALARM, it
false-REASSURES -- but it means `SessionFresh=1` is not evidence of anything until the probe
is redeployed.

---

## 5. OPEN ROWS IN MY COORDINATE

All in `org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md`.
Next free id in my coordinate is **`IRPT_BCKEND-W3-S26`**. Never edit an existing row.

| id | class / hazard | what it is |
|---|---|---|
| `W3-S23` | BLOCKING / ARMED | the two legacy readers outside the grant. **GRANTED by the amendment and now DISCHARGED** -- arm (a) reads 4 of 4. Ready for disposition by the issuer. |
| `W3-S24` | OBSERVATION / ARMED | the "7 of 25 phantom build inputs" premise is false; acting on it is destructive. Disarm owner `2.0.0_SA_COO~B`. |
| `W3-S25` | OBSERVATION / ARMED | `ids.py` packaging gap on three functions. Declaration fixed; **the deploy is owed** (section 3). |

---

## 6. NO PROOF-OF-SPEC INSTANCE EXISTS YET, ON PURPOSE

I did not write
`.../deliverables/0.9.0_WK_IRPT_BCKEND~3/IRPT_BCKEND.TO-IB-rt-9.ycharts-session-broker-on-the-fixed-cloud-chain.proof_of_spec.json`.

The `PENDING-THIS-COMMIT` sentinel is ONE-SHOT: an artifact row pinned with it is only valid in
the commit that carries the artifact, so writing the instance now would burn the sentinel on
five arms that do not exist and leave you pinning artifacts to a commit that has already
landed. Write the instance when arms (b)-(f) pass, pin its artifact rows to the commit that
carries them, then:

```
python .tools/proof-of-spec-check.py \
  org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IRPT_BCKEND.TO-IB-rt-9.ycharts-session-broker-on-the-fixed-cloud-chain.proof_of_spec.json \
  RT9-AC1,RT9-AC2
```

The ids are POSITIONAL and ONLY the exit code is the verdict. rc 0 AND every mechanical
criterion PASS-by-output, then flip `<status>` to `complete` and commit instance, deliverables
and flip together. `RT9-AC2` is `judgment="true"`: it gets its output and NO verdict, under
`UNVERIFIABLE-BY-INSTRUMENT` with a `status_reason` naming `3.0.0_SA_CVO`.

---

## 7. TRAPS THAT COST ME TIME IN THIS WORKTREE

- `safe-commit.sh` force-adds gitignored files under a DIRECTORY pathspec (it once staged a
  685 MB provider binary). **Always pass explicit FILE paths.**
- **Heredoc backslashes arrive HALVED in the Bash tool**, and a heredoc body containing
  `['single-quoted']` can abort the whole call with `unexpected EOF`. Write scripts with the
  Write tool; never build a commit message with `printf` or a heredoc.
- **A rail denial aborts the WHOLE Bash call**, so every later segment in a `&&` chain is a
  SILENT no-op -- including your commit. Put gated reads in their own call.
- A raw `grep` over a directory is denied and routed to `comp-find`; `cmd | grep` as a pipe
  RECEIVER is free.
- `.tools/terraform.exe` is gitignored and ABSENT in a fresh worktree; four roots read `rc 1`
  for want of `terraform init`, and **an rc is not a reading**.
- `safe-apply.sh` has TWO identity gates. `export OPAL_AGENT_SERIAL=...` satisfies only the
  commit-lane one; the halt gate reads `org/mcp/sessions/$CLAUDE_CODE_SESSION_ID.serial`,
  which is gitignored per-session runtime state you must write yourself before any apply
  (row `W4-S2`). **Write it before you need it.**
- Import closure measured in-process reads 6 of 6 where a clean subprocess reads 5 of 6: a
  saved-and-restored `sys.modules` is not isolation. Only a new interpreter is.
