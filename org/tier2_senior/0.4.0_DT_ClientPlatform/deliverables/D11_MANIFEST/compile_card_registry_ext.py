#!/usr/bin/env python
"""KEYFILL-JOIN, the registry COMPILE half -- extend card_population_registry.v1 to waves 2 and 4.

⛔ THIS TOOL REFUSES TO RUN WHILE THE FILL LANES ARE MOVING, and that refusal is the point.

THE FINDING THAT SHAPED IT (measured, 0.4.0_DT_ClientPlatform~X 79140): the registry identifies its
members by CONTENT -- `git_blob_id` -- and at HEAD not one of its 13 pins named the blob at that
path. 13 of 13 stale. Measured against the commit BEFORE this seat's first keyfill commit, 13 of 13
were ALREADY stale, so the drift PREDATES the keyfill round; the round then moved 9 of them again
while three lanes filled concurrently.

The compile half was cleared to start immediately because it was thought independent of the fills.
A CONTENT-ADDRESSED registry is not independent of them: compiling mid-round produces pins naming
bytes that three lanes are still editing, and the JOIN admits ONLY registry-ratified members, so the
mismatch would surface at join time -- or silently not surface at all, if anything falls back to
matching by path.

4.0.0_SA_CRO~X RULING (210720Z), implemented here as GUARDS rather than as intentions:
  * do not write or ratify while any fill face is not issuer-COMPLETE  -> refuse_unless_settled()
  * name ONE settled authority commit; recompute EVERYTHING at it      -> --pin, required
  * inherited W3 pins recomputed at that same pin, not carried forward -> no carry-forward path
  * candidate_set_digest from the SAME member set at the SAME pin      -> single-pin digest
  * path-only fallback REFUSED                                         -> a missing blob is an error
  * silent stale carry-forward REFUSED                                 -> old pins are never copied
  * mixed-pin digesting REFUSED                                        -> one pin threads everything
  * record the 13/13 staleness and its pre-round attribution           -> written onto the output
An earlier pinned draft is diagnostic only, must not overwrite the registry, and cannot feed RAT or
JOIN -- so --apply is refused unless the settle guard passes, and --draft never writes the registry.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
REGISTRY = os.path.join(HERE, "card_population_registry.v1.json")
FILL_FACES = [
    "org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/NFRA_SUBSTRATECARDING.TO-KEYFILL-DTX.key-expression-fill.md",
    "org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_SUBSTRATECARDING.TO-KEYFILL-COX.key-expression-fill.md",
    "org/tier2_senior/0.8.0_AE_CloudComp/task_orders/NFRA_SUBSTRATECARDING.TO-KEYFILL-CCX.key-expression-fill.md",
    "org/tier2_senior/0.8.0_AE_CloudComp/task_orders/NFRA_SUBSTRATECARDING.TO-KEYFILL-CCY.key-expression-fill.md",
]
WAVE_GLOBS = ["org/**/D11_CARDS_W2/*.json", "org/**/D11_CARDS_W4/*.json"]


def face_status(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return "FACE ABSENT"
    with open(p, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if "<status>" in line:
                return line.split("<status>")[1].split("</status>")[0].strip()[:40]
    return "NO STATUS TAG"


def refuse_unless_settled():
    """Every fill face must read complete. A face that is merely ABSENT is NOT complete -- absence
    and completion are different facts and this guard must not confuse them."""
    rows = [(rel.split("TO-")[1][:12], face_status(rel)) for rel in FILL_FACES]
    unsettled = [(n, s) for n, s in rows if not s.lower().startswith("complete")]
    print("FILL FACES, the settle guard (denominator %d):" % len(rows))
    for n, s in rows:
        print("   %-14s %s" % (n, s[:70]))
    return unsettled


def blob_at(pin, rel):
    """The blob id AT THE PIN. git's clean filter has already LF-normalised what it stored, so this
    is the LF-normalised id by construction -- verified on this repo: git rev-parse HEAD:<path>,
    git hash-object on the worktree, and a hand-computed sha1 over LF-normalised bytes all agree."""
    try:
        return subprocess.check_output(["git", "rev-parse", "%s:%s" % (pin, rel)],
                                       cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError:
        return None


def card_at(pin, rel):
    """The parsed object at the pin, or None if it will not parse."""
    try:
        raw = subprocess.check_output(["git", "show", "%s:%s" % (pin, rel)],
                                      cwd=ROOT, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        return None


def subject_of(pin, rel):
    try:
        raw = subprocess.check_output(["git", "show", "%s:%s" % (pin, rel)],
                                      cwd=ROOT, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None
    try:
        return (json.loads(raw).get("subject") or {}).get("id")
    except ValueError:
        return None


def candidates_at(pin):
    """Card paths under the wave globs, listed FROM THE PIN's tree, not from the working directory.
    Listing from disk would mix an unpinned view into a pinned compile."""
    out = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", pin], cwd=ROOT)
    names = out.decode("utf-8", "replace").splitlines()
    keep = []
    for n in names:
        if ("/D11_CARDS_W2/" in n or "/D11_CARDS_W4/" in n) and n.endswith(".json"):
            keep.append(n)
    return sorted(keep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin", help="the ONE settled authority commit; everything is computed at it")
    ap.add_argument("--apply", action="store_true", help="write the registry (settle guard must pass)")
    ap.add_argument("--draft", action="store_true", help="diagnostic only; never writes the registry")
    args = ap.parse_args()

    unsettled = refuse_unless_settled()
    if unsettled and args.apply:
        print("\nREFUSING to apply: %d fill face(s) are not issuer-COMPLETE -- %s"
              % (len(unsettled), ", ".join(n for n, _ in unsettled)))
        print("A registry compiled while lanes are filling pins bytes those lanes are still editing,")
        print("and the JOIN admits only registry-ratified members (4.0.0_SA_CRO~X 210720Z).")
        return 2
    if not args.pin:
        print("\nREFUSING: --pin is required. A compile with no named authority commit cannot say")
        print("what its blob ids are ids OF, and mixed-pin digesting is refused by the ruling.")
        return 2

    pin = subprocess.check_output(["git", "rev-parse", "--verify", "%s^{commit}" % args.pin],
                                  cwd=ROOT).decode().strip()
    with open(REGISTRY, encoding="utf-8") as fh:
        reg = json.load(fh)
    inherited = reg["extension_population"]["members"]

    # 1. the inherited W3 pins, RECOMPUTED at the pin -- never carried forward
    stale, recomputed, missing = 0, [], []
    for m in inherited:
        b = blob_at(pin, m["path"])
        if b is None:
            missing.append(m["path"])
            continue
        if b != m["git_blob_id"]:
            stale += 1
        recomputed.append({"git_blob_id": b, "path": m["path"],
                           "subject_id": m.get("subject_id") or subject_of(pin, m["path"])})

    # 2. the W2/W4 candidates, at the same pin
    # A FILE UNDER THE WAVE GLOB THAT IS NOT A CARD IS AN EXCLUSION, NAMED WITH ITS REASON.
    # A file that IS a card but whose blob or subject cannot be read at the pin is an ERROR. The
    # first compile conflated them and failed the whole run on W4-FILE.cells.json -- a cell manifest
    # (to_id / decomp_ref / cell_total) that happens to live in a wave directory. Certification arm
    # 3 asks for that exclusion to be NAMED, not for the compile to die on it; and the distinction
    # is the same one this project keeps paying for -- a thing absent by its nature versus a read
    # that failed.
    added, add_missing, excluded = [], [], []
    for rel in candidates_at(pin):
        b = blob_at(pin, rel)
        if b is None:
            add_missing.append((rel, "blob unreadable at the pin"))
            continue
        card = card_at(pin, rel)
        if card is None:
            add_missing.append((rel, "unparseable JSON at the pin"))
            continue
        if not card.get("schema_version") and not card.get("subject"):
            excluded.append((rel, "NOT A CARD: no schema_version and no subject -- %s"
                             % ", ".join(list(card)[:4])))
            continue
        s = (card.get("subject") or {}).get("id")
        if not s:
            add_missing.append((rel, "a card with no subject.id"))
            continue
        added.append({"git_blob_id": b, "path": rel, "subject_id": s})

    members = sorted(recomputed + added, key=lambda m: m["path"])

    # -- THE BINDING RAT RULE (4.0.0_SA_CRO~X 211251Z) -------------------------------------------
    # SUBSTRATE_CARD.v3 ACCEPTS basis_by_field.key_expression == 'inferred'. I verified it against
    # the schema: the enum is [measured, inferred, held, absent] and a card carrying 'inferred'
    # VALIDATES. So a v3 PASS does NOT enforce arm 2, and any "inferred = 0" is EXECUTOR AND
    # CERTIFIER evidence, never schema evidence. This compiler must not borrow the schema's
    # authority for a guarantee the schema does not make -- so it scans every candidate member
    # ITSELF, at the pin, and REFUSES on any inferred, citing path and blob.
    dist, inferred_members = {}, []
    for m in members:
        card = card_at(pin, m["path"])
        b = (((card or {}).get("trust") or {}).get("key") or {}).get("basis_by_field", {})             .get("key_expression")
        dist[str(b)] = dist.get(str(b), 0) + 1
        if b == "inferred":
            inferred_members.append((m["path"], m["git_blob_id"]))
    print("   key_expression basis across the member set: %s" % json.dumps(dist, sort_keys=True))
    print("   (this is the COMPILER's own scan at the pin -- v3 accepts 'inferred', so a v3 PASS")
    print("    does not establish this and the guarantee is not attributed to it)")
    if inferred_members:
        print("   REFUSING: %d member(s) carry basis 'inferred' for key_expression"
              % len(inferred_members))
        for path, blob in inferred_members[:10]:
            print("      %s  blob %s" % (path, blob[:12]))
        return 1
    # 3. ONE digest, over the SAME member set, at the SAME pin
    payload = "\n".join("%s %s %s" % (m["git_blob_id"], m["path"], m["subject_id"])
                        for m in members) + "\n"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    print("\nCOMPILE at pin %s" % pin[:12])
    print("   inherited W3 members recomputed : %d (stale against the registry: %d)"
          % (len(recomputed), stale))
    print("   W2/W4 members added             : %d" % len(added))
    print("   members TOTAL                   : %d" % len(members))
    print("   candidate_set_digest            : %s" % digest)
    print("   digest method                   : sha256 over '<blob> <path> <subject>' lines, sorted")
    print("                                     by path, LF-joined -- ONE pin for every line")
    print("   EXCLUDED, not a card (arm 3 names each): %d" % len(excluded))
    for rel, why in excluded:
        print("      %s" % rel)
        print("         reason: %s" % why)
    if missing or add_missing:
        print("   ERRORS, a CARD whose bytes could not be read at the pin: %d inherited, %d candidate"
              % (len(missing), len(add_missing)))
        for item in (missing + [r for r, _w in add_missing])[:5]:
            print("      %s" % item)
        print("   A path-only member is refused by the ruling, so these are errors, not entries.")
        return 1

    out = dict(reg)
    out["extension_population"] = {"members": members}
    out["candidate_set_digest"] = digest
    out["ratified_at_commit"] = None          # the RATIFIER sets this; the compiler never does
    out["compiled_at_commit"] = pin
    out["discovery_globs"] = sorted(set(reg.get("discovery_globs", []) + WAVE_GLOBS))
    out["compile_note"] = (
        "Inherited W3 pins were RECOMPUTED at compiled_at_commit, not carried forward: measured "
        "%d of %d stale against the previous registry (ratified_at_commit %s). The staleness "
        "PREDATES the keyfill round -- at the commit before this seat's first keyfill commit, 13 of "
        "13 were already stale -- and the round moved 9 of them again while three lanes filled "
        "concurrently. Every blob id and the digest are computed at ONE pin; path-only fallback, "
        "silent stale carry-forward and mixed-pin digesting are refused (4.0.0_SA_CRO~X 210720Z). "
        "EXCLUDED as not-a-card: %s."
        % (stale, len(recomputed), (reg.get("ratified_at_commit") or "?")[:12],
           "; ".join(r for r, _w in excluded) or "none"))

    if args.apply and not unsettled:
        with open(REGISTRY, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("   APPLIED to %s (ratified_at_commit left NULL for the ratifier)"
              % os.path.relpath(REGISTRY, ROOT).replace("\\", "/"))
    else:
        print("   NOT WRITTEN -- %s" % ("draft/diagnostic only, and it cannot feed RAT or JOIN"
                                        if args.draft else "pass --apply once the faces settle"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
