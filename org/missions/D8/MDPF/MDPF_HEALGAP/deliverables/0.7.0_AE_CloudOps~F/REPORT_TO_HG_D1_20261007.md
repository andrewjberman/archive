# REPORT -- MDPF_HEALGAP.TO-HG-d1, the Rebalancer runner's guard reaches the live Lambda

**Seat:** `0.7.0_AE_CloudOps~F` (laptop, the box). **Issuer:** `2.0.0_SA_COO~G1` (dell1). **Order:** @d0a18c6394,
flipped `staged -> pending -> complete`. **Result: the deploy landed and both criteria PASS.** The order asks for seven
things; they are the seven headings below, in its order.

## 1. The ledger entry path

`org/critical_paths/change_management/20261007T1029Z_mdpf-healgap-hg-t1-runner-deploy-20261007_deploy_completion.md`

Opened at deploy START (commit `6df8b0457b`) with 5 legs, a 4-hour window, and the laptop named as the box. CLOSED
(commit `c02cba3b17`) with every leg carrying measured proof and the `.open_deploys` sentinel removed -- nothing
stranded, and the close happened in-session as the NEVER law requires.

## 2. The build sha

`QxLvPLTMO5YSkS+vaRXEkhaA78ZAr1arTyS0ADOOMvk=` -- byte-equal to the sha the COO half names from its dell1 BUILD_ONLY
at `ca914096d7`. The order of operations was deliberate: `BUILD_ONLY=1` ran FIRST, printed the sha, uploaded nothing
and left the source map untouched, so the comparison happened before anything was written to S3 (CTO half condition 2).
Only then did the real `build-and-upload.sh` run, landing object version `uNNJvohJ8HVjIlEcIjEmpouzIRxLROD8` with the
script's own write-verify (`size=12290, sha256 metadata match`).

**Why this is the load-bearing fact of the whole order:** before the apply, the live function AND the staged S3
artifact were both the 2026-09-11 vintage, so the named sha existed on neither. It was an unbuilt target. This box
reproducing it byte-for-byte from its own trunk is what proves the build is deterministic across the two boxes --
had it differed by a byte, the order's instruction was to stop and refuse, and it would have.

## 3. The plan's change list

`terraform -chdir=infra/aws/terraform/opal-assets plan -target=module.cot_rebalancer_runner`, Terraform v1.15.8
resolved on PATH (`.tools/terraform.exe` does not exist on this box, so the binary was resolved, never assumed).

Verdict line: **`Plan: 0 to add, 1 to change, 0 to destroy.`** One resource,
`module.cot_rebalancer_runner.aws_lambda_function.this`, update in-place. The complete change list, three attributes,
all of them code:

| attribute | from | to |
|---|---|---|
| `source_code_hash` | `b1m7jUh6jC55tBfoUX20xRmmKAjB4P1Wvxnwvn2N/Fw=` | `QxLvPLTMO5YSkS+vaRXEkhaA78ZAr1arTyS0ADOOMvk=` |
| `s3_object_version` | `XeSy4IKGvKXGsEwBQRpeXUekk5qb.TYp` | `uNNJvohJ8HVjIlEcIjEmpouzIRxLROD8` |
| `last_modified` | `2026-09-11T03:26:00.000+0000` | (known after apply -- computed) |

Plus `# (28 unchanged attributes hidden)` and `# (4 unchanged blocks hidden)`. CTO half condition 1 is met and its two
stop conditions are both absent: no environment, role, timeout, memory or layer attribute appears, and no second
resource does.

A precondition of the plan, recorded because it touched a file outside the grant and therefore had to be proven not
to have: `terraform init` was required (the provider was not cached in this module) and was run with
`-lockfile=readonly`, because `.terraform.lock.hcl` is NOT in this order's `<paths>`. It reported
`Using hashicorp/aws v5.100.0 from the shared cache directory` -- the locked version was already on the box, so no
download -- and the lock file hashed `92a2bcccd88ce2a409d7d92dd02e1fa222d3984c` both before and after, with
`git status --porcelain` empty on it.

## 4. The apply output tail

`.tools/safe-apply.sh -chdir=infra/aws/terraform/opal-assets apply -target=module.cot_rebalancer_runner` (never bare
`terraform apply`), rc=0:

```
module.cot_rebalancer_runner.aws_lambda_function.this: Modifying... [id=cot-rebalancer-runner]
module.cot_rebalancer_runner.aws_lambda_function.this: Modifications complete after 6s [id=cot-rebalancer-runner]
Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

Live read-back from the served plane, not the producer's self-report: `CodeSha256
QxLvPLTMO5YSkS+vaRXEkhaA78ZAr1arTyS0ADOOMvk=`, `LastModified 2026-10-07T10:44:25.000+0000`, `State Active`,
`LastUpdateStatus Successful`, and `Runtime python3.12 / MemorySize 512 / Timeout 300` unchanged from the base. The
targeted re-plan returned `No changes. Your infrastructure matches the configuration.` at `-detailed-exitcode` rc=0,
which is a mechanical discriminator rather than parsed prose.

**The first attempt failed CLOSED and applied nothing, and that is reported rather than buried.** `safe-apply` exited
rc=7 with `BLOCKED by the naming plan limb (LGIC_ENFORCE DEC-6, ENFORCE mode, rc=2)`. The verdict line named the wrong
cause: one line above, the gate could not open its own script at the mangled path
`C:\c\Users\...\.tools\naming-apply-gate.py`, because `MSYS_NO_PATHCONV=1` was exported in the shell. CLAUDE.md's Git
section bans that variable for `safe-apply` by name, so this was my error, correctly caught. Unset, the re-run was
clean. Nothing was planned or applied on the failed attempt -- confirmed by the live sha still reading the base value
at that point. It is row 3 of the owed surprises because the diagnostic misreports its own cause.

## 5. Both checks' output

| criterion | expected | observed | base |
|---|---|---|---|
| `HG1-d1-AC1` | `DEPLOYED-OK` | `DEPLOYED-OK CodeSha256=QxLvPLTMO5YSkS+vaRXEkhaA78ZAr1arTyS0ADOOMvk= LastModified=2026-10-07T10:44:25.000+0000` (rc=0) | `DEPLOYED-BAD` -- this seat measured `b1m7jUh6...` / 2026-09-11 itself before the apply |
| `HG1-d1-AC2` | `UNCHANGED-OK` | `UNCHANGED-OK retry=2 age=21600 on_success=opal-assets-silver-blackdiamond daily=cron(0 6 * * ? *) input=pull bronze-complete-targets=1` (rc=0) | `UNCHANGED-OK` -- a control, per the order |

Both invoked twice several minutes apart, byte-identical on both runs. AC2's limit is stated rather than glossed: it
passes at the base too, so it cannot by itself distinguish a good deploy from no deploy; the plan's three-attribute
change list is the stronger read of "code only", because it bounds what the apply COULD have touched instead of
sampling what survived.

Proof-of-spec instance
`org/missions/D8/MDPF/MDPF_HEALGAP/deliverables/0.7.0_AE_CloudOps~F/MDPF_HEALGAP.TO-HG-d1.deploy-runner-guard.proof_of_spec.json`,
`proof-of-spec-check.py` **VALID (rc=0)** against the governing order, run before the flip as the order requires.

## 6. Commits

| commit | what |
|---|---|
| `8eb532e5fd` | the seat's readiness record and the carrier ask (pre-order) |
| `6df8b0457b` | ledger OPENED + sentinel, 2 files |
| `b84c07b204` | `ci: record deploy opal-assets @ be658629 [skip ci]` -- source map + CHANGELOG, 2 files |
| `c02cba3b17` | ledger CLOSED + sentinel removed + order `-> pending`, 3 files |
| `8c03191a87` | proof-of-spec VALID + owed-rows record + order `-> complete`, 3 files |

Tag `opal-assets-v0.51.0` created per Deployment Rule 6 (the previous tag was `v0.50.0`, read with
`git tag -l | sort -V | tail`, never assumed).

Every commit used an exact pathspec. This matters today: several seats are live on this laptop's shared index, the
first ledger commit lost a race to `index.lock` and had to be retried, and `deploy_ledger.py close` rewrote ten OTHER
seats' `.open_deploys` sentinels. Those ten were left modified-but-uncommitted and are in none of the commits above --
verified by each commit's own file count (2, 2, 3, 3).

## 7. Push state

**LOCAL.** Measured at write time with `git ls-remote`, not defaulted. This seat does not push shared branches:
`CLOUD` is pushed by `0.0.0_AB_MSTR` on Andrew's word (LD-0367/0368, LD-0522), and the tag is local with it. The
measured hashes are carried in the message that delivers this report, re-read at send time, because a push-state
value written here ages the moment the integrator merges.

---

## What is NOT done, and who owns it

1. **The next 06:00Z stamp read** (`meta/<next date>-complete.json` at ~06:01Z). CTO half condition 3 calls it the
   ledger's verify leg; the order's act step 5 directs closing the ledger before the acceptance reads. A next-day read
   cannot gate an entry opened today without that entry blaring past its window, so the ledger closed on the five
   deploy legs and this is recorded as owed. **Owner: `2.0.0_SA_COO~G1`.** This is a genuine tension between two
   signed documents and is flagged, not resolved by this seat.
2. **FWD-1 is not REALIZED by this order.** This order put the code that makes a second same-day invocation safe onto
   the live function. The induced morning failure -- the actual FWD-1 exercise -- and HG-t-2's re-attempt target are
   both held on PRD ACT 1 per the COO half's own "Not signed here".
3. **Three surprise rows are owed an id.** Full text with `spec_asserts` and `world_is` in
   `SURPRISE_ROWS_OWED_FROM_TO_HG_D1_20261007.md` beside this file; ids are minted on dell1 per the order's refusal
   clause, so `0.0.0_AB_MSTR` carries them and the issuer files them.
4. **The `<status>` flip to a terminal state beyond `complete`** is the issuer's, not this seat's.

-- `0.7.0_AE_CloudOps~F`, 2026-10-07
