# OPAL_ASSETS.C1 — THE MONOLITH: Terraform `s3://opal-data-assets` + prefix grammar + router IAM

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO (coordination lane, Andrew-direct ~01:07Z) — authored from PRD v1.3.1 §4 row C1; architecture owner remains 1.0.0_SA_CTO</issued_by>
<date>2026-07-14</date>
<status>complete</status>
<closure date="2026-07-14 ~04:3xZ" by="2.0.0_SA_COO (state reconciliation, Andrew-ordered)">
ALL ACs DELIVERED + INDEPENDENTLY VALIDATED + RAVC-CLOSED: bucket live (head-bucket us-east-1, AES256,
versioning, COO-verified ~02:55Z), 22/0/0 apply + 0-diff (0d5b0cdda, tag opal-assets-v0.4.0), 10/10
probes _probe/-only at the ruled grammar, fence matrix with the PAIRED instrument control (real inf
writer allowed / router explicitDeny on the SAME exact ARN incl. the Door-6 key), deliverable-5
design-review evidence, source map n/a (no lambda in C1), NEVER#6 half-landed apply finished in-session
(IAM-tag-parentheses gotcha banked). Successor work lives in its own TOs (C2 mirror; C3/C4 landings).
</closure>
<project>OPAL_ASSETS — Grand Consolidation P1</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §2 (target architecture) + §2b (end-state) + §4 row C1 + §4a compiler mandates + §4 cross-domain — **authored at v1.3.1 @ 34333469b; ruled amendments folded through v1.3.8 @ a0ed08933 (SSE final state, grammar rulings 15/v1.3.6, denominator law 13b)**</prd>
<priority>P1 — **THE CRITICAL PATH for every LANDING: C2, C3-landing, C4-landing and C6-wiring all wait on this bucket.** (C6-authoring, C7's DS half, C10, C12 and the 0824 recovery are C1-independent and proceed in parallel — the dependency map is PRD §4's, not broader.)</priority>

<authority amended="2026-07-14 ~02:3xZ per Andrew-ordered review (findings 8/47) — the release chain is now CITED, not inferred">
The 00:25Z dispatch hold ("Wait to dispatch until I give the go, I want to respawn the workers first") is
RELEASED on this chain:
  1. Andrew's release protocol (CTO relay, msg 20260714T005942Z): "Andrew is spawning YOU + DS + 0.6.2...
     Protocol he set: spawned agents reach out to ME confirming readiness; I validate against the live
     roster and GO the staged TOs in dependency order." The GO condition Andrew set = respawn + readiness
     confirms, with CTO holding the GO authority.
  2. Andrew, verbatim (~01:07Z, to CTO, interactive): "You can direct these through COO, I do not want you
     to be distracted with Coordination. That can be their job."
  3. CTO's pre-authorization (msg 20260714T010814Z, verbatim): "GO RELAYS against the staged TOs AS
     WRITTEN... 0.7.0 on his registration + confirm: the CONTAINER package -- C1 (critical path, first),
     C2, C7 deploy-half, C9" — "pre-authorized, no round-trip to me needed."
  4. Precondition met on the live roster (all four workers LIVE, verified immediately before relay);
     0.7.0's readiness confirm received 20260714T011240Z.
Coordination lane is COO's; CTO retains architecture, rulings, and EVERY APPLY GATE (C1's apply
subsequently GO'd by CTO 20260714T020311Z).
</authority>

## Scope

Stand up **THE MONOLITH** — one bucket holding canonical bronze + silver for EVERYTHING.

Andrew, verbatim (~01:05Z), which IS the scope:
> "the schwab data will be brought in to the bronze level of opal-data-assets/schwab/{acct}/bronze, it will
> probably be in .zip form. In ~/silver, it will be parquet. In essence, what I am building to here is
> actually having one monolith bucket, all in canonical form (raw bronze, parquet silver, gold just the
> dynamodb to start). I would like to store EVERYTHING in here, at least with regard to bronze and silver.
> Then the gold runners/platinum buckets stay where they are for the various ADVI partner structures. The
> idea is that we will be able to centralize and not have all these resources and processes floating around."

Deliverables (each = a landed byte, via Terraform):
1. **`s3://opal-data-assets`** — the bucket, in Terraform, under `.tools/safe-apply.sh`.
   **SSE RULED (PRD v1.3.3 ruling 13 @ 5f530a074, then 13a REVERSED at v1.3.4 @ f8ea5725d — final state):
   SSE-S3/AES256 DEFAULT ENCRYPTION ONLY. NO `DenyUnencryptedObjectUploads` statement — 13a's deny was
   formally reversed on 0.6.2's evidence (his schwab measurement was a HAZARD report, not a pattern
   endorsement: that deny's failure mode is a permissions-bug-shaped AccessDenied whose historical fix is
   IAM-widening, and S3 encrypts unconditionally since 2023). NO KMS — every producer role stays KMS-free.
   Producers write plain; the bucket default encrypts; NO producer ever carries an SSE header requirement
   for the monolith. Your deliberate omission in the HCL stands as written.**
2. **The prefix grammar** — `{source}/{scope}/{layer}/{type|feed}/{date}/` (PRD §2 layout, reproduced below).
3. **Router IAM** — per-source READ, assets WRITE, **explicit grants, fan-in ONE-WAY**. **The source
   read-set is EXACTLY: `opal-data-inf` (orion + eclipse bronze) and `opal-data-cot` (cottonwood bronze)**
   — the C2-ruling's three map rows; the fence below bans PutObject on ANY `opal-data-*` source, and the
   deny must be demonstrated against EACH bucket in this read-set, not just inf.
4. **(v1.3) Reserve the `{source}/{scope}/gold/` grammar** — *naming reserved, NOTHING BUILT.*
5. **(v1.3) IAM shaped so future per-source runner roles attach without restructure.**

```
s3://opal-data-assets/            grammar: {source}/{scope}/{layer}/{type|feed}/{date}/
  schwab/08242234/bronze/{type}/{YYYYMMDD}/{vendor}.zip     raw zips, as Schwab ships them
  schwab/08242234/silver/{TYPE}/date=YYYY-MM-DD/data.parquet
  schwab/08335338/bronze/... + silver/...   (staged objects remap in from opal-data-schwab -- C3;
                                             the denominator is ENUMERATED AT RUN TIME from the source,
                                             never read from a doc: the 0824 pull is still landing and
                                             any fixed count in a document is stale the moment it is
                                             written -- 0.6.2 F-1, 2026-07-14)
  smartx/{model|platform}/bronze/{feed}/{YYYYMMDD}/...json
  smartx/{model|platform}/silver/{feed}/date=YYYY-MM-DD/data.parquet
  orion/inflection/bronze|silver/...        eclipse/inflection/bronze|silver/...
  blackdiamond/cottonwood/bronze|silver/... trueshares/{DIVZ,IDVZ}/bronze|silver/...
  pathfinder/filepoint/bronze/{feed}/{YYYYMMDD}/       (ruling 15, PRD v1.3.3: BRONZE SCOPE = THE
                                             VENDOR'S DELIVERY SCOPE -- Filepoint ships ONE file
                                             carrying BOTH funds; per-fund {PFOE,PFDE} scope
                                             materializes at SILVER only)
  msn/{TICKER}/bronze/netassets/{YYYYMMDD}/{instrument_id}.{tag}.json   (fallback tier, homed by
                                             ruling 15 -- fires only when a primary issuer feed breaks)
  {source}/{scope}/gold/                    <-- RESERVED IN THE LAYOUT. BUILD NOTHING HERE.

  BRONZE law: raw byte-for-byte as the vendor shipped (zips stay zips), NEVER parquet, compact YYYYMMDD.
  SILVER law: parquet, dedup + dtype ONLY, every vendor column kept, hive date= partitions.
  GOLD:       DynamoDB opal-assets-daily-aua only — "just the dynamodb to start". The daily snapshot
              parquet dump is DEFERRED, not designed away.
```

## Fences — read before you write a line of HCL

- **APPLY IS NOT YOURS.** Author + `plan` + route the plan to **1.0.0_SA_CTO** for the apply gate. Every
  terraform apply, every IAM grant, the sentinel DENY, anything INF-adjacent gates through CTO. You may
  NOT run `safe-apply` on this without his GO. (`terraform apply` bare is a NEVER-rule regardless.)
- **`opal-data-inf` is a HELD DOMAIN.** The router reads it, and must be **PROVABLY INCAPABLE of writing
  its sources** — no `PutObject` on ANY `opal-data-*` source bucket. **The fence lives in the ROLE, not in
  intent** (the 0.5.0 precedent).
- **NOBODY writes `opal-data-inf/gold/meta/pipeline-complete.json`.** That ~40-byte key dispatches the held
  INF chain by the back door. Not from a role you author, not by hand, not as a test.
- **S3 bucket-notification config is a SINGLETON per bucket.** A TF `aws_s3_bucket_notification` on a source
  bucket **REPLACES that bucket's entire existing config.** That hazard is C2's to clear, but **do not
  author any notification resource against a source bucket in C1** — you would silently clobber INF's
  event-driven silver chain.
- **cot is a COMPLETELY separate firm pipeline from bd.** One-way fan-in only; the mirror READS cot, never
  the reverse. Never reference another firm's bucket from a pipeline tree.
- **Do not commingle masters. Do not sum 0824 and 0833.** Record at each granularity.
- `opal-data-schwab` prefixes are **0.6.2's active lane** — MCP him before touching any schwab prefix.

## <compiler_tools_mandate>
Phase 1 (before writing): `comp-iam gaps` — BASELINE. `comp-blast` on the infra you touch.
Phase 2 (before commit): `.tools/commit-gate.sh` (automatic); post-`iam.tf`, `comp-iam gaps` again.
Phase 3 (after apply, CTO-gated): **live `aws iam simulate-principal-policy` per Rule 22a** for the router
role against the **EXACT new-bucket ARNs**.

> **`comp-iam` IS NOT SUFFICIENT HERE AND IT FAILS *GREEN*.** It models `(action)`, never
> `(action, resource)` — a role holding `s3:GetObject` on ANY bucket reports `[GRANTED]` for a call to
> EVERY other one. `opal-data-assets` is a **NEW BUCKET**, so a comp-iam PASS on it is worth nothing.
> **ONE `--resource-arns` PER CALL** (2+ ARNs flips the HELD ones to `implicitDeny`). **Run the positive
> control as a SEPARATE INVOCATION** (a control batched with the target is corrupted by its own presence).
> Pass `--context-entries` for any conditioned statement (an unsatisfied condition returns a deny
> byte-identical to a real one). And comp-iam's default view is **DESIRED** (parsed Terraform) — it cannot
> tell landed from planned. Ground the applied state on live `aws iam get-role-policy`.
>
> Report **DESIRED + APPLIED + EXERCISED separately.** A config read is not a behavioral claim.
</compiler_tools_mandate>

## <cross_domain_coordination>
- `opal-data-inf` — HELD. Read-only mirror; notification-config singleton hazard; any diff = CTO pre-apply review.
- `opal-data-schwab` — 0.6.2_AE_PartnerETL's active recovery lane. MCP him before touching a schwab prefix.
- `opal-data-cot` — one-way fan-in only; separate firm from bd (gate + IAM enforced).
- `_cloudprobe/` parity window — 0.5.0_AE_OpalETL's ETF net-assets parity runs 07-14 + 07-15. **Do not
  disturb it.** C4 retargets onto YOUR bucket; his parity artifacts must remain untouched.
- Your downstream consumers, all blocked on this TO: **C2** (router, yours), **C3** (0.6.2, landing),
  **C4** (0.5.0, ETF retarget), **C6 wiring** (DS).
</cross_domain_coordination>

## <acceptance_criteria>
1. `aws s3api head-bucket` / `get-bucket-location` on `opal-data-assets` returns success against LIVE AWS —
   not a plan output, not `rc=0` from Terraform.
2. Terraform `plan` is **0-diff** after apply. Quote it.
3. The prefix grammar is realized and demonstrated: create one probe object per source tree, **landed
   under an explicit `_probe/` prefix and said so — the ONLY sanctioned mechanism** (review findings
   26/30/38: probes at canonical paths would plant synthetic non-vendor bytes in bronze trees, and
   "then remove them" instructs an S3-object deletion, a human-confirmation class per CLAUDE.md Agent
   Autonomy; `_probe/` needs neither), **verified LISTING-BASED — ListObjectsV2 key + ETag + Size (CTO
   ruling 20260714T024205Z: head-object is never the acceptance instrument).** `_probe/` objects stay;
   C12-class inventories mark them.
4. **Router IAM live-simulated per Rule 22a** — corrected per review findings 27/12/10 (the original deny
   leg was a GUARANTEED-PASS instrument: simulating PutObject against a BUCKET ARN returns implicitDeny
   for every role, because object-scoped Allows do not match a bucket ARN):
   a. POSITIVE leg: `allowed` for `s3:PutObject` on an EXACT `opal-data-assets/{source}/...` OBJECT key.
   b. DENY leg, **against EXACT OBJECT-KEY ARNs, never the bucket ARN**, one per invocation, for EACH
      source bucket in the read-set: `arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json` (a
      simulate is a pure IAM evaluation — it writes nothing; there is no safer key to prove the fence
      against), one ordinary inf key, and one `opal-data-cot` key. Expect `implicitDeny`/`explicitDeny`
      on every one. `--context-entries` for any conditioned statement.
   c. **INSTRUMENT POSITIVE CONTROL, its own separate invocation:** the SAME action on the SAME inf
      object ARN for a role KNOWN to hold PutObject on `opal-data-inf` (an INF producer role) →
      `allowed`. This single call proves the deny instrument CAN fail; without it every deny verdict is
      indistinguishable from the vacuous bucket-ARN pass.
   ONE `--resource-arns` per call throughout. **Label honestly: a simulate verifies the APPLIED layer —
   it is NOT "exercised"** (an exercise would be a real denied PutObject attempt); report
   DESIRED / APPLIED / EXERCISED separately and mark the fence APPLIED-VERIFIED unless a real attempt
   was made.
5. `{source}/{scope}/gold/` grammar reserved in the layout doc/TF comments — **and nothing built under it.**
6. Source map updated if any Lambda is touched (`infra/aws/lambda/ci/lambda-source-map.json`).
7. Deliverable 5 (IAM shaped for future per-source runner roles) evidenced as a DESIGN-REVIEW item: the
   role/policy shape documented in the module README or TF comments (what a future runner role attaches
   to, without restructure) and CTO's ack of that shape cited — no runtime check exists for a future
   property, so the evidence is the reviewed design, stated as such (review finding 35).
8. Session log with a Compiler Tools section. RAVC close **to COO** with evidence (bucket head, 0-diff plan,
   the simulate outputs including the instrument positive control, prefix listing with denominators).
</acceptance_criteria>

## RAVC
ACK to COO immediately. Report evidence to **COO** (2.0.0_SA_COO) — coordination traffic is mine.
**Apply gates and architecture forks: send them to COO, who ferries them to CTO — one path, no direct
routing needed from you** (review finding 50 killed the ambiguous double-instruction). Do not adjudicate
scope yourself; surface it.

## Sentinel disposition (so this TO's silence on it reads as ruled, not dropped)
The Door-6 sentinel DENY (PRD §6 fork 4) was PLACED into this lane by CTO (msg 20260714T012053Z),
authored + imported + planned by 0.7.0 per ruling 14iii — and then **CANCELLED-SOVEREIGN by Andrew
(~02:05Z: "I dont want more sentinels and alarms... the thing I never wanted is holding up progress on
our P0 project"), never applied, fully unwound, estate live-verified untouched.** Door-6 protection is
the institutional prohibition; the ETag baseline (`fbcddcbf4d9370310e0e5dccbbaa3efd`/135B) is a MANUAL
reference value, not a control. Nobody re-places the sentinel without Andrew's word.
