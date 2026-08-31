import os
import sys
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ["DRY_RUN"] = "1"          # egress stays blocked; we never open a socket
sys.path.insert(0, "infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull")
import lambda_function as L

Q_START, Q_END, RUN_YEAR = "2026-07-01", "2026-08-28", 2026
passed = failed = 0
def arm(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print("  OK:  %-52s %s" % (name, detail))
    else:
        failed += 1
        print("  FAIL:%-52s %s" % (name, detail))

b = L.body_performance_period(account_id=123, q_start=Q_START, q_end=Q_END,
                              inception="2024-03-15", run_year=RUN_YEAR)
dr = b["parameters"]["dateRanges"]
names = [r["name"] for r in dr]
types = [r["type"] for r in dr]

arm("ruled/QTD-present", any(r["type"]=="Custom" and r["startDate"]==Q_START for r in dr), "start=%s" % Q_START)
arm("ruled/YTD-present", "Year To Date" in names, "start=%s" % [r["startDate"] for r in dr if r["name"]=="Year To Date"])
arm("ruled/1Y-trailing-12m-not-calendar-year",
    any(r["name"]=="Trailing 12 Months" and r["startDate"]=="2025-08-28" for r in dr),
    "start=%s" % [r["startDate"] for r in dr if r["name"]=="Trailing 12 Months"])
arm("ruled/SI-present", "SinceInception" in types, "start=%s" % [r["startDate"] for r in dr if r["type"]=="SinceInception"])
# RELATION arm, not a COUNT arm: the baseline has 4 dateRanges (Custom/2025/2024/SI) and a
# len()>=4 test PASSED on it -- certifying the ruled set from a number that never meant it.
ruled_present = {
    "QTD": any(r["type"]=="Custom" and r["startDate"]==Q_START for r in dr),
    "YTD": any(r["name"]=="Year To Date" for r in dr),
    "1Y":  any(r["name"]=="Trailing 12 Months" for r in dr),
    "SI":  any(r["type"]=="SinceInception" for r in dr)}
arm("ruled/ALL-FOUR-ruled-periods-in-ONE-request", all(ruled_present.values()),
    "present=%s" % ruled_present)

# YTD default must be the PROVEN Custom shape, not the un-attested type
# crash-safe: on the BASELINE there is no YTD range at all, and an IndexError here would kill
# the run before the later arms are ever REACHED -- a dead arm reads like a passing one.
_ytd_hits = [r for r in dr if r["name"] == "Year To Date"]
arm("ytd/default-is-proven-Custom-shape",
    bool(_ytd_hits) and _ytd_hits[0]["type"] == "Custom",
    "type=%s" % (_ytd_hits[0]["type"] if _ytd_hits else "NO YTD RANGE"))
bt = L.body_performance_period(account_id=1, q_start=Q_START, q_end=Q_END, inception="2024-01-01",
                               run_year=RUN_YEAR, ytd_mode="typed")
arm("ytd/typed-mode-emits-YearToDate",
    any(r["type"]=="YearToDate" for r in bt["parameters"]["dateRanges"]), "opt-in only")
bb = L.body_performance_period(account_id=1, q_start=Q_START, q_end=Q_END, inception="2024-01-01",
                               run_year=RUN_YEAR, ytd_mode="both")
ytd_b = [r for r in bb["parameters"]["dateRanges"] if r["name"]=="Year To Date"]
arm("ytd/both-mode-carries-2-carriers", len(ytd_b)==2, "types=%s" % [r["type"] for r in ytd_b])
try:
    L.body_performance_period(account_id=1, q_start=Q_START, q_end=Q_END, inception="2024-01-01",
                              run_year=RUN_YEAR, ytd_mode="nonsense")
    arm("ytd/bad-mode-raises", False, "no raise")
except ValueError:
    arm("ytd/bad-mode-raises", True, "ValueError")

# RE-POINTED by 3.0.0_SA_CVO 84169: the SI range is ALWAYS REQUESTED. BD substitutes its own
# funding-inception and ignores our startDate, so omitting the range would drop the very range
# that SUPPLIES the anchor. The strict no-default rule moves to OUR linking side.
for bad in (None, ""):
    nb = L.body_performance_period(account_id=99, q_start=Q_START, q_end=Q_END,
                                   inception=bad, run_year=RUN_YEAR)
    ndr = nb["parameters"]["dateRanges"]
    si = [r for r in ndr if r["type"] == "SinceInception"]
    arm("si/ALWAYS-requested-even-with-no-anchor (%r)" % bad, len(si) == 1,
        "the anchor-supplying range is never dropped")
    arm("si/probe-start-falls-back-to-q_start (%r)" % bad,
        bool(si) and si[0]["startDate"] == Q_START, "a PROBE value, not an anchor assertion")
    arm("si/no-anchor-KEEPS-the-other-periods (%r)" % bad,
        all(any(pred(r) for r in ndr) for pred in (
            lambda r: r["type"] == "Custom" and r["startDate"] == Q_START,
            lambda r: r["name"] == "Year To Date",
            lambda r: r["name"] == "Trailing 12 Months")),
        "QTD/YTD/1Y unaffected")
arm("si/known-anchor-is-passed-through",
    [r for r in dr if r["type"] == "SinceInception"][0]["startDate"] == "2024-03-15",
    "caller's value carried")
try:
    L.body_performance_period(account_id=1, q_start=Q_START, q_end=Q_END, inception="2024-01-01",
                              run_year=RUN_YEAR, anchor_basis="made-up")
    arm("cell-i/bad-anchor_basis-raises", False, "no raise")
except ValueError:
    arm("cell-i/bad-anchor_basis-raises", True, "ValueError")

# POSITION IS THE JOIN (84169): BD returns name=None/type=None, so the probe joins by index and
# certifies with the dates at that index.
idx = L.requested_range_index(b)
arm("join/index-is-dense-and-ordered", [e["index"] for e in idx] == list(range(len(dr))),
    "indices=%s" % [e["index"] for e in idx])
arm("join/index-carries-the-dates-that-certify",
    all(e["startDate"] == dr[e["index"]]["startDate"] and e["endDate"] == dr[e["index"]]["endDate"]
        for e in idx), "start/end recoverable at every index")
arm("join/SI-slot-is-locatable-by-index",
    any(e["type"] == "SinceInception" for e in idx),
    "SI at index %s" % [e["index"] for e in idx if e["type"] == "SinceInception"])

arm("cell-ii/default-is-proven-Annualized",
    b["parameters"]["dataPointOptions"]["returnMethod"] == "Annualized", "default preserved")
bc = L.body_performance_period(account_id=1, q_start=Q_START, q_end=Q_END, inception="2024-01-01",
                               run_year=RUN_YEAR, return_method="Cumulative")
arm("cell-ii/ruling-lands-as-an-ARGUMENT",
    bc["parameters"]["dataPointOptions"]["returnMethod"] == "Cumulative", "no redeploy needed")

# leap-day fold
arm("1Y/leap-day-folds-to-28-Feb", L._minus_one_year("2024-02-29") == "2023-02-28",
    L._minus_one_year("2024-02-29"))

# NEGATIVE CONTROL: the static proven block must be otherwise untouched
dpo = b["parameters"]["dataPointOptions"]
arm("control/proven-static-block-unchanged",
    dpo["feeMethod"]=="NetOfFees" and dpo["feesIn"]=="NetAdditions" and dpo["marketValueMethod"]=="Accrued",
    "fee/feesIn/mv preserved")
arm("control/egress-still-DRY", L.DRY_RUN is True, "DRY_RUN=1, no socket permitted")

print("\nBP1-1 builder probe: %d of %d arms passed." % (passed, passed+failed))
sys.exit(1 if failed else 0)
