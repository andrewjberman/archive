# NFRA_GLOBGRPH.NODEGAP: CodeBuild recognizer -- design for CTO arch-gate

**Author:** 0.7.0_AE_CloudOps~B · **Date:** 2026-07-08 · **Status:** DESIGN (staged for CTO arch-gate; NOT applied)
**TO:** NFRA_GLOBGRPH.NODEGAP.7-dangling-endpoint-triage.md (item #2, `opal-drift-producer`) · follow-on from the triage (commit 770e839b4)

## Problem (recap)

`opal-drift-producer` is a live CodeBuild project (`arn:aws:codebuild:us-east-1:313476888478:project/opal-drift-producer`, live-confirmed this session) with a dangling `TRIGGERS` edge from its EventBridge rule (`opal-drift-producer-nightly`), because `comp_aws_cli.py` has **zero CodeBuild recognizer** -- grep-confirmed, not a filter bug. The surrounding resources (IAM role, log group, EventBridge rule) all materialize; the project itself does not.

## Design

**New recognizer function** (mirrors `live_ssm_documents()` / `live_schedules()`'s shape exactly -- same file, same pagination/error-swallow pattern, same dict shape):

```python
def live_codebuild_projects():
    """CODEBUILD_PROJECT nodes (aws_codebuild_project) -- the CI/build-runner surface the
    graph never scanned. Fills the opal-drift-producer NODEGAP finding (2026-07-08)."""
    c = _boto("codebuild")
    nodes = []
    try:
        names = []
        tok = None
        while True:
            kw = {"nextToken": tok} if tok else {}
            resp = c.list_projects(**kw)
            names += resp.get("projects", [])
            tok = resp.get("nextToken")
            if not tok:
                break
        # batch_get_projects caps at 100 names/call; chunk defensively (estate has 1 today,
        # but the pattern shouldn't silently truncate if it grows).
        for i in range(0, len(names), 100):
            resp = c.batch_get_projects(names=names[i:i + 100])
            for p in resp.get("projects", []):
                nm = p["name"]
                src = p.get("source", {}) or {}
                nodes.append({
                    "id": nm, "type": "CODEBUILD_PROJECT",
                    "arn": p.get("arn"), "name": nm,
                    "service_role": p.get("serviceRole"),   # -> USES_ROLE-class edge (existing IAM-edge former picks this up, mirrors other AWS-resource-to-IAM-role edges)
                    "source_type": src.get("type"),
                    "timeout_minutes": p.get("timeoutInMinutes"),
                })
    except Exception:
        return nodes
    return nodes
```

**Registration** (`comp_aws_cli.py:1130`-area recognizer-registry dict, alongside `"ssm_document": (live_ssm_documents, ["aws_ssm_document"])`):
```python
"codebuild_project": (live_codebuild_projects, ["aws_codebuild_project"]),
```

**Taxonomy addition** (`derive_runner.py:1623`, `NODE_TYPE_LAYER`): `"CODEBUILD_PROJECT": "aws"` -- a NEW node_type on the SAME fail-closed `NodeTypeLayerGap` gate the semctl (`C2Motif`/`C3System`) and SSM_DOCUMENT/SCHEDULE/LAMBDA_LAYER additions went through today (commits d2ab31596, 24790cf54). Per that established pattern: dual-sign required (CTO arch-gate + CVO count re-sign) BEFORE any derive run encounters the new recognizer's output, or the derive fails closed the instant `live_codebuild_projects()` starts emitting nodes.

**Edge formation:** no new edge-forming code needed. The EventBridge `TRIGGERS` edge (from `live_eventbridge()`, already resolves `target_arn` -> a node lookup) will resolve automatically once a `CODEBUILD_PROJECT` node with `id=opal-drift-producer` / matching `arn` exists -- this closes the specific dangling edge NODEGAP found, by construction, with zero edge-code changes.

## Round-trip test plan (for CTO's I3 exercise ask)

1. **Pre-change baseline:** comp-kuzu query confirms 0 `CODEBUILD_PROJECT` nodes exist (grounded this session).
2. **Post-arch-gate derive run:** re-query -- expect exactly 1 `CODEBUILD_PROJECT` node (`opal-drift-producer`, the only live CodeBuild project in the estate today), `layer=aws`, 0 `UNCATEGORIZED` (confirms the taxonomy gate held).
3. **Dangling-edge closure check:** the `opal-drift-producer-nightly` EVENT_RULE's `TRIGGERS` edge, previously dangling (target absent), now resolves to the new node -- verify via `MATCH (r:CloudNode {node_id:'arn:...:rule/opal-drift-producer-nightly'})-[e:CloudEdge {edge_type:'TRIGGERS'}]->(t) RETURN t.node_id` returning the CodeBuild project, not empty.
4. **IAM-edge check:** `service_role` (`opal-drift-producer-codebuild-role`) forms whatever edge-type the existing IAM-role-reference pattern uses for other AWS resource types (grounding this at build time against the actual edge-former code, not assumed here).

## Blast radius / rollback

Additive: 1 recognizer function, 1 registry-dict line, 1 `NODE_TYPE_LAYER` entry. **Checked this session (`comp-iam service derive_runner`): the derive role has NO CodeBuild grant today** -- this needs a NEW IAM policy statement (`codebuild:ListProjects`, `codebuild:BatchGetProjects`, read-only) on the derive role, alongside the code change. Not a blast-radius risk (additive, read-only, no new resource exposure beyond visibility into project metadata already visible via CodeBuild's own console/API to anyone with account access) but it IS a real `iam.tf` touch -- run `comp-iam gaps` after landing per the standard post-iam.tf-change discipline. Rollback = revert the 3 code additions + the IAM statement; no other component depends on `CODEBUILD_PROJECT` existing yet.

## Ask

Arch-gate GO on the new `CODEBUILD_PROJECT` node_type (layer=`aws`) + CVO count re-sign (additive-only, +1 type, mirrors today's SSM_DOCUMENT/SCHEDULE/LAMBDA_LAYER precedent exactly) + the new read-only CodeBuild IAM grant on the derive role. On GO: land the recognizer + registration + taxonomy entry + IAM statement, coordinate the derive-image rebuild (per the established rebuild-coordinator pattern), exercise the round-trip test plan above, run `comp-iam gaps`, RAVC CTO + CVO.
