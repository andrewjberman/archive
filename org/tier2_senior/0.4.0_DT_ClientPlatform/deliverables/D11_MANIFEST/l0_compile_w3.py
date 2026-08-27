#!/usr/bin/env python3
"""W3-m-6 -- THE COMPILE STEP. Fold wave-3 substrate cards into the L0 graph substrate manifest.

⛔ EXTEND, NOT BUILD. The oracle as CUT said "populated instances estate-wide: ZERO"; that premise
was 0.0.0_AB_MSTR's, WITHDRAWN at 06:29Z, and the cell was corrected to EXTEND @7d03d9e788. A
conformant 39-part instance already exists. Building from zero would have re-derived 39 measured
parts and thrown away their denominator method.

⛔ AND THIS SCRIPT IS ITSELF THE POINT. 0.0.0_AB_MSTR's corrected finding was not that the manifest
was missing -- it was that the manifest is a HAND-COMPILED artifact with a vintage, NO GENERATOR and
no step that advances it, so at wave-3 close it would not be ABSENT, it would be STALE while reading
COMPLETE. Every validator passes on a stale conformant manifest. A generator is the remedy; this is it.

WHAT IT DOES NOT DO, STATED SO THE LIMIT IS NOT DISCOVERED LATER:
  - It does NOT re-derive the original 39 parts. They are carried forward VERBATIM from the phase-A
    instance, whose denominator records an estate sweep this script does not repeat. Those 39 remain
    hand-compiled; what is now generated is the WAVE-3 EXTENSION and the recompilation itself.
  - It does NOT invent the card->part join. That join is DECLARED in w3_card_part_map.json, because
    9 of 13 cards carry prose in artifact.location.home and cannot be joined mechanically. See that
    file's _why_declared_and_not_derived.
  - It does NOT blend multi-writer parts. graph_nodes has THREE measured writers and L0 `generation`
    holds ONE. On disagreement the existing value STANDS and the disagreement is written into
    evidence. A compiler that picked would look tidier and would be lying.
"""
from __future__ import annotations
import glob
import json
import os
import re
import subprocess
from collections import Counter, defaultdict

from jsonschema import Draft202012Validator

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST")
# ⛔ SEPARATE INPUT FROM OUTPUT. The first version of this script read AND wrote
# graph_object_manifest.json, which made it NON-RE-RUNNABLE: a second run re-appended every
# declared_opinion and tripped the add-target assert. A generator whose output is its own input
# corrupts or aborts on the second run -- and "it runs when cards land" REQUIRES a second run.
# BASE39 is the immutable phase-A instance; OUT is derived and fully rebuilt every time.
BASE39 = os.path.join(HERE, "graph_object_manifest.base39.json")
BASE = os.path.join(HERE, "graph_object_manifest.json")
MAP = os.path.join(HERE, "w3_card_part_map.json")
SCHEMA = os.path.join(WS, "org/standards/L0_GRAPH_SUBSTRATE_MANIFEST.schema.json")
CARD_GLOB = os.path.join(WS, "org/**/D11_CARDS_W3/*.json")

ME = "0.4.0_DT_ClientPlatform~X"
PIN = "e48a7466ba"
COMPILED_UTC = "2026-08-27T07:10:00Z"   # one clock read, per-run, stated
ORDER = {"measured": 3, "held": 2, "inferred": 1, "absent": 0}


def load_cards() -> dict:
    out = {}
    for f in sorted(glob.glob(CARD_GLOB, recursive=True)):
        c = json.load(open(f, encoding="utf-8"))
        if c.get("schema_version") != 2:      # generators and non-cards live here too
            continue
        out[c["subject"]["id"]] = c
    return out


def classify_home_space(home: str):
    """4.0.0_SA_CRO~A's rules, FAIL CLOSED. Returns None when unclassifiable.

    ⛔ NEVER GUESSES iceberg_table. An Iceberg table has no unambiguous surface form here -- the
    same table is addressed as a tuple by pyiceberg and as a dotted name by Trino
    (cse_schema.py:595), which is the very split `home_space` exists to record. Guessing it would
    mint the defect the field was added to prevent.
    """
    h = str(home or "")
    if h == "NONE":
        return "none"
    if h.startswith("s3://"):
        return "s3_uri"
    if (" " not in h) and ("/" in h) and not h.startswith("/"):
        return "repo_path"
    return None


def _localize_home(card_home, card_subject):
    """Prefer the card's home; fall back to the map's exact subject path when it is prose."""
    if classify_home_space(card_home) is not None:
        return card_home
    return str(card_subject).split(" :: ")[0].split("#")[0].strip()


def card_generation_bits(c: dict) -> dict:
    """The four L0 `generation` fields this card actually measures."""
    meth = c["process"]["methodology"]
    cad = c["process"]["cadence"]
    return {
        "materializer_standing": meth.get("materializer_standing"),
        "declared_opinions": meth.get("declared_opinions") or [],
        # ⛔ A MEASURED NONE-FOUND MUST NOT DEGRADE INTO AN UNKNOWN NULL. In a card,
        # actual_trigger=None with cadence.basis=measured means "measured, nothing fires it".
        # In L0, trigger=null means "not known". Passing the None straight through SILENTLY
        # DROPS THE CLAIM -- a value must carry its claim into the field a consumer reads.
        "cadence": cad.get("declared_rhythm") or (
            "NONE DECLARED (measured)" if cad.get("basis") == "measured" else None),
        "trigger": cad.get("actual_trigger") or (
            "NONE-FOUND (measured)" if cad.get("basis") == "measured" else None),
        "basis": min([meth.get("basis", "absent"), cad.get("basis", "absent")],
                     key=lambda v: ORDER[v]),
    }


def main() -> None:
    base = json.load(open(BASE39, encoding="utf-8"))
    mapping = json.load(open(MAP, encoding="utf-8"))
    cards = load_cards()
    parts = {p["id"]: p for p in base["parts"]}
    base_count = len(parts)

    rows = mapping["rows"]
    # ---- PARTITION CHECK FIRST: a partition whose parts do not sum is a residual bucket.
    acts = Counter(r["action"] for r in rows)
    assert len(rows) == len(cards), (
        "map rows %d != cards on disk %d -- the map and the population disagree" % (len(rows), len(cards)))
    missing = sorted(set(cards) - {r["card_subject"] for r in rows})
    assert not missing, "cards with NO map row (would be silently dropped): %s" % missing

    # ---- ENRICH -------------------------------------------------------------------
    contrib: dict[str, list] = defaultdict(list)
    for r in rows:
        if r["action"] != "enrich":
            continue
        c = cards[r["card_subject"]]
        for pid in r["part_ids"]:
            assert pid in parts, "enrich target %r absent from base manifest" % pid
            contrib[pid].append((r["card_subject"], card_generation_bits(c)))

    enriched = []
    for pid, contribs in sorted(contrib.items()):
        p = parts[pid]
        gen = p["generation"]
        standings = {b["materializer_standing"] for _, b in contribs}
        # NO BLENDING: one contributor -> take it; several that agree -> take it;
        # several that disagree -> the existing value STANDS and the split is recorded.
        if len(standings) == 1:
            gen["materializer_standing"] = standings.pop()
            standing_note = ""
        else:
            standing_note = (" ⛔ WRITERS DISAGREE ON STANDING (%s); the pre-existing value %r is "
                             "RETAINED rather than picked -- L0 generation holds ONE standing and "
                             "this artifact has %d measured writers."
                             % (", ".join("%s=%s" % (s, b["materializer_standing"])
                                          for s, b in contribs),
                                gen.get("materializer_standing"), len(contribs)))

        # declared_opinions: UNION, every entry SOURCE-PREFIXED so provenance survives the merge.
        ops = list(gen.get("declared_opinions") or [])
        for subj, b in contribs:
            for o in b["declared_opinions"]:
                ops.append("[%s] %s" % (subj, o))
        gen["declared_opinions"] = ops or None

        cads = {b["cadence"] for _, b in contribs if b["cadence"]}
        trigs = {b["trigger"] for _, b in contribs if b["trigger"]}
        if len(contribs) == 1:
            gen["cadence"] = next(iter(cads), None) or gen.get("cadence")
            gen["trigger"] = next(iter(trigs), None) or gen.get("trigger")
        else:
            gen["cadence"] = ("PER WRITER: " + "; ".join(
                "%s=%s" % (s, b["cadence"]) for s, b in contribs)) if cads else gen.get("cadence")
            gen["trigger"] = ("PER WRITER: " + "; ".join(
                "%s=%s" % (s, b["trigger"] or "none-found") for s, b in contribs))

        # ⛔ GRAIN: the part-level `basis` covers the part's OWN claims (that it exists, its home,
        # its vintage). A contributing card's GENERATION-row uncertainty must NOT demote it --
        # doing so turns a measured part into basis='absent', i.e. "no basis exists yet", which
        # DESTROYS a true claim. Measured instance: comp_aws_cli's cadence.basis is genuinely
        # `absent`, and the first version of this line drove graph_nodes from measured to absent.
        # L0 v1 has ONE basis for twelve fields; SUBSTRATE_CARD.v2 solved exactly this with
        # basis_by_field. Until L0 has that, the generation floor is recorded in evidence.
        gen_floor = min([b["basis"] for _, b in contribs], key=lambda v: ORDER[v])
        p["evidence"] = (p.get("evidence", "") +
                         " || W3 COMPILE @%s: generation enriched from %d wave-3 card(s) [%s]; "
                         "join DECLARED in w3_card_part_map.json, not derived (9 of 13 cards carry "
                         "prose in artifact.location.home and cannot be joined mechanically). "
                         "GENERATION-ROW BASIS FLOOR ACROSS CONTRIBUTORS: %s (the part-level basis "
                         "is deliberately NOT demoted by it -- different grain).%s"
                         % (PIN, len(contribs), ", ".join(s for s, _ in contribs),
                            gen_floor, standing_note))
        enriched.append(pid)

    # ---- ADD ----------------------------------------------------------------------
    added = []
    for r in rows:
        if r["action"] != "add":
            continue
        c = cards[r["card_subject"]]
        pid = r["part_ids"][0]
        assert pid not in parts, "add target %r already exists -- that is an ENRICH" % pid
        b = card_generation_bits(c)
        loc = c["artifact"]["location"]
        per = c["artifact"]["persistence"]
        parts[pid] = {
            "id": pid,
            "part_class": "materializer",
            # ⛔ 4.0.0_SA_CRO~A audit item 3: a card's `home` may be PROSE ("...py (436 lines)
            # @76c58923ac; writes globgrph.<surface>..."), which is not a location a consumer can
            # resolve. When it will not classify, fall back to the MAP ROW'S CARD SUBJECT, which is
            # an exact path -- and say so in evidence rather than silently substituting.
            "home": _localize_home(loc.get("home"), r["card_subject"]),
            "authority_role": per.get("authority_role", "none"),
            "temporal_claim": "current_state",
            "lineage": {
                "projection_of": [x["id"] for x in (loc.get("projection_of") or [])],
                "source_identity": None,
            },
            "generation": {
                "materializer": c["subject"]["id"],
                "materializer_digest": None,
                "materializer_standing": b["materializer_standing"] or "unknown",
                "declared_opinions": b["declared_opinions"] or None,
                "cadence": b["cadence"],
                "trigger": b["trigger"],
            },
            "population_status": "production",
            "vintage": {
                "measured_utc": c["as_of"]["carded_utc"],
                "method": "wave-3 substrate card, SUBSTRATE_CARD.v2, pinned @" + c["as_of"]["commit_ish"],
                "age_note": None,
            },
            "basis": b["basis"],
            "evidence": ("NEW PART, added by the W3 compile step @%s. %s || Card verdict: %s -- %s"
                         % (PIN, r["evidence"], c["verdict"]["standing"],
                            c["verdict"]["why"][:400])),
            "owner": c.get("carded_by", "UNOWNED"),
        }
        added.append(pid)

    unresolved = [r for r in rows if r["action"] == "unresolved"]

    # ---- the known-false attribution the compile surfaced --------------------------
    fx = parts.get("fedobs_coevolution_snap")
    if fx:
        fx["evidence"] += (" || ⛔ W3 COMPILE FLAG @%s: this part names generation.materializer = "
                           "cse_emit_frontend_coevolution.py, but wave 3 carded BOTH of that file's "
                           "write paths and NEITHER writes this table (PATH A = local JSONL, PATH B "
                           "= an S3 watermark object). 2.0.0_SA_COO~X independently falsified the "
                           "same claim in 74880. Either an uncarded third path exists or this "
                           "attribution is wrong. NOT RESOLVED -- flagged so the next reader "
                           "inherits the doubt rather than the claim." % PIN)

    # ---- reassemble ---------------------------------------------------------------
    out = dict(base)
    out["compiled_by"] = ME
    out["as_of"] = {"compiled_utc": COMPILED_UTC, "commit_ish": PIN}
    # ⛔ home_space stamped MECHANICALLY, AUTHORED VALUES PRESERVED, FAIL CLOSED.
    # An unclassifiable home aborts the emit rather than shipping a part whose address space is a
    # guess -- 4.0.0_SA_CRO~A audit item 2.
    _unclassifiable = []
    for _p in parts.values():
        if "home_space" in _p:          # authored upstream (base39's C3 triplet) -- never overwritten
            continue
        _hs = classify_home_space(_p.get("home"))
        if _hs is None:
            _unclassifiable.append((_p["id"], str(_p.get("home"))[:70]))
        else:
            _p["home_space"] = _hs
    if _unclassifiable:
        raise SystemExit(
            "REFUSING TO EMIT -- home_space unclassifiable, and it is NOT guessed: "
            + "; ".join("%s -> %r" % r for r in _unclassifiable))

    out["parts"] = sorted(parts.values(), key=lambda p: p["id"])

    # ⛔ SHALLOW-COPY ALIAS: `out = dict(base)` means out["denominator"] IS
    # base["denominator"]. Anything appended to it before this line MUTATES the frozen phase-A
    # method that the very next statement embeds as "unchanged and NOT re-run by this compiler".
    # Snapshotted so that sentence stays true of its own content.
    prior = dict(base["denominator"])
    out["denominator"] = {
        # ⛔ NAMES BOTH POPULATIONS RATHER THAN BLENDING THEM -- the oracle's own words.
        "method": (
            "TWO POPULATIONS, NAMED SEPARATELY AND NOT BLENDED. "
            "(A) THE ORIGINAL %d PARTS -- carried forward VERBATIM from the phase-A instance "
            "compiled 2026-08-26T19:33Z @14da312322. Their method, unchanged and NOT re-run by this "
            "compiler: %s "
            "(B) THE WAVE-3 MATERIALIZER POPULATION -- %d substrate cards conforming to "
            "SUBSTRATE_CARD.v2, produced by 4 lanes under NFRA_SUBSTRATECARDING wave 3 and read off "
            "disk at %s. Folded in as %d ENRICH mappings touching %d distinct parts, %d ADD, %d "
            "UNRESOLVED-and-deliberately-unwritten. 13 = 9 + 3 + 1, and the partition sums. "
            "The card->part join is DECLARED in w3_card_part_map.json rather than derived, because "
            "9 of 13 cards carry prose in artifact.location.home; that is a contract finding routed "
            "to the schema owner, not a lane defect. "
            "⛔ WHAT COUNTS AS A PART, STATED ON THE FACE BECAUSE IT WAS NOT (3.0.0_SA_CVO~X 74911). "
            "An L0 part is an ARTIFACT A NAMED WRITER ACTUALLY WRITES, with whether the estate "
            "INTENDS it recorded in population_status -- NOT canonical-artifacts-only. That is "
            "measured from the registry rather than preferred: population_status carries 'orphaned' "
            "as a legal value and kuzu_db is registered with it, so observed-not-intended artifacts "
            "are demonstrably admissible. THE CONSEQUENCE FOR REGISTRATION: an artifact is declined "
            "only when no named writer in scope wrote it -- never merely because its writer COULD "
            "have written elsewhere, which reasons from the writer's domain about the artifact and "
            "is a grain slip. The one declined instance here (cse_emit_frontend_coevolution PATH A) "
            "is declined on the first test, not the second: its own card measures that the path "
            "writes a LOCAL dev-box file with no boto3, and that the surviving S3 object is that "
            "file AFTER A HUMAN UPLOADED IT -- a different artifact with a different writer. "
            "⛔ POPULATION B DOES NOT RE-SWEEP THE ESTATE. It spans exactly what wave 3 chose to "
            "card, and wave 3's own decomp states on its face that its subject set enumerates "
            "writers we can FIND, never every writer that EXISTS."
            % (base_count, prior["method"], len(cards), PIN,
               acts["enrich"], len(enriched), acts["add"], acts["unresolved"])),
        "population_searched": (
            "(A) %s || (B) org/**/D11_CARDS_W3/*.json across all lanes -- %d cards from %d lane "
            "directories, the complete wave-3 card population as it stood at compile time. A card "
            "landing after this run is NOT represented; re-run the compiler."
            % (prior["population_searched"], len(cards),
               len({os.path.dirname(f) for f in glob.glob(CARD_GLOB, recursive=True)}))),
        # ⛔ parts_registered REMOVED 2026-08-27 on my own ruling in 75051 (a), 1.0.0_SA_CTO~X GO
        # in 75063. A NUMBER A MACHINE CAN DERIVE MUST NOT ALSO BE TYPED: it sat beside parts[] as
        # a second copy of len(parts), and JSON Schema cannot express the equality between them, so
        # the only thing preventing drift was this generator computing it correctly. THAT IS WHY THE
        # DEFECT NEVER FIRED AND WHY IT STAYED INVISIBLE -- 1.0.0_SA_CTO~X's point, and it is right.
        # Consumers compute len(parts). SEQUENCE: this removal lands FIRST, then 1.0.0_SA_CTO~X
        # removes the property from the schema -- never an invalid state in either direction.
        # ⛔ DERIVED FROM THE UNRESOLVED ROWS, NOT TYPED BESIDE THEM. The first version hardcoded a
        # sentence about the ONE unresolved row that existed then; when 3.0.0_SA_CVO~X's 74902 attack
        # moved cse_store PATH B to unresolved, a typed list would have silently kept saying ONE.
        # That is the typed-beside-derived class this session keeps producing, so the list is
        # generated from the map and cannot disagree with it.
        "known_unsearched": list(prior.get("known_unsearched") or []) + [
            "DELIBERATELY NOT REGISTERED -- %s :: %s" % (r["card_subject"], r["evidence"])
            for r in rows if r["action"] == "unresolved"
        ] + [
            "The wave-3 card population is the writers wave 3 SELECTED, not a fresh estate sweep. "
            "Any materializer outside that selection is invisible to population B.",
            "L0 `generation` holds ONE materializer/standing/cadence/trigger; graph_nodes has THREE "
            "measured writers and graph_edges TWO. Where writers disagree the pre-existing standing "
            "is RETAINED and the disagreement recorded in evidence -- the manifest cannot currently "
            "express per-writer standing, so that dimension is UNREPRESENTED rather than resolved.",
        ],
    }

    # ---- PARTS_VS_OBJECTS, DERIVED AFTER THE DENOMINATOR OBJECT EXISTS --------------
    # ⛔ MOVED HERE from before the replacement, 4.0.0_SA_CRO~A pre-commit finding. Appending
    # to out["denominator"] before `out["denominator"] = {...}` wrote through the shallow
    # alias into base's FROZEN method, which the new object then embedded as population A's
    # "unchanged" method -- so the 42-part split was emitted MIS-ATTRIBUTED to the 39-part
    # population rather than discarded. Order is the whole fix.
    # ⛔ 4.0.0_SA_CRO~A's instruction: prefer DERIVING this after the final population exists over
    # freezing another count in base39 prose. base39 is an INPUT; a count frozen in an input is
    # stale the moment the population changes, and it had (39 -> 42).
    # KEYED ON home_space == "none", the DECLARED ENUM -- not on `basis` (which was carrying two
    # meanings) and not on a prose prefix (which was the same defect one field over,
    # 1.0.0_SA_CTO~X ruling 75231).
    NON_ENUMERABLE_FAMILIES = {"kuzu_nessie_db.rebuild.tmp.SET"}
    ENUMERABLE_SETS = ("_build_manifest.json.SET", ".comp-graph/platinum.CACHE_SET")

    # ---- member_set EMITTED FIRST, MEMBERS DERIVED FROM EACH PART'S OWN HOME ---------
    # 4.0.0_SA_CRO~A rework items 1 + 3 against 5e210c95fd. The prior cut hand-typed
    # ["kuzu_nessie_db", "kuzu_db", "kuzu_stitch_db"] as members: those are the brace
    # ALTERNATIVES, not artifact identities -- and each one is the id of a DIFFERENT PART
    # in this same manifest, so the member array named three other parts. The home is the
    # authoritative identity and the expansion is total, so DERIVE, never retype.
    def _expand_braces(text):
        """FULL RECURSIVE expansion. A single-group parser under-counted a nested pattern
        at three seats; this handles nesting and the empty alternative in `{,.wal}`."""
        i = text.find("{")
        if i < 0:
            return [text]
        depth = 0
        for j in range(i, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
        else:
            raise SystemExit("REFUSING TO EMIT -- unbalanced brace in a home: %r" % text)
        head, body, tail = text[:i], text[i + 1:j], text[j + 1:]
        alts, d, cur = [], 0, ""
        for ch in body:
            if ch == "{":
                d += 1
            elif ch == "}":
                d -= 1
            if ch == "," and d == 0:
                alts.append(cur)
                cur = ""
            else:
                cur += ch
        alts.append(cur)
        expanded = []
        for a in alts:
            expanded.extend(_expand_braces(head + a + tail))
        return expanded

    _by_id = {p["id"]: p for p in out["parts"]}
    for _pid in ENUMERABLE_SETS:
        _p = _by_id[_pid]           # KeyError is the loud failure; a silent skip is not
        _mem = _expand_braces(_p["home"])
        assert not any("{" in m or "}" in m for m in _mem), (
            "brace survived expansion for %s: %s" % (_pid, _mem))
        assert len(_mem) == len(set(_mem)), "duplicate member for %s: %s" % (_pid, _mem)
        assert len(_mem) >= 2, (
            "a %d-member set is the ABSENT case wearing the PRESENT case's shape (%s)"
            % (len(_mem), _pid))
        assert _p["basis"] != "absent", "member basis cannot be `absent` (%s)" % _pid
        _p["member_set"] = {
            "enumerable": True,
            "members": _mem,
            "basis": _p["basis"],
            "evidence": (
                "MEMBER IDENTITIES DERIVED, NOT TYPED: full recursive brace expansion of this "
                "part's own `home`, which is the authoritative artifact identity. The part's own "
                "vintage.method records a stat on each member. NOTHING IS DERIVED FROM THE PART "
                "ID -- a brace pattern is a claim about a set, and the id is not the pattern."),
            "owner": _p["owner"],
        }

    # ---- the RUNTIME FAMILY, under 1.0.0_SA_CTO~X's rework12 ruling @8e95441c36 -------
    # 4.0.0_SA_CRO~A held this shape (rework item 2) pending a representation that preserves
    # BOTH sibling forms and the source provenance. That ruling landed: `variant_suffixes` is
    # REQUIRED under enumerable=false ([] is the claim "no companions"), the placeholder names
    # name the VARYING QUANTITY (<monotonic_ns>, never <mono>), and the literal segments
    # INCLUDE THE PATH -- the template is the family's HOME shape. Emitting under it now.
    _nef = _by_id["kuzu_nessie_db.rebuild.tmp.SET"]
    _stem = _nef["home"].split("{", 1)[0]
    _groups = re.findall(r"\{([^{}]*)\}", _nef["home"])
    assert len(_groups) == 2, (
        "the runtime family's home is not <stem>{instances}{siblings}: %r" % _nef["home"])
    # DERIVED, not typed: the companion axis is the LAST brace group's non-empty alternatives.
    # ⛔ rework14 @b238f34351 -- an OBJECT KEYED BY SUFFIX, never an array: a JSON array's order
    # is DATA, so [".lock",".wal"] and [".wal",".lock"] are byte-, schema- and digest-distinct
    # spellings of one claim, and an object makes that ambiguity INEXPRESSIBLE rather than
    # forbidden by instruction. The KEY SET is derived here; the per-suffix STATEMENTS are
    # knowledge and cannot be sliced out of a path, so they are authored against source and a
    # derived key with no authored statement REFUSES TO EMIT.
    _COMPANION_MEANING = {
        ".wal": ("write-ahead log; kuzu writes a <db>.wal beside each single-file DB "
                 "(_canonical.py:179-182) and a failed rebuild orphans it"),
    }
    _companion_keys = sorted({a for a in _groups[-1].split(",") if a})
    assert all(re.fullmatch(r"\.[A-Za-z0-9]+", c) for c in _companion_keys), (
        "a derived companion suffix is not a real filename suffix: %s" % _companion_keys)
    _unstated = [c for c in _companion_keys if not _COMPANION_MEANING.get(c)]
    assert not _unstated, (
        "REFUSING TO EMIT -- a companion suffix is in the home with no authored statement of "
        "what it holds; a bare suffix is the loud-but-unresolvable class: %s" % _unstated)
    _companions = {c: _COMPANION_MEANING[c] for c in _companion_keys}
    _nef["member_set"] = {
        "enumerable": False,
        "pattern": _stem + "<pid>.<monotonic_ns>.<uniq>",
        "pattern_source_home": "infra/aws/globgrph/_canonical.py",
        "pattern_source_line": 288,
        "variant_suffixes": _companions,
        "basis": _nef["basis"],
        "evidence": (
            "INSTANCE AXIS, UNBOUNDED: _unique_tmp at _canonical.py:288 builds the name from "
            "os.getpid() + time.monotonic_ns() + next(_UNIQ) (an itertools.count at :37), and "
            "_gc_stale_tmps (:291, called from the rebuild path) reaps them, so TOTAL CARDINALITY "
            "IS UNDEFINED and no member list can be true of this family. The literal prefix is the "
            "part's own home stem, derived here rather than retyped. COMPANION AXIS, FINITE: "
            "derived from the home's own sibling brace group; kuzu writes a <db>.wal beside each "
            "single-file DB (:179-182). PER-INSTANCE cardinality is 1 + the number of KEYS, "
            "DERIVED. OBSERVATION, ROUTED NOT DECIDED: _rm_kuzu at :188 clears FOUR side-artifact "
            "suffixes (.wal .lock .shadow .tmp), so the source's possible-companion set is wider "
            "than the measured one recorded here; this array is the MEASURED companion set as of "
            "the part's 2026-08-25 stat, not a proof of closure."),
        "owner": _nef["owner"],
    }

    _absent = [p for p in out["parts"] if p.get("home_space") == "none"]
    _present = [p for p in out["parts"] if p.get("home_space") != "none"]
    # THE PARTITION IS NOW DERIVED FROM THE EMITTED member_set, not from a parallel table.
    _enum = [p for p in _present if p.get("member_set", {}).get("enumerable") is True]
    _nonenum = [p for p in _present if p.get("member_set", {}).get("enumerable") is False]
    _single = [p for p in _present if "member_set" not in p]
    assert len(_single) + len(_enum) + len(_nonenum) == len(_present), "partition does not sum"
    assert {p["id"] for p in _enum} == set(ENUMERABLE_SETS), (
        "the emitted enumerable sets are not the declared ones: %s" % sorted(p["id"] for p in _enum))
    assert {p["id"] for p in _nonenum} == NON_ENUMERABLE_FAMILIES, (
        "the emitted non-enumerable families are not the declared ones: %s"
        % sorted(p["id"] for p in _nonenum))
    # THE ONLY OBJECT FIGURE, DERIVED FROM THE EMITTED ARRAYS THEMSELVES.
    _enum_objects = sum(len(p["member_set"]["members"]) for p in _enum)

    # CONTROL: the W3 compile must PRESERVE the C3 triplet it inherits from base39.
    _EXPECTED_UNBUILT = {"affinity_matrix", "similarity_network_fusion", "identity_and_succession"}
    assert {p["id"] for p in _absent} == _EXPECTED_UNBUILT, (
        "the unbuilt set is not the C3 triplet after compile: %s"
        % sorted(p["id"] for p in _absent))
    assert all(p["basis"] == "held" and p["home"] == "NONE" for p in _absent), (
        "the compile did not preserve the C3 triplet (basis=held, home=NONE, home_space=none)")

    out["denominator"]["method"] += (
        " PARTS_VS_OBJECTS, DERIVED AT COMPILE over the FINAL population, NO SINGLE OBJECT TOTAL: "
        "%d parts = %d present + %d recording an ABSENCE (the unbuilt C3 stages, keyed on "
        "home_space=='none' -- their `basis` is `held` on a named authority and their UNBUILT-NESS "
        "is a different question from their epistemic basis). The %d present parts partition as %d "
        "singleton + %d ENUMERABLE set rows covering %d named members + %d NON-ENUMERABLE family "
        "whose members are runtime-named and whose CARDINALITY IS UNDEFINED. ⛔ NO TOTAL "
        "DISTINCT-OBJECT COUNT EXISTS FOR THIS POPULATION and none is printed -- a total spanning a "
        "family of undefined cardinality would be a number the estate does not have. The enumerable "
        "subtotal is %d objects across %d set rows and is the only object figure quotable here."
        % (len(out["parts"]), len(_present), len(_absent), len(_present), len(_single),
           len(_enum), _enum_objects, len(_nonenum),
           _enum_objects, len(_enum)))


    # ⛔ FINAL-STATE CONTROL, on the EMITTED object rather than on the logic that built it.
    # My static controls tested the computation and could not have seen the mis-attribution,
    # because the computation was correct and its DESTINATION was wrong.
    _final = out["denominator"]["method"]
    assert "PARTS_VS_OBJECTS, DERIVED AT COMPILE" in _final, (
        "the derived split is not in the EMITTED method")
    assert ("%d parts = %d present" % (len(out["parts"]), len(_present))) in _final, (
        "the emitted split does not carry the FINAL population counts")
    for _legacy in ("14 member objects", "47 DISTINCT OBJECTS", "6-member SET row",
                    "3 are SET rows"):
        assert _legacy not in _final, "LEGACY claim survives in the emitted method: %r" % _legacy

    # ---- RECEIVERS: 42/42 CARRIED, 0/42 DECLARED ----------------------------------
    # 4.0.0_SA_CRO~A 75304 + rework items 4 and 5. 0.0.0_AB_MSTR's bar is TWO NUMBERS:
    # (1) EMISSION -- 42 of 42 parts CARRY all four receivers with a coherent claim_status;
    # (2) DECLARATION -- the declared/unknown split printed beside it, never alone.
    # NOTHING IS SYNTHESISED. The compiler admits exactly org/**/D11_CARDS_W3/*.json (13 cards)
    # and exact card subject.id -> part.id among them is ZERO, measured. No declared payload is
    # taken from w3_card_part_map (an ARTIFACT-LOCATION join, right source for where a writer's
    # output lives, WRONG source for which part a card's trust block qualifies) or from cards the
    # compiler does not admit.
    #
    # ⛔ AND "0 DECLARED" IS ONE NUMBER OVER THREE DIFFERENT FACTS. The evidence is per field
    # because the remedies do not move together (Rule 24 iv). ⛔ EACH RECEIVER IS BLOCKED AT
    # SEVERAL INDEPENDENT LAYERS AND THE LAYER SET IS THE POINT -- an earlier version of this
    # comment said failure_mode was "one glob line from declared" and that is WITHDRAWN
    # (1.0.0_SA_CTO~X 75362, verified in this file: ZERO code paths assign a declared receiver):
    #   failure_mode  SOURCE PAYLOAD COMPLETE (23/23 W4 exact matches) + REGISTRY admission
    #                 blocked + schema-bound TRANSFORM absent + no COMPILER path that declares
    #   key           the three above, and SOURCE ABSENT TOO -- SUBSTRATE_CARD.v2 has no
    #                 key_expression field, so there is nothing to admit or transform
    #   grain         the three above, and SOURCE ABSENT TOO -- no authored grain projection
    #                 exists in any card, admitted or not
    # ⛔ A GLOB CHANGE IS NOT SUFFICIENT FOR ANY OF THEM, and 4.0.0_SA_CRO~A has RULED it is not
    # even permitted: W3-only is INTENTIONAL-BUT-TEMPORAL, this file is a fail-closed 13-card W3
    # extension compiler rather than a durable receiver-source boundary, and the successor is an
    # authored card_population_registry.v1.json -- globs become candidate-discovery diagnostics
    # that never expand authority. DO NOT WIDEN CARD_GLOB.
    _R_SCOPE = (
        "The compiler admits org/**/D11_CARDS_W3/*.json (13 cards); exact card subject.id -> "
        "part.id among them = 0, measured by this lane. ")
    _R_UNOWNED = ("UNOWNED -- needs an admitted-card registry and a schema-bound "
                  "card-to-L0 transform; neither exists at this commit")
    _R_EV = {
        "grain": (
            _R_SCOPE
            + "A SOURCE FACT, INDEPENDENT OF THE GLOB: no authored grain projection exists to "
            "admit. 1.0.0_SA_CTO~X measured the 23 exact-match cards outside the admitted glob "
            "and found an authored grain projection in 0 of 23 -- no key containing 'grain' "
            "anywhere in them (75350, their instrument, cited not re-derived). Widening the "
            "admitted population would not move this receiver."),
        "key": (
            _R_SCOPE
            + "A KNOWLEDGE FACT, INDEPENDENT OF THE GLOB: L0 requires key_expression and "
            "SUBSTRATE_CARD.v2's trust.key HAS NO SUCH FIELD. It carries seven of the eight "
            "L0-required fields -- identity_space, key_is_stable, crosses_spaces, "
            "declared_mapping, basis, evidence, owner -- i.e. every PROPERTY of the key and "
            "never the key itself (1.0.0_SA_CTO~X 75342). No card population of any size can "
            "supply a declared key, so carding harder cannot move this receiver."),
        "failure_mode": (
            _R_SCOPE
            + "BLOCKED AT FOUR INDEPENDENT LAYERS -- SOURCE PAYLOAD COMPLETE, but REGISTRY "
            "admission blocked, schema-bound TRANSFORM absent, and NO COMPILER PATH DECLARES. "
            "The PAYLOADS EXIST: "
            "1.0.0_SA_CTO~X measured trust.failure_mode complete in 23 of 23 exact-match cards "
            "outside the admitted glob (75350). ⛔ BUT WIDENING CARD_GLOB WOULD DECLARE "
            "NOTHING: it makes 23 payloads REACHABLE and this compiler has NO CODE PATH THAT "
            "ASSIGNS A DECLARED RECEIVER AT ALL (75362, corrected at source; re-verified in this "
            "file -- 0 assignments of claim_status `declared`, positive control 3 for `unknown`). "
            "That distinction is the whole point: DATA EXISTING is a weaker claim than a value "
            "being reachable, and this is the only receiver where even the weaker one holds. "
            "Doctrine principle 13 still binds the 0 -- a coverage fraction is evidence only if "
            "its denominator comes from outside the instrument's own configuration, and "
            "CARD_GLOB is this instrument's configuration with a wave number baked into it. "
            "⛔ AND THE GLOB ROUTE IS CLOSED BY RULING, NOT MERELY INSUFFICIENT: 4.0.0_SA_CRO~A "
            "ruled W3-only INTENTIONAL-BUT-TEMPORAL and forbade widening CARD_GLOB; the "
            "successor is an authored card_population_registry.v1.json whose receiver_sources "
            "role starts EMPTY until each receiver source and its governed transform exist."),
    }
    _R_OWN = {
        "grain": _R_UNOWNED,
        "key": ("UNOWNED -- needs a key_expression field in SUBSTRATE_CARD.v2 "
                "(4.0.0_SA_CRO~A's contract) BEFORE any registry or transform question"),
        "failure_mode": ("UNOWNED -- and NO SINGLE OWNER CAN CLOSE IT. Three independent "
                         "changes are required and a glob change is NOT among them: an authored "
                         "card_population_registry.v1.json receiver_sources role "
                         "(4.0.0_SA_CRO~A's ruling, which explicitly forbids widening "
                         "CARD_GLOB), a schema-bound card-to-L0 transform with a version, and a "
                         "declaring code path in this compiler, which this lane owns and which "
                         "does not exist at this commit"),
    }

    # ⛔ setdefault WOULD HAVE PRESERVED a stale declared receiver while the compiler reported
    # 0/42 declared -- a wrong value protected by the very call meant to be conservative
    # (4.0.0_SA_CRO~A rework item 4). Assert the frozen input is clean, then ASSIGN.
    _RFIELDS = ("grain", "key", "failure_mode")
    _preexisting = [(p["id"], f) for p in out["parts"] for f in _RFIELDS if f in p]
    assert not _preexisting, (
        "the input already carries a receiver object; a merge would have hidden it behind a "
        "0/42-declared report: %s" % _preexisting)

    for _p in out["parts"]:
        _p["grain"] = {
            "claim_status": "unknown", "unit": None,
            "basis": "absent", "evidence": _R_EV["grain"], "owner": _R_OWN["grain"]}
        _p["key"] = {
            "claim_status": "unknown", "identity_space": None, "key_expression": None,
            "key_is_stable": None, "crosses_spaces": None, "declared_mapping": None,
            "basis": "absent", "evidence": _R_EV["key"], "owner": _R_OWN["key"]}
        _p["failure_mode"] = {
            "claim_status": "unknown", "returns_on_failure": None,
            "distinguishable_from_true_negative": None, "silent_degrade_paths": None,
            "basis": "absent", "evidence": _R_EV["failure_mode"],
            "owner": _R_OWN["failure_mode"]}

    # ---- FINAL-STATE CONTROLS ON THE EMITTED OBJECT --------------------------------
    # Presence and declaration are SEPARATE assertions because they are the bar's two numbers.
    _missing = [(p["id"], f) for p in out["parts"]
                for f in _RFIELDS + ("home_space",) if f not in p]
    assert not _missing, "EMISSION bar fails -- receiver not carried: %s" % _missing
    _declared = {f: sum(1 for p in out["parts"] if p[f]["claim_status"] != "unknown")
                 for f in _RFIELDS}
    assert set(_declared.values()) == {0}, (
        "a declared receiver was synthesised from an unadmitted source: %s" % _declared)
    assert all(p["home_space"] in ("repo_path", "s3_uri", "iceberg_table", "none")
               for p in out["parts"]), "home_space carries a value outside the declared enum"
    # ⛔ EXACT ID EQUALITY, not len()==3: a count passes while the wrong parts carry it.
    _ms_ids = {p["id"] for p in out["parts"] if "member_set" in p}
    assert _ms_ids == set(ENUMERABLE_SETS) | NON_ENUMERABLE_FAMILIES, (
        "member_set landed on the wrong parts: %s" % sorted(_ms_ids))
    # member_set is NEVER required of the other 39: the only shape a singleton could take is a
    # one-member set, which is the defect minItems:2 closed (1.0.0_SA_CTO~X 75331).
    _singletons = [p["id"] for p in out["parts"] if "member_set" not in p]
    assert len(out["parts"]) == len(_ms_ids) + len(_singletons), (
        "the member_set partition does not sum over the emitted parts")

    # ---- validate, with the negative control ---------------------------------------
    v = Draft202012Validator(json.load(open(SCHEMA, encoding="utf-8")))
    errs = sorted(v.iter_errors(out), key=lambda e: list(e.path))
    for e in errs[:10]:
        print("L0 SCHEMA ERROR:", list(e.path)[:4], e.message[:180])
    neg = len(list(v.iter_errors({})))

    print("base parts        : %d" % base_count)
    print("cards read        : %d  (from %d lane dirs)"
          % (len(cards), len({os.path.dirname(f) for f in glob.glob(CARD_GLOB, recursive=True)})))
    print("map rows          : %d  -> enrich=%d add=%d unresolved=%d  (sums: %s)"
          % (len(rows), acts["enrich"], acts["add"], acts["unresolved"],
             acts["enrich"] + acts["add"] + acts["unresolved"] == len(rows)))
    print("parts enriched    : %d distinct  %s" % (len(enriched), enriched))
    print("parts added       : %d  %s" % (len(added), added))
    print("unresolved        : %d  %s" % (len(unresolved), [r["card_subject"] for r in unresolved]))
    print("PARTS REGISTERED  : %d   (> %d required by the oracle: %s)"
          % (len(out["parts"]), base_count, len(out["parts"]) > base_count))
    # ---- 0.0.0_AB_MSTR's BAR, BOTH HALVES, DERIVED FROM THE EMITTED OBJECT ----------
    # (1) EMISSION is a CONTRACT-SHAPE claim. (2) DECLARATION is a KNOWLEDGE claim.
    # ⛔ (2) IS PER RECEIVER AND IS NEVER SUMMED (amendment 75355): one figure moving
    # 0/42 -> 23/42 would read as one-third of the way to a target when it is one receiver
    # changing state and two staying exactly as unreachable.
    # ⛔ AND THE FATE COLUMN NAMES BLOCKING LAYERS, NOT ONE WORD (correction 75362): the
    # earlier "CONFIGURATION -- one glob line away" was WITHDRAWN because no receiver is one
    # line from declared. Widening CARD_GLOB moves the declaration count by ZERO -- there is no
    # transform to run on what it would admit. A LAYER SET is what a reader can act on: it says
    # how many independent things must change, and by whom.
    _BAR = ("home_space", "failure_mode", "key", "grain")
    _FATE = {
        "home_space":   "NONE          mechanical, classified in-compiler from the home, fail-closed",
        "failure_mode": "REGISTRY + TRANSFORM + COMPILER   payloads EXIST (23/23), nothing reads them",
        "key":          "the three above + SOURCE          no key_expression field in the contract",
        "grain":        "the three above + SOURCE          no authored projection exists anywhere",
    }
    _carry = sum(1 for p in out["parts"] if all(f in p for f in _BAR))
    print("BAR (1) EMISSION  : %d of %d parts CARRY all four receivers  -> %s"
          % (_carry, len(out["parts"]),
             "MET" if _carry == len(out["parts"]) else "*** NOT MET ***"))
    print("BAR (2) DECLARATION -- PER RECEIVER, NEVER SUMMED (0.0.0_AB_MSTR 75355 as corrected):")
    for _f in _BAR:
        if _f == "home_space":
            _n = sum(1 for p in out["parts"] if p.get(_f) is not None)
        else:
            _n = sum(1 for p in out["parts"] if p[_f].get("claim_status") != "unknown")
        print("    %-13s %2d/%d declared   blocked at: %s"
              % (_f, _n, len(out["parts"]), _FATE[_f]))
    print("    member_set is NOT ON THIS BAR: applicable to %d of %d parts; requiring it would "
          "force a one-member set on every singleton" % (len(_ms_ids), len(out["parts"])))
    print("VALIDATION ERRORS : %d" % len(errs))
    print("NEGATIVE CONTROL  : %d errors on {} -> %s"
          % (neg, "FIRES" if neg else "*** DEAD CONTROL ***"))

    if errs:
        raise SystemExit("REFUSING TO WRITE -- the recompiled manifest does not validate.")
    with open(BASE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=True)
        f.write("\n")
    print("OK: wrote %s" % os.path.relpath(BASE, WS).replace("\\", "/"))


if __name__ == "__main__":
    main()
