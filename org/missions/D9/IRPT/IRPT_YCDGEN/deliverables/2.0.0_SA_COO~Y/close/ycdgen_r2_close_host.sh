# IRPT_YCDGEN round-2 close: TWO live runs of the probe map (coverage_probe_map.json, 2 calls) on the resident host,
# inside the served lease, 8 s apart per call. Run A bootstraps the previous-run index (--bootstrap-index, once for
# Cottonwood); run B must then read changed_since_previous true/false per call against run A (FWD-2, E4). Both answers
# are E3's live probe of the OTHER_ENDPOINT routes. THIS IS A LIVE YCHARTS READ (Andrew-direct ~17:3xZ 2026-10-03,
# record @ce20ca6854). Shape: ycdgen_close_host_r3.sh. The bundle is fetched BY KEY and checked by sha256 before anything
# runs. No sign-in, no session write, no generate call, no retry. Bounded at 240 s per run. ASCII only.
set -u
umask 077
BUNDLE_KEY=ec2/investor-reporting-ycharts/resident/ycdgen/ycdgen-r2-bundle-09ee7fa0bfce.tar.gz
WANT=09ee7fa0bfce459b67fa7c3f5985c60e3da1b8c229c4ca9240152e7f90aee141
REQ_A=YCD-R2-20261004T2315Z-A
REQ_B=YCD-R2-20261004T2315Z-B
PORTFOLIO=P:2377833
UNIT=irpt-analysis-resident.service
PID=$(systemctl show $UNIT -p MainPID --value)
ROOT=$(readlink /proc/$PID/cwd)
echo "r2 close start $(date -u +%Y-%m-%dT%H:%M:%SZ) resident pid $PID root $ROOT"
T=$(mktemp -d /tmp/irpt-ycdgen-XXXXXX)
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$BUNDLE_KEY" "$T/bundle.tar.gz" --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing ran"; rm -rf "$T"; exit 30; }
GOT=$(sha256sum "$T/bundle.tar.gz" | cut -d' ' -f1)
[ "$GOT" = "$WANT" ] || { echo "ERROR: bundle sha256 $GOT is not the signed bytes; nothing ran"; rm -rf "$T"; exit 31; }
mkdir -p "$T/research"
tar -xzf "$T/bundle.tar.gz" -C "$T/research" || { echo "ERROR: extract failed; nothing ran"; rm -rf "$T"; exit 32; }
cat > "$T/drive.py" <<'PY'
import sys
root, research = sys.argv[1], sys.argv[2]
sys.path.insert(0, root + "/ycharts/generate")
import resident_main  # noqa: F401,E402  (the unit's own path setup)
sys.path.insert(0, root + "/lib")
sys.path.insert(0, research)
import runner  # noqa: E402
sys.exit(runner.main(sys.argv[3:]))
PY
chown -R ec2-user "$T"
cd "$T"
run() {
  timeout 240 sudo -u ec2-user env -i HOME=/home/ec2-user USER=ec2-user LOGNAME=ec2-user LANG=C.UTF-8 \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 \
    /usr/bin/python3.12 "$T/drive.py" "$ROOT" "$T/research" \
    --firm cottonwood --portfolio "$PORTFOLIO" --map "$T/research/coverage_probe_map.json" \
    --bindings "$ROOT/reports/resident_bindings.json" --start "" --end "" --min-gap-s 8 "$@" 2>&1 | cut -c1-300
  return ${PIPESTATUS[0]}
}
echo "--- run A $REQ_A (bootstrap the index)"
run --request "$REQ_A" --bootstrap-index; RC_A=$?
sleep 10
echo "--- run B $REQ_B"
run --request "$REQ_B"; RC_B=$?
cd /
rm -rf "$T"
echo "r2 close end $(date -u +%Y-%m-%dT%H:%M:%SZ) rc A=$RC_A B=$RC_B work dir removed: $([ -d "$T" ] && echo no || echo yes)"
