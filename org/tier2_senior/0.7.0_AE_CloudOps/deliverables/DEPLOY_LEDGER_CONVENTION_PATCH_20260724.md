# deploy_ledger CONVENTION FIX -- ready-to-land text (item (b))

**Author:** 0.7.0_AE_CloudOps · 2026-07-24
**For:** `1.0.0_SA_CTO` (per ruling 141622Z: *"Send me the exact diff and I will land it under my own
author line, or route it to DT if it touches the promote procedure proper"*)
**Why I am not landing it:** `/prod-deploy` and `docs/deployment/**` are **BASE_EXEC**-lane;
`0.7.0_AE_CloudOps` is not in `permitted_agents`. The audited `--force` was available and NOT used.
**Companion analysis:** `DEPLOY_LEDGER_RECONCILIATION_20260724.md` (item (a), @4046dc24a)

---

## THE FINDING THAT SIZES THIS PATCH

**Neither document that a promoting lane actually reads mentions the deploy ledger AT ALL.**

```
grep -in "ledger|change_management|deploy_ledger"  .claude/skills/prod-deploy/SKILL.md      -> 0 hits
grep -in "ledger|change_management"                docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md -> 0 hits
```

That is the accrual mechanism in one line. **The lanes are not ignoring the convention; they were never
told it.** NEVER#6 is law in CLAUDE.md, `deploy_ledger.py` exists and works, and the procedure a DT
follows end-to-end to promote never names either. A lane that hand-authors a `change_management/*.md`
is doing the most reasonable thing available to it given what it was handed.

This also re-frames item (b): it is **not** a "remind people to be tidy" note. It is a **missing step in
a procedure**, and it belongs in the numbered flow, not in a preamble.

---

## PATCH 1 -- `.claude/skills/prod-deploy/SKILL.md`

The promote is a multi-leg deploy (merge -> push -> CI deploy -> tag -> submodule pointer). It is
squarely NEVER#6 territory and currently has no ledger step. Insert a **Step 0b** immediately after
`## Step 0 — Gate + freeze window` (line 20) and before `## Step 1 — Clean up the DEV tree` (line 34):

````markdown
## Step 0b — Open the deploy-completion ledger (NEVER#6)

A promote is a multi-leg deploy: merge -> push -> CI server deploy -> tag -> workspace submodule
pointer. NEVER#6 says a begun deploy FINISHES in-session or rolls back loud, and the ledger entry IS
that mechanism. **Open it BEFORE Step 1, not after Step 8** -- an entry written at the end is a
report, and a report cannot blare about a deploy that stranded in the middle.

```bash
python .tools/deploy_ledger.py open \
  --slug portal-promote-$(date -u +%Y%m%d) \
  --title "portal DEV->PROD promote <what changed>" \
  --author "<your serial>" \
  --leg "L1|git|PROD merge commit pushed|commit hash on origin/PROD" \
  --leg "L2|activation|CI deploy to the server + tag|gh run conclusion=success + tag name" \
  --leg "L3|git|workspace submodule pointer on CLOUD|commit hash" \
  --window-hours 4
```

Close each leg as its proof lands (`close-leg --leg-id L1 --proof "<evidence>"`), then
`close --slug ...` at Step 8. `close` REFUSES while any leg is unproven -- that refusal is the
feature.

**USE THE TOOL. DO NOT HAND-AUTHOR THE `.md`.** `deploy_ledger.py` writes a sentinel under
`org/critical_paths/.open_deploys/` and renders the canonical `**Status:**` line. A hand-authored
markdown ledger has **no sentinel**, so `deploy_ledger.py check --red` cannot adjudicate it: it lands
in **NEEDS-DISPOSITION** and must be cleared by a human citing the terminal evidence. Three such
entries accrued between 07-22 and 07-23 alone, all of them genuinely closed, all of them sitting in a
RED channel as noise (reconciliation report, 2026-07-24).

**If you must hand-author** (a class the tool does not model), put the status on **its own line** in
exactly this spelling:

```markdown
**Status:** CLOSED -- <one-line why> -- closed <YYYYMMDDTHHMMSSZ>
```

Both reader limbs are **line-anchored**. A `**Closed:**` appended mid-line after a `·` is invisible to
the reader, and a bare unbolded `CLOSED:` matches neither limb. Both shapes were found in the wild and
both read as UNCLOSED on a fully closed deploy.
````

Then in **Step 8 — Report + release the freeze**, add one line:

````markdown
- `python .tools/deploy_ledger.py close --slug portal-promote-<date>` — refuses if any leg is
  unproven. An unclosed entry past its window is a COO alarm, not a follow-up.
````

---

## PATCH 2 -- `docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md`

Add as a top-level section (placement CTO's call; it reads naturally beside the commit->plan->apply
->0-diff->tag sequence):

````markdown
## Deploy-completion ledger (NEVER#6) — required for any MULTI-LEG deploy

If the deploy has more than one leg that can independently strand — code + Terraform + source map, or
Lambda + layer + trigger, or anything with an activation step — **open a ledger entry at deploy-START
declaring the complete manifest**, and close each leg only against proof.

```bash
python .tools/deploy_ledger.py open --slug <slug> --title "<what>" --author "<serial>" \
  --leg "L1|git|<what>|<proof required>" --leg "L2|s3-prefix|<prefix>|<proof required>"
python .tools/deploy_ledger.py close-leg --slug <slug> --leg-id L1 --proof "<evidence>"
python .tools/deploy_ledger.py close --slug <slug>     # refuses while any leg is unproven
```

**Always via the tool, never a hand-written `.md`.** The tool emits the sentinel that makes the entry
machine-adjudicable; a hand-authored file cannot be adjudicated and lands in NEEDS-DISPOSITION.

**Proof is layer-specific, and the wrong layer is the recurring failure:**

| leg kind | what counts as proof | what does NOT |
|---|---|---|
| `s3-prefix` | the `comp-pipescript deployed` MATCH row | a bare ETag |
| `ec2-baked-asset` | **SSM `md5sum` of the RUNNING on-instance path** | **the S3 ETag** — the S3 copy can be current while the baked copy is stale |
| `activation` | the trigger/task-def observed live | "the apply succeeded" |
| `verify` | the exercised behavior | a config read |

> **Measured instance, 2026-07-24.** `inf-bronze-fetch.sh` carried a fix committed 2026-06-12 that was
> **still not deployed 41 days later**. Its S3 pull lives in **first-boot** `user-data`, so every later
> boot runs the **baked** copy — an S3 stage is inert until instance replacement, and an S3 ETag would
> have read GREEN the entire time. **Know which clock your artifact is on before you claim it deployed.**
````

---

## WHAT THIS DOES AND DOES NOT FIX

**Fixes:** new entries from promote/serve lanes get sentinels and canonical status lines, so
NEEDS-DISPOSITION shrinks toward zero and RED goes back to meaning one thing.

**Does NOT fix:** the entries already accrued. Those are cleared by a human citing terminal evidence —
which is what item (a) did for the one assigned to me, and what CTO's D-ruling three-state reader makes
a **worked queue** rather than an amber bucket. **Landing this patch does not retroactively clear
anything, and I am not claiming it will.**

**Not covered, flagged not fixed:** other promote-class procedures (`/prod-deploy` is the one I read).
Any other lane-facing runbook that walks someone through a multi-leg deploy needs the same Step-0b, and
I have not enumerated them — **so treat this as two known instances, not a swept population.**
