set -u
# IRPT_ANLREQ TO-APPLY-R34D step 8 (READ ONLY): r34c read back after the rollback. Writes nothing.
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
RUN=$(systemctl show -p ExecStart --value $UNIT | grep -o '/opt/irpt-resident/[^/]*' | head -1)
echo "RB unit $(systemctl is-active $UNIT) MainPID=$(systemctl show -p MainPID --value $UNIT) NRestarts=$(systemctl show -p NRestarts --value $UNIT) ActiveEnter=$(systemctl show -p ActiveEnterTimestamp --value $UNIT)"
echo "RB running root $RUN (want /opt/irpt-resident/0485393f3a-r34c)"
echo "RB member intake/yfinance_check.py sha256 $(sha256sum $RUN/intake/yfinance_check.py | cut -c1-64) (r34c value 343ab79c58de6c2da072f650f3b340e06842edf3eeb8ad6a062ca7a677985808)"
echo "RB allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "RB queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "RB sign-in lines since the unit started: $(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c -i -E 'capture|EVICTION|session refresh')"
echo "RB journal since the unit started: polls=$(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c Traceback)"
echo "RB kept: r34c root $([ -d /opt/irpt-resident/0485393f3a-r34c ] && echo present || echo ABSENT); r34d root $([ -d /opt/irpt-resident/0485393f3a-r34d ] && echo present || echo ABSENT); r34 first-attempt root $([ -d /opt/irpt-resident/0485393f3a-r34 ] && echo present || echo ABSENT); library $(sha256sum /opt/investor-reporting-ycharts/ycharts_session.js | cut -c1-16)"
echo "RB transient V2 unit left: $(systemctl list-units --all --no-legend 2>/dev/null | grep -c -i -E 'v2s|r34d-v2|run-.*yfinance')"
