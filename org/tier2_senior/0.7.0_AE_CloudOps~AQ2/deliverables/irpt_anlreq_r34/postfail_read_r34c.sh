set -u
# IRPT_ANLREQ TO-APPLY-R34C (READ ONLY): what the failed first send of install_r34.sh (run as ec2-user, not root) left on the host. Writes nothing.
echo "POST whoami: $(id -un)"
echo "POST roots under /opt/irpt-resident: $(ls -A /opt/irpt-resident | tr '\n' ' ')"
echo "POST r34c root present: $([ -d /opt/irpt-resident/0485393f3a-r34c ] && echo yes || echo no)"
echo "POST r34 (first attempt) root present: $([ -d /opt/irpt-resident/0485393f3a-r34 ] && echo yes || echo no)"
echo "POST kept-copy path ycharts_session.js.before-0485393f3a-r34c present: $([ -e /opt/investor-reporting-ycharts/ycharts_session.js.before-0485393f3a-r34c ] && echo yes || echo no)"
echo "POST ycharts_session.js: $(stat -c '%U:%G %a %s' /opt/investor-reporting-ycharts/ycharts_session.js) sha256 $(sha256sum /opt/investor-reporting-ycharts/ycharts_session.js | cut -c1-64)"
echo "POST unit: $(systemctl is-active irpt-analysis-resident.service) MainPID=$(systemctl show -p MainPID --value irpt-analysis-resident.service) NRestarts=$(systemctl show -p NRestarts --value irpt-analysis-resident.service) ActiveEnter=$(systemctl show -p ActiveEnterTimestamp --value irpt-analysis-resident.service)"
echo "POST ExecStart: $(systemctl show -p ExecStart --value irpt-analysis-resident.service | grep -o '/opt/irpt-resident/[^/]*' | head -1)"
echo "POST receipts: $(ls /opt/irpt-resident/cutover_receipt.* 2>/dev/null | tr '\n' ' ')"
echo "POST tmp r34c leftovers: $(ls -d /tmp/*r34c* /tmp/irpt-r34* 2>/dev/null | tr '\n' ' ')"
echo "POST library sha256: $(sha256sum /opt/investor-reporting-ycharts/ycharts_session.js | cut -c1-16) (the order's P1 reads the library a1c28801...)"
