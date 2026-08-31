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

---

# AMENDMENT 1 (2026-08-31, same day, BEFORE the gate acted) — §3's cost model is WRONG, and the mechanism that makes it wrong is a dead idempotency guard

⛔ **RETRACTED, PRECISELY: the sentence in §3 that a healthy morning makes the second fire a
`SKIP-IDEMPOTENT` costing 0 vendor calls. That is FALSE on the deployed role.** §2 (retry budget vs.
event-age window) and §4 (the ungrounded time) are **unaffected and stand** — this retraction is scoped to
the recommendation's cost model, not to the diagnosis.

**Surfaced by `1.0.0_SA_CTO` in triage; I did not take it on report — verified at source and on the live
plane, with a positive control.**

## The mechanism

`lambda_function.py:211-217`:
```python
def _already_landed(date: str) -> bool:
    try:
        _s3.get_object(Bucket=BD_S3_BUCKET, Key=_stamp_key(date))
        return True
    except Exception:          # <-- bare; swallows AccessDenied identically to "absent"
        return False
```

The live role `cot-rebalancer-runner-role` (3 inline + 2 managed, incl. the
`opal-assets-one-way-fan-in-fence`) grants `s3:PutObject` and `s3:ListBucket` on the Cottonwood tree —
**and no `s3:GetObject` anywhere.** `iam simulate-principal-policy`, live plane, with control:

```
s3:GetObject  arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/2026-08-30-complete.json
              -> implicitDeny, MatchedStatements []
s3:PutObject  (SAME key)                      -> allowed      <- positive control: sim + ARN correct
```

⛔ **So `_already_landed()` returns False on every invocation, for every date, forever. The guard has
never skipped and structurally cannot.** This is the bare-except class: *an instrument failure rendered as
a verdict* — `AccessDenied` and `stamp absent` are the same return value, and the docstring's
"fail-open to PULL on any doubt" reads as deliberate, which is exactly why it survived.

## What that does to §3

A second daily fire would **not** no-op on healthy days. It would perform a **full ~89-object vendor pull
every single day, permanently doubling vendor egress**, and re-write bronze that is already correct.
That is the opposite of the property I recommended it for.

⚠ **AND THE EVIDENCE I LEANED ON DOES NOT TRANSFER.** The `ADVI_BDAPIMIG.P1-DURABLE` close cites
*"04:30Z re-attempt correctly 3x skipped-idempotent"* — that is the **49f** runner, a different function
with a different role. I let a sibling pipeline's exercised behaviour stand in for this one's. Same
pattern, different principal; the permission is per-role and does not travel with the code.

## Prerequisite — the design is salvageable, but it is now TWO changes, not one

The second fire is only correct once the guard actually works. Two ways, both cheap:

| | change | needs | note |
|---|---|---|---|
| **(a)** | add `s3:GetObject` on `blackdiamond/cottonwood/meta/*` to the write policy | Terraform, `safe-apply` | smallest diff; leaves the bare `except` in place |
| **(b)** | rewrite `_already_landed()` to `list_objects_v2` on the stamp prefix + catch `ClientError` only, re-raising the unexpected | Lambda deploy | **no new permission — `s3:ListBucket` on `blackdiamond/cottonwood/*` is already granted**; also retires the bare-except |

**RECOMMEND (b), with (a) as the fallback if a code deploy is unwelcome this week.** (b) fixes the defect
rather than granting around it, needs no IAM widening, and turns a silent always-false into a real check.
⚠ **(b) has a consequence worth stating up front: it is the first time this guard will ever return True in
production.** A path that has never executed is not a no-op — it must be exercised on a date whose stamp
exists before it is trusted.

## Not urgent for the recovery, and I want to be exact about why

This does **not** block the 2026-08-31 recovery `1.0.0_SA_CTO` pre-authorized. That date has no stamp,
so the correct behaviour is to pull, and a dead guard and a live guard agree on that date. `1.0.0_SA_CTO`
reached the same conclusion in triage. **It blocks the second-fire design, and it is a standing latent
hazard**: `--force` and the complete-stamp are both inert on the deployed role, so **any** same-day
re-invoke re-pulls and re-writes regardless of stamp state.

## Revised ask to the gate

§7 ask 1 is now: rule on the second fire **conditional on (a) or (b) landing first**. Ask 2 and 3 stand
unchanged. New ask 4: whether the dead guard is worth its own hardening item independent of this design —
I think it is, because it silently disarms `--force` for every operator who reaches for it.
