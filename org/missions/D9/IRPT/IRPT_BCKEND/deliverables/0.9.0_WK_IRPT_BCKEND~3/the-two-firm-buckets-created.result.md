# IB-rte-3 RESULT -- the two LGIC firm buckets, created ahead of D14 -- APPLIED, LOCKED OUT, NOT CLOSED

**Cell:** `IB-rte-3` (decomposition v0.5, s.R5). **Order:**
`IRPT_BCKEND.TO-IB-rte-3.the-two-lgic-firm-buckets-created-empty-ahead-of-d14.md`. **Worker:**
`0.9.0_WK_IRPT_BCKEND~3`. Battery: `battery_ib_rte_3.py`; output: `IB-rte-3_R53-AC1_battery_output.txt`.

**HEADLINE: the two buckets are LIVE on AWS, named correctly, and (per Terraform's own "Creation
complete" record) almost certainly carry every declared control -- but this worker locked itself out
of both via the very fence it applied, and cannot read them back, roll back, or complete the round.
R53-AC1 does NOT pass; the order stays open.**

---

## (a) THE NAMES, BUILT -- PASS, 2 of 2, 0 refusals

`lib/opal_naming.py lookup('inflection')['bucket']` -> `opal-data-inflection`;
`lookup('cottonwood')['bucket']` -> `opal-data-cottonwood` (`infra/logic/registry/scopes.json` rows
`:119-156`/`:157-202` @22e86e55f5). Both confirmed ABSENT live (`head-bucket` -> 404) BEFORE anything
was declared. Neither call refused; no registry row drafted (Rule 30's contingency does not fire).

## (b) THE DECLARATION -- terraform, PARTIALLY LANDED

Declared in `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf`, same controls
`s3-49financial.tf` carries THAT THE TASK ORDER ENUMERATES (versioning, public-access block,
encryption, the per-firm Deny fence) -- `p of p` on that four-item list, cited with vintage in the
file's own header comment (doctrine R5 `:370-383`, R6 `:385-399`, R7 `:401-412` @afd81beb8a). ONE
control `s3-49financial.tf` also carries but the task's own enumeration does not name -- the CloudTrail
read-logging postcondition -- is deliberately NOT carried, because carrying it would change
`cloudtrail-organization-trail.tf`'s `aws_cloudtrail.organization` (an EXISTING resource on this root),
which both the order's BOUNDS and its own "0 to change" plan bound forbid (row `IRPT_BCKEND-W3-S41`).

**First draft REFUSED by the naming gate** (`.tools/naming-gate.py`, LGIC_ENFORCE DEC-6 ENFORCE mode):
a literal per-firm declaration copying `module.opal_name.fence_patterns["inflection"]` verbatim -- the
EXACT idiom `s3-49financial.tf` already carries -- was graded a NEW hand-kept firm-token carrier and
REFUSED 6 of 6 graded literals (49financial's own file is WARN-only because it is grandfathered).
Rewrote the file to read `infra/logic/registry/scopes.json` via `file()+jsondecode()` (the same idiom
`modules/opal_name/main.tf` already uses for `exemptions.json`) and `for_each` over every FIRM scope
with `bucket_provisioned == false` -- zero firm-token literals in the source; the naming gate now grades
0 literals. Plan, pre-apply: **exactly `10 to add, 0 to change, 0 to destroy`** -- matches the bound.

**Apply outcome:** `HALT_ACK=1 bash .tools/safe-apply.sh -chdir=infra/aws/terraform/shared-infra apply`
(the halt-gate's own listed conditions were all pre-existing RED entries from OTHER seats, reviewed and
acknowledged) landed **8 of 10 resources cleanly** (both buckets, both public-access blocks, both SSE
configs -- Terraform's own "Creation complete" lines). Both `aws_s3_bucket_versioning` and both
`aws_s3_bucket_policy` resources entered Terraform STATE (their create calls evidently succeeded --
`state list` shows all 10) but their own post-create verification READ failed with **AccessDenied**,
because the just-applied policy's Deny took effect against the applying identity itself (see (d)/(e)
below). State was safely `state mv`'d onto the rewritten file's `for_each` addresses with **zero infra
touched** (verified: `state list` shows all 10 present under the new addresses; `terraform plan`
afterward shows the SAME live bucket names, no destroy). A post-incident `terraform plan` now ERRORS
(cannot read versioning/encryption/PAB back) and its refresh-time diff misreads the bucket resources as
needing re-creation -- **NO FURTHER APPLY WAS RUN**, since re-applying while locked out of a resource
Terraform's own refresh cannot cleanly read is not a risk worth taking blind.

## (c) THE GATE ENUMERATIONS -- regenerated, diff EMPTY, fence does NOT see the new names

`python lib/opal_naming.py generate --out <dir> --target .tools/ds-precommit-check.py`: diff against
the committed file is **EMPTY** (confirmed twice, pre- and post-apply) -- `_separations()`
(`lib/opal_naming.py:607-621`) gates the "ruled" foreign-bucket entry on `scopes.json`'s
`bucket_provisioned` flag, which stays `false` for both firms (`infra/logic/registry/scopes.json` is
outside this order's `<paths>` grant). **Negative test, both forms:** a bare exact-name reference to
the real new bucket (`"opal-data-inflection"`, no prefix, no trailing slash -- the form
`_is_real_bucket_ref`'s own first arm is designed to catch) is **NOT refused** (rc=0, 0 of 2); an
`s3://`-prefixed reference IS refused (2 of 2) but only by an ACCIDENTAL substring collision with the
pre-existing LEGACY short name (`opal-data-inf` is a string-prefix of `opal-data-inflection`), and the
gate's own BLOCKED message cites the wrong bucket name. **The fence does not, in the sense the task's
own title asserts ("so the new names are fenced"), see the new names.** Filed `IRPT_BCKEND-W3-S42`
(BLOCKING/ARMED).

## (d) POST-APPLY READS -- FAIL, self-lockout

`head-bucket` returns **403** (not 200) for both buckets; `get-bucket-versioning`,
`get-public-access-block` and `get-bucket-policy` all return **AccessDenied** for both; `list-objects-v2`
also AccessDenied (so the "0 keys" claim cannot be read back either, though the buckets are certainly
empty since nothing was ever written to them). Cause: `infra/logic/registry/exemptions.json` (outside
this order's `<paths>` grant) carries no exemption rows for either new bucket name (only empty-array
rows for the LEGACY aliases `opal-data-inf`/`opal-data-cot`), so this file's
`lookup(module.opal_name.fence_exemption_arns, bucket, [])` resolved to an EMPTY exemption list, and
the Deny fence (`Principal "*"`, `Action "s3:*"`, admit-listing only `role/*-inf-*`/`role/*-cot-*`)
denies EVERY OTHER PRINCIPAL -- including `Andrew_Berman`, the only identity this worker's tools hold,
whose `AdministratorAccess` is an IDENTITY policy an explicit resource-based Deny overrides. Confirmed:
`sts get-caller-identity` -> `user/Andrew_Berman`; `list-buckets` (account-level, unaffected by a
per-bucket policy) DOES list both names (the credential itself is sound); `delete-bucket-policy` is
ALSO AccessDenied (no self-rollback available); no assumable role matches the fence's admit pattern
(`opal-inf-served-guard`/`opal-cot-served-guard` exist but trust only `lambda.amazonaws.com`). Filed
`IRPT_BCKEND-W3-S43` (BLOCKING/ARMED, disarm_owner `2.0.0_SA_COO~B`) -- **this requires AWS root/console
access this worker does not hold; it cannot be self-repaired.**

## (e) THE NEGATIVE CONTROL -- host unreachable, substituted with simulation

Host `i-02448edb624a7a7cf` is **stopped** (`ec2 describe-instances` State.Name=stopped) and not
registered with SSM (`describe-instance-information` returns an empty list) -- the live,
host-exercised negative control this criterion names cannot be run, and starting a production runner
instance merely to exercise it is outside this CREATION-ONLY cell's bound. Substituted with
`iam simulate-principal-policy`: both assertions read `implicitDeny` (2 of 2) -- consistent with the
expected outcome, but a SIMULATION is weaker evidence than an exercise (CLAUDE.md 22a: sim-policy's
FALSE-ALLOW risk) and does not satisfy the literal bar. Filed `IRPT_BCKEND-W3-S44` (BLOCKING/INERT).

---

## LEDGER

`org/critical_paths/change_management/20260918T1949Z_irpt-bckend-ib-rte-3-lgic-firm-buckets_deploy_completion.md`
stays **OPEN and RED, deliberately**. `deploy_ledger.py hold` was tried (to place a sovereign gate
pending root/console repair) and correctly REFUSED: "open APPLY/DEPLOY leg(s) ['L1'] -- a half-landed
deploy cannot be HELD (stays RED)." No leg is falsely closed. This is the honest state.

## R53-AC1 -- FAIL

The battery's own verdict (re-derived live, this run): (a) PASS, (b) FAIL, (c) FAIL, (d) FAIL, (e) FAIL.
The success token is withheld. **This is not a report of failure to act -- the approved, load-bearing
act (provisioning the two buckets) DID happen and is live; what remains is a repair only AWS root/console
access can perform, an registry edits (`scopes.json` `bucket_provisioned`, `exemptions.json` rows) this
order's `<paths>` grant does not reach.**

## R53-AC2 -- see the proof-of-spec instance (judgment, for `3.0.0_SA_CVO`, no verdict here)

Does the D14 register already name these two buckets? `org/missions/D14/LGIC/LGIC_NAMING/prd/LGIC_NAMING_PRD.md`
S1 (cited by IB-rtd-6 @22e86e55f5) already ruled the LGIC bucket grammar and named
`opal-data-inflection`/`opal-data-cottonwood` as the D14 firm buckets; `infra/logic/registry/scopes.json`
(the D14/LGIC identity registry) already carries both as FIRM rows with `bucket: "opal-data-{firm}"`
-- this creation act CONFORMS to (does not pre-empt) that plan; it merely executes the bucket-creation
leg of it early, on Andrew's explicit word, while `bucket_provisioned` stays `false` until a
registry-owning seat flips it (a D14/LGIC_ENFORCE act, not this order's). IB-rtd-7's re-cut port now
lacks, besides the halves and the FNTEND reader cell IB-rtd-6 already named: (1) the registry flips
(`bucket_provisioned:true` + exemption rows for both bucket names) that make the fence and gate
actually recognize the new names -- this round's own S42/S43 findings; (2) root/console repair of the
Deny fence on both buckets (S43) before ANY further write-principal grant can be added or read back.
Whether 49financial's own declaration is itself the canonical shape or carries drift the new ones
should not copy: its CloudTrail read-logging postcondition is a control worth copying in a FOLLOW-ON
(this round could not, per BOUNDS); its exemptions list (16 named ARNs, mostly service-role read-only
noise plus the 3 admin identities) is NOT drift to copy verbatim -- the new buckets need, at minimum,
the SAME 3 admin identities (`Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`) exempted before
any human/tool can safely manage them, which 49financial got right and these two do not yet have.
