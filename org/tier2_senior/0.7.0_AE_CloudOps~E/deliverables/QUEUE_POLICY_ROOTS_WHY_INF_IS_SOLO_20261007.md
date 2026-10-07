# Why `inf-pipeline` is the only firm pipeline caught by the queue-attribute Deny -- and what that narrows for the owed mapping

**By:** `0.7.0_AE_CloudOps~E`, 2026-10-07 ~15:5xZ, on an Andrew-direct question at the terminal
("why is inflection different from the others? what does inflection do that is so different from the other firms that
it has this solo pattern?"). Measured, not recalled.

**Bears on:** the item `1.0.0_SA_CTO`'s half for `NFRA_CTLPLN.TO-APPLY-7` names as NOT READ BY ANYONE and assigns to
`2.0.0_SA_COO~C` -- whether a Dell-placed project owns one of `globgrph`, `inf-pipeline`, `opal-gateway` or
`partner-etl-ops-alerts`. This note does not answer that mapping. It narrows what to look for and removes one
misreading.

---

## THE HEADLINE

**The six-root list is not firm-shaped and `inf-pipeline` is not on it because of anything about Inflection.** It is
on it because of ONE architectural choice: `inf-pipeline` is the only firm data pipeline that gives EventBridge a
dead-letter queue to write into. The chain is mechanical:

1. Three EventBridge rules in `inf-pipeline` dead-letter on failure.
2. A DLQ needs a sender, and the sender is a SERVICE, not an IAM principal:
   `Principal = { Service = "events.amazonaws.com" }`.
3. A service principal cannot be granted from the IAM side; it must be a policy ON the queue.
4. A policy on the queue is written by `sqs:SetQueueAttributes` -- an access change -- so it lands at the laptop
   under the Deny applied by TO-APPLY-7.

Source, read directly: `infra/aws/terraform/inf-pipeline/eventbridge.tf:165-200` --
`aws_sqs_queue.inf_gold_trigger_dlq` and `aws_sqs_queue_policy.inf_gold_trigger_dlq`, Sid `AllowEventBridgeSend`,
conditioned `ArnEquals aws:SourceArn` on three rules: `inf_canonical_prices_daily` (the nightly fallback),
`inf_gold_incremental_daily` (wired, DISABLED until the incremental-current-day path is armed) and
`inf_gold_full_on_bronze_complete` (the ADVI_INFREF L7 additive trigger).

## THE MEASUREMENT, with its denominator

Declared resource types per root, `*.tf` only (no `.draft` / `.proposed`), counted by regex over the file text:

| root | event rules | SQS queues | queue policies | `dead_letter_config` | `events.amazonaws.com` grants |
|---|---|---|---|---|---|
| `inf-pipeline` | 24 | **1** | **1** | 3 | 3 |
| `bd-pipeline` (49 Financial / Black Diamond) | 20 | 0 | 0 | 0 | 1 |
| `cot-pipeline` (Cottonwood) | 7 | 0 | 0 | 0 | 0 |
| `mdpf-pipeline` | 1 | 1 | 0 | 3 | 0 |

**DENOMINATOR: 4 firm/partner data pipelines.** Separately, all 8 firm-named roots under
`infra/aws/terraform/` -- `49f-value-parity`, `bd-49f-auto-login`, `bd-bucket-lifecycle`, `bd-pipeline`,
`cot-pipeline`, `cot-value-parity`, `served-guard-49f`, `served-guard-cot` -- declare **0 queues and 0 queue
policies** between them.

**A POSITIVE CONTROL was required here and it caught a broken instrument.** A first pass counted with
`grep -hc ... | paste -sd+ | bc` and reported `event rules: 0` and `queue policies: 0` for `inf-pipeline` -- flatly
contradicting the two resources read by eye in that same file minutes earlier. The zeros were a pipeline artefact,
not a reading of the estate. They were discarded and the count re-run in Python with the rule "inf-pipeline MUST show
>= 1 of each, or the instrument is wrong". **A census whose zero contradicts a file you have read is the instrument,
not the world** (CLAUDE.md rule 24(i): a wrong-domain census returning EMPTY gets acted on).

## WHAT THIS REMOVES, AND WHAT IT NARROWS

- **REMOVES a misreading.** The list does not mean firms are treated differently, and it does not mean 49 Financial
  or Cottonwood were exempted. They run 20 and 7 EventBridge rules respectively, so they are not less automated --
  they simply do not dead-letter, so there is no queue, no sender to grant, and nothing for the Deny to catch.
- **`mdpf-pipeline` is the contrast that proves the mechanism.** It HAS a queue and three `dead_letter_config`
  blocks -- the same reliability feature -- and **zero** queue policies. Its DLQ is fed by something already
  authorized on the IAM side, not by EventBridge. Same feature, different sender, no laptop dependency.
- **NARROWS the owed mapping.** The question `2.0.0_SA_COO~C` owes is not "which firms are affected" but "does a
  Dell-placed project own a root that grants a SERVICE principal send rights to a queue". For the four unmapped
  roots the specific objects are: `globgrph` (`item2b.tf:34`, `projection.tf:42`), `inf-pipeline`
  (`eventbridge.tf:175`), `opal-gateway` (`otp-alert-sqs.tf:44`, `coo_critical_alerts`) and
  `partner-etl-ops-alerts` (`ops-alerts.tf:21`). The two agentbus roots (`nfra-agentbus`,
  `nfra-agentbus-alyssa01`) were never a Dell's to apply, per the CTO half.

## WHAT THIS DOES NOT ESTABLISH

- It does not answer whether any Dell-placed project owns one of the four. That read is still owed and is the only
  part with live blast radius: a Dell seat could meet a refused `terraform apply` on a CREATE and not know why.
- It does not revisit the Deny. The Deny is correct as signed and as applied; the question is only who trips it.
- The counts are of DECLARED resources in `*.tf` text, not of live state. A queue policy created outside Terraform
  would not appear. `comp-find` over `infra` returned 46 hits across 12,640 files for `aws_sqs_queue_policy`, whose
  SURFACED band is the six roots above plus a `.draft`, a `.proposed`, and an `infra/system/sdk` module that is not
  a root under `infra/aws/terraform`.

## ONE CORRECTION TO THIS SEAT'S OWN EARLIER WORDING

In answering Andrew this seat first called `inf-pipeline`'s membership "incidental". Wrong emphasis: it is not
arbitrary, it is a direct and predictable consequence of the EventBridge-fed DLQ. The part that held is that it is
not about Inflection's data or its status as a firm.
