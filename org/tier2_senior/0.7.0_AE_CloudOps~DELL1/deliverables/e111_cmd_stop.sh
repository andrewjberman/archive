sudo systemctl stop gold-layer-runner
echo STOP-RC=$?
echo ACTIVE=$(systemctl is-active gold-layer-runner)
ps -eo pid,etimes,cmd | grep -E 'gold_dispatch|run_gold_layer|gold-layer|build_canonical|A_00|A_02|C_06|python3? .*gold' | grep -v grep || echo NO-GOLD-PROCESS
echo UPTIME_SINCE=$(uptime -s) NOW=$(date -u +%H:%M:%SZ)
echo "--- steps the boot chain started (runner log)"
grep -E 'RUNNING|CHAIN|S_00|A_00|A_02|C_06|Started' /var/log/gold-layer-runner.log 2>/dev/null | tail -15 || true
echo "--- telemetry files written since boot"
find / -xdev -path '*telemetry*' -name '*.jsonl' -newermt "$(uptime -s)" 2>/dev/null | head -20
echo "--- logs in /tmp/gold_logs"
ls -la --time-style=full-iso /tmp/gold_logs 2>/dev/null | tail -8
