#!/usr/bin/env python3
"""CCX3 -- NFRA_SUBSTRATECARDING WAVE 3 card builder (0.8.0_AE_CloudComp~X).

Generates the three v2 substrate cards for this lane's subjects and validates
each against org/standards/SUBSTRATE_CARD.v2.schema.json.

WHY GENERATED, NOT HAND-TYPED: a typed number beside a derived one always goes
stale. as_of is bound ONCE here and stamped into all three cards, which is what
CCX3-AC2 asks for (byte-identical commit_ish + graph_vintage across the wave).

carded_utc GRAIN: PER-BATCH. One clock read (`date -u`) at 2026-08-27T06:37:53Z,
stamped identically into all three cards. It is NOT a per-card read and does not
claim to be.
"""
from __future__ import annotations

import json
import pathlib
import sys

WS = pathlib.Path(__file__).resolve().parents[5]
OUT = pathlib.Path(__file__).resolve().parent
SCHEMA = WS / "org" / "standards" / "SUBSTRATE_CARD.v2.schema.json"

# --- the ONE wave pin (CCX3-AC2) -------------------------------------------
# commit_ish: verified `git diff <PIN> -- <both subject files>` EMPTY, with a
# positive control on CLAUDE.md that produced a non-empty diff -- so the pin is
# the vintage of the bytes actually read, not merely the newest commit.
PIN = "3b918f21b42366fce14f7c2076f18444cd782931"
CARDED_UTC = "2026-08-27T06:37:53Z"
GRAPH_VINTAGE = (
    "nessie:main batch_ts=1787796032859 (2026-08-27T02:00:32Z) -- the commit written by the "
    "/ecs/globgrph/derive-runner run whose log stream last-event is 2026-08-27T02:10:24.659Z; "
    "read from CloudWatch, not from a producer self-report of intent"
)

AS_OF = {"carded_utc": CARDED_UTC, "commit_ish": PIN, "graph_vintage": GRAPH_VINTAGE}
CARDED_BY = "0.8.0_AE_CloudComp~X"

# Owners (CCX3-AC6 Rule 26 -- measured NON-UNIFORM in wave 2, so read per row).
OWN_AE_OPS = "0.7.0_AE_CloudOps"      # infra/aws/terraform/globgrph/item2a.tf:5 "owner: 0.7.0_AE_CloudOps"
OWN_CVO = "3.0.0_SA_CVO"              # derive_runner.py:301-302 "CVO TO-3 owns its rows"
OWN_COMP = "0.8.0_AE_CloudComp"       # org/modules/graph/ comp-tool surface


def ref(rid: str, note: str) -> dict:
    """A joinable_ref: identity and description are TWO fields, not one string.

    The schema REJECTS an id containing ' -- ' or ' (' -- the two prose markers
    2.0.0_SA_COO~X's dedup had to key on across 8 wave-1 cards, where 51 raw
    entries covered 43 distinct subjects. Keeping the id clean is what makes the
    note safe to write at length.
    """
    assert " -- " not in rid and " (" not in rid, f"unjoinable id: {rid!r}"
    return {"id": rid, "note": note}

# ---------------------------------------------------------------------------
# CARD 1 -- derive_runner.py :: PATH A  (graph_nodes + graph_edges)
# ---------------------------------------------------------------------------
PATH_A = {
    "schema_version": 2,
    "carded_by": CARDED_BY,
    "subject": {
        "id": "infra/aws/globgrph/derive_runner.py :: PATH A -- graph_nodes + graph_edges",
        "kind": "script",
        "declared_domain": (
            "The nightly full-replace materialization of the globgrph cloud graph: every node and "
            "edge derived from the live AWS control plane for account 313476888478, written to "
            "globgrph.graph_nodes and globgrph.graph_edges. DOMAIN EXCLUDES globgrph.graph_contracts, "
            "which this path touches ENSURE-ONLY (derive_runner.py:301-308) -- that is PATH B's and "
            "the CVO's domain, and the exclusion is enforced in code, not merely declared."
        ),
    },
    "as_of": AS_OF,
    "process": {
        "methodology": {
            "how": (
                "commit_to_iceberg() (:251-380) builds two pyarrow tables from the in-memory derive "
                "graph and writes each through the GENERIC helper _overwrite_with_retry(catalog, "
                "table_id, pa_table, label) (:125-164), called at :345 with nodes_id and :376 with "
                "edges_id. The helper RE-LOADS the table on every attempt (:138) before calling "
                "table.overwrite(pa_table) (:139), because a conflicted in-memory Table still points "
                "at pre-conflict metadata and would 409 forever. Full-replace semantics: each run "
                "replaces the ENTIRE table contents. The input graph is not derived here -- it comes "
                "from comp_aws_cli.cmd_derive(), imported and called at derive_runner.py:101."
            ),
            "determinism": "deterministic",
            "inference_detail": None,
            "composes": [
                ref("org/modules/graph/comp_aws_cli.py::cmd_derive",
                    "imported and called at derive_runner.py:101 @ " + PIN + "; supplies the entire "
                    "input graph. This path derives nothing itself."),
                ref("aws:control-plane:313476888478",
                    "live AWS control-plane APIs, us-east-1, read THROUGH cmd_derive rather than "
                    "directly. Estate coverage is cmd_derive's property, not this path's."),
                ref("nessie:opal-globgrph:main",
                    "pyiceberg + Nessie REST catalog, NESSIE_URI=http://nessie.opal-globgrph.local:19120 "
                    "in taskdef globgrph-derive-runner:6"),
            ],
            "invents": [
                ref("graph_nodes.snapshot_ts",
                    "and graph_edges.snapshot_ts. Set to batch_ts and stamped onto EVERY row at :342 "
                    "and :378. A materializer-minted value, not a property of the AWS resource."),
                ref("graph_nodes.layer",
                    "and graph_edges.layer. Defaults to the literal 'aws' at :340 and :372 where the "
                    "node or edge carries none. Contrast comp_aws_cli.py:3096, which hardcodes it "
                    "unconditionally."),
                ref("graph_nodes.source",
                    "defaults to 'full-derive' at :341 where the node carries none. This is the "
                    "comp-kuzu discriminator separating AWS nodes from MS-graph nodes."),
                ref("graph_nodes.props",
                    "and graph_edges.props. _props_and_guard at :343 and :380 JSON-encodes every "
                    "non-fixed key into one string column."),
            ],
            "basis": "measured",
            "basis_by_field": {
                "how": "measured",
                "determinism": "measured",
                "composes": "measured",
                "invents": "measured",
            },
            "evidence": (
                "infra/aws/globgrph/derive_runner.py:251-380 (commit_to_iceberg), :125-164 "
                "(_overwrite_with_retry), :139 (table.overwrite), :345 + :376 (the two call sites), "
                ":101 (comp_aws_cli.cmd_derive) @ " + PIN + ". Write-method population established by "
                "AST (ast.Call over an attribute in the table-op set), NOT by regex -- a regex over "
                "this file returns 49 hits of which 45 are list.append; the 4 true table ops are "
                ":120 create_table, :139 overwrite, :1214 overwrite, :1217 append."
            ),
            "owner": OWN_AE_OPS,
            "materializer_standing": "canonical",
            "declared_opinions": [
                "derive_runner.py:301-302 asserts 'the derive overwrites graph_nodes/graph_edges but "
                "MUST NOT touch graph_contracts'. This is a COMMENT, and a comment is not a binding -- "
                "but it is CORROBORATED by live behaviour: the 2026-08-27T02:10Z run emitted "
                "'GRAPH_CONTRACTS_ENSURED (net-new create or already-present; NEVER overwritten by the "
                "derive)' and NO CONTRACTS_APPENDED/CONTRACTS_OVERWRITTEN marker. Comment and exercise "
                "agree; the exercise is what carries the claim."
            ],
        },
        "cadence": {
            "declared_rhythm": (
                "cron(0 2 * * ? *) -- daily 02:00 UTC, declared on EventBridge rule "
                "opal-globgrph-derive-runner-nightly and described at "
                "infra/aws/terraform/globgrph/item2a.tf:4"
            ),
            "actual_trigger": (
                "EVENTS plane. Rule opal-globgrph-derive-runner-nightly, State=ENABLED, "
                "ScheduleExpression=cron(0 2 * * ? *). Target Arn is the ECS CLUSTER "
                "arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph with EcsParameters "
                "TaskDefinitionArn=globgrph-derive-runner:6, LaunchType=FARGATE. "
                "*** CCX3-AC5: THE CLUSTER IS NOT THE SCRIPT. *** Task definition revision 6 has "
                "command=null AND entryPoint=null, so the taskdef does NOT name derive_runner.py. The "
                "trigger->script step is INFERRED from infra/aws/globgrph/Dockerfile:186 "
                "CMD [\"python\", \"/app/derive_runner.py\"] plus Dockerfile:60 COPY of this file to "
                "that path -- which is the BUILD INPUT, not the running bytes."
            ),
            "live_matches_declared": "yes",
            "live_instance_age": (
                "4h27m at carded_utc. Last run log-stream last-event 2026-08-27T02:10:24.659Z "
                "(/ecs/globgrph/derive-runner, stream derive-runner/derive-runner/3d162efb...). "
                "NOT DORMANT under Rule 25 (>=90d); it is 0.19d stale."
            ),
            "basis": "inferred",
            "basis_by_field": {
                "declared_rhythm": "measured",
                "actual_trigger": "inferred",
                "live_matches_declared": "measured",
                "live_instance_age": "measured",
            },
            "evidence": (
                "aws events describe-rule --name opal-globgrph-derive-runner-nightly -> "
                "{ScheduleExpression: 'cron(0 2 * * ? *)', State: 'ENABLED'}; "
                "aws events list-targets-by-rule -> Arn=cluster/opal-globgrph, "
                "EcsParameters.TaskDefinitionArn=globgrph-derive-runner:6; "
                "aws ecs describe-task-definition globgrph-derive-runner:6 -> containerDefinitions[0]"
                ".command=null, .entryPoint=null (THIS is why actual_trigger is basis=inferred); "
                "aws logs describe-log-streams /ecs/globgrph/derive-runner --order-by LastEventTime "
                "--descending -> lastEventTimestamp 1787796624659 = 2026-08-27T02:10:24.659Z; "
                "aws logs get-log-events on that stream -> 'OK: ICEBERG_NODES_WRITTEN count=27067', "
                "'OK: ICEBERG_EDGES_WRITTEN count=60872', 'OK: NESSIE_COMMIT branch=main "
                "ts=1787796032859'. TRIGGER CENSUS SWEPT BOTH PLANES: events list-rules = 137 rules "
                "(4 globgrph-matching), scheduler list-schedules = 18 schedules (1 matching, "
                "globgrph-cse-producer-nightly, which is NOT this subject). A one-plane sweep would "
                "have returned a true, well-controlled answer about the wrong population."
            ),
            "owner": OWN_AE_OPS,
        },
    },
    "artifact": {
        "persistence": {
            "persisted": True,
            "authority_role": "projection",
            "mutation_policy": "replaceable",
            "form": (
                "Apache Iceberg tables globgrph.graph_nodes and globgrph.graph_edges, via pyiceberg "
                "against a Nessie REST catalog on branch main; parquet + metadata under "
                "s3://opal-313476888478-globgrph/warehouse"
            ),
            "basis": "inferred",
            "basis_by_field": {
                "persisted": "measured",
                "authority_role": "inferred",
                "mutation_policy": "measured",
                "form": "measured",
            },
            "evidence": (
                "mutation_policy=replaceable is MEASURED: :139 table.overwrite(pa_table) with no "
                "overwrite_filter = full-table replace (contrast PATH B :1214, which passes "
                "overwrite_filter=In('contract_id', ids) and is therefore scoped). form/persisted from "
                "the pyiceberg Schema at :270-292 and WAREHOUSE_URI=s3://opal-313476888478-globgrph/"
                "warehouse in taskdef rev 6. "
                "*** authority_role IS INFERRED AND THE TENSION IS DELIBERATE: *** these tables are a "
                "PROJECTION of the live AWS control plane (nothing originates here -- a row deleted in "
                "AWS vanishes on the next overwrite), yet every downstream consumer "
                "(.tools/_trino_fed.py:44, fedobs_views.sql:34, the Kuzu loader) treats them as SOURCE. "
                "Naming it 'source' would license reading it as authoritative about resources AWS no "
                "longer has; naming it 'projection' is what the mechanism supports."
            ),
            "owner": OWN_AE_OPS,
        },
        "location": {
            "home": (
                "nessie:main -> globgrph.graph_nodes and globgrph.graph_edges. Namespace bound at "
                "derive_runner.py:263 ns = \"globgrph\"; table names bound at :281 "
                "nodes_id = (ns, \"graph_nodes\") and :292 edges_id = (ns, \"graph_edges\"). "
                "Warehouse s3://opal-313476888478-globgrph/warehouse."
            ),
            "projection_of": [
                ref("aws:control-plane:313476888478",
                    "us-east-1; read via comp_aws_cli.cmd_derive at derive_runner.py:101 @ " + PIN),
            ],
            "co_resident_stores": [
                ref("globgrph.graph_contracts",
                    "SAME namespace, DIFFERENT writer and DIFFERENT authority. This path is "
                    "ENSURE-ONLY on it at :301-308, inside a try/except that only WARNs."),
                ref("globgrph.cse", "0.7.0_AE_CloudOps~X's subject this wave"),
                ref("globgrph.resource_summaries", "0.7.0_AE_CloudOps~X's subject this wave"),
            ],
            "basis": "measured",
            "evidence": (
                "derive_runner.py:263 (ns), :281 (nodes_id), :292 (edges_id), :301-308 (the "
                "ensure-only contracts boundary), :416 (the four-table namespace list "
                "('graph_nodes','graph_edges','graph_contracts','cse')) @ " + PIN + "; "
                "WAREHOUSE_URI from aws ecs describe-task-definition globgrph-derive-runner:6."
            ),
            "owner": OWN_AE_OPS,
        },
    },
    "trust": {
        "coverage": {
            "universe": (
                "Every node and edge present in the derive graph returned by comp_aws_cli.cmd_derive "
                "for account 313476888478 at run time. NOT 'every AWS resource' -- coverage of the "
                "estate is cmd_derive's property, not this write path's, and this card does not "
                "inherit it."
            ),
            "denominator": (
                "27067 nodes and 60872 edges, written by the 2026-08-27T02:10:24Z run. This is the "
                "COUNT THE MATERIALIZER WROTE, and it certifies the WRITE, not the estate: it is the "
                "denominator of what cmd_derive handed over, and says nothing about what cmd_derive "
                "failed to discover."
            ),
            "explicitly_out": [
                "globgrph.graph_contracts row content -- ENSURE-ONLY here (:301-308); PATH B and "
                "3.0.0_SA_CVO own it",
                "the completeness of cmd_derive's estate discovery -- a DIFFERENT subject with a "
                "different owner",
                "*** CCX3-AC7: THE WRITER POPULATION OF THESE TWO TABLES. *** This card does NOT "
                "assert it is the only writer, and it is NOT. MEASURED: globgrph.graph_nodes has "
                "THREE writers and this path is one of them. " + "ESTATE CENSUS, INDEPENDENT INSTRUMENT, DENOMINATOR PRINTED: 7236 .py files swept under "
                "infra/, org/modules/, .tools/, data/, workflows/, excluding vendored "
                "pyiceberg-nessie-deps and __pycache__; 33 files NAME graph_nodes; 5 carry a "
                "strong non-append Iceberg write op by AST. THREE of those five write "
                "globgrph.graph_nodes itself: [1] derive_runner.py PATH A, FULL overwrite, "
                "nightly; [2] org/modules/graph/comp_aws_cli.py:3051, FULL overwrite, "
                "untriggered; [3] infra/aws/lambda/globgrph/incremental_updater/"
                "lambda_function.py, table_id bound at :434 and written at :501 with "
                "table.overwrite(pa_table, overwrite_filter=combined_filter) -- a SCOPED "
                "delete+append, NOT a full replace. The other two of the five write different "
                "tables (cse_store.py, resource_summaries_store.py). THIS IS A DIFFERENT "
                "INSTRUMENT ON A DIFFERENT POPULATION from the AST enclosure test that "
                "established the per-file write paths: that one asked which call sites in THOSE "
                "TWO FILES are table ops; this one asks who in the ESTATE names and writes this "
                "table. Only the second question can find a writer the first cannot see, and it "
                "found one." + " NOTE THE MECHANISM "
                "SPLIT, which matters more than the count: this path and comp_aws_cli FULL-overwrite; "
                "incremental_updater does a FILTERED overwrite. A full replace landing after a scoped "
                "update DISCARDS that update, and incremental_updater knows the table is contended -- "
                "lambda_function.py:43 records a race on graph_nodes Nessie commits where the losing "
                "writer takes a 409. Coordination between the three is NOT carded here and is not "
                "this lane's to design.",
            ],
            "basis": "measured",
            "evidence": (
                "counts from the CloudWatch run log (see cadence.evidence). The other writers are "
                "measured at org/modules/graph/comp_aws_cli.py:3032, :3045, :3051, :3091 (the third "
                "card in this batch) and at infra/aws/lambda/globgrph/incremental_updater/"
                "lambda_function.py:434, :501, @ " + PIN + ". " + "ESTATE CENSUS, INDEPENDENT INSTRUMENT, DENOMINATOR PRINTED: 7236 .py files swept under "
                "infra/, org/modules/, .tools/, data/, workflows/, excluding vendored "
                "pyiceberg-nessie-deps and __pycache__; 33 files NAME graph_nodes; 5 carry a "
                "strong non-append Iceberg write op by AST. THREE of those five write "
                "globgrph.graph_nodes itself: [1] derive_runner.py PATH A, FULL overwrite, "
                "nightly; [2] org/modules/graph/comp_aws_cli.py:3051, FULL overwrite, "
                "untriggered; [3] infra/aws/lambda/globgrph/incremental_updater/"
                "lambda_function.py, table_id bound at :434 and written at :501 with "
                "table.overwrite(pa_table, overwrite_filter=combined_filter) -- a SCOPED "
                "delete+append, NOT a full replace. The other two of the five write different "
                "tables (cse_store.py, resource_summaries_store.py). THIS IS A DIFFERENT "
                "INSTRUMENT ON A DIFFERENT POPULATION from the AST enclosure test that "
                "established the per-file write paths: that one asked which call sites in THOSE "
                "TWO FILES are table ops; this one asks who in the ESTATE names and writes this "
                "table. Only the second question can find a writer the first cannot see, and it "
                "found one."
            ),
            "owner": OWN_AE_OPS,
        },
        "key": {
            "identity_space": (
                "TABLE identity: the pyiceberg 2-tuple (namespace, table) -- ('globgrph','graph_nodes'), "
                "('globgrph','graph_edges'). ROW identity: node_id (StringType, required=True) for "
                "nodes; (src_id, dst_id, edge_type) for edges, all required=True. NOTE the row keys are "
                "required=True but NOT unique-constrained -- Iceberg has no uniqueness enforcement; "
                "required=True is satisfied by the EMPTY STRING, which is exactly how the A11 defect "
                "went silent (see failure_mode)."
            ),
            "key_is_stable": "stable",
            "crosses_spaces": True,
            "declared_mapping": (
                "NONE -- there is no normalising layer, and this is the finding. The SAME table is "
                "addressed THREE ways in this estate: "
                "(1) 2-TUPLE ('globgrph','graph_nodes') -- derive_runner.py:281, comp_aws_cli.py:3032; "
                "(2) DOTTED 2-PART string 'globgrph.graph_nodes' -- derive_runner.py:1435-1436, "
                "catalog.load_table(\"globgrph.graph_nodes\"), i.e. INSIDE THIS VERY FILE, a different "
                "rendering from the one at :281; "
                "(3) DOTTED 3-PART Trino string 'iceberg.globgrph.graph_nodes' -- .tools/_trino_fed.py:44 "
                "and infra/aws/globgrph/fedobs/fedobs_views.sql:34, where 'iceberg' is the Trino CATALOG. "
                "All three are CORRECT addressings of one artifact; none is wrong. A join key built on "
                "string equality splits one table into up to three rows and announces nothing."
            ),
            "basis": "measured",
            "evidence": (
                "derive_runner.py:281, :292, :1435-1436; org/modules/graph/comp_aws_cli.py:3032, :3045; "
                ".tools/_trino_fed.py:44, :50; infra/aws/globgrph/fedobs/fedobs_views.sql:9-10, :34; "
                "schemas at derive_runner.py:270-292 @ " + PIN + ". "
                "CORROBORATION, NOT REPETITION: 0.7.0_AE_CloudOps~X (msg 74756) measured this same "
                "two-plane split for globgrph.cse by RESOLVING THE BINDING at "
                "org/modules/graph/cse_schema.py:595. My instrument differs -- I enumerated the "
                "ADDRESSING FORMS of an already-known table across the tree -- and it surfaced a THIRD "
                "rendering their subject's evidence did not need: the dotted 2-part form, in the same "
                "file as the tuple form."
            ),
            "owner": OWN_COMP,
        },
        "failure_mode": {
            "returns_on_failure": (
                "COMMIT CONFLICT: _overwrite_with_retry retries CommitFailedException and "
                "CommitStateUnknownException up to COMMIT_MAX_ATTEMPTS (:58, default 5, env "
                "ICEBERG_COMMIT_MAX_ATTEMPTS) with a table RE-LOAD each attempt; on exhaustion it "
                "raises and the ECS task fails -- LOUD. "
                "CONTRACTS-ENSURE FAILURE: caught at :306-308, prints "
                "'WARN: GRAPH_CONTRACTS_ENSURE_FAIL ...' and the run CONTINUES by design (the "
                "nodes/edges write is the declared critical path). "
                "EMPTY INPUT: no exception at all -- see silent_degrade_paths."
            ),
            "distinguishable_from_true_negative": "no",
            "silent_degrade_paths": [
                "*** THE SHARP ONE: `if all_nodes:` (:330) and `if all_edges:` (:357) guard the "
                "writes. If cmd_derive returns an EMPTY node or edge list, the overwrite is SKIPPED "
                "ENTIRELY -- no exception, no WARN, and NO 'ICEBERG_NODES_WRITTEN' marker. The table "
                "then retains the PREVIOUS run's rows. A consumer reading graph_nodes cannot "
                "distinguish 'tonight's estate, freshly written' from 'last night's estate, silently "
                "retained' -- both are a fully-populated table with a plausible snapshot_ts, because "
                "snapshot_ts belongs to the rows that were written, and stale rows carry the OLD "
                "batch_ts while nothing forces a reader to check it. THIS IS THE ANTI-CORRELATED "
                "SHAPE: the more completely the derive fails, the more intact the table looks.",
                "'WARN: GRAPH_CONTRACTS_ENSURE_FAIL' is a WARN on a rc=0 run -- a consumer scoring the "
                "run on exit code sees success while graph_contracts may be absent.",
                "The image tag is ':latest' and ECR image_tag_mutability is 'MUTABLE' "
                "(item2a.tf:14), while the taskdef pins no digest -- so 'the nightly runs THIS source' "
                "is not decidable from the trigger chain. Running bytes older than built bytes would "
                "pass every rung of this card.",
            ],
            "basis": "measured",
            "basis_by_field": {
                "returns_on_failure": "measured",
                "distinguishable_from_true_negative": "measured",
                "silent_degrade_paths": "measured",
            },
            "evidence": (
                "derive_runner.py:330 (`if all_nodes:`), :357 (`if all_edges:`), :125-164 (retry "
                "helper), :58 (COMMIT_MAX_ATTEMPTS), :304-308 (best-effort contracts ensure) @ " + PIN
                + "; infra/aws/terraform/globgrph/item2a.tf:14 image_tag_mutability = \"MUTABLE\"; "
                "aws ecr describe-images opal-globgrph-derive-runner -> tag 'latest' currently resolves "
                "to sha256:b1e3da0989f42200aadf2377f5c1f783b2156790d773cec9108e66cd44f1f82e pushed "
                "2026-08-26T00:48:59Z. "
                "distinguishable_from_true_negative='no' is MEASURED from the guard structure, not "
                "assumed: the empty-input path emits no marker and raises nothing, so its log signature "
                "is a SUBSET of a crash-before-write signature."
            ),
            "owner": OWN_AE_OPS,
        },
    },
    "verdict": {
        "standing": "QUALIFIED",
        "why": (
            "All seven rows MEASURED against source at " + PIN + " and against live AWS + the "
            "2026-08-27T02:10:24Z run; the write path is EXERCISED, not merely configured "
            "(27067 nodes / 60872 edges). Usable as load-bearing substrate WITHIN three named limits: "
            "(1) the trigger->script binding is INFERRED, not measured -- taskdef rev 6 carries "
            "command=null and the image tag is mutable, so this card cannot certify that the nightly "
            "runs the source it describes; (2) an empty derive silently retains stale rows with no "
            "marker and no error; (3) the artifact has TWO OTHER WRITERS -- comp_aws_cli.py "
            "cmd_iceberg_commit and the incremental_updater Lambda -- which this path neither knows "
            "about nor coordinates with, and one writes with a DIFFERENT mutation shape (filtered vs "
            "full replace), so a nightly full overwrite can silently discard an incremental update. "
            "None of the three blocks "
            "use; all three change what a consumer may CONCLUDE, which is why they are named rather "
            "than folded into a SOUND."
        ),
        "blocking_defects": [],
    },
    "forward_disposition": {
        "standing": "undecided",
        "set_by": None,
        "basis": "absent",
        "evidence": (
            "CCX3-AC8: this lane made ZERO commits touching any module it cards. Remedies are NAMED, "
            "not APPLIED. The mutable-tag and empty-input findings are surfaced to " + OWN_AE_OPS +
            " and to 3.0.0_SA_CVO via the completion route; the identity-space finding is surfaced to "
            "2.0.0_SA_COO~X as a join-key input. basis='held' because the disposition is this seat's "
            "assertion of scope discipline, not a measurement of anything."
        ),
        "decided_utc": None,
    },
}

# ---------------------------------------------------------------------------
# CARD 2 -- derive_runner.py :: PATH B  (graph_contracts)
# ---------------------------------------------------------------------------
PATH_B = {
    "schema_version": 2,
    "carded_by": CARDED_BY,
    "subject": {
        "id": "infra/aws/globgrph/derive_runner.py :: PATH B -- graph_contracts",
        "kind": "script",
        "declared_domain": (
            "The operator-invoked load of CVO-authored contract rows from a YAML file into "
            "globgrph.graph_contracts, plus the create-if-absent of that table. Same FILE as PATH A, "
            "DIFFERENT write path: different mechanism (scoped append/overwrite vs full replace), "
            "different bound (one table, bound as a literal tuple at :202 and :1154), and different "
            "AUTHORITY (rows are authored by 3.0.0_SA_CVO; the nightly derive is forbidden from "
            "touching them). Excludes graph_nodes/graph_edges entirely."
        ),
    },
    "as_of": AS_OF,
    "process": {
        "methodology": {
            "how": (
                "TWO entry points onto one table. "
                "(a) ENSURE: ensure_graph_contracts_table(catalog) (:197-207) builds table_id = "
                "(\"globgrph\", \"graph_contracts\") at :202 and calls _ensure_table (:203), which "
                "load_table-or-create_table (:112-122, create at :120) against the RATIFIED schema "
                "_graph_contracts_schema() (:167). This is reachable from the NIGHTLY (PATH A calls it "
                "at :305) and from --ensure-contracts (:2232). It CREATES A TABLE but writes no rows. "
                "(b) LOAD: load_contracts_from_yaml() (:1102-1240), reached via --load-contracts "
                "(:2238). It normalises YAML rows, skips ids already present unless named in "
                "--overwrite (:1163), FAILS CLOSED on an unstampable ratified_at pin (:1204-1206, "
                "returns 1 with NOTHING written), then branches: if overwriting, "
                "tbl.overwrite(pa_table, overwrite_filter=In(\"contract_id\", ids)) at :1214 -- a "
                "SCOPED delete+append in one Nessie commit, rows outside the filter untouched; else "
                "tbl.append(pa_table) at :1217, append-only. It then RE-READS the table (:1222) and "
                "gates on a per-row integrity check, returning 1 if any row fails (:1233-1236)."
            ),
            "determinism": "deterministic",
            "inference_detail": None,
            "composes": [
                ref("yaml:--load-contracts",
                    "a CVO-authored YAML file passed to the --load-contracts flag, "
                    "derive_runner.py:2238-2240 @ " + PIN),
                ref("nessie:opal-globgrph:main",
                    "read by _nessie_main_hash at :1199 to stamp ratified_at. This is the one "
                    "non-fixed input, and it FAILS CLOSED on empty at :1204-1206 rather than "
                    "substituting a placeholder, so non-determinism cannot leak into a written row."),
                ref("derive_runner.py::_graph_contracts_schema",
                    ":167, the RATIFIED NFRA_GCONTR PRD section-3 v0.1 schema"),
            ],
            "invents": [
                ref("graph_contracts.ratified_at",
                    "the Nessie main hash read at :1199 and stamped at :1204. Minted here, not "
                    "present in the source YAML, and fail-closed on empty rather than placeholdered."),
            ],
            "basis": "measured",
            "basis_by_field": {
                "how": "measured",
                "determinism": "measured",
                "composes": "measured",
                "invents": "measured",
            },
            "evidence": (
                "derive_runner.py:197-207 (ensure), :202 (the literal table_id tuple), :112-122 "
                "(_ensure_table), :167 (ratified schema), :1102-1240 (load_contracts_from_yaml), "
                ":1153-1154, :1163, :1173, :1199, :1204-1206, :1214, :1217, :1222, :1233-1236, "
                ":2232 + :2238 (the two CLI flags), :305 (the nightly's ensure-only call) @ " + PIN + ". "
                "Table-op population by AST, not regex."
            ),
            "owner": OWN_CVO,
            "materializer_standing": "canonical",
            "declared_opinions": [
                "The TO described PATH B as 'APPEND-ONLY (:116...'. MEASURED CORRECTION, and it is a "
                "REFINEMENT not a contradiction: append-only is the DEFAULT (:1217) and the skip "
                "message at :1163 says so verbatim -- 'already-present (append-only; pass --overwrite "
                "to replace)'. But a SCOPED OVERWRITE EXISTS at :1214 behind the --overwrite flag "
                "(:2246). So mutation_policy is append_only-by-default with an explicit, id-scoped "
                "operator escape -- not append_only absolutely. Carding it as pure append-only would "
                "tell a consumer that a contract row can never be replaced in place, which is false."
            ],
        },
        "cadence": {
            "declared_rhythm": (
                "NONE for the LOAD path. --load-contracts is an operator-invoked CLI flag; no schedule "
                "declares it. The ENSURE half rides the PATH A nightly (cron(0 2 * * ? *)) as a "
                "best-effort side effect."
            ),
            "actual_trigger": (
                "none-found for the LOAD path. Trigger census swept BOTH planes: aws events "
                "list-rules = 137 rules, aws scheduler list-schedules = 18 schedules; ZERO reference "
                "--load-contracts or graph_contracts. A repo sweep for a shell/tf/yaml invoker of "
                "load-contracts returned only documentation and census artifacts -- no wiring. "
                "The ENSURE half IS triggered, event-plane, via the PATH A nightly at :305, and that "
                "is MEASURED: the 2026-08-27T02:10:24Z run emitted 'OK: GRAPH_CONTRACTS_ENSURED "
                "(net-new create or already-present; NEVER overwritten by the derive)'."
            ),
            "live_matches_declared": "not_applicable",
            "live_instance_age": (
                "LOAD path: UNMEASURED. No CONTRACTS_APPENDED or CONTRACTS_OVERWRITTEN marker appears "
                "in the 2026-08-27T02:10:24Z run, which is expected (the nightly does not invoke it) "
                "and is NOT evidence about when the load last ran -- I did not sweep historical "
                "streams for it, and I am not going to imply a dormancy verdict I have not measured. "
                "ENSURE path: 4h27m (same run as PATH A). "
                "*** RULE 25 DORMANCY: UNDETERMINED for the load path, NOT 'dormant'. *** An absent "
                "trigger is a compliance fact, not a liveness fact."
            ),
            "basis": "absent",
            "basis_by_field": {
                "declared_rhythm": "measured",
                "actual_trigger": "measured",
                "live_matches_declared": "measured",
                "live_instance_age": "absent",
            },
            "evidence": (
                "*** THE ROW SCALAR IS 'absent' BY THE SCHEMA'S FLOOR RULE, NOT BECAUSE THE ROW IS "
                "UNGROUNDED. *** The floor is the WEAKEST sub-claim, never the mode: three of four "
                "sub-claims here are measured and the trigger census was exhaustive, but "
                "live_instance_age has no basis at all, so the scalar reports 'absent'. Read "
                "basis_by_field, not the scalar, to see which half is solid -- that split is exactly "
                "what the v2 basis_by_field addition exists to preserve. "
                "aws events list-rules (137, client-side count after auto-paginate) + aws scheduler "
                "list-schedules (18) -- BOTH PLANES, denominators printed; neither carries a "
                "graph_contracts or load-contracts target. Repo sweep for load-contracts invokers "
                "across *.sh/*.tf/*.yaml/*.yml/*.json returned only "
                "org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/D.raw_evidence.json "
                "(a census artifact, not a trigger). ENSURE liveness from CloudWatch "
                "/ecs/globgrph/derive-runner stream derive-runner/derive-runner/3d162efb..., message "
                "'OK: GRAPH_CONTRACTS_ENSURED'. derive_runner.py:305, :2232, :2238 @ " + PIN + "."
            ),
            "owner": OWN_CVO,
        },
    },
    "artifact": {
        "persistence": {
            "persisted": True,
            "authority_role": "source",
            "mutation_policy": "append_only",
            "form": (
                "Apache Iceberg table globgrph.graph_contracts via pyiceberg + Nessie REST catalog on "
                "branch main; schema is the RATIFIED NFRA_GCONTR PRD section-3 v0.1 shape "
                "(_graph_contracts_schema, :167), including a period_defs map column"
            ),
            "basis": "measured",
            "basis_by_field": {
                "persisted": "measured",
                "authority_role": "measured",
                "mutation_policy": "measured",
                "form": "measured",
            },
            "evidence": (
                "authority_role='source' is MEASURED, and it is the row that most distinguishes this "
                "path from PATH A: the rows are AUTHORED by 3.0.0_SA_CVO and nothing derives them from "
                "an upstream system -- there is no other system that could regenerate a lost contract "
                "row. The code enforces that authority: derive_runner.py:301-302 forbids the nightly "
                "from touching this table and :305 restricts it to ensure-only, corroborated live by "
                "'NEVER overwritten by the derive' in the 2026-08-27T02:10Z run. "
                "mutation_policy='append_only' is the DEFAULT branch at :1217; the schema enum has no "
                "'append_only_with_scoped_override' member, so the qualification lives in "
                "methodology.declared_opinions and in the coverage row rather than being silently "
                "dropped -- the :1214 scoped overwrite behind --overwrite (:2246) is REAL and a "
                "consumer must not read append_only as 'immutable'."
            ),
            "owner": OWN_CVO,
        },
        "location": {
            "home": (
                "nessie:main -> globgrph.graph_contracts. Bound as a LITERAL 2-tuple in TWO places: "
                "derive_runner.py:202 table_id = (\"globgrph\", \"graph_contracts\") in "
                "ensure_graph_contracts_table, and :1154 catalog.load_table((\"globgrph\", "
                "\"graph_contracts\")) in load_contracts_from_yaml, with a third at :1222 for the "
                "post-write verify re-read. Warehouse s3://opal-313476888478-globgrph/warehouse."
            ),
            "projection_of": [],
            "co_resident_stores": [
                ref("globgrph.graph_nodes",
                    "same namespace, written by PATH A, which is explicitly forbidden from touching "
                    "this table at :301-302"),
                ref("globgrph.graph_edges", "same namespace, written by PATH A"),
                ref("globgrph.cse", "0.7.0_AE_CloudOps~X's wave-3 subject"),
                ref("globgrph.resource_summaries", "0.7.0_AE_CloudOps~X's wave-3 subject"),
            ],
            "basis": "measured",
            "evidence": (
                "derive_runner.py:202, :1154, :1222, :416 (the namespace's four-table list) @ " + PIN +
                ". projection_of is EMPTY and that is a positive claim, not an omission: these rows "
                "have no upstream to be a projection OF -- they are authored, which is exactly why "
                "authority_role is 'source' and why an append-only default is the right mechanism."
            ),
            "owner": OWN_CVO,
        },
    },
    "trust": {
        "coverage": {
            "universe": (
                "The contract rows present in the YAML file handed to --load-contracts on a given "
                "invocation, plus every row already in globgrph.graph_contracts from prior loads."
            ),
            "denominator": None,
            "denominator_absent_reason": (
                "UNMEASURED, and deliberately so. A denominator here would be the row count of "
                "globgrph.graph_contracts, which requires a live read of the Nessie/Iceberg table. "
                "This device has no reachable path to nessie.opal-globgrph.local:19120 (a VPC-internal "
                "endpoint), and I will not substitute the count printed by a past run's "
                "'LOAD_CONTRACTS_COMPLETE table_row_count=' line -- that is a PRODUCER SELF-REPORT of "
                "a run I did not observe, at an unknown vintage. An honest absent beats a number "
                "whose grain I cannot state."
            ),
            "explicitly_out": [
                "graph_nodes / graph_edges -- PATH A's domain, and this path never addresses them",
                "the CONTENT correctness of CVO-authored contract rows -- 3.0.0_SA_CVO's domain",
                "*** CCX3-AC7: the writer population of graph_contracts. *** This card does NOT assert "
                "PATH B is the only writer. What IS measured: the nightly derive is forbidden and "
                "observably does not write rows (ensure-only). No sweep for OTHER writers of this "
                "table was performed, so the bound on the writer population is UNMEASURED -- not zero.",
            ],
            "basis": "absent",
            "basis_by_field": {
                "universe": "measured",
                "denominator": "absent",
                "explicitly_out": "measured",
            },
            "evidence": (
                "Scalar is the FLOOR: universe and explicitly_out are measured, denominator has no "
                "basis, so the row reports 'absent'. "
                "universe + explicitly_out from derive_runner.py:1102-1240, :301-308 @ " + PIN + ". "
                "denominator absent per denominator_absent_reason -- no live table read was possible "
                "from this device, and no substitute was accepted."
            ),
            "owner": OWN_CVO,
        },
        "key": {
            "identity_space": (
                "TABLE identity: the pyiceberg 2-tuple ('globgrph','graph_contracts'). ROW identity: "
                "contract_id -- and unlike PATH A's row keys this one IS actively used as a key: it "
                "drives the already-present skip (:1163), the overwrite id set (:1173), the "
                "overwrite_filter In('contract_id', ids) (:1214), and the post-write verify join "
                "(:1226-1228)."
            ),
            "key_is_stable": "stable",
            "crosses_spaces": True,
            "declared_mapping": (
                "NONE. Same three-rendering class as PATH A and it is not hypothetical here: this "
                "table is addressed as a 2-TUPLE at :202/:1154/:1222 and as a DOTTED 3-PART Trino "
                "string 'iceberg.globgrph.graph_contracts' by the Trino/fedobs consumers of the "
                "globgrph namespace. A string-equality join key on artifact identity splits one table "
                "into multiple rows silently. Flagged to 2.0.0_SA_COO~X as a join-key input; the "
                "normalisation is not this seat's to build (CCX3-AC8)."
            ),
            "basis": "inferred",
            "basis_by_field": {
                "identity_space": "measured",
                "key_is_stable": "measured",
                "crosses_spaces": "measured",
                "declared_mapping": "inferred",
            },
            "evidence": (
                "derive_runner.py:202, :1154, :1163, :1173, :1214, :1222 @ " + PIN + ". "
                "declared_mapping is basis='inferred' for the Trino rendering SPECIFICALLY: I measured "
                "the dotted 3-part form for graph_nodes/graph_edges directly "
                "(.tools/_trino_fed.py:44, fedobs_views.sql:34) and am reasoning from the shared "
                "namespace to graph_contracts rather than from a line I read for THIS table. The "
                "tuple-form renderings ARE measured."
            ),
            "owner": OWN_COMP,
        },
        "failure_mode": {
            "returns_on_failure": (
                "FAILS CLOSED, repeatedly and by design -- this is the most defensive path in the "
                "file. Unstampable ratified_at pin -> print ERROR, return 1, NOTHING written "
                "(:1204-1206). Post-write integrity gate: re-reads the table (:1222), checks each "
                "written row (:1231), and on any failure prints 'ERROR: WRITE_VERIFY_GATE FAILED' and "
                "returns 1 (:1233-1236). Already-present id without --overwrite -> SKIPPED with a "
                "reason string (:1163), not silently merged."
            ),
            "distinguishable_from_true_negative": "yes",
            "silent_degrade_paths": [
                "The ENSURE half is the exception to this path's fail-closed character, and the "
                "asymmetry is worth stating plainly: when reached from the NIGHTLY (:305) a failure is "
                "swallowed into 'WARN: GRAPH_CONTRACTS_ENSURE_FAIL' on an rc=0 run (:306-308). That is "
                "a deliberate trade -- the comment at :303-304 says a contracts-ensure failure must "
                "not fail the nightly graph commit -- but a consumer scoring the nightly on exit code "
                "cannot see it.",
                "The WRITE_VERIFY gate re-reads through the SAME catalog client that just wrote "
                "(:1222). It is a genuine read-back and it caught the real period_defs-wipe bug, but "
                "it shares an instrument with the write: a catalog-layer fault that corrupted both the "
                "write and the read-back identically would pass the gate. This is a residual, not an "
                "observed defect.",
            ],
            "basis": "measured",
            "evidence": (
                "derive_runner.py:1163, :1204-1206, :1222-1236, :303-308 @ " + PIN + ". "
                "distinguishable_from_true_negative='yes' is MEASURED from structure: every failure "
                "branch on the load path returns a non-zero rc AND prints a distinct ERROR string, so "
                "'nothing was written because it failed' and 'nothing was written because there was "
                "nothing to write' (:1163 skip, which prints its own reason) have different, readable "
                "signatures. This is the opposite of PATH A's empty-input case, in the same file -- "
                "which is why the two paths could not honestly be carded as one."
            ),
            "owner": OWN_CVO,
        },
    },
    "verdict": {
        "standing": "QUALIFIED",
        "why": (
            "All seven rows measured against source at " + PIN + "; the ENSURE half is EXERCISED live "
            "(2026-08-27T02:10:24Z, 'GRAPH_CONTRACTS_ENSURED'), the LOAD half is measured at source "
            "and NOT exercised by me. Qualified on three named limits: (1) coverage carries NO "
            "denominator -- the live table row count is unreachable from this device and I refused a "
            "producer self-report substitute; (2) the LOAD path's last-run age is UNMEASURED, so no "
            "Rule 25 dormancy verdict is offered in either direction -- an absent trigger is a "
            "compliance fact, not a liveness fact; (3) mutation_policy='append_only' is the enum's "
            "closest member but the scoped --overwrite escape at :1214 is real and must not be read as "
            "immutability. Nothing here blocks load-bearing use of graph_contracts; all three limits "
            "constrain what a consumer may conclude from this card."
        ),
        "blocking_defects": [],
    },
    "forward_disposition": {
        "standing": "undecided",
        "set_by": None,
        "basis": "absent",
        "evidence": (
            "CCX3-AC8: zero commits by this lane touching derive_runner.py. The append_only enum "
            "under-expression is NAMED for the contract owner, not patched here. basis='held' -- this "
            "is a scope assertion, not a measurement."
        ),
        "decided_utc": None,
    },
}

# ---------------------------------------------------------------------------
# CARD 3 -- comp_aws_cli.py  (the UNMEASURED-write-paths subject)
# ---------------------------------------------------------------------------
COMP_AWS = {
    "schema_version": 2,
    "carded_by": CARDED_BY,
    "subject": {
        "id": "org/modules/graph/comp_aws_cli.py",
        "kind": "tool",
        "declared_domain": (
            "The comp-aws CLI module. AS A MATERIALIZER its domain is ONE write path: the "
            "iceberg-commit verb (cmd_iceberg_commit, :2964-3101), which overwrites "
            "globgrph.graph_nodes and globgrph.graph_edges from a graph JSON. The module's OTHER "
            "responsibilities -- deriving the cloud graph from live AWS (cmd_derive, consumed by "
            "derive_runner.py:101) -- are READS and are out of this card's domain."
        ),
    },
    "as_of": AS_OF,
    "process": {
        "methodology": {
            "how": (
                "*** THE TO LEFT write_paths AS 'UNMEASURED -- yours to resolve'. RESOLVED: ONE WRITE "
                "PATH, TWO TABLES. NOT a path-multiplicity surprise. *** "
                "All four Iceberg write operations in this 3174-line module live inside a SINGLE "
                "function, cmd_iceberg_commit() (:2964-3101): create_table for nodes (:3034), "
                "create_table for edges (:3047), nodes_table.overwrite (:3051), edges_table.overwrite "
                "(:3091). They share one invocation, one mechanism (full-table overwrite), one "
                "authority and one trigger, which is the same shape the decomp already treats as ONE "
                "path in derive_runner PATH A (graph_nodes + graph_edges through one helper). "
                "Mechanically: namespace create (:3013, exception-swallowed), then load-or-create each "
                "table against a locally-declared Schema (:3021-3037 nodes, :3038-3048 edges), then "
                "overwrite each from a pa.table built by list comprehension over all_nodes/all_edges. "
                "The edges branch runs an endpoint-resolution guard FIRST (:3072-3089) and REFUSES the "
                "overwrite with RC_FAIL if any edge has an empty endpoint."
            ),
            "determinism": "deterministic",
            "inference_detail": None,
            "composes": [
                ref("json:--graph",
                    "a graph JSON supplied via the --graph flag, typically this module's own "
                    "cmd_derive output @ " + PIN + ". Unlike PATH A this verb does not itself read "
                    "live AWS; it consumes an already-materialised graph, so batch_ts at :3057/:3097 "
                    "is its only per-run minted value."),
                ref("nessie:opal-globgrph:main",
                    "pyiceberg against a Nessie REST catalog at the --nessie-uri argument"),
            ],
            "invents": [
                ref("graph_nodes.snapshot_ts",
                    "and graph_edges.snapshot_ts, set to batch_ts on every row at :3057 and :3097"),
                ref("graph_edges.layer",
                    "the hardcoded literal 'aws' on EVERY edge row at :3096. THIS IS A CONSTANT here, "
                    "whereas derive_runner PATH A reads a per-edge layer and only DEFAULTS to 'aws' "
                    "at :372. The two writers of this one table disagree about how layer is "
                    "determined, and because both full-overwrite, whichever ran last decides."),
            ],
            "basis": "measured",
            "basis_by_field": {
                "how": "measured",
                "determinism": "measured",
                "composes": "measured",
                "invents": "measured",
            },
            "evidence": (
                "org/modules/graph/comp_aws_cli.py:2964-3101 (the whole function), :3012 (ns), :3032 "
                "(nodes_id), :3034, :3045 (edges_id), :3047, :3051, :3072-3089 (the endpoint guard), "
                ":3091, :3096 @ " + PIN + ". "
                "THE ONE-PATH FINDING IS AST-MEASURED, NOT EYEBALLED: an ast.FunctionDef enclosure "
                "test over the four write linenos returned cmd_iceberg_commit (2964-3101) for all "
                "four. The same AST pass is what makes the count trustworthy at all -- a naive "
                "write-token census over this file returns 71 hits, of which 67 are list.append on "
                "locals (nodes, resources, behaviors, ...). Exactly the trap the TO named."
            ),
            "owner": OWN_COMP,
            "materializer_standing": "superseded",
            "declared_opinions": [
                "*** A SELF-DESCRIPTION UNDER TEST, NOT ACCEPTED. *** The in-source comment at "
                ":3068-3071 states this verb 'is the stale duplicate of derive_runner.commit_to_"
                "iceberg', that it has had '2 invocations ever', and that it 'is recommended for "
                "deprecation rather than maintenance'. I am carrying the SUPERSEDED standing on the "
                "parts I could corroborate and REFUSING the part I could not. CORROBORATED "
                "INDEPENDENTLY: it writes the same two tables as derive_runner PATH A (:3032/:3045 vs "
                "derive_runner :281/:292); no EventBridge rule or Scheduler schedule targets it "
                "(137 + 18 sweep); no caller exists outside its own argparse dispatch (:3149, :3154); "
                "and derive_runner imports this module but calls cmd_derive (:101), NOT this verb. "
                "*** NOT CORROBORATED: the '2 invocations ever' count. *** That is a producer "
                "self-report about its own history, at an unstated vintage, and I have no instrument "
                "for it -- so it is not carried as a measured value anywhere on this card.",
                "NAME COLLISION worth flagging: infra/aws/terraform/globgrph/item2a.tf:3 describes the "
                "NIGHTLY as 'comp-aws derive -> Nessie iceberg-commit'. That prose names PATH A's "
                "internal commit, NOT this module's iceberg-commit VERB. Two different things share a "
                "phrase, and the TF comment is the more authoritative-looking of the two. A reader "
                "resolving 'iceberg-commit' from that line lands on the wrong writer."
            ],
        },
        "cadence": {
            "declared_rhythm": None,
            "actual_trigger": (
                "none-found. This is a manual CLI verb: argparse subparser 'iceberg-commit' at :3149, "
                "bound to cmd_iceberg_commit at :3154. Reachable only as `comp-aws iceberg-commit` by "
                "an operator. BOTH TRIGGER PLANES SWEPT AND BOTH ARE NEGATIVE: aws events list-rules "
                "= 137 rules, aws scheduler list-schedules = 18 schedules, zero targeting this verb. "
                "The module IS baked into the nightly container (Dockerfile:53) but the container's "
                "CMD is derive_runner.py (:186), which calls cmd_derive (:101) and never this verb -- "
                "so PRESENT IN THE IMAGE is not TRIGGERED, and the two read identically to a "
                "file-level census."
            ),
            "live_matches_declared": "not_applicable",
            "live_instance_age": (
                "UNMEASURED. There is no log group, no ECS task and no rule for this verb, so this "
                "device has no instrument for when it last ran. "
                "*** RULE 25: I DO NOT RETURN A DORMANCY VERDICT HERE. *** The source comment claims 2 "
                "lifetime invocations, which would imply dormancy, but that is the self-report I "
                "declined above. 'No trigger found' is a COMPLIANCE fact; it is not a LIVENESS fact, "
                "and an operator ran this verb at least twice by its own account without any trigger "
                "existing. Calling it dormant would convert an absence of instrument into a "
                "measurement."
            ),
            "basis": "absent",
            "basis_by_field": {
                "declared_rhythm": "measured",
                "actual_trigger": "measured",
                "live_matches_declared": "measured",
                "live_instance_age": "absent",
            },
            "evidence": (
                "Scalar is the FLOOR, not a summary: the two-plane trigger census IS measured and "
                "negative; live_instance_age has no basis, so the row reports 'absent'. A consumer "
                "wanting the trigger fact should read basis_by_field.actual_trigger, which is "
                "'measured'. "
                "comp_aws_cli.py:3149, :3154 (argparse dispatch) @ " + PIN + "; "
                "infra/aws/globgrph/Dockerfile:53 (COPY of this module) and :186 (CMD is "
                "derive_runner.py); derive_runner.py:101 (calls cmd_derive, not this verb). "
                "aws events list-rules -> 137 names, aws scheduler list-schedules -> 18 names, "
                "auto-paginated and counted client-side, grep for this verb = 0 on both planes. "
                "Repo-wide sweep for callers of cmd_iceberg_commit outside this file returned only "
                ".tools/tool_index.py (a catalogue), org/modules/graph/comp_icedrill.py (a docstring), "
                "infra/aws/globgrph/extract_portal_stitch.py (a docstring) and "
                "org/modules/graph/tests/test_comp_aws_cert_mutants.py (a test) -- no executable "
                "caller."
            ),
            "owner": OWN_COMP,
        },
    },
    "artifact": {
        "persistence": {
            "persisted": True,
            "authority_role": "projection",
            "mutation_policy": "replaceable",
            "form": (
                "Apache Iceberg tables globgrph.graph_nodes and globgrph.graph_edges via pyiceberg + "
                "Nessie REST catalog. NOTE the schemas declared HERE (:3021-3027 nodes, :3038-3043 "
                "edges) are NARROWER than the ones derive_runner declares for the same tables: this "
                "module's nodes schema has 7 fields and NO 'source' and NO 'props' column; "
                "derive_runner's has 9 including both (:270-280). Two writers, one artifact, "
                "divergent schema declarations."
            ),
            "basis": "inferred",
            "basis_by_field": {
                "persisted": "measured",
                "authority_role": "inferred",
                "mutation_policy": "measured",
                "form": "measured",
            },
            "evidence": (
                "comp_aws_cli.py:3021-3048 (both Schema declarations), :3051 + :3091 (unfiltered "
                "overwrite = full replace) vs derive_runner.py:270-292 @ " + PIN + ". "
                "authority_role='projection' inherits PATH A's reasoning -- same tables, same "
                "derived-from-AWS character. The SCHEMA DIVERGENCE is the sharp finding and it is "
                "measured by direct comparison of the two NestedField lists: because both writers "
                "issue a FULL overwrite, whichever ran last determines the table's shape."
            ),
            "owner": OWN_COMP,
        },
        "location": {
            "home": (
                "nessie:main -> globgrph.graph_nodes and globgrph.graph_edges. Namespace bound at "
                "comp_aws_cli.py:3012 ns = \"globgrph\"; table names bound as literal 2-tuples at "
                ":3032 nodes_id = (ns, \"graph_nodes\") and :3045 edges_id = (ns, \"graph_edges\"). "
                "Warehouse from the --warehouse argument."
            ),
            "projection_of": [
                ref("json:--graph",
                    "the graph JSON handed to --graph, itself derived from live AWS control-plane "
                    "state for account 313476888478"),
            ],
            "co_resident_stores": [
                ref("globgrph.graph_contracts",
                    "same namespace; this module never addresses it"),
                ref("globgrph.cse", "0.7.0_AE_CloudOps~X's wave-3 subject"),
                ref("globgrph.resource_summaries", "0.7.0_AE_CloudOps~X's wave-3 subject"),
            ],
            "basis": "measured",
            "evidence": "comp_aws_cli.py:3012, :3032, :3045 @ " + PIN + ".",
            "owner": OWN_COMP,
        },
    },
    "trust": {
        "coverage": {
            "universe": (
                "Every node and edge in the graph JSON handed to `comp-aws iceberg-commit --graph "
                "FILE` on a given invocation."
            ),
            "denominator": None,
            "denominator_absent_reason": (
                "ABSENT because the verb has no observed invocation to take a denominator FROM. There "
                "is no log group, no ECS task and no scheduled run for it, so unlike PATH A -- where I "
                "could quote 27067/60872 from a specific run -- there is no run here to count. "
                "Fabricating one from the source comment's '2 invocations ever' would be quoting a "
                "self-report as a measurement."
            ),
            "explicitly_out": [
                "cmd_derive and every other verb in this 3174-line module -- they are READS; this "
                "card's domain is the single write path",
                "globgrph.graph_contracts -- never addressed here",
                "*** CCX3-AC7: THE BOUND IS ENUMERABLE AND CLOSED, BUT THE WRITER POPULATION IS NOT. "
                "*** The table names this path can write are bound as module-local literals at :3032 "
                "and :3045 -- so the bound set is exactly {globgrph.graph_nodes, globgrph.graph_edges} "
                "and it is ENUMERABLE; this path cannot write a table it does not name. The WRITER "
                "population of those two tables is a different question and is NOT closed. MEASURED: "
                "THREE writers of globgrph.graph_nodes. " + "ESTATE CENSUS, INDEPENDENT INSTRUMENT, DENOMINATOR PRINTED: 7236 .py files swept under "
                "infra/, org/modules/, .tools/, data/, workflows/, excluding vendored "
                "pyiceberg-nessie-deps and __pycache__; 33 files NAME graph_nodes; 5 carry a "
                "strong non-append Iceberg write op by AST. THREE of those five write "
                "globgrph.graph_nodes itself: [1] derive_runner.py PATH A, FULL overwrite, "
                "nightly; [2] org/modules/graph/comp_aws_cli.py:3051, FULL overwrite, "
                "untriggered; [3] infra/aws/lambda/globgrph/incremental_updater/"
                "lambda_function.py, table_id bound at :434 and written at :501 with "
                "table.overwrite(pa_table, overwrite_filter=combined_filter) -- a SCOPED "
                "delete+append, NOT a full replace. The other two of the five write different "
                "tables (cse_store.py, resource_summaries_store.py). THIS IS A DIFFERENT "
                "INSTRUMENT ON A DIFFERENT POPULATION from the AST enclosure test that "
                "established the per-file write paths: that one asked which call sites in THOSE "
                "TWO FILES are table ops; this one asks who in the ESTATE names and writes this "
                "table. Only the second question can find a writer the first cannot see, and it "
                "found one." + " This card asserts no "
                "completeness about who else may write them; it reports what one estate-wide sweep "
                "found, with its denominator printed.",
            ],
            "basis": "absent",
            "basis_by_field": {
                "universe": "measured",
                "denominator": "absent",
                "explicitly_out": "measured",
            },
            "evidence": (
                "Scalar is the FLOOR: the enumerable-bound finding is measured, the denominator has "
                "no basis because the verb has no observed run to count. "
                "comp_aws_cli.py:3032, :3045 (the literal bindings that make the bound enumerable) @ "
                + PIN + "; the other writers at derive_runner.py:281, :292, :345, :376 and "
                "infra/aws/lambda/globgrph/incremental_updater/lambda_function.py:434, :501. " + "ESTATE CENSUS, INDEPENDENT INSTRUMENT, DENOMINATOR PRINTED: 7236 .py files swept under "
                "infra/, org/modules/, .tools/, data/, workflows/, excluding vendored "
                "pyiceberg-nessie-deps and __pycache__; 33 files NAME graph_nodes; 5 carry a "
                "strong non-append Iceberg write op by AST. THREE of those five write "
                "globgrph.graph_nodes itself: [1] derive_runner.py PATH A, FULL overwrite, "
                "nightly; [2] org/modules/graph/comp_aws_cli.py:3051, FULL overwrite, "
                "untriggered; [3] infra/aws/lambda/globgrph/incremental_updater/"
                "lambda_function.py, table_id bound at :434 and written at :501 with "
                "table.overwrite(pa_table, overwrite_filter=combined_filter) -- a SCOPED "
                "delete+append, NOT a full replace. The other two of the five write different "
                "tables (cse_store.py, resource_summaries_store.py). THIS IS A DIFFERENT "
                "INSTRUMENT ON A DIFFERENT POPULATION from the AST enclosure test that "
                "established the per-file write paths: that one asked which call sites in THOSE "
                "TWO FILES are table ops; this one asks who in the ESTATE names and writes this "
                "table. Only the second question can find a writer the first cannot see, and it "
                "found one."
            ),
            "owner": OWN_COMP,
        },
        "key": {
            "identity_space": (
                "TABLE identity: pyiceberg 2-tuple (namespace, table). ROW identity: node_id "
                "(required=True) for nodes; (src_id, dst_id, edge_type) (all required=True) for edges. "
                "*** required=True IS SATISFIED BY THE EMPTY STRING, and that is not a hypothetical "
                "here -- it is the recorded mechanism of the A11 defect on this exact function. ***"
            ),
            "key_is_stable": "stable",
            "crosses_spaces": True,
            "declared_mapping": (
                "NONE -- same three-rendering split as PATH A, and this module supplies one of the "
                "renderings: the 2-tuple at :3032/:3045, against the dotted 2-part form at "
                "derive_runner.py:1435-1436 and the dotted 3-part Trino form at .tools/_trino_fed.py:44 "
                "and fedobs_views.sql:34. One artifact, three addressings, no normaliser."
            ),
            "basis": "measured",
            "evidence": (
                "comp_aws_cli.py:3021-3024, :3038-3040 (the required=True NestedFields), :3032, :3045; "
                "the A11 record at :3062-3071 and its regression test at "
                "org/modules/graph/tests/test_comp_aws_cert_mutants.py:400-404; "
                ".tools/_trino_fed.py:44; infra/aws/globgrph/fedobs/fedobs_views.sql:34; "
                "derive_runner.py:1435-1436 @ " + PIN + "."
            ),
            "owner": OWN_COMP,
        },
        "failure_mode": {
            "returns_on_failure": (
                "EDGES: fails closed since the A11 fix. The endpoint resolver _nid tries "
                "'source'/'src' then 'target'/'dst' (:3072-3080); any edge resolving to an empty "
                "endpoint triggers a refusal -- prints the offender, prints 'REFUSING to overwrite "
                "globgrph.graph_edges', returns RC_FAIL (:3081-3089). "
                "NODES: NO equivalent guard. The nodes branch (:3049-3060) overwrites unconditionally "
                "on a truthy all_nodes, with n.get('id','') defaulting to the empty string per row. "
                "NAMESPACE: create_namespace failure is swallowed by a bare `except Exception: pass` "
                "(:3013-3015)."
            ),
            "distinguishable_from_true_negative": "no",
            "silent_degrade_paths": [
                "*** THE HISTORICAL DEFECT, RECORDED AT THE SITE (:3062-3071, CVO 2026-07-10): *** "
                "this function read e['src']/e['dst'] while both edges.append sites in the module emit "
                "{'source','target'}, so _nid returned '' for EVERY edge and graph_edges was "
                "overwritten with empty src_id/dst_id on all rows. It was SILENT precisely because the "
                "schema's required=True is satisfied by ''. The remedy landed and IS the :3081-3089 "
                "guard -- so the edges arm is now loud. I am recording it because it is the clearest "
                "measured instance in this wave of a NOT-NULL constraint failing to be an "
                "IS-MEANINGFUL constraint.",
                "The nodes arm still carries the shape the edges arm was fixed for: "
                "n.get('id', '') at :3052 defaults to '' and no guard rejects it, so a node list with "
                "unresolvable ids overwrites graph_nodes with empty node_id rows and returns RC_OK. "
                "The asymmetry is measured, not alleged: the guard exists at :3081-3089 for edges and "
                "has no counterpart before :3051. NAMED, NOT FIXED (CCX3-AC8) -- and note this verb is "
                "recommended for deprecation, so the correct remedy may be removal rather than a "
                "second guard. That call is not this seat's.",
                "`except Exception: pass` on create_namespace (:3013-3015) converts an instrument "
                "failure into a verdict -- a permissions or connectivity fault reads identically to "
                "'namespace already exists'.",
                "Both overwrites are full-table replaces with no filter, and this module's declared "
                "schemas are NARROWER than derive_runner's for the same tables (no 'source', no "
                "'props'). An invocation of this verb after a nightly can therefore REMOVE columns the "
                "nightly writes -- last-writer-wins on shape, not merely on rows.",
            ],
            "basis": "measured",
            "basis_by_field": {
                "returns_on_failure": "measured",
                "distinguishable_from_true_negative": "measured",
                "silent_degrade_paths": "measured",
            },
            "evidence": (
                "comp_aws_cli.py:3013-3015 (bare except), :3049-3060 (unguarded nodes overwrite), "
                ":3052 (the '' default), :3062-3071 (the A11 record), :3072-3089 (the edges guard), "
                ":3091 @ " + PIN + "; the schema-width comparison against derive_runner.py:270-280. "
                "distinguishable_from_true_negative='no' is scoped to the NODES arm: an all-empty "
                "node_id overwrite returns RC_OK and prints a normal 'WRITE OK: N nodes -> "
                "graph_nodes' line, so success and silent corruption share a signature. The EDGES arm "
                "alone would score 'yes'; the card takes the weaker of the two because the subject is "
                "the write path as a whole."
            ),
            "owner": OWN_COMP,
        },
    },
    "verdict": {
        "standing": "QUALIFIED",
        "why": (
            "All seven rows measured against source at " + PIN + " and against both live trigger "
            "planes. The TO's UNMEASURED write-path question is RESOLVED: ONE write path, two tables, "
            "one function, one mechanism -- NOT a BLOCKING path-multiplicity surprise, and the "
            "measurement (AST enclosure test over all four write linenos) is stated so it can be "
            "re-run. QUALIFIED, not SOUND, on four named defects, none of which blocks USE of this "
            "card: (1) the nodes arm has no endpoint guard and will overwrite graph_nodes with empty "
            "node_id rows at RC_OK -- the same shape the edges arm was repaired for; (2) this "
            "module's declared schemas for graph_nodes/graph_edges are narrower than derive_runner's "
            "for the SAME tables, and both writers full-overwrite, so shape is last-writer-wins; "
            "(3) a bare `except Exception: pass` on namespace creation turns instrument failure into a "
            "verdict; (4) no denominator -- this verb has no observed run to count. "
            "It is NOT UNSOUND: the verb is untriggered on both planes and has no executable caller, "
            "so the nodes-arm defect is latent rather than firing nightly. It would become UNSOUND the "
            "moment anything scheduled it."
        ),
        "blocking_defects": [],
    },
    "forward_disposition": {
        "standing": "undecided",
        "set_by": None,
        "basis": "absent",
        "evidence": (
            "CCX3-AC8: zero commits by this lane touching comp_aws_cli.py. The unguarded nodes arm is "
            "NAMED for " + OWN_COMP + " and routed to 3.0.0_SA_CVO, NOT patched -- and because the "
            "source recommends this verb for deprecation, adding a guard may be the wrong remedy "
            "entirely. Choosing between guard and removal is the owner's call, not the carder's. "
            "basis='absent', set_by=null -- this lane may not dispose of its own subject."
        ),
        "decided_utc": None,
    },
}

CARDS = [
    ("W3-bsft_derive_runner_PATH_A_graph_nodes_edges.json", PATH_A),
    ("W3-csnj_derive_runner_PATH_B_graph_contracts.json", PATH_B),
    ("W3-ggoq_comp_aws_cli_iceberg_commit.json", COMP_AWS),
]


def main() -> int:
    import jsonschema

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)

    # NEGATIVE CONTROL: the validator must be able to REJECT, or a clean pass
    # below proves nothing. A control that cannot fail is not a control.
    try:
        validator.validate({"schema_version": 2})
        print("ERROR: NEG-CONTROL DID NOT FIRE -- validator accepted an empty card. "
              "Every PASS below is therefore UNMEASURED.")
        return 2
    except jsonschema.ValidationError:
        print("OK: NEG-CONTROL FIRED -- validator rejects a malformed card, so a PASS is meaningful.")

    rc = 0
    pins = set()
    stamps = set()
    for name, card in CARDS:
        errs = sorted(validator.iter_errors(card), key=lambda e: list(e.path))
        if errs:
            rc = 1
            print(f"FAIL: {name} -- {len(errs)} validation error(s)")
            for e in errs[:8]:
                print(f"   at {'/'.join(str(p) for p in e.path) or '<root>'}: {e.message[:160]}")
            continue
        (OUT / name).write_text(json.dumps(card, indent=2, ensure_ascii=True) + "\n",
                                encoding="utf-8")
        pins.add((card["as_of"]["commit_ish"], card["as_of"]["graph_vintage"]))
        stamps.add(card["as_of"]["carded_utc"])
        print(f"OK: {name} VALIDATES against SUBSTRATE_CARD.v2 -- written")

    # CCX3-AC2: prove the wave pin is byte-identical, do not assert it.
    print(f"AC2 wave-pin distinct (commit_ish, graph_vintage) pairs across {len(CARDS)} cards: "
          f"{len(pins)} (must be 1)")
    print(f"AC2 distinct carded_utc values: {len(stamps)} (must be 1; grain=PER-BATCH, one clock read)")
    if len(pins) != 1 or len(stamps) != 1:
        print("ERROR: AC2 FAILED -- the wave pin is not uniform across this lane's cards.")
        rc = 1

    # ASCII-only guard (CLAUDE.md section 4: no non-ASCII in production output).
    for name, _ in CARDS:
        p = OUT / name
        if not p.exists():
            continue
        raw = p.read_bytes()
        bad = [i for i, b in enumerate(raw) if b > 127]
        print(f"ASCII {name}: {len(bad)} non-ASCII byte(s)")
        if bad:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
