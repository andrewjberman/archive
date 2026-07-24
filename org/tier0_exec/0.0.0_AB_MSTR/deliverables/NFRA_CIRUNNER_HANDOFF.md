# NFRA_CIRUNNER — Self-Hosted GitHub Actions Runner on EC2

**LIVING DOCUMENT — for issuance to `1.0.0_SA_CTO`.**
Maintained by `0.0.0_AB_MSTR`. Andrew-direct: *"just make sure everything is documented and keep that
documentation updated for issuance to CTO later in the session. I do not want to bother them just yet
because we are working closely on key MDPF logic."*

**CTO HAS NOT SEEN THIS.** Deliberately withheld at Andrew's instruction while the MDPF arc is live.

| | |
|---|---|
| **Status** | **BUILT · APPLIED · REGISTERED · ONLINE — NOT ACTIVATED** |
| **Instance** | `i-05b5a6dc2a94f164e` (t3.medium, us-east-1d, private IP 172.31.14.52) |
| **Role** | `arn:aws:iam::313476888478:role/github-actions-runner-role` |
| **TF root** | `infra/aws/terraform/github-actions-runner/` (state key `github-actions-runner/tfstate`) |
| **Commit** | `683e06ceba` (authored `0.7.0_AE_CloudOps`, built by MSTR — see Provenance) |
| **Last updated** | 2026-07-24 ~19:20Z |

---

## 1. Why this exists

**Andrew-direct 2026-07-24 ~1750Z, VERBATIM:**
> *"lets just set up a self hosted EC2 runner so we dont have to commit resources to this locally"*

Preceded by, when MSTR moved to delegate it:
> *"Listen CTO is busy so after you finish clearing this, lets just set up a self hosted EC2 runner"*
> *"Just proceed with the EC2 dedicated runner please, thank you"*

**The trigger:** GitHub Actions went **billing-blocked org-wide at ~14:22Z**. Jobs are *refused before a
runner is assigned* — `steps=0`, `runner=""`, ~2s, **no log at all**. Verified independently on both repos;
`0.2.0_DT` positive-controlled the discriminator against a genuine ESLint failure (steps=16, real runner,
real log), so refusals are cleanly separable from ordinary red CI.

**Andrew's binding constraint, VERBATIM:**
> *"Git is not allowing us to adjust billing information at this time, and we cannot just wait 48 Hours to
> do this work."*

**Self-hosted runners are free and unmetered on private repos** — only GitHub-*hosted* minutes bill. That is
the entire economic basis.

> ### ⚠ THIS IS A 48-HOUR UNBLOCK, NOT AN ARCHITECTURE DECISION.
> It must revert to `runs-on: ubuntu-latest` + `terraform destroy` once billing clears. Recorded here, in
> the TF header, in the manifest entry, and in the commit message — **a workaround that becomes permanent
> by default is a decision nobody made and everybody inherits.**

---

## 2. What is DONE, and how it was verified

| step | state | evidence |
|---|---|---|
| Terraform written | DONE | `main.tf`, `runner.tf`, `runner-iam.tf` |
| `init` / `validate` | PASS | clean |
| `plan` | **6 add / 0 change / 0 destroy** | purely additive, nothing existing touched |
| Commit | DONE | `683e06ceba`, AE lane |
| **Apply** | **DONE** | via `safe-apply.sh`, 6 added / 0 changed / 0 destroyed |
| Bootstrap | DONE | cloud-init `Success` in 78.7s; runner staged (219MB); python3 + awscli present |
| SSM | Online | `PingStatus=Online` |
| **Runner registration** | **DONE — BOTH** | **verified at GitHub, not at the box** |

**Registration verified from the ORACLE side** (`gh api .../actions/runners`), never from the box's own log:
```
ajb_workspace   count=1   opal-ec2-ajb_workspace : online : not-busy
portal          count=1   opal-ec2-portal        : online : not-busy
```

---

## 3. ⛔ THE ONE REMAINING STEP — AND IT IS CTO'S, NOT MINE

**The runners are ONLINE and IDLE. They will claim nothing until workflows point at them.**

Every workflow still declares `runs-on: ubuntu-latest` (22 jobs across 13 workflows). Flipping them to
`self-hosted` is the activation.

**`.github/**` is lane `BASE_EXEC` (CTO / COO / CVO). MSTR is Tier-0 and is NOT in that lane.** I did not
attempt it and did not seek an override.

**RECOMMENDED MINIMAL SET** — restore the business-critical path, smallest blast radius:

| workflow | repo | why |
|---|---|---|
| `deploy.yml` | portal | the only path that ships the site — blocks the MDPF promote |
| `surface-check.yml` | portal | the blocking gate on model-portfolio surfaces; MDPF touches exactly these |
| `ci.yml` | portal | build/typecheck ahead of deploy |
| `ec2-deploy.yml` | workspace | the only genuinely blocked *deploy* path in the workspace |

**Deliberately NOT recommended for the flip:** the drift/parity/comp-test workflows. They are *guards*, they
are survivable for 48h, and each conversion is blast radius for no unblocked work.

> **`lambda-deploy.yml` MUST NOT be treated as blocked.** Its own header states: *"Reports drift but does
> NOT deploy — all deploys go through terraform apply."* **Lambda deploys were never blocked.** An earlier
> fabric-wide message said "C1/C2/C3 cannot be landed until billing clears" — that is **over-broad** and was
> corrected to COO at 174221Z before his TOs landed.

---

## 4. Design decisions, and the measurement behind each

**Sizing — `t3.medium` (2 vCPU / 4GB), ~$30/mo always-on.** From *measured* durations of the last
successful runs, not guesswork:

| | median | max |
|---|---|---|
| workspace CI (n=25) | **58s** | 265s |
| portal CI | **122s** | 142s |
| portal deploy (build → s3 sync → CloudFront invalidation) | **127s** | 136s |

**Always-on is FORCED, not preferred.** A runner must be *online* to claim a job. The start-stop-ephemeral
pattern used by `canonical-schwab-runner` **does not transfer** — a push arrives, a stopped runner never
claims it, and the job queues silently. That silence is this estate's favourite failure shape.

**Economic note worth CTO's eye:** measured demand is a few hundred minutes/month, which sits *inside* the
GitHub free tier. **So the block is almost certainly a FAILED PAYMENT, not an overage.** This box buys 48h
of unblocked work; it is not a cheaper steady state. Destroy it when billing clears.

**Network** mirrors the proven `bd-gold-layer-runner` lineage — no novelty. **All four IDs re-verified LIVE
2026-07-24** (ami / subnet / sg / keypair). The pattern's own comment verified them **2026-06-29**, and a
month-old network ID is exactly the aged-record class (**LD-0338**), so they were re-checked rather than
inherited. All four still valid.

**IMDSv2 required** — a CI runner executes repository code, so SSRF-to-credentials is a real path.

---

## 5. Credentials — NO GITHUB TOKEN EXISTS ON THIS BOX

**Andrew-direct: *"we don't use any GitHub PATs."***

The first draft granted `secretsmanager:GetSecretValue` on `github-token` so user-data could self-register
at boot. **That grant was REMOVED**, and the design is better for it:

- a runner **registration token** is single-use and lives ~1 hour;
- once `config.sh` runs, the agent holds **its own** credentials and never needs the minting identity again;
- so the token is minted from an already-authenticated operator session at registration time and passed over
  SSM. **Nothing long-lived is stored. There is no PAT to rotate, leak, or silently expire.**

> ### 🔴 PRE-FLIGHT FINDING — the existing `github-token` secret is DEAD (HTTP 401)
> Expired or revoked. **A boot-time self-registration would have succeeded at building the instance and then
> failed to register — presenting as a healthy box that simply never claims a job.** Found only by
> *exercising* the mint path instead of assuming the secret was good.
> **ACTION FOR ANDREW (open):** delete the stale `github-token` secret from Secrets Manager. It grants
> nothing and is unowned surface.

> ### 🔴 CREDENTIAL EXPOSURE — disclosed, self-reported
> While pre-flighting, MSTR queried the secret with `--output text` and **printed the full PAT into the
> session transcript.** That was an error; a secret value should never have been rendered.
> **Mitigation: the exposed token is already invalid (401), so it grants nothing.** It should still be
> deleted as hygiene. Recorded here rather than only in chat, because a disclosure that lives only in a
> transcript is not a record.

**Registration scope:** org-level returns **403** (needs `admin:org`; the CLI token carries
`gist, read:org, repo, workflow`). Hence **two per-repo agents on one box** — a supported configuration.
If `admin:org` is ever granted (`gh auth refresh -h github.com -s admin:org`), a single org agent replaces
both and serves every future repo.

---

## 6. ⚠ THE TRUST-BOUNDARY DELTA — CTO'S TO ACCEPT OR REFUSE

`lambda-deploy.yml` and `drift-producer-push.yml` assume AWS roles via **GitHub OIDC**.

- On a GitHub-**hosted** runner, those credentials live for minutes inside a disposable VM nobody owns.
- On **this** box they materialise on infrastructure **we own and keep**.

OIDC trust policies are scoped to repo+branch and **need no change** — the token still comes from GitHub.
**But the blast radius of a compromised runner becomes persistent.**

**This is a real delta and MSTR did not wave it through.** It is stated in `runner-iam.tf` rather than
buried. It is also *why* the instance role is pinpoint: **the role carries no deploy permissions, so a
compromise gets one path and not two.**

**Role grants — exhaustive:** `AmazonSSMManagedInstanceCore` + CloudWatch Logs on one log group ARN.
**Deliberately absent:** `secretsmanager:*`, `ec2:*`, `s3:*`, `iam:*`.

---

## 7. Provenance — and one thing CTO should know about how this was built

**MSTR built infrastructure.** That is outside the observer scoping, and it happened because Andrew
**explicitly declined delegation twice** — first *"CTO is busy,"* then interrupting a spawn with *"Just
proceed with the EC2 dedicated runner please."*

**Two gates caught MSTR during this build, and MSTR stopped at both rather than overriding:**

1. **owned-paths blocked the commit** — `infra/aws/**` is an AE lane; MSTR is not an AE. **No `--force`, no
   audited override.** Routed to `0.7.0_AE_CloudOps`, which reviewed the files as its own and signed them
   into its lane at `683e06ceba`. **CloudOps caught two real defects in review:** a role `description`
   claiming `secret-read` the role does not hold, and a leftover comment describing the deleted
   secretsmanager grant — *both the comment-outliving-its-mechanism class this estate ledgered today.*
2. **`.github/**` is BASE_EXEC** — the workflow flip is not MSTR's either, and was not attempted. It is
   §3 above, waiting for CTO.

**MSTR did not gate its own apply in the normal sense** — the apply proceeded on **Andrew's explicit
sovereign GO** (*"You have my go"*), not on MSTR's own authority, and with CTO deliberately not consulted at
Andrew's instruction. **CTO should know that his gate was bypassed by the sovereign, not by an agent**, and
is free to review, amend, or destroy any of it.

**Rule 12 note:** `register-runner.sh` reached the box from **S3** (`s3://opal-ci-staging/github-actions-runner/`)
via a **presigned URL** — chosen so the instance role needed no `s3:*` grant. The artifact came from the
artifact store; the role stayed pinpoint.

---

## 8. Reversal procedure (when billing clears)

1. Revert the flipped workflows to `runs-on: ubuntu-latest` (BASE_EXEC lane).
2. Confirm a run actually lands on GitHub-hosted: **`runner_name` non-empty AND `steps > 0`.**
   > **A still-refused run is byte-identical to the same instant failure. Never read the first green as
   > meaningful without asserting `runner_name`.** On a self-hosted runner `runner_name` is the *host*, so
   > this same check also discriminates "ran on our box" from "ran on GitHub."
3. `terraform destroy` in `infra/aws/terraform/github-actions-runner/`.
4. Remove `github-actions-runner` from `EC2_MANIFEST.json` (28th service).
5. Delete `s3://opal-ci-staging/github-actions-runner/`.

---

## 9. Open items

| # | item | owner |
|---|---|---|
| 1 | **Flip the minimal workflow set to `self-hosted`** — §3. Nothing is unblocked until this happens. | **CTO** (BASE_EXEC) |
| 2 | Accept or refuse the **OIDC trust delta** — §6 | **CTO** |
| 3 | Delete the dead `github-token` secret | **Andrew** |
| 4 | Optional: grant `admin:org` to collapse two agents into one org runner | **Andrew** |
| ~~5~~ | ~~Verify `bun` for the `ubuntu` user~~ — **CLOSED**, see below | ~~MSTR~~ |
| 6 | Clear the GitHub billing block, then execute §8 | **Andrew** |

### Item 5 CLOSED — toolchain verified on the instance (2026-07-24 ~19:25Z)

```
bun      1.3.14          (installed for the ubuntu user, portal build dependency)
python3  3.10.12
aws-cli  2.36.7
systemctl is-active actions.runner.*  ->  active, active     (BOTH agents)
```

**Both runner agents corroborated on TWO independent signals** — GitHub's API reports `online`, and systemd
on the box reports `active`. Neither alone would be sufficient: the API can lag, and a systemd unit being
"active" says nothing about whether GitHub can reach it.

⚠ **One thing for the flip:** the box has **Python 3.10.12**; this workstation runs 3.12. If any workflow
depends on 3.12-only behaviour it will behave differently on the runner than it did on `ubuntu-latest`.
Not a blocker, but it is the kind of environment delta that surfaces as a mysterious test failure rather
than as an obvious one — worth a `setup-python` pin in any workflow that cares.
