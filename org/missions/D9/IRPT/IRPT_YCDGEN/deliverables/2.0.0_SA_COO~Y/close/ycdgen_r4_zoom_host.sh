# IRPT_YCDGEN round-4 close, window 3: E5 by a lever that changes the answer under one call name (row IRPT_YCDGEN-S7:
# fund_data ignores startDate/endDate, so --end is not one). On the resident host inside the served lease, in the slot
# 2.0.0_SA_COO~D frees between Y-6 runs 2 and 3. THIS IS A LIVE YCHARTS READ (Andrew-direct ~17:3xZ 2026-10-03, record
# @ce20ca6854). Shape: ycdgen_r4_feed_host.sh. The bundle is fetched BY KEY and checked by sha256 before anything runs.
# - Run F: e5_zoom_5y_map_r4.json (portfolio_info + portfolio_level_series_zoom at zoom=5y), 2 requests.
# - Run G, 10 s later: e5_zoom_max_map_r4.json (the same two call names, zoom=max), 2 requests. G reads
#   changed_since_previous against F: true on the level series, false on portfolio_info.
# 4 requests in the window, 8 s apart. No sign-in, no session write, no generate call, no retry. Bounded at 120 s per run.
# ASCII only.
set -u
umask 077
BUNDLE_KEY=ec2/investor-reporting-ycharts/resident/ycdgen/ycdgen-r4z-bundle-ce7ccba6dc26.tar.gz
WANT=ce7ccba6dc263c7ba0b45fc1b802b4f2af02ae3aaf178577a0e52f5cec2462b0
REQ_F=YCD-R4-20261005T0700Z-F
REQ_G=YCD-R4-20261005T0700Z-G
PORTFOLIO=P:2377833
UNIT=irpt-analysis-resident.service
PID=$(systemctl show $UNIT -p MainPID --value)
ROOT=$(readlink /proc/$PID/cwd)
echo "r4 window 3 start $(date -u +%Y-%m-%dT%H:%M:%SZ) resident pid $PID root $ROOT"
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
  timeout 120 sudo -u ec2-user env -i HOME=/home/ec2-user USER=ec2-user LOGNAME=ec2-user LANG=C.UTF-8 \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 \
    /usr/bin/python3.12 "$T/drive.py" "$ROOT" "$T/research" \
    --firm cottonwood --portfolio "$PORTFOLIO" --bindings "$ROOT/reports/resident_bindings.json" \
    --start "" --end "" --min-gap-s 8 "$@" 2>&1 | cut -c1-300
  return ${PIPESTATUS[0]}
}
echo "--- run F $REQ_F zoom=5y at $(date -u +%H:%M:%SZ)"
run --request "$REQ_F" --map "$T/research/e5_zoom_5y_map_r4.json"; RC_F=$?
sleep 10
echo "--- run G $REQ_G zoom=max at $(date -u +%H:%M:%SZ)"
run --request "$REQ_G" --map "$T/research/e5_zoom_max_map_r4.json"; RC_G=$?
cd /
rm -rf "$T"
echo "r4 window 3 end $(date -u +%Y-%m-%dT%H:%M:%SZ) rc F=$RC_F G=$RC_G work dir removed: $([ -d "$T" ] && echo no || echo yes)"
