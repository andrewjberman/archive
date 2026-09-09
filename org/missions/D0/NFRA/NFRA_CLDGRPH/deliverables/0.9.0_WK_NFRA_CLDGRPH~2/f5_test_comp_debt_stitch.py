#!/usr/bin/env python3
"""F5-AC1 -- comp-debt's repointed REACHABILITY leg, exercised WITHOUT A NETWORK. TO-CG-F-5.

projection_client is replaced in sys.modules by a stub BEFORE comp_debt is imported, so every row
the dispatcher sees comes from this file. That is also the assertion behind STITCH_LEG_SOURCE: if
the stitch leg still opened a local store, the stub could not account for its rows and the counts
below would not add up.

WHAT EACH ARM IS FOR -- an arm that cannot fail is not a test:
  1  both legs are served      two statements, one connection, no kuzu import anywhere
  2  the scope rides Cypher    each statement names its own type set, built from the constants
  3  the stitch scope is THE   the statement's types are exactly REACH_STITCH_TYPES, so the S31
     named constant            rename is one edit and this test follows it without being touched
  4  DEDUP ACROSS SURFACES     one node_id returned by BOTH legs counts once, and the drop is
                               counted -- the real graph's scopes are disjoint today, so this
                               mechanism is only ever provable on a fixture
  5  script-level filter       gold:a:b is dropped as a function-granular sub-node and counted;
                               gold:a survives
  6  suppression still applies  a suppressed isolate leaves the residual list and is logged
  7  the vintage is the ANSWER'S the line comes from the connection AFTER the queries, so it is
                               the vintage of the rows returned, not of a separate health call
  8  the unreachable REFUSAL   names BOTH served scopes, so a reader of the refusal knows the
                               stitch leg went with it
  9  the retired names are gone STITCH_DB / STITCH_STALE_HOURS / _stitch_freshness are absent
"""
import io
import json
import os
import sys
import types

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("  %-36s %s %s" % (name, "PASS" if ok else "FAIL", detail))


def _find_ws(start):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(12):
        if os.path.isfile(os.path.join(d, "infra", "aws", "globgrph", "comp_debt.py")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise SystemExit("BLOCKED: could not locate the workspace root from " + start)


WS = _find_ws(__file__)
GLOBGRPH = os.path.join(WS, "infra", "aws", "globgrph")

# ---- the stub, installed BEFORE comp_debt is imported -------------------------
STATEMENTS = []
NESSIE_ROWS = [
    {"t": "LAMBDA", "id": "arn:aws:lambda:us-east-1:1:function:only-nessie"},
    {"t": "S3_BUCKET", "id": "arn:aws:s3:::shared-both-surfaces"},      # the DUPLICATE
    {"t": "JSXElement", "id": "out-of-scope-should-never-arrive"},      # scope guard
]
STITCH_ROWS = [
    {"t": "GOLD_SCRIPT", "id": "gold:script_level_one"},
    {"t": "GOLD_SCRIPT", "id": "gold:script_level_one:main"},           # function-granular -> dropped
    {"t": "S3_DATA_KEY", "id": "s3:gold/thing.parquet"},
    {"t": "S3_DATA_KEY", "id": "arn:aws:s3:::shared-both-surfaces"},    # the DUPLICATE, other scope
]
VINTAGE = ("VINTAGE: Built from the estate as of 2026-09-09 21:05:17 UTC. Stitch source: "
           "stitch-codebuild built 2026-09-09T19:55:00Z.  [vintage=2026-09-09T21:05:17+00:00]")


class _Res:
    def __init__(self, rows):
        self._rows, self._i = list(rows), 0

    def has_next(self):
        return self._i < len(self._rows)

    def get_next(self):
        r = self._rows[self._i]
        self._i += 1
        return [r["t"], r["id"]]


class _Conn:
    def __init__(self):
        self.vintage = "2026-09-09T21:05:17+00:00"
        self.age_line = "Built from the estate as of 2026-09-09 21:05:17 UTC. Stitch source: ..."
        self.manifest_sha256 = "09be45b5ff92"
        self.executions = 0

    def execute(self, statement, timeout_s=None):
        STATEMENTS.append(statement)
        self.executions += 1
        return _Res(STITCH_ROWS if "GOLD_SCRIPT" in statement else NESSIE_ROWS)


_STUB = types.ModuleType("projection_client")
_STUB.connect = lambda timeout_s=None: _Conn()
_STUB.vintage_line = lambda source=None, counts=None: VINTAGE
_STUB.health = lambda timeout_s=None: {"status": "ok", "vintage": "2026-09-09T21:05:17+00:00"}
sys.modules["projection_client"] = _STUB

sys.path.insert(0, GLOBGRPH)
import comp_debt as CD          # noqa: E402


def main():
    print("F5-AC1 -- COMP-DEBT'S REPOINTED REACHABILITY LEG, NO NETWORK")
    print("  module under test: %s" % os.path.join(GLOBGRPH, "comp_debt.py"))
    print()

    # suppression must not reach the filesystem's real yaml in a unit test
    CD._load_suppression = lambda: [
        {"id": "FP_TEST_ONLY", "affected_types": ["LAMBDA"], "filter": "isolated_only"}]

    out = CD.dispatch_reachability(("current", "hdr"))

    print("STITCH_LEG_SOURCE=%s" % ("projection_client" if STATEMENTS else "UNKNOWN"))
    print("DEDUP_ACROSS_SURFACES=%d" % out["deduped_across_surfaces"])
    print("UNREACHABLE_REFUSAL_NAMES=", end="")

    # ---- arm 8: the refusal, before anything else prints -------------------------
    def _boom(timeout_s=None):
        raise OSError("connection refused")

    _STUB.health = _boom
    refusal = ""
    try:
        CD.freshness_assert()
    except SystemExit as ex:
        refusal = str(ex)
    _STUB.health = lambda timeout_s=None: {"status": "ok", "vintage": "x"}
    names_both = ("served nessie+stitch" in refusal
                  and "GOLD_SCRIPT" in refusal and "S3_DATA_KEY" in refusal
                  and "no local database to fall back to" in refusal)
    print("served nessie+stitch" if names_both else "INCOMPLETE")
    print()

    check("both_legs_are_served", len(STATEMENTS) == 2,
          "statements=%d on ONE connection" % len(STATEMENTS))
    check("no_kuzu_import_in_the_module", "kuzu" not in sys.modules,
          "sys.modules has no 'kuzu' after a full dispatch")
    check("scope_rides_the_cypher",
          all("n.node_type IN [" in st for st in STATEMENTS),
          "each statement carries its own type set")
    stitch_stmt = [st for st in STATEMENTS if "GOLD_SCRIPT" in st][0]
    scoped = {t.strip().strip("'") for t in
              stitch_stmt.split("n.node_type IN [")[1].split("]")[0].split(",")}
    check("stitch_scope_IS_the_named_constant", scoped == CD.REACH_STITCH_TYPES,
          "statement types %s == REACH_STITCH_TYPES" % sorted(scoped))
    check("dedup_across_surfaces_counts", out["deduped_across_surfaces"] == 1,
          "the shared ARN arrived on BOTH legs and is one entry")
    check("per_surface_counts_reported", out["per_surface_count"] == {"nessie": 2, "stitch": 3},
          "per_surface=%s" % out["per_surface_count"])
    check("out_of_scope_row_never_admitted",
          "out-of-scope-should-never-arrive" not in json.dumps(out),
          "the scope guard holds even if the service over-returns")
    check("gold_subnode_dropped_and_counted", out["gold_subnodes_dropped"] == 1,
          "gold:script_level_one:main dropped, gold:script_level_one kept")
    check("census_is_the_deduped_union", out["census_count"] == 4,
          "census=%d (2+3 rows admitted, 1 shared)" % out["census_count"])
    check("suppression_still_applies", out["suppressed_count"] == 1
          and out["suppressed_log"][0]["cleared_by"] == "FP_TEST_ONLY",
          "the LAMBDA isolate is cleared and LOGGED, not dropped silently")
    check("residual_is_the_remainder", len(out["residual_candidates"]) == 3,
          "residual=%d = census 4 - suppressed 1" % len(out["residual_candidates"]))
    check("vintage_is_the_ANSWERS_not_a_health_call",
          out["served_vintage_line"] == VINTAGE and "Stitch source:" in out["served_vintage_line"])
    check("unreachable_refusal_names_both_scopes", names_both,
          "the refusal names the stitch scope's types and says there is no local fallback")

    src = io.open(os.path.join(GLOBGRPH, "comp_debt.py"), encoding="utf-8").read()
    code = "\n".join(ln for ln in src.splitlines()
                     if not ln.lstrip().startswith("#") and "STITCH_DB and STITCH_STALE" not in ln)
    check("retired_names_absent_from_code",
          not any(n in code for n in ("STITCH_DB =", "STITCH_STALE_HOURS =", "def _stitch_freshness")),
          "the three stitch-local names survive only in the docstring that records their retirement")
    check("no_kuzu_open_in_source",
          "kuzu.Database(" not in src and "kuzu.Connection(" not in src and "import kuzu" not in src)

    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    total = len(RESULTS)
    print()
    print("F5_TESTS=%d passed of %d" % (passed, total))
    print("  DENOMINATOR: %d of %d assertions across 9 named arms, 4 of them controls that must be"
          " able to fail (the duplicate across surfaces, the function-granular sub-node, the"
          " out-of-scope row, and the unreachable refusal's text)." % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
