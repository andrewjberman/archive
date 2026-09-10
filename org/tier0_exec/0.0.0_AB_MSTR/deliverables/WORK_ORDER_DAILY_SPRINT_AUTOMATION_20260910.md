# WORK ORDER — automate the Daily Sprint as a scheduled Lambda

**Author:** `0.0.0_AB_MSTR` · **2026-09-10 ~19:5xZ** · **Status:** MEASURED, NOT BUILT
**For:** the next session of this seat. Andrew: *"i need you to continue this in the next session.
+ yes we have a pattern for this type of operation you should adhere to"*

---

## 1. ANDREW'S WORDS, VERBATIM

> *"DId we ever establish how the /daily-sprint runs in the cloud every time? was that completed?"*
> *"This needs to be an automatic run. Please build it now."*
> *"No claude schedule skill, this should be a lambda with an openai 5.6 call"*

**HE REJECTED THE CLAUDE ROUTINE MECHANISM EXPLICITLY.** Do not re-propose `/schedule`. The build is
a Lambda on a schedule that makes an OpenAI call.

---

## 2. WHAT IS TRUE TODAY — MEASURED, NOT RECALLED

**THE VIEWER EXISTS AND IS REAL.** `infra/aws/ec2/opal-gateway/app/sprint_view.py` serves `/sprint`,
`/sprint/<date>` and `/sprint/archive` behind the ALB sign-in with a roster check, built 2026-08-28,
with its own tests and a Terraform read grant (`daily-reports-iam.tf`).

**NOTHING RUNS IT.** There is no schedule for it anywhere I looked:

| checked | result |
|---|---|
| gateway Terraform schedule expressions | 2 found — `ms-ingest.tf`, `otp-liveness.tf`. Neither is the sprint. |
| this laptop's scheduled tasks | 2 OPAL tasks — estate capture, outset drift. Neither is the sprint. |

⚠ **NOT CHECKED: site Z's scheduled tasks.** A trigger there would not appear in either read above.
Close that before asserting "nothing anywhere".

**THE PUBLISHED RECORD IS THE PROOF, and it is the strongest evidence:**

```
s3://opal-data-portal-v2/daily-reports/
  2026-08-27 … 2026-09-04   nine consecutive days
  2026-09-05 … 2026-09-08   MISSING (four days)
  2026-09-09                published
  2026-09-10 (today)        NOT published
  latest/
```

⭐ **A SCHEDULED JOB DOES NOT MISS FOUR DAYS AND RESUME.** That gap is the answer to "every time":
it ran while a person drove it and stopped when nobody did.

⛔ **PREFIX TRAP, BANKED:** the prefix is `daily-reports/` (HYPHEN). My first read used
`daily_reports/` (underscore, which is the LOCAL folder name) and returned EMPTY WITH NO ERROR —
byte-identical to a real absence. Control: the bucket root lists 8+ prefixes.

---

## 3. THE PATTERN TO ADHERE TO — measured from the estate's own OpenAI Lambdas

Andrew confirmed a pattern exists. These are its parts, read from source:

| part | where | note |
|---|---|---|
| Lambda source | `infra/aws/lambda/<name>/lambda_function.py` | exemplars: `trending_image_generator`, `trending_image_selector`, `security-sweep-comprehensive` |
| OpenAI key | Secrets Manager, secret id **`opal/external-apis`**, field **`openai_api_key`** | via `get_openai_key()` — 5 first-party implementations exist; copy the exemplar's, do not invent |
| OpenAI SDK | vendored as a layer: `infra/aws/lambda/layers/news-trending-deps/python/openai/` | do not pip-install into the function |
| Terraform | `infra/aws/terraform/<name>/main.tf` | 57 components follow this shape |
| scheduling | EventBridge `schedule_expression` | precedent `rate(6 hours)`; a dedicated schedule module exists at `canonical-schwab-si2-schedule/` |
| deploy | **Terraform only** | ⛔ CLAUDE.md: NEVER `aws lambda update-function-code` |
| apply | **`safe-apply`** | ⛔ CLAUDE.md: NEVER bare `terraform apply` |

⛔ **`get_openai_key()` HAS A KNOWN DEFECT — DO NOT COPY IT BLIND.** `.tools/comp-deadgrant.py:60`
records it: in `trending_image_generator` the reader SWALLOWS the failure and returns `''`, so a
missing key surfaces as a downstream `ValueError` rather than at the point of failure. Copy the
SHAPE, fix the swallow — a sprint that silently publishes nothing is the same class of defect this
whole work order exists to end.

---

## 4. ⛔ THE UNSOLVED DESIGN PROBLEM — SOLVE THIS BEFORE WRITING CODE

**THE SPRINT'S SUBSTANCE COMES FROM THE FABRIC'S OWN RECORDS, AND A LAMBDA HAS NONE OF THEM.**

`/daily-sprint` builds its packet from: `comp-state` (self-test gated), a two-fabric git census, the
directives dashboard, open-TO totals, and the day's records. A Lambda gets no repo checkout, no
`org/mcp/` telemetry, and no broker.

So the real question is **WHERE THE PACKET COMES FROM**, and there are three shapes. Andrew has not
chosen one and I did not guess:

1. **Lambda clones the repo.** Self-contained; needs a deploy key or a token in Secrets Manager, and
   a clone of this repo is large. Fabric telemetry under `org/mcp/liveness.json` is GITIGNORED and
   would still be absent.
2. **Something on a fabric box publishes the PACKET to S3; the Lambda reads it and writes the
   prose.** Clean split: the machine that has the facts produces the facts, and the cloud does the
   language. Needs a small scheduled producer on the box.
3. **Lambda composes from what is already in S3** (the estate report, drift artifacts, published
   data) and never touches the repo. Cheapest, and the sprint stops being about the fabric's work.

⭐ **MY RECOMMENDATION IS (2)**, because the sprint's value is "what did the fabric do today", which
only a fabric box can answer — and it keeps the OpenAI call cloud-side as Andrew asked. But this is
his design call, and asking it is the first act of the next session, not the last.

---

## 5. STANDING CONSTRAINTS THAT BIND THIS BUILD

- **VENDOR EGRESS.** Andrew's *"this should be a lambda with an openai 5.6 call"* IS the per-use word
  for OpenAI in this build. It does not extend to any other vendor.
- **"openai 5.6"** is his phrasing for the model. Resolve the exact model id against the API before
  pinning it; do not assume a string.
- **NO ALERT/MONITOR.** CLAUDE.md's standing moratorium bars building a freshness checker or notifier
  around this unless he asks separately. A publisher is not a monitor; keep it that way.
- **NEVER#1** — publishing to `s3://opal-data-portal-v2/daily-reports/` MOVES SERVED OUTPUT. A verified
  DELTA=0 needs no hold; anything else needs the never-widen sign-off.
- **LEDGER** — an MSTR commit touching non-record paths needs an `LD-NNNN`.

---

## 6. FIRST ACTS OF THE NEXT SESSION

1. Put the §4 packet-source question to Andrew with the recommendation. One card.
2. Close the site-Z schedule gap in §2 so "nothing runs it" is estate-wide rather than laptop-wide.
3. Resolve the exact OpenAI model id for "5.6".
4. Then build, following §3, deploying by Terraform through `safe-apply`.
