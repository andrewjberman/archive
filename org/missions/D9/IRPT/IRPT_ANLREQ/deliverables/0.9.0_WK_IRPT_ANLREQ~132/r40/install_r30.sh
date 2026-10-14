set -u
# Ledger irpt-resident-r30-20261014, legs D2 + V1: fetch the signed r30 install script BY KEY (the host role holds GetObject, not GetObjectVersion), verify its sha256
# (it binds the bytes), run it (it stages the tar, checks every member, reinstalls the library with the same bytes, keeps the r29 root and library for rollback and rolls both
# back itself on a failed start), then read the running package back. Sent through Systems Manager by host_read.py. No vendor call.
# Written under IRPT_ANLREQ.TO-AR-y-324 (worker 0.9.0_WK_IRPT_ANLREQ~132). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it under a later order.
# Derived from install_r29.sh (release 29) by the AR-y-301 method. Changed: NEW, OLD, WANT, WANTSUM; the reader read-backs take the release-30 values of the build record (uploads.py replaced; _scope/interactive_access.py and ycharts/generate/composition_admission.py read back); the ten-member
# table (uploads.py replaced; _scope/interactive_access.py and ycharts/generate/composition_admission.py added; seven unchanged and read back at their release-30 values); the package sums (298 entries); READER_VERSION r19.3 unchanged; the import read-backs unchanged; the sums temp file.
# Every fetch, sha256 and refusal guard of install_r29.sh is kept with its exit code.
NEW=0485393f3a-r30
OLD=0485393f3a-r29
P=ec2/investor-reporting-ycharts/resident
KEY=$P/resident_host_install_$NEW.sh
WANT=2e72c822c05f1522dc44f4764e2a24dc1f02f4b6c684ed7a0b460bfd0d0efdb9
SUMKEY=$P/irpt-resident-$NEW.package.SHA256SUMS
WANTSUM=1ae1df0d147f529fdfc0d05f09dff83f23f156ec17d982b3419492f8531f4812
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
echo "V1 running root $RUN active=$(systemctl is-active $UNIT) restarts=$(systemctl show $UNIT -p NRestarts --value) (want $R/$NEW active)"
echo "V1 P2 reader members: uploads.py $(sha256sum $RUN/intake/uploads.py | cut -d' ' -f1) (want 48f39329ea4c947dc30cba02e07ed499d6f683726204710b16656c29d6f3c0c1) template_reader.py $(sha256sum $RUN/intake/template_reader.py | cut -d' ' -f1) (want a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35)"
echo "V1 P2 READER_VERSION: $(grep -m1 '^READER_VERSION' $RUN/intake/template_reader.py) (want READER_VERSION = \"irpt-template-reader.r19.3\")"
echo "V1 P2b release-30 members against the r30 build record (RESIDENT_BUILD.json release_input new_sha256; the wanted values are the record's, not computed here):"
for ent in \
  "ycharts/generate/resident_worker.py 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5" \
  "ycharts/research/opal_packager.py e874f26ee8c90d37f8334d7050683b9c541b412ff8cade769e4f4989d4b46ab2" \
  "intake/portfolio.py d1232a1255b2ea03ff5c7fb04b7282701c6037a1ed5305a12cad7d95f0aa22e8" \
  "intake/security_resolution.py 1248f6c0b51d5289fe11f9ee0ca427613b7bdeaf4b10f614bccc05563f2694d3" \
  "intake/template_reader.py a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35" \
  "intake/uploads.py 48f39329ea4c947dc30cba02e07ed499d6f683726204710b16656c29d6f3c0c1" \
  "_scope/interactive_access.py d416e3755d587b14a0b8ccbd2599b9183bada64c6aed5a9b56edc5a7ce19838b" \
  "ycharts/generate/composition_admission.py 8d9b7aadc7c4db0b078737b155b4ec999d245d20c8bee83515c628639d0f64fd" \
  "ops/status.py 87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030" \
  "lib/trading_calendar.py 9bc467c6ce4d11e435803681f3ba62835d531cea7c06c39770f1d085c7e4446f"; do
  set -- $ent
  GOT=$(sha256sum $RUN/$1 | cut -d' ' -f1)
  echo "V1 P2b member $1 sha256 $GOT (want $2) $([ "$GOT" = "$2" ] && echo MATCH || echo MISMATCH)"
done
echo "V1 P3 held members: the package's own sums (298 entries) checked against the running root:"
( cd "$RUN" && sha256sum -c --quiet $S > /tmp/r29_sumcheck.txt 2>&1; echo "V1 P3 sha256sum -c rc=$? lines not OK: $(grep -c -v ': OK$' /tmp/r29_sumcheck.txt) of $(wc -l < $S) checked (want 0 of 298, the build record's sha256sums_check)" )
echo "V1 P3 members that differ from the package: $(grep -v ': OK$' /tmp/r29_sumcheck.txt | head -5 | tr '\n' ' ')"
rm -f $S /tmp/r29_sumcheck.txt
echo "V1 P3 host member count $(wc -l < $RUN/SHA256SUMS) (the package's 298 plus the host's pydeps; the release-19 root had 4346; the build record carries no host count, printed for the record only)"
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
# release 30 (AR-y-324): the members this release adds or replaces, imported the way the producer and the reader are
sys.path.append(os.path.join(root, "ycharts", "research"))
sys.path.append(os.path.join(root, "lib"))
import opal_packager  # noqa: F401
import trading_calendar
print("V1 P4 import OK: opal_packager from", os.path.relpath(opal_packager.__file__, root))
print("V1 P4 import OK: resident_worker registry identity port callable", callable(getattr(resident_worker, "registry_identity_port", None)), "from", os.path.relpath(resident_worker.__file__, root))
print("V1 P4 import OK: trading_calendar from", os.path.relpath(trading_calendar.__file__, root))
PY
echo "V1 proof process exit code: $?"
echo "V1 P4 yfinance_check.py absent from the root: $([ -z "$(find "$RUN" -name yfinance_check.py -print -quit)" ] && echo yes || echo no) (want yes; the build record: not in this release by design)"
echo "V1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (want 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5; release-19 a643b007...)"
echo "V1 queue: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "V1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
echo "V1 capture pins: host library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) | bindings library $(python3.12 -c "import json;print(json.load(open('$RUN/reports/resident_bindings.json'))['capture']['library_sha256'])") | want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841"
echo "V1 capture pins: host wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1) | bindings wrapper $(python3.12 -c "import json;print(json.load(open('$RUN/reports/resident_bindings.json'))['capture']['wrapper_sha256'])") | want 55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9"
echo "V1 old library kept for rollback: $(test -f $H/ycharts_session.js.before-$NEW && sha256sum $H/ycharts_session.js.before-$NEW | cut -d' ' -f1 || echo ABSENT) (want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841)"
echo "V1 rollback root $OLD still present: $(test -d $R/$OLD && echo yes || echo no) (want yes)"
echo "V1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/$NEW and irpt-resident-r30-20261014; the manifest prefix is the host's own SHA256SUMS, no build-record value)"
echo "V1 NO SIGN-IN since the start: journal lines naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since '-120 s' --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED') (expect 0)"
