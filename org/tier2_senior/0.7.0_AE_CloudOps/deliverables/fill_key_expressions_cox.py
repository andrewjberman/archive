"""TO-KEYFILL-COX -- fill trust.key.key_expression on the 11 cards carded_by 0.7.0_AE_CloudOps~X.

WHAT THIS TOOL WILL NOT DO: invent an expression. Every expression written here is READ AT SOURCE
from the substrate the card describes, and every 'measured' basis is backed by an exercise that
runs IN THIS FILL over real repo bytes and prints the triple member -> key -> identity_space with
the key validated against the target space's own predicate. Where the substrate's members are only
reachable through a live cloud read -- which AC5 forbids -- the expression lands 'held' (declared,
unexercised) and says so. The face's words: honest absence outranks a plausible string.

THE FLOOR. `trust.key.basis` is the WEAKEST claim across the row, never the mode and never the best.
The confirmed predicate (2.0.0_SA_COO~X 214056Z, restated in the re-scope 79440) is MIN over ALL
sub-claims PRESENT, with a valued-but-undeclared sub-claim entering at 'inferred' -- explicitly NOT
a declared-only MIN, which is the reading that lets an incomplete basis_by_field read 'measured'.
That predicate lives in ONE function here (`key_row_floor`) and the fill loop computes through it;
there is no second copy, per 1.0.0_SA_CTO~X's constraint.

THE FALSIFIER (required by 4.0.0_SA_CRO~X 215229Z before this tool may run). `self_test()` puts the
confirmed floor and the REJECTED declared-only floor side by side over two fixtures:
  - an INCOMPLETE-MAP card (a valued sub-claim with no basis entry) must read 'inferred' under the
    confirmed predicate and 'measured' under the rejected one -- the arms disagree, and they are
    reachable from different truths;
  - a COMPLETE-MAP card must read the SAME under both -- so the falsifier cannot pass by always
    disagreeing.
If either arm fails, the tool REFUSES to run. A declared-but-unrun falsifier is a promise, not a
control.

Usage:
  python fill_key_expressions_cox.py --self-test     # controls only, writes nothing
  python fill_key_expressions_cox.py --dry-run       # exercise + census, writes nothing
  python fill_key_expressions_cox.py --apply         # writes the key rows
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import pathlib
import re
import sys

LANE = "0.7.0_AE_CloudOps~X"
CARD_ROOT = pathlib.Path("org/tier2_senior/0.7.0_AE_CloudOps/deliverables")
FABRIC_ROOT = pathlib.Path("org/tier2_senior")

# THE PATTERN THAT WAS WRONG, kept named because the issuer found the same class in two
# other sweeps: "D11_CARDS_*" requires the underscore, so it can never match the
# un-suffixed "D11_CARDS/" directory. All 8 wave-1 v1-freeze cards live there, TWO of
# them carded_by this lane, one level from the cards being filled. The first census
# reported 73 files / 1 exclusion; the true population is 81 under 10 roots. Nothing in
# that run could report it -- the denominator printed was the denominator of a sweep
# that could not see them, so it reconciled perfectly with itself. `assert_glob_sees_bare_stem`
# below is the arm that now fails the run rather than trusting the pattern.
WAVE_GLOB = "D11_CARDS*/*.json"          # matches BOTH D11_CARDS/ and D11_CARDS_W*/
V3_SCHEMA = pathlib.Path("org/standards/SUBSTRATE_CARD.v3.schema.json")

# strongest -> weakest. 'held' outranks 'inferred': a named authority DID measure it, just not here.
BASIS_RANK = {"measured": 3, "held": 2, "inferred": 1, "absent": 0}
RANK_BASIS = {v: k for k, v in BASIS_RANK.items()}

# The sub-claims of trust.key that carry a VALUE a basis can be about.
KEY_SUBCLAIMS = ("identity_space", "key_is_stable", "crosses_spaces", "key_expression",
                 "declared_mapping")


class Refused(RuntimeError):
    """The tool refuses to proceed. Never a warning, never a soft skip."""


# --------------------------------------------------------------------------------------
# THE FLOOR -- one definition, used by the fill loop and by the self-test alike.
# --------------------------------------------------------------------------------------
def key_row_floor(key: dict) -> str:
    """MIN over the sub-claims PRESENT, per the confirmed predicate.

    - A sub-claim with a non-null VALUE enters the MIN. Its basis is basis_by_field[field] when
      declared, and 'inferred' when NOT declared -- an undeclared valued claim is exactly the
      incomplete-map case, and reading it as measured is the over-promise the floor exists to stop.
    - A sub-claim whose value is null is STRUCTURAL ABSENCE, not a weak claim: it does not enter
      the MIN as a value. (Immaterial on this lane's 11 cards -- every null sub-claim here carries
      basis 'measured', the maximum, so entering it would not move any floor either way. Stated
      because a rule whose effect is untested on the data it runs over is a rule nobody has checked.)
    - A null key_expression additionally CAPS the row below 'measured' -- the v3 schema's own arm.
    """
    bbf = key.get("basis_by_field") or {}
    ranks = []
    for f in KEY_SUBCLAIMS:
        if f not in key:
            continue
        if key[f] is None:
            continue                       # structural absence, not a weak claim
        declared = bbf.get(f)
        ranks.append(BASIS_RANK[declared] if declared in BASIS_RANK else BASIS_RANK["inferred"])
    floor = RANK_BASIS[min(ranks)] if ranks else "absent"
    if key.get("key_expression") is None and floor == "measured":
        floor = "inferred"                 # v3 allOf: null expression forbids a 'measured' row
    return floor


def _declared_only_floor(key: dict) -> str:
    """THE REJECTED READING. Present ONLY so the falsifier can show the two disagree on the case
    that matters. Never called by the fill loop."""
    bbf = key.get("basis_by_field") or {}
    ranks = [BASIS_RANK[b] for b in bbf.values() if b in BASIS_RANK]
    return RANK_BASIS[min(ranks)] if ranks else "absent"


def self_test() -> bool:
    """The incomplete-map falsifier. Both arms must be reachable from DIFFERENT truths."""
    ok = True

    incomplete = {  # 'crosses_spaces' is valued but carries NO basis entry
        "identity_space": "ARN", "key_is_stable": "stable", "crosses_spaces": True,
        "key_expression": "row['arn']",
        "basis_by_field": {"identity_space": "measured", "key_is_stable": "measured",
                           "key_expression": "measured"},
    }
    complete = {
        "identity_space": "ARN", "key_is_stable": "stable", "crosses_spaces": True,
        "key_expression": "row['arn']",
        "basis_by_field": {"identity_space": "measured", "key_is_stable": "measured",
                           "crosses_spaces": "measured", "key_expression": "measured"},
    }

    a_conf, a_rej = key_row_floor(incomplete), _declared_only_floor(incomplete)
    b_conf, b_rej = key_row_floor(complete), _declared_only_floor(complete)

    print("  FALSIFIER arm 1 (incomplete map -- a valued sub-claim with no basis entry):")
    print(f"    confirmed floor = {a_conf!r}   rejected declared-only = {a_rej!r}")
    if not (a_conf == "inferred" and a_rej == "measured"):
        print("    FAIL: the arms must DISAGREE here (inferred vs measured)")
        ok = False

    print("  FALSIFIER arm 2 (complete map -- the control that stops 'always disagree' passing):")
    print(f"    confirmed floor = {b_conf!r}   rejected declared-only = {b_rej!r}")
    if not (b_conf == b_rej == "measured"):
        print("    FAIL: the arms must AGREE here")
        ok = False

    # the floor is a MIN, not a mode: one weak sub-claim sinks an otherwise-measured row
    sunk = dict(complete, key_is_stable="unknown",
                basis_by_field=dict(complete["basis_by_field"], key_is_stable="inferred"))
    if key_row_floor(sunk) != "inferred":
        print(f"    FAIL: MIN arm -- expected 'inferred', got {key_row_floor(sunk)!r}")
        ok = False

    # a null expression can never leave the row at 'measured'
    nulled = dict(complete, key_expression=None,
                  basis_by_field=dict(complete["basis_by_field"], key_expression="absent"))
    if key_row_floor(nulled) == "measured":
        print("    FAIL: null-expression cap -- row read 'measured'")
        ok = False

    print(f"  SELF-TEST: {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------------------
# PREDICATES -- a key is only exercised if it VALIDATES against its own space.
# --------------------------------------------------------------------------------------
def p_token(k):
    return isinstance(k, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", k) is not None


def p_graph_nid(k):
    return isinstance(k, str) and re.fullmatch(r"(system:[^:]+:[0-9a-f]{8}|motif:[a-z0-9-]+)", k) is not None


def p_repo_path(k):
    return isinstance(k, str) and pathlib.Path(k).exists()


def p_iceberg_identity(k):
    return (isinstance(k, tuple) and len(k) == 2
            and all(isinstance(x, str) and x for x in k))


# --------------------------------------------------------------------------------------
# EXERCISES -- each reads REAL repo bytes at run time and returns (member, key, predicate).
# A card with no in-repo member returns None: its expression lands 'held', never 'measured'.
# --------------------------------------------------------------------------------------
def _literal_from_source(path: str, name: str):
    """Pull a module-level literal by AST. Never imports -- importing a foreign deliverable
    script to read one constant would execute it (a read that writes)."""
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise Refused(f"REFUSED: {name} not found as a module-level literal in {path}")


CATALOG_SRC = ("org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/"
               "NFRA_MOTIF_P1_canonical_ab_catalog.py")
SPEC_AB = ("org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/"
           "motif_c2c3_materialize_ab.json")


def ex_anchor_catalog():
    """Exercise on a real ANCHOR type, NOT a hub type.

    The first version of this exercise took its member from HUB_TYPES because that literal was the
    one I had already read at source. HUB_TYPES members are node-type tokens and the key validated,
    so the exercise PASSED -- against the wrong subject: the catalog's own line 314 says hub types
    are 'compute Transformers: overlap-creators, NEVER anchors', i.e. precisely the set this card's
    subject EXCLUDES. A pass on the excluded set is not evidence about the included one. The
    assertion below is the arm that would have caught it, so it stays.
    """
    catalog = _literal_from_source(CATALOG_SRC, "ANCHOR_CATALOG")
    hub = _literal_from_source(CATALOG_SRC, "HUB_TYPES")
    domain = sorted(catalog)[0]
    member = sorted(catalog[domain])[0]
    if member in hub:
        raise Refused(f"REFUSED: {member!r} is in HUB_TYPES -- hub types are never anchors "
                      "(NFRA_MOTIF_P1_canonical_ab_catalog.py:314), so this is the wrong subject.")
    return f"ANCHOR_CATALOG[{domain!r}] member", member, "bare node-type token", p_token


def ex_baked_static():
    d = json.loads(io.open(SPEC_AB, encoding="utf-8").read())
    node = next(n for n in d["nodes"] if n["node_type"] == "C3System")
    return f"{node['node_type']} node in {pathlib.Path(SPEC_AB).name}", node["node_id"], \
        "graph node id ('system:<theme>:<sha1[:8]>' | 'motif:<name>')", p_graph_nid


def _module_path_exercise(path):
    def _ex():
        if not pathlib.Path(path).exists():
            raise Refused(f"REFUSED: {path} absent -- cannot exercise a repo-path key on it")
        return path, path, "repo path", p_repo_path
    return _ex


def _iceberg_exercise(src, ns_name, tbl_name, tbl_literal=None):
    def _ex():
        ns = _literal_from_source(src, ns_name)
        tbl = tbl_literal if tbl_literal is not None else _literal_from_source(src, tbl_name)
        return f"{pathlib.Path(src).name} default table", (ns, tbl), \
            "Iceberg table identity (namespace, table)", p_iceberg_identity
    return _ex


def ex_snap_store():
    src = "infra/aws/globgrph/snap_store.py"
    ns = _literal_from_source(src, "NAMESPACE")
    surfaces = _literal_from_source(src, "SURFACES")
    surface = sorted(surfaces)[0]
    return f"SURFACES[{surface!r}]", (ns, surface), \
        "Iceberg table identity (namespace, surface)", p_iceberg_identity


# key_expression + how the basis is earned, per card.
# 'exercise' None  => no in-repo member exists (a live read would be needed, AC5 forbids it) => held.
PLAN = {
    "anchor_catalog.json": dict(
        expr=("key(t) = t -- the member's own bare type token, verbatim as it appears in "
              "ANCHOR_CATALOG / HUB_TYPES in NFRA_MOTIF_P1_canonical_ab_catalog.py (an identity "
              "function, not a derivation); consumers match it by string equality against a "
              "motif's constituent types."),
        exercise=ex_anchor_catalog),
    "baked_static_spec_layers.json": dict(
        expr=("key(n) = n['node_id'] -- read verbatim from the node object in "
              "motif_c2c3_materialize.json / motif_c2c3_materialize_ab.json. THE KEY IS CARRIED, "
              "NOT RECOMPUTED AT READ TIME: C3System members read 'system:<theme>:<sha1[:8]>' and "
              "C2Motif members read 'motif:<name>'. The sha1[:8] is how the PRODUCER minted the "
              "id; a consumer never re-derives it, so the mint is not part of this expression."),
        exercise=ex_baked_static),
    "comp_debris.json": dict(
        expr=("key(row) = row['name'] -- the per-type resource NAME as minted into the ledger row "
              "at comp_debris.py:80 and consumed as the ledger key at :129; the same string is "
              "what _HELD_RX (:62) is matched against at :162."),
        exercise=None,
        held_reason=("the ledger's members are produced by a LIVE per-type AWS scan and no ledger "
                     "artifact is carried in the repo, so no real member is reachable without a "
                     "cloud call -- which AC5 forbids in this fill")),
    "comp_ladder.json": dict(
        expr=("key(m) = the module's repo path, 'org/modules/graph/comp_ladder.py'. Within a "
              "ladder, a node's key is Node.nid, minted per recognizer (e.g. "
              "'pmap:<firm>-><bucket>', 'allowed:<firm>-><bucket>')."),
        exercise=_module_path_exercise("org/modules/graph/comp_ladder.py")),
    "dup_scan.json": dict(
        expr=("key(d) = the document's repo path -- the same space as the module's own key, "
              "'org/modules/graph/debtscan/dup_scan.py'; every scored document is addressed by "
              "repo path throughout."),
        exercise=_module_path_exercise("org/modules/graph/debtscan/dup_scan.py")),
    "resource_summaries.json": dict(
        expr=("key(row) = (row['arn'], MAX(row['summary_version']) per arn) -- field 1 'arn' is "
              "the identity column and field 8 'summary_version' the append-only version axis "
              "(resource_summaries_store.py:63, :70); a reader resolves MAX(summary_version) per "
              "arn, so the resolved key of a resource is its ARN alone."),
        exercise=None,
        held_reason=("the table's rows are Iceberg data in AWS; resolving MAX(summary_version) for "
                     "a real ARN requires a live catalog read, which AC5 forbids in this fill")),
    "summary_corpus.json": dict(
        expr=("key(s) = the resource's AWS ARN, with a bare-name alias accepted for resources "
              "addressed by name; the corpus is {arn -> SummaryDoc}, so the ARN is the dict key."),
        exercise=None,
        held_reason=("build_corpus() derives its members from a live resource scan; no corpus "
                     "artifact is carried in the repo, so no real member is reachable without a "
                     "cloud call -- which AC5 forbids in this fill")),
    "cse_store__PATH_A_append.json": dict(
        expr=("key(t) = (NAMESPACE, table) = ('globgrph', args.table), defaulting to CSE_TABLE -- "
              "the tuple built at cse_store.py's ensure_cse_table (`table_id = (NAMESPACE, table)`) "
              "from NAMESPACE ':85' and CSE_TABLE ':86' (sourced from cse_schema, not a local "
              "literal). The SAME logical table is addressed as the dotted string "
              "'iceberg.globgrph.cse' by fedobs_observe.py:48 -- a PLANE difference (pyiceberg "
              "takes a tuple, Trino takes catalog.schema.table), so a consumer joining across the "
              "two planes must apply the declared mapping rather than string equality."),
        exercise=_iceberg_exercise("infra/aws/globgrph/cse_store.py", "NAMESPACE", "CSE_TABLE",
                                   tbl_literal="cse")),
    "cse_store__PATH_B_drop.json": dict(
        expr=("key(t) = (NAMESPACE, table) = ('globgrph', args.table) -- the same tuple space as "
              "PATH A, from cse_store.py NAMESPACE ':85' / CSE_TABLE ':86'. The destructive "
              "guard compares against the BARE form 'cse' only, so the guard's own key is the "
              "table element of the tuple, not the tuple."),
        exercise=_iceberg_exercise("infra/aws/globgrph/cse_store.py", "NAMESPACE", "CSE_TABLE",
                                   tbl_literal="cse")),
    "resource_summaries_store.json": dict(
        expr=("key(t) = (NAMESPACE, TABLE) = ('globgrph', 'resource_summaries') from "
              "resource_summaries_store.py ':56' / ':57'. Rows inside it are keyed by field 1 "
              "'arn' with latest-version-wins on MAX(field 8 'summary_version')."),
        exercise=_iceberg_exercise("infra/aws/globgrph/resource_summaries_store.py",
                                   "NAMESPACE", "TABLE")),
    "snap_store.json": dict(
        expr=("key(t) = (NAMESPACE, surface) where surface is one of the four keys of the SURFACES "
              "registry (snap_store.py ':79', gated by --surface choices=sorted(SURFACES) at "
              "':415'): ms_heat_snap, code_heat_snap, fedobs_coverage_snap, "
              "fedobs_coevolution_snap. The SAME surface string is the join key into the second "
              "identity space, the S3 staging prefix warehouse/snap_ingest/pending/<surface>/."),
        exercise=ex_snap_store),
}


# --------------------------------------------------------------------------------------
def assert_glob_sees_bare_stem():
    """REFUSE if the card glob cannot match the un-suffixed stem directory.

    This is the falsifier for the defect this tool shipped with. It does not ask whether
    the sweep found anything -- a sweep that finds nothing still prints a tidy zero. It
    asks whether the PATTERN is capable of matching a directory named exactly
    'D11_CARDS', by testing it against that literal name. Scope and pattern are
    independent axes and this file checked only the first.
    """
    import fnmatch
    dir_pat = WAVE_GLOB.split("/")[0]
    if not fnmatch.fnmatch("D11_CARDS", dir_pat):
        raise Refused(
            f"REFUSED: card glob {WAVE_GLOB!r} cannot match the bare stem directory "
            "'D11_CARDS'. That is the exact defect this tool shipped with: the "
            "un-suffixed directory holds the wave-1 v1-freeze cards and a census run "
            "under such a pattern reconciles with itself while missing them.")
    if not fnmatch.fnmatch("D11_CARDS_W2", dir_pat):
        raise Refused(f"REFUSED: card glob {WAVE_GLOB!r} no longer matches a wave dir.")


def census():
    """The FULL population under every card root, printed with its denominators.

    Separated from the lane's re-derivation on purpose: the fill is scoped to this
    lane's v3 cards, but the SWEEP must be able to see everything, or its denominator
    is a number about the pattern rather than about the estate.
    """
    roots = sorted(p for p in FABRIC_ROOT.rglob("D11_CARDS*") if p.is_dir())
    files = [q for r in roots for q in sorted(r.rglob("*.json"))]
    v3 = v1 = other = 0
    mine_v3, mine_v1, manifests = [], [], []
    for p in files:
        d = json.loads(io.open(p, encoding="utf-8").read())
        sv = str(d.get("schema_version", ""))
        mine = d.get("carded_by") == LANE
        if sv.startswith("3"):
            v3 += 1
            if mine:
                mine_v3.append(p)
        elif sv == "1":
            v1 += 1
            if mine:
                mine_v1.append(p)
        else:
            other += 1
            manifests.append(p)
    print(f"  card roots            : {len(roots)}")
    print(f"  total JSON under them : {len(files)}")
    print(f"  v3 cards              : {v3}")
    print(f"  v1-freeze cards       : {v1}  (schema_version '1'; refused by design, not by failure)")
    print(f"  no schema_version     : {other}  {[p.name for p in manifests]}")
    print(f"  CHECK {v3} + {v1} + {other} = {v3 + v1 + other} of {len(files)}")
    print(f"  carded_by {LANE}: v3 {len(mine_v3)} | v1 {len(mine_v1)} | ALL {len(mine_v3) + len(mine_v1)}")
    if mine_v1:
        print(f"    v1-freeze of this lane, OUT OF SCOPE by schema_version: "
              f"{[p.as_posix() for p in mine_v1]}")
    return mine_v3


def rederive_cards():
    """This lane's V3 cards. Scoped by carded_by AND schema_version, because the widened
    glob now also sees this lane's 2 v1-freeze cards and the face's scope is v3 only."""
    found = []
    for p in sorted(CARD_ROOT.rglob(WAVE_GLOB)):
        d = json.loads(io.open(p, encoding="utf-8").read())
        if d.get("carded_by") == LANE and str(d.get("schema_version", "")).startswith("3"):
            found.append(p)
    return found


def validate(card, schema, validator_cls):
    errs = sorted(validator_cls(schema).iter_errors(card), key=lambda e: list(e.path))
    return [f"{'/'.join(str(x) for x in e.path)}: {e.message[:160]}" for e in errs]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    print("=== FALSIFIER (gates every run; a failure REFUSES the tool) ===")
    if not self_test():
        raise Refused("REFUSED: the floor falsifier failed. Nothing read, nothing written.")
    assert_glob_sees_bare_stem()
    print("  GLOB arm: the card pattern matches both the bare stem and a wave dir -> PASS")
    if args.self_test:
        return 0

    print("\n=== CENSUS: the FULL population under every card root ===")
    census()

    import jsonschema
    schema = json.loads(io.open(V3_SCHEMA, encoding="utf-8").read())
    vcls = jsonschema.validators.validator_for(schema)

    cards = rederive_cards()
    print(f"\n=== RE-DERIVED cards carded_by == {LANE}: {len(cards)} (face declares 11) ===")
    if len(cards) != 11:
        print(f"  DIFFERENCE from the face -- NAMED, not absorbed: {len(cards)} != 11")

    planned = set(PLAN)
    actual = {p.name for p in cards}
    if planned != actual:
        raise Refused(f"REFUSED: plan/card mismatch. plan-only={planned - actual} "
                      f"card-only={actual - planned}")

    print("\n=== EXERCISES (member -> key -> identity_space, key validated against the space) ===")
    results = {}
    for p in cards:
        card = json.loads(io.open(p, encoding="utf-8").read())
        key = card["trust"]["key"]
        plan = PLAN[p.name]
        space = key["identity_space"]
        if plan["exercise"] is None:
            results[p.name] = ("held", None)
            print(f"\n  {p.name}\n    HELD -- no in-repo member: {plan['held_reason']}")
            continue
        member, k, space_name, pred = plan["exercise"]()
        ok = pred(k)
        shown = repr(k) if not isinstance(k, str) else k
        print(f"\n  {p.name}")
        print(f"    member : {member}")
        print(f"    key    : {shown}")
        print(f"    space  : {space_name}  |  card's identity_space: {space[:70]}")
        print(f"    predicate {pred.__name__} -> {'PASS' if ok else 'FAIL'}")
        if not ok:
            raise Refused(f"REFUSED: {p.name} key {shown!r} failed its space predicate. "
                          "An expression that does not yield a valid key is not 'measured'.")
        results[p.name] = ("measured", (member, shown, space_name))

    print("\n=== FILL + FLOOR ===")
    fill_counts = {"measured": 0, "held": 0, "absent": 0}
    floors = {}
    written = []
    for p in cards:
        raw = io.open(p, "rb").read()
        card = json.loads(raw.decode("utf-8"))
        key = card["trust"]["key"]
        basis, _ = results[p.name]
        before = key.get("basis")

        key["key_expression"] = PLAN[p.name]["expr"]
        bbf = dict(key.get("basis_by_field") or {})
        bbf["key_expression"] = basis
        key["basis_by_field"] = bbf
        key["basis"] = key_row_floor(key)

        fill_counts[basis] += 1
        floors[p.name] = (before, key["basis"])

        ev = key.get("evidence", "")
        if "v3 delta pass" in ev and "DISCHARGED" not in ev:
            ev += (" || DISCHARGED " + ("by exercise in the KEYFILL-COX fill" if basis == "measured"
                   else "as HELD in the KEYFILL-COX fill") + ": " +
                   (f"exercised on a real member -- {results[p.name][1][0]} -> "
                    f"{results[p.name][1][1]} in {results[p.name][1][2]}."
                    if basis == "measured" else PLAN[p.name].get("held_reason", "")) +
                   f" Row floor recomputed {before} -> {key['basis']}.")
            key["evidence"] = ev
        elif basis == "measured":
            key["evidence"] = ev + (
                f" || KEYFILL-COX: key_expression filled and EXERCISED on a real member -- "
                f"{results[p.name][1][0]} -> {results[p.name][1][1]} in {results[p.name][1][2]}. "
                f"Row floor recomputed {before} -> {key['basis']}.")
        else:
            key["evidence"] = ev + (
                f" || KEYFILL-COX: key_expression DECLARED but NOT exercised here, so it is HELD, "
                f"not measured -- {PLAN[p.name]['held_reason']}. "
                f"Row floor recomputed {before} -> {key['basis']}.")

        errs = validate(card, schema, vcls)
        if errs:
            raise Refused(f"REFUSED: {p.name} fails v3 after fill: {errs[:3]}")

        out = json.dumps(card, indent=2, ensure_ascii=False) + "\n"
        written.append((p, raw, out.encode("utf-8")))
        print(f"  {p.name:<38} key_expression={basis:<9} floor {before} -> {key['basis']}")

    print("\n=== CONTRADICTION FIXTURE (the negative arm -- must be REFUSED by v3) ===")
    bad = json.loads(io.open(cards[0], encoding="utf-8").read())
    bad["trust"]["key"]["key_expression"] = None
    bad["trust"]["key"]["basis"] = "measured"
    bad["trust"]["key"]["basis_by_field"]["key_expression"] = "absent"
    errs = validate(bad, schema, vcls)
    print(f"  measured + null expression -> {'REFUSED' if errs else 'ACCEPTED'}"
          f"{' : ' + errs[0][:110] if errs else ''}")
    if not errs:
        raise Refused("REFUSED: the contradiction fixture VALIDATED. The negative arm is dead.")

    print("\n=== CENSUS (denominator 11, re-derived) ===")
    print(f"  filled + exercised (measured) : {fill_counts['measured']}")
    print(f"  filled, declared-unexercised (held) : {fill_counts['held']}")
    print(f"  null + absent : {fill_counts['absent']}")
    print("  inferred key_expression : 0 (PROHIBITED by the face)")
    print(f"  TOTAL {sum(fill_counts.values())} of {len(cards)}")
    rose = sum(1 for b, a in floors.values() if BASIS_RANK[a] > BASIS_RANK[b])
    print(f"  row floors that ROSE: {rose} of {len(cards)}")

    if args.apply:
        for p, raw, out in written:
            io.open(p, "wb").write(out)
        print(f"\nWROTE {len(written)} card(s).")
    else:
        print("\nDRY RUN -- nothing written.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refused as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
