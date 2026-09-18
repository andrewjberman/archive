# RESULT -- IRPT_BCKEND.TO-IB-rtd-5: the route-bindings drift resolved under both halves

**Worker:** `0.9.0_WK_IRPT_BCKEND~3`. **Branch tip:** `d0efd33085cf1e9f5bce2a211f2346eb624f0318` (LOCAL, `wk-irpt_bckend-4-3b`).
**Committed this order:** `e066636be0` (ledger OPEN), `9be69444d7` (ledger CLOSE), `d0efd33085` (surprise row
`IRPT_BCKEND-W3-S40`).

## THE ACT, PERFORMED

Targeted `terraform apply -target=aws_s3_object.mdpf_route_bindings`, sourced from the committed LF bytes
(`git cat-file -p HEAD:data/mdpf/config/route_bindings.yaml` == 13,516 bytes, sha256
`98f5e9c51d016d5283562e525b53088292576d86752c6cf0449865fbf328d923`, git oid `73924ab7efbf8eb3808bd9994bbf7a95ed1f3e2e`
via `git hash-object --no-filters`), materialised temporarily at `data/mdpf/config/route_bindings.yaml`
(this box's normal checkout renders that path CRLF, sha256 `37eb8451...`, per `.gitattributes` carrying no
`eol` attribute on it -- `git check-attr eol` reads `unspecified`) and restored via `git checkout --`
immediately after every plan/apply so the tracked file's CONTENT was never edited (`git status --porcelain`
reads clean for that path at every checkpoint, including after the battery's own two plan re-runs).

Both mechanical conditions were held BEFORE the apply (targeted plan, this session, `.scratch/tf_plan_targeted.txt`,
not committed -- scratch): the plan named `aws_s3_object.mdpf_route_bindings` alone, `Plan: 0 to add, 1 to change,
0 to destroy`, `content-sha256 "c9e54ce28351752a382cc14ac17c380ccea471da9191aa1170cf834cbf971fcd" ->
"98f5e9c51d016d5283562e525b53088292576d86752c6cf0449865fbf328d923"`. The apply (`HALT_ACK=1 bash
.tools/safe-apply.sh -chdir=infra/aws/terraform/mdpf-pipeline apply -target=aws_s3_object.mdpf_route_bindings
-auto-approve`, this session) read `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.` (the HALT-GATE's
25 pending fabric messages were reviewed in full -- none `[STOP]`-class, none addressed to this act -- and
acknowledged per the tool's own usage line, `HALT_ACK=1 ... apply ...`).

**Served object identity, before -> after (`head-object`, this session):**

| | VersionId | ETag | content-sha256 metadata | ContentLength |
|---|---|---|---|---|
| before | `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz` | `56a03a1410848f88b006f1f98b69dced` | `c9e54ce2...971fcd` | 12,008 |
| after | `WXkE2epIOTpxH8OJap.2h35dhJkd1whq` | `650f893a7b9594404ce1d6f067b5b078` | `98f5e9c5...328d923` | 13,516 |

## R45-AC1 -- PASSES BY OUTPUT

Invocation: `timeout 1800 py -3.12
org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rtd_5.py`
(this session, RC=0; verbatim output at `IB-rtd-5_R45-AC1_battery_output.txt`).
Deciding line: `IBR45-ROUTE-BINDINGS-DRIFT-RESOLVED-ROOT-CONVERGED`, printed only because every arm held
(`SUMMARY: {"arm_a": true, "arm_b": true, "arm_c": true, "arm_d": true}`,
`battery_ib_rtd_5.py:335 @d0efd33085`).

- **(a) `2 of 2` halves at HEAD naming the packet blob:** `battery_ib_rtd_5.py:81-144 @d0efd33085` (`arm_a`)
  re-hashes the packet LIVE (`git hash-object` == `d3dfc6f6f335762ad9b955d17a1441c13ef088e7`, matching the
  hand-off line's expectation) and re-reads both half files, confirming each names the packet's blob prefix
  and the targeted-apply act with the committed sha256's 8-hex prefix (the CTO half quotes only the
  abbreviated form throughout -- `NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtd-5_ROUTE_BINDINGS.md:26,51
  @55825f9669`, `` `98f5e9c5…` ``). Battery output line 5-8 (this run): `2 of 2 halves name the packet blob
  AND the act`.
- **(b) The act under ledger, plan equal to the packet's, before -> after identities, post-apply plan on the
  root:** `battery_ib_rtd_5.py:146-228 @d0efd33085` (`arm_b`) reads the CLOSED ledger entry
  (`org/critical_paths/change_management/20260918T1501Z_ib-rtd-5-route-bindings_deploy_completion.md@9be69444d7`,
  both legs proven, no OPEN sentinel), re-derives before/after content-sha256 LIVE via versioned `head-object`
  (prior `iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz` == `c9e54ce2...`, current == `98f5e9c5...`, VersionId changed),
  re-runs a TARGETED plan NOW (LF-sourced) reading "no changes" (already converged, durable), and re-runs the
  UNTARGETED plan NOW (LF-sourced): **0 resource actions on the root** -- no `Plan:` summary line at all, no
  `aws_s3_object.mdpf_route_bindings` diff block; the ONLY thing the untargeted plan reports differently is a
  `Changes to Outputs:` block for the derived `mdpf_route_bindings_sha256` output (still `c9e54ce2...` cached
  in state because a `-target` apply does not recompute outputs -- exactly what the apply's own emitted
  warning said would happen: *"output values may not be fully updated ... Run terraform plan"*). This is a
  state-bookkeeping artifact of `-target`, not a second drifted resource, filed as
  `IRPT_BCKEND-W3-S40 @d0efd33085` (INERT) rather than treated as a resource-level drift, since applying
  anything further on this root to clear a cached output value would violate this order's own BOUNDS
  ("nothing else on that root is applied"). Read strictly by RESOURCE actions -- what S68 is about, the served
  object's content -- the root is `0 to add, 0 to change, 0 to destroy`.
- **(c) Consumers `4 of 4` load the new object:** `battery_ib_rtd_5.py:231-302 @d0efd33085` (`arm_c`), each
  against its own real load path: (1) `mdpf-gold-lambda`'s deployed zip, downloaded live this run, packaged
  `route_bindings.yaml` member loads (schema check) and its sha256 (`98f5e9c5...`) equals the new served
  object's -- `data/mdpf/scripts/gold/mdpf_gold_consolidator.py:304-323 @1465fd3f7d` load path,
  `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:158` bakes it from the repo file at build
  time; (2) `build_mdpf_spine.load_bindings()` called live against `data/mdpf/config/route_bindings.yaml`
  (`data/mdpf/scripts/gold/build_mdpf_spine.py:53-65 @bf74d031c1`), loads without error; (3)
  `route_bindings_tieout.py` run live (`data/mdpf/config/route_bindings_tieout.py @8058f55233`): `34 tie
  rows checked ... 34 TIE / 0 FAIL`; (4) the EC2 runner's own synced key
  (`opal-data-mdpf/code/config/route_bindings.yaml`, a DIFFERENT bucket/prefix per
  `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:130,136-140 @cf838e54d5`) `head-object` succeeds,
  confirming that consumer's own load path is intact and genuinely separate from this key's drift (not
  applicable, as the packet found).
- **(d) The prior `VersionId` retrievable:** `battery_ib_rtd_5.py:305-321 @d0efd33085` (`arm_d`) --
  `head-object --version-id iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz` succeeds, ETag `56a03a14...` (the pre-act bytes).
  Rollback recipe PRINTED, not run: `.tools/aws s3api delete-object --bucket opal-data-assets --key
  config/mdpf/route_bindings.yaml --version-id WXkE2epIOTpxH8OJap.2h35dhJkd1whq`.

**Denominator summary:** halves 2 of 2; ledger legs 2 of 2 closed; consumers 4 of 4 loaded without error, 1
of 4 (the packaged Lambda copy) with a hash check reading EQUAL to the new object; tie-out 34 of 34 TIE / 0
FAIL; rollback 1 of 1 prior version retrievable.

## R45-AC2 -- JUDGMENT, RECORDED, NOT SELF-GRADED (for `3.0.0_SA_CVO`)

**Whether S68's exposure is closed (the root converged) or merely moved:**

CLOSED, on the RESOURCE-level reading both never-widen halves' condition (3) is written to test. The served
object `s3://opal-data-assets/config/mdpf/route_bindings.yaml` now carries the committed content
(`head-object` this session: `content-sha256` `98f5e9c51d016d5283562e525b53088292576d86752c6cf0449865fbf328d923`,
`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtd-4.md:19 @1922c400e1` naming that as the committed identity). The
post-apply untargeted `terraform plan` on the root reports **zero resource actions** -- no `Plan:` summary
line, no diff block for any resource, including the object itself (`battery_ib_rtd_5.py:198-206 @d0efd33085`,
this run's own re-derivation). The live W-1 tie-out validator reads `34 of 34 TIE / 0 FAIL`
(`data/mdpf/config/route_bindings_tieout.py @8058f55233`, run this session), the SAME instrument the packet
used to justify the committed content over the stale served content in the first place -- so the object the
root now serves is the one the live code constants actually agree with, not merely a different stale value.

ONE THING DID NOT FULLY CLOSE, and is reported plainly rather than folded into a silent PASS: the root's
Terraform STATE still carries the PRE-act value (`c9e54ce2...`) for the derived OUTPUT
`mdpf_route_bindings_sha256`, because the `-target` apply (both the packet's and the halves' own
recommendation, to bound blast radius) never recomputes outputs -- Terraform's own apply-time warning said
so at the moment of the act (*"output values may not be fully updated ... Run terraform plan to verify"*),
and the post-apply untargeted plan (`-detailed-exitcode` rc=2, this session) confirms it is still pending in
state. This is NOT a second copy of the drift -- nothing reads `c9e54ce2...` as an object's content
anywhere; it is a cached OUTPUT VALUE in Terraform's own bookkeeping, distinct from any resource -- and this
order's BOUNDS forbid applying anything further on this root to clear it ("nothing else on that root is
applied; `-target` only if the packet names it"). Filed as `IRPT_BCKEND-W3-S40 @d0efd33085` (INERT: no
consumer reads this output value at runtime per the packet's own ARM B census -- it exists for the
build/coordination plane's manifest recording, `infra/aws/terraform/mdpf-pipeline/config_objects.tf:52-58
@1450298a1dfb`).

**S68's grading, stated:** if S68 is read as "is the served object's CONTENT current," it is CLOSED. If S68
is read to also require the root's cached STATE OUTPUTS current, it stays technically open on that one
non-resource field until an unrelated future apply/plan on this root recomputes outputs as a side effect (no
infrastructure change, per Terraform's own text). Both never-widen halves' condition (3) is written in terms
of resource actions ("a non-zero untargeted plan means that measurement was wrong" -- discussing the packet's
measurement of the ONE DRIFTED RESOURCE), which this act satisfies.

**Whether the `eol` finding needs a repo change so the drift cannot recur from this device:**

YES, as a routed recommendation, not an act this order performs (explicitly out of scope: both halves,
`NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtd-5_ROUTE_BINDINGS.md:36 @9d7b707082` and
`NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtd-5_ROUTE_BINDINGS.md:85-86 @55825f9669`, both say "the file
owner's row, not this act's"). `git check-attr eol -- data/mdpf/config/route_bindings.yaml` reads
`unspecified` (this session and the packet's, `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtd-4.md:37 @1922c400e1`) --
without an `eol=lf` (or `text eol=lf`) `.gitattributes` line for this path, ANY future checkout on an
autocrlf-enabled Windows box renders it CRLF, and an operator who runs `terraform apply` on this root
directly from that render (skipping the LF-materialisation dance this order and IB-rtd-4 both had to
perform by hand) reproduces exactly the instrument trap the packet found -- uploading `37eb8451...` bytes
instead of `98f5e9c5...`. The recurring risk is structural (every future apply on this object from an
un-normalised Windows checkout), not one-time, so the repo change (a `.gitattributes` entry) is the durable
fix; this order's targeted apply is a one-time correction of the SYMPTOM (the served bytes), not the CAUSE
(the missing `eol` attribute).

## Instrument note (not a criterion, carried for completeness)

`.tools/safe-apply.sh`'s HALT-GATE fired on 25 pending fabric messages addressed to this worker's issuer
(`2.0.0_SA_COO~B`) and no others; none were `[STOP]`-class or named this act, and re-running with
`HALT_ACK=1` (per the tool's own documented usage) proceeded correctly to the apply. Not filed as a surprise
row: this is the gate's documented, intended behaviour for routine pending mail, not a premise the task order
or the halves got wrong.
