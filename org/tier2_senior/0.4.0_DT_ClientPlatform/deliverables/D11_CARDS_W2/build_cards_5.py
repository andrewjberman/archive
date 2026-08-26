#!/usr/bin/env python3
"""Wave-2 substrate cards, part 5 of 5 (TO-W2-DTX2) -- the CVO composer harness and its outputs.

The last 3 of this lane's 16 subjects. WAVE-2 ANCHOR 100e7ea130.

⛔ READ-ONLY TREE. org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/ belongs
to CVO. Every measurement below is a READ; nothing in that tree was written, tracked or moved.

⛔ NO DEPRECATION VERDICTS -- and this is the hardest place to hold that line, because Andrew
named these artifacts directly (1907Z, 1911Z). Each is carded at full depth and NOTHING here
says anything about any subject's fate.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHOR = "100e7ea130"
GRAPH_VINTAGE = "kuzu_nessie_db@2902399899597701830"
CARDED = "2026-08-26T23:25:00Z"
ME = "0.4.0_DT_ClientPlatform~X"
ORDER = {"measured": 3, "inferred": 2, "held": 1, "absent": 0}
H = "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/"


def ref(id_, note=None):
    assert " -- " not in id_ and " (" not in id_, "joinable_ref id carries prose: %r" % id_
    return {"id": id_, "note": note}


def row(basis, evidence, owner, **kw):
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


CARDS = []

# ---------------------------------------------------------------- W2-nthk : the harness DIRECTORY
CARDS.append(card(
    "nthk", H, "corpus",
    "the CVO subdivision-harness tree as a whole -- the composer code plus its outputs plus its "
    "test suite, carded as ONE corpus because wave 1 named the directory itself",
    row("measured",
        "Directory enumerated at HEAD: 12 entries. 4 composer/pipeline scripts (c2_individuate.py "
        "40,828 B, c3_cover.py 16,495 B, kimi_pipeline.py 46,114 B, kimi_steps_monolith.py 8,915 "
        "B), 1 stage script (stage1_sides.py), 4 test files, 2 JSON outputs and a __pycache__. "
        "COMPOSES the canonical graph projection; INVENTS the subdivision method itself. "
        "DECLARED_OPINIONS IS NULL AND THE REASON IS THE GRAIN: this subject is a DIRECTORY, "
        "which has no single producer whose filters, thresholds and definitional choices "
        "could be enumerated. The opinions belong to the member scripts, and the two member "
        "artifacts carded separately enumerate theirs. A directory-level opinion set would "
        "have to be invented.",
        "3.0.0_SA_CVO",
        how="A self-contained harness that reads the canonical graph and emits C2 instance and C3 "
            "structure artifacts. It carries its OWN test suite in-tree -- 4 test files including "
            "test_producer_reader_executed.py and test_incontainer_reader_equivalence.py -- which "
            "is unusual among the subjects this lane carded and is a strength worth naming."
            " DECLARED_OPINIONS IS NULL AND THE REASON IS THE GRAIN: this subject is a DIRECTORY, which has no single producer whose filters, thresholds and definitional choices could be enumerated. The opinions live in the member scripts, and the two member artifacts that are separately carded (c2_instances.json, c3_structures.json) enumerate theirs. Enumerating a directory-level opinion set would mean inventing one. "
            "DETERMINISM IS 'unknown' AND THAT IS A MEASURED REFUSAL, NOT A GAP I OVERLOOKED: I "
            "did NOT read kimi_pipeline.py, so I cannot say whether a model stage runs inside "
            "this harness. I nearly recorded 'hybrid' on the strength of the filename -- which "
            "is a NAME-BASED INFERENCE, the exact move this wave exists to prevent, and v2 "
            "rightly demands model + invocations_per_run + failure_is_loud before that claim is "
            "expressible. I have none of the three, so 'unknown' is the honest value. "
            "DECLARED_OPINIONS IS NULL AND THE REASON IS THE GRAIN: this subject is a "
            "DIRECTORY, which has no single producer whose filters, thresholds and "
            "definitional choices could be enumerated. The opinions live in the member "
            "scripts, and the two member artifacts carded separately enumerate theirs. A "
            "directory-level opinion set would have to be invented.",
        determinism="unknown",
        composes=[ref("kuzu_nessie_db", "the canonical projection the composer reads")],
        invents=[ref("subdivision_method", "overlapping-domain-cover anchored on catalog anchor nodes")],
        materializer_standing="canonical",
        declared_opinions=None,
        basis_by_field={"how": "measured", "determinism": "absent",
                        "composes": "inferred"}),
    row("measured",
        "The tree is git-managed; its two JSON outputs carry db_built_at 2026-08-07T02:20:12Z. "
        "1.0.0_SA_CTO~X measured (73215 Q2) that the GENERATORS ran in production at 02:00Z on "
        "the carding day -- so the CODE is exercised on a schedule while the OUTPUTS in this tree "
        "are 19 days old. Those are two different clocks for one directory, which is precisely "
        "why the directory is a poor unit of cadence and its two output files are separate "
        "subjects.",
        "3.0.0_SA_CVO",
        declared_rhythm=None, actual_trigger="a production run at 02:00Z, per 1.0.0_SA_CTO~X",
        live_matches_declared="unmeasured",
        live_instance_age="code exercised same-day; outputs 19 days old",
        basis_by_field={"actual_trigger": "held", "live_instance_age": "measured"}),
    row("measured",
        "MEASURED SPLIT: of 12 entries, 9 are git-TRACKED and 3 are UNTRACKED "
        "(c2_instances.json, c3_structures.json, __pycache__). So THE CODE IS VERSIONED AND THE "
        "OUTPUTS ARE NOT -- and the outputs are 12.4MB that the derive ingests.",
        "3.0.0_SA_CVO",
        persisted=True, authority_role="evidence", mutation_policy="replaceable",
        form="directory: python sources (tracked) + JSON outputs (untracked)"),
    row("measured",
        "Directory listed directly at HEAD. ⛔ GRAIN OVERLAP, STATED SO IT IS NOT READ AS "
        "TRIPLE-COUNTING: this subject is the DIRECTORY, and two of its members "
        "(c2_instances.json, c3_structures.json) are ALSO separate wave-2 subjects in this same "
        "lane. Their coverage is a strict subset of this card's. Three cards, one tree, by the "
        "frozen subject set's own construction.",
        "3.0.0_SA_CVO",
        home=H,
        projection_of=[ref("kuzu_nessie_db", "per the outputs' in-file graph_vintage")],
        co_resident_stores=[ref(H + "c2_instances.json", "also a separate wave-2 subject"),
                            ref(H + "c3_structures.json", "also a separate wave-2 subject")]),
    row("measured",
        "COUNTED: 12 entries, 9 tracked / 3 untracked. ⛔ THE DENOMINATOR IS THE DIRECTORY, WHICH "
        "IS A WEAK UNIT: a file count says nothing about what the harness COVERS of the graph. "
        "The meaningful coverage figures live in the two output subjects' own counts blocks and "
        "are reported there, not double-counted here.",
        "3.0.0_SA_CVO",
        universe="files constituting the subdivision harness",
        denominator="12 of 12 entries enumerated; 9 tracked, 3 untracked",
        explicitly_out=["the graph-coverage question, which belongs to the two output subjects"]),
    row("measured",
        "Filesystem paths. No cross-space concern at the directory grain; the id-space questions "
        "belong to the outputs, which key on graph node ids.",
        "3.0.0_SA_CVO",
        identity_space="filesystem paths under the harness directory",
        key_is_stable="stable", crosses_spaces=False, declared_mapping=None,
        basis_by_field={"identity_space": "measured", "key_is_stable": "inferred",
                        "crosses_spaces": "measured"}),
    row("inferred",
        "⛔ NOT EXERCISED, AND DELIBERATELY SO. Exercising this harness means RUNNING CVO's "
        "composer, and this tree is READ-ONLY at my seat. I read its file listing and its "
        "outputs; I did not execute c2_individuate.py or c3_cover.py and I did not run its test "
        "suite. The presence of 4 in-tree tests including test_producer_reader_executed.py "
        "suggests the failure surface IS tested by its owner, but I did not run them and will "
        "not claim their result.",
        "3.0.0_SA_CVO",
        returns_on_failure="UNMEASURED at this seat -- the harness was not executed",
        distinguishable_from_true_negative="unmeasured",
        silent_degrade_paths=["the outputs are untracked, so a deleted or truncated output is "
                              "unrecoverable from git and would surface only as a downstream "
                              "derive failure"],
        basis_by_field={"returns_on_failure": "absent",
                        "distinguishable_from_true_negative": "absent",
                        "silent_degrade_paths": "measured"}),
    "INCOMPLETE",
    "Carded at the DIRECTORY grain because the frozen subject set names the directory, and that "
    "grain is the card's own limitation: a file count is not a coverage measure, the code and the "
    "outputs run on two different clocks, and the meaningful trust questions belong to the two "
    "output subjects carded separately. INCOMPLETE rather than QUALIFIED because the failure-mode "
    "row is unexercised by choice -- this is CVO's tree and running its composer is not my act. "
    "The tree's genuine strength, which no other subject this lane carded has, is that it ships "
    "its own test suite.",
    ["failure mode unexercised -- read-only tree, composer not run by this lane",
     "directory grain admits no meaningful coverage denominator"]))

# ---------------------------------------------------------------- W2-hffm : c2_instances.json
CARDS.append(card(
    "hffm", H + "c2_instances.json", "artifact",
    "the C2 motif INSTANCE corpus emitted by the CVO composer -- the artifact the derive ingests "
    "to populate C2Motif instance nodes",
    row("measured",
        "Parsed at HEAD: {producer, supersedes_shape_of, graph_vintage, grounding, counts, nodes, "
        "edges}. Self-declares producer '3.0.0_SA_CVO c2_individuate'. ⛔ IT DECLARES ITS OWN "
        "RELATION TO TWO OTHER SUBJECTS: supersedes_shape_of = [motif_c2c3_materialize.json, "
        "motif_c2c3_materialize_ab.json]. That is a DECLARED lineage claim, not my inference -- "
        "and it is about SHAPE, not about replacement, which matters because 1.0.0_SA_CTO~X "
        "measured both of those specs still being consumed by today's derive (specs=3).",
        "3.0.0_SA_CVO",
        how="Emits one C2Motif node per matched motif instance over the canonical graph, plus "
            "CONTAINS edges to member nodes. c2_individuate.py:350 declares EMITTED_NODE_TYPES = "
            "(C2Motif, C3System). DETERMINISM IS 'unknown' BY REFUSAL: the harness filename "
            "lineage hints at a model stage, but I did not read the pipeline source and v2 "
            "requires model + invocations_per_run + failure_is_loud before 'hybrid' may be "
            "claimed. Naming a determinism class off a filename is the same defect as merging "
            "two stores off a shared leaf name.",
        determinism="unknown",
        composes=[ref("kuzu_nessie_db", "per the in-file graph_vintage snapshot ids")],
        invents=[ref("c2_motif_instance_identity", "one node per matched motif occurrence")],
        materializer_standing="canonical",
        declared_opinions=[
            "duplicate member sets are COLLAPSED -- the file declares collapsed_duplicate_member_sets 519",
            "the 13-family motif taxonomy in by_family is a fixed vocabulary",
            "_detector_types enumerates 24 node types by hand; anything outside that list is "
            "structurally invisible to the coverage figures this file reports",
            "the BACKEND/FRONTEND/KNOWLEDGE side split is declared, and KNOWLEDGE is measured at 0"],
        basis_by_field={"how": "measured", "determinism": "absent",
                        "composes": "measured"}),
    row("measured",
        "In-file graph_vintage.db_built_at = 2026-08-07T02:20:12Z; file mtime 2026-08-07T00:49Z; "
        "19 days before carding. ⛔ THE CODE AND THE OUTPUT HAVE DIFFERENT VINTAGES AND MUST NOT "
        "BE COLLAPSED: 1.0.0_SA_CTO~X measured (73215 Q2) that c2_individuate.py RAN IN "
        "PRODUCTION at 02:00Z on the carding day. So the GENERATOR is current and THIS OUTPUT is "
        "19 days old. Recording one 'currency' verdict would either condemn live code or bless a "
        "stale artifact.",
        "3.0.0_SA_CVO",
        declared_rhythm=None, actual_trigger="a production composer run",
        live_matches_declared="unmeasured", live_instance_age="output 19 days old; generator ran same-day",
        basis_by_field={"live_instance_age": "measured", "actual_trigger": "held"}),
    row("measured",
        "10,329,963 bytes. ⛔ UNTRACKED **AND NOT GITIGNORED** -- `git ls-files --error-unmatch` "
        "fails and `git check-ignore` finds no rule, so it shows as '??' in every agent's git "
        "status on this device. A 10MB artifact the derive INGESTS, with no version history: if "
        "it were deleted or truncated, it could not be recovered from the repo.",
        "3.0.0_SA_CVO",
        persisted=True, authority_role="evidence", mutation_policy="replaceable", form="json"),
    row("measured", "Path read directly at HEAD, in a READ-ONLY tree.", "3.0.0_SA_CVO",
        home=H + "c2_instances.json",
        projection_of=[ref("kuzu_nessie_db", "in-file nodes_snapshot_id 8601547680771488785, NOT the wave pin")],
        co_resident_stores=[ref(H + "c3_structures.json", "the C3 sibling, which consumes this file's declared instance count"),
                            ref("org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/motif_c2c3_materialize.json",
                                "a spec this file declares it supersedes_shape_of, and which is still consumed")]),
    row("measured",
        "⛔ THE FILE REPORTS A RICHER COVERAGE TRIPLE THAN ANY OTHER SUBJECT THIS LANE CARDED, "
        "AND IT IS DAMNING ON ONE SIDE: coverage_triple_by_side gives BACKEND covered 2,755 of "
        "2,936 in-scope (93.8%) against 3,393 on-side (81.2%); FRONTEND covered 1,479 of 5,245 "
        "in-scope (28.2%) against 11,338 on-side (13.0%); and KNOWLEDGE covered 0 of 0 in-scope "
        "against 5,851 on-side (0.0%). "
        "⛔ SO 5,851 KNOWLEDGE-SIDE NODES ARE NOT MERELY UNCOVERED -- THEY ARE OUT OF DETECTOR "
        "SCOPE ENTIRELY (in_detector_scope_Y = 0), which means no detector could ever have found "
        "them and 0.0% is a structural, not an incidental, zero. "
        "Also declared: instances_with_no_catalog_anchor 1,103; distinct_members 4,234.",
        "3.0.0_SA_CVO",
        universe="C2 motif instances discoverable by the 24 declared detector types over the composed snapshot",
        denominator="6,138 distinct instances declared, over 6,657 rows_seen with 519 collapsed; "
                    "coverage BACKEND 81.2% of side, FRONTEND 13.0% of side, KNOWLEDGE 0.0% of 5,851 on-side nodes",
        explicitly_out=["all 5,851 KNOWLEDGE-side nodes -- in_detector_scope is 0, so they are "
                        "outside the detector set by construction",
                        "any node type outside the 24 hand-enumerated _detector_types"]),
    row("measured",
        "Nodes key on graph node ids and CONTAINS edges point at member node ids, so this "
        "artifact's identity space is the canonical projection's -- CloudNode.node_id, only 6.4% "
        "ARN-shaped. ⛔ AND ITS SNAPSHOT IS NOT THE CURRENT ONE: in-file nodes_snapshot_id is "
        "8601547680771488785 while the wave pin is 2902399899597701830. So its ids were resolved "
        "against a graph state that the current projection no longer holds, and a join to today's "
        "projection is a join across two snapshots with no declared reconciliation. "
        "⚠ graph_nodes_total is NULL in-file -- the artifact records no denominator for the "
        "population it sampled.",
        "3.0.0_SA_CVO",
        identity_space="canonical graph node ids at snapshot 8601547680771488785",
        key_is_stable="unstable", crosses_spaces=True, declared_mapping=None,
        basis_by_field={"identity_space": "measured", "crosses_spaces": "measured",
                        "declared_mapping": "measured", "key_is_stable": "measured"}),
    row("measured",
        "EXERCISED as a self-consistency control, and IT FOUND A DISAGREEMENT THE FILE MAKES "
        "ABOUT ITSELF. Recomputed the node_type census against the declared counts block: "
        "ACTUAL C2Motif = 6,157 and C3System = 4 (6,161 nodes total), while the file declares "
        "c2_motif_instances_distinct = 6,138. ⛔ A 19-NODE GAP BETWEEN THE ARRAY AND THE TALLY, "
        "IN THE SAME FILE. The file's own _tally_denominator note explains the tally counts "
        "DISTINCT INSTANCES POST-COLLAPSE and not rows_seen -- and 6,657 rows_seen minus 519 "
        "collapsed = 6,138 exactly, so the tally is internally consistent with its stated "
        "definition. The array is simply a different population: it also carries "
        "class_nodes_marked_grain_class = 23. "
        "⛔ THE CONSEQUENCE FOR A CONSUMER: counting len([n for n in nodes if node_type=='C2Motif']) "
        "gives 6,157 and reading counts.c2_motif_instances_distinct gives 6,138, BOTH FROM THIS "
        "FILE, both defensible, differing silently. That is the same class/instance grain "
        "collision 0.8.0_AE_CloudComp~X carded on C2 from the graph side, corroborated here from "
        "the artifact side with different numbers and a different instrument.",
        "3.0.0_SA_CVO",
        returns_on_failure="no lookup surface; the file is ingested wholesale and reports no error state",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=[
            "two defensible instance counts (6,157 array vs 6,138 tally) differ by 19 with no "
            "field marking which a consumer should use",
            "a stale snapshot id resolves against today's projection without any reconciliation signal"]),
    "UNSOUND",
    "A genuinely well-instrumented artifact -- it declares its producer, its lineage, its "
    "vintage, a 15-field counts block and a coverage triple, which is more self-description than "
    "any other subject this lane carded. It is UNSOUND on TRUST for three measured reasons: its "
    "array and its own tally disagree by 19 nodes with nothing marking which is authoritative; "
    "its ids resolve against a snapshot that is no longer the pinned one, with graph_nodes_total "
    "recorded NULL; and 5,851 KNOWLEDGE-side nodes sit at 0.0% coverage with in_detector_scope 0, "
    "meaning no detector could ever reach them. ⛔ NOTHING HERE SPEAKS TO THIS ARTIFACT'S FUTURE.",
    ["array count 6,157 vs declared tally 6,138 -- a 19-node silent disagreement in one file",
     "ids resolved against snapshot 8601547680771488785, not the current pin, with graph_nodes_total NULL",
     "5,851 KNOWLEDGE-side nodes structurally out of detector scope at 0.0% coverage",
     "10.3MB untracked and un-gitignored, unrecoverable from the repo if lost"]))

# ---------------------------------------------------------------- W2-xzjx : c3_structures.json
CARDS.append(card(
    "xzjx", H + "c3_structures.json", "artifact",
    "the C3 structure corpus emitted by the CVO composer -- the nearest thing in this estate to "
    "a materialized C3 layer",
    row("measured",
        "Parsed at HEAD: {producer, graph_vintage, input_freshness, grounding, counts, nodes, "
        "edges}. Self-declares producer '3.0.0_SA_CVO c3_cover -- anchor-NODE "
        "overlapping-domain-cover'. Its grounding block cites TWO rulings by id: the model is "
        "'OVERLAPPING-DOMAIN-COVER, CTO-ruled @f7f21f406; NOT connected-components (over-merges "
        "to 1 supersystem, @fbfa06590a)' and the key is 'ANCHOR NODE, Andrew-ruled 2026-08-07'. "
        "That is the most explicitly grounded methodology row of this lane's 16 subjects.",
        "3.0.0_SA_CVO",
        how="Promotes C3System structures from the C2 instance corpus by an overlapping-domain "
            "cover anchored on catalog anchor nodes, emitting CONTAINS edges to member motifs.",
        determinism="deterministic",
        composes=[ref(H + "c2_instances.json", "declared instances_considered 6138, matching that file's own tally")],
        invents=[ref("c3_system_identity", "one node per promoted overlapping domain")],
        materializer_standing="canonical",
        declared_opinions=[
            "OVERLAPPING-DOMAIN-COVER is chosen over connected-components, and the file states "
            "WHY: connected-components over-merges to a single supersystem",
            "the ANCHOR NODE key, Andrew-ruled",
            "domains with a single motif are NOT promoted -- 617 of them, an explicit exclusion"]),
    row("measured",
        "⛔ THE ARTIFACT DECLARES ITS OWN FRESHNESS AND THE DECLARATION IS NOW FALSE. In-file "
        "input_freshness reads 'CURRENT -- input composed against the live graph snapshot'. Its "
        "own graph_vintage.db_built_at is 2026-08-07T02:20:12Z with nodes_snapshot_id "
        "8601547680771488785, and the wave-pinned projection is 2902399899597701830 built "
        "2026-08-26T14:07:59Z. ⛔ 'CURRENT' IS A FROZEN STRING THAT DOES NOT AGE: it was true when "
        "written and the artifact carries it forward unchanged 19 days later. This is exactly the "
        "violation the v2 temporal_claim field exists to make expressible -- a part claiming "
        "current_state while measurably stale -- occurring here as free prose inside the artifact "
        "rather than in a field a consumer could reject on.",
        "3.0.0_SA_CVO",
        declared_rhythm=None, actual_trigger="a production composer run",
        live_matches_declared="no", live_instance_age="19 days; self-declared 'CURRENT'"),
    row("measured",
        "2,115,118 bytes. UNTRACKED **AND NOT GITIGNORED**, same as its C2 sibling -- '??' in "
        "every agent's git status, ingested by the derive, with no version history.",
        "3.0.0_SA_CVO",
        persisted=True, authority_role="evidence", mutation_policy="replaceable", form="json"),
    row("measured", "Path read directly at HEAD, in a READ-ONLY tree.", "3.0.0_SA_CVO",
        home=H + "c3_structures.json",
        projection_of=[ref(H + "c2_instances.json", "instances_considered 6138"),
                       ref("kuzu_nessie_db", "in-file snapshot 8601547680771488785, NOT the wave pin")],
        co_resident_stores=[ref(H + "c2_instances.json", "the C2 input, also a separate wave-2 subject")]),
    row("measured",
        "COUNTED and cross-checked against the declared counts block, which AGREES: nodes = 1,255 "
        "and node_type census is C3System 1,255 with no other type, matching declared "
        "c3_structures_promoted = 1,255; edges = 8,978 matching contains_edges = 8,978. "
        "⛔ THE EXCLUSIONS ARE THE INTERESTING HALF AND THE FILE DECLARES THEM: "
        "domains_unpromoted_single_motif = 617 (excluded by the single-motif rule) and "
        "instances_with_no_catalog_anchor = 1,103 of 6,138 instances considered, i.e. 18.0% of "
        "the input had NO ANCHOR -- and the anchor is the Andrew-ruled key this whole method "
        "turns on.",
        "3.0.0_SA_CVO",
        universe="C3 systems promotable from the C2 instance corpus by overlapping-domain cover",
        denominator="1,255 promoted from 6,138 instances considered; 617 domains unpromoted as "
                    "single-motif; 1,103 of 6,138 instances (18.0%) had no catalog anchor",
        explicitly_out=["single-motif domains, excluded by declared rule",
                        "instances with no catalog anchor, which the anchor-node key cannot place"]),
    row("measured",
        "Keys are C3System node ids anchored on catalog anchor nodes -- the key is Andrew-ruled "
        "per the file's own grounding. Crosses into the canonical graph id space via member "
        "edges, at snapshot 8601547680771488785 rather than the current pin. graph_nodes_total is "
        "NULL in-file. ⚠ 1,103 instances had no anchor at all, so for 18% of the input the "
        "declared key could not be applied -- an identity space that does not span its own input.",
        "3.0.0_SA_CVO",
        identity_space="C3System ids anchored on catalog anchor nodes, over graph node ids at a stale snapshot",
        key_is_stable="unstable", crosses_spaces=True,
        declared_mapping="the anchor-node rule is declared in-file and cited to an Andrew ruling; "
                         "the snapshot reconciliation to the current pin is NOT declared",
        basis_by_field={"identity_space": "measured", "crosses_spaces": "measured",
                        "declared_mapping": "measured", "key_is_stable": "measured"}),
    row("measured",
        "EXERCISED as a self-consistency control with both arms reachable: recomputed the "
        "node_type census and edge count against the declared counts block. UNLIKE ITS C2 "
        "SIBLING IT AGREES EXACTLY -- 1,255 C3System nodes against c3_structures_promoted 1,255, "
        "8,978 edges against contains_edges 8,978, and a single node_type with no grain mixing. "
        "The same control that surfaced a 19-node gap in c2_instances.json returns clean here, "
        "which is what makes it a control rather than a formality. "
        "⛔ THE FAILURE MODE THAT REMAINS IS THE SELF-DECLARED FRESHNESS: input_freshness reads "
        "'CURRENT' and will keep reading CURRENT forever, so a consumer trusting that string "
        "receives a confident claim about a 19-day-old composition with nothing in the artifact "
        "to contradict it.",
        "3.0.0_SA_CVO",
        returns_on_failure="no lookup surface; ingested wholesale, and its self-declared freshness "
                           "string never changes regardless of age",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=[
            "input_freshness 'CURRENT' is a frozen string that does not age with the artifact",
            "18% of considered instances had no anchor and are absent from the output with no "
            "signal at the consumer"]),
    "UNSOUND",
    "The best-grounded methodology of this lane's 16 subjects -- it cites the rulings behind its "
    "model AND its key by commit and by sovereign, states why the rejected alternative was "
    "rejected, and its internal counts control returns clean where its own sibling's does not. "
    "It is UNSOUND on one axis that overrides that: IT DECLARES ITSELF CURRENT AND IS 19 DAYS "
    "STALE, and that declaration is a frozen prose string a consumer cannot reject on. "
    "Additionally 18.0% of its input could not be placed by its own anchor key. "
    "⛔ AND THE THING THIS CARD MUST NOT BE READ AS SAYING: this is NOT the C3 layer. Andrew, "
    "1911Z verbatim -- 'we are nowhere even close to doing c3 right now, so any card they do is "
    "simply representative of current state.' This artifact is a one-off materialization at "
    "authority_role evidence, and its standing here is a snapshot of now, not a verdict on it.",
    ["self-declared input_freshness 'CURRENT' against a measured 19-day-old composition",
     "1,103 of 6,138 instances (18.0%) had no catalog anchor and could not be placed by the declared key",
     "ids resolved against snapshot 8601547680771488785, not the current pin",
     "2.1MB untracked and un-gitignored, unrecoverable from the repo if lost"]))

written = []
for token, c in CARDS:
    name = c["subject"]["id"].replace("/", "_").replace(":", "_").strip("_")
    path = os.path.join(HERE, "W2-%s__%s.json" % (token, name[:70]))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    written.append((token, os.path.basename(path)))

print("part-5 cards written:", len(written))
for t, n in written:
    print("  W2-%-5s %s" % (t, n))
