#!/usr/bin/env python3
"""Wave-2 substrate cards, part 2 of 2 (TO-W2-DTX2, the STORES).

Split from build_cards.py only for file size; identical contract, identical helpers.
Both emit into this directory and both are deterministic.

WAVE-2 ANCHOR 100e7ea130. NO DEPRECATION VERDICTS.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHOR = "100e7ea130"
GRAPH_VINTAGE = "kuzu_nessie_db@2902399899597701830"
CARDED = "2026-08-26T22:55:00Z"
ME = "0.4.0_DT_ClientPlatform~X"
ORDER = {"measured": 3, "inferred": 2, "held": 1, "absent": 0}


def ref(id_, note=None):
    assert " -- " not in id_ and " (" not in id_, "joinable_ref id carries prose: %r" % id_
    return {"id": id_, "note": note}


def row(basis, evidence, owner, **kw):
    """Enforce the FULL floor rule; the schema can only enforce the 'measured' case."""
    bbf = kw.get("basis_by_field")
    if bbf:
        floor = min(bbf.values(), key=lambda v: ORDER[v])
        if ORDER[floor] < ORDER[basis]:
            basis = floor
    d = {"basis": basis, "evidence": evidence, "owner": owner}
    d.update(kw)
    return d


def card(token, sid, kind, domain, methodology, cadence, persistence, location,
         coverage, key, failure_mode, standing, why, blocking=None):
    return token, {
        "schema_version": 2, "carded_by": ME,
        "subject": {"id": sid, "kind": kind, "declared_domain": domain},
        "as_of": {"carded_utc": CARDED, "commit_ish": ANCHOR, "graph_vintage": GRAPH_VINTAGE},
        "process": {"methodology": methodology, "cadence": cadence},
        "artifact": {"persistence": persistence, "location": location},
        "trust": {"coverage": coverage, "key": key, "failure_mode": failure_mode},
        "verdict": {"standing": standing, "why": why, "blocking_defects": blocking},
    }


WH = "s3://opal-313476888478-globgrph/warehouse/globgrph/"
CARDS = []

# ---------------------------------------------------------------- W2-coth : the LOCAL kuzu
CARDS.append(card(
    "coth", "kuzu_nessie_db", "projection",
    "the canonical LOCAL kuzu traversal projection of the Iceberg/Nessie graph -- the default "
    "surface comp-kuzu opens with no --db-path",
    row("measured",
        "comp-kuzu's provenance header read in-session: source nessie, nodes snapshot "
        "2902399899597701830, edges snapshot 6557038275462806297, nodes metadata resolved to "
        "warehouse/globgrph/graph_nodes_4c6c23bd-.../metadata/00000-9c6dea4d-....metadata.json. "
        "Loaded by kuzu_nessie_load.py (full) or kuzu_incremental_refresh.py (incremental); "
        "WAREHOUSE_BUCKET and WAREHOUSE_NS_PREFIX are literals at kuzu_nessie_load.py:40-41.",
        "0.8.0_AE_CloudComp lane (NFRA_KUZUSPLIT)",
        how="A kuzu database rebuilt from the Iceberg tables. It COMPOSES graph_nodes, "
            "graph_edges, cse and graph_contracts and INVENTS nothing -- every row traces to a "
            "warehouse row. Rebuilt engine-internally when the local pin trails the Nessie HEAD "
            "marker, so an agent never runs a rebuild to answer a traversal.",
        determinism="deterministic",
        composes=[ref("graph_nodes"), ref("graph_edges"), ref("cse"), ref("graph_contracts")],
        invents=[], materializer_standing="canonical",
        declared_opinions=[
            "the HEAD oracle is a writer-stamped _branch_head.main.json marker; mtime-scan was "
            "retired, so 'current' means current-per-marker and a stale marker reads as current",
            "the 26h WARN threshold on per-table cadence",
            "the large-delta gate that sends a post-nightly whole-table delta to the full path"]),
    row("measured",
        "Provenance header read TWICE in this session: built 2026-08-26T14:07:59.485515+00:00 at "
        "both reads, ~4.2h then ~8.8h old, i.e. IT DID NOT REBUILD BETWEEN THEM -- a measured "
        "sameness, not a copied value. Header reports 'Nessie HEAD: current (pin == marker "
        "HEAD)'. Per-table last-write at read: graph_nodes 5.4h, graph_edges 16.1h, cse 14.8h, "
        "graph_contracts 1703.4h.",
        "0.8.0_AE_CloudComp lane",
        declared_rhythm="auto-refresh on Nessie-HEAD-advance; nodes <6h, edges/cse <26h cadences",
        actual_trigger="a comp-kuzu call whose pin trails the branch-head marker",
        live_matches_declared="yes", live_instance_age="built 2026-08-26T14:07:59Z"),
    row("measured",
        "82,567,168 bytes on disk. UNTRACKED and gitignored at infra/aws/globgrph/.gitignore:3. "
        "DEVICE-LOCAL: this row describes THIS DEVICE, and the site-Z copy is a different object "
        "this census never saw.",
        "0.8.0_AE_CloudComp lane",
        persisted=True, authority_role="projection", mutation_policy="replaceable",
        form="kuzu database file"),
    row("measured",
        "Path resolved from comp-heat-independent evidence: comp-kuzu --help reports its "
        "--db-path default as <workspace>/infra/aws/globgrph/kuzu_nessie_db, and the file at "
        "that path is 82,567,168 bytes. 0.8.0_AE_CloudComp~X (73371) independently resolved the "
        "same path to a byte-identical size, and 1.0.0_SA_CTO~X read it separately -- three "
        "seats, and the identity was recoverable only from the TOOL's default, never from a "
        "card's text.",
        "0.8.0_AE_CloudComp lane",
        home="infra/aws/globgrph/kuzu_nessie_db",
        projection_of=[ref("graph_nodes"), ref("graph_edges"), ref("cse"), ref("graph_contracts")],
        co_resident_stores=[
            ref("s3://opal-estate-report/kuzu_nessie_db",
                "a DIFFERENT object sharing this leaf name: 51,068,928 bytes, S3 plane, 20 days older"),
            ref("infra/aws/globgrph/kuzu_db", "an older local kuzu, separate file"),
            ref("infra/aws/globgrph/kuzu_stitch_db", "a third local kuzu, separate file")]),
    row("measured",
        "Queried directly: MATCH (n) RETURN count(n) = 27,035; the header reports 58,224 edges. "
        "Label census: MATCH (n) RETURN label(n), count(*) returns a SINGLE label, CloudNode, at "
        "27,035 -- so the node population is homogeneous by label. Layer census sums exactly: "
        "portal 11,338 + semctl 6,230 + ms 6,047 + aws 2,083 + pipeline 1,337 = 27,035.",
        "0.8.0_AE_CloudComp lane",
        universe="the canonical estate graph as projected from the warehouse",
        denominator="27,035 nodes / 58,224 edges at snapshot 2902399899597701830, across 5 layers",
        explicitly_out=["anything absent from the warehouse tables it composes",
                        "any node created after the pinned snapshot"]),
    row("measured",
        "node_id is the key. ⛔ THE CROSS-SPACE GAP ANDREW NAMED, MEASURED: only 1,730 of 27,035 "
        "node_ids (6.4%) are ARN-shaped; 25,305 are not. The population spans FIVE layers "
        "(portal/semctl/ms/aws/pipeline) and the ARN grammar can only express the aws one -- and "
        "even there it is partial, since layer=aws holds 2,083 nodes against 1,730 ARN-shaped "
        "ids. A sample node carries node_id == arn for an S3 bucket, so the two fields coincide "
        "where an ARN exists and diverge where it does not. NO DECLARED MAPPING to the "
        "'gold:MODULE.function' space used by .comp-graph/graph.json, which nerves_resolve reads.",
        "0.8.0_AE_CloudComp lane",
        identity_space="CloudNode.node_id -- ARN where one exists, otherwise a layer-specific string",
        key_is_stable="unknown", crosses_spaces=True, declared_mapping=None,
        basis_by_field={"identity_space": "measured", "crosses_spaces": "measured",
                        "declared_mapping": "measured", "key_is_stable": "inferred"}),
    row("measured",
        "EXERCISED at three distinct failure depths, each with a reachable control: "
        "(1) a nonexistent LABEL -- MATCH (n:ZzzNotALabel) -> 'ERROR: query failed: Binder "
        "exception: Table ZzzNotALabel does not exist.' LOUD. "
        "(2) a nonexistent PROPERTY -- WHERE n.id = 'zzz' -> 'Binder exception: Cannot find "
        "property id for n.' LOUD, and notable because the real key is node_id, so the obvious "
        "wrong guess fails loudly rather than returning empty. "
        "(3) a genuine VALUE miss on the real key -- WHERE n.node_id = 'zzz_cannot_exist_qqq' "
        "-> returns 0 in 1 row. A clean, correct zero. "
        "So schema errors are LOUD and a true negative is a well-formed 0 -- the two are "
        "distinguishable, which is the strongest failure profile of the stores this lane carded.",
        "0.8.0_AE_CloudComp lane",
        returns_on_failure="Binder exception on a bad label or property; a well-formed 0 on a genuine value miss",
        distinguishable_from_true_negative="yes",
        silent_degrade_paths=["if the branch-head marker is stale, the header reports 'current' "
                              "and the projection answers confidently about an older world"]),
    "QUALIFIED",
    "Fresh, deterministic, owned, auto-refreshing, and the only store this lane carded whose "
    "failure modes are loud at every depth exercised -- schema errors raise and a true negative "
    "returns a clean 0. QUALIFIED, not SOUND, on the KEY row alone: its identity space spans "
    "five layers with an ARN grammar covering 6.4% of the population, and it declares NO mapping "
    "to the symbol space the C3 chain's stage-1 store uses. A join between them cannot be "
    "performed on the key, and that is the axis Andrew named directly.",
    None))

# ---------------------------------------------------------------- W2-yjky : the S3 kuzu
CARDS.append(card(
    "yjky", "s3://opal-estate-report/kuzu_nessie_db", "projection",
    "the kuzu graph object published into the estate-report bucket for the estate-report EC2 "
    "runner to consume as its blast-radius substrate",
    row("inferred",
        "⛔ I HAVE NEVER OPENED THIS OBJECT. Its EXISTENCE, SIZE and VINTAGE are MEASURED by "
        "head-object; everything about HOW IT IS PRODUCED is read from "
        "infra/aws/terraform/estate-report/instance.tf:136-143 @HEAD, which declares it is "
        "'published daily into this same bucket by the early-morning Nessie run and OVERWRITTEN "
        "each day'. That is the CONFIG's account of the producer, not an observation of it. "
        "0.8.0_AE_CloudComp~X (73339) measured the same object independently and states the "
        "identical limit.",
        "estate-report pipeline owner -- 0.7.0_AE_CloudOps lane per EC2 ownership",
        how="Per instance.tf, the early-morning Nessie run publishes the canonical kuzu graph to "
            "this key; the runner drops it at <clone>/infra/aws/globgrph/kuzu_nessie_db, which is "
            "where comp-blast resolves it with no flag. Placing the file IS the integration.",
        determinism="unknown",
        composes=[ref("graph_nodes", "per instance.tf, not observed"),
                  ref("graph_edges", "per instance.tf, not observed")],
        invents=[], materializer_standing="unknown",
        declared_opinions=None,
        basis_by_field={"how": "inferred", "determinism": "absent", "composes": "inferred"}),
    row("measured",
        "DESIRED vs APPLIED, and they disagree. DECLARED: instance.tf:136-138 says published "
        "DAILY and OVERWRITTEN each day. MEASURED: head-object returns LastModified "
        "2026-08-06T21:49:50Z -- 20 DAYS before carding. ⛔ The config's own comment anticipates "
        "a MISSING object ('A MISSING OBJECT MUST READ AS INSTRUMENT_FAILED, NEVER AS no blast "
        "radius') and does NOT cover a STALE one, which is present and answers.",
        "estate-report pipeline owner",
        declared_rhythm="daily, overwritten each day", actual_trigger="the early-morning Nessie run",
        live_matches_declared="no", live_instance_age="20 days at carding"),
    row("measured",
        "head-object: ContentLength 51,068,928, VersionId 1qzIq4TIzcemaprP8Rqq.3AaYvpnMy2O, "
        "ServerSideEncryption AES256. A VersionId is present, so the bucket is versioned and an "
        "overwrite would retain prior bytes.",
        "estate-report pipeline owner",
        persisted=True, authority_role="projection", mutation_policy="replaceable",
        form="kuzu database object"),
    row("measured",
        "aws s3api head-object --bucket opal-estate-report --key kuzu_nessie_db -> rc=0. "
        "POSITIVE CONTROL: head-object on code/estate_report_runner.py returns a DIFFERENT "
        "LastModified in the same run, so the probe discriminates. "
        "⛔ NEAR-MISS DISCLOSED: comp-keys prefix WITHOUT --all displays 40 of 129 keys and this "
        "key falls past the cut, so the default view shows it ABSENT. I had drafted the sentence "
        "calling it absent before head-object corrected me.",
        "estate-report pipeline owner",
        home="s3://opal-estate-report/kuzu_nessie_db",
        projection_of=[ref("graph_nodes", "per instance.tf, not observed"),
                       ref("graph_edges", "per instance.tf, not observed")],
        co_resident_stores=[ref("infra/aws/globgrph/kuzu_nessie_db",
                                "a DIFFERENT object sharing this leaf name: 82,567,168 bytes, local plane, 20 days newer")],
        basis_by_field={"home": "measured", "projection_of": "inferred"}),
    row("inferred",
        "⛔ COVERAGE IS NOT MEASURABLE WITHOUT OPENING THE OBJECT, AND I DID NOT OPEN IT. The "
        "51,068,928-byte size is measured; a node/edge count is not, because reading it would "
        "mean downloading and opening a kuzu database whose contents I make no claim about.",
        "estate-report pipeline owner",
        universe="whatever subset of the estate graph the publishing run wrote 20 days ago",
        denominator=None,
        denominator_absent_reason="The object was never opened by this lane. Size is measured "
            "(51,068,928 bytes) but a row count requires downloading and opening the database, "
            "which was out of scope for a card whose subject is the published artifact. Stating "
            "this rather than inferring a count from the byte size, which would be a guess "
            "dressed as a measurement.",
        explicitly_out=["anything written to the warehouse after 2026-08-06T21:49:50Z"]),
    row("inferred",
        "Not opened, so the internal key space is not observed. IF it is a copy of the canonical "
        "projection its key space would be CloudNode.node_id -- but that is exactly the "
        "inference this card refuses to make, because a 51MB object and an 82MB object are not "
        "the same object and the difference is unexplained.",
        "estate-report pipeline owner",
        identity_space="UNOBSERVED -- the object was not opened",
        key_is_stable="unknown", crosses_spaces=False, declared_mapping=None,
        basis_by_field={"identity_space": "absent", "key_is_stable": "absent",
                        "crosses_spaces": "absent"}),
    row("measured",
        "EXERCISED on the retrieval path, which is the failure this store's CONSUMER actually "
        "meets: head-object on a key that cannot exist returns 'An error occurred (404) when "
        "calling the HeadObject operation: Not Found'. LOUD and distinguishable from the "
        "rc=0 + ContentLength of the real key in the same session. "
        "⛔ BUT THE CONSUMER-SIDE FAILURE IS NOT THE 404: instance.tf states a missing object "
        "must read as INSTRUMENT_FAILED. The measured condition is a 20-day-STALE object, which "
        "returns rc=0 and full bytes -- so the runner receives a confident answer about a "
        "20-day-old world, and NOTHING in the retrieval distinguishes that from a fresh one.",
        "estate-report pipeline owner",
        returns_on_failure="404 Not Found on absence; on staleness, a complete and successful read of old bytes",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=["a stale object returns rc=0 with full bytes, so the declared "
                              "INSTRUMENT_FAILED path never triggers and blast radius is computed "
                              "against a 20-day-old graph"]),
    "UNSOUND",
    "The store EXISTS and is retrievable, and its absence would be loud. It is UNSOUND because "
    "its declared cadence and its measured vintage disagree by 20 days on a DAILY contract, and "
    "the disagreement is invisible to its consumer: the config anticipates a missing object but "
    "not a stale one, so a successful read of 20-day-old bytes is indistinguishable from a "
    "correct read. Three of seven rows additionally rest on inference because the object was "
    "never opened, which this card records rather than papers over.",
    ["declared daily cadence vs 20-day measured vintage",
     "staleness is invisible to the consumer -- the INSTRUMENT_FAILED path covers absence only",
     "coverage and key space unmeasured because the object was not opened"]))

# ---------------------------------------------------------------- W2-xnwo / W2-vlov : warehouse
for tok, tname, tdir, nobj, vintage, cov, univ in [
    ("xnwo", "graph_nodes", "graph_nodes_4c6c23bd-fffa-427e-9cd9-7a9deaa3426d", 180225,
     "2026-08-26T12:50:48Z", "27,035 nodes at the pinned projection snapshot",
     "every estate resource the derive can see, across 5 layers"),
    ("vlov", "graph_edges", "graph_edges_6629328d-a582-46d2-80bc-5059de1a77ce", 612,
     "2026-08-26T02:09:51Z", "58,224 edges at the pinned projection snapshot",
     "every relationship the derive emits between graph_nodes rows"),
]:
    CARDS.append(card(
        tok, WH + tdir, "store",
        "the governed Iceberg/Nessie %s table -- the authoritative warehouse-plane store the "
        "canonical kuzu projection is built from" % tname,
        row("measured",
            "Table located by enumerating the warehouse namespace: aws s3api list-objects-v2 "
            "over warehouse/globgrph/ with full pagination returned 181,412 keys, and table dirs "
            "were derived from key segment 3. This table holds %d objects. Written by "
            "derive_runner.py; graph_nodes additionally by kuzu_incremental_refresh.py. "
            "WAREHOUSE_BUCKET/WAREHOUSE_NS_PREFIX are literals at kuzu_nessie_load.py:40-41."
            % nobj,
            "0.8.0_AE_CloudComp lane (derive path)",
            how="An Iceberg table under a Nessie catalog. Every Nessie REST commit writes a fresh "
                "metadata.json, so table state is anchored to the newest metadata file rather "
                "than to a live Nessie HEAD -- kuzu_nessie_load.py:11-17 records that the Nessie "
                "REST endpoint is in-VPC and unreachable from the dev box.",
            determinism="deterministic",
            composes=[ref("live_aws_estate"), ref("repo_source_tree")],
            invents=[], materializer_standing="canonical",
            declared_opinions=[
                "table state is pinned to the newest *.metadata.json rather than a true Nessie "
                "HEAD, because the REST endpoint is unreachable off-VPC -- a deliberate "
                "substitution the loader documents at its own :11-17"]),
        row("measured",
            "Newest metadata object LastModified %s, computed as max over the MATERIALISED "
            "listing rather than by a paginated --query (which applies PER PAGE and returned "
            "~130 values for this prefix) and not by a lexicographic sort (which reported "
            "2026-06-12 for graph_nodes against a true 2026-08-26, because Iceberg metadata "
            "filenames do not sort chronologically). Both wrong methods were run and discarded "
            "before this figure." % vintage,
            "0.8.0_AE_CloudComp lane",
            declared_rhythm="02:00Z full re-derive plus event-driven CloudTrail incremental" if tok == "xnwo" else "nightly re-derive",
            actual_trigger="schedule, plus CloudTrail events for the incremental path" if tok == "xnwo" else "schedule",
            live_matches_declared="yes",
            live_instance_age="newest metadata %s" % vintage),
        row("measured",
            "%d objects present under the table prefix in a fully paginated listing. Iceberg "
            "tables are append-plus-snapshot: existing data files are not edited, and a new "
            "state is a new metadata.json." % nobj,
            "0.8.0_AE_CloudComp lane",
            persisted=True, authority_role="source", mutation_policy="append_only",
            form="Iceberg table (parquet + metadata.json under a Nessie catalog)"),
        row("measured",
            "Prefix enumerated directly against the bucket with full pagination.",
            "0.8.0_AE_CloudComp lane",
            home=WH + tdir, projection_of=[],
            co_resident_stores=[ref("infra/aws/globgrph/kuzu_nessie_db",
                                    "the local projection built FROM this table")]),
        row("measured",
            "%s, read from comp-kuzu's provenance header in the same session. ⛔ PLANE NAMED: "
            "that count is the PROJECTION plane. The warehouse plane's own row count was NOT "
            "read -- doing so requires opening the Iceberg table through pyiceberg, which this "
            "card did not do. The two planes are known to differ (1.0.0_SA_CTO~X read the "
            "warehouse at 27,061/60,858 against the projection's 27,035/58,224), and reporting "
            "the projection figure as the warehouse figure would be exactly the conflation this "
            "wave exists to prevent." % cov,
            "0.8.0_AE_CloudComp lane",
            universe=univ,
            denominator="%s -- PROJECTION plane; the warehouse-plane row count is unmeasured by this card" % cov,
            explicitly_out=["anything the derive cannot see",
                            "rows written after the pinned snapshot"],
            basis_by_field={"universe": "measured", "denominator": "measured",
                            "explicitly_out": "inferred"}),
        row("inferred",
            "The projection built from this table keys on CloudNode.node_id, of which 1,730 of "
            "27,035 are ARN-shaped -- measured on the PROJECTION. I did NOT open the Iceberg "
            "table itself, so the warehouse-plane column names and key are inferred from the "
            "projection's shape rather than read from the table schema.",
            "0.8.0_AE_CloudComp lane",
            identity_space="node_id as surfaced in the projection; the table's own schema was not read",
            key_is_stable="unknown", crosses_spaces=True, declared_mapping=None,
            basis_by_field={"identity_space": "inferred", "key_is_stable": "absent",
                            "crosses_spaces": "inferred"}),
        row("measured",
            "EXERCISED on the retrieval path with both arms reachable: head-object on "
            "warehouse/globgrph/zzz_no_such_table/metadata/v1.metadata.json returns 'An error "
            "occurred (404) when calling the HeadObject operation: Not Found'. POSITIVE CONTROL: "
            "head-object on a real metadata key of THIS table returns ContentLength 2094 in the "
            "same session. So a missing table is LOUD at the retrieval layer. "
            "⛔ WHAT IS NOT COVERED: the loader pins to the NEWEST metadata.json, so a table "
            "whose newest metadata is old still resolves and returns successfully. Absence is "
            "loud; staleness is silent, and graph_contracts in this same namespace sits 71 days "
            "old while resolving normally.",
            "0.8.0_AE_CloudComp lane",
            returns_on_failure="404 Not Found on a missing table or metadata key",
            distinguishable_from_true_negative="yes",
            silent_degrade_paths=["a stale newest-metadata.json resolves and returns successfully, "
                                  "so a frozen table is indistinguishable from a live one at read time"]),
        "QUALIFIED",
        "The governed, append-only, owned warehouse store with a loud absence failure and a "
        "fresh vintage measured today. QUALIFIED on two honest limits rather than on any defect: "
        "the row count reported here is the PROJECTION plane because the Iceberg table was not "
        "opened, and the key row is inferred from the projection's shape rather than read from "
        "the table schema. Both are stated in basis_by_field rather than smoothed over.",
        None))

written = []
for token, c in CARDS:
    name = c["subject"]["id"].replace("s3://", "").replace("/", "_").replace(":", "_").strip("_")
    path = os.path.join(HERE, "W2-%s__%s.json" % (token, name[:70]))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    written.append((token, os.path.basename(path)))

print("part-2 cards written:", len(written))
for t, n in written:
    print("  W2-%-5s %s" % (t, n))
