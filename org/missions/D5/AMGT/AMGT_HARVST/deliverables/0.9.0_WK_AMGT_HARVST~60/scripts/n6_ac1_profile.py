"""HVST-n-6 AC1: the BASELINE.
(a) the deployed /timeline/day timed for the 3 named days (+1 extra 992_HK day that really has
    articles), each 3 times, with the Lambda's own REPORT duration;
(b) the per-step breakdown of the OLD code path run locally against the same S3 reads (list calls,
    objects read, bytes, seconds per step), cold (fresh process) and warm, dominant step named.
READ-ONLY: S3 LIST/GET and read-only Invokes. Output also written to n6_ac1_profile.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import n6_common as c  # noqa: E402

OUT = os.path.join(os.path.dirname(c.HERE), "n6_ac1_profile.json")


def main():
    result = {"deployed": {}, "old_local": {}}
    print("=== (a) DEPLOYED %s /timeline/day: 3 named days + 1 extra, 3 invokes each ===" % c.FUNCTION)
    for key, day in c.ALL_DAYS:
        tag = "%s %s%s" % (key, day, "" if (key, day) in c.NAMED_DAYS else "  [EXTRA day, not named by the TO]")
        rows = []
        for i in range(1, 4):
            wall, rep, status, body = c.invoke_deployed(key, day)
            rows.append({"invoke": i, "client_wall_s": round(wall, 3), "status": status,
                         "report": rep, "body_sha256": c.sha256_text(body), "body_len": len(body),
                         "articles": len(json.loads(body).get("articles") or []) if body else None})
            print("  %s  #%d  client_wall=%.3fs  REPORT %s  status=%s articles=%s body_sha256=%s" % (
                tag, i, wall, rep, status, rows[-1]["articles"], rows[-1]["body_sha256"][:16]))
        result["deployed"]["%s|%s" % (key, day)] = rows
        durs = [r["report"].get("duration_ms") for r in rows if r["report"].get("duration_ms") is not None]
        if durs:
            print("  %s  REPORT duration ms: %s  median=%.0f" % (tag, durs, c.median(durs)))

    print()
    print("=== (b) OLD code path, local, same S3 reads (rep 1 = COLD fresh process, reps 2-3 = warm) ===")
    dom_votes = {}
    for key, day in c.ALL_DAYS:
        reps, _body = c.spawn("old", key, day, 3)
        result["old_local"]["%s|%s" % (key, day)] = reps
        print("--- %s %s  (articles=%s)" % (key, day, reps[0]["articles"]))
        for r in reps:
            print("  rep %d %s total=%.3fs | S3 list ops=%d pages=%d (%.3fs) | S3 gets=%d bytes=%d (sum %.3fs) | "
                  "parquet decode sum=%.3fs" % (
                      r["rep"], "COLD" if r["cold"] else "warm", r["total_s"], r["list_ops"], r["list_pages"],
                      r["list_s"], r["gets"], r["get_bytes"], r["get_s_sum"], r["decode_s_sum"]))
            phased = sum(r["phase_wall_s"].values())
            steps = dict(r["phase_wall_s"])
            steps["join+serve+other"] = round(r["total_s"] - phased, 4)
            for name, sec in sorted(steps.items(), key=lambda kv: -kv[1]):
                s3 = r["phase_s3"].get(name, {})
                print("      step %-34s %.3fs  lists=%s pages=%s gets=%s bytes=%s" % (
                    name, sec, s3.get("list_ops", 0), s3.get("list_pages", 0), s3.get("gets", 0), s3.get("get_bytes", 0)))
            if r["articles"]:
                top = max(steps.items(), key=lambda kv: kv[1])[0]
                dom_votes[(r["cold"], top)] = dom_votes.get((r["cold"], top), 0) + 1
    print()
    print("DOMINANT STEP votes over the reps of the days with articles ((cold?, step): n):", dom_votes)
    steps_dom = {}
    for (cold, step), n in dom_votes.items():
        steps_dom[step] = steps_dom.get(step, 0) + n
    dominant = max(steps_dom.items(), key=lambda kv: kv[1])[0] if steps_dom else "none"
    print("DOMINANT STEP: %s" % dominant)
    result["dominant_step"] = dominant
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
