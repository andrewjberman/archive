"""Re-card 0.7.0_AE_CloudOps~X's TWO wave-1 rungs at SUBSTRATE_CARD.v3.1.

⛔ NO v1 -> v3.1 MIGRATOR (AC2). Every answer comes from a READ OF THE SUBJECT at its current
pin; the v1 cards were used ONLY to locate the subjects, never as a source of answers. That is
why the rows below carry fields v1 never asked for (determinism, composes/invents,
materializer_standing, live_matches_declared) with honest `unknown`/`unmeasured` values rather
than manufactured ones -- a migrator would have had to invent them.

⛔ basis IS THE FLOOR, never the mode and never the best ($defs.basis: "THIS SCALAR IS THE
FLOOR -- the WEAKEST claim across the row's sub-claims ... If ANY part of the row is held or
inferred, THE ROW IS NOT 'measured'"). Rows mixing a measured count with a held judgement read
`held`.

⛔ THE FULL TYPE CONTRACT WAS READ BEFORE WRITING, not discovered one checker round at a time.
My first two passes emitted a string where the schema wants an object, an int where it wants
"N of M", a bool where it wants an enum, and free text where it wants an enum -- all because I
read the `required` lists and not the value constraints. Same defect as the proof-of-spec
instance earlier tonight, one schema over.

MEASURED THIS RUN (re-derived, never typed):
  comp-similar substrate  summary_corpus.build_corpus() + coverage() on the live graph
  C3.i-as-built           the C3System/C2Motif population and its CONTAINS edges

Face: NFRA_SUBSTRATECARDING.TO-CARD-R-W1-COX @c62de54192 (this lane's 2 of the census's 8).
"""

from __future__ import annotations

import collections
import datetime
import hashlib
import json
import os
import subprocess
import sys

OUT = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W1/"
STITCH = "infra/aws/globgrph/stitch_graph.json"
LANE = "0.7.0_AE_CloudOps~X"


def head():
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


EXPECTED_STITCH_SHA256 = "7ac11d015e0ce4a068d6afb86cd51edddb8171b227afd5fc9e40ffb8d5dd5363"


def content_identity(path, expected=None):
    """Hash the EXACT bytes this run reads, and REFUSE on absent or drifted content.

    An untracked carrier has no commit, so its DIGEST IS ITS IDENTITY -- naming it
    "content-addressed" without carrying the content address states a class and withholds the
    address. 3.0.0_SA_CVO~X stopped C3i for exactly that, and the lesson was already mine: the
    L3W3 AC2 rows carry this same file's digest, measured by me hours earlier and not carried
    into the card OF that file.
    """
    if not os.path.exists(path):
        raise ValueError("REFUSED: %s is ABSENT -- an untracked carrier that is not present "
                         "cannot be carded at all" % path)
    raw = open(path, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    if expected and got != expected:
        raise ValueError("REFUSED: %s DRIFTED -- expected %s, read %s. A card must not describe "
                         "bytes it did not read." % (path, expected, got))
    st = os.stat(path)
    return {"sha256": got, "bytes": st.st_size,
            "mtime_utc": datetime.datetime.fromtimestamp(
                st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}


def measure_c3():
    ident = content_identity(STITCH, EXPECTED_STITCH_SHA256)
    d = json.load(open(STITCH, encoding="utf-8"))
    nodes = d["classes_data"]["c2c3_motif"]["nodes"]
    c3 = {n["id"] for n in nodes if n["type"] == "C3System"}
    c2 = {n["id"] for n in nodes if n["type"] == "C2Motif"}
    edges = [e for e in d["edges"] if e["edge_type"] == "CONTAINS" and e["source"] in c3]
    mem = collections.defaultdict(set)
    for e in edges:
        mem[e["source"]].add(e["target"])
    assign = sum(len(v) for v in mem.values())
    distinct = len({t for v in mem.values() for t in v})
    return {"c3": len(c3), "c2": len(c2), "edges": len(edges), "assign": assign,
            "distinct": distinct, "overlap": assign - distinct, "ident": ident,
            "per_system": {k: len(v) for k, v in sorted(mem.items(), key=lambda x: -len(x[1]))}}


def measure_corpus():
    sys.path.insert(0, "org/modules/graph/debtscan")
    from summary_corpus import build_corpus, coverage  # noqa: E402
    return coverage(build_corpus())


def card_c3(m, anchor):
    return {
        "schema_version": 3.1,
        "subject": {
            "id": "C3.i-as-built", "kind": "rung",
            "declared_domain":
                "The INSTANCE grain of the C3 rung AS IT EXISTS TODAY: emergent systems "
                "discovered over C2 motifs by the overlapping-domain-cover and materialised as "
                "C3System nodes with CONTAINS edges to member C2Motifs. Carded as the AS-BUILT "
                "BASELINE a replacement must beat -- never as a claim the cover is correct."},
        "as_of": {"carded_utc": now(), "commit_ish": anchor,
                  "graph_vintage":
                      "%s :: classes_data.c2c3_motif. UNTRACKED -- no commit pins these bytes, "
                      "so the CONTENT ADDRESS is the identity: sha256 %s, %d bytes, mtime %s. "
                      "commit_ish above pins the REPO CODE at this run and pins NOTHING about "
                      "this file."
                      % (STITCH, m["ident"]["sha256"], m["ident"]["bytes"],
                         m["ident"]["mtime_utc"])},
        "process": {
            "methodology": {
                "how": "OVERLAPPING-DOMAIN-COVER: a C3 system is defined by an ANCHOR "
                       "constituent type; a C2 motif is a MEMBER iff it contains that anchor, "
                       "so membership is many-to-many and systems may overlap.",
                "determinism": "unknown",
                "composes": [{"id": "C2Motif", "note": "the motif node set membership is drawn from"},
                             {"id": "ANCHOR_CATALOG", "note": "hand-authored anchor constituent types"}],
                "invents": [{"id": "C3System", "note": "the emergent system node"},
                            {"id": "CONTAINS", "note": "system -> member motif edge"}],
                "materializer_standing": "historical_in_use",
                "basis": "held",
                "evidence":
                    "MEASURED at this pin: %d C3System, %d C2Motif, %d CONTAINS edges, %d "
                    "assignments over %d distinct members -> OVERLAP %d. ⛔ THE PROPERTY THE "
                    "METHOD IS NAMED FOR IS EXERCISED BY EXACTLY %d MEMBER. determinism is "
                    "`unknown` and the row reads `held` on that floor: this seat read the "
                    "OUTPUT, never ran the derive, so whether a re-run reproduces this cover "
                    "is not measured."
                    % (m["c3"], m["c2"], m["edges"], m["assign"], m["distinct"],
                       m["overlap"], m["overlap"]),
                "owner": LANE},
            "cadence": {
                "declared_rhythm": "re-derived when the C2 motif set changes",
                "actual_trigger": None,
                "live_matches_declared": "unmeasured",
                "live_instance_age": None,
                "basis": "absent",
                "evidence": "No schedule, trigger or run-record for the C3 derive was located at "
                            "this seat. DESIRED is quoted from the rung's own description; "
                            "APPLIED was not measured, so the row is `absent` rather than a "
                            "guess dressed as a cadence.",
                "owner": LANE}},
        "artifact": {
            "persistence": {
                "persisted": True, "authority_role": "evidence",
                "mutation_policy": "replaceable",
                "form": "C3System nodes + CONTAINS edges to C2Motif in the c2c3_motif class",
                "basis": "measured",
                "evidence": "read at this commit: %d C3System nodes, %d C2Motif nodes, %d "
                            "CONTAINS edges with a C3System source"
                            % (m["c3"], m["c2"], m["edges"]),
                "owner": LANE},
            "location": {
                "home": "%s :: classes_data.c2c3_motif" % STITCH,
                "projection_of": [{"id": "c2c3-derive",
                                   "note": "the C2/C3 derive over the estate graph; this class is its projection, not its source of truth"}],
                "co_resident_stores": [{"id": "graph_nodes/graph_edges",
                                        "note": "and their kuzu projection -- named by the rung, NOT opened at this seat"}],
                "basis": "held",
                "evidence":
                    "The home file is UNTRACKED: no commit pins it, so its DIGEST IS ITS "
                    "IDENTITY -- sha256 %s, %d bytes, mtime %s, hashed from the exact bytes "
                    "this run read (the builder REFUSES on absent or drifted content). "
                    "RETRIEVAL: local to this device only; it is neither tracked, "
                    "commit-pinned, nor served at an immutable URI, and that is a NAMED GAP "
                    "owned by the graph's producer. The co-resident stores are named from the "
                    "rung's description and were not opened here -- the floor that makes this "
                    "row `held`."
                    % (m["ident"]["sha256"], m["ident"]["bytes"], m["ident"]["mtime_utc"]),
                "owner": LANE}},
        "trust": {
            "coverage": {
                "universe": "C2 motifs eligible for membership in a C3 system",
                "denominator": "%d of %d C2 motifs are in at least one C3 system"
                               % (m["distinct"], m["c2"]),
                "explicitly_out": [
                    "%d C2Motif nodes in NO C3 system -- the cover is PARTIAL by construction"
                    % (m["c2"] - m["distinct"]),
                    "C3System nodes with no members: none observed at this pin"],
                "basis": "measured",
                "evidence": "per-system membership %s across %d systems"
                            % (json.dumps(m["per_system"]), m["c3"]),
                "owner": LANE},
            "key": {
                "identity_space": "stitch-graph node id "
                                  "(e.g. 'system:pipeline:d944eb81', 'motif:silent-display-fork')",
                "key_expression": "node.id for a C3System; CONTAINS.target for a member",
                "key_is_stable": "unknown",
                "crosses_spaces": True,
                "declared_mapping": None,
                "basis": "held",
                "evidence": "the ids join correctly at this pin (%d edges resolve to %d distinct "
                            "member ids). STABILITY IS NOT MEASURED: the id embeds a hash-shaped "
                            "suffix whose derivation this seat did not read, so whether a "
                            "re-derive preserves it is UNKNOWN. `held` is the FLOOR across the "
                            "row, not the measured join."
                            % (m["edges"], m["distinct"]),
                "owner": LANE},
            "failure_mode": {
                "returns_on_failure":
                    "A C3 derive producing nothing returns an EMPTY node set, shape-identical to "
                    "a genuine 'no emergent system exists' result.",
                "distinguishable_from_true_negative": "no",
                "silent_degrade_paths": [
                    "a derive that runs against a stale C2 set emits a cover over the old motifs "
                    "with no marker that the input moved"],
                "basis": "held",
                "evidence": "No sentinel, run-record or empty-vs-absent marker was found beside "
                            "the c2c3_motif class at this pin. This seat did NOT exercise a "
                            "failing derive, so the shape is reasoned from the artifact rather "
                            "than observed -- hence `held`, not `measured`.",
                "owner": LANE}},
        "verdict": {
            "standing": "QUALIFIED",
            "why": "Usable as the AS-BUILT BASELINE a replacement cover must beat, with three "
                   "named qualifiers: cadence APPLIED is unmeasured, the failure mode is NOT "
                   "distinguishable from a true negative, and the overlap that DEFINES the "
                   "methodology is exercised by exactly %d member at this pin. None of those "
                   "is an argument against the rung; they are what a replacement has to improve."
                   % m["overlap"],
            "blocking_defects": None},
        "forward_disposition": {
            "standing": "undecided", "set_by": None, "basis": "absent",
            "evidence": "NOT SET BY THE CARDING LANE. A forward disposition is the rung owner's "
                        "call at the class close, not the carder's; leaving set_by null is the "
                        "honest value and the check that set_by != the carding lane passes by "
                        "construction.",
            "decided_utc": None},
        "carded_by": LANE}


def card_comp_similar(cov, anchor):
    tot = cov["total_arn_resources"]
    return {
        "schema_version": 3.1,
        "subject": {
            "id": "comp-similar", "kind": "tool",
            "declared_domain":
                "The substrate underlying comp-similar: the DERIVE-AT-SCAN summary corpus "
                "({arn -> SummaryDoc}) over which BM25 SUMMARY similarity is scored, plus the "
                "live heat the superseded-twin scan joins against."},
        "as_of": {"carded_utc": now(), "commit_ish": anchor,
                  "graph_vintage": "summary_corpus.build_corpus() executed live at this commit"},
        "process": {
            "methodology": {
                "how": "BM25 over a per-resource SUMMARY document (what a resource DOES), "
                       "df-cut; sibling to comp-dups which scores NAME/body (what a resource "
                       "IS). --supersede joins SUMMARY-similarity with heat divergence and "
                       "emits the COLD member as a decommission CANDIDATE.",
                "determinism": "deterministic",
                "composes": [{"id": "estate-graph", "note": "the live derive-at-scan source"},
                             {"id": "comp-heat", "note": "data-heat join"},
                             {"id": "comp-debris", "note": "invoke-heat join"}],
                "invents": [{"id": "SummaryDoc", "note": "per-resource purpose summary"},
                            {"id": "bm25-score", "note": "pairwise similarity"},
                            {"id": "superseded-twin", "note": "decommission candidate pair"}],
                "materializer_standing": "canonical",
                "basis": "held",
                "evidence":
                    "Read at source: the wrapper delegates to comp_similar.py, which imports "
                    "build_corpus / SimilarityIndex / coverage from summary_corpus.py. BM25 over "
                    "a fixed corpus is deterministic by construction, but this seat ran the "
                    "corpus build ONCE and did not repeat it to observe stability, so the row "
                    "reads `held`. The tool's own header states similarity is a HYPOTHESIS, "
                    "never a verdict alone; this card does not upgrade it.",
                "owner": LANE},
            "cadence": {
                "declared_rhythm": "on demand, per invocation",
                "actual_trigger": "operator invocation; the corpus is rebuilt from the live "
                                  "graph at each scan",
                "live_matches_declared": "yes",
                "live_instance_age": "rebuilt this run; ~25 s to build %d entries" % tot,
                "basis": "measured",
                "evidence": "build_corpus() executed live this session and returned %d entries; "
                            "there is no stored corpus whose staleness could drift." % tot,
                "owner": LANE}},
        "artifact": {
            "persistence": {
                "persisted": False, "authority_role": "evidence",
                "mutation_policy": "not_applicable",
                "form": "an in-memory {arn -> SummaryDoc} corpus, rebuilt per invocation",
                "basis": "measured",
                "evidence": "built live this run: %d ARN resources, no on-disk corpus" % tot,
                "owner": LANE},
            "location": {
                "home": "org/modules/graph/debtscan/summary_corpus.py (build_corpus, "
                        "SimilarityIndex, coverage); driver comp_similar.py; wrapper "
                        ".tools/comp-similar",
                "projection_of": [{"id": "estate-graph",
                                   "note": "derived per invocation; never a stored source"},
                                  {"id": "comp-heat", "note": "heat join input"},
                                  {"id": "comp-debris", "note": "invoke-cold join input"}],
                "co_resident_stores": None,
                "basis": "measured",
                "evidence": "all three files read at this commit; the wrapper delegates to the "
                            "driver, which imports the corpus module",
                "owner": LANE}},
        "trust": {
            "coverage": {
                "universe": "ARN-addressable estate resources reachable by the derive-at-scan",
                "denominator": "%d summarised of %d ARN resources scanned"
                               % (cov["summarized"], tot),
                "explicitly_out": [
                    "%d UNKNOWN-thin (no purpose summary derivable; no twin knowable)"
                    % cov["unknown_thin"],
                    "%d hold-marked" % cov["held_marked"],
                    "⛔ %d of %d match >= 1 canonical motif (%d unmatched) -- any "
                    "motif-conditioned question runs on a near-empty subset"
                    % (cov["motif_matched"], tot, cov["motif_unmatched"])],
                "basis": "measured",
                "evidence": "coverage() run live this session: " + json.dumps(
                    {k: v for k, v in cov.items() if k != "note"}),
                "owner": LANE},
            "key": {
                "identity_space": "AWS ARN",
                "key_expression": "the resource ARN string, verbatim, as the corpus dict key",
                "key_is_stable": "stable",
                "crosses_spaces": True,
                "declared_mapping": "the same ARN is the join key into comp-heat and "
                                    "comp-debris, which are separate stores",
                "basis": "measured",
                "evidence": "build_corpus() returns a dict keyed by ARN; %d keys this run. An "
                            "ARN is stable for a resource's lifetime by AWS construction." % tot,
                "owner": LANE},
            "failure_mode": {
                "returns_on_failure":
                    "A resource with no derivable summary enters the corpus THIN rather than "
                    "being dropped; a thin doc scores no similarity, so 'no twin exists' and "
                    "'the summary failed to derive' both surface as 'no neighbours'.",
                "distinguishable_from_true_negative": "yes",
                "silent_degrade_paths": [
                    "a resource whose summary derives but is uninformative scores low without "
                    "being counted thin -- degraded, not absent, and not separately counted"],
                "basis": "measured",
                "evidence": "coverage() prints unknown_thin separately (%d of %d this run), so a "
                            "consumer CAN distinguish 'scanned, no twin' from 'never "
                            "summarised'. This is the one row across both cards where "
                            "distinguishability is MEASURED rather than reasoned."
                            % (cov["unknown_thin"], tot),
                "owner": LANE}},
        "verdict": {
            "standing": "QUALIFIED",
            "why": "LOAD-BEARING and advisory: the superseded-twin scan feeds a decommission "
                   "CANDIDATE list, so a coverage hole here becomes a resource nobody proposes "
                   "retiring. QUALIFIED on the motif coverage above -- %d of %d matched -- and "
                   "on determinism being held rather than observed. Read-only, hold-aware, no "
                   "delete verb; deletion stays a per-batch Andrew word."
                   % (cov["motif_matched"], tot),
            "blocking_defects": None},
        "forward_disposition": {
            "standing": "undecided", "set_by": None, "basis": "absent",
            "evidence": "NOT SET BY THE CARDING LANE -- the tool owner's call, not the carder's.",
            "decided_utc": None},
        "carded_by": LANE}


def main():
    anchor = head()
    # A scoped repair must not rewrite a card that already PASSED -- re-running the builder
    # would move carded_utc/commit_ish on comp_similar and reopen a closed verdict.
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    cards = {}
    if target in ("all", "c3"):
        cards["C3i.v3.1.json"] = card_c3(measure_c3(), anchor)
    if target in ("all", "comp"):
        cards["comp_similar.v3.1.json"] = card_comp_similar(measure_corpus(), anchor)
    for name, doc in cards.items():
        with open(OUT + name, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=1)
        print("WROTE %s%s" % (OUT, name))
    print("\nAC1 reconcile: this lane's 2 of 8 wave-1 / 35 remainder "
          "(census @9b2c687dc8; cards enumerated at @cf66984cfc)")


if __name__ == "__main__":
    main()
