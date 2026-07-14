# OPAL_ASSETS.C1 — THE MONOLITH: Terraform `s3://opal-data-assets` + prefix grammar + router IAM

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO (coordination lane, Andrew-direct ~01:07Z) — authored from PRD v1.3.1 §4 row C1; architecture owner remains 1.0.0_SA_CTO</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<project>OPAL_ASSETS — Grand Consolidation P1</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §2 (target architecture) + §2b (end-state) + §4 row C1 + §4a compiler mandates + §4 cross-domain</prd>
<priority>P1 — **THE CRITICAL PATH. C2, C3-landing, C4 and C6-wiring all wait on this bucket.** Nothing else in the consolidation lands until C1 does.</priority>

<authority>
Andrew, verbatim (~01:07Z, to CTO, interactive): "You can direct these through COO, I do not want you to be
distracted with Coordination. That can be their job." Coordination lane is COO's; CTO retains architecture,
rulings, and EVERY APPLY GATE. The 00:25Z dispatch hold ("Wait to dispatch until I give the go, I want to
respawn the workers first") is SATISFIED — the worker respawn wave is complete and all four workers are live.
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
3. **Router IAM** — per-source READ, assets WRITE, **explicit grants, fan-in ONE-WAY**.
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
3. The prefix grammar is realized and demonstrated: create + head-object one probe object per source tree,
   proving the layout, then remove the probes (or land them under an explicit `_probe/` prefix and say so).
4. **Router IAM live-simulated per Rule 22a**: for the router role, `simulate-principal-policy` shows
   `allowed` for `s3:PutObject` on an EXACT `opal-data-assets/{source}/...` key, and — separately invoked —
   **`implicitDeny`/`explicitDeny` for `s3:PutObject` against `opal-data-inf`** (the one-way fan-in fence,
   exercised, not asserted). ONE `--resource-arns` per call; positive control a SEPARATE invocation.
5. `{source}/{scope}/gold/` grammar reserved in the layout doc/TF comments — **and nothing built under it.**
6. Source map updated if any Lambda is touched (`infra/aws/lambda/ci/lambda-source-map.json`).
7. Session log with a Compiler Tools section. RAVC close **to COO** with evidence (bucket head, 0-diff plan,
   the simulate outputs including the DENY control, prefix listing with denominators).
</acceptance_criteria>

## RAVC
ACK to COO immediately. Report evidence to **COO** (2.0.0_SA_COO) — coordination traffic is mine.
Route the **apply gate** and any architecture fork to **CTO** (1.0.0_SA_CTO) — those are his, and I take
them to him. Do not adjudicate scope yourself; surface it.
