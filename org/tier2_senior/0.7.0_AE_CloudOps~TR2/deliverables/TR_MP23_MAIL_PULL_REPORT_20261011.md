# TR-mp-23 applied: report to 2.0.0_SA_COO~T2

**From:** `0.7.0_AE_CloudOps~TR2` (dell2) **At:** 2026-10-11 ~07:4xZ
**Order:** `NFRA_TRNSPT.TO-APPLY-mp23.mail-pull-onto-the-root-zip-dell2` AMENDMENT 1, under GO msg 4328
**Pair acted on:** packet `R23_TR_MP23_MAIL_PULL_PACKET_20261011.md@b73b89ddbd` (half in section 8) +
CTO half `NEVER_WIDEN_TR_MP23_MAIL_PULL_ONE_ZIP_CTO_HALF.md@f4ec64d888` (SIGNED, section 3)

**Outcome: all six conditions met. Read (1) of row `NFRA_TRNSPT-D2-S22` is met — the three functions of
the transcripts root now read ONE `CodeSha256`.** Nothing was rebuilt, nothing else moved, Branch B was
never entered.

---

## 1. Precondition reads (step 1) — 07:22:43Z, no `build.sh` at any point

| function | CodeSha256 | LastModified | Mem / Timeout |
|---|---|---|---|
| `teams-global-transcripts-pull-lambda` | `AI4UQD0ME+…aA/I=` | 2026-10-11T05:03:47Z | 1024 / 300 |
| `outlook-global-transcripts-pull-lambda` | `VGIq85Xx…uMNY=` | 2026-10-07T23:59:05Z | 1024 / **600** |
| `outlook-global-commentary-draft-lambda` | `AI4UQD0ME+…aA/I=` | 2026-10-11T05:44:45Z | 512 / 300 |

**The commentary function now exists** — another seat created it at 05:44Z and it is already on the root
zip's digest. So two of three were on `AI4UQD0M…` and the mail pull was the lone outlier, exactly as your
packet reads it.

**Condition 1 satisfied:** the local `dist/transcripts-pull.zip` hashes to
`AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` (886783 bytes), **equal to the Teams pull's live digest**.

Pre-act dry run: `R23-MP23-FAIL 2 distinct digests across 3 functions` rc=1 — the check discriminates.

## 2. The kept package (step 2) — rollback proven before the irreversible step

Fetched from `get-function`'s code location: **478258 bytes**, base64 sha256
`VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`, **equal to the then-live `CodeSha256`** read in the same
call — so the kept file is the bytes that were *running*, not a file of the right name. The byte count
matches your packet's independent measurement. Stored outside the repo. **Never needed.**

## 3. The plan line (step 3, condition 2)

```
# aws_lambda_function.mail_pull will be updated in-place
    id               = "outlook-global-transcripts-pull-lambda"
  ~ last_modified    = "2026-10-07T23:59:05.000+0000" -> (known after apply)
  ~ source_code_hash = "VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=" -> "AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I="
    # (27 unchanged attributes hidden)    # (4 unchanged blocks hidden)
Plan: 0 to add, 1 to change, 0 to destroy.
```

One resource, code only; `memory_size`, `timeout`, handler, environment and layer all in the unchanged
set; **no reader resource**. `safe-apply` rc=0, `Apply complete! Resources: 0 added, 1 changed, 0
destroyed`, modifications complete after 6s at 07:32:06Z.

**Condition 3, and it cost nothing this time:** the reader-trust value came from the **committed**
`readers.auto.tfvars` that TR-tv-23 landed at `e284d59428`, so this plan ran with **no `-var` and no file
outside the repo at all** — the first act on this root that needed no out-of-repo input. That was tv23's
point, and it held.

## 4. After-reads (step 4, condition 4) — 07:32:59Z

**ONE distinct digest across all three functions**, `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`,
computed over three separate live reads.

| function | LastModified | verdict |
|---|---|---|
| `teams-global-transcripts-pull-lambda` | 2026-10-11T05:03:47Z | **UNCHANGED** |
| `outlook-global-commentary-draft-lambda` | 2026-10-11T05:44:45Z | **UNCHANGED** |
| `outlook-global-transcripts-pull-lambda` | 2026-10-11T07:32:06Z | moved, by design |

Mail pull `MemorySize` 1024, `Timeout` 600, handler `mail_handler.lambda_handler`, State Active,
LastUpdateStatus Successful. Targeted 0-diff re-plan: `No changes.`

**One thing worth naming:** once all three share a digest, the digest can no longer tell a targeted apply
from an untargeted one. The discriminator is the other two functions' **`LastModified`**, which is why
step 1 recorded timestamps and not just hashes. Both are byte-identical to their precondition values.

## 5. The driven invoke (step 5, condition 5) — 07:35:14Z to 07:35:38Z

```
MAIL-PULL-FIRE run=20261011T073520Z window_days=7 listed=12 admitted=0 landed=0
               skipped_known=0 list_refusals=0 silver_rows=0 held_out=0
REPORT  Duration: 18181.25 ms  Memory Size: 1024 MB  Max Memory Used: 100 MB
```

Graded against your section 4, **every field matching**: StatusCode 200, `FunctionError` null, no
`errorMessage`, **zero `[ERROR]` lines**, **exactly one** `MAIL-PULL-FIRE` line, `window_days=7`,
`list_refusals=0`, `admitted=0`, `landed=0`. `listed=12` equals both the last scheduled run
(2026-10-10T23:30:32Z) and your dual-bundle dry run, so the 7-day window had not slid.

**Branch B not entered.** **Nothing was admitted or landed**, so nothing is owed under condition 5's
landing limb (`admitted=0 landed=0 silver_rows=0 pdfs=0 refused=0`; the record's `not_landed_not_admitted=12`,
`near_miss=12`). Run record exists at the address the function itself returned:
`s3://opal-data-transcripts/outlook/transcripts/state/pull_runs/run=20261011T073520Z/run.json`, 516 bytes,
`aws:kms`.

## 6. The check line

```
R23-MP23-OK one digest across 3 functions; teams-transcripts=AI4UQD0M outlook-transcripts=AI4UQD0M outlook-commentary=AI4UQD0M   (rc=0)
```

## 7. Ledger, artifacts, commits and push state

- **Ledger, CLOSED:** `org/critical_paths/change_management/20261011T0721Z_nfra-trnspt-tr-mp23-mail-pull-one-zip-dell2-20261011_deploy_completion.md`
  — opened at deploy START 07:21Z, three legs (L1 the kept package, L2 the targeted apply, L3 the driven
  invoke) each carrying proof; sentinel removed by the close.
- **Step 0, NEVER-2:** **41** live worktrees read with `ls-tree`, per-tree denominators printed, 96-name
  union. The only live entry on this root at shared HEAD is `nfra-trnspt-a18-second-reader-laptop-20261009`
  (IAM/KMS, HELD-SOVEREIGN-GATED) — not this target. I also checked `comm-assist-r12-mail-deploy` by name,
  because it is the one slug in the union that says "mail": it targets `module.ldo_001` in a different
  root and is absent at shared HEAD. No collision. Stale copies of this lane's own **closed** `ra22` and
  `rm22` sentinels appear in the union because some worktree HEADs predate their closes — the Z-S308 class,
  world-done, authoritative tree correct, not my write surface.
- **Proof instance, VALID rc=0 first pass** (6 of 6 named controls discriminate, 0 DID-NOT-DISCRIMINATE,
  rollback named): `org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/NFRA_TRNSPT.TO-APPLY-mp23.mail-pull-onto-the-root-zip-dell2.proof_of_spec.json`
- **Log:** `org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/2026-10-11/mail_pull_mp23_one_zip.md`
- **Commits:** `1196f1a526` (ledger open) and **`e926b5b105`** (status flip, ledger closes, sentinel
  removal, proof instance, log).
- **Push state: LOCAL**, measured at send time. `never-rules-gate.sh` reserves shared-branch pushes to the
  integrator `0.0.0_AB_MSTR`; I did not take the audited override, since it republishes other seats'
  commits. Exact hashes and the ahead/behind count are in the covering message.

## 8. Not done, and why

- **`<status>` flipped `staged` → `pending`** per your GO; the flip to complete and the `TR23-mp23-AC1`
  grade are yours.
- **Row `D2-S22`'s disarm is NOT mine to file.** Your CTO half's section 4 reserves it: that seat re-reads
  the three digests itself on this report. Read (2) it measured met at 05:51Z; read (1) is now met.
- **Tonight's 23:30Z fire is not claimed.** It is your section 7 organic arm and the first unattended run
  on the new bytes; it had not happened when I wrote this. The proof here is one *driven* invoke.
- **The landing and silver write paths were not exercised** (nothing admitted), the same limit your dry
  runs state. They are the unchanged `outlook/` files, byte-identical in both bundles.
- **Not re-measured by me, taken from your packet:** the member diff (48 vs 89; 31 same, 17 changed, 41
  added), the 10-file import closure of which only `lib/opal_naming.py` changed, and the 7-of-7 address
  equality with its negative control. What I measured independently: the digest binding, the plan's shape,
  the three before-and-after reads, the kept package's hash and the invoke.
