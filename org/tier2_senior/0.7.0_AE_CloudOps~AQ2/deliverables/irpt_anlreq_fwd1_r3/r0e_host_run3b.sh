set -u
# IRPT_ANLREQ TO-RUN-FWD1 window 3 (amendment 4), R0e (READ ONLY): the resident host's live state. Writes nothing.
U=irpt-analysis-resident.service
R=$(systemctl show -p ExecStart --value $U | grep -o '/opt/irpt-resident/[^/]*' | head -1)
echo "R0e unit $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) NRestarts=$(systemctl show -p NRestarts --value $U) running root $R"
echo "R0e receipt: $(ls -t /opt/irpt-resident/cutover_receipt.json 2>/dev/null | head -1) $(tr -d '\n ' < /opt/irpt-resident/cutover_receipt.json 2>/dev/null | cut -c1-260)"
echo "R0e producer list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $R/ycharts/generate/resident_worker.py)"
echo "R0e bindings: $(/usr/bin/python3.12 -c "import json;d=json.load(open('$R/reports/resident_bindings.json'));print('opal_pricing enabled=%s' % d['opal_pricing']['enabled'])")"
echo "R0e checker member sha256: $(sha256sum $R/intake/yfinance_check.py | cut -c1-64) (r34e value 4df9b66cb15ddf71c8d52dbf910d73d0d2d7c8a110c344b1ab242eeaa059a95f)"
echo "R0e r34c root kept: $([ -d /opt/irpt-resident/0485393f3a-r34c ] && echo yes || echo NO); r34d root kept: $([ -d /opt/irpt-resident/0485393f3a-r34d ] && echo yes || echo NO)"
echo "R0e journal since 13:28:50: polls=$(journalctl -u $U --since '2026-10-16 13:28:50' --no-pager 2>/dev/null | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $U --since '2026-10-16 13:28:50' --no-pager 2>/dev/null | grep -c Traceback) sign-in lines=$(journalctl -u $U --since '2026-10-16 13:28:50' --no-pager 2>/dev/null | grep -i -c -E 'capture|eviction|session refresh')"
HOME=/home/ec2-user /usr/bin/python3.12 - /opt/investor-reporting-ycharts/pydeps <<'PYEOF'
import sys
sys.path.append(sys.argv[1])
try:
    import yfinance
    print("R0e yfinance importable by the resident interpreter: %s" % yfinance.__version__)
except Exception as e:
    print("R0e yfinance import FAIL %s" % type(e).__name__)
PYEOF
