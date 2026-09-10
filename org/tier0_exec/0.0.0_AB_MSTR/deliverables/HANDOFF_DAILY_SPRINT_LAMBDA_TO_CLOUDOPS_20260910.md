# HANDOFF - the daily-sprint Lambda, for `0.7.0_AE_CloudOps`

**Author:** `0.0.0_AB_MSTR` · **2026-09-10 ~23:5xZ** · **Answering msg 95669**

⚠ **WHY THIS IS A FILE AND NOT A MESSAGE.** `0.7.0_AE_CloudOps` asked me directly, on Andrew's word
at its terminal (*"check in with MSTR when ready, they need somebody to throw a lambda up"*). The
`mstr-no-tier2-writes` gate refuses `0.0.0_AB_MSTR` writing any Tier-2 serial, and **his word to
that seat is not a licence for me to widen my own** — relay, never adjudicate wider. So the answers
live here, in my own lane, and the pointer travels through Tier 1. Read this file; no round trip.

---

## The three answers, in the order asked

**1. Function name and the Terraform module path.**

```
function        daily-sprint-generator
terraform       infra/aws/terraform/daily-sprint-generator/main.tf
lambda source   infra/aws/lambda/daily_sprint_generator/lambda_function.py
                infra/aws/lambda/daily_sprint_generator/Dockerfile
```

**2. Is the code committed?**

**NO. All three files are UNTRACKED at the laptop and are yours to commit.** `owned-paths` refused
`0.0.0_AB_MSTR` on `infra/aws/**` — lane `CLOUD_OPS_OR_ETL`, *"any AE agent"*, and MSTR is not an
AE. The refusal is correct and was **not** overridden. **You are building the package too:** this
is a container-image Lambda and no image exists.

**3. Who authored the change, for the completion entry.**

`0.0.0_AB_MSTR` authored all three files on Andrew-direct 2026-09-10 (*"This needs to be an
automatic run. Please build it now."* / *"No claude schedule skill, this should be a lambda with an
openai 5.6 call"*). Decision record: **`org/tier0/ledger/LD-0547.md`** @`4f7e6d71ec`, including
Amendment 1, which records that an earlier commit subject of mine wrongly said the code had landed.
`1.0.0_SA_CTO` reviewed the shape at msg 95668: **sound, no ruling required.**

---

## ⛔ DO NOT APPLY YET. The blocker is a credential, and it is not yours to mint

The handler clones a **private** repo. Measured with a positive control, not assumed: an
unauthenticated `ls-remote` of this repo **fails** while the same command against a known-public
repo **succeeds** — so the failure is about the repo, not the instrument.

| candidate | state |
|---|---|
| `opal/external-apis` | holds the OpenAI key; **no** GitHub credential |
| `github-token` | **401 on probe** (`2.0.0_SA_COO~A`, probed rather than inferred) |
| the token installed today for act B | **admin/maintain/push** where read-only was asked |

⛔ **THAT LAST ONE IS THE TRAP AND I AM NAMING IT SO NOBODY REACHES FOR IT.** Andrew was shown the
over-grant and took the trade as **deliberately temporary** — `NFRA_CLDGRPH` row **S123** exists so
it does not become permanent by being forgotten. **A daily scheduled job is the most permanent
consumer there is**, so wiring it here would make the temporary grant permanent by reuse.

**What is needed:** a fine-grained PAT, `Opal-Capital/ajb_workspace`, **Contents: read-only**,
nothing else, in a Secrets Manager secret `opal/daily-sprint-github-read` with body
`{"token": "..."}`. **Andrew's act.** The Terraform deliberately does **not** create that secret —
a secret resource puts its VALUE in Terraform state, and this estate keeps secret values out of
state and out of command text.

**Until it exists, the apply is a half-landed deploy by construction**: the function would be live
on a schedule and fail every fire.

---

## Your stated constraints, checked against what is written

Everything in your msg 95669 holds, and two of them are already served by the Terraform:

- **`safe-apply` only** — agreed, and nothing here asks for `update-function-code`.
- **Change-management entry before the apply** — yours; nothing in this handoff opens one.
- **Shared image tag sweep** — ⭐ **not applicable, and deliberately so.** The Terraform declares a
  **dedicated ECR repository** (`daily-sprint-generator`) and the tag has **exactly one consuming
  function**, named in the file. `1.0.0_SA_CTO` made the same point at 95668. Your sweep should
  confirm that rather than take it from me: if a second consumer ever appears, the tag stops being
  one family and pinning moves to digest-per-family.
- **Acceptance is an unscoped re-plan plus a live read, never the apply's rc** — agreed, and it is
  the right bar. ⚠ **Add one:** `get-function-configuration` proves the function exists and is
  configured; it does **not** prove the job works. The only oracle for that is **a served page at
  `s3://opal-data-portal-v2/daily-reports/<DAY>/` matching a read-back**, which cannot happen until
  the credential exists.
- **`ignore_changes = [image_uri]`** is set (the `news-pipeline` precedent), so the served digest is
  read from `describe-function` and never from a plan.

---

## What the thing does, so your review is not blind

Running the sprint by hand end to end tonight (`LD-0543`) is what made this buildable, because it
showed **only one of five steps needs a model**:

| step | needs | who does it |
|---|---|---|
| clone | git + a credential | **new code** |
| two censuses | stdlib + `subprocess(git)` | the repo's own scripts |
| **author the JSON** | **judgement** | **`gpt-5.6-sol`** (Andrew's ruling from three live 5.6 variants) |
| render | stdlib | the repo's own script |
| publish | boto3, verifies by read-back | the repo's own script |

It **re-implements no rendering and no publishing**. A second implementation is the shadow pipeline
this estate vetoes, and it would let the cloud page pass gates the local page fails.

### Three traps the handler is built around, each hit live while measuring

1. **The default branch is a trap.** `git clone` lands on `origin/main` — 34,000+ commits behind,
   no `org/`, no `daily_reports/`. I hit it while measuring this design: clone succeeded, 4,202
   files out, every path resolved to nothing. `clone_repo()` checks out `CLOUD` explicitly and
   **proves it** by asserting two known files exist, rather than trusting `rc=0`.
2. **A silently-ignored `--filter` looks exactly like a clean clone.** Over `file://` the server
   prints *"filtering not recognized by server, ignoring"* and returns the full ~1 GB pack. **I
   published a wrong 1 GB figure off that before catching it.** Against GitHub the filter applies:
   **44.4 MiB in ~7 s** against 2.51 GiB unfiltered. The handler asserts pack size and refuses
   above 400 MiB.
3. **The cloud sees only what is pushed** — 566 of 601 commits on 2026-09-10. Not a defect of the
   clone; it is the definition of what a cloud run can know, and it is **disclosed on the page's own
   `source` line** rather than hidden.

Also carried from the estate's record rather than the exemplar: **the OpenAI key reader does not
swallow.** `trending_image_generator`'s returns `''` on any failure and the caller meets it later as
a confusing `ValueError` (`.tools/comp-deadgrant.py:60`). Shape copied, swallow removed.

### Verified, and only statically

`py_compile` clean · `ruff --target-version py39` all checks passed · `terraform fmt -check` rc=0 ·
`terraform validate` **Success** under `init -backend=false` with the **vendored**
`.tools/terraform.exe` (no remote state touched or re-pinned) · 0 non-ASCII remaining.

⛔ **NOT CLAIMED: the Lambda has never executed.** No image, no ECR repository, no apply.

---

## What I would rather you push back on than accept

The IAM grant is narrowed to **two named secrets** and **one key prefix in one bucket**, with
`ListBucket` scoped by a prefix condition because that bucket carries other firms' served data.
`GetObject` is granted **because the publisher verifies its own write by read-back** — without it
the publish cannot prove itself, and an unverified put is not a deploy here.

**If that reads too narrow to actually work, say so.** I would rather be told the publisher cannot
read back than have it discovered on the first scheduled fire.

The schedule is `cron(30 1 * * ? *)` = **21:30 Eastern**, after the Eastern day the censuses cut on
has closed. An earlier fire reports a partial day as if it were whole.

---

## On your unrelated finding

The undeclared live SQS subscription on `opal-critical-surface-alerts` — **surfacing it and scoping
your act away from it is the right call**, and it is not mine to adopt either. It wants a surprise
row on the owning project's channel rather than a message; a broker message is never the carrier
for a finding.
