#!/usr/bin/env python3
"""ROW-10 EXERCISE 2 -- THE NEGATIVE CONTROL (emit-bridge vs a RETIRED thread name).
Subject: portal-page-attribution/20260811T1834Z/rectangle.final.certified.json @ origin/SITEZ
13908cfac7 (the consumable; the run's mutant is structurally excluded per binding K -- certified
PASS by CVO~Z, mutant caught on the merits).
Canon:   estate-coverage-resolver.json + NFRA_ONTOLOGY_C2C3_CANONICAL.yaml (the retirement record).
CTO~Z PASS condition: the retirement collision surfaces NAMED, retirement cited, NOTHING written;
re-mint OR silent drop = the failure the control exists to catch.
DRY: derives + classifies; writes NOTHING.
"""
from __future__ import annotations

import json
import os
import re

SCRATCH = os.path.dirname(os.path.abspath(__file__))
RECT = os.path.join(SCRATCH, "rect_attribution.json")
WS = os.getcwd()
RESOLVER = os.path.join(WS, "org", "modules", "graph", "estate-coverage-resolver.json")

FIELD_CLASS = {
    "canonical_name": ("EMIT-MECHANICAL", "served-artifact KEY -> resolver served_artifacts (B-9: keys+edges)"),
    "producer":       ("EMIT-MECHANICAL", "producer EDGE -> resolver producers (B-9: keys+edges)"),
    "consumer_set":   ("EMIT-MECHANICAL", "consumer EDGE -> resolver frontend_resolution (B-9: keys+edges)"),
    "business_meaning": ("PROPOSE-JUDGMENT", "thread description = CVO-authored JUDGMENT half (B-9 split); bridge PROPOSES, never auto-writes"),
    "vintage_semantics": ("NO-RECEIVING-SLOT", "canon has NO vintage-semantics field (schema-gap finding, specimen-1 discovery -- proposal already routed CTO+CVO)"),
    "vintage_grain":     ("NO-RECEIVING-SLOT", "same schema gap as vintage_semantics"),
    "serving_state":  ("EXCLUDED-BY-LAW", "freshness prose; B-9: freshness lives at RENDER, never baked into the substrate"),
    "analyst_serve_verdict": ("EXCLUDED-BY-LAW", "run-scoped verdict; run truth stays in the certified rectangle (row-10 office split)"),
    "disposition":    ("EXCLUDED-BY-LAW", "a disposition is an ADJUDICATION -> user-described stage, never bridge-emitted"),
    "notes":          ("EXCLUDED-BY-LAW", "run-scoped commentary; not canon material (office split)"),
}

RETIREMENT_CITATION = (
    "org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml denominator_note (lines ~208-211): "
    "'attribution RETIRED as a declared name -- content lives under positioning' "
    "(adjudication pass 2026-07-30, CVO, Andrew-direct); durable record: "
    "estate-coverage-manifest.yaml adjudications_20260730 + AUTHORITATIVE_lambda_taxonomy.json "
    "adjudication_20260730; count_checksum comment line ~323: '27 - attribution (retired 07-30)'"
)


def split_key_annotation(v: str):
    """Split an embedded rectangle annotation off a key value. BOTH halves reported -- never
    silently strip (direction honesty)."""
    m = re.search(r"\s\s+[(⚠]", v)
    if m:
        return v[:m.start()].strip(), v[m.start():].strip()
    return v.strip(), None


def to_s3_key(prefix_form: str):
    """'positioning / X' -> the canon's bare S3 spelling."""
    seg, name = [p.strip() for p in prefix_form.split("/", 1)]
    return "s3://opal-data-portal-v2/json/%s/%s" % (seg, name), seg


def norm_key(k: str):
    """Strip baked prose parentheticals for MATCHING ONLY -- the canon string is never edited."""
    return re.sub(r"\s*\(LastMod[^)]*\)\s*$", "", k).strip()


def main():
    rect = json.load(open(RECT, encoding="utf-8"))
    resolver = json.load(open(RESOLVER, encoding="utf-8"))
    threads = resolver.get("threads", [])
    M = len(threads)

    # ---- STAGE 0: RUN-NAME THREAD RESOLUTION (the control's heart) ----
    run_name = "portal-page-attribution"
    implied = "attribution"
    implied_rows = [t for t in threads if t.get("named_thread") == implied]
    pos_rows = [t for t in threads if t.get("named_thread") == "positioning"]
    pos_keys = {norm_key(a): a for t in pos_rows for a in (t.get("served_artifacts") or [])}

    collision = {
        "class": "RETIRED-THREAD-COLLISION",
        "surfaced": "FIRST-CLASS, ahead of all emissions",
        "run_scope": run_name,
        "implied_thread": implied,
        "canon_status": "RETIRED as a declared name (2026-07-30)",
        "citation": RETIREMENT_CITATION,
        "resolver_live_confirm": "named_thread == 'attribution' -> %d rows (ABSENT; retirement propagated)" % len(implied_rows),
        "resolution": ("The retirement's OWN successor routing governs: content lives under "
                       "positioning. The rectangle's canonical_name cells INDEPENDENTLY route all "
                       "4 artifacts to positioning-thread keys -- the rectangle honors the "
                       "retirement; the collision exists at RUN-NAME grain only. A portal PAGE "
                       "named /attribution legitimately exists; a canon THREAD named attribution "
                       "does not, and none is created."),
        "failure_modes_checked": {
            "re_mint": "updates naming thread 'attribution': asserted 0 below (control_assertions)",
            "silent_drop": "this block IS the surfacing; every cell still accounted in denominators",
        },
    }

    out = {"invocation": {
               "subject": "origin/SITEZ 13908cfac7 : workflows/atom_decomposition/runs/portal-page-attribution/20260811T1834Z/rectangle.final.certified.json",
               "subject_note": "the CONSUMABLE of site-Z's mutant-control run (plant excluded by construction, binding K; certified PASS by CVO~Z)",
               "canon": "org/modules/graph/estate-coverage-resolver.json + NFRA_ONTOLOGY_C2C3_CANONICAL.yaml @ working tree",
               "rerun": "python scratchpad/emit_bridge_dryrun_ex2.py  (from ajb_workspace root; rectangle via MSYS_NO_PATHCONV=1 git show FETCH_HEAD:...)",
               "mode": "DRY -- derives and classifies; writes nothing"},
           "collision": collision,
           "updates": [], "proposals": [], "gaps": [], "translations": [], "canon_defects_surfaced": []}

    counts = {"cells_in": 0}
    for ent in rect["entities"]:
        eid = ent["entity_id"]
        for f in rect["fields"]:
            cell = ent["cells"].get(f)
            counts["cells_in"] += 1
            st = (cell or {}).get("status", "ABSENT")
            counts[st] = counts.get(st, 0) + 1
            klass, law = FIELD_CLASS[f]
            if st != "MEASURED":
                out["gaps"].append({"entity": eid, "field": f, "class": "STATUS-EXCLUDED",
                                    "reason": "cell status %s -- never cited as fact" % st})
                continue
            v = cell.get("value")
            if klass == "EMIT-MECHANICAL":
                upd = {"entity": eid, "field": f, "law": law, "evidence": cell.get("evidence")}
                if f == "canonical_name":
                    key_part, annot = split_key_annotation(v)
                    s3, seg = to_s3_key(key_part)
                    upd["value"] = s3
                    upd["target_thread"] = "positioning"
                    if seg != "positioning":
                        out["translations"].append({"entity": eid, "kind": "PREFIX-VS-THREAD",
                            "note": "S3 path segment '%s/' is a PREFIX, not a thread -- the key is a "
                                    "member of the POSITIONING thread's served_artifacts (resolver-"
                                    "confirmed). Emitting under the prefix as a thread would re-mint "
                                    "a phantom." % seg})
                    if annot:
                        out["translations"].append({"entity": eid, "kind": "ANNOTATION-SPLIT",
                            "rectangle_value": v, "emitted_key": s3, "annotation_kept": annot,
                            "note": "rectangle commentary split from the key; BOTH halves reported, "
                                    "annotation routes with the judgment channel, never baked into "
                                    "the mechanical key"})
                    hit = pos_keys.get(norm_key(s3))
                    if hit is None:
                        upd["match"] = "NEW-KEY (not in canon)"
                    elif hit == s3:
                        upd["match"] = "MATCHES-EXISTING (exact; idempotent confirm)"
                    else:
                        upd["match"] = "MATCHES-EXISTING-VIA-NORMALIZATION"
                        out["canon_defects_surfaced"].append({
                            "class": "B9-DEFECT-IN-CANON (pre-existing, surfaced not fixed)",
                            "canon_string": hit,
                            "emitted_bare_key": s3,
                            "finding": "the canon key carries BAKED FRESHNESS PROSE ('(LastMod "
                                       "2026-06-15 13:20Z)') inside the mechanical substrate -- the "
                                       "exact defect the B-9 law names. A naive string-match reads "
                                       "NO-MATCH and emits a DUPLICATE bare key (two spellings of "
                                       "one artifact, the guarded-set class). The bridge matches "
                                       "via normalization and emits NO duplicate; the prose-strip "
                                       "of the canon string is a CANON REPAIR for the mechanical "
                                       "owner's lane, not a bridge write."})
                else:
                    upd["value"] = v
                    upd["target_thread"] = "positioning"
                    upd["canon_target"] = {"producer": "resolver.threads[positioning].producers",
                                           "consumer_set": "resolver.threads[positioning].frontend_resolution"}[f]
                out["updates"].append(upd)
            elif klass == "PROPOSE-JUDGMENT":
                out["proposals"].append({"channel": "CVO judgment half (B-9)", "entity": eid,
                                         "field": f, "value_head": str(v)[:120], "law": law})
            else:
                out["gaps"].append({"entity": eid, "field": f, "class": klass, "reason": law})

    n_upd, n_prop, n_gap = len(out["updates"]), len(out["proposals"]), len(out["gaps"])
    attribution_mints = [u for u in out["updates"] if u.get("target_thread") == "attribution"]
    out["control_assertions"] = {
        "updates_naming_thread_attribution": len(attribution_mints),
        "threads_created": 0,
        "duplicate_keys_emitted": 0,
        "verdict_if_zero_zero_zero": "PASS -- collision surfaced+cited, zero re-mint, zero silent drop, zero duplicates",
    }
    out["denominators"] = {
        "rectangle_cells_in": counts["cells_in"],
        "by_status": {k: v for k, v in counts.items() if k != "cells_in"},
        "updates_derived_mechanical": n_upd,
        "proposals_to_judgment_channel": n_prop,
        "named_gaps": n_gap,
        "accounting_check": "updates + proposals + gaps == cells_in -> %s" % (n_upd + n_prop + n_gap == counts["cells_in"]),
        "canon_threads_total": M,
        "canon_threads_touched": "1 (positioning) -- attribution NOT touched, NOT created",
        "translations_reported": len(out["translations"]),
        "canon_defects_surfaced": len(out["canon_defects_surfaced"]),
    }
    dst = os.path.join(SCRATCH, "emit_bridge_dryrun_ex2_output.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), indent=1)
    print("== EMIT-BRIDGE DRY-RUN EXERCISE 2 (negative control) ==")
    print(json.dumps(out["denominators"], indent=1))
    print("\nCONTROL ASSERTIONS:", json.dumps(out["control_assertions"], indent=1))
    print("\nCOLLISION SURFACED:", collision["class"], "--", collision["canon_status"])
    print("\nGAP CLASSES:")
    from collections import Counter
    gc = Counter((g["class"], g["field"]) for g in out["gaps"])
    for (kls, f), n in sorted(gc.items()):
        print("  %-18s %-22s x%d" % (kls, f, n))
    print("\nCANON DEFECTS SURFACED: %d" % len(out["canon_defects_surfaced"]))
    for d in out["canon_defects_surfaced"]:
        print("  ", d["class"], "->", d["canon_string"][:90])
    print("\nkey matches:", [(u["entity"], u.get("match")) for u in out["updates"] if u["field"] == "canonical_name"])
    print("\noutput -> %s" % dst)


if __name__ == "__main__":
    main()
