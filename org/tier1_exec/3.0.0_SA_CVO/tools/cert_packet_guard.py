# -*- coding: utf-8 -*-
"""cert_packet_guard -- the CVO~Z certification-packet guard (K.2 companion).

WHY THIS EXISTS. Under K.2 every certification carries a signed reconstruction
attestation: did the verifier derive, or attempt to derive, the plant's location by any
non-assessment route? A "no" is only worth something if the verifier's own instruments
could not have taken such a route by ACCIDENT -- and mine could. My booleans-only leak
check walked EVERY file in the run directory. Under K.1/K.2 packaging that is harmless,
because the packet no longer contains rectangle.dry.json. But it is a route that would
reconstruct incidentally if the packaging ever regressed or a stray artifact landed in the
directory, and it would do so WHILE I WAS RUNNING A CONTROL.

An accidental reconstruction is still a reconstruction, and "I did not mean to" is not an
answer an attestation can carry. So this guard FAILS CLOSED: it reads only an explicit
allowlist of packet members, and REFUSES on anything else it finds rather than opening it.
A refusal is not an error -- it is a finding, and it goes into the attestation as a route
ENCOUNTERED AND DECLINED.

It also runs the leak check itself, which is the part that must never leak while checking:
every result is a BOOLEAN. The file contents never reach the operator, so verifying
leak-freedom cannot itself hand the verifier the thing being verified.

Usage:  python cert_packet_guard.py <run_dir>
Exit 0 = packet conforms and no leak detected. 1 = refusal(s) or leak(s) -- both are
findings for the certification, never silent.
"""
from __future__ import annotations

import json
import os
import sys

# The K.1/K.2 verifier packet. Anything outside this is REFUSED, not read.
ALLOWED_EXACT = {
    "rectangle.c0.json",
    "rectangle.final.json",
    "run.json",
    "run_supplement.json",
    "MUTANT_WARNING.md",
    "axis_declaration.json",
    "certification.json",
    "SEMANTICS_CVO_PLANE_BC.json",
}
ALLOWED_DIRS = {"patches"}

# NEVER OPENED, by name, even if present. rectangle.dry.json is the mutant's complement
# under binding K; the intermediate rectangles reconstruct cells the same way.
FORBIDDEN_EXACT = {"rectangle.dry.json", "rectangle.final.certified.json"}
FORBIDDEN_PREFIX = ("rectangle.c",)   # c1, c2, ... intermediates
FORBIDDEN_ALLOW = {"rectangle.c0.json"}   # c0 is the born-UNMEASURED skeleton; safe

# The seal. Opened only AFTER the pass is written and signed -- never by this guard.
SEAL = "MUTANT_SEALED.md"


def classify(name: str, allowed_names=None) -> str:
    if name == SEAL:
        return "SEAL (not opened by this guard)"
    if name in FORBIDDEN_EXACT:
        return "FORBIDDEN -- reconstructs the plant"
    if name.startswith(FORBIDDEN_PREFIX) and name not in FORBIDDEN_ALLOW:
        return "FORBIDDEN -- intermediate rectangle reconstructs cells"
    if name in (allowed_names if allowed_names is not None else ALLOWED_EXACT):
        return "allowed"
    return "UNEXPECTED -- refused, not read"


def main(run_dir: str, extra_allowed=None) -> int:
    """extra_allowed: names the AUTHOR declared as packet members for THIS program.

    THE PACKET COMPOSITION IS PER-PROGRAM AND MY ALLOWLIST WAS HARDCODED TO ONE SHAPE.
    Measured on the first non-portal subject (comp-verdict-tools, an INSTRUMENT run): the
    guard refused DOMAIN_BAR.md and exercises/ -- both DECLARED members of that packet, and
    exercises/ is the certifier's whole exercise basis for an instrument subject. Refusing a
    declared member is fail-closed and therefore SAFE, but it is a FALSE POSITIVE, and a
    guard that cries wolf on legitimate members trains its operator to wave it through --
    which is the failure mode a fail-closed guard is supposed to prevent.
    So the DECLARED allowlist now TRAVELS WITH THE INVOCATION rather than being assumed.
    What does NOT travel: the FORBIDDEN set. dry, the intermediate rectangles and the seal
    are never openable by declaration, because those are the certifier's own integrity
    boundary and not the author's to widen.
    """
    entries = sorted(os.listdir(run_dir))
    allowed_names = set(ALLOWED_EXACT) | set(extra_allowed or [])
    allowed_dirs = set(ALLOWED_DIRS) | {n.rstrip("/") for n in (extra_allowed or [])}

    # ---- PHASE GATE, and this one was found by exercising the guard ---------
    # K.1 composition binds the PRE-VERDICT packet only. At CLOSURE the full set
    # ships by design -- dry, the intermediates, the certification naming the plant.
    # Run against a closed run, an earlier version of this guard reported FORBIDDEN
    # and SEAL LEAK on a completely legitimate archive. THAT IS THE FALSE-ALARM CLASS
    # THIS PROGRAM KEEPS CATALOGUING, arriving in the instrument I built to prevent it:
    # a control that cannot tell the state it polices from the state it does not.
    # Discriminator: a signed certification.json means the verdict exists, so the seal
    # is already public and K.1 no longer applies.
    if "certification.json" in entries:
        print("PACKET GUARD -- %s" % run_dir)
        print("  PHASE: POST-VERDICT (certification.json present).")
        print("  K.1 packet composition DOES NOT APPLY -- at closure the full set ships")
        print("  by design, including dry and the intermediates. Nothing here is a finding.")
        print("  VERDICT: N/A -- run this guard BEFORE the pass, on a pre-verdict packet.")
        return 0

    allowed, refused, forbidden = [], [], []
    for name in entries:
        path = os.path.join(run_dir, name)
        if os.path.isdir(path):
            (allowed if name in allowed_dirs else refused).append(name + "/")
            continue
        k = classify(name, allowed_names)
        if k == "allowed":
            allowed.append(name)
        elif k.startswith("FORBIDDEN"):
            forbidden.append((name, k))
        elif k.startswith("SEAL"):
            pass
        else:
            refused.append(name)

    print("PACKET GUARD -- %s" % run_dir)
    print("  packet members read : %d  %s" % (len(allowed), allowed))
    if forbidden:
        print("  ** FORBIDDEN PRESENT (NOT READ) **")
        for n, k in forbidden:
            print("     %-34s %s" % (n, k))
        print("     -> K.1 packaging REGRESSION. Record in the attestation as a route")
        print("        ENCOUNTERED AND DECLINED, and report it to the author + CTO~Z.")
    if refused:
        print("  ** UNEXPECTED, REFUSED (NOT READ) **: %s" % refused)
        print("     -> fail-closed by design. Adjudicate before reading anything.")

    # ---- leak check, BOOLEANS ONLY -----------------------------------------
    rect_path = os.path.join(run_dir, "rectangle.final.json")
    if not os.path.exists(rect_path):
        print("  LEAK CHECK: SKIPPED -- no rectangle.final.json in packet")
        return 1 if (forbidden or refused) else 0
    rect = json.load(open(rect_path, encoding="utf-8"))
    ents = [e["entity_id"] for e in rect.get("entities", [])]
    fields = list(rect.get("fields", []))
    rels = [r.get("relation_id") for r in (rect.get("relations") or []) if r.get("relation_id")]

    leaks = []
    for name in allowed:
        if name.endswith("/"):
            continue
        text = open(os.path.join(run_dir, name), encoding="utf-8", errors="replace").read()
        for line in text.splitlines():
            low = line.lower()
            if "mutant" not in low:
                continue
            names_entity = any(e.lower() in low for e in ents) or any(r and r in line for r in rels)
            names_field = any(f in line for f in fields)
            if names_entity and names_field:
                leaks.append(name)          # FILE NAME ONLY -- never the line
                break

    print("  LEAK CHECK (booleans only; no content is surfaced)")
    print("    entities in rectangle : %d   relations: %d   fields: %d"
          % (len(ents), len(rels), len(fields)))
    print("    files co-locating a mutant mention with an entity/relation AND a field: %s"
          % (sorted(set(leaks)) or "NONE"))
    if leaks:
        print("    -> SEAL LEAK. The packet discloses the plant. Record it and do NOT")
        print("       score the resulting catch as blind.")

    ok = not (forbidden or refused or leaks)
    print("  VERDICT: %s" % ("CLEAN -- blind pass is available" if ok else "FINDINGS -- see above"))
    return 0 if ok else 1


if __name__ == "__main__":
    # usage: cert_packet_guard.py <run_dir> [--allow name1,name2,...]
    # --allow carries the AUTHOR's DECLARED packet members for this program. It can only
    # ever WIDEN the allowed set; it can never open a FORBIDDEN one (dry / intermediate
    # rectangles / the seal), because that boundary is the certifier's, not the author's.
    if len(sys.argv) not in (2, 4) or (len(sys.argv) == 4 and sys.argv[2] != "--allow"):
        print(__doc__)
        sys.exit(2)
    extra = sys.argv[3].split(",") if len(sys.argv) == 4 else []
    if extra:
        print("DECLARED-PACKET WIDENING accepted for this program: %s" % ", ".join(extra))
    try:
        sys.exit(main(sys.argv[1], extra))
    except (IOError, OSError, ValueError) as exc:
        print("READ ERROR -- I could not look, which is NOT a violation: %s" % exc)
        sys.exit(2)
