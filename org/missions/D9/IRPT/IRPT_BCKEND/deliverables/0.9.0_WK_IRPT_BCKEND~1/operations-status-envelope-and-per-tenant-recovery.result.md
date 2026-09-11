# IB-s-16 RESULT -- OPERATIONS: the StatusEnvelope, manifests, clocks, leases and traces --
the seven failure arms, each shown to touch no second firm

**TO:** `IRPT_BCKEND.TO-IB-s-16` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-1-1`
**base commit:** `5fa4a113107af2d884a1fe101c135584852586e8` (HEAD of `CLOUD` at hand-off)
**This cell APPLIED infrastructure.** 4 resources added on the new `ops` root (role, policy,
log group, the `irpt-status` Lambda); artifact built/uploaded/verified by `CodeSha256`; the
seven recovery arms driven live against real QA S3 objects and real offline fixtures.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `S16-AC1` | **PASS-by-output** | `timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_s_16.py` | rc=0, `"overall_pass": true` then `IBS16-RECOVERY-ISOLATED` |
| `S16-AC2` | **PASS-by-output** | `timeout 120 .tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/ops plan -no-color -input=false -lock=false` | rc=0, `No changes. Your infrastructure matches the configuration.` |
| `S16-AC3` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Transcripts committed beside this file: `IB-s-16_S16-AC1_battery_output.txt`,
`IB-s-16_S16-AC2_plan_output.txt`.

## The seven arms, each real, each hashing a second firm's live QA objects

| arm | deployed job driven | mechanism | second firm | N of N |
|---|---|---|---|---|
| (a) failed source partition | holdings snapshot (IB-s-12) | `FailingS3Proxy` -- an INJECTED S3 read failure on `build_snapshot('cottonwood', ...)`; raises before `land()` is ever reached | 49financial | 4 of 4 |
| (b) stale model map | holdings snapshot's own `expand_model()` (IB-s-12), pure/offline | a dangling model reference retains 0.4 of its weight as UNRESOLVED mass rather than being dropped | inflection | 4 of 4 |
| (c) duplicated event | mailbox intake poller (IB-s-6) | `run_scan` twice, same owner/store, second scan replays page1-3 (a resync) -- `already_complete=5`, 0 new S3 puts, 0 new queue sends | 49financial | 4 of 4 |
| (d) expired lease | this cell's own `ops.manifests.TenantLease` (generalising `intake.checkpoint.ScanLease`) | a fenced-out dead owner's late write is refused after a live owner's takeover | cottonwood | 4 of 4 |
| (e) queue replay | YCharts generation (IB-s-9) | `GenerationJob.run()` invoked twice, same job/request id -- second run reads `EXISTING_ARTIFACT_REUSED`, `vendor_requests=0`, 0 PDF downloads | inflection | 4 of 4 |
| (f) worker restart | YCharts generation (IB-s-9) | `kill_after={"submitting_before_create"}` then `resume=True` -- reconciles `OWNED_BY_NAME`, `newest_row_adopted=False`, `resubmitted=False` | cottonwood | 4 of 4 |
| (g) revocation mid-job | **EXPORT (IB-s-14) STAND-IN** -- IB-s-14 is not on this branch (in flight, slot ~4) | `_authz.Enforcer.submit_job`/`consume_job` directly, revoked between the two -- refused `EMPTY_GRANT`, result never returned | inflection | 4 of 4 |

Every second-firm hash pair above is RE-DERIVED by the battery on every run (real S3
`list_objects_v2`/`get_object` against `investor-reporting/qa/{holdings,directory}/` in each
firm's own bucket) -- never a cached manifest. Arms (c)-(g) run entirely offline (recorded
transports / in-memory fixtures, no socket reachable); their hash pairs are measured and
trivially identical, and this instance says so rather than dressing a vacuous check as a
discovery. Arm (a)'s hash pair is the load-bearing one: a REAL injected S3 failure, on
Opal's own evidence bucket (never a vendor call), proving the false-complete-publish control
on real infrastructure.

## The three difference controls, with a red-first mutant on control 2

1. **No false-complete publish.** Arm (a): the injected read failure raises before
   `holdings_snapshot.land()` is ever reached; cottonwood's own QA `latest.json` objects are
   byte-identical before/after (4 of 4).
2. **No older-over-newer.** `ops/status.py::revision_is_newer` correctly refuses `3` over
   `7` and allows `9` over `7`. A MUTANT guard (`lambda c, i: True`, "always newer") is
   evaluated alongside the real one and shown to WRONGLY allow the same case the real guard
   refuses -- proving the check discriminates a disabled guard rather than passing
   vacuously.
3. **No resurrected revocation.** Arm (g): `consume_job` after `deps.revoke()` reads
   `EMPTY_GRANT`; the job's result (`SHOULD-NEVER-BE-RETURNED`) never appears in the refusal
   envelope.

## Nine states, one envelope, no credential-shaped leak

Every one of the nine closed states (`QUEUED, RUNNING, READY, PARTIAL, STALE, UNAVAILABLE,
NEEDS_CORRECTION, UNCERTAIN, FAILED`) builds a validating envelope; `public_view()` strips
`internal_correlation_id` (the contract's one `x-server-only` property, read from the
schema, not a hand-typed list -- mirrors `_scope.resolve.browser_safe_view`, IB-s-2's own
idiom); `credential_shaped_leak_census()` finds zero ARN/role/secret/bucket-shaped strings
in any of the nine public views (9 of 9).

## Lineage reconciliation and the manifest census

Lineage: 3 of 3 sample published snapshots reconcile to their own manifest ids (never a
second, uninspected copy). Manifest completeness: 14 of 14 declared concrete paths this
cell's deployed role and code touch (`ops/{status.py,manifests.py,RUNBOOK.md,iam.tf,
lambda.tf,main.tf}`, `ib_s_16_recovery_arms.py`, `iam-role://irpt-status-role`,
`lambda://irpt-status`, the lambda-source-map.json registration, `irpt-jobs`,
`irpt-checkpoints`, `dynamodb://irpt-requests`, `core/kms.tf`) carry a `PATH_MANIFEST.json`
entry with an owner -- 10 new entries appended this cell (never editing an existing one);
live `entries` array is 274 of 274, RE-DERIVED by `manifests.live_entries_total()` rather
than trusted from the (measured-stale) cached `_meta.denominators.entries_total` field.

## The missing normaliser -- filed, not silently worked around

Row `IRPT_BCKEND-W1-S9`: the hand-off's claim that "IB-s-4's one normaliser" strips the
`<firm>:acct:` namespace prefix under `infra/aws/lambda/investor-reporting/directory/` does
not hold -- every top-level `def` in `handler.py`/`refresh.py`/`expiry.py` was enumerated
and none does this, and `git show 624a60e4fc --stat` (IB-s-4's actual merge) confirms no
such file was ever added. This cell needed no id-crossing join for its own seven arms (none
of them join holdings ids to directory ids), so the gap did not block anything here; filed
OBSERVATION/ARMED so a future cell does not `import` a function that is not there.

## Rows filed

- `IRPT_BCKEND-W1-S9` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- the claimed
  shared account-id namespace normaliser under `directory/` does not exist on disk.

## Bounds observed

No live vendor call anywhere -- (a)/(b) read Opal's own S3 evidence bucket; (c) uses
`intake.graph_client.RecordedTransport` (fixtures only, no socket); (e)/(f) use
`ycharts.generate.transport.ReplayTransport` (no socket); (g) uses in-memory `_authz`
fixtures. No monitor, alarm, SNS or SES send. `irpt-status` is deployed UNWIRED: no route,
no schedule, no event source. No credential in any artifact -- the credential-shaped-leak
census (9 of 9 states, zero hits) is the measured claim, not an assertion. No served output
touched: only the new `ops` root's own resources, QA-prefix reads/writes, and this worker's
deliverables. `.tools/commit-gate.sh` rc=0 on every `.py` file. Every invocation ran under
`timeout`. No existing surprise row edited.
