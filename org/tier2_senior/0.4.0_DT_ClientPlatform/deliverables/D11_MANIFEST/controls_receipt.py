#!/usr/bin/env python3
"""EXECUTABLE controls for the governed receipt -- 4.0.0_SA_CRO~A's tranche, Base rework 2 and
its addendum.

Eleven schema-valid verifier-clean mutants were found in the prior revision, and four more
requirements followed. THE COMMON ROOT OF ALL OF THEM WAS ONE THING: THE SHAPE WAS BOUND AND THE
DOMAIN WAS NOT. Every arm below exists because a well-formed lie passed.

⛔ NO COMPILE IS RUN. The fixture comes from the emitter's OWN `build_receipt()`, called directly
-- a hand-copied fixture stops matching the emitter the moment either moves, which is the
typed-beside-derived defect wearing a test's costume.

⛔ EVERY MUTANT IS PROVEN NON-INERT before its result is read. A mutation control that mutates
nothing tests nothing, and it fails OPEN on any arm expecting a rejection.

    python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/controls_receipt.py
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

from jsonschema import Draft202012Validator

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)        # module level only -- main() is NEVER called
    return mod


l0 = _load("l0_compile_w3", os.path.join(HERE, "l0_compile_w3.py"))
vr = _load("verify_receipt", os.path.join(HERE, "verify_receipt.py"))

with open(os.path.join(HERE, "MANIFEST_RECEIPT.v1.schema.json"), encoding="utf-8") as _fh:
    SCHEMA = json.load(_fh)
V = Draft202012Validator(SCHEMA)

CHECKS: list = []
FAILURES: list = []


def check(label: str, ok: bool, detail: str = "") -> None:
    CHECKS.append(label)
    print("  %-58s %s" % (label, "PASS" if ok else "*** FAIL ***"))
    if detail:
        print("      %s" % detail)
    if not ok:
        FAILURES.append(label)


print("=" * 84)
print("SCHEMA META-VALIDATION AND THE BASELINE FIXTURE")
print("=" * 84)
Draft202012Validator.check_schema(SCHEMA)
check("MANIFEST_RECEIPT.v1 meta-validates", True)

ART = os.path.join(HERE, "graph_object_manifest.json")
BASE = l0.build_receipt(ART, "2026-08-27T11:27:48Z", reg=l0.load_registry())
BASE_BYTES = json.dumps(BASE, sort_keys=True)
check("the emitter's OWN build_receipt() output validates",
      len(list(V.iter_errors(BASE))) == 0,
      "%d errors" % len(list(V.iter_errors(BASE))))

# ⛔ THE BASELINE ARM ASSERTS DISCRIMINATION, NOT ZERO. "0 findings" is only true when every
# pinned input is committed; under an edited-but-uncommitted compiler the verifier CORRECTLY
# reports a commit:path mismatch. An arm demanding zero would have forced me to weaken the
# verifier or to commit before the suite passed -- both are the tail wagging the dog.
ROLES = ("compiler", "registry", "registry_schema", "base39", "card_part_map", "card_schema")
dirty = set()
for r in ROLES:
    pin = BASE["input_closure"][r]
    at = subprocess.run(["git", "rev-parse", "%s:%s" % (pin["commit"], pin["home"])],
                        cwd=WS, capture_output=True, text=True)
    if at.stdout.strip() != pin["git_blob_id"]:
        dirty.add(r)
findings = vr.verify(BASE)
reported = {f.split(":")[0] for f in findings}
check("the verifier's findings are EXACTLY the tree's dirty inputs",
      reported == {"input_closure.%s" % r for r in dirty},
      "dirty: %s | reported: %s -- EQUALITY is the claim, and it holds in both tree states"
      % (sorted(dirty) or "none", sorted(reported) or "none"))
check("and every finding is a commit:path binding, nothing else",
      all(f.startswith("input_closure.") for f in findings),
      "%d findings" % len(findings))

print()
print("=" * 84)
print("REQUIRED NEGATIVES -- the eleven, plus the addendum's four")
print("=" * 84)


def mutate(label, fn, *, expect_schema=False):
    d = copy.deepcopy(BASE)
    fn(d)
    if json.dumps(d, sort_keys=True) == BASE_BYTES:
        check(label, False, "*** INERT MUTATION -- this control would have tested nothing ***")
        return
    n_schema = len(list(V.iter_errors(d)))
    if expect_schema:
        check(label, n_schema > 0, "%d schema errors -- rejected by the contract" % n_schema)
        return
    # ⛔ COMPARE WHOLE FINDINGS, NOT THEIR KEYS. Filtering by key suppressed a REAL detection on
    # any role the tree already reports dirty -- so "forged compiler commit" and "blob_presence
    # flipped" both read as undetected when the compiler happened to be uncommitted. A control
    # that cannot fire because of unrelated tree state is worse than no control.
    extra = [f for f in vr.verify(d) if f not in findings]
    check(label, len(extra) > 0,
          "%d schema errors (contract cannot see it) / %d NEW verifier findings: %s"
          % (n_schema, len(extra), extra[0][:90] if extra else "-"))


# --- the original six -------------------------------------------------------------
mutate("a MISSING LIFECYCLE AXIS (mutation_policy dropped)",
       lambda d: d.pop("mutation_policy"), expect_schema=True)
mutate("a MISSING GOVERNING SCHEMA", lambda d: d.pop("governing_schema"), expect_schema=True)
mutate("a WRONG REGISTRY BLOB",
       lambda d: d["input_closure"]["registry"].__setitem__("git_blob_id", "a" * 40))
mutate("an INCOMPLETE admitted-card closure (one card dropped)",
       lambda d: d["input_closure"]["admitted_cards"].pop())
mutate("a WRONG ARTIFACT DIGEST", lambda d: d["describes"].__setitem__("sha256", "c" * 64))
mutate("SOURCE/EXECUTION TIME COLLAPSE (the two clocks equal)",
       lambda d: d.__setitem__("executed_utc", d["source_snapshot_utc"]))

# --- the eleven Base rework 2 found -----------------------------------------------
mutate("1. null describes.git_blob_id",
       lambda d: d["describes"].__setitem__("git_blob_id", None), expect_schema=True)
mutate("2. a WRONG governing_schema.home",
       lambda d: d["governing_schema"].__setitem__("home", "org/standards/SOMETHING.json"),
       expect_schema=True)
mutate("3. a WRONG exact_home",
       lambda d: d.__setitem__("exact_home", "org/x/elsewhere.receipt.json"), expect_schema=True)
mutate("4. a DUPLICATED admitted card (set comparison is blind to it)",
       lambda d: d["input_closure"]["admitted_cards"].append(
           copy.deepcopy(d["input_closure"]["admitted_cards"][0])), expect_schema=True)
mutate("5. the BASE39 ROLE carrying the REGISTRY's pin",
       lambda d: d["input_closure"].__setitem__(
           "base39", copy.deepcopy(d["input_closure"]["registry"])), expect_schema=True)
mutate("6. a FORGED compiler commit",
       lambda d: d["input_closure"]["compiler"].__setitem__("commit", "d" * 40))
mutate("7. a FORGED two-emission replay claim",
       lambda d: d.__setitem__("replay", {"comparison_state": "byte_identical",
                                          "emissions_compared": 2,
                                          "observed_digests": ["e" * 64]}))
mutate("8. EXECUTION BEFORE the source snapshot",
       lambda d: d.__setitem__("executed_utc", "2026-01-01T00:00:00Z"))
mutate("9. a HAND-AUTHORED same-run receipt",
       lambda d: d.__setitem__("authorship_mode", "hand_authored"), expect_schema=True)
mutate("10. a RECONSTRUCTED relationship carrying same-run execution claims",
       lambda d: d["describes"].__setitem__("relationship", "reconstructed"), expect_schema=True)
mutate("11. a snapshot derivation OMITTING the schema commit",
       lambda d: d["input_closure"]["source_snapshot_pin"].__setitem__(
           "derived_from", ["registry_ratified_commit", "compiler_commit"]), expect_schema=True)

# --- the addendum's four ------------------------------------------------------------
print()
print("  ADDENDUM (all four confirmed on my own artifacts BEFORE implementing)")


def raw(label, text, want_refuse=True):
    """RAW BYTES through the verifier's own loader -- the only way to test duplicate keys,
    which no in-memory dict can represent."""
    fd, p = tempfile.mkstemp(suffix=".json", prefix="rcpt_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        refused = False
        try:
            vr.load_json_strict(p)
        except SystemExit:
            refused = True
        check(label, refused == want_refuse,
              "the VERIFIER's own loader %s it" % ("refused" if refused else "ACCEPTED"))
    finally:
        os.remove(p)


raw("A. invalid-first/valid-last authority_role -> verifier loader REFUSES",
    '{"authority_role": "authority", "authority_role": "evidence"}')
raw("   POSITIVE CONTROL: a clean two-key document parses", '{"a": 1, "b": 2}', want_refuse=False)

mutate("B. a WINDOWS CASE ALIAS in a pinned home (ORG/...)",
       lambda d: d["input_closure"]["card_part_map"].__setitem__(
           "home", d["input_closure"]["card_part_map"]["home"].replace("org/", "ORG/", 1)),
       expect_schema=True)
ALIAS = BASE["input_closure"]["card_part_map"]["home"].replace("D11_MANIFEST", "d11_manifest", 1)
check("   the alias resolves to the SAME blob (why exact case must be bound)",
      vr.blob_of(ALIAS) == BASE["input_closure"]["card_part_map"]["git_blob_id"],
      "every digest check agrees across it, so nothing downstream can tell them apart")
check("   canonical_mismatch() DETECTS it", vr.canonical_mismatch(ALIAS) is not None,
      vr.canonical_mismatch(ALIAS) or "-")

check("C. the receipt home is RUN-QUALIFIED, not one fixed overwritable path",
      BASE["exact_home"].endswith(".receipt.json")
      and "graph_object_manifest.receipt.json" not in BASE["exact_home"],
      BASE["exact_home"].rsplit("/", 1)[-1])
mutate("   the OLD fixed home (immutable yet overwritable)",
       lambda d: d.__setitem__(
           "exact_home", "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/"
                         "graph_object_manifest.receipt.json"), expect_schema=True)

_p = BASE["input_closure"]["compiler"]
check("D. blob_presence is MEASURED, not assumed (%s)" % _p["blob_presence"],
      _p["blob_presence"] in ("in_object_db", "computed_only"),
      "a `git hash-object` id for an uncommitted file names NO OBJECT -- correct arithmetic, "
      "resolvable by nobody, and indistinguishable from a real one by shape")
mutate("   blob_presence FLIPPED against the measured truth",
       lambda d: d["input_closure"]["compiler"].__setitem__(
           "blob_presence",
           "computed_only" if _p["blob_presence"] == "in_object_db" else "in_object_db"))

print()
print("  THE REPLAY STATE -- every arm, because a clause that cannot be satisfied is a defect")
for label, rep, want_ok in [
        ("not_performed / 1 emission / 1 digest (the honest single run)",
         {"comparison_state": "not_performed", "emissions_compared": 1,
          "observed_digests": [BASE["describes"]["sha256"]]}, True),
        ("byte_identical / 2 emissions / 1 digest",
         {"comparison_state": "byte_identical", "emissions_compared": 2,
          "observed_digests": [BASE["describes"]["sha256"]]}, True),
        ("byte_different / 2 emissions / 2 digests (drift must be expressible)",
         {"comparison_state": "byte_different", "emissions_compared": 2,
          "observed_digests": [BASE["describes"]["sha256"], "f" * 64]}, True),
        ("byte_identical claimed on ONE emission",
         {"comparison_state": "byte_identical", "emissions_compared": 1,
          "observed_digests": [BASE["describes"]["sha256"]]}, False),
        ("not_performed claiming TWO emissions",
         {"comparison_state": "not_performed", "emissions_compared": 2,
          "observed_digests": [BASE["describes"]["sha256"]]}, False),
        ("byte_different with only ONE digest",
         {"comparison_state": "byte_different", "emissions_compared": 2,
          "observed_digests": [BASE["describes"]["sha256"]]}, False)]:
    d = copy.deepcopy(BASE)
    d["replay"] = rep
    n = len(list(V.iter_errors(d)))
    check(label, (n == 0) == want_ok,
          "%d errors, expected %s" % (n, "accept" if want_ok else "reject"))

print()
print("=" * 84)
print("THE REPAIRED DUPLICATE-KEY FIXTURE (stale under rework18)")
print("=" * 84)
# ⛔ THE OLD FIXTURE'S SURVIVING VALUE OMITTED `condition`, which rework18 made REQUIRED under
# mint=conditional. So the "valid last" value was NOT schema-valid and the control proved only
# that a duplicate was refused -- never that the survivor would have passed.
VALID_LAST = ('{"variant_suffixes": {'
              '".wal": {"mint": "banana", "note": ""}, '
              '".wal": {"mint": "conditional", "note": "write-ahead log", '
              '"condition": "present mid-flight, absent after a clean checkpoint"}}}')
survivor = json.loads(VALID_LAST)["variant_suffixes"][".wal"]
with open(os.path.join(WS, "org/standards/L0_GRAPH_SUBSTRATE_MANIFEST.schema.json"),
          encoding="utf-8") as _fh:
    L0 = json.load(_fh)
# A SUB-SCHEMA LIFTED OUT OF ITS DOCUMENT LOSES ITS $refs -- carrying $defs is what resolves them.
_frag = L0["$defs"]["part"]["properties"]["member_set"]["properties"]["variant_suffixes"][
    "additionalProperties"]
VS = Draft202012Validator({**_frag, "$defs": L0["$defs"]})
check("the SURVIVING (last) value is schema-valid under rework18",
      len(list(VS.iter_errors(survivor))) == 0,
      "it carries `condition`; the stale fixture omitted it and was therefore invalid")
check("the DISCARDED (first) value is schema-INVALID",
      len(list(VS.iter_errors({"mint": "banana", "note": ""}))) > 0,
      "so invalid-first / valid-last is the ordering where the document passes and the rejected "
      "value is the one a reviewer would have caught")
fd, p = tempfile.mkstemp(suffix=".json", prefix="dup_")
try:
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(VALID_LAST)
    refused = False
    try:
        l0.load_json_strict(p)
    except SystemExit:
        refused = True
    check("invalid-first / SCHEMA-VALID-last -> strict loader REFUSES", refused,
          "plain json.load returns the valid survivor and hides the invalid first")
finally:
    os.remove(p)

print()
print("=" * 84)
if FAILURES:
    print("RESULT: %d of %d controls FAILED: %s" % (len(FAILURES), len(CHECKS), FAILURES))
    sys.exit(1)
print("RESULT: all %d controls PASS -- DENOMINATOR COUNTED, NOT ASSERTED. (I reported 21 last "
      "time and 4.0.0_SA_CRO~A counted 22; a figure about my own work is the one population no "
      "external check covers.) NO compile run, no receipt on disk touched." % len(CHECKS))
