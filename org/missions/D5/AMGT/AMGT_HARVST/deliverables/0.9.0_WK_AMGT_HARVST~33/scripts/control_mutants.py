"""Mutant controls for HVST-z-2's two scripts. Read-only, no S3 call (the snapshot reader is patched).

MUTANT A (ac2): plant 4 rows -- one fully carried with an EMPTY list, one with a NULL mention_in_lead,
one with a NULL co_mentioned_securities, one with a NULL article_key. Expect: 1 carried (empty list
NOT counted missing), 2 failing rows named with their missing column, 1 UNMEASURABLE, verdict NOT MET.
MUTANT B (ac1): patch GOLD_MENTION_SCHEMA to drop signal_tier and ADD a `share` column. Expect: the
strength-grade fact reported ABSENT / not closable, and share reported present (contract violation),
so the census is shown to discriminate rather than always print MAPPED.
"""
import contextlib
import importlib.util
import io
import json
import os
import sys

import pyarrow as pa

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_main(mod):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.main()
    return json.loads(buf.getvalue())


def good(a, s, lst):
    return {"article_key": a, "security_key": s, "mention_in_title": True, "mention_in_lead": False,
            "mention_count": 3, "blocks_hit": 1, "blocks_total": 4, "signal_tier": "T1",
            "co_mentioned_securities": lst}


def main():
    ac2 = load("ac2_census_non_null")
    rows = [good("a1", "s1", []), good("a2", "s2", ["x"]), good("a3", "s3", ["x"]),
            good("a4", "s4", None), good(None, "s5", ["x"])]
    rows[1]["mention_in_lead"] = None
    ac2.pg._latest_gold_snapshot_rows = lambda table, client=None: rows
    r = run_main(ac2)
    print("MUTANT A:", json.dumps({k: r[k] for k in (
        "gold_rows_total_in_newest_snapshot", "unmeasurable_rows_count", "failing_rows_count",
        "failing_rows", "list_column_empty_vs_null_split", "verdict")}))
    a_ok = (r["failing_rows_count"] == 2 and r["unmeasurable_rows_count"] == 1
            and r["met_rows_count"] == 2
            and r["list_column_empty_vs_null_split"]["co_mentioned_securities"]["present_empty"] == 1
            and r["verdict"].startswith("clause (i) NOT MET"))

    ac1 = load("ac1_state_the_mapping")
    fields = [f for f in ac1.pg.GOLD_MENTION_SCHEMA if f.name != "signal_tier"]
    fields.append(pa.field("share", pa.float64()))
    ac1.pg.GOLD_MENTION_SCHEMA = pa.schema(fields)
    r1 = run_main(ac1)
    print("MUTANT B:", json.dumps({"unmapped_facts": r1["unmapped_facts"],
                                   "share_column_finding": r1["share_column_finding"],
                                   "verdict": r1["verdict"]}))
    b_ok = (len(r1["unmapped_facts"]) == 1 and r1["share_column_finding"]["contract_compliant"] is False
            and "NOT CLOSABLE" in r1["verdict"])
    print("MUTANT A FIRED-AS-EXPECTED:", a_ok)
    print("MUTANT B FIRED-AS-EXPECTED:", b_ok)
    sys.exit(0 if (a_ok and b_ok) else 1)


if __name__ == "__main__":
    main()
