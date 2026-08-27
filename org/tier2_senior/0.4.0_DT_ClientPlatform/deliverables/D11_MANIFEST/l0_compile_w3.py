#!/usr/bin/env python3
"""W3-m-6 -- THE COMPILE STEP. Fold wave-3 substrate cards into the L0 graph substrate manifest.

⛔ EXTEND, NOT BUILD. The oracle as CUT said "populated instances estate-wide: ZERO"; that premise
was 0.0.0_AB_MSTR's, WITHDRAWN at 06:29Z, and the cell was corrected to EXTEND @7d03d9e788. A
conformant 39-part instance already exists. Building from zero would have re-derived 39 measured
parts and thrown away their denominator method.

⛔ AND THIS SCRIPT IS ITSELF THE POINT. 0.0.0_AB_MSTR's corrected finding was not that the manifest
was missing -- it was that the manifest is a HAND-COMPILED artifact with a vintage, NO GENERATOR and
no step that advances it, so at wave-3 close it would not be ABSENT, it would be STALE while reading
COMPLETE. Every validator passes on a stale conformant manifest. A generator is the remedy; this is it.

WHAT IT DOES NOT DO, STATED SO THE LIMIT IS NOT DISCOVERED LATER:
  - It does NOT re-derive the original 39 parts. They are carried forward VERBATIM from the phase-A
    instance, whose denominator records an estate sweep this script does not repeat. Those 39 remain
    hand-compiled; what is now generated is the WAVE-3 EXTENSION and the recompilation itself.
  - It does NOT invent the card->part join. That join is DECLARED in w3_card_part_map.json, because
    9 of 13 cards carry prose in artifact.location.home and cannot be joined mechanically. See that
    file's _why_declared_and_not_derived.
  - It does NOT blend multi-writer parts. graph_nodes has THREE measured writers and L0 `generation`
    holds ONE. On disagreement the existing value STANDS and the disagreement is written into
    evidence. A compiler that picked would look tidier and would be lying.
"""
from __future__ import annotations
import glob
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from collections import Counter, defaultdict

from jsonschema import Draft202012Validator

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST")
# ⛔ SEPARATE INPUT FROM OUTPUT. The first version of this script read AND wrote
# graph_object_manifest.json, which made it NON-RE-RUNNABLE: a second run re-appended every
# declared_opinion and tripped the add-target assert. A generator whose output is its own input
# corrupts or aborts on the second run -- and "it runs when cards land" REQUIRES a second run.
# BASE39 is the immutable phase-A instance; OUT is derived and fully rebuilt every time.
BASE39 = os.path.join(HERE, "graph_object_manifest.base39.json")
BASE = os.path.join(HERE, "graph_object_manifest.json")
MAP = os.path.join(HERE, "w3_card_part_map.json")
SCHEMA = os.path.join(WS, "org/standards/L0_GRAPH_SUBSTRATE_MANIFEST.schema.json")
# ⛔ NO DISCOVERY CONSTANT LIVES HERE ANY MORE. The registry's own `discovery_globs` is the
# sole diagnostic source; a constant beside it was a second authority, and it was the inert one.
CARD_REGISTRY = os.path.join(HERE, "card_population_registry.v1.json")
REGISTRY_SCHEMA = os.path.join(HERE, "CARD_POPULATION_REGISTRY.v1.schema.json")
CARD_SCHEMA = os.path.join(WS, "org/standards/SUBSTRATE_CARD.v2.schema.json")
RECEIPT_SCHEMA = os.path.join(HERE, "MANIFEST_RECEIPT.v1.schema.json")

ME = "0.4.0_DT_ClientPlatform~X"
PIN = "e48a7466ba"
# ⛔ THE PRIOR CONSTANT WAS A FALSIFIED EXECUTION TIME. It read 2026-08-27T07:10:00Z -- EARLIER
# than the frozen schema commit and earlier than the compiler commit that would emit it, so the
# artifact claimed to have been compiled before its own inputs existed. Determinism was being
# bought by freezing a clock reading, which is not determinism, it is a false statement that
# happens to repeat.
# TWO FIELDS, TWO CLAIMS: the SOURCE SNAPSHOT is a deterministic property of the pinned inputs
# and belongs in the artifact; the EXECUTION TIME is a per-run fact and belongs in a receipt
# beside it, where a replay comparison can ignore it on purpose rather than by accident.
def _source_snapshot_utc() -> str:
    """Committer time of the newest PINNED INPUT: the ratified commit and the frozen schema.
    Deterministic for a given input set, and it moves only when an input does."""
    pins = []
    for ref in (_registry_commit(), _schema_commit(), _card_schema_commit(),
                _compiler_commit(), _receipt_schema_commit()):
        if ref:
            r = subprocess.run(["git", "show", "-s", "--format=%cI", ref], cwd=WS,
                               capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                pins.append(r.stdout.strip())
    if not pins:
        raise SystemExit("REFUSING TO COMPILE -- no pinned input carries a commit time; a "
                         "snapshot stamp with no source is the falsified clock one step over")
    # ⛔ NORMALISE TO REAL UTC. `git show --format=%cI` emits the COMMITTER'S OFFSET, so the
    # newest pin is picked correctly only after conversion, and a field named `_utc` carrying
    # `-04:00` is the local-time-with-a-Z defect wearing the right name.
    from datetime import timezone
    from datetime import datetime as _dt
    return max(_dt.fromisoformat(p).astimezone(timezone.utc) for p in pins).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def _registry_commit():
    try:
        return load_json_strict(CARD_REGISTRY)["ratified_at_commit"]
    except Exception:
        return None


def _schema_commit():
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", SCHEMA], cwd=WS,
                       capture_output=True, text=True)
    return r.stdout.strip() or None


def _card_schema_commit():
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", CARD_SCHEMA], cwd=WS,
                       capture_output=True, text=True)
    return r.stdout.strip() or None


def _receipt_schema_commit():
    """The receipt contract is a TEMPORAL pin too. If it moves, the meaning of every field in an
    already-written receipt moves with it, and a snapshot blind to that is deterministic over a
    closure that excludes its own definition."""
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", RECEIPT_SCHEMA], cwd=WS,
                       capture_output=True, text=True)
    return r.stdout.strip() or None


def _compiler_commit():
    """⛔ THE COMPILER IS A TEMPORAL PIN TOO, and leaving it out of the snapshot derivation was
    the same omission one file over: the thing that PRODUCES the output can move, and a snapshot
    blind to it is deterministic over a closure that does not include the producer."""
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--",
                        os.path.relpath(os.path.abspath(__file__), WS).replace(os.sep, "/")],
                       cwd=WS, capture_output=True, text=True)
    return r.stdout.strip() or None
ORDER = {"measured": 3, "held": 2, "inferred": 1, "absent": 0}


def _no_dupes(pairs):
    """object_pairs_hook that REFUSES duplicate raw object keys.

    ⛔ JSON PERMITS DUPLICATE KEYS AND `json.load` SILENTLY KEEPS THE LAST. rework14 keyed
    `variant_suffixes` by suffix on the ground that "duplicate keys are impossible" -- true of
    the parsed dict, FALSE of the bytes. Without this hook a document carrying two `.wal` keys
    validates cleanly with one silently discarded: the ambiguity the object shape was chosen to
    make INEXPRESSIBLE, reintroduced one layer below the schema. Runs BEFORE validation, because
    a validator only ever sees what the parser already collapsed.
    """
    seen = set()
    for k, _v in pairs:
        if k in seen:
            raise SystemExit("REFUSING TO PARSE -- duplicate JSON object key %r; the parser "
                             "would silently keep the last and no validator could see it" % k)
        seen.add(k)
    return dict(pairs)


def load_json_strict(path: str):
    """Every read in this compiler goes through here. One door, so the guard cannot be
    bypassed by a future call site that simply forgot it."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh, object_pairs_hook=_no_dupes)


def git_blob_id(path: str) -> str:
    """⛔ THE IDENTITY PIN, AND IT IS NOT A DIGEST OF THE BYTES ON DISK.

    The prior revision hashed the working-tree bytes with sha256 and 9 of 13 members failed
    against Git-object bytes -- the CRLF/LF boundary on a Windows checkout, in the field whose
    entire job is identity. A DIGEST WITHOUT ITS NORMALISATION IS NOT AN IDENTITY.
    `git hash-object` applies the repo's own filters, so the pin and the check are computed the
    same way and the comparison cannot straddle the boundary.
    """
    r = subprocess.run(["git", "hash-object", "--", path], cwd=WS,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("REFUSING TO COMPILE -- git hash-object failed for %r: %s"
                         % (path, r.stderr.strip()[:120]))
    return r.stdout.strip()


def resolve_inside_workspace(rel: str) -> str:
    """⛔ A REGEX CANNOT RESOLVE A PATH, so containment is enforced HERE, not in the schema.

    CRO Base reproduced an external invalid card admitted through BACKSLASH TRAVERSAL. On
    Windows `a\\..\\..\\x` traverses and `\\\\host\\share` is a UNC alias for a location outside
    the repo entirely -- and the old pattern only forbade FORWARD-slash dot segments, so both
    walked straight through. The schema now rejects backslashes; this rejects everything a
    pattern structurally cannot see.
    """
    if "\\" in rel:
        raise SystemExit("REFUSING TO COMPILE -- backslash in an admitted path %r; it is a "
                         "traversal and UNC vector the pattern cannot resolve" % rel)
    full = os.path.realpath(os.path.join(WS, rel))
    root = os.path.realpath(WS)
    if os.path.commonpath([full, root]) != root:
        raise SystemExit("REFUSING TO COMPILE -- admitted path %r resolves OUTSIDE the "
                         "workspace: %s" % (rel, full))
    # POSIX-normalised equality: the resolved path must be the declared one, not merely inside.
    back = os.path.relpath(full, root).replace(os.sep, "/")
    if back != rel:
        raise SystemExit("REFUSING TO COMPILE -- admitted path %r normalises to %r; two "
                         "spellings of one location is the identity split this registry exists "
                         "to prevent" % (rel, back))
    return full


def load_registry() -> dict:
    """The admitted-card registry, VALIDATED and BOUND before use.

    Validation is not enough on its own: a schema cannot check that a commit EXISTS, that a
    path RESOLVES inside the workspace, or that the ratified candidate set is the one in front
    of the ratifier. Each of those is enforced here and named as a schema limit rather than
    assumed away.
    """
    from jsonschema import Draft202012Validator
    doc = load_json_strict(CARD_REGISTRY)
    errs = list(Draft202012Validator(load_json_strict(REGISTRY_SCHEMA)).iter_errors(doc))
    if errs:
        raise SystemExit(
            "REFUSING TO COMPILE -- the card registry does not validate (%d errors): %s"
            % (len(errs), "; ".join("%s: %s" % ("/".join(str(x) for x in e.path), e.message[:90])
                                    for e in errs[:5])))
    if doc["registry_version"] != "v1":
        raise SystemExit("REFUSING TO COMPILE -- registry_version %r is not the v1 this "
                         "compiler reads" % doc["registry_version"])
    # ⛔ EXISTENCE IS NOT A SCHEMA PROPERTY. A 40-hex string that names no object validated.
    if subprocess.run(["git", "cat-file", "-e", doc["ratified_at_commit"] + "^{commit}"],
                      cwd=WS, capture_output=True).returncode != 0:
        raise SystemExit("REFUSING TO COMPILE -- ratified_at_commit %s names no commit in this "
                         "repository" % doc["ratified_at_commit"])
    # ⛔ AND THE COMMIT ALONE BINDS NOTHING ABOUT WHAT THE RATIFIER SAW.
    got = candidate_set_digest(doc["ratified_discovery_globs"])
    if got != doc["candidate_set_digest"]:
        raise SystemExit(
            "REFUSING TO COMPILE -- the candidate set has CHANGED since ratification "
            "(pinned %s, now %s). The registry still admits exactly what it admitted; this "
            "refusal says the DIAGNOSTIC ground moved and the ratification must be re-read, "
            "not that admission is wrong." % (doc["candidate_set_digest"][:12], got[:12]))
    return doc


def candidate_set_digest(globs) -> str:
    """sha256 over the sorted `path\x00git_blob_id` lines of every candidate the globs match.

    Binds a ratification to the SET IT SAW. `ratified_at_commit` alone names a moment and says
    nothing about what was in front of the ratifier -- two different candidate sets at one
    commit are indistinguishable, and "ratified at HEAD" would be true of both.
    """
    lines = []
    for pattern in sorted(globs):
        for p in glob.glob(os.path.join(WS, pattern), recursive=True):
            rel = os.path.relpath(p, WS).replace(os.sep, "/")
            lines.append(rel + chr(0) + git_blob_id(rel))
    return hashlib.sha256(chr(10).join(sorted(lines)).encode("utf-8")).hexdigest()


def load_cards() -> dict:
    """ADMISSION BY ENUMERATION. Every member is verified on THREE axes before it is read:
    the file EXISTS, its raw bytes hash to the pinned digest, and its subject.id is the pinned
    one. ⛔ THE THIRD IS NOT REDUNDANT: path+digest identify the FILE, subject_id identifies
    WHAT IT IS ABOUT, and a card whose subject was replaced under an unchanged path is caught
    by the digest only because the bytes happened to change with it. Pinning the subject makes
    the check direct instead of incidental.

    A card is never read because a glob matched it. Unlisted candidates are REPORTED by
    registry_diagnostics() and admitted by nothing.
    """
    from jsonschema import Draft202012Validator
    reg = load_registry()
    card_validator = Draft202012Validator(load_json_strict(CARD_SCHEMA))
    out, failures = {}, []
    for m in reg["extension_population"]["members"]:
        full = resolve_inside_workspace(m["path"])
        if not os.path.exists(full):
            failures.append("%s: LISTED BUT MISSING" % m["path"])
            continue
        got = git_blob_id(m["path"])
        if got != m["git_blob_id"]:
            failures.append("%s: BLOB MISMATCH (pinned %s, in tree %s)"
                            % (m["path"], m["git_blob_id"][:12], got[:12]))
            continue
        with open(full, "rb") as fh:
            raw = fh.read()
        c = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_dupes)
        # ⛔ schema_version == 2 IS A LABEL, NOT A VALIDATION, and CRO Base walked an external
        # invalid card straight through it. The card is now validated against the PINNED
        # SUBSTRATE_CARD.v2 contract, which is the only thing that makes the label mean anything.
        cerrs = list(card_validator.iter_errors(c))
        if cerrs:
            failures.append("%s: CARD INVALID against SUBSTRATE_CARD.v2 (%d errors, first: %s)"
                            % (m["path"], len(cerrs), cerrs[0].message[:80]))
            continue
        subject = (c.get("subject") or {}).get("id")
        if subject != m["subject_id"]:
            failures.append("%s: SUBJECT MISMATCH (pinned %r, in file %r)"
                            % (m["path"], m["subject_id"], subject))
            continue
        if subject in out:
            failures.append("%s: DUPLICATE SUBJECT within one population" % m["path"])
            continue
        out[subject] = c
    if failures:
        raise SystemExit("REFUSING TO COMPILE -- %d admitted member(s) failed verification:\n  %s"
                         % (len(failures), "\n  ".join(failures)))
    return out


def registry_diagnostics() -> dict:
    """What the DISCOVERY glob can see versus what the registry ADMITS. Reporting only."""
    reg = load_registry()
    admitted = {m["path"] for m in reg["extension_population"]["members"]}
    # ⛔ THE REGISTRY'S OWN FIELD IS THE SOLE DIAGNOSTIC SOURCE. It previously carried
    # discovery_globs while this function read a module constant, so the field was INERT and a
    # reader editing it would have changed nothing. A second copy of a value is a second
    # authority, and the inert one is the one people trust.
    candidates = set()
    for pattern in reg["discovery_globs"]:
        candidates |= {os.path.relpath(p, WS).replace(os.sep, "/")
                       for p in glob.glob(os.path.join(WS, pattern), recursive=True)}
    return {"admitted": sorted(admitted),
            "candidates": sorted(candidates),
            "unlisted": sorted(candidates - admitted),
            "receiver_populations": {
                r: len(v["members"])
                for r, v in sorted(reg["receiver_source_populations"].items())}}


def classify_home_space(home: str):
    """4.0.0_SA_CRO~A's rules, FAIL CLOSED. Returns None when unclassifiable.

    ⛔ NEVER GUESSES iceberg_table. An Iceberg table has no unambiguous surface form here -- the
    same table is addressed as a tuple by pyiceberg and as a dotted name by Trino
    (cse_schema.py:595), which is the very split `home_space` exists to record. Guessing it would
    mint the defect the field was added to prevent.
    """
    h = str(home or "")
    if h == "NONE":
        return "none"
    if h.startswith("s3://"):
        return "s3_uri"
    if (" " not in h) and ("/" in h) and not h.startswith("/"):
        return "repo_path"
    return None


def _localize_home(card_home, card_subject):
    """Prefer the card's home; fall back to the map's exact subject path when it is prose."""
    if classify_home_space(card_home) is not None:
        return card_home
    return str(card_subject).split(" :: ")[0].split("#")[0].strip()


def card_generation_bits(c: dict) -> dict:
    """The four L0 `generation` fields this card actually measures."""
    meth = c["process"]["methodology"]
    cad = c["process"]["cadence"]
    return {
        "materializer_standing": meth.get("materializer_standing"),
        "declared_opinions": meth.get("declared_opinions") or [],
        # ⛔ A MEASURED NONE-FOUND MUST NOT DEGRADE INTO AN UNKNOWN NULL. In a card,
        # actual_trigger=None with cadence.basis=measured means "measured, nothing fires it".
        # In L0, trigger=null means "not known". Passing the None straight through SILENTLY
        # DROPS THE CLAIM -- a value must carry its claim into the field a consumer reads.
        "cadence": cad.get("declared_rhythm") or (
            "NONE DECLARED (measured)" if cad.get("basis") == "measured" else None),
        "trigger": cad.get("actual_trigger") or (
            "NONE-FOUND (measured)" if cad.get("basis") == "measured" else None),
        "basis": min([meth.get("basis", "absent"), cad.get("basis", "absent")],
                     key=lambda v: ORDER[v]),
    }



def _presence(blob):
    """⛔ A COMPUTED IDENTITY IS NOT AN ADMITTED ONE. `git hash-object` without -w does correct
    arithmetic over the bytes and writes nothing, so the id names no object anyone else can
    resolve -- and it is indistinguishable from a real one by shape. Stated per pin."""
    if not blob:
        return "computed_only"
    ok = subprocess.run(["git", "cat-file", "-e", blob], cwd=WS, capture_output=True).returncode
    return "in_object_db" if ok == 0 else "computed_only"


def _pin(rel: str) -> dict:
    """One input, pinned by CONTENT **and** COMMIT. ⛔ `commit` WAS OPTIONAL AND THAT LET A
    FORGED COMMIT SIT BESIDE A REAL BLOB with nothing able to object, because the verifier only
    ever checked the blob. Both are required now and the verifier binds them: the commit must
    EXIST and `commit:path` must RESOLVE THE CLAIMED BLOB."""
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", rel], cwd=WS,
                       capture_output=True, text=True)
    commit = r.stdout.strip()
    if not commit:
        raise SystemExit("REFUSING TO EMIT A RECEIPT -- input %r has no commit, so its pin "
                         "cannot be bound to anything" % rel)
    b = _blob(rel)
    return {"home": rel, "git_blob_id": b, "commit": commit, "blob_presence": _presence(b)}


def _blob(rel: str):
    r = subprocess.run(["git", "hash-object", "--", rel], cwd=WS,
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def _rel(p: str) -> str:
    return os.path.relpath(p, WS).replace(os.sep, "/")


def build_receipt(out_path: str, snapshot_utc: str, reg: dict,
                  run_utc: str = None) -> dict:
    """The receipt for ONE emission. PURE apart from reading the tree -- callable by a control
    without running a compile, which is the only way a fixture stays honest about the emitter."""
    art = _rel(out_path)
    with open(out_path, "rb") as fh:
        raw = fh.read()
    _run_utc = run_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "document_kind": "manifest_execution_receipt",
        "governing_schema": {"home": _rel(RECEIPT_SCHEMA),
                             "id": "https://opal.internal/schemas/MANIFEST_RECEIPT.v1.schema.json"},
        # ⛔ QUALIFIED BY THE RUN, NOT THE CLOSURE. Qualifying by the SNAPSHOT made two
        # emissions of an identical closure collide, so the second refused and replay evidence
        # could never be furnished -- the immutability guard made the determinism claim beside
        # it unprovable. Run identity and closure identity are two axes.
        "exact_home": "%s.%s.receipt.json" % (art.rsplit(".json", 1)[0],
                                              _run_utc.replace("-", "").replace(":", "")),
        # FOUR INDEPENDENT AXES. A document's origin, its permitted future, its time semantics
        # and its standing move separately, and collapsing any two hides a real state.
        "authorship_mode": "machine_emitted",
        "mutation_policy": "immutable",
        "temporal_claim": "point_in_time",
        # ⛔ evidence, NEVER authority: this reports what a run did and can be wrong about it.
        "authority_role": "evidence",
        "describes": {"relationship": "emitted_by_same_run", "home": art,
                      "sha256": hashlib.sha256(raw).hexdigest(),
                      "git_blob_id": _blob(art), "blob_presence": _presence(_blob(art))},
        "input_closure": {
            # THE GOVERNING CONTRACT IS AN INPUT: it can change what every other field
            # in this document MEANS, and it was absent from the closure meant to be complete.
            "receipt_schema": _pin(_rel(RECEIPT_SCHEMA)),
            # THREE DISTINCT SCHEMA ROLES: what governs THIS document, what governs the emitted
            # MANIFEST, and what governs the INPUT CARDS. Conflating any two hides a swap.
            "output_schema": _pin(_rel(SCHEMA)),
            "compiler": _pin(_rel(os.path.abspath(__file__))),
            "registry": _pin(_rel(CARD_REGISTRY)),
            "registry_schema": _pin(_rel(REGISTRY_SCHEMA)),
            "base39": _pin(_rel(BASE39)),
            "card_part_map": _pin(_rel(MAP)),
            "card_schema": _pin(_rel(CARD_SCHEMA)),
            # THE LIST vs WHAT THE LIST RESOLVED TO -- two claims, and v0 pinned neither.
            "admitted_cards": [{"path": m["path"], "subject_id": m["subject_id"],
                                "git_blob_id": m["git_blob_id"],
                                "blob_presence": _presence(m["git_blob_id"])}
                               for m in reg["extension_population"]["members"]],
            "source_snapshot_pin": {
                # ⛔ ALL THREE. A subset validated before, so a derivation OMITTING THE
                # SCHEMA COMMIT passed -- and a snapshot ignoring an input that can move is not
                # deterministic over the closure it claims to cover.
                "derived_from": ["registry_ratified_commit", "output_schema_commit",
                                 "card_schema_commit", "compiler_commit",
                                 "receipt_schema_commit"],
                "value_utc": snapshot_utc},
            "complete": True,
        },
        "source_snapshot_utc": snapshot_utc,
        "executed_utc": _run_utc,
        "executed_by": ME,
        # ⛔ ONE emission per run, so the state is `not_performed` -- NOT "byte_identical:
        # false", which meant BOTH 'compared and differed' AND 'never compared'. One value over
        # two facts, and the second is the honest state of every single-emission run.
        # The digest here is the ARTIFACT'S OWN, which is what makes the claim checkable.
        # PER-EMISSION EVIDENCE: the count IS the array length and the digests ARE its
        # members, so a forged comparison cannot claim runs it has no record of.
        "replay": {"comparison_state": "not_performed",
                   "emissions": [{"sequence": 1, "digest": hashlib.sha256(raw).hexdigest(),
                                  "executed_utc": _run_utc}]},
    }

def main(out_path: str = None) -> None:
    """out_path redirects the EMISSION only. ⛔ NOT a reduced mode: every read, every control
    and every refusal is identical, so a clean replay is evidence about the real compile rather
    than about a simplified stand-in."""
    out_path = out_path or BASE
    base = load_json_strict(BASE39)
    mapping = load_json_strict(MAP)
    SOURCE_SNAPSHOT_UTC = _source_snapshot_utc()
    cards = load_cards()
    _diag = registry_diagnostics()
    parts = {p["id"]: p for p in base["parts"]}
    base_count = len(parts)

    rows = mapping["rows"]
    # ---- PARTITION CHECK FIRST: a partition whose parts do not sum is a residual bucket.
    acts = Counter(r["action"] for r in rows)
    assert len(rows) == len(cards), (
        "map rows %d != cards on disk %d -- the map and the population disagree" % (len(rows), len(cards)))
    missing = sorted(set(cards) - {r["card_subject"] for r in rows})
    assert not missing, "cards with NO map row (would be silently dropped): %s" % missing

    # ---- ENRICH -------------------------------------------------------------------
    contrib: dict[str, list] = defaultdict(list)
    for r in rows:
        if r["action"] != "enrich":
            continue
        c = cards[r["card_subject"]]
        for pid in r["part_ids"]:
            assert pid in parts, "enrich target %r absent from base manifest" % pid
            contrib[pid].append((r["card_subject"], card_generation_bits(c)))

    enriched = []
    for pid, contribs in sorted(contrib.items()):
        p = parts[pid]
        gen = p["generation"]
        standings = {b["materializer_standing"] for _, b in contribs}
        # NO BLENDING: one contributor -> take it; several that agree -> take it;
        # several that disagree -> the existing value STANDS and the split is recorded.
        if len(standings) == 1:
            gen["materializer_standing"] = standings.pop()
            standing_note = ""
        else:
            standing_note = (" ⛔ WRITERS DISAGREE ON STANDING (%s); the pre-existing value %r is "
                             "RETAINED rather than picked -- L0 generation holds ONE standing and "
                             "this artifact has %d measured writers."
                             % (", ".join("%s=%s" % (s, b["materializer_standing"])
                                          for s, b in contribs),
                                gen.get("materializer_standing"), len(contribs)))

        # declared_opinions: UNION, every entry SOURCE-PREFIXED so provenance survives the merge.
        ops = list(gen.get("declared_opinions") or [])
        for subj, b in contribs:
            for o in b["declared_opinions"]:
                ops.append("[%s] %s" % (subj, o))
        gen["declared_opinions"] = ops or None

        cads = {b["cadence"] for _, b in contribs if b["cadence"]}
        trigs = {b["trigger"] for _, b in contribs if b["trigger"]}
        if len(contribs) == 1:
            gen["cadence"] = next(iter(cads), None) or gen.get("cadence")
            gen["trigger"] = next(iter(trigs), None) or gen.get("trigger")
        else:
            gen["cadence"] = ("PER WRITER: " + "; ".join(
                "%s=%s" % (s, b["cadence"]) for s, b in contribs)) if cads else gen.get("cadence")
            gen["trigger"] = ("PER WRITER: " + "; ".join(
                "%s=%s" % (s, b["trigger"] or "none-found") for s, b in contribs))

        # ⛔ GRAIN: the part-level `basis` covers the part's OWN claims (that it exists, its home,
        # its vintage). A contributing card's GENERATION-row uncertainty must NOT demote it --
        # doing so turns a measured part into basis='absent', i.e. "no basis exists yet", which
        # DESTROYS a true claim. Measured instance: comp_aws_cli's cadence.basis is genuinely
        # `absent`, and the first version of this line drove graph_nodes from measured to absent.
        # L0 v1 has ONE basis for twelve fields; SUBSTRATE_CARD.v2 solved exactly this with
        # basis_by_field. Until L0 has that, the generation floor is recorded in evidence.
        gen_floor = min([b["basis"] for _, b in contribs], key=lambda v: ORDER[v])
        p["evidence"] = (p.get("evidence", "") +
                         " || W3 COMPILE @%s: generation enriched from %d wave-3 card(s) [%s]; "
                         "join DECLARED in w3_card_part_map.json, not derived (9 of 13 cards carry "
                         "prose in artifact.location.home and cannot be joined mechanically). "
                         "GENERATION-ROW BASIS FLOOR ACROSS CONTRIBUTORS: %s (the part-level basis "
                         "is deliberately NOT demoted by it -- different grain).%s"
                         % (PIN, len(contribs), ", ".join(s for s, _ in contribs),
                            gen_floor, standing_note))
        enriched.append(pid)

    # ---- ADD ----------------------------------------------------------------------
    added = []
    for r in rows:
        if r["action"] != "add":
            continue
        c = cards[r["card_subject"]]
        pid = r["part_ids"][0]
        assert pid not in parts, "add target %r already exists -- that is an ENRICH" % pid
        b = card_generation_bits(c)
        loc = c["artifact"]["location"]
        per = c["artifact"]["persistence"]
        parts[pid] = {
            "id": pid,
            "part_class": "materializer",
            # ⛔ 4.0.0_SA_CRO~A audit item 3: a card's `home` may be PROSE ("...py (436 lines)
            # @76c58923ac; writes globgrph.<surface>..."), which is not a location a consumer can
            # resolve. When it will not classify, fall back to the MAP ROW'S CARD SUBJECT, which is
            # an exact path -- and say so in evidence rather than silently substituting.
            "home": _localize_home(loc.get("home"), r["card_subject"]),
            "authority_role": per.get("authority_role", "none"),
            "temporal_claim": "current_state",
            "lineage": {
                "projection_of": [x["id"] for x in (loc.get("projection_of") or [])],
                "source_identity": None,
            },
            "generation": {
                "materializer": c["subject"]["id"],
                "materializer_digest": None,
                "materializer_standing": b["materializer_standing"] or "unknown",
                "declared_opinions": b["declared_opinions"] or None,
                "cadence": b["cadence"],
                "trigger": b["trigger"],
            },
            "population_status": "production",
            "vintage": {
                "measured_utc": c["as_of"]["carded_utc"],
                "method": "wave-3 substrate card, SUBSTRATE_CARD.v2, pinned @" + c["as_of"]["commit_ish"],
                "age_note": None,
            },
            "basis": b["basis"],
            "evidence": ("NEW PART, added by the W3 compile step @%s. %s || Card verdict: %s -- %s"
                         % (PIN, r["evidence"], c["verdict"]["standing"],
                            c["verdict"]["why"][:400])),
            "owner": c.get("carded_by", "UNOWNED"),
        }
        added.append(pid)

    unresolved = [r for r in rows if r["action"] == "unresolved"]

    # ---- the known-false attribution the compile surfaced --------------------------
    fx = parts.get("fedobs_coevolution_snap")
    if fx:
        fx["evidence"] += (" || ⛔ W3 COMPILE FLAG @%s: this part names generation.materializer = "
                           "cse_emit_frontend_coevolution.py, but wave 3 carded BOTH of that file's "
                           "write paths and NEITHER writes this table (PATH A = local JSONL, PATH B "
                           "= an S3 watermark object). 2.0.0_SA_COO~X independently falsified the "
                           "same claim in 74880. Either an uncarded third path exists or this "
                           "attribution is wrong. NOT RESOLVED -- flagged so the next reader "
                           "inherits the doubt rather than the claim." % PIN)

    # ---- reassemble ---------------------------------------------------------------
    out = dict(base)
    out["compiled_by"] = ME
    # ⛔ THE FIELD NAMES ARE THE FROZEN CONTRACT'S AND ARE NOT MINE TO RENAME -- `as_of` requires
    # compiled_utc + commit_ish and forbids additional properties. What changes is the VALUE:
    # compiled_utc was a HARD-CODED 2026-08-27T07:10:00Z, EARLIER than both the schema commit and
    # the compiler commit that emits it, so the artifact claimed to predate its own inputs.
    # Determinism bought by freezing a clock reading is not determinism; it is a false statement
    # that happens to repeat. It is now DERIVED from the newest pinned input, so it is
    # deterministic for a given input set and moves only when an input moves.
    # ⛔ AND THE ACTUAL EXECUTION TIME GOES IN A SEPARATE RECEIPT, not here: a replay comparison
    # must be able to ignore it ON PURPOSE, which it cannot do while it shares a field with a
    # value that is supposed to be stable.
    out["as_of"] = {"compiled_utc": SOURCE_SNAPSHOT_UTC, "commit_ish": PIN}
    # ⛔ home_space stamped MECHANICALLY, AUTHORED VALUES PRESERVED, FAIL CLOSED.
    # An unclassifiable home aborts the emit rather than shipping a part whose address space is a
    # guess -- 4.0.0_SA_CRO~A audit item 2.
    _unclassifiable = []
    for _p in parts.values():
        if "home_space" in _p:          # authored upstream (base39's C3 triplet) -- never overwritten
            continue
        _hs = classify_home_space(_p.get("home"))
        if _hs is None:
            _unclassifiable.append((_p["id"], str(_p.get("home"))[:70]))
        else:
            _p["home_space"] = _hs
    if _unclassifiable:
        raise SystemExit(
            "REFUSING TO EMIT -- home_space unclassifiable, and it is NOT guessed: "
            + "; ".join("%s -> %r" % r for r in _unclassifiable))

    out["parts"] = sorted(parts.values(), key=lambda p: p["id"])

    # ⛔ SHALLOW-COPY ALIAS: `out = dict(base)` means out["denominator"] IS
    # base["denominator"]. Anything appended to it before this line MUTATES the frozen phase-A
    # method that the very next statement embeds as "unchanged and NOT re-run by this compiler".
    # Snapshotted so that sentence stays true of its own content.
    prior = dict(base["denominator"])
    out["denominator"] = {
        # ⛔ NAMES BOTH POPULATIONS RATHER THAN BLENDING THEM -- the oracle's own words.
        "method": (
            "TWO POPULATIONS, NAMED SEPARATELY AND NOT BLENDED. "
            "(A) THE ORIGINAL %d PARTS -- carried forward VERBATIM from the phase-A instance "
            "compiled 2026-08-26T19:33Z @14da312322. Their method, unchanged and NOT re-run by this "
            "compiler: %s "
            "(B) THE WAVE-3 MATERIALIZER POPULATION -- %d substrate cards conforming to "
            "SUBSTRATE_CARD.v2, produced by 4 lanes under NFRA_SUBSTRATECARDING wave 3 and read off "
            "disk at %s. Folded in as %d ENRICH mappings touching %d distinct parts, %d ADD, %d "
            "UNRESOLVED-and-deliberately-unwritten. %d = %d + %d + %d, DERIVED from the map's "
            "own action counts at compile -- the prior revision TYPED `13 = 9 + 3 + 1` beside a "
            "map that actually reads 8 + 3 + 2, so the sentence asserted a partition the "
            "artifact contradicted and still claimed it summed. "
            "The card->part join is DECLARED in w3_card_part_map.json rather than derived, because "
            "9 of 13 cards carry prose in artifact.location.home; that is a contract finding routed "
            "to the schema owner, not a lane defect. "
            "⛔ WHAT COUNTS AS A PART, STATED ON THE FACE BECAUSE IT WAS NOT (3.0.0_SA_CVO~X 74911). "
            "An L0 part is an ARTIFACT A NAMED WRITER ACTUALLY WRITES, with whether the estate "
            "INTENDS it recorded in population_status -- NOT canonical-artifacts-only. That is "
            "measured from the registry rather than preferred: population_status carries 'orphaned' "
            "as a legal value and kuzu_db is registered with it, so observed-not-intended artifacts "
            "are demonstrably admissible. THE CONSEQUENCE FOR REGISTRATION: an artifact is declined "
            "only when no named writer in scope wrote it -- never merely because its writer COULD "
            "have written elsewhere, which reasons from the writer's domain about the artifact and "
            "is a grain slip. The one declined instance here (cse_emit_frontend_coevolution PATH A) "
            "is declined on the first test, not the second: its own card measures that the path "
            "writes a LOCAL dev-box file with no boto3, and that the surviving S3 object is that "
            "file AFTER A HUMAN UPLOADED IT -- a different artifact with a different writer. "
            "⛔ POPULATION B DOES NOT RE-SWEEP THE ESTATE. It spans exactly what wave 3 chose to "
            "card, and wave 3's own decomp states on its face that its subject set enumerates "
            "writers we can FIND, never every writer that EXISTS."
            % (base_count, prior["method"], len(cards), PIN,
               acts["enrich"], len(enriched), acts["add"], acts["unresolved"],
               len(rows), acts["enrich"], acts["add"], acts["unresolved"])),
        "population_searched": (
            "(A) %s || (B) org/**/D11_CARDS_W3/*.json across all lanes -- %d cards from %d lane "
            "directories, the complete wave-3 card population as it stood at compile time. A card "
            "landing after this run is NOT represented; re-run the compiler."
            % (prior["population_searched"], len(cards),
               len({os.path.dirname(f) for f in _diag["admitted"]}))),
        # ⛔ parts_registered REMOVED 2026-08-27 on my own ruling in 75051 (a), 1.0.0_SA_CTO~X GO
        # in 75063. A NUMBER A MACHINE CAN DERIVE MUST NOT ALSO BE TYPED: it sat beside parts[] as
        # a second copy of len(parts), and JSON Schema cannot express the equality between them, so
        # the only thing preventing drift was this generator computing it correctly. THAT IS WHY THE
        # DEFECT NEVER FIRED AND WHY IT STAYED INVISIBLE -- 1.0.0_SA_CTO~X's point, and it is right.
        # Consumers compute len(parts). SEQUENCE: this removal lands FIRST, then 1.0.0_SA_CTO~X
        # removes the property from the schema -- never an invalid state in either direction.
        # ⛔ DERIVED FROM THE UNRESOLVED ROWS, NOT TYPED BESIDE THEM. The first version hardcoded a
        # sentence about the ONE unresolved row that existed then; when 3.0.0_SA_CVO~X's 74902 attack
        # moved cse_store PATH B to unresolved, a typed list would have silently kept saying ONE.
        # That is the typed-beside-derived class this session keeps producing, so the list is
        # generated from the map and cannot disagree with it.
        "known_unsearched": list(prior.get("known_unsearched") or []) + [
            "DELIBERATELY NOT REGISTERED -- %s :: %s" % (r["card_subject"], r["evidence"])
            for r in rows if r["action"] == "unresolved"
        ] + [
            "The wave-3 card population is the writers wave 3 SELECTED, not a fresh estate sweep. "
            "Any materializer outside that selection is invisible to population B.",
            "L0 `generation` holds ONE materializer/standing/cadence/trigger; graph_nodes has THREE "
            "measured writers and graph_edges TWO. Where writers disagree the pre-existing standing "
            "is RETAINED and the disagreement recorded in evidence -- the manifest cannot currently "
            "express per-writer standing, so that dimension is UNREPRESENTED rather than resolved.",
        ],
    }

    # ---- PARTS_VS_OBJECTS, DERIVED AFTER THE DENOMINATOR OBJECT EXISTS --------------
    # ⛔ MOVED HERE from before the replacement, 4.0.0_SA_CRO~A pre-commit finding. Appending
    # to out["denominator"] before `out["denominator"] = {...}` wrote through the shallow
    # alias into base's FROZEN method, which the new object then embedded as population A's
    # "unchanged" method -- so the 42-part split was emitted MIS-ATTRIBUTED to the 39-part
    # population rather than discarded. Order is the whole fix.
    # ⛔ 4.0.0_SA_CRO~A's instruction: prefer DERIVING this after the final population exists over
    # freezing another count in base39 prose. base39 is an INPUT; a count frozen in an input is
    # stale the moment the population changes, and it had (39 -> 42).
    # KEYED ON home_space == "none", the DECLARED ENUM -- not on `basis` (which was carrying two
    # meanings) and not on a prose prefix (which was the same defect one field over,
    # 1.0.0_SA_CTO~X ruling 75231).
    NON_ENUMERABLE_FAMILIES = {"kuzu_nessie_db.rebuild.tmp.SET"}
    ENUMERABLE_SETS = ("_build_manifest.json.SET", ".comp-graph/platinum.CACHE_SET")

    # ---- member_set EMITTED FIRST, MEMBERS DERIVED FROM EACH PART'S OWN HOME ---------
    # 4.0.0_SA_CRO~A rework items 1 + 3 against 5e210c95fd. The prior cut hand-typed
    # ["kuzu_nessie_db", "kuzu_db", "kuzu_stitch_db"] as members: those are the brace
    # ALTERNATIVES, not artifact identities -- and each one is the id of a DIFFERENT PART
    # in this same manifest, so the member array named three other parts. The home is the
    # authoritative identity and the expansion is total, so DERIVE, never retype.
    def _expand_braces(text):
        """FULL RECURSIVE expansion. A single-group parser under-counted a nested pattern
        at three seats; this handles nesting and the empty alternative in `{,.wal}`."""
        i = text.find("{")
        if i < 0:
            return [text]
        depth = 0
        for j in range(i, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
        else:
            raise SystemExit("REFUSING TO EMIT -- unbalanced brace in a home: %r" % text)
        head, body, tail = text[:i], text[i + 1:j], text[j + 1:]
        alts, d, cur = [], 0, ""
        for ch in body:
            if ch == "{":
                d += 1
            elif ch == "}":
                d -= 1
            if ch == "," and d == 0:
                alts.append(cur)
                cur = ""
            else:
                cur += ch
        alts.append(cur)
        expanded = []
        for a in alts:
            expanded.extend(_expand_braces(head + a + tail))
        return expanded

    _by_id = {p["id"]: p for p in out["parts"]}
    for _pid in ENUMERABLE_SETS:
        _p = _by_id[_pid]           # KeyError is the loud failure; a silent skip is not
        _mem = _expand_braces(_p["home"])
        assert not any("{" in m or "}" in m for m in _mem), (
            "brace survived expansion for %s: %s" % (_pid, _mem))
        assert len(_mem) == len(set(_mem)), "duplicate member for %s: %s" % (_pid, _mem)
        assert len(_mem) >= 2, (
            "a %d-member set is the ABSENT case wearing the PRESENT case's shape (%s)"
            % (len(_mem), _pid))
        assert _p["basis"] != "absent", "member basis cannot be `absent` (%s)" % _pid
        _p["member_set"] = {
            "enumerable": True,
            "members": _mem,
            "basis": _p["basis"],
            "evidence": (
                "MEMBER IDENTITIES DERIVED, NOT TYPED: full recursive brace expansion of this "
                "part's own `home`, which is the authoritative artifact identity. The part's own "
                "vintage.method records a stat on each member. NOTHING IS DERIVED FROM THE PART "
                "ID -- a brace pattern is a claim about a set, and the id is not the pattern."),
            "owner": _p["owner"],
        }

    # ---- the RUNTIME FAMILY, under 1.0.0_SA_CTO~X's rework12 ruling @8e95441c36 -------
    # 4.0.0_SA_CRO~A held this shape (rework item 2) pending a representation that preserves
    # BOTH sibling forms and the source provenance. That ruling landed: `variant_suffixes` is
    # REQUIRED under enumerable=false ([] is the claim "no companions"), the placeholder names
    # name the VARYING QUANTITY (<monotonic_ns>, never <mono>), and the literal segments
    # INCLUDE THE PATH -- the template is the family's HOME shape. Emitting under it now.
    _nef = _by_id["kuzu_nessie_db.rebuild.tmp.SET"]
    _stem = _nef["home"].split("{", 1)[0]
    _groups = re.findall(r"\{([^{}]*)\}", _nef["home"])
    assert len(_groups) == 2, (
        "the runtime family's home is not <stem>{instances}{siblings}: %r" % _nef["home"])
    # DERIVED, not typed: the companion axis is the LAST brace group's non-empty alternatives.
    # ⛔ rework14 @b238f34351 -- an OBJECT KEYED BY SUFFIX, never an array: a JSON array's order
    # is DATA, so [".lock",".wal"] and [".wal",".lock"] are byte-, schema- and digest-distinct
    # spellings of one claim, and an object makes that ambiguity INEXPRESSIBLE rather than
    # forbidden by instruction.
    #
    # ⛔ 4.0.0_SA_CRO~A's BLOCKING SEMANTIC FORK, RESOLVED BY MEASUREMENT, NOT BY PREFERENCE.
    # Deriving the key set FROM THE OBSERVED HOME cannot certify closure -- it certifies one
    # 2026-08-25 stat. And the "prove .wal is exactly always-minted" branch is REFUTED at source
    # by this estate's own code, three independent sites:
    #   kuzu_incremental_refresh.py:315  "do NOT copy the .wal (A CLEAN CHECKPOINT)" -> after a
    #                                    clean checkpoint there is NO .wal to copy
    #   kuzu_stitch_load.py:64           `if os.path.exists(args.db + ".wal")`  -> conditional
    #   kuzu_nessie_load.py:129-131      `wal = ...; if os.path.exists(wal)`    -> conditional
    # ⛔ AND THE TRUE PRODUCER IS UNREADABLE: kuzu 0.11.3's suffix behaviour lives in the compiled
    # _kuzu.cp312-win_amd64.pyd. The only Python-level "lock" hits in that package are
    # threading.Lock() -- A TOKEN COLLISION, not a file suffix, and quoting them as producer
    # evidence would be the wrong-population read this manifest exists to refuse.
    # SO: THESE ARE POSSIBLE CONDITIONAL COMPANIONS, NOT AN EXACT MINTED SET, and the key set is
    # derived from the nearest thing to producer authority the estate actually has -- its own
    # side-artifact cleanup tuples -- CROSS-CHECKED ACROSS TWO INDEPENDENT SITES.
    # ⛔ AUTHORITY_HOME is the file the contract NAMES for the companion repertoire (_rm_kuzu);
    # the second site is a CROSS-CHECK, not a second authority. rework16 makes this a DIFFERENT
    # pin from pattern_source_*: two axes, two producers, two pins.
    AUTHORITY_HOME = "infra/aws/globgrph/_canonical.py"
    CROSSCHECK_HOME = "infra/aws/globgrph/kuzu_incremental_refresh.py"

    def _side_artifact_suffixes():
        """Parse the `for <suffix> in (...)` cleanup tuples out of both owning sites and return
        (suffixes, authority_line). Two independent declarations of one set: if they DISAGREE,
        REFUSE -- a silently diverged pair would let one site's superset masquerade as the
        estate's answer. THE LINE IS RETURNED FROM THE AST NODE, never typed beside it."""
        import ast as _ast
        seen, lineno = {}, {}
        for _rel in (AUTHORITY_HOME, CROSSCHECK_HOME):
            _tree = _ast.parse(open(os.path.join(WS, _rel), encoding="utf-8").read())
            for _n in _ast.walk(_tree):
                if not isinstance(_n, _ast.For) or not isinstance(_n.iter, _ast.Tuple):
                    continue
                _vals = [e.value for e in _n.iter.elts
                         if isinstance(e, _ast.Constant) and isinstance(e.value, str)]
                if len(_vals) == len(_n.iter.elts) and _vals and all(
                        re.fullmatch(r"\.[A-Za-z0-9]+", v) for v in _vals):
                    seen.setdefault(_rel, set()).update(_vals)
                    lineno.setdefault(_rel, _n.lineno)
        if len(seen) != 2:
            raise SystemExit(
                "REFUSING TO EMIT -- a side-artifact cleanup tuple was not found at every "
                "owning site; the companion axis has no derivable authority: %s" % sorted(seen))
        _sets = list(seen.values())
        if _sets[0] != _sets[1]:
            raise SystemExit(
                "REFUSING TO EMIT -- the two side-artifact sites DISAGREE, so neither is the "
                "estate's answer: %s" % {k: sorted(v) for k, v in seen.items()})
        return sorted(_sets[0]), lineno[AUTHORITY_HOME]

    # The per-suffix STATEMENTS are knowledge and cannot be sliced out of a path, so they are
    # authored against source; a derived key with no authored statement REFUSES TO EMIT.
    # Each value states THE CONDITION under which that companion appears (rework16). ⛔ THREE OF
    # THE FOUR CONDITIONS ARE NOT DETERMINABLE FROM HERE and say so: kuzu 0.11.3's file
    # behaviour is inside a compiled .pyd, and a CLEANUP list names what may be REMOVED, never
    # when it is MINTED. Writing a plausible condition for those three would manufacture
    # substrate, which is the failure Rule 28 exists to refuse -- an unknown condition stated as
    # unknown is a claim a consumer can reject on; an invented one is not.
    # ⛔ `mint` IS THE CLOSURE AXIS, PER COMPANION -- and NONE of these is `always`, because
    # `always` requires evidence that the producer's code makes it unconditional and no such
    # evidence exists from here: kuzu 0.11.3's file behaviour is inside a compiled .pyd.
    # ONE OF THE FOUR IS `conditional` ON MEASURED GROUNDS; THREE ARE `unknown`. Those three are
    # NOT weak conditionals -- a removal list names what MAY BE DELETED and never says when the
    # artifact is MINTED, so the producer's rule is UNREAD, and reading a repertoire entry as a
    # mint rule would be the wrong-population read this manifest exists to refuse.
    # RESOLVED at rework18: `condition` is REQUIRED iff mint=conditional and PROHIBITED
    # otherwise, so `note` carries artifact meaning ONLY and the two intents have two fields.
    # The tension this comment used to describe is closed in the frozen contract; leaving the
    # old text in place would have made a reader hunt for a defect that no longer exists.
    _COMPANION_MEANING = {
        ".wal": {
            "mint": "conditional",
            "note": "write-ahead log for the rebuild tmp DB",
            "condition": ("a rebuild is mid-flight, or one exited abnormally and orphaned it; "
                          "absent after a clean checkpoint"),
        },
        ".lock": {
            "mint": "unknown",
            "note": "kuzu single-file-DB lock side-artifact; not observed in the 2026-08-25 stat",
        },
        ".shadow": {
            "mint": "unknown",
            "note": ("kuzu single-file-DB shadow side-artifact; not observed in the 2026-08-25 "
                     "stat"),
        },
        ".tmp": {
            "mint": "unknown",
            "note": ("kuzu single-file-DB temporary side-artifact; not observed in the "
                     "2026-08-25 stat"),
        },
    }
    _companion_keys, _authority_line = _side_artifact_suffixes()

    # ⛔ THE PATTERN'S LINE IS DERIVED TOO. It was typed as 288 beside a parser that already
    # knows how to find it -- a typed number beside a derived one always goes stale, and this
    # one pins a file no lane here controls.
    PATTERN_HOME = "infra/aws/globgrph/_canonical.py"

    def _pattern_producer_line():
        """Line of the `return f"...rebuild.tmp..."` inside _unique_tmp. Refuses on 0 or >1 --
        two producers of one template is the identity split this contract exists to prevent."""
        import ast as _ast
        _tree = _ast.parse(open(os.path.join(WS, PATTERN_HOME), encoding="utf-8").read())
        _hits = []
        for _fn in _ast.walk(_tree):
            if not (isinstance(_fn, _ast.FunctionDef) and _fn.name == "_unique_tmp"):
                continue
            for _n in _ast.walk(_fn):
                if isinstance(_n, _ast.Return) and isinstance(_n.value, _ast.JoinedStr):
                    _hits.append(_n.lineno)
        if len(_hits) != 1:
            raise SystemExit(
                "REFUSING TO EMIT -- _unique_tmp has %d f-string returns, not exactly 1; the "
                "family template has no single producing statement to pin: %s"
                % (len(_hits), _hits))
        return _hits[0]

    _pattern_line = _pattern_producer_line()
    _observed = sorted({a for a in _groups[-1].split(",") if a})
    assert all(re.fullmatch(r"\.[A-Za-z0-9]+", c) for c in _companion_keys), (
        "a derived companion suffix is not a real filename suffix: %s" % _companion_keys)
    # ⛔ THE OBSERVED SET MUST BE A SUBSET OF THE DECLARED ONE. If a home carries a companion the
    # cleanup sites do not name, the estate is leaking an artifact nothing reaps -- refuse loudly
    # rather than quietly widen the claim to cover it.
    _unnamed = [c for c in _observed if c not in _companion_keys]
    assert not _unnamed, (
        "REFUSING TO EMIT -- the home carries a companion NO cleanup site names, so something "
        "is minting an artifact nothing reaps: %s" % _unnamed)
    _unstated = [c for c in _companion_keys
                 if not (_COMPANION_MEANING.get(c) or {}).get("note")]
    assert not _unstated, (
        "REFUSING TO EMIT -- a companion suffix has no authored statement of what it holds; a "
        "bare suffix is the loud-but-unresolvable class: %s" % _unstated)
    # The frozen contract now binds every one-line field to $defs/one_line_text, which names
    # eight terminator classes explicitly. This emitter-side refusal is therefore REDUNDANT with
    # the schema rather than compensating for it -- kept as a cheap second arm, and labelled as
    # redundant so nobody reads it as evidence the schema is still open.
    _multiline = [(c, k) for c in _companion_keys
                  for k, v in _COMPANION_MEANING[c].items()
                  if chr(10) in v or chr(13) in v]
    assert not _multiline, (
        "REFUSING TO EMIT -- a companion text spans lines; a multiline value is unreadable in "
        "every consumer that renders one line: %s" % _multiline)
    # ⛔ `always` IS A CLOSURE CLAIM AND CARRIES ITS PROOF OR IT IS NOT MADE. Enforced here too,
    # not only in the schema, because this emitter is the thing that would make the claim.
    # rework18 made the three branches EXCLUSIVE: always needs evidence and forbids condition;
    # conditional needs condition and forbids evidence; unknown carries neither. Enforced here
    # too, because this emitter is the thing that would make the claim.
    _REQUIRED_BY_MINT = {"always": "evidence", "conditional": "condition", "unknown": None}
    _mint_shape = []
    for c in _companion_keys:
        _m = _COMPANION_MEANING[c]["mint"]
        _need = _REQUIRED_BY_MINT[_m]
        _extra = [k for k in ("evidence", "condition")
                  if k != _need and k in _COMPANION_MEANING[c]]
        if _need and not _COMPANION_MEANING[c].get(_need):
            _mint_shape.append("%s: mint=%s without %s" % (c, _m, _need))
        if _extra:
            _mint_shape.append("%s: mint=%s carries %s" % (c, _m, _extra))
    assert not _mint_shape, (
        "REFUSING TO EMIT -- a companion's payload does not match its mint branch; mint=always "
        "without evidence is the withdrawn closure claim re-made one level down: %s"
        % _mint_shape)
    _companions = {c: _COMPANION_MEANING[c] for c in _companion_keys}
    _nef["member_set"] = {
        "enumerable": False,
        "pattern": _stem + "<pid>.<monotonic_ns>.<uniq>",
        "pattern_source_home": PATTERN_HOME,
        "pattern_source_line": _pattern_line,
        "variant_suffixes": _companions,
        "variant_suffixes_source_home": AUTHORITY_HOME,
        "variant_suffixes_source_line": _authority_line,
        # ⛔ `unknown`, NOT `partial`, AND THE DIFFERENCE IS THE WHOLE POINT. Both other values
        # presuppose that variant_suffixes_source_home names the MINTING producer -- closed_at
        # _source says "these are ALL it can mint", partial says "more may exist elsewhere IN
        # THE PRODUCER". The pinned file is a REMOVAL repertoire (_rm_kuzu), and the thing that
        # actually mints these is kuzu's compiled _kuzu.cp312-win_amd64.pyd, which nobody here
        # can read. Completeness is therefore NOT ESTABLISHED, and claiming `partial` would
        # quietly assert the cleanup list is the producer.
        "variant_suffixes_completeness": "unknown",
        "basis": _nef["basis"],
        "evidence": (
            "INSTANCE AXIS, UNBOUNDED: _unique_tmp at _canonical.py:288 builds the name from "
            "os.getpid() + time.monotonic_ns() + next(_UNIQ) (an itertools.count at :37), and "
            "_gc_stale_tmps (:291, called from the rebuild path) reaps them, so TOTAL CARDINALITY "
            "IS UNDEFINED and no member list can be true of this family. The literal prefix is the "
            "part's own home stem, derived here rather than retyped. COMPANION AXIS, FINITE: "
            "derived from the home's own sibling brace group; kuzu writes a <db>.wal beside each "
            "single-file DB (:179-186). ⛔ COMPANION AXIS IS POSSIBLE-CONDITIONAL, NOT AN EXACT "
            "MINTED SET, and NO EXACT PER-INSTANCE CARDINALITY IS CLAIMED: an instance carries "
            "1 + a SUBSET of these keys, so the count is bounded above by 1 + 4 and is not "
            "defined for the family. `.wal` is REFUTED as always-minted at three sites in this "
            "estate's own code -- a CLEAN CHECKPOINT leaves none "
            "(kuzu_incremental_refresh.py:315), and kuzu_stitch_load.py:64 and "
            "kuzu_nessie_load.py:129-131 both guard it with os.path.exists. The KEY SET is "
            "the PRODUCER'S REPERTOIRE -- what it CAN mint, never a closure claim over any one "
            "instance -- derived from the estate's side-artifact cleanup tuples and "
            "cross-checked across TWO independent sites which must agree or the emit refuses. "
            "Its authority is pinned SEPARATELY from the pattern's, because the name template "
            "and the companion repertoire are two axes with two producers, and BOTH SOURCE "
            "LINES are returned from parsed AST nodes rather than typed beside them. THE TRUE PRODUCER IS "
            "UNREADABLE: kuzu 0.11.3's behaviour is inside a compiled .pyd, so closure cannot be "
            "certified by anyone from here -- stated as a limit, not walked past. Only `.wal` "
            "was observed in the part's 2026-08-25 stat; the other three are declared-possible "
            "and unobserved, which an after-the-fact stat cannot distinguish from absent."),
        "owner": _nef["owner"],
    }

    _absent = [p for p in out["parts"] if p.get("home_space") == "none"]
    _present = [p for p in out["parts"] if p.get("home_space") != "none"]
    # THE PARTITION IS NOW DERIVED FROM THE EMITTED member_set, not from a parallel table.
    _enum = [p for p in _present if p.get("member_set", {}).get("enumerable") is True]
    _nonenum = [p for p in _present if p.get("member_set", {}).get("enumerable") is False]
    _single = [p for p in _present if "member_set" not in p]
    assert len(_single) + len(_enum) + len(_nonenum) == len(_present), "partition does not sum"
    assert {p["id"] for p in _enum} == set(ENUMERABLE_SETS), (
        "the emitted enumerable sets are not the declared ones: %s" % sorted(p["id"] for p in _enum))
    assert {p["id"] for p in _nonenum} == NON_ENUMERABLE_FAMILIES, (
        "the emitted non-enumerable families are not the declared ones: %s"
        % sorted(p["id"] for p in _nonenum))
    # THE ONLY OBJECT FIGURE, DERIVED FROM THE EMITTED ARRAYS THEMSELVES.
    _enum_objects = sum(len(p["member_set"]["members"]) for p in _enum)

    # CONTROL: the W3 compile must PRESERVE the C3 triplet it inherits from base39.
    _EXPECTED_UNBUILT = {"affinity_matrix", "similarity_network_fusion", "identity_and_succession"}
    assert {p["id"] for p in _absent} == _EXPECTED_UNBUILT, (
        "the unbuilt set is not the C3 triplet after compile: %s"
        % sorted(p["id"] for p in _absent))
    assert all(p["basis"] == "held" and p["home"] == "NONE" for p in _absent), (
        "the compile did not preserve the C3 triplet (basis=held, home=NONE, home_space=none)")

    out["denominator"]["method"] += (
        " PARTS_VS_OBJECTS, DERIVED AT COMPILE over the FINAL population, NO SINGLE OBJECT TOTAL: "
        "%d parts = %d present + %d recording an ABSENCE (the unbuilt C3 stages, keyed on "
        "home_space=='none' -- their `basis` is `held` on a named authority and their UNBUILT-NESS "
        "is a different question from their epistemic basis). The %d present parts partition as %d "
        "singleton + %d ENUMERABLE set rows covering %d named members + %d NON-ENUMERABLE family "
        "whose members are runtime-named and whose CARDINALITY IS UNDEFINED. ⛔ NO TOTAL "
        "DISTINCT-OBJECT COUNT EXISTS FOR THIS POPULATION and none is printed -- a total spanning a "
        "family of undefined cardinality would be a number the estate does not have. The enumerable "
        "subtotal is %d objects across %d set rows and is the only object figure quotable here."
        % (len(out["parts"]), len(_present), len(_absent), len(_present), len(_single),
           len(_enum), _enum_objects, len(_nonenum),
           _enum_objects, len(_enum)))


    # ⛔ FINAL-STATE CONTROL, on the EMITTED object rather than on the logic that built it.
    # My static controls tested the computation and could not have seen the mis-attribution,
    # because the computation was correct and its DESTINATION was wrong.
    _final = out["denominator"]["method"]
    assert "PARTS_VS_OBJECTS, DERIVED AT COMPILE" in _final, (
        "the derived split is not in the EMITTED method")
    assert ("%d parts = %d present" % (len(out["parts"]), len(_present))) in _final, (
        "the emitted split does not carry the FINAL population counts")
    for _legacy in ("14 member objects", "47 DISTINCT OBJECTS", "6-member SET row",
                    "3 are SET rows"):
        assert _legacy not in _final, "LEGACY claim survives in the emitted method: %r" % _legacy

    # ---- RECEIVERS: 42/42 CARRIED, 0/42 DECLARED ----------------------------------
    # 4.0.0_SA_CRO~A 75304 + rework items 4 and 5. 0.0.0_AB_MSTR's bar is TWO NUMBERS:
    # (1) EMISSION -- 42 of 42 parts CARRY all four receivers with a coherent claim_status;
    # (2) DECLARATION -- the declared/unknown split printed beside it, never alone.
    # NOTHING IS SYNTHESISED. The compiler admits exactly the registry's extension_population
    # (13 members, digest-pinned) and exact card subject.id -> part.id among them is ZERO,
    # measured. A glob can report an unlisted candidate and can admit nothing. No payload is
    # taken from w3_card_part_map (an ARTIFACT-LOCATION join, right source for where a writer's
    # output lives, WRONG source for which part a card's trust block qualifies) or from cards the
    # compiler does not admit.
    #
    # ⛔ AND "0 DECLARED" IS ONE NUMBER OVER THREE DIFFERENT FACTS. The evidence is per field
    # because the remedies do not move together (Rule 24 iv). ⛔ EACH RECEIVER IS BLOCKED AT
    # SEVERAL INDEPENDENT LAYERS AND THE LAYER SET IS THE POINT -- an earlier version of this
    # comment said failure_mode was "one glob line from declared" and that is WITHDRAWN
    # (1.0.0_SA_CTO~X 75362, verified in this file: ZERO code paths assign a declared receiver):
    #   failure_mode  SOURCE PAYLOAD COMPLETE (23/23 W4 exact matches) + REGISTRY admission
    #                 blocked + schema-bound TRANSFORM absent + no COMPILER path that declares
    #   key           the three above, and SOURCE ABSENT TOO -- SUBSTRATE_CARD.v2 has no
    #                 key_expression field, so there is nothing to admit or transform
    #   grain         the three above, and SOURCE ABSENT TOO -- no authored grain projection
    #                 exists in any card, admitted or not
    # ⛔ NO GLOB CHANGE REACHES ANY OF THEM, AND THERE IS NO LONGER A GLOB TO CHANGE: admission
    # moved to card_population_registry.v1.json, and a discovery pattern now only REPORTS.
    # W3-only remains INTENTIONAL-BUT-TEMPORAL; adding a receiver source means adding a member
    # to that receiver's population WITH a transform_version, which no transform can supply.
    _R_SCOPE = (
        "ADMISSION IS BY REGISTRY, NOT BY GLOB (4.0.0_SA_CRO~A's ruling, landed): the "
        "compiler reads card_population_registry.v1.json, whose extension_population pins "
        "13 members by path + SHA256 + subject.id, and every member is verified on all "
        "three axes before it is read. Exact card subject.id -> part.id among them = 0, "
        "measured by this lane. The discovery glob can only REPORT an unlisted candidate. "
        "The three receiver_source_populations are EMPTY, each with its own written "
        "admission predicate. ")
    _R_UNOWNED = ("UNOWNED -- needs an admitted-card registry and a schema-bound "
                  "card-to-L0 transform. THE REGISTRY NOW EXISTS -- "
                  "card_population_registry.v1.json, with this receiver's own population, its "
                  "structured admission predicate and its blocking-layer set. The transform "
                  "does not.")
    _R_EV = {
        "grain": (
            _R_SCOPE
            + "A SOURCE FACT, INDEPENDENT OF THE GLOB: no authored grain projection exists to "
            "admit. 1.0.0_SA_CTO~X measured the 23 exact-match cards outside the admitted glob "
            "and found an authored grain projection in 0 of 23 -- no key containing 'grain' "
            "anywhere in them (75350, their instrument, cited not re-derived). Widening the "
            "admitted population would not move this receiver."),
        "key": (
            _R_SCOPE
            + "A KNOWLEDGE FACT, INDEPENDENT OF THE GLOB: L0 requires key_expression and "
            "SUBSTRATE_CARD.v2's trust.key HAS NO SUCH FIELD. It carries seven of the eight "
            "L0-required fields -- identity_space, key_is_stable, crosses_spaces, "
            "declared_mapping, basis, evidence, owner -- i.e. every PROPERTY of the key and "
            "never the key itself (1.0.0_SA_CTO~X 75342). No card population of any size can "
            "supply a declared key, so carding harder cannot move this receiver."),
        "failure_mode": (
            _R_SCOPE
            + "BLOCKED AT FOUR INDEPENDENT LAYERS -- SOURCE PAYLOAD COMPLETE, but REGISTRY "
            "admission blocked, schema-bound TRANSFORM absent, and NO COMPILER PATH DECLARES. "
            "The PAYLOADS EXIST: "
            "1.0.0_SA_CTO~X measured trust.failure_mode complete in 23 of 23 exact-match cards "
            "outside the admitted population (75350). ⛔ BUT ADMITTING THEM WOULD DECLARE "
            "NOTHING: it makes 23 payloads REACHABLE and this compiler has NO CODE PATH THAT "
            "ASSIGNS A DECLARED RECEIVER AT ALL (75362, corrected at source; re-verified in this "
            "file -- 0 assignments of claim_status `declared`, positive control 3 for `unknown`). "
            "That distinction is the whole point: DATA EXISTING is a weaker claim than a value "
            "being reachable, and this is the only receiver where even the weaker one holds. "
            "Doctrine principle 13 still binds the 0 -- a coverage fraction is evidence only if "
            "its denominator comes from outside the instrument's own configuration -- which "
            "is exactly why the wave-numbered glob was retired as the authority: it WAS this "
            "instrument's configuration answering a question about the estate. "
            "⛔ AND THE GLOB ROUTE IS CLOSED BY RULING, NOT MERELY INSUFFICIENT: 4.0.0_SA_CRO~A "
            "ruled W3-only INTENTIONAL-BUT-TEMPORAL and forbade widening the glob; the "
            "successor LANDED as card_population_registry.v1.json with INDEPENDENT NAMED "
            "POPULATIONS rather than one role enum -- extension_population pinning the exact 13 "
            "W3 members for the existing map/enrich path only, and receiver_source_populations "
            "keyed SEPARATELY by grain, key and failure_mode. Overlap across populations is "
            "lawful: W3-extension participation and receiver-source participation are "
            "independent consumer dimensions and one card may lawfully be in both. ALL RECEIVER "
            "SOURCE POPULATIONS START EMPTY because no governed transform exists."),
    }
    _R_OWN = {
        "grain": _R_UNOWNED,
        "key": ("UNOWNED -- needs a key_expression field in SUBSTRATE_CARD.v2 "
                "(4.0.0_SA_CRO~A's contract) BEFORE any registry or transform question"),
        "failure_mode": ("UNOWNED -- and NO SINGLE OWNER CAN CLOSE IT. Three independent "
                         "changes are required and a glob change is NOT among them: an authored "
                         "card_population_registry.v1.json failure_mode receiver-source "
                         "population, one of three keyed independently (4.0.0_SA_CRO~A's ruling, "
                         "landed, which forbids widening the discovery glob), a schema-bound "
                         "card-to-L0 transform with a pinned version, and a "
                         "declaring code path in this compiler, which this lane owns and which "
                         "does not exist at this commit. The registry population itself "
                         "EXISTS and is empty, which is a different claim and the weaker one."),
    }

    # ⛔ setdefault WOULD HAVE PRESERVED a stale declared receiver while the compiler reported
    # 0/42 declared -- a wrong value protected by the very call meant to be conservative
    # (4.0.0_SA_CRO~A rework item 4). Assert the frozen input is clean, then ASSIGN.
    _RFIELDS = ("grain", "key", "failure_mode")
    _preexisting = [(p["id"], f) for p in out["parts"] for f in _RFIELDS if f in p]
    assert not _preexisting, (
        "the input already carries a receiver object; a merge would have hidden it behind a "
        "0/42-declared report: %s" % _preexisting)

    for _p in out["parts"]:
        _p["grain"] = {
            "claim_status": "unknown", "unit": None,
            "basis": "absent", "evidence": _R_EV["grain"], "owner": _R_OWN["grain"]}
        _p["key"] = {
            "claim_status": "unknown", "identity_space": None, "key_expression": None,
            "key_is_stable": None, "crosses_spaces": None, "declared_mapping": None,
            "basis": "absent", "evidence": _R_EV["key"], "owner": _R_OWN["key"]}
        _p["failure_mode"] = {
            "claim_status": "unknown", "returns_on_failure": None,
            "distinguishable_from_true_negative": None, "silent_degrade_paths": None,
            "basis": "absent", "evidence": _R_EV["failure_mode"],
            "owner": _R_OWN["failure_mode"]}

    # ---- FINAL-STATE CONTROLS ON THE EMITTED OBJECT --------------------------------
    # Presence and declaration are SEPARATE assertions because they are the bar's two numbers.
    _missing = [(p["id"], f) for p in out["parts"]
                for f in _RFIELDS + ("home_space",) if f not in p]
    assert not _missing, "EMISSION bar fails -- receiver not carried: %s" % _missing
    _declared = {f: sum(1 for p in out["parts"] if p[f]["claim_status"] != "unknown")
                 for f in _RFIELDS}
    assert set(_declared.values()) == {0}, (
        "a declared receiver was synthesised from an unadmitted source: %s" % _declared)
    assert all(p["home_space"] in ("repo_path", "s3_uri", "iceberg_table", "none")
               for p in out["parts"]), "home_space carries a value outside the declared enum"
    # ⛔ EXACT ID EQUALITY, not len()==3: a count passes while the wrong parts carry it.
    _ms_ids = {p["id"] for p in out["parts"] if "member_set" in p}
    assert _ms_ids == set(ENUMERABLE_SETS) | NON_ENUMERABLE_FAMILIES, (
        "member_set landed on the wrong parts: %s" % sorted(_ms_ids))
    # member_set is NEVER required of the other 39: the only shape a singleton could take is a
    # one-member set, which is the defect minItems:2 closed (1.0.0_SA_CTO~X 75331).
    _singletons = [p["id"] for p in out["parts"] if "member_set" not in p]
    assert len(out["parts"]) == len(_ms_ids) + len(_singletons), (
        "the member_set partition does not sum over the emitted parts")

    # ---- validate, with the negative control ---------------------------------------
    v = Draft202012Validator(load_json_strict(SCHEMA))
    errs = sorted(v.iter_errors(out), key=lambda e: list(e.path))
    for e in errs[:10]:
        print("L0 SCHEMA ERROR:", list(e.path)[:4], e.message[:180])
    neg = len(list(v.iter_errors({})))

    print("base parts        : %d" % base_count)
    print("cards read        : %d  (from %d lane dirs)"
          % (len(cards), len({os.path.dirname(f) for f in _diag["admitted"]})))
    print("REGISTRY ADMISSION: %d admitted / %d glob candidates / %d UNLISTED %s"
          % (len(_diag["admitted"]), len(_diag["candidates"]), len(_diag["unlisted"]),
             _diag["unlisted"]))
    print("    ^ unlisted candidates are REPORTED, NEVER ADMITTED. A glob is a discovery "
          "instrument; it was being used as an authority boundary and no longer is.")
    print("    receiver source populations: %s -- empty by contract, not by oversight"
          % _diag["receiver_populations"])
    print("map rows          : %d  -> enrich=%d add=%d unresolved=%d  (sums: %s)"
          % (len(rows), acts["enrich"], acts["add"], acts["unresolved"],
             acts["enrich"] + acts["add"] + acts["unresolved"] == len(rows)))
    print("parts enriched    : %d distinct  %s" % (len(enriched), enriched))
    print("parts added       : %d  %s" % (len(added), added))
    print("unresolved        : %d  %s" % (len(unresolved), [r["card_subject"] for r in unresolved]))
    print("PARTS REGISTERED  : %d   (> %d required by the oracle: %s)"
          % (len(out["parts"]), base_count, len(out["parts"]) > base_count))
    # ---- 0.0.0_AB_MSTR's BAR, BOTH HALVES, DERIVED FROM THE EMITTED OBJECT ----------
    # (1) EMISSION is a CONTRACT-SHAPE claim. (2) DECLARATION is a KNOWLEDGE claim.
    # ⛔ (2) IS PER RECEIVER AND IS NEVER SUMMED (amendment 75355): one figure moving
    # 0/42 -> 23/42 would read as one-third of the way to a target when it is one receiver
    # changing state and two staying exactly as unreachable.
    # ⛔ AND THE FATE COLUMN NAMES BLOCKING LAYERS, NOT ONE WORD (correction 75362): the
    # earlier "CONFIGURATION -- one glob line away" was WITHDRAWN because no receiver is one
    # line from declared. Admitting more cards moves the declaration count by ZERO -- there is no
    # transform to run on what it would admit. A LAYER SET is what a reader can act on: it says
    # how many independent things must change, and by whom.
    _BAR = ("home_space", "failure_mode", "key", "grain")
    _FATE = {
        "home_space":   "NONE          mechanical, classified in-compiler from the home, fail-closed",
        "failure_mode": "REGISTRY + TRANSFORM + COMPILER   payloads EXIST (23/23), nothing reads them",
        "key":          "the three above + SOURCE          no key_expression field in the contract",
        "grain":        "the three above + SOURCE          no authored projection exists anywhere",
    }
    _carry = sum(1 for p in out["parts"] if all(f in p for f in _BAR))
    print("BAR (1) EMISSION  : %d of %d parts CARRY all four receivers  -> %s"
          % (_carry, len(out["parts"]),
             "MET" if _carry == len(out["parts"]) else "*** NOT MET ***"))
    print("BAR (2) DECLARATION -- PER RECEIVER, NEVER SUMMED (0.0.0_AB_MSTR 75355 as corrected):")
    for _f in _BAR:
        if _f == "home_space":
            _n = sum(1 for p in out["parts"] if p.get(_f) is not None)
        else:
            _n = sum(1 for p in out["parts"] if p[_f].get("claim_status") != "unknown")
        print("    %-13s %2d/%d declared   blocked at: %s"
              % (_f, _n, len(out["parts"]), _FATE[_f]))
    print("    member_set is NOT ON THIS BAR: applicable to %d of %d parts; requiring it would "
          "force a one-member set on every singleton" % (len(_ms_ids), len(out["parts"])))
    print("VALIDATION ERRORS : %d" % len(errs))
    print("NEGATIVE CONTROL  : %d errors on {} -> %s"
          % (neg, "FIRES" if neg else "*** DEAD CONTROL ***"))

    if errs:
        raise SystemExit("REFUSING TO WRITE -- the recompiled manifest does not validate.")

    # ⛔ THE END-TO-END GATE RUNS BEFORE ANYTHING LANDS. main() used to shape-validate and then
    # WRITE, so a dirty closure could emit an immutable verifier-failing receipt AFTER the
    # manifest was already on disk -- evidence that cannot be corrected because it is immutable
    # and cannot be trusted because its pins do not bind. THE GATE A CONSUMER RUNS MUST BE THE
    # GATE THE PRODUCER PASSES. The manifest is staged, the receipt is built against the staged
    # bytes and fully verified, and only then do both land.
    import tempfile as _tf
    _fd, _stage = _tf.mkstemp(suffix=".json", prefix="stage_",
                              dir=os.path.dirname(out_path))
    try:
        with os.fdopen(_fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, indent=2, ensure_ascii=True, sort_keys=True)
            f.write("\n")
        _receipt = build_receipt(_stage, SOURCE_SNAPSHOT_UTC, reg=load_registry())
        _receipt["describes"]["home"] = os.path.relpath(out_path, WS).replace(os.sep, "/")
        import importlib.util as _il
        _sp = _il.spec_from_file_location("verify_receipt", os.path.join(HERE,
                                                                        "verify_receipt.py"))
        _vr = _il.module_from_spec(_sp)
        _sp.loader.exec_module(_vr)
        _f = _vr.verify(_receipt, actual_home=_receipt["exact_home"])
        if _f:
            raise SystemExit(
                "REFUSING TO WRITE -- the receipt this run would emit FAILS the same gate a "
                "consumer runs (%d findings):\n  %s" % (len(_f), "\n  ".join(_f)))
    finally:
        try:
            os.remove(_stage)
        except OSError:
            pass

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        # ⛔ sort_keys: DETERMINISTIC EMISSION. Two runs producing identical data in
        # different key order are byte-distinct and digest-distinct, so any hash-based
        # comparison reports drift that does not exist -- the CRLF-vs-LF lesson in a
        # different coordinate. Canonicalise where the bytes are WRITTEN; never leave it
        # to each consumer, which is the unenforced-obligation defect this contract has
        # now refused five times.
        json.dump(out, f, indent=2, ensure_ascii=True, sort_keys=True)
        f.write("\n")
    print("OK: wrote %s" % os.path.relpath(out_path, WS).replace(os.sep, "/"))

    # ---- THE GOVERNED EXECUTION RECEIPT ---------------------------------------------
    # ⛔ v0 WAS NINE FREE KEYS WITH NO GOVERNING SCHEMA, so nothing could reject a missing pin,
    # a wrong blob or a collapsed clock -- and three seats quoted its digest as evidence while
    # it was an ungoverned producer self-report. Shape and contract: MANIFEST_RECEIPT.v1.
    receipt = _receipt
    rerrs = list(Draft202012Validator(load_json_strict(RECEIPT_SCHEMA)).iter_errors(receipt))
    if rerrs:
        raise SystemExit(
            "REFUSING TO WRITE A RECEIPT -- it does not satisfy its own governing schema "
            "(%d errors): %s" % (len(rerrs), "; ".join(
                "%s: %s" % ("/".join(str(x) for x in e.path), e.message[:80])
                for e in rerrs[:5])))
    rpath = os.path.join(WS, receipt["exact_home"])
    if os.path.exists(rpath):
        raise SystemExit("REFUSING TO OVERWRITE AN IMMUTABLE RECEIPT at %s -- immutability that "
                         "depends on nobody re-running is not immutability" % receipt["exact_home"])
    with open(rpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=True, sort_keys=True)
        f.write("\n")
    print("OK: receipt %s  artifact sha256 %s"
          % (os.path.relpath(rpath, WS).replace(os.sep, "/"),
             receipt["describes"]["sha256"][:12]))


if __name__ == "__main__":
    import argparse

    _ap = argparse.ArgumentParser(description=__doc__)
    _ap.add_argument("--out", default=None,
                     help="redirect the emission (replay control); default is the real manifest")
    main(_ap.parse_args().out)
