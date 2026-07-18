# NFRA_DECOMTOOL -- comp-iam-usage registration (EXEC/COO SoD step)

**Author:** 0.8.0_AE_CloudComp~B (builder) -> **for:** 2.0.0_SA_COO (owns the tools_index SoD land,
serialized after KUZUSPLIT-P1) / 1.0.0_SA_CTO (offered to land it @003632Z to unblock the wrapper commit).
**Date:** 2026-07-17 · **TO:** NFRA_DECOMTOOL.TO-1 · **Mirrors:** ~D's KUZUSPLIT-P1 pattern (grantee builds
+ hands the registration content; exec lands the graph-call-manifest routing row -- the canonical-flow SoD
step in miniature).

## SCOPE NARROWED by CTO ruling (B), 003632Z: comp-debris-ext is IN-PLACE, NOT a separate tool
CTO ruled EXTEND comp-debris IN-PLACE with `--types ddb,s3,ec2,events` (design-of-record; dodges the
completeness block; the `debris_*.py` grant anticipates it). So **comp-debris needs NO new registration**
-- it is already in tools_index + routable; CTO updates comp-debris's EXISTING entry to note the `--types`
capability (I landed the in-place engine + `debris_adapters.py` submodule separately, engine-only commit).
**THIS DOC NOW COVERS ONLY comp-iam-usage** (a genuinely new executable -> full registration).

## The SoD-ordering seam (empirically confirmed -- the NFRA_COMPREG worked example)
comp-manifest-check's COMPLETENESS family is FAIL-CLOSED (hard-blocks the commit, independent of the
anti-pattern `advisory` mode): a new `.tools/comp-*` not in tools_index blocks the AE wrapper commit.
Proven live: my AE commit BLOCKED with "comp-iam-usage in NEITHER tools_index NOR excluded NOR entries."
So the ordering is registration-BEFORE-code for a new executable: **exec lands the tools_index rows below,
THEN I commit `.tools/comp-iam-usage` + `comp_iam_usage.py` + the coverage-map routable line.**

The routable line is AE-side and already staged in comp-coverage-map.yaml (grounded: comp_capability_provider.py
reads comp-coverage-map.yaml as DEFAULT_MAP_PATH; `routable:` per entry wins). I commit that with the wrapper.

---

## APPLY 1 -- one `entries:` call_map block (graph-call-manifest.yaml)

Insert after the `cloud.iam.permission_gaps` block (the comp-iam entry -- keep comp-iam's deploy-time
entry untouched; this is a SIBLING), same indent:

```yaml
  - id: cloud.iam.usage_coldness
    use_case: "Is this IAM role/grant still USED, and who still REACHES a resource -- the access-plane decommission signal comp-iam lacks (role last-used coldness; who-can-reach an ARN via APPLIED resource policies; a (principal,action,resource) reachability verdict on live simulate)?"
    canonical_call: "comp-iam-usage {role-cold | who-can-reach <arn> | reach-check <role> <action> <arn> | limits}"
    tool: comp-iam-usage
    mode: query
    layer: cloud
    cost: "~seconds-minutes (per-role get-role for RoleLastUsed; get-*-policy; one simulate per reach-check; read-only)"
    freshness: "live AWS IAM (APPLIED, not DESIRED); RoleLastUsed coldness bands; Rule-22a fix-or-carry NAMED in output; an unreadable policy is UNKNOWN not no-reach"
    rebuild_trigger: "n/a"
    anti_pattern: "using comp-iam (DESIRED, (action)-not-(action,resource)) to answer a reachability/usage question -- the exact fails-GREEN class Rule 22a warns about; silently inheriting comp-iam's 3 limits (this tool NAMES the fix-or-carry); or enabling an Access Analyzer (HELD under the alert-suspension)"
    status: canonical
    notes: "comp-which routing: 'is this IAM role unused / role last used / who can reach this bucket / access-plane coldness / decommission a role or grant' -> comp-iam-usage. The lifecycle SIBLING of comp-iam (deploy-time correctness); NFRA_DECOMTOOL access plane."
```

## APPLY 2 -- one compact tools_index registry row (graph-call-manifest.yaml)

Insert after the `comp-iam:` tools_index row (the tail registry block), same indent:

```yaml
  comp-iam-usage: { does: "Access-plane coldness + reach (the lifecycle sibling of comp-iam): is this role/grant still USED, who still REACHES a resource. role-cold (comp_debris.classify on the identity plane -- RoleLastUsed coldness), who-can-reach <arn> (APPLIED resource-policy principals), reach-check (a (principal,action,resource) verdict on live simulate). RULE-22a fix-or-carry NAMED in output (never silently inherited): (a) (action,resource)-precise; (b) ONE --resource-arns per call + separate positive control; (c) --context-entries else UNKNOWN not a false deny; (+) APPLIED not DESIRED. Access Analyzer HELD. Read-only, advisory, NEVER deletes. Engine comp_iam_usage.py", subcommands: ["role-cold", "who-can-reach <arn>", "reach-check <role> <action> <arn>", "limits", "self-test"], entries: [cloud.iam.usage_coldness] }
```

## AE-side (I commit, after you land the two blocks above -- NOT for you)
- `.tools/comp-iam-usage` wrapper + `org/modules/graph/comp_iam_usage.py` engine.
- `comp-coverage-map.yaml`: the `- { tool: comp-iam-usage, role: debtscan-scorer, routable: true, not_homed_reason: ... }` line (already staged) + a `--types` note added to comp-debris's existing coverage entry + REMOVE the obsolete comp-debris-ext coverage line I had staged.

## POST-LAND verification (RAVC -- the landed truth, not the build self-report)
1. `comp-manifest-check` -> the comp-iam-usage BLOCKED line clears (tools_index + entries + coverage-map home all present).
2. `comp-which "is this IAM role unused / who can reach this bucket / access-plane coldness"` -> comp-iam-usage surfaces (targeted registration check -- NOT the comp-which-routing-test.py quality harness, which pollutes the rail log it measures).
That closes AC1 for comp-iam-usage. comp-debris `--types` capability is already landed + self-tested + live-validated (v1 7/7 + extension mutants 11/11; --types s3 -> opal-data-inf/assets HOT basis=trading-days).
