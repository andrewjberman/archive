#!/usr/bin/env python3
"""THE CONSUMING HALF OF THE RECEIPT CONTRACT.

A schema can check that a pin is a 40-hex string. It cannot check that the pin is the RIGHT
40-hex string, and that gap is exactly where the v0 receipt lived: nine well-formed keys, none
of them compared against anything. ⛔ AN UNVERIFIED PIN IS A DECORATION WITH A CHECKSUM'S SHAPE.

This module validates a receipt against its governing schema AND re-derives every pin from the
tree. It reads only; it never runs the compiler, never emits a manifest, and never edits a
receipt.

    python .../verify_receipt.py [path-to-receipt]
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

from jsonschema import Draft202012Validator

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST")
SCHEMA = os.path.join(HERE, "MANIFEST_RECEIPT.v1.schema.json")


def blob_of(rel: str):
    """git hash-object, so the pin and the check cross the SAME filters. Hashing the bytes on
    disk with sha256 is what put 9 of 13 registry pins on the wrong side of CRLF."""
    r = subprocess.run(["git", "hash-object", "--", rel], cwd=WS,
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def sha256_of(rel: str):
    p = os.path.join(WS, rel)
    if not os.path.exists(p):
        return None
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def verify(receipt: dict) -> list:
    """Return a list of findings. EMPTY means every pin re-derived to the value it claims."""
    out = []

    def bad(where, msg):
        out.append("%s: %s" % (where, msg))

    with open(SCHEMA, encoding="utf-8") as fh:
        errs = list(Draft202012Validator(json.load(fh)).iter_errors(receipt))
    for e in errs:
        bad("schema/" + "/".join(str(x) for x in e.path), e.message[:110])
    if errs:
        return out          # a document that does not validate cannot be pin-checked coherently

    # ---- the described artifact -----------------------------------------------------
    d = receipt["describes"]
    got = sha256_of(d["home"])
    if got is None:
        bad("describes.home", "artifact MISSING at %s" % d["home"])
    elif got != d["sha256"]:
        bad("describes.sha256", "claimed %s, artifact hashes %s" % (d["sha256"][:12], got[:12]))
    if d.get("git_blob_id") is not None and blob_of(d["home"]) != d["git_blob_id"]:
        bad("describes.git_blob_id", "claimed %s, tree has %s"
            % (d["git_blob_id"][:12], (blob_of(d["home"]) or "-")[:12]))

    # ---- every pinned input ---------------------------------------------------------
    clo = receipt["input_closure"]
    for name in ("compiler", "registry", "registry_schema", "base39", "card_part_map",
                 "card_schema"):
        pin = clo[name]
        got = blob_of(pin["home"])
        if got is None:
            bad("input_closure.%s" % name, "MISSING at %s" % pin["home"])
        elif got != pin["git_blob_id"]:
            bad("input_closure.%s" % name,
                "blob claimed %s, tree has %s" % (pin["git_blob_id"][:12], got[:12]))

    # ---- the admitted-card closure MUST equal the registry's own population ----------
    # ⛔ THE REGISTRY BLOB PINS THE LIST; THIS PINS WHAT THE LIST RESOLVED TO. A correct
    # registry can name a card whose bytes moved, so agreeing on the registry is not agreeing
    # on the cards -- and the v0 receipt pinned neither.
    reg_home = clo["registry"]["home"]
    try:
        with open(os.path.join(WS, reg_home), encoding="utf-8") as fh:
            reg = json.load(fh)
        declared = {(m["path"], m["subject_id"], m["git_blob_id"])
                    for m in reg["extension_population"]["members"]}
    except Exception as exc:                      # noqa: BLE001 - reported, never swallowed
        declared = None
        bad("input_closure.registry", "unreadable (%s)" % type(exc).__name__)
    if declared is not None:
        claimed = {(c["path"], c["subject_id"], c["git_blob_id"])
                   for c in clo["admitted_cards"]}
        if claimed != declared:
            bad("input_closure.admitted_cards",
                "INCOMPLETE CLOSURE -- %d claimed vs %d in the registry; missing %d, extra %d"
                % (len(claimed), len(declared),
                   len(declared - claimed), len(claimed - declared)))
        for c in clo["admitted_cards"]:
            got = blob_of(c["path"])
            if got is not None and got != c["git_blob_id"]:
                bad("input_closure.admitted_cards",
                    "%s blob claimed %s, tree has %s"
                    % (c["path"], c["git_blob_id"][:12], got[:12]))

    # ---- the two clocks must not collapse -------------------------------------------
    # ⛔ EQUALITY IS THE TELL, NOT A COINCIDENCE. A deterministic snapshot derived from commit
    # times and a real execution clock agreeing to the second means one was copied from the
    # other, which is how the v0 compiler bought "determinism" with a frozen clock reading.
    if receipt["source_snapshot_utc"] == receipt["executed_utc"]:
        bad("clocks", "source_snapshot_utc == executed_utc -- the two have COLLAPSED; a "
                      "deterministic pin and a per-run clock cannot legitimately coincide")
    if receipt["input_closure"]["source_snapshot_pin"]["value_utc"] != receipt["source_snapshot_utc"]:
        bad("clocks", "source_snapshot_pin.value_utc disagrees with source_snapshot_utc")
    if not receipt["input_closure"]["complete"]:
        bad("input_closure.complete", "the closure declares itself INCOMPLETE")
    return out


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "graph_object_manifest.receipt.json")
    with open(path, encoding="utf-8") as fh:
        receipt = json.load(fh)
    findings = verify(receipt)
    print("receipt   : %s" % os.path.relpath(path, WS).replace(os.sep, "/"))
    print("findings  : %d" % len(findings))
    for f in findings:
        print("    %s" % f)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
