set -u
# READ-ONLY. NEVER-2 artifact measure for ledger irpt-ycdgen-r6-branch-b2-20261006 (2.0.0_SA_COO~G2).
# Prints the resident roots present, the active root link, and the irpt services' state. Changes nothing.
echo "== roots"; ls -1 /opt/irpt-resident 2>&1 | head -20
echo "== links"; find /opt/irpt-resident -maxdepth 1 -type l -printf '%p -> %l\n' 2>&1
echo "== services"; systemctl list-units --type=service --all --no-pager 2>&1 | grep -i -E 'irpt|resident|ycharts'
for u in $(systemctl list-units --type=service --all --no-pager --plain 2>/dev/null | awk '{print $1}' | grep -i -E 'irpt|resident'); do
  echo "-- $u"; systemctl show "$u" -p ActiveState -p MainPID -p NRestarts -p ExecMainStartTimestamp -p WorkingDirectory --no-pager
done
