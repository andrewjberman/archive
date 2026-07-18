# comp-describe -- COO-SoD routing handoff (NFRA_COMPSIMILAR describe surface)

**From:** 0.8.0_AE_CloudComp~D  **To:** 2.0.0_SA_COO  **Date:** 2026-07-18
**AE code shipped:** `ff21627b0` (pushed CLOUD). **Same SoD shape as KUZUSPLIT-P1 `@7288d1267`.**

Andrew-direct pull-forward (via base 003245Z, COO GO 003449Z): the describe/summary surface AHEAD of
the KUZUSPLIT-P1 projection. Decoupled from BOTH gates (no Kuzu projection, no resource_summaries
table) -- servable NOW off the LANDED derive-at-scan engine over the EXISTING comp-kuzu QUERY path.

## What AE already landed (`ff21627b0`, self-commit)
- `org/modules/graph/debtscan/summary_corpus.py` -- `--describe <arn-or-name>` verb (2-query
  derive-at-scan, lexical resolve ladder, `_partition_edges` + self-test **M5**, `--json`).
- `org/modules/graph/comp-tools.yaml` -- comp-describe reference entry.
- `org/modules/graph/comp-coverage-map.yaml` -- comp-describe `meta_tools` row, **routable: false**.
- `.tools/comp-describe` -- wrapper **on-disk, functional, UNTRACKED** (grantee cannot self-register:
  committing it now would DISK-IMPLIES-REGISTERED-block member 5 until the tools_index/entries row lands).

Gates already green on the AE half: self-test 5/5, commit-gate clean, `comp-manifest-check`
registration-invariant PASS, `comp-coverage-check` PASS.

## COO-SoD: 4 pieces to land in one commit

### A. `org/modules/graph/graph-call-manifest.yaml` -- add an `entries:` row (place near the cloud-graph entries, e.g. after `cloud.refresh.incremental`)
```yaml
  - id: cloud.describe.resource
    use_case: "What IS this resource / what does it do / describe this ARN / find + describe one AWS resource -- ONE resource's purpose synthesized from the graph (type + layer + producers/consumers/wiring)."
    canonical_call: "comp-describe <arn-or-name> [--json]   # find + describe ONE resource off the derive-at-scan engine"
    tool: comp-describe
    mode: query
    write_path: false
    layer: cloud
    cost: "~ms: 2 targeted comp-kuzu queries for an exact ARN (node + edges); +1 light all-node sweep only for name/substring resolution. Never the full-corpus build."
    freshness: "reads the live comp-kuzu graph (shares its provenance/HEAD-oracle); derive-at-scan -- no projected property, no table, nothing to go stale beyond the graph vintage. 0 matches -> hints comp-kuzu-inc (broken retrieval != absent)."
    rebuild_trigger: "never (Rule 20 QUERY-default)"
    anti_pattern: "using it for NEAREST-BY-PURPOSE similarity (that is comp-similar Phase-2, KUZUSPLIT-P1 + table gated) -> describe is exact/lexical find of ONE resource. Arbitrary Cypher traversal -> comp-kuzu; blast radius -> comp-blast; a named pipeline thread -> pipescript."
    status: canonical
    notes: "NFRA_COMPSIMILAR describe surface (Andrew-direct pull-forward 2026-07-18, code @ff21627b0, 0.8.0_AE_CloudComp~D; registration COO-SoD -- grantee cannot self-register). Servable off the LANDED derive-at-scan engine (summary_corpus.py @3fe0eedf0) over the EXISTING comp-kuzu QUERY path; decoupled from BOTH the KUZUSPLIT-P1 projection AND the resource_summaries table. Resolution LEXICAL (exact ARN -> exact name -> substring); ambiguous -> disambiguation list, no silent guess."
```

### B. `.tools/comp-which` -- add a curated RULE (near the comp-kuzu block in `RULES`)
```python
    (["what is this resource", "what does this resource do", "describe this resource",
      "describe the resource", "describe this arn", "describe this lambda", "describe this bucket",
      "what is this arn", "what does this lambda do", "what does this bucket do",
      "what does this resource", "explain this resource", "summarize this resource",
      "purpose of this resource", "what is this aws resource", "look up this resource",
      "find and describe a resource", "describe a resource by name"],
     "find + describe ONE AWS resource (comp-describe)",
     ["comp-describe <arn-or-name>"],
     "FIND + DESCRIBE one AWS resource -- its purpose (type + layer + producers/consumers/wiring) "
     "synthesized from the graph. DISTINCT from comp-kuzu (arbitrary Cypher traversal), comp-blast "
     "(what breaks if I change X), pipescript (a named pipeline thread). Nearest-BY-PURPOSE similarity "
     "is comp-similar Phase-2 (gated) -- this is exact/lexical find of ONE resource"),
```
**Collision note (measured baseline, pre-land):** the phrases above match **no curated rule today** (clean
gap -- verified `comp-which "what does this resource do"` = NO CURATED RULE). The one phrase to AVOID adding
verbatim is bare **"find an aws resource"** -- it fuzzy-hits `comp-assets` (OPAL_ASSETS backfill census, score
1.85), a different intent. Kept it out of the list above; steer the vocab to "describe / what IS this ONE resource".

### C. `org/modules/graph/comp-coverage-map.yaml` -- flip comp-describe `routable: false` -> `true`
(and, mirroring the kuzu rows, swap the trailing "routable:false in the AE ship ... COO-SoD flips to true"
clause for "LANDED by COO 2026-07-18 (SoD; routing entry cloud.describe.resource in graph-call-manifest.yaml; code @ff21627b0)").

### D. `git add -f .tools/comp-describe` -- force-add the wrapper (`.gitignore` ignores `.tools/` wholesale; a plain `git add` no-ops).

## Verification (COO, before/after land) -- exercise, not infer
```
comp-which "what does this resource do"     # -> comp-describe rank-1 (target)
comp-which "describe this resource"         # -> comp-describe rank-1
python .tools/comp-which-routing-test.py    # regression clean (kuzu/assets/blast/pipescript unchanged)
comp-manifest-check                          # registration-invariant PASS (comp-describe now via entries tool:)
comp-coverage-check                          # PASS
comp-describe "arn:aws:s3:::opal-data-mdpf"  # exercised: returns S3_BUCKET summary (proven on AE side)
```
AE-side already-exercised (live graph): exact ARN (`bd-49f-fees-runner` -> full summary + producers/consumers/
wiring), exact name unique (`opal-data-mdpf`), exact name **ambiguous** (`opal-cot-value-parity` -> BOTH an
IAM_ROLE and a LAMBDA -> disambiguation, no guess), substring, 0-match (refresh hint), `--json`.

Ping ~D on land (or if the rank-1 routing needs a vocab tune). Another worked example for NFRA_COMPREG.
