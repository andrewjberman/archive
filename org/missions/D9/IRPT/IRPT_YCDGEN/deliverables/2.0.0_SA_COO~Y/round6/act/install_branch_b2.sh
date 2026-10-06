set -u
# Ledger irpt-ycdgen-r6-branch-b2-20261006, leg D2: stage the pinned pyarrow into the host's pydeps, fetch the signed install script BY KEY, verify, add the
# renderer environment as a systemd drop-in, run the install, read the running package back. Sent through Systems Manager by host_read.py. No vendor call.
# NOT RUN until the CTO half for branch B2 is signed. The install script copies the host pydeps into the new root (`cp -a $H/pydeps/. $ROOT/`), which is
# how pyarrow reaches the package: no PYTHONPATH change, no unit-file change.
NEW=409e3066d1-st24
OLD=3d705e700f-st22
KEY=ec2/investor-reporting-ycharts/resident/resident_host_install_$NEW.sh
WANT=c9ad01d7f1a15108e7b59424b30cc845651af55269f4aa78153bf21b3782e9b0
AKEY=ec2/investor-reporting-ycharts/resident/deps/pyarrow-18.1.0-cp312-awssdkpandas16.tar.gz
AWANT=dad8a09e088722e1fc4b506b921583a3d62b7097a7eacf0907bce6f284393506
T=/tmp/resident_host_install_$NEW.sh
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
PYD=$H/pydeps
UNIT=irpt-analysis-resident.service
DROPDIR=/etc/systemd/system/$UNIT.d
DROP=$DROPDIR/opal-render.conf
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
undo_pyarrow() { rm -rf $PYD/pyarrow $PYD/pyarrow-18.1.0.dist-info; }
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing moved"; exit 30; }
[ "$(sha256sum $T | cut -d' ' -f1)" = "$WANT" ] || { echo "ERROR: the fetched script is not the signed bytes; nothing moved"; rm -f $T; exit 31; }
echo "install script sha256 verified on the host at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "before: active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) dropin=$(test -f $DROP && echo present || echo absent) pydeps_pyarrow=$(test -d $PYD/pyarrow && echo present || echo absent)"
test -d $R/$OLD || { echo "ERROR: rollback root $OLD absent"; rm -f $T; exit 10; }
test -d $PYD/pyarrow && { echo "BLOCKED: pydeps already holds a pyarrow; refusing to overwrite it"; rm -f $T; exit 12; }
DEPTH=$(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)
echo "queue visible/in-flight before: $DEPTH"
[ "$DEPTH" = "0	0" ] || { echo "BLOCKED: queue not empty; nothing moved"; rm -f $T; exit 20; }
# 1. the pinned pyarrow into the host's pydeps (the running st22 service does not read this directory; only the next install copies it)
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$AKEY" /tmp/pyarrow-pin.tar.gz --only-show-errors --region us-east-1 || { echo "ERROR: fetch pyarrow failed; nothing moved"; rm -f $T; exit 33; }
[ "$(sha256sum /tmp/pyarrow-pin.tar.gz | cut -d' ' -f1)" = "$AWANT" ] || { echo "ERROR: pyarrow tar is not the pinned bytes; nothing moved"; rm -f $T /tmp/pyarrow-pin.tar.gz; exit 34; }
tar -xzf /tmp/pyarrow-pin.tar.gz -C $PYD || { echo "ERROR: pyarrow extract failed"; undo_pyarrow; rm -f $T /tmp/pyarrow-pin.tar.gz; exit 35; }
chown -R ec2-user:ec2-user $PYD/pyarrow $PYD/pyarrow-18.1.0.dist-info
rm -f /tmp/pyarrow-pin.tar.gz
echo "pyarrow staged in pydeps: $(ls $PYD/pyarrow | wc -l) entries, $(du -sh $PYD/pyarrow | cut -f1)"
# 2. the renderer's environment as a drop-in
mkdir -p $DROPDIR
printf '[Service]\nEnvironment=IRPT_PLAYWRIGHT_CORE=/opt/investor-reporting-ycharts/node_modules/playwright-core\n' > $DROP
chmod 644 $DROP
systemctl daemon-reload
# 3. the signed install script
bash $T
RC=$?
rm -f $T
echo "install script rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
ACTIVE=$(systemctl is-active $UNIT)
echo "V1 running root $RUN active=$ACTIVE"
if [ "$RUN" != "$R/$NEW" ] || [ "$ACTIVE" != active ] || [ $RC -ne 0 ]; then
  echo "ROLLBACK STATE: the install script rolled the package back (root $RUN); removing the renderer drop-in and the staged pyarrow"
  rm -f $DROP; rmdir $DROPDIR 2>/dev/null; undo_pyarrow; systemctl daemon-reload
  echo "final: root=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) active=$(systemctl is-active $UNIT)"
  exit 40
fi
echo "V1 unit environment: $(systemctl show $UNIT -p Environment --value | cut -c1-260)"
IR=$RUN
echo "V1 pyarrow in the new root: $(test -d $IR/pyarrow && echo present || echo absent)"
chk() { got=$(sha256sum "$IR/$1" 2>/dev/null | cut -d' ' -f1); [ "$got" = "$2" ] && echo "V1 member OK $1" || echo "V1 member DIFF $1 got=$got"; }
chk "reports/resident_bindings.json" 34f949a5bcc0019642212535abefa08e2ae42e3ecbe4729c323ad1b9b2080e5a
chk "infra/logic/registry/reporting_policies.json" cb0167ec4aa98d52ef071670c46384ec5b8627e09ef18359194fdd47080b0e8f
chk "ycharts/generate/resident_worker.py" 9317219ad37ed49235bd11721d35fc18e3190df1620df40a7195d869bee40ce5
chk "ycharts/research/etf_classifications_dynamodb.py" 92b64d97d69bfee9bc2d4b06fe13c8719a30856fc70f8588e1b29289f89afccc
chk "ycharts/research/file_stop_row.py" 437ec97deffc47a958dc32df7099aeda92595c8b96a68dd422f3f6a10075b65b
chk "ycharts/research/held_data.py" 69a2912449f287d6ea237471f0ed70db1da67e51ff287cd2c603f376b329ab42
chk "ycharts/research/keeper.py" ee1bb2dcf338d771215bd2787a8dc059b8e343597f226900516c6db290508c0b
chk "ycharts/research/layout_overview.py" a1c125427680a6f7526de07e3f1a16943d59c4a3e1c5dac9767b14ad0b98d891
chk "ycharts/research/lookup.py" 04d79d97ecf93516b18c99e50ec0affa58b498ecda7a0695fc98babb46fb9d84
chk "ycharts/research/map_pdf.py" b7e8793f18612e732286d6dacb821c342d62ccf0f1066229922db45456c9c525
chk "ycharts/research/opal_producer.py" d8e43fc0b337ac7302f5b05cae1adae0b5670628f2322b12e1e6e0e314150636
chk "ycharts/research/overview_map.json" 21a8f6d690bbd28cf7eedfc979c3edcfa8d8a156336d9de779e8438c4913310f
chk "ycharts/research/render_pdf.cjs" 040cbc483ae35d67d0f760fe4d2d8011774134d7843afe66b625d57542e3c890
chk "ycharts/research/runner.py" 5360c965824ce9b7c601021fde102acb846415bc87fe0e5216706cc209b280a1
sudo -u ec2-user ROOT="$IR" HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import hashlib, io, json, os, sys
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
print("V1 opal_map binding: present", os.path.isfile(path), "sha256 equal", hashlib.sha256(open(path, "rb").read()).hexdigest() == om.get("sha256"))
import layout_overview as lo
row = lo._default_classifier().get_classification("SPY")
print("V1 classification client: get_classification(SPY) ->", sorted(row)[:5] if row else row)
import boto3
import pyarrow
import pyarrow.parquet as pq
s3 = boto3.client("s3", region_name="us-east-1")
days = sorted(c["Prefix"] for c in s3.list_objects_v2(Bucket="opal-data-etfs", Prefix="bbg/", Delimiter="/").get("CommonPrefixes", []))
key_field = lo.held_data.KEY_FIELD[lo.held_data.CHARACTERISTICS]
rows = pq.read_table(io.BytesIO(s3.get_object(Bucket="opal-data-etfs", Key=days[-1] + "characteristics.parquet")["Body"].read()), use_threads=False).to_pylist()
want = sorted(lo.held_data.index_by_ticker(rows, key_field))[:3]
got = lo._read_characteristics(set(want), ["NAME"], s3=s3)
print("V1 characteristics read: pyarrow", pyarrow.__version__, "asked", want, "returned", len(got), "of", len(want))
PY
echo "V1 proof process exit code: $?"
echo "V1 queue: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text 2>&1)"
echo "V1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
