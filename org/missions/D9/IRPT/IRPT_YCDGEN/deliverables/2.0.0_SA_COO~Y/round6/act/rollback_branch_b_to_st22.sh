set -u
# ROLLBACK of branch B (ledger irpt-ycdgen-r6-branch-b-20261006) to st22, on the CTO's ruling msg 105485 (row IRPT_YCDGEN-S10 armed: the resident
# package lacks the classification client). This is the install script's own rollback path run by hand: restore the st22 receipt the st23 install
# saved, stop, remove the renderer drop-in, run the st22 root's own install-resident.sh, verify. No vendor call. No package bytes move.
OLD=3d705e700f-st22
NEW=09139ee34d-st23
R=/opt/irpt-resident
UNIT=irpt-analysis-resident.service
DROPDIR=/etc/systemd/system/$UNIT.d
DROP=$DROPDIR/opal-render.conf
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
qd() { aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text; }
echo "before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) dropin=$(test -f $DROP && echo present || echo absent)"
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent"; exit 10; }
test -f $R/cutover_receipt.$OLD.json || { echo "ERROR: saved receipt cutover_receipt.$OLD.json absent"; exit 11; }
DEPTH=$(qd)
echo "queue visible/in-flight before: $DEPTH"
[ "$DEPTH" = "0	0" ] || { echo "BLOCKED: queue not empty; nothing moved"; exit 20; }
cp -p $R/cutover_receipt.json $R/cutover_receipt.$NEW.json
cp -p $R/cutover_receipt.$OLD.json $R/cutover_receipt.json
echo "receipt restored: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16])")"
systemctl stop $UNIT
rm -f $DROP; rmdir $DROPDIR 2>/dev/null; systemctl daemon-reload
PYTHONPATH="$R/$OLD" bash "$R/$OLD/ycharts/generate/install-resident.sh" "$R/$OLD" /usr/bin/python3.12 resident_installed:build_resident_runtime ec2-user $R/cutover_receipt.json
RC=$?
echo "install-resident.sh (st22 root) rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
sleep 25
echo "final active: $(systemctl is-active $UNIT)"
systemctl show $UNIT -p MainPID -p ActiveEnterTimestamp -p NRestarts -p ExecStart | cut -c1-200
echo "running root: $(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
echo "unit environment: $(systemctl show $UNIT -p Environment --value | cut -c1-200)"
echo "dropin: $(test -f $DROP && echo present || echo absent)"
echo "journal 30s: polls=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c Traceback)"
echo "queue after: $(qd)"
echo "running worker allow list line: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $R/$OLD/ycharts/generate/resident_worker.py)"
