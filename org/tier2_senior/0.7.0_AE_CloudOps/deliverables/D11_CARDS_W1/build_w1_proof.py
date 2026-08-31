"""Emit the TO-CARD-R-W1-COX proof-of-spec instance, and exercise its own coverage control.

Everything the face can supply is READ FROM THE FACE: the criterion ids, their oracles, their
cell_refs, and the decomp_ref (doc + vintage). The first draft of this file TYPED the decomp doc
as a `DECOMP.md` path at vintage 3f88172e4d; the face says
`rectangle.final.certified.json @603f5546dc`. Both typed values were wrong, and a wrong
decomp_ref does not fail loudly -- the checker resolves it, reports a vintage-frame line, and the
proof reads VALID while pointing at a document that never governed this face.

THE COVERAGE CONTROL (issuer's "widened-set coverage mutant"). The checker enforces that every
acceptance row's cell_ref resolves to the decomp's id space. That is NOT the same question as
"are these the cells this FACE owns" -- this decomp declares 18 certified cells, of which the
issuer discharges 5 mechanism cells that no face may claim. So the mutant that matters widens the
set with CARD-R-m-1: a REAL id, in the decomp, which an id-space check ACCEPTS and only an
owned-set check REFUSES.

⛔ WHY THAT MUTANT IS WRITTEN THAT WAY. My last coverage mutant on the previous face tested
nothing at my own invocation -- it mutated a value the check did not read, so it "passed" by
being inert, and I reported it as UNSOUND rather than as a control. An inert mutant and a sound
one produce the same green line. The discriminator is whether the mutant is REJECTED FOR THE
REASON UNDER TEST, so each arm below asserts on the refusal's REASON, not merely on its verdict.
"""

from __future__ import annotations

import copy
import json
import re
import subprocess

FACE = ("org/tier2_senior/0.7.0_AE_CloudOps/task_orders/"
        "NFRA_SUBSTRATECARDING.TO-CARD-R-W1-COX.carding.md")
D = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W1/"
PROOF = ("org/tier2_senior/0.7.0_AE_CloudOps/deliverables/"
         "NFRA_SUBSTRATECARDING.TO-CARD-R-W1-COX_PROOF_OF_SPEC.json")
LANE = "0.7.0_AE_CloudOps~X"


def artifact_identity(path):
    """dirty -> PENDING-THIS-COMMIT; clean -> full last-change hex; neither -> refuse."""
    dirty = subprocess.run(["git", "status", "--porcelain", "--", path],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        return "PENDING-THIS-COMMIT"
    last = subprocess.run(["git", "log", "-1", "--format=%H", "--", path],
                          capture_output=True, text=True).stdout.strip()
    if not last:
        raise ValueError("cannot derive an identity for %s -- neither dirty nor committed; "
                         "REFUSING rather than typing one" % path)
    return last


def read_face():
    text = open(FACE, encoding="utf-8").read()
    crits = []
    for m in re.finditer(r'<criterion id="([^"]+)"([^>]*)>(.*?)</criterion>', text, re.S):
        refs = re.search(r'cell_refs="([^"]+)"', m.group(2))
        o = re.search(r"<oracle>(.*?)</oracle>", m.group(3), re.S)
        crits.append({"id": m.group(1),
                      "cell_refs": refs.group(1).split() if refs else [],
                      "oracle": " ".join(o.group(1).split()) if o else ""})
    dref = re.search(r"<decomp_ref>\s*(\S+)\s*@(\w+)", text)
    owned = re.search(r"<owned_cells>\s*(.*?)\s*</owned_cells>", text, re.S)
    return crits, dref.group(1), dref.group(2), owned.group(1).split()


def check_exact_ids(proof, crits, owned_cells):
    """The 4-id checker: the proof's acceptance ids EXACTLY the face's, and each face
    criterion's cell_refs within <owned_cells>.

    ⛔ THE TWO HALVES HAVE DIFFERENT SUBJECTS AND THAT IS NOT COSMETIC. The id half reads the
    PROOF; the cell_ref half reads the FACE, because `cell_refs` is not a legal acceptance
    property (additionalProperties:false) and proof-of-spec-check resolves the mapping from the
    TO. So the cell_ref arm is a control on the FACE-derived mapping this proof is scored
    against, NOT on anything this proof emits -- said plainly here because a mutant whose
    subject is misdescribed reads exactly like one whose subject is wrong."""
    face_ids = [c["id"] for c in crits]
    got = [r["criterion_id"] for r in proof["acceptance"]]
    if len(got) != len(set(got)):
        return "REFUSED", "duplicate criterion_id in acceptance"
    missing, extra = sorted(set(face_ids) - set(got)), sorted(set(got) - set(face_ids))
    if missing:
        return "REFUSED", "face criterion(s) with no acceptance row: %s" % ",".join(missing)
    if extra:
        return "REFUSED", "acceptance row(s) not on the face: %s" % ",".join(extra)
    for c in crits:
        off = sorted(set(c["cell_refs"]) - set(owned_cells))
        if off:
            return "REFUSED", ("cell_ref(s) outside this face's <owned_cells> on %s: %s"
                               % (c["id"], ",".join(off)))
        if not c["cell_refs"]:
            return "REFUSED", "no cell_ref on %s" % c["id"]
    return "ACCEPTED", "%d of %d face criteria, all cell_refs within owned set" % (
        len(got), len(face_ids))


def run_controls(proof, crits, owned):
    """Baseline FIRST -- a mutant battery whose base does not pass reports 'all fired' and
    means nothing. Each arm asserts on the REASON, not just the verdict."""
    arms = []

    v, why = check_exact_ids(proof, crits, owned)
    arms.append(("BASELINE untouched proof + face map", v, why, v == "ACCEPTED"))

    m = copy.deepcopy(proof)
    m["acceptance"].append({"criterion_id": "CARD-R-m-1"})
    v, why = check_exact_ids(m, crits, owned)
    arms.append(("WIDENED with CARD-R-m-1 (a REAL decomp cell the ISSUER discharges -- an "
                 "id-space check accepts this; only an owned-set check refuses it)",
                 v, why, v == "REFUSED" and "not on the face" in why))

    mc = copy.deepcopy(crits)
    mc[0]["cell_refs"] = ["CARD-R-m-3"]
    v, why = check_exact_ids(proof, mc, owned)
    arms.append(("FACE MAP REPOINTED to a mechanism cell (acceptance ids still exactly 4 -- "
                 "the arm the id-count half cannot see; subject is the face map, not the proof)",
                 v, why, v == "REFUSED" and "outside this face's <owned_cells>" in why))

    m = copy.deepcopy(proof)
    m["acceptance"] = m["acceptance"][:3]
    v, why = check_exact_ids(m, crits, owned)
    arms.append(("NARROWED to 3 rows", v, why,
                 v == "REFUSED" and "no acceptance row" in why))
    return arms


def refuse_coverage_contradiction(doc):
    """An artifact named in an EXCLUSION as unscored may not also claim artifact_covered_by.

    The exclusion and the coverage field are two carriers of ONE proposition, and nothing in the
    schema or in proof-of-spec-check compares them -- the checker's A_03 arm is satisfied by
    EITHER, so a row carrying both passes every automated gate while asserting a thing and its
    negation. It walks the EMITTED structure rather than the source because the defect it exists
    to catch was introduced by a blanket edit to the loop that builds these rows: correct line
    by line, false in the document."""
    excluded = [ex["item"] for ex in doc["declared_exclusions"]
                if "EXCLUDED FROM ACCEPTANCE SCORING" in ex["item"]]
    for a in doc["artifacts_produced"]:
        base = a["path_or_key"].rsplit("/", 1)[-1]
        named = [e for e in excluded if base in e]
        if named and a.get("artifact_covered_by"):
            raise ValueError(
                "COVERAGE CONTRADICTION on %s: artifact_covered_by=%s while an exclusion says "
                "no criterion scores it. Remove one; they cannot both be true"
                % (a["path_or_key"], a["artifact_covered_by"]))
    return len(excluded)


EV = {
  "W1-COX-AC1": (
    "command",
    "git ls-tree -r 9b2c687dc8 + git show per card -- the census's OWN instrument re-run over "
    "its own pin, never a retyped list",
    "81 cards at the census pin = 72 v3.1 + 8 v1 + 1 cells-carrier, RECONCILING with the "
    "census's declared 72/8/1. The 8 v1 rungs resolve 2 to this lane (C3i, comp_similar) and 6 "
    "to 0.8.0_AE_CloudComp -- the issuer's 3+3+2 owner partition confirmed BY DERIVATION, not "
    "accepted. A non-reconciling set would be a REFUSAL. This face discharges 2 of 8 wave-1 / "
    "35 remainder.",
    "2 of 8 wave-1 rungs; census denominator 8 @9b2c687dc8; 81 cards scanned", "PASS"),
  "W1-COX-AC2": (
    "command",
    "build_w1_cards.py -- each card authored from a READ of its subject at its current pin; "
    "summary_corpus.build_corpus()/coverage() run live for comp-similar, the c2c3_motif class "
    "read for C3.i",
    "NO MIGRATOR. The v1 cards located the subjects and supplied no answers -- visible in the "
    "output, where the v3.1 fields v1 never asked for (determinism, composes/invents, "
    "materializer_standing, live_matches_declared) carry honest unknown/unmeasured/absent "
    "values a migrator could not have produced without inventing them.",
    "2 of 2 cards authored from subject reads", "PASS"),
  "W1-COX-AC3": (
    "manual_read_with_citation",
    "git creator of each v1 rung, read at the census pin, against the face's <subjects/> block",
    "Both subjects' v1 creator is this lane. forward_disposition.set_by is NULL on both cards -- "
    "a forward disposition is the rung owner's call at the class close, never the carder's -- so "
    "set_by != carding lane passes BY CONSTRUCTION rather than by assertion. The other 6 rungs "
    "are unreachable from this seat by this same rule, which is why the face is 2 and not 8.",
    "2 of 2 cards owner-lane authored", "PASS"),
  "W1-COX-AC4": (
    "command",
    "substrate-card-check.py per card, rc read UNPIPED with rc=1 (card defect) and rc=2 "
    "(tool/usage) distinguished",
    "C3i.v3.1.json rc=0 VALID violations=0; comp_similar.v3.1.json rc=0 VALID violations=0. "
    "Both at SUBSTRATE_CARD.v3.1 (const 3.1, NOT the legacy const-1 path). key_expression "
    "carries basis from the measured|inferred|held|absent enum, and basis is the FLOOR: C3's "
    "key row reads `held` because the id JOINS are measured and id STABILITY is not; C3's "
    "cadence reads `absent` because DESIRED was quotable and APPLIED was never measured.",
    "2 of 2 at v3.1; denominator 8 (the census's wave-1 population)", "PASS"),
}


def build(crits, ddoc, dvintage):
    acceptance = []
    for c in crits:
        method, inv, out, den, status = EV[c["id"]]
        acceptance.append({"criterion_id": c["id"], "criterion_verbatim": c["oracle"],
                           "method": method, "invocation": inv,
                           "output_evidence": out, "denominator": den, "status": status,
                           "status_reason": "scored on this face's 2 subjects per the "
                                            "face_scope amended @c62de54192; the class-level 8 "
                                            "is the CLASS oracle, discharged at the issuer's "
                                            "class close over 3+3+2, never at a single face. A "
                                            "row claiming 8/8 here is FORM_DEFECT."})

    # PER-ROW, and the field is OMITTED where no criterion scores the artifact. A blanket
    # append inside this loop is what put artifact_covered_by on build_w1_proof.py while the
    # exclusion below said no AC scores it -- 3.0.0_SA_CVO~X STOPped @697a0134b4 on exactly that
    # contradiction. AC2's invocation names build_w1_cards.py, so AC2 covers the card builder;
    # AC4 scores the CARDS validating, not the builder, so the builder does not carry AC4.
    arts = []
    for name, kind, covered in (
            ("build_w1_cards.py", "script", ["W1-COX-AC2"]),
            ("C3i.v3.1.json", "config_data", ["W1-COX-AC2", "W1-COX-AC4"]),
            ("comp_similar.v3.1.json", "config_data", ["W1-COX-AC2", "W1-COX-AC4"]),
            ("build_w1_proof.py", "script", [])):
        row = {"path_or_key": D + name, "kind": kind,
               "commit_or_etag": artifact_identity(D + name),
               "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
               "deploy_evidence": "repo artifact; this face deploys nothing"}
        if covered:
            row["artifact_covered_by"] = covered
        arts.append(row)
    arts.append({"path_or_key": PROOF, "kind": "config_data",
                 "commit_or_etag": artifact_identity(PROOF),
                 "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE",
                 "deploy_evidence": "repo artifact; carried by the commit bearing this proof, "
                                    "which is the only PENDING row this --stat covers besides "
                                    "its builder"})

    return {
        "schema_version": "1.0",
        "to_id": "NFRA_SUBSTRATECARDING.TO-CARD-R-W1-COX",
        "decomp_ref": {"doc": ddoc, "vintage_commit": dvintage, "to_ref": FACE},
        "phase": "NON-BUILD-OTHER",
        "spec_ref": {"doc": FACE, "group": "OTHER", "vintage_commit": "c62de54192"},
        "assignee": LANE,
        "artifacts_produced": arts,
        "acceptance": acceptance,
        "controls": {},
        "declared_exclusions": [
            {"item": "the other 6 wave-1 rungs (0.8.0_AE_CloudComp's)",
             "reason": "AC3's owner-lane rule makes them unreachable from this seat; they are "
                       "carded on W1-CCY (3, CLOSED @2de6121a7c) and W1-CCX (3). Naming them "
                       "here is the reconcile AC1 demands, not a discharge."},
            {"item": "the global 8-of-8 receipt",
             "reason": "UNCOMPUTABLE-BY-CONSTRUCTION at any single face (face_scope "
                       "@c62de54192) -- the issuer's CLASS-CLOSE receipt over 3+3+2."},
            {"item": "the 5 mechanism cells (CARD-R-m-1..5)",
             "reason": "present on this face but DISCHARGED BY THE ISSUER, not owned here. They "
                       "are in the decomp's id space, which is why the coverage control below "
                       "mutates with one: an id-space check cannot tell them from mine."},
            {"item": ("build_w1_proof.py (and the proof instance it emits) EXCLUDED FROM "
                  "ACCEPTANCE SCORING, not from the commit"),
             "reason": "these two are the face's REPORTING instrument, not a subject any of the "
                       "four criteria score -- AC1/AC2/AC3/AC4 are about the census, the cards' "
                       "authorship and their validation. Naming them here is the honest route "
                       "the checker's A_03 arm offers; claiming artifact_covered_by on an AC "
                       "that does not score them would satisfy the same arm by asserting "
                       "something false. They are scored instead by proof-of-spec-check and by "
                       "both certifiers."},
            {"item": "a forward_disposition on either card",
             "reason": "the rung owner's call at the class close, never the carder's; set_by is "
                       "NULL by construction."},
            {"item": "any W4-COX act",
             "reason": "sequenced after this face's acceptance (Rule 27); no concurrent "
                       "opening. The %h->%H housekeeping pair likewise lands as its own commit "
                       "after the flip, never bundled here."}],
        "surprises": [
            "OBSERVATION/INERT -- the C3 overlapping-domain-cover exercises the OVERLAP THAT "
            "DEFINES IT exactly once: 12 membership assignments over 11 distinct members. A "
            "fact about the as-built baseline, never an argument against the rung; it is what a "
            "replacement cover has to improve, and nothing in v1 asked for it.",
            "OBSERVATION/INERT -- comp-similar's substrate matches only 5 of 1,863 ARN "
            "resources to >= 1 canonical motif (1,858 unmatched), so any motif-conditioned "
            "question runs on a near-empty subset. On the card's explicitly_out rather than in "
            "prose because the superseded-twin scan feeds a DECOMMISSION CANDIDATE list: a "
            "coverage hole there is a resource nobody proposes retiring.",
            "OBSERVATION/INERT -- this lane published a false absence during this face's "
            "pre-write hold ('there is no <subjects> container'), corrected by 3.0.0_SA_CVO~X. "
            "Both probes required a BARE tag and the tag carries attributes, so neither could "
            "match the thing being denied. The remedy is a positive control on the probe before "
            "publishing any absence.",
            "OBSERVATION/INERT -- this builder's first draft TYPED the decomp_ref as a "
            "DECOMP.md path @3f88172e4d; the face declares rectangle.final.certified.json "
            "@603f5546dc. Both typed values were wrong and NEITHER fails loudly: the checker "
            "resolves whatever vintage it is handed and prints a green vintage-frame line, so a "
            "proof can read VALID while citing a document that never governed it."],
        "session_log": ("org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-08-30/"
                        "session_TO-CARD-R-W1-COX.md"),
        "compiler_tools": [
            {"tool": "comp-to",
             "invocation": "comp-to NFRA_SUBSTRATECARDING.TO-CARD-R-W1-COX.carding",
             "result": "PASS -- bound before any read of the face, as the first act on the TO"},
            {"tool": "substrate-card-check.py",
             "invocation": "python .tools/substrate-card-check.py <card> (rc UNPIPED)",
             "result": "PASS -- 2 of 2 cards rc=0 VALID violations=0; rc=1 and rc=2 "
                       "distinguished throughout, and four earlier rc=1 rounds were card "
                       "defects of this lane's own making"},
            {"tool": "proof-of-spec-check.py",
             "invocation": "python .tools/proof-of-spec-check.py <this file> (rc UNPIPED)",
             "result": "see acceptance; run post-write by the emitting session and re-run by "
                       "both certifiers on the committed blob"}],
    }


def main():
    crits, ddoc, dvintage, owned = read_face()

    open(PROOF, "a", encoding="utf-8").close()   # exist, so its own row derives as PENDING
    proof = build(crits, ddoc, dvintage)
    arms = run_controls(proof, crits, owned)

    proof["controls"] = {
        "mutant": {
            "description": "the 4-id coverage checker (acceptance ids EXACTLY the face's; every "
                           "cell_ref within <owned_cells>), exercised baseline-first against a "
                           "widened set, a repointed cell_ref, and a narrowed set",
            "expected": "baseline ACCEPTED; all three mutants REFUSED, each naming the reason "
                        "under test",
            "observed": " | ".join("%s -> %s (%s)" % (n, v, w) for n, v, w, _ in arms),
            "status": "FIRED-AS-EXPECTED" if all(ok for _, _, _, ok in arms) else "UNSOUND"},
        "determinism": {
            "method": "re-derive the census enumeration and the C3 counts from their pins and "
                      "compare to the values carried on the cards",
            "observed": "81 = 72+8+1 reproduced against the census's declared split; C3=4, "
                        "C2=19, edges=12, assignments=12, distinct=11, overlap=1, systems "
                        "4/3/3/2 reproduced. Both certifiers independently reproduced the "
                        "comp-similar coverage in full (1863/1508/355/29, motif 5/1858, "
                        "membership 1254/609, variance 50, fork shadows 6) and the C3i "
                        "ACCEPT/REFUSE/REFUSE triple, the drift arm with a real one-byte "
                        "mutation digest b9f72b171f5293a7aad4130649bd4c77ec7b414ea9eb928f1b7ec"
                        "c8e1f228783 where this seat had only faked a digest.",
            "status": "STABLE"}}

    refuse_coverage_contradiction(proof)                       # BASELINE: must pass
    bad = copy.deepcopy(proof)
    for r in bad["artifacts_produced"]:
        if r["path_or_key"].endswith("build_w1_proof.py"):
            r["artifact_covered_by"] = ["W1-COX-AC2", "W1-COX-AC4"]    # the STOPped @697a shape
    try:
        refuse_coverage_contradiction(bad)
        guard_arm = "[XX] UNSOUND -- guard did NOT refuse the shape CVO STOPped"
    except ValueError as e:
        guard_arm = "[ok] REFUSED: %s" % e

    with open(PROOF, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(proof, fh, indent=1)

    print("WROTE %s" % PROOF)
    print("decomp_ref DERIVED: %s @%s" % (ddoc, dvintage))
    print("owned_cells: %s" % " ".join(owned))
    for a in proof["artifacts_produced"]:
        print("  %-13s %s" % (a["commit_or_etag"][:13], a["path_or_key"]))
    print("COVERAGE-CONTRADICTION GUARD:")
    print("  [ok] BASELINE emitted document passed")
    print("  %s" % guard_arm)
    print("CONTROLS (baseline first):")
    for n, v, w, ok in arms:
        print("  [%s] %-9s %s" % ("ok" if ok else "XX", v, n))
        print("        reason: %s" % w)


if __name__ == "__main__":
    main()
