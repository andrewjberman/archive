"""C5-POLICY Phase 3 -- the engine answers over a READ-ONLY snapshot of the real enumerations.

⛔ THIS IS A MEASUREMENT OF THE ESTATE'S AUTHORITY SURFACE, NOT AN ENFORCEMENT OF IT.
The file is opened 'r' and never written. Nothing here evaluates a real act, blocks a real
commit, or wires into a hook. The engine is asked questions ABOUT declared policy objects.

⛔ PLANE = DESIRED, SUBSTRATE = codebase, AND THE CHOICE IS THE POINT.
`.owned-paths.yaml` is the DECLARED authority. The pre-commit hook is what APPLIES it. This
phase reads the FILE, so the honest plane is DESIRED -- not APPLIED (I did not read the
hook's behaviour) and not EXERCISED (I did not run an act through it). My S0 limits section
already conceded exactly this, and the emitted Observation_Records must not claim a rung the
measurement never stood on. Same discipline as C6's fixture emissions, one plane over.

Run:  python phase3_snapshot.py
Exit: 0 iff the snapshot loads, every control discriminates, and the denominators print.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

from policy_objects import Regime, WhatPlane, WhoPlane

REPO = Path(__file__).resolve().parents[5]
OWNED = REPO / ".owned-paths.yaml"
SPAWN_AUDIT = REPO / "org" / "mcp" / "agent-spawn-audit.log"
INBOX = REPO / "org" / "mcp" / "inbox"

PLANE, SUBSTRATE = "DESIRED", "codebase"


# ------------------------------------------------------------------ the principal resolver

def build_resolver():
    """Does this principal exist? Union of spawn history and inbox presence.

    RETURNS (resolver, provenance) -- provenance names WHAT WAS READ, so a False verdict can
    be audited rather than trusted. A resolver whose sources are unstated is an oracle, and
    an oracle is what this component exists to replace.
    """
    seen: set[str] = set()
    sources: dict[str, int] = {}

    if SPAWN_AUDIT.is_file():
        txt = SPAWN_AUDIT.read_text(encoding="utf-8", errors="replace")
        found = set(re.findall(r"\b\d+\.\d+\.\d+_[A-Za-z]+_[A-Za-z0-9]+(?:~[A-Za-z0-9]+)?\b", txt))
        seen |= found
        sources["agent-spawn-audit.log"] = len(found)
    else:
        sources["agent-spawn-audit.log"] = -1  # ABSENT, not zero

    if INBOX.is_dir():
        dirs = set()
        for base in INBOX.iterdir():
            if not base.is_dir():
                continue
            dirs.add(base.name)
            for sub in base.iterdir():
                if sub.is_dir() and sub.name.startswith("~"):
                    dirs.add(f"{base.name}{sub.name}")
        seen |= dirs
        sources["inbox dirs"] = len(dirs)
    else:
        sources["inbox dirs"] = -1

    # THIRD SOURCE, ADDED AFTER THE FIRST RUN PRODUCED FALSE DEAD VERDICTS.
    # The first version sourced existence from spawn-audit + inbox dirs only, and reported
    # 14 dead members. Two of them -- 0.1.2_RD_CausalityEngine and 0.3.3_RD_DataRefresh --
    # HAVE AGENT FOLDERS under org/tier*/ and are plainly real seats. They simply predate
    # the spawn-audit log or never took inbox mail.
    #
    # THIS IS THE LIMIT THIS MODULE ALREADY DECLARED IN ITS OWN LIMITS LIST -- "a principal
    # that existed and left no trace in either would read DEAD incorrectly" -- FIRING. The
    # declaration was correct and did not prevent the error; only widening the source did.
    # A resolver's verdict is bounded by its sources, and an incomplete source set produces
    # FALSE DEAD, which is the direction that defames a real seat rather than missing a
    # dead one.
    tiers = ("tier0", "tier0_exec", "tier1_exec", "tier2_senior", "tier3_junior")
    folders = set()
    for t in tiers:
        d = REPO / "org" / t
        if d.is_dir():
            folders |= {p.name for p in d.iterdir() if p.is_dir()}
    seen |= folders
    sources["org/tier*/ agent folders"] = len(folders)

    return (lambda p: p in seen), sources, seen


# ---------------------------------------------------------------------------- the report

def main() -> int:
    print("=" * 86)
    print("C5-POLICY Phase 3 -- READ-ONLY snapshot measurement of the authority surface")
    print("=" * 86)

    if not OWNED.is_file():
        print(f"FAIL: {OWNED} not found. Refusing to measure a surface I cannot read.")
        return 1

    raw = OWNED.read_text(encoding="utf-8")          # 'r' -- never written
    doc = yaml.safe_load(raw)
    lanes, paths = doc["lanes"], doc["paths"]
    print(f"  SNAPSHOT: {OWNED.relative_to(REPO)}  {len(raw):,} bytes  "
          f"rollout_phase={doc.get('rollout_phase')}")
    print(f"  plane={PLANE} substrate={SUBSTRATE}  <- the DECLARED config, not the applied hook")

    resolver, sources, seen = build_resolver()
    print("\n  RESOLVER SOURCES (named so a False verdict is auditable):")
    for k, v in sources.items():
        print(f"    {k:<26} {'** ABSENT, NOT READ **' if v < 0 else f'{v} principals'}")
    print(f"    union known principals     {len(seen)}")

    # --- CONTROLS ON THE RESOLVER, run before any verdict is quoted -------------------
    print("\n  RESOLVER CONTROLS (it must return BOTH answers):")
    ctrl = [("0.7.0_AE_CloudOps", True), ("0.4.0_DS_ClientPlatform~A", True),
            ("0.4.0_DS_ClientPlatform_A", False), ("9.9.9_ZZ_NoSuchSeat", False)]
    ctrl_ok = True
    for probe, expect in ctrl:
        got = resolver(probe)
        flag = "OK" if got == expect else "*** MISCLASSIFIED ***"
        if got != expect:
            ctrl_ok = False
        print(f"    {probe:<30} resolves={str(got):<5} expected={str(expect):<5} {flag}")
    if not ctrl_ok:
        print("  FAIL: the resolver does not discriminate. Every verdict below would be worthless.")
        return 1

    # --- WHAT PLANE ------------------------------------------------------------------
    print("\n" + "-" * 86)
    print("  WHAT PLANE -- 'which objects are in scope'")
    print("-" * 86)
    enum_p = [k for k in paths if not WhatPlane._GLOB.search(k)]
    pred_p = [k for k in paths if WhatPlane._GLOB.search(k)]
    print(f"    DENOMINATOR {len(paths)} path rules")
    print(f"    ENUMERATION {len(enum_p):>4}  ({100*len(enum_p)/len(paths):.1f}%)  "
          f"a NEW file is NOT covered")
    print(f"    PREDICATE   {len(pred_p):>4}  ({100*len(pred_p)/len(paths):.1f}%)  "
          f"a NEW file IS covered if in scope")

    # honesty: does each declared plane match its own regime?
    dishonest = []
    for k in paths:
        regime = Regime.PREDICATE if WhatPlane._GLOB.search(k) else Regime.ENUMERATION
        wp = WhatPlane(regime=regime, members=(k,))
        if not wp.declared_regime_is_honest():
            dishonest.append(k)
    print(f"    regime-honesty check: {len(paths) - len(dishonest)}/{len(paths)} consistent"
          + (f"  INCONSISTENT: {dishonest[:5]}" if dishonest else ""))

    # --- WHO PLANE -- the part with provenance ---------------------------------------
    print("\n" + "-" * 86)
    print("  WHO PLANE -- 'which principals hold it' (ENUMERATION-WITH-PROVENANCE)")
    print("-" * 86)
    total_entries = 0
    dead_by_lane: dict[str, tuple[str, ...]] = {}
    patterned = []
    for lane, v in lanes.items():
        members = tuple(v.get("permitted_agents") or [])
        total_entries += len(members)
        regime = (Regime.PREDICATE
                  if any(WhatPlane._GLOB.search(str(m)) for m in members)
                  else Regime.ENUMERATION)
        if regime is Regime.PREDICATE:
            patterned.append(lane)
            continue
        wp = WhoPlane(regime=regime, members=members, resolver=resolver)
        dead = wp.dead_members()
        if dead:
            dead_by_lane[lane] = dead

    print(f"    DENOMINATOR {total_entries} permitted_agents entries across {len(lanes)} lanes")
    print(f"    PREDICATE lanes (a new seat COULD be covered): {len(patterned)}  {patterned}")
    print(f"    ENUMERATION lanes                            : {len(lanes) - len(patterned)}")
    dead_total = sum(len(v) for v in dead_by_lane.values())
    print(f"\n    DEAD MEMBERS: {dead_total} across {len(dead_by_lane)} lane(s)")
    for lane, dead in sorted(dead_by_lane.items()):
        print(f"       {lane:<22} {list(dead)}")
    if not dead_by_lane:
        print("       none -- but note this is a MEASURED zero against a discriminating "
              "resolver, not an assumption")

    # --- THE HEADLINE ASYMMETRY ------------------------------------------------------
    print("\n" + "=" * 86)
    pct_pred_what = 100 * len(pred_p) / len(paths)
    pct_enum_who = 100 * (total_entries - sum(
        len(v.get("permitted_agents") or []) for k, v in lanes.items() if k in patterned)
    ) / total_entries
    print(f"  THE ASYMMETRY: {pct_pred_what:.0f}% PREDICATE on WHAT may be touched, "
          f"{pct_enum_who:.0f}% ENUMERATION on WHO may touch it.")
    print(f"  A newly spawned seat is covered by {len(patterned)} lane(s) and no other.")
    print("=" * 86)

    # --- the C1 acquisition record ----------------------------------------------------
    rec = {
        "plane": PLANE,
        "substrate": SUBSTRATE,
        "population_predicate": "authority rules declared in .owned-paths.yaml",
        "denominator": {"paths": len(paths), "lanes": len(lanes),
                        "permitted_agents_entries": total_entries},
        "substantive_result": {
            "state": "KNOWN",
            "value": {"what_enumeration": len(enum_p), "what_predicate": len(pred_p),
                      "who_predicate_lanes": len(patterned),
                      "dead_members": dead_total},
            "reason": None,
        },
        "limits": [
            "measured the FILE, not the ENFORCEMENT -- plane is DESIRED, never APPLIED",
            f"rollout_phase={doc.get('rollout_phase')} is present and NOT interpreted; these "
            f"are rules PRESENT, not rules currently ENFORCED",
            "the resolver's union is spawn-audit + inbox dirs; a principal that existed and "
            "left no trace in either would read DEAD incorrectly",
        ],
    }
    print("\n  C1 ACQUISITION RECORD (shape shown; emission wires to the C1 envelope):")
    print("   ", json.dumps(rec, separators=(",", ":"))[:200] + "...")

    print(f"\n  READ-ONLY CONFIRMED: {OWNED.name} opened 'r'; 0 writes performed.")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
