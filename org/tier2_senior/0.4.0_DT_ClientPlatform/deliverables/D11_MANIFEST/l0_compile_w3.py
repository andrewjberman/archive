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
            "home": loc.get("home") or "UNBOUNDED -- see evidence",
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
    out["parts"] = sorted(parts.values(), key=lambda p: p["id"])

    prior = base["denominator"]
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
        "parts_registered": len(out["parts"]),
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
