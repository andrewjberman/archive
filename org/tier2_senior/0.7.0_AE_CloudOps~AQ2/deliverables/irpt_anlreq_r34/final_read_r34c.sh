set -u
# IRPT_ANLREQ TO-APPLY-R34C (READ ONLY): the host after V2.
U=irpt-analysis-resident.service
echo "FINAL unit $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) NRestarts=$(systemctl show -p NRestarts --value $U) ActiveEnter=$(systemctl show -p ActiveEnterTimestamp --value $U)"
echo "FINAL running root: $(systemctl show -p ExecStart --value $U | grep -o '/opt/irpt-resident/[^/]*' | head -1)"
echo "FINAL journal since the start: polls=$(journalctl -u $U --since '2026-10-16 09:56:45' --no-pager 2>/dev/null | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $U --since '2026-10-16 09:56:45' --no-pager 2>/dev/null | grep -c Traceback) sign-in lines=$(journalctl -u $U --since '2026-10-16 09:56:45' --no-pager 2>/dev/null | grep -i -c -E 'capture|eviction|session refresh')"
echo "FINAL kept: r32 root $([ -d /opt/irpt-resident/0485393f3a-r32 ] && echo present || echo ABSENT); first-attempt r34 root $([ -d /opt/irpt-resident/0485393f3a-r34 ] && echo present || echo ABSENT); moved-aside copies: $(ls -d /opt/irpt-resident/*moved-aside* /opt/investor-reporting-ycharts/*moved-aside* /tmp/*moved-aside* 2>/dev/null | wc -l)"
echo "FINAL receipt copies: $(ls /opt/irpt-resident/cutover_receipt.* | wc -l) files; library sha256 $(sha256sum /opt/investor-reporting-ycharts/ycharts_session.js | cut -c1-16)"
