"""Append the six surprise rows of cell FB-g-3 (ADVI_FIRMBKTS-D1-W26-S1..S6) to INVESTIGATION_v1.md as fenced json blocks."""
import json
import os

CH = os.path.join(os.getcwd(), "org/missions/D8/ADVI/ADVI_FIRMBKTS/surprise-channel/investigations/INVESTIGATION_v1.md")
BASE = "f30d22f82c"
SURF = "2026-10-11T12:36:08Z"
SURFACED_BY = "0.9.0_WK_ADVI_FIRMBKTS~26"
DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
CHECK = DELIV + "/2.0.0_SA_COO~B1/round4/checks/r4_mapping.py"
OWNER = "1.0.0_SA_CTO~DELL1"


def row(n, cls, hazard, one_line, spec, world, evidence, notes, disarm=None):
    r = {
        "id": "ADVI_FIRMBKTS-D1-W26-S%d" % n,
        "project": "ADVI_FIRMBKTS",
        "fabric": "dell1",
        "surfaced_by": SURFACED_BY,
        "surfaced_at": SURF,
        "class": cls,
        "hazard_standing": hazard,
        "one_line": one_line,
        "spec_asserts": spec,
        "world_is": world,
        "grounding": {"status": "GROUNDED", "evidence": evidence},
        "disposition": "UNDER_INVESTIGATION",
        "notes": notes,
    }
    if disarm:
        r["disarm_owner"] = disarm
    return r


rows = [
    row(1, "BLOCKING", "INERT",
        "S10 REWRITES A v3-PLACED ROW THAT THE S5 DIFFERENCE CONTROL FORBIDS TO MOVE: AC1 READS 4 OF 5",
        "Ruling S10 (ROUND_ANALYSIS.round3.md section 2): the one class-grain row with a {partition} token is re-written at "
        "class grain. Check arm S5 (r4_mapping.py structure): every class the previous table placed keeps its disposition, "
        "address and pattern.",
        "opal-data-bd gold/clients/ is MOVE in mapping_v3.json with address s3://opal-data-49financial/advi/49financial/"
        "platinum/clients/{partition}. The S10 rewrite (partition null, address at class grain) changes that placed address, "
        "so S5 reads DISTURBED for this one class and AC1 reads 4 of 5. Keeping the v3 address instead leaves the token that "
        "S10 and arm U5 forbid. The two rulings conflict on this row; the repair applied S10 and did not rule between them.",
        [DELIV + "/mapping_v3.json row opal-data-bd gold/clients/ (MOVE, dest.partition {partition}) @" + BASE,
         CHECK + " structure arm S5 (compares v3 to v4): AC1 output line DISTURBED opal-data-bd gold/clients/",
         DELIV + "/mapping_v4.json row opal-data-bd gold/clients/ (MOVE, partition null, address at class grain)"],
        "Owner " + OWNER + ": rule which of S5 or S10 governs this row, or exempt S10-rewritten rows from the difference "
        "control. The table keeps the S10 rewrite until ruled."),
    row(2, "BLOCKING", "INERT",
        "S7 SKIP FILES CANNOT BE A MARKER ROW WITHOUT A SECOND ROW AT A CLASS KEY: 1,142 performance_dim_SKIP.json OBJECTS "
        "STAY IN THEIR DATE-PARTITION DATA CHILDREN",
        "Ruling S7: *_SKIP.json is a marker by literal tail under ADDENDUM 1 marker_match, and goes to the <tier>_complete "
        "family as a skip kind. Check arm U3: a _SKIP.json tail carries marker_kind skip.",
        "bronze/orion-api/ date partitions hold 1,142 objects named performance_dim_SKIP.json (110 bytes each) at the live "
        "listing of this round. The class-grain marker row bronze/orion-api/ (mapping_v4 row, marker_match completion tails) "
        "already holds that key; a skip row at the same (bucket, prefix) is a duplicate key (arm S2 dup count), and a skip row "
        "per date child would be a second row at each child key. S7 is therefore applied as 0 rows, and the skip objects "
        "remain counted in their date-partition data children. Writers of the skip file: "
        "infra/aws/lambda/inf-pipeline/inf-performance-daily/lambda_function.py:92 and "
        "infra/aws/lambda/inf-pipeline/inf-performance-daily/pull_inflection_performance_dim.py:212.",
        [CHECK + " arm U3 reads 0 skip markers; S2 dup count is 0 by construction",
         "live listing of bronze/orion-api/ (LIST, 17,188 objects): performance_dim_SKIP.json count 1,142, sizes 110",
         "infra/aws/lambda/inf-pipeline/inf-performance-daily/lambda_function.py@" + BASE + ":92"],
        "Owner " + OWNER + ": rule the shape of the skip marker (a per-date skip child, or a split of the class-grain marker "
        "row) because the structure arm forbids a second row at a class key."),
    row(3, "BLOCKING", "INERT",
        "FIVE QA-NAMED ROWS HAVE NO WRITER IN THE PIPELINE CODE: S6 CANNOT SAY qa-tool OR production, AND ARM U4 READS FAIL",
        "Ruling S6: a QA-named feed is QA only if its WRITER is a QA tool, read from the writer, not the name. Arm U4 needs "
        "qa_verdict qa-tool (RETIRE) or production (placed) on every QA-named row.",
        "opal-data-bd qa-scratch/ (4 rows: ds1_run5_log.txt, ds1_run6_log.txt, ds1_validate/, gate2_unit_delta_run7.parquet; "
        "RETIRE from round 1) and opal-data-inf bronze/orion-api/probe/ (1 row) have no writer in infra/, data/, workflows/, "
        "lib/ or .tools/: a grep for the prefix tokens and the object names returns no pipeline hit. Naming them qa-tool "
        "would be a guess from the name, which S6 forbids; naming them production would move round-1 RETIRE rows. The rows "
        "carry qa_verdict unresolved. Arm U4 reads FAIL and AC2 reads 4 of 5.",
        [CHECK + " arm U4 output: QA-NAMED-WITHOUT-WRITER for the five rows",
         "grep of infra/, data/, workflows/, lib/, .tools/ for qa-scratch, ds1_validate, gate2_unit_delta and orion-api/probe @" + BASE + ": 0 pipeline hits"],
        "Owner " + OWNER + ": name the writer of these prefixes, or rule them not QA by writer. The order stays open until then."),
    row(4, "OBSERVATION", "INERT",
        "TWO ROUND-1 PLACED COT CLASSES SHARE ONE DESTINATION: S3 RETURNS BOTH TO PLACEMENT, AND THE SHARED KEYS ARE UNRULED",
        "Ruling S3: a round-1 placed row stays as placed (the copied-unchanged rule wins). Round-2 collision rule 1e: a new "
        "class colliding with a placed class is FAULT until ruled.",
        "opal-data-cot gold/positions_cube/ and gold/timeseries/positions_cube/ are both MOVE in mapping.json (round 1) to "
        "advi/cottonwood/gold/positions_cube/date={D}/data.parquet, with 342 of 342 keys in common. mapping_v2.json and "
        "mapping_v3.json made both FAULT (1e). S3 returns both to their round-1 placement (rulings_applied S3 = 2), so two "
        "placed rows now name the same destination keys.",
        [DELIV + "/mapping.json rows opal-data-cot gold/positions_cube/ and gold/timeseries/positions_cube/ (MOVE) @" + BASE,
         DELIV + "/mapping_v3.json rows of the same prefixes (FAULT, reason overlap 342 of 342)"],
        "Owner " + OWNER + ": rule which of the two classes owns the shared destination, or split it. Not decided here."),
    row(5, "OBSERVATION", "INERT",
        "TWO DATE PARTITIONS AND ONE FOLDER LIVE SINCE THE CENSUS HAVE NO ROW: ADDED UNDER RULE (c), CHILDREN RE-DERIVED FROM THE LIVE LISTING",
        "Ruling S9: a re-grid's child objects sum to its LIVE listing, and both numbers are printed. Ruling (c): a re-grid is per "
        "date partition.",
        "The live listing holds a 2026-10-11 partition in bronze/eclipse_qa/ (884 objects live, 871 in v3) and in "
        "bronze/orion-api/ (17,188 live, 17,170 in v3). Neither partition is in the census or in the v3 children. Five parents "
        "moved since the v3 listing (cot forwardfill realized and transactions, cot silver, eclipse_qa, orion-api) and are flagged "
        "moving true with the two counts. mapping_v4 adds HOME child rows for bronze/eclipse_qa/2026-10-11/ and "
        "bronze/orion-api/2026-10-11/, a FAULT row for the non-date folder bronze/orion-api/2026-10-11/_markers/ (8 objects), "
        "and re-derives 12 child object counts and 1 excluded_markers count from the live listing.",
        [DELIV + "/mapping_v4.json regrids entries with moving true and their moving_reason",
         "live LIST of bronze/eclipse_qa/ and bronze/orion-api/ (LIST calls, listed_at per parent in the regrids entries)"],
        "Owner: issuer 2.0.0_SA_COO~B1 to confirm the added child rows and the moving flags at the round-4 analysis."),
    row(6, "OBSERVATION", "INERT",
        "FORWARDFILL _complete/ MARKERS USE THE TAIL .json: THE GROUP HAS NO NARROWER LITERAL NAME TAIL",
        "Arm U3 and the ruling wording: marker_match is a non-empty list of literal key tails, with no *, ? or bracket.",
        "The ten forwardfill _complete/ groups (bd 4, cot 6) hold one object per date named <date>.json. Every live key in the "
        "ten groups ends .json, so marker_match is ['.json'] in each row. The tail is literal and passes the arms, but it is "
        "broad: any .json placed under a _complete/ prefix would be marked.",
        ["live LIST of the ten _complete/ prefixes (LIST calls, .scratch/live_parents.json): every key ends .json (asserted in the build)",
         DELIV + "/mapping_v4.json rows with state_family bronze_complete and marker_match .json"],
        "Owner: CTO to confirm the .json tail, or to name a finer rule for the forwardfill markers."),
]

text = ""
for r in rows:
    text += "\n```json\n" + json.dumps(r, indent=2, ensure_ascii=True) + "\n```\n"
with open(CH, "a", encoding="utf-8", newline="\n") as fh:
    fh.write(text)
print("APPENDED", len(rows), "rows to", CH)
