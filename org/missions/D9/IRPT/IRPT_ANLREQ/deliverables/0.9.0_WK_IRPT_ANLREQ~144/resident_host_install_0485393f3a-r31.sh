set -uo pipefail
# Ledger irpt-resident-r31-20261014: resident root 0485393f3a-r29 -> 0485393f3a-r31 (the r29 member set with the trunk blobs of the
# thirteen package members that the merged cells of AR-y-318, AR-y-319, AR-y-327, AR-y-330, AR-y-331, AR-y-333 and AR-y-336 change, the package sums and the
# bindings replaced; base pin 0485393f3a, package pin c4c2afe89639071f41242fc9f663cadaffa0ffd8), and the 0485393f3a-r29 root and its library stay on the host for rollback.
# Copy of the r30 script with NEW, WANT_TAR, the member checks (one per differing member, equal to the extracted r31 tarball), the ledger and this header changed;
# written by 0.9.0_WK_IRPT_ANLREQ~144 for 2.0.0_SA_COO~Y2 (TO-AR-y-338, build only); operator 0.7.0_AE_CloudOps~YC2. Authoring this script uploaded, installed and applied nothing.
NEW=0485393f3a-r31
OLD=0485393f3a-r29
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
ROOT=$R/$NEW
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
KEY=ec2/investor-reporting-ycharts/resident/irpt-resident-$NEW.tar.gz
WANT_TAR=22193944345ce2dd52d2b732ce0ac8d569aa2359958601686239b7e1da8e6021
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
check "SHA256SUMS" 4710d4eab4e4f1e87fdcc4ab422f5b29a70af4fe74423a534dd411603a2db449
check "_scope/interactive_access.py" d416e3755d587b14a0b8ccbd2599b9183bada64c6aed5a9b56edc5a7ce19838b
check "intake/uploads.py" 48f39329ea4c947dc30cba02e07ed499d6f683726204710b16656c29d6f3c0c1
check "ops/entry.py" 8d9b7e76242af5b731875c2fc169e1f57963ecc0f48e97a965549f1e1cabdd1e
check "ops/owned_report.py" fd57437f792d4904232f2a6d2d9c0853e34bce7bc2fc3cd3ff3e76a68712a5d2
check "ops/pdf_link.py" 9ac02114da9383022e4c30bb6a276b7c98b3b92d0999975d679b6fb8dee6ebb0
check "reports/build_resident_package.py" 9cfa787a457cbb3c07945d6023dc431cb5abc0e01f1fed47786292c66be93bc1
check "reports/resident_bindings.json" 804404d95b947d4f12e8b8a521d8867890d6bac195e90eb1df02e7eb33e7ca11
check "reports/status_installed.py" 8ae1892eef9fe43c3e03b53f1310b9663d5a0cb95c8ef108d912ba3a42028de5
check "ycharts/generate/acceptance.py" 0c4acec625b7da70da82efccf58cc967e9e5bf53c32e955d67079b711701513d
check "ycharts/generate/composition_admission.py" 8d9b7aadc7c4db0b078737b155b4ec999d245d20c8bee83515c628639d0f64fd
check "ycharts/generate/resident_worker.py" d779f7dc2e2218822f6b1b2cbca8cc15580202d67e51374f8cd170cb05a31eab
check "ycharts/research/layout_overview.py" c368aa71db3cec88054c0c508fb005d3d97046469ed417e69b509fce824e9f48
check "ycharts/research/opal_packager.py" 3117cceb4ff5107f380ab66e8fd0b2fa16cd194e60853c52137e99bf203f1a12
check "ycharts/research/opal_producer.py" 48fa9af965e3bc92ec6e159f4ba1aa147f6e5a1593cdeec07d8d23a8b83714d6
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
          "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ledger": "irpt-resident-r31-20261014"})
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
