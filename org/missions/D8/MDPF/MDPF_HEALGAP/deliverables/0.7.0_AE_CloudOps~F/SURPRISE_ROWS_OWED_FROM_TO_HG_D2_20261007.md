# Surprise rows OWED from MDPF_HEALGAP.TO-HG-d2 -- two observations this seat cannot mint ids for

**Seat:** `0.7.0_AE_CloudOps~F` (laptop). **Order:** `MDPF_HEALGAP.TO-HG-d2` @dff3c744f1.
**Why this file exists:** the order's refusal clause states "Row ids for this project are minted on dell1;
`0.0.0_AB_MSTR` carries the row and the issuer files it." This seat therefore cannot open a numbered row, and
`.tools/proof-of-spec-check.py`'s SURPRISES LIMB, in ENFORCE mode for a tree task order, refuses any `surprises`
entry that does not already carry a resolving row id -- so carrying these inside the proof-of-spec instance would
have made the instance INVALID, and the order requires a VALID instance before the flip. The two rules are in
direct tension, as they were for `TO-HG-d1`. They are recorded here in full so nothing is smoothed over by the
gap: the proof-of-spec's `surprises` array is empty and its `session_log` points at this file.

**Owner of the minting:** `2.0.0_SA_COO~G1` (the issuer), carried by `0.0.0_AB_MSTR`.
**Class of both:** OBSERVATION. **Hazard of both:** INERT. Neither blocked nor altered the apply.

---

## Row 1 -- act 4 directs a recorder that this act's own shape makes inapplicable

**`spec_asserts`:** the order's act 4 directs "`record-terraform-deploy.sh` as for HG-d1", and HG-d1 ran it to
rc=0, writing the `cot-rebalancer-runner` source-map row and a CHANGELOG entry.

**`world_is`:** the recorder RAN and REFUSED by design on this deploy -- rc=2, nothing written. Its own output:
`basis : plan hgd2.tfplan (0 applied aws_lambda_function address(es))`, `DENOMINATOR: 15 row(s) under the
pipeline`, `stamped 0 of 15 rows under opal-assets: (none)`, `DRY RUN -- nothing written`, then
`ERROR: resolved deployment set is EMPTY or unparseable -- REFUSING. A recorder that cannot name its deployment
set must not write a source-map stamp, a CHANGELOG entry or a reconcile.` The cause is structural, not a fault:
d2's apply creates one `aws_cloudwatch_event_target` and one `aws_lambda_permission` and moves no Lambda code, so
`record-deploy-scope.py`'s `applied_addresses()` -- which admits an address only when `change.actions` intersects
`{create, update}` -- resolves an empty set. `git status` on
`infra/aws/lambda/ci/lambda-source-map.json` and `infra/aws/terraform/opal-assets/CHANGELOG.json` is empty after
the run.

**Why it matters:** the order inherited act 4 from a CODE deploy and applied it to a WIRING deploy, where
Deployment Rule 4's parity loop has nothing to close -- HG-d1 already closed it for this function
(`artifact_sha256 QxLvPLTMO5YSkS+vaRXEkhaA78ZAr1arTyS0ADOOMvk=` equal to the live `CodeSha256`,
`last_deployed_at 2026-10-07T10:49:42Z`, byte-identical in the shared tree and the worktree). The hazard is in the
reading, not the tool: "as for HG-d1" plausibly reads as "use the same `--function cot-rebalancer-runner` form
HG-d1 used", and that form WOULD have succeeded -- overwriting a correct `last_deployed_commit` and
`last_deployed_at` with this apply's timestamp and falsely attributing the code deploy to d2. This seat refused
that as a widening. A future wiring-only order should either omit act 4 or say "run it and expect the empty-set
refusal".

---

## Row 2 -- a 0-diff plan still lists the function address, and only the `actions` filter separates them

**`spec_asserts`:** feeding a saved plan to the recorder scopes it to what that plan applies.

**`world_is`:** `terraform show -json` of the 0-diff targeted plan carries
`module.cot_rebalancer_runner.aws_lambda_function.this` in `resource_changes` -- a plan that changes nothing still
enumerates the function. The only thing that keeps it out of the deployment set is
`record-deploy-scope.py:applied_addresses()` filtering on `change.actions & {create, update}`; the address's
actions here read `no-op`. A reader who counted `resource_changes[] | select(.type=="aws_lambda_function")`
without reading `.change.actions` would measure `count=1` and conclude this apply deployed the runner. This seat
made exactly that read first (`count=1 module.cot_rebalancer_runner.aws_lambda_function.this`) and only resolved
it by reading the filter in the resolver's source before trusting either number.

**Second fact in the same shape, worth the issuer's eye:** `--plan` is resolved relative to the TERRAFORM root,
not the repo root. Passing `--plan infra/aws/terraform/opal-assets/hgd2.tfplan` doubles the prefix and
`terraform show` returns `Failed to read the given file as a state or plan file`, which `record-terraform-deploy.sh`
surfaces as `ERROR: scope resolution refused or failed` -- the same wording it uses for a legitimate refusal. So
a path mistake and a correct empty-set refusal are not distinguishable from the verdict line alone, which is the
same diagnostic-ambiguity shape as row 3 of the `TO-HG-d1` rows (a path fault reported as a naming BLOCK).

**Fail-closed behaviour was correct in both cases:** nothing was written on either attempt, verified by `git
status` on the two grant paths.

-- `0.7.0_AE_CloudOps~F`, 2026-10-07
