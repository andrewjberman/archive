set -u
# Ledger irpt-resident-st30-20261011, legs D2 + V1: fetch the signed st30 install script BY KEY (the host role holds GetObject, not GetObjectVersion), verify its sha256 (it binds the bytes), run it
# (it stages the tar, checks every member, keeps st27 for rollback and rolls back itself on a failed start), then read the running
# package back. Sent through Systems Manager by host_read.py. No vendor call. Operator 0.7.0_AE_CloudOps~YC2 for 2.0.0_SA_COO~G2.
NEW=37210c771a-st30
KEY=ec2/investor-reporting-ycharts/resident/resident_host_install_$NEW.sh
VER=__ST30_SCRIPT_VERSION__  # the staged version (fetched by key; the sha256 binds the bytes)
WANT=dd85725806894839bd46fc66d990ba195f966862015a2983bb7bbbef0964b969
T=/tmp/resident_host_install_$NEW.sh
R=/opt/irpt-resident
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing moved"; exit 30; }
[ "$(sha256sum $T | cut -d' ' -f1)" = "$WANT" ] || { echo "ERROR: the fetched script is not the signed bytes; nothing moved"; rm -f $T; exit 31; }
echo "D2 install script sha256 verified on the host at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
bash $T
RC=$?
rm -f $T
echo "D2 install script rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "V1 running root $RUN active=$(systemctl is-active $UNIT) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "V1 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "V1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (built a9f71b6d236e7a9e...)"
echo "V1 pyarrow in root: $(test -d $RUN/pyarrow && echo present || echo absent); renderer drop-in: $(test -f /etc/systemd/system/$UNIT.d/opal-render.conf && echo present || echo absent)"
sudo -u ec2-user ROOT="$RUN" HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import os, sys
root = os.environ["ROOT"]
for rel in ("intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract", "ycharts/generate"):
    sys.path.insert(0, os.path.join(root, rel))
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
sys.path.insert(0, root)
import resident_installed  # noqa: F401
import resident_worker
p = resident_worker.load_opal_producer()
print("V1 producer import OK: family", p.OPAL_FAMILY, "allow list", resident_worker.OPAL_PRODUCER_PRINCIPALS)
sys.path.insert(0, os.path.join(root, "ycharts", "research"))
import layout_overview as lo
b = lo.load_brand()
print("V1 brand from the RUNNING root: spec", lo._asset_path("IRPT_BRAND_SPEC", lo.SPEC_REL), "logo", lo._asset_path("IRPT_OPAL_LOGO", lo.LOGO_REL),
      "logo bytes", len(b["logo_svg"]), "spec keys", sorted(b["spec"])[:4], "env brand vars", [k for k in os.environ if k.startswith("IRPT_BRAND") or k == "IRPT_OPAL_LOGO"])
print("V1 producer_for svc ->", resident_worker.producer_for({"owner": {"principal_id": "svc-irpt-analysis@opalinvest.com"}}),
      "| andrew ->", resident_worker.producer_for({"owner": {"principal_id": "andrew@opalinvest.com"}}),
      "| other ->", resident_worker.producer_for({"owner": {"principal_id": "someone-else@example.invalid"}}))
PY
echo "V1 proof process exit code: $?"
echo "V1 packaged research row firms: $(python3.12 -c "import json;d=json.load(open('$RUN/infra/logic/registry/reporting_policies.json'));print([p['firms'] for p in d['policies'] if p['policy_revision']=='irpt-ycdgen-research-v1'][0])")"
echo "V1 queue: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text 2>&1)"
echo "V1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
echo "V1 S2 packaged request schema names ticket_id: $(grep -c '"ticket_id"' $RUN/docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json)"
echo "V1 S3 read-back release seconds: $(grep -m1 '^READ_BACK_RELEASE_VISIBILITY_S' $RUN/ycharts/generate/resident_worker.py)"
echo "V1 I1/I2 bindings carry: commentary_ready_queue_url=$(grep -c commentary_ready_queue_url $RUN/reports/resident_bindings.json) analysis_ready_queue_url=$(grep -c analysis_ready_queue_url $RUN/reports/resident_bindings.json) (expect 0 and 0)"
MP=$(systemctl show $UNIT -p MainPID --value)
echo "V1 S5 running process environment names IRPT_ANALYSIS_READY_QUEUE_URL: $(tr '\0' '\n' < /proc/$MP/environ | grep -c '^IRPT_ANALYSIS_READY_QUEUE_URL=') (expect 0; pid $MP)"
echo "V1 S5 journal since start: I3 send failures=$(journalctl -u $UNIT --since '-120 s' --no-pager | grep -c ANALYSIS_READY_SEND_FAILED) unset warnings=$(journalctl -u $UNIT --since '-120 s' --no-pager | grep -c ANALYSIS_READY_QUEUE_UNSET)"
