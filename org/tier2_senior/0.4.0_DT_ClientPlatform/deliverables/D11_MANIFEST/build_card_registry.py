#!/usr/bin/env python3
"""RATIFY the current CARD_GLOB result into an explicit card population registry.

4.0.0_SA_CRO~A's admission ruling: W3-only is INTENTIONAL-BUT-TEMPORAL, CARD_GLOB must NOT be
widened, and the successor is an authored registry with INDEPENDENT populations. This is the
one-time hand-off from a PATTERN to an ENUMERATION.

⛔ WHY THIS IS A ONE-SHOT WITH AN EXPLICIT FLAG, AND NOT A REBUILD. If this script simply
regenerated the registry from the glob on every run, THE GLOB WOULD STILL BE THE AUTHORITY --
one indirection further away, where nobody would look for it. That is the whole defect being
retired. So:

    --ratify   writes the registry, and REFUSES if one already exists
    (default)  DIFFS the glob against the registry and reports, changing nothing

The diff mode is the honest use after ratification: it tells a reader which candidates the
discovery glob can see and the registry does not admit. Reporting a candidate is not admitting
it, and that distinction is the reason the file exists.

⛔ THIS SCRIPT DOES NOT RUN THE COMPILER and does not touch graph_object_manifest.json.
"""
from __future__ import annotations

import argparse
import glob as _glob
import hashlib
import json
import os
import subprocess
import sys

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST")
REGISTRY = os.path.join(HERE, "card_population_registry.v1.json")
SCHEMA = os.path.join(HERE, "CARD_POPULATION_REGISTRY.v1.schema.json")
DISCOVERY_GLOBS = ["org/**/D11_CARDS_W3/*.json"]

# The predicate is written out because "incomplete receiver payload cannot admit" is
# unactionable until someone states what complete means. 1.0.0_SA_CTO~X supplied the exact
# L0-side requirement for `key`; the other two follow the same shape.
PREDICATES = {
    "grain": (
        "The card carries an AUTHORED GRAIN PROJECTION that satisfies the L0 declared `grain` "
        "branch -- unit non-blank, basis in {measured, held, inferred}, evidence and owner "
        "non-blank. No card in the estate carries such a projection today, admitted or not, "
        "so this population is empty on a SOURCE fact rather than a configuration one."),
    "key": (
        "The card satisfies the L0 declared `key` branch: identity_space, key_expression, "
        "key_is_stable, crosses_spaces, declared_mapping, basis in {measured, held, inferred}, "
        "evidence, owner -- ALL NON-BLANK. ⛔ SUBSTRATE_CARD.v2 HAS NO key_expression FIELD "
        "(it carries the other seven, i.e. every property of the key and never the key), so no "
        "card of any vintage can satisfy this. Empty BY CONTRACT, not by oversight."),
    "failure_mode": (
        "The card carries a complete trust.failure_mode: returns_on_failure, "
        "distinguishable_from_true_negative, silent_degrade_paths, basis in {measured, held, "
        "inferred}, evidence, owner -- all non-blank. Payloads satisfying this DO exist outside "
        "the admitted population, so this is the one receiver whose emptiness is not a "
        "knowledge fact -- but admitting them still requires a schema-bound transform, which "
        "does not exist, so no member can carry a transform_version yet."),
}


def sha256_of(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def rel(path: str) -> str:
    return os.path.relpath(path, WS).replace(os.sep, "/")


def discover() -> list:
    """CANDIDATE DISCOVERY ONLY. The return value of this function is never authority."""
    hits = []
    for pattern in DISCOVERY_GLOBS:
        hits.extend(_glob.glob(os.path.join(WS, pattern), recursive=True))
    return sorted(set(hits))


def member_of(path: str) -> dict:
    with open(path, "rb") as fh:
        raw = fh.read()
    card = json.loads(raw.decode("utf-8"))
    subject = (card.get("subject") or {}).get("id")
    if not subject:
        raise SystemExit("REFUSING -- %s has no subject.id; a member pinned by path and digest "
                         "alone cannot tell a substituted subject from an edited file"
                         % rel(path))
    return {"path": rel(path), "sha256": hashlib.sha256(raw).hexdigest(),
            "subject_id": subject}


def build() -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS,
                          capture_output=True, text=True, check=True).stdout.strip()
    members = [member_of(p) for p in discover()]
    seen = {}
    for m in members:
        if m["subject_id"] in seen:
            raise SystemExit(
                "REFUSING -- two admitted cards share subject.id %r (%s and %s). A population "
                "with a duplicate subject cannot answer 'which card qualifies this part'."
                % (m["subject_id"], seen[m["subject_id"]], m["path"]))
        seen[m["subject_id"]] = m["path"]
    return {
        "registry_version": "v1",
        "ratified_at_commit": head,
        "extension_population": {"members": members},
        "receiver_source_populations": {
            r: {"members": [], "transform_version": None,
                "declared_branch_predicate": PREDICATES[r]}
            for r in ("grain", "key", "failure_mode")
        },
        "discovery_globs": list(DISCOVERY_GLOBS),
    }


def validate(doc: dict) -> list:
    from jsonschema import Draft202012Validator
    with open(SCHEMA, encoding="utf-8") as fh:
        return list(Draft202012Validator(json.load(fh)).iter_errors(doc))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ratify", action="store_true",
                    help="write the registry ONCE; refuses if it already exists")
    args = ap.parse_args()

    if args.ratify:
        if os.path.exists(REGISTRY):
            raise SystemExit(
                "REFUSING -- %s already exists. Re-ratifying from the glob would restore the "
                "glob as the authority one indirection away, which is the defect the registry "
                "retires. Edit the registry deliberately instead." % rel(REGISTRY))
        doc = build()
        errs = validate(doc)
        if errs:
            for e in errs[:10]:
                print("  %s -- %s" % ("/".join(str(x) for x in e.path), e.message[:200]))
            raise SystemExit("REFUSING TO WRITE -- the registry does not validate.")
        with open(REGISTRY, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=True, sort_keys=True)
            fh.write("\n")
        print("OK: ratified %d extension members at %s"
              % (len(doc["extension_population"]["members"]), doc["ratified_at_commit"][:10]))
        print("    receiver source populations: grain=0 key=0 failure_mode=0, all by contract")
        return

    # DIFF MODE -- reports, admits nothing.
    if not os.path.exists(REGISTRY):
        raise SystemExit("no registry at %s; run with --ratify once" % rel(REGISTRY))
    with open(REGISTRY, encoding="utf-8") as fh:
        doc = json.load(fh)
    errs = validate(doc)
    print("registry validates       : %s (%d errors)" % (not errs, len(errs)))
    admitted = {m["path"]: m for m in doc["extension_population"]["members"]}
    candidates = {rel(p) for p in discover()}
    print("admitted (AUTHORITY)     : %d" % len(admitted))
    print("glob candidates (DIAG)   : %d" % len(candidates))
    unlisted = sorted(candidates - set(admitted))
    print("candidates NOT admitted  : %d %s" % (len(unlisted), unlisted))
    print("    ^ REPORTED, NOT ADMITTED. A glob never expands authority.")
    missing, drifted = [], []
    for path, m in sorted(admitted.items()):
        full = os.path.join(WS, path)
        if not os.path.exists(full):
            missing.append(path)
        elif sha256_of(full) != m["sha256"]:
            drifted.append(path)
    print("admitted but MISSING     : %d %s" % (len(missing), missing))
    print("admitted but DIGEST DRIFT: %d %s" % (len(drifted), drifted))
    if errs or missing or drifted:
        sys.exit(1)


if __name__ == "__main__":
    main()
