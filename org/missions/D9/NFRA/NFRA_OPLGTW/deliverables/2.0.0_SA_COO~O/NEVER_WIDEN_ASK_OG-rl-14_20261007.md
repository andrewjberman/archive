# Never-widen ask -- OG-rl-14, the r28 opal-gateway release on live 510c8cfed2 (round 29)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-07 ~21:2xZ.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-14.gateway-release-r28.md`, with A1
  (@6ed67c659f). Cut to `RELEASE_ORDER_FORM.md` (@eee9b52ced: the fetch control R45 is in it).
- **Spec:** `ledger/ROUND_ANALYSIS.round27.md` @f6fd7281cf: R39, R40, R43, R45, R46, and the round-29 list.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~28/ANNOUNCE_OG-rl-14.md`, worker commit `83842e8e8c` on branch
  `wk-NFRA_OPLGTW-26-28`.
- **Release sha the halves sign:** `aa75078e1b72a28219e6148d3ec8e9bf705ea111`, branch `rel-nfra-oplgtw-r28b`
  (`/c/tmp/og-rel24`). The first cut, `419297b525` on `rel-nfra-oplgtw-r28`, is superseded: it left three tests red.

**Halves owed, all three against THIS file at its commit:** `1.0.0_SA_CTO~Z` (CTO); `3.0.0_SA_CVO~Z` (CVO); `2.0.0_SA_COO~O`
(COO, signed in section 7).

## 1. The bytes -- the issuer's own reads at 21:17Z

- `aa75078e1b` is ONE commit on live `510c8cfed2` (`git rev-list --count` = 1; its parent is the live sha).
- `git diff --name-only 510c8cfed2 aa75078e1b`: 8 files, all in the gateway tree.
- `git diff --name-only aa75078e1b CLOUD -- infra/aws/ec2/opal-gateway` at CLOUD @33e8bbe318: one line, the CLOUD-only
  `runbooks/SCHWAB_PILOT_RUNBOOK.md`.
- Each release blob equals its cell's blob, 8 of 8: 2 against OG-lk-1 @3e1b858b63, 6 against OG-bi-1 to bi-4 @90a85c5706.
- Not in the diff: the gateway's `requirements.txt`, any `bun.lock`, `app/integrations/opal_portal/integration.py`. So
  the CTO-first term of msg 31254 does not fire and the send-path timing rule does not bind.

| File | Reaches the host | What |
|---|---|---|
| `app/audit.py` | YES, the only one | the lake key builder `_lake_key` (OG-lk-1) |
| `deploy-to-ec2.sh` | no: it is the deploy tool, run on this box | the pre-check before the dashboard install; the host's `--upgrade pip` line removed (OG-bi-1, bi-2) |
| `ops/bun_cache_precheck.py` | no: the deploy tool's pre-check | a lockfile entry counts as cached only with a `package.json` naming its exact name and version (OG-bi-3) |
| five files under `tests/` | no | tests, among them the base-guard rig (OG-bi-4) |

**Worker's measurements (ANNOUNCE):** host md5 97 of 97 equal to live; the deploy's own tar command on the release tree
lists 97 files, 0 under `ops/` or `tests/`; tests 652 passed and 7 failed, the same 7 ids as on live, 0 new
(`test_deploy_base_guard.py` 8 passed); rollback tree `/c/tmp/og-rb22` at `510c8cfed2`, 97 of 97 equal to the live
artifact.

## 2. THE SCRIPT THAT RUNS, and its install lines (for the CTO half; read from the release tree at `aa75078e1b`)

The deploy runs `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` FROM THE RELEASE TREE, so it is the changed script. This is
the first deploy under it.

| Line | On | What it does |
|---|---|---|
| 206-211 | this box | one subshell under `set -euo pipefail`: finds a python, runs `ops/bun_cache_precheck.py bun.lock`; on a miss prints `ERROR: bun cache miss` with the list and exits before the install; only then `bun install --frozen-lockfile && bun run build` |
| 308 | the EC2 host | `pip install --progress-bar off -r requirements.txt` (unchanged; the gateway's `requirements.txt` is not in this release) |

- The host's `pip install --upgrade pip` line is gone.
- Pre-check against the real dashboard lockfile and the real cache: 77 of 77 (worker, Phase A; taken again before
  Phase B).
- **UNDETERMINED:** whether a frozen install with every entry cached still sends a metadata request to the registry
  (`deliverables/0.9.0_WK_NFRA_OPLGTW~33/BI3_METADATA.md`). No package is fetched either way.
- **What the pre-check does not prove:** a partial extraction that kept its `package.json` passes it. R45's control
  below is the catch for that.
- Census lines for this script: `org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/SITEZ_INSTALL_DOWNLOAD_LINE_CENSUS_20261007.md`
  @543bee5743 listed `:207` (bun) and `:303-304` (pip) on the earlier bytes; they are lines 211 and 308 here, and 303 is
  removed.

## 3. Blast radius -- what the act may touch

**One movement of served behaviour.** A lake object written for a record that carries no usable `ts` gets a key with a
time part, `audit/dt=<day>/<ts>-<id>.jsonl`, the time being the writer's own UTC clock.
- Before, on the installed code: that record's key has an EMPTY time part (the object found today, row Z-W28-S26).
- Rehearsal, on the staged bytes: non-empty time part, day equal to that time's day; a record with `ts` gets the same
  key shape as before; 0 of 4 records changed by the builder; 0 lake objects written by the rehearsal.
- Writers of a lake key: N = 1, `_emit` through `_lake_key` in `app/audit.py`. Records reaching it with no `ts`: one
  known writer, `taxsma_workbook._audit` (`deliverables/0.9.0_WK_NFRA_OPLGTW~34/LK1_CAUSE.md`).
- Keys already written stay as written. Nothing is renamed, moved or deleted in the lake.

**Unchanged:** every record's fields; every route, tool, identity and grant; tools 66; the concierge's consent 9; `.env`;
the state store (0 writes); Terraform, IAM, the ALB, secrets. **Manifest:** `deployed_commit` moves; previous value
`510c8cfed2`. **Rollback, one act:** redeploy `/c/tmp/og-rb22`.

## 4. Both branches of each named property

- **The key of a record with no time.** Expected: a stamped key. Other branch: the time part still empty: roll back.
- **The key of a record with a time.** Expected: unchanged shape. Other branch: any change: roll back.
- **Whether the deploy fetched (R45).** Expected: 0 bun cache entries created or modified since the deploy command
  started. Other branch: above 0. That is a fetch: the criteria are not run, a BLOCKING row is filed, the release
  rolls back and comes to the CTO.
- **The host's pip step.** Expected: every line `already satisfied`. Other branch: a `Collecting` or `Downloading` line.
  That is reported as a finding; it is not a rollback trigger, because whether the host is a box under Andrew's
  no-fetch word is his to say and unanswered.

## 5. Limits

- **(a)** The stamp is the WRITE time, not the record's own `observed_at`. For the one known writer the two differ by
  the call's latency.
- **(b)** The lake key reads call the builder on installed code; no object is written to the lake by any check.
- **(c)** R45's count reads creation and modified times of cache entries to depth 2. A fetch that rewrote a file deeper
  than that without touching its entry directory's times would not be counted.
- **(d)** The audit-lake acceptance for the rivalfunds record (round-24 ruling) is ALREADY read and is not part of this
  release: the first such record after r27 was written 18:55:34Z and keeps `day` and `route` with `bytes`.
- **(e)** One extra host run was made in the re-cut (row Z-W28-S31): a read-only rehearsal labelled with the new sha,
  because the host record's `served_release` is inside the digest. Same staged bytes; 0 lake objects.
- **(f)** A cross-box notice bars an untargeted Terraform apply of `infra/aws/terraform/opal-assets` until 06:20Z
  2026-10-08. This release applies no Terraform.

## 6. Act and verify (Phase B steps 9-12, Phase D step 13)

1. Re-read live; if it moved, STOP (a new sha voids the halves).
2. Pre-check by hand, read-only: every lockfile entry cached, or STOP with the list.
3. Open ledger `nfra-oplgtw-gateway-release-r28`, entry and sentinel committed before the act.
4. BEFORE page reads with `LastModified`; `r28_verify.sh before`. Record the deploy command's start time.
5. Deploy from `/c/tmp/og-rel24` with `DEPLOY_BASE_REF=510c8cfed2c852946e3e57fb4dd1c0467e2f3a52`, by the issuer-serial
   halt-gate route.
6. **R45 first:** count the bun cache entries touched since the start; write `RL14_BUN_CACHE.json`. Above 0: stop,
   BLOCKING row, roll back.
7. AFTER page reads; `r28_verify.sh after`; `r28b_postdeploy.sh` (writes `RL14_READ.json`, `RL14_FLOOR.json`).
8. **Rollback triggers:** R45 above 0; the no-`ts` key still empty in its time part; a record changed by the builder; a
   rivalfunds page changing with `LastModified` unmoved; an arg other than `day`, `route`, `fund` kept; the status
   tool failing on a well-formed id; a refused id making a request; tools off 66; consent off 9; a floor read off
   its bar.
9. Manifest by hand, this release's note only. Close the ledger. Run `rl14.AC1`, then `rl14.AC2`, one after the other.
   Both were exercised pre-GO on the new sha with negative controls (2 and 6). The issuer re-grades both.

## 7. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-07.**
- The act may touch exactly what section 3 names, plus the manifest.
- The script that runs and each of its install lines are named in section 2, read by me from the release tree.
- The rollback is pre-built and proven against the live artifact.
- Each property has both branches named; the limits of section 5 are disclosed.
- My reads in section 1 are independent of the worker's. I read the pre-check's code (`_entry_state`, `_state`) and
  every line the rig fix removed from the base-guard test.

**CTO -- owed** (`1.0.0_SA_CTO~Z`).

**CVO -- owed** (`3.0.0_SA_CVO~Z`, required).
