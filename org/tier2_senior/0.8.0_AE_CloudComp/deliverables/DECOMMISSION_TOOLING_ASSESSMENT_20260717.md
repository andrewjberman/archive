# Decommission-Identification Tooling — Research Assessment

**Author:** 0.8.0_AE_CloudComp · **Date:** 2026-07-17 · **Trigger:** Andrew-direct (verbatim @dc4207c7c / 1d81e760b / 3d326af47)
**For:** Andrew (sovereign ask) · CTO (registration + arch gate) · 0.8.0~C (consumes read-only for P3-CENSUS)
**Status:** RESEARCH / ASSESSMENT. No tool built, no resource touched. Every recommendation is CTO-gated; any actual decommission stays behind the destructive-op confirmation + NEVER-rules + LCLRPO's Andrew-gated delete word.

---

## 0. TL;DR — the finding that reframes the ask

**The decommission-identification pipeline is ~70% already built.** Andrew's instinct that heat analytics + comp-dups are the instruments is not just correct — the estate has been converging on exactly this since 2026-07-14, when Andrew directed comp-debris ("checking cloudtrail and organizing resources by oldest last invocation"). That tool's own docstring designs the whole pipeline: a **coldest-first invocation ledger** plus a **confirmation pass** run on the cold tail (comp-heat-federated + comp-dups + comp-deadgrant + comp-trigger).

So the work is **COMPOSE + EXTEND**, not build-from-scratch:

| Layer | Exists? | The gap |
|---|---|---|
| Cold-resource ledger (`comp-debris`) | ✅ v1 | **Lambda-only.** The monolith cutover is S3 + DynamoDB + EC2 (the inf/cot/bd gold runners) + EventBridge — none covered. And it reads CloudWatch Lambda-Invocations, not CloudTrail (which Andrew named as the general signal). |
| Structural dead-twin (`comp-dups`) | ✅ v2 | Name + file-body corpus. Not resource-summary. Not fused with heat. |
| Asset×code heat federation (`comp-heat federated`) | ✅ | Data/code heat, not resource-invocation heat; not joined to the cold ledger. |
| Access-side coldness (`comp-deadgrant`, `comp-iam`) | ◑ partial | comp-deadgrant hunts dead *secret* grants for live-degrade, not decommission. comp-iam grabs almost none of the IAM signal that says "nobody uses this" (Part A). |
| Trigger wiring (`comp-trigger`) | ✅ | EventBridge/Scheduler forensics — good; needs to be a column in the fused view. |
| **Joint fast-scan (Andrew's heuristic)** | ❌ | The superseded-twin detector (§4). Needs `comp-similarity` (new) + a heat-divergence join. |
| Disposal pipeline (`OPAL_LCLRPO` + taxonomy census) | ✅ | The rulings/gates path exists; my research feeds its input column, per CTO. |

**One genuinely new tool is warranted: `comp-similarity`.** Everything else is composition and extending `comp-debris` past Lambda.

---

## Part A — comp-iam: what it grabs, and the IAM information we don't

### A.1 What comp-iam does today
Modes: `gaps` (action-only), `roles`, `services`, `service <fn>` (resource-aware), `role <name>`, `stats`, `resource-sweep`, `attach-census`, `simulate` (live), `reconcile` (DESIRED-vs-LIVE). It parses **Terraform identity policies** (role → what actions it can take) and, in `reconcile`, overlays a live IAM census. Its own banners already state its three known limits honestly: models `(action)` not always `(action, resource)`; **DESIRED (Terraform), not APPLIED**; a Deny it never parsed reads as silence.

### A.2 The IAM information we simply don't grab — ranked by decommission-relevance
This is the direct answer to Andrew's "a lot of IAM information which we simply dont grab." comp-iam is **identity-policy-only, Terraform-only, role-only**. It is blind to:

1. **IAM last-used data** *(highest decommission value)* — `get_role` returns `RoleLastUsed` (timestamp + region); IAM Access Advisor (`GenerateServiceLastAccessedDetails`) gives per-service last-access. **A role unused for 90+ days is the single cleanest "nobody uses this" signal, and we capture none of it.** This is the access-side twin of comp-debris's invocation coldness — same idea, IAM plane.
2. **IAM Access Analyzer unused-access findings** — AWS's own native "this role/permission/access-key is unused" analyzer. Purpose-built for exactly this cleanup; we don't read it.
3. **Resource-based policies** — bucket policies, KMS key policies, SQS/SNS/Lambda resource policies. comp-iam reads only the *identity* side (role → resource). To answer "does **anything** still have access to this bucket?" for a decommission you need the resource side too: the bucket policy + every identity policy referencing it. This is the same structural blindness class as `(action)`-not-`(action,resource)`, one plane over.
4. **Trust policies / assume-role graph** — who/what can assume each role, cross-account trust. comp-iam has zero trust-policy parsing (only ARN-matching comments mention "assume"). A role nothing can assume is dead; a role trusting a decommissioned service is dead. Invisible today.
5. **Managed-policy attachments resolved into the grant set** — `attach-census` flags standalone `aws_iam_policy` as "a different world"; they aren't folded into role grants, so a role's real permissions are under-counted.
6. **Permission boundaries, instance profiles, users/groups/access keys, SCPs** — comp-iam is role-scoped; the rest of the IAM surface (EC2 instance profiles for the gold runners, human/service users, org SCP deny layer) is out of frame.

### A.3 The expansion, framed for the gate
comp-iam's charter is **correctness-before-deploy** (does this role have the perms this call needs). The decommission asks are a **different question** on the same substrate: *is this grant/role/resource still used, and who else reaches this resource*. Two clean options for CTO:
- **(a) Extend comp-iam** with a `last-used` mode (RoleLastUsed + Access Advisor) and a `resource-policy` / `who-can-reach <arn>` mode. Risk: overloads a deploy-time tool with a lifecycle question.
- **(b) A sibling `comp-iam-usage`** (or fold last-used into `comp-deadgrant`'s access-side). Keeps the deploy-time tool focused.
Either way the **new data** is the same: last-used + resource-policies + trust + Access Analyzer. My lean is (b) for separation of concerns, but this is CTO's call. **Whichever ships must fix-or-explicitly-carry comp-iam's three named limits — never silently inherit them** (CTO, this session).

---

## Part B — the Trino heat-analytics estate across platforms

### B.1 Inventory (grounded on the live globgrph warehouse, 2026-07-17)
Iceberg tables: `graph_nodes` (20,429), `graph_edges` (35,731), `graph_contracts`, `cse`, `code_heat_snap`, `ms_heat_snap`, `fedobs_coevolution_snap`, `fedobs_coverage_snap`. Non-Iceberg heat stores: `code_heat/`, `ms_heat/`, `axes_history/`, `tool_activity/`, `fedobs_signals/`, `fedobs_obs_findings/`.

The heat "platforms" and what each actually measures:

| Analytic | Platform / signal | Grain | Decommission use |
|---|---|---|---|
| `code_heat` | **git** commit recency (decay-weighted) | repo file | which *code* is hot/cold |
| `ms_heat` | **SharePoint/OneDrive** file activity | MS document | which *documents* are hot/cold |
| `comp-heat federated` | **estate assets × git** (LIVE Trino join) | S3 asset × its code | which *served data* is stale vs its producer code |
| `comp-debris` | **CloudWatch** Lambda Invocations | Lambda fn | which *Lambdas* are dormant ← the only AWS-resource heat |
| `comp-debt` / `comp-pulse` / `comp-depth` / `comp-debris` (comp-axes) | mixed estate axes | mixed | the 8-axis directory + delta store (my TO-3) |

### B.2 The platform coverage gap — the load-bearing finding for decommission
Heat exists for **code** (git) and **documents** (MS) and **Lambda invocation** (comp-debris). It does **not** exist for the rest of the **AWS-resource** plane: **S3 prefixes/buckets, DynamoDB tables, EC2 instances, EventBridge rules**. Yet the monolith cutover is precisely an S3 + DDB + EC2 migration. The decay-weighted hot/warm/cold band pattern — proven on code_heat and ms_heat, with the append-only `*_snap` delta siblings I built for TO-7 — should be **extended to a "resource heat" analytic** whose input is AWS activity: **CloudTrail** (Andrew's named source) for data-events + management-events, plus per-service metrics (S3 request metrics / DDB ConsumedCapacity / EC2 CPU + NetworkIn). That is the missing platform, and it's the same shape we already run twice.

**The pattern to reuse, not reinvent:** the snap-sibling delta architecture (`snap_store.py`, one writer, `{surface}_snap` + freshness twin) already generalizes any dated analytic into a queryable day-over-day Trino series. A `resource_heat_snap` slots straight in — and its delta is exactly what surfaces "this bucket went cold the week its successor went hot."

---

## Part C — the decommission-identification pipeline (compose the triad)

comp-debris already designed this. Formalized:

```
  STAGE 1  LEDGER (broad, cheap)          STAGE 2  CONFIRM (on the cold tail only)
  comp-debris coldest-first        --->   comp-dups          structural dead-twin
   Lambda today; EXTEND to                comp-heat federated stale-served vs hot-code
   S3/DDB/EC2/EventBridge                 comp-deadgrant     access-side dead reach
   via CloudTrail                         comp-trigger       is anything wired to fire it?
                                          comp-iam last-used who still holds/uses the grant (Part A)
                                                 |
                                                 v
  STAGE 3  DISPOSITION           OPAL_LCLRPO census-cleared batches + taxonomy census
   (deviation-from-standard  +  unused-by-heat  = two columns of one resource table — CTO)
   migrate / retire / carve-out  @ CTO gate; DELETE word = Andrew (LCLRPO)
```

Three binding properties, all already honored by the existing tools and all mandatory for any extension:
- **NEVER-INVOKED ≠ COLD** (comp-debris refinement 1): a zero-history resource is TOO-YOUNG or STILLBORN-OR-GUARD, never ranked cold — a monthly/on-incident guard is not debris.
- **UNKNOWN is a band** (refinement 2): a blind read is not a dead resource (the anti-correlation trap).
- **ADVISORY, hold-aware, never deletes** (refinement 3): INF-chain / frozen / sovereign names are excluded from any reap output.

**Do not build a second disposal path** (CTO): the census→ruling→gate pattern in OPAL_LCLRPO + the taxonomy standard IS the disposal pipeline; this research feeds its "unused" input column.

---

## Part D — comp-similarity (the one new tool) + the joint-signal fast-scan

### D.1 The joint-signal heuristic (Andrew's algorithm, formalized) — the centerpiece
A decommission candidate is the **intersection** of two signals over a similar-name cluster:

```
  candidate  =  argmax( heat_divergence )   within a similar-NAME cluster
                        AND
                summary_similarity(a, b) >= HIGH   (comp-similarity)

  where heat_divergence(a,b) = |heat(a) - heat(b)|  with one HOT and one COLD
```

The reading: **name-similar + summary-similar + heat-divergent = a superseded resource whose hot twin is its live replacement.** This is the exact monolith-cutover shape (old `opal-data-inf` gold path COLD next to its hot `opal-data-assets` successor; names + summaries near-identical). The signals are individually weak, jointly sharp:
- **name-similarity alone** false-positives — cross-firm same-name (`bd`/`cot`/`inf`) is *expected architecture*, and comp-dups already suppresses it (auditably).
- **coldness alone** can't tell superseded from a rare-event guard.
- **summary-similarity** confirms the two resources do the same *thing*.
- **heat DIVERGENCE (not coldness)** is the supersession tell — the whole point is one is hot *because* it replaced the other.

This is a fast pre-filter: score the cheap name-clusters first, compute heat-divergence only within clusters, and run the (slightly costlier) summary-similarity only on the divergent pairs. It scans the estate for supersession in one pass.

### D.2 comp-similarity design — engine, and the real prerequisite
- **Engine:** reuse the `dup_scan.py` BM25 class (Andrew's stated intent; confirmed self-contained, takes `[doc_strings]`). The engine is copy-reusable — the entire novel work is the **corpus**. The comp-state 12s-fix proved the BM25 layer is cheap; cost was serial subprocess I/O, so a corpus assembled in one graph read stays fast.
- **Corpus (the crux Andrew flagged — "a stable summary location"):** CTO's steer is the node summary, not AWS Description fields, because Description exists on Lambda/IAM/EventBridge/SG but **not S3/DDB** — and S3+DDB *is* most of the consolidation surface, so a Description corpus is structurally blind to the majority of the estate (the same failure class as comp-iam's `(action)`-not-`(action,resource)`). **Grounding correction (this session):** the comp-graph `graph_nodes` schema is `node_id, arn, node_type, name, layer, drift_class, source, snapshot_ts, props` — **there is no canonical `summary` string field today**, and `props` is empty for the S3 bucket node I checked. So "use the node summary" has a real prerequisite: **the stable summary location must be *established*, not merely read.** Two ways:
  - **(i) Derive-at-scan** — synthesize each resource's summary document from what the graph already holds: `node_type + name + layer + arn + its edges (producers → served → consumers) + drift/reachability flags`. This is exactly what **pipescript already projects per thread** — pipescript's projection logic is the strongest existing "resource summary" generator, uniform across resource types. comp-similarity's corpus = the pipescript-style per-node projection.
  - **(ii) Enrich the node writer** to emit a canonical `summary` field once (CTO's "make the summary better, one place"). Cleaner long-term; a bigger change to the derive path (0.7.0-coordinated).
  My lean: **(i) derive-at-scan from the graph neighborhood** for v1 (no producer change, uniform coverage, stable because the graph is the estate's canonical store), with (ii) as the enrichment follow-on if v1's summaries prove too thin for some node classes — never fall back to Description for those classes (that re-introduces the S3/DDB hole).

### D.3 Registration
comp-similarity is a new `.tools/comp-*` → CTO registration gate + the `comp-manifest-check` registration invariant (manifest + tools_index + coverage-map + comp-which curated rule + routing-test). Same closure discipline as every comp tool.

---

## Recommendations & sequencing (P3, CTO-gated)

1. **Extend comp-debris past Lambda** (S3/DDB/EC2/EventBridge via CloudTrail) — the highest-leverage single move; it turns the ledger from "cold Lambdas" into "cold cloud", covering the actual monolith surface. Keeps the three binding refinements.
2. **Add the access-side column** — last-used + resource-policy + Access Analyzer (Part A), as `comp-iam-usage` or a comp-deadgrant extension. Feeds the "who still reaches this" confirmation.
3. **Fuse the cold ledger + confirmation pass into one resource table** — the two-column view CTO named (deviation-from-standard from the census ⊕ unused-by-heat from this pipeline), so ~C's P3-CENSUS and this research land as one artifact.
4. **Build comp-similarity** around the joint-signal heuristic (§D), corpus = graph-derived node summary (derive-at-scan v1). Slots behind #1–3 unless it directly feeds the decommission column — which, via the superseded-twin scan, it does.
5. **Resource-heat as a `*_snap` delta sibling** (reuse `snap_store.py`) so "went cold when its twin went hot" is a first-class day-over-day Trino query.

**Disposal is not in scope here** — it routes through OPAL_LCLRPO's existing census-cleared, CTO-gated, Andrew-delete-word pipeline. This research produces the *identification* column only.

## Part E — costing the one-off summary-authoring pass (Andrew Q, 2026-07-17)

**Q: if we one-off pay subagents to write a stable summary field per resource, how many nodes, and where stored?**

### E.1 How many nodes — grounded on the live graph (20,429 nodes total)
You do NOT summarize 20k nodes. Tiered by what actually needs an authored cloud-resource summary:

| Scope | Count | What it is |
|---|---|---|
| Total graph | 20,429 | Incl. ~18,500 code-structure (Field/JSXElement/TypeDecl/Prop/Module/PipelineFunction) + document (MS_FILE/FOLDER) nodes — **out of scope** (already covered by code-heat / ms-heat / comp-dups). |
| **All ARN-bearing cloud resources** | **1,894** | Every AWS resource in the estate. |
| — dependent/attachment nodes | ~1,053 | LOG_GROUP 233, IAM_POLICY 450, CW_ALARM 115, EVENT_SOURCE 97, API_ROUTE 82, INSTANCE_PROFILE 19, SERVICE_PRINCIPAL 17, SECURITY_GROUP 24, S3_BUCKET_POLICY 10, VPC_ENDPOINT/ROUTE53 6 — **summary is mechanically derivable from the parent** ("log group for lambda X"); no LLM needed. |
| **Independent resources (natural one-off scope)** | **~841** | 1,894 − 1,053. Each carries a distinct purpose worth an authored summary. |
| — of which prime decommission targets | ~549 | LAMBDA 196, EVENT_RULE 147, S3_BUCKET 38, DYNAMODB_TABLE 36, EC2_INSTANCE 33, SSM_DOCUMENT 24, SCHEDULE 16, SNS_TOPIC 15, LAMBDA_LAYER 13, SQS_QUEUE 12, ECS_TASK_DEF 6, API_GW 5, CODEBUILD 4, ECS_CLUSTER/CLOUDFRONT/STATE_MACHINE/LOAD_BALANCER 4. |
| — + security resources | +91 | SECRET 81, KMS_KEY 10. |
| — + IAM identities | +201 | IAM_ROLE 197, IAM_USER 4. |

**Practical one-off cost: ~550 (prime targets) to ~841 (all independent resources)** bounded per-node tasks — each: read the node's graph neighborhood + TF definition + last-modified, write 2-3 sentences. Haiku-class, small context, a tractable single fan-out. The ~1,050 dependents get derive-at-scan summaries for free; and derive-at-scan can pre-populate ALL ~841 mechanically so subagents only ENRICH the ambiguous/high-value ones — driving the true LLM count well below 841.

### E.2 Where stored — Iceberg/Nessie → Kuzu projection, with ONE critical refinement
Andrew's framing is right (Iceberg/Nessie, projected to Kuzu in full fidelity for current-state) with one structural correction:

**NOT a column on `graph_nodes`.** graph_nodes is MACHINE-DERIVED and regenerated every derive / incremental_updater run — an editorial summary written as a graph_nodes column would be **clobbered on the next derive**. Editorial content and derived content must live in separate tables.

**The design:** a SEPARATE append-only Iceberg table in the globgrph Nessie catalog — `resource_summaries` (or `node_cards`):
- **Keyed on ARN** — confirmed the natural key: for cloud resources `node_id == arn` (e.g. `arn:aws:s3:::opal-data-inf`). Stable across derive regenerations; node_id for code nodes is synthetic, ARN for resources is durable.
- Schema: `arn`, `node_type`, `summary` (the authored text), `authored_by`, `authored_at`, `source_inputs` (what it was derived from — audit/regeneration), `summary_version`.
- **Append-only + snapshot-versioned** (same discipline as graph_nodes / cse / the `*_snap` siblings): a re-summarization appends a new row; current-state = latest-per-ARN.
- **Projection to Kuzu:** the comp-kuzu refresh (which already projects graph_nodes → Kuzu in full fidelity) **LEFT JOINs `resource_summaries` (latest-per-ARN) onto graph_nodes on node_id/ARN** — so every current-state node carries its `summary` property. Because it is a join-overlay, **a re-derive of graph_nodes NEVER clobbers the editorial layer** — the one-off investment is durable by construction, which is the whole point of "paying the cost once."
- **New resources after the pass** left-outer-null until an incremental summarization fills them (or the derive-at-scan fallback) — so the one-off pass is never re-done wholesale; only the trickle of new arrivals needs topping up.

This is the concrete form of the assessment's "establish the stable summary location": an ARN-keyed overlay table, authored once, projected as a node property, surviving every derive. comp-similarity then reads the `summary` property off the current-state Kuzu nodes exactly as it would any other node field.

## Open questions / caveats for the gate
- Which resource classes matter most first for comp-debris extension — S3 (the monolith) vs EC2 (the runners)? (Andrew/CTO priority call.)
- comp-similarity corpus: derive-at-scan (i) vs node-writer enrichment (ii) — I lean (i); CTO's arch call.
- CloudTrail coverage: management-events are ~90d in the console but the org trail (`opal-cloudtrail-logs`) has the full history in S3 — the extension should read the trail bucket, not the console API, for anything older than 90d. (Grounded: `opal-cloudtrail-logs-313476888478` is a live node.)
- comp-iam expansion vs sibling tool: separation-of-concerns call for CTO.
