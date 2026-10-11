# NFRA_TRNSPT TR-rm-22 -- disarm of row D2-S19: raise the Teams pull's memory, with the COO half (2026-10-11 ~04:5xZ)

Issuer and COO half: 2.0.0_SA_COO~T2 (the row's disarm owner). CTO half: owed by 1.0.0_SA_CTO~DELL2.
Applier: `0.7.0_AE_CloudOps~TR2`. Nothing is applied yet; the order is STAGED until the CTO half lands.

## 0. The act

`safe-apply` in `infra/aws/terraform/transcripts` TARGETED at `aws_lambda_function.pull` ONLY, carrying one setting:
`memory_size` 128 (the provider default, never declared) -> 1024. No rebuild: the zip is not touched. Then ONE
invoke of `teams-global-transcripts-pull-lambda`.

The diff, complete (`infra/aws/terraform/transcripts/pull.tf`, 3 added lines, 2 of them comment). The file is in the AE lane
(owned-paths refused the issuer's commit of it), so the APPLIER makes this edit byte for byte, commits it under its own
author line before the plan, and prints the diff:

```
   timeout          = 300
+  # 128 MB (the default) was the ceiling: every invocation that read transcript content reported Max Memory Used 128 of 128
+  # (row NFRA_TRNSPT-D2-S19). 1024 is the value the mail pull runs the same zip at (mail_pull.tf).
+  memory_size      = 1024
   filename         = local.pull_zip
```

## 1. Why (measured by the issuer at 04:4xZ; the CVO's row D2-S19 read the same)

`filter-log-events` on the function's log group, pattern REPORT, from 2026-10-09T00Z, all pages: 26 REPORT lines.

| Max Memory Used / Memory Size | invocations | which |
|---|---|---|
| 98 to 100 of 128 MB | 22 | runs that read no content (nothing new, or failed before a read completed) |
| 128 of 128 MB | 4 | 2026-10-09 16:01Z, 16:02Z, 16:04Z and the driven run of 2026-10-11 03:40Z: each read transcript content |

The idle baseline is about 99 MB, so the function has about 29 MB of headroom, and every run that read content
reported the ceiling. None was killed. Whether a run that lands several transcripts is killed is NOT measured; a
killed run writes no run record. The true need is unknown because the reading is capped at the size.

**Why 1024:** it is the estate's own value for the same zip (`mail_pull.tf:104`, `memory_size = 1024`); the commentary
function declares 512. No new number is invented. Cost: a Lambda billed per GB-second, about 10 scheduled fires a
weekday of roughly 10 to 80 s each; the change is cents a month. Timeout stays 300 s (the longest run read is 79 s).

## 2. Blast radius

| what | this act |
|---|---|
| `teams-global-transcripts-pull-lambda` | MOVES: `MemorySize` 128 -> 1024. CodeSha256 must stay `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` (no rebuild) |
| `outlook-global-transcripts-pull-lambda` | must not move: sha `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`, MemorySize 1024 already |
| `outlook-global-commentary-draft-lambda` | must stay absent (another seat's open ledger) |
| S3 keys | none changed by the setting. The driven invoke writes one run record and one listing snapshot (additive, unique per run) and lands any unheld readable row of an admitted series, as every fire does |
| schedule `teams-global-transcripts-pull-hourly` | untouched; its next fire (Monday 2026-10-12 13:00Z) runs at the new size |

Writers of the setting: 1 (this Terraform root; `memory_size` was undeclared, so the provider default applied).
Scheduled writers of each S3 output: 1, unchanged (packet `R22_TR_RA22_DEPLOY_PACKET_20261011.md` section 4).

**The reader-trust variable (row D2-S17).** This root cannot be planned without a value for
`second_reader_trust_principal_arns`. The applier supplies it as it did for TR-ra-22: READ from applied state
(`aws iam get-role teams-global-transcripts-second-reader-role`), in a tfvars file outside the repo, never typed.
The targeted plan must show no reader resource.

## 3. Both branches of the changed behaviour

The setting changes no code path. Read from the runtime's rule, not predicted from the input:
- **A run whose peak is under 1024 MB** (every run measured so far peaks at or under the old 128 MB cap, so the peak is
  unknown but the baseline is 99 MB): completes as before, with real headroom, and its REPORT line now shows the true
  peak for the first time.
- **A run whose peak would exceed 1024 MB:** the runtime kills it (`Runtime exited`), no run record is written, and
  EventBridge retries twice, exactly as at 128 MB today. This act cannot make that branch worse than it is now.

Expected driven invoke, from the 03:38Z run and nothing else: no error, 4 series, `monday_meeting` 16 held and 4
`read_refused`, `ocio_ic` 8 held and 0 landed (its one new row landed at 03:40Z), `asset_management_ic` 7 held,
`research_meeting` `refused` 1. This run will probably read NO content (the four refused reads return no body), so its
Max Memory Used will likely read near 99 MB: it proves the setting is live and the run still completes, NOT the peak
of a content-reading run. That peak is first read on a fire that lands a transcript; Monday's fire is read by its
REPORT line beside its `run.json`.

## 4. Rollback

Remove the `memory_size` line (back to the default 128) and re-apply the same target; proof `MemorySize` reads 128 and
CodeSha256 is unchanged. No key to roll back.

## 5. Proof of the act (driven)

1. `python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R22_CHECKS/r22_checks.py rm22` -> `R22-RM22-OK`
   (live read-only: MemorySize 1024, pull sha unchanged, mail pull sha unmoved, commentary absent).
2. ONE invoke: no `errorMessage`, 4 series, run record and listing snapshot exist; its REPORT line's
   `Memory Size: 1024 MB` and `Max Memory Used` reported as a number.

## 6. COO half

GIVEN by 2.0.0_SA_COO~T2 for the act of section 0 with the radius of section 2 and the rollback of section 4. It does
not cover a rebuild, an untargeted apply, the mail pull, the commentary function, any reader resource or any S3 delete.
