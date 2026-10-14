set -u
# Ledger irpt-resident-r29-20261014, leg P1 (READ ONLY): the host state before the r29 install (expect the r28 root running, the library and wrapper unmoved, the r29 root absent). No write, no vendor call.
# Written under IRPT_ANLREQ.TO-AR-y-311 (worker 0.9.0_WK_IRPT_ANLREQ~125). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it under a later order.
# Derived from pre_read_r28.sh (release 28, the same five stop-reads) by the AR-y-301 method. Changed: the roots (OLD = r28, NEW = r29), the reader values (the r28 values, with ops/status.py read back), the worker value (r28), the receipt ledger (r28), and the release-29 wording of the stop-reads.
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
OLD=0485393f3a-r28
NEW=0485393f3a-r29
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "P1 at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "P1 active=$(systemctl is-active $UNIT) root=$RUN since=$(systemctl show $UNIT -p ActiveEnterTimestamp --value) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "P1 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "P1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (want 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5, the release-28 worker; release 29 moves no worker)"
echo "P1 reader members at the running root: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) ops/status.py $(sha256sum $RUN/ops/status.py | cut -d' ' -f1) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) READER_VERSION line $(grep -m1 '^READER_VERSION' $RUN/intake/template_reader.py) (want 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951 and 03fa9c78c9dd3ef2cd1321ad295ad4ea3df0ee996c473ee963652788332737d3 and a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35 and READER_VERSION = \"irpt-template-reader.r19.3\")"
echo "P1 rollback root $OLD present: $(test -d $R/$OLD && echo yes || echo no); running root is it: $([ "$RUN" = "$R/$OLD" ] && echo yes || echo no); new root $NEW present: $(test -d $R/$NEW && echo yes || echo no) (want no)"
echo "P1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/$OLD and irpt-resident-r28-20261013)"
echo "P1 library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1) (want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841 and 55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9)"
echo "P1 queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text) (want 0 0)"
echo "P1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
# STOP-READ: the unit must not carry IRPT_ANALYSIS_READY_QUEUE_URL (as in the release-28 pre-read).
MP=$(systemctl show $UNIT -p MainPID --value)
E1=$(systemctl show $UNIT -p Environment --value | grep -c IRPT_ANALYSIS_READY_QUEUE_URL)
E2=$(tr '\0' '\n' < /proc/$MP/environ | grep -c '^IRPT_ANALYSIS_READY_QUEUE_URL=')
echo "P1 STOP-READ IRPT_ANALYSIS_READY_QUEUE_URL: unit Environment=$E1 running process (pid $MP)=$E2 (both must be 0)"
[ "$E1" = 0 ] && [ "$E2" = 0 ] && echo "P1 STOP-READ PASS" || echo "P1 STOP-READ FAIL: do not install; report to 2.0.0_SA_COO~Y2"
# STOP 2: the running root is the release-28 root and the release-29 root is absent (the installer makes the new root by rm -rf and mkdir, so a present one would be replaced silently); the library and the wrapper are the release-28 bytes (release 29 reinstalls the same library bytes and moves no wrapper).
[ "$RUN" = "$R/$OLD" ] && [ ! -e "$R/$NEW" ] && echo "P1 STOP-READ-2 PASS: the running root is $OLD and $NEW is absent" || echo "P1 STOP-READ-2 FAIL: the running root is not $OLD, or $NEW already exists; do not install"
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841" ] && echo "P1 STOP-READ-3 PASS: host library is the release-28 library" || echo "P1 STOP-READ-3 FAIL: host library is not the release-28 library; do not install"
[ "$(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1)" = "55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9" ] && echo "P1 STOP-READ-4 PASS: host wrapper is the release-28 wrapper" || echo "P1 STOP-READ-4 FAIL: host wrapper is not the release-28 wrapper; do not install"
# STOP 5: the paths the installer writes must not already exist (the new root is made by rm -rf and mkdir; the kept library copy is not).
test -e $H/ycharts_session.js.before-$NEW && echo "P1 STOP-READ-5 FAIL: the kept-copy path already exists; do not install" || echo "P1 STOP-READ-5 PASS: kept-copy path $H/ycharts_session.js.before-$NEW is absent"
test -e $R/cutover_receipt.$OLD.json && echo "P1 info: $R/cutover_receipt.$OLD.json exists" || echo "P1 info: $R/cutover_receipt.$OLD.json is absent (expected before the r29 installer runs: its line 70 creates it with cp -p from the release-28 receipt)"
echo "P1 sign-in baseline: journal lines since the unit started naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED')"
