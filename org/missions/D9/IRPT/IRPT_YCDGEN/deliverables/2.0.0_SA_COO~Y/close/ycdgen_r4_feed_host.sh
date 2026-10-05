# IRPT_YCDGEN round-4 close, window 2 (E1's live half + E5's second attempt), on the resident host inside the served
# lease. THIS IS A LIVE YCHARTS READ (Andrew-direct ~17:3xZ 2026-10-03, record @ce20ca6854). Shape:
# ycdgen_r4_measure_host.sh. The bundle is fetched BY KEY and checked by sha256 before anything runs.
# - Waits until 06:20:30Z: more than 660 s after window 1's last request (06:08:56Z).
# - Run C: feed_probe_map.json (YCD-o-4) over Y-5's frozen holdings (REQ-a618aa83, 99 rows): 3 expand calls x 2 chunks
#   of 50 = exactly 6 requests, never a 7th.
# - 660 s later, runs D and E: e5_dated_level_map_r4.json, ONE call each (the level series without zoom=max), --start
#   2025-10-01, --end 2026-09-30 then 2026-10-02, 10 s apart (2 requests in that window). E reads
#   changed_since_previous against D.
# No sign-in, no session write, no generate call, no retry. Bounded at 240 s per run. ASCII only.
set -u
umask 077
BUNDLE_KEY=ec2/investor-reporting-ycharts/resident/ycdgen/ycdgen-r4f-bundle-605c8a5ec2e2.tar.gz
WANT=605c8a5ec2e2387b1b2430fe09ddcd21886619a67701bf66eecdeb973cc57ff6
REQ_C=YCD-R4-20261005T0620Z-C
REQ_D=YCD-R4-20261005T0620Z-D
REQ_E=YCD-R4-20261005T0620Z-E
HOLDINGS_FROM=REQ-a618aa83407689bc95193a01
PORTFOLIO=P:2377833
NOT_BEFORE=$(date -u -d 2026-10-05T06:20:30Z +%s)
UNIT=irpt-analysis-resident.service
PID=$(systemctl show $UNIT -p MainPID --value)
ROOT=$(readlink /proc/$PID/cwd)
echo "r4 window 2 start $(date -u +%Y-%m-%dT%H:%M:%SZ) resident pid $PID root $ROOT"
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
    --firm cottonwood --portfolio "$PORTFOLIO" --bindings "$ROOT/reports/resident_bindings.json" "$@" 2>&1 | cut -c1-300
  return ${PIPESTATUS[0]}
}
NOW=$(date -u +%s)
[ "$NOW" -lt "$NOT_BEFORE" ] && { echo "--- waiting $((NOT_BEFORE - NOW)) s until 06:20:30Z"; sleep $((NOT_BEFORE - NOW)); }
echo "--- run C $REQ_C feed probe at $(date -u +%H:%M:%SZ)"
run --request "$REQ_C" --map "$T/research/feed_probe_map.json" --start "" --end "" --min-gap-s 8 --holdings-from "$HOLDINGS_FROM"; RC_C=$?
echo "--- wait 660 s from $(date -u +%H:%M:%SZ)"
sleep 660
echo "--- run D $REQ_D --end 2026-09-30 at $(date -u +%H:%M:%SZ)"
run --request "$REQ_D" --map "$T/research/e5_dated_level_map_r4.json" --start 2025-10-01 --end 2026-09-30; RC_D=$?
sleep 10
echo "--- run E $REQ_E --end 2026-10-02 at $(date -u +%H:%M:%SZ)"
run --request "$REQ_E" --map "$T/research/e5_dated_level_map_r4.json" --start 2025-10-01 --end 2026-10-02; RC_E=$?
cd /
rm -rf "$T"
echo "r4 window 2 end $(date -u +%Y-%m-%dT%H:%M:%SZ) rc C=$RC_C D=$RC_D E=$RC_E work dir removed: $([ -d "$T" ] && echo no || echo yes)"
