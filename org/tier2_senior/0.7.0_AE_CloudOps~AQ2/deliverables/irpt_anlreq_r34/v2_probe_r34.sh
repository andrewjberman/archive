set -u
# IRPT_ANLREQ TO-APPLY-R34B, after the V2 FAIL (ModuleNotFoundError on `import yfinance`): ONE read-only probe of where the library is and is not.
# No Yahoo call, no network call, no install, no write. Prints booleans, counts and directory NAMES only.
R=/opt/irpt-resident
RUN=$(systemctl show irpt-analysis-resident.service -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "PROBE at $(date -u +%Y-%m-%dT%H:%M:%SZ) running root $RUN"
echo "PROBE pydeps directory names matching yfinance, pandas, numpy, requests, curl_cffi, peewee, lxml (names only):"
ls -1 /opt/investor-reporting-ycharts/pydeps 2>/dev/null | grep -i -E '^(yfinance|pandas|numpy|requests|curl_cffi|peewee|lxml|multitasking|frozendict|platformdirs)' | head -30
echo "PROBE pydeps entry count: $(ls -1 /opt/investor-reporting-ycharts/pydeps 2>/dev/null | wc -l)"
for who in ec2-user root; do
  if [ "$who" = root ]; then PREFIX=""; else PREFIX="sudo -u ec2-user HOME=/home/ec2-user"; fi
  $PREFIX /usr/bin/python3.12 - <<'PY'
import getpass, importlib.util, os, sys
who = getpass.getuser()
plain = importlib.util.find_spec("yfinance") is not None
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
withdeps = importlib.util.find_spec("yfinance") is not None
print("PROBE user %s: yfinance found on the default path=%s, with the resident's pydeps appended=%s" % (who, plain, withdeps))
PY
done
echo "PROBE site-packages directory names matching yfinance (system python3.12, names only): $(ls -d /usr/lib/python3.12/site-packages/yfinance* /usr/lib64/python3.12/site-packages/yfinance* /usr/local/lib/python3.12/site-packages/yfinance* /home/ec2-user/.local/lib/python3.12/site-packages/yfinance* 2>/dev/null | wc -l)"
echo "PROBE r32 root and r34 root hold a yfinance directory: r32=$(find /opt/irpt-resident/0485393f3a-r32 -maxdepth 2 -type d -name 'yfinance*' | wc -l) r34=$(find /opt/irpt-resident/0485393f3a-r34 -maxdepth 2 -type d -name 'yfinance*' | wc -l)"
