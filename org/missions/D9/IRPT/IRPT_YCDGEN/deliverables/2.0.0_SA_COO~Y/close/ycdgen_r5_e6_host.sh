# IRPT_YCDGEN round-5 close, E6 (CTO round-4 analysis E6; FWD-1, FWD-6): ONE budgeted live Overview run on the resident
# host. The merged map (overview_map.json @ff51386f38) plans 8 requests: 7 portfolio calls an element reads plus the
# benchmark level series (YCD-p-5); no per-holding call (the 158 held-data elements read Opal-held data, YCD-h-5/w-5).
# Run through the runner's budget (contract 4.1): 6 requests, the lease released and 660 s between windows (CTO batch 262
# item 3: 390 s only after its after-read holds), then 2. Holdings from Y-5's frozen input (REQ-a618aa83, 99 rows) ride
# run.json v2 for the Opal-held weights. The PLAN line prints first (contract 5.1).
# THIS IS A LIVE YCHARTS READ (Andrew-direct ~17:3xZ 2026-10-03, record @ce20ca6854). Bundle fetched BY KEY, checked by
# sha256. No sign-in, no session write, no generate call, no retry. Bounded at 900 s. ASCII only.
set -u
umask 077
BUNDLE_KEY=ec2/investor-reporting-ycharts/resident/ycdgen/ycdgen-e6-bundle-fb6c0f63feb7.tar.gz
WANT=fb6c0f63feb790f37b59e6fed6e10b2e36e41bf9042c715c2afcf950ecb2c5fb
REQ=YCD-R5-E6-$(date -u +%Y%m%dT%H%MZ)
PORTFOLIO=P:2377833
UNIT=irpt-analysis-resident.service
PID=$(systemctl show $UNIT -p MainPID --value)
ROOT=$(readlink /proc/$PID/cwd)
echo "e6 start $(date -u +%Y-%m-%dT%H:%M:%SZ) request $REQ resident pid $PID root $ROOT"
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
timeout 900 sudo -u ec2-user env -i HOME=/home/ec2-user USER=ec2-user LOGNAME=ec2-user LANG=C.UTF-8 \
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 \
  /usr/bin/python3.12 "$T/drive.py" "$ROOT" "$T/research" \
  --firm cottonwood --request "$REQ" --portfolio "$PORTFOLIO" --map "$T/research/overview_map.json" \
  --bindings "$ROOT/reports/resident_bindings.json" --start "" --end "" --min-gap-s 8 \
  --requests-per-window 6 --window-seconds 660 --holdings-from REQ-a618aa83407689bc95193a01 2>&1 | cut -c1-300
RC=${PIPESTATUS[0]}
cd /
rm -rf "$T"
echo "e6 end $(date -u +%Y-%m-%dT%H:%M:%SZ) runner rc=$RC work dir removed: $([ -d "$T" ] && echo no || echo yes)"
