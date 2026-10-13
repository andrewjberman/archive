set -u
# Ledger irpt-resident-r19-20261013, legs D2 + V1: fetch the signed r19 install script BY KEY (the host role holds GetObject, not GetObjectVersion), verify its sha256
# (it binds the bytes), run it (it stages the tar, checks every member, reinstalls the library with the same bytes, keeps the st32 root and library for rollback and rolls both
# back itself on a failed start), then read the running package back. Sent through Systems Manager by host_read.py. No vendor call.
# Derived from install_st32.sh of the st32 release; the read-backs that proved st32-only members are replaced by the reader reads and a whole-package comparison.
NEW=0485393f3a-r19
OLD=0485393f3a-st32
P=ec2/investor-reporting-ycharts/resident
KEY=$P/resident_host_install_$NEW.sh
WANT=8b53be1328f9ed20827e0118aee9c1b1b402d66b25d82a434275b1c83cfa57f0
SUMKEY=$P/irpt-resident-$NEW.package.SHA256SUMS
WANTSUM=a3dea4ec9afe05db66db96e8110064e70a6ba7ea50e4d04038cdee301ddfa933
T=/tmp/resident_host_install_$NEW.sh
S=/tmp/irpt-resident-$NEW.package.SHA256SUMS
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing moved"; exit 30; }
[ "$(sha256sum $T | cut -d' ' -f1)" = "$WANT" ] || { echo "ERROR: the fetched script is not the signed bytes; nothing moved"; rm -f $T; exit 31; }
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$SUMKEY" $S --only-show-errors --region us-east-1 || { echo "ERROR: fetch of the package sums failed; nothing moved"; rm -f $T; exit 32; }
[ "$(sha256sum $S | cut -d' ' -f1)" = "$WANTSUM" ] || { echo "ERROR: the fetched package sums are not the signed bytes; nothing moved"; rm -f $T $S; exit 33; }
echo "D2 install script and package sums sha256 verified on the host at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
bash $T
RC=$?
rm -f $T
echo "D2 install script rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "V1 running root $RUN active=$(systemctl is-active $UNIT) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "V1 P2 reader members: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) (want 176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) (want 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58)"
echo "V1 P2 READER_VERSION: $(grep -m1 '^READER_VERSION' $RUN/intake/template_reader.py) (want irpt-template-reader.r18.1)"
echo "V1 P3 held members: the package's own sums (297 members) checked against the running root:"
( cd "$RUN" && sha256sum -c --quiet $S > /tmp/r19_sumcheck.txt 2>&1; echo "V1 P3 sha256sum -c rc=$? lines not OK: $(grep -c -v ': OK$' /tmp/r19_sumcheck.txt) of $(wc -l < $S) checked" )
echo "V1 P3 members that differ from the package: $(grep -v ': OK$' /tmp/r19_sumcheck.txt | head -5 | tr '\n' ' ')"
rm -f $S /tmp/r19_sumcheck.txt
echo "V1 P3 host member count $(wc -l < $RUN/SHA256SUMS) (the package's 297 plus the host's pydeps; the st32 root had 4346)"
sudo -u ec2-user ROOT="$RUN" HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import os, sys
root = os.environ["ROOT"]
for rel in ("intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract", "ycharts/generate"):
    sys.path.insert(0, os.path.join(root, rel))
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
sys.path.insert(0, root)
import resident_installed  # noqa: F401
import resident_worker
import template_reader
import uploads  # noqa: F401
p = resident_worker.load_opal_producer()
print("V1 producer import OK: family", p.OPAL_FAMILY, "allow list", resident_worker.OPAL_PRODUCER_PRINCIPALS)
print("V1 reader import OK: READER_VERSION", getattr(template_reader, "READER_VERSION", None))
PY
echo "V1 proof process exit code: $?"
echo "V1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (st32 a643b0074258f373...)"
echo "V1 queue: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "V1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
echo "V1 capture pins: host library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) | bindings library $(python3.12 -c "import json;print(json.load(open('$RUN/reports/resident_bindings.json'))['capture']['library_sha256'])") | want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841"
echo "V1 capture pins: host wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1) | bindings wrapper $(python3.12 -c "import json;print(json.load(open('$RUN/reports/resident_bindings.json'))['capture']['wrapper_sha256'])") | want 55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9"
echo "V1 old library kept for rollback: $(test -f $H/ycharts_session.js.before-$NEW && sha256sum $H/ycharts_session.js.before-$NEW | cut -d' ' -f1 || echo ABSENT) (want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841)"
echo "V1 rollback root $OLD still present: $(test -d $R/$OLD && echo yes || echo no)"
echo "V1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))")"
echo "V1 NO SIGN-IN since the start: journal lines naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since '-120 s' --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED') (expect 0)"
