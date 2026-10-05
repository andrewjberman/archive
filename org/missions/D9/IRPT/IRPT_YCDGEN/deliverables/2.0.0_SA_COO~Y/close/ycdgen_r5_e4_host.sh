# IRPT_YCDGEN round-5 close, E4 (FWD-2's true arm, CTO round-4 ruling 3): ONE research run of e5_zoom_max_map_r4.json
# (portfolio_info + portfolio_level_series_zoom at zoom=max; 2 requests, 8 s apart) on the MERGED runner (YCD-r-5 @84a7af1854:
# each kept call records request_sha256, and the flag compares like requests only), then the lookup (contract 5.4) of the
# level-series call. Leg 1 runs during the day: its previous is run G (no request_sha256), so it reads no_previous by
# contract. Leg 2 is this same script after today's close has reached YCharts: the byte-identical request against leg 1
# must read true, with the kept series' last date advanced.
# THIS IS A LIVE YCHARTS READ (Andrew-direct ~17:3xZ 2026-10-03, record @ce20ca6854). Bundle fetched BY KEY, checked by
# sha256. No sign-in, no session write, no generate call, no retry. Bounded at 120 s. ASCII only.
set -u
umask 077
BUNDLE_KEY=ec2/investor-reporting-ycharts/resident/ycdgen/ycdgen-e4-bundle-57a792acb47c.tar.gz
WANT=57a792acb47c61eca7cb2cd02308a8baf72c400c6f422c0a10e72d41eb063572
REQ=YCD-R5-E4-$(date -u +%Y%m%dT%H%MZ)
PORTFOLIO=P:2377833
UNIT=irpt-analysis-resident.service
PID=$(systemctl show $UNIT -p MainPID --value)
ROOT=$(readlink /proc/$PID/cwd)
echo "e4 start $(date -u +%Y-%m-%dT%H:%M:%SZ) request $REQ resident pid $PID root $ROOT"
T=$(mktemp -d /tmp/irpt-ycdgen-XXXXXX)
aws s3 cp "s3://opal-313476888478-lambda-artifacts/$BUNDLE_KEY" "$T/bundle.tar.gz" --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing ran"; rm -rf "$T"; exit 30; }
GOT=$(sha256sum "$T/bundle.tar.gz" | cut -d' ' -f1)
[ "$GOT" = "$WANT" ] || { echo "ERROR: bundle sha256 $GOT is not the signed bytes; nothing ran"; rm -rf "$T"; exit 31; }
mkdir -p "$T/research"
tar -xzf "$T/bundle.tar.gz" -C "$T/research" || { echo "ERROR: extract failed; nothing ran"; rm -rf "$T"; exit 32; }
cat > "$T/drive.py" <<'PY'
import sys
root, research, tool = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root + "/ycharts/generate")
import resident_main  # noqa: F401,E402  (the unit's own path setup)
sys.path.insert(0, root + "/lib")
sys.path.insert(0, research)
import importlib  # noqa: E402
sys.exit(importlib.import_module(tool).main(sys.argv[4:]))
PY
chown -R ec2-user "$T"
cd "$T"
as_user() {
  timeout 120 sudo -u ec2-user env -i HOME=/home/ec2-user USER=ec2-user LOGNAME=ec2-user LANG=C.UTF-8 \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 \
    /usr/bin/python3.12 "$T/drive.py" "$ROOT" "$T/research" "$@" 2>&1 | cut -c1-300
  return ${PIPESTATUS[0]}
}
as_user runner --firm cottonwood --request "$REQ" --portfolio "$PORTFOLIO" --map "$T/research/e5_zoom_max_map_r4.json" \
  --bindings "$ROOT/reports/resident_bindings.json" --start "" --end "" --min-gap-s 8; RC=$?
echo "--- lookup portfolio_level_series_zoom"
as_user lookup --firm cottonwood --request "$REQ" --call portfolio_level_series_zoom; RC_L=$?
cd /
rm -rf "$T"
echo "e4 end $(date -u +%Y-%m-%dT%H:%M:%SZ) runner rc=$RC lookup rc=$RC_L work dir removed: $([ -d "$T" ] && echo no || echo yes)"
