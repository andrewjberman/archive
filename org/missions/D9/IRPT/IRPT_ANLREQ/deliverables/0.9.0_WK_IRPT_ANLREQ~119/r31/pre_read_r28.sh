set -u
# Ledger irpt-resident-r28-20261013, leg P1 (READ ONLY): the host state before the r28 install (expect the r19 root running, the library and wrapper unmoved, the r28 root absent). No write, no vendor call.
# Written under IRPT_ANLREQ.TO-AR-y-301 (worker 0.9.0_WK_IRPT_ANLREQ~119). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it under a later order.
# Derived from pre_read_r19.sh (release 19, the same five stop-reads). Changed: the roots, the reader and worker values, the receipt copy name, and STOP-READ-2's new-root condition.
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
OLD=0485393f3a-r19
NEW=0485393f3a-r28
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "P1 at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "P1 active=$(systemctl is-active $UNIT) root=$RUN since=$(systemctl show $UNIT -p ActiveEnterTimestamp --value) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "P1 allow list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "P1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (want a643b0074258f3732abbb28e2712e60ee5433f6fc633d2c7ecc887ac5829113d, the release-19 worker; release 28 moves it to 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5)"
echo "P1 reader members at the running root: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) READER_VERSION line $(grep -m1 '^READER_VERSION' $RUN/intake/template_reader.py) (want 176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea and 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58 and READER_VERSION = \"irpt-template-reader.r18.1\")"
echo "P1 rollback root $OLD present: $(test -d $R/$OLD && echo yes || echo no); running root is it: $([ "$RUN" = "$R/$OLD" ] && echo yes || echo no); new root $NEW present: $(test -d $R/$NEW && echo yes || echo no) (want no)"
echo "P1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/$OLD and irpt-resident-r19-20261013)"
echo "P1 library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1) (want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841 and 55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9)"
echo "P1 queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text) (want 0 0)"
echo "P1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
# STOP-READ: the unit must not carry IRPT_ANALYSIS_READY_QUEUE_URL (as in the release-19 pre-read).
MP=$(systemctl show $UNIT -p MainPID --value)
E1=$(systemctl show $UNIT -p Environment --value | grep -c IRPT_ANALYSIS_READY_QUEUE_URL)
E2=$(tr '\0' '\n' < /proc/$MP/environ | grep -c '^IRPT_ANALYSIS_READY_QUEUE_URL=')
echo "P1 STOP-READ IRPT_ANALYSIS_READY_QUEUE_URL: unit Environment=$E1 running process (pid $MP)=$E2 (both must be 0)"
[ "$E1" = 0 ] && [ "$E2" = 0 ] && echo "P1 STOP-READ PASS" || echo "P1 STOP-READ FAIL: do not install; report to 2.0.0_SA_COO~Y2"
# STOP 2: the running root is the release-19 root and the release-28 root is absent (the installer makes the new root by rm -rf and mkdir, so a present one would be replaced silently); the library and the wrapper are the release-19 bytes (release 28 reinstalls the same library bytes and moves no wrapper).
[ "$RUN" = "$R/$OLD" ] && [ ! -e "$R/$NEW" ] && echo "P1 STOP-READ-2 PASS: the running root is $OLD and $NEW is absent" || echo "P1 STOP-READ-2 FAIL: the running root is not $OLD, or $NEW already exists; do not install"
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841" ] && echo "P1 STOP-READ-3 PASS: host library is the release-19 library" || echo "P1 STOP-READ-3 FAIL: host library is not the release-19 library; do not install"
[ "$(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1)" = "55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9" ] && echo "P1 STOP-READ-4 PASS: host wrapper is the release-19 wrapper" || echo "P1 STOP-READ-4 FAIL: host wrapper is not the release-19 wrapper; do not install"
# STOP 5: the paths the installer writes must not already exist (the new root is made by rm -rf and mkdir; the kept library copy is not).
test -e $H/ycharts_session.js.before-$NEW && echo "P1 STOP-READ-5 FAIL: the kept-copy path already exists; do not install" || echo "P1 STOP-READ-5 PASS: kept-copy path $H/ycharts_session.js.before-$NEW is absent"
test -e $R/cutover_receipt.$OLD.json && echo "P1 info: $R/cutover_receipt.$OLD.json exists" || echo "P1 info: $R/cutover_receipt.$OLD.json is absent (expected before the r28 installer runs: its line 70 creates it with cp -p from the release-19 receipt)"
echo "P1 sign-in baseline: journal lines since the unit started naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED')"
