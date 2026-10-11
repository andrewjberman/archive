set -u
# Ledger irpt-resident-st30-20261011, leg P1 (READ ONLY): the host state before the st30 install (expect st27 running). No write, no vendor call.
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "P1 at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "P1 active=$(systemctl is-active $UNIT) root=$RUN since=$(systemctl show $UNIT -p ActiveEnterTimestamp --value) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "P1 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "P1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1)"
echo "P1 rollback root e606008994-st27 present: $(test -d $R/e606008994-st27 && echo yes || echo no); running root is it: $([ "$RUN" = "$R/e606008994-st27" ] && echo yes || echo no); members in the running root named packager: $(find $RUN -name '*packager*' | wc -l)"
echo "P1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))")"
echo "P1 library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1)"
echo "P1 pydeps pyarrow: $(test -d $H/pydeps/pyarrow && echo present || echo absent); renderer drop-in: $(test -f /etc/systemd/system/$UNIT.d/opal-render.conf && echo present || echo absent)"
echo "P1 queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text 2>&1)"
echo "P1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
# THE STOP (census part 2, S5; CTO msgs 4597, 4620): the unit must not carry IRPT_ANALYSIS_READY_QUEUE_URL, or I3 goes live with this release.
MP=$(systemctl show $UNIT -p MainPID --value)
E1=$(systemctl show $UNIT -p Environment --value | grep -c IRPT_ANALYSIS_READY_QUEUE_URL)
E2=$(tr '\0' '\n' < /proc/$MP/environ | grep -c '^IRPT_ANALYSIS_READY_QUEUE_URL=')
E3=$(grep -rl IRPT_ANALYSIS_READY_QUEUE_URL /etc/systemd/system/$UNIT /etc/systemd/system/$UNIT.d 2>&1 | grep -c -v 'No such file')
echo "P1 STOP-READ IRPT_ANALYSIS_READY_QUEUE_URL: unit Environment=$E1 running process (pid $MP)=$E2 unit and drop-in files=$E3 (all three must be 0)"
echo "P1 unit EnvironmentFiles: $(systemctl show $UNIT -p EnvironmentFiles --value)"
echo "P1 unit drop-ins: $(ls /etc/systemd/system/$UNIT.d 2>&1 | tr '\n' ' ')"
[ "$E1" = 0 ] && [ "$E2" = 0 ] && [ "$E3" = 0 ] && echo "P1 STOP-READ PASS" || echo "P1 STOP-READ FAIL: do not install; report to 2.0.0_SA_COO~G2"
