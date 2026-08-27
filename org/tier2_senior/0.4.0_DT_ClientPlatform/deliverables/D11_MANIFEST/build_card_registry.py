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
# ⛔ STRUCTURED, NOT PROSE. The prior revision put the admission predicate, the blockage
# census, the contract gap and the transform lifecycle in ONE free-text string, so no consumer
# could branch on any of them and no two could move separately -- Rule 24 (iii) inside the
# artifact that governs admission. Four independent axes now, each with its own field.
RECEIVERS = {
    "grain": {
        "required_fields": ["trust.grain.unit", "trust.grain.basis", "trust.grain.evidence",
                            "trust.grain.owner"],
        "blocking_layers": ["source", "registry", "transform", "compiler"],
        "source_gap_kind": "no_authored_projection",
        "source_gap_detail": ("no card in the estate authors a grain projection, admitted or "
                              "not; measured by 1.0.0_SA_CTO~X over the 23 exact-match cards"),
    },
    "key": {
        "required_fields": ["trust.key.identity_space", "trust.key.key_expression",
                            "trust.key.key_is_stable", "trust.key.crosses_spaces",
                            "trust.key.declared_mapping", "trust.key.basis",
                            "trust.key.evidence", "trust.key.owner"],
        "blocking_layers": ["source", "registry", "transform", "compiler"],
        "source_gap_kind": "no_field_in_card_contract",
        "source_gap_detail": ("SUBSTRATE_CARD.v2 trust.key carries seven of these eight and has "
                              "NO key_expression field -- every property of the key, never the key"),
    },
    "failure_mode": {
        "required_fields": ["trust.failure_mode.returns_on_failure",
                            "trust.failure_mode.distinguishable_from_true_negative",
                            "trust.failure_mode.silent_degrade_paths",
                            "trust.failure_mode.basis", "trust.failure_mode.evidence",
                            "trust.failure_mode.owner"],
        "blocking_layers": ["registry", "transform", "compiler"],
        "source_gap_kind": "none",
        "source_gap_detail": ("payloads satisfying this EXIST outside the admitted population; "
                              "this is the one receiver with no source-level gap"),
    },
}


def git_blob_id(rel: str) -> str:
    """⛔ NOT sha256 OF THE WORKING-TREE BYTES. That is what the prior revision pinned, and 9 of
    13 members failed against Git-object bytes -- the CRLF/LF boundary on a Windows checkout, in
    the field whose entire job is identity. `git hash-object` applies the repo's own filters, so
    the pin and the later check are computed identically."""
    r = subprocess.run(["git", "hash-object", "--", rel], cwd=WS,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("REFUSING -- git hash-object failed for %r: %s" % (rel, r.stderr[:120]))
    return r.stdout.strip()


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
    return {"path": rel(path), "git_blob_id": git_blob_id(rel(path)),
            "subject_id": subject}


def candidate_set_digest() -> str:
    """sha256 over the sorted `path\\x00blob` lines of every candidate the globs match.

    Binds the ratification to the SET IT SAW. `ratified_at_commit` alone names a moment and says
    nothing about what was in front of the ratifier -- two different candidate sets at one commit
    are indistinguishable, and "ratified at HEAD" would be true of both.
    """
    lines = []
    for p in discover():
        r = rel(p)
        lines.append(r + chr(0) + git_blob_id(r))
    return hashlib.sha256(chr(10).join(sorted(lines)).encode("utf-8")).hexdigest()


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
        "candidate_set_digest": candidate_set_digest(),
        "ratified_discovery_globs": list(DISCOVERY_GLOBS),
        "discovery_globs": list(DISCOVERY_GLOBS),
        "extension_population": {"members": members},
        "receiver_source_populations": {
            r: {"members": [],
                # ⛔ transform STATUS and transform REFERENCE are two axes. The prior single
                # `transform_version` string conflated a lifecycle claim with an identity claim
                # and accepted an arbitrary `v7` that named nothing.
                "transform_status": "absent",
                "transform_reference": None,
                "admission_predicate": {
                    "required_fields": cfg["required_fields"],
                    "basis_allowed": ["measured", "held", "inferred"],
                    "all_non_blank": True},
                "blocking_layers": cfg["blocking_layers"],
                "source_gap": {"kind": cfg["source_gap_kind"],
                               "detail": cfg["source_gap_detail"]}}
            for r, cfg in RECEIVERS.items()
        },
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
        elif git_blob_id(path) != m["git_blob_id"]:
            drifted.append(path)
    print("admitted but MISSING     : %d %s" % (len(missing), missing))
    print("admitted but BLOB DRIFT: %d %s" % (len(drifted), drifted))
    if errs or missing or drifted:
        sys.exit(1)


if __name__ == "__main__":
    main()
