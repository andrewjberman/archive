"""Posture rollup of the committed permission-grain census. Stdlib only, no network/AWS call."""
import json
import sys

CB = "opal-drift-producer-codebuild-role"


def counts(role):
    c = {"used": 0, "never-used": 0, "unobservable": 0}
    for row in role["rows"]:
        c[row["status"]] += 1
    return c


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        b = json.load(fh)
    res = b["results"]
    for label, excl in (("TOTALS", False), ("TOTALS-EXCL-CODEBUILD", True)):
        t = {"used": 0, "never-used": 0, "unobservable": 0}
        n = 0
        for name, r in res.items():
            if excl and name == CB:
                continue
            n += 1
            for k, v in counts(r).items():
                t[k] += v
        g = sum(t.values())
        obs = t["used"] + t["never-used"]
        print(f"{label} roles={n} granted={g} used={t['used']} never-used={t['never-used']} "
              f"unobservable={t['unobservable']}")
        print(f"  {label}-SHARES observable={obs}/{g}={100*obs/g:.1f}% "
              f"used-of-observable={t['used']}/{obs}={100*t['used']/obs:.1f}% "
              f"unobservable={t['unobservable']}/{g}={100*t['unobservable']/g:.1f}% "
              f"never-used-of-observable={t['never-used']}/{obs}={100*t['never-used']/obs:.1f}%")
    no_obs = all_used = with_unused = 0
    for r in res.values():
        c = counts(r)
        if c["used"] + c["never-used"] == 0:
            no_obs += 1
        elif c["never-used"] == 0:
            all_used += 1
        else:
            with_unused += 1
    print(f"ROLE-DISTRIBUTION roles={len(res)} no-observable-grant={no_obs} "
          f"observable-all-used={all_used} observable-with-never-used={with_unused}")
    big = max(res.items(), key=lambda kv: len(kv[1]["rows"]))
    print(f"LARGEST-ROLE {big[0]} grants={len(big[1]['rows'])}")
    print(f"VINTAGE run_date_utc={b['run_date_utc']} lookback_days={b['lookback_days']} "
          f"attempted={b['attempted']} account={b['account']}")


main()
