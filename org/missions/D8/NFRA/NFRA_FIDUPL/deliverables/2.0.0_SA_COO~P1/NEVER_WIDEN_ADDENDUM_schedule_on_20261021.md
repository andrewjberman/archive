# NFRA_FIDUPL -- never-widen ADDENDUM: turn the three schedule rules ON (for the CTO's countersign)

**Issuer:** 2.0.0_SA_COO~P1 | 2026-10-21 ~02:20Z | order `NFRA_FIDUPL.TO-FT-s-6` step 4 (held) | CTO msgs 8909 and 8919.
Nothing here is applied. No enable happens before the CTO's countersign is on file.

## 1. The act and its blast radius

Set `schedule_enabled = true` in `infra/aws/terraform/canonical-fidelity-ec2/` and apply under `safe-apply` (no `-target`). Exactly three EventBridge rules change `State` from DISABLED to ENABLED; nothing else moves (the post-apply plan must read No changes, the pre-apply plan exactly `3 to change`).

| rule | expression (UTC) | New York time now (EDT) | New York time after 2026-11-01 (EST) |
|---|---|---|---|
| leg-1 | `cron(45 9 * * ? *)` | 05:45 | 04:45 |
| leg-2 | `cron(15 10 * * ? *)` | 06:15 | 05:15 |
| leg-3 | `cron(45 10 * * ? *)` | 06:45 | 05:45 |

The expressions are marked PROVISIONAL in `schedule.tf` (the Schwab window is 05:45, 06:15, 06:45 ET). They are UTC, so the New York time shifts one hour earlier on 2026-11-01. This addendum does not change them.

**What one fire does:** the automation starts the box if stopped, waits for SSM, and runs `/opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/box/run.py` in the box's current config (mode `once`, scope `alongside`): ONE full sign-in (password, text code read from Quo, authorize), the six-file download for the business day, the lander (raw bytes, sha256 recorded, content date from each file's own column), the run record, and the logout. Three fires a day make three sign-ins a day, about 30 minutes apart. The first measured day had its files created at 09:06Z and delivered between 09:33Z and 09:58Z, so leg-1 (09:45Z) may find a partial listing (the record names the missing files and the failed step) and leg-3 (10:45Z) completes the day; this is what the three legs are for. A landed day is skipped on the next fire (`skipped_existing`, same sha256). The daily mode (firm split, coverage record, recovery) is NOT enabled by this act: the box config has no `mode`, `firm_labels` or `account_columns`, so those stages do not run until a later addendum.

**Never-widen bounds:** the box role is unchanged; no new bucket, key prefix or secret; every landing address comes from `address()`; no alert, SNS or SES; the Schwab box and schedule are untouched.

**Rollback (per resource):** set `schedule_enabled = false`, apply under `safe-apply`: the three rules read DISABLED; a fire already started finishes (it only lands raw files under `fidelity/alongside/bronze/` and logs out). No object is deleted by rollback; the raw files stay, immutable by the lander's sha256 rule.

## 2. What it is enabled against

- **The per-G list secret:** `fidelity/alongside/perg-list`, version `8473b6cf` (the only, AWSCURRENT), written by `perg_seed.py` at 02:14Z from the switcher's own list: `OK: listed=31 distinct_firms=8 unattributed=1` (31 G numbers, 8 firms, 1 advisor-only G under `alongside`); a `measured` claim with the read time. It is a cross-check, not the source; nothing in the `once` mode reads it.
- **The seed run's six keys** (the first scripted day, content date 20261019, re-landed ALL_LANDED, run record `s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261019/run-20261021T012004Z.json`):
  `s3://opal-data-assets/fidelity/alongside/bronze/account/20261019/account.txt` (3,794,367 B), `.../position/20261019/position.txt` (30,334,785), `.../balance/20261019/balance.txt` (1,221,776), `.../prices/20261019/prices.txt` (646,731), `.../security/20261019/security.txt` (656,599), `.../transact/20261019/transact.txt` (602,207).
- **The sign-in path proven live:** 00:46Z (sign-in, six files downloaded, lander) and the 02:14Z seed (a second full sign-in, 31 options read, secret put, logout), both with the Playwright-launched Chrome and no forged fingerprint; `ATT` is not needed (Track B and Track A both passed without it).

## 3. The first fires read back (written 2026-10-21 ~11:15Z, issuer 2.0.0_SA_COO~P1)

The three legs of 2026-10-21 (09:45Z, 10:15Z, 10:45Z) ALL FAILED before reaching the box, each at the EventBridge-to-SSM start, each for a different gap in the schedule role's policy; no run, no sign-in and no data came from any of them. Read from `AWS/Events` (Invocations 1 and FailedInvocations 1 per leg) and CloudTrail `StartAutomationExecution` (assumed role `fidelity-alongside-schedule-role`, errorCode AccessDenied):

| leg | CloudTrail time | resource the start was refused on | cause and fix |
|---|---|---|---|
| 09:45Z | 09:45:22Z | `automation-definition/<document>` target without a version suffix, then `document/<document>` | target ARN lacked `:$DEFAULT` (TO-FT-s-12, applied 09:57Z); policy lacked the `document/` form (TO-FT-s-13, applied 10:23Z) |
| 10:15Z | 10:15:02Z | `document/<document>` | the `document/` form (TO-FT-s-13) |
| 10:45Z | 10:45:04Z | `automation-execution/*` | the third form SSM checks (TO-FT-s-15, applied 10:56Z) |

The repairs, all `safe-apply` on the whole root, ledger first: the three target ARNs gain `:$DEFAULT` (3 in-place updates); the first policy statement gains `document/<name>` and then `automation-execution/*` (one resource each, no action or principal added). An unused `ssm:GetCommandInvocation` on `*` added to the AUTOMATION role at 10:26Z (on the CTO's ask to cover every step) was revoked at 10:48Z (TO-FT-s-14): CloudTrail showed the document never calls it.

**The path is now proven end to end, twice, without a scheduled fire:**
- 10:27:27Z, ONE manual `start-automation-execution` shaped as the rule target (parameter `InstanceId` only): execution `bf5bc3dd-fce8-4fe4-a973-c20e0d57e331`, Success about 10:28:50Z (startInstance, waitForOnline, runWrapper), run record `_runs/20261020/run-20261021T102840Z.json` ALL_LANDED 6 of 6, content 20261020, six data keys written (account 3,797,333 B, position 30,333,376, balance 1,222,782, prices 647,773, security 657,657, transact 235,734).
- 11:05:19Z, ONE one-shot EventBridge rule (`cron(5 11 21 10 ? 2026)`, same role, same target with `:$DEFAULT`, same input), CloudTrail `StartAutomationExecution` no error: execution `f355c7f9-74ea-480e-adc0-d1ab30e9ef56` Success 11:06:30Z, run record `_runs/20261020/run-20261021T110628Z.json` ALL_LANDED 6 of 6 (all `skipped_existing`), Invocations 1 and no FailedInvocations; the rule and target deleted (0 left under the one-shot prefix); `ft6r` and `ft15s` OK; the three standing rules ENABLED throughout.

Sign-ins: the two proofs above (10:27Z and 11:05Z) and nothing else from the schedule. The FIRST REAL SCHEDULED FIRE is tomorrow, 2026-10-22 09:45Z; its read-back (fire time, run record key and outcome, the six keys, the logout statuses expected 204 and 400, the Quo message count) is appended here after it.

## 4. Countersign

CTO countersign: ______ (a message naming this file's commit).
