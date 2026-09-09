# CG-s-31 -- THE VOCABULARY IS UNIFIED AT THE PRODUCER, AND THE PRODUCER CANNOT PUBLISH IT

**TO:** `NFRA_CLDGRPH.TO-CG-F-11` · **cell:** CG-s-31 · **worker:** `0.9.0_WK_NFRA_CLDGRPH~2`,
branch `wk-cldgrph-6-2` · **status: OPEN** -- F11-AC1, AC4 and AC5 PASS; F11-AC2 and F11-AC3 are
BLOCKING on `NFRA_CLDGRPH-W2-S60`. **Push state: LOCAL.**

```json
{
  "cell": "CG-s-31",
  "to_id": "NFRA_CLDGRPH.TO-CG-F-11",
  "outcome": "OPEN -- the unification is built, measured end to end locally and committed; the PUBLISH is blocked by a certified grain baseline written in the retired vocabulary",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~2",
  "branch": "wk-cldgrph-6-2",
  "push_state": "LOCAL",

  "the_four_identity_censuses": {
    "measured_on": "the PUBLISHED artifact s3://opal-313476888478-globgrph/stitch/stitch_graph.json, producer=stitch-codebuild, built_at 2026-09-09T19:55:00Z, sha256 918d825f... verified against its own marker",
    "measured_when": "BEFORE the producer edit existed",
    "GOLD_SCRIPT": {"resolved": 1330, "of": 1380, "script": 166, "function": 1214,
                    "script_resolved": 132, "function_resolved": 1198, "carried": 50,
                    "reasons": {"no-canonical-pipeline-node": 50}},
    "S3_DATA_KEY": {"resolved": 145, "of": 294, "carried": 149,
                    "reasons": {"ambiguous-across-firms": 24, "no-canonical-s3-key": 125}},
    "PORTAL_COMPONENT": {"resolved": 20, "of": 22, "carried": 2,
                         "reasons": {"no-canonical-component": 2}},
    "REACT_QUERY_KEY": {"resolved": 26, "of": 94, "carried": 68,
                        "reasons": {"no-canonical-query-key": 68}},
    "carried_with_origin_stitch": 269,
    "lost": "0 of 1790",
    "cvo_agreement": "three of the four reproduce C-S40's INDEPENDENT census exactly -- S3_DATA_KEY 169 in S3Key (of which 24 ambiguous, so 145 merge), PORTAL_COMPONENT 20 of 22, REACT_QUERY_KEY 26 of 94",
    "PORTAL_BUNDLE": "EXCLUDED by the cell -- the one genuinely new class, kept"
  },

  "the_reconciliation": {
    "run": "python infra/aws/globgrph/derive_stitch.py on a HEAD-built source tree (zip 298ada9a4f, repo_head 139cbe1d40, portal/src 435 files)",
    "per_type": {"PipelineScript": {"admitted": 332, "merged": 264, "carried": 68},
                 "PipelineFunction": {"admitted": 2428, "merged": 2396, "carried": 32},
                 "S3Key": {"admitted": 588, "merged": 290, "carried": 298},
                 "Component": {"admitted": 24, "merged": 20, "carried": 4},
                 "ReactQueryKey": {"admitted": 188, "merged": 52, "carried": 136}},
    "total": "admitted=3560 merged=3022 created=538 lost=0 edges_rewritten=3273",
    "why_double_the_census": "the prior cycle -- 1,770 nodes re-typed from the snapshot the derive archives (W2-S61); each object is admitted twice in this pass, once freshly emitted and once arriving from the snapshot, and both resolve to one identity",
    "retyped_prior_cycle": {"GOLD_SCRIPT": 1380, "S3_DATA_KEY": 294, "REACT_QUERY_KEY": 94,
                            "PORTAL_COMPONENT": 2}
  },

  "the_edge_resolution": {
    "derives_from": "216",
    "stored_in": "955",
    "genuine_dangling": 0,
    "before_the_STORED_IN_fix": "0 -- the builder read a class literal the producer no longer emits; caught by the local run, before anything was pushed",
    "unioned": "nodes 28077, edges 61281"
  },

  "the_map": {
    "keys_before": 65,
    "keys_after": 61,
    "by_layer_before": {"aws": 34, "portal": 18, "pipeline": 4, "ms": 7, "semctl": 2},
    "by_layer_after": {"aws": 33, "portal": 16, "pipeline": 3, "ms": 7, "semctl": 2},
    "entries_retired": ["GOLD_SCRIPT", "S3_DATA_KEY", "PORTAL_COMPONENT", "REACT_QUERY_KEY"],
    "entry_kept": "PORTAL_BUNDLE",
    "frozen_COND_A_resource_type_count": "32, UNMOVED -- S3_DATA_KEY merged INTO S3Key, already an aws type; no aws type was created or destroyed",
    "stamp": "STITCH_V1_TYPES / STITCH_V1_STAMP gone; the fold writes no vocabulary property; the stamped counter stays and stays at 0",
    "cvo_resign": "PENDING -- 3.0.0_SA_CVO's at L9; this record carries the counts it needs"
  },

  "the_build_derive_pointer_ids": {
    "zip_built": "sha256 298ada9a4f75c98fc875180d2aeba84d104a9e5c094c95da12bf172dca7de578, 8226 entries, portal/src 435, stitch_source_sha.txt 139cbe1d40",
    "zip_pushed": false,
    "stitch_build_id": null,
    "derive_task": null,
    "derive_image": "unchanged, sha256:478d0a43... (F-4's); no image act taken",
    "pointer_before": "projection/2026-09-09T21:05:17.968166+00:00/",
    "pointer_after": "projection/2026-09-09T21:05:17.968166+00:00/ -- UNCHANGED; this order published nothing",
    "reason": "NFRA_CLDGRPH-W2-S60 -- the unified artifact cannot pass the producer's own grain sentinel"
  },

  "the_distinct_node_type_list": {
    "served_now": "the PRE-unification vocabulary -- GOLD_SCRIPT 1380, S3_DATA_KEY 294, PORTAL_COMPONENT 2, REACT_QUERY_KEY 94, PORTAL_BUNDLE 1, and 1771 nodes carrying vocabulary=stitch-v1 in props",
    "in_the_LOCAL_unified_graph": "0 of the four provisional names; PORTAL_BUNDLE 1; PipelineScript / PipelineFunction / S3Key / Component / ReactQueryKey carry the merged and carried members",
    "note": "F11-AC2's read is against the SERVED graph and is what the block holds"
  },

  "comp_debt_second_leg": {
    "types": "PipelineScript(tier=gold),S3Key",
    "rc": 0,
    "stitch_leg_isolated": "0 of 365",
    "nessie_leg_isolated": 308,
    "note": "the SCOPE moved; the GRAPH it reads is still the pre-unification one"
  },

  "surprise_rows_filed": ["NFRA_CLDGRPH-W2-S60", "NFRA_CLDGRPH-W2-S61",
                          "NFRA_CLDGRPH-W2-S62", "NFRA_CLDGRPH-W2-S63"],
  "commits": ["139cbe1d40 the producer, the map, comp-debt, the census and the fixture",
              "<the acts commit>", "<the instance commit>"]
}
```

---

## The unification works. It is the publishing that is blocked.

Run the unified producer against the real snapshot and the real portal source and it does exactly
what S31 asks: **0 of the four provisional names survive**, 3,022 members merge onto their
canonical identities, 538 are carried with `origin=stitch` and a stated reason, **0 are lost**,
955 of 955 `STORED_IN` and 216 of 216 `DERIVES_FROM` resolve, and there are **0 genuine dangling
edges**. Then the producer's own grain sentinel refuses to emit the graph, and it is right to.

`grain_baseline.json` is a **CVO-certified** file, and it still names all four retired types with
counts from the vocabulary they belonged to — `GOLD_SCRIPT 1260`, `S3_DATA_KEY 272`,
`PORTAL_COMPONENT 27`, `REACT_QUERY_KEY 85`. AC-GRAIN.2 compares each baseline key against the
stream; four classes that correctly become **0** read `0.00x`, four violation groups,
`derive_stitch.main()` returns 2. Pushing this source zip would make `opal-stitch-produce` fail in
precisely the way it failed 67 times before CG-s-23 repaired it, so **the zip was not pushed, no
build was started, no image was rebuilt and no derive was run.**

The remedy is the file's own and it is precedented: recertify the four to **0**, which makes the
sentinel skip them permanently (`check_magnitude: base<=0 -> skip`) — exactly what the 2026-07-25
`EXTERNAL_ENDPOINT` entry did for a class an Andrew-direct taxonomy change had dropped, with a
`verified_reason` and a signer. `grain_baseline.json` is not in this order's `<paths>`, and every
recertification in it names its CTO gate and CVO sign. Row `W2-S60`.

**It is the mirror of `W2-S45`, one layer out.** That row was five types a frozen map had never
seen and the ruling ADMITTED them. This one is four types a certified baseline still expects and
the ruling must RETIRE them. Same gate, opposite direction, and the second only became visible
because the first was granted.

## The census came first, and it is what authorises the merge

Measured on the published artifact, sha256-verified against its own marker, **before the producer
edit existed** — because a merge is only defensible if the resolution rate was known before the
code that performs it:

| population | resolved | of | carried | why carried |
|---|---|---|---|---|
| `GOLD_SCRIPT` | 1330 | 1380 | 50 | no canonical pipeline node |
| `S3_DATA_KEY` | 145 | 294 | 149 | 125 no canonical key, **24 ambiguous across firms** |
| `PORTAL_COMPONENT` | 20 | 22 | 2 | no canonical component |
| `REACT_QUERY_KEY` | 26 | 94 | 68 | no canonical query key |

**Three of those four reproduce the CVO's independent C-S40 census exactly.** Two seats, two
instruments, one set of numbers.

**Ambiguity is a carry, not a coin flip.** Twenty-four firm-relative keys like
`gold/artifacts/firm_mix_views.json` exist in *two* firms' buckets. Choosing one would invent a
cross-firm claim, so they are carried under `S3Key` with `origin=stitch` and
`origin_reason=ambiguous-across-firms`. R17's rule is merge by identity or carry — never guess,
never drop — and `lost = 0` is an arithmetic identity over the same populations, not a hope.

**The carried are a finding, not a defect of the merge.** The 68 unresolved query keys are things
like `rqk:QUERY_KEY` and multi-line template expressions — extractor artefacts *and* real keys the
canonical side misses. The 50 unresolved pipeline members are scripts the projection's own
extractor does not have. Both belong in front of the CVO at L9, which is what `F11-AC6` is for.

## The grain split, which is the whole reason this could not be a rename

`GOLD_SCRIPT` was **one type holding two grains**: 166 script-level members and 1,214
function-level. `PipelineScript` holds 133 and `PipelineFunction` 1,201. A rename at the fold
would have merged 1,380 mixed-grain members into a 133-member type by *name* — `W2-S48`'s grain
violation. The split happens at emission from the grain the trace id already carries
(`gold:x` -> `PipelineScript`, `gold:x:fn` -> `PipelineFunction`), and 1,198 of 1,214 functions
and 132 of 166 scripts then resolve by identity.

## Two defects the local run caught before anything was published

**The `STORED_IN` builder read a class literal the producer no longer emits**, and 955 boundary
edges silently became 0. A count that goes to zero because a dict key was renamed looks exactly
like a count that goes to zero because the estate changed.

**The producer's input carries its own prior output.** `derive_runner.archive_snapshot()` writes
the snapshot `derive_stitch.load_aws_layer()` reads, so after CG-s-24's fold the snapshot holds
**1,771 stitch-sourced nodes under the retired names** — measured in
`snapshots/20260909/graph-20260909.tar.gz`, LastModified `21:05:21Z`, re-archived by this worker's
own F-4 derive. Emitting new names is therefore not enough: the old ones keep arriving for one more
cycle, the graph is mixed in between, and the sentinel sees the old classes at collapsed counts.
`_retype_prior_cycle` closes it inside the grant — the producer re-typing its *own* earlier output,
identified by its own `source` stamp, not a fold-time rename of someone else's data. Row `W2-S61`;
the cycle itself is a standing property of this pipeline that no document stated.

Both would have shipped in the zip. Neither is visible from the source alone.

## What the CVO needs for the re-sign

`NODE_TYPE_LAYER` goes **65 -> 61** keys: `aws` 34 -> 33, `portal` 18 -> 16, `pipeline` 4 -> 3, `ms`
and `semctl` unchanged. **The frozen COND-A resource-type count is unmoved at 32** — `S3_DATA_KEY`
merged *into* `S3Key`, which was already an `aws` type, and no `aws` type was created or destroyed;
the layer count moves because a retired entry left it, not because a resource type did. The comment
keeps the GO's own words, because the retirement is only readable against them, and the re-sign
line says `PENDING`: it is the CVO's to write.

## What is committed and what is not

Committed and proven: the producer's canonical emission and grain split, the identity merge with
its carry rules, the `STORED_IN` fix, the prior-cycle re-type, the four map retirements, the
retired stamp, comp-debt's re-pointed scope, a 20-arm fixture and the census script that imports
the producer's own resolver rather than reimplementing it.

Not done, and it is the block, not a narrowing: the zip re-push, the ad-hoc `opal-stitch-produce`
build, the derive image act, the ad-hoc derive, the projection and the served reads. The manual-
trigger form the 21:5xZ amendment specifies is understood and was ready to run — one same-target
`start-build`, one `run-task` on the current `globgrph-derive-runner` revision, told apart on the
artifact rather than the clock, with the rules' own prior firings listed from history. None of it
was spent, because the first act in the chain would have re-broken the producer.
