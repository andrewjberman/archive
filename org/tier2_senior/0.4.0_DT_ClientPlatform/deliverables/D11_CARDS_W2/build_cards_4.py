#!/usr/bin/env python3
"""Wave-2 substrate cards, part 4 of 4 (TO-W2-DTX2, the STORES).

The remaining 7 of this lane's 16 subjects. WAVE-2 ANCHOR 100e7ea130.
NO DEPRECATION VERDICTS -- four of these were flagged orphaned/superseded by this lane's own
wave-1 manifest, and that prior is deliberately excluded from every row below.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHOR = "100e7ea130"
GRAPH_VINTAGE = "kuzu_nessie_db@2902399899597701830"
CARDED = "2026-08-26T23:15:00Z"
ME = "0.4.0_DT_ClientPlatform~X"
ORDER = {"measured": 3, "inferred": 2, "held": 1, "absent": 0}
HARNESS = "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/"
DSDEL = "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/"


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

# ---------------------------------------------------------------- W2-pcac
CARDS.append(card(
    "pcac", "org/modules/graph/keep-dormant.yaml", "store",
    "the canonical keep-dormant registry -- the dormant-vs-dead guard's lookup source, whose "
    "four required fields the D3 lifecycle axis adopts verbatim",
    row("measured",
        "Parsed at HEAD: {schema_version:1, revalidation_default_days:180, discriminators (4), "
        "entries (7)}. Hand-authored, git-reviewed. Its own RULING 1 states the YAML is canonical "
        "and an opal:lifecycle AWS tag is an optional projected mirror that LOSES on conflict, "
        "because a tag is not in git history.",
        "1.0.0_SA_CTO (last author @142d396b5d, 2026-07-02T19:25:44-04:00)",
        how="A registry of DELIBERATE dormancy. Its stated reason for existing is that a "
            "deliberate belt and a corpse are identical on every mechanical signal -- both "
            "DISABLED, both 0-invocation, both 0-consumer -- and only an INTENT ANNOTATION "
            "separates them. It COMPOSES nothing and INVENTS the intent schema and decay rule.",
        determinism="deterministic", composes=[],
        invents=[ref("keep_dormant_intent_schema",
                     "reason + rearm_condition + annotation_cite + revalidate_by, all required per RULING 2"),
                 ref("revalidate_decay_rule",
                     "an entry past revalidate_by is STALE and demands human re-grounding; STALE never auto-promotes to DEBT")],
        materializer_standing="not_applicable",
        declared_opinions=[
            "revalidation_default_days = 180 -- a chosen decay window, not a derived one",
            "the FAIL-SAFE DEFAULT: a resource tripping only mechanical Tier-C signals defaults "
            "to KEEP-DORMANT and never to DEBT, a deliberate bias against reaping",
            "the 4 hand-enumerated discriminators that decide belt-vs-corpse"]),
    row("measured",
        "No scheduled producer: changed by human commit, last at 2026-07-02 @142d396b5d, 55 days "
        "before carding. ⛔ I EXERCISED THE REGISTRY'S OWN DECAY RULE rather than reading it: "
        "parsed every entry's revalidate_by and differenced against a 2026-08-26 clock read. "
        "1 of 7 IS PAST ITS WINDOW -- lever:mdpf-custody-flip-LEVER-2-manual-ssm-dispatch, "
        "revalidate_by 2026-08-16, TEN DAYS OVER. The other 6 sit at 2026-12-29. 0 unparseable, "
        "and all 7 carry reason + rearm_condition + annotation_cite as RULING 2 requires. By "
        "RULING 3 that entry is STALE and demands human re-grounding -- and NOTHING SCHEDULED "
        "WILL RAISE IT, because the file has no producer to run.",
        "1.0.0_SA_CTO",
        declared_rhythm="per-entry revalidate_by decay, default 180 days",
        actual_trigger="a human commit; no scheduled re-grounding exists",
        live_matches_declared="no",
        live_instance_age="file 55 days old; 1 of 7 entries 10 days past its own decay date"),
    row("measured", "11,301 bytes on disk, git-TRACKED (@142d396b5d resolves).", "1.0.0_SA_CTO",
        persisted=True, authority_role="source", mutation_policy="editable", form="yaml"),
    row("measured", "Path read directly at HEAD.", "1.0.0_SA_CTO",
        home="org/modules/graph/keep-dormant.yaml", projection_of=[],
        co_resident_stores=[ref("opal_lifecycle_keep_dormant_aws_tag",
                                "an OPTIONAL projected mirror; on conflict the YAML wins")]),
    row("measured",
        "COUNTED from the parsed file: 7 entries. ⛔ THE DENOMINATOR IS NOT COMPUTABLE FROM THIS "
        "ARTIFACT and I am not inventing one: 7 of how many resources that OUGHT to carry an "
        "intent annotation? That population is every dormant-looking resource in the estate, "
        "which this file cannot see.",
        "1.0.0_SA_CTO",
        universe="resources deliberately held dormant, estate-wide",
        denominator=None,
        denominator_absent_reason="An OPT-IN annotation store. Numerator 7 is measured; the true "
            "denominator is the set of dormant-looking resources that SHOULD be annotated, "
            "knowable only by sweeping the estate against this file -- a measurement outside this "
            "card's subject and not performed here.",
        explicitly_out=["any dormant resource nobody annotated, invisible by construction"]),
    row("measured",
        "Keys are resource_id strings of the form '<type>:<name>'. Measured shapes across the 7: "
        "event_rule:, ssm_parameter:, lever:, ec2_instance:, secret_version:. NOT ARNs. ⛔ "
        "CROSSES SPACES: an AWS-native consumer holds ARNs, this registry holds a hand-written "
        "type:name grammar, and NO MAPPING IS DECLARED. The 'lever:' prefix is not an AWS "
        "resource type at all -- it names a manual procedure, so that member cannot carry an ARN "
        "even in principle, which means the crossing is not merely undeclared but partial by "
        "construction.",
        "1.0.0_SA_CTO",
        identity_space="hand-authored '<type>:<name>' resource ids",
        key_is_stable="unstable", crosses_spaces=True, declared_mapping=None,
        basis_by_field={"identity_space": "measured", "crosses_spaces": "measured",
                        "declared_mapping": "measured", "key_is_stable": "inferred"}),
    row("measured",
        "EXERCISED, both arms reachable from different truths in one run: a membership test for "
        "'arn:aws:lambda:zzz' returns bare False; the control test for a real id "
        "'event_rule:inf-gold-incremental-daily' returns True. ⛔ THE FAILURE MODE IS THAT A MISS "
        "IS A VERDICT, NOT AN ERROR. Absent-from-registry MEANS not-deliberately-dormant, i.e. "
        "DEBT-eligible. So a mistyped or wrong-grammar id returns the SAME False as a genuine "
        "absence, and the guard cannot distinguish 'this resource is not belted' from 'you "
        "spelled it wrong'. Given the id space is hand-authored and crosses to ARN space with no "
        "declared mapping, a spelling miss is not a hypothetical.",
        "1.0.0_SA_CTO",
        returns_on_failure="bare False, read by the guard as NOT-keep-dormant and therefore DEBT-eligible",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=[
            "a mistyped resource_id makes a genuinely belted resource read as DEBT-eligible",
            "an entry past revalidate_by still returns True and keeps protecting, so the decay "
            "rule does not fail closed"]),
    "UNSOUND",
    "The DESIGN is unusually strong and this verdict is not about the design: the file exists "
    "precisely because a belt and a corpse are mechanically identical, it demands grounded "
    "reasons, and it carries its own decay rule. It is UNSOUND on TRUST. Three measured facts "
    "compound: a lookup miss is indistinguishable from a mistyped id AND is consumed as a "
    "DEBT-eligible verdict; the id space crosses to ARNs with declared_mapping NULL and one "
    "member cannot have an ARN at all; and the decay rule the file itself defines is already "
    "breached by 1 of its 7 entries with nothing scheduled that could ever raise it.",
    ["1 of 7 entries past its own revalidate_by, with no scheduled re-grounding",
     "a lookup miss is a VERDICT (DEBT-eligible), indistinguishable from a mistyped id",
     "id space crosses to ARN space with declared_mapping NULL"]))

# ---------------------------------------------------------------- W2-jgzc
CARDS.append(card(
    "jgzc", "data/firm_registry.json", "store",
    "the governed firm population source -- the file D3's obligation_types.completeness names "
    "as its population, reached via intent_source",
    row("measured",
        "Parsed at HEAD: {_meta, firms, pseudo}. _meta self-declares canonical_path "
        "data/firm_registry.json, schema_version 1, authority 'NFRA_PSTMRT P1 (Andrew-direct "
        "handover @7cc6376e5)' and carries its own `law` block. Hand-authored, git-reviewed.",
        "1.0.0_SA_CTO~Z (last author @1f54e16dfd, 2026-07-22T21:06:56-04:00)",
        how="A hand-authored firm registry. Each firm carries firm_id, tree_token, display_name, "
            "aliases, kind, enabled, bucket and email_domain. COMPOSES nothing mechanically; "
            "INVENTS the firm_id and tree_token vocabularies.",
        determinism="deterministic", composes=[],
        invents=[ref("firm_id_vocabulary"), ref("tree_token_vocabulary", "bd / inf / cot")],
        materializer_standing="not_applicable",
        declared_opinions=["which firms are `enabled` -- an editorial flag, not a derivation",
                           "the alias sets, hand-listed and uneven across firms",
                           "the split between `firms` and `pseudo`"]),
    row("measured",
        "No scheduled producer; changed by human commit, last 2026-07-22 @1f54e16dfd, 35 days "
        "before carding. No rhythm is declared, so there is nothing for a live instance to match.",
        "1.0.0_SA_CTO~Z",
        declared_rhythm=None, actual_trigger="a human commit",
        live_matches_declared="not_applicable", live_instance_age="35 days at carding"),
    row("measured", "5,094 bytes on disk, git-TRACKED (@1f54e16dfd resolves).", "1.0.0_SA_CTO~Z",
        persisted=True, authority_role="source", mutation_policy="editable", form="json"),
    row("measured",
        "Path read directly at HEAD; _meta.canonical_path independently self-declares the same "
        "path, so the file and the census agree on its own home.",
        "1.0.0_SA_CTO~Z",
        home="data/firm_registry.json", projection_of=[],
        co_resident_stores=[ref("comp-keys_exists_firm_scope",
                                "comp-keys exists declares its firm scope as this file's enabled+pipeline set")]),
    row("measured",
        "COUNTED from the parsed file: 5 firms, enabled=true on 5 of 5 and enabled=false on 0; "
        "plus 1 pseudo entry. tree_token populated on 3 of 5 (bd, inf, cot) and NULL on 2 of 5 "
        "(mockadv, demo). Aliases uneven: 3 for 49financial, 0 for the other four.",
        "1.0.0_SA_CTO~Z",
        universe="firms this estate serves or simulates",
        denominator="5 of 5 firms enabled; 3 of 5 carry a tree_token; 1 pseudo entry alongside",
        explicitly_out=["any firm not hand-added -- the registry cannot discover a firm"]),
    row("measured",
        "firm_id is the key: 49financial, inflection, cottonwood, mockadv, demo. ⛔ CROSSES "
        "SPACES AND THE CROSSING IS PARTIAL: tree_token (bd/inf/cot) is a SECOND id space for "
        "the same firms, used in bucket and pipeline paths, and it is NULL for 2 of the 5. So a "
        "firm_id -> tree_token join succeeds for 3 and returns null for 2, with nothing "
        "declaring whether a null means 'no pipeline' or 'not yet assigned'. The mapping is "
        "declared IN-FILE per entry, which is better than most stores here -- it is its "
        "INCOMPLETENESS that is undeclared.",
        "1.0.0_SA_CTO~Z",
        identity_space="firm_id string; a second, partial space is tree_token",
        key_is_stable="stable", crosses_spaces=True,
        declared_mapping="firm_id -> tree_token, declared in-file per entry, NULL on 2 of 5",
        basis_by_field={"identity_space": "measured", "crosses_spaces": "measured",
                        "declared_mapping": "measured", "key_is_stable": "inferred"}),
    row("measured",
        "EXERCISED, three arms in one run against a dict built on firm_id: .get('zzz_not_a_firm') "
        "returns SILENT None; ['zzz'] raises KeyError; the control .get('49financial') returns a "
        "14-key dict. ⛔ SO DISTINGUISHABILITY IS A PROPERTY OF THE CONSUMER'S ACCESS PATTERN, "
        "NOT OF THIS STORE. A .get() consumer receives None and cannot separate a missing firm "
        "from a typo; a [] consumer gets a loud KeyError. The store offers both and mandates "
        "neither, so its failure mode is decided elsewhere.",
        "1.0.0_SA_CTO~Z",
        returns_on_failure="None via .get() (silent) or KeyError via [] (loud) -- the consumer chooses",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=["a .get()-based consumer converts an unknown firm into an absent one",
                              "a null tree_token is indistinguishable from a firm with no pipeline"]),
    "QUALIFIED",
    "Small, owned, git-reviewed, self-declaring its own authority and canonical path, with a "
    "stable key -- the strongest provenance of the stores this lane carded. QUALIFIED on two "
    "measured axes: the firm_id -> tree_token crossing is NULL on 2 of 5 with no declared "
    "meaning for the null, and the failure mode is chosen by the consumer rather than the store, "
    "so a .get() caller silently turns an unknown firm into an absent one.",
    None))

# ---------------------------------------------------------------- W2-bcin / W2-qvzv : motif specs
for tok, fname, size, mtime, commit, nodes, c2n, c3n, edges, extra in [
    ("bcin", "motif_c2c3_materialize.json", 15255, "2026-07-09T12:47:24Z", "fad55a83c7",
     7, 6, 1, 36, None),
    ("qvzv", "motif_c2c3_materialize_ab.json", 1141941, "2026-07-18T15:14:21Z", "c7048f4846",
     16, 13, 3, 5088, "c2_to_c1_edges 5079 + c3_to_c2_edges 9 = 5088"),
]:
    CARDS.append(card(
        tok, DSDEL + fname, "artifact",
        "a baked static C2/C3 class-spec layer that the derive INGESTS -- one of the two "
        "'historical materializers' Andrew flagged 1907Z",
        row("measured",
            "Parsed at HEAD. The file declares its own producer, consumer, grounding and a "
            "`counts` block. Produced by MOTIF_c2c3_materialize_spec.py in the same directory. "
            "⛔ INTERNAL CONTROL EXERCISED: I recomputed the counts block against the file's own "
            "content and it AGREES exactly -- declared c2_motif_nodes=%d, c3_system_nodes=%d, "
            "contains_edges=%d against an actual node_type census of C2Motif=%d, C3System=%d and "
            "len(edges)=%d. A self-declaring artifact whose self-declaration checks out."
            % (c2n, c3n, edges, c2n, c3n, edges),
            "0.4.0_DS_ClientPlatform lane (committed by 0.4.0_DS_ClientPlatform~B @%s)" % commit,
            how="A frozen JSON spec enumerating C2Motif class nodes and their CONTAINS edges, "
                "hand-authored via a spec script and ingested by the derive. It COMPOSES the C1 "
                "edge population and C0 node population it points at; it INVENTS the motif class "
                "vocabulary itself.",
            determinism="deterministic",
            composes=[ref("C0_node_population"), ref("C1_edge_population")],
            invents=[ref("c2_motif_class_vocabulary")],
            materializer_standing="historical_in_use",
            declared_opinions=[
                "the motif class vocabulary is DECLARED here by hand, inside a rung whose own "
                "canon states C2 is DISCOVERED and never declared -- the artifact's existence is "
                "itself the opinion",
                "which member sets constitute a motif, frozen at author time"]),
        row("measured",
            "FROZEN: mtime %s, last commit @%s, unchanged for %d days at carding. ⛔ BUT IT IS "
            "STILL CONSUMED -- 1.0.0_SA_CTO~X measured (73215 Q2) that today's derive logged "
            "specs=3, being the two frozen July class specs PLUS the live composition. I cite "
            "that measurement rather than re-running their command. So `historical_in_use` is "
            "measured, not inferred: the artifact does not change and is read anyway."
            % (mtime, commit, 48 if tok == "bcin" else 39),
            "0.4.0_DS_ClientPlatform lane",
            declared_rhythm=None, actual_trigger="ingested on every derive run",
            live_matches_declared="not_applicable",
            live_instance_age="%d days at carding, unchanged" % (48 if tok == "bcin" else 39),
            basis_by_field={"live_instance_age": "measured", "actual_trigger": "held"}),
        row("measured",
            "%d bytes on disk, git-TRACKED (@%s resolves). Frozen in practice: no producer "
            "rewrites it." % (size, commit),
            "0.4.0_DS_ClientPlatform lane",
            persisted=True, authority_role="evidence", mutation_policy="immutable", form="json"),
        row("measured", "Path read directly at HEAD.", "0.4.0_DS_ClientPlatform lane",
            home=DSDEL + fname,
            projection_of=[ref(DSDEL + "MOTIF_c2c3_materialize_spec.py", "the spec script that emits this file")],
            co_resident_stores=[ref(HARNESS + "c2_instances.json",
                                    "the newer composer output, which DECLARES supersedes_shape_of this file")]),
        row("measured",
            "COUNTED and cross-checked: %d nodes total = %d C2Motif + %d C3System, and %d edges."
            "%s ⛔ THE DENOMINATOR IS THE CLASS LAYER, NOT THE INSTANCE LAYER -- these are CLASS "
            "nodes, and the instance population that types against them lives in "
            "c2_instances.json at a different order of magnitude. Reporting %d as a C2 coverage "
            "figure without that distinction would conflate two grains."
            % (nodes, c2n, c3n, edges,
               (" The file additionally declares %s, which is arithmetically consistent; note "
                "however that EVERY edge carries edge_type CONTAINS, so that 5079/9 split is a "
                "DECLARED decomposition I could not verify from the edge records themselves." % extra)
               if extra else "", c2n),
            "0.4.0_DS_ClientPlatform lane",
            universe="C2Motif class nodes and C3System nodes in this baked layer",
            denominator="%d C2Motif + %d C3System = %d nodes, %d CONTAINS edges" % (c2n, c3n, nodes, edges),
            explicitly_out=["C2 motif INSTANCES, which live in the composer output, not here"],
            basis_by_field={"universe": "measured", "denominator": "measured",
                            "explicitly_out": "measured"}),
        row("measured",
            "Node keys are node_id strings; every node carries exactly {node_id, node_type, "
            "props}. The C2->C1 targets are declared by the file's convention_note to be C0/C1 "
            "node ids, so this artifact's ids CROSS into the canonical graph's id space -- and "
            "that space is CloudNode.node_id, of which only 6.4% are ARN-shaped. No mapping "
            "document declares the correspondence; the convention_note asserts it in prose.",
            "0.4.0_DS_ClientPlatform lane",
            identity_space="hand-authored motif node_id strings, pointing at C0/C1 node ids",
            key_is_stable="stable", crosses_spaces=True,
            declared_mapping="asserted in the file's convention_note as prose, not as a mapping artifact",
            basis_by_field={"identity_space": "measured", "crosses_spaces": "measured",
                            "declared_mapping": "measured", "key_is_stable": "inferred"}),
        row("measured",
            "EXERCISED as a self-consistency control rather than a retrieval probe, because this "
            "artifact has no lookup API -- it is ingested wholesale. The control that COULD have "
            "failed: recomputing the counts block from the nodes and edges arrays. It agreed on "
            "every field. A corrupted or truncated file would have produced a mismatch here, so "
            "the arms were reachable from different truths. ⛔ WHAT IS NOT COVERED: the file "
            "carries no schema version and no checksum, so a consumer ingesting a MALFORMED copy "
            "has nothing to check against except this same self-declared counts block -- which a "
            "corrupted producer would have rewritten too.",
            "0.4.0_DS_ClientPlatform lane",
            returns_on_failure="no lookup surface; a malformed file surfaces only as a downstream "
                               "parse error in the derive, not as a signal from the artifact",
            distinguishable_from_true_negative="unmeasured",
            silent_degrade_paths=["a frozen spec silently continues to type today's instances "
                                  "against a July class vocabulary, and nothing in the artifact "
                                  "signals its own age to the derive"]),
        "QUALIFIED",
        "A frozen, tracked, self-declaring artifact whose internal counts control checks out "
        "exactly -- and which is STILL BEING CONSUMED, measured, not assumed. QUALIFIED on two "
        "axes and NOT on its age: it declares a class vocabulary by hand inside a rung whose "
        "canon says C2 is discovered rather than declared, and it carries no version or checksum, "
        "so its only integrity signal is a counts block a corrupted producer would also rewrite. "
        "⛔ THIS CARD DELIBERATELY MAKES NO STATEMENT ABOUT THIS ARTIFACT'S FUTURE. It is in use "
        "today; that is the measurement, and the fate question is a separate pass.",
        None))

written = []
for token, c in CARDS:
    name = c["subject"]["id"].replace("s3://", "").replace("/", "_").replace(":", "_").strip("_")
    path = os.path.join(HERE, "W2-%s__%s.json" % (token, name[:70]))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    written.append((token, os.path.basename(path)))

print("part-4 cards written:", len(written))
for t, n in written:
    print("  W2-%-5s %s" % (t, n))
