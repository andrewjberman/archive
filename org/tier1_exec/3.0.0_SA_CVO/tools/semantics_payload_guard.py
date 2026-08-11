# -*- coding: utf-8 -*-
"""semantics_payload_guard -- the CERTIFIER-SIDE counterpart to the author's K4 assert.

M-14, named by 0.5.0_AE_OpalETL~Z and routed to me by CTO~Z as my call. I am building it,
because declining would contradict my own finding: on /positioning I shipped a semantics
payload that crossed MY OWN plane split and dropped the evidence triple -- a REGRESSION from
a correct payload one page earlier. THE DEFECT ARRIVED WITH THE PACE, NOT THE IGNORANCE, and
what caught it was 0.5.0's build-time assert on THEIR side. There was no counterpart on mine.
A plane split enforced on one side only is a courtesy the receiving seat extends; this makes
it a split.

THE LOAD-BEARING RULE, and it is deliberately NOT a hardcoded field list:

    A SEMANTICS PAYLOAD MAY ONLY FILL CELLS THAT ARE **UNMEASURED** IN THE TARGET RECTANGLE.

That single predicate enforces the plane split without knowing what a plane is, so it CANNOT
drift from the axis the way a copied list can (the hand-copied-list defect this estate keeps
paying for -- see org/XXX.md A.3's own history). If the author measured a cell, it is theirs;
if they left it UNMEASURED, it is mine. When axis_declaration.json is present its Plane B/C
set is checked as a SECOND, independent limb -- two instruments, and a disagreement between
them is itself reported rather than silently resolved.

Also checked, because my /positioning regression failed both at once:
  - every cell is an OBJECT carrying {value, status, evidence{instrument, locator, vintage}},
    never a bare string;
  - every entity in the payload EXISTS in the target rectangle (a typo in an entity_id would
    otherwise merge into nothing and report success);
  - every entity is COMPLETE across the fields it is entitled to fill -- a partial payload is
    reported, not silently accepted, because a missing semantic cell is invisible downstream.

Usage:  python semantics_payload_guard.py <payload.json> <rectangle.final.json>
Exit 0 = payload conforms and is safe to merge. 1 = violations named. 2 = usage/read error.
Refuse to ship on rc=1: a guard whose failures are advisory is not a guard.
"""
from __future__ import annotations

import io
import json
import os
import sys

CANONICAL_BC = {"canonical_name", "business_meaning", "vintage_semantics",
                "analyst_serve_verdict", "disposition", "notes"}
REQUIRED_EVIDENCE_KEYS = ("instrument", "locator", "vintage")


def _load(path):
    return json.load(io.open(path, encoding="utf-8"))


def main(payload_path: str, rect_path: str) -> int:
    payload = _load(payload_path)
    rect = _load(rect_path)

    # --- SHAPE GATE ON THE TARGET, and it exists because I hit this twice ---------
    # First fix here caught FILE-level failures (missing path) and let STRUCTURAL ones
    # through: a non-conforming rectangle (entities as an object rather than the schema's
    # array -- the /cma 1729Z shape I refused certification on) raised an AttributeError,
    # which exits 1 and is byte-identical to "violations found". I closed the instance and
    # left the class open, which is the exact pattern CTO~Z named on the packaging fixes.
    # THE CLASS, closed: I CANNOT REPORT ON A TARGET I CANNOT READ, and that is rc=2 with a
    # named reason -- never a verdict about the payload.
    ents = rect.get("entities")
    if not isinstance(ents, list) or not ents:
        print("TARGET NOT READABLE AS A CONFORMING RECTANGLE: 'entities' is %s, expected a "
              "non-empty array per ssot_establishment.schema.json#/$defs/rectangle."
              % type(ents).__name__)
        print("  -> This is NOT a verdict about the payload. Validate the target first:")
        print("     ssot_validate.py rectangle <target>")
        return 2
    cells_by_entity = {}
    for e in ents:
        if not isinstance(e, dict) or "entity_id" not in e or not isinstance(e.get("cells"), dict):
            print("TARGET NOT READABLE: an entity is not {entity_id, cells{...}}. "
                  "Validate the target first; I am not reporting on the payload.")
            return 2
        cells_by_entity[e["entity_id"]] = {
            f: (c.get("status") if isinstance(c, dict) else None)
            for f, c in e["cells"].items()}

    # --- second, independent limb: the declared axis, when it travels ------------
    axis_bc = None
    axis_path = os.path.join(os.path.dirname(rect_path), "axis_declaration.json")
    if os.path.exists(axis_path):
        planes = (_load(axis_path) or {}).get("field_planes") or {}
        if planes:
            axis_bc = {f for f, p in planes.items() if p in ("B", "C")}

    entities = [k for k in payload if not k.startswith("_")]
    v_plane, v_shape, v_unknown, v_partial, v_axis = [], [], [], [], []

    for eid in entities:
        if eid not in cells_by_entity:
            v_unknown.append(eid)
            continue
        target = cells_by_entity[eid]
        fillable = {f for f, st in target.items() if st == "UNMEASURED"}
        for field, cell in payload[eid].items():
            # LIMB 1 -- the load-bearing one. Derived, never copied.
            if field not in target:
                v_plane.append((eid, field, "field does not exist in the rectangle"))
            elif field not in fillable:
                v_plane.append((eid, field,
                                "target cell is %s -- the AUTHOR's, not mine" % target[field]))
            # LIMB 2 -- independent cross-check against the declared axis
            if axis_bc is not None and field not in axis_bc:
                v_axis.append((eid, field))
            # SHAPE
            if not isinstance(cell, dict):
                v_shape.append((eid, field, "bare %s, not a cell object" % type(cell).__name__))
                continue
            ev = cell.get("evidence")
            if not isinstance(ev, dict):
                v_shape.append((eid, field, "no evidence object"))
            else:
                missing = [k for k in REQUIRED_EVIDENCE_KEYS if not ev.get(k)]
                if missing:
                    v_shape.append((eid, field, "evidence missing %s" % ",".join(missing)))
            if "value" not in cell or "status" not in cell:
                v_shape.append((eid, field, "missing value/status"))
        # COMPLETENESS against what this entity was entitled to fill
        gap = sorted(fillable - set(payload[eid]))
        if gap:
            v_partial.append((eid, gap))

    # COUNT DISCIPLINE, and this was found by pointing this guard at a MISMATCHED target
    # (the /market payload against /macro's rectangle) after COO~Z's staleness check caught the
    # same class in itself. The old single figure counted only cells whose ENTITY was known, and
    # printed it as "cells offered" -- so a wholly wrong-subject payload reported "cells offered: 0"
    # while carrying 12. WELL-FORMED, REFUSED CORRECTLY, AND STILL WRONG ABOUT WHAT IT COUNTED.
    # A denominator answers HOW MANY; it does not answer OF WHAT. Both numbers now print, and
    # they diverge exactly when the subject is wrong.
    offered = sum(len(payload[e]) for e in entities)
    total = sum(len(payload[e]) for e in entities if e in cells_by_entity)
    print("SEMANTICS PAYLOAD GUARD")
    print("  payload   : %s" % payload_path)
    print("  target    : %s" % rect_path)
    print("  entities  : %d   cells IN PAYLOAD: %d   cells against a KNOWN entity: %d%s"
          % (len(entities), offered, total,
             "   <-- DIVERGENT: the payload is addressing a different subject"
             if offered != total else ""))
    print("  axis limb : %s" % ("axis_declaration.json present -- cross-check ACTIVE"
                                if axis_bc is not None else
                                "axis_declaration.json ABSENT -- single-limb (derived) only"))

    def report(name, rows, fmt):
        if rows:
            print("  ** %s (%d) **" % (name, len(rows)))
            for r in rows:
                print("     " + fmt(r))

    report("CROSS-PLANE / NOT-MINE-TO-FILL", v_plane,
           lambda r: "%-30s %-22s %s" % (r[0], r[1], r[2]))
    report("SHAPE", v_shape, lambda r: "%-30s %-22s %s" % (r[0], r[1], r[2]))
    report("UNKNOWN ENTITY (not in rectangle)", v_unknown, lambda r: str(r))
    report("INCOMPLETE (fillable cells left empty)", v_partial,
           lambda r: "%-30s missing: %s" % (r[0], ", ".join(r[1])))
    if axis_bc is not None and v_axis:
        report("AXIS-LIMB DISAGREEMENT", v_axis, lambda r: "%-30s %s" % (r[0], r[1]))
        if not v_plane:
            print("     -> ⚠ THE TWO LIMBS DISAGREE: derived says fillable, declared axis says "
                  "not Plane B/C. Adjudicate before shipping; do NOT pick the permissive one.")

    bad = bool(v_plane or v_shape or v_unknown or v_partial or v_axis)
    print("  VERDICT: %s" % ("VIOLATIONS -- DO NOT SHIP" if bad else
                             "CLEAN -- safe to merge as FILL_UNMEASURED"))
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    # A RETRIEVAL FAILURE MUST NOT WEAR A VIOLATION'S EXIT CODE. Found by exercising this
    # guard: an unreadable payload path raised an uncaught FileNotFoundError, which exits 1 --
    # byte-identical to "violations found". A caller scripting on rc would have recorded a
    # missing file as a rejected payload, and a caller scripting on rc==0 would have recorded
    # it as a rejection it could act on. That is the retrieval-failure-returns-a-value class
    # arriving in the instrument built to enforce discipline. rc=2 is reserved for "I could
    # not look", and it is DISTINCT from "I looked and it is bad".
    try:
        sys.exit(main(sys.argv[1], sys.argv[2]))
    except (IOError, OSError, ValueError) as exc:
        print("READ ERROR -- I COULD NOT LOOK, which is NOT the same as a violation: %s" % exc)
        sys.exit(2)
