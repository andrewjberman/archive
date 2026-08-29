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
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
REGISTRY = os.path.join(HERE, "card_population_registry.v1.json")
MANIFEST = os.path.join(HERE, "graph_object_manifest.declared.json")
PRESERVED = os.path.join(HERE, "preserved")

# THE ACTIVE PRE-FILL MANIFEST, named by 3.0.0_SA_CVO~X 013801Z. Held as an EXPECTATION to refuse
# on, never as a value to write: preservation must capture the artifact the certifier named, and an
# existing preserved/ file for a DIFFERENT artifact (47f583e6) is not evidence about this one.
PREFILL_DECLARED = "e840260d7f6376c2e28c011e85c2236ca60dd7731181beb8e9fcdae669377c69"
CARD_PIN = "cf66984cfc"          # the cards' v3.1 pin, cited in every declared receiver's evidence
CRLF, LF = bytes([13, 10]), bytes([10])


def lf_sha256(raw):
    """LF-normalised, because a CRLF checkout and an LF blob are the same source and different
    bytes. A digest that does not say which it took is not an identity."""
    return hashlib.sha256(raw.replace(CRLF, LF)).hexdigest()


def dotted(obj, path):
    """(value, present). ABSENT and NULL are different failures and are reported differently."""
    cur = obj
    for seg in path.split("."):
        if not isinstance(cur, dict) or seg not in cur:
            return None, False
        cur = cur[seg]
    return cur, True


def blank(v):
    return v is None or (isinstance(v, str) and not v.strip()) or v == [] or v == {}


def key_admission(card, pred):
    """THE PREDICATE IS READ FROM THE RATIFIED REGISTRY, NEVER RECONSTRUCTED HERE.

    I got this wrong once in exactly the way the order warned against. Rebuilding the predicate from
    the TO's prose ("all_non_blank; basis measured/held/inferred; key_expression required") gave
    25 ADMITTED / 1 NOT_ADMITTED. The RATIFIED predicate names EIGHT required fields -- it also
    requires declared_mapping, evidence and owner -- and gives 23 / 3. A reconstruction is a
    LOOSENING even when it is written in good faith, because the fields you forget are exactly the
    ones you did not think of. `pred` is therefore the registry's object, passed in.
    """
    fails = []
    if pred.get("all_non_blank"):
        for f in pred["required_fields"]:
            v, present = dotted(card, f)
            if not present:
                fails.append("%s ABSENT" % f)
            elif blank(v):
                fails.append("%s blank/null" % f)
    basis, _p = dotted(card, "trust.key.basis")
    if basis not in pred.get("basis_allowed", []):
        fails.append("trust.key.basis=%r not in %s" % (basis, pred.get("basis_allowed")))
    return (not fails), fails


def prior_preserved_ok(prior_path):
    """Is an EXISTING preserved pre-fill trustworthy? A PURE decision, so the tampered-copy mutant
    can drive it directly (the gate_check() pattern from the registry compile).

    4.0.0_SA_CRO~X 021147Z: the re-run branch tested os.path.exists(prior) and nothing else, so a
    post-fill re-run would announce "the pre-fill IS already preserved" about a file that had since
    been replaced, truncated or corrupted -- FAIL-OPEN, and the louder failure (a missing file) was
    the only one it could see. A NAME IS NOT AN IDENTITY: open the thing and hash it.
    """
    if not os.path.exists(prior_path):
        return False, None, "ABSENT"
    with open(prior_path, "rb") as fh:
        d = lf_sha256(fh.read())
    if d != PREFILL_DECLARED:
        return False, d, "DIGEST MISMATCH -- the preserved file is not the declared pre-fill"
    return True, d, "digest matches the declared pre-fill"


def preserve_prefill(apply, prior_path=None, active_override=None):
    """ACT 4 / AC3: the ACTIVE pre-fill manifest, digest-addressed, BEFORE any write.

    The ordering is the whole control: preserved-after-write preserves the wrong artifact and reads
    identically in the output. Re-run safe -- once the fill has landed the active digest is no
    longer the pre-fill, so the function REFUSES rather than preserving a post-fill copy under a
    pre-fill name.
    """
    with open(MANIFEST, "rb") as fh:
        raw = fh.read()
    active = active_override or lf_sha256(raw)
    dest = os.path.join(PRESERVED, "graph_object_manifest.PREFILL_%s.json" % active[:8])
    prior = prior_path or os.path.join(
        PRESERVED, "graph_object_manifest.PREFILL_%s.json" % PREFILL_DECLARED[:8])
    print("=== AC3 step 1: PRESERVE THE ACTIVE PRE-FILL, BEFORE ANY WRITE ===")
    print("   active manifest sha256 (LF) : %s" % active)
    print("   declared active pre-fill    : %s  MATCH=%s"
          % (PREFILL_DECLARED, active == PREFILL_DECLARED))
    if active != PREFILL_DECLARED:
        ok, dig, why = prior_preserved_ok(prior)
        print("   prior preservation: %s  (%s)" % (
            (dig[:16] if dig else "no file"), why))
        if ok:
            print("   the active manifest is NOT the pre-fill, but the pre-fill IS already preserved")
            print("   at %s and its bytes were HASHED, not merely found."
                  % os.path.basename(prior))
            return PREFILL_DECLARED, prior, True
        print("   REFUSING: the active manifest is not the declared pre-fill, and the preserved")
        print("   pre-fill is %s. Writing now would land on unmeasured state." % why)
        return active, None, False
    if os.path.exists(dest):
        with open(dest, "rb") as fh:
            same = lf_sha256(fh.read()) == active
        print("   already preserved, bytes identical: %s   %s" % (same, os.path.basename(dest)))
        return active, dest, same
    if apply:
        if not os.path.isdir(PRESERVED):
            os.makedirs(PRESERVED)
        with open(dest, "wb") as fh:
            fh.write(raw)
        with open(dest, "rb") as fh:
            ok = lf_sha256(fh.read()) == active
        print("   PRESERVED -> %s   round-trip digest match: %s" % (os.path.basename(dest), ok))
        return active, dest, ok
    print("   DRY RUN -- would preserve to %s" % os.path.basename(dest))
    return active, dest, True


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


def fill_key(part, card, member):
    """Write the DECLARED key receiver from an ADMITTED 1:1 card.

    Only the nine fields the L0 schema declares; the receiver is additionalProperties:false and
    carries NO mapping_digest slot, so the mapping digest goes in `evidence`, the contract's own
    slot. I invented card fields once on this arc and took 7 of 18 INVALID for it.
    """
    k = card["trust"]["key"]
    card_mapping = k.get("declared_mapping")
    crosses = k.get("crosses_spaces")
    # "MAPPING DIGEST WHERE APPLICABLE" IS DECLARED BY THE L0 SCHEMA, NOT JUDGED BY ME. part.key
    # allOf[2]/[3]: declared + crosses_spaces true REQUIRES a non-blank declared_mapping; declared +
    # crosses_spaces false REQUIRES it null. So applicability is crosses_spaces, and I do not parse
    # the card's prose to decide whether a mapping "really" applies -- 20 admitted cards carry the
    # string "NONE NEEDED -- ..." in that field with crosses_spaces false, which is the CARD's way
    # of saying no mapping and the MANIFEST's null is the same fact in the receiver's vocabulary.
    mapping = card_mapping if crosses is True else None
    mdig = (lf_sha256(mapping.encode("utf-8"))
            if isinstance(mapping, str) and mapping.strip() else None)
    ev = ("DECLARED by TO-KEYFILL-JOIN from an ADMITTED 1:1 registry member. card %s @ %s; "
          "registry subject_id %s; blob %s. Admission by the RATIFIED registry's own key predicate "
          "(receiver_source_populations.key.admission_predicate), read from the registry, not "
          "reconstructed." % (member["path"], CARD_PIN, member["subject_id"],
                              str(member.get("git_blob_id"))[:12]))
    if crosses is not True and isinstance(card_mapping, str) and card_mapping.strip():
        # NOTHING IS SILENTLY DISCARDED. The receiver field must be null here, so the card's own
        # sentence is carried into evidence rather than dropped on the floor.
        ev += (" The card's declared_mapping field is not carried into the receiver because "
               "crosses_spaces is %r and the schema requires null there; the card's own text is "
               "retained here verbatim: %r" % (crosses, card_mapping[:300]))
    if mdig:
        # "mapping digest where applicable" -- applicability is decided MECHANICALLY (the card
        # declares a non-blank declared_mapping), never by parsing the prose to judge whether a
        # mapping "really" applies. The digest identifies the DECLARATION TEXT; it does not assert
        # that a mapping exists, and several cards declare "NONE NEEDED" in this field.
        ev += " mapping digest sha256:%s over the card's declared_mapping string." % mdig[:16]
    part["key"] = {
        "claim_status": "declared",
        "identity_space": k.get("identity_space"),
        "key_expression": k.get("key_expression"),
        "key_is_stable": k.get("key_is_stable"),
        "crosses_spaces": k.get("crosses_spaces"),
        "declared_mapping": mapping,
        "basis": k.get("basis"),
        "evidence": ev,
        "owner": k.get("owner"),
    }
    return mdig


def main():
    apply = "--apply" in sys.argv
    reg = load(REGISTRY)
    # THE RAT GATE IS FIRST, AND IT HAS TO BE FIRST TO MEAN WHAT I SAID IT MEANT.
    # 4.0.0_SA_CRO~X 021147Z: the manifest was loaded ONE LINE ABOVE this gate while the notice and
    # the proof both claimed the arm "exits before any manifest or card read". The arm did fire and
    # did return 2 -- so every test passed -- but the SENTENCE ABOUT IT WAS FALSE, and the ordering
    # a reader was relying on did not exist. An arm that returns the right code for the wrong reason
    # is the exact shape this file keeps being refused for. Nothing below this gate is read until it
    # passes: not the manifest, not a card, not the predicate.
    ratified = reg.get("ratified_at_commit")
    if not ratified:
        print("REFUSING: the registry carries no ratified_at_commit. The join admits only")
        print("registry-RATIFIED members, and an unratified registry cannot supply them.")
        print("   nothing has been read past this point: manifest UNREAD, cards UNREAD.")
        return 2
    man = load(MANIFEST)
    members = reg["extension_population"]["members"]
    subs = index_members(members)
    parts = man["parts"]
    den = len(parts)

    print("JOIN -- manifest parts against the RATIFIED card registry")
    print("   ratified_at_commit : %s" % ratified[:12])
    print("   registry members   : %d" % len(members))
    print("   manifest parts     : %d   <- THE denominator; every count below is against it" % den)
    print()
    pred = reg["receiver_source_populations"]["key"]["admission_predicate"]
    print("   RATIFIED key admission predicate, READ FROM THE REGISTRY (not reconstructed):")
    print("      all_non_blank : %s" % pred.get("all_non_blank"))
    print("      basis_allowed : %s" % pred.get("basis_allowed"))
    print("      required      : %d field(s)" % len(pred.get("required_fields", [])))
    print()
    prefill_digest, prefill_path, preserved_ok = preserve_prefill(apply)
    if not preserved_ok:
        return 3
    print()

    joined, unjoined, ambiguous = classify(parts, subs)

    dup_subjects = {s: v for s, v in subs.items() if len(v) > 1}
    print("   registry subject_ids carrying >1 member: %d  (the AMBIGUOUS branch's fuel)"
          % len(dup_subjects))
    print()
    print("=== AC1: per-part join line, admission strictly by the ratified registry ===")
    admitted, not_admitted, mapping_digests = [], [], 0
    for p, m in joined:
        card = load(m["path"])
        ok, fails = key_admission(card, pred)
        if ok:
            if fill_key(p, card, m):
                mapping_digests += 1
            admitted.append((p, m))
            print("   ADMITTED   %-46s -> declared from card %s"
                  % (p["id"][:46], os.path.basename(m["path"])[:30]))
        else:
            not_admitted.append((p, m, fails))
            # THE FAILING FIELD IS NAMED. "not admitted" without the field is a verdict a reader
            # cannot check, and the remedy is owned by whoever owns that field on that card.
            print("   NOT_ADMTD  %-46s -> stays UNKNOWN; failing: %s"
                  % (p["id"][:46], "; ".join(fails)[:60]))
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
    # DECLARATION IS THE KEY RECEIVER'S SPLIT ON THIS FACE. My first cut computed it CONJUNCTIVELY
    # over all four receivers, which returns 0/42 forever: this TO fills the KEY receiver only, so
    # a conjunctive number can never move and reports the fill as having done nothing. Both are
    # printed, so neither reading needs a re-run -- the same treatment the (a)/(b) join key gets.
    declared = [p for p in parts if (p.get("key") or {}).get("claim_status") == "declared"]
    unknown = [p for p in parts if (p.get("key") or {}).get("claim_status") != "declared"]
    conj = [p for p in parts
            if all(isinstance(p.get(r), dict) and p[r].get("claim_status") == "declared"
                   for r in RECEIVERS if isinstance(p.get(r), dict))]

    # THE THREE PERMANENTLY UNKNOWN BY CONSTRUCTION, named from the PRD, never derived by a
    # predicate of mine: L2/L3/L4, this arc's own unbuilt destinations. "They are not debt and any
    # future count treating them as outstanding is reading the wrong thing." (PRD 10.2)
    PERMANENT_UNKNOWN = ("affinity_matrix", "identity_and_succession", "similarity_network_fusion")
    perm = [p for p in parts if p.get("id") in PERMANENT_UNKNOWN]

    print()
    print("=== AC2: EMISSION and DECLARATION against the ONE denominator %d ===" % den)
    print("   EMISSION    %d of %d  -- carries all four receivers (%s) with a coherent claim_status"
          % (len(emitted), den, ", ".join(RECEIVERS)))
    print("   DECLARATION %d declared / %d unknown of %d  -- the knowledge split, KEY receiver"
          % (len(declared), len(unknown), den))
    print("      of which admitted 1:1 %d | NOT_ADMITTED %d | ambiguous %d | name-miss %d"
          % (len(admitted), len(not_admitted), len(ambiguous), len(unjoined)))
    print("      conjunctive reading (all four receivers declared): %d of %d -- printed so the"
          % (len(conj), den))
    print("      other reading needs no re-run; it cannot move on a face that fills ONE receiver")
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
    print("   EMISSION is a SHAPE claim the manifest already satisfied; DECLARATION is a KNOWLEDGE")
    print("   claim, and THIS PASS IS WHAT MOVED IT -- key goes 0 -> %d declared by writing the" % len(declared))
    print("   admitted cards' payloads into part.key. The other three receivers did not move and")
    print("   are not claimed to have: grain and failure_mode remain unknown on 42 of 42, and")
    print("   home_space carries no claim_status at all. THE EARLIER RUN OF THIS FILE PRINTED")
    print("   'nothing in this round changed it', which was true when written and was outlived by")
    print("   the fill -- the same class as the card delta prose this arc already discharged.")
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

    # -- AC3: RE-EMIT, then validate THE RE-EMITTED MANIFEST with its denominator -----------------
    # THE PAYLOAD IS BUILT BEFORE THE FILE IS OPENED FOR WRITE. open("wb") truncates on the OPEN, so
    # a failure between open and write leaves an empty manifest where 42 parts used to be.
    post_bytes = (json.dumps(man, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    post_sha = lf_sha256(post_bytes)
    print()
    print("=== AC3: re-emission + L0 validation, against the preserved pre-fill ===")
    print("   pre-fill  sha256 (LF, preserved) : %s" % prefill_digest)
    print("   re-emitted sha256 (LF)           : %s" % post_sha)
    print("   preserved at                     : %s"
          % (os.path.basename(prefill_path) if prefill_path else "NOT PRESERVED"))
    if apply:
        with open(MANIFEST, "wb") as fh:
            fh.write(post_bytes)
        with open(MANIFEST, "rb") as fh:
            back = lf_sha256(fh.read())
        print("   WRITTEN; read-back digest match  : %s" % (back == post_sha))
        if back != post_sha:
            print("   REFUSING: the manifest on disk is not what was built.")
            return 4
    else:
        print("   DRY RUN -- manifest not written (pass --apply)")
    tracked = subprocess.run(["git", "rev-parse", "HEAD:org/tier2_senior/0.4.0_DT_ClientPlatform/"
                              "deliverables/D11_MANIFEST/graph_object_manifest.declared.json"],
                             cwd=ROOT, capture_output=True, text=True)
    print("   manifest blob at HEAD            : %s"
          % (tracked.stdout.strip()[:16] if tracked.returncode == 0 else "NOT TRACKED"))
    schema_p = os.path.join(ROOT, "org", "standards", "L0_GRAPH_SUBSTRATE_MANIFEST.schema.json")
    try:
        import jsonschema
        with open(schema_p, encoding="utf-8") as fh:
            v = jsonschema.Draft202012Validator(json.load(fh))
        errs = sorted(v.iter_errors(man), key=lambda e: list(e.path))
        print("   L0 VALIDATION of the RE-EMITTED manifest: %s over %d parts (denominator "
              "printed, never a bare PASS)"
              % ("PASS" if not errs else "FAIL (%d error(s))" % len(errs), den))
        if errs:
            print("   REFUSING: the re-emitted manifest does not validate.")
            return 5
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

    # -- MUTANT: A TAMPERED PRESERVED COPY MUST REFUSE (4.0.0_SA_CRO~X 021147Z) ------------------
    # Driven through the REAL preserve_prefill, with a post-fill active digest injected so the
    # re-run branch is the one under test. Paired with a positive control on the untampered file.
    import tempfile
    if not prefill_path:
        print("   NOT EXERCISABLE -- no preserved pre-fill path in this run; not the same as a pass")
        return 6
    with open(prefill_path, "rb") as fh:
        good = fh.read()
    tdir = tempfile.mkdtemp(prefix="prefill_mutant_")
    tampered = os.path.join(tdir, "tampered.json")
    with open(tampered, "wb") as fh:
        fh.write(good.replace(b'"parts"', b'"partz"', 1))
    fake_active = "d" * 64          # a post-fill digest: not the declared pre-fill
    print()
    print("=== MUTANT: a TAMPERED preserved pre-fill on a post-fill re-run ===")

    def _quiet(**kw):
        """Run the REAL preserve_prefill, keeping its banner out of this block. The arm's own
        reason line is pulled back out of the capture and printed, so suppressing the noise does
        not suppress the evidence."""
        buf, real = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            out = preserve_prefill(False, **kw)
        finally:
            sys.stdout = real
        reason = [ln.strip() for ln in buf.getvalue().splitlines()
                  if "prior preservation:" in ln]
        return out, (reason[0] if reason else "")

    (_d, _p, ctrl_ok), ctrl_why = _quiet(prior_path=prefill_path, active_override=fake_active)
    (_d2, _p2, mut_ok), mut_why = _quiet(prior_path=tampered, active_override=fake_active)
    print("   both arms run through the REAL preserve_prefill, post-fill active digest injected")
    print("   CONTROL  untampered preserved file -> proceeds : %-5s | %s" % (ctrl_ok, ctrl_why))
    print("   MUTANT   one byte flipped          -> proceeds : %-5s | %s" % (mut_ok, mut_why))
    print("   exit-3 path taken by the mutant: %s" % (not mut_ok))
    shutil.rmtree(tdir, ignore_errors=True)
    if ctrl_ok is not True or mut_ok is not False:
        print("   REFUSING: the preservation gate does not discriminate a tampered copy.")
        return 6
    print("   the two arms differ in ONE byte and land in DIFFERENT states, so existence is no")
    print("   longer standing in for identity on the re-run path.")

    print()
    print("=== RECONCILIATION ===")
    print("   admitted %d + not_admitted %d = joined %d  %s"
          % (len(admitted), len(not_admitted), len(joined),
             "OK" if len(admitted) + len(not_admitted) == len(joined) else "DOES NOT RECONCILE"))
    print("   declared %d + unknown %d = %d of %d  %s   (unknown = not_admitted %d + ambiguous %d"
          " + name-miss %d)"
          % (len(declared), len(unknown), len(declared) + len(unknown), den,
             "OK" if len(declared) + len(unknown) == den else "DOES NOT RECONCILE",
             len(not_admitted), len(ambiguous), len(unjoined)))
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
