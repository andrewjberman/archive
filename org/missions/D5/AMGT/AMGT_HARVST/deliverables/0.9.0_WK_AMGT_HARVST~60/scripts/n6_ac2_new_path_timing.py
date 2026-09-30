"""HVST-n-6 AC2: the NEW code path run locally against the same S3 reads for the same days, COLD
(rep 1 of a fresh process) and WARM (reps 2-3 of the same process), per-step breakdown and total
beside the OLD path's, S3 list and object-read counts OLD vs NEW, the ratio per day.

Also: the "first hit on a day the warm process has not seen" figure (a warm Lambda container asked
for a NEW day): one process visiting the days in order, each once.

The OLD path is the verbatim copy in n6_old_path.py (lib code @d357a9e247). Both paths read through
the same metering proxy over the same boto3 client. READ-ONLY: S3 LIST/GET only.
Output also written to n6_ac2_new_path_timing.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import n6_common as c  # noqa: E402

OUT = os.path.join(os.path.dirname(c.HERE), "n6_ac2_new_path_timing.json")


def steps_of(r):
    steps = dict(r["phase_wall_s"])
    steps["join+serve+other"] = round(r["total_s"] - sum(r["phase_wall_s"].values()), 4)
    return steps


def show(label, r):
    print("  %-4s rep %d %s total=%.3fs | S3 LIST ops=%d pages=%d | S3 GET objects=%d bytes=%d | decode sum=%.3fs" % (
        label, r["rep"], "COLD" if r["cold"] else "warm", r["total_s"], r["list_ops"], r["list_pages"],
        r["gets"], r["get_bytes"], r["decode_s_sum"]))
    for name, sec in sorted(steps_of(r).items(), key=lambda kv: -kv[1]):
        s3 = r["phase_s3"].get(name, {})
        print("        step %-34s %.3fs  lists=%s gets=%s bytes=%s" % (
            name, sec, s3.get("list_ops", 0), s3.get("gets", 0), s3.get("get_bytes", 0)))


def main():
    result = {"days": {}, "sequence_new_warm_process": []}
    print("=== OLD vs NEW, per day (local, same S3 reads, 3 reps each in a FRESH process) ===")
    rows = []
    for key, day in c.ALL_DAYS:
        old, old_body = c.spawn("old", key, day, 3)
        new, new_body = c.spawn("new", key, day, 3)
        print("--- %s %s   articles=%s" % (key, day, new[0]["articles"]))
        for r in old:
            show("OLD", r)
        for r in new:
            show("NEW", r)
        eq = old_body == new_body and old[0]["body_sha256"] == new[0]["body_sha256"]
        print("  body OLD==NEW byte-equal: %s  (sha256 %s)" % (eq, new[0]["body_sha256"]))
        o_cold, n_cold = old[0]["total_s"], new[0]["total_s"]
        o_warm = c.median([r["total_s"] for r in old[1:]])
        n_warm = c.median([r["total_s"] for r in new[1:]])
        row = {"key": key, "day": day, "articles": new[0]["articles"], "body_equal": eq,
               "old_cold_s": o_cold, "new_cold_s": n_cold, "old_warm_s": round(o_warm, 4), "new_warm_s": round(n_warm, 4),
               "cold_ratio": round(o_cold / n_cold, 2), "warm_ratio": round(o_warm / n_warm, 2),
               "old_lists": old[0]["list_ops"], "new_lists_cold": new[0]["list_ops"], "new_lists_warm": new[1]["list_ops"],
               "old_gets": old[0]["gets"], "new_gets_cold": new[0]["gets"], "new_gets_warm": new[1]["gets"],
               "old_bytes": old[0]["get_bytes"], "new_bytes_cold": new[0]["get_bytes"], "new_bytes_warm": new[1]["get_bytes"]}
        rows.append(row)
        result["days"]["%s|%s" % (key, day)] = {"old": old, "new": new, "summary": row}

    print()
    print("=== RATIO PER DAY (OLD seconds / NEW seconds) ===")
    print("%-16s %-11s %4s | %9s %9s %7s | %9s %9s %7s | %-12s %-18s %-22s" % (
        "security", "day", "arts", "OLD cold", "NEW cold", "ratio", "OLD warm", "NEW warm", "ratio",
        "LIST o/n(w)", "GET objs o/n/n(w)", "GET bytes o/n/n(w)"))
    for r in rows:
        print("%-16s %-11s %4s | %8.3fs %8.3fs %6.2fx | %8.3fs %8.3fs %6.2fx | %d/%d(%d)%s %d/%d/%d%s %d/%d/%d" % (
            r["key"], r["day"], r["articles"], r["old_cold_s"], r["new_cold_s"], r["cold_ratio"],
            r["old_warm_s"], r["new_warm_s"], r["warm_ratio"], r["old_lists"], r["new_lists_cold"], r["new_lists_warm"],
            "        ", r["old_gets"], r["new_gets_cold"], r["new_gets_warm"], "       ",
            r["old_bytes"], r["new_bytes_cold"], r["new_bytes_warm"]))
        print("      body byte-equal OLD==NEW: %s" % r["body_equal"])

    print()
    print("=== NEW path, ONE warm process visiting the days in order (first hit on a day it has not seen) ===")
    plan = ",".join("%s:%s" % kd for kd in c.ALL_DAYS)
    seq, _ = c.spawn("new", "SEQ", plan, 0)
    for r in seq:
        print("  %s %s visit %d %s total=%.3fs LIST ops=%d GET objects=%d bytes=%d articles=%d" % (
            r["key"], r["day"], r["rep"], "COLD" if r["cold"] else "warm-process", r["total_s"], r["list_ops"],
            r["gets"], r["get_bytes"], r["articles"]))
    result["sequence_new_warm_process"] = seq

    all_equal = all(r["body_equal"] for r in rows)
    print()
    print("ALL DAYS body OLD==NEW byte-equal: %s (%d of %d)" % (all_equal, sum(1 for r in rows if r["body_equal"]), len(rows)))
    with_arts = [r for r in rows if r["articles"]]
    print("MIN RATIO over the %d days with articles: cold %.2fx, warm %.2fx" % (
        len(with_arts), min(r["cold_ratio"] for r in with_arts), min(r["warm_ratio"] for r in with_arts)))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
