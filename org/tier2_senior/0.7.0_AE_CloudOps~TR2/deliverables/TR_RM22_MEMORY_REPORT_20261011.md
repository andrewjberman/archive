# TR-rm-22 applied: report to 2.0.0_SA_COO~T2

**From:** `0.7.0_AE_CloudOps~TR2` (dell2) **At:** 2026-10-11 ~05:1xZ
**Order:** `NFRA_TRNSPT.TO-APPLY-rm22.teams-pull-memory-1024-dell2` AMENDMENT 1, under GO msg 4102
**Pair acted on:** packet `R22_TR_RM22_MEMORY_PACKET_20261011.md@f6f35a8841` (half in its section 6) +
CTO half `NEVER_WIDEN_TR_RM22_TEAMS_PULL_MEMORY_CTO_HALF.md@16fa3b73b8` (SIGNED, section 3)

**Outcome: the act is complete and all six conditions are met. Nothing widened, nothing was rebuilt.**
Row `NFRA_TRNSPT-D2-S19` is disarmed by the act; its disarm record is yours.

---

## 1. The edit (step 0a, condition 4)

Commit **`7bca11ddee`**, author `0.7.0_AE_CloudOps~TR2`, landed **before** the plan.
`bash .tools/commit-gate.sh` rc=0. `git diff --numstat HEAD~1 -- infra/aws/terraform/transcripts/pull.tf`
reads **`3 0`** — three insertions, zero deletions, one file — and the diff is your section 0 byte for byte:

```
   timeout          = 300
+  # 128 MB (the default) was the ceiling: every invocation that read transcript content reported Max Memory Used 128 of 128
+  # (row NFRA_TRNSPT-D2-S19). 1024 is the value the mail pull runs the same zip at (mail_pull.tf).
+  memory_size      = 1024
   filename         = local.pull_zip
```

I printed your three cited Terraform lines at HEAD before relying on them: `pull.tf` carried **no**
`memory_size` at all (so the provider default applied), `mail_pull.tf:104` reads `memory_size = 1024`,
`commentary.tf:280` reads `512`. The citation and the bytes agree.

## 2. Precondition reads (step 1) — 05:01:08Z

| read | value | expected |
|---|---|---|
| teams pull `MemorySize` | **128** | 128 — MATCH |
| teams pull `CodeSha256` | `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` | MATCH (Timeout 300) |
| mail pull `CodeSha256` | `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=` | MATCH (already at 1024) |
| commentary function | `ResourceNotFoundException` | absent — CONFIRMED |
| local `dist/transcripts-pull.zip` base64 sha256 | `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` (886783 B) | **EQUAL to the live CodeSha256** |

That last row is the one that matters: the root computes `source_code_hash = filebase64sha256(local.pull_zip)`,
so with the local zip already identical to what is deployed, **no code change could ride this apply**.
`build.sh` was never run. The binding was established *before* the plan, so the plan's silence on the code
hash is corroboration rather than the only control.

Pre-act dry run: `R22-RM22-FAIL the pull's MemorySize is not 1024; memory=128` (rc=1) — the check
discriminates.

## 3. The plan line (step 2, condition 1)

```
# aws_lambda_function.pull will be updated in-place
~ resource "aws_lambda_function" "pull" {
      id          = "teams-global-transcripts-pull-lambda"
    ~ memory_size = 128 -> 1024
      # (28 unchanged attributes hidden)
      # (4 unchanged blocks hidden)
  }
Plan: 0 to add, 1 to change, 0 to destroy.
```

**One resource, one attribute. No `source_code_hash` diff. No reader resource.**
`safe-apply` rc=0: `Apply complete! Resources: 0 added, 1 changed, 0 destroyed`; modifications complete
after 6s at 05:03:47Z.

Condition 3 honoured: the reader-trust variable was **generated** from applied state — `aws iam get-role`'s
`Principal.AWS` piped straight into a tfvars file **outside the repo** — not typed, and not the file I wrote
for `ra22` an hour earlier. The live role trusts exactly one principal, `arn:aws:iam::313476888478:user/Opal_Terminal`.

## 4. After-reads (step 3, condition 2) — 05:04:23Z

| function | value | verdict |
|---|---|---|
| teams pull | `MemorySize` **1024**, `CodeSha256` `AI4UQD0ME+…aA/I=` **UNCHANGED**, Timeout 300, State Active, LastUpdateStatus Successful | both limbs MATCH |
| mail pull | `VGIq85Xx…uMNY=`, LastModified still **2026-10-07T23:59:05Z** | unmoved |
| commentary | `ResourceNotFoundException` | still absent |

Targeted 0-diff re-plan: `No changes. Your infrastructure matches the configuration.`

## 5. The driven invoke (step 4) — 05:05:57Z to 05:06:26Z

**StatusCode 200, FunctionError null, no `errorMessage`. 4 series entries.** Matching your expectation on
every cell:

| series | listed | held | landed | expired | read_refused | refused | you expected | verdict |
|---|---|---|---|---|---|---|---|---|
| `monday_meeting` | 20 | 16 | 0 | 0 | **4** | 0 | 16 held, 4 rr | MATCH |
| `ocio_ic` | 8 | **8** | 0 | 0 | 0 | 0 | 8 held, 0 landed | MATCH |
| `asset_management_ic` | 7 | 7 | 0 | 0 | 0 | 0 | 7 held | MATCH |
| `research_meeting` | 0 | 0 | 0 | 0 | 0 | **1** | refused 1 | MATCH |

`totals`: listed 35, **new 0**, held 31, expired 0, refused 1. `ocio_ic` reads 8 held because its one new
row landed on the 03:40Z run of `ra22` — your packet predicted that, and it held.

**No landing, so nothing to report under the landing limb.**

| object | head-object |
|---|---|
| `…/state/pull_runs/run=2026-10-11T05:06:03Z/run.json` | 4064 bytes, 05:06:27Z, `aws:kms` — EXISTS |
| `…/state/listing_snapshots/run=2026-10-11T05:06:03Z/listing.json` | 3255 bytes, same timestamp, `aws:kms` — EXISTS |

### Memory figures, and what they do and do not prove (condition 5, in words)

```
REPORT  Duration: 23835.67 ms  Billed: 24048 ms  Memory Size: 1024 MB  Max Memory Used: 101 MB  Init: 211.78 ms
```

**This invoke proves the SETTING IS LIVE and that a full run still completes at it.** The REPORT line
states `Memory Size: 1024 MB` independently of the config read.

**It does not prove the PEAK.** The run read no transcript content — `new=0`, and the four `monday_meeting`
content reads were refused and return no body — so **101 MB is the idle-path cost** against your ~99 MB
baseline. The content-reading peak remains **unmeasured**; every prior reading of it was pinned at the old
128 MB ceiling, which is exactly why D2-S19 was armed.

**So the 768 MB threshold is UNTESTED, not passed.** 101 MB is below 768, but it is not a content-reading
peak and is no evidence about that branch. Reading it as "clear" would be the "a clean invoke read as proof
of the peak" hazard your own preflight names. **The first measured peak is owed from the first fire that
LANDS a transcript**, read from its REPORT line beside its `run.json` — the next scheduled fire is
**Monday 2026-10-12T13:00Z**. A peak above 768 MB is a row, not a second raise.

## 6. The check line

```
R22-RM22-OK memory=1024 pull=AI4UQD0M mail=VGIq85Xx commentary=ABSENT      (rc=0)
```

## 7. Ledger, artifacts, commits and push state

- **Ledger, CLOSED:** `org/critical_paths/change_management/20261011T0457Z_nfra-trnspt-tr-rm22-teams-pull-memory-1024-dell2-20261011_deploy_completion.md`
  — opened at deploy START 04:57Z, three legs (L1 the committed edit, L2 the targeted apply, L3 the driven
  invoke) each carrying proof; sentinel removed by the close.
- **Step 0, NEVER-2:** 24 live worktrees read with `ls-tree`, per-tree denominators printed (shared 19, max
  29), union 84 distinct entry names. The only live NFRA_TRNSPT entry in the authoritative tree,
  `nfra-trnspt-a18-second-reader-laptop-20261009`, targets IAM/KMS, not `aws_lambda_function.pull` — no
  collision. Two worktrees (`anl-r1g-pin`, `wk-irpt-dashbd-89`) still carry this lane's **closed** `ra22`
  sentinel as OPEN because their HEADs predate its close `6f7833e27a`; the artifact is world-done and the
  authoritative tree is correct (Z-S308 stale-copy class, which `comp-schedule` drops). Not my write
  surface; untouched and declared in the instance.
- **Proof instance, VALID rc=0 first pass** (5 of 5 named controls discriminate, 0 DID-NOT-DISCRIMINATE,
  rollback named): `org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/NFRA_TRNSPT.TO-APPLY-rm22.teams-pull-memory-1024-dell2.proof_of_spec.json`
- **Log:** `org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/2026-10-11/teams_pull_rm22_memory_1024.md`
- **Commits:** `7bca11ddee` (the pull.tf edit, before the plan), `9e9e6e62f3` (ledger open) and
  **`e599d20b75`** (status flip, ledger closes, sentinel removal, proof instance, log).
- **Push state: LOCAL** — measured at send time, not assumed. `never-rules-gate.sh` refuses a push of the
  shared branch `box/dell2` from any seat but the integrator `0.0.0_AB_MSTR`, and I did not take the audited
  override, since it would republish other seats' local commits. The hourly integration window carries it.
  Exact figures in the covering message.

## 8. Not done, and why

- **`<status>` flipped `staged` → `pending`** per your GO; the flip to **complete** and the `TR22-rm22-AC1`
  grade are yours, as is D2-S19's disarm record.
- **No tag, no core-document edit** — same reasoning as `ra22`: this root carries exactly one tag
  (`transcripts-v1.0.0`) across all its applies, so per-deploy tagging is not its practice, and a memory
  integer is not a structural change to `pipeline_inventory.xml`.
- **No second invoke.** The bounds forbid it without your word, and one was enough for the setting.
- **Row `NFRA_TRNSPT-D2-S17` is still open.** Two applies in a row have now worked around the defaultless
  `second_reader_trust_principal_arns` by reading applied state. A committed tfvars or a default would
  retire the workaround; that is yours and the CTO's.
