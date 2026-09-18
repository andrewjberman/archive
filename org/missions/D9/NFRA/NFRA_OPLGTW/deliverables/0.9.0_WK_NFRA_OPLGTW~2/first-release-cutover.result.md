# NFRA_OPLGTW.TO-OG-r-1 -- first release cutover -- RESULT

**Assignee:** 0.9.0_WK_NFRA_OPLGTW~2 | **Worktree:** C:/tmp/wk-oplgtw-2a, branch wk-nfra_oplgtw-2a, cut from CLOUD @1ca5067f6e
**Proof instance:** `NFRA_OPLGTW.TO-OG-r-1.first-release-cutover.proof_of_spec.json` (schema-valid, `jsonschema.validate` this run)

## Outcome, in one line

The release deploy (OGR1-AC2) could not run: `infra/aws/ec2/safe-ec2-deploy.sh`'s own worktree-redirect logic
points its halt-gate identity resolver at the SHARED MAIN TREE rather than this worker's own worktree (where
the issuer pre-provisioned the session-serial file per this order's identity line), so the gate fails closed
with "IDENTITY UNRESOLVED" before Step 2 (Running Deployment) ever runs. No override exists for that failure
branch and none was attempted. Nothing was deployed: no artifact built, no S3 upload, no SSM command issued,
no host or AWS state changed. Filed as ARMED surprise row `NFRA_OPLGTW-W2-S5`, disarm owner `2.0.0_SA_COO~O`
(a worker cannot carry an ARMED row's disarm word past its own drain, per R-18).

**5 of 14 criteria PASS by output: OGR1-AC1, AC3, AC11, AC12, AC14.**
**9 of 14 FAIL: OGR1-AC2, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC13** -- AC4/AC5/AC6/AC7/AC8/AC13 because the
deploy never ran (a true, disclosed gate, not a fabricated pass); AC9 because OG-p-1's BASELINE.json records
no error-count metric to compare against (a real premise gap in the baseline artifact, independent of AC2);
AC10 because the previous release artifact itself fails the runbook's own rollback restorability precondition
(a real, separate finding, surprise row `NFRA_OPLGTW-W2-S7`) even though its content-hash mechanism (R-40) is
itself correct and verified.

`<status>` is left `pending`: per this order's own proof_of_spec block, `complete` is flipped "only when every
MECHANICAL criterion PASSES by output," which is not the case here.

## What actually happened, in order

1. **OGR1-AC1** -- opened the deploy-completion ledger (`deploy_ledger.py open`, slug
   `nfra-oplgtw-og-r-1-first-release`, 3 legs: L1 ec2-baked-asset digest match, L2 verify post-deploy checks,
   L3 git manifest commit) and committed the sentinel + rendered entry (`7752ea3bdb`) BEFORE any deploy attempt.
   Also recorded the previous-release snapshot for AC10 (the current `deployed_commit`'s git TREE hash,
   `1556d6e979e68b1c47983a31506d0d96f8aacf36`, and its restorability pre-checks) at this same moment, before AC2
   could overwrite `EC2_MANIFEST.json`. PASS.
2. **OGR1-AC11** -- ran the local, pre-deploy, moto-emulated authority difference test (`og_r1_ac11_pytest.py`,
   reusing `tests/acceptance/conftest.py`'s `og_v2` harness exactly as `tests/test_schwab_wiring.py` already
   does from outside `tests/acceptance/`): an identity with `menachem@opalinvest.com`'s email but no tid/oid
   grant is denied on 5 of 5 live `TOOL_NAMES`; the same tid, a fresh oid, after `og_v2.grant(tid, oid)`, is
   allowed on `schwab_get_access`. Never reaches the host or the live state store. PASS.
3. **OGR1-AC2** -- ran `bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh i-07dccb1615503ac99`.
   Step 1 (pre-deployment check) passed. The sourced `halt-gate-check.sh` then printed "IDENTITY UNRESOLVED --
   BLOCKED" and the wrapper exited rc=3 before Step 2. Root cause traced and filed (surprise row
   `NFRA_OPLGTW-W2-S5`, see below). FAIL, reproduced twice, identical both times.
4. **OGR1-AC3 / AC12** -- live `dynamodb:Scan` on `gateway-access-state-table` (8 items total, all classified as
   OTHER cells' own pre-existing test fixtures, `probe-og-i1-*` / `probe-og-i5-*`, never a real principal --
   surprise row `NFRA_OPLGTW-W2-S6`, INERT). 0 real principal profiles, 0 restricted-profile principals. Both
   PASS.
5. **OGR1-AC4, AC5, AC6, AC7, AC13** -- each explicitly gated on `state.json`'s `deploy_head` (set only by a
   successful AC2); since AC2 never completed, each returns FAIL with that stated reason rather than measuring
   the OLD, still-running build (which is not what the criterion names).
6. **OGR1-AC8** -- refused to close the ledger: with no leg provable, closing would fabricate proof of an apply
   that never happened. The ledger stays OPEN (correctly reading as a stranded start once its 4h window elapses,
   per `deploy_ledger.py check --red`) until the surprise row's fix lands. FAIL, by design, never faked.
7. **OGR1-AC9** -- read `BASELINE.json` (OG-p-1's own record): no key carries an error-count metric under any
   window (only latency p95 in OGP1-AC11, digests, host facts, bucket/IAM/closure/notification/OAuth-client
   facts). There is no referent to compare a post-deploy error count against, independent of AC2. FAIL.
8. **OGR1-AC10** -- recorded, at AC1 time, the previous release's git-TREE content hash (immutable,
   content-addressed identity for the whole `infra/aws/ec2/opal-gateway` directory, per R-40) beside its commit
   identity; read it back independently at AC10 time -- identical, as expected for an immutable git object.
   Restorability sub-checks: commit exists (OK), `app/revocation.py` present (OK), Schwab flag off in that
   commit's deploy script (OK), but **`app/data_entitlement.py` absent at that commit** -- so the runbook's own
   s.7.2 step 1 precondition ("not older than ... the restricted-profile denial") FAILS for the actual previous
   release. Surprise row `NFRA_OPLGTW-W2-S7`. FAIL, truthfully -- the hash mechanism itself is proven correct.
9. **OGR1-AC14** -- built a scratch copy (`.scratch/og_r1_ac14/`, untracked, removed after the run) of
   `app/integrations/schwab/aws_roles.py` with its one `sts.assume_role(...)` call site replaced by an immediate
   `raise`; loaded it as a distinct module under the real `app.integrations.schwab` package (so its relative
   imports resolve identically); constructing an `AssumedRole` and calling `.session(lambda: True)` raised
   before any AWS call, and `git status --porcelain` on the tracked file was empty. PASS.

## Surprise rows filed (all committed, `org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md`)

- **NFRA_OPLGTW-W2-S5** -- BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~O`. The halt-gate identity-resolution
  defect that blocks OGR1-AC2 (root cause above, with file:line citations).
- **NFRA_OPLGTW-W2-S6** -- OBSERVATION, INERT. Leftover test fixtures in the live access-state table (OG-i-1 /
  OG-i-5's own probes), classified and excluded by OGR1-AC3/AC12 rather than false-failing on a non-zero count.
- **NFRA_OPLGTW-W2-S7** -- OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~O`. The currently-deployed (previous)
  commit fails the runbook's own rollback restorability precondition (no `app/data_entitlement.py`).

## Not attempted / declared exclusions

- Setting `SCHWAB_ACCOUNT_REF_SECRET_ID` in the release configuration (WORKER FACE narrative, not a graded
  criterion): requires editing `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, outside this order's `<paths>`
  grant. No AC1-AC14 criterion tests it; leaving it unset keeps `app/account_ref.py`'s `UNAVAILABLE` default,
  consistent with "you do not enable anything." Not filed as a separate surprise row (blocks no criterion).

## Validation

- `jsonschema.validate` against `org/standards/PROOF_OF_SPEC.schema.json`: SCHEMA VALID (this run).
- `bash .tools/commit-gate.sh` on both probe scripts: clean, 2 of 2 files.
- `py -3.12 .tools/proof-of-spec-check.py <instance> OGR1-AC1,...,OGR1-AC14`: see the run recorded immediately
  below this file's commit in the session log.
