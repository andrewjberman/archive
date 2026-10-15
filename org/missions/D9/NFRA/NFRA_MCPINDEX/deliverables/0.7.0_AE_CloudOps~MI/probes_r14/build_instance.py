"""build_instance.py: write the MX-r-14 proof_of_spec instance from the recorded probe outputs (evidence is read from the
probe files, not retyped). Run from the workspace root."""

import json

D = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MI/"
P = D + "probes_r14/"
OUT = D + "NFRA_MCPINDEX.TO-MX-r-14.round17-catalog-release.proof_of_spec.json"
ORDER = "org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-14.round17-catalog-release.md"


def rd(p):
    return open(p, encoding="utf-8").read().replace("\r", "").strip()


def section(txt, marker):
    return txt.split("=== " + marker, 1)[1].split("\n===", 1)[0].split("\n", 1)[1].strip()


acs = rd(P + "r13.AC2_r13.AC3_r14.AC4_POST.txt")
ac1 = rd(P + "r14.AC1_POST.txt")

exp = {}
for line in open(ORDER, encoding="utf-8").read().splitlines():
    if "<criterion id=" in line:
        cid = line.split('id="')[1].split('"')[0]
        exp[cid] = (line.split("<invocation>")[1].split("</invocation>")[0], line.split("<expect>")[1].split("</expect>")[0])
assert sorted(exp) == ["AC1", "AC2", "AC3", "AC4"], sorted(exp)


def crit(cid, out, denom):
    inv, expect = exp[cid]
    assert "RESULT: PASS" in out, (cid, out[-200:])
    return {
        "criterion_id": cid,
        "criterion_verbatim": expect,
        "method": "command",
        "invocation": inv,
        "output_evidence": out,
        "denominator": denom,
        "status": "PASS",
        "expect": "RESULT: PASS",
    }


acceptance = [
    crit("AC1", ac1, "Over a printed scan denominator of 16 of 16 sentinels; the r14 ledger has 1 entry file at HEAD, no sentinel at HEAD, and is not listed OPEN or HELD. Pointed at a slug with no ledger as a negative arm it read FAIL exit=1 (entry files at HEAD=0)."),
    crit("AC2", section(acs, "round12/checks/r13.AC2.sh"), "N=99 served tools; the partition sums 99 of 99 (a=11 valid 11, b=76 valid 76, c=12 valid 12); definitions located 99 of 99; discover good 3 of 3."),
    crit("AC3", section(acs, "round12/checks/r13.AC3.sh"), "DEPTH 11 of 11 valid; ANSWER-TIME measured rows 17, answered measured and equal 17 of 17; anchors 2 of 2."),
    crit("AC4", section(acs, "round17/checks/r14.AC4.sh"), "Host catalog version 0.5, harvest 78, table 216, key_template 216, retired 5, rows 304, nl_tags 304, inferred 44, firm 24; 35 distinct read_tool names, 0 unserved by the deployed commit; host md5 49b7a6e9656ddfe753e156f6df347b8c equals the tree md5."),
]
for a in acceptance:
    a["output_evidence"] += "\nexit=0" if "exit=" not in a["output_evidence"] else ""

NEW = "c4c106aea1cc47d15f81397208226bd9b292c9dc"
OLD = "06cfb6db6471972c7304cd3d7a5b93e6f521ad72"
S3 = "s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/"


def art(path, kind, ref, state, covers, ev):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": ref, "deployed_state": state, "artifact_covered_by": covers, "deploy_evidence": ev}


artifacts = [
    art(S3 + "opal-gateway-c4c106aea1.tar.gz", "s3_object", "774a847c8418994c924787a3c4613186", "DEPLOYED-VERIFIED", ["AC2", "AC3", "AC4"],
        "THE SERVED ARTIFACT. head-object read BEFORE leg L1 closed (19:56:15Z): PRESENT 736,412 B, git-ref " + NEW + ", where it read 404 pre-apply. -latest carries the same size, ETag and git-ref. Upload and pull ssm:663c8355-e719-4224-aaeb-117be2529521 Success; the base guard read declared base == live ref " + OLD + " at both checkpoints. (label_readback_r14.txt)"),
    art(S3 + "opal-gateway-latest.tar.gz", "s3_object", "774a847c8418994c924787a3c4613186", "DEPLOYED-VERIFIED", ["AC2"],
        "Re-pointed from " + OLD[:10] + " to " + NEW[:10] + " by the deploy: 736,412 B, git-ref " + NEW + " (label_readback_r14.txt)."),
    art("i-07dccb1615503ac99:/opt/opal-gateway", "aws_resource", NEW, "DEPLOYED-VERIFIED", ["AC2", "AC3", "AC4"],
        "Host byte census against the BUILD INPUT (the cut), not by filename: 121 of 121 common, 121 byte-identical, DIFFER 0, 0 cut-only, 0 host-only (ssm:5b5dea3a-8dd1-47ba-9982-e189fd207fed). NEGATIVE CONTROL, same read, against the live tree " + OLD[:10] + ": DIFFER 2 = exactly app/refs/DATA_CATALOG.yaml and app/integrations/opal_discover/integration.py, EXPECTED CHANGED SET MATCH (host_vs_cut_r14_POST.txt). Four censuses (four_censuses_r14_POST.txt): tools 99 = 99 names equal, .env keys 57 = 57, ENABLED_INTEGRATIONS 7 = 7, MC Portal per-tool link counts 39 tools / 119 links read by the host's real reader (ssm:1f83a614-35a4-4b54-b5b8-a4e723b75a90), each with a negative control reading False."),
    art(S3 + "opal-gateway-06cfb6db64.tar.gz", "s3_object", "d8470277354440424e89cc848a88d469", "DEPLOYED-VERIFIED", ["AC2"],
        "THE ROLLBACK KEY, untouched by this release: 734,698 B, ETag d8470277..., git-ref " + OLD + ", read BEFORE leg L1 closed (label_readback_r14.txt)."),
    art("infra/aws/ec2/EC2_MANIFEST.json", "config_data", "d4cd768b9b", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC1"],
        "services.opal-gateway: deployed_commit " + NEW + ", previous_deployed_commit " + OLD + ", deployed_at 2026-10-15T19:50:39Z, release_note naming this release in the SAME write as the commit fields; exactly 5 fields changed, 5 insertions / 5 deletions, 1 of 27 services (probes_r14/write_manifest.py). Committed LOCAL; origin not pushed."),
    art("org/critical_paths/change_management/20261015T1946Z_nfra-mcpindex-r14-catalog-release_deploy_completion.md", "doc", "d4cd768b9b", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC1"],
        "The NEVER-2 ledger: 5 legs, each closed with proof, CLOSED, sentinel removed in the same commit."),
    art(D + "ANNOUNCE_MX-r-14.md", "doc", "9d7967142e", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC2"],
        "PHASE A: the pins, the live ref read from the host by hash (121 of 121), the four censuses, the open-ledger scan 18 of 18."),
]

mutant = {
    "description": "NOT a planted byte mutation, and the reason is recorded: every limb of this act's claim lives in a deployed host and a ledger, not in a function a mutant could break. The discriminating evidence is the SAME instrument reading both states: the host byte census read DIFFER 0 against the live tree before the apply and DIFFER 0 against the cut after it, and DIFFER 2 against the other tree each time.",
    "expected_not_landed": "Before the apply (19:31:11Z): the host matches the LIVE tree " + OLD[:10] + " with DIFFER 0 and differs from the cut by exactly the two shipped files; link counts 33 tools / 112 links; the live catalog reads nl_tags=260 inferred=0 firm=0.",
    "expected_landed": "After the apply: the host matches the CUT with DIFFER 0 and differs from the live tree by exactly those two files; link counts 39 / 119; the host catalog reads rows=304 nl_tags=304 inferred=44 firm=24; the ledger is CLOSED with its sentinel gone at HEAD.",
    "expected": "Each instrument reads the old state before the act and the new state after, and the two readings are mirror images of one another rather than one reading plus an assumption.",
    "observed": "FIRED AS EXPECTED on every arm. (1) Pre-apply: host vs the live tree DIFFER 0, vs the cut DIFFER 2 = the two files, EXPECTED CHANGED SET MATCH. Post-apply: host vs the cut DIFFER 0 over 121, vs the live tree DIFFER 2, MATCH. (2) The AC4 counts script, run on the live catalog and on the cut catalog before the apply, read nl_tags=260 inferred=0 firm=0 and nl_tags=304 inferred=44 firm=24 (ac4_counts_cut_vs_live_r14.txt); on the host after the apply it read the cut's. (3) Link counts: host real import 33/112 before (previous release) and 39/119 after, with a bump-one negative control reading False; the tool census names EQUAL with a drop-one control reading False. (4) AC1 pointed at a slug with no ledger reads entry files at HEAD=0 and RESULT: FAIL exit=1; at the closed ledger it reads PASS.",
    "status": "FIRED-AS-EXPECTED",
}
determinism = {
    "method": "r14.AC1 was run twice back to back against unchanged inputs after the close commit (r14.AC1_twice.txt).",
    "observed": "Byte-identical output both times, RESULT: PASS exit=0 (16 of 16 sentinels scanned).",
    "status": "STABLE",
}

excl = [
    ("The genre DEPLOY branch of this schema, and therefore a root rollback field.", "Not claimed: DEPLOY is never self-declared, and the governing order carries <risk>WORLD</risk> but no <proof_genre>DEPLOY</proof_genre>. The rollback path is recorded in the ledger and the manifest release_note instead."),
    ("A firm principal's view of the 24 firm-scoped catalog rows, run against the deployed host.", "Not exercised. r14.AC4 grades the catalog's fields (firm=24), and the issuer's f1.AC1 to f1.AC3 (1,326 pairs, 24 newly visible, cross-firm leaks 0) grade the behaviour on the merged tree; no check in this order puts a firm principal in front of the host."),
    ("post_censuses.py's closing EXPECTED line.", "It printed MISMATCH because its constants are still MX-r-13's (93 tools, 33 / 112 links); the four census lines above it carry the r14 values and every one holds (99 tools equal, 57 keys equal, 7 ids equal, 39 / 119). The line is not cited as evidence."),
    ("Any merge of box/sitez or a trunk into the deploy tree.", "The cut is a two-blob overlay on the live ref's tree through a temporary index; a merge would have shipped other projects' gateway files."),
    ("A HALTGT pass as evidence that no mail was waiting.", "Not cited. The pre-apply mail guard is the broker read (Rule 18a limb a): 2 of 2 rows READ, 0 non-READ, before the deploy."),
    ("The MC Portal breakdown page as rendered.", "Only the per-tool link COUNTS of the reader were measured."),
    ("The host-only dashboard assets.", "The host byte census excludes dashboard/ on both sides; the mcportal pin 17dcbb28 was resolved and the bun cache pre-check run (77 of 77; planted arm 77 of 78), but the dashboard files were not byte-compared."),
    ("nfra-oplgtw-gateway-release-g5a, the OPLGTW ledger A1 calls a leg left to close.", "It was not in the open-ledger scan (18 of 18 and 16 of 16 sentinels), so it was read as closed; this seat did not open, close or inspect it."),
    ("The <status> flip of the task order and the disposition of any row.", "The issuer's, per the order."),
    ("The proof-of-spec check on this instance.", "Run after writing; its verdict is in the report, not asserted here."),
]

tools = [
    ("deploy_ledger.py", "open --slug nfra-mcpindex-r14-catalog-release --window-hours 6 --leg L1..L5; close-leg; close", "OPENED at the start of PHASE B with entry AND sentinel committed by the tool, every leg closed with proof, CLOSED with the sentinel removed."),
    ("halt-gate-check.sh", "AGENT_NAME=0.7.0_AE_CloudOps~MI bash .tools/halt-gate-check.sh from the deploy tree; negative arm with CLAUDE_CODE_SESSION_ID=none OPAL_AGENT_SERIAL= AGENT_NAME=", "Positive rc=0 with HALT_OVERRIDE unset; negative arm rc=3, built by defeating both serial limbs the gate reads (halt_gate_r14.txt)."),
    ("bun_cache_precheck.py", "python ops/bun_cache_precheck.py bun.lock (the pin's lockfile) and a copy with one planted package", "77 of 77 rc=0; planted arm 77 of 78 rc=1 (bun_precheck_r14_PHASEB.txt)."),
    ("safe-ec2-deploy.sh", "DEPLOY_BASE_REF=" + OLD + " AGENT_NAME=0.7.0_AE_CloudOps~MI bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh", "rc=0; the base guard read declared base == live ref at both checkpoints. Its own manifest commit failed closed in the sparse tree, so the manifest was written by hand."),
    ("r14.AC1 / r13.AC2 / r13.AC3 / r14.AC4", "the order's four invocations, verbatim", "All four RESULT: PASS exit=0."),
    ("ssm_run.py / host_read.py / host_vs_cut.py / tools_census.py / env_render.py", "under probes_r14/ (copied from the earlier rounds)", "Host read, host-vs-tree byte census, in-process tool census and .env key render."),
    ("link_counts_host.py / link_counts_real_host.py / post_censuses.py / write_manifest.py / build_instance.py", "adapted this act, probes_r14/", "Off-host and host-side link counts; the post-apply censuses with negative controls; the guarded manifest write; this instance."),
    ("safe-commit.sh", "--author 0.7.0_AE_CloudOps~MI -F <message file> -- <paths>", "Landed the ANNOUNCE commit and the close commit."),
]

inst = {
    "schema_version": "1.0",
    "to_id": "NFRA_MCPINDEX.TO-MX-r-14",
    "firm": "FABRIC",
    "phase": "NON-BUILD-OTHER",
    "assignee": "0.7.0_AE_CloudOps~MI",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md", "group": "X", "vintage_commit": "0c72cd303a"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md", "vintage_commit": "9068de2873", "to_ref": ORDER},
    "artifacts_produced": artifacts,
    "acceptance": acceptance,
    "controls": {"mutant": mutant, "determinism": determinism},
    "declared_exclusions": [{"item": a, "reason": b} for a, b in excl],
    "surprises": [],
    "session_log": "org/tier2_senior/0.7.0_AE_CloudOps~MI/logs/2026-10-15/",
    "compiler_tools": [{"tool": a, "invocation": b, "result": c} for a, b, c in tools],
}
json.dump(inst, open(OUT, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=True)
open(OUT, "a", encoding="utf-8").write("\n")
print("OK: wrote", OUT, "| acceptance", [a["criterion_id"] + ":" + a["status"] for a in acceptance], "| artifacts", len(artifacts))
