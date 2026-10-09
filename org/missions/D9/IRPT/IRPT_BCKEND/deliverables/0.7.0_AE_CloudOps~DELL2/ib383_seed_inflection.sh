set -uo pipefail
# IB-pr-383 leg S1 -- the inflection seeding run, packet Branch A step 2.
#
# THIN FETCH + EXEC, the same shape as refresh.py's own runner_script(): the code reaches this host
# only as the S3 bundle (CLAUDE.md rule 12), and no pipeline logic lives in this string. The one
# difference from the production recipe is the packet's --previous-key, which carries from the last
# accounted-completion build instead of the served directory. NO --as-of: the runner's own
# trading-day walk picks the newest COMPLETED date, which is what row W2-S55 taught.
#
# It prints the bundle sha256 and the runner sha256 BEFORE building, so the record shows which
# bytes actually ran rather than which bytes were uploaded.
echo "[seed] S1 inflection at $(date -u +%Y-%m-%dT%H:%M:%SZ) on $(hostname)"
W=/tmp/irpt-383-seed-inflection
rm -rf $W && mkdir -p $W
aws s3 cp s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz $W/bundle.tar.gz --only-show-errors --region us-east-1 || { echo "[seed] ERROR: bundle fetch failed; nothing ran"; exit 90; }
echo "[seed] bundle sha256 $(sha256sum $W/bundle.tar.gz | cut -d' ' -f1)"
echo "[seed] bundle expected 2e3e6648312f5daad1da91f0c3aaeb4736a81b16cc9bb0dd4f43e5e93886b968"
tar -xzf $W/bundle.tar.gz -C $W || { echo "[seed] ERROR: extract failed; nothing ran"; exit 91; }
R=$W/data/assets/scripts/gold/investor_reporting
echo "[seed] runner sha256 $(sha256sum $R/directory_runner.py | cut -d' ' -f1)"
echo "[seed] --- build: inflection, previous-key investor-reporting/directory/2026-09-25/directory.json ---"
set +e
python3 $R/directory_runner.py --firms inflection --upload --previous-key investor-reporting/directory/2026-09-25/directory.json 2>&1
RC=$?
set -e
echo "[seed] runner rc=$RC"
rm -rf $W
echo "[seed] scratch removed; S1 done at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
