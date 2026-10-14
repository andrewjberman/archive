set -uo pipefail
# Ledger irpt-resident-r29-20261014: resident root 0485393f3a-r28 -> 0485393f3a-r29 (the r28 member set with the trunk HEAD blobs of
# intake/uploads.py and ops/status.py replaced (AR-y-308 Shares words; the rest of the r28 member set unchanged, base pin 0485393f3a, package pin f812980d12),
# and the 0485393f3a-r28 root and its library stay on the host for rollback.
# Copy of the r28 script with NEW, OLD, WANT_TAR, the two moved member checks, the ledger and this header changed; written by 0.9.0_WK_IRPT_ANLREQ~125
# for 2.0.0_SA_COO~Y2 (AR-y-311, build only); operator 0.7.0_AE_CloudOps~YC2. Authoring this script uploaded, installed and applied nothing.
NEW=0485393f3a-r29
OLD=0485393f3a-r28
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
ROOT=$R/$NEW
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
KEY=ec2/investor-reporting-ycharts/resident/irpt-resident-$NEW.tar.gz
WANT_TAR=2de2adce622f8bb9bbd5ebc071e862446b056303c0d9ffd7d41b050bd17f51a4
WANT_LIBRARY=a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841
WANT_WRAPPER=55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9
check() { [ "$(sha256sum "$ROOT/$1" | cut -d' ' -f1)" = "$2" ] || { echo "ERROR: $1 is not the built member"; exit 17; }; }
echo "before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) library=$(sha256sum $H/ycharts_session.js | cut -c1-16)"
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent"; exit 10; }
[ "$(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1)" = "$WANT_WRAPPER" ] || { echo "ERROR: the host wrapper is not the package's wrapper; this script moves the library only"; exit 18; }
rm -rf "$ROOT"; mkdir -p "$ROOT"
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" /tmp/irpt-resident-$NEW.tar.gz --only-show-errors --region us-east-1 || exit 11
[ "$(sha256sum /tmp/irpt-resident-$NEW.tar.gz | cut -d' ' -f1)" = "$WANT_TAR" ] || { echo "ERROR: tar is not the built bytes"; exit 16; }
tar -xzf /tmp/irpt-resident-$NEW.tar.gz -C "$ROOT" || exit 12
cd "$ROOT" || exit 13
sha256sum -c SHA256SUMS --quiet && echo "package SHA256SUMS OK ($(wc -l < SHA256SUMS) members)" || exit 14
check "ycharts/generate/resident_main.py" 84e24280401ce85f533a678d34b81c3a02e15da92188e402ee75f1ff39f9f6ed
check "ycharts/generate/resident_worker.py" 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5
check "ycharts/generate/current_authority.py" 5291b3be7e0006ade14db553caa78aa74fc6c91f638e63077a1be15607f16dec
check "ycharts/generate/recipe.py" aeef18516f1152eff5cf45452db8989b431e2e804cf772c78d99c1cb28add89c
check "ycharts/generate/job.py" 02137c1bd42556a7d9988b5cbe4178e8f81a6bea75377ab51dad944694a6a4b2
check "ycharts/generate/transport.py" d8cdbf3907a7d1493de208afbb25d6ef9b6ac4b768be936d880ed4ab0c069960
check "ycharts/generate/publisher.py" 2e83c9f1e38d597d8e10d547e15dc260333606be068b90988899e5eb1a85e620
check "ycharts/generate/templates.json" 54656584f476b616622368d60c227b1519a70f3e9aced14edb88c776f9823866
check "ycharts/extract/extract.py" c4c4908338fdce62972fe7dc0f6250030ad213c88e6d7c6636639430b3dc0bc3
check "ycharts/extract/publication.py" 5a3c676c64ea630909e44d165f126e9351e8a5b8cab9b927d50607a83c1b368b
check "ycharts/extract/certify.py" 0a18fdf5bee20ce3856a7d5b9b404f3e63511d84403d68a6e198e146845ceff1
check "ycharts/session/broker.py" 96f0e7782c106d4930ab5f348fdef9251fa3de33d51e9dfbc920010a33864393
check "ycharts/session/host_capture.py" 324865e6954774a2dc0e359ab2a3362027d9e54a3cf041b727a67f293cc3d545
check "_scope/canonical_profile_reads.py" 30c8a05ad6746d6ae25ded31a5dd26b3789dac1646a23420b9da876c5db438a4
check "_scope/maintained_sources.py" 29c35dbfba72ca031a7d172d74f401b5976ef383d5fc4ef5deaa3a21ab2d1587
check "reports/resident_installed.py" bddb702a20efcebe6194492a8697e45e41fc95de668598ee3fe199e30bf184ba
check "intake/template_reader.py" a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35
check "intake/portfolio.py" d1232a1255b2ea03ff5c7fb04b7282701c6037a1ed5305a12cad7d95f0aa22e8
check "intake/uploads.py" f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494
check "intake/security_resolution.py" 1248f6c0b51d5289fe11f9ee0ca427613b7bdeaf4b10f614bccc05563f2694d3
check "ops/status.py" 87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030
check "ycharts/research/opal_packager.py" e874f26ee8c90d37f8334d7050683b9c541b412ff8cade769e4f4989d4b46ab2
check "lib/trading_calendar.py" 9bc467c6ce4d11e435803681f3ba62835d531cea7c06c39770f1d085c7e4446f
check ycharts-host/ycharts_session.js $WANT_LIBRARY
node --check "$ROOT/ycharts-host/ycharts_session.js" || { echo "ERROR: the new capture library does not parse"; exit 19; }
cp -a $H/pydeps/. "$ROOT/"
rm -rf "$ROOT/bin"
chown -R ec2-user:ec2-user "$ROOT"
python3.12 - <<'PY'
import hashlib, os
rows = []
for dp, dn, fn in os.walk('.'):
    for f in fn:
        p = os.path.join(dp, f)
        if p == './SHA256SUMS':
            continue
        rows.append(hashlib.sha256(open(p, 'rb').read()).hexdigest() + '  ' + p)
rows.sort(key=lambda r: r.split('  ', 1)[1])
open('SHA256SUMS', 'w').write('\n'.join(rows) + '\n')
PY
MAN=$(sha256sum SHA256SUMS | cut -d' ' -f1)
echo "host members $(wc -l < SHA256SUMS) manifest_sha $MAN"
cp -p $R/cutover_receipt.json $R/cutover_receipt.$OLD.json
python3.12 - "$MAN" "$ROOT" <<'PY'
import json, sys, time
path = "/opt/irpt-resident/cutover_receipt.json"
r = json.load(open(path))
r.update({"package_manifest_sha256": sys.argv[1], "package_root": sys.argv[2], "written_by": "0.7.0_AE_CloudOps~YC2",
          "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ledger": "irpt-resident-r29-20261014"})
open(path, "w").write(json.dumps(r, indent=2) + "\n")
PY
chown ec2-user:ec2-user SHA256SUMS $R/cutover_receipt.json
restore_receipt() { cp -p $R/cutover_receipt.$OLD.json $R/cutover_receipt.json; }
queue_depth() { aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text | tr -s ' \t' ' '; }
# The library moves BEFORE the factory check: the factory refuses PINNED_FILE_DIFFERS:library unless the host file is
# the one the bindings pin. The running unit pins the OLD library, so between this swap and the stop below a capture
# would refuse; the queue is read empty first, and again before the stop.
DEPTH0=$(queue_depth)
echo "queue visible/in-flight before the library swap: $DEPTH0"
if [ "$DEPTH0" != "0 0" ]; then restore_receipt; echo "BLOCKED: queue not empty; receipt restored, nothing moved"; exit 20; fi
cp -p $H/ycharts_session.js $H/ycharts_session.js.before-$NEW
install -m 0644 -o root -g root "$ROOT/ycharts-host/ycharts_session.js" $H/ycharts_session.js
restore_library() { install -m 0644 -o root -g root $H/ycharts_session.js.before-$NEW $H/ycharts_session.js; }
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "$WANT_LIBRARY" ] || { restore_library; restore_receipt; echo "BLOCKED: library install did not land; restored"; exit 21; }
sudo -u ec2-user PYTHONPATH="$ROOT" /usr/bin/python3.12 - "$ROOT" <<'PY'
import sys
for rel in ('intake', 'ops', 'reports', '_keys', '_authz', '_gate', 'ycharts/session', 'ycharts/extract'):
    sys.path.insert(0, sys.argv[1] + '/' + rel)
import resident_installed as ri
rt = ri.build_resident_runtime()
print('factory OK:', sorted(rt), 'enrolled', rt['assembly'].session.broker.enrolled_user_id)
PY
if [ $? -ne 0 ]; then restore_library; restore_receipt; echo "BLOCKED: factory failed; library and receipt restored, unit untouched"; exit 15; fi
DEPTH=$(queue_depth)
echo "queue visible/in-flight: $DEPTH"
if [ "$DEPTH" != "0 0" ]; then restore_library; restore_receipt; echo "BLOCKED: queue not empty; library and receipt restored, unit untouched"; exit 20; fi
systemctl stop $UNIT
install_root() {
  PYTHONPATH="$R/$1" bash "$R/$1/ycharts/generate/install-resident.sh" "$R/$1" /usr/bin/python3.12 resident_installed:build_resident_runtime ec2-user $R/cutover_receipt.json
}
install_root $NEW
RC=$?
echo "install $NEW rc=$RC"
sleep 25
ACTIVE=$(systemctl is-active $UNIT)
POLLS=$(journalctl -u $UNIT --since "-30 s" --no-pager | grep -c "IRPT_RESIDENT_POLL")
TRACE=$(journalctl -u $UNIT --since "-30 s" --no-pager | grep -c "Traceback")
echo "active=$ACTIVE polls_30s=$POLLS tracebacks_30s=$TRACE"
if [ $RC -ne 0 ] || [ "$ACTIVE" != active ] || [ "$POLLS" -lt 1 ] || [ "$TRACE" -ne 0 ]; then
  echo "ROLLBACK to $OLD"
  systemctl stop $UNIT
  restore_library
  restore_receipt
  install_root $OLD
  echo "rollback install rc=$?"
  sleep 20
fi
echo "final active: $(systemctl is-active $UNIT)"
systemctl show $UNIT -p MainPID -p ActiveEnterTimestamp -p NRestarts -p ExecStart | cut -c1-200
journalctl -u $UNIT --since "-1 min" --no-pager -o short-iso | cut -c1-200 | tail -6
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "running root $RUN"
echo "running current_authority $(sha256sum $RUN/ycharts/generate/current_authority.py | cut -d' ' -f1) allowedFirmIds mentions $(grep -c allowedFirmIds $RUN/ycharts/generate/current_authority.py)"
echo "running worker $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) PERMANENT_AUTHORITY_REFUSALS mentions $(grep -c PERMANENT_AUTHORITY_REFUSALS $RUN/ycharts/generate/resident_worker.py)"
echo "running reader $(sha256sum $RUN/_scope/canonical_profile_reads.py | cut -d' ' -f1) host library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1)"
