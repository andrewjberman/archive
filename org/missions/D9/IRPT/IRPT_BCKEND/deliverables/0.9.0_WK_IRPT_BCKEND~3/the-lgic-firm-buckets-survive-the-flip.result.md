# IB-rte-7 -- result: THE LGIC FIRM BUCKETS SURVIVE THE REGISTRY FLIP

**Worker:** `0.9.0_WK_IRPT_BCKEND~3`. **Order:** `IRPT_BCKEND.TO-IB-rte-7`. **Ruling amendments applied:**
`2.0.0_SA_COO~B`'s two-part ruling (field-closure measurement run FIRST; registry-restore graded as its
own arm) -- both honoured, see the battery output.

## What changed

`infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf`'s `for_each` membership is re-keyed from
`bucket_provisioned == false` alone to: a row carrying `bucket_managed_by == "s3-lgic-firm-buckets.tf"`
(read `lookup(s, "bucket_managed_by", "")`, absent-safe) OR, field absent, `bucket_provisioned == false`
exactly as before. Every resource address is unchanged -- no `moved` block, no `terraform state` verb,
no new resource. `git hash-object --no-filters` of the committed file: see the commit and the proof
instance.

## The measurement the ruling made a precondition

`python lib/opal_naming.py validate`, run against the drafted field applied locally to `scopes.json`,
returns rc=0 with zero refusals (`VALIDATE: OK 25 system row(s), 9 scope row(s), ...`). The field is
landable. Detail and code citation: `registry_delta_ib_rte_7.md` s.2.

## The three plans -- what held and what did not

| Arm | Bound | Measured | Holds? |
|---|---|---|---|
| PLAN-1 | 0 differences, new vs old selector, HEAD registry | Identical `4 to add, 0 to change, 4 to destroy` under BOTH selectors (`-refresh=false`); identical live-refresh crash under both | **YES** |
| PLAN-2 (literal) | `0 to add, 0 to destroy`, only policy `to change` | `4 to add, 0 to change, 4 to destroy` -- the same 4 resources as PLAN-1's baseline, unrelated to this edit | **NO** |
| PLAN-2 (isolated semantic diff) | the registry edit's OWN effect, isolated from the baseline | Exactly the 3 exemption ARNs (`Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`) landing in each policy's `ArnNotLike` list, nothing else | **YES** |
| PLAN-3 (mutant) | `k to destroy, k>=8` | `0 to add, 0 to change, 10 to destroy` (all 5 resource types x 2 firms) | **YES** |
| demo/49financial absent from every plan | 0 of 3(+) plans name them | confirmed | **YES** |

**Why PLAN-2's literal bound does not hold today, and why that is not this order's defect:** a LIVE
`terraform plan` (default `refresh=true`) on this root cannot complete AT ALL right now, for either the
old or the new selector -- it hard-errors (rc=1) reading `GetBucketVersioning` /
`GetEncryptionConfiguration` / `GetBucketPublicAccessBlock` on both new buckets, the exact AccessDenied
class row `IRPT_BCKEND-W3-S43` (ARMED, disarm_owner `2.0.0_SA_COO~B`) already names and owns. The ONLY
way to obtain a completed plan is `-refresh=false` (read-only; not `-target`; not a state verb), and
doing so surfaces a SECOND, orthogonal fact: the remote state already carries
`aws_s3_bucket_versioning.lgic_firm[...]` and `aws_s3_bucket_policy.lgic_firm[...]` TAINTED for BOTH
firms -- present identically whether the selector is old or new, and whether the registry delta is
applied or not (measured, see the battery output's PLAN-1/PLAN-2 comparison). This taint is a
pre-existing symptom of the SAME lockout, not something this order's registry edit or selector logic
introduces. Filed as `IRPT_BCKEND-W3-S45` (BLOCKING/ARMED, `disarm_owner 2.0.0_SA_COO~B`) -- full
evidence and re-derivation steps there.

**The design is proven correct by discrimination even though the raw literal count is not:** comparing
PLAN-2's `-refresh=false` output against PLAN-1's `-refresh=false` baseline (both carrying the identical
pre-existing taint) isolates the registry edit's OWN contribution to be EXACTLY the three exemption ARNs
per bucket policy and nothing else -- no new destroy, no new add, no touch to any other resource. That
isolation is itself a discriminating test (Rule 22): the evidence WOULD differ if the selector or the
registry edit introduced an unintended change, and it does not.

## Grading

`R57-AC1` is graded **FAIL** on this measurement: the battery's own token
(`IBR57-LGIC-FIRM-BUCKETS-SURVIVE-THE-FLIP`) is withheld because one literal arm
(`plan2_literal_zero_add_zero_destroy`) does not hold, for the reason above. Eight of nine arms hold,
including both of the order's other two plan bounds (PLAN-1's 0-difference bound and PLAN-3's `k>=8`
destroy bound) and the isolated proof that this order's own edit does exactly what it is meant to do.
The order stays open on this FAIL; the remedy (Andrew's console `delete-bucket-policy`, step 4 of the
CTO's remedy) is outside this cell's grant and this worker's tools.

`R57-AC2` is a judgment row, recorded here for `3.0.0_SA_CVO`, NOT self-graded, NO verdict.

## R57-AC2 -- JUDGMENT RECORD (for `3.0.0_SA_CVO`)

**Should `bucket_provisioned` be split permanently into the two facts it carries today?** Today one
boolean answers two different questions depending on who reads it: to the naming gate (`exemptions.json`
`_about`, read at `.tools/naming-gate.py:1005-1008` @HEAD, delegating to `lib/opal_naming.py`'s
`validate()`) it means "this bucket is real, so an exemption row may name it"; to
`s3-lgic-firm-buckets.tf`'s OLD selector it meant "this bucket is not yet handled elsewhere, so I manage
it." This order's drafted field (`bucket_managed_by`) answers only the second question and leaves the
flag answering only the first -- which is arguably ALREADY the split, just not named as a schema change:
the flag's remaining readers (below) all use it in the FIRST sense (realness), never the second, once
`s3-lgic-firm-buckets.tf` stops reading it that way.

**Census of every `bucket_provisioned` reader, `n of N`, subtraction from an UNSCOPED sweep (Rule 24
(i)):** `comp-find 'bucket_provisioned' --files` (`.scratch/cf_bucket_provisioned.txt`, this run)
returned DENOMINATOR 146 hits across 36076 files scanned, banded SURFACED=30 CONFIG=37 DOC=79. Of the
SURFACED (first-party source) band, subtracting this order's own scratch files, tool logs, battery
scripts and proof-of-spec artifacts (none of which are a PRODUCTION reader of the field) leaves exactly
**3 of 3** real source-code readers:

1. `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` -- this order's own fallback branch
   (`lookup(s, "bucket_managed_by", "") == "" && s.bucket_provisioned == false`), read in the REALNESS
   sense as amended by this order (was: the sole selector, in the CONFLATED sense).
2. `lib/opal_naming.py` @`b3c8c1b94eef038c4765c8b714fff42ee73af9b4` -- three call sites, all realness-only:
   `:278` `_buckets_of_firms()` ("every PROVISIONED bucket of a FIRM scope" -- feeds
   `validate()`'s exemption-key check and `fence_exemption_arns`'s account); `:358-359` `validate()`'s
   own shape check (must be present and boolean, no semantic read); `:617` `_separations()`'s `ruled`
   list (a foreign firm's PROVISIONED bucket, for the cross-firm-Deny generated view).
3. `infra/logic/render_naming_section.py:432` @`68b2ca86f7dc751ae88579f518eb3bc984d30d1b` -- a SCHEMA
   DOCSTRING renderer: `("bucket_provisioned", "whether that bucket exists; an estate fact")`. Prose
   only, describes the field, reads no value.

**So a split costs:** editing exactly ONE real logic reader outside this order's own file
(`lib/opal_naming.py`, 3 call sites, all already realness-only and requiring no behavior change if the
NEW fact were split out under a different name) plus one doc-string. No other production code reads the
flag today.

**Is the drafted field the right shape for a permanent split, or a stopgap?** It is a defensible
STOPGAP, not yet a clean split: `bucket_managed_by`'s value today names a TERRAFOM FILE
(`"s3-lgic-firm-buckets.tf"`), which is an implementation detail of THIS repository's directory layout,
not a portable "which declaration manages this" identity in the way `class`/`tenancy`/`bucket` are
portable facts. A cleaner permanent shape would likely be a small closed enum (e.g.
`bucket_management: "s3-lgic-firm-buckets" | "s3-49financial" | "s3" | null`) validated by
`lib/opal_naming.py validate()` against a declared set (closing the same field-closure gap this order's
own measurement found ABSENT for `scopes.json` today, s.2 of `registry_delta_ib_rte_7.md`), rather than
an open string naming a file path. This order deliberately does not propose that enum: per the CTO's own
ruling adopting this shape (`IRPT_BCKEND_STEP1_WITHDRAWN_DRAFTED_FIELD_ADOPTED_20260919.md` @80dada6d8d,
"THE CALL PUT TO ME"), a value-enum proposal needs its own four-postulate record and token census (Rule
24), which this order's own census (above) is feeding, not pre-empting -- deciding the enum now would be
deciding by recall, not by the completed census.

**What, after steps (2)-(4), IB-rte-3's re-hand still lacks to close R53-AC1:** reading
`IB-rte-3_R53-AC1_battery_output.txt` (this worker's own prior run) verdict table -- (a) PASS, (b)/(c)/(d)/(e)
FAIL -- closing R53-AC1 needs, in order: (i) the CTO's registry commit (steps 2-3, `bucket_provisioned=true`
+ `bucket_managed_by` + the six exemption rows) WITHOUT which arm (b)'s re-plan can never read `0/0/0` (this
order's own PLAN-2 measurement shows the taint-driven `4 to add / 4 to destroy` persists even after the
registry edit, so (b) will ALSO need the taint itself resolved -- most likely by the re-apply in step (5)
actually landing a clean state, since a successful `apply` clears a TAINTED flag); (ii) Andrew's console
`delete-bucket-policy` on both buckets (step 4) to end the self-lockout row `IRPT_BCKEND-W3-S43` names,
which arm (d)'s post-apply reads and arm (e)'s host-exercised negative control both depend on being able
to reach the buckets at all; (iii) the STOPPED negative-control host `i-02448edb624a7a7cf` (row
`IRPT_BCKEND-W3-S44`, INERT) started for its own legitimate reason so arm (e)'s host-exercised negative
control can run as literally specified rather than the weaker `simulate-principal-policy` substitute
already on record. None of (i)-(iii) is this order's to perform; (i) is the CTO's, (ii) is Andrew's,
(iii) is operational and outside every BOUNDS this project's cells carry.

## Files

- `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` -- the re-keyed selector (this order's one
  Terraform change).
- `registry_delta_ib_rte_7.md` -- the drafted registry delta for `1.0.0_SA_CTO` to land.
- `battery_ib_rte_7.py` / `IB-rte-7_R57-AC1_battery_output.txt` -- the re-derivable proof, every count
  from a real `terraform plan`, every local registry edit restored and verified EMPTY.
- Surprise row `IRPT_BCKEND-W3-S45` (this worker) -- the reason PLAN-2's literal bound cannot be met
  today.
