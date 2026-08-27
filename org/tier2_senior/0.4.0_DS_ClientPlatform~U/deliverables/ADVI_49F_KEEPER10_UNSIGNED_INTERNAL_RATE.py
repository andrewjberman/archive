"""KEEPER #10's RATE, so the campaign decision rests on a number instead of one account.

The anecdote: 0086046319 on 2026-03-24 serves +158.23% because 12 transfer legs worth $59.5k sit
in the ledger as code-rule INTERNAL with signed_amount == 0.00, so the engine saw cf_net = 0.00.

THE PROXY, and its limits stated up front. For each sampled date I count accounts that are
simultaneously: |r_net| > 20% (outlier band), cf_net == 0.00 (no flow attributed), and holding at
least one INTERNAL/code-rule ledger row with signed_amount == 0.00 (the unsigned-legs signature).
That is a STRONG proxy, not a proof per account -- proving each one needs the fact_trn arithmetic
I ran for 0086046319. I do NOT re-run that per account here; the proxy's job is a RATE.

Reads SERVED artifacts only (twr_daily + flow_ledger, which exist for ~532 of 533 dates), so it
needs none of the A/B-plane inputs that bound CF-3 to 6 partitions. Nothing is written.
"""
import json
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import pandas as pd  # noqa: E402
import runner_common as rc  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
twr_dates = rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/twr_daily")
led_dates = set(rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/flow_ledger"))
usable = [d for d in twr_dates if d in led_dates]
step = max(1, len(usable) // N)
sample = usable[::step][:N]
print(f"twr_daily partitions {len(twr_dates)} | with a flow_ledger too {len(usable)}")
print(f"sampling {len(sample)} evenly across {usable[0]} .. {usable[-1]}\n")

rows = []
for d in sample:
    try:
        twr = rc.read_partition(f"{rc.OUT_ROOT}/canonical/twr_daily", d)
        led = rc.read_partition(f"{rc.OUT_ROOT}/canonical/flow_ledger", d)
    except Exception as exc:
        print(f"  {d}: unreadable ({type(exc).__name__}) -- SKIPPED, not counted")
        continue
    ok = twr[twr["status"] == "OK"].copy()
    if not len(ok):
        print(f"  {d}: 0 computable rows -- SKIPPED")
        continue
    ok["acct"] = ok["account_id"].astype(str).str.zfill(10)
    r = pd.to_numeric(ok["r_net"], errors="coerce")
    cf = pd.to_numeric(ok["cf_net"], errors="coerce").fillna(0.0)
    led["acct"] = led["account_id"].astype(str).str.zfill(10)
    amt = pd.to_numeric(led["signed_amount"], errors="coerce").fillna(0.0)
    unsigned_internal = led[(led["final_class"] == "INTERNAL")
                            & (led["resolution_provenance"] == "code-rule")
                            & (amt == 0.0)]
    suspect_accts = set(unsigned_internal["acct"])
    out20 = ok[(r.abs() > 0.20) & (cf == 0.0)]
    out100 = ok[(r.abs() > 1.00) & (cf == 0.0)]
    hit20 = out20[out20["acct"].isin(suspect_accts)]
    hit100 = out100[out100["acct"].isin(suspect_accts)]
    # ⛔ THIS DICT PREVIOUSLY CARRIED THE KEY "of_those_with_unsigned_internal" TWICE -- once
    # for the >20% hits and again for the >100% hits. Python keeps the LAST, so the pooled
    # summary silently reported the >100% count under the >20% label: 2 (3.3%) where the true
    # figure is 17 (27.9%). The per-date PRINTED lines were right the whole time because they
    # used len(hit20)/len(hit100) directly -- only the aggregate was wrong, which is the worst
    # place for it, since the aggregate is the number a decision reads. Distinct keys now.
    rec = {"date": d, "computable": int(len(ok)),
           "outliers_20pct_noflow": int(len(out20)),
           "hit20_unsigned_internal": int(len(hit20)),
           "outliers_100pct_noflow": int(len(out100)),
           "hit100_unsigned_internal": int(len(hit100)),
           "accounts_holding_unsigned_internal": len(suspect_accts),
           "unsigned_internal_rows": int(len(unsigned_internal))}
    rows.append(rec)
    print(f"  {d}: computable {rec['computable']:>5} | >20% & no-flow {len(out20):>3} "
          f"(unsigned-internal {len(hit20):>3}) | >100% & no-flow {len(out100):>2} "
          f"(unsigned-internal {len(hit100):>2}) | accts holding unsigned-internal "
          f"{len(suspect_accts):>4}")

if rows:
    tc = sum(r["computable"] for r in rows)
    t20 = sum(r["outliers_20pct_noflow"] for r in rows)
    t100 = sum(r["outliers_100pct_noflow"] for r in rows)
    h20 = sum(r["hit20_unsigned_internal"] for r in rows)
    h100 = sum(r["hit100_unsigned_internal"] for r in rows)
    print(f"\n===== POOLED over {len(rows)} partitions of {len(usable)} available")
    print(f"  computable account-days                : {tc:,}")
    print(f"  |r_net|>20% WITH cf_net==0             : {t20:,}  ({100.0*t20/tc:.4f}%)")
    print(f"  |r_net|>100% WITH cf_net==0            : {t100:,}")
    print(f"  of the >20% set, holding unsigned       : {h20:,}  "
          f"({100.0*h20/max(1,t20):.1f}% of that outlier set)")
    print(f"  of the >100% set, holding unsigned      : {h100:,}  "
          f"({100.0*h100/max(1,t100):.1f}% of that outlier set)")
    print("\n  READ THIS AS A RATE, NOT A PROOF: the unsigned-internal column is a SIGNATURE.")
    print("  Per-account proof needs the fact_trn arithmetic run for 0086046319 (legs total vs")
    print("  EMV-BMV move). What the pooled figure supports is how OFTEN the signature appears,")
    print("  which is what a campaign-timing decision actually needs.")
    print(json.dumps(rows, indent=2))
