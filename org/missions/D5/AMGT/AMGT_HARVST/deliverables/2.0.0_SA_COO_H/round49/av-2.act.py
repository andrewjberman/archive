"""HARVST served gold rebuild #7 (round 49, HVST-av-2) -- THE ACT (issuer; only under the signed never-widen pair,
`round49/NEVER_WIDEN_HALF_COO_GOLD_REBUILD7.md` + the CTO half). The stored link (`url`) reaches the served mention gold.
Same five steps as round37/gold_rebuild5.act.py: BEFORE snapshot; GATE = round48/au-3.signing.py, which writes nothing unless
`RULE (rebuild #7): HOLDS`; ACT = the builders' own CLI, once each; VERIFY on what was written; ROLLBACK = the BEFORE rows
written back as a newer part. The rebuild-#7 rule:
- mention: gone 0; a changed pre-existing row only in class (c) (record_hash alone, equal to the current silver row's);
  every written row carries `url`;
- daily: gone 0; every changed row is in (a) an added mention, (b) as-of-day coverage-only, or (d) past-day coverage-only; OTHER 0.
Writes `round48/au-3.act_<stamp>.json`.
"""
import datetime
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R32 = os.path.join(os.path.dirname(HERE), "round32")
ADDED_FIELDS = ("url",)

_spec = importlib.util.spec_from_file_location("r32_act", os.path.join(R32, "gold_rebuild.act.py"))
a32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a32)
c, pg, store, UNIVERSE = a32.c, a32.pg, a32.store, a32.UNIVERSE
from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402


STATUS_RANK = {"DENIED": 0, "PARTIAL": 1, "COMPLETE": 2}


def coverage_bounds(before, after, as_of, gained_mention):
    """CTO half @b69262724d: class (b) COVERAGE-ONLY is IN only when all four bounds hold. Returns (in_b, bounds)."""
    diff = {f for f in set(before) | set(after)
            if json.dumps(before.get(f), default=str) != json.dumps(after.get(f), default=str)}
    b1 = str(after.get("day"))[:10] == str(as_of)
    b2 = bool(diff) and diff <= {"data_status", "publishers_covered", "publishers_covered_codes"}
    b3 = ((after.get("publishers_covered") or 0) >= (before.get("publishers_covered") or 0)
          and set(after.get("publishers_covered_codes") or []) >= set(before.get("publishers_covered_codes") or [])
          and STATUS_RANK.get(after.get("data_status"), -1) >= STATUS_RANK.get(before.get("data_status"), -1))
    b4 = not gained_mention
    bounds = {"as_of_day": b1, "coverage_fields_only": b2, "coverage_grows": b3, "no_mention_gained": b4,
              "changed": sorted(diff), "status": [before.get("data_status"), after.get("data_status")],
              "covered": [before.get("publishers_covered"), after.get("publishers_covered")],
              "codes": [list(before.get("publishers_covered_codes") or []), list(after.get("publishers_covered_codes") or [])]}
    return b1 and b2 and b3 and b4, bounds


def pre(r):
    return {k: v for k, v in r.items() if k not in ADDED_FIELDS}


def digest_pre(rows):
    return a32.digest([pre(r) for r in rows])


def rule(before_m, before_d, after_m, after_d, as_of=None):
    mk = lambda r: (r.get("article_key"), r.get("security_key"))  # noqa: E731
    dk = lambda r: (r.get("security_key"), str(r.get("day"))[:10])  # noqa: E731
    om_rows, nm_rows = {mk(r): pre(r) for r in before_m}, {mk(r): pre(r) for r in after_m}
    gone = [k for k in om_rows if k not in nm_rows]
    changed = [k for k in nm_rows if k in om_rows
               and json.dumps(nm_rows[k], sort_keys=True, default=str) != json.dumps(om_rows[k], sort_keys=True, default=str)]
    silver_hash = {}
    for pub in sorted({r.get("publisher") for r in after_m if r.get("publisher")}):
        for (ak,), srow in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            silver_hash[ak] = srow.get("record_hash")
    def fields(a, b):
        return {f for f in set(a) | set(b) if json.dumps(a.get(f), default=str) != json.dumps(b.get(f), default=str)}
    hash_only = [k for k in changed if fields(om_rows[k], nm_rows[k]) == {"record_hash"}
                 and nm_rows[k].get("record_hash") == silver_hash.get(k[0])]
    unexplained = [k for k in changed if k not in set(hash_only)]
    bu = {mk(r): r.get("url") for r in before_m}
    au_rows = {mk(r): r for r in after_m}
    url_moves = [k for k in au_rows if k in bu and (bu[k] or None) != (au_rows[k].get("url") or None)]
    url_bad = [k for k in url_moves if bu[k] not in (None, "") or au_rows[k].get("publisher") not in ("ft", "wsj")]
    missing_fields = sum(1 for r in after_m if any(f not in r for f in ADDED_FIELDS))
    with_url = sum(1 for r in after_m if r.get("url"))
    added_secs = {k[1] for k in nm_rows if k not in om_rows}
    od_rows, nd_rows = {dk(r): r for r in before_d}, {dk(r): r for r in after_d}
    od = {k: json.dumps(r, sort_keys=True, default=str) for k, r in od_rows.items()}
    nd = {k: json.dumps(r, sort_keys=True, default=str) for k, r in nd_rows.items()}
    d_gone = [k for k in od if k not in nd]
    d_changed = [k for k in nd if k in od and nd[k] != od[k]]
    cov, past, other, per_row = [], [], [], {}
    for k in d_changed:
        if k[0] in added_secs:
            continue
        in_b, bounds = coverage_bounds(od_rows[k], nd_rows[k], as_of, False)
        if in_b:
            cov.append(k)
        elif bounds["coverage_fields_only"] and bounds["coverage_grows"] and bounds["no_mention_gained"]:
            past.append(k)
        else:
            other.append(k)
            per_row["|".join(k)] = dict(bounds, cls="OTHER")
    return {"mention_gone": len(gone), "mention_changed_pre_existing": len(changed), "mention_hash_only": len(hash_only),
            "mention_changed_unexplained": len(unexplained), "url_fill_e": len(url_moves) - len(url_bad),
            "url_bad_move": len(url_bad), "mention_added": len(nm_rows) - len(om_rows) + len(gone),
            "mention_rows_missing_url": missing_fields, "mention_rows_with_url": with_url,
            "daily_gone": len(d_gone), "daily_changed": len(d_changed),
            "daily_by_added_mention": len([k for k in d_changed if k[0] in added_secs]),
            "daily_coverage_only": len(cov), "daily_past_coverage_only": len(past), "daily_other": len(other),
            "daily_bounds": per_row,
            "holds": not gone and not unexplained and not url_bad and not missing_fields and not d_gone and not other}


def finish(record, rc):
    path = os.path.join(HERE, "av-2.act_%s.json" % record["stamp"])
    json.dump(record, open(path, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", path)
    return rc


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    as_of = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    record = {"stamp": stamp, "as_of": as_of, "universe_file": UNIVERSE, "rebuild": 7}
    bm, bd = a32.snap()
    record["before"] = {"mention_rows": len(bm), "mention_digest_pre": digest_pre(bm), "daily_rows": len(bd),
                        "daily_digest": a32.digest(bd), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                        "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    gate = subprocess.run([sys.executable, os.path.join(HERE, "av-2.signing.py")], cwd=c.ROOT,
                          capture_output=True, text=True, timeout=2400)
    record["gate"] = gate.stdout.strip().splitlines()[-8:]
    print("\n".join(record["gate"]))
    if gate.returncode != 0 or "RULE (rebuild #7): HOLDS" not in gate.stdout:
        record["result"] = "STOP: the rebuild-#7 dry-run rule does not hold; nothing written"
        print(record["result"])
        return finish(record, 1)
    for cmd in ("build-mention", "build-daily"):
        p = subprocess.run([sys.executable, "-m", "lib.research.harvest.publication_gold", cmd, "--securities-json",
                            UNIVERSE, "--as-of", as_of], cwd=c.ROOT, capture_output=True, text=True, timeout=2400)
        record[cmd] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]}
        print(cmd, "rc", p.returncode)
        if p.returncode != 0:
            record["result"] = "STOP: %s rc %d" % (cmd, p.returncode)
            return finish(record, 1)
    am, ad = a32.snap()
    record["after"] = {"mention_rows": len(am), "mention_digest_pre": digest_pre(am), "daily_rows": len(ad),
                       "daily_digest": a32.digest(ad), "mention_part": a32.newest_part(pg.GOLD_TABLE),
                       "daily_part": a32.newest_part(pg.GOLD_DAILY_TABLE)}
    verdict = rule(bm, bd, am, ad, as_of=as_of)
    record["verify"] = verdict
    print("VERIFY:", json.dumps({k: v for k, v in verdict.items() if k != "daily_bounds"}))
    for k, b in verdict["daily_bounds"].items():
        print("  %s %s bounds as_of=%s fields=%s grows=%s no_mention=%s status=%s covered=%s codes=%s" % (
            b["cls"], k, b["as_of_day"], b["coverage_fields_only"], b["coverage_grows"], b["no_mention_gained"],
            b["status"], b["covered"], b["codes"]))
    if verdict["holds"]:
        record["result"] = "DONE: rebuild-#7 rule holds on the written parts"
        return finish(record, 0)
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    pg.write_gold(pg.GOLD_TABLE, bm, as_of, run_stamp, schema=pg.GOLD_MENTION_SCHEMA)
    pg.write_gold(pg.GOLD_DAILY_TABLE, bd, as_of, run_stamp, schema=pg.GOLD_DAILY_SCHEMA)
    rm, rd = a32.snap()
    record["rollback"] = {"mention_digest_pre_equal": digest_pre(rm) == record["before"]["mention_digest_pre"],
                          "daily_digest_equal": a32.digest(rd) == record["before"]["daily_digest"]}
    record["result"] = "ROLLED BACK: the rule failed on the written parts"
    print(record["result"], record["rollback"])
    return finish(record, 1)


if __name__ == "__main__":
    sys.exit(main())
