"""append_rows.py: append the two MX-r-13 PHASE B rows to the surprise channel file, inside its JSON array.
Reads the file as bytes, validates the existing array parses, inserts before the closing bracket, validates again."""

import json
import sys
import time

F = "org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md"
now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
P = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MI/probes_r13/"

rows = [
    {
        "project": "NFRA_MCPINDEX",
        "fabric": "site-z",
        "surfaced_by": "0.7.0_AE_CloudOps~MI",
        "surfaced_at": now,
        "disarm_owner": "2.0.0_SA_COO~MI",
        "disposition": "UNDER_INVESTIGATION",
        "id": "NFRA_MCPINDEX-Z-S118",
        "one_line": "MX-r-13 PHASE B: the deployed cut d020bee315 failed r13.AC2 (index rc=1: 5 index-named tools carry no depth claim, 2 tools have no definition), so the release was rolled back to ee23dd004c as both signed halves direct.",
        "spec_asserts": "NEVER_WIDEN_ASK_MX-r-13_20261015.md section 3: 'Any other read-back fails -> redeploy ee23dd004c, plus a BLOCKING row. Never roll back past ee23dd004c.' TO-MX-r-13 r13.AC2 expect: 'PARTITION sums N of N, every member valid (index rc=0), and discover reads good 3 of 3'.",
        "world_is": "On the deployed cut (host bytes 118 of 118 equal to d020bee315, 06:38Z) r13.AC2 read: PARTITION a=11 (index named, valid 6; depth claim 6; freshness claim 11) b=70 (valid 70) c=12 (valid 12); sum 93 of N=93; definitions located 91 of 93; duplicates 0; entries naming an unserved tool 0; row identity in tool_index 0; RC index=1; discover good 3 of 3, RC discover=0. The 7 MISSING lines: gateway_query_catalog, opal_asker_query, schwab_describe_dataset, schwab_list_files, schwab_query (member a, link=1 depth=0 fresh=1 def=1: no depth claim) and opal_describe, opal_discover (member b, owner NFRA_MCPINDEX, def=0: no definition). Re-run untruncated at 06:4xZ: identical. r13.AC3 PASS (11 of 11, 17 of 17, anchors 2 of 2) and r13.AC4 PASS (0.5/78/216/216/5, md5 equal, no unserved read_tool) on the same bytes; the four censuses held (tools 93, keys 57, ids 7, links 33/112). Rolled back 06:46Z: host bytes 118 of 118 equal to ee23dd004c, /health 200, links 11/14, keys 57, tools 93.",
        "class": "BLOCKING",
        "hazard_standing": "INERT",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                P + "r13.AC2_AC3_AC4_POST.txt (the three checks on the deployed cut)",
                P + "r13.AC2_POST_wide.txt (AC2 re-run with untruncated lines, same 7 MISSING)",
                P + "host_vs_cut_r13_POST.txt (118 of 118 equal to the cut; DIFFER 2 against the live tree)",
                P + "label_readback_r13_ROLLBACK.txt and host_vs_base_r13_ROLLBACK.txt (the rollback, 118 of 118 equal to ee23dd004c)",
            ],
        },
        "notes": "The signed halves covered this branch; the rollback used the rollback tree C:/tmp/mx-dep-r13-rb at ee23dd004c. The next cut needs the five depth claims and the two definitions in the catalog, or an AC2 that does not grade them; that is the issuer's call.",
    },
    {
        "project": "NFRA_MCPINDEX",
        "fabric": "site-z",
        "surfaced_by": "0.7.0_AE_CloudOps~MI",
        "surfaced_at": now,
        "disarm_owner": "2.0.0_SA_COO~MI",
        "disposition": "UNDER_INVESTIGATION",
        "id": "NFRA_MCPINDEX-Z-S119",
        "one_line": "r13.AC2 FAILS on the live base ee23dd004c itself (partition sums 67 of N=93; 26 served tools are in no catalog member), though the order records it as a live regression guard that PASSES on the host.",
        "spec_asserts": "TO-MX-r-13 ISSUER NOTES: 'r13.AC2 a live regression guard, PASS on the host now'; A3: 'Base dry-runs 2026-10-15: AC1 FAIL (no entry), AC2 live guard PASS'.",
        "world_is": "After the rollback to ee23dd004c (host bytes 118 of 118 equal to that tree, /health 200, 06:5xZ) r13.AC2 read: PARTITION a=11 (valid 11; depth 11; freshness 11) b=44 (valid 44) c=12 (valid 12); sum 67 of N=93; definitions located 57 of 93; RC index=1; discover good 3 of 3. The MISSING lines open with harvest_get_article, harvest_get_chatter, harvest_get_filing_analysis, harvest_get_fundamentals, harvest_get_peers_and_scores, harvest_get_research, harvest_list, harvest_query_columns, harvest_read, harvest_resolve_security (member=none), i.e. tools OG-ap-18 and OG-ap-19 put live. The host base has been ee23dd004c since 04:23Z, so the issuer's PASS reading does not reproduce on the same bytes. I did not establish what the dry-run ran against.",
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                P + "r13.AC2_ROLLBACK.txt (AC2 on the rolled-back host)",
                P + "host_vs_base_r13_ROLLBACK.txt (host equals ee23dd004c, DIFFER 0)",
                "org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-13.depth-every-tool-release.md (ISSUER NOTES and A3)",
            ],
        },
        "notes": "Against the cut the same check sums 93 of 93, so the release closes 26 of the 33 gaps the base has; 7 remain (row Z-S118).",
    },
]

b = open(F, "rb").read()
crlf = b"\r\n" in b
text = b.decode("utf-8")
nl = "\r\n" if crlf else "\n"
tail = nl + "]" + nl + "```"
i = text.rstrip().rfind(tail)
assert i > 0 and text.rstrip().endswith(tail), "unexpected file tail"
head = text[:i]
body = head[head.index("```json") + len("```json"):] if "```json" in head else None
start = head.rfind("```json")
before = json.loads(head[start + len("```json"):] + nl + "]")
assert isinstance(before, list) and before, "array did not parse"
add = "".join("," + nl + "  " + json.dumps(r, indent=2, ensure_ascii=True).replace("\n", nl + "  ") for r in rows)
new = head + add + tail + text.rstrip()[i + len(tail):] + (nl if text.endswith(nl) else "")
after = json.loads(new[new.rfind("```json") + len("```json"):new.rstrip().rfind("```")])
assert len(after) == len(before) + len(rows), (len(before), len(after))
open(F, "wb").write(new.encode("utf-8"))
print("OK: appended %d rows; array %d -> %d; crlf=%s; ids %s" % (len(rows), len(before), len(after), crlf, [r["id"] for r in rows]))
sys.exit(0)
