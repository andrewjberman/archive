# WP8-DECOM cell 3 -- SI2 code-home re-home PROPOSAL (opal-data-schwab/_ops -> opal-data-assets/code)

**Author:** 0.6.2_AE_PartnerETL | **Date:** 2026-07-17 ~19:2xZ | **For:** 1.0.0_SA_CTO (technical gate: target location + IAM delta + apply) + 0.5.0_AE_OpalETL (WP8 lead: sequencing + GO). CC 2.0.0_SA_COO.
**Status:** PROPOSAL / PREP ONLY. **EXECUTION HELD** until D1's two clean cycles (~07-18 + ~07-21; 07-19 is a Saturday, NEVER#1) AND 0.5.0's explicit GO as WP8 lead. CTO gates the apply. Nothing in this doc has been executed.

> **LANGUAGE (Andrew-direct 2026-07-17, recorded `memory/feedback_schwab_auto_pull_is_rest_not_ui_quartz.md`):** the LIVE Schwab auto pull is a **REST call to the SDDServices backend riding the standing SI2 session's refresh token** -- NOT a UI/Quartz-driven process. "Quartz" is box/role naming only. The UI-driven click-download channel is DEAD (see PART 2).

---

## 0. What this cell is (scope)

WP8-DECOM cell 3 = re-home the SI2 pipeline's **code artifact home** OUT of `opal-data-schwab` (Andrew-ordered decommissioned) to a surviving bucket, BEFORE stage D5, without the daily pull skipping a beat. This is the SI2 chain's **only remaining live opal-data-schwab dependency** (grounded below).

---

## 1. Grounded current state (landed bytes + live rules, 2026-07-17)

The daily pull's data path **already migrated to the monolith.** The `-daily-pull` rules run `-Target monolith`:

| Location | Latest partition | Meaning |
|---|---|---|
| `opal-data-assets/schwab/{08242234,08335338}/bronze/` (MONOLITH) | **20260716** (obj written 2026-07-17 06:15Z) | LIVE data home. Fresh at T-1. |
| `opal-data-schwab/{08242234,08335338}/bronze/` (STAGING) | 20260710 (last write 2026-07-13) | FROZEN. No live writes. (07-11/12 = weekend.) |

**The ONLY live thing still reading opal-data-schwab is the CODE PULL.** When `-Target monolith`, the puller writes both data AND its run-manifest to `opal-data-assets` (`sdd-daily-pull.ps1:53-60`, `:548-559`). It touches `opal-data-schwab` for nothing except the code artifact the box pulls each run.

### Live consumers of the code home `s3://opal-data-schwab/_ops/canonical-schwab-si2/`
| # | Consumer | Cadence | Reads |
|---|---|---|---|
| 1 | `monolith-daily-schedule.tf:119` -- both `-daily-pull` SSM commands | DAILY (0824 10:15/22:15Z; 0833 09:45/21:45Z UTC) | `sdd-daily-pull.ps1` fresh every run (Rule 12) |
| 2 | `bootstrap.ps1:40` -- box bootstrap | on-demand (session-capture setup, NOT scheduled) | `schwab_sdd_session_capture.py` |

### IAM
- Box role **`quartz-si2-spike-role`** (instance profile `quartz-si2-spike-profile`, box `i-0f3d57a97f14727af`).
- Grant **`SchwabOpsCodeRead`** = `s3:GetObject` on `opal-data-schwab/_ops/canonical-schwab-si2/*` (`iam.tf:120-123`). Narrow, code-only, no ListBucket. This is the grant that must move.
- (Separately: `SchwabBronzeWrite` = PutObject on `opal-data-schwab/{08242234,08335338}/bronze/*` (`iam.tf:105-111`) -- the vestigial `-Target staging` escape-hatch grant. NOT this cell; it retires in the D5 removal battery / 0.5.0's prefix dispositions.)

### Code-home contents (22 objects in S3)
Load-bearing + git-tracked (canonical source `infra/aws/ec2/canonical-schwab-si2/`): `sdd-daily-pull.ps1` (the daily, 35842B repo==S3), `schwab_sdd_session_capture.py` (bootstrap), `bootstrap.ps1`, `sdd-backfill-08335338.ps1`, `cred-read.ps1`, `run-admin.ps1`, `run-admin-bg.ps1`, `run-capture.ps1`, `requirements.txt`. The rest (`schwab_sdd_{probe,discover,authprobe}.py`, `schwab_dll_scan.py`, `sdd-{download,harness,history,search,inspect-positions,investigate-holdings}.ps1`, `dl-specific-*`, `sched-tasks-discovery`) are **dormant diagnostic one-shots** (ledger B4) -- no scheduler, retire in D5; they do NOT need re-homing for the live path.

---

## 2. Proposed new code home -- RECOMMENDATION (answers 0.5.0 census row 3 "0.6.2/CTO call")

**`s3://opal-data-assets/code/canonical-schwab-si2/`**

**Rationale -- this is the ESTATE-WIDE EC2/runner code convention, not a new pattern.** Every EC2 pipeline homes its code at `{data-bucket}/code/{pipeline}`, measured live:
`opal-data-inf/code/{bronze-runner,gold}`, `opal-data-bd/code/{runner,bronze,silver,gold}`, `opal-data-mdpf/code/scripts`, `opal-runner-shared/code/gold` -- and the **monolith already uses it**: `opal-data-assets/code/consolidation-gold/{run-gold.sh,...}` (written 07-15). So `opal-data-assets/code/canonical-schwab-si2/` is the monolith's own convention applied to the SI2 box.
- opal-data-assets SURVIVES the decommission; `code/` keeps CODE out of the `schwab/` data keyspace, so the box-role GetObject is unambiguously a code read, never a firm-data read (IAM note sec.3).

**Reconciling 0.5.0's two named candidates (census row 3):**
- *"opal-data-assets `_ops/`"* -- `_ops/` is the puller's own RUN-MANIFEST convention (`schwab/{master}/_ops/daily_pull/`), a data-adjacent record tier, not the estate's CODE convention. Homing code there conflates code with run-records. `code/` is the right tier.
- *"the lambda-artifacts bucket"* (`opal-313476888478-lambda-artifacts`) -- that bucket is for **Lambda deploy zips + layers**; the SI2 puller is an **EC2 box PowerShell script**, not a Lambda artifact. Wrong artifact class. Home it with the EC2-code convention.

CTO gates the final choice; the recommendation is the estate-consistent one.

---

## 3. IAM delta (CTO gate -- the delicate part)

Add to `quartz-si2-spike-role` a new statement, mirroring `SchwabOpsCodeRead`:
```
Sid: SchwabOpsCodeReadMonolith
Effect: Allow
Action: [s3:GetObject]
Resource: [arn:aws:s3:::opal-data-assets/code/canonical-schwab-si2/*]
```
- **Additive.** The old `SchwabOpsCodeRead` on opal-data-schwab STAYS until the cutover is exercised-verified, then is removed in the D5 battery (both homes readable across the cutover = no skip).
- **NEVER-WIDEN note (DoR sec.6.1):** the box is deliberately WRITE-ONLY on the monolith (no GetObject) so it cannot read back the consolidated firm estate. A GetObject scoped to `code/canonical-schwab-si2/*` reads CODE only -- it is NOT the data keyspace, and it cannot enumerate (no ListBucket). This preserves the never-widen property; CTO to confirm.
- **Rule 22a verification (applied + exercised, not comp-iam):** after apply, `aws iam simulate-principal-policy --policy-source-arn <quartz-si2-spike-role> --action-names s3:GetObject --resource-arns arn:aws:s3:::opal-data-assets/code/canonical-schwab-si2/sdd-daily-pull.ps1` (ONE resource-arn; positive control run SEPARATELY), then the live pull-and-run below.

---

## 4. Code + TF/script edits (staged, not applied)

1. **Upload code to new home (Rule 12, repo -> S3):** the load-bearing git-tracked artifacts from `infra/aws/ec2/canonical-schwab-si2/` -> `s3://opal-data-assets/code/canonical-schwab-si2/` (`--sse AES256`; harmless no-op on the monolith, required on opal-data-schwab). At minimum `sdd-daily-pull.ps1` + `schwab_sdd_session_capture.py`; the other tracked helpers for parity.
2. **`monolith-daily-schedule.tf:119`** -- change the pull literal:
   `$s3='s3://opal-data-schwab/_ops/canonical-schwab-si2/sdd-daily-pull.ps1'`
   -> `$s3='s3://opal-data-assets/code/canonical-schwab-si2/sdd-daily-pull.ps1'`
3. **`infra/aws/ec2/canonical-schwab-si2/bootstrap.ps1:40`** -- change the capturer pull to the new home.
4. **`iam.tf`** -- add the `SchwabOpsCodeReadMonolith` statement (sec.3).
5. Doc sync: `SCHWAB_AUTO_PULL_DESIGN.md` (the two `_ops` references) in the same commit as the flip.

Two literal changes on the live daily path (#2, #3) + one additive IAM statement (#4). Small, reviewable, no logic change.

---

## 5. No-skip sequencing (the ~09:46/10:15Z cycle must NOT skip)

Ordered so the box can ALWAYS read the code at every fire:
1. Upload code to the new home (both homes now populated).
2. Commit + apply the **IAM GetObject-on-new-home** (additive; old grant intact -> box reads BOTH homes).
3. **Exercise a manual pull** reading `sdd-daily-pull.ps1` from the NEW home on the box -> confirm it lands bytes in `opal-data-assets/schwab/{master}/bronze/` (the DoR "certify on landed bytes" bar).
4. Only then flip the TF `$s3=` + `bootstrap.ps1` literals; commit + apply.
5. Prove on the next scheduled fire (or a supervised manual run) -- landed bytes at the new partition.
6. After N clean cycles: remove the old `SchwabOpsCodeRead` grant + delete the old `_ops/canonical-schwab-si2/` objects (folds into D5 / the removal battery).

**Timing:** apply in the GAP between the twice-daily fires, never mid-cycle. The `-daily-pull` skip-if-landed makes any same-day second fire a cheap no-op, so a same-day supervised re-run is safe.

---

## 6. Acceptance criteria (exercised, per DoR "landed bytes, never a config read")

- AC-1: the box, reading `sdd-daily-pull.ps1` from `opal-data-assets/code/canonical-schwab-si2/`, completes a pull that LANDS bytes at a new `opal-data-assets/schwab/{master}/bronze/{type}/{partition}/` object (listing-verified: key+ETag+Size).
- AC-2: live `simulate-principal-policy` shows the new `SchwabOpsCodeReadMonolith` GetObject GRANTED on the exact code key (positive control run separately; DoR sec.6 conditioned-ListBucket trap N/A here -- no condition, no ListBucket).
- AC-3: 0-diff `terraform plan` after apply; tag + push.

---

## 7. PART 2 -- staging trees (08242234/ + 08335338/): grounded finding, routed to 0.5.0

The ASK-A phrasing "re-point the staging trees, still written twice daily" does not match landed bytes: the staging trees are **FROZEN at partition 20260710** (last write 2026-07-13) and the `-daily-pull` rules already write `-Target monolith`. The only thing still firing at the staging concept is the **dead GUI channel** `canonical-schwab-si2-download-schedule` (08:35/20:35Z, still ENABLED) -> `SchwabAutoDownload` (GUI, frozen 07-02) -> `SchwabS3Sync` -> staging = an **expected no-op** (frozen source). **So there is no live data-write to re-point.**

**This is independently CONFIRMED by the WP8 lead's own verified census** (0.5.0, `SCHWAB_BUCKET_DECOMMISSION_CENSUS_20260716.md` sec.3a, ETag+MD5 evidence): **08335338 VERIFIED-TIED** (6,932/6,932 keys+ETags; monolith-only 40 = *"new daily deliveries landing monolith-side directly -- the automatic chain, not a gap"*) -> **disposition: no action**; **08242234 VERIFIED copied-complete** (5,966/5,966 keys; 645 ETag-diffs all multipart-vs-plain shape, size-tied, MD5 content-grade 3/3; monolith-only 291 = new deliveries + recovered rld history) -> **disposition: no action**. So my landed-bytes finding and 0.5.0's rigorous copy-census CONVERGE: the staging data re-point is already complete and ruled no-action; the "same `{master}/bronze/` path shape in two buckets" is the only reason the phrasing reads as a live write.

Per CTO 191834Z, the dead GUI channel retires under **0.5.0's step-3 prefix dispositions** (CTO's ~20:30Z batch). I offer this as corroboration; 0.5.0 owns the ruling, I do not execute a data re-point. SURFACE, not adjudicate.

---

## 8. Gates / hold
- EXECUTION HELD: 0.5.0's explicit GO (WP8 lead) is the gate, not any calendar date (COO 184348Z correction).
- CTO gates: the target-location choice (sec.2), the IAM delta (sec.3), and the apply (safe-apply / HALTGT).
- 0824/0833 NEVER SUMMED, NEVER SUBSTITUTED throughout. Bronze raw untouched (17a). This does not touch the puller's write logic, only where it reads its own code from.

---

## 9. Execution runbook (STAGED -- runs on 0.5.0 GO + CTO location ruling; nothing below executed yet)

**Exhaustiveness (no-skip basis):** the full-repo `comp-grep` + live control-plane sweep found EXACTLY THREE live readers of the code home -- `monolith-daily-schedule.tf:119` (both `-daily-pull` SSM commands), `bootstrap.ps1:40`, and the `iam.tf` grant. No other SSM document, EventBridge rule, Lambda, or script reads it. Everything else is docs/ledgers.

**Timing:** run in the GAP between the twice-daily fires -- fires are 0833 09:45/21:45Z, 0824 10:15/22:15Z, download-schedule (dead) 08:35/20:35Z. Safe windows: ~11:00-21:00Z or ~23:00-09:00Z. Never flip mid-fire. Skip-if-landed makes a same-day supervised re-run a cheap no-op.

**Step 1 -- upload code to the new home (Rule 12, repo -> S3; the box only READS it, I write it).**
```
cd infra/aws/ec2/canonical-schwab-si2
for f in sdd-daily-pull.ps1 schwab_sdd_session_capture.py bootstrap.ps1 cred-read.ps1 \
         run-admin.ps1 run-admin-bg.ps1 run-capture.ps1 requirements.txt sdd-backfill-08335338.ps1; do
  aws s3 cp "$f" "s3://opal-data-assets/code/canonical-schwab-si2/$f" --sse AES256 --only-show-errors
done
aws s3 ls s3://opal-data-assets/code/canonical-schwab-si2/     # verify key+ETag+Size (listing-based)
```
Both homes now populated -> box can read either.

**Step 2 -- IAM: add the additive GetObject on the new home (old grant untouched).**
Edit `iam.tf` (add `SchwabOpsCodeReadMonolith` to inline policy `quartz-si2-spike-inline`) ->
`safe-commit` -> `terraform plan` -> `.tools/safe-apply.sh` -> 0-diff plan -> tag -> `git push --follow-tags`.
Box now reads BOTH homes (never-widen: code-only, no ListBucket).

**Step 3 -- Rule 22a verify (applied + exercised, live primitive, ONE resource-arn, control SEPARATE).**
```
aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::313476888478:role/quartz-si2-spike-role \
  --action-names s3:GetObject --resource-arns arn:aws:s3:::opal-data-assets/code/canonical-schwab-si2/sdd-daily-pull.ps1   # expect allowed
# positive control, SEPARATE invocation -- a firm-DATA key the box must NOT read (proves grant stayed code-only):
aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::313476888478:role/quartz-si2-spike-role \
  --action-names s3:GetObject --resource-arns arn:aws:s3:::opal-data-assets/schwab/08242234/bronze/rps/20260716/anything   # expect implicitDeny
```

**Step 4 -- EXERCISE from the new home BEFORE flipping the literals (AC-1, landed bytes).**
Supervised SSM on the box: `aws s3 cp` sdd-daily-pull.ps1 from the NEW home, run as **Administrator** (identity is the whole game -- DoR top box), `-Master 08242234 -Target monolith`. Confirm a new object lands at `opal-data-assets/schwab/08242234/bronze/{type}/{partition}/` (listing-verified). This proves the box reads the new home + the pull works, WITHOUT yet changing the scheduled path.

**Step 5 -- flip the two literals to the new home.**
`monolith-daily-schedule.tf:119` `$s3=...opal-data-schwab/_ops/...` -> `...opal-data-assets/code/...` ; `bootstrap.ps1:40` capturer pull -> new home ; doc-sync `SCHWAB_AUTO_PULL_DESIGN.md` -> `safe-commit` -> plan -> `safe-apply` -> 0-diff -> tag -> push.

**Step 6 -- prove on the next scheduled fire (AC-1 on the real path).**
Watch the next 0824 + 0833 fires land bytes at new partitions. A flipped `cp` that ever fails FATALs loudly (`monolith-daily-schedule.tf:124` `throw`) -- there is NO silent stale-local-copy run. Two clean cycles = cutover proven.

**Step 7 -- cleanup (LAST, folds into D5 removal battery, NOT this GO).**
Remove `SchwabOpsCodeRead` (old opal-data-schwab grant) from `iam.tf` -> apply -> 0-diff. Delete old `_ops/canonical-schwab-si2/` objects only on Andrew's final destructive-go (0.5.0 census stage 6). Order guarantees the old home stays readable until the new one is proven.

**No-skip guarantee:** Steps 1-4 keep BOTH homes readable; the flip (5) happens only after (4) proves the new home; the old grant/objects are removed LAST (7). At no instant can the box lack a readable code home.
