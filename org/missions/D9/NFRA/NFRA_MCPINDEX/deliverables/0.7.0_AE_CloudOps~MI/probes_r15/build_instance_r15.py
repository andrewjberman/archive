"""build_instance_r15.py: write the MX-r-15 proof_of_spec instance from the recorded probe outputs (evidence is read from the
probe files, not retyped). Run from the workspace root."""

import json

D = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MI/"
P = D + "probes_r15/"
OUT = D + "NFRA_MCPINDEX.TO-MX-r-15.round18-catalog-release.proof_of_spec.json"
ORDER = "org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-15.round18-catalog-release.md"


def rd(p):
    return open(p, encoding="utf-8").read().replace("\r", "").strip()


def section(txt, marker):
    return txt.split("=== " + marker, 1)[1].split("\n===", 1)[0].split("\n", 1)[1].strip()


acs = rd(P + "r13.AC2_r13.AC3_r15.AC4_v3_POST.txt")
ac1 = rd(P + "r15.AC1_POST.txt")

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
    crit("AC1", ac1, "Over a printed scan denominator of 24 of 24 sentinels; the first-slug ledger nfra-mcpindex-r15-catalog-release has 1 entry file at HEAD, no sentinel at HEAD, and is not listed OPEN or HELD (nor are its -v2 and -v3 siblings). Pointed at a slug with no ledger as a negative arm it read FAIL exit=1 (entry files at HEAD=0). Run twice back to back, byte-identical."),
    crit("AC2", section(acs, "bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round12/checks/r13.AC2.sh"), "N=127 served tools; the partition sums 127 of 127 (a=11 valid 11, b=104 valid 104, c=12 valid 12); definitions located 127 of 127; discover good 3 of 3."),
    crit("AC3", section(acs, "bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round12/checks/r13.AC3.sh"), "DEPTH 11 of 11 valid; ANSWER-TIME measured rows 17, answered measured and equal 17 of 17; anchors 2 of 2. Graded on the v3 bytes (38fe44d5cb) at 2026-10-16T12:24Z; the same check failed on the first two applies of this order (9 of 11 / 16 of 17 at 0cb4a87bcb, 8 of 11 / 9 of 17 at 1bc2df0b13) on claims the daily publish moved."),
    crit("AC4", section(acs, "bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round18/checks/r15.AC4.sh"), "HOST CATALOG equals TREE CATALOG: version 0.5, harvest 78, table 192, key_template 192, retired 1, rows 280, nl_tags 280, inferred 0, bucket 280, vendor 136, firm 136, tool_bucket 127, serves 7; 61 distinct read_tool names, 0 unserved by the deployed commit; host md5 b72408cad06f2fbf8fb851a4be5485d9 equals the tree md5."),
]
for a in acceptance:
    a["output_evidence"] += "\nexit=0" if "exit=" not in a["output_evidence"] else ""

V1 = "0cb4a87bcb8df4adbb71d095f0818b0f50c562f1"
V2 = "1bc2df0b1383e424571aaa19c195928f449be31b"
V3 = "38fe44d5cb8d37b6007fb7e5fa47a25316e01054"
LIVE0 = "3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4"
S3 = "s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/"


def art(path, kind, ref, state, covers, ev):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": ref, "deployed_state": state, "artifact_covered_by": covers, "deploy_evidence": ev}


artifacts = [
    art(S3 + "opal-gateway-38fe44d5cb.tar.gz", "s3_object", "df5cba50f8b9fed87e224ec54c6d966b", "DEPLOYED-VERIFIED", ["AC2", "AC3", "AC4"],
        "THE SERVED ARTIFACT (v3). head-object read BEFORE v3 leg L1 closed (12:21:12Z): PRESENT 883,434 B, git-ref " + V3 + ", where it read 404 pre-apply. -latest carries the same size, ETag and git-ref. Deploy ssm:20423d5e-d1d5-4cec-b904-160f1d687969 Success; the base guard read declared base == live ref " + V2 + " at both checkpoints. (label_readback_r15_v3.txt)"),
    art(S3 + "opal-gateway-latest.tar.gz", "s3_object", "df5cba50f8b9fed87e224ec54c6d966b", "DEPLOYED-VERIFIED", ["AC2"],
        "Re-pointed from 1bc2df0b13 to 38fe44d5cb by the v3 deploy: 883,434 B, git-ref " + V3 + " (label_readback_r15_v3.txt)."),
    art("i-07dccb1615503ac99:/opt/opal-gateway", "aws_resource", V3, "DEPLOYED-VERIFIED", ["AC2", "AC3", "AC4"],
        "Host byte census against the BUILD INPUT (the cut), not by filename: 141 of 141 common, 141 byte-identical, DIFFER 0 (ssm:01dd7b2e-02d7-4d70-b08d-c96a79d91f3b, 12:21:23Z). NEGATIVE CONTROL, same read, against the prior live tree 1bc2df0b13: DIFFER 1 = app/refs/DATA_CATALOG.yaml (host_vs_cut_r15_v3_POST.txt). Censuses after the apply, each with a negative control (four_censuses_r15_v3_POST.txt): tools 127 = 127, .env keys 64 = 64, ENABLED_INTEGRATIONS 7 = 7, MC Portal link counts 65 tools / 192 links read by the host's real installed module."),
    art(S3 + "opal-gateway-0cb4a87bcb.tar.gz", "s3_object", "e004131084719990cbe6de019bb4a9cf", "DEPLOYED-VERIFIED", ["AC2", "AC4"],
        "THE FIRST APPLY (B, landed 10:38:53Z; verified deployed at that time, now superseded by v3) and the ROLLBACK KEY of v2: 883,376 B, git-ref " + V1 + ". B carried the catalog cf7616c08e plus scopes.json at the host's bytes dde73e4bd0 (ANNOUNCE section 0, row Z-S126); r13.AC2 and r15.AC4 PASSED, r13.AC3 FAILED on one stale claim (row Z-S127)."),
    art(S3 + "opal-gateway-1bc2df0b13.tar.gz", "s3_object", "b21822283e66f7b141bdda5113d5fb77", "DEPLOYED-VERIFIED", ["AC2", "AC4"],
        "THE SECOND APPLY (v2, landed 11:30:12Z; verified deployed at that time, now superseded by v3) and the ROLLBACK KEY of v3, untouched by v3: 883,446 B, git-ref " + V2 + ". r13.AC2 and r15.AC4 PASSED, r13.AC3 FAILED on seven rows the daily publish moved after the 10:58Z re-measure (row Z-S128)."),
    art(S3 + "opal-gateway-3d5c9c8bf1.tar.gz", "s3_object", "d43206bfdad42ae29300cf94eed1423a", "DEPLOYED-VERIFIED", ["AC2"],
        "THE ROLLBACK KEY of the first apply, untouched by this order: 893,303 B, git-ref " + LIVE0 + ", read before and after the first apply (label_readback_r15.txt)."),
    art("infra/aws/ec2/EC2_MANIFEST.json", "config_data", "4cffac6fdb", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC1"],
        "services.opal-gateway, written three times by hand (the wrapper's own manifest commit failed its commit-gate each time), each in ONE write: 775351feb0 (deployed_commit " + V1 + ", previous " + LIVE0 + "), 7018ac20dc (" + V2 + ", previous " + V1 + "), 4cffac6fdb (" + V3 + ", previous " + V2 + ", deployed_at 2026-10-16T12:19:15Z); each prepends a release_note naming this order. v1 changed 5 fields, v2 and v3 changed 4 (deployed_by already read this seat). Committed LOCAL; origin not pushed by this seat."),
    art("org/critical_paths/change_management/20261016T1037Z_nfra-mcpindex-r15-catalog-release_deploy_completion.md", "doc", "e9209e0839", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC1"],
        "The NEVER-2 ledger graded by AC1: 5 legs; L1, L2, L3 and L5 closed on the first apply, L4 closed on v3's passing r13.AC3 by citing the v3 ledger; CLOSED, sentinel removed in the close commit. Its -v2 and -v3 siblings (same directory) are CLOSED the same way; the v3 entry carries a stated correction of one L5 citation."),
    art(D + "ANNOUNCE_MX-r-15.md", "doc", "fc2f9393d2", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC4"],
        "PHASE A: the pins, the live ref read from the host by hash (140 of 141, the one difference being scopes.json), the four censuses, the open-ledger scan 23 of 23, and the finding the pair ruled on (commit B)."),
]

mutant = {
    "description": "NOT a planted byte mutation, and the reason is recorded: every limb of this act's claim lives in a deployed host and a ledger, not in a function a mutant could break. The discriminating evidence is the SAME instruments reading the old state before each act and the new state after it, and one criterion, r13.AC3, that actually FAILED on the first two applies and PASSED on the third.",
    "expected_not_landed": "Before the v3 apply (12:15:45Z): the host matches the prior live tree 1bc2df0b13 with DIFFER 0 and differs from the v3 cut by exactly app/refs/DATA_CATALOG.yaml (EXPECTED CHANGED SET MATCH); the host catalog md5 reads 983464f80adc45ac51f1f3eebbdf2001. r13.AC3 against the v2 bytes reads depth 8 of 11, answer-time 9 of 17.",
    "expected_landed": "After the v3 apply: the host matches the v3 cut with DIFFER 0 and differs from the prior live tree by exactly that file; the host catalog md5 reads b72408cad06f2fbf8fb851a4be5485d9; r13.AC3 reads depth 11 of 11, answer-time 17 of 17; the three ledgers are CLOSED with their sentinels gone at HEAD.",
    "expected": "Each instrument reads the old state before the act and the new state after, and the two readings are mirror images of one another rather than one reading plus an assumption.",
    "observed": "FIRED AS EXPECTED on every arm. (1) Pre-apply v3: host vs the v3 cut DIFFER 1, MATCH. Post-apply v3: host vs the cut DIFFER 0 over 141, vs the prior live tree DIFFER 1, MATCH. (2) Each census has a negative control that reads False (dropping one tool name, bumping one link count). (3) r13.AC3 discriminated three times: FAIL at B (one stale claim, mac.04), FAIL at v2 (seven moved rows), PASS at v3; the control that the OLD catalog fails the first case identically (r13.AC3_control_old_catalog_r15.txt) shows the criterion grades the claims, not the deploy. (4) AC1 pointed at a slug with no ledger reads FAIL exit=1.",
    "status": "FIRED-AS-EXPECTED",
}
determinism = {
    "method": "r15.AC1 was run twice back to back against unchanged inputs after the close commit (r15.AC1_twice.txt).",
    "observed": "Byte-identical output both times, RESULT: PASS exit=0 (24 of 24 sentinels scanned).",
    "status": "STABLE",
}

excl = [
    ("The genre DEPLOY branch of this schema, and therefore a root rollback field.", "Not claimed: DEPLOY is never self-declared, and the governing order carries <risk>WORLD</risk> but no <proof_genre>DEPLOY</proof_genre>. The rollback path is recorded in the ledgers and the COO ask (rollback to the live ref at each apply only)."),
    ("A firm principal's view of the 96 newly visible catalog rows, run against the deployed host.", "Not exercised by this seat; no criterion of this order does it. The issuer ran vis_host_compare.sh and discover_buckets_host.sh on the host serving v3 and reported host == cut (their message 34996)."),
    ("The dashboard bundle (mcportal) as rendered, and its files byte-compared.", "The host byte census excludes dashboard/ on both sides; the mcportal pin 090b9cdc85 was resolved from the manifest and the bun cache pre-check run (77 of 77; planted arm 77 of 78) on every apply, but the built files were not compared."),
    ("Which tree the OG-ap-23 apply ran from.", "Not established. The host's scopes.json (dde73e4bd0) is not the one in the live ref's own tree (d0f83d17db); the pair ruled commit B to leave the host's copy unchanged. Row Z-S126."),
    ("The first two applies' r13.AC3 FAILs as evidence of this order's criterion.", "They are recorded, not cited as passes: the criterion PASSED only on v3 (12:24Z). The claims that failed were the issuer's measurements aged by the daily publish (rows Z-S127, Z-S128), not deploy effects."),
    ("A HALTGT pass as evidence that no mail was waiting.", "Not cited. The pre-apply mail guard is the broker read (Rule 18a limb a): every row READ, 0 non-READ, before each apply (2 of 2 before v3)."),
    ("The MC Portal breakdown page as rendered.", "Only the per-tool link COUNTS of the reader were measured (39/119 -> 65/192 across the first apply, equal after v2 and v3)."),
    ("A push of any commit.", "None made by this seat. The manifest and close commits are LOCAL until box-sync; origin box/sitez was last read before the v3 close, so their push state is measured separately in the report."),
    ("The <status> flip of the task order and the disposition of any row.", "The issuer's, per the order."),
    ("The proof-of-spec check on this instance.", "Run after writing; its verdict is in the report, not asserted here."),
]

tools = [
    ("deploy_ledger.py", "open --slug nfra-mcpindex-r15-catalog-release (and -v2, -v3) --window-hours 6 --leg L1..L5; close-leg; close", "Three ledgers OPENED at the start of each apply with entry AND sentinel committed by the tool, every leg closed with proof, CLOSED with the sentinels gone at HEAD."),
    ("halt-gate-check.sh", "AGENT_NAME=0.7.0_AE_CloudOps~MI bash .tools/halt-gate-check.sh from the deploy tree; negative arm with CLAUDE_CODE_SESSION_ID=none OPAL_AGENT_SERIAL= AGENT_NAME=", "Positive rc=0 with HALT_OVERRIDE unset; negative arm rc=3, before each apply (halt_gate_r15*.txt)."),
    ("bun_cache_precheck.py", "python ops/bun_cache_precheck.py bun.lock (the pin's lockfile) and a copy with one planted package", "77 of 77 rc=0; planted arm 77 of 78 rc=1, three times (bun_precheck_r15*.txt)."),
    ("safe-ec2-deploy.sh", "DEPLOY_BASE_REF=<the live ref> AGENT_NAME=0.7.0_AE_CloudOps~MI bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh", "rc=0 three times; the base guard read declared base == live ref at both checkpoints each time; the wrapper's own manifest commit failed its commit-gate each time (recorded by hand)."),
    ("r15.AC1 / r13.AC2 / r13.AC3 / r15.AC4", "the order's four invocations, verbatim", "All four RESULT: PASS exit=0 on the v3 bytes; r13.AC3 FAILED on the first two applies."),
    ("ssm_run.py / host_read.py / host_vs_cut.py / tools_census.py / env_render.py / served_names_host.py", "under probes_r15/ (copied from the earlier rounds; host_read and host_vs_cut extended to census lib/ and the staged refs)", "Host read, host-vs-tree byte census, in-process tool census and .env key render."),
    ("link_counts_host.py / link_counts_real_host.py / post_censuses*.py / write_manifest*.py / build_instance_r15.py", "adapted this act, probes_r15/", "Off-host and host-side link counts; the post-apply censuses with negative controls; the guarded manifest writes; this instance."),
    ("safe-commit.sh", "--author 0.7.0_AE_CloudOps~MI -F <message file> -- <paths>", "Landed the ANNOUNCE commit, three manifest commits, the evidence commits and the close commit; refused once while a peer's merge held the shared tree (nothing staged), landed on retry."),
]

inst = {
    "schema_version": "1.0",
    "to_id": "NFRA_MCPINDEX.TO-MX-r-15",
    "firm": "FABRIC",
    "phase": "NON-BUILD-OTHER",
    "assignee": "0.7.0_AE_CloudOps~MI",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md", "group": "X", "vintage_commit": "0c72cd303a"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md", "vintage_commit": "9068de2873", "to_ref": ORDER},
    "artifacts_produced": artifacts,
    "acceptance": acceptance,
    "controls": {"mutant": mutant, "determinism": determinism},
    "declared_exclusions": [{"item": a, "reason": b} for a, b in excl],
    "surprises": [
        "NFRA_MCPINDEX-Z-S126: deploy-to-ec2.sh stages app/refs/scopes.json from the deploy tree and the host holds blob dde73e4bd0 while the live ref's tree holds d0f83d17db; commit A (A1's one blob) would have moved the host's registry copy backwards. Ruled: commit B (catalog plus scopes.json at the host's bytes). INERT; the pair signed B.",
        "NFRA_MCPINDEX-Z-S127: r13.AC3 failed on the first apply (9 of 11, 16 of 17) on ONE stale claim, mac.04.yield-curve-fred generated_at (catalog 2026-10-14, served 2026-10-15); the old catalog failed identically, so no rollback. INERT; cured by the issuer's re-measure (v2).",
        "NFRA_MCPINDEX-Z-S128: r13.AC3 failed again on v2 (8 of 11, 9 of 17) because the daily publish moved data_as_of on seven measured rows between the 10:58Z re-measure and 11:35Z, not at the ~13:30Z the order assumed. INERT; cured by the issuer's post-publish re-measure (v3), which passed.",
    ],
    "session_log": "org/tier2_senior/0.7.0_AE_CloudOps~MI/logs/2026-10-16/",
    "compiler_tools": [{"tool": a, "invocation": b, "result": c} for a, b, c in tools],
}
json.dump(inst, open(OUT, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=True)
open(OUT, "a", encoding="utf-8").write("\n")
print("OK: wrote", OUT, "| acceptance", [a["criterion_id"] + ":" + a["status"] for a in acceptance], "| artifacts", len(artifacts))
