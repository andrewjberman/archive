set -uo pipefail
# IB-pr-383 leg S2 -- the cottonwood seeding run, packet Branch A step 2.
#
# An exact analogue of ib383_seed_inflection.sh. THIN FETCH + EXEC, the same shape as refresh.py's
# own runner_script(): the code reaches this host only as the S3 bundle (CLAUDE.md rule 12), and no
# pipeline logic lives in this string. The one difference from the production recipe is the packet's
# --previous-key, which carries from the last accounted-completion build instead of the served
# directory. NO --as-of: the runner's own trading-day walk picks the newest COMPLETED date, which is
# what row W2-S55 taught.
#
# THE ONLY DIFFERENCES FROM THE S1 SCRIPT are the firm and its --previous-key. cottonwood's last
# accounted-completion build is 2026-10-05 (CTO 380/381 half, step 2), where inflection's is
# 2026-09-25. Those two dates are per-firm facts and are NOT interchangeable -- using inflection's
# key here would carry the wrong firm's frontier.
#
# It prints the bundle sha256 and the runner sha256 BEFORE building, so the record shows which bytes
# actually ran rather than which bytes were uploaded.
echo "[seed] S2 cottonwood at $(date -u +%Y-%m-%dT%H:%M:%SZ) on $(hostname)"
W=/tmp/irpt-383-seed-cottonwood
rm -rf $W && mkdir -p $W
aws s3 cp s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz $W/bundle.tar.gz --only-show-errors --region us-east-1 || { echo "[seed] ERROR: bundle fetch failed; nothing ran"; exit 90; }
echo "[seed] bundle sha256 $(sha256sum $W/bundle.tar.gz | cut -d' ' -f1)"
echo "[seed] bundle expected 2e3e6648312f5daad1da91f0c3aaeb4736a81b16cc9bb0dd4f43e5e93886b968"
tar -xzf $W/bundle.tar.gz -C $W || { echo "[seed] ERROR: extract failed; nothing ran"; exit 91; }
R=$W/data/assets/scripts/gold/investor_reporting
echo "[seed] runner sha256 $(sha256sum $R/directory_runner.py | cut -d' ' -f1)"
echo "[seed] --- build: cottonwood, previous-key investor-reporting/directory/2026-10-05/directory.json ---"
set +e
python3 $R/directory_runner.py --firms cottonwood --upload --previous-key investor-reporting/directory/2026-10-05/directory.json 2>&1
RC=$?
set -e
echo "[seed] runner rc=$RC"
rm -rf $W
echo "[seed] scratch removed; S2 done at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
