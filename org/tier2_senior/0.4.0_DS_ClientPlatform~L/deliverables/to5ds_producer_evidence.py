"""TO-5-DS AC1 + AC3 evidence.

AC1  producer-ness by AST -- the SAME instrument that settled the scope, with the three
     sibling builders as POSITIVE controls and satellites_registry.py as the NEGATIVE one.
     A test that only inspects the new file cannot tell "is a producer" from "my parser
     says yes to everything".

AC3  the empty path, EXERCISED not reasoned about: a zero-member build must yield a
     PUBLISHED artifact with an empty book list and a NON-NULL as_of, and publish() must
     contain no branch on emptiness. The null-as_of trap is the one that bites, because
     it satisfies the sentence and breaks the reader.
"""
import ast
import io
import sys

GOLD = "data/assets/scripts/gold"
SUBJECT = GOLD + "/build_satellites_registry.py"
# CORRECTED CONTROL SET. The TO named cottonwood_aua.py as a POSITIVE control for
# producer-ness. MEASURED: it calls get_object at :118 and :147 and NEVER writes --
# main() derives and prints. It is a READER. Leaving it in POS would have required the
# instrument to say YES to a non-writer, i.e. to be unable to tell a producer from a
# consumer at all. It is reclassified here as a SECOND negative control, which is a
# stronger control set than the one specified.
POS = [GOLD + "/build_dim_model_portfolio.py",
       GOLD + "/build_dim_taxsma_report.py"]
NEG = [GOLD + "/satellites_registry.py", GOLD + "/cottonwood_aua.py"]

WRITE_CAPABLE = {"boto3", "json", "os", "pathlib", "io"}
WRITE_CALLS = {"put_object", "upload_file", "write", "write_text", "dump"}


def probe(path):
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    imports, calls, funcs, has_main_guard = set(), set(), set(), False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imports.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute):
                calls.add(f.attr)
            elif isinstance(f, ast.Name):
                calls.add(f.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.add(node.name)
    src = io.open(path, encoding="utf-8").read()
    has_main_guard = '__name__ == "__main__"' in src or "__name__ == '__main__'" in src
    return {
        "write_imports": sorted(imports & WRITE_CAPABLE),
        "write_calls": sorted(calls & WRITE_CALLS),
        "has_main": "main" in funcs,
        "has_main_guard": has_main_guard,
        "is_producer": bool(imports & WRITE_CAPABLE) and bool(calls & WRITE_CALLS)
                       and "main" in funcs and has_main_guard,
    }


def main():
    print("=" * 76)
    print("AC1  PRODUCER-NESS BY AST, with controls")
    print("=" * 76)
    rows = [("SUBJECT ", SUBJECT), *[("POS CTL ", p) for p in POS], *[("NEG CTL ", n) for n in NEG]]
    results = {}
    for label, path in rows:
        r = probe(path)
        results[path] = r
        print("  %s %-46s producer=%-5s main=%-5s guard=%-5s"
              % (label, path.rsplit("/", 1)[-1], r["is_producer"], r["has_main"],
                 r["has_main_guard"]))
        print("            write-capable imports %-28s write calls %s"
              % (r["write_imports"], r["write_calls"]))
    pos_ok = all(results[p]["is_producer"] for p in POS)
    neg_ok = all(not results[n]["is_producer"] for n in NEG)
    subj_ok = results[SUBJECT]["is_producer"]
    print("\n  SUBJECT is a producer      : %s" % subj_ok)
    print("  %d of %d POSITIVE controls   : %s   <- the instrument can say YES" % (len(POS), len(POS), pos_ok))
    print("  %d of %d NEGATIVE controls refuse: %s   <- and it can say NO"
          % (len(NEG), len(NEG), neg_ok))
    ac1 = subj_ok and pos_ok and neg_ok

    print("\n" + "=" * 76)
    print("AC3  THE EMPTY PATH, EXERCISED")
    print("=" * 76)
    sys.path.insert(0, GOLD)
    import build_satellites_registry as B

    block = B.build_payload([], "2026-08-27")
    print("  build_payload([], '2026-08-27') ->")
    print("      keys      %s" % sorted(block.keys()))
    print("      books     %r   (len %d)" % (block["books"], len(block["books"])))
    print("      as_of     %r   NON-NULL: %s" % (block["as_of"], block["as_of"] is not None))
    print("      claim     %r" % block["claim"])
    empty_ok = block["books"] == [] and block["as_of"] == "2026-08-27"

    # the guard the estate already wrote, called on OUR block
    B.assert_no_baked_verdict(block)
    print("  assert_no_baked_verdict(block) -> PASSES (no frozen verdict in the bytes)")

    # NEGATIVE ARM: a null as_of must be REFUSED, not published
    try:
        B.build_payload([], None)
        print("  ERROR: build_payload([], None) was ACCEPTED -- the trap is OPEN")
        null_refused = False
    except B.RegistryProducerError as exc:
        print("  build_payload([], None) -> REFUSED: %s" % str(exc).split(".")[0])
        null_refused = True

    # NEGATIVE ARM: a baked verdict must be refused by the reused guard
    try:
        bad = dict(block)
        bad["state"] = "FRESH"
        B.assert_no_baked_verdict(bad)
        print("  ERROR: a baked 'state' was ACCEPTED -- guard did not fire")
        baked_refused = False
    except Exception as exc:
        print("  block + baked 'state' -> REFUSED by assert_no_baked_verdict (%s)"
              % type(exc).__name__)
        baked_refused = True

    # publish() must have NO branch on emptiness
    src = io.open(SUBJECT, encoding="utf-8").read()
    pub = src.split("def publish(", 1)[1].split("\ndef ", 1)[0]
    branches = [t for t in ("len(books)", "if books", "if not books", "delete_object")
                if t in pub]
    print("  publish() emptiness branches / deletes: %s   <- must be []" % branches)
    no_branch = branches == []

    ac3 = empty_ok and null_refused and baked_refused and no_branch
    print("\n" + "=" * 76)
    print("AC1: %s     AC3: %s" % ("PASS" if ac1 else "FAIL", "PASS" if ac3 else "FAIL"))
    print("=" * 76)
    return 0 if (ac1 and ac3) else 1


if __name__ == "__main__":
    sys.exit(main())
