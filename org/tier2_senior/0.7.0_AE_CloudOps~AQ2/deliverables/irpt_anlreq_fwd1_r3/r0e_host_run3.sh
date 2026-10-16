set -u
# IRPT_ANLREQ TO-RUN-FWD1 window 3, R0e (READ ONLY): the resident host's live state. Writes nothing.
U=irpt-analysis-resident.service
R=$(systemctl show -p ExecStart --value $U | grep -o '/opt/irpt-resident/[^/]*' | head -1)
echo "R0e unit $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) NRestarts=$(systemctl show -p NRestarts --value $U) running root $R"
echo "R0e receipt: $(ls /opt/irpt-resident/cutover_receipt.* | tail -1) -> $(tr -d '\n' < $(ls /opt/irpt-resident/cutover_receipt.0485393f3a-r34c.json 2>/dev/null | head -1) 2>/dev/null | cut -c1-300)"
echo "R0e producer list: $(grep -h 'OPAL_PRODUCER_PRINCIPALS' $R/ycharts/research/opal_producer.py | head -1)"
echo "R0e bindings: $(/usr/bin/python3.12 -c "import json;d=json.load(open('$R/reports/resident_bindings.json'));print('opal_pricing enabled=%s' % d['opal_pricing']['enabled'])")"
echo "R0e journal since 09:56:45: polls=$(journalctl -u $U --since '2026-10-16 09:56:45' --no-pager 2>/dev/null | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $U --since '2026-10-16 09:56:45' --no-pager 2>/dev/null | grep -c Traceback)"
HOME=/home/ec2-user /usr/bin/python3.12 - /opt/investor-reporting-ycharts/pydeps <<'PYEOF'
import sys
sys.path.append(sys.argv[1])
try:
    import yfinance
    print("R0e yfinance importable by the resident interpreter: %s" % yfinance.__version__)
except Exception as e:
    print("R0e yfinance import FAIL %s" % type(e).__name__)
PYEOF
