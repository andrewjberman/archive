set -u
# Ledger irpt-resident-r30-20261014, leg P1 (READ ONLY): the host state before the r30 install (expect the r29 root running, the library and wrapper unmoved, the r30 root absent). No write, no vendor call.
# Written under IRPT_ANLREQ.TO-AR-y-324 (worker 0.9.0_WK_IRPT_ANLREQ~132). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it under a later order.
# Derived from pre_read_r29.sh (release 29, the same five stop-reads) by the AR-y-301 method. Changed: the roots (OLD = r29, NEW = r30), the reader values (the r29 values, with ops/status.py read back, and _scope/interactive_access.py and ycharts/generate/composition_admission.py read back), the worker value (r29), the receipt ledger (r29), and the release-30 wording of the stop-reads.
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
OLD=0485393f3a-r29
NEW=0485393f3a-r30
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "P1 at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "P1 active=$(systemctl is-active $UNIT) root=$RUN since=$(systemctl show $UNIT -p ActiveEnterTimestamp --value) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "P1 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "P1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (want 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5, the release-29 worker; release 30 moves no worker)"
echo "P1 reader members at the running root: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) ops/status.py $(sha256sum $RUN/ops/status.py | cut -d' ' -f1) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) interactive_access.py $(sha256sum $RUN/_scope/interactive_access.py | cut -d' ' -f1) composition_admission.py $(sha256sum $RUN/ycharts/generate/composition_admission.py | cut -d' ' -f1) READER_VERSION line $(grep -m1 '^READER_VERSION' $RUN/intake/template_reader.py) (want f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494 and 87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030 and a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35 and c28d9a74c9af2c5d5014ae54ffda388c2666d24e9c98ac42df3ace457e59e684 and 50f5d11cd8ffb8161b9f42af61bdfcdffe698cfc4e66b5cc3338048572563606 and READER_VERSION = \"irpt-template-reader.r19.3\")"
echo "P1 rollback root $OLD present: $(test -d $R/$OLD && echo yes || echo no); running root is it: $([ "$RUN" = "$R/$OLD" ] && echo yes || echo no); new root $NEW present: $(test -d $R/$NEW && echo yes || echo no) (want no)"
echo "P1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/$OLD and irpt-resident-r29-20261014)"
echo "P1 library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1) (want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841 and 55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9)"
echo "P1 queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text) (want 0 0)"
echo "P1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
# STOP-READ: the unit must not carry IRPT_ANALYSIS_READY_QUEUE_URL (as in the release-29 pre-read).
MP=$(systemctl show $UNIT -p MainPID --value)
E1=$(systemctl show $UNIT -p Environment --value | grep -c IRPT_ANALYSIS_READY_QUEUE_URL)
E2=$(tr '\0' '\n' < /proc/$MP/environ | grep -c '^IRPT_ANALYSIS_READY_QUEUE_URL=')
echo "P1 STOP-READ IRPT_ANALYSIS_READY_QUEUE_URL: unit Environment=$E1 running process (pid $MP)=$E2 (both must be 0)"
[ "$E1" = 0 ] && [ "$E2" = 0 ] && echo "P1 STOP-READ PASS" || echo "P1 STOP-READ FAIL: do not install; report to 2.0.0_SA_COO~Y2"
# STOP 2: the running root is the release-29 root and the release-30 root is absent (the installer makes the new root by rm -rf and mkdir, so a present one would be replaced silently); the library and the wrapper are the release-29 bytes (release 30 reinstalls the same library bytes and moves no wrapper).
[ "$RUN" = "$R/$OLD" ] && [ ! -e "$R/$NEW" ] && echo "P1 STOP-READ-2 PASS: the running root is $OLD and $NEW is absent" || echo "P1 STOP-READ-2 FAIL: the running root is not $OLD, or $NEW already exists; do not install"
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841" ] && echo "P1 STOP-READ-3 PASS: host library is the release-29 library" || echo "P1 STOP-READ-3 FAIL: host library is not the release-29 library; do not install"
[ "$(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1)" = "55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9" ] && echo "P1 STOP-READ-4 PASS: host wrapper is the release-29 wrapper" || echo "P1 STOP-READ-4 FAIL: host wrapper is not the release-29 wrapper; do not install"
# STOP 5: the paths the installer writes must not already exist (the new root is made by rm -rf and mkdir; the kept library copy is not).
test -e $H/ycharts_session.js.before-$NEW && echo "P1 STOP-READ-5 FAIL: the kept-copy path already exists; do not install" || echo "P1 STOP-READ-5 PASS: kept-copy path $H/ycharts_session.js.before-$NEW is absent"
test -e $R/cutover_receipt.$OLD.json && echo "P1 info: $R/cutover_receipt.$OLD.json exists" || echo "P1 info: $R/cutover_receipt.$OLD.json is absent (expected before the r30 installer runs: its line 70 creates it with cp -p from the release-29 receipt)"
echo "P1 sign-in baseline: journal lines since the unit started naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED')"
