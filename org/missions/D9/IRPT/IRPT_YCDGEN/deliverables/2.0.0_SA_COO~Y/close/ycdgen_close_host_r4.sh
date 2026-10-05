# IRPT_YCDGEN round-1 close: the ONE live run of FWD-1's calls on the resident host, inside the served lease.
# Sent verbatim through Systems Manager by live_walk/host_read.py (root). THIS IS A LIVE YCHARTS READ (Andrew-direct
# ~17:3xZ 2026-10-03: "COO~Y and any underlying agents have whitelisted egress to YCharts"; record @ce20ca6854).
# Shape follows live_walk/lookup_shape_host.sh: the RUNNING root (the unit's cwd), the unit's own path setup
# (import resident_main), the resident's user under env -i. The research bundle (runner.py, keeper.py, the element
# map) is fetched BY KEY from the host role's own artifact prefix and checked by sha256 before anything runs.
# runner.main composes ResidentSession, whose capture_workflow is None (no sign-in is reachable), takes the provider
# lease (OPERATION_BUSY stops it), keeps each answer scrubbed in Cottonwood's research table, writes run.json, releases
# the lease, and prints store keys, counts and clocks only. No session write, no vendor mutation. Bounded at 300 s. START/END are empty: the estate's proven fund_data form
# (ycharts-market-data-pull/ycharts_client.py fund_data: startDate/endDate empty, zoom=max) returns the whole series.
# Run 2 (after row IRPT_YCDGEN-S1): the runner writes on irpt-cot-ycharts-research-role, assumed before the lease.
# Run 3: --min-gap-s 8 (run 2 was WAF-challenged at its 7th call at ~1.5 s spacing; amendment f9f0d95cad), started
# after the challenge window (Y-4's cleared within its 900 s release). 12 calls x 8 s fits the 300 s bound and the lease.
# Round-3 close (E1 + E2): the derived 26-call map (round 1's failing calls retired), holdings from Y-5's frozen input
# (REQ-a618aa83, 99 rows, the user's SGOV correction), lease spacing only (~119 calls, ~5 min, inside the 600 s lease).
# ASCII only.
set -u
umask 077
BUNDLE_KEY=ec2/investor-reporting-ycharts/resident/ycdgen/ycdgen-r3-bundle-a876a58bae62.tar.gz
WANT=a876a58bae62dbbd85f1f49e5a0945152caa145f9ce5970a55fa0231d438bcfb
REQ=YCD-R3-20261005T0207Z
PORTFOLIO=P:2377833
START=""
END=""
UNIT=irpt-analysis-resident.service
PID=$(systemctl show $UNIT -p MainPID --value)
ROOT=$(readlink /proc/$PID/cwd)
echo "close run start $(date -u +%Y-%m-%dT%H:%M:%SZ) resident pid $PID root $ROOT"
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
timeout 560 sudo -u ec2-user env -i HOME=/home/ec2-user USER=ec2-user LOGNAME=ec2-user LANG=C.UTF-8 \
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 \
  /usr/bin/python3.12 "$T/drive.py" "$ROOT" "$T/research" \
  --firm cottonwood --request "$REQ" --portfolio "$PORTFOLIO" --map "$T/research/overview_map_r3_close.json" \
  --bindings "$ROOT/reports/resident_bindings.json" --start "$START" --end "$END" --holdings-from REQ-a618aa83407689bc95193a01 2>&1 | cut -c1-300
RC=${PIPESTATUS[0]}
cd /
rm -rf "$T"
echo "close run end $(date -u +%Y-%m-%dT%H:%M:%SZ) runner rc=$RC work dir removed: $([ -d "$T" ] && echo no || echo yes)"
