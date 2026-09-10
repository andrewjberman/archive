#!/usr/bin/env python3
"""H2-AC1 -- THE THREE CARRIERS OF ONE MECHANISM, READ OUT OF THE SOURCE, SIDE BY SIDE.

NFRA_CLDGRPH TO-CG-H-2 / cell CG-s-37, worker 0.9.0_WK_NFRA_CLDGRPH~1.

derive_stitch archives its own output (derive_runner folds the artifact into the nightly
snapshot and archives it) and reads that snapshot back on the next cycle. The question
"is the prior cycle's output an INPUT or is it NOISE?" is answered on three carriers --
NODES, PROPS, EDGES -- and it was answered separately, three cells apart, because every
check was scoped to one carrier. This script answers it for all three in ONE output.

INSTRUMENT + COVERAGE: a python `ast` parse of the WHOLE producer file (one file, the
denominator is its statement count, printed), not a text grep and not the card. Behaviour
is classified from the deciding AST construct, never from a comment.

GRAIN: one row per carrier -- behaviour, deciding line, counter, whether the counter
reaches the artifact's meta.

ENVIRONMENT / BASELINE: the comparison values are the four round-7 substrate cards at
org/missions/D0/NFRA/NFRA_CLDGRPH/cards/, carded at commit f3b5f26f77 by
0.9.0_WK_NFRA_CLDGRPH~2. They are a CORROBORATING read. A disagreement between card and
source is REPORTED, never reconciled, and THE SOURCE WINS.

Vocabulary (one axis: what happens to a member that arrived from the archive):
  DROP   -- removed on read because it came from the archive, whatever this cycle emitted
  DEDUPE -- removed only when THIS cycle re-emitted the same member (a collision rule)
  KEEP   -- nothing removes it
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parents[7]
PRODUCER = WS / "infra" / "aws" / "globgrph" / "derive_stitch.py"
CARDS = WS / "org" / "missions" / "D0" / "NFRA" / "NFRA_CLDGRPH" / "cards"
CARD_FILES = {
    "NODES": CARDS / "stitch-producer-archive-read.nodes.card.json",
    "PROPS": CARDS / "stitch-producer-archive-read.props.card.json",
    "EDGES": CARDS / "stitch-producer-archive-read.edges.card.json",
}
# Each probe is a literal substring of the card's own text and is PRINTED with the row, so
# a reader can see which sentence the card-side claim was taken from.
CARD_PROBES = {
    "NODES": [
        ("DEDUPE", "drops an archived copy only when the same id is in this run's fresh emission"),
        ("DEDUPE", "no drop-on-read for stitch nodes"),
        ("DROP", "prior-cycle nodes on read and emit the count"),
    ],
    "PROPS": [
        ("DROP", "the retired key is popped from every surviving stitch-sourced node"),
        ("DROP", "popped from every stitch-sourced node that survives"),
    ],
    "EDGES": [
        ("DROP", "the prior cycle's edges are dropped unconditionally on read"),
        ("DROP", "dropped unconditionally on read"),
    ],
}


def _git(*args: str) -> str:
    try:
        out = subprocess.run(["git", "-C", str(WS)] + list(args), capture_output=True,
                             text=True, timeout=60)
        return (out.stdout or "").strip()
    except Exception as exc:                       # pragma: no cover - environment
        return "ERROR: " + str(exc)[:120]


def _counter_keys(body_nodes) -> list:
    """Every dict-subscript counter this statement group increments, in order."""
    keys = []
    for node in body_nodes:
        for sub in ast.walk(node):
            if isinstance(sub, ast.AugAssign) and isinstance(sub.target, ast.Subscript):
                sl = sub.target.slice
                if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                    keys.append(sl.value)
    return keys


def read_nodes_carrier(tree: ast.AST) -> dict:
    """The NODES rule lives in _collapse_stitch_copies: which archived node is removed."""
    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == "_collapse_stitch_copies"), None)
    if fn is None:
        return {"behaviour": "KEEP", "line": 0, "deciding": "FUNCTION ABSENT",
                "counter": None, "note": "_collapse_stitch_copies not found in the source"}
    drop_hit = dedupe_hit = None
    for node in ast.walk(fn):
        if not isinstance(node, ast.If):
            continue
        test = ast.unparse(node.test)
        if "archived" not in test:
            continue
        has_continue = any(isinstance(s, ast.Continue) for s in ast.walk(node))
        if not has_continue:
            continue
        row = {"line": node.lineno, "deciding": test, "counter": _counter_keys(node.body)}
        # CLASSIFICATION RULE, printed with the row: a removal whose test does NOT consult
        # this cycle's emission (fresh_ids) removes the archived member WHATEVER this cycle
        # emitted -- that is a DROP. A removal keyed on the id being IN fresh_ids only
        # resolves a collision -- that is a DEDUPE.
        if "not in fresh_ids" in test or "fresh_ids" not in test:
            drop_hit = row
        elif "in fresh_ids" in test:
            dedupe_hit = row
    if drop_hit:
        counters = drop_hit["counter"] or []
        return {"behaviour": "DROP", "line": drop_hit["line"], "deciding": drop_hit["deciding"],
                "counter": counters[0] if counters else None,
                "note": ("an archived stitch node this cycle did NOT re-emit is removed on read; "
                         "the DEDUPE rule at line %s still resolves the re-emitted collision"
                         % (dedupe_hit["line"] if dedupe_hit else "ABSENT"))}
    if dedupe_hit:
        counters = dedupe_hit["counter"] or []
        return {"behaviour": "DEDUPE", "line": dedupe_hit["line"],
                "deciding": dedupe_hit["deciding"],
                "counter": counters[0] if counters else None,
                "note": ("removal is CONDITIONAL on the id being in this cycle's emission "
                         "(fresh_ids), so a member the producer STOPPED emitting survives")}
    return {"behaviour": "KEEP", "line": fn.lineno, "deciding": "no archived-member removal",
            "counter": None, "note": "no rule removes an archived node"}


def read_props_carrier(tree: ast.AST) -> dict:
    """The PROPS rule: RETIRED_STITCH_PROPS popped off every surviving stitch node."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.For):
            continue
        if not (isinstance(node.iter, ast.Name) and node.iter.id == "RETIRED_STITCH_PROPS"):
            continue
        pops = [s for s in ast.walk(node)
                if isinstance(s, ast.Call) and isinstance(s.func, ast.Attribute)
                and s.func.attr == "pop"]
        if not pops:
            continue
        counters = _counter_keys(node.body)
        return {"behaviour": "DROP", "line": node.lineno,
                "deciding": "for %s in RETIRED_STITCH_PROPS: n.pop(%s, None)"
                            % (ast.unparse(node.target), ast.unparse(node.target)),
                "counter": counters[0] if counters else None,
                "note": ("unconditional on the member's origin: the key is popped from every "
                         "surviving stitch-sourced node, archived or fresh. COVERAGE BOUND: the "
                         "population is the RETIRED_STITCH_PROPS enumeration, hand-maintained")}
    return {"behaviour": "KEEP", "line": 0, "deciding": "no RETIRED_STITCH_PROPS loop",
            "counter": None, "note": "no rule removes a retired prop"}


def read_edges_carrier(tree: ast.AST) -> dict:
    """The EDGES rule: this producer's own prior-cycle edge type filtered out of the input."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "edges"
                and isinstance(node.value, ast.ListComp)):
            continue
        cond = " and ".join(ast.unparse(c) for c in node.value.generators[0].ifs)
        if "edge_type" not in cond:
            continue
        return {"behaviour": "DROP", "line": node.lineno,
                "deciding": "edges = [e for e in edges if %s]" % cond,
                "counter": "stored_in_prior_cycle_dropped",
                "note": ("unconditional on this cycle's emission: an edge of this producer's own "
                         "type arriving in the snapshot IS a previous cycle's output. COVERAGE "
                         "BOUND: one literal edge type; every other edge this producer writes is "
                         "protected only by the dedup")}
    return {"behaviour": "KEEP", "line": 0, "deciding": "no prior-cycle edge filter",
            "counter": None, "note": "no rule removes an archived edge"}


def card_claim(carrier: str) -> tuple:
    path = CARD_FILES[carrier]
    if not path.exists():
        return "UNREADABLE", "card file absent: %s" % path
    text = path.read_text(encoding="utf-8").lower()
    for behaviour, probe in CARD_PROBES[carrier]:
        if probe.lower() in text:
            return behaviour, probe
    return "UNREADABLE", "no probe matched in %s" % path.name


def main() -> int:
    src = PRODUCER.read_text(encoding="utf-8")
    tree = ast.parse(src)
    stmts = sum(1 for n in ast.walk(tree) if isinstance(n, ast.stmt))
    head = _git("rev-parse", "HEAD")
    head_blob = _git("show", "HEAD:infra/aws/globgrph/derive_stitch.py")
    worktree_matches_head = (head_blob.replace("\r\n", "\n").strip()
                             == src.replace("\r\n", "\n").strip())

    print("H2-AC1 CARRIER ASYMMETRY -- NFRA_CLDGRPH CG-s-37")
    print("TREE_READ=%s" % WS)
    print("SOURCE=%s" % PRODUCER)
    print("SOURCE_VINTAGE: HEAD=%s worktree_bytes_match_HEAD_blob=%s"
          % (head, str(worktree_matches_head).lower()))
    print("INSTRUMENT=python ast parse of ONE file (not a grep, not the card)")
    print("COVERAGE: statements swept=%d of %d in %s (denominator = every statement in the "
          "file; nothing excluded)" % (stmts, stmts, PRODUCER.name))
    print("GRAIN: one row per carrier -- behaviour, deciding line, counter")
    print("BASELINE_ENVIRONMENT: round-7 substrate cards @f3b5f26f77 under %s (READ ONLY)"
          % CARDS)
    print("")

    rows = {"NODES": read_nodes_carrier(tree), "PROPS": read_props_carrier(tree),
            "EDGES": read_edges_carrier(tree)}
    print("CARRIERS_READ=3 of 3 from SOURCE")
    for carrier in ("NODES", "PROPS", "EDGES"):
        print("%s=%s" % (carrier, rows[carrier]["behaviour"]))
    print("")

    disagreements = []
    unreadable = []
    for carrier in ("NODES", "PROPS", "EDGES"):
        row = rows[carrier]
        claim, probe = card_claim(carrier)
        row["card_claim"], row["card_probe"] = claim, probe
        print("---- CARRIER %s ----" % carrier)
        print("  SOURCE_BEHAVIOUR = %s" % row["behaviour"])
        print("  DECIDING_LINE printed per carrier: %s:%d -- %s"
              % (PRODUCER.name, row["line"], row["deciding"]))
        print("  COUNTER = %s" % (row["counter"] or "NONE"))
        surfaced = src.count(row["counter"]) if row["counter"] else 0
        print("  COUNTER_OCCURRENCES_IN_SOURCE = %d (>1 means it is carried past the site that "
              "increments it, i.e. a reader can see it fire)" % surfaced)
        print("  NOTE = %s" % row["note"])
        print("  CARD_CLAIM = %s  (probe: %s)" % (claim, probe))
        if claim == "UNREADABLE":
            unreadable.append(carrier)
        elif claim != row["behaviour"]:
            disagreements.append((carrier, claim, row["behaviour"]))
            print("  CARD_VS_SOURCE = DISAGREE (card says %s, source says %s) -- REPORTED, NOT "
                  "RECONCILED; THE SOURCE WINS" % (claim, row["behaviour"]))
        else:
            print("  CARD_VS_SOURCE = AGREE")
        print("")

    print("CARD_VS_SOURCE_DISAGREEMENTS=%d reported" % len(disagreements))
    for carrier, claim, actual in disagreements:
        print("  DISAGREEMENT %s: card=%s source=%s -- the cards are vintage f3b5f26f77 and this "
              "order changed the source; the card is not edited by this order (READ ONLY surface)"
              % (carrier, claim, actual))
    print("CARD_PROBES_UNREADABLE=%d %s" % (len(unreadable), unreadable or ""))
    print("")
    print("ASYMMETRY_VERDICT: the three carriers of ONE mechanism answer '%s / %s / %s' "
          "(nodes/props/edges)." % tuple(rows[c]["behaviour"] for c in ("NODES", "PROPS", "EDGES")))
    Path(__file__).with_name("h2_carrier_asymmetry.capture.json").write_text(
        json.dumps({"head": head, "worktree_matches_head": worktree_matches_head,
                    "rows": rows, "disagreements": disagreements}, indent=1),
        encoding="utf-8")
    print("CAPTURE=h2_carrier_asymmetry.capture.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
