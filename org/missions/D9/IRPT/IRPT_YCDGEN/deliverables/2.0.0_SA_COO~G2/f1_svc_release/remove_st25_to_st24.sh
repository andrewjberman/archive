set -u
# Ledger irpt-ycdgen-f1-svc-20261008, legs X1 + V2: the REMOVAL release (= the rollback of st25, CTO~DELL2 GO msg 1359): restore the st24
# receipt the st25 install saved, stop, run the st24 root's own install-resident.sh, verify the allow list is Andrew's sign-in only.
# The renderer drop-in and pydeps stay (st24 needs both). No package bytes move. No vendor call. Operator 2.0.0_SA_COO~G2.
OLD=409e3066d1-st24
NEW=3cf5d52a7b-st25
R=/opt/irpt-resident
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
qd() { aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text; }
echo "X1 before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent"; exit 10; }
test -f $R/cutover_receipt.$OLD.json || { echo "ERROR: saved receipt cutover_receipt.$OLD.json absent"; exit 11; }
DEPTH=$(qd)
echo "X1 queue visible/in-flight before: $DEPTH"
[ "$DEPTH" = "0	0" ] || { echo "BLOCKED: queue not empty; nothing moved"; exit 20; }
cp -p $R/cutover_receipt.json $R/cutover_receipt.$NEW.json
cp -p $R/cutover_receipt.$OLD.json $R/cutover_receipt.json
echo "X1 receipt restored: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16])")"
systemctl stop $UNIT
PYTHONPATH="$R/$OLD" bash "$R/$OLD/ycharts/generate/install-resident.sh" "$R/$OLD" /usr/bin/python3.12 resident_installed:build_resident_runtime ec2-user $R/cutover_receipt.json
RC=$?
echo "X1 install-resident.sh (st24 root) rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
sleep 25
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "V2 final active: $(systemctl is-active $UNIT) root=$RUN restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "V2 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "V2 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (st24 9317219ad37ed492...)"
echo "V2 renderer drop-in: $(test -f /etc/systemd/system/$UNIT.d/opal-render.conf && echo present || echo absent)"
echo "V2 journal 30s: polls=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c Traceback)"
echo "V2 queue after: $(qd)"
