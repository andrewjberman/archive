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

## 3. The first fire read back (filled after the enable)

After the apply, the first scheduled fire is read and appended here: the fire time, the run record key and its `outcome`, the six keys landed or `skipped_existing`, the `logout` statuses (expected 204,400), and the Quo line's message count (one text per sign-in). If the first fire fails, the issuer disables the rules the same turn (rollback above) and reports the step.

## 4. Countersign

CTO countersign: ______ (a message naming this file's commit).
