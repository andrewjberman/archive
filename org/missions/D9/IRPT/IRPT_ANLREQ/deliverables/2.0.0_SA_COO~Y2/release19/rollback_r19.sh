set -u
# Ledger irpt-resident-r19-20261013, leg X1 (NOT run unless the issuer orders it): put the resident back on the st32 root. The library and the wrapper were never moved by r19
# (the install reinstalled the same library bytes), so no library step is needed. Derived from lines 109-112 of resident_host_install_0485393f3a-r19.sh (the installer's own rollback).
NEW=0485393f3a-r19
OLD=0485393f3a-st32
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent; nothing moved"; exit 10; }
test -f $R/cutover_receipt.$OLD.json || { echo "ERROR: $R/cutover_receipt.$OLD.json absent; nothing moved"; exit 11; }
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841" ] || { echo "ERROR: the host library is not st32's; nothing moved"; exit 12; }
echo "X1 before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
systemctl stop $UNIT
cp -p $R/cutover_receipt.$OLD.json $R/cutover_receipt.json
PYTHONPATH="$R/$OLD" bash "$R/$OLD/ycharts/generate/install-resident.sh" "$R/$OLD" /usr/bin/python3.12 resident_installed:build_resident_runtime ec2-user $R/cutover_receipt.json
echo "X1 install $OLD rc=$?"
sleep 25
echo "X1 active=$(systemctl is-active $UNIT) polls_30s=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks_30s=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c Traceback)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "X1 running root $RUN (want $R/$OLD)"
echo "X1 reader members: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) (want 47f89e0b46609c5b... and 76795b75313b0764...)"
echo "X1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))")"
