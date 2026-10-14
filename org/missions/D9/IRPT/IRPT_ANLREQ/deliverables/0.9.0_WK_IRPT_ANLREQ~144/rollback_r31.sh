set -u
# Ledger irpt-resident-r31-20261014, leg X1 (NOT run unless the issuer orders it): put the resident back on the r29 root. The library bytes are the same before and after
# release 31 (a1c288, reinstalled by the r31 install from the package), so no library step is needed beyond the refusal check.
# Written under IRPT_ANLREQ.TO-AR-y-338 (worker 0.9.0_WK_IRPT_ANLREQ~144). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it only if the issuer orders it.
# Derived from rollback_r30.sh by the AR-y-301 method. Changed: NEW, the reader read-back (the thirteen members the release changes, each at its release-29 sha256, the values the
# rollback target must hold), and the wording. Every refusal guard of rollback_r30.sh is kept with its exit code.
NEW=0485393f3a-r31
OLD=0485393f3a-r29
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent; nothing moved"; exit 10; }
test -f $R/cutover_receipt.$OLD.json || { echo "ERROR: $R/cutover_receipt.$OLD.json absent; nothing moved"; exit 11; }
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841" ] || { echo "ERROR: the host library is not the release-29 library; nothing moved"; exit 12; }
echo "X1 before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
systemctl stop $UNIT
cp -p $R/cutover_receipt.$OLD.json $R/cutover_receipt.json
PYTHONPATH="$R/$OLD" bash "$R/$OLD/ycharts/generate/install-resident.sh" "$R/$OLD" /usr/bin/python3.12 resident_installed:build_resident_runtime ec2-user $R/cutover_receipt.json
echo "X1 install $OLD rc=$?"
sleep 25
echo "X1 active=$(systemctl is-active $UNIT) polls_30s=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks_30s=$(journalctl -u $UNIT --since '-30 s' --no-pager | grep -c Traceback)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "X1 running root $RUN (want $R/$OLD)"
echo "X1 members that release 31 changes, read at the running root (each wanted value is the release-29 sha256):"
for ent in \
  "_scope/interactive_access.py c28d9a74c9af2c5d5014ae54ffda388c2666d24e9c98ac42df3ace457e59e684" \
  "intake/uploads.py f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494" \
  "ops/entry.py 7fba25e33e676b24caf26e680926e5d82bc80f54d6ed83a77dee443125f7d2af" \
  "ops/owned_report.py ba0bc7cabbbc39c1e847e0f255c381d62f1c0c4af21511540eaec0c4cc394cdd" \
  "ops/pdf_link.py 41d98e94d39ea63c7da088a102ff738648b6cd0b6544a0b96611626d185d4afd" \
  "reports/build_resident_package.py c74554be2fa141f17f91d9feb52fa228c114da7e406baeb1037d07b14f2bc9f4" \
  "reports/status_installed.py 326fed4f54b4bbb8419379d686c89faec92ca3ae00846b4d9c9c858fc82d8d13" \
  "ycharts/generate/acceptance.py 138da769bdf424c56dfe8666c1eb4f5e779d32696d16d8cff45066ce3c4b3b99" \
  "ycharts/generate/composition_admission.py 50f5d11cd8ffb8161b9f42af61bdfcdffe698cfc4e66b5cc3338048572563606" \
  "ycharts/generate/resident_worker.py 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5" \
  "ycharts/research/layout_overview.py 752eee099caf720eb1e5ea271f40c01951efb6be4eee38438059b2ff850330d3" \
  "ycharts/research/opal_packager.py e874f26ee8c90d37f8334d7050683b9c541b412ff8cade769e4f4989d4b46ab2" \
  "ycharts/research/opal_producer.py b5f0877e8512e547912b82ae29b68d62464e3f9af124468f27cdf9338066b293"; do
  set -- $ent
  GOT=$(sha256sum $RUN/$1 | cut -d' ' -f1)
  echo "X1 member $1 sha256 $GOT (want $2) $([ "$GOT" = "$2" ] && echo MATCH || echo MISMATCH)"
done
echo "X1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/$OLD and irpt-resident-r29-20261014)"
