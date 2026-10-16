set -u
# IRPT_ANLREQ TO-APPLY-R34C step 7 (V2): through the resident's interpreter (python3.12, ec2-user, the r34c root on the path, pydeps appended) make ONE yf.download call for SPY (period 1mo, interval 1mo, progress off) and ONE YfinanceChecker().check(["SPY"]) call, then load the shipped pool with today's UTC date. No job, no queue message. Prints counts, states, reason codes and exception class names only.
R34=/opt/irpt-resident/0485393f3a-r34c
PYD=/opt/investor-reporting-ycharts/pydeps
HOME=/home/ec2-user /usr/bin/python3.12 - "$R34" "$PYD" <<'PYEOF'
import datetime, os, sys
r34, pyd = sys.argv[1:3]
sub = ["", "ycharts/research", "ycharts/generate", "ycharts/session", "intake", "ops", "reports", "lib"]
sys.path[:0] = [os.path.join(r34, s) if s else r34 for s in sub]
sys.path.append(pyd)
calls = 0
try:
    import yfinance as yf
    print("V2 import yfinance OK %s from %s" % (yf.__version__, "pydeps" if str(yf.__file__).startswith(pyd) else "elsewhere"))
except Exception as e:
    print("V2 import FAIL %s" % type(e).__name__)
    sys.exit(3)
rows = None
try:
    calls += 1
    frame = yf.download("SPY", period="1mo", interval="1mo", progress=False)
    rows = len(frame)
    print("V2 yf.download SPY: call %d, frame returned, rows %d" % (calls, rows))
except Exception as e:
    print("V2 yf.download SPY: call %d, exception class %s" % (calls, type(e).__name__))
state = reason = chk_rows = None
try:
    from yfinance_check import YfinanceChecker
    calls += 1
    res = YfinanceChecker().check(["SPY"])
    r = res.get("SPY", {})
    state, reason, chk_rows = r.get("state"), r.get("reason"), r.get("rows")
    print("V2 YfinanceChecker().check([SPY]): call %d, state %s, reason %s, rows %s" % (calls, state, reason, chk_rows))
except Exception as e:
    print("V2 YfinanceChecker: exception class %s" % type(e).__name__)
print("V2 Yahoo calls made in all: %d (want 2)" % calls)
try:
    import swap_pass
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    pool = swap_pass.load_pool(os.path.join(r34, "ycharts/research/swap_pool.json"), today)
    print("V2 swap_pass.load_pool today=%s: pool_as_of %s pool_claim %s rows_count %s stale %s (stale_days %s)" % (today, pool["pool_as_of"], pool["pool_claim"], pool["rows_count"], pool["stale"], pool["stale_days"]))
except Exception as e:
    print("V2 load_pool: exception class %s" % type(e).__name__)
print("V2 RESULT rows_from_download=%s checker_state=%s" % (rows, state))
PYEOF
