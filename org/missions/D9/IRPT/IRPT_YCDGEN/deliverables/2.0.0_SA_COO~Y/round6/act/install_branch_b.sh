set -u
# Ledger irpt-ycdgen-r6-branch-b-20261006, leg D2: fetch the signed install script BY KEY, verify, add the renderer environment as a systemd
# drop-in, run the install, then read the running package back. Sent through Systems Manager by host_read.py. No vendor call.
# NOT RUN until the CTO half for branch B is signed and Andrew's word for his sign-in is on that half. Branch B: the allow list holds
# Andrew's principal id, so his requests are served by the Opal producer.
NEW=09139ee34d-st23
OLD=3d705e700f-st22
KEY=ec2/investor-reporting-ycharts/resident/resident_host_install_$NEW.sh
WANT=d3ecf55d0c4e7245679be6bfc4f75a91796490f35151deacbd546fae29cca84d
T=/tmp/resident_host_install_$NEW.sh
R=/opt/irpt-resident
UNIT=irpt-analysis-resident.service
DROPDIR=/etc/systemd/system/$UNIT.d
DROP=$DROPDIR/opal-render.conf
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing moved"; exit 30; }
[ "$(sha256sum $T | cut -d' ' -f1)" = "$WANT" ] || { echo "ERROR: the fetched script is not the signed bytes; nothing moved"; rm -f $T; exit 31; }
echo "install script sha256 verified on the host at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) dropin=$(test -f $DROP && echo present || echo absent)"
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent"; rm -f $T; exit 10; }
DEPTH=$(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)
echo "queue visible/in-flight before: $DEPTH"
[ "$DEPTH" = "0	0" ] || { echo "BLOCKED: queue not empty; nothing moved"; rm -f $T; exit 20; }
# The renderer's environment: render_pdf.cjs finds playwright-core through this variable (the host has no git). A drop-in leaves the unit file the install writes untouched.
mkdir -p $DROPDIR
printf '[Service]\nEnvironment=IRPT_PLAYWRIGHT_CORE=/opt/investor-reporting-ycharts/node_modules/playwright-core\n' > $DROP
chmod 644 $DROP
systemctl daemon-reload
bash $T
RC=$?
rm -f $T
echo "install script rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
ACTIVE=$(systemctl is-active $UNIT)
echo "V1 running root $RUN active=$ACTIVE"
if [ "$RUN" != "$R/$NEW" ] || [ "$ACTIVE" != active ] || [ $RC -ne 0 ]; then
  echo "ROLLBACK STATE: the install script rolled the package back (root $RUN); removing the renderer drop-in"
  rm -f $DROP; rmdir $DROPDIR 2>/dev/null; systemctl daemon-reload
  echo "final: root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) active=$(systemctl is-active $UNIT)"
  exit 40
fi
echo "V1 unit environment: $(systemctl show $UNIT -p Environment --value | cut -c1-260)"
IR=$RUN
chk() { got=$(sha256sum "$IR/$1" 2>/dev/null | cut -d' ' -f1); [ "$got" = "$2" ] && echo "V1 member OK $1" || echo "V1 member DIFF $1 got=$got"; }
chk "reports/resident_bindings.json" 51dd37a2c6de9a5c201afc5f1873450dedfed19f44bf8580061cd0f74f1eee76
chk "infra/logic/registry/reporting_policies.json" cb0167ec4aa98d52ef071670c46384ec5b8627e09ef18359194fdd47080b0e8f
chk "ycharts/generate/resident_worker.py" 9317219ad37ed49235bd11721d35fc18e3190df1620df40a7195d869bee40ce5
chk "ycharts/research/file_stop_row.py" 437ec97deffc47a958dc32df7099aeda92595c8b96a68dd422f3f6a10075b65b
chk "ycharts/research/held_data.py" 69a2912449f287d6ea237471f0ed70db1da67e51ff287cd2c603f376b329ab42
chk "ycharts/research/keeper.py" ee1bb2dcf338d771215bd2787a8dc059b8e343597f226900516c6db290508c0b
chk "ycharts/research/layout_overview.py" e30696d4e694b29168fe6cf70ce536e82196e42da39b94235c5437fa6d805cc5
chk "ycharts/research/lookup.py" 04d79d97ecf93516b18c99e50ec0affa58b498ecda7a0695fc98babb46fb9d84
chk "ycharts/research/map_pdf.py" b7e8793f18612e732286d6dacb821c342d62ccf0f1066229922db45456c9c525
chk "ycharts/research/opal_producer.py" d8e43fc0b337ac7302f5b05cae1adae0b5670628f2322b12e1e6e0e314150636
chk "ycharts/research/overview_map.json" 21a8f6d690bbd28cf7eedfc979c3edcfa8d8a156336d9de779e8438c4913310f
chk "ycharts/research/render_pdf.cjs" 040cbc483ae35d67d0f760fe4d2d8011774134d7843afe66b625d57542e3c890
chk "ycharts/research/runner.py" 5360c965824ce9b7c601021fde102acb846415bc87fe0e5216706cc209b280a1
sudo -u ec2-user ROOT="$IR" /usr/bin/python3.12 - <<'PY'
import hashlib, json, os, sys
root = os.environ["ROOT"]
for rel in ("intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract", "ycharts/generate"):
    sys.path.insert(0, os.path.join(root, rel))
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
sys.path.insert(0, root)
import resident_installed  # noqa: F401
import resident_worker
p = resident_worker.load_opal_producer()
print("V1 producer import OK: family", p.OPAL_FAMILY, "revision", p.OPAL_POLICY_REVISION, "allow list", resident_worker.OPAL_PRODUCER_PRINCIPALS)
b = json.load(open(os.path.join(root, "reports", "resident_bindings.json")))
om = b.get("opal_map") or {}
path = os.path.normpath(os.path.join(root, "reports", om.get("path", "")))
print("V1 opal_map binding: path", om.get("path"), "present", os.path.isfile(path), "sha256 equal", hashlib.sha256(open(path, "rb").read()).hexdigest() == om.get("sha256"))
for mod in ("layout_overview", "runner", "keeper", "held_data"):
    __import__(mod)
print("V1 research modules import OK: layout_overview runner keeper held_data")
PY
echo "V1 queue: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text 2>&1)"
echo "V1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
