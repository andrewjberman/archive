#!/usr/bin/env python
"""OG-ap-23: write the proof instance from the two live runs. The criterion text, invocation and expect are READ from the order,
not retyped. usage: python ap23_proof_gen.py <out.json> <ac1.txt> <ac2.txt>   (from the repository root)"""
from __future__ import annotations

import html
import json
import re
import sys

out, ac1_path, ac2_path = sys.argv[1:4]
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-23.code-batch-release.md"
text = open(TO, encoding="utf-8").read()
ac1 = open(ac1_path, encoding="utf-8").read().replace("\r", "").strip()
ac2 = open(ac2_path, encoding="utf-8").read().replace("\r", "").strip()


def crit(cid):
    m = re.search(r'<criterion id="%s"[^>]*><invocation>(.*?)</invocation><expect>(.*?)</expect>' % cid, text, re.S)
    return html.unescape(m.group(1)), html.unescape(m.group(2))


inv1, exp1 = crit("AC1")
inv2, exp2 = crit("AC2")
assert re.search(exp1, ac1) and re.search(exp2, ac2), "a live run does not match its criterion's expect"
bullet = re.search(r"^- `AC1`: (.*)$", text, re.M).group(1)
v1, v2 = bullet.split(" `AC2`: ")
v3 = re.search(r"^- `AC3` \(judgment, `3.0.0_SA_CVO~Z`\): (.*)$", text, re.M).group(1)

REL = "3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4"
STAND = "365b8c133a"
G = "infra/aws/ec2/opal-gateway/"
host = ("host md5 equals the release blob inside the 141-of-141 walk across app/, deploy/ and lib/ (W/ap23_host_md5_2.json), "
        "and the tool(s) it defines served in contract through the installed code")


def art(path, kind, state, ev, intro, cov, commit=REL):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": commit, "deployed_state": state, "deploy_evidence": ev,
            "introduces": intro, "artifact_covered_by": cov}


arts = [
    art(G + "app/client_core.py", "script", "DEPLOYED-VERIFIED", host,
        ["client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees"], ["AC1", "AC2"]),
    art(G + "app/client_role.py", "script", "DEPLOYED-VERIFIED", host, ["role_env_name", "FIRM_KEYED_VENDORS"], ["AC1", "AC2"]),
]
for n in ("schwab", "bd49f", "orion", "eclipse", "bdcottonwood", "smartx", "commonwealth"):
    arts.append(art(G + "app/client_adapter_%s.py" % n, "script", "DEPLOYED-VERIFIED", host, ["bind_firms", "resolve_account"], ["AC1", "AC2"]))
arts += [
    art(G + "app/etfs_rivals.py", "script", "DEPLOYED-VERIFIED", host,
        ["etfs_get_peer_group_members", "etfs_get_rival_fund_holdings", "etfs_who_holds", "etfs_get_security_reference", "etfs_get_coverage"], ["AC1", "AC2"]),
    art(G + "app/etfs_rivals_flow.py", "script", "DEPLOYED-VERIFIED", host,
        ["etfs_get_fund_trades", "etfs_get_fund_flows", "etfs_compare_peers", "etfs_get_research_notes", "etfs_get_rival_page_status"], ["AC1", "AC2"]),
    art(G + "app/etfs_silver.py", "script", "DEPLOYED-VERIFIED", host + " (after OG-ap-27 granted its prefixes to the internal reader)",
        ["etfs_get_new_securities", "etfs_get_fund_bloomberg_characteristics", "etfs_get_fund_snapshot"], ["AC1", "AC2"]),
    art(G + "app/portal_served.py", "script", "DEPLOYED-VERIFIED", host, ["mdpf_get_model_composition"], ["AC1", "AC2"]),
    art(G + "app/portal_json_served.py", "script", "DEPLOYED-VERIFIED", host,
        ["portal_get_correlations", "portal_get_etf_returns", "portal_get_factor_tilts", "portal_get_model_portfolio_timeseries",
         "portal_get_peer_performance", "portal_get_trending", "portal_get_cma_assumptions"], ["AC1", "AC2"]),
    art(G + "app/mdpf_classification.py", "script", "DEPLOYED-VERIFIED", host + "; the call ran as gateway-global-internal-reader-role (via_internal_reader true)",
        ["mdpf_get_security_classification"], ["AC1", "AC2"]),
    art(G + "app/data_entitlement.py", "script", "DEPLOYED-VERIFIED",
        host + "; taken WHOLE (A7): CLIENT_TOOLS in DATA_GRANT_TOOLS and TIER_ADMITTED_TOOLS (client_admission true on the host) and OG-bd-3's master_admin branch",
        ["CLIENT_TOOLS", "OG-bd-3"], ["AC1", "AC2"]),
    art(G + "app/tools.py", "script", "DEPLOYED-VERIFIED", "host md5 equal; registry 76 -> 103 on app.tools.mcp._tool_manager.list_tools(), delta exactly 27",
        ["etfs_get_rival_page_status", "portal_get_cma_assumptions", "mdpf_get_security_classification"], ["AC1", "AC2"]),
    art(G + "app/destructive_ops.py", "script", "DEPLOYED-VERIFIED", "host md5 equal; SAFE_TOOLS carries all 27 (AC1 SAFE 27 of 27)",
        ["client_get_fees", "mdpf_get_security_classification"], ["AC1"]),
    art(G + "app/integrations/portal_index/integration.py", "script", "DEPLOYED-VERIFIED", host + "; the MX-c-22 hunk, all that differs base to trunk",
        ["fund_ticker"], ["AC1"]),
    art(G + "deploy-to-ec2.sh", "script", "DEPLOYED-VERIFIED",
        "ran as committed: the staging block, the tar line (bundle group first, SRC group excluding the two app/refs names) and the six reader keys written into the .env (58 -> 64 key names, W/ap23_env_keys_after2.json)",
        ["BLACKDIAMOND49F_READER_ROLE_ARN", "_stage_src"], ["AC1", "AC2"]),
    art(G + "tests/test_og_ad1.py", "test", "COMMITTED-NOT-DEPLOY-SCOPE", "224 tests of the taken and related set pass in the release tree (12 more fail identically on the base)",
        ["CLIENT_TOOLS"], ["AC1"]),
    art(G + "tests/test_og_bd3.py", "test", "COMMITTED-NOT-DEPLOY-SCOPE", "passes in the release tree", ["MASTER_ADMIN"], ["AC1"]),
    art(G + "tests/test_entitlement_admin.py", "test", "COMMITTED-NOT-DEPLOY-SCOPE", "registered pin 95 -> 122, taken whole with data_entitlement.py", ["122"], ["AC1"]),
    art(G + "tests/test_data_entitlement_family.py", "test", "COMMITTED-NOT-DEPLOY-SCOPE", "non-data pin 86 -> 108, taken whole", ["108"], ["AC1"]),
    art("infra/aws/ec2/EC2_MANIFEST.json", "config_data", "COMMITTED-NOT-DEPLOY-SCOPE",
        "deployed_commit 3d5c9c8bf1 with previous_deployed_commit d577e0e729, mcportal_commit 090b9cdc85, file_checksums from the release blobs 10 of 10 cross-checked against the host's md5 (2 move)",
        [REL], ["AC2"], STAND),
    art(G + "runbooks/SCHWAB_PILOT_RUNBOOK.md", "doc", "COMMITTED-NOT-DEPLOY-SCOPE",
        "section 7.2 names 3d5c9c8bf1 live with d577e0e729 as the rollback target; rb.AC2 PASS (targets named 3, without guard 0, not in manifest history 0)",
        ["3d5c9c8bf1"], ["AC2"], STAND),
]

doc = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-23", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~Z",
    "session_log": "org/tier2_senior/0.7.0_AE_CloudOps~Z/logs/2026-10-16/ap23_code_batch_release.md",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "f2b066d9ad"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "3b056fd12e", "to_ref": TO},
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "AC1: " + v1, "method": "command", "invocation": inv1, "expect": exp1, "output_evidence": ac1,
         "denominator": "48 files differing, 0 outside the batch set; 0 Terraform files; 27 tools added by trunk, 27 registered, 0 extra, 27 of 27 in SAFE and in data_entitlement.py; "
                        "the manifest's mcportal_commit equals the GO's and is the only manifest field changed; the deploy script carries 3 opal_naming, 4 roster and 4 registry-copy staging lines, "
                        "the sources exist at trunk, 0 data copies are committed; the tar census reads each of the two app/refs files once with md5 equal to trunk's blobs. Re-run after the "
                        "release landed, when the manifest names the release as live, so its base clause reads the previous_deployed_commit.",
         "status": "PASS"},
        {"criterion_id": "AC2", "criterion_verbatim": "AC2: " + v2, "method": "command", "invocation": inv2, "expect": exp2, "output_evidence": ac2,
         "denominator": "ledger 1 of 1 CLOSED (the newest entry of the slug; the first, rolled back, is also closed) with 0 sentinels at HEAD; landed=current; registry 76 -> 103 on one named instrument, "
                        "delta exactly 27; per-tool 27 of 27 on opal_served, non_opal_refused and reads_on_refusal 0; reader env keys 6 of 6; client admission refused-then-served; the classification "
                        "call via the internal reader; C1 and C2 true. THIS IS THE SECOND ATTEMPT: the first read 23 of 27 (four IAM denials, row Z-S164) and was rolled back under C5.",
         "status": "PASS"},
        {"criterion_id": "AC3", "criterion_verbatim": "AC3 (judgment, 3.0.0_SA_CVO~Z): " + v3, "method": "manual_read_with_citation",
         "invocation": "NOT RUN BY THIS SEAT. The criterion carries judgment=\"true\" and names 3.0.0_SA_CVO~Z as its grader; a judgment criterion is graded at L9 and never self-graded.",
         "output_evidence": "What this seat CAN say, and no more: all 27 tools are live and answer in contract through the installed code (27 of 27 served an Opal stand-in an enveloped answer and refused a non-Opal with zero reads), "
                            "and one real SmartX read returned 12 rows for firm A and 0 for the other. That is AC3's PRECONDITION, not AC3: whether the first client and rival answers read as an analyst would want them "
                            "(a firm's data date stated, figures with units, rows never merged across firms, Schwab masters never summed) is a judgment about content on a real call, and the probes here were argument-shaped "
                            "and printed counts only.",
         "denominator": "0 of 4 named judgment specifics exercised by this seat; 27 of 27 tools proven to answer in contract, which is the criterion's precondition. The grader is 3.0.0_SA_CVO~Z.",
         "status": "N/A-BY-CONSTRUCTION",
         "status_reason": "A JUDGMENT criterion, graded at L9 and never self-graded (CLAUDE.md section 1, L9); not unverifiable and not PASS, simply not this seat's to compute."},
    ],
    "controls": {
        "determinism": {
            "method": "The release was cut on a base read three ways (the manifest at HEAD, the S3 git-ref metadata and an SSM md5 walk of the host), the ask's hash was compared with the one each half signed, the deploy ran from a tree whose HEAD was the signed release and whose parent was the live ref, "
                      "and every state the act changed was read back on the instrument that owns it. The refusal arm counts reads on boto3 and on every internal-reader and client-role factory, so a read on a refusal path both counts and fails loudly.",
            "observed": "ask sha256 prefix ba5b9325bca5 equal at the GO; deploy tree HEAD == 3d5c9c8bf1 and its parent == live d577e0e729 on the manifest AND on the artifact's git-ref (the wrapper's guard, twice); 141 of 141 host files equal with 0 differ, 0 missing, 0 extra and the two app/refs files equal to trunk's blobs; "
                        ".env 58 -> 64 names (six added, none removed); registry 76 -> 103 delta exactly 27; per_tool_good 27 of 27 with reads_on_refusal 0; client_admission true with the non-admin refused on all five; the classification call's session role gateway-global-internal-reader-role against an instance role opal-gateway-role.",
            "status": "STABLE"},
        "mutant": {
            "description": "The order names no mutant. Negative arms stand in its place: (a) the tar census, run on the previous cut's script as well, which must FAIL; (b) the first deploy attempt itself, whose served read caught four IAM gaps the preflight had declared absent; (c) the host md5 walk, bracketed by BEGIN_WALK/END_WALK so a truncated read cannot pass; (d) the refusal guard, which raises on any data-client request.",
            "expected": "the control reads differently where the positive read matches; a truncated walk refuses; reads_on_refusal 0 with the guards proven installed",
            "observed": "(a) the previous cut's script shipped the planted decoy under both app/refs names, the committed script ships each file once with the trunk md5; (b) the first served read read 23 of 27, naming s3:ListBucket AccessDenied for etfs_get_new_securities, etfs_get_fund_bloomberg_characteristics, etfs_get_fund_snapshot (opal-data-etfs) and mdpf_get_model_composition (opal-data-mdpf), and the base was redeployed; after OG-ap-27 the same read gave 27 of 27; (c) both walks were bracketed; (d) the guard read 0.",
            "status": "N/A-SPEC-NAMES-NONE"},
    },
    "artifacts_produced": arts,
    "compiler_tools": [
        {"tool": "the seam enumeration", "invocation": "python W/ap23_seams.py <trunk_sha> W/ap23_seams_r5.json", "result": "61 distinct seams over 173 importer edges, 0 STOP; lib/trading_calendar.py differs base to trunk but the take files call only names the base has"},
        {"tool": "the naming gate in ENFORCE", "invocation": "ng2.AC2.sh, ng3.AC1.sh and .tools/safe-commit.sh on the release commit", "result": "ng2.AC2 PASS (0 REFUSE, 10 RULED), ng3.AC1 PASS (0 REFUSE, 11 RULED), the release commit NAMING-GATE WARN 14 graded and 0 REFUSE; trunk's gate, registry, schema and lib siblings laid over the base-era tree as uncommitted files (W/ap23_gate_overlay_manifest.txt)"},
        {"tool": "the tar census", "invocation": "python W/ap23_tar_census.py <script> <trunk_sha> W/ap23_tar_census.json", "result": "PASS on the committed script, FAIL on the previous cut's script"},
        {"tool": "the deploy ledger", "invocation": ".tools/deploy_ledger.py open / close-leg x4 / close, twice", "result": "nfra-oplgtw-gateway-release-code: the first entry closed superseded by the rollback, the second closed with 4 legs each on its own proof and the sentinel removed"},
        {"tool": "the served read", "invocation": "W/ap23_run_served.py -> W/ap23_served_harness.py over SSM under /opt/opal-gateway/.venv/bin/python", "result": "registry 76 -> 103; per_tool_good 27 of 27; client_admission, via_internal_reader, reader keys 6, C1 and C2 true"},
        {"tool": "rb.AC2, the standing runbook criterion", "invocation": "bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks/rb.AC2.sh", "result": "PASS exit 0, live 3d5c9c8bf1, targets named 3, without guard 0, not in manifest history 0"},
    ],
    "surprises": [
        "NFRA_OPLGTW-Z-S161: the first release commit was refused by the naming gate on 23 lines of three taken files (partner roster, portal_served, etfs_silver); resolved by A2 (roster and registry copy staged at bundle time) and OG-ng-3.",
        "NFRA_OPLGTW-Z-S164: the first Phase B attempt served 23 of 27 tools; four were AccessDenied for the internal reader role, which the order's preflight declared as needing no IAM; the base was redeployed under C5 and OG-ap-27 granted the four prefixes before this second attempt.",
    ],
    "declared_exclusions": [
        {"item": "AC3, the analyst reading of the first client and rival answers", "reason": "A judgment criterion graded by 3.0.0_SA_CVO~Z at L9 on a real call; this seat proved only its precondition."},
        {"item": "dashboard/ is outside the md5 verdict", "reason": "By grain: deploy-to-ec2.sh builds it from the mcportal checkout at the manifest pin 090b9cdc85, so no release blob exists in this repo to compare it to."},
        {"item": "the stand-in for master_admin", "reason": "Built in-process from the host's own configured roster key with a synthetic Opal-domain address; no identifier was printed or written and the policy store was only read. It exercises the real tier resolution but is not a call by a person through the public edge, which needs a per-user delegated token this seat does not mint."},
    ],
}
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(doc, indent=1) + "\n")
print("wrote", out)
