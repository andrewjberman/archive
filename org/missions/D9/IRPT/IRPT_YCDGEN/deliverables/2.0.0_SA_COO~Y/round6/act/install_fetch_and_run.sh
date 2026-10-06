set -u
# Ledger irpt-ycdgen-r6-branch-a-20261006, leg D2: fetch the signed install script on the host BY KEY, check its sha256, run it, then read the running package back.
# CTO half 20261006 (msg 105445) and COO half 20261006 both SIGNED for branch A; R1 (step 1) closed PASS; the pre-install step-2 answers are on the ledger.
# Sent through Systems Manager by host_read.py. No vendor call. Branch A: the allow list stays on its placeholder.
NEW=3d705e700f-st22
KEY=ec2/investor-reporting-ycharts/resident/resident_host_install_$NEW.sh
WANT=94454580c49ba0079bd936364a1362331d45df046ca6f9607e61baa45ab75eef
T=/tmp/resident_host_install_$NEW.sh
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing moved"; exit 30; }
[ "$(sha256sum $T | cut -d' ' -f1)" = "$WANT" ] || { echo "ERROR: the fetched script is not the signed bytes; nothing moved"; rm -f $T; exit 31; }
echo "install script sha256 verified on the host at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
bash $T
RC=$?
rm -f $T
echo "install script rc=$RC at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "V1 running root $RUN"
echo "V1 unit $(systemctl is-active $UNIT) since $(systemctl show $UNIT -p ActiveEnterTimestamp --value) restarts=$(systemctl show $UNIT -p NRestarts --value); library $(sha256sum $H/ycharts_session.js | cut -c1-16)"
IR=$RUN
chk() { f="$1"; want="$2"; case "$f" in infra/logic/registry/*) p="$IR/$f";; *) p="$IR/$f";; esac; got=$(sha256sum "$p" 2>/dev/null | cut -d' ' -f1); [ "$got" = "$want" ] && echo "V1 member OK $f" || echo "V1 member DIFF $f got=$got"; }
if [ "$RUN" = "$R/$NEW" ]; then
  chk "ops/owned_report.py" ff2bced5cdf8bb89cdfb43044ef06d7b33fbd89e221655dd47f0642d51b86f28
  chk "reports/composition.py" 52bffacbdffda9d9621049fe080f585e514aed6cc92d3948c128f15199ded2fc
  chk "reports/repository.py" 3ce2552a59b21ab1d9cf01b2e44c5649fc9c22aa171584efe4126aaede54832c
  chk "reports/resident_installed.py" 56cee28bd3d32f42fe9d3de847a16170260e10b77f68adb782e51674a99eec11
  chk "reports/retention.py" f7540e3552416cbe42082ae6a95fa15f8fc2150b40c3aa7d919db082bcdffa71
  chk "ycharts/generate/publication_worker.py" f2b3ecc0cdbc6c0e9b3846054c71a01c6a79c42dcb52338edc21b147a5f62a7b
  chk "ycharts/generate/publisher.py" 2e83c9f1e38d597d8e10d547e15dc260333606be068b90988899e5eb1a85e620
  chk "ycharts/generate/resident_worker.py" 3e9f691ad840fc33c5d830fc1ade46938f60d40ee1b0e9122ab88ab000b1fd32
  chk "_contracts/AnalysisReport.v2.schema.json" 748cdd900b45074ee2a1dd84f8ff599a192acbac414c009c621aeb383bc64503
  chk "infra/logic/registry/reporting_policies.json" 2bd3520dd3869fe244a285f824cdaf3d32ccc4aada5c3bca743943a349775013
fi
echo "V1 queue: $(aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text 2>&1)"
echo "V1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
