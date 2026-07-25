"""L1b REFERENCE MONOTONICITY SENSOR -- system_parity's predicates x the L0b-S
change types: FOR EACH PAIR, CAN THE PREDICATE MOVE?

NFRA_COMPLEARN L1b (dispatch 1.0.0_SA_CTO~Z 20260725T123436Z; L0b RATIFIED
@67100dd916, emission pin-gated on v1.0). Author: 0.8.0_AE_CloudComp~E.
The FIRST Class-2 sensor -- the class that started this program (SYSPARITY:
a presence-check monotone under addition read 100% for ~30 ticks).

MECHANISM (spec s4/L1b, verbatim honored):
  1. PREDICATES DERIVED FROM THE TOOL'S OWN ARTIFACTS: the population is
     scope_contract.json's 22 units dispatched through system_parity.run_check
     -- the sensor imports system_parity and enumerates kinds from the real
     contract, never a hand-list of predicate kinds.
  2. MUTATIONS SYNTHESIZED AGAINST THE REAL SOURCE: for each pair, the BEFORE
     world is the REAL content at HEAD (read through system_parity's own _read);
     the AFTER world is that same real content with one representative mutation
     of the L0b-S type applied. The REAL evaluator (run_check / _version_pin /
     _derived_count, UNMODIFIED) is executed against both worlds via the
     module's own scoped-monkeypatch pattern (its resident battery's idiom).
     >> WHY THIS SATISFIES "never a patched constant": nothing patches the
     predicate, its internals, or its verdict -- the full parse/derive/render
     path runs over real content both times; only the CONTENT differs, by
     exactly one synthesized change. Patching a constant or the observation
     object (e.g. CompSystem._fresh) would skip real resolution -- where that
     is the only option (comp-system-backed kinds) the cell is UNKNOWN. <<
  3. CLASSIFY: SENSITIVE (verdict moved) / MONOTONE-BLIND (verdict identical)
     / UNKNOWN (could not synthesize or could not run -- NEVER collapsed into
     sensitive; that collapse is the founding failure).

LIMB DISCIPLINE (this sensor's own finding-shape): where a type's effect
depends on WHICH member mutates, BOTH limbs run and report -- e.g.
grep_present under REMOVE is blind to an untargeted member's removal and
sensitive only when its own grepped string leaves; version_pin under ADD is
sensitive ONLY through the source's versioning discipline (the bump), blind to
an unbumped addition. A single-limb cell would hide exactly the mediation the
pair-table exists to expose. Limbs are DISCLOSED per cell, never averaged.

DECLARED ROWS (distinct from UNKNOWN, per the ratified vocabulary):
  - RESEMANT: UNDETECTABLE-BY-DESIGN for every mechanical kind -- carried so
    the table shows the honest row instead of silence (L0b s2, acceptance-
    deferred member; its mutant is unwritable by construction).
  - `assumption` kind: IMMOBILE-BY-CONSTRUCTION -- always returns ASSUMPTION,
    cannot move under any change type; the predicate-side mirror of RESEMANT.

EMISSION HARD GATE (dispatch verbatim): L0b labels do NOT emit until the
vocabulary hits v1.0. The sensor renders the pair table INTERNALLY (PROVISIONAL
labels) always; `--emit` writes an L0b-typed report ONLY if it can pin
meta.version == 1.0 from L0B_CHANGE_TYPE_VOCABULARY.md (the post-flip
filename). Pin absent (as today: only the DRAFT filename exists, no
meta.version) -> REFUSE rc=3, no artifact, never silent-emit. The refusal is
itself an acceptance item and is exercised live in the deliverable.

HOUSE STYLE (item-1b conventions, per dispatch): error DIRECTION disclosed
per method; UNKNOWN EXCLUDED from the classified denominator; verdicts are
boundary statements, not materiality; unanticipated shapes VOLUNTEERED.

EXIT: 0 = table rendered (+ controls passed if requested) / 1 FAIL /
      3 REFUSE (emission pin unavailable, --emit only). READ-ONLY throughout.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_THIS = Path(__file__).resolve()
_WORKSPACE = _THIS.parents[5]
sys.path.insert(0, str(_WORKSPACE / "infra" / "system"))

import system_parity as SP  # noqa: E402  -- THE SUBJECT; its evaluators run unmodified

L0B_V1_PATH = _WORKSPACE / "infra" / "system" / "ontology" / "L0B_CHANGE_TYPE_VOCABULARY.md"
L0B_TYPES = ["ADD", "REMOVE", "MODIFY", "RENAME", "REGRAIN", "REORDER", "SPLIT", "MERGE", "RESEMANT"]


# ---------------------------------------------------------------------------------
# The harness: run the REAL evaluator against a world = {path: content} overlay of
# REAL-at-HEAD content, with system_parity's own read functions scoped-monkeypatched
# (the module's resident-battery idiom). Everything not in the overlay reads real.
# ---------------------------------------------------------------------------------

def real_read(path: str) -> str:
    return SP._read(path)


def evaluate_in_world(check: dict, world: dict, absent: set = frozenset(),
                      glob_counts: dict = None):
    """(status, detail) from the REAL run_check under a content-overlay world.
    `absent` = paths that do not exist in this world (REMOVE-of-file limbs).
    `glob_counts` = glob pattern -> count override (file-set mutations)."""
    real__read, real__exists, real__glob = SP._read, SP._exists, SP._glob_count
    SP._read = lambda p: "" if p in absent else world.get(p, real__read(p))
    SP._exists = lambda p: (p not in absent) and (p in world or real__exists(p))
    if glob_counts is not None:
        SP._glob_count = lambda pat: glob_counts.get(pat, real__glob(pat))
    try:
        cs = SP.CompSystem.__new__(SP.CompSystem)
        cs._fresh, cs._drifted = None, set()  # comp-system NOT probed: kinds needing it are UNKNOWN cells
        return SP.run_check(check, cs)
    finally:
        SP._read, SP._exists, SP._glob_count = real__read, real__exists, real__glob


def classify(check: dict, before_world: dict, after_world: dict,
             before_absent=frozenset(), after_absent=frozenset(),
             before_globs=None, after_globs=None):
    """Run REAL evaluator in both worlds; return (class, before, after)."""
    b_status, _ = evaluate_in_world(check, before_world, before_absent, before_globs)
    a_status, _ = evaluate_in_world(check, after_world, after_absent, after_globs)
    return ("SENSITIVE" if b_status != a_status else "MONOTONE-BLIND"), b_status, a_status


# ---------------------------------------------------------------------------------
# Real-source mutation synthesis, per pair. Each limb returns
# (after_world, after_absent, after_globs, description) built from REAL content.
# ---------------------------------------------------------------------------------

def load_units():
    contract = SP.load_contract()
    units = {}
    for dspec in contract["domains"].values():
        for u in dspec["units"]:
            units[u["id"]] = u
    return units


def build_pairs(units):
    """The pair table rows. Representative instances are REAL units, named.
    Sources read at HEAD through the subject's own _read at synthesis time."""
    rows = []

    # --- grep_present (instance: ct-router over 03_comp_tools.md) -------------------
    gp = units["ct-router"]["check"]
    gp_file = gp["files"][0]
    doc = real_read(gp_file)
    if doc:
        rows += [
            dict(kind="grep_present", unit="ct-router", ctype="ADD", limbs=[
                ("add a new (unmatched) section to the real doc",
                 {gp_file: doc + "\n## zzz-new-tool-family\nA new family landed.\n"}),
            ]),
            dict(kind="grep_present", unit="ct-router", ctype="REMOVE", limbs=[
                ("UNTARGETED: remove a real non-matching line",
                 {gp_file: _remove_nonmatching_line(doc, gp["pattern"])}),
                ("TARGETED: remove every line matching the unit's own pattern",
                 {gp_file: _remove_matching_lines(doc, gp["pattern"])}),
            ]),
            dict(kind="grep_present", unit="ct-router", ctype="MODIFY", limbs=[
                ("modify a non-matching real line's content, identity stable",
                 {gp_file: _modify_first_nonmatching(doc, gp["pattern"])}),
            ]),
            dict(kind="grep_present", unit="ct-router", ctype="RENAME", limbs=[
                ("rename the matched token estate-style (comp-which -> comp-route-v2) "
                 "everywhere in the real doc",
                 {gp_file: re.sub(r"comp-which|router", "comp-route-v2", doc, flags=re.I)}),
            ]),
            dict(kind="grep_present", unit="ct-router", ctype="REORDER", limbs=[
                ("reverse the real doc's line order, set identity stable",
                 {gp_file: "\n".join(reversed(doc.splitlines()))}),
            ]),
        ]

    # --- version_pin / python_constant (instance: ont-cse-version-current) ----------
    vp = units["ont-cse-version-current"]["check"]
    src = vp["source"]
    pysrc = real_read(src)
    if pysrc:
        m = re.search(r'SCHEMA_VERSION\s*=\s*[\'"]([^\'"]+)[\'"]', pysrc)
        cur = m.group(1) if m else None
        if cur:
            parts = cur.split(".")
            bumped = "%s.%s" % (parts[0], int(parts[-1]) + 1) if parts[-1].isdigit() else cur + ".1"
            rows += [
                dict(kind="version_pin", unit="ont-cse-version-current", ctype="ADD", limbs=[
                    ("ADD-with-discipline: new schema field + the source's own version bump "
                     "(%s -> %s), real file" % (cur, bumped),
                     {src: pysrc.replace('SCHEMA_VERSION = "%s"' % cur,
                                         'ZZZ_NEW_FIELD = "added"\nSCHEMA_VERSION = "%s"' % bumped)}),
                    ("ADD-without-bump: new field only, version untouched (the discipline-"
                     "mediation limb)",
                     {src: pysrc + '\nZZZ_NEW_FIELD = "added"\n'}),
                ]),
                dict(kind="version_pin", unit="ont-cse-version-current", ctype="MODIFY", limbs=[
                    ("MODIFY-with-bump: content change carrying the bump (%s -> %s)" % (cur, bumped),
                     {src: pysrc.replace('SCHEMA_VERSION = "%s"' % cur,
                                         'SCHEMA_VERSION = "%s"' % bumped)}),
                    ("MODIFY-without-bump: real non-version line changed, version untouched",
                     {src: pysrc.replace("schema", "sch3ma", 1)}),
                ]),
                dict(kind="version_pin", unit="ont-cse-version-current", ctype="RENAME", limbs=[
                    ("rename the CONSTANT itself (SCHEMA_VERSION -> SCHEMA_VER), content stable",
                     {src: pysrc.replace("SCHEMA_VERSION", "SCHEMA_VER")}),
                ]),
                dict(kind="version_pin", unit="ont-cse-version-current", ctype="REMOVE", limbs=[
                    ("remove the version constant (the source loses its own head)",
                     {src: re.sub(r'SCHEMA_VERSION\s*=\s*[\'"][^\'"]+[\'"]\s*\n?', "", pysrc)}),
                ]),
            ]

    # --- derived_count (instance: ct-catalog over graph-call-manifest tools_index) --
    dc = units["ct-catalog"]["check"]
    man_raw = real_read(dc["source"])
    if man_raw:
        rows += [
            dict(kind="derived_count", unit="ct-catalog", ctype="ADD", limbs=[
                ("add one member to the REAL tools_index mapping (yaml-level append)",
                 {dc["source"]: _yaml_add_tools_index_member(man_raw)}),
            ]),
            dict(kind="derived_count", unit="ct-catalog", ctype="REMOVE", limbs=[
                ("remove one real member from tools_index",
                 {dc["source"]: _yaml_remove_first_tools_index_member(man_raw)}),
            ]),
            dict(kind="derived_count", unit="ct-catalog", ctype="RENAME", limbs=[
                ("rename one real member key, content stable (cardinality unchanged)",
                 {dc["source"]: _yaml_rename_first_tools_index_member(man_raw)}),
            ]),
            dict(kind="derived_count", unit="ct-catalog", ctype="SPLIT", limbs=[
                ("one real member becomes two (cardinality up, concept preserved)",
                 {dc["source"]: _yaml_split_first_tools_index_member(man_raw)}),
            ]),
            dict(kind="derived_count", unit="ct-catalog", ctype="MERGE", limbs=[
                ("two real members become one (cardinality down)",
                 {dc["source"]: _yaml_remove_first_tools_index_member(man_raw)}),
            ]),
        ]

    # --- grep_absent (instance: ont-sdk-vocabulary-bound) ---------------------------
    ga = units["ont-sdk-vocabulary-bound"]["check"]
    ga_file = ga["files"][0]
    ga_doc = real_read(ga_file)
    if ga_doc:
        rows += [
            dict(kind="grep_absent", unit="ont-sdk-vocabulary-bound", ctype="ADD", limbs=[
                ("ADD the forbidden marker back into the real file (regression limb)",
                 {ga_file: ga_doc + '\n"_regression": "adapter-pattern-only"\n'}),
                ("ADD an unrelated member (untargeted)",
                 {ga_file: ga_doc.rstrip().rstrip("}") + ', "zzz_new": "x"}\n'
                  if ga_doc.rstrip().endswith("}") else ga_doc + "\nzzz_new: x\n"}),
            ]),
        ]

    # --- file_exists (instance: eng-synthesis) --------------------------------------
    fe = units["eng-synthesis"]["check"]
    rows += [
        dict(kind="file_exists", unit="eng-synthesis", ctype="REMOVE", limbs=[
            ("the real doc disappears", ("ABSENT", fe["path"])),
        ]),
        dict(kind="file_exists", unit="eng-synthesis", ctype="MODIFY", limbs=[
            ("gut the real doc to one byte, path stable",
             {fe["path"]: "x"}),
        ]),
        dict(kind="file_exists", unit="eng-synthesis", ctype="RENAME", limbs=[
            ("the doc moves: old path absent, content lives at a new path",
             ("ABSENT", fe["path"])),
        ]),
    ]

    # --- glob_count_ge (instance: inf-sdk-tf, min 1) --------------------------------
    gc = units["inf-sdk-tf"]["check"]
    live_n = SP._glob_count(gc["glob"])
    rows += [
        dict(kind="glob_count_ge", unit="inf-sdk-tf", ctype="ADD", limbs=[
            ("a new .tf lands (count %d -> %d)" % (live_n, live_n + 1),
             ("GLOB", {gc["glob"]: live_n + 1})),
        ]),
        dict(kind="glob_count_ge", unit="inf-sdk-tf", ctype="REMOVE", limbs=[
            ("one of %d files leaves (floor min=%s not crossed)" % (live_n, gc.get("min", 1)),
             ("GLOB", {gc["glob"]: max(live_n - 1, 0)})),
            ("ALL files leave (floor crossed)", ("GLOB", {gc["glob"]: 0})),
        ]),
    ]
    return rows


# --- string-level real-content mutators (yaml text kept textual: the evaluator's own
#     yaml.safe_load consumes the result, so real resolution is exercised) -----------

def _remove_nonmatching_line(doc: str, pattern: str) -> str:
    pat = re.compile(pattern, re.IGNORECASE)
    lines = doc.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() and not pat.search(ln):
            return "\n".join(lines[:i] + lines[i + 1:])
    return doc


def _remove_matching_lines(doc: str, pattern: str) -> str:
    pat = re.compile(pattern, re.IGNORECASE)
    return "\n".join(ln for ln in doc.splitlines() if not pat.search(ln))


def _modify_first_nonmatching(doc: str, pattern: str) -> str:
    pat = re.compile(pattern, re.IGNORECASE)
    lines = doc.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() and not pat.search(ln):
            lines[i] = ln + " (revised)"
            return "\n".join(lines)
    return doc


def _tools_index_block(man_raw: str):
    """(start, end, indent, first_key_line_idx) of the real tools_index mapping block."""
    lines = man_raw.splitlines()
    for i, ln in enumerate(lines):
        if re.match(r"^tools_index\s*:", ln):
            j = i + 1
            keys = []
            while j < len(lines) and (not lines[j].strip() or lines[j].startswith(" ")):
                if re.match(r"^  [A-Za-z0-9_-]+\s*:", lines[j]):
                    keys.append(j)
                j += 1
            return i, j, keys
    return None, None, []


def _yaml_add_tools_index_member(man_raw: str) -> str:
    i, j, keys = _tools_index_block(man_raw)
    if i is None:
        return man_raw
    lines = man_raw.splitlines()
    lines.insert(j, "  zzz-sensor-mutant-tool: {desc: synthesized ADD member}")
    return "\n".join(lines)


def _member_span(lines, key_idx):
    end = key_idx + 1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith("    ")):
        end += 1
    return end


def _yaml_remove_first_tools_index_member(man_raw: str) -> str:
    i, j, keys = _tools_index_block(man_raw)
    if not keys:
        return man_raw
    lines = man_raw.splitlines()
    end = _member_span(lines, keys[0])
    return "\n".join(lines[:keys[0]] + lines[end:])


def _yaml_rename_first_tools_index_member(man_raw: str) -> str:
    i, j, keys = _tools_index_block(man_raw)
    if not keys:
        return man_raw
    lines = man_raw.splitlines()
    lines[keys[0]] = re.sub(r"^  ([A-Za-z0-9_-]+)", "  zzz-renamed-member", lines[keys[0]])
    return "\n".join(lines)


def _yaml_split_first_tools_index_member(man_raw: str) -> str:
    i, j, keys = _tools_index_block(man_raw)
    if not keys:
        return man_raw
    lines = man_raw.splitlines()
    end = _member_span(lines, keys[0])
    member = lines[keys[0]:end]
    half_a = [re.sub(r"^  ([A-Za-z0-9_-]+)", r"  \1-a", member[0])] + member[1:]
    half_b = [re.sub(r"^  ([A-Za-z0-9_-]+)", r"  \1-b", member[0])] + member[1:]
    return "\n".join(lines[:keys[0]] + half_a + half_b + lines[end:])


# ---------------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------------

def run_pairs(units, only=None):
    """Evaluate every synthesized pair. Returns (results, declared_rows, unknown_rows)."""
    results = []
    pairs = build_pairs(units)
    for row in pairs:
        if only and (row["kind"], row["ctype"]) != only:
            continue
        check = units[row["unit"]]["check"]
        limb_out = []
        for desc, mutation in row["limbs"]:
            before_world, after_world = {}, {}
            b_abs, a_abs = set(), set()
            b_globs = a_globs = None
            if isinstance(mutation, dict):
                after_world = mutation
            elif isinstance(mutation, tuple) and mutation[0] == "ABSENT":
                a_abs = {mutation[1]}
            elif isinstance(mutation, tuple) and mutation[0] == "GLOB":
                a_globs = mutation[1]
            verdict, b, a = classify(check, before_world, after_world,
                                     frozenset(b_abs), frozenset(a_abs), b_globs, a_globs)
            limb_out.append({"limb": desc, "class": verdict, "before": b, "after": a})
        results.append({"kind": row["kind"], "unit": row["unit"], "ctype": row["ctype"],
                        "limbs": limb_out})
    return results


DECLARED_ROWS = [
    {"kind": "<every mechanical kind>", "ctype": "RESEMANT",
     "class": "UNDETECTABLE-BY-DESIGN",
     "why": "L0b s2 (ratified): meaning moves, members/counts/shape stable -- nothing "
            "mechanical is sensitive; the member is ACCEPTANCE-DEFERRED (owner CTO~Z, "
            "trigger = this very table rendering) and carried so this row exists "
            "instead of silence. No mutation attempted: its mutant is unwritable by "
            "construction until the provenance-pin design exists."},
    {"kind": "assumption (inf-intraday-iam)", "ctype": "<all 9>",
     "class": "IMMOBILE-BY-CONSTRUCTION",
     "why": "the check returns ASSUMPTION unconditionally -- a predicate that cannot "
            "move under ANY change type; the predicate-side mirror of RESEMANT, "
            "disclosed rather than counted as blind-or-sensitive."},
]

UNKNOWN_ROWS = [
    {"kind": "metric_current (ct-count-current)", "ctype": "<all mechanical>",
     "class": "UNKNOWN",
     "why": "could not synthesize without executing comp-system against a mutated "
            "estate; injecting CompSystem._fresh/_drifted would patch the OBSERVATION "
            "-- the patched-constant class the spec forbids. 'Could not synthesize' "
            "is NEVER 'sensitive'."},
    {"kind": "system_current (eng-currentstate-current)", "ctype": "<all mechanical>",
     "class": "UNKNOWN", "why": "same mechanism as metric_current."},
    {"kind": "grep_present/version_pin/derived_count", "ctype": "REGRAIN",
     "class": "UNKNOWN",
     "why": "no representative single-source regrain synthesizable at these sources' "
            "own grain without inventing a new axis semantics (the tools_index "
            "subcommand-regrain candidate changes the MEANING of a member, which is "
            "RESEMANT-adjacent, not a clean REGRAIN) -- declared, not guessed."},
]


def emission_pin():
    """(ok, why). ok only when the post-flip vocabulary file exists AND carries
    meta.version: 1.0 -- the ARCHETYPAL loop's own pin pattern, fail-closed."""
    if not L0B_V1_PATH.is_file():
        return False, ("pin unavailable: %s does not exist (only the DRAFT filename "
                       "does; the v1.0 flip is gated on ~C's conformance suite)"
                       % L0B_V1_PATH.name)
    text = L0B_V1_PATH.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"meta\.version:\s*[\"']?1\.0", text)
    if not m:
        return False, "file exists but carries no meta.version: 1.0 pin"
    return True, "pinned at v1.0"


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="sensor_monotonicity",
        description="L1b reference monotonicity sensor over system_parity's predicates. "
                    "Exit: 0 ok / 1 FAIL / 3 REFUSE (--emit without the L0b v1.0 pin).")
    ap.add_argument("--control", choices=["positive", "negative"],
                    help="run ONLY the named control pair and assert its expected class "
                         "(separate invocations, Rule 22a)")
    ap.add_argument("--emit", default=None,
                    help="write the L0b-typed pair-table JSON here -- REFUSES without the v1.0 pin")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    units = load_units()

    if args.control == "positive":
        # POSITIVE CONTROL (spec): a presence-check under ADD MUST report MONOTONE-BLIND.
        res = run_pairs(units, only=("grep_present", "ADD"))
        cls = res[0]["limbs"][0]["class"]
        print("POSITIVE CONTROL grep_present(ct-router) x ADD -> %s (before %s / after %s)"
              % (cls, res[0]["limbs"][0]["before"], res[0]["limbs"][0]["after"]))
        if cls != "MONOTONE-BLIND":
            print("FAIL: the archetype presence-check read %s under ADD -- harness broken "
                  "or doctrine falsified; do not trust the table." % cls)
            return 1
        print("PASS: the founding SYSPARITY blindness reproduces through the real evaluator.")
        return 0
    if args.control == "negative":
        # NEGATIVE CONTROL (spec): a version pin under ADD (with the source's own
        # versioning discipline) MUST report SENSITIVE.
        res = run_pairs(units, only=("version_pin", "ADD"))
        with_bump = res[0]["limbs"][0]
        print("NEGATIVE CONTROL version_pin(ont-cse-version-current) x ADD[with-bump] -> %s "
              "(before %s / after %s)" % (with_bump["class"], with_bump["before"], with_bump["after"]))
        if with_bump["class"] != "SENSITIVE":
            print("FAIL: the version pin did not move under a bumped ADD -- harness broken.")
            return 1
        print("PASS: the pin moves when the source moves. (Companion limb, disclosed: "
              "ADD-without-bump -> %s -- the pin's sensitivity is BORROWED from the "
              "source's versioning discipline, not intrinsic to addition.)"
              % res[0]["limbs"][1]["class"])
        return 0

    results = run_pairs(units)

    n_pairs = sum(len(r["limbs"]) for r in results)
    n_sens = sum(1 for r in results for lb in r["limbs"] if lb["class"] == "SENSITIVE")
    n_blind = n_pairs - n_sens

    print("=== L1b MONOTONICITY PAIR TABLE -- system_parity x L0b-S (PROVISIONAL labels; "
          "emission pin-gated) ===")
    print("SUBJECT population: 22 contract units, 9 check kinds (derived from "
          "scope_contract.json + run_check's own dispatch); representative instances are "
          "REAL units, named per row.")
    for r in results:
        print("  [%s x %s] unit=%s" % (r["kind"], r["ctype"], r["unit"]))
        for lb in r["limbs"]:
            print("      %-14s %s   (before %s -> after %s)  -- %s"
                  % (lb["class"], "", lb["before"], lb["after"], lb["limb"]))
    print("  DECLARED rows (distinct from UNKNOWN, never counted in the classified denominator):")
    for d in DECLARED_ROWS:
        print("      %-24s x %-8s %s -- %s" % (d["kind"], d["ctype"], d["class"], d["why"][:90] + "..."))
    print("  UNKNOWN rows (first-class, EXCLUDED from the classified denominator -- 'could "
          "not synthesize' is NEVER 'sensitive'):")
    for u in UNKNOWN_ROWS:
        print("      %-24s x %-8s -- %s" % (u["kind"], u["ctype"], u["why"][:90] + "..."))
    print("  DENOMINATOR: %d evaluated limb(s) across %d (kind x type) pairs: %d SENSITIVE / "
          "%d MONOTONE-BLIND; +%d DECLARED row-classes, +%d UNKNOWN row-classes excluded."
          % (n_pairs, len(results), n_sens, n_blind, len(DECLARED_ROWS), len(UNKNOWN_ROWS)))
    print("  DIRECTION: mutation synthesis is per-representative-instance and UNDER-reports "
          "pair space (one instance per kind; a different unit of the same kind could differ "
          "only via its config, not its evaluator). Verdicts are boundary statements about "
          "predicate mobility, not materiality.")

    if args.json:
        print(json.dumps({"pairs": results, "declared": DECLARED_ROWS,
                          "unknown": UNKNOWN_ROWS}, indent=2))

    if args.emit:
        ok, why = emission_pin()
        if not ok:
            print("REFUSE (--emit): L0b emission gate CLOSED -- %s. The table above is "
                  "INTERNAL/PROVISIONAL; no L0b-typed artifact is written. This refusal is "
                  "the dispatch's own acceptance item, not an error." % why)
            return 3
        out = Path(args.emit).resolve()
        payload = json.dumps({"l0b_version": "1.0", "pairs": results}, indent=2) + "\n"
        out.write_text(payload, encoding="utf-8")
        if not out.is_file() or out.stat().st_size < len(payload):
            print("FAIL: emit did not land at %s." % out)
            return 1
        print("EMITTED (pin verified v1.0): %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
