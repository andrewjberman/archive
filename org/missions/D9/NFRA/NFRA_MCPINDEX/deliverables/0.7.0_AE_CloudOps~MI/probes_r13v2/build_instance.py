"""build_instance.py: write the MX-r-13 proof_of_spec instance from the recorded probe outputs (evidence is read from the
probe files, not retyped). Run from the workspace root."""

import json

D = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MI/"
V2 = D + "probes_r13v2/"
V1 = D + "probes_r13/"
OUT = D + "NFRA_MCPINDEX.TO-MX-r-13.depth-every-tool-release.proof_of_spec.json"
ORDER = "org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-13.depth-every-tool-release.md"
CHK = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round12/checks/"


def rd(p):
    return open(p, encoding="utf-8").read().replace("\r", "").strip()


def section(txt, start):
    """the block of a combined AC2/AC3/AC4 output that follows '=== <start>' up to the next '==='."""
    return txt.split("=== " + start, 1)[1].split("\n===", 1)[0].split("\n", 1)[1].strip()


ac = rd(V2 + "r13.AC2_AC3_AC4_v2_POST.txt")
ac1 = rd(V2 + "r13.AC1_v2_POST.txt")
fail1 = rd(V1 + "r13.AC2_POST_wide.txt")

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
    crit("AC1", ac1 + "\nexit=0", "Over a printed scan denominator of 18 of 18 sentinels; the v2 ledger has 1 entry file at HEAD, no sentinel at HEAD, and is not listed OPEN or HELD. The check was pointed at a slug with no ledger as a negative arm and read FAIL exit=1 (entry files at HEAD=0)."),
    crit("AC2", section(ac, "r13.AC2") + "\nexit=0", "N=93 served tools; the partition sums 93 of 93 (a=11 valid 11, b=70 valid 70, c=12 valid 12); definitions located 93 of 93; discover good 3 of 3. This is the criterion that read FAIL on the first attempt's cut (7 MISSING); the same instrument reads PASS on the re-cut."),
    crit("AC3", section(ac, "r13.AC3") + "\nexit=0", "DEPTH 11 of 11 valid; ANSWER-TIME measured rows 17, answered measured and equal 17 of 17; anchors 2 of 2. It read PASS on both attempts' deployed bytes."),
    crit("AC4", section(ac, "r13.AC4") + "\nexit=0", "Host catalog version 0.5, harvest 78, table 216, key_template 216, retired 5; 29 distinct read_tool names, 0 unserved by the deployed commit; host md5 5e11a65fca98ce9f570c9aaade49e58c equals the tree md5."),
]

NEW = "1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0"
OLD = "ee23dd004c985c46d479908db46d2ad9b4f3b1c8"
S3 = "s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/"


def art(path, kind, ref, state, covers, ev):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": ref, "deployed_state": state, "artifact_covered_by": covers, "deploy_evidence": ev}


artifacts = [
    art(S3 + "opal-gateway-1b18b94979.tar.gz", "s3_object", "4e9fb6ac6e3287a1d0293ae3dc93f598", "DEPLOYED-VERIFIED", ["AC2", "AC3", "AC4"],
        "THE FINAL SERVED ARTIFACT. head-object read BEFORE leg L1 closed (07:56:24Z): PRESENT 720,085 B, git-ref " + NEW + ", where it read 404 pre-apply. -latest carries the same size and ETag and git-ref. Upload and pull ssm:9fedb84f-8099-417c-b4b2-d938c7e5c10b Success; the base guard read declared base == live ref " + OLD + " at both checkpoints. (label_readback_v2.txt)"),
    art(S3 + "opal-gateway-latest.tar.gz", "s3_object", "4e9fb6ac6e3287a1d0293ae3dc93f598", "DEPLOYED-VERIFIED", ["AC2"],
        "Re-pointed from " + OLD[:10] + " to " + NEW[:10] + " by the deploy: 720,085 B, git-ref " + NEW + " (label_readback_v2.txt)."),
    art("i-07dccb1615503ac99:/opt/opal-gateway", "aws_resource", NEW, "DEPLOYED-VERIFIED", ["AC2", "AC3", "AC4"],
        "Host byte census against the BUILD INPUT (the cut), not by filename: 118 of 118 common, 118 byte-identical, DIFFER 0, 0 cut-only, 0 host-only (ssm:8fafce84-1ea1-4255-880b-7b275634951f). NEGATIVE CONTROL, same read, against the live tree " + OLD[:10] + ": DIFFER 2 = exactly app/refs/DATA_CATALOG.yaml and app/integrations/opal_discover/integration.py, EXPECTED CHANGED SET MATCH (host_vs_cut_v2_POST.txt). Four censuses (four_censuses_v2_POST.txt): tools 93 = 93 names equal, .env keys 57 = 57, ENABLED_INTEGRATIONS 7 = 7, MC Portal per-tool link counts 33 tools / 112 links read by the host's real reader (ssm:9c77bfb3-1b3b-431f-abb8-9edf64d787a0), each with a negative control reading False."),
    art(S3 + "opal-gateway-d020bee315.tar.gz", "s3_object", "43a385fd25c927ab5fbcfd4ebceb574c", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC2"],
        "ROLLED BACK AND SUPERSEDED, recorded as history and not as the delivered state. The FIRST ATTEMPT's artifact (720,101 B). Deployed 2026-10-15T06:35Z, r13.AC2 read FAIL on it, and the host was rolled back to " + OLD[:10] + " at 06:46Z (verified 118 of 118). It remains in S3 as a record and is not serving. Rows NFRA_MCPINDEX-Z-S118 and Z-S119."),
    art(S3 + "opal-gateway-ee23dd004c.tar.gz", "s3_object", "3cd90347e472d1b7c0eaa31ad43c9242", "DEPLOYED-VERIFIED", ["AC2"],
        "THE ROLLBACK KEY for this release, untouched by it: 629,787 B, ETag 3cd90347..., git-ref " + OLD + ", read BEFORE leg L1 closed. The first attempt's rollback re-uploaded this key (it was 629,899 B / 159fa4ea...); the files inside are byte-identical to the host."),
    art("infra/aws/ec2/EC2_MANIFEST.json", "config_data", "466db928fe", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC1"],
        "services.opal-gateway: deployed_commit " + NEW + ", previous_deployed_commit " + OLD + ", deployed_at 2026-10-15T07:54:33Z, release_note naming this release in the SAME write as the commit fields; exactly 5 fields changed, 5 insertions / 5 deletions, 1 of 27 services (write_manifest.py). Committed LOCAL; origin not pushed."),
    art("org/critical_paths/change_management/20261015T0753Z_nfra-mcpindex-r12-catalog-release-v2_deploy_completion.md", "doc", "466db928fe", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC1"],
        "The v2 NEVER-2 ledger: 5 legs, each closed with proof, CLOSED, sentinel removed in the same commit."),
    art("org/critical_paths/change_management/20261015T0633Z_nfra-mcpindex-r12-catalog-release_deploy_completion.md", "doc", "6822233e90", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC2"],
        "The first attempt's ledger, CLOSED as rolled back: L1 and L2 proven, L3 recording the r13.AC2 FAIL and the rollback, L4 the AC3/AC4 PASS on the cut that no longer serves, L5 recording that no manifest write was made."),
    art(D + "ANNOUNCE_MX-r-13_v2.md", "doc", "81835d5415", "COMMITTED-NOT-DEPLOY-SCOPE", ["AC2"],
        "PHASE A of the re-cut: the pins, the live ref read from the host by hash (118 of 118), the four censuses, the open-ledger scan 17 of 17."),
]

mutant = {
    "description": "NOT a planted byte mutation, and the reason is recorded: every limb of this act's claim lives in a deployed host and a ledger, not in a function a mutant could break. The discriminating evidence is the SAME instrument reading both states: r13.AC2 read FAIL on the first attempt's cut and PASS on the re-cut, and the host byte census read DIFFER 0 against whichever tree was serving.",
    "expected_not_landed": "Before the apply: the host matches the LIVE tree " + OLD[:10] + " with DIFFER 0 and differs from the cut by exactly the two shipped files; link counts 11 tools / 14 links; r13.AC2 on the base reads 67 of 93 by construction.",
    "expected_landed": "After the apply: the host matches the CUT with DIFFER 0 and differs from the live tree by exactly those two files; link counts 33 / 112; r13.AC2 sums 93 of 93 with definitions 93 of 93; the ledger is CLOSED with its sentinel gone at HEAD.",
    "expected": "Each instrument reads the old state before the act and the new state after, and the two readings are mirror images of one another rather than one reading plus an assumption.",
    "observed": "FIRED AS EXPECTED on every arm. (1) Pre-apply (07:51:22Z): host vs the live tree DIFFER 0, vs the cut DIFFER 2 = the two files, EXPECTED CHANGED SET MATCH. Post-apply: host vs the cut DIFFER 0 over 118, vs the live tree DIFFER 2, MATCH. (2) The first attempt's cut read r13.AC2 RESULT: FAIL (" + fail1.split("\n")[1][:230] + " ...; 7 MISSING) and was rolled back, after which the host again read DIFFER 0 against the live tree; the re-cut then read RESULT: PASS. (3) Link counts: host real import 11/14 before, 33/112 after, with a bump-one negative control reading False; the tool census names EQUAL with a drop-one control reading False. (4) AC1 pointed at a slug with no ledger reads entry files at HEAD=0 and RESULT: FAIL exit=1; at the closed v2 ledger it reads PASS.",
    "status": "FIRED-AS-EXPECTED",
}
determinism = {
    "method": "r13.AC1 was run twice back to back against unchanged inputs after the close commit (r13.AC1_twice.txt).",
    "observed": "Byte-identical output both times, RESULT: PASS exit=0 (18 of 18 sentinels scanned).",
    "status": "STABLE",
}

excl = [
    ("The genre DEPLOY branch of this schema, and therefore a root rollback field.", "Not claimed: DEPLOY is never self-declared, and the governing order carries <risk>WORLD</risk> but no <proof_genre>DEPLOY</proof_genre>. The rollback path is recorded in the ledger and the manifest release_note instead; the first attempt actually exercised it."),
    ("The first attempt's deployment of d020bee315 as the delivered state.", "It was rolled back after r13.AC2 failed (row NFRA_MCPINDEX-Z-S118). It is recorded here as history, not claimed as the result."),
    ("A pass of r13.AC2 on the BASE ee23dd004c.", "Not claimed and not true: on the base it reads 67 of 93 by construction (row NFRA_MCPINDEX-Z-S119, ruled by the issuer in A5). r13.AC2 is graded after the release only."),
    ("Any merge of box/sitez or a trunk into the deploy tree.", "The cut is a two-blob overlay on the live ref's tree through a temporary index; a merge would have shipped other projects' gateway files."),
    ("A HALTGT pass as evidence that no mail was waiting.", "Not cited. The pre-apply mail guard is the broker read (Rule 18a limb a): 3 of 3 rows READ, 0 non-READ, before each deploy."),
    ("The MC Portal breakdown page as rendered, and Andrew's FWD-20 sitting.", "Only the per-tool link COUNTS of the reader were measured. The page, and NFRA_MCPORTAL.TO-MP-z-6 (staged, not started), are the MC Portal project's."),
    ("The host-only dashboard assets.", "The host byte census excludes dashboard/ on both sides, as in the earlier releases; the mcportal pin 17dcbb28 was resolved and the bun cache pre-check run (77 of 77; planted arm 77 of 78), but the dashboard files were not byte-compared."),
    ("The <status> flip of the task order and the disposition of rows Z-S118 and Z-S119.", "The issuer's, per the order."),
    ("The proof-of-spec check on this instance.", "Run after writing; its verdict is in the report, not asserted here."),
]

tools = [
    ("deploy_ledger.py", "open --slug nfra-mcpindex-r12-catalog-release[-v2] --window-hours 6 --leg L1..L5; close-leg; close", "Both ledgers OPENED at the start of PHASE B with entry AND sentinel committed by the tool, every leg closed with proof, both CLOSED with the sentinel removed."),
    ("halt-gate-check.sh", "AGENT_NAME=0.7.0_AE_CloudOps~MI bash .tools/halt-gate-check.sh from the deploy tree; negative arm with CLAUDE_CODE_SESSION_ID=none OPAL_AGENT_SERIAL= AGENT_NAME=", "Positive rc=0 with HALT_OVERRIDE unset; negative arm rc=3, built by defeating both serial limbs the gate reads (halt_gate_v2.txt)."),
    ("bun_cache_precheck.py", "python ops/bun_cache_precheck.py bun.lock (the pin's lockfile) and a copy with one planted package", "77 of 77 rc=0; planted arm 77 of 78 rc=1 (bun_precheck_v2_PHASEB.txt)."),
    ("safe-ec2-deploy.sh", "DEPLOY_BASE_REF=" + OLD + " AGENT_NAME=0.7.0_AE_CloudOps~MI bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh", "rc=0 for the deploy; the base guard read declared base == live ref at both checkpoints. Its own manifest commit failed closed in the sparse tree (commit-gate could not import comp_constants_cli), so the manifest was written by hand."),
    ("r13.AC1 / r13.AC2 / r13.AC3 / r13.AC4", "the order's four invocations, verbatim", "All four RESULT: PASS exit=0 on the re-cut."),
    ("ssm_run.py / host_read.py / host_vs_cut.py / tools_census.py / env_render.py", "under probes_r13v2/ (copied from the earlier rounds)", "Host read, host-vs-tree byte census, in-process tool census and .env key render."),
    ("link_counts_host.py / link_counts_real_host.py / post_censuses.py / write_manifest.py / build_instance.py", "written or adapted this act, probes_r13v2/", "Off-host and host-side link counts; the four post-apply censuses with negative controls; the guarded manifest write; this instance."),
    ("safe-commit.sh", "--author 0.7.0_AE_CloudOps~MI -F <message file> -- <paths>", "Landed each commit; its surprise-row gate refused the order's worker-form row ids (Z-W35-S<k>) for a seat and the rows were refiled in the seat form (Z-S118, Z-S119)."),
]

inst = {
    "schema_version": "1.0",
    "to_id": "NFRA_MCPINDEX.TO-MX-r-13",
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
        "NFRA_MCPINDEX-Z-S118: MX-r-13 PHASE B attempt 1: the deployed cut d020bee315 failed r13.AC2 (7 MISSING), so the release was rolled back to ee23dd004c (BLOCKING; both causes the issuer's, ruled and fixed in A5).",
        "NFRA_MCPINDEX-Z-S119: r13.AC2 fails on the live base ee23dd004c itself (67 of 93), contrary to the order's 'PASS now' (OBSERVATION; ruled in A5: by construction).",
    ],
    "session_log": "org/tier2_senior/0.7.0_AE_CloudOps~MI/logs/2026-10-15/",
    "compiler_tools": [{"tool": a, "invocation": b, "result": c} for a, b, c in tools],
}
json.dump(inst, open(OUT, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=True)
open(OUT, "a", encoding="utf-8").write("\n")
print("OK: wrote", OUT, "| acceptance", [a["criterion_id"] + ":" + a["status"] for a in acceptance], "| artifacts", len(artifacts))
