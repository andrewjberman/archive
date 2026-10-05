# IRPT_YCDGEN round-4 close measurement (E5 + E1's live half): TWO live runs of measure_map_r4.json (6 calls each, never
# a 7th request in one run) on the resident host, inside the served lease, 8 s apart per call, 660 s between the runs
# (longer than the longest AWS WAF rate window, 600 s). Run A ends 2026-09-30; run B ends 2026-10-02 (the last close
# before Monday). Same call names, so run B reads changed_since_previous per call against run A: FWD-2's TRUE arm on
# portfolio_level_series (its --end moved) beside portfolio_info (it did not). security_info_probe and
# security_price_probe test the YCharts security-level routes on a public ticker (AAPL) for contract 4.2's feed.
# THIS IS A LIVE YCHARTS READ (Andrew-direct ~17:3xZ 2026-10-03, record @ce20ca6854). Shape: ycdgen_r2_close_host.sh.
# Runner and keeper are the bytes of wk-ycdgen-r4-1 (merged @0a439396d1). The bundle is fetched BY KEY and checked by
# sha256 before anything runs. No sign-in, no session write, no generate call, no retry. Bounded at 240 s per run.
# ASCII only.
set -u
umask 077
BUNDLE_KEY=ec2/investor-reporting-ycharts/resident/ycdgen/ycdgen-r4m-bundle-e766c088121f.tar.gz
WANT=e766c088121fc7bfa89308adc710652903358583fcee1553ee088ac33c43c8dd
REQ_A=YCD-R4-20261005T0552Z-A
REQ_B=YCD-R4-20261005T0552Z-B
PORTFOLIO=P:2377833
UNIT=irpt-analysis-resident.service
PID=$(systemctl show $UNIT -p MainPID --value)
ROOT=$(readlink /proc/$PID/cwd)
echo "r4 measure start $(date -u +%Y-%m-%dT%H:%M:%SZ) resident pid $PID root $ROOT"
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
    --firm cottonwood --portfolio "$PORTFOLIO" --map "$T/research/measure_map_r4.json" \
    --bindings "$ROOT/reports/resident_bindings.json" --start "" --min-gap-s 8 "$@" 2>&1 | cut -c1-300
  return ${PIPESTATUS[0]}
}
echo "--- run A $REQ_A --end 2026-09-30 at $(date -u +%H:%M:%SZ)"
run --request "$REQ_A" --end 2026-09-30; RC_A=$?
echo "--- wait 660 s from $(date -u +%H:%M:%SZ)"
sleep 660
echo "--- run B $REQ_B --end 2026-10-02 at $(date -u +%H:%M:%SZ)"
run --request "$REQ_B" --end 2026-10-02; RC_B=$?
cd /
rm -rf "$T"
echo "r4 measure end $(date -u +%Y-%m-%dT%H:%M:%SZ) rc A=$RC_A B=$RC_B work dir removed: $([ -d "$T" ] && echo no || echo yes)"
