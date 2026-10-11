# TR-ra-22 applied: report to 2.0.0_SA_COO~T2

**From:** `0.7.0_AE_CloudOps~TR2` (dell2) **At:** 2026-10-11 ~03:5xZ
**Order:** `NFRA_TRNSPT.TO-APPLY-ra22.teams-pull-refused-read-fix-dell2` AMENDMENT 2, under GO msg 3967
**Pair acted on:** packet `R22_TR_RA22_DEPLOY_PACKET_20261011.md@eb2d9e5451` ADDENDUM 1 + CTO half
`NEVER_WIDEN_TR_RA22_TEAMS_PULL_FIX_CTO_HALF.md@ee82091502`, **the FRESH HALF section only** (F2's six
conditions; everything above that heading is VOID and was not relied on).

**Outcome: the act is complete and every condition is met. Nothing widened.**

---

## 1. Precondition reads (step 1, condition 1) — 03:27:27Z

| function | CodeSha256 | LastModified | condition 1 |
|---|---|---|---|
| `teams-global-transcripts-pull-lambda` | `taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=` | 2026-10-09T11:12:54Z | MATCH |
| `outlook-global-transcripts-pull-lambda` | `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=` | 2026-10-07T23:59:05Z | MATCH |
| `outlook-global-commentary-draft-lambda` | `ResourceNotFoundException` | — | absent, CONFIRMED |

No other act had moved the pull. Pre-act dry run of the criterion: `R22-RA22-FAIL the pull still runs the
pre-fix zip` (rc=1) — so the check discriminates.

## 2. The build (step 2)

`bash infra/aws/lambda/transcripts-pull/build.sh` → **89 files, 886783 bytes, base64 sha256
`AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`**.

Pin resolved by CONTENT, never by `merge-base`: the `data/transcripts/scripts/teams/pull.py` bundled
**inside the built zip** hashes to git blob `8aef45f2fc026aa231dc48ba93bf7c5fe43293c2` — the AMENDMENT 2
pin exactly.

Build tree `box/dell2 5a36586b5f`. The order asks that none of the packet's 12 files differ from
`5ae3b3ddd9`; I measured the stronger statement over **every** `build.sh` input (both handlers,
`data/transcripts/scripts`, `data/transcripts/assets`, `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json`,
`infra/logic/registry/*.json`, `data/firm_registry.json`, the IRPT `_keys/keys.py`): **0 paths dirty in
the working tree and 0 paths differing from the pin.** HEAD moved three times during the session as other
lanes committed; no bundled path was ever touched.

Build-input control: the zip `build.sh` replaced hashed to `taFbGTCU…6HA=`, **equal to the then-live
CodeSha256**, proving the local zip was the deployed build input and not merely a file of the right name.
It was preserved off-repo before the rebuild.

## 3. The plan line (step 3, condition 2)

```
# aws_lambda_function.pull will be updated in-place
~ last_modified    = "2026-10-09T11:12:54.673+0000" -> (known after apply)
~ source_code_hash = "taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=" -> "AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I="
  # (27 unchanged attributes hidden)   # (4 unchanged blocks hidden)
Plan: 0 to add, 1 to change, 0 to destroy.
```

**Exactly one resource block, and the only diffs are the code hash and its timestamp.** `safe-apply` rc=0
at 03:36:14Z. Targeted 0-diff re-plan: `No changes. Your infrastructure matches the configuration.`

**One thing you should know about this root** (also filed as row `NFRA_TRNSPT-D2-S17`): it cannot be
planned or applied at all without a `-var`. `readers.tf:15` declares `second_reader_trust_principal_arns`
with no default and the root carries no tfvars, so `terraform` refuses with `Error: No value for required
variable`. That variable reaches `local.named_reader_arns`, hence the KMS key that `pull.tf` depends on.
I supplied it **from applied state** — `aws iam get-role teams-global-transcripts-second-reader-role`
shows the live trust is exactly `arn:aws:iam::313476888478:user/Opal_Terminal` — in a tfvars file **outside
the repo**, so no committed artifact asserts a routing decision that is Andrew's, and the plan showed no
reader resource. A future applier typing a guess here would not be refused, and on an **untargeted** apply
it would rewrite who may read the transcripts tier. Worth a committed tfvars or a default.

## 4. After-reads (step 4, condition 3) — 03:37:01Z

| function | CodeSha256 | LastModified | verdict |
|---|---|---|---|
| `teams-global-transcripts-pull-lambda` | `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` | 2026-10-11T03:36:14Z | **equals step 2's zip hash**; State Active, LastUpdateStatus Successful |
| `outlook-global-transcripts-pull-lambda` | `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=` | 2026-10-07T23:59:05Z | **UNCHANGED**, timestamp included |
| `outlook-global-commentary-draft-lambda` | `ResourceNotFoundException` | — | **still absent** |

## 5. The driven invoke (step 5, condition 4) — 03:38:44Z to 03:40:10Z, 86 s

**StatusCode 200, FunctionError null, no `errorMessage` key. 4 series entries.** Graded against A4 both
ways — **MATCH on every cell:**

| series | listed | held | landed | expired | read_refused | refused | A4 | verdict |
|---|---|---|---|---|---|---|---|---|
| `monday_meeting` | 20 | 16 | 0 | 0 | **4** | 0 | 20 / 16 / 4 rr | MATCH |
| `ocio_ic` | 8 | 7 | **1** | 0 | 0 | 0 | 8 / 7 / 1 would land | MATCH |
| `asset_management_ic` | 7 | 7 | 0 | 0 | 0 | 0 | 7 / 7 | MATCH |
| `research_meeting` | 0 | 0 | 0 | 0 | 0 | **1** | refused 1 | MATCH |

`totals`: listed 35, new 1, held 30, expired 0, refused 1. All four `monday_meeting` refusals read
`GatewayGraphError status=502`; `research_meeting` reads `list GatewayGraphError status=502` — the
listing-side class AMENDMENT 2 exists to catch.

**No landing count above A4's.** The one covered `ocio_ic` catch-up landed bronze and silver (`LANDED`
plus `SILVER-WRITTEN`); nothing else landed. Nothing to report under condition 4's second limb.

`state_key`: `s3://opal-data-transcripts/teams/transcripts/state/pull_runs/run=2026-10-11T03:38:57Z/run.json`

| object | head-object |
|---|---|
| run record | 4183 bytes, 2026-10-11T03:40:10Z, `aws:kms` — EXISTS |
| listing snapshot `.../listing_snapshots/run=2026-10-11T03:38:57Z/listing.json` | 3255 bytes, same timestamp, `aws:kms` — EXISTS |

Both are objects a failing fire never wrote. Counts and statuses only throughout; no transcript text, no
bearer, no meeting id in this report, the ledger, the log or the proof instance.

## 6. The check line

```
R22-RA22-OK pull=AI4UQD0M local_zip=AI4UQD0M mail=VGIq85Xx commentary=ABSENT      (rc=0)
```

## 7. Ledger, artifacts, commit and push state

- **Ledger, CLOSED:** `org/critical_paths/change_management/20261011T0326Z_nfra-trnspt-tr-ra22-teams-pull-fix-dell2-20261011_deploy_completion.md`
  — opened at deploy START 03:26Z (commit `c513e72fa1`), three legs each carrying proof, closed on step 5's
  result; the `.open_deploys` sentinel is removed.
- **Step 0, NEVER-2:** 16 live worktrees read with `ls-tree`, per-tree denominators printed (shared 19,
  max 29), union 78 distinct entry names. The only NFRA_TRNSPT entry in the shared tree,
  `nfra-trnspt-a18-second-reader-laptop-20261009`, is HELD-SOVEREIGN-GATED on IAM/KMS targets, not on
  `aws_lambda_function.pull` — no collision. `irpt-anlreq-t1-commentary-store-and-lambda-20261009` is
  `2.0.0_SA_COO~Y2`'s and was not touched.
- **Proof instance, VALID rc=0** (4 of 4 named controls discriminate, 0 DID-NOT-DISCRIMINATE, rollback
  named): `org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/NFRA_TRNSPT.TO-APPLY-ra22.teams-pull-refused-read-fix-dell2.proof_of_spec.json`
- **Log:** `org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/2026-10-11/teams_pull_ra22_applied_and_driven.md`
- **Commits:** `c513e72fa1` (ledger open) and **`6f7833e27a`** (ledger closes, sentinel removal, proof
  instance, log, row `NFRA_TRNSPT-D2-S17`).
- **Push state: LOCAL** — measured, not assumed: `git ls-remote origin refs/heads/box/dell2` reads
  `b04afa8412`, local HEAD `6f7833e27a`, **3 ahead / 0 behind**. `never-rules-gate.sh` refuses a push of
  the shared branch from any seat but the integrator `0.0.0_AB_MSTR`, and I did not take the audited
  override, because it would republish other seats' local commits. The hourly integration window carries it.

## 8. Not done, and why

- **No tag.** Deployment rule 6 asks for one per 0-diff apply, but this root carries exactly ONE tag
  (`transcripts-v1.0.0`) across all of its applies, so per-deploy tagging is not its practice. Inventing it
  mid-round against an order whose bounds are "no other resource, root, key policy or function" is your
  call, not mine.
- **No core-document edit.** A code hash moved, which is not a structural change, and `pipeline_inventory.xml`
  belongs to the base seat.
- **`<status>` not flipped, AC1 not graded.** Both are yours.
- **The 2026-10-12T13:00Z fire is not claimed as evidence.** This proof rests on one invoke that was
  driven, not waited for. It is declared as an exclusion in the instance.
- **`2.0.0_SA_COO~Y2` must re-read the shared `dist/` zip** before steps A2 and B of its open ledger: it is
  now `AI4UQD0ME+…aA/I=`, not `taFbGTCU…6HA=`. You told that seat at msg 3939; I did not touch its entry.
