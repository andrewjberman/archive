#!/usr/bin/env python3
"""Build the L0 GRAPH SUBSTRATE MANIFEST for SC-m-3 (TO-W1-DTX).

Emits a manifest conforming to org/standards/L0_GRAPH_SUBSTRATE_MANIFEST.schema.json
(top-level additionalProperties:False, 5 keys; parts additionalProperties:False, 12 required).

The Rule 24 record, findings, C3-chain status and instrument-trap disclosures do NOT fit
that contract's closed top level and live in the COMPANION file beside it -- which TO s.8
explicitly permits ("in the manifest or beside it").

DTX-AC5: this script is an instrument for producing the MANIFEST. It is not a graph
materializer, is not a part registered below, and touches no store or generator.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "graph_object_manifest.json")

COMPILED_UTC = "2026-08-26T19:33:00Z"   # clock read in-session, never estimated
COMMIT_ISH = "14da312322"               # HEAD when the tree was read; NOT back-dated to the wave anchor
WH = "s3://opal-313476888478-globgrph/warehouse/globgrph/"

DERIVE = "infra/aws/globgrph/derive_runner.py"
LAMBDA_WRITER = "infra/aws/lambda/globgrph/incremental_updater/lambda_function.py"
FULL_EXTRACTOR = "org/modules/graph/comp_aws_cli.py"
S3_EV = "aws s3api list-objects-v2, full pagination, max(LastModified) computed client-side over the MATERIALISED set"
STAT_EV = "stat -c %s/%Y + git ls-files/check-ignore, read at HEAD 14da312322"


def wh(tbl_dir):
    return WH + tbl_dir + "/"


def part(id, part_class, home, authority_role, temporal_claim, projection_of, source_identity,
         materializer, standing, declared_opinions, cadence, trigger, population_status,
         measured_utc, method, basis, evidence, owner, age_note=None, coverage=None,
         consumers=None, digest=None):
    p = {
        "id": id,
        "part_class": part_class,
        "home": home,
        "authority_role": authority_role,
        "temporal_claim": temporal_claim,
        "lineage": {"projection_of": projection_of, "source_identity": source_identity},
        "generation": {
            "materializer": materializer,
            "materializer_digest": digest,
            "materializer_standing": standing,
            "declared_opinions": declared_opinions,
            "cadence": cadence,
            "trigger": trigger,
        },
        "population_status": population_status,
        "vintage": {"measured_utc": measured_utc, "method": method, "age_note": age_note},
        "basis": basis,
        "evidence": evidence,
        "owner": owner,
    }
    if coverage is not None:
        p["coverage"] = coverage
    if consumers is not None:
        p["consumers"] = consumers
    return p


PARTS = []

# ---------------- WAREHOUSE PLANE: Iceberg/Nessie, the governed store ----------------
PARTS.append(part(
    "graph_nodes", "store", wh("graph_nodes_4c6c23bd-fffa-427e-9cd9-7a9deaa3426d"),
    "source", "current_state", [], "iceberg:graph_nodes",
    DERIVE + " -> " + FULL_EXTRACTOR + " + " + LAMBDA_WRITER, "canonical", None,
    "02:00Z full re-derive + event-driven CloudTrail incremental", "schedule + CloudTrail event",
    "production", "2026-08-26T12:50:48Z", S3_EV, "measured",
    "180,225 objects under the table prefix; newest metadata object 2026-08-26T12:50:48Z. "
    "TWO PRODUCERS write this table (comp-kuzu provenance header), so one incremental row makes "
    "the whole table read as freshly written -- last-write is NOT the age of the data. "
    "⛔ CONFIRMATION STATUS PER WRITER, because the chain notation alone does not carry it "
    "(1.0.0_SA_CTO~X AST join 74385 and their own correction 74403): comp_aws_cli.py is a "
    "CONFIRMED writer BY NAME (overwrite -> graph_nodes AND graph_edges); the incremental "
    "Lambda is a CONFIRMED writer BY NAME (delete, overwrite -> graph_nodes); "
    "derive_runner.py is the ORCHESTRATOR -- source-confirmed at :101 calling "
    "comp_aws_cli.cmd_derive -- and its OWN direct write to these tables is NOT CONFIRMED. "
    "The evidence first cited for it (:625) was WITHDRAWN by its author within 12 minutes as "
    "a MARK-AND-SWEEP READ PATH, a garbage collector loading the tables to compare metadata "
    "locations. Re-read at this seat: :625-631 builds a `live` set from "
    "catalog.load_table(...).metadata_location -- a READ. So this row names a CHAIN, and only "
    "TWO of its three members are name-confirmed writers. "
    "CORRECTION OF RECORD, source-confirmed after 1.0.0_SA_CTO~X 74284: my first cut named "
    "kuzu_incremental_refresh.py as the second producer. IT IS NOT A PRODUCER OF THIS TABLE -- its "
    ":65 reads the HEAD Iceberg graph_nodes/graph_edges and its :123 _apply_node_upsert writes the "
    "KUZU PROJECTION. IT IS A CONSUMER. The real second writer is the Lambda named above, whose own "
    "header reads 'pyiceberg upsert into graph_nodes / graph_edges ... ONE Nessie commit per SQS "
    "batch', triggered by opal-globgrph-cloudtrail-mgmt -> SQS. I KNEW THERE WERE TWO PRODUCERS -- "
    "the provenance header says so and I quoted it -- AND I MATCHED THE WORD 'incremental' IN A "
    "FILENAME TO THE HEADER'S PHRASE 'event-driven CloudTrail incremental'. A fourth name-based "
    "inference, on the two most load-bearing parts in the estate.",
    "0.8.0_AE_CloudComp lane (derive path)",
    age_note="180,225 objects for a 27,035-node table: heavy small-file accumulation. Observation, not chased.",
    coverage={"population": "the canonical node set", "denominator": "27,035 nodes at the wave projection vintage (PROJECTION plane, not warehouse)"},
    consumers=["kuzu_nessie_load.py", "comp-kuzu", "comp-blast"]))

PARTS.append(part(
    "graph_edges", "store", wh("graph_edges_6629328d-a582-46d2-80bc-5059de1a77ce"),
    "source", "current_state", [], "iceberg:graph_edges",
    DERIVE + " -> " + FULL_EXTRACTOR + " + " + LAMBDA_WRITER, "canonical", None,
    "nightly re-derive + event-driven CloudTrail incremental", "schedule + SQS", "production",
    "2026-08-26T02:09:51Z", S3_EV, "measured",
    "612 objects; sort_by(LastModified)[-1] on metadata/, single page so no pagination spill",
    "0.8.0_AE_CloudComp lane (derive path)",
    coverage={"population": "the canonical edge set", "denominator": "58,224 edges at the wave projection vintage (PROJECTION plane)"},
    consumers=["kuzu_nessie_load.py", "comp-kuzu"]))

PARTS.append(part(
    "cse", "store", wh("cse_b557721f-8b81-4ec2-9289-fe5f44c3f272"),
    "source", "current_state", [], "iceberg:cse",
    "infra/aws/globgrph/cse_producers_nightly.py + infra/aws/globgrph/cse_emit_agent.py + infra/aws/globgrph/cse_emit_deploy.py + infra/aws/globgrph/cse_emit_frontend_coevolution.py + infra/aws/globgrph/cse_emit_graphhead.py + infra/aws/globgrph/cse_emit_promote.py + infra/aws/globgrph/cse_store.py",
    "canonical", None, "nightly (<26h per the provenance header)", "schedule", "production",
    "2026-08-26T03:31:12Z", S3_EV, "measured",
    "389 objects; corroborated by comp-kuzu provenance header 'cse: last-write 14.8h ago (< 26h cadence)'",
    "0.8.0_AE_CloudComp lane", consumers=["comp-kuzu"]))

PARTS.append(part(
    "resource_summaries", "store", wh("resource_summaries_b38ddc35-944f-4dd4-b801-120e96c6d4cd"),
    "source", "current_state", [], "iceberg:resource_summaries",
    "infra/aws/globgrph/resource_summaries_store.py", "unknown", None, None, None,
    "production", "2026-07-18T21:11:05Z", S3_EV, "measured",
    "71 objects. ROW COUNT DELIBERATELY NOT PUBLISHED HERE -- TO s.7 requires coordination with "
    "0.7.0_AE_CloudOps~X first so one seat measures and the other cites with attribution. The 71 is "
    "an S3 OBJECT count and is explicitly not a row count.",
    "0.7.0_AE_CloudOps~X (card subject)",
    age_note="39 days at carding against a temporal_claim of current_state -- an expressible violation, "
             "recorded rather than resolved.",
    consumers=["comp-kuzu"]))

PARTS.append(part(
    "graph_contracts", "store", wh("graph_contracts_bccbceec-941a-424e-be43-edd7d751a1cf"),
    "source", "current_state", [], "iceberg:graph_contracts",
    None, "unknown", None, None, None, "production", "2026-06-16T18:53:51Z", S3_EV, "measured",
    "21 objects. GENERATOR UNKNOWN: not resolved to a named producer by directory enumeration of "
    "infra/aws/globgrph/ nor by the comp-find DEF-band sweep. RECORDED AS UNKNOWN RATHER THAN "
    "OMITTED (DTX-AC2) -- an omitted row and an unowned row are opposite facts that look identical. "
    "SECOND INSTRUMENT AGREES: comp-kuzu's provenance header independently reports last-write "
    "1703.4h (=70.97d) against my 71d from S3 metadata; writer-stamped marker vs S3 object metadata, "
    "different instruments, same answer.",
    "UNOWNED -- no owner identified; this is the finding",
    age_note="71 days at carding against a temporal_claim of current_state.",
    consumers=["comp-kuzu"]))

for tid, tdir, utc, gen, days in [
    ("ms_heat_snap", "ms_heat_snap_a1875ebc-9d80-4078-b8e7-19e6455265bd", "2026-07-17T18:11:09Z",
     "infra/aws/globgrph/ms_cloud_extract.py", 40),
    ("fedobs_coverage_snap", "fedobs_coverage_snap_a9637eab-f8d2-4421-847c-4a2ca27cdc86",
     "2026-07-16T15:28:07Z", "infra/aws/globgrph/emit_fedobs_snap.py", 41),
    ("fedobs_coevolution_snap", "fedobs_coevolution_snap_499558ba-0181-42ab-a008-93a518692299",
     "2026-07-17T17:43:21Z", "infra/aws/globgrph/cse_emit_frontend_coevolution.py", 40),
    ("code_heat_snap", "code_heat_snap_8b0bca7a-9078-4b8e-8868-ef04062d9952",
     "2026-07-16T15:28:06Z", "infra/aws/globgrph/code_heat_emit.py", 41),
]:
    PARTS.append(part(
        tid, "store", wh(tdir), "evidence", "point_in_time", [], "iceberg:" + tid,
        gen, "unknown", None, None, None, "production", utc, S3_EV, "measured",
        "NOT ON THE STARTING LIST -- found by this census. Generator is INFERRED FROM NAME ADJACENCY "
        "in infra/aws/globgrph/ and is NOT source-confirmed; basis for the generator field alone is "
        "inferred, not measured.",
        "UNKNOWN",
        age_note="%d days at carding; temporal_claim point_in_time, so age is not per se a defect for a snapshot table." % days))

for tid, tdir, utc, nobj in [
    ("cse_test_24458e6c", "cse_test_24458e6c-667c-4e85-ba44-33751795e182", "2026-07-08T15:51:17Z", 57),
    ("cse_test_bb57a916", "cse_test_bb57a916-76de-454d-a71e-932dc173620e", None, 13),
]:
    PARTS.append(part(
        tid, "store", wh(tdir), "evidence", "point_in_time", [], "iceberg:" + tid,
        None, "unknown", None, None, None, "test",
        utc,
        S3_EV if utc else "NOT SEPARATELY PROBED -- the per-table loop resolved only the first "
                          "cse_test_* prefix. STATED AS UNMEASURED RATHER THAN INHERITED FROM ITS SIBLING.",
        # basis describes THE PART, not one field. cse_test_bb57a916 EXISTS (13 objects measured);
        # only its VINTAGE is unprobed, and vintage.measured_utc=null already says so. Using
        # "absent" here would assert the TABLE is absent, which is false -- two different facts
        # sharing one enum value is the exact defect this manifest exists to find.
        "measured",
        "FINDING: A TEST TABLE PERSISTING IN THE GOVERNED PRODUCTION WAREHOUSE (%d objects). "
        "population_status=test is the field that makes this expressible; it exists in the schema "
        "because of this live finding. NOT REMEDIATED -- DTX-AC5 binds." % nobj,
        "cse producer owner -- UNRESOLVED"))

# ---------------- PROJECTION PLANE ----------------
PARTS.append(part(
    "kuzu_nessie_db.local", "projection", "infra/aws/globgrph/kuzu_nessie_db",
    "projection", "current_state", ["graph_nodes", "graph_edges", "cse", "graph_contracts"],
    "kuzu:kuzu_nessie_db@2902399899597701830",
    "infra/aws/globgrph/kuzu_nessie_load.py + infra/aws/globgrph/kuzu_incremental_refresh.py",
    "canonical", None, "rebuilds engine-internally on Nessie-HEAD-advance", "Nessie HEAD advance",
    "production", "2026-08-26T14:07:59Z",
    "comp-kuzu provenance header (built-time + snapshot ids + counts) cross-read against stat mtime",
    "measured",
    "82,567,168 bytes; 27,035 nodes / 58,224 edges; nodes snapshot 2902399899597701830, edges "
    "6557038275462806297; Nessie HEAD current (pin == marker HEAD). UNTRACKED, ignored via "
    "infra/aws/globgrph/.gitignore:3 -- DEVICE-LOCAL, so this row describes THIS DEVICE only.",
    "0.8.0_AE_CloudComp lane (NFRA_KUZUSPLIT)",
    coverage={"population": "the canonical projection of the warehouse graph", "denominator": "27,035 nodes / 58,224 edges at snapshot 2902399899597701830"},
    consumers=["comp-kuzu", "comp-kuzu-full", "comp-kuzu-inc", "comp-blast", "comp_iam_live.py"]))

PARTS.append(part(
    "kuzu_nessie_db.s3", "projection", "s3://opal-estate-report/kuzu_nessie_db",
    "projection", "current_state", ["graph_nodes (INFERRED)", "graph_edges (INFERRED)"],
    "kuzu:estate-report-published",
    "the early-morning Nessie run per infra/aws/terraform/estate-report/instance.tf:136-143",
    "unknown", None,
    "DECLARED daily, overwritten each day (instance.tf:136-138)", "early-morning Nessie run",
    "production", "2026-08-06T21:49:50Z",
    "aws s3api head-object --bucket opal-estate-report --key kuzu_nessie_db; POSITIVE CONTROL "
    "head-object on code/estate_report_runner.py returned a DIFFERENT LastModified, so the probe "
    "discriminates",
    "measured",
    "FINDING -- DESIRED != APPLIED. ContentLength 51,068,928, LastModified 2026-08-06T21:49:50Z, "
    "VersionId 1qzIq4TIzcemaprP8Rqq.3AaYvpnMy2O. instance.tf declares this object published DAILY and "
    "OVERWRITTEN each day; measured age at carding is 20 DAYS. The config's own comment says 'A "
    "MISSING OBJECT MUST READ AS INSTRUMENT_FAILED, NEVER AS no blast radius' -- a 20-day-STALE object "
    "is the case that comment does NOT cover, because it is present and it answers. "
    "NEAR-MISS DISCLOSURE: this part was nearly recorded ABSENT -- comp-keys prefix without --all "
    "showed 40 of 129 keys and this key was past the cut; head-object corrected it. "
    "PER-FIELD BASIS, and the part-level basis field CANNOT express this: EXISTENCE, HOME, SIZE and "
    "VINTAGE are MEASURED (head-object, with a positive control). LINEAGE IS *INFERRED* FROM "
    "instance.tf's PROSE -- I HAVE NEVER OPENED THIS OBJECT and make no claim about its contents or "
    "its generator. Corroborated by 0.8.0_AE_CloudComp~X (73339), who measured the same object "
    "independently and states the same limit. "
    "AND THE TRAP THEY NAMED, which I am recording because it would invert this row's treatment: "
    "LastModified 2026-08-06 makes this look like a STALE COPY of kuzu_nessie_db.local (2026-08-26). "
    "IT IS A DIFFERENT OBJECT, on a different plane, with a different id -- 'stale duplicate' and "
    "'distinct store' take OPPOSITE manifest treatments, and AGE IS THE WRONG AXIS to tell them "
    "apart. The F-1 staleness finding is against this object's OWN DECLARED DAILY CADENCE in "
    "instance.tf, NOT against the local kuzu.",
    "estate-report pipeline owner (0.7.0_AE_CloudOps lane per EC2 ownership)",
    age_note="20 days against a DECLARED DAILY cadence and a temporal_claim of current_state: an "
             "expressible, testable violation of exactly the kind temporal_claim exists to express.",
    consumers=["estate_report_runner.py on the estate-report EC2, resolved via ESTATE_GRAPH_KEY"]))

for pid, home, ig, sz, utc, gen, days, po in [
    ("kuzu_db", "infra/aws/globgrph/kuzu_db", ".gitignore:1", 9224192, "2026-06-12T13:55:12Z",
     "infra/aws/globgrph/kuzu_load.py", 75, "orphaned"),
    ("kuzu_stitch_db", "infra/aws/globgrph/kuzu_stitch_db", ".gitignore:5", 9170944,
     "2026-07-07T15:46:39Z", "infra/aws/globgrph/kuzu_stitch_load.py", 50, "orphaned"),
    ("kuzu_ac7.db", "infra/aws/globgrph/kuzu_ac7.db", "infra/.gitignore:82 (*.db) -- a WIDER rule not written for it",
     4050944, "2026-06-12T14:57:51Z", None, 75, "orphaned"),
]:
    PARTS.append(part(
        pid, "projection", home, "projection", "point_in_time",
        ["stitch_graph.json"] if pid == "kuzu_stitch_db" else [], "kuzu:" + pid,
        gen, "superseded" if pid != "kuzu_ac7.db" else "unknown", None, None, None,
        po, utc, STAT_EV, "measured",
        "NOT ON THE STARTING LIST. %d bytes. UNTRACKED, ignored via %s. A scratch DB is a FROZEN "
        "VINTAGE and is only reachable via comp-kuzu --db-path, never as the default surface. "
        "population_status=orphaned is asserted on NO READER FOUND, not on age alone." % (sz, ig),
        "0.8.0_AE_CloudComp lane",
        age_note="%d days at carding." % days))

PARTS.append(part(
    "kuzu_ac7.dir", "projection", "infra/aws/globgrph/kuzu_ac7/", "projection", "point_in_time",
    [], "kuzu:kuzu_ac7-dir", None, "unknown", None, None, None, "orphaned",
    "2026-06-09T00:00:00Z", "directory mtime via ls -la; NOT probed further", "inferred",
    "NOT ON THE STARTING LIST. UNTRACKED **AND NOT IGNORED** -- git check-ignore returns no match, "
    "so unlike its sibling kuzu_ac7.db this directory is visible as working-tree noise.",
    "0.8.0_AE_CloudComp lane"))

PARTS.append(part(
    "stitch_graph.json", "output_artifact", "infra/aws/globgrph/stitch_graph.json",
    "projection", "point_in_time", [], "json:stitch_graph",
    "infra/aws/globgrph/derive_stitch.py + infra/aws/globgrph/extract_portal_stitch.py", "unknown", None, None, None,
    "unknown", "2026-07-25T18:44:34Z", STAT_EV, "measured",
    "NOT ON THE STARTING LIST. 25,489,187 bytes -- a 25MB graph JSON. UNTRACKED, ignored via "
    "infra/aws/globgrph/.gitignore:7.",
    "0.8.0_AE_CloudComp lane", age_note="32 days at carding.",
    consumers=["kuzu_stitch_load.py"]))

PARTS.append(part(
    "kuzu_nessie_db.rebuild.tmp.SET", "output_artifact",
    "infra/aws/globgrph/kuzu_nessie_db.rebuild.tmp.{11532.35476078000000.1,27528.34391796000000.1,"
    "30644.34692687000000.1}{,.wal}",
    "none", "point_in_time", [], None,
    "infra/aws/globgrph/_canonical.py:347 (rebuild writes a tmp db then swaps)", "canonical", None,
    "per rebuild", "Nessie HEAD advance", "orphaned",
    "2026-08-25T21:31:00Z", "stat on each of the 6 members; du -ch for the total", "measured",
    "FINDING -- 158MB (165,675,008 bytes) of ORPHANED REBUILD TEMPORARIES from THREE separate "
    "interrupted rebuilds on 2026-08-25, as 6 files (3 dbs + 3 WALs). UNTRACKED **AND NOT IGNORED**: "
    "they appear as '??' in EVERY agent's git status on this device, which is working-tree noise "
    "every seat must read past. NOT DELETED -- DTX-AC5 binds and deletion is not this seat's act. "
    "SET ROW: covers 6 objects; see the companion denominator note.",
    "kuzu rebuild path owner (0.8.0_AE_CloudComp lane, NFRA_KUZUSPLIT)"))

PARTS.append(part(
    "kuzu_nessie_db.fallback.jsonl", "output_artifact",
    "infra/aws/globgrph/kuzu_nessie_db.fallback.jsonl", "evidence", "point_in_time", [], None,
    "infra/aws/globgrph/kuzu_incremental_refresh.py (the COND-2 persistent fallback sink)",
    "canonical", None, "on fallback only", "incremental-refresh fallback", "production",
    "2026-07-25T23:01:00Z", STAT_EV, "measured",
    "1,232 bytes. UNTRACKED **AND NOT IGNORED**. DECLARED in graph-call-manifest.yaml:224 as the "
    "COND-2 persistent .fallback.jsonl sink -- I HAVE NOT OPENED THIS FILE and have NOT determined "
    "whether it is a LIVE FALLBACK READ PATH or a dead artifact. 0.8.0_AE_CloudComp~X (73371) raised "
    "the hypothesis worth naming: a fallback that STILL ANSWERS is the fails-open family this wave "
    "has hit repeatedly, where a degraded path and a healthy one are byte-identical to the caller. "
    "THAT IS A HYPOTHESIS ABOUT A NAME, NOT A FINDING -- neither of us chased it, and it belongs to "
    "whoever owns the incremental-refresh path.",
    "0.8.0_AE_CloudComp lane", consumers=["comp-kuzu-inc provenance path"]))

PARTS.append(part(
    "_build_manifest.json.SET", "output_artifact",
    "infra/aws/globgrph/{kuzu_nessie_db,kuzu_db,kuzu_stitch_db}._build_manifest.json",
    "evidence", "point_in_time", [], None,
    "infra/aws/globgrph/kuzu_load.py + infra/aws/globgrph/kuzu_nessie_load.py + infra/aws/globgrph/kuzu_stitch_load.py", "canonical", None,
    "stamped beside each DB at build", "db build", "production",
    "per-DB, matches each DB", "stat; gitignore rule read at HEAD", "measured",
    "3 objects. UNTRACKED, ignored via infra/aws/globgrph/.gitignore '*._build_manifest.json' -- "
    "DELIBERATELY, per its own TO-F1 comment (machine-specific source paths, runtime artifacts, never "
    "committed). NOTE: these are the substrate the ENTIRE provenance-header contract stands on, and "
    "they are device-local and uncommitted BY DESIGN -- a manifest-less DB reads as UNKNOWN VINTAGE. "
    "SET ROW: covers 3 objects.",
    "0.7.0_AE_CloudOps (NFRA_GLOBGRPH TO-F1)"))

# ---------------- CACHE PLANE ----------------
PARTS.append(part(
    ".comp-graph/graph.json", "store", ".comp-graph/graph.json", "projection", "current_state",
    [], "json:trace-graph", "comp-trace graph build (write_path:true, graph-call-manifest.yaml:568)",
    "canonical", None, "5-min TTL, rebuilds on read if stale", "read-triggered", "production",
    "2026-08-06T22:49:11Z", STAT_EV, "measured",
    "1,557,219 bytes, UNTRACKED. STAGE-1 SUBSTRATE OF THE C3 CHAIN -- nerves_resolve reads this. "
    "NODE COUNT NOT RE-MEASURED HERE: the 2,249 figure is 1.0.0_SA_CTO~X's HELD value at their "
    "vintage, cited not re-derived (Rule 22 -- do not re-run a peer's command).",
    "UNOWNED -- no cadence owner identified; this is part of the Q4 binding constraint",
    age_note="20.0 days at carding against a declared 5-min TTL and temporal_claim current_state. The "
             "TTL governs REBUILD-ON-READ, so an unread graph simply ages -- which is exactly how a "
             "stage-1 substrate reaches 19.7d stale without any alarm firing.",
    coverage={"population": "canonical graph nodes reachable by nerves_resolve", "denominator": "2,249 of 27,061 = 8.3% -- HELD at 1.0.0_SA_CTO~X's vintage, cited not re-derived"},
    consumers=["comp-blast", "comp-trace", "nerves_resolve"]))

for pid, sz, utc, days, ar, gen, cons in [
    (".comp-graph/baseline.json", 1558019, "2026-07-31T19:20:36Z", 26, "evidence", None, []),
    (".comp-graph/pydeps.json", 112725, "2026-07-16T19:37:43Z", 41, "projection", None,
     ["comp-blast (python dependency edges)"]),
    (".comp-graph/pathrooting-census.json", 101336, "2026-07-29T00:10:51Z", 29, "evidence", None, []),
    (".comp-graph/managed_policy_actions_cache.json", 106971, "2026-07-08T19:44:08Z", 49,
     "reference", "comp-iam managed-policy resolution", ["comp-iam"]),
]:
    PARTS.append(part(
        pid, "store", pid, ar, "point_in_time", [], None, gen, "unknown", None, None, None,
        "unknown", utc, STAT_EV, "measured",
        "NOT ON THE STARTING LIST. %d bytes, UNTRACKED (device-local). %s" % (
            sz,
            "Byte-size within 800 of graph.json -- almost certainly a snapshot of the same structure, "
            "NOT CONFIRMED and recorded as unconfirmed." if "baseline" in pid else
            "Generator not resolved by directory enumeration; recorded UNKNOWN rather than omitted."),
        "UNKNOWN", age_note="%d days at carding." % days,
        consumers=cons or None))

PARTS.append(part(
    ".comp-graph/platinum.CACHE_SET", "store",
    ".comp-graph/platinum.{dag.bd,dag.cot,dag.inf,dataflows,routing}.cache",
    "projection", "current_state", [], None,
    "comp-platinum per-firm cache build", "canonical", None,
    "5-min TTL (graph-call-manifest.yaml:297)", "read-triggered", "production",
    "2026-08-24T21:36:18Z", "stat on each of the 5 members; range recorded", "measured",
    "NOT ON THE STARTING LIST. 5 objects, 173,092 bytes total, UNTRACKED. THE FIVE MEMBERS SPAN 33 "
    "DAYS: bd/routing 2026-08-24, cot/inf 2026-07-22, dataflows 2026-07-25. SET ROW: covers 5 objects.",
    "0.4.0_DE/DT ClientPlatform lane (platinum surface)",
    age_note="33-day spread against a declared 5-min TTL. The TTL governs rebuild-on-read, so an "
             "unread firm's cache simply ages -- recorded as an observation, NOT asserted as a defect.",
    consumers=["comp-platinum", "comp-blast reverse"]))

# ---------------- TRACKED GRAPH JSON ----------------
PARTS.append(part(
    "nerves-edges.json", "store", "org/modules/graph/nerves-edges.json", "source", "current_state",
    [], "json:nerves-edges", None, "unknown", None, None, None, "production",
    "2026-07-14T06:09:20Z", STAT_EV, "measured",
    "132,774 bytes, TRACKED. Generator not resolved -- recorded UNKNOWN rather than omitted.",
    "UNKNOWN", age_note="43 days at carding against temporal_claim current_state.",
    consumers=["comp-pulse", "nerves_resolve"]))

PARTS.append(part(
    "nerves-risk-edges.json", "store", "org/modules/graph/nerves-risk-edges.json", "source",
    "current_state", [], "json:nerves-risk-edges", None, "unknown", None, None, None, "production",
    "2026-08-25T07:50:00Z", STAT_EV, "measured",
    "2,147,060 bytes, TRACKED. EXERCISED AT THIS SEAT, not merely read: safe-commit.sh's risk-reflex "
    "printed 'danger map: 33.9h old / DENOMINATOR: N file(s) checked against 1832 danger node(s)' on "
    "MY OWN commits. That independently confirms the 1,832 figure AND confirms this store is "
    "LIVE-READ on every commit in this estate -- STATE at EXERCISED, not merely APPLIED.",
    "UNKNOWN", consumers=["comp-pulse (the pre-commit risk reflex)"]))

PARTS.append(part(
    "estate-coverage-resolver.json", "store", "org/modules/graph/estate-coverage-resolver.json",
    "projection", "current_state", [], "json:estate-coverage-resolver",
    "org/modules/graph/gen-estate-resolver.py", "unknown", None,
    None, None, "production", "2026-08-20T18:59:22Z", STAT_EV, "measured",
    "213,450 bytes, TRACKED. Generator named from graph-call-manifest.yaml:706, NOT source-confirmed "
    "at the file itself.", "UNKNOWN", age_note="6 days at carding.",
    consumers=["comp-estate coverage surface"]))

PARTS.append(part(
    "axes_history.jsonl", "store", "org/modules/graph/axes_history.jsonl", "evidence",
    "point_in_time", [], None, None, "unknown", None, None, None, "unknown",
    "2026-08-25T07:50:00Z", STAT_EV, "measured",
    "NOT ON THE STARTING LIST. 11,523 bytes, TRACKED. Generator and consumers both UNKNOWN.",
    "UNKNOWN"))

# ---------------- MATERIALIZER OUTPUTS -- the Andrew 1907Z family ----------------
PARTS.append(part(
    "motif_c2c3_materialize.json", "spec_artifact",
    "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/motif_c2c3_materialize.json",
    "evidence", "point_in_time", [], "json:motif-class-spec",
    "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MOTIF_c2c3_materialize_spec.py",
    "historical_in_use", None, "frozen -- no cadence", "none (frozen artifact, consumed on each derive)",
    "production", "2026-07-09T12:47:24Z", STAT_EV, "measured",
    "15,255 bytes, TRACKED (committed @fad55a83c7 by 0.4.0_DS_ClientPlatform~B). Emits 19 C2Motif "
    "CLASS nodes. STANDING MEASURED BY 1.0.0_SA_CTO~X (73215 Q2), CITED NOT RE-DERIVED: today's "
    "derive logged specs=3 -- the two frozen July class specs PLUS the live composition -- so this is "
    "CONSUMED RIGHT NOW. historical_in_use is NOT superseded and NOT canonical, and it is the most "
    "dangerous standing in the schema BECAUSE IT WORKS: a frozen July artifact silently feeding "
    "today's derive breaks nothing and alarms nobody, so neither a staleness check (it is in use) nor "
    "a liveness check (it works) can find it.",
    "0.4.0_DS_ClientPlatform lane",
    age_note="48 days at carding; temporal_claim point_in_time, so age is not the defect -- the "
             "standing is.",
    consumers=["the derive, which INGESTS this output"]))

PARTS.append(part(
    "motif_c2c3_materialize_ab.json", "spec_artifact",
    "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/motif_c2c3_materialize_ab.json",
    "evidence", "point_in_time", [], "json:motif-class-spec-ab",
    "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_MOTIF_P1_canonical_ab_catalog.py",
    "historical_in_use", None, "frozen -- no cadence", "none (frozen artifact)", "production",
    "2026-07-18T15:14:21Z", STAT_EV, "measured",
    "1,141,941 bytes, TRACKED (committed @c7048f4846). A/B variant of the same spec. Same "
    "historical_in_use standing and same basis as its sibling (1.0.0_SA_CTO~X 73215 Q2, specs=3).",
    "0.4.0_DS_ClientPlatform lane", age_note="39 days at carding.",
    consumers=["the derive"]))

PARTS.append(part(
    "c2_instances.json", "output_artifact",
    "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_instances.json",
    "evidence", "point_in_time", ["motif_c2c3_materialize.json"], "json:c2-instances",
    "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c2_individuate.py",
    "canonical", None, "runs in production at 02:00Z", "schedule", "production",
    "2026-08-07T00:49:00Z", STAT_EV, "measured",
    "10,329,963 bytes. UNTRACKED **AND NOT IGNORED**. "
    "⛔ ITS GENERATOR IS ON THE PRODUCTION NIGHTLY PATH, source-confirmed at this seat after "
    "1.0.0_SA_CTO~X 74335: derive_runner.py:1383 defines _C2C3_COMPOSE_DIRS, an ORDERED tuple "
    "whose first entry is the in-image copy at _APP/kimi_subdivision_harness and whose later "
    "entry is org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness; :1588 takes "
    "the FIRST dir containing c2_individuate.py and :1598 imports it. PRECISION THAT MATTERS: "
    "this is FIRST-MATCH-WINS, so the CVO deliverables directory is a FALLBACK ON THE "
    "RESOLUTION PATH, not the guaranteed winner -- which of the two runs depends on which "
    "contains the file at runtime, and I did NOT determine that on the live container. Either "
    "way an exec seat's deliverables folder is reachable from the production nightly derive, "
    "and a path-based classifier sorts it LANE-DELIVERABLE while reachability sorts it "
    "PRODUCTION -- the collision is the finding. "
    "Emits 6,207 C2Motif INSTANCE nodes "
    "(c2_individuate.py:350 EMITTED_NODE_TYPES = (C2Motif, C3System)); generator committed "
    "2026-08-07 @23220a7b20. "
    "CODE-VS-OUTPUT SPLIT, measured by 1.0.0_SA_CTO~X (73215 Q2) and NOT collapsible: THE GENERATOR "
    "IS CURRENT (ran in production 02:00Z TODAY) WHILE THIS OUTPUT IS 19 DAYS OLD. Recording one "
    "'currency' verdict would be wrong in both directions -- it would either condemn live code or "
    "bless a stale artifact. The Dockerfile's own warning applies: COPYing the composition's CODE is "
    "packaging; COPYing its OUTPUT is 'archaeology from the day after the build'. "
    "FINDING: a 10MB untracked, unignored artifact the derive INGESTS -- loss would be silent and "
    "unrecoverable from the repo. "
    "ACCESS: READ-ONLY at this seat; the kimi_subdivision_harness tree belongs to CVO. An untracked "
    "output IS a manifest row and IS a finding; it is not this seat's to track or move. "
    "C2 HAS TWO MATERIALIZERS AT TWO VINTAGES OWNED BY TWO LANES (0.8.0_AE_CloudComp~X, 73195, cited "
    "not re-derived): the derive INGESTS the older family's OUTPUT while CALLING the newer family's "
    "CODE -- so 'which is the most updated/relevant' is NOT WELL-FORMED for C2, and a row naming a "
    "single C2 generator would be false in a way no vintage check could catch.",
    "3.0.0_SA_CVO", age_note="output 19 days old; generator current.",
    consumers=["the derive"]))

PARTS.append(part(
    "c3_structures.json", "output_artifact",
    "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c3_structures.json",
    "evidence", "point_in_time", ["c2_instances.json"], "json:c3-structures",
    "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/c3_cover.py",
    "canonical", None, "runs in production at 02:00Z", "schedule", "production",
    "2026-08-07T00:55:00Z", STAT_EV, "measured",
    "2,115,118 bytes. UNTRACKED **AND NOT IGNORED**. Same CODE-CURRENT / OUTPUT-STALE split as "
    "c2_instances.json (1.0.0_SA_CTO~X 73215 Q2). READ-ONLY at this seat. "
    "THIS IS NOT A C3 LAYER. Andrew-direct 1911Z, verbatim: 'the entire reason we're doing this is to "
    "ultimately get to a position where we can construct C3 via the nerves_resolve->affinity "
    "matrix->similarity network fusion process. We are nowhere even close to doing c3 right now.' "
    "This artifact is a ONE-OFF HISTORICAL MATERIALIZATION at authority_role=evidence, and any "
    "consumer reading it as THE C3 layer is reading it wrong.",
    "3.0.0_SA_CVO", age_note="output 19 days old; generator current.",
    consumers=["the derive"]))

# ---------------- C3 CHAIN: stages that DO NOT EXIST ----------------
CHAIN_EV = ("1.0.0_SA_CTO~X 73215 Q1, answering an Andrew-directed ask. HELD at that seat's vintage, "
            "cited not re-derived. Recorded as an ABSENT ROW rather than omitted: an empty row is a "
            "finding and skipping it loses the baseline (D11 stance block). An omitted row and an "
            "absent row are opposite facts that look identical in a manifest.")

PARTS.append(part(
    "nerves_resolve", "materializer", "org/modules/graph/nerves_resolve.py", "none", "current_state",
    [], None, "org/modules/graph/nerves_resolve.py", "canonical", None,
    "NONE -- no cadence", "none", "production", None,
    "no persisted artifact to date; 1.0.0_SA_CTO~X 73215 Q1", "held",
    "C3 CHAIN STAGE 1 -- THE ONLY STAGE THAT EXISTS. READS .comp-graph/graph.json, comp_pydeps.py, "
    "git tracked files, .tools/. WRITES NOTHING -- pure function, in-memory lru_cache only. "
    "BINDING CONSTRAINT OF THE WHOLE CHAIN, in 1.0.0_SA_CTO~X's words (73215 Q4): 'stage one of the "
    "C3 chain currently resolves against 2,249 of 27,061 canonical graph nodes (8.3%), from an input "
    "19.7 days stale, with NO cadence and NO named owner, and a failure mode where SUBSTRATE-ABSENT "
    "is byte-identical to GENUINELY-UNADDRESSED.' Their qualifier: the design is sound and it is the "
    "ONLY DECLARED CROSS-SPACE MAPPING IN THE ESTATE -- but a spine at 8.3% with no owner is A "
    "SAMPLE, NOT A SPINE, and nothing above L1 can be contracted until that changes.",
    "UNOWNED -- no named owner; that absence IS the constraint",
    coverage={"population": "canonical graph nodes reachable by nerves_resolve", "denominator": "2,249 of 27,061 = 8.3% -- HELD at 1.0.0_SA_CTO~X's vintage, cited not re-derived"},
    consumers=["the C3 chain, stages 2-4, none of which exist"]))

for pid, stage, wr, ww in [
    ("affinity_matrix", 2,
     "the L1 entity set + the four views (structure/flow/behavior/semantic)",
     "a per-view affinity store -- UNBUILT, unnamed, unhomed"),
    ("similarity_network_fusion", 3, "the per-view affinity matrices",
     "a fused affinity store -- UNBUILT"),
    ("identity_and_succession", 4, "fused clusters",
     "an identity register carrying birth/death/split/merge -- UNBUILT"),
]:
    PARTS.append(part(
        pid, "materializer", "NOWHERE -- unbuilt; no code, no store, no artifact", "none", "unknown", [], None,
        None, "unknown", None, None, None, "unknown", None,
        "ABSENT -- no code, no store, no artifact to measure", "absent",
        "C3 CHAIN STAGE %d -- ABSENT. WOULD READ: %s. WOULD WRITE: %s. %s" % (stage, wr, ww, CHAIN_EV),
        "UNOWNED -- unbuilt"))


MANIFEST = {
    "schema_version": 1,
    "compiled_by": "0.4.0_DT_ClientPlatform~X",
    "as_of": {"compiled_utc": COMPILED_UTC, "commit_ish": COMMIT_ISH},
    "denominator": {
        "method": (
            "PHASE A, INDEPENDENT INSTRUMENT. The estate was swept FIRST and 1.0.0_SA_CTO~X's "
            "starting list was diffed against the result AFTERWARD, in that order, so the list "
            "stayed falsifiable rather than becoming a template. Planes swept: (1) the Iceberg/Nessie "
            "warehouse s3://opal-313476888478-globgrph/warehouse/globgrph/ -- COMPLETE over 181,412 "
            "keys, full pagination, table dirs derived from key segment 3; (2) infra/aws/globgrph/ -- "
            "COMPLETE by directory enumeration; (3) .comp-graph/ -- COMPLETE by directory "
            "enumeration; (4) org/modules/graph/ -- PARTIAL, graph-bearing JSON only; (5) "
            "s3://opal-estate-report/ -- COMPLETE over 129 keys via raw s3api full pagination AFTER "
            "comp-keys' 40-row default truncation nearly produced a false absence; (6) repo-wide "
            "filename sweep for *kuzu* -- 65 hits over 28,797 files scanned. "
            "ALL COUNTS COMPUTED FROM THE POPULATION, NEVER TYPED -- the first cut of this file "
            "declared 39 against 35 rows and the TO's own phase-2 mandate caught it. "
            "-- READ THIS BEFORE QUOTING ANY COUNT: PARTS ARE NOT OBJECTS, AND NEITHER IS A "
            "SUBSTITUTE FOR THE OTHER. See the computed PARTS_VS_OBJECTS line appended below; the "
            "figures there are derived from the population at build time, never typed. Cross-checked against an INDEPENDENT sweep: "
            "0.8.0_AE_CloudComp~X (73371) ran comp-find --name 'kuzu_nessie_db' (7 hits / 28,837 "
            "scanned) and found exactly the 7 sibling artifacts at that prefix; ALL 7 ARE ALREADY "
            "REGISTERED HERE, carried by 2 parts -- 1 exact row plus the 6-member SET row. Their "
            "instrument (repo filename sweep) DIFFERS from mine (directory enumeration), so this is "
            "corroboration and not a repetition. "
            "-- AND A LIMIT ON `consumers` THAT APPLIES TO NEARLY EVERY ROW: consumers are DECLARED "
            "FROM CONFIG (graph-call-manifest.yaml, instance.tf, module source) and are NOT MEASURED "
            "READS unless a row's evidence says EXERCISED. Exactly ONE row is exercised: "
            "nerves-risk-edges.json, which safe-commit's risk reflex read live on this seat's own "
            "commits (1,832 danger nodes). Everywhere else, a named consumer means 'something "
            "declares it reads this', never 'I watched it read'. THE PRACTICAL CONSEQUENCE: a "
            "declared consumer that has silently stopped reading, and a live one, are "
            "INDISTINGUISHABLE in this manifest."),
        "population_searched": (
            "181,412 warehouse keys + 129 estate-report keys + 28,797 repo files scanned by filename "
            "sweep + 3 directories enumerated exhaustively"),
        "parts_registered": len(PARTS),
        "known_unsearched": [
            "OTHER AWS ACCOUNTS AND REGIONS -- the warehouse sweep is one bucket in us-east-1. A "
            "graph store in another account is invisible here and no claim is made about it.",
            "THE SITE-Z FABRIC -- this census ran on the laptop fabric only. Every local-plane part "
            "(.comp-graph/, infra/aws/globgrph/) describes THIS DEVICE, and the other device's "
            "local stores are BY CONSTRUCTION different and unmeasured.",
            "DYNAMODB / RDS / ANY NON-S3 PERSISTENCE -- not swept at all. A graph-bearing DynamoDB "
            "table would be missed entirely. THIS IS THE SINGLE WIDEST GAP IN THE CENSUS.",
            "org/modules/graph/ beyond graph-bearing JSON -- ~100 further .py/.yaml files were not "
            "classified. A store hiding as a .yaml in that tree would be missed.",
            "IN-MEMORY / EPHEMERAL graph state -- out of scope by form.",
            "PORTAL-SIDE graph surfaces -- not swept; the portal repo was not entered for this census.",
            "⛔ THE TREE-SCOPE LIMIT, QUANTIFIED BY 1.0.0_SA_CTO~X (74321) AND HELD AT THEIR "
            "VINTAGE -- I HAVE NOT RE-DERIVED IT: this census's 24 distinct materializers ALL sit "
            "in globgrph + org/modules/graph + comp-tools. A writer predicate they VALIDATED "
            "AGAINST KNOWN POSITIVES FIRST (their first attempt returned 3 files and missed the "
            "incremental updater they had just read upserting into graph_nodes, so they discarded "
            "it rather than report 3) returned 40 candidate graph-writers across SEVEN TREES. FIVE "
            "OF THE SEVEN WERE NEVER A SWEPT PLANE HERE. "
            "⛔ THE 40 IS NOW PARTITIONED BY MEASUREMENT (1.0.0_SA_CTO~X 74368, resolved by DIFFING "
            "THE LISTS rather than picking between two counts): 48 files REFERENCE the graph "
            "tables; 41 of those are ALSO write-shaped (their predicate, tests included); 7 "
            "reference them ONLY and are CONSUMERS. A reference-based population therefore "
            "admits consumers as materializers -- WHICH IS THE EXACT DEFECT THIS MANIFEST "
            "COMMITTED EARLIER TONIGHT, when it named kuzu_incremental_refresh.py as a "
            "producer of graph_nodes. For a census whose subjects are materializers the WRITE "
            "TEST IS NOT AN OPTIMISATION, IT IS THE DEFINITION. Their first hypothesis for the "
            "gap -- their own tests/workflows exclusions -- was TESTED AND KILLED (removing "
            "both moves 40 to 41, one file), and they recorded the killed hypothesis. "
            "⛔ AND THE RESULT THAT VINDICATES A ROW HERE RATHER THAN CORRECTING ONE: "
            "infra/aws/globgrph/_canonical.py lands in their READ-ONLY set for "
            "graph_nodes/graph_edges, while this manifest names it a materializer with "
            "standing=canonical for kuzu_nessie_db.rebuild.tmp.SET. BOTH ARE CORRECT. It is a "
            "materializer OF A DIFFERENT ARTIFACT. >> MATERIALIZER IS NOT A PROPERTY OF A "
            "FILE; IT IS A RELATION BETWEEN A FILE AND AN ARTIFACT << -- so a claim that "
            "'X is a materializer' without naming WHICH artifact is unfalsifiable, and a "
            "file-level materializer population carries false positives AND false negatives at "
            "once. THIS MANIFEST IS AT THE RIGHT GRAIN BY CONSTRUCTION AND NOT BY INSIGHT: "
            "generation.materializer sits INSIDE a part, so every claim here is already "
            "(file, artifact) -- the L0 schema chose that, I did not reason to it. "
            "⛔ AND THE OBSERVER IS INSIDE ITS OWN POPULATION -- MEASURED ON THIS FILE: a "
            "reference+write-shaped predicate ADMITS FOUR OF THIS LANE'S OWN DELIVERABLES as "
            "graph-writers (build_manifest.py refs=13/write=32, build_cards_2.py 15/8, this "
            "manifest 12/3, build_reconcile.py 4/1) -- and build_manifest.py carries MORE "
            "table references than the real incremental writer does (10). DECOMPOSED: 28 of "
            "its 32 write-shaped hits are `PARTS.append(`, A PYTHON LIST APPEND, and 3 are "
            "`upsert` inside QUOTED citations of the Lambda's own header; zero are "
            "overwrite/load_table/put_object/to_arrow/write_parquet, and the file opens "
            "exactly one thing for write -- its own JSON. ⛔ SO THE DOOR IS WIDER THAN "
            "QUOTATION: Iceberg's write verb and list.append are the SAME TOKEN, so any "
            "python file that mentions the tables and builds a list scores as a writer. A "
            "pyiceberg-citation filter (2.0.0_SA_COO~X, 3 of 43) would leave 28 of my 32 hits "
            "untouched. AND THE CONTAMINATION IS CAUSED BY DOING THE JOB WELL: this builder "
            "quotes the Lambda's header verbatim so a reader can see WHY the Lambda is called "
            "a writer -- the more evidence an artifact quotes, the more writer-shaped it "
            "looks. A wave-3 driver building a population from this estate must exclude D11's "
            "own deliverables or admit them knowingly. "
            "⛔ NEITHER 40 NOR 48 IS THE POPULATION -- both are FLOORS OVER DIFFERENT "
            "PREDICATES, AND THE ERROR RUNS "
            "BOTH WAYS -- it OVER-counts (a reader that also writes elsewhere, a helper, a "
            "one-shot, a lane's own analysis script all match) and UNDER-counts (dynamic table "
            "names, a writer that never names the table in source, anything outside *.py). That "
            "sentence travels with the number wherever it goes; it must not become a denominator "
            "without it. "
            "⛔ AND THE SELF-CRITICISM IS THEIRS AND IS EXACT: THE SINGLE-TREE SCOPE WAS NEVER "
            "WRONG AS A SCOPE -- IT WAS NEVER STATED AS A LIMIT. That is the whole defect in this "
            "block's earlier versions: not that I swept one tree, but that nothing in the artifact "
            "said so. "
            "⚠ ALSO SURFACED THERE AND NOT REGISTERED HERE, because parts are HELD: "
            "org/threads/handoff/NFRA_GCONTR.TO-2_contract_engine.NEW.py -- 21,296 B, executable, "
            "2026-06-16, references the graph tables, write-shaped calls, UNTRACKED BY GIT AND NOT "
            "IGNORED (positive control: derive_runner.py reads TRACKED by the same command). It "
            "describes itself as the value-layer NEVER-WIDEN machinery. 1.0.0_SA_CTO~X does NOT "
            "claim it runs and did not look for a caller; comp-surface-check is RETIRED per Rule "
            "20, so it may be a dead draft. Recorded because NOBODY CAN CARD WHAT IS NOT IN THE "
            "REPOSITORY, which is the class this directive exists to surface. "
            "⛔ THE PRODUCER SURFACE IS WIDER THAN ANY TREE I SWEPT, AND THE RIGHT PREDICATE IS NOT "
            "A DIRECTORY LIST: per 1.0.0_SA_CTO~X 74305 it is ANY TREE REACHED BY SYS.PATH INSERTION "
            "FROM A MATERIALIZER. derive_runner.py:36 inserts WS=/app and :40 imports comp_aws_cli "
            "from org/modules/graph/ -- a tree I DID sweep, where a 157,941-byte module with 79 "
            "describe/list/get sites carries the estate's entire AWS extraction surface, and ZERO of "
            "my 39 parts matched it. A cross-tree import is not an unreachable node; IT IS NOT A NODE "
            "AT ALL, so no reachability denominator I built ever had a slot for it. "
            "⛔ AND I REPRODUCED THE PREDICATE FAILURE AT MY OWN SEAT: a static grep for "
            "client('ec2')-style literals returns 0 over that file, because :87 builds every client "
            "through `boto3.client(svc, region_name=region)`. A zero that disagrees with the node "
            "types the same file mints is the tell, and the count is not. "
            "⛔ HOLD DECLARED, SO 39 IS NOT READ AS A CLOSED CENSUS: 1.0.0_SA_CTO~X instructed this "
            "lane to HOLD the 40th part because it is AT LEAST TWO -- comp_aws_cli.py and the "
            "incremental Lambda. Those parts are NOT registered here and their absence is a "
            "declared hold, not a measured absence. "
            "⛔ AND A HOLD THAT RESOLVED: I earlier recorded a THIRD candidate producer, lambda "
            "infrastructure-daily-snapshot on cron(0 7), as resolved-by-target and unexamined. "
            "1.0.0_SA_CTO~X examined it (74329) and IT IS NOT A GRAPH PRODUCER. Re-measured at "
            "this seat: 0 graph_nodes/graph_edges references in its 27,237 bytes, against a "
            "POSITIVE CONTROL of 10 for the same grep on the known incremental producer, so the "
            "zero discriminates. Its own header calls it a disaster-recovery snapshot for "
            "30-day rollback. THE CHAIN IS TWO PRODUCERS, NOT THREE -- recorded because an "
            "unexamined candidate that quietly disappears from a later version of this block "
            "reads as an oversight rather than as a closed question. "
            "-- KEPT AS A LESSON: infra/aws/lambda/ was never swept "
            "by this census, and the WRITER of graph_nodes and graph_edges lives there -- "
            "infra/aws/lambda/globgrph/incremental_updater/lambda_function.py, found by "
            "1.0.0_SA_CTO~X (74284) after 0.8.0_AE_CloudComp~X refused to guess it. ZERO of these 39 "
            "parts named it. My census swept the graph MODULE and the WAREHOUSE and treated those as "
            "the producer surface; a producer one directory away was structurally invisible to every "
            "sweep I ran.",
            "GENERATOR CURRENCY on 20 of 24 materializer-bearing parts, and THE SEMANTIC-DEFECT AXIS "
            "ON EVERY PART -- no instrument in this estate discriminates a deprecated opinion "
            "(1.0.0_SA_CTO~X 73215 Q3, converging with 2.0.0_SA_COO~X ruling 2). Not a plane, but "
            "recorded here because it is the largest UNMEASURED surface and silence must not read as "
            "clean.",
        ],
    },
    "parts": PARTS,
}

# ---- PARTS vs OBJECTS: computed from the population, never typed ----
SET_MEMBERS = {"kuzu_nessie_db.rebuild.tmp.SET": 6, "_build_manifest.json.SET": 3,
               ".comp-graph/platinum.CACHE_SET": 5}
_absent = [p for p in PARTS if p["basis"] == "absent"]
_present = [p for p in PARTS if p["basis"] != "absent"]
_objects = sum(SET_MEMBERS.get(p["id"], 1) for p in _present)
MANIFEST["denominator"]["method"] += (
    " PARTS_VS_OBJECTS (computed at build): %d parts total = %d describing a PRESENT thing + %d "
    "recording an ABSENCE (the unbuilt C3 stages, which are NOT objects and must never be counted "
    "as inventory). Of the %d present parts, %d are SET rows covering %d member objects, so the "
    "present parts describe %d DISTINCT OBJECTS. A reader quoting '%d' as an object count "
    "overstates by the absences and understates by the sets, in opposite directions, which is "
    "exactly why both figures are printed."
    % (len(PARTS), len(_present), len(_absent), len(_present), len(SET_MEMBERS),
       sum(SET_MEMBERS.values()), _objects, len(PARTS)))

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(MANIFEST, f, indent=2, ensure_ascii=False)

print("parts_registered:", len(PARTS))
print("declared:", MANIFEST["denominator"]["parts_registered"])
assert MANIFEST["denominator"]["parts_registered"] == len(MANIFEST["parts"])
print("SELF-CHECK: declared denominator == population  PASS")
cls = {}
for p in PARTS:
    cls[p["part_class"]] = cls.get(p["part_class"], 0) + 1
print("by part_class:", cls)
pop = {}
for p in PARTS:
    pop[p["population_status"]] = pop.get(p["population_status"], 0) + 1
print("by population_status:", pop)
