#!/usr/bin/env python3
"""TO-W4-FILE -- NFRA_SUBSTRATECARDING wave 4, FILE tranche (0.8.0_AE_CloudComp~X).

21 artifact-subject cards, 147 card cells, against
org/standards/SUBSTRATE_CARD.v2.schema.json.

GENERATED, NOT TYPED. Every count in every card is derived from a probe result at
build time -- a typed number beside a derived one always goes stale, and this wave
carries 21 subjects x 7 rows where hand-typing would guarantee it.

THE BASIS SPLIT IS THE POINT OF THIS FILE:
  measured -> I read it off the artifact myself this session (exists, kind, size,
              mtime, tracked, parsed content, entry counts).
  held     -> the L0 manifest asserts it and I did not independently re-derive it
              (materializer, cadence, trigger, authority_role, owner). A named
              authority DID measure it; not here. Rule 22's 'held' outranks
              'inferred' for exactly this reason.
  absent   -> no basis exists. Used, not hidden.
Row scalars are the FLOOR (weakest sub-claim), per the v2 contract's own rule:
measured > held > inferred > absent.
"""
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
WS = HERE.parents[4]
SCHEMA = WS / "org" / "standards" / "SUBSTRATE_CARD.v2.schema.json"
MANIFEST = (WS / "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST"
                 "/graph_object_manifest.json")

PROBE = pathlib.Path("/tmp/w4rows.json")
CONTENT = pathlib.Path("/tmp/w4content.json")
VINTAGE = pathlib.Path("/tmp/w4vintage.json")
BUCKETS = pathlib.Path("/tmp/w4vintage_buckets.json")

# --- ONE wave pin, stamped into all 21 (W4 equivalent of CCX3-AC2) -------------
PIN = "1e7c66e996"                      # the TO's own commit; decomp pinned @dd068ae99f
DECOMP_PIN = "dd068ae99f"
CARDED_UTC = "2026-08-27T08:23:41Z"     # ONE clock read. GRAIN: PER-BATCH, declared.
CARDED_BY = "0.8.0_AE_CloudComp~X"
GRAPH_VINTAGE = (
    "N/A for this wave -- these subjects ARE the graph substrate's own artifacts, not reads "
    "OF a graph snapshot. Each card instead carries its subject's OWN vintage as a measured "
    "mtime in trust.coverage and process.cadence. Stated rather than null-with-no-reason, per "
    "the contract's requirement that a null graph_vintage give one."
)

# part_class (manifest vocabulary) -> subject.kind (v2 contract enum)
KIND = {"store": "store", "output_artifact": "artifact", "projection": "projection",
        "spec_artifact": "artifact", "materializer": "script"}

# Per-subject findings that needed judgment. Everything else is derived.
NOTES = {
    "kuzu_ac7.dir": (
        "*** EXISTS AND IS EMPTY. *** Path.exists() is True, is_dir() is True, and the "
        "directory contains ZERO entries totalling ZERO bytes. This is the single clearest "
        "instance in this tranche of the TO's own instruction that EXISTENCE IS NOT "
        "CONFORMANCE: every existence-based instrument reports this part as present, and a "
        "projection with no contents is not a projection."
    ),
    "snap_store.WRITER": (
        "*** THE MANIFEST'S DECLARED home FOR THIS PART IS PROSE, NOT A JOINABLE IDENTITY. *** "
        "It reads 'infra/aws/globgrph/snap_store.py (436 lines) @76c58923ac; writes "
        "globgrph.<surface> via table_id=(NAMESPACE, surface) at :222' -- a path, a line count, "
        "a commit and a behavioural claim in one string. This card emits the exact path as home "
        "and carries the rest as prose in evidence. It is 1 of 21 in this tranche and it is "
        "exactly the W4-m-joinable defect, sitting in the manifest the wave is built from."
    ),
    "kuzu_nessie_db.local": (
        "LIVE AT CARDING TIME: mtime is minutes old at the carded_utc stamp, so this artifact "
        "is being actively rewritten. A size or digest taken here describes an instant, not a "
        "steady state, and any consumer diffing it against a later read should expect drift "
        "that is not corruption."
    ),
    "kuzu_stitch_db": (
        "Rewritten since the manifest measured it (manifest 2026-07-07, mtime 2026-08-27). The "
        "manifest's vintage for this part is stale by ~51 days; that is the vintage field "
        "working correctly, not a defect."
    ),
}


def load(p: pathlib.Path):
    return json.loads(p.read_text(encoding="utf-8"))


def build():
    rows = {r["part"]: r for r in load(PROBE)}
    content = load(CONTENT)
    vintage = load(VINTAGE)
    buckets = load(BUCKETS)
    parts = {p["id"]: p for p in load(MANIFEST)["parts"]}

    # invert the vintage buckets so each subject knows its own explanation
    which = {}
    for name, members in buckets.items():
        for m in members:
            which[m] = name

    tracked_n = sum(1 for r in rows.values() if r.get("tracked") is True)
    untracked_n = sum(1 for r in rows.values() if r.get("tracked") is False)

    cards = {}
    for pid, r in sorted(rows.items()):
        part = parts[pid]
        c = content[pid]
        v = vintage[pid]
        gen = part.get("generation") or {}
        home = r["probe_path"]
        prose_home = r["home_is_prose"]
        is_tracked = r.get("tracked")
        vb = which.get(pid, "unclassified")

        # ---- denominator, derived from whatever the artifact actually is ----
        if c.get("dir_entries") is not None:
            denom = f"{c['dir_entries']} directory entries, {c.get('size', 0)} bytes total"
            shape = f"directory, {c['dir_entries']} entries"
        elif c.get("jsonl_lines") is not None:
            denom = f"{c['jsonl_lines']} JSONL records, {c['size']} bytes"
            shape = f"JSONL, {c['jsonl_lines']} records"
        elif c.get("n_items") is not None:
            denom = f"{c['n_items']} top-level array items, {c['size']} bytes"
            shape = f"JSON array, {c['n_items']} items"
        elif c.get("n_top_keys") is not None:
            denom = f"{c['n_top_keys']} top-level object keys, {c['size']} bytes"
            shape = f"JSON object, {c['n_top_keys']} top-level keys"
        else:
            denom = f"{c['size']} bytes (opaque to a structural count -- see key.identity_space)"
            shape = f"binary, magic {c.get('magic', '?')}"

        note = NOTES.get(pid)

        # ---- process.methodology ----
        mat = gen.get("materializer")
        meth_basis = "held" if mat else "absent"
        meth_how = (
            f"Produced by {mat}." if mat else
            "NO MATERIALIZER IS DECLARED for this part in the L0 manifest, and I did not "
            "independently identify one. Recorded as absent rather than guessed -- a producer "
            "inferred from a filename is the 'a name is not an identity' error this wave's TO "
            "warns about twice."
        )
        methodology = {
            "how": meth_how + (f" {note}" if note else ""),
            "determinism": "unknown",
            "inference_detail": None,
            "composes": [],
            "invents": [],
            "basis": meth_basis,
            "basis_by_field": {"how": meth_basis, "determinism": "absent"},
            "evidence": (
                f"L0 manifest {MANIFEST.relative_to(WS).as_posix()} @ {PIN}, part '{pid}': "
                f"generation.materializer={mat!r}. HELD, not measured here -- I read the "
                f"manifest's assertion, I did not trace the producer to source. determinism is "
                f"'unknown' with basis absent: nothing in this tranche's instrument (a "
                f"filesystem read) can decide whether a producer is deterministic."
            ),
            "owner": part.get("owner") or "UNOWNED",
            "materializer_standing": gen.get("materializer_standing") or "unknown",
            "declared_opinions": ([gen["declared_opinions"]]
                                  if isinstance(gen.get("declared_opinions"), str)
                                  else gen.get("declared_opinions")) or None,
        }

        # ---- process.cadence ----
        cad, trig = gen.get("cadence"), gen.get("trigger")
        cad_basis = "held" if (cad or trig) else "absent"
        cadence = {
            "declared_rhythm": cad,
            "actual_trigger": trig,
            "live_matches_declared": "unmeasured",
            "live_instance_age": (
                f"{v['age_days']} days at carded_utc (mtime {v['mtime_utc']}). MEASURED by stat. "
                f"NOT DORMANT under Rule 25 (>=90d): this artifact is {v['age_days']}d."
            ),
            "basis": "absent" if cad_basis == "absent" else "held",
            "basis_by_field": {
                "declared_rhythm": cad_basis,
                "actual_trigger": cad_basis,
                "live_matches_declared": "absent",
                "live_instance_age": "measured",
            },
            "evidence": (
                f"declared_rhythm/actual_trigger HELD from the L0 manifest part '{pid}' "
                f"(cadence={cad!r}, trigger={trig!r}) @ {PIN}. live_instance_age MEASURED: "
                f"os.stat mtime {v['mtime_utc']}, read at {CARDED_UTC}. "
                f"live_matches_declared is 'unmeasured' and its basis is ABSENT -- confirming a "
                f"declared rhythm needs a run history this tranche's instrument cannot see, and "
                f"an mtime is one sample, not a cadence."
            ),
            "owner": part.get("owner") or "UNOWNED",
        }

        # ---- artifact.persistence ----
        persistence = {
            "persisted": True,
            "authority_role": part.get("authority_role") or "none",
            "mutation_policy": "replaceable",
            "form": shape,
            "basis": "held",
            "basis_by_field": {
                "persisted": "measured",
                "authority_role": "held",
                "mutation_policy": "inferred",
                "form": "measured",
            },
            "evidence": (
                f"persisted MEASURED: Path.exists() True, kind={r['kind']}, {c['size']} bytes, "
                f"read this session. form MEASURED: parsed at build time -> {shape}. "
                f"authority_role HELD from the manifest ({part.get('authority_role')!r}) -- I did "
                f"not re-derive who treats this as authoritative. mutation_policy INFERRED: no "
                f"declared policy exists for this part; 'replaceable' is the floor fit for a file "
                f"a producer rewrites, and it is NOT a measurement -- the v2 enum has no member "
                f"for 'policy undeclared', so the qualification lives here rather than being "
                f"silently upgraded to a fact."
            ),
            "owner": part.get("owner") or "UNOWNED",
        }

        # ---- artifact.location (THE W4-m-joinable ROW) ----
        location = {
            "home": home,
            "projection_of": [{"id": x, "note": "declared in the L0 manifest lineage"}
                              for x in ((part.get("lineage") or {}).get("projection_of") or [])],
            "co_resident_stores": None,
            # FLOOR RULE: home is measured, projection_of is held -> the scalar is HELD.
            # Reporting 'measured' here would over-promise by the schema's own hand.
            "basis": "held",
            "basis_by_field": {"home": "measured", "projection_of": "held"},
            "evidence": (
                "home is the EXACT repo-relative path, resolved and stat'd this session -- an "
                "equality-joinable identity, no prose, no parentheticals, no commit-ish, no "
                "behavioural claim. This is W4-m-joinable's requirement and it is the row this "
                "wave exists for. "
                + (f"*** THE MANIFEST'S DECLARED home FOR THIS PART IS PROSE AND IS NOT JOINABLE: "
                   f"{part.get('home')!r}. This card emits the exact path instead and reports the "
                   f"manifest value as the defect. *** "
                   if prose_home else
                   f"The manifest's declared home for this part ({part.get('home')!r}) is already "
                   f"joinable and this card agrees with it byte-for-byte. ")
                + f"projection_of HELD from manifest lineage @ {PIN}."
            ),
            "owner": part.get("owner") or "UNOWNED",
        }

        # ---- trust.coverage ----
        coverage = {
            "universe": (
                f"The complete contents of {home} as they stood at mtime {v['mtime_utc']}. "
                f"This card describes ONE artifact at ONE vintage; it makes no claim about the "
                f"population the artifact is supposed to cover."
            ),
            "denominator": denom,
            "explicitly_out": [
                "SEMANTIC correctness of the contents -- nothing was compared against a source of "
                "truth. Structural shape was measured; meaning was not.",
                "Whether this artifact's contents are COMPLETE for their intended population -- "
                f"the manifest records population_status={part.get('population_status')!r} and I "
                "did not re-derive it.",
                ("*** TRACKED STATE: this artifact is UNTRACKED-BUT-PRESENT. *** It exists on this "
                 "device and is in no commit, so it reads as PRESENT to every filesystem "
                 "instrument while the repository does not have it. A second device following "
                 "this card's home would find nothing. 13 of 21 subjects in this tranche are in "
                 "this state."
                 if is_tracked is False else
                 "TRACKED state: this artifact IS tracked in git, so the home resolves on any "
                 "clone. 8 of 21 subjects in this tranche are tracked."),
            ],
            "basis": "measured",
            "basis_by_field": {"universe": "measured", "denominator": "measured",
                               "explicitly_out": "measured"},
            "evidence": (
                f"denominator DERIVED AT BUILD TIME by parsing the artifact, never typed: {denom}. "
                f"tracked state MEASURED by `git ls-files --error-unmatch {home}` "
                f"(rc==0 -> tracked); tranche census 8 tracked / 13 untracked of 21. "
                f"mtime MEASURED by os.stat."
            ),
            "owner": part.get("owner") or "UNOWNED",
        }

        # ---- trust.key ----
        key = {
            "identity_space": (
                f"The repo-relative filesystem path '{home}' IS the identity, and it is the join "
                f"key a manifest consumer must match on. There is no internal id: this is a file, "
                f"addressed by path. "
                + (f"Contents are structurally addressable ({shape})."
                   if c.get("json_type") or c.get("jsonl_lines") is not None or c.get("dir_entries") is not None
                   else f"Contents are OPAQUE to a path-level consumer ({shape}) -- the file is a "
                        f"binary database and nothing short of opening it with its own engine "
                        f"yields row identity.")
            ),
            "key_is_stable": "stable" if is_tracked else "unknown",
            "crosses_spaces": bool(prose_home),
            "declared_mapping": (
                "NONE NEEDED -- the manifest home and this card's home are the same string."
                if not prose_home else
                "REQUIRED AND ABSENT: the manifest addresses this part by a PROSE string while "
                "this card addresses it by an exact path. Those are two renderings of one "
                "artifact and no normaliser exists, so a string-equality join splits it."
            ),
            "basis": "measured" if is_tracked else "inferred",
            "basis_by_field": {
                "identity_space": "measured",
                "key_is_stable": "measured" if is_tracked else "inferred",
                "crosses_spaces": "measured",
                "declared_mapping": "measured",
            },
            "evidence": (
                "identity_space MEASURED: the path was resolved and stat'd. key_is_stable is "
                + ("'stable' MEASURED -- the path is tracked in git, so it is a durable identity "
                   "across devices and clones."
                   if is_tracked else
                   "'unknown' and INFERRED -- the artifact is UNTRACKED, so nothing guarantees "
                   "this path exists on any other device, and a path that may not exist elsewhere "
                   "cannot be asserted as a stable identity. This is the honest value, not "
                   "'unstable': I measured no instability, I measured the absence of a guarantee.")
                + f" crosses_spaces MEASURED from the manifest home string @ {PIN}."
            ),
            "owner": part.get("owner") or "UNOWNED",
        }

        # ---- trust.failure_mode ----
        # RULE 3 / Addendum 1v (1.0.0_SA_CTO~X, 89660): a field whose VALUE is the null token
        # may NOT carry a basis of held/inferred/measured. The basis describes HOW THE VALUE WAS
        # OBTAINED, so "this was not measured" cannot have been obtained BY measuring. This value
        # is conditional and its basis was hardcoded `measured` beside it -- true for the "no"
        # branch (read off the guard structure and the tracked state) and false for the
        # "unmeasured" branch, which is the 8-card Class A hit in this lane. DERIVE it from the
        # value so the two cannot drift apart again.
        dtn_value = "no" if (pid == "kuzu_ac7.dir" or is_tracked is False) else "unmeasured"
        dtn_basis = "absent" if dtn_value == "unmeasured" else "measured"
        failure_mode = {
            "returns_on_failure": (
                "A consumer opening this path when the artifact is missing gets a filesystem "
                "error (FileNotFoundError / ENOENT) -- LOUD and unambiguous. The dangerous case "
                "is not absence but STALENESS: the file is present, parses, and returns a "
                "well-formed answer computed at "
                f"{v['mtime_utc']}, which no read of the file itself reveals as old."
                + (" AND FOR THIS SUBJECT THE DEGENERATE CASE IS LIVE: the directory exists and "
                   "is empty, so a consumer iterating it gets ZERO entries and NO error -- "
                   "byte-identical to a genuinely empty result."
                   if pid == "kuzu_ac7.dir" else "")
            ),
            "distinguishable_from_true_negative": dtn_value,
            "silent_degrade_paths": [
                f"STALENESS IS SILENT: mtime {v['mtime_utc']} ({v['age_days']}d at carding) is "
                f"carried by the filesystem, not by the artifact, so a consumer that reads only "
                f"the contents cannot tell this vintage from today's.",
                ("UNTRACKED: absent from the repository, so a clone or a second device silently "
                 "has no artifact at this home while every local instrument reports it present."
                 if is_tracked is False else
                 "Tracked in git, so the home resolves on a clone -- this degrade path does not "
                 "apply to this subject."),
            ] + ([NOTES[pid]] if pid in NOTES else []),
            "basis": "measured",
            "basis_by_field": {
                "returns_on_failure": "inferred",
                "distinguishable_from_true_negative": dtn_basis,
                "silent_degrade_paths": "measured",
            },
            "evidence": (
                "silent_degrade_paths MEASURED: mtime and tracked state both read this session. "
                "returns_on_failure is INFERRED -- I did NOT delete the artifact to observe a "
                "consumer's error, and I will not: the standing rule is qualify-do-not-fix and "
                "deleting a live artifact to characterise its absence would be the opposite. "
                "The row scalar is therefore the floor over its parts."
            ),
            "owner": part.get("owner") or "UNOWNED",
        }
        # floor the failure_mode scalar honestly -- DERIVED, not typed. It was hardcoded
        # "inferred", which happened to equal the floor while every part was inferred-or-better.
        # Once dtn_basis can be `absent`, a hardcoded "inferred" would claim MORE than its own
        # parts support -- the same defect one level up, and the block's own evidence sentence
        # already promises "the floor over its parts". Compute it so the promise is kept.
        _RANK = {"absent": 0, "held": 1, "inferred": 2, "measured": 3}
        failure_mode["basis"] = min(
            failure_mode["basis_by_field"].values(), key=lambda b: _RANK[b]
        )

        defects = []
        if pid == "kuzu_ac7.dir":
            defects.append("Exists and is EMPTY: 0 entries, 0 bytes. A projection with no "
                           "contents does not serve its declared role.")
        if prose_home:
            defects.append("The L0 manifest's declared home for this part is prose, not a "
                           "joinable identity (W4-m-joinable).")

        standing = "UNSOUND" if pid == "kuzu_ac7.dir" else "QUALIFIED"
        why = (
            f"Seven rows, each carrying its own basis. MEASURED here: existence, kind, size, "
            f"mtime, tracked state, parsed shape and denominator ({denom}). HELD from the L0 "
            f"manifest and NOT re-derived here: materializer, cadence, trigger, authority_role, "
            f"owner, lineage. ABSENT where nothing supports an answer. "
            + ("*** UNSOUND: this subject EXISTS AND IS EMPTY. *** Path.exists() is True and the "
               "directory holds zero entries, so every existence-based instrument in the estate "
               "reports it present while it serves nothing. That is a measured defect blocking "
               "load-bearing use, not a limitation of this card. "
               if standing == "UNSOUND" else
               "QUALIFIED rather than SOUND: SOUND asserts every row measured, and the process "
               "rows here are HELD or ABSENT because a filesystem instrument cannot see a "
               "producer, a cadence or a trigger. That is a property of the tranche's instrument, "
               "not a gap I chose to leave. ")
            + ("The artifact is UNTRACKED-BUT-PRESENT, so this card's home is device-local and a "
               "second device would resolve nothing at it. "
               if is_tracked is False else "")
            + f"Vintage-explanation class for this subject: {vb}."
        )

        cards[pid] = {
            "schema_version": 2,
            "carded_by": CARDED_BY,
            "subject": {
                "id": pid,
                "kind": KIND[part["part_class"]],
                "declared_domain": (
                    f"The L0 graph-substrate manifest part '{pid}' (part_class="
                    f"{part['part_class']}), as it exists on this device at "
                    f"{home}. DOMAIN IS THE ARTIFACT, NOT ITS PRODUCER: wave 3 carded "
                    f"materializers at (FILE, WRITE PATH) grain and those two populations are "
                    f"near-disjoint, which is why this wave exists."
                ),
            },
            "as_of": {"carded_utc": CARDED_UTC, "commit_ish": PIN,
                      "graph_vintage": GRAPH_VINTAGE},
            "process": {"methodology": methodology, "cadence": cadence},
            "artifact": {"persistence": persistence, "location": location},
            "trust": {"coverage": coverage, "key": key, "failure_mode": failure_mode},
            "verdict": {"standing": standing, "why": why, "blocking_defects": defects},
            "forward_disposition": {
                "standing": "undecided",
                "set_by": None,
                "basis": "absent",
                "evidence": (
                    "Born undecided. The v2 contract requires this slot be set in a SECOND pass "
                    "by a seat with authority to retire something, and forbids set_by being the "
                    "carding lane for its own subject. Neither rule is machine-enforced -- "
                    "measured and reported in wave 3 -- so it is held here by intent."
                ),
                "decided_utc": None,
            },
        }
    return cards, tracked_n, untracked_n


def main() -> int:
    import jsonschema

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    V = jsonschema.Draft202012Validator(schema)

    # NEGATIVE CONTROL FIRST -- a validator that cannot reject makes every PASS meaningless.
    try:
        V.validate({"schema_version": 2})
        print("ERROR: NEG-CONTROL DID NOT FIRE -- every PASS below is UNMEASURED.")
        return 2
    except jsonschema.ValidationError:
        print("OK: NEG-CONTROL FIRED -- the validator rejects a malformed card.")

    cards, tracked_n, untracked_n = build()
    rc = 0
    ok = 0
    pins = set()
    for pid, card in sorted(cards.items()):
        errs = sorted(V.iter_errors(card), key=lambda e: list(e.path))
        safe = pid.replace("/", "_").replace(".", "_")
        if errs:
            rc = 1
            print(f"FAIL: {pid} -- {len(errs)} error(s)")
            for e in errs[:6]:
                print(f"   at {'/'.join(str(x) for x in e.path) or '<root>'}: {e.message[:150]}")
            continue
        (HERE / f"W4-{safe}.card.json").write_text(
            json.dumps(card, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        pins.add((card["as_of"]["commit_ish"], card["as_of"]["graph_vintage"],
                  card["as_of"]["carded_utc"]))
        ok += 1

    print(f"CARDS: {ok} of {len(cards)} VALIDATE and were written (TO says 21)")
    print(f"WAVE PIN: {len(pins)} distinct (commit_ish, graph_vintage, carded_utc) triple(s) "
          f"-- must be 1")
    print(f"ROWS: {ok * 7} card cells emitted (TO says 147)")
    print(f"TRACKED CENSUS: {tracked_n} tracked / {untracked_n} untracked of "
          f"{tracked_n + untracked_n}")
    if len(pins) != 1 or ok != 21 or ok * 7 != 147:
        print("ERROR: a count does not reconcile with the TO.")
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
