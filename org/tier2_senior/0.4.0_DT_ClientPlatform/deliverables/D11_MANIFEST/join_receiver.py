#!/usr/bin/env python
"""TO-KEYFILL-JOIN -- join the L0 manifest's parts to the RATIFIED card registry.

ADMISSION IS STRICTLY BY THE RATIFIED REGISTRY. A part joins only when its id appears VERBATIM as a
`subject_id` in the registry at the RAT-committed state; nothing is parsed, fuzzed, basename-matched
or otherwise reconstructed. Everything else is UNJOINED and counted.

⛔ THE JOIN KEY IS A NAMED GAP AND I AM NOT INVENTING ONE. There is no registry-MINTED part id: the
registry's members carry {path, git_blob_id, subject_id} and the manifest's parts carry an `id` that
is a path string. 1.0.0_SA_CTO~X recorded this ("grain 'part'; a member-grain id is a named gap,
never invented"). So two readings of the certification arm exist and they differ by 26 rows:

  (a) LITERAL -- join only through a registry-minted part id. None exists, so 0 of 42 join and every
      part is unjoined.
  (b) OPERATIVE -- "registry-minted" means the identifier AS RATIFIED: a part joins on an EXACT
      match against a registry subject_id, and the arm's own clause "leave string-name misses
      unjoined" names the remainder.

THIS FILE IMPLEMENTS (b), and the text is why: under (a) there could be no string-name match at all,
so "leave string-name misses unjoined" would be vacuous. A clause that is vacuous under one reading
and operative under the other argues for the operative one. BOTH counts are printed every run, so a
ratifier who reads it the other way sees the (a) number without re-running anything.

EMISSION and DECLARATION are printed as TWO NUMBERS against ONE denominator, never summarised into
a rate and never alone (D11 PRD 10.2), with the parts that are unknown BY CONSTRUCTION named inside
unknown rather than silently dropped.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
REGISTRY = os.path.join(HERE, "card_population_registry.v1.json")
MANIFEST = os.path.join(HERE, "graph_object_manifest.declared.json")


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def index_members(members):
    """subject_id -> LIST of members. A MULTIMAP, NOT A DICT.

    `{m["subject_id"]: m for m in members}` COLLAPSES duplicate subject_ids silently, so the hit
    count below could never exceed 1 and the AMBIGUOUS branch was UNREACHABLE BY CONSTRUCTION
    (4.0.0_SA_CRO~X 012112Z, at this line). The 0 it printed was not a measurement of the
    population -- it was a property of the data structure, and it would have read 0 on a registry
    that DID carry duplicates.

    I reported that zero as "the rule was not exercised on this population". That was too kind to
    myself: the rule could not be exercised on ANY population, and the difference between those two
    statements is the whole finding.
    """
    idx = {}
    for m in members:
        idx.setdefault(m["subject_id"], []).append(m)
    return idx


def classify(parts, idx):
    """The ONE classifier. The mutant arm below runs THROUGH THIS, not beside it -- a control that
    re-implements the logic it is testing proves only that I can write the bug twice."""
    joined, unjoined, ambiguous = [], [], []
    for p in parts:
        hits = idx.get(p.get("id"), [])
        if len(hits) == 1:
            joined.append((p, hits[0]))
        elif len(hits) > 1:
            ambiguous.append((p, hits))
        else:
            unjoined.append(p)
    return joined, unjoined, ambiguous


def main():
    reg = load(REGISTRY)
    man = load(MANIFEST)
    ratified = reg.get("ratified_at_commit")
    if not ratified:
        print("REFUSING: the registry carries no ratified_at_commit. The join admits only")
        print("registry-RATIFIED members, and an unratified registry cannot supply them.")
        return 2
    members = reg["extension_population"]["members"]
    subs = index_members(members)
    parts = man["parts"]
    den = len(parts)

    print("JOIN -- manifest parts against the RATIFIED card registry")
    print("   ratified_at_commit : %s" % ratified[:12])
    print("   registry members   : %d" % len(members))
    print("   manifest parts     : %d   <- THE denominator; every count below is against it" % den)
    print()

    joined, unjoined, ambiguous = classify(parts, subs)

    dup_subjects = {s: v for s, v in subs.items() if len(v) > 1}
    print("   registry subject_ids carrying >1 member: %d  (the AMBIGUOUS branch's fuel)"
          % len(dup_subjects))
    print()
    print("=== AC1: per-part join line, admission strictly by the ratified registry ===")
    for p, m in joined:
        print("   JOINED     %-52s -> card %s" % (p["id"][:52], os.path.basename(m["path"])[:34]))
    for p, hits in ambiguous:
        # UNKNOWN, and BOTH CANDIDATES PRINTED -- the face requires the candidates to survive the
        # ambiguity. A count alone would discard the very thing a reader needs to resolve it.
        print("   AMBIGUOUS  %-52s -> %d candidates, NOT picked between, part left UNKNOWN"
              % (p["id"][:52], len(hits)))
        for h in hits:
            print("                 candidate: %s  blob %s"
                  % (h.get("path"), str(h.get("git_blob_id"))[:12]))
    for p in unjoined:
        print("   UNJOINED   %-52s -> no exact subject_id in the ratified registry" % str(p.get("id"))[:52])

    print()
    print("=== the two readings of the join key, both counted ===")
    print("   (a) literal, via a registry-MINTED part id : 0 of %d  (no such id exists on either side)" % den)
    print("   (b) operative, exact match as ratified     : %d of %d joined | %d unjoined | %d ambiguous"
          % (len(joined), den, len(unjoined), len(ambiguous)))
    print("   this run implements (b); (a) is printed so the other reading needs no re-run")

    # -- AC2: EMISSION and DECLARATION, per the PRD's own definitions ----------------------------
    # D11_SUBSTRATE_ANALYSIS_PRD.md 10.2, read at source rather than paraphrased:
    #   EMISSION    -- parts that CARRY all four receivers with a coherent claim_status.
    #                  A CONTRACT-SHAPE claim.
    #   DECLARATION -- the declared/unknown split printed BESIDE it. A KNOWLEDGE claim.
    #   "never summarised and never reported alone."
    # My first cut invented both predicates ("a part with a home", "claim_status == declared") and
    # got 42/42 for each -- the right shape by luck, from the wrong rule. The four receivers are the
    # ones the manifest grew for the card contract: grain, key, failure_mode, home_space.
    RECEIVERS = ("grain", "key", "failure_mode", "home_space")

    def carries_all(p):
        return all(p.get(r) not in (None, "", {}, []) for r in RECEIVERS)

    def coherent(p):
        for r in RECEIVERS:
            v = p.get(r)
            if isinstance(v, dict) and v.get("claim_status") in ("", None):
                return False
        return True

    emitted = [p for p in parts if carries_all(p) and coherent(p)]
    declared, unknown = [], []
    for p in parts:
        st = [(p.get(r) or {}).get("claim_status") for r in RECEIVERS if isinstance(p.get(r), dict)]
        (declared if st and all(s == "declared" for s in st) else unknown).append(p)

    # THE THREE PERMANENTLY UNKNOWN BY CONSTRUCTION, named from the PRD, never derived by a
    # predicate of mine: L2/L3/L4, this arc's own unbuilt destinations. "They are not debt and any
    # future count treating them as outstanding is reading the wrong thing." (PRD 10.2)
    PERMANENT_UNKNOWN = ("affinity_matrix", "identity_and_succession", "similarity_network_fusion")
    perm = [p for p in parts if p.get("id") in PERMANENT_UNKNOWN]

    print()
    print("=== AC2: EMISSION and DECLARATION against the ONE denominator %d ===" % den)
    print("   EMISSION    %d of %d  -- carries all four receivers (%s) with a coherent claim_status"
          % (len(emitted), den, ", ".join(RECEIVERS)))
    print("   DECLARATION %d declared / %d unknown of %d  -- the knowledge split"
          % (len(declared), len(unknown), den))
    print("   printed as TWO numbers, never summarised into a rate and never reported alone")
    # A BARE ZERO IS NOT A FINDING UNTIL IT SAYS WHAT IT IS ZERO OF. The per-receiver split:
    import collections as _cc
    for r in RECEIVERS:
        c = _cc.Counter()
        for p in parts:
            v = p.get(r)
            c[v.get("claim_status") if isinstance(v, dict) else
              ("no claim_status (%s)" % type(v).__name__)] += 1
        print("      %-13s %s" % (r, json.dumps(dict(c), sort_keys=True)))
    print("   so EMISSION is a SHAPE claim the manifest fully satisfies, while DECLARATION is a")
    print("   KNOWLEDGE claim it makes nowhere -- which is exactly why the PRD forbids reporting")
    print("   either one alone. Nothing in this round changed it: the keyfill declared the CARDS'")
    print("   key_expression, not the MANIFEST's part.key.")
    print()
    print("   PERMANENTLY UNKNOWN BY CONSTRUCTION, named from the PRD: %d of 3 found in this population"
          % len(perm))
    for p in perm:
        joined_ids = [x["id"] for x, _m in joined]
        print("      %-30s  L2/L3/L4 unbuilt destination | joined: %s | NOT DEBT"
              % (p["id"], "yes" if p["id"] in joined_ids else "no"))
    missing = [n for n in PERMANENT_UNKNOWN if n not in [p.get("id") for p in parts]]
    if missing:
        print("      NOT PRESENT in this population: %s" % ", ".join(missing))

    # -- AC3: L0 validation with its denominator, and the manifest preserved by digest ------------
    import hashlib
    with open(MANIFEST, "rb") as fh:
        man_bytes = fh.read()
    _CRLF, _LF = bytes([13, 10]), bytes([10])
    man_sha = hashlib.sha256(man_bytes.replace(_CRLF, _LF)).hexdigest()
    tracked = subprocess.run(["git", "rev-parse", "HEAD:org/tier2_senior/0.4.0_DT_ClientPlatform/"
                              "deliverables/D11_MANIFEST/graph_object_manifest.declared.json"],
                             cwd=ROOT, capture_output=True, text=True)
    print()
    print("=== AC3: L0 validation + manifest preservation ===")
    print("   manifest sha256 (LF-normalised) : %s" % man_sha)
    print("   manifest blob at HEAD           : %s"
          % (tracked.stdout.strip()[:16] if tracked.returncode == 0 else "NOT TRACKED"))
    schema_p = os.path.join(ROOT, "org", "standards", "L0_GRAPH_SUBSTRATE_MANIFEST.schema.json")
    try:
        import jsonschema
        with open(schema_p, encoding="utf-8") as fh:
            v = jsonschema.Draft202012Validator(json.load(fh))
        errs = sorted(v.iter_errors(man), key=lambda e: list(e.path))
        print("   L0 VALIDATION: %s over %d parts (denominator printed, never a bare PASS)"
              % ("PASS" if not errs else "FAIL (%d error(s))" % len(errs), den))
        for e in errs[:3]:
            print("      %s" % str(e.message)[:110])
    except ImportError:
        print("   L0 VALIDATION: NOT EXERCISABLE -- jsonschema unavailable; not the same as a PASS")

    # -- THE TWO-CANDIDATE MUTANT, WITH ITS SINGLE-CANDIDATE POSITIVE CONTROL --------------------
    # Required by 4.0.0_SA_CRO~X 012112Z / issuer 80151 / 80153: a zero on a branch nobody can reach
    # is not evidence. The two arms differ in ONE fact -- whether a second member shares the
    # subject_id -- and they run through the SAME index_members() and classify() as the live join.
    # A control that re-implements the logic it is testing proves only that I can write the bug
    # twice; a hand-computed len() would have "passed" against the dict too.
    #
    # THE INJECTION IS INTO A COPY OF THE MEMBER LIST, NEVER THE REGISTRY. The ratified bytes are
    # out of the repair boundary and are not touched; `mutant_members` is a new list.
    mutant_fired = None
    if joined:
        victim = joined[0][0]
        vid = victim.get("id")
        mutant_members = list(members) + [{"path": "MUTANT/second_card_same_subject.json",
                                           "git_blob_id": "0" * 40, "subject_id": vid}]
        m_joined, m_unjoined, m_ambiguous = classify(parts, index_members(mutant_members))
        m_hits = dict((p["id"], h) for p, h in m_ambiguous).get(vid, [])
        mutant_fired = any(p["id"] == vid for p, _h in m_ambiguous)
        print()
        print("=== THE AMBIGUOUS BRANCH: mutant + positive control, one fact apart ===")
        print("   subject under both arms : %s" % str(vid)[:60])
        print("   CONTROL  real registry     -> %d candidate  -> JOINED     (card %s)"
              % (len(subs.get(vid, [])), os.path.basename(joined[0][1]["path"])[:34]))
        print("   MUTANT   +1 same subject_id-> %d candidates -> %s"
              % (len(m_hits) or len(subs.get(vid, [])) + 1,
                 "AMBIGUOUS" if mutant_fired else "NOT AMBIGUOUS  <- BRANCH STILL DEAD"))
        for h in m_hits:
            print("                candidate printed, not picked: %s" % h.get("path"))
        print("   the two arms differ in ONE fact and land in DIFFERENT states, so the branch is")
        print("   REACHABLE and the live 0 above is a MEASUREMENT of the population, not an")
        print("   artifact of the index. Population unchanged under the mutant elsewhere: %s"
              % (len(m_joined) == len(joined) - 1 and len(m_unjoined) == len(unjoined)))

    print()
    print("=== RECONCILIATION ===")
    print("   joined %d + unjoined %d + ambiguous %d = %d of %d  %s"
          % (len(joined), len(unjoined), len(ambiguous),
             len(joined) + len(unjoined) + len(ambiguous), den,
             "OK" if len(joined) + len(unjoined) + len(ambiguous) == den else "DOES NOT RECONCILE"))
    # THE CONTROL IS A REFUSAL ARM, NOT A PRINT. A mutant that reports "branch dead" and still
    # exits 0 is a description of a control (the declared-but-unrun falsifier class, named by the
    # issuer at 80151). If AMBIGUOUS cannot be made to fire, this run is not evidence of anything.
    if mutant_fired is False:
        print("   REFUSING: the two-candidate mutant did not reach AMBIGUOUS.")
        return 1
    return 0 if len(joined) + len(unjoined) + len(ambiguous) == den else 1


if __name__ == "__main__":
    sys.exit(main())
