set -u
# Ledger irpt-resident-st32-20261011, legs X1 + V2: the ROLLBACK of st32 to st31 (the root that runs today): restore the st31
# receipt the st32 install saved, stop, PUT THE OLD CAPTURE LIBRARY BACK (st31's bindings pin it; its factory refuses otherwise), run the st31 root's own install-resident.sh, verify.
# The renderer drop-in and pydeps stay. No package bytes move. No vendor call. Operator 0.7.0_AE_CloudOps~YC2 for 2.0.0_SA_COO~G2.
OLD=19b02b2971-st31
NEW=0485393f3a-st32
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
OLD_LIB=857d90b81960d69a7a6700be6fffe33d86628694aef95f8cfb64aca7a82cb839
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
qd() { aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text; }
echo "X1 before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent"; exit 10; }
test -f $R/cutover_receipt.$OLD.json || { echo "ERROR: saved receipt cutover_receipt.$OLD.json absent"; exit 11; }
[ "$(sha256sum $H/ycharts_session.js.before-$NEW | cut -d' ' -f1)" = "$OLD_LIB" ] || { echo "ERROR: the kept old library is absent or is not st31's; nothing moved"; exit 12; }
DEPTH=$(qd)
echo "X1 queue visible/in-flight before: $DEPTH"
[ "$DEPTH" = "0	0" ] || { echo "BLOCKED: queue not empty; nothing moved"; exit 20; }
cp -p $R/cutover_receipt.json $R/cutover_receipt.$NEW.json
cp -p $R/cutover_receipt.$OLD.json $R/cutover_receipt.json
echo "X1 receipt restored: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16])")"
systemctl stop $UNIT
install -m 0644 -o root -g root $H/ycharts_session.js.before-$NEW $H/ycharts_session.js
echo "X1 library restored: $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) (want $OLD_LIB)"
PYTHONPATH="$R/$OLD" bash "$R/$OLD/ycharts/generate/install-resident.sh" "$R/$OLD" /usr/bin/python3.12 resident_installed:build_resident_runtime ec2-user $R/cutover_receipt.json
RC=$?
echo "X1 install-resident.sh (st31 root) rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
sleep 25
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "V2 final active: $(systemctl is-active $UNIT) root=$RUN restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "V2 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "V2 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (st31 8e671e18c7858694...)"
echo "V2 renderer drop-in: $(test -f /etc/systemd/system/$UNIT.d/opal-render.conf && echo present || echo absent)"
echo "V2 journal 30s: polls=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c Traceback)"
echo "V2 queue after: $(qd)"
