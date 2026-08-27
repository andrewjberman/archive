#!/usr/bin/env python3
"""Build the wave-3 substrate cards for TO-W3-DTX3 (the KUZU MATERIALIZERS).

Conforms to org/standards/SUBSTRATE_CARD.v2.schema.json.

WAVE-3 PIN is e48a7466ba -- the decomp's OWN last commit, per 2.0.0_SA_COO~X 74831, which
upheld 0.7.0_AE_CloudOps~X's BLOCKING that every wave-3 TO had been pinned one commit behind
its own decomp by construction (cut_tos.py read `git rev-parse HEAD` at emit time, which
necessarily precedes the decomp commit). The superseded pin d2cf839c79/af384e8da1 is NOT used
here. Every citation below was re-verified byte-identical at e48a7466ba AND in the worktree
with a firing positive control -- see METHOD.

CARDED_UTC GRAIN: **PER-BATCH** (DTX3-AC2 requires the grain be stated). ONE `date -u` read at
2026-08-27T06:36:02Z covers both cards, so `as_of` is byte-identical across them by construction
rather than by my remembering to copy it.

QUALIFY-DO-NOT-FIX (DTX3-AC8): zero commits by this lane touch either carded module. Both were
EXERCISED (read-only w.r.t. the repo -- every exercise wrote into the session scratchpad under
--db-path/--db, never into infra/aws/globgrph/). The defects found are NAMED, not repaired.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# --- THE WAVE PIN (DTX3-AC2): one value, both cards, byte-identical --------------------
PIN = "e48a7466ba"
GRAPH_VINTAGE = "kuzu_nessie_db@2902399899597701830"
CARDED = "2026-08-27T06:36:02Z"          # PER-BATCH, one clock read, never estimated
ME = "0.4.0_DT_ClientPlatform~X"

ORDER = {"measured": 3, "held": 2, "inferred": 1, "absent": 0}

# METHOD, cited once and referenced by the rows rather than retyped (a typed number beside a
# derived one always goes stale -- this lane's own banked class):
_IDENT = ("file byte-identical at e48a7466ba and in the worktree "
          "(git hash-object both sides; positive control: `git diff --name-only e48a7466ba HEAD` "
          "is non-empty, so the comparison can detect change)")
_SWEEP = ("comp-find content sweep, --all, DENOMINATOR PRINTED: 27,093 files scanned in scope, "
          "13 UNREADABLE not searched, 1,948 BINARY not searched")


def ref(id_, note=None):
    """A joinable_ref: identity and description are TWO FIELDS, not one string.

    v2 REJECTS an id containing ' -- ' or ' (' -- the two prose markers that made wave-1
    lineage arrays unjoinable. Asserted here so a bad id fails at BUILD, not at validate."""
    assert " -- " not in id_ and " (" not in id_, "joinable_ref id carries prose: %r" % id_
    return {"id": id_, "note": note}


def row(basis, evidence, owner, **kw):
    """Build a row and ENFORCE THE WHOLE FLOOR RULE rather than trusting myself to hold it.

    The schema enforces only the 'measured' case (JSON Schema cannot express an ordering
    comparison). The half the validator cannot see is the half that would ship silently, so
    the scalar is recomputed here as MIN over basis_by_field."""
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
        "schema_version": 2,
        "carded_by": ME,
        "subject": {"id": sid, "kind": kind, "declared_domain": domain},
        "as_of": {"carded_utc": CARDED, "commit_ish": PIN, "graph_vintage": GRAPH_VINTAGE},
        "process": {"methodology": methodology, "cadence": cadence},
        "artifact": {"persistence": persistence, "location": location},
        "trust": {"coverage": coverage, "key": key, "failure_mode": failure_mode},
        "verdict": {"standing": standing, "why": why, "blocking_defects": blocking},
        # Born UNDECIDED and never set by the carding lane -- describing and deciding are
        # different acts and this seat has a stake in the second.
        "forward_disposition": {"standing": "undecided", "set_by": None,
                                "basis": "absent", "evidence": None, "decided_utc": None},
    }


CARDS = []

# ============================================================ W3-gkih : kuzu_load.py
CARDS.append(card(
    "gkih", "infra/aws/globgrph/kuzu_load.py", "script",
    "materializes a local Kuzu graph DB of AWS cloud shape (tables CloudNode + CloudEdge) from a "
    "GLOBGRPH snapshot tarball in S3 -- the snapshot-tarball loader, one of three Kuzu loaders "
    "sharing this directory",

    # ---- ROW 1 / W3-gkih-1 : methodology (AC3 binding site, AC8 qualify-not-fix) --------
    methodology=row(
        "measured",
        "WRITER CLASS 1, BOUND AT THE CALL SITE AS A LITERAL: kuzu_load.py:142 "
        "'CREATE NODE TABLE IF NOT EXISTS CloudNode(' and kuzu_load.py:147 "
        "'CREATE REL TABLE IF NOT EXISTS CloudEdge(' @e48a7466ba -- both inside _build_schema(), "
        "both string literals, no code path derives a table name from input. THE BOUND SET IS "
        "ENUMERABLE AND IS EXACTLY {CloudNode, CloudEdge}. "
        "WRITE-PATH MULTIPLICITY, the TO's blocking question, MEASURED AS ONE: load() :244-283 "
        "has two branches; the DB-exists-without---force branch :250-253 opens a connection and "
        "writes NOTHING. The single write branch :254-283 is schema-create -> node insert -> edge "
        "insert -> manifest. The --force delete at :257 (shutil.rmtree) / :259 (os.remove) is a "
        "CONDITIONAL PREFIX INSIDE that one path, not an alternative to it: same bound (db_path), "
        "same authority (same CLI, same operator), and it never occurs without the create that "
        "follows. By the TO's own conjunctive test -- mechanism AND bound AND authority, the test "
        "that split derive_runner -- it does not split. NOT carded as two. "
        "QUALIFY-DO-NOT-FIX HOLDS: zero commits by this lane touch this module; the exercises "
        "below wrote only into the session scratchpad via --db-path. " + _IDENT,
        "UNOWNED -- no seat owns the remedy for this module's superseded standing. Last two "
        "authors are 0.8.0_AE_CloudComp~C (cbbe75134c, 2026-07-25) and 0.7.0_AE_CloudOps "
        "(a84de54a5a, 2026-06-12); neither is a standing owner and neither authored the "
        "supersession.",
        how="Reads a cloud-shape snapshot JSON -- either --snapshot-path, or the latest tarball "
            "resolved through s3://opal-313476888478-globgrph/snapshots/latest.txt and extracted "
            "to a temp dir (:66-90). Flattens classes_data into an arn-keyed node dict, dropping "
            "any node without an `arn` (:93-113); synthesises stub nodes in class IMPLICIT for "
            "ARNs that appear only in edges (:116-134); creates the two tables and inserts "
            "row-by-row with one execute() per node and per edge (:150-180). On success writes a "
            "sibling build manifest (:269-279). Uses boto3 rather than a shelled `aws` so it runs "
            "identically on the Linux runner and the Windows dev box (:70-73).",
        determinism="deterministic",
        composes=[ref("kuzu", "kuzu==0.11.3 measured importable at this device"),
                  ref("boto3"),
                  ref("infra/aws/globgrph/_provenance.py"),
                  ref("s3://opal-313476888478-globgrph/snapshots/latest.txt")],
        invents=[ref("the 5-column CloudNode schema",
                     "arn PRIMARY KEY, id, node_type, class, props-as-JSON-string"),
                 ref("the _arn_to_type ARN-to-node_type service map", "kuzu_load.py:34-64"),
                 ref("the IMPLICIT node class for edge-only ARNs", "kuzu_load.py:116-134")],
        materializer_standing="superseded",
        declared_opinions=[
            "ARN is the SOLE node identity; a snapshot node lacking an `arn` key is dropped "
            "silently at :96-98 and NO count of drops is emitted anywhere",
            "an ARN appearing only in an edge is materialised as a stub node in class IMPLICIT "
            "rather than dropped (:116-134)",
            "a stub's node_type is derived from the ARN string by a hand-written service map "
            "(:34-64); an unmapped service becomes svc.upper() and a non-ARN string becomes "
            "UNKNOWN -- so 'UNKNOWN' conflates 'not an ARN' with 'unrecognised'",
            "every node attribute other than id/type/arn is flattened into ONE `props` column as "
            "a JSON string; nothing is typed and nothing is queryable without parsing",
            "an edge whose source or target does not resolve is SKIPPED, counted, and only the "
            "first 5 are printed (:170-180)",
            "IF NOT EXISTS on both DDL statements means a pre-existing table carrying a DIFFERENT "
            "column schema is accepted silently -- which is live risk here, because two sibling "
            "loaders in this same directory declare tables of the same NAME with different columns",
        ],
        basis_by_field={"how": "measured", "determinism": "measured", "composes": "measured",
                        "invents": "measured", "materializer_standing": "measured",
                        "declared_opinions": "measured"},
    ),

    # ---- ROW 2 / W3-gkih-2 : cadence (AC5 trigger+plane+basis, AC6 rule25/26) -----------
    cadence=row(
        "measured",
        "TRIGGER PLANE = none-found, on TWO instruments that fail differently. "
        "(1) REPO-INVOCATION PLANE: " + _SWEEP + " for `kuzu_load` returns 187 hits "
        "(bands HEAD=3 SURFACED=83 CONFIG=67 DOC=34) and ZERO of them is an invocation -- every "
        "hit is a docstring usage line, a 'NOT kuzu_load.py' disambiguation in a sibling tool, an "
        "audit-log echo, a config/doc declaration, or an archive-prediction row. "
        "(2) CONTAINER PLANE, READ FROM THE IMAGE DEFINITION AS AC5 REQUIRES, NOT INFERRED FROM A "
        "RULE TARGET: infra/aws/globgrph/Dockerfile:186 is CMD [\"python\", \"/app/derive_runner.py\"] "
        "-- not this loader. Dockerfile:26 states `kuzu` is imported ONLY by "
        "derive_runner._c2c3_incontainer_reader(); Dockerfile:156 states comp-kuzu and a local Kuzu "
        "DB are ABSENT in-container. kuzu_load.py is not in the image's execution path. "
        "(3) THE DISCRIMINATING ORACLE -- the artifact's own stamp: _provenance.write_manifest is "
        "called UNCONDITIONALLY on every successful build (:269), so a successful run cannot happen "
        "without moving built_at. kuzu_db._build_manifest.json still reads "
        "built_at=2026-06-12T13:55:02.779461+00:00 = 75.68d at 2026-08-27T06:17:47Z. NOTHING HAS "
        "SUCCESSFULLY BUILT THIS ARTIFACT IN 75 DAYS. Evidence would differ if the claim were false. "
        "RESIDUALS, NAMED: a trigger that fires and FAILS leaves no stamp, and a trigger writing to "
        "a non-default --db-path stamps elsewhere -- so the measured claim is scoped to the DEFAULT "
        "artifact, and I did not sweep `aws events list-rules` / `aws scheduler list-schedules`. "
        "DESIRED vs APPLIED: the decomp cell's own write_evidence asserts 'REACHABLE FROM THE LIVE "
        "NIGHTLY'; on the container command and the 75-day stamp that is NOT APPLIED. "
        "RULE 25 (dormancy): 75.68d < 90d, so NOT dormant by the bar -- but the rule's successor "
        "clause is the operative half here, because dormant-because-ABANDONED and "
        "dormant-because-KEY-MIGRATED are byte-identical from age alone. SUCCESSOR IDENTIFIED AND "
        "MEASURED: kuzu_nessie_load.py -> kuzu_nessie_db, built_at 2026-08-26T14:07:59Z (0.67d), "
        "27,035 nodes. THIS IS MIGRATED, NOT ABANDONED. "
        "RULE 26 (device/apply owner), MEASURED FOR THIS SUBJECT AND NOT ASSUMED FROM THE CLASS: "
        "runs on the DEV BOX only; there is no automated applier, so the apply owner is whoever "
        "runs the CLI. The module is NEVER-rule compliant on device-specificity -- :29-30 derive "
        "both _WORKSPACE and DEFAULT_DB_PATH from __file__ rather than hardcoding a drive prefix.",
        "UNOWNED -- there is no cadence owner, no scheduler entry and no automated applier for "
        "this loader on any plane measured.",
        declared_rhythm=None,
        actual_trigger=None,
        live_matches_declared="no",
        live_instance_age="kuzu_db built_at 2026-06-12T13:55:02.779461+00:00 = 75.68 d at "
                          "2026-08-27T06:17:47Z; 1,166 nodes / 2,488 edges; source_vintage "
                          "tarball_key snapshots/20260612/graph-20260612.tar.gz",
        basis_by_field={"declared_rhythm": "measured", "actual_trigger": "measured",
                        "live_matches_declared": "measured", "live_instance_age": "measured"},
    ),

    # ---- ROW 3 / W3-gkih-3 : persistence (AC6) -----------------------------------------
    persistence=row(
        "measured",
        "persisted=true: infra/aws/globgrph/kuzu_db measured on disk at 9,224,192 bytes with a "
        "327-byte sibling manifest. authority_role=projection: every byte is rebuildable from the "
        "S3 snapshot named in its own manifest, and nothing edits it in place, so it governs "
        "nothing (projection_of is named in the location row). mutation_policy=replaceable is "
        "MEASURED, NOT INFERRED FROM THE WORD --force: with the DB present and no --force the "
        "script writes nothing at all (:250-253), and with --force it deletes the whole DB "
        "(:257/:259) and rebuilds from scratch. There is no incremental or partial-update path -- "
        "rebuild-or-nothing is the entire mutation surface. Contrast measured against the sibling "
        "subject: kuzu_stitch_load.py MERGE-upserts and therefore is `editable`, so this value is "
        "NOT a class constant across the two loaders.",
        "UNOWNED -- no seat owns the remedy; the artifact is a dev-box local file with no "
        "lifecycle manager.",
        persisted=True,
        authority_role="projection",
        mutation_policy="replaceable",
        form="Kuzu embedded database materialised as a SINGLE FILE on this device (9,224,192 bytes) "
             "plus a sibling JSON build manifest (327 bytes)",
        basis_by_field={"persisted": "measured", "authority_role": "measured",
                        "mutation_policy": "measured", "form": "measured"},
    ),

    # ---- ROW 4 / W3-gkih-4 : location (AC3 + AC4 WHAT IT WRITES, resolvable) ------------
    location=row(
        "measured",
        "WHAT IT WRITES -- RESOLVABLE NAMES, NOT A DESCRIPTION (AC4). TWO artifacts, both on every "
        "successful run: (1) the Kuzu node table CloudNode and rel table CloudEdge INSIDE the DB at "
        "--db-path, default infra/aws/globgrph/kuzu_db (bound at :30, DERIVED from __file__); "
        "(2) the sibling manifest file infra/aws/globgrph/kuzu_db._build_manifest.json -- path "
        "computed as db_path + '._build_manifest.json' at _provenance.py:34 + :44-46, written from "
        "kuzu_load.py:269. Both were read on disk this session. "
        "THE DB PATH IS UNBOUNDED FROM CLI INPUT: --db-path (:292) accepts an arbitrary path, and "
        "under --force that path is passed straight to shutil.rmtree (:257) / os.remove (:259). So "
        "the TABLE-NAME bound is CLASS 1 and enumerable, while the LOCATION bound is arbitrary "
        "runtime input -- the Class-3 shape displaced from the name axis onto the location axis. "
        "NAMED, NOT FIXED (AC8). "
        "CO-RESIDENCY HAZARD, MEASURED: three Kuzu DBs share this one directory and the two "
        "actively-loaded ones both declare tables literally named CloudNode/CloudEdge with "
        "DIFFERENT columns -- kuzu_load's is (arn PK, id, node_type, class, props) at :142-146, "
        "kuzu_nessie_load's is (node_id PK, arn, node_type, name, layer, drift_class, source, "
        "snapshot_ts, props) measured live via CALL TABLE_INFO('CloudNode'). The estate carries "
        "this as hand-written prose warnings in FOUR sibling tools (.tools/comp-kuzu:9, "
        "canon_motif_scorer.py:73, comp_debt.py:86, comp_detect.py:92) rather than as a schema "
        "guard. " + _IDENT,
        "UNOWNED for the co-residency hazard. 0.4.0_DT_ClientPlatform~X owns this card only.",
        home="infra/aws/globgrph/kuzu_db",
        projection_of=[
            ref("s3://opal-313476888478-globgrph/snapshots/latest.txt",
                "the pointer the loader resolves when --snapshot-path is omitted"),
            ref("s3://opal-313476888478-globgrph/snapshots/20260612/graph-20260612.tar.gz",
                "the tarball the LIVE instance was actually built from, per its own manifest -- "
                "not the current latest.txt target"),
        ],
        co_resident_stores=[
            ref("infra/aws/globgrph/kuzu_nessie_db",
                "the SUCCESSOR surface; same table NAMES, different columns, 27,035 nodes vs 1,166"),
            ref("infra/aws/globgrph/kuzu_stitch_db",
                "the sibling subject's output; same table NAMES, a third column set"),
            ref("infra/aws/globgrph/kuzu_ac7.db", "a 2026-06-12 scratch DB, no live producer found"),
        ],
        basis_by_field={"home": "measured", "projection_of": "measured",
                        "co_resident_stores": "measured"},
    ),

    # ---- ROW 5 / W3-gkih-5 : coverage (AC7 DISCOVERABILITY IS NOT COVERAGE) -------------
    coverage=row(
        "measured",
        "DENOMINATOR PRINTED, AND IT IS A COUNT OF ONE INSTANCE, NOT OF THE WORLD: the live "
        "kuzu_db holds 1,166 nodes / 2,488 edges per its own manifest. Against the successor "
        "surface built from the same estate 75 days later -- kuzu_nessie_db, 27,035 nodes / 58,224 "
        "edges, read live -- that is 4.3% of the successor's node count. "
        "AC7, THE STANDING LIMIT, STATED ON THE FACE: this row describes WHAT THE LIVE INSTANCE "
        "CONTAINS. It asserts NOTHING about completeness of the writer population and nothing about "
        "the AWS resource population. The 1,166 is a count of what one 2026-06-12 tarball happened "
        "to carry, filtered by this loader's declared opinions. Discoverability is not coverage, and "
        "this number measures neither -- it measures one materialisation. "
        "THE 4.3% IS NOT A COVERAGE DEFECT CLAIM: the two DBs were built 75 days apart from "
        "different sources (tarball vs Iceberg) and the successor spans layers this loader never "
        "had (below). Vintage and scope both move between them, so the ratio bounds nothing on its "
        "own -- it is reported as the scale gap that motivates the supersession finding, not as a "
        "measured loss.",
        "UNOWNED",
        universe="AWS resources present in the GLOBGRPH cloud-shape snapshot tarball named by "
                 "snapshots/latest.txt at run time, restricted to nodes carrying an `arn` key, "
                 "plus synthesised stub nodes for ARNs appearing only in edges",
        denominator="1,166 nodes / 2,488 edges in the live instance "
                    "(kuzu_db._build_manifest.json, built 2026-06-12T13:55:02Z); successor "
                    "kuzu_nessie_db at 27,035 nodes / 58,224 edges (2026-08-26T14:07:59Z)",
        explicitly_out=[
            "any snapshot node lacking an `arn` key -- dropped at :96-98, and NO drop count is "
            "emitted, so this exclusion is invisible at run time",
            "any edge whose source or target does not resolve to a loaded node -- skipped and "
            "counted, but only the first 5 are printed (:170-180)",
            "everything the upstream snapshot generator did not collect -- this loader cannot see "
            "past its input tarball",
            "the portal, pipeline, ms and semctl layers entirely -- this loader has no `layer` "
            "column at all (:142-146); the successor carries 5 layers, of which this DB spans none "
            "as a declared field",
        ],
        basis_by_field={"universe": "measured", "denominator": "measured",
                        "explicitly_out": "measured"},
    ),

    # ---- ROW 6 / W3-gkih-6 : key -------------------------------------------------------
    key=row(
        "measured",
        "identity_space measured at :142-144 -- `arn STRING` is the declared PRIMARY KEY and the "
        "raw ARN string is used verbatim as the key (:104-110). key_is_stable=stable: an ARN "
        "survives ordinary change to the resource it names. crosses_spaces=true WITH A MEASURED "
        "HAZARD: the same column also admits NON-ARN synthetic strings -- :38-40 classifies "
        "`event-source::` prefixed keys, and stub ids are whatever the edge carried -- with no type "
        "discriminator column, so a join across id spaces silently mixes ARN and non-ARN members "
        "and nothing in the schema can reject that. "
        "declared_mapping=None is the finding, not a gap in my reading: the successor DB keys on "
        "`node_id`, not `arn` (measured live via CALL TABLE_INFO), so joining kuzu_db to "
        "kuzu_nessie_db requires a hand-written column rename that exists NOWHERE as a declared "
        "mapping -- it survives only as prose warnings in four sibling tools.",
        "UNOWNED -- the missing cross-space mapping has no owner; it is the estate's most-repeated "
        "defect class and is unowned here specifically.",
        identity_space="AWS ARN string, used verbatim as the CloudNode PRIMARY KEY",
        key_is_stable="stable",
        crosses_spaces=True,
        declared_mapping=None,
        basis_by_field={"identity_space": "measured", "key_is_stable": "measured",
                        "crosses_spaces": "measured", "declared_mapping": "measured"},
    ),

    # ---- ROW 7 / W3-gkih-7 : failure_mode (EXERCISED, not read off a docstring) ---------
    failure_mode=row(
        "measured",
        "EXERCISED 2026-08-27T06:2xZ against scratch DBs under --db-path; the repo artifacts were "
        "never touched. THREE distinct behaviours measured, not read from the docstring. "
        "(a) MISSING INPUT IS LOUD: --snapshot-path pointing at a non-existent file raises an "
        "UNCAUGHT FileNotFoundError from :241 with a traceback and rc=1. "
        "(b) THE DANGEROUS ONE -- DB PRESENT AND NO --force: exercised by building a scratch DB "
        "from a 3-node snapshot (loaded 4 with the implicit stub), then re-running the SAME command "
        "against a 9-node snapshot. The run READ the newer snapshot, printed 'INFO: 9 explicit "
        "nodes', then 'INFO: DB already exists ... Use --force to rebuild.', WROTE NOTHING, printed "
        "'OK: Kuzu DB at <path>' and EXITED rc=0. Oracle after the re-run: the DB still held 4 "
        "nodes and the manifest still carried the FIRST run's node_count=4 and its built_at. A "
        "caller that scores this run on rc, or on the trailing 'OK:' line, reads a refresh that did "
        "not happen as a success. "
        "(c) PARTIAL LOAD IS REPORTED AS OK: per-edge failures are caught at :172-180, counted, and "
        "only the first 5 printed; the run still ends 'OK: loaded N nodes + M edges (K edges "
        "skipped)' at rc=0, with the skip count as the only signal. "
        "distinguishable_from_true_negative=no is about case (b): a stale no-op serve is byte-"
        "identical on BOTH rc and the final stdout line to a genuine successful build. The only "
        "discriminator is the manifest's built_at, and the 26-hour age warning that surfaces it "
        "(_provenance.py:41 DEFAULT_AGE_WARN_HOURS = 26.0) lives on the READ side, in comp-kuzu's "
        "provenance header -- NOT on this writer's exit path. The writer cannot tell you it "
        "declined to write.",
        "UNOWNED -- the rc=0-on-no-write path has no owner. NAMED, NOT FIXED (AC8): the module is "
        "not touched by this lane.",
        returns_on_failure="Missing input: uncaught FileNotFoundError + traceback, rc=1 (LOUD). "
                           "DB already present without --force: no write at all, 'OK: Kuzu DB at "
                           "<path>' on stdout, rc=0 (SILENT). Unresolvable edges: skipped and "
                           "counted, run still 'OK:' at rc=0 (PARTIAL, weakly signalled).",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=[
            "DB present and no --force -> writes nothing, prints OK:, exits 0 -- EXERCISED "
            "2026-08-27: 4 nodes retained against a 9-node input, manifest unchanged",
            "snapshot nodes lacking an `arn` key -> dropped at :96-98 with NO count emitted; "
            "unlike the edge skips this exclusion has no run-time signal whatsoever",
            "edges whose endpoints do not resolve -> skipped, only first 5 printed, run still rc=0",
            "IF NOT EXISTS on both DDL statements -> a pre-existing table with a DIFFERENT column "
            "schema is silently accepted, which is a live path given three co-resident DBs "
            "declaring the same two table names",
        ],
        basis_by_field={"returns_on_failure": "measured",
                        "distinguishable_from_true_negative": "measured",
                        "silent_degrade_paths": "measured"},
    ),

    standing="UNSOUND",
    why="EVERY ROW MEASURED, so this is not INCOMPLETE -- it is a verdict about the resource. "
        "UNSOUND is scoped to STANDING AS LOAD-BEARING SUBSTRATE and is NOT a claim the script is "
        "broken: exercised with --force it builds correctly and its manifest is accurate at write "
        "time. Three measured facts block standing on it. (1) SUPERSEDED, corroborated on two "
        "independent instruments: four sibling tools carry hand-written 'NOT kuzu_load.py' warnings "
        "routing readers to kuzu_nessie_load, and the successor DB is 27,035 nodes at 0.67d against "
        "this one's 1,166 at 75.68d. (2) NOTHING FIRES IT: no invocation site across 27,093 files, "
        "and the derive-runner container command is derive_runner.py, so the default artifact has "
        "not been successfully rebuilt in 75.68 days -- measured from a stamp the writer emits "
        "unconditionally. (3) THE DEFAULT INVOCATION SILENTLY DECLINES TO WRITE AND REPORTS rc=0 "
        "WITH 'OK:' -- so wiring this into any schedule as-is produces a permanently frozen DB that "
        "reports success forever, which is precisely the shape a monitor cannot see. "
        "Rule 25 dormancy does NOT fire (75.68d < 90d) and the successor clause resolves this as "
        "MIGRATED, not abandoned -- stated so the verdict is not read as an age finding.",
    blocking=[
        "rc=0 and 'OK:' on the no-write path: kuzu_load.py:250-253 vs :281 -- a stale serve is "
        "indistinguishable from a successful build on both rc and final stdout. UNOWNED.",
        "superseded by kuzu_nessie_load.py with no deprecation marker in the module itself: the "
        "supersession is recorded only as prose in four OTHER files, so a reader who opens "
        "kuzu_load.py alone cannot learn it. UNOWNED.",
        "the default artifact is 75.68d stale with no trigger on any measured plane. UNOWNED.",
    ],
))

# ============================================================ W3-mdiu : kuzu_stitch_load.py
CARDS.append(card(
    "mdiu", "infra/aws/globgrph/kuzu_stitch_load.py", "script",
    "NFRA_GLOBGRPH P2-STITCH step 3 -- materializes a local Kuzu DB (tables CloudNode + CloudEdge) "
    "from the step-2 UNIONED cross-layer graph: the AWS layer, the portal/pipeline layer, and the "
    "inter-system stitch edges between them",

    # ---- ROW 1 / W3-mdiu-1 : methodology (AC3, AC8) ------------------------------------
    methodology=row(
        "measured",
        "WRITER CLASS 1, BOUND AT THE CALL SITE AS A LITERAL: kuzu_stitch_load.py:70 "
        "'CREATE NODE TABLE IF NOT EXISTS CloudNode(' and :74 "
        "'CREATE REL TABLE IF NOT EXISTS CloudEdge(FROM CloudNode TO CloudNode, ' @e48a7466ba. "
        "THE BOUND SET IS ENUMERABLE AND IS EXACTLY {CloudNode, CloudEdge}; no code path derives a "
        "table name from input. "
        "SAME TWO NAMES AS THE SIBLING SUBJECT, DIFFERENT COLUMNS -- kuzu_load.py:142-146 declares "
        "(arn PK, id, node_type, class, props) while :70-72 here declares (node_id PK, arn, "
        "node_type, name, layer, drift_class, source). ONE TABLE NAME, THREE INCOMPATIBLE SCHEMAS "
        "ACROSS THE DIRECTORY once kuzu_nessie_load is counted. "
        "WRITE-PATH MULTIPLICITY MEASURED AS ONE: main() :37-129 is straight-line -- dedup, "
        "optional --force delete (:56-65), DDL, node MERGE, edge MERGE, manifest. The --force "
        "delete is a conditional PREFIX on the same bound with the same authority and never occurs "
        "without the load that follows; by the TO's conjunctive test it does not split. "
        "QUALIFY-DO-NOT-FIX HOLDS: zero commits by this lane touch this module; exercises wrote "
        "only to scratch --db paths. " + _IDENT,
        "UNOWNED -- last substantive author 0.7.0_AE_CloudOps (a84de54a5a, 2026-06-12, the TO-F1 "
        "provenance work); no standing owner.",
        how="Reads the step-2 stitch_graph.json (--in, default infra/aws/globgrph/stitch_graph.json "
            "at :29), dedups nodes by a canonical key that is arn-if-present else id (:33-34, "
            ":49-54, first-seen wins), optionally deletes the DB under --force, creates the two "
            "tables, then MERGE-upserts every node (:78-84) and every edge whose BOTH endpoints "
            "resolved (:88-99). Edges with an unresolved endpoint are skipped and bucketed by "
            "_wild() into 'wildcard/external' vs 'genuine' (:93, :140-145). Prints a per-layer node "
            "count and an UNTYPED_NODES gate, then stamps a sibling build manifest (:116-126).",
        determinism="deterministic",
        composes=[ref("kuzu", "imported lazily inside main() at :44"),
                  ref("infra/aws/globgrph/_provenance.py"),
                  ref("infra/aws/globgrph/stitch_graph.json",
                      "the step-2 input; produced by derive_stitch.py per "
                      "org/modules/graph/graph_status_cli.py:236")],
        invents=[ref("the 7-column CloudNode schema with layer/drift_class/source",
                     "kuzu_stitch_load.py:70-72"),
                 ref("the arn-else-id canonical key reconciliation", "kuzu_stitch_load.py:33-34"),
                 ref("the _wild wildcard/external endpoint classifier",
                     "kuzu_stitch_load.py:140-145")],
        materializer_standing="superseded",
        declared_opinions=[
            "node identity is arn-if-present ELSE id (:33-34), so AWS nodes key on ARN and portal "
            "nodes key on their path/name -- ONE column holding TWO id spaces by design",
            "on a key collision the FIRST node seen wins and later ones are discarded silently "
            "(:53-54); classes_data iteration order therefore decides which duplicate survives",
            "an edge with an unresolved endpoint is dropped, and the drop is EXCUSED as "
            "'wildcard/external' when _wild() matches -- a classifier that treats any id containing "
            "'*' or '::' or ':ecs:' as expected-missing (:140-145)",
            "MERGE rather than CREATE means a re-run UPDATES in place and NEVER DELETES: nodes "
            "removed from the input persist in the DB until someone passes --force",
            "the only quality gate is UNTYPED_NODES == 0 (:105-108, rc at :129); nothing checks "
            "counts, layers or edge resolution against any expectation",
            "IF NOT EXISTS on both DDL statements accepts a pre-existing table with different "
            "columns -- live risk, since two sibling loaders declare these same names differently",
        ],
        basis_by_field={"how": "measured", "determinism": "measured", "composes": "measured",
                        "invents": "measured", "materializer_standing": "measured",
                        "declared_opinions": "measured"},
    ),

    # ---- ROW 2 / W3-mdiu-2 : cadence (AC5, AC6) ----------------------------------------
    cadence=row(
        "measured",
        "TRIGGER PLANE = none-found, same two instruments. "
        "(1) REPO-INVOCATION PLANE: " + _SWEEP + " for `kuzu_stitch_load` returns 70 hits "
        "(bands HEAD=2 SURFACED=21 CONFIG=26 DOC=21), ZERO of them an invocation. "
        "(2) CONTAINER PLANE, READ FROM THE IMAGE DEFINITION: Dockerfile:186 is "
        "CMD [\"python\", \"/app/derive_runner.py\"]; Dockerfile:156 states a local Kuzu DB is "
        "ABSENT in-container. Not in the image's execution path. "
        "(3) THE DISCRIMINATING ORACLE: the manifest is stamped on every successful run (:116), and "
        "kuzu_stitch_db._build_manifest.json still reads built_at=2026-07-07T15:46:38.578615+00:00 "
        "= 50.60d. NOTHING HAS SUCCESSFULLY RUN THIS IN 50 DAYS. "
        "⛔ AND THE INPUT HAS MOVED PAST THE LOAD: the manifest records it loaded a stitch_graph.json "
        "whose mtime was 2026-07-07T15:45:33Z; that file's CURRENT mtime is 2026-07-25T18:44:34Z -- "
        "THE INPUT IS 18 DAYS NEWER THAN THE ARTIFACT DERIVED FROM IT, and nothing re-ran the load. "
        "DESIRED vs APPLIED IS SHARPER HERE THAN FOR THE SIBLING, because a rhythm IS declared: "
        "org/modules/graph/critical-surfaces.yaml:163 declares "
        "when: 'nightly graph refresh (derive -> Nessie -> kuzu_stitch_load)' and "
        "org/modules/graph/graph_status_cli.py:236 still routes 'comp-kuzu (after "
        "kuzu_stitch_load)'. A NIGHTLY IS DECLARED AND THE ARTIFACT IS 50.60 DAYS OLD -- "
        "live_matches_declared=no, on the artifact's own stamp. "
        "RESIDUALS, NAMED: a failing trigger leaves no stamp; a trigger writing to a non-default "
        "--db stamps elsewhere; I did not sweep `aws events list-rules` / `aws scheduler "
        "list-schedules`. "
        "RULE 25: 50.60d < 90d, NOT dormant by the bar; successor clause resolves this as MIGRATED "
        "(see coverage row for the measured layer-by-layer successor comparison), not abandoned. "
        "RULE 26, MEASURED FOR THIS SUBJECT: dev-box only, no automated applier, apply owner is "
        "whoever runs the CLI. Module is NEVER-rule compliant on device-specificity (:28-30 derive "
        "from __file__) -- BUT ITS OUTPUT IS NOT: the live manifest embeds the absolute device path "
        "'C:\\\\Users\\\\AndrewBerman\\\\Desktop\\\\ajb_workspace\\\\infra\\\\aws\\\\globgrph\\\\"
        "stitch_graph.json' as stitch_path, so the ARTIFACT carries a device fingerprint the CODE "
        "correctly avoids. That is data, not logic, so it is not a NEVER-rule violation -- it is "
        "named because it makes the manifest non-portable.",
        "UNOWNED for the missing trigger. The declared-nightly record at critical-surfaces.yaml:163 "
        "is a graph-module record; its drift from the artifact is a finding routed to "
        "3.0.0_SA_CVO~X, not repaired by this lane.",
        declared_rhythm="nightly graph refresh (derive -> Nessie -> kuzu_stitch_load), declared at "
                        "org/modules/graph/critical-surfaces.yaml:163",
        actual_trigger=None,
        live_matches_declared="no",
        live_instance_age="kuzu_stitch_db built_at 2026-07-07T15:46:38.578615+00:00 = 50.60 d at "
                          "2026-08-27T06:17:47Z; 3,414 nodes / 5,329 edges; its declared input "
                          "stitch_graph.json is itself 18 days NEWER than this build",
        basis_by_field={"declared_rhythm": "measured", "actual_trigger": "measured",
                        "live_matches_declared": "measured", "live_instance_age": "measured"},
    ),

    # ---- ROW 3 / W3-mdiu-3 : persistence (AC6) -----------------------------------------
    persistence=row(
        "measured",
        "persisted=true: infra/aws/globgrph/kuzu_stitch_db measured on disk at 9,170,944 bytes with "
        "a 349-byte sibling manifest. authority_role=projection -- rebuildable from stitch_graph.json, "
        "governs nothing. "
        "mutation_policy=editable IS MEASURED AND IS THE OPPOSITE OF THE SIBLING SUBJECT'S: both "
        "node and edge writes are MERGE (:79, :97), so a re-run without --force upserts into the "
        "existing DB rather than declining (kuzu_load) or replacing. EXERCISED: loaded a scratch DB "
        "from a 5-node input, then re-ran against a SHRUNKEN 2-node input with no --force; the DB "
        "afterwards held 5 nodes. DELETIONS NEVER PROPAGATE -- the store monotonically accumulates "
        "until someone passes --force. "
        "⛔ THIS IS WHY mutation_policy IS NOT A CLASS CONSTANT: two loaders, same directory, same "
        "table names, and one is replaceable while the other is editable. A card written at class "
        "grain would be true of one and silently wrong about the other.",
        "UNOWNED",
        persisted=True,
        authority_role="projection",
        mutation_policy="editable",
        form="Kuzu embedded database materialised as a SINGLE FILE on this device (9,170,944 bytes) "
             "plus a sibling JSON build manifest (349 bytes)",
        basis_by_field={"persisted": "measured", "authority_role": "measured",
                        "mutation_policy": "measured", "form": "measured"},
    ),

    # ---- ROW 4 / W3-mdiu-4 : location (AC3 + AC4) --------------------------------------
    location=row(
        "measured",
        "WHAT IT WRITES -- RESOLVABLE NAMES, NOT A DESCRIPTION (AC4). TWO artifacts on every "
        "successful run: (1) the Kuzu node table CloudNode and rel table CloudEdge INSIDE the DB at "
        "--db, default infra/aws/globgrph/kuzu_stitch_db (bound at :30, DERIVED from __file__); "
        "(2) the sibling manifest infra/aws/globgrph/kuzu_stitch_db._build_manifest.json "
        "(_provenance.py:34 + :44-46, written from kuzu_stitch_load.py:116). Both read on disk. "
        "THE DB PATH IS UNBOUNDED FROM CLI INPUT: --db (:40) takes an arbitrary path and --force "
        "passes it to shutil.rmtree (:59) / os.remove (:61) -- and here it also removes "
        "args.db + '.wal' (:65). Table-name bound is CLASS 1 and enumerable; LOCATION bound is "
        "arbitrary runtime input. NAMED, NOT FIXED (AC8).",
        "UNOWNED",
        home="infra/aws/globgrph/kuzu_stitch_db",
        projection_of=[
            ref("infra/aws/globgrph/stitch_graph.json",
                "the step-2 union; the live artifact was built from its 2026-07-07T15:45:33Z "
                "revision and the file has since moved to 2026-07-25T18:44:34Z"),
            ref("org/modules/graph/derive_stitch.py",
                "declared producer of stitch_graph.json per graph_status_cli.py:236; NOT "
                "independently verified by this lane"),
        ],
        co_resident_stores=[
            ref("infra/aws/globgrph/kuzu_nessie_db",
                "the successor; carries every layer this DB has plus ms and semctl"),
            ref("infra/aws/globgrph/kuzu_db",
                "the sibling subject's output; same table NAMES, a different column set"),
            ref("infra/aws/globgrph/kuzu_ac7.db", "a 2026-06-12 scratch DB, no live producer found"),
        ],
        basis_by_field={"home": "measured", "projection_of": "inferred",
                        "co_resident_stores": "measured"},
    ),

    # ---- ROW 5 / W3-mdiu-5 : coverage (AC7) --------------------------------------------
    coverage=row(
        "measured",
        "DENOMINATOR PRINTED, MEASURED LAYER BY LAYER OFF THE LIVE DBs rather than from either "
        "manifest -- because the manifest is not a sound oracle for this subject (see failure_mode). "
        "kuzu_stitch_db: aws=1,599 pipeline=1,627 portal=188, TOTAL 3,414. "
        "Successor kuzu_nessie_db: aws=2,083 ms=6,047 pipeline=1,337 portal=11,338 semctl=6,230, "
        "TOTAL 27,035. "
        "THE SUCCESSOR COMPARISON IS NOT UNIFORM AND I AM NOT SMOOTHING IT: it carries 2 layers "
        "this DB has never had (ms, semctl), 60x the portal nodes (11,338 vs 188) and 1.3x the aws "
        "nodes -- BUT THIS DB CARRIES 290 MORE `pipeline` NODES THAN THE SUCCESSOR (1,627 vs 1,337). "
        "⛔ I CANNOT DISCRIMINATE, FROM COUNTS ALONE, WHETHER THOSE 290 ARE STALE NODES SINCE "
        "LEGITIMATELY REMOVED OR GENUINE COVERAGE THE SUCCESSOR LOST. Naming the residual instead "
        "of assigning it: a residual bucket is a claim, not a remainder. The two DBs are 50 days "
        "apart and built from different sources, so a same-vintage comparison is the instrument "
        "that would settle it, and it has not been run. "
        "AC7, THE STANDING LIMIT: these are counts of TWO MATERIALISATIONS. Nothing here asserts "
        "completeness of the writer population or of the estate.",
        "UNOWNED for the 290-node pipeline residual; it is routed as an OBSERVATION to "
        "3.0.0_SA_CVO~X, not resolved here.",
        universe="the union of the AWS layer, the portal/pipeline layer, and the inter-system "
                 "stitch edges, as present in stitch_graph.json at run time, deduped by "
                 "arn-else-id with first-seen winning",
        denominator="3,414 nodes / 5,329 edges in the live instance, measured live as "
                    "aws=1,599 pipeline=1,627 portal=188; successor kuzu_nessie_db 27,035 nodes "
                    "across 5 layers (aws=2,083 ms=6,047 pipeline=1,337 portal=11,338 semctl=6,230)",
        explicitly_out=[
            "any node whose canonical key (arn-else-id) is empty -- dropped at :53",
            "any duplicate key after the first seen -- discarded silently at :53-54",
            "any edge whose source or target did not resolve -- skipped at :90-94, bucketed as "
            "'wildcard/external' or 'genuine', with only the bucket counts printed",
            "the ms and semctl layers entirely -- they exist in the successor and have never been "
            "in this loader's input",
            "anything derive_stitch.py did not put into stitch_graph.json -- this loader cannot "
            "see past its input file",
        ],
        basis_by_field={"universe": "measured", "denominator": "measured",
                        "explicitly_out": "measured"},
    ),

    # ---- ROW 6 / W3-mdiu-6 : key -------------------------------------------------------
    key=row(
        "measured",
        "identity_space measured at :70-71 -- `node_id STRING PRIMARY KEY` -- and populated at "
        ":33-34 by _key(), which is arn-if-present ELSE id. THIS IS A DELIBERATELY MIXED IDENTITY "
        "SPACE: AWS nodes key on ARN, portal nodes key on their path/name, and BOTH live in the "
        "`node_id` column with the ARN also duplicated into a separate `arn` column when present. "
        "The docstring at :8-10 states the intent -- the two layers join on shared ARN-keyed nodes. "
        "key_is_stable=unstable IS THE MEASURED VALUE AND IT IS NOT THE ARN'S FAULT: the portal half "
        "of the space keys on a path/name, so a file rename or move mints a NEW node_id and the "
        "predecessor is unlinked with no forwarding. The AWS half is stable; the column as a whole "
        "is only as stable as its weakest member, and a single enum over a mixed unit must report "
        "the floor. "
        "crosses_spaces=true: node_id is joinable to kuzu_nessie_db, which uses the SAME node_id PK "
        "and the same layer/drift_class/source columns (measured live via CALL TABLE_INFO) -- so "
        "unlike the sibling subject, this DB's key DOES line up with the successor without a rename. "
        "declared_mapping is the arn-else-id rule itself at :33-34: it is expressed as three lines "
        "of code, not as a declared contract, so a consumer must read the loader to know how to "
        "join.",
        "UNOWNED -- the id-space mixing is by design and has no owner for a declared mapping.",
        identity_space="node_id -- arn-if-present else the node's id (path/name for portal nodes); "
                       "one column, two id spaces, no type discriminator",
        key_is_stable="unstable",
        crosses_spaces=True,
        declared_mapping="infra/aws/globgrph/kuzu_stitch_load.py:33-34 (_key), as CODE rather than "
                         "as a declared contract; kuzu_nessie_load.py uses the same node_id PK so "
                         "the two join without a rename",
        basis_by_field={"identity_space": "measured", "key_is_stable": "measured",
                        "crosses_spaces": "measured", "declared_mapping": "measured"},
    ),

    # ---- ROW 7 / W3-mdiu-7 : failure_mode (EXERCISED) ----------------------------------
    failure_mode=row(
        "measured",
        "EXERCISED 2026-08-27T06:3xZ against scratch DBs under --db; repo artifacts never touched. "
        "(a) MISSING INPUT IS LOUD: --in pointing at a non-existent file raises an UNCAUGHT "
        "FileNotFoundError from :46 with a traceback and rc=1. "
        "(b) THE TYPED-NESS GATE IS REAL: :105-108 counts nodes with empty/NULL node_type and :129 "
        "returns rc=1 when that count is non-zero -- an actual quality gate on the exit code, which "
        "the sibling subject has no equivalent of. "
        "(c) ⛔ THE DANGEROUS ONE -- MERGE MEANS DELETIONS NEVER PROPAGATE, AND THE MANIFEST LIES "
        "ABOUT IT. Exercised: built a scratch DB from a 5-node input (manifest node_count=5), then "
        "re-ran against a SHRUNKEN 2-node input with no --force. The run printed 'INFO: NODES "
        "loaded = 2', 'OK: UNTYPED_NODES count=0', 'OK: KUZU_STITCH_LOAD_COMPLETE' and exited rc=0. "
        "ORACLE: the DB then held 5 NODES while the manifest claimed node_count=2. "
        "THE PROVENANCE STAMP REPORTS THE INPUT'S SIZE, NOT THE STORE'S -- :123 passes len(best), "
        "which is the deduped INPUT count, into write_manifest. Under MERGE semantics those two "
        "quantities are not the same number, and the manifest is the artifact whose entire purpose "
        "is making the store's vintage and scale checkable. _provenance.py:6-8 says comp-kuzu prints "
        "this manifest as a provenance header on EVERY invocation, so a consumer reading that header "
        "can be told a node count that is wrong about the DB in front of it. "
        "⛔ NOT TRUE OF THE SIBLING: kuzu_load writes its manifest only inside the rebuild branch, "
        "where the DB was just dropped and repopulated from exactly those nodes, so its count is "
        "accurate at write time. The defect is created by MERGE, not by _provenance.",
        "UNOWNED -- the manifest-vs-store divergence has no owner. NAMED, NOT FIXED (AC8): the "
        "one-line site is kuzu_stitch_load.py:123 and this lane does not touch it.",
        returns_on_failure="Missing --in: uncaught FileNotFoundError + traceback, rc=1 (LOUD). "
                           "Untyped nodes present: prints 'ERROR: UNTYPED_NODES count=N' and "
                           "returns rc=1 (LOUD, and a genuine gate). Shrunken or partial input: "
                           "'OK: KUZU_STITCH_LOAD_COMPLETE' at rc=0 while the store still holds "
                           "everything the input dropped (SILENT).",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=[
            "MERGE never deletes -- nodes and edges removed from the input persist in the DB "
            "indefinitely until someone passes --force. EXERCISED 2026-08-27: 5 nodes retained "
            "against a 2-node input, rc=0, 'COMPLETE' printed",
            "the build manifest records len(best), the deduped INPUT count, not the store's actual "
            "node count (:123) -- EXERCISED: manifest said 2 while the DB held 5. The provenance "
            "artifact is wrong about the store in exactly the case that matters",
            "duplicate canonical keys -> first seen wins, later ones discarded with NO count "
            "emitted (:53-54)",
            "unresolved edge endpoints -> skipped and excused as 'wildcard/external' whenever "
            "_wild() matches (:140-145); a genuinely broken ARN containing '*' or '::' is bucketed "
            "as expected-missing",
            "IF NOT EXISTS on both DDL statements -> a pre-existing table with different columns is "
            "silently accepted",
        ],
        basis_by_field={"returns_on_failure": "measured",
                        "distinguishable_from_true_negative": "measured",
                        "silent_degrade_paths": "measured"},
    ),

    standing="UNSOUND",
    why="EVERY ROW MEASURED, so this is not INCOMPLETE. UNSOUND is scoped to STANDING AS "
        "LOAD-BEARING SUBSTRATE and is not a claim the script is broken: exercised with --force and "
        "a current input it loads correctly and its typed-ness gate genuinely fires. Four measured "
        "facts block standing on it. (1) A NIGHTLY IS DECLARED "
        "(critical-surfaces.yaml:163) AND THE ARTIFACT IS 50.60 DAYS OLD -- DESIRED is not APPLIED, "
        "measured from a stamp the writer emits unconditionally. (2) THE INPUT HAS MOVED 18 DAYS "
        "PAST THE ARTIFACT DERIVED FROM IT and nothing re-ran the load, so the served DB is a "
        "projection of a superseded revision of its own source. (3) THE BUILD MANIFEST CAN BE WRONG "
        "ABOUT THE STORE -- exercised at 2 claimed vs 5 held -- and comp-kuzu prints that manifest "
        "as its provenance header, so the instrument built to make staleness checkable is itself "
        "unsound for this subject under its own MERGE semantics. (4) SUPERSEDED: kuzu_nessie_db "
        "carries every layer this DB has, plus ms and semctl, at 27,035 nodes and 0.67d. "
        "Rule 25 dormancy does NOT fire (50.60d < 90d); the successor clause resolves this as "
        "MIGRATED rather than abandoned. THE 290-NODE PIPELINE RESIDUAL IS EXPLICITLY UNRESOLVED "
        "and is not counted as supporting this verdict.",
    blocking=[
        "the build manifest reports the deduped INPUT count, not the store's node count "
        "(kuzu_stitch_load.py:123) -- EXERCISED at 2 claimed vs 5 held; comp-kuzu serves this as a "
        "provenance header. UNOWNED.",
        "MERGE semantics mean deletions never propagate: the store accumulates silently at rc=0 "
        "until someone passes --force. UNOWNED.",
        "a nightly is DECLARED at critical-surfaces.yaml:163 and no trigger exists on any measured "
        "plane; the artifact is 50.60d old and its input is 18d newer. UNOWNED.",
    ],
))


def main() -> None:
    out_dir = HERE
    written = []
    for token, obj in CARDS:
        stem = obj["subject"]["id"].replace("/", "_").replace(".", "_")
        path = os.path.join(out_dir, "W3-%s__%s.json" % (token, stem))
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, indent=2, sort_keys=True, ensure_ascii=True)
            f.write("\n")
        written.append(path)
        print("OK: wrote %s" % os.path.relpath(path, os.getcwd()).replace("\\", "/"))

    # AC2 self-check: as_of byte-identical across every card in the batch.
    stamps = {json.dumps(obj["as_of"], sort_keys=True) for _, obj in CARDS}
    if len(stamps) != 1:
        raise SystemExit("ERROR: as_of is NOT byte-identical across the batch: %d distinct" % len(stamps))
    print("OK: AC2 as_of byte-identical across %d card(s): %s" % (len(CARDS), stamps.pop()))
    print("OK: %d card(s) written" % len(written))


if __name__ == "__main__":
    main()
