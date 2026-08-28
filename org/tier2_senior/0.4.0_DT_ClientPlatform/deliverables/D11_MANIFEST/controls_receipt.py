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

# ---- NO-DEBRIS: SUPPRESSION FIRST, THEN THE BASELINE, BOTH BEFORE ANY LOCAL LOAD -------------
# WARN: THE PREVIOUS NO-DEBRIS ARM WAS SELF-BLIND AND I WROTE IT. Its baseline was taken at the
# arm itself, ~440 lines below -- AFTER the `_load()` calls had already written __pycache__ into
# HERE. So the "pre" listing ALREADY CONTAINED THE DEBRIS THE HARNESS ITSELF CREATED, and the arm
# reported NO-DEBRIS PASS while an external clean-worktree boundary measured the directory going
# 17 -> 18 entries. A control that cannot return the failing verdict for the one artifact it is
# MOST LIKELY TO PRODUCE is not a weak control, it is a decoration: its PASS and a genuinely clean
# tree are the same output. Found by 4.0.0_SA_CRO~X from outside the process, which is the only
# vantage that could see it.
# AND THE REASON IT HID: lines 42-43 DO NOT LOOK LIKE IMPORTS. They are `_load(...)` calls --
# dynamic imports with no `import` keyword -- so a reader, a linter, or a "move the baseline above
# the imports" reflex all skip them. 2.0.0_SA_COO~X's first probe grepped lines 40-50 for
# import/from and returned EMPTY, and nearly reported that as evidence against the defect.
# THE FIX IS SUPPRESSION, NOT CLEANUP: bytecode is never written, so there is nothing to remove
# and no window in which a reaper could touch the shared tree. The baseline is captured on the
# line after, so it is upstream of every local load.
sys.dont_write_bytecode = True
_PRE_LISTING = set(os.listdir(HERE))


def _pair_state(where=None):
    """git hash-object for each pair member, or None where the member is absent.

    WARN: THE PAIR ARMS USED TO ASSERT THE TWO PRESERVED IDS AS LITERALS, AND THAT MADE THEM
    UNRUNNABLE IN THE ONE ENVIRONMENT THE VERDICT ASKS FOR. The pair is a WORKING-TREE pair --
    the manifest is tracked-modified and the receipt was never stored -- so a CLEAN DETACHED
    CHECKOUT has a different manifest and NO receipt at all, and both arms failed there by
    construction. A control that can only pass in one tree is measuring the tree, not the run.
    The claim that matters is NOT "these bytes are the preserved bytes" (the commit gate and the
    external evidence already say that) but "THIS RUN CHANGED NOTHING", so the baseline is taken
    at process start like the listing baseline, and absence is a legal baseline value.
    """
    out = {}
    for _n in ("graph_object_manifest.json", "graph_object_manifest.receipt.json"):
        _p = os.path.join(where or HERE, _n)
        out[_n] = (subprocess.run(["git", "hash-object", _p], cwd=WS,
                                  capture_output=True, text=True).stdout.strip()
                   if os.path.exists(_p) else None)
    return out


_PRE_PAIR = _pair_state()


def _listing_delta(before, where=None):
    """Entries added to `where` since `before`. The comparison the no-debris arm scores."""
    return set(os.listdir(where or HERE)) - before


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
# DERIVED, never typed: a constant here goes stale the moment the derivation gains
# a pin, and the cheapest repair is to retype it, which is how a control stops
# measuring without anyone deciding to stop measuring.
SNAP = l0._source_snapshot_utc()
BASE = l0.build_receipt(ART, SNAP, reg=l0.load_registry())
BASE_BYTES = json.dumps(BASE, sort_keys=True)
check("the emitter's OWN build_receipt() output validates",
      len(list(V.iter_errors(BASE))) == 0,
      "%d errors" % len(list(V.iter_errors(BASE))))

# ⛔ THE BASELINE ARM ASSERTS DISCRIMINATION, NOT ZERO. "0 findings" is only true when every
# pinned input is committed; under an edited-but-uncommitted compiler the verifier CORRECTLY
# reports a commit:path mismatch. An arm demanding zero would have forced me to weaken the
# verifier or to commit before the suite passed -- both are the tail wagging the dog.
ROLES = ("receipt_schema", "output_schema", "compiler", "registry", "registry_schema",
         "base39", "card_part_map", "card_schema")
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
check("and every finding is an input-closure binding, nothing else",
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
print("  THE REPLAY STATE -- DERIVED FROM PER-EMISSION EVIDENCE, not asserted beside it")
_ART = BASE["describes"]["sha256"]
_T1, _T2 = "2026-08-27T12:00:00Z", "2026-08-27T12:00:01Z"


def _em(seq, dig, when):
    return {"sequence": seq, "digest": dig, "executed_utc": when}


for label, rep, want_ok in [
        ("not_performed / one emission (the honest single run)",
         {"comparison_state": "not_performed", "emissions": [_em(1, _ART, _T1)]}, True),
        # ⛔ v1 CANNOT EXPRESS A COMPARISON, so these flip from ACCEPT to REJECT. A claim a
        # single document makes about its own replay is self-mintable: copying the one row and
        # bumping `sequence` forged a second identical emission and nothing could contradict it.
        ("byte_identical / two emissions -- INEXPRESSIBLE in v1",
         {"comparison_state": "byte_identical",
          "emissions": [_em(1, _ART, _T1), _em(2, _ART, _T2)]}, False),
        ("byte_different / two emissions -- INEXPRESSIBLE in v1",
         {"comparison_state": "byte_different",
          "emissions": [_em(1, _ART, _T1), _em(2, "f" * 64, _T2)]}, False),
        ("byte_identical claimed with ONE emission record",
         {"comparison_state": "byte_identical", "emissions": [_em(1, _ART, _T1)]}, False),
        ("not_performed claimed with TWO emission records",
         {"comparison_state": "not_performed",
          "emissions": [_em(1, _ART, _T1), _em(2, _ART, _T2)]}, False),
        ("R4-3. a COPIED row with only `sequence` changed -- the self-mint",
         {"comparison_state": "not_performed",
          "emissions": [_em(1, _ART, _T1), _em(2, _ART, _T1)]}, False)]:
    # NOTE: the FUTURE-2099 emission moved OUT of this schema-only loop -- see R4-3-CLI below.
    # It is a CROSS-FIELD temporal bound (emission instant vs the receipt's own executed_utc),
    # which JSON Schema cannot express at all, so asking the schema for it scored a real law
    # against an instrument structurally incapable of holding it and read as a FAILING ARM.
    # The law exists and the VERIFIER enforces it; the control now tests the instrument that
    # actually holds it. An arm aimed at the wrong instrument is not evidence the law is missing.
    d = copy.deepcopy(BASE)
    d["replay"] = rep
    n = len(list(V.iter_errors(d)))
    check(label, (n == 0) == want_ok, "%d schema errors, expected %s"
          % (n, "accept" if want_ok else "reject"))

# The two CRO~A built by hand, which the count/set pair could not contradict.
for label, rep in [
        ("D1. an emission instant EARLIER than the source snapshot",
         {"comparison_state": "not_performed",
          "emissions": [_em(1, _ART, "2026-01-01T00:00:00Z")]}),
        ("D2. an emission digest belonging to nothing this receipt describes",
         {"comparison_state": "not_performed", "emissions": [_em(1, "b" * 64, _T1)]})]:
    d = copy.deepcopy(BASE)
    d["replay"] = rep
    extra = [f for f in vr.verify(d) if f not in findings]
    check(label, len(extra) > 0,
          "%d NEW verifier findings: %s" % (len(extra), extra[0][:100] if extra else "-"))


print()
print("=" * 84)
print("REWORK 3 -- SIX MUTANTS THROUGH THE ACTUAL CLI, NOT THE HELPER")
print("=" * 84)
# ⛔ MUTANT 6 EXISTED BECAUSE EVERY ARM ABOVE CALLS vr.verify() IN-PROCESS. The CLI is a
# DIFFERENT PATH: it loads the file itself, and it was loading it with json.load. A suite that
# only ever calls the helper proves the protection exists and never that the path uses it.
VERIFIER = os.path.join(HERE, "verify_receipt.py")


def via_cli(label, text, *, want_findings=True, expect=None):
    """Write bytes, run `python verify_receipt.py <file>`, read rc and findings."""
    fd, p = tempfile.mkstemp(suffix=".json", prefix="cli_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        r = subprocess.run([sys.executable, VERIFIER, p], cwd=WS,
                           capture_output=True, text=True)
        flagged = r.returncode != 0
        # ⛔ SEARCH BOTH STREAMS. A SystemExit refusal prints to STDERR, so an expect-check
        # reading only stdout reported the duplicate-key arm as not-fired while the refusal was
        # sitting in the other pipe. A control blind to half its subject's output is blind.
        both = (r.stdout or "") + (r.stderr or "")
        ok = flagged == want_findings
        if expect:
            ok = ok and expect in both
        check(label, ok,
              "rc=%d  %s" % (r.returncode,
                             ("MATCHED %r" % expect) if expect and expect in both
                             else (both.strip().splitlines() or ["-"])[-1][:96]))
    finally:
        os.remove(p)


def cli_mutant(label, fn, expect=None):
    d = copy.deepcopy(BASE)
    fn(d)
    if json.dumps(d, sort_keys=True) == BASE_BYTES:
        check(label, False, "*** INERT MUTATION ***")
        return
    via_cli(label, json.dumps(d, indent=2, sort_keys=True), expect=expect)


cli_mutant("M1. describes.blob_presence FLIPPED",
           lambda d: d["describes"].__setitem__(
               "blob_presence",
               "computed_only" if d["describes"]["blob_presence"] == "in_object_db"
               else "in_object_db"))
cli_mutant("M2. ONE admitted card's blob_presence FLIPPED",
           lambda d: d["input_closure"]["admitted_cards"][0].__setitem__(
               "blob_presence",
               "computed_only"
               if d["input_closure"]["admitted_cards"][0]["blob_presence"] == "in_object_db"
               else "in_object_db"))


def _earlier(d):
    """An arbitrary EARLIER legal instant, with exact_home's qualifier adjusted to match --
    the mutant CRO~A built, which passed because nothing re-derived the snapshot."""
    e = "2026-08-27T09:00:00Z"
    d["source_snapshot_utc"] = e
    d["input_closure"]["source_snapshot_pin"]["value_utc"] = e
    # the home tracks run_id now, so the mutant leaves it alone and only the snapshot moves
    _ = e


cli_mutant("M3. an arbitrary EARLIER snapshot, home adjusted to match", _earlier,
           expect="source_snapshot_utc: claims")
cli_mutant("M4. ONLY the run-qualified home's timestamp changed",
           lambda d: d.__setitem__(
               "exact_home",
               "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/"
               "graph_object_manifest.20260101T000000000000Z.receipt.json"),
           expect="exact_home: qualifier does not match")
cli_mutant("M5. executed_by FORGED to another well-shaped serial",
           lambda d: d.__setitem__("executed_by", "0.7.0_AE_CloudOps~X"),
           expect="executed_by")
via_cli("M6. raw invalid-first/valid-last duplicate key THROUGH THE CLI",
        '{"authority_role": "authority", "authority_role": "evidence"}',
        expect="duplicate JSON object key")
# ⛔ NO CLI POSITIVE CONTROL IS POSSIBLE, AND THAT IS THE CONTRACT WORKING. `exact_home` is
# pattern-bound to the D11_MANIFEST location AND bound to the path the document was read from,
# so a clean run from any other path is UNREPRESENTABLE. Loosening either binding to let a test
# run would undo the property both were added to create. In-process with the declared home
# supplied; the CLI's path binding is proven by arm A, which fires on `was READ FROM` alone.
_pos = vr.verify(BASE, actual_home=BASE["exact_home"])
check("    POSITIVE CONTROL (in-process): the fixture is clean at its DECLARED home",
      _pos == findings,
      "%d findings, identical to the baseline -- so the declared-home path adds nothing and "
      "removes nothing" % len(_pos))

print()
print("  ADDENDUM A/B -- the two the CLI accepted")
_fake = copy.deepcopy(BASE)
via_cli("A. a schema-valid receipt AT A FAKE PATH -> the PATH is flagged",
        json.dumps(_fake, indent=2, sort_keys=True), expect="was READ FROM")
for _f, _v in (("source_snapshot_utc", "2026-13-45T99:99:99Z"),
               ("executed_utc", "2026-02-30T00:00:00Z")):
    d = copy.deepcopy(BASE)
    d[_f] = _v
    if _f == "source_snapshot_utc":
        d["input_closure"]["source_snapshot_pin"]["value_utc"] = _v
    extra = [f for f in vr.verify(d) if f not in findings]
    check("B. %s = %s (matches the pattern, is no calendar instant)" % (_f, _v),
          any("NOT A REAL INSTANT" in f or "not a real instant" in f for f in extra),
          "%d NEW findings" % len(extra))

print()
print("  REWORK 4 -- the six CRO~A built, through the CLI")
cli_mutant("R4-1a. output_schema.git_blob_id FORGED",
           lambda d: d["input_closure"]["output_schema"].__setitem__("git_blob_id", "a" * 40),
           expect="input_closure.output_schema")
cli_mutant("R4-1b. output_schema.blob_presence FLIPPED",
           lambda d: d["input_closure"]["output_schema"].__setitem__(
               "blob_presence",
               "computed_only"
               if d["input_closure"]["output_schema"]["blob_presence"] == "in_object_db"
               else "in_object_db"),
           expect="input_closure.output_schema")
cli_mutant("R4-1c. output_schema.commit NONEXISTENT",
           lambda d: d["input_closure"]["output_schema"].__setitem__("commit", "e" * 40),
           expect="input_closure.output_schema")
# R4-2 -- THE REDIRECT MUST BE OBSERVABLE, OR IT TESTS NOTHING.
# WARN: THIS ARM FAILED FOR A ROUND, AND THE LAW WAS NEVER THE PROBLEM. It redirected the registry
# pin to HEAD -- and HEAD carries the registry file at the SAME BLOB as the pin (measured:
# 2977bd517021 at both). A redirect to byte-identical content changes nothing a consumer can
# observe, so nothing refused it, and the arm read as a missing authority binding. The binding
# works: redirected to a commit where the registry bytes genuinely DIFFER, the verifier refuses
# with a correctly-named `input_closure.registry` finding.
# `cli_mutant`'s INERT-MUTATION guard could not catch this -- it asks "did the JSON change?"
# (yes, a different commit string) and cannot ask "did anything OBSERVABLE change?". A mutant
# that perturbs a field without perturbing the claim is the negative-arm twin of a control that
# cannot fail. The redirect target is now DERIVED as a commit with differing bytes, and asserted
# to differ before it is used, so this arm cannot silently go inert again.
def _nonratification_commit_with_different_bytes():
    home = BASE["input_closure"]["registry"]["home"]
    pin = BASE["input_closure"]["registry"]["commit"]

    def blob_at(c):
        r = subprocess.run(["git", "rev-parse", "%s:%s" % (c, home)], cwd=WS,
                           capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None

    pinned = blob_at(pin)
    hist = subprocess.run(["git", "log", "--format=%H", "--follow", "--", home], cwd=WS,
                          capture_output=True, text=True).stdout.split()
    for c in hist:
        b = blob_at(c)
        if b and b != pinned:
            return c
    return None


_R42 = _nonratification_commit_with_different_bytes()
check("   R4-2 PRECONDITION: a valid non-ratification commit with DIFFERING registry bytes exists",
      _R42 is not None,
      "without one the redirect is inert and the arm would pass vacuously")
if _R42:
    cli_mutant("R4-2. registry pin REDIRECTED to a valid non-ratification commit (bytes differ)",
               lambda d: d["input_closure"]["registry"].__setitem__("commit", _R42),
               expect="input_closure.registry")
cli_mutant("R4-5. run_id NOT carrying executed_utc",
           lambda d: d.__setitem__("run_id", "20990101T000000000000Z"),
           expect="run_id")
# R4-1d -- the COMMIT:PATH BINDING, which is a different claim from the commit EXISTING.
# R4-1c proves a nonexistent commit is refused. A commit that EXISTS but does not carry the
# pinned path at that commit is the case a bare existence check waves through, and it is the
# likelier real-world corruption: a pin copied from a neighbouring role resolves to a real
# commit every time.
cli_mutant("R4-1d. output_schema.commit REAL but does NOT carry that path",
           lambda d: d["input_closure"]["output_schema"].__setitem__(
               "commit", subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=WS,
                                        capture_output=True, text=True).stdout.split()[0]),
           expect="input_closure.output_schema")
# R4-3-CLI -- relocated from the schema-only loop. See the note at that loop: a cross-field
# temporal bound is not schema-expressible, so this arm must run through the consumer path.
cli_mutant("R4-3-CLI. a FUTURE-2099 emission inside a present receipt",
           lambda d: d["replay"].__setitem__(
               "emissions", [{"sequence": 1,
                              "digest": d["describes"]["sha256"],
                              "executed_utc": "2099-01-01T00:00:00Z"}]),
           expect="replay.emissions")

print()
print("  R4-5. TWO SAME-SECOND RESERVATIONS MUST NOT COLLIDE")
_ids = {l0.build_receipt(ART, SNAP, reg=l0.load_registry(),
                         run_utc="2026-08-27T14:00:00Z")["run_id"] for _ in range(8)}
check("   8 receipts built inside one second yield 8 DISTINCT run_ids",
      len(_ids) == 8, "%d distinct of 8 -- a seconds-only qualifier gave 1" % len(_ids))
_homes = {l0.build_receipt(ART, SNAP, reg=l0.load_registry(),
                           run_utc="2026-08-27T14:00:00Z")["exact_home"] for _ in range(8)}
check("   and 8 DISTINCT immutable homes", len(_homes) == 8, "%d distinct of 8" % len(_homes))

print()
print("  R4-4. LOGICAL-FINAL-HOME PREWRITE VALIDATION -- the would-be bytes, no final artifact")
# The gate must validate the EXACT bytes that would land at the FINAL home, while writing
# nothing there. Validating a staging path instead is the defect this replaced: `exact_home`
# then derived from the staging name and failed its own pattern BY CONSTRUCTION -- a gate that
# could only ever refuse, which is indistinguishable from a gate that works until you ask it to
# pass something.
# (the no-debris baseline is NOT taken here -- it is `_PRE_LISTING`, captured pre-load at line 45.
# Taking it at the point of use was the self-blindness: by here, the harness's own bytecode was
# already on disk and inside the "before" set.)
_r44 = l0.build_receipt(ART, SNAP, reg=l0.load_registry())
_r44_home = os.path.join(WS, _r44["exact_home"])
check("   the receipt is built against the LOGICAL FINAL home, not a staging path",
      _r44["exact_home"].endswith(".receipt.json")
      and "stage" not in _r44["exact_home"] and "tmp" not in _r44["exact_home"],
      _r44["exact_home"])
check("   NO final artifact exists at that home after validation",
      not os.path.exists(_r44_home),
      "prewrite validation must not create the thing it validates")
_bytes_a = json.dumps(_r44, indent=2, sort_keys=True, ensure_ascii=True)
_r44b = l0.build_receipt(ART, SNAP, reg=l0.load_registry(), run_utc=_r44["executed_utc"])
_bytes_b = json.dumps(dict(_r44b, run_id=_r44["run_id"], exact_home=_r44["exact_home"]),
                      indent=2, sort_keys=True, ensure_ascii=True)
check("   the would-be bytes are DETERMINISTIC for a fixed run clock",
      _bytes_a == _bytes_b,
      "same inputs + same run clock must serialise identically, or 'the exact bytes' is undefined")
check("   those exact bytes satisfy the schema",
      not list(V.iter_errors(json.loads(_bytes_a))), "schema errors on the would-be final bytes")
check("   and the verifier accepts them AT THE LOGICAL FINAL HOME",
      len([f for f in vr.verify(json.loads(_bytes_a), _r44["exact_home"])
           if "exact_home" in f]) == 0,
      "the home the bytes name must be the home they are judged at")
check("   POSITIVE CONTROL: the same bytes judged at a WRONG home are refused",
      any("exact_home" in f for f in vr.verify(
          json.loads(_bytes_a),
          _r44["exact_home"].replace(".receipt.json", ".WRONG.receipt.json"))),
      "if a wrong home also passed, the check above would be vacuous")

print()
print("  R4-6. THE PRODUCER PREWRITE GATE IS THE CONSUMER PATH -- identical, not merely similar")
# WARN: "The producer runs the same checks" is a DESCRIPTION unless the two paths are the same
# object. Two verifiers that agree today drift apart on the first edit to one of them, and the
# producer is the copy nobody re-reads.
_gate_src = os.path.join(HERE, "verify_receipt.py")
_emitter_txt = open(os.path.join(HERE, "l0_compile_w3.py"), encoding="utf-8").read()
check("   the emitter loads THE verifier module by path, not a reimplementation",
      "verify_receipt.py" in _emitter_txt and "_vr.verify(" in _emitter_txt,
      "the prewrite gate must call the shipped verifier")
check("   and the CLI consumer entry point is that same file",
      os.path.abspath(VERIFIER) == os.path.abspath(_gate_src), VERIFIER)
check("   the emitter REFUSES TO WRITE when that gate finds anything",
      "REFUSING TO WRITE" in _emitter_txt and "FAILS the same gate" in _emitter_txt,
      "a gate whose failure does not stop the write is a log line")
# no-debris / no-pair-touch: the whole control run above built receipts, ran the CLI many times,
# and wrote temp files. NOTHING of that may remain here, and the preserved pair must be untouched.
_added = _listing_delta(_PRE_LISTING)
check("   NO DEBRIS: the run added nothing to the deliverables directory (baseline taken "
      "PRE-LOAD, line 45)",
      not _added,
      "added: %s -- baseline is upstream of every local _load(), so the harness's own "
      "bytecode is INSIDE this arm's reach" % sorted(_added))
check("   and bytecode writing is SUPPRESSED, not cleaned up afterward",
      sys.dont_write_bytecode is True,
      "suppression leaves nothing to remove and no window in which a reaper touches the tree")
# POSITIVE CONTROL: the arm must be able to go RED on exactly the artifact that fooled it.
# Run against a TEMP directory, never HERE -- proving the comparison can fail must not require
# writing into the protected deliverables tree.
_probe_dir = tempfile.mkdtemp(prefix="nodebris_")
try:
    _probe_before = set(os.listdir(_probe_dir))
    os.mkdir(os.path.join(_probe_dir, "__pycache__"))
    with open(os.path.join(_probe_dir, "__pycache__", "x.cpython-312.pyc"), "wb") as _pf:
        _pf.write(b"\x00")
    _probe_added = _listing_delta(_probe_before, _probe_dir)
    check("   POSITIVE CONTROL: the SAME comparison goes RED on a planted __pycache__",
          _probe_added == {"__pycache__"},
          "an arm that passes both with and without the debris is where this started")
finally:
    for _root, _dirs, _files in os.walk(_probe_dir, topdown=False):
        for _n in _files:
            os.remove(os.path.join(_root, _n))
        for _n in _dirs:
            os.rmdir(os.path.join(_root, _n))
    os.rmdir(_probe_dir)
_POST_PAIR = _pair_state()
for _name in sorted(_PRE_PAIR):
    _b, _a = _PRE_PAIR[_name], _POST_PAIR[_name]
    check("   NO PAIR TOUCH: %s unchanged across the run" % _name, _b == _a,
          "start=%s end=%s" % ((_b or "ABSENT")[:12], (_a or "ABSENT")[:12]))
# AND, WHERE THE PRESERVED PAIR IS ACTUALLY PRESENT, pin it to the ordered ids. This arm is
# environment-declared rather than environment-blind: in a clean detached checkout the receipt
# half does not exist, and saying so out loud beats a literal comparison that fails there for a
# reason unrelated to anything the run did.
_ORDERED = {"graph_object_manifest.json": "db684f932995d519a9087725b2d2539d249ea533",
            "graph_object_manifest.receipt.json": "3da49495aa16c5f92563c9c955bbd888d4f85072"}
_present = {k: v for k, v in _PRE_PAIR.items() if v is not None}
if _present == _ORDERED:
    check("   PAIR IDENTITY: both members match the ordered preserved ids (shared tree)", True,
          "db684f932995 / 3da49495aa16")
else:
    print("  %-58s %s" % ("   PAIR IDENTITY: not the preserved-pair tree -- DECLARED, not assumed",
                          "N/A"))
    for _k in sorted(_PRE_PAIR):
        print("      %-38s %s" % (_k, (_PRE_PAIR[_k] or "ABSENT (untracked half absent in a "
                                       "clean checkout)")[:60]))

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
