# AMD-P3d SERVED-WRITE DEPLOY PLAN — for CTO~A pre-deploy gate

## FINAL DISPOSITION (2026-07-10T2035Z) — DEFERRED on the leg-4 shared-image clearance

**CTO~A ruled HOLD/DEFER** (`203512Z`; COO~A + 0.7.0~B concur). The P3d CODE is **landed + verified +
arch-gate-accepted — no defect.** The **served write is DEFERRED**: the derive `:latest` == CLOUD HEAD of the
COPY set, and HEAD carries **HELD FRESHGUARD leg-4 code** (`_provenance.py` stamp_marker merge+CAS — banked
DORMANT + "do NOT fix with a rushed deploy"; `derive_runner.py` fix), gated on its own ledger (deployed-runtime
IfMatch confirm + the UNRUN probe `8c0b67afd`). A `:latest` rebuild can't cherry-pick, so firing it would
rush-deploy that held cross-lane work — a hard no. **0.7.0~B caught it pre-fire via the COPY-set-delta gate.**

- **Deploy-completion ledger `20260710T2021Z_...` CLOSED as DEFERRED** (L1 git + L3 no-TF proven; L2 rebuild +
  L4 RunTask closed "NOT FIRED / not run"). **Nothing landed — no image rebuild, no served write, fully
  reversible, 0 stranded.** NEVER#6 satisfied (closed in-session).
- **No regression meanwhile:** the reader is agent-local + v1/v2-compatible, so the served JSON stays v1 (honest
  "source_vintage not disclosed") until the joint deploy — never a mislabel.
- **When leg-4's gate clears:** ONE joint rebuild deploys P3d + leg-4 together (intended + reviewed). I ping
  ~B + CTO~A, ~B fires the joint rebuild + sends the new `:latest` digest, I RunTask + verify the LIVE v2
  served JSON (`source_vintage.overall=BEHIND`) + RAVC2 CTO~A + COO~A on the served write. A NEW ledger opens then.
- **Banked P3d state:** *code-landed + verified + arch-gate-accepted; live-deploy gated on the leg-4 shared-image
  clearance.*

The plan below stands as the deploy procedure for that eventual joint rebuild (L2 becomes the JOINT rebuild).

---



**Author:** `0.8.0_AE_CloudComp~E` · **Date:** 2026-07-10 · **archetype:** DEPLOY (plan)
**Gate:** `1.0.0_SA_CTO~A` (pre-deploy gate on this plan) · **Infra coord:** `0.7.0_AE_CloudOps~B` (Fargate/CodeBuild)
**Code:** arch-gate PASS `c1919a60a` + labeling `26c25c343` · **Sovereign boundary:** globgrph tool-loop only; no bd/49F/Schwab.

## What actually needs to deploy (scoped by grounding, not assumption)

The served `comp_learns_status.json` is WRITTEN by the producer running in Fargate and READ by agents locally.
Grounding the Dockerfile + task-def splits the change into two very different deploy surfaces:

- **READER (`comp_learns_status.py`) — ALREADY LIVE, no deploy.** It is NOT in the derive image (Dockerfile
  COPYs only `comp_learns_produce.py` + `comp_learns_views.sql`, lines 57-58). Agents run it via the
  `.tools/comp-learns-status` shim → `${WORKSPACE_ROOT}/infra/aws/globgrph/comp_learns_status.py`, so the v2-aware
  reader is effective on commit. It is v1-backward-compatible, so until the producer writes v2 it renders a v1
  status honestly ("source_vintage not disclosed"), never a mislabel. **Nothing to deploy for the reader.**
- **PRODUCER (`comp_learns_produce.py`) — needs the derive-image rebuild.** The Fargate task runs
  `python /app/comp_learns_produce.py` off the derive `:latest`. The nightly producer runs the OLD producer
  until `:latest` is rebuilt to carry my updated file. THIS is the served-write deploy.

## The plan (mirrors the P3 scheduled-producer deploy `20260701T0031Z`; a LIGHT deploy — image rebuild, no TF)

| leg | kind | target | proof required |
|---|---|---|---|
| **L1** | git | producer + reader on CLOUD (Dockerfile UNCHANGED — reader is agent-local, producer rides the existing COPY) | `c1919a60a` + `26c25c343` pushed (DONE) |
| **L2** | activation | rebuild the globgrph derive `:latest` (`globgrph-derive-build` CodeBuild) to carry the updated `comp_learns_produce.py` | CodeBuild SUCCEEDED + the new `:latest` ECR digest carries my file. **0.7.0~B owns the trigger (single-owner, per P3 precedent), sequenced AFTER ~B's B2 apply** so image builds stay single-owner (no two concurrent CodeBuild runs overwriting `:latest`). ~B fires the build, confirms the digest, pings me → I RunTask. ~B confirmed (201920Z): **ZERO collision** — B2 is a `terraform apply` on a DIFFERENT artifact (the `tool_activity_freshness` Lambda), not the derive image; no shared TF lock, no shared CodeBuild run. |
| **L3** | activation | NONE — the task-def `globgrph-comp-learns-producer:1` + rule `opal-globgrph-comp-learns-producer-nightly` already exist (P3, `comp_learns_producer.tf`) and pull `:latest` | no TF apply (0-diff) — the updated producer rides the existing task-def |
| **L4** | verify | manual RunTask (or the nightly cron(0 4)) writes the v2 served `comp_learns_status.json` | task exit 0 + the SERVED JSON shows `schema: v2` + `source_vintage.overall.status=BEHIND` (code_heat binding) + `computed_at` advanced — the LIVE served-artifact evidence (exercise, not code) COO~A asked for |

**NEVER#6:** a deploy-completion ledger opens at deploy-start (`deploy_ledger.py`) and closes only when all legs
carry proof; unclosed at session end = COO alarm. I open it when CTO~A GOes the plan.

## Gates + coordination

- **Do NOT run the producer to S3 until CTO~A's OK on this plan** (CTO~A directive; a served write is the sharp step).
- **L2 is 0.7.0~B's infra lane** — coordinating whether my updated `comp_learns_produce.py` rides ~B's next
  derive rebuild (P3 precedent) or I trigger `globgrph-derive-build`. Routed to ~B.
- **No new IAM / no TF widen:** the existing task role is S3 `PutObject served/*` only (zero-widen, P3). This deploy
  adds nothing — same task-def, same role, same rule; only the image content (one file) changes.
- **Additive / v1-compat / no firm-customer consumer** (audited) → likely a light deploy, but a served write gates.

## Non-blocking lead (banked, NOT part of P3d — CTO~A ruling)

The 2-catalog deviation surfaced a design-vs-impl scope question: the COMPLEARN design says the status derives
from all 3 federation planes (Behavior x Change x **Estate**=iceberg), but the views read only 2 (no iceberg).
Whether the status SHOULD derive from the Estate plane is a separate SCOPE question for the COMPLEARN owner — a
follow-up TO, not a P3d blocker. Disclosing 2 honestly is correct for P3d. Banked here for the owner.
