# cot-rebalancer-runner — post-heal retry: design note

**Author:** `0.6.2_AE_PartnerETL` · **Date:** 2026-08-31 · **Gate:** `1.0.0_SA_CTO` (production-trigger change, Rule 13 DT/AE lane)
**Status:** DESIGN — proposes, applies nothing. No Terraform written, no deploy.
**Lane authority:** `0.0.0_AB_MSTR` 89878 — *"a production-trigger design change — Rule 13 puts that in the DT/AE lane"*, and *"the alarm moratorium does NOT bind this ... a retry is none of those; it is the pipeline doing its own job."*

---

## 1. The incident, measured

```
2026-08-31 06:00:41Z / 06:01:35Z / 06:03:26Z   3 invocations, all raised:
  RuntimeError: rebalancer /auth/token 200 but no access_token -- session TTL expired?
  lambda_function.py:151 mint_rebalancer_bearer <- :163 Puller.__init__ <- :361 ingest

Landed 2026-08-31:  rebalancer_models 0 · rebalancer_accounts 0 · rebalancer_model_detail 0   -> 0 of 3
Control  2026-08-30:                  1 ·                     5 ·                       83   -> 3 of 3

Cookie healed on its own:  secret blackdiamond/cot/session LastChanged 11:33:37Z
                           cot-bd-session-trigger last event          11:36:40Z
```

**Series sweep (the severity bound):** 1,659 keys, 41 distinct dates, `2026-07-21..2026-08-30` = 41
calendar days. **0 fully-missing, 0 partial.** 2026-08-31 is the **first hole in the feed's life** — this
is a first occurrence, not a chronic silent loss. Denominator printed because the number is the point.

---

## 2. Mechanism — the two parameters disagree, and one of them is uncloseable

`infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf:222-229`:

```hcl
resource "aws_lambda_function_event_invoke_config" "cot_rebalancer_runner" {
  maximum_retry_attempts       = 2       # -> 3 total invocations
  maximum_event_age_in_seconds = 21600   # 6 hours
}
```

⛔ **The retry BUDGET is spent in ~3 minutes; the event-age WINDOW is 6 hours.** The 21600s expresses an
intent — *"we tolerate up to 6h of recovery"* — that 2 attempts on Lambda's async backoff (~1 min, ~2 min)
makes **structurally unreachable.** The window was sized for a recovery the budget cannot wait for.

Today makes the gap concrete: the cookie healed at **11:33:37Z**, which is **inside** the 6h window
(06:00 + 6h = 12:00Z) and **5h30m past** the exhausted budget. The config already encoded the right
tolerance and the retry count defeated it.

⛔ **`maximum_retry_attempts` CANNOT close this — AWS caps it at 2.** The knob that looks like the fix is
already at its maximum. Any design that "increases the retries" is not available.

⚠ **AND THE SURFACE THAT LOOKS LIKE THE ALTERNATIVE IS THE WRONG ONE.** An
`aws_cloudwatch_event_target.retry_policy` (up to 185 attempts / 24h) governs EventBridge's failure to
**deliver** the event. Our invocation **delivered fine** — we have CloudWatch logs of the function running
and raising. A function error after successful delivery is retried by the Lambda async invoke config, not
by EventBridge's retry policy. **Reaching for `retry_policy` here would land a change that reads as a fix,
deploys clean, and retries nothing.** Naming it because it is the plausible-wrong answer, not to knock
down a strawman.

---

## 3. Recommendation — a second idempotent fire

Add a second `aws_cloudwatch_event_rule` → same target, same `input = {"mode":"pull"}`, later in the day.

**Why this is safe by construction, verified at source, not assumed:**

```
lambda_function.py:356  def ingest(now_iso, date, force=False):
lambda_function.py:357      if not force and _already_landed(date):
lambda_function.py:358          print({"verdict": "SKIP-IDEMPOTENT", ...});  return
lambda_function.py:394      # complete-stamp LAST -- only now that all 3 types landed + BOTH gates passed
lambda_function.py:405      _land(_stamp_key(date), ...)
```

⭐ **The complete-stamp is written LAST, after all three feeds land and both gates pass.** That single
property is what makes the second fire nearly free:

| morning outcome | stamp present? | second fire does |
|---|---|---|
| succeeded | yes | `SKIP-IDEMPOTENT` — **0 vendor calls**, ~200 ms |
| failed / partial | **no** (stamp is last) | the real pull — closes the hole |

So the healthy path costs one no-op invocation a day, and the failure path self-heals. It also covers
**any** failure cause, not just auth — which the retry-count framing would not.

**BUILD LADDER:** this is rung 4 (native platform feature) + existing idempotency. No new code, no new
service, no monitor. One rule + one target + one `aws_lambda_permission`.

---

## 4. THE INPUT I COULD NOT GROUND — and it decides the schedule time

⛔ **I cannot derive the correct second-fire time from the repo, and I am not going to invent one.**

`infra/aws/terraform/cot-pipeline/cot-detection-layer.tf:25` — *"cot-bd-session-trigger path; **NOT
TF-managed** -- referenced read-only for IAM."* The component that actually re-seeds the cookie is outside
Terraform, so **its refresh cadence is not in this repo.** What I can see: `bd-cot-keepalive` runs
`rate(15 minutes)` (`:154`), and today's actual re-seed landed 11:33:37Z — **one observation, n=1.** One
sample is not a cadence.

⚠ **AND THE FIRST FIRE'S OWN TIME WAS NEVER CONFIRMED EITHER.** `cot_rebalancer_runner.tf:171`:

```hcl
schedule_expression = "cron(0 6 * * ? *)" # PLACEHOLDER 06:00Z -- exact time = CTO/WS-4 chain-timing confirm
```

**That confirm never happened.** So the runner has been firing for 41 days at a time explicitly declared
provisional against a chain whose timing was never measured. 41 for 41 says 06:00Z is *usually* inside a
valid-cookie window — it does **not** say the placeholder was ever validated, and today is what the
un-validated tail looks like.

**Therefore the real deliverable is one measurement, not one number:** the `cot-bd-session-trigger`
re-seed cadence. Both the second-fire time *and* the still-open WS-4 placeholder resolve off it, and
picking either from today's single 11:33Z sample would be a guess wearing a timestamp.

---

## 5. What this does NOT fix — stated so the note cannot be over-read

- **Not a monitor.** It does not detect or report a hole; it removes one class of hole. A detector is a
  separate question and sits under the standing moratorium.
- **Does not cover an all-day cookie death.** If the chain never heals that day, both fires fail and the
  hole stands. This narrows the window; it does not close the class.
- **Does not backfill 2026-08-31 or any past date.** That is vendor egress on Andrew's word — open, and
  the reason this note exists rather than a repair.
- **Does not touch the auth design.** `ADVI_BDAPIMIG.P1-DURABLE` (self-remint / autologin) is
  `complete-superseded`; nothing here reopens it.

## 6. Cost

One EventBridge rule + target + lambda permission in
`infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf`. Zero application-code change. Steady-state
runtime cost: one `SKIP-IDEMPOTENT` invocation per day (~200 ms, 0 vendor calls). Deploy via `safe-apply`
(Rule: never bare `terraform apply`).

## 7. Asks of the gate

1. **Ruling** on the second-fire approach vs. leaving the runner dying on the day.
2. **Whose lane** measures the `cot-bd-session-trigger` cadence — it is not TF-managed and may sit with
   `0.7.0_AE_CloudOps`. I will take it if it is mine.
3. Whether closing the **WS-4 placeholder** on the 06:00Z first fire rides this change or is separate.
