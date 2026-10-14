"""IRPT_DASHBD round 102 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msgs 7486 and 7494 (the benchmark-source read; the Cottonwood build cells wait on DB-b-190's re-read).

  DB-b-192 (~157, LOCAL)  a READ: where the four Opal model benchmark returns come from (MDPF's yang-model-portfolio-benchmarks, served as period windows), whether a dated daily
                          model series exists in gold, and what the report's 32 benchmark members can be filled from.                                                 DB102-1-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import json
import re
import sys
from pathlib import Path

RECORD = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~157/BENCHMARK_SOURCE_READ.json"
STEMS = ("benchmark_ultra_short_term", "benchmark_short_term", "benchmark_intermediate_term", "benchmark_long_term")
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
RUN = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def nes(v):
    return isinstance(v, str) and v.strip() != ""


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k) not in ("path", "file", "entry_file", "address", "key"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def check(root):
    p = root / RECORD
    need(p.is_file(), "no %s" % RECORD)
    r = json.loads(p.read_bytes().decode("utf-8"))
    c = json.loads((root / "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json").read_bytes().decode("utf-8"))
    bm = [m["id"] for m in c["members"] if "benchmark" in m["id"]]
    need(len(bm) == 32 and all(any(s in i for s in STEMS) for i in bm), "the contract's benchmark members are 32 across the four stems %s" % (STEMS,))

    pr = r.get("producer") or {}
    need(pr.get("name") == "yang-model-portfolio-benchmarks" and nes(pr.get("entry_file")) and (root / pr["entry_file"]).is_file(), "producer %r: name yang-model-portfolio-benchmarks and an existing entry_file" % pr)
    for k in ("reads", "writes"):
        need(isinstance(pr.get(k), list) and pr[k] and all(isinstance(x, dict) and nes(x.get("address")) and nes(x.get("kind")) for x in pr[k]), "producer.%s must list {address, kind} (at least one)" % k)

    sv = r.get("served") or {}
    need(sv.get("tool") == "mdpf_get_model_benchmarks" and nes(sv.get("bucket")) and nes(sv.get("prefix")) and isinstance(sv.get("windows"), list) and sv["windows"] and all(nes(x) for x in sv["windows"])
         and isinstance(sv.get("dated_series"), bool) and nes(sv.get("vintage")) and nes(sv.get("data_as_of_field")), "served %r: tool mdpf_get_model_benchmarks, bucket, prefix, windows, dated_series, vintage, data_as_of_field" % sv)

    dd = r.get("dated_daily_model_series") or {}
    need(isinstance(dd.get("exists"), bool) and is_int(dd.get("partitions")) and nes(dd.get("evidence")) and ((dd["exists"] is True and nes(dd.get("address")) and isinstance(dd.get("columns"), list) and dd["columns"] and dd["partitions"] > 0)
         or (dd["exists"] is False and dd["partitions"] == 0)), "dated_daily_model_series %r: exists, partitions (above 0 exactly when it exists), evidence, and when it exists an address and columns" % dd)

    bs = r.get("benchmarks")
    need(isinstance(bs, list) and sorted(x.get("member_stem") for x in bs if isinstance(x, dict)) == sorted(STEMS), "benchmarks must hold one entry for each of the four stems %s" % (STEMS,))
    for x in bs:
        need(nes(x.get("served_name")) and isinstance(x.get("found_in_served"), bool), "benchmark %s: served_name and found_in_served" % x.get("member_stem"))

    mp = r.get("mapping_plan") or {}
    ch = mp.get("choice")
    need(ch in ("COMPOUND_FROM_GOLD", "MAP_SERVED_PERIOD_FIGURES", "NOT_ESTABLISHED") and isinstance(mp.get("windows_covered"), list) and set(mp["windows_covered"]) <= set(WINDOWS) and isinstance(mp.get("chart_available"), bool) and nes(mp.get("label_words")),
         "mapping_plan %r: choice, windows_covered (a subset of %s), chart_available, label_words" % (mp, WINDOWS))
    if ch == "COMPOUND_FROM_GOLD":
        need(dd["exists"] is True, "COMPOUND_FROM_GOLD needs a dated daily model series that exists")
    if ch == "MAP_SERVED_PERIOD_FIGURES":
        need(dd["exists"] is False and "since_inception" not in mp["windows_covered"] and mp["chart_available"] is False and all(b["found_in_served"] for b in bs),
             "MAP_SERVED_PERIOD_FIGURES: no dated series, since_inception and the chart stay absent, every benchmark found in the served figures")
    need(nes(r.get("recommendation")), "recommendation must be stated")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0, "reads %r" % rd)
    need(r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "served_values_changed, pushed and deployed must be false")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: benchmark source read: dated daily model series exists: %s; plan %s covering %s" % (str(dd["exists"]).lower(), ch, ",".join(mp["windows_covered"]) or "none"))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid == "DB102-1-AC1", "unknown criterion %r" % cid)
        check(root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB102"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
