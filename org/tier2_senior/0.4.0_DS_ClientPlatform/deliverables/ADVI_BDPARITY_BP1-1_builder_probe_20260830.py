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
arm("ytd/default-is-proven-Custom-shape",
    [r for r in dr if r["name"]=="Year To Date"][0]["type"] == "Custom", "type=Custom")
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

# A3: the silent-collapse defect must now be LOUD
for bad in (None, ""):
    try:
        L.body_performance_period(account_id=99, q_start=Q_START, q_end=Q_END,
                                  inception=bad, run_year=RUN_YEAR)
        arm("A3/missing-inception-RAISES (%r)" % bad, False, "SILENT COLLAPSE STILL LIVE")
    except ValueError as e:
        arm("A3/missing-inception-RAISES (%r)" % bad, "arithmetically QTD" in str(e), "loud refusal")

# methodology cell (ii) is a parameter, not a baked constant
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
