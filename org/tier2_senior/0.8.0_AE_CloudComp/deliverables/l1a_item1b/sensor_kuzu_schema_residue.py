"""L1a residue sensor (build-order item 1b) -- comp-kuzu assumed schema vs the
LIVE canonical Kuzu binary DB. THE NON-TEXT SHAPE: doc_only is N/A BY SHAPE.

NFRA_COMPLEARN item-1b (dispatch 1.0.0_SA_CTO~Z 20260725T111534Z).
Author: 0.8.0_AE_CloudComp~E. PATTERN, not platform (SENSOR_CONTRACT).

THE QUESTION (L1a): which schema elements does the comp-kuzu layer's OWN source
ASSUME (table names + column refs inside its Cypher string literals / DDL) that
the LIVE canonical Kuzu database does not actually carry -- and vice-plane?

DOC-PLANE STATUS (CORRECTED per CVO~Z bounce 20260725T114312Z -- the original
"N/A BY SHAPE" claim was FALSE): `CALL show_tables()` carries a `comment` FIELD
(['id','name','type','database name','comment']), populatable via
`COMMENT ON TABLE` (kuzu 0.11.3, CVO~Z round-trip on scratch). The surface
therefore HAS a table-level prose plane; on the canonical DB it is EMPTY (''
on every table) -- and EMPTY != ABSENT (L0b-I draft). `doc_only` is
APPLICABLE-AND-MEASURED here: count = tables whose comment is non-empty and
which no query literal walks (0 on canonical today -- a real, measured zero).
Scope nuance, field-enumerated: `table_info` exposes NO comment field, so the
doc plane covers TABLE-kind elements only; column-kind elements have no prose
plane on this surface (disclosed per-kind, not generalized).
THE ORIGINAL ERROR, kept visible: --oracle-check enumerated the metadata
FUNCTIONS while the N/A claim was about their FIELDS -- the `comment` column
was in the returned data all along, summarized away as "name/type/arity only."
The oracle now prints get_column_names() for every metadata call so it can
falsify its own conclusion. CONSEQUENCE: this sensor does NOT satisfy item-1b's
doc_only-N/A-by-shape gate (the surface has a doc plane); the re-target /
L0b-coupling call is CTO~Z's.

DERIVED, NEVER HAND-DECLARED:
  - ASSUMED plane: Cypher string literals extracted from the layer's own .py
    files via ast (string constants containing a Cypher keyword) + the bash
    wrapper's comment example. Per literal: (var:Label) bindings are parsed and
    var.prop refs resolve THROUGH the binding -- an unbound var's props are
    UNKNOWN (reported), never guessed. This is what kills the Python-attr noise
    (r.stdout, m.get): those vars are never Cypher-bound.
  - DECLARED plane: CREATE (NODE|REL) TABLE DDL parsed from the loaders' own
    source (name + column list).
  - LIVE plane: a direct READ-ONLY kuzu connection to the tool's own
    _canonical.CANONICAL_DB_PATH, WITHOUT the wrapper's refresh env vars
    (the comp-kuzu wrapper exports GLOBGRPH_KUZU_INCREMENTAL_REFRESH=1 -- the
    wrapper MUTATES on invoke, so the wrapper is not a read-only oracle; the
    engine's own read path is). The tool's own provenance header is printed
    (_provenance.format_provenance_header) -- never a scratch --db-path vintage.

CELLS (units = schema elements: `table:<T>` and `column:<T>.<c>`;
address_space=kuzu_schema_element, new -- BR008 is designed visibility):
  covered  = ASSUMED (query-side) element present in the live schema
  member   = DECLARED-ONLY (loader DDL) element present in the live schema
             (a row under the known load-plane axis, not query-exercised)
  orphan   = element (either plane) ABSENT from the live schema
  doc_only = applicable=false, count=null -- N/A BY SHAPE (above)
An element in BOTH planes and live counts ONCE, in covered (query use is the
stronger fact); items carry the dual-plane note. UNKNOWN (unbound var props,
un-introspectable tables) is EXCLUDED from surface_total and printed.

CONTENTION: a locked/contended DB (read_only open fails) is UNKNOWN-grade ->
rc=3 REFUSE with explicit DB-CONTENDED language. NEVER a FAIL, NEVER a silent
PASS. Every other unevaluable branch fails closed.

EXIT: 0 CLEAN / 2 VERDICT (orphans) / 3 REFUSE (contended DB or empty
extraction) / 1 FAIL (internal error, nonexistent input, or --out not landing).
READ-ONLY against the DB always. ASCII-only output.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

_THIS = Path(__file__).resolve()
_WORKSPACE = _THIS.parents[5]
_GLOBGRPH = _WORKSPACE / "infra" / "aws" / "globgrph"
sys.path.insert(0, str(_GLOBGRPH))
sys.path.insert(0, str(_WORKSPACE / "org" / "modules" / "graph"))

import boundary_report  # noqa: E402

# The tool's own layer: wrapper + engine + engine imports + the loaders that
# declare the schema. Enumerated here as the SCOPE STATEMENT (memo s2 carries
# the why); the mutant enters via --extra-source, never by editing these.
LAYER_FILES = [
    _WORKSPACE / ".tools" / "comp-kuzu",
    _GLOBGRPH / "kuzu_cli.py",
    _GLOBGRPH / "_canonical.py",
    _GLOBGRPH / "_provenance.py",
    _GLOBGRPH / "kuzu_load.py",
    _GLOBGRPH / "kuzu_nessie_load.py",
    _GLOBGRPH / "kuzu_stitch_load.py",
]

_CYPHER_HINT = re.compile(r"\b(MATCH|RETURN|WHERE|CREATE\s+(?:NODE|REL)\s+TABLE|CALL)\b")
_BINDING = re.compile(r"[(\[]\s*(\w+)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)")
_PROPREF = re.compile(r"\b(\w+)\.([a-z_][a-z0-9_]*)\b")
_DDL = re.compile(
    r"CREATE\s+(NODE|REL)\s+TABLE\s+IF\s+NOT\s+EXISTS\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\)",
    re.S)
_DDL_COL = re.compile(r"^\s*([a-z_][a-z0-9_]*)\s+[A-Z]", re.M)


def cypher_literals_from_py(path: Path):
    """All string constants in a .py that look Cypher-bearing, via ast."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return None  # unparseable source -> caller records UNKNOWN, never skips silently
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if _CYPHER_HINT.search(node.value):
                out.append(node.value)
    return out


def cypher_literals_from_bash(path: Path):
    """Comment/usage lines in a bash wrapper that carry a Cypher example."""
    out = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if _CYPHER_HINT.search(ln):
            out.append(ln)
    return out


def extract_planes(files):
    """(assumed, declared, unknown_refs, per_file_counts)
    assumed:  set of ('table', T) / ('column', T, c) from query-side literals
    declared: same shapes from loader DDL
    unknown:  list of (file, var, prop, reason) -- unbound var refs, reported"""
    assumed, declared, unknown = set(), set(), []
    per_file = {}
    for f in files:
        if not f.is_file():
            unknown.append((str(f), "-", "-", "layer file missing on disk"))
            continue
        lits = (cypher_literals_from_bash(f) if f.suffix != ".py"
                else cypher_literals_from_py(f))
        if lits is None:
            unknown.append((str(f), "-", "-", "source unparseable by ast"))
            continue
        n_before = len(assumed) + len(declared)
        for lit in lits:
            for kind, tname, body in _DDL.findall(lit):
                declared.add(("table", tname))
                for col in _DDL_COL.findall(body):
                    if col not in ("from", "to"):  # REL DDL endpoints, not columns
                        declared.add(("column", tname, col))
            no_ddl = _DDL.sub(" ", lit)  # DDL columns are not query-side refs
            bindings = dict(_BINDING.findall(no_ddl))
            for tname in bindings.values():
                assumed.add(("table", tname))
            for var, prop in _PROPREF.findall(no_ddl):
                if var in bindings:
                    assumed.add(("column", bindings[var], prop))
                elif _CYPHER_HINT.search(lit) and re.search(
                        r"\b(MATCH|RETURN|WHERE)\b", no_ddl) and var in ("n", "m", "a", "b", "e", "r", "p"):
                    # a Cypher-idiomatic var used unbound in this literal:
                    # cannot resolve its table -- UNKNOWN, never guessed.
                    unknown.append((f.name, var, prop, "var not bound to a label in its own literal"))
        per_file[f.name] = (len(assumed) + len(declared)) - n_before
    return assumed, declared, unknown, per_file


def live_schema(db_path: str):
    """((tables:dict name->list[col]|None, comments:dict name->str), err) via a
    DIRECT read-only connection. Field positions are resolved FROM
    get_column_names(), never assumed by index -- the bounce's field-vs-function
    lesson applied to the reader itself.
    None columns = table exists but not introspectable (UNKNOWN-grade for its cols).
    err != None = the DB could not be opened read-only (contended/locked)."""
    import kuzu
    try:
        db = kuzu.Database(db_path, read_only=True)
        conn = kuzu.Connection(db)
    except Exception as e:  # noqa: BLE001 -- the contended path is a designed verdict
        return None, "%s: %s" % (type(e).__name__, e)
    tables, comments = {}, {}
    r = conn.execute("CALL show_tables() RETURN *;")
    fields = r.get_column_names()
    i_name, i_comment = fields.index("name"), (fields.index("comment") if "comment" in fields else None)
    while r.has_next():
        row = r.get_next()
        tables[row[i_name]] = None
        comments[row[i_name]] = (row[i_comment] or "") if i_comment is not None else ""
    for t in list(tables):
        try:
            r2 = conn.execute("CALL table_info('%s') RETURN *;" % t)
            f2 = r2.get_column_names()
            j = f2.index("name")
            cols = []
            while r2.has_next():
                cols.append(r2.get_next()[j])
            tables[t] = cols
        except Exception:  # noqa: BLE001
            tables[t] = None  # exists, columns UNKNOWN -- reported, not guessed
    return (tables, comments), None


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="sensor_kuzu_schema_residue",
        description="item-1b L1a sensor: comp-kuzu assumed schema vs live canonical Kuzu DB. "
                    "Exit: 0 CLEAN / 2 VERDICT / 3 REFUSE / 1 FAIL.")
    ap.add_argument("--extra-source", action="append", default=[],
                    help="additional source file(s) to include (the mutant fixture path)")
    ap.add_argument("--only-source", action="append", default=[],
                    help="REPLACE the layer list with these file(s) -- the CLEAN positive "
                         "control runs on a real layer subset known to reference live schema")
    ap.add_argument("--oracle-check", action="store_true",
                    help="negative/positive-control the LIVE oracle itself, then exit")
    ap.add_argument("--out", default=None, help="write the boundary_report JSON here")
    args = ap.parse_args()

    import _canonical  # noqa: E402  -- the tool's own DB-path authority
    import _provenance  # noqa: E402
    db_path = _canonical.CANONICAL_DB_PATH

    if args.oracle_check:
        # ORACLE CONTROL, separate invocation: it must be able to say YES and NO --
        # and it must print the FIELD NAMES of every metadata call it makes, so the
        # enumeration's denominator is fields, not functions (the bounce's fix: an
        # oracle that summarizes its own returned columns cannot falsify its claim).
        result, err = live_schema(db_path)
        if err:
            print("REFUSE: DB not openable read-only (%s) -- oracle unevaluable, "
                  "UNKNOWN-grade, not a FAIL and not a pass." % err)
            return 3
        tables, comments = result
        import kuzu
        db = kuzu.Database(db_path, read_only=True)
        conn = kuzu.Connection(db)
        r = conn.execute("CALL show_tables() RETURN *;")
        print("ORACLE fields: show_tables() -> %s" % r.get_column_names())
        for t in sorted(tables):
            r2 = conn.execute("CALL table_info('%s') RETURN *;" % t)
            print("ORACLE fields: table_info('%s') -> %s" % (t, r2.get_column_names()))
        print("ORACLE positive: show_tables returned %d table(s): %s"
              % (len(tables), sorted(tables)))
        if not tables:
            print("FAIL: oracle cannot say YES (zero tables) -- do not trust any clean result.")
            return 1
        try:
            conn.execute("CALL table_info('ZzzNoSuchTable9999') RETURN *;")
            print("FAIL: oracle cannot say NO (table_info on a nonexistent table did not error) "
                  "-- an oracle that cannot refuse cannot certify.")
            return 1
        except Exception as e:  # noqa: BLE001
            print("ORACLE negative: table_info('ZzzNoSuchTable9999') errored as required "
                  "(%s). Oracle discriminates both ways." % type(e).__name__)
        print("DOC-PLANE (measured at field level, CORRECTED per the 1143Z bounce): "
              "show_tables carries a 'comment' prose field; canonical values: %s. "
              "table_info carries NO comment field (column-kind elements have no prose "
              "plane). doc_only on this surface is APPLICABLE; EMPTY != ABSENT."
              % {t: repr(c) for t, c in sorted(comments.items())})
        return 0

    base = [Path(p) for p in args.only_source] if args.only_source else list(LAYER_FILES)
    files = base + [Path(p) for p in args.extra_source]
    for p in (Path(p) for p in (args.extra_source + args.only_source)):
        if not p.is_file():
            print("FAIL: source file does not exist: %s (a nonexistent domain is not an "
                  "empty one)." % p)
            return 1

    assumed, declared, unknown, per_file = extract_planes(files)
    if not assumed and not declared:
        print("REFUSE: zero schema references extracted from %d layer file(s) -- nothing "
              "could be compared." % len(files))
        return 3

    result, err = live_schema(db_path)
    if err:
        print("REFUSE (DB-CONTENDED/UNKNOWN-grade): canonical DB not openable read-only: %s. "
              "Per the 6-lane contention lesson this is NEVER a FAIL and NEVER a silent "
              "PASS -- re-run when the writer lock clears." % err)
        return 3
    tables, comments = result
    print(_provenance.format_provenance_header(db_path), file=sys.stderr)

    # doc_only, CORRECTED (bounce 1143Z): the table-level comment plane EXISTS.
    # Count = tables carrying a NON-EMPTY comment that no query literal walks.
    assumed_tables = {el[1] for el in assumed if el[0] == "table"}
    doc_named_unwalked = sorted(t for t, c in comments.items()
                                if c.strip() and t not in assumed_tables)

    def is_live(el):
        """True/False/None(=UNKNOWN: table exists but columns not introspectable)."""
        if el[0] == "table":
            return el[1] in tables
        t, c = el[1], el[2]
        if t not in tables:
            return False
        if tables[t] is None:
            return None
        return c in tables[t]

    covered, member, orphan = [], [], []
    unknown_live = []
    for el in sorted(assumed | declared):
        v = is_live(el)
        if v is None:
            unknown_live.append(el)
        elif not v:
            orphan.append(el)
        elif el in assumed:
            covered.append(el)   # dual-plane counts ONCE, here
        else:
            member.append(el)    # declared-only, live

    surface_total = len(covered) + len(member) + len(orphan) + len(doc_named_unwalked)

    def addr(el):
        return ("table:%s" % el[1]) if el[0] == "table" else "column:%s.%s" % (el[1], el[2])

    report = {
        "tool": "comp-kuzu",
        "source": "kuzu layer source (%d file(s)%s) vs LIVE %s" % (
            len(files),
            ", restricted" if args.only_source else (
                " + %d extra" % len(args.extra_source) if args.extra_source else ""),
            Path(db_path).name),
        "address_space": "kuzu_schema_element",
        "head": "kuzu_nessie_db@read-only (provenance header above; pin==marker checked by the tool's own header)",
        "surface_total": surface_total,
        "cells": {
            "covered": {"applicable": True, "count": len(covered), "method": "mention"},
            "member": {"applicable": True, "count": len(member), "method": "mention"},
            "doc_only": {"applicable": True, "count": len(doc_named_unwalked), "method": "mention"},
            "orphan": {"applicable": True, "count": len(orphan), "method": "mention"},
        },
        "doc_only_status": (
            "CORRECTED (CVO~Z bounce 20260725T114312Z; original 'no prose plane exists' claim "
            "FALSIFIED): show_tables() carries a table-level 'comment' prose field, populatable "
            "via COMMENT ON TABLE (kuzu 0.11.3 round-trip, CVO~Z scratch). On canonical the "
            "plane is EMPTY ('' on every table) -- doc_only is APPLICABLE with a measured count "
            "(%d). BOTH readings' consequence, labels PROVISIONAL pending the L0b ratification: "
            "under the L0b-I draft EMPTY is a DISTINCT member from ABSENT, so this surface does "
            "NOT demonstrate N/A-by-shape and does NOT clear item 1b; were EMPTY ruled "
            "equivalent to ABSENT (not the draft's position), the original claim would still "
            "have been wrong about the FIELD's existence. Scope per-kind: table_info exposes no "
            "comment field, so column-kind elements carry no prose plane on this surface."
            % len(doc_named_unwalked)),
        "items": (
            [{"address": addr(e), "cell": "orphan", "method": "mention",
              "evidence": "referenced in layer source (%s plane); ABSENT from live schema"
                          % ("assumed" if e in assumed else "declared")} for e in orphan]
            + [{"address": addr(e), "cell": "member", "method": "mention",
                "evidence": "declared in loader DDL, present live, never query-referenced"}
               for e in member]
            + [{"address": "table:%s" % t, "cell": "doc_only", "method": "mention",
                "evidence": "table carries a non-empty live comment; no query literal walks it"}
               for t in doc_named_unwalked]
        ),
    }

    violations = boundary_report.validate(report)
    hard = [v for v in violations if v.code != "BR008"]
    for v in violations:
        print("CONFORMANCE%s: %s at %s: %s"
              % ("" if v.code != "BR008" else " (expected, new shape)", v.code, v.where, v.message))
    if hard:
        print("FAIL: emitted report NON-CONFORMANT (%d hard violation(s))." % len(hard))
        return 1

    # RAW ACCOUNTING LINE (the input-4 contract) + both-side denominators + UNKNOWN + direction
    print("SENSOR comp-kuzu schema residue -- LIVE db=%s" % Path(db_path).name)
    print("  ACCOUNTING: N=%d = covered %d + member %d + doc_only %d + orphan %d"
          % (surface_total, len(covered), len(member), len(doc_named_unwalked), len(orphan)))
    print("  DOC-PLANE (corrected 1143Z): table-level comment field EXISTS, canonical values "
          "all EMPTY (%s) -- doc_only APPLICABLE-and-measured, EMPTY != ABSENT (provisional "
          "pending L0b); column-kind elements have no prose plane (table_info field-checked)."
          % ", ".join("%s=%r" % (t, c) for t, c in sorted(comments.items())))
    print("  DENOMINATOR (assumed-refs side): %d query-assumed + %d loader-declared distinct "
          "elements from %d file(s): %s"
          % (len(assumed), len(declared), len(files),
             ", ".join("%s=%d" % kv for kv in sorted(per_file.items()))))
    print("  DENOMINATOR (live side): %d table(s); columns: %s"
          % (len(tables), ", ".join("%s=%s" % (t, len(c) if c is not None else "UNKNOWN")
                                    for t, c in sorted(tables.items()))))
    print("  UNKNOWN (first-class, EXCLUDED from N): %d unbound-var ref(s)%s; %d element(s) on "
          "un-introspectable table(s)%s"
          % (len(unknown), " -- " + "; ".join("%s %s.%s (%s)" % u for u in unknown[:8]) if unknown else "",
             len(unknown_live), " -- " + ", ".join(addr(e) for e in unknown_live[:8]) if unknown_live else ""))
    print("  DIRECTION: both planes are source-text extraction (mention) and UNDER-report -- "
          "a dynamically composed query string is invisible to ast/regex extraction. Residue "
          "can be an UNDERCOUNT, never an overcount; live-side lookups are exact.")
    for it in report["items"]:
        if it["cell"] == "orphan":
            print("  RESIDUE [orphan] %s -- %s" % (it["address"], it["evidence"]))

    if args.out:
        out_path = Path(args.out).resolve()
        payload = json.dumps(report, indent=2) + "\n"
        try:
            out_path.write_text(payload, encoding="utf-8")
        except OSError as e:
            print("FAIL: could not write report to %s (%s: %s)" % (out_path, type(e).__name__, e))
            return 1
        if not out_path.is_file() or out_path.stat().st_size < len(payload):
            print("FAIL: report write did not land at %s." % out_path)
            return 1
        print("  REPORT WRITTEN (verified on disk): %s" % out_path)

    if orphan:
        print("VERDICT: %d orphan element(s) of %d surface -- boundary statement, not a "
              "materiality judgment." % (len(orphan), surface_total))
        return 2
    print("CLEAN: every extracted schema element is present in the live schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
