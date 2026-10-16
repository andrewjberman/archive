set -u
# IRPT_ANLREQ TO-APPLY-R34B V2 (packet section 3 step 5): the Yahoo reads through the resident's interpreter. Sent as the SSM command text.
# EXACTLY two Yahoo calls, both for the ONE ticker SPY: ONE yf.download (period 1mo, interval 1mo, progress off) and ONE
# YfinanceChecker().check(["SPY"]) (its single history call), then swap_pass.load_pool on the shipped pool with today's UTC date.
# No job, no queue message, no write to the resident root. yfinance's tz cache is pointed at a temp directory this process creates and removes.
# Prints counts, states and exception CLASS names only: no message body, no price.
R=/opt/irpt-resident
RUN=$(systemctl show irpt-analysis-resident.service -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
[ "$RUN" = "$R/0485393f3a-r34" ] || { echo "V2 STOP: the running root is ${RUN:-none}, not $R/0485393f3a-r34; nothing was called"; exit 41; }
echo "V2 at $(date -u +%Y-%m-%dT%H:%M:%SZ) root $RUN"
sudo -u ec2-user ROOT="$RUN" HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import datetime
import os
import shutil
import sys
import tempfile

root = os.environ["ROOT"]
for rel in ("intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract", "ycharts/generate"):
    sys.path.insert(0, os.path.join(root, rel))
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
sys.path.insert(0, root)
sys.path.append(os.path.join(root, "ycharts", "research"))
sys.path.append(os.path.join(root, "lib"))
calls = 0
failures = []
cache = tempfile.mkdtemp(prefix="aq2_yf_")
try:
    try:
        import yfinance as yf
        print("V2 import yfinance: OK version %s" % getattr(yf, "__version__", "unknown"))
        if hasattr(yf, "set_tz_cache_location"):
            yf.set_tz_cache_location(cache)
    except Exception as exc:  # noqa: BLE001
        yf = None
        print("V2 import yfinance: FAIL exception_class=%s" % type(exc).__name__)
        failures.append("import:%s" % type(exc).__name__)
    rows = None
    if yf is not None:
        calls += 1
        try:
            frame = yf.download("SPY", period="1mo", interval="1mo", progress=False)
            rows = len(frame)
            print("V2 yf.download SPY (call 1 of 2): rows=%d exception_class=None" % rows)
            if rows == 0:
                failures.append("download:EMPTY_FRAME")
        except Exception as exc:  # noqa: BLE001
            print("V2 yf.download SPY (call 1 of 2): rows=None exception_class=%s" % type(exc).__name__)
            failures.append("download:%s" % type(exc).__name__)
    try:
        from yfinance_check import YfinanceChecker
        calls += 1
        res = YfinanceChecker().check(["SPY"]).get("SPY", {})
        print("V2 YfinanceChecker().check(['SPY']) (call 2 of 2): state=%s reason=%s rows=%s" % (res.get("state"), res.get("reason"), res.get("rows")))
        if res.get("state") != "KEPT":
            failures.append("checker:%s:%s" % (res.get("state"), res.get("reason")))
    except Exception as exc:  # noqa: BLE001
        print("V2 YfinanceChecker().check(['SPY']) (call 2 of 2): FAIL exception_class=%s" % type(exc).__name__)
        failures.append("checker:%s" % type(exc).__name__)
    print("V2 Yahoo call count (yf.download and the checker): %d (the order allows 2)" % calls)
    try:
        import swap_pass
        today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        pool = swap_pass.load_pool(os.path.join(root, "ycharts", "research", "swap_pool.json"), today)
        print("V2 swap_pass.load_pool with today %s: pool_as_of=%s pool_claim=%s rows_count=%d stale=%s stale_days=%s" % (
            today, pool["pool_as_of"], pool["pool_claim"], pool["rows_count"], pool["stale"], pool["stale_days"]))
    except Exception as exc:  # noqa: BLE001
        print("V2 swap_pass.load_pool: FAIL exception_class=%s" % type(exc).__name__)
        failures.append("pool:%s" % type(exc).__name__)
finally:
    shutil.rmtree(cache, ignore_errors=True)
print("V2 RESULT %s" % ("PASS" if not failures else "FAIL " + ",".join(failures)))
PY
echo "V2 python exit code: $?"
