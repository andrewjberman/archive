#!/usr/bin/env python3
"""ROW-10 LIVE EXERCISE -- the emit-bridge DRY-RUN (certified rectangle -> derived canon updates).
Subject: portal-page-portfolios/20260811T1640Z/rectangle.final.certified.json @ origin/SITEZ 7ea4fdbd38
Canon:   estate-coverage-resolver.json (mechanical half) + judgment/user channels per the B-9 contract.
Three conditions (CTO~Z): (1) re-runnable invocation + denominators; (2) named gaps never silent
skips; (3) direction honesty -- derive FROM the rectangle, list both spellings where translated.
DRY: derives + classifies; writes NOTHING to the canon.
"""
from __future__ import annotations

import json
import os

SCRATCH = os.path.dirname(os.path.abspath(__file__))
RECT = os.path.join(SCRATCH, "rect_portfolios.json")
WS = os.getcwd()
RESOLVER = os.path.join(WS, "org", "modules", "graph", "estate-coverage-resolver.json")

# Field -> emission class, per the bridge's own laws (each reason cites its law):
FIELD_CLASS = {
    "canonical_name": ("EMIT-MECHANICAL", "served-artifact KEY -> resolver served_artifacts (B-9: keys+edges)"),
    "producer":       ("EMIT-MECHANICAL", "producer EDGE -> resolver producers (B-9: keys+edges)"),
    "consumer_set":   ("EMIT-MECHANICAL", "consumer EDGE -> resolver frontend_resolution (B-9: keys+edges)"),
    "business_meaning": ("PROPOSE-JUDGMENT", "thread description = CVO-authored JUDGMENT half (B-9 split); bridge PROPOSES to CVO, never auto-writes"),
    "vintage_semantics": ("NO-RECEIVING-SLOT", "canon has NO vintage-semantics field -- the rectangle knows a thing the canon cannot hold (schema-gap FINDING)"),
    "vintage_grain":     ("NO-RECEIVING-SLOT", "same schema gap as vintage_semantics"),
    "serving_state":  ("EXCLUDED-BY-LAW", "point-in-time liveness = freshness prose; B-9: freshness lives at RENDER, never baked into the substrate"),
    "analyst_serve_verdict": ("EXCLUDED-BY-LAW", "run-scoped verdict; run truth stays in the certified rectangle (row-10 office split)"),
    "disposition":    ("EXCLUDED-BY-LAW", "a disposition is an ADJUDICATION -> user-described stage (lifecycle sitting), never bridge-emitted"),
    "notes":          ("EXCLUDED-BY-LAW", "run-scoped commentary; not canon material (office split)"),
}

# direction-honesty: known spelling translations (rectangle form -> canon/on-disk form)
def translate_key(v: str):
    """Return (canon_spelling, translated?) -- NEVER silently normalize; both spellings reported."""
    if not isinstance(v, str):
        return v, False
    t = v
    tr = False
    if t.startswith("mdpf-platinum / "):
        t = "platinum/mdpf/" + t[len("mdpf-platinum / "):]
        tr = True
    return t, tr


def main():
    rect = json.load(open(RECT, encoding="utf-8"))
    resolver = json.load(open(RESOLVER, encoding="utf-8"))
    mp_threads = [t for t in resolver.get("threads", [])
                  if t.get("named_thread") in ("mdpf", "model-portfolios")]
    M = len(resolver.get("threads", []))

    out = {"invocation": {
               "subject": "origin/SITEZ 7ea4fdbd38 : workflows/atom_decomposition/runs/portal-page-portfolios/20260811T1640Z/rectangle.final.certified.json",
               "canon": "org/modules/graph/estate-coverage-resolver.json @ working tree (v1.9 registry era)",
               "rerun": "python scratchpad/emit_bridge_dryrun.py  (from ajb_workspace root; rectangle fetched via MSYS_NO_PATHCONV=1 git show)",
               "mode": "DRY -- derives and classifies; writes nothing"},
           "updates": [], "proposals": [], "gaps": [], "translations": []}

    counts = {"cells_in": 0, "MEASURED": 0, "NOT_MEASURABLE": 0}
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
                                    "reason": "cell status %s -- never cited as fact (cell law)" % st})
                continue
            v = cell.get("value")
            if klass == "EMIT-MECHANICAL":
                cv, tr = translate_key(v) if f == "canonical_name" else (v, False)
                upd = {"canon_target": "resolver.threads[named_thread in {mdpf, model-portfolios}].%s" %
                                       {"canonical_name": "served_artifacts", "producer": "producers",
                                        "consumer_set": "frontend_resolution"}[f],
                       "entity": eid, "field": f, "value": cv,
                       "evidence": cell.get("evidence"), "law": law}
                if tr:
                    upd["translation"] = {"rectangle_spelling": v, "canon_spelling": cv}
                    out["translations"].append({"entity": eid, "field": f,
                                                "rectangle": v, "canon": cv})
                out["updates"].append(upd)
            elif klass == "PROPOSE-JUDGMENT":
                out["proposals"].append({"channel": "CVO judgment half (B-9)", "entity": eid,
                                         "field": f, "value_head": str(v)[:120], "law": law})
            else:
                out["gaps"].append({"entity": eid, "field": f, "class": klass, "reason": law})

    # the underscore/hyphen guarded family -- direction-honesty on the known two-spelling set
    for eid in ("mp.02.account-distribution", "mp.12.account-units", "mp.11.non-model-assets"):
        out["translations"].append({"entity": eid, "field": "canonical_name",
            "note": "GUARDED SET: served spells with '-', gold spells with '_' (one spelling per LAYER "
                    "by construction, publisher _KEY_RE). Both spellings are REAL; a canon update keyed "
                    "on either alone reads the other half as orphaned. Emitted keys keep the SERVED "
                    "spelling; the gold twin is NOT a canon absence."})

    n_upd = len(out["updates"])
    out["denominators"] = {
        "rectangle_cells_in": counts["cells_in"],
        "by_status": {k: v for k, v in counts.items() if k not in ("cells_in",)},
        "updates_derived_mechanical": n_upd,
        "proposals_to_judgment_channel": len(out["proposals"]),
        "named_gaps": len(out["gaps"]),
        "accounting_check": "updates + proposals + gaps == cells_in -> %s"
                            % (n_upd + len(out["proposals"]) + len(out["gaps"]) == counts["cells_in"]),
        "canon_entries_touched": "%d of %d resolver threads (the mdpf + model-portfolios rows)" % (len(mp_threads), M),
        "translations_reported": len(out["translations"]),
    }
    dst = os.path.join(SCRATCH, "emit_bridge_dryrun_output.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), indent=1)
    print("== EMIT-BRIDGE DRY-RUN (row-10 live exercise) ==")
    print(json.dumps(out["denominators"], indent=1))
    print("\nGAP CLASSES (every non-emitted cell named):")
    from collections import Counter
    gc = Counter((g["class"], g["field"]) for g in out["gaps"])
    for (kls, f), n in sorted(gc.items()):
        print("  %-18s %-22s x%d" % (kls, f, n))
    print("\nsample mechanical update:", json.dumps(out["updates"][0], indent=1)[:500])
    print("\noutput -> %s" % dst)


if __name__ == "__main__":
    main()
