"""HARVST served gold rebuild #10 (round 72) -- THE ACT (issuer; ONLY under the signed never-widen pair,
`round72/NEVER_WIDEN_HALF_COO_GOLD_REBUILD10.md` + the CTO half).

The served gold moves from the rebuild-#9 matcher to the merged matcher, which adds the capitalised-headline rule (HVST-bk-2)
and the TTE grouping (HVST-bi-1). The list does not move: `round72/securities.universe.r72.json` equals
`round64/securities.universe.r64.json` (242 names). The silver read is whatever is held at the act, which the live
collection leg keeps adding to, so the pair signs the RULE and the act re-reads it on what it writes.

The same five steps as the act script of round 64:
  1. BEFORE  the served snapshot of mention and daily, read and kept in the record;
  2. GATE    `gold_rebuild10.signing.py`, which writes nothing; it must print `RULE (rebuild #10): HOLDS`;
  3. ACT     the builders' own CLI, once each, with the r72 list file;
  4. VERIFY  `gold_rebuild10_rule.rule` on what was WRITTEN, against the BEFORE snapshot;
  5. RECORD  the parts written, the counts, the rollback key per part.
Writes `gold_rebuild10.act_<stamp>.json`. `--gate-only` stops after step 2 and writes nothing to S3.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
R32 = os.path.join(PARENT, "round32")
sys.path.insert(0, HERE)

_spec = importlib.util.spec_from_file_location("r32_act", os.path.join(R32, "gold_rebuild.act.py"))
a32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a32)
c, pg, store = a32.c, a32.pg, a32.store

import gold_rebuild10_rule as r9  # noqa: E402
from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402

R60 = os.path.join(PARENT, "round64", "securities.universe.r64.json")
R64 = os.path.join(HERE, "securities.universe.r72.json")
NAMED = os.path.join(HERE, "REBUILD10_NAMED_REMOVALS.json")
GATE = os.path.join(HERE, "gold_rebuild10.signing.py")
HOLDS = "RULE (rebuild #10): HOLDS"


def silver_hashes(rows):
    result = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (key,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            result[key] = srow.get("record_hash")
    return result


def verify(before_m, before_d, after_m, after_d, as_of):
    served_list = json.load(open(R60, encoding="utf-8"))
    proposed = json.load(open(R64, encoding="utf-8"))
    named_doc = json.load(open(NAMED, encoding="utf-8"))
    named = [(row["article_key"], row["security_key"]) for row in named_doc["rows"]]
    return r9.rule(before_m, before_d, after_m, after_d, served_list, proposed, silver_hashes(after_m), as_of,
                   named_removals=named)


def bnp_counts(rows):
    """CTO half C2 (@d4eb3dc22f): BNP_FP_Equity's pair count, and the pairs whose only matched form is the ticker form."""
    mine = [r for r in rows if r.get("security_key") == "BNP_FP_Equity"]
    only = [r for r in mine if list(r.get("match_forms") or []) == ["BNP"]]
    return {"pairs": len(mine), "pairs_on_the_form_BNP_alone": len(only),
            "keys_on_the_form_alone": sorted(r.get("article_key") for r in only)}


def finish(record, rc):
    path = os.path.join(HERE, "gold_rebuild10.act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    gate_only = "--gate-only" in sys.argv[1:]
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    as_of = now.date().isoformat()
    named_doc = json.load(open(NAMED, encoding="utf-8"))
    record = {"stamp": stamp, "as_of": as_of, "universe_file": R64, "served_universe_file": R60, "rebuild": 10,
              "gate_only": gate_only,
              # CTO msg 31571 term 1 and ADDENDUM 2: what goes, by key, and what is stated and not graded.
              "named_removals": named_doc["rows"], "named_removal_classes": named_doc["classes"],
              "true_pairs_lost": [[r["article_key"], r["security_key"]] for r in named_doc["rows"] if r["true_pair"]],
              "stated_bounds": {
                  "new_alias_forms_no_reviewer_sampled": {
                      "CATERPILLAR INC / CATERPILLAR (CAT_US_Equity, from the identity registry)": "6 pairs added, 77 rows changed at the signing dry run",
                      "American International Group / American International (AIG_US_Equity, the fragment cut)": "0 pairs added, 12 rows changed",
                      "ASML on ASML_US_Equity (issuer grouping)": "0 pairs added, 2 rows changed",
                      "KEYENCE CORP / KEYENCE (6861_JP_Equity)": "0 pairs", "Kimberly-Clark de Mexico (KCDMY_US_Equity)": "0 pairs"},
                  "bnp_gap": "row AMGT_HARVST-Z-W112-S1: dry run 3 of rebuild #8 printed BNP 5 pairs on the form, the served gold holds 2; an UNEXPLAINED 3",
                  "hei_counts": "44 served pairs = 43 with an exact-case HEI span + 1 without (by subtraction); of the 43: 40 name HEICO and stay, 2 bare ticker lists are true pairs lost, 1 is Hawaiian Electric",
                  "symbol_anchors": "CSLLY and HEI.A are evidenced by article spans only (pool 0, registry 0, collector identity record 0)",
                  "ICT_US_Equity": "stays on the list with 0 pairs (1.0.0_SA_CTO~Z msg 31533; row AMGT_RESAPP-Z-S369)"}}
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest": a32.digest(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                        "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    record["bnp_before"] = bnp_counts(bm)
    print("BEFORE: mention %d rows, daily %d rows; parts %s | %s" % (
        len(bm), len(bd), record["before"]["mention_part"], record["before"]["daily_part"]))
    sys.stdout.flush()
    gate = subprocess.run([sys.executable, GATE], cwd=c.ROOT, capture_output=True, text=True, timeout=9000)
    record["gate"] = gate.stdout.strip().splitlines()[-14:]
    print("\n".join(record["gate"]))
    sys.stdout.flush()
    if gate.returncode != 0 or HOLDS not in gate.stdout or "PUTS SENT: 0" not in gate.stdout:
        record["result"] = "STOP: the rebuild-#10 dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    if gate_only:
        record["result"] = "GATE ONLY: the rule holds on the dry run; nothing written"
        print(record["result"])
        return finish(record, 0)
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            R64, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=5400)
        record[cmd] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]}
        print(cmd, "rc", p.returncode)
        sys.stdout.flush()
        if p.returncode != 0:
            record["result"] = "STOP: %s rc %d (a mention part may be written; VERIFY and ROLLBACK follow by hand)" % (
                cmd, p.returncode)
            return finish(record, 1)
    am, ad = a32.snap()
    record["after"] = {"mention_rows": len(am), "mention_digest": a32.digest(am), "daily_rows": len(ad),
                       "daily_digest": a32.digest(ad), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                       "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    record["bnp_after"] = bnp_counts(am)
    print("BNP_FP_Equity: before %s after %s" % (record["bnp_before"], record["bnp_after"]))
    verdict = verify(bm, bd, am, ad, as_of)
    record["verify"] = verdict
    print("VERIFY:", json.dumps({k: v for k, v in verdict.items()
                                 if k not in ("daily_other", "mention_removed_named_keys", "mention_unexplained_sample")}))
    if verdict["holds"]:
        record["result"] = "DONE: the rebuild-#9 rule holds on the written parts"
        print(record["result"])
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, as_of, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, as_of, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_equal": a32.digest(rm) == record["before"]["mention_digest"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
