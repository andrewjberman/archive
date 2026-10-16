set -u
# IRPT_ANLREQ TO-APPLY-R34C (READ ONLY): how complete the r34c root is that the failed first send left. Writes nothing.
R=/opt/irpt-resident/0485393f3a-r34c
echo "POST2 r34c root owner/mode: $(stat -c '%U:%G %a' $R) mtime $(stat -c '%y' $R | cut -c1-19)"
echo "POST2 r34c root file count (excluding pydeps): $(find $R -type f -not -path '*/pydeps/*' | wc -l)"
echo "POST2 r34 (first attempt) root unchanged mtime: $(stat -c '%y' /opt/irpt-resident/0485393f3a-r34 | cut -c1-19)"
echo "POST2 kept copy: $(stat -c '%U:%G %a %s' /opt/investor-reporting-ycharts/ycharts_session.js.before-0485393f3a-r34c) sha256 $(sha256sum /opt/investor-reporting-ycharts/ycharts_session.js.before-0485393f3a-r34c | cut -c1-16)"
echo "POST2 /tmp tar: $(stat -c '%U:%G %a %s' /tmp/irpt-resident-0485393f3a-r34c.tar.gz) sha256 $(sha256sum /tmp/irpt-resident-0485393f3a-r34c.tar.gz | cut -c1-64)"
echo "POST2 r34c root members that are not owned by ec2-user: $(find $R -not -user ec2-user 2>/dev/null | wc -l)"
echo "POST2 r34c intake/yfinance_check.py: $([ -f $R/intake/yfinance_check.py ] && echo present || echo absent); swap_pool.json: $([ -f $R/ycharts/research/swap_pool.json ] && sha256sum $R/ycharts/research/swap_pool.json | cut -c1-64 || echo absent)"
echo "POST2 r32 root untouched: mtime $(stat -c '%y' /opt/irpt-resident/0485393f3a-r32 | cut -c1-19); worker sha256 $(sha256sum /opt/irpt-resident/0485393f3a-r32/ycharts/generate/resident_worker.py | cut -c1-16)"
echo "POST2 queue and journal: polls last 60s=$(journalctl -u irpt-analysis-resident.service --since '-60s' --no-pager 2>/dev/null | grep -c IRPT_RESIDENT_POLL)"
