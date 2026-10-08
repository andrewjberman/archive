"""IRPT_DASHBD round 27 B (issuer 2.0.0_SA_COO~D2) -- row S31: the extended reporting-gold handler measured at the 49F population
(1.0.0_SA_CTO~DELL2 msg 1184: "one trading day of the extended handler over all 7,597 49F accounts. Print wall time and peak memory
against 900 s / 2048 MB, plus the per-account tail. A breach is a finding with its size, not a tuning loop.").

Usage: python <this file> <repo_root> <criterion_id>
  DB27-2-AC1  SIZING_S31.json: `population_count` read from the handler's own population function (>= 7,000), `accounts_run` equal to it
              (or, when stopped at the wall cap, `stopped_at_cap` true with `accounts_run` < population and the cap stated);
              `wall_seconds` and `peak_mb` per stage (returns, class, lots) and in total; `limits` {timeout_s: 900, memory_mb: 2048};
              `per_account_seconds` {p50, p95, p99, max}; `verdict` FITS only when total wall <= 900 and peak <= 2048 and the run was
              not stopped, else BREACH with `breach` naming each limit exceeded and by how much. Base: FAIL.
  DB27-2-AC2  the run measured the handler at HEAD: `handler_sha256` and `producer_sha256` equal the sha256 of
              infra/aws/lambda/investor-reporting/reporting-gold/handler.py and
              data/assets/scripts/gold/irpt_reporting/account_activity_lots.py at the repo root. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~26/SIZING_S31.json"
HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB27-2"))
        sys.exit(1)

    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    if cid == "DB27-2-AC1":
        pop, run = r.get("population_count"), r.get("accounts_run")
        if not isinstance(pop, int) or pop < 7000 or not isinstance(run, int):
            fail("population_count %r, accounts_run %r" % (pop, run))
        stopped = r.get("stopped_at_cap") is True
        if (run != pop and not stopped) or (stopped and (run >= pop or not r.get("cap_seconds"))):
            fail("accounts_run %d of %d, stopped_at_cap %r, cap %r" % (run, pop, r.get("stopped_at_cap"), r.get("cap_seconds")))
        lim = r.get("limits") or {}
        if lim.get("timeout_s") != 900 or lim.get("memory_mb") != 2048:
            fail("limits %r" % lim)
        tot = r.get("total") or {}
        w, m = tot.get("wall_seconds"), tot.get("peak_mb")
        stages = r.get("stages") or {}
        if w is None or m is None or [s for s in ("returns", "class", "lots") if not (stages.get(s) or {}).get("wall_seconds") is not None]:
            fail("total %r or stages %r incomplete" % (tot, sorted(stages)))
        tail = r.get("per_account_seconds") or {}
        if [k for k in ("p50", "p95", "p99", "max") if tail.get(k) is None]:
            fail("per_account_seconds %r" % tail)
        fits = (not stopped) and float(w) <= 900 and float(m) <= 2048
        v = r.get("verdict")
        if v != ("FITS" if fits else "BREACH") or (v == "BREACH" and not r.get("breach")):
            fail("verdict %r disagrees with wall %s s, peak %s MB, stopped %s" % (v, w, m, stopped))
        print("OK: %d of %d accounts; wall %.1f s, peak %.0f MB vs 900 s / 2048 MB; tail p95 %s s, max %s s; %s %s" % (
            run, pop, float(w), float(m), tail["p95"], tail["max"], v, r.get("breach") or ""))
    elif cid == "DB27-2-AC2":
        got = {"handler_sha256": hashlib.sha256((root / HANDLER).read_bytes()).hexdigest(),
               "producer_sha256": hashlib.sha256((root / PRODUCER).read_bytes()).hexdigest()}
        bad = [k for k, v in got.items() if r.get(k) != v]
        if bad:
            fail("%s differ from the files at the root" % bad)
        print("OK: measured handler and producer equal HEAD's bytes")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
