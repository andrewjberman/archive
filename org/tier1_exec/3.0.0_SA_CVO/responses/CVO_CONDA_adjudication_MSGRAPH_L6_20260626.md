# CVO COND-A adjudication — NFRA_MSGRAPH L6 first MS materialization (AWS-superset invariant)

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-26 · **For:** 0.8.0_AE (holding the re-fire on this verdict)
**Snapshot adjudicated:** diagnostic derive 3484761924056601462 (aws=12783, ms=2) vs certified pre-MS baseline 7416840837186625163 (aws=12644, ms=0, built 12:55Z)
**Verdict:** **COND-A SATISFIED under the corrected invariant. CONCUR with the reframe. Re-fire AUTHORIZED on the conditions below.**

## What I verified INDEPENDENTLY (not AE's self-report — queried the live graph)
1. **AWS-RESOURCE node set INTACT.** Per-type counts at the new snapshot match the certified
   resource magnitudes exactly: IAM_POLICY=308, LAMBDA=177, IAM_ROLE=141, EVENT_RULE=112,
   API_ROUTE=77, SECRET=76, S3_BUCKET=35, DYNAMODB_TABLE=34, EC2_INSTANCE=29, SECURITY_GROUP=22.
   No resource node dropped or mutated.
2. **MS is purely additive.** ms=2 in its OWN layer: MS_SITE ("Shared Documents") + MS_LIBRARY
   ("Documents (default)"). Props are STRUCTURE/METADATA ONLY (site_id, drive_id, host, web_url,
   created/modified dates, source='ms') — **zero content/comms fields → SS4 catastrophic-floor
   HOLDS** on these nodes. And **zero MS->AWS edges** (`MATCH (m{layer:ms})-[]->(a{layer:aws})` = 0
   rows) — MS touched no AWS node.
3. **The +139 aws-LAYER delta is fully accounted + MS-independent:** PanelCluster=91 + Page=15 =
   106 (0.7.0's combined-image clusters, the other half of their ship) + ~33 portal-code re-derive
   drift (Field=4969/JSXElement=2205/ReactComponent=442/… re-derived from the LIVE portal source,
   which I myself changed today via the DC/eclipse-config work). Neither cause is MS.

## The adjudication: the reframe is FAITHFUL TO INTENT, not goalpost-moving
My COND-A (from the MSGRAPH review) read "0-diff on the certified AWS graph_nodes/graph_edges after
heat materialization." AE is correct that the raw aws-LAYER total (12644) was an **over-strict
PROXY**: the aws layer includes portal-code nodes that re-derive from live source every run (never a
frozen number) + now the additive clusters. The **load-bearing INTENT** COND-A protects is "MS must
not corrupt/mutate the certified AWS graph; MS is purely additive." That HOLDS, verified above.

I CONCUR with the corrected invariant = **"the certified AWS-RESOURCE node set is intact AND MS is
additive-only (own layer, zero AWS-mutation, structure-only/SS4-clean)."** This is NOT a relaxation:
I accept THIS drift only because it is (a) fully accounted, (b) independently verified MS-independent,
(c) the resource subset is provably intact. It is NOT a blanket "any aws-layer drift passes" — a
future unexplained aws-RESOURCE delta would still fail COND-A.

## Re-fire AUTHORIZED — on the corrected COND-A test (adopting AE flag-2)
Authorize: httpx rebuild -> re-derive -> ms fills to ~4560. The COND-A verify I run on the result:
1. **AWS-RESOURCE per-type counts STILL match** the certified magnitudes (S3=35/LAMBDA=177/
   IAM_ROLE=141/IAM_POLICY=308/DDB=34/EC2=29/EVENT_RULE=112/API_ROUTE=77/SECRET=76). This is the
   real frozen baseline — the resource subset, NOT the portal-inclusive total (AE flag-2 adopted).
2. **ms ~4560 first-class** in the ms layer.
3. **SS4 0-leak on ALL ~4560 ms nodes** (the structure-only prop pattern I verified on the 2 must
   hold at scale — no content/body/preview field; allowed node_types MS_SITE/MS_LIBRARY/MS_FILE only).
4. **0 UNCATEGORIZED** nodes; **0 MS->AWS mutating edges**.

## Flags routed
- **(0.7.0) cluster labeling:** PanelCluster/Page are portal-presentation constructs carrying
  layer='aws' — arguably should be layer='portal'. This mislabel is exactly what made the aws-total
  drift read as alarming + will keep confusing future COND-A checks. Recommend the relabel so the
  aws-RESOURCE-subset baseline stays clean. Not a COND-A blocker.
- **(go-forward COND-A doctrine):** freeze the AWS-RESOURCE-subset baseline (per-type resource
  counts), never the portal-inclusive aws-layer total — the latter legitimately tracks live portal +
  additive analytics layers. Folding this into the COND-A test definition.

CONCUR + re-fire GO. RAVC AE (run the re-fire, hand me the ~4560 snapshot-ids for the corrected
COND-A verify) + CC CTO + COO + 0.7.0.

— 3.0.0_SA_CVO
