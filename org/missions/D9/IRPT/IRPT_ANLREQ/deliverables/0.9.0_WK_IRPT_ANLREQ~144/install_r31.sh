set -u
# Ledger irpt-resident-r31-20261014, legs D2 + V1: fetch the signed r31 install script BY KEY (the host role holds GetObject, not GetObjectVersion), verify its sha256
# (it binds the bytes), run it (it stages the tar, checks every changed member, reinstalls the library with the same bytes, keeps the r29 root and library for rollback and rolls both
# back itself on a failed start), then read the running package back. Sent through Systems Manager by host_read.py. No vendor call.
# Written under IRPT_ANLREQ.TO-AR-y-338 (worker 0.9.0_WK_IRPT_ANLREQ~144). NOT RUN: the applier 0.7.0_AE_CloudOps~YC2 runs it under a later order.
# Derived from install_r30.sh (release 30) by the AR-y-301 method. Changed: NEW, WANT, WANTSUM; a guard before the fetch that refuses unless the running root is
# 0485393f3a-r29 (exit 34) and the unit carries no IRPT_ANALYSIS_READY_QUEUE_URL (exit 35); the release-31 member table (thirteen members, each at its release-31 sha256);
# the expected producer list printed and read back; the imports of layout_overview and opal_producer. Every fetch, sha256 and refusal guard of install_r30.sh is kept with its exit code.
NEW=0485393f3a-r31
OLD=0485393f3a-r29
P=ec2/investor-reporting-ycharts/resident
KEY=$P/resident_host_install_$NEW.sh
WANT=6f5590899dc64b2371e7dd04a21de386e15e33ce955420ec4b0083c673611987
SUMKEY=$P/irpt-resident-$NEW.package.SHA256SUMS
WANTSUM=4710d4eab4e4f1e87fdcc4ab422f5b29a70af4fe74423a534dd411603a2db449
T=/tmp/resident_host_install_$NEW.sh
S=/tmp/irpt-resident-$NEW.package.SHA256SUMS
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
[ "$RUN" = "$R/$OLD" ] || { echo "ERROR: the running root is ${RUN:-none}, not $R/$OLD; nothing moved"; exit 34; }
UNITENV=$(systemctl show $UNIT -p Environment --value | grep -c IRPT_ANALYSIS_READY_QUEUE_URL)
[ "$UNITENV" = 0 ] || { echo "ERROR: the unit carries IRPT_ANALYSIS_READY_QUEUE_URL; nothing moved"; exit 35; }
echo "R31 guard: running root $RUN (want $R/$OLD); unit IRPT_ANALYSIS_READY_QUEUE_URL count $UNITENV (want 0)"
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$KEY" $T
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
echo "V1 P2b release-31 members (each wanted value is the release-31 build record sha256 of the member):"
for ent in \
  "_scope/interactive_access.py d416e3755d587b14a0b8ccbd2599b9183bada64c6aed5a9b56edc5a7ce19838b" \
  "intake/uploads.py 48f39329ea4c947dc30cba02e07ed499d6f683726204710b16656c29d6f3c0c1" \
  "ops/entry.py 8d9b7e76242af5b731875c2fc169e1f57963ecc0f48e97a965549f1e1cabdd1e" \
  "ops/owned_report.py fd57437f792d4904232f2a6d2d9c0853e34bce7bc2fc3cd3ff3e76a68712a5d2" \
  "ops/pdf_link.py 9ac02114da9383022e4c30bb6a276b7c98b3b92d0999975d679b6fb8dee6ebb0" \
  "reports/build_resident_package.py 9cfa787a457cbb3c07945d6023dc431cb5abc0e01f1fed47786292c66be93bc1" \
  "reports/status_installed.py 8ae1892eef9fe43c3e03b53f1310b9663d5a0cb95c8ef108d912ba3a42028de5" \
  "ycharts/generate/acceptance.py 0c4acec625b7da70da82efccf58cc967e9e5bf53c32e955d67079b711701513d" \
  "ycharts/generate/composition_admission.py 8d9b7aadc7c4db0b078737b155b4ec999d245d20c8bee83515c628639d0f64fd" \
  "ycharts/generate/resident_worker.py d779f7dc2e2218822f6b1b2cbca8cc15580202d67e51374f8cd170cb05a31eab" \
  "ycharts/research/layout_overview.py c368aa71db3cec88054c0c508fb005d3d97046469ed417e69b509fce824e9f48" \
  "ycharts/research/opal_packager.py 3117cceb4ff5107f380ab66e8fd0b2fa16cd194e60853c52137e99bf203f1a12" \
  "ycharts/research/opal_producer.py 48fa9af965e3bc92ec6e159f4ba1aa147f6e5a1593cdeec07d8d23a8b83714d6"; do
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
# release 31 (AR-y-324): the members this release adds or replaces, imported the way the producer and the reader are
sys.path.append(os.path.join(root, "ycharts", "research"))
sys.path.append(os.path.join(root, "lib"))
import opal_packager  # noqa: F401
import layout_overview  # noqa: F401
import opal_producer  # noqa: F401
import trading_calendar
print("V1 P4 import OK: opal_packager from", os.path.relpath(opal_packager.__file__, root))
print("V1 P4 import OK: resident_worker registry identity port callable", callable(getattr(resident_worker, "registry_identity_port", None)), "from", os.path.relpath(resident_worker.__file__, root))
print("V1 P4 import OK: trading_calendar from", os.path.relpath(trading_calendar.__file__, root))
PY
echo "V1 proof process exit code: $?"
echo "V1 P4 yfinance_check.py absent from the root: $([ -z "$(find "$RUN" -name yfinance_check.py -print -quit)" ] && echo yes || echo no) (want yes; the build record: not in this release by design)"
echo "V1 worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (want d779f7dc2e2218822f6b1b2cbca8cc15580202d67e51374f8cd170cb05a31eab; release-29 190f0e14bceb97ca870b6eefeffbc6d96e6e63fb1eb3fcc905541d789b8e40d5)"
echo "V1 expected producer list (release 31, two entries): andrew@opalinvest.com fwd1-staff-r41a@opal.invalid; running: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
echo "V1 queue: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "V1 journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
echo "V1 capture pins: host library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) | bindings library $(python3.12 -c "import json;print(json.load(open('$RUN/reports/resident_bindings.json'))['capture']['library_sha256'])") | want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841"
echo "V1 capture pins: host wrapper $(sha256sum $H/run-ycharts-session.sh | cut -d' ' -f1) | bindings wrapper $(python3.12 -c "import json;print(json.load(open('$RUN/reports/resident_bindings.json'))['capture']['wrapper_sha256'])") | want 55ddb8f7947cba7cdca1b9139d4d0a1a3ad620e330c86ba3ab648d334763aff9"
echo "V1 old library kept for rollback: $(test -f $H/ycharts_session.js.before-$NEW && sha256sum $H/ycharts_session.js.before-$NEW | cut -d' ' -f1 || echo ABSENT) (want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841)"
echo "V1 rollback root $OLD still present: $(test -d $R/$OLD && echo yes || echo no) (want yes)"
echo "V1 receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/$NEW and irpt-resident-r31-20261014; the manifest prefix is the host's own SHA256SUMS, no build-record value)"
echo "V1 NO SIGN-IN since the start: journal lines naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since '-120 s' --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED') (expect 0)"
