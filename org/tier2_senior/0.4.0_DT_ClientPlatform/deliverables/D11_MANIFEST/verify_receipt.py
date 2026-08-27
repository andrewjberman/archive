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
from datetime import datetime, timezone
import sys

from jsonschema import Draft202012Validator

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST")
SCHEMA = os.path.join(HERE, "MANIFEST_RECEIPT.v1.schema.json")


def _no_dupes(pairs):
    """⛔ THE VERIFIER USED json.load, WHICH IS LAST-WINS -- so an invalid-first/valid-last
    duplicate key COLLAPSED and this module returned ZERO findings on a document carrying a
    forgery. The compiler had this guard; the thing that checks the compiler's output did not."""
    seen = set()
    for k, _val in pairs:
        if k in seen:
            raise SystemExit("REFUSING TO PARSE -- duplicate JSON object key %r" % k)
        seen.add(k)
    return dict(pairs)


def load_json_strict(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh, object_pairs_hook=_no_dupes)


def canonical_mismatch(rel: str):
    """⛔ `ORG/...` RESOLVES TO THE SAME BLOB AS `org/...` ON THIS DEVICE -- measured, rc=0.
    A case alias is a second spelling of one location, and every digest check agrees across it,
    so nothing downstream can tell them apart. Compare each segment against what the directory
    actually holds."""
    cur = WS
    for seg in rel.split("/"):
        try:
            entries = os.listdir(cur)
        except OSError:
            return None
        if seg not in entries:
            match = [e for e in entries if e.lower() == seg.lower()]
            if match:
                return "%s (on disk: %s)" % (seg, match[0])
            return None
        cur = os.path.join(cur, seg)
    return None


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


def verify(receipt: dict, actual_home: str = None) -> list:
    """Findings. EMPTY means every pin re-derived to the value it claims.

    `actual_home` is the repo-relative path the document was READ FROM. ⛔ WITHOUT IT A
    SCHEMA-VALID RECEIPT SITTING AT A FAKE PATH EXITS 0 -- the document declares where it lives
    and nothing compared that to where it was found, so `exact_home` was a self-report checked
    against itself.
    """
    out = []

    def bad(where, msg):
        out.append("%s: %s" % (where, msg))

    errs = list(Draft202012Validator(load_json_strict(SCHEMA)).iter_errors(receipt))
    for e in errs:
        bad("schema/" + "/".join(str(x) for x in e.path), e.message[:110])
    if errs:
        return out          # a document that does not validate cannot be pin-checked coherently

    if actual_home is not None and actual_home != receipt["exact_home"]:
        bad("exact_home", "declares %s but was READ FROM %s -- a declared home checked against "
                          "nothing is a self-report" % (receipt["exact_home"], actual_home))

    # ---- ⛔ THE UTC PATTERN IS A SHAPE, NOT A CALENDAR --------------------------------
    # `2026-13-45T99:99:99Z` matched the regex. Digit counts and separators say nothing about
    # whether an instant EXISTS, and every ordering comparison downstream is string-based, so an
    # impossible date sorts perfectly well against a real one.
    for _field, _val in (("source_snapshot_utc", receipt["source_snapshot_utc"]),
                         ("executed_utc", receipt["executed_utc"]),
                         ("input_closure.source_snapshot_pin.value_utc",
                          receipt["input_closure"]["source_snapshot_pin"]["value_utc"])):
        try:
            datetime.strptime(_val, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            bad(_field, "%r matches the pattern and is NOT A REAL INSTANT" % _val)
    for _e in receipt["replay"]["emissions"]:
        try:
            datetime.strptime(_e["executed_utc"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            bad("replay.emissions", "%r is not a real instant" % _e["executed_utc"])

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
    # ⛔ `receipt_schema` WAS ADDED TO THE CONTRACT AND THE EMITTER AND NOT TO THIS LOOP -- so
    # the governing contract was pinned and never checked. A field needs a whole PATH, not a
    # slot: schema, emitter, AND the code that assigns the verdict. My own baseline arm caught
    # it by comparing the verifier's findings against the tree's dirty set.
    for name in ("receipt_schema", "compiler", "registry", "registry_schema", "base39",
                 "card_part_map", "card_schema"):
        pin = clo[name]
        got = blob_of(pin["home"])
        if got is None:
            bad("input_closure.%s" % name, "MISSING at %s" % pin["home"])
        elif got != pin["git_blob_id"]:
            bad("input_closure.%s" % name,
                "blob claimed %s, tree has %s" % (pin["git_blob_id"][:12], got[:12]))
        # ⛔ A COMMIT BESIDE A BLOB IS TWO UNRELATED CLAIMS UNTIL SOMETHING BINDS THEM. Checking
        # only the blob let a FORGED COMMIT ride along clean. Two checks: the commit must exist,
        # and `commit:path` must resolve to the blob the receipt claims.
        alias = canonical_mismatch(pin["home"])
        if alias:
            bad("input_closure.%s" % name,
                "PATH CASE ALIAS -- claimed %r but the filesystem holds %s; two spellings of "
                "one location and every digest agrees across both" % (pin["home"], alias))
        # ⛔ BOTH DIRECTIONS. The first version checked only the over-claim (in_object_db on an
        # absent object) and my own control caught the asymmetry the moment the tree went clean:
        # claiming `computed_only` for a blob git DOES hold is also false, and an asymmetric
        # check is one that reports a field as verified while half its domain is unexamined.
        if got:
            present = subprocess.run(["git", "cat-file", "-e", got], cwd=WS,
                                     capture_output=True).returncode == 0
            measured = "in_object_db" if present else "computed_only"
            if pin["blob_presence"] != measured:
                bad("input_closure.%s" % name,
                    "claims blob_presence=%s but %s is measurably %s"
                    % (pin["blob_presence"], got[:12], measured))
        commit = pin["commit"]
        if subprocess.run(["git", "cat-file", "-e", commit + "^{commit}"], cwd=WS,
                          capture_output=True).returncode != 0:
            bad("input_closure.%s" % name, "commit %s names no object" % commit[:12])
        else:
            at = subprocess.run(["git", "rev-parse", "%s:%s" % (commit, pin["home"])], cwd=WS,
                                capture_output=True, text=True)
            resolved = at.stdout.strip() if at.returncode == 0 else None
            if resolved is None:
                bad("input_closure.%s" % name,
                    "%s does not exist at commit %s" % (pin["home"], commit[:12]))
            elif resolved != pin["git_blob_id"]:
                bad("input_closure.%s" % name,
                    "commit %s resolves %s to %s, receipt claims %s"
                    % (commit[:12], pin["home"], resolved[:12], pin["git_blob_id"][:12]))

    # ---- the admitted-card closure MUST equal the registry's own population ----------
    # ⛔ THE REGISTRY BLOB PINS THE LIST; THIS PINS WHAT THE LIST RESOLVED TO. A correct
    # registry can name a card whose bytes moved, so agreeing on the registry is not agreeing
    # on the cards -- and the v0 receipt pinned neither.
    reg_home = clo["registry"]["home"]
    try:
        reg = load_json_strict(os.path.join(WS, reg_home))
        declared = {(m["path"], m["subject_id"], m["git_blob_id"])
                    for m in reg["extension_population"]["members"]}
    except Exception as exc:                      # noqa: BLE001 - reported, never swallowed
        declared = None
        bad("input_closure.registry", "unreadable (%s)" % type(exc).__name__)
    if declared is not None:
        # ⛔ MULTIPLICITY IS PART OF THE CLAIM. A SET comparison is blind to a duplicated
        # entry -- adding a card twice leaves the set identical -- so a receipt claiming to have
        # read one card twice was clean. Counted, then compared.
        rows = [(c["path"], c["subject_id"], c["git_blob_id"]) for c in clo["admitted_cards"]]
        if len(rows) != len(set(rows)):
            dupes = sorted({r[0] for r in rows if rows.count(r) > 1})
            bad("input_closure.admitted_cards",
                "DUPLICATE entries (%d rows, %d distinct): %s" % (len(rows), len(set(rows)), dupes))
        claimed = set(rows)
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

    # ---- blob_presence, MEASURED FOR EVERY PINNED IDENTITY, BOTH DIRECTIONS ----------
    # It was checked on the six input roles and NOT on `describes` or on any admitted card, so a
    # flipped presence on either was clean. An unmeasured field beside measured ones reads as
    # covered by the same rigour.
    def _presence(blob):
        ok = subprocess.run(["git", "cat-file", "-e", blob], cwd=WS,
                            capture_output=True).returncode == 0
        return "in_object_db" if ok else "computed_only"

    if d["git_blob_id"]:
        m = _presence(d["git_blob_id"])
        if d["blob_presence"] != m:
            bad("describes.blob_presence",
                "claims %s but %s is measurably %s" % (d["blob_presence"],
                                                       d["git_blob_id"][:12], m))
    for c in clo["admitted_cards"]:
        m = _presence(c["git_blob_id"])
        if c["blob_presence"] != m:
            bad("input_closure.admitted_cards",
                "%s claims blob_presence=%s but %s is measurably %s"
                % (c["path"], c["blob_presence"], c["git_blob_id"][:12], m))

    # ---- THE SNAPSHOT IS RE-DERIVED, NOT ACCEPTED ------------------------------------
    # An arbitrary EARLIER legal instant validated -- correct format, correct ordering against a
    # forged execution time, and derived from nothing. A deterministic value that is not
    # re-derived is a free string wearing a timestamp's shape.
    # ⛔ `schema_commit` MAPPED TO card_schema WHILE THE EMITTER MEANT THE OUTPUT SCHEMA --
    # one ambiguous token for two different contracts, silently reading the wrong one. Each
    # schema now has its own token and its own role.
    _role_of = {"registry_ratified_commit": "registry",
                "output_schema_commit": "output_schema",
                "card_schema_commit": "card_schema",
                "compiler_commit": "compiler",
                "receipt_schema_commit": "receipt_schema"}
    times = []
    for token in clo["source_snapshot_pin"]["derived_from"]:
        pin = clo.get(_role_of[token])
        if not pin:
            continue
        r = subprocess.run(["git", "show", "-s", "--format=%cI", pin["commit"]], cwd=WS,
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            times.append(datetime.fromisoformat(r.stdout.strip()).astimezone(
                timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    if times:
        expect = max(times)
        if receipt["source_snapshot_utc"] != expect:
            bad("source_snapshot_utc",
                "claims %s but the pinned commits derive %s" % (receipt["source_snapshot_utc"],
                                                                expect))
    else:
        bad("source_snapshot_utc", "no pinned commit yielded a time; the value is underived")

    # ---- exact_home's QUALIFIER IS BOUND TO THE SNAPSHOT ------------------------------
    # Changing only the qualifier was accepted: the pattern matched, and nothing tied the
    # timestamp in the filename to the timestamp in the document.
    # ⛔ BOUND TO THE RUN, NOT THE CLOSURE. This check compared against source_snapshot_utc
    # while the emitter moved to executed_utc -- and I changed the producer without changing the
    # consumer, which is the whole-path defect one file over from where I had just fixed it.
    want_q = receipt["executed_utc"].replace("-", "").replace(":", "")
    if not receipt["exact_home"].endswith(".%s.receipt.json" % want_q):
        bad("exact_home",
            "qualifier does not match executed_utc (%s); a run-qualified home whose qualifier "
            "is free is a second, unbindable clock" % want_q)

    # ---- the two clocks must not collapse -------------------------------------------
    # ⛔ EQUALITY IS THE TELL, NOT A COINCIDENCE. A deterministic snapshot derived from commit
    # times and a real execution clock agreeing to the second means one was copied from the
    # other, which is how the v0 compiler bought "determinism" with a frozen clock reading.
    # ⛔ STRICTLY LATER, not merely different. Equality is collapse; EARLIER is worse -- a
    # receipt whose execution precedes its source snapshot claims to have compiled inputs that
    # did not yet exist, and that ordering validated until now.
    if receipt["executed_utc"] <= receipt["source_snapshot_utc"]:
        bad("clocks", "executed_utc %s is NOT STRICTLY LATER than source_snapshot_utc %s -- the "
                      "run claims to precede or coincide with the inputs it compiled"
                      % (receipt["executed_utc"], receipt["source_snapshot_utc"]))
    # ⛔ AND THE REPLAY CLAIM MUST BE INDEPENDENTLY CHECKABLE. Digests belonging to nothing made
    # a two-emission claim unfalsifiable; the described artifact's own digest must be among them.
    # ---- THE REPLAY STATE IS DERIVED FROM THE EVIDENCE, NOT READ BESIDE IT ------------
    # A count and a digest set could not prove each other: a forged `byte_identical / 2` carried
    # no second emission, and `byte_different` could claim more distinct digests than emissions.
    # Both are now arithmetic over the per-emission array, which the document must carry.
    rep = receipt["replay"]
    ems = rep["emissions"]
    digests = {e["digest"] for e in ems}
    if receipt["describes"]["sha256"] not in digests:
        bad("replay.emissions",
            "the described artifact's digest %s is NOT among the emissions -- the comparison "
            "claim references nothing this receipt describes"
            % receipt["describes"]["sha256"][:12])
    seqs = sorted(e["sequence"] for e in ems)
    if seqs != list(range(1, len(ems) + 1)):
        bad("replay.emissions", "sequences are not 1..%d: %s" % (len(ems), seqs))
    derived = ("not_performed" if len(ems) < 2
               else "byte_identical" if len(digests) == 1 else "byte_different")
    if rep["comparison_state"] != derived:
        bad("replay.comparison_state",
            "claims %s but %d emission(s) carrying %d distinct digest(s) derive %s"
            % (rep["comparison_state"], len(ems), len(digests), derived))
    if receipt["input_closure"]["source_snapshot_pin"]["value_utc"] != receipt["source_snapshot_utc"]:
        bad("clocks", "source_snapshot_pin.value_utc disagrees with source_snapshot_utc")
    if not receipt["input_closure"]["complete"]:
        bad("input_closure.complete", "the closure declares itself INCOMPLETE")
    return out


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "graph_object_manifest.receipt.json")
    # ⛔ THE ENTRY POINT MUST USE THE STRICT LOADER. It called json.load while the helper
    # beside it was strict, so the ACTUAL CLI path swallowed a duplicate key and returned
    # rc=0 / findings=0 on a forged document. A protection the entry point does not call is a
    # protection that exists only in a function.
    receipt = load_json_strict(path)
    findings = verify(receipt, actual_home=os.path.relpath(path, WS).replace(os.sep, "/"))
    print("receipt   : %s" % os.path.relpath(path, WS).replace(os.sep, "/"))
    print("findings  : %d" % len(findings))
    for f in findings:
        print("    %s" % f)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
