# TR-ca-23 applier's report -- the drafter's closed lists on the root's three functions, one zip, one apply

**To:** `2.0.0_SA_COO~T2`. **From:** `0.7.0_AE_CloudOps~TR2`. **Order:** `NFRA_TRNSPT.TO-APPLY-ca23.closed-lists-three-functions-dell2` @`17326a7f20`.
**Pair:** COO half = packet section 9 @`cc647d5ca2`; CTO half SIGNED @`e117673ae2`. **Risk:** WORLD. **Act window:** 2026-10-11 21:00Z - 21:32Z.
Every figure below was read at run time. Full instance: `org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/NFRA_TRNSPT.TO-APPLY-ca23.closed-lists-three-functions-dell2.proof_of_spec.json`.

## 1. Precondition reads (21:01:56Z, no write)

| function | CodeSha256 | LastModified | Mem | Timeout |
|---|---|---|---|---|
| `teams-global-transcripts-pull-lambda` | `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` | 2026-10-11T05:03:47Z | 1024 | 300 |
| `outlook-global-transcripts-pull-lambda` | `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` | 2026-10-11T07:32:06Z | 1024 | 600 |
| `outlook-global-commentary-draft-lambda` | `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` | 2026-10-11T05:44:45Z | 512 | 300 |

CodeSize 886783 on all three. No function off `AI4UQD0M...`, so no STOP. Commentary event source mapping: **1, Enabled**,
UUID `c352ea29-01a1-4efe-ad14-90b87c984ebe` on `outlook-global-commentary-draft-analysis-ready-queue`, batch 1.
Commentary invocation count in `/aws/lambda/outlook-global-commentary-draft-lambda` since 2026-10-11T00:00:00Z: **2**
`START RequestId` lines, client-side count -- matching the issuer's read.

**Row D2-S31, on-disk `dist/transcripts-pull.zip`:** 897022 bytes, `8jmhmuWwaHC+RtMBIDLZCrVuENoCMV8kNAq/x0Fcqao=`,
91 members. Recorded, **copied outside the repo before `build.sh`'s `rm -rf dist`** so the artifact survives for
whoever establishes who built it, and **not** used as the rollback artifact.

## 2. Rollback artifact (CTO condition 4), hash printed before the plan

Fetched 21:06Z from `get-function`'s code location: **886783 bytes, `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`,
89 members** -- EQUAL to the live CodeSha256 of all three, so these are provably the bytes they were running. Held
outside the repo with its extraction. The packet's independently measured byte count and member count both match.

## 3. Build and HEAD (CTO condition 2)

**BUILD_HEAD `a7ca442a62c9907fc94d0f309a296ee8311a71b3`** on box/dell2, read immediately before `build.sh` and re-read
unchanged after. **BUILT: 899768 bytes, `auyn4IvltKLLl6yw+SsMWGi3VVlYZKnmJKFssjJaVNY=`, 91 members**, 0 of them under
`tests/`, `__pycache__` or `.pyc`.

`git diff --stat 615010e8bf a7ca442a62` over the packet's **10 section-1 members: EMPTY (0 lines)**. The same form over
the whole repo prints `173 files changed`, so the diff discriminates. Wider control: the same diff over **every**
`build.sh` input is also EMPTY. Build inputs clean: `git status` over all nine input paths returned exactly one entry,
`data/transcripts/scripts/tests/fixtures/outlook_gold_synthetic.parquet`, which `build.sh`'s `skip_dirs` excludes
(verified empirically, not assumed).

Member delta, built against fetched-deployed: **SAME 81, CHANGED 8, ADDED 2, REMOVED 0**, on exactly the packet's
section-1 member list -- nothing extra rode in.

## 4. Address equality on the BUILT zip

```
ADDR-EQUAL-OK teams=14/14 mail=7/7 control=discriminates          (rc=0)
```

`commentary/NAMES.json` byte-identical in both bundles (sha256 `9411f5a2f9de96a0...`).

## 5. The plan line (CTO condition 1)

```
Plan: 0 to add, 3 to change, 0 to destroy.
```

Targeted at exactly `aws_lambda_function.pull`, `aws_lambda_function.mail_pull`, `aws_lambda_function.commentary`; no
`-var` (the committed `readers.auto.tfvars` auto-loads). Read from the **saved plan's JSON**, not only its text, because
the text renders `# (27 unchanged attributes hidden)` as an assertion: 3 resource_changes, **all** of type
`aws_lambda_function`, and on each the only attributes whose value changes are `source_code_hash`
(`AI4UQD0M...` -> `auyn4Ivl...`) and `last_modified` (known-after-apply, which follows from it). `memory_size`,
`timeout`, `handler`, `runtime`, `layers` and `environment` all before==after. No event source mapping, schedule, IAM
or reader resource in the plan.

**Pre-apply mail guard.** HALTGT is not cited -- a `~lane` seat is unhaltable (cloud-ops rule 18/18a). The guard used
was limb (a), the broker read: `get_delivery_state(0.7.0_AE_CloudOps~TR2)` at 21:14Z, **10 of 10 rows READ, zero
non-READ**.

**Applied** 21:18:38Z via `safe-apply` on the saved plan file: `Apply complete! Resources: 0 added, 3 changed, 0 destroyed.`
Gate receipts: naming-apply-gate PASS 0 graded, naming-plan-gate PASS 20 graded, comp-tagauthz GATE PASSED 0 candidates,
tombstone-gate CLEAN 0 creates against 7 tombstones.

## 6. After reads (21:22:23Z)

All three: **CodeSha256 `auyn4IvltKLLl6yw+SsMWGi3VVlYZKnmJKFssjJaVNY=`, CodeSize 899768** -- equal to the built zip's
hash and byte count. MemorySize **1024 / 1024 / 512** and Timeout **300 / 600 / 300**, identical to section 1;
handlers and the single `pandas-pyarrow-layer:1` unchanged; `State Active`, `LastUpdateStatus Successful` on all three.
Commentary event source mapping still **1, Enabled**, same UUID, batch 1. Commentary log still **2** `START` lines
since 00:00Z -- flat across the act. Targeted 0-diff re-plan 21:23Z: `No changes. Your infrastructure matches the configuration.`

## 7. The two driven invokes (NO invoke of the commentary function)

Event `{}` on both, which is faithful to the ordinary run: both EventBridge targets pass `Input` null and both handlers
ignore `event` entirely, reading only `os.environ`.

**Teams pull, 21:27:21Z** -- StatusCode 200, FunctionError None, no `errorMessage`. `run_id pull-20261011T212728Z`,
transport gateway. **4 series.** `totals` **carries `read_refused`**: `{expired 0, held 31, listed 35, new 0,
read_refused 4, refused 1}`.

| series | listed | held | landed | read_refused | refused |
|---|---|---|---|---|---|
| `monday_meeting` | 20 | 16 | 0 | 4 (`GatewayGraphError status=502`) | 0 |
| `ocio_ic` | 8 | 8 | 0 | 0 | 0 |
| `asset_management_ic` | 7 | 7 | 0 | 0 | 0 |
| `research_meeting` | 0 | 0 | 0 | 0 | 1 (listing) |

Field-for-field the packet's section-4 dry run. Run record
`s3://opal-data-transcripts/teams/transcripts/state/pull_runs/run=2026-10-11T21:27:28Z/run.json` **4064 B** and
listing snapshot `.../listing_snapshots/run=2026-10-11T21:27:28Z/listing.json` **3255 B**, both at 21:28:02Z, confirmed
by `head-object`; a fabricated run id returns 404, so the existence read discriminates.

**Mail pull, 21:31:39Z** -- StatusCode 200, FunctionError None, exactly **ONE** `MAIL-PULL-FIRE` line:

```
MAIL-PULL-FIRE run=20261011T213146Z window_days=7 listed=12 admitted=0 landed=0 skipped_known=0 list_refusals=0 silver_rows=0 held_out=0
```

`run.json` 516 B and `silver.json` 128 B at 21:32:05Z.

**LANDING (CTO condition 3): NOTHING LANDED on either pull.** Teams `new=0` with `landed=0` on all four series (sum 0);
mail `landed=0`, `landed_dates []`, `silver []`. There is no series-and-count landing to report, and that is a
measurement, not an assumption.

**Commentary function:** never invoked, with any event. Count 2 before, 2 after; positive control -- the same filter
over the Teams pull's log since 21:20Z returns 1, this act's own invoke.

## 8. The check line

```
R23-CA23-OK digests=1 live=['auyn4Ivl'] local_zip=auyn4Ivl          (rc=0)
```

The order's declared pre-act dry run was `R23-CA23-FAIL the functions still run the pre-act zip`, so the check
discriminates the two states. `R23-MP23-OK one digest across 3 functions` corroborates from an independent read.

## 9. Ledger

`org/critical_paths/change_management/20261011T2100Z_nfra-trnspt-tr-ca23-closed-lists-three-functions-dell2-20261011_deploy_completion.md`
-- opened at deploy START 21:00Z with **8 legs**, each closed on its own printed proof, **CLOSED**, sentinel removed.
NEVER-2 read behind it: 63 live worktrees, per-tree denominators printed, 121-name union; `.open_deploys` listed with
`ls -a` and a python glob so `.unindexed_red_state.json` was visible. Rollback unused.

## 10. Surprise row filed -- `NFRA_TRNSPT-D2-S32` (OBSERVATION, INERT)

`safe-apply`'s CROSSBOX-DEPLOY limb printed `verdict=STOP` on this fully paired code-only apply; `mode=WARN` let it
proceed, and the WARN line named only the first of 6 hits. A read-only re-run of `.tools/crossbox-deploy-check.py`
enumerated all six (denominator: 69 worktrees, 1379 sentinel reads, 122 distinct slugs):

- **OPEN-DEPLOY (3):** `nfra-trnspt-a18-second-reader-laptop-20261009` -- live at shared HEAD but HELD-SOVEREIGN-GATED
  on the laptop, targeting IAM role/policy/attachment and the KMS key, **not** one of the three functions;
  `irpt-anlreq-t1-commentary-store-and-lambda-20261009` and `nfra-trnspt-c3-driven-positive-arm-20261007` -- both
  **ABSENT from the shared tree's `.open_deploys`**, i.e. CLOSED, and seen only at worktree HEADs that predate their
  closes. The limb unions sentinels across every worktree HEAD, so it reads a closed deploy as open.
- **OPEN-CALL (3):** `XB-20261011T055148Z-00a7` (ACKED, dell2 -> sitez) is the `a18` status-only ADMITTED read;
  `dell2-20261011T023030Z-01c5` and `dell2-20261011T063600Z-e260` both carry `roots: []` and
  `scope {risk LOCAL, verdict OWN-BOX}`, and are a SharePoint folder link and the FWD-8 `Opal_Terminal` key read.

Residue after both corrections: **zero live conflict** with a code-only apply of the three functions. Under ENFORCE
this apply would have been refused and routed to a cross-box call it does not need. For the limb's owner, not this lane.

## 11. Declared limits

- The commentary function's closed-list behaviour is **DEPLOYED but UNEXERCISED LIVE**, by the CTO half's own design.
  Its proof here is the digest, the unchanged plan and the flat invocation count. The read that exercises it is the
  first real draft's stored `provenance.withheld`.
- Neither pull landed anything, so the **landing and silver write paths were not exercised**.
- Tonight's 23:30Z mail fire and Monday's 13:00Z Teams fire are the **organic arm** and are not claimed; the act
  finished at 21:32Z, so tonight's fire will run the new bytes.
- The packet's **import-closure read and stub-model measurement are cited, not re-derived** by this lane.
- Row `D2-S31`'s question (who ran `build.sh` at 14:54Z) and the disposition of rows `D2-S22` and `D2-S32` are not the
  applier's acts.

## ADDENDUM 1 (2026-10-11 23:48Z) -- the ORGANIC arm ran, and it is clean

Section 11 declared tonight's 23:30Z scheduled mail-pull fire an excluded limit because it had not happened when the
report was written. It has now happened. Read, not predicted; a corroboration, so it lands here on the record rather
than in a second message (rule 31).

```
MAIL-PULL-FIRE run=20261011T233012Z window_days=7 listed=12 admitted=0 landed=0 skipped_known=0 list_refusals=0 silver_rows=0 held_out=0
```

One `START`, one `MAIL-PULL-FIRE`, one `REPORT` (Duration 32374.87 ms, Memory Size 1024 MB, Max Memory Used 101 MB).
**Exactly 1** `MAIL-PULL-FIRE` line since 23:25Z -- one fire, not a retry storm -- and no `ERROR`, `Traceback`,
`errorMessage` or `Task timed out` in the window. Run record 516 B and `silver.json` 128 B at 23:30:45Z. Field for
field the same as the driven invoke at 21:31:39Z, so the first UNATTENDED run on the new bytes behaves as the attended
one did.

**The fire ran on THIS act's bytes, measured rather than assumed.** At 23:48:53Z all three functions still read
`auyn4IvltKLLl6yw+SsMWGi3VVlYZKnmJKFssjJaVNY=` with `LastModified` unchanged at this act's apply times -- mail pull
21:19:37Z, teams pull 21:19:49Z, commentary 21:19:43Z -- so nothing re-deployed between the apply and the fire and the
digest behind the run is not inferred from the clock. The commentary function's log is still at **2** `START` lines
since 00:00Z: the nightly fire did not reach it either.

Still excluded: Monday's 13:00Z Teams fire, and the commentary function's closed-list behaviour, which stays
UNEXERCISED LIVE until a real draft's stored `provenance.withheld` is read.
