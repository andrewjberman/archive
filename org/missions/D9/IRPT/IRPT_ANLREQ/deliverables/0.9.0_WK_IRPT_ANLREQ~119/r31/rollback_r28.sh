set -u
# Ledger irpt-resident-r28-20261013, leg X1 (NOT run unless the issuer orders it): put the resident back on the r19 root. The library bytes are the same before and after
# release 28 (a1c288, reinstalled by the r28 install from the package), so no library step is needed beyond the refusal check.
# Written under IRPT_ANLREQ.TO-AR-y-301 (worker 0.9.0_WK_IRPT_ANLREQ~119). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it only if the issuer orders it.
# Derived from rollback_r19.sh (release 19), which derives from the installer's own rollback (lines 109-112 of the r19 host script). Changed: NEW, OLD, the refusal texts, the
# reader read-backs (the release-19 values), and the rollback root's receipt copy name. Every refusal guard of rollback_r19.sh is kept with its exit code.
NEW=0485393f3a-r28
OLD=0485393f3a-r19
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent; nothing moved"; exit 10; }
test -f $R/cutover_receipt.$OLD.json || { echo "ERROR: $R/cutover_receipt.$OLD.json absent; nothing moved"; exit 11; }
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841" ] || { echo "ERROR: the host library is not the release-19 library; nothing moved"; exit 12; }
echo "X1 before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
systemctl stop $UNIT
cp -p $R/cutover_receipt.$OLD.json $R/cutover_receipt.json
PYTHONPATH="$R/$OLD" bash "$R/$OLD/ycharts/generate/install-resident.sh" "$R/$OLD" /usr/bin/python3.12 resident_installed:build_resident_runtime ec2-user $R/cutover_receipt.json
echo "X1 install $OLD rc=$?"
sleep 25
echo "X1 active=$(systemctl is-active $UNIT) polls_30s=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks_30s=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c Traceback)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "X1 running root $RUN (want $R/$OLD)"
echo "X1 reader members: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) (want 176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) (want 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58)"
echo "X1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/$OLD and irpt-resident-r19-20261013)"
