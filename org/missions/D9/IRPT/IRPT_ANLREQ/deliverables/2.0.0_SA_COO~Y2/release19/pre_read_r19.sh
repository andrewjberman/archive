set -u
# Ledger irpt-resident-r19-20261013, leg P1 (READ ONLY): the host state before the r19 install (expect the st32 root running, the library unmoved). No write, no vendor call.
# Derived from pre_read.sh of the st32 release (org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st32_release/); the same reads, with the roots and pins of this release.
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
OLD=0485393f3a-st32
NEW=0485393f3a-r19
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "P1 at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "P1 active=$(systemctl is-active $UNIT) root=$RUN since=$(systemctl show $UNIT -p ActiveEnterTimestamp --value) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "P1 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "P1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1)"
echo "P1 reader members at the running root: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) READER_VERSION lines $(grep -c '^READER_VERSION' $RUN/intake/template_reader.py) (want 47f89e0b46609c5b... and 76795b75313b076e... and 0)"
echo "P1 rollback root $OLD present: $(test -d $R/$OLD && echo yes || echo no); running root is it: $([ "$RUN" = "$R/$OLD" ] && echo yes || echo no); new root $NEW present: $(test -d $R/$NEW && echo yes || echo no) (want no)"
echo "P1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))")"
echo "P1 library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1)"
echo "P1 queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "P1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
# STOP-READ: the unit must not carry IRPT_ANALYSIS_READY_QUEUE_URL (as in the st32 release).
MP=$(systemctl show $UNIT -p MainPID --value)
E1=$(systemctl show $UNIT -p Environment --value | grep -c IRPT_ANALYSIS_READY_QUEUE_URL)
E2=$(tr '\0' '\n' < /proc/$MP/environ | grep -c '^IRPT_ANALYSIS_READY_QUEUE_URL=')
echo "P1 STOP-READ IRPT_ANALYSIS_READY_QUEUE_URL: unit Environment=$E1 running process (pid $MP)=$E2 (both must be 0)"
[ "$E1" = 0 ] && [ "$E2" = 0 ] && echo "P1 STOP-READ PASS" || echo "P1 STOP-READ FAIL: do not install; report to 2.0.0_SA_COO~Y2"
# STOP 2: the running root is the st32 root, the library is st32's and the wrapper is st32's (this release moves neither).
[ "$RUN" = "$R/$OLD" ] && echo "P1 STOP-READ-2 PASS: the running root is $OLD" || echo "P1 STOP-READ-2 FAIL: the running root is not $OLD; do not install"
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841" ] && echo "P1 STOP-READ-3 PASS: host library is st32's" || echo "P1 STOP-READ-3 FAIL: host library is not st32's; do not install"
[ "$(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1)" = "55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9" ] && echo "P1 STOP-READ-4 PASS: host wrapper is st32's" || echo "P1 STOP-READ-4 FAIL: host wrapper is not st32's; do not install"
# STOP 5: the paths the installer writes must not already exist (the new root is made by rm -rf and mkdir; the kept library copy is not).
test -e $H/ycharts_session.js.before-$NEW && echo "P1 STOP-READ-5 FAIL: the kept-copy path already exists; do not install" || echo "P1 STOP-READ-5 PASS: kept-copy path $H/ycharts_session.js.before-$NEW is absent"
test -e $R/cutover_receipt.$OLD.json && echo "P1 info: $R/cutover_receipt.$OLD.json exists (the installer overwrites it with cp -p)" || echo "P1 info: $R/cutover_receipt.$OLD.json is absent"
echo "P1 sign-in baseline: journal lines since the unit started naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED')"
