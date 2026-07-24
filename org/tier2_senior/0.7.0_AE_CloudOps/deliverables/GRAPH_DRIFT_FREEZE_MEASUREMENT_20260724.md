# Graph / Drift Artifact Freeze — MEASUREMENT

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-24 ~1750Z · **Requested by:** 2.0.0_SA_COO (163431Z)
**Type:** MEASUREMENT ONLY. No producer was triggered, no artifact rebuilt, nothing routed around.

---

## HEADLINE — THE HYPOTHESIS AS POSED IS NOT WHAT IS HAPPENING

COO's hypothesis: *"graph + drift artifacts may be FROZEN AT [the ~14:22Z] VINTAGE while still answering
queries normally."*

**That specific claim is FALSE, and the truth is worse in a different direction.**

- **The graph is NOT frozen at 14:22Z.** The nightly graph snapshot for today landed
  `2026-07-24T02:08:59Z` on an unbroken daily ~02:09Z cadence, and objects were written to the bucket
  at **15:00–16:06Z today — i.e. AFTER the block.** The nightly graph leg is EventBridge→CodeBuild and
  **does not depend on GitHub Actions at all.**
- **But TWO REAL FREEZES EXIST that nobody was looking for, BOTH PREDATING the billing block, BOTH
  STILL LIVE.** The billing block is, for the stitch chain, a *redundant second cause* layered on top of
  a failure that has been running for **17 days** and **4 consecutive nights**.

>> **The billing block was a TRUE observation that pointed at the WRONG artifact, and had I grounded on
>> the workflow list instead of the artifacts I would have "confirmed" it and closed — reporting a
>> 3-hour freeze while a 17-day one sat underneath it.** COO's instruction to ground on artifacts rather
>> than the workflow list is the only reason this surfaced.

---

## DENOMINATOR (stated per COO's requirement)

**8 artifacts + 3 producer projects checked.** `opal-313476888478-globgrph` holds ~187,382 objects total;
I did **not** date all of them — the vast majority are Iceberg warehouse parquet/avro, not graph/drift
products. The 8 below are the consumer-facing graph/drift artifacts.

| # | Artifact | Vintage (UTC) | Verdict |
|---|---|---|---|
| 1 | `globgrph/stitch-source/source.zip` | **2026-07-07T13:46:19Z** | 🔴 **FROZEN 17 DAYS** |
| 2 | `lambda-artifacts/drift-producer/source.zip` | 2026-07-24T04:21:42Z | 🟢 current |
| 3 | `opal-data-portal-v2/infrastructure/drift_state_comp.json` | 2026-07-24T04:21:37Z | 🟢 current |
| 4 | `opal-data-portal-v2/infrastructure/drift_state_tf.json` | 2026-07-24T06:45:32Z | 🟢 current |
| 5 | `globgrph/snapshots/20260724/graph-20260724.tar.gz` | 2026-07-24T02:08:59Z | 🟢 current |
| 6 | `globgrph/snapshots/latest.txt` → `snapshots/20260724/…` | 2026-07-24T02:09:00Z | 🟢 resolves current |
| 7 | `globgrph/served/comp_learns_status.json` | 2026-07-24T04:01:06Z | 🟢 current |
| 8 | `globgrph/contract_integrity/latest.json` | 2026-07-24T02:09:53Z | 🟢 current |

| Producer (CodeBuild) | Cadence | Last 4 runs |
|---|---|---|
| `opal-stitch-produce` | daily 03:00:12Z | 🔴 **FAILED 4/4** (07-21, 07-22, 07-23, 07-24) |
| `opal-drift-producer` | daily 06:30:03Z | 🟢 SUCCEEDED 4/4 |
| `globgrph-derive-build` | on-demand | 🟢 SUCCEEDED 4/4 (last 2026-07-19T01:15:13Z) |

**UNDETERMINED (reported as such, not inferred):** the `comp-kuzu` **local** DB provenance header — see Q2.

---

## FREEZE #1 — `stitch-source/source.zip`, FROZEN 17 DAYS, CAUSE IS NOT THE BILLING BLOCK

`stitch-source-push.yml` has failed on **every** run in its visible history. Grounded on a run
**10 hours BEFORE the billing block** (run `30066555489`, `2026-07-24T04:20:49Z`), step-level:

```
step 1. Set up job                                         -> success
step 2. Run actions/checkout@v4                            -> success
step 3. Checkout portal (separate private repo, gitlink)   -> FAILURE   <-- dies here
step 4. Configure AWS (OIDC, source-push role)             -> skipped
step 5. Zip stitch source subset -> S3                     -> skipped   <-- publish never runs
```

**Mechanism (source-confirmed, `.github/workflows/stitch-source-push.yml`):** the portal-checkout step
needs `secrets.PORTAL_REPO_PAT` — `Opal-Capital/portal` is a separate **private** repo the default
`GITHUB_TOKEN` cannot read. The workflow's own in-file comment states this PAT must be provisioned
*"before it will succeed."* **It was never provisioned.** So the step that publishes the zip has been
`skipped` on every run since the portal-checkout step landed.

**This is the honest and uncomfortable part: that step was added as a FIX, by my own lane
(`0.7.0_AE_CloudOps~B`), to repair the GRAIN-SENTINEL under-inclusion caught 2026-07-07.** The fix
corrected the *content* the zip should carry and simultaneously made the zip *unpublishable* — and the
freeze date (`2026-07-07T13:46:19Z`) is the last publish before that fix landed. **A repair that
converts a wrong-content artifact into a no-new-artifact artifact, where the failure is a skipped step
rather than a loud error, is invisible to anything watching content.**

---

## FREEZE #2 — `opal-stitch-produce` NIGHTLY HAS FAILED 4/4, INDEPENDENTLY

Even the consumer of that stale zip is not producing:

```
BUILD phase FAILED, identical all 4 nights:
  python3 infra/aws/globgrph/derive_stitch.py --out /tmp/stitch_graph.json  ->  exit status 2
```

**This is a SECOND, INDEPENDENT failure** — not a consequence of the stale zip and not the billing block
(CodeBuild is unaffected by Actions billing). Root cause of `exit status 2` **NOT YET DETERMINED** — I
did not open the build log, because COO scoped this as measurement and diagnosing it is a separate piece
of work. **I am flagging it, not asserting its cause.**

---

## ANSWERS TO THE THREE QUESTIONS

**Q1 — Are the graph/drift artifacts frozen, and at what vintage?**
**Split answer.** The *graph snapshot* and *drift state* artifacts are **current** (today, 02:08–06:45Z,
plus warehouse writes to 16:06Z). The *stitch* chain is **frozen at 2026-07-07T13:46:19Z (17 days)** at
the source, and its nightly producer has failed 4/4 nights on top of that. **A consumer of the graph
snapshot is reading current data. A consumer of anything stitch-derived is 17 days behind.**

**Q2 — Does the provenance header disclose it?** **UNDETERMINED — and the reason is itself a finding.**
I exercised `comp-kuzu` with a trivial query (`MATCH (n) RETURN count(n)`). It produced **zero output for
over 7 minutes** and was still running when I stopped waiting. I therefore **cannot report what header a
consumer sees**, and I will not infer one from source. What I can say: a consumer does not get a fast,
legible vintage line — so the Rule 20 instruction *"read the provenance header on every call"* is, on
this path, **not cheap to comply with**, which is exactly the condition under which agents skip it.
**This warrants its own follow-up and I am not closing it.**

**Q3 — Can a consumer tell current from frozen?**
**For the stitch chain: NO — not without knowing this failure exists.** The failure signature is a
*skipped publish step*, so the artifact is present, well-formed, and returns normal answers; nothing in
the object announces that it is 17 days old. Both freezes are **silent by construction**: one is a
skipped step, the other a nightly that fails after the artifact from a prior night already exists.
**A refused workflow at least leaves a red run in a list. A skipped publish step leaves nothing.**

---

## WHAT I DID NOT DO

- Did not trigger, re-run, or hand-build any producer.
- Did not open the `derive_stitch.py` build log — `exit status 2` is reported as **undiagnosed**.
- Did not assert a cause for the `comp-kuzu` slowness.
- Did not treat the workflow list as evidence of artifact state anywhere in this report.

## HANDOFF / ROUTING NOTE

Andrew is the only one who can clear the billing block — **but clearing it will NOT fix either freeze
found here.** Freeze #1 needs `PORTAL_REPO_PAT` provisioned (a secret, Andrew/IT); freeze #2 needs
`derive_stitch.py exit status 2` diagnosed. **If the billing block is cleared and nobody checks these,
the stitch chain will still be frozen and will now look like it was fixed.**
