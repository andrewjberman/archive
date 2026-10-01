#!/usr/bin/env bash
# MS-t-3 AC1 (the built files, read in the nested opal_ai checkout): opal/runtime-msp/ holds CLAUDE.md,
# .claude/settings.json, mcp.json.example with EXACTLY ONE server whose url is https://mcp.opalinvest.dev/mcp, and
# provision/runtime.msp.config.example.json whose account_name is Opal_MSP; and each of the four shared scripts
# (provision-account.ps1, verify-boundary.ps1, launcher.ps1, launch-gate.ps1) reads `account_name` from its config.
. "$(dirname "$0")/_root.sh"
O="opal_ai/opal"
res=$(python - "$O" <<'EOF' 2>&1 | tr -d '\r'
import json, os, sys
O = sys.argv[1]; M = os.path.join(O, 'runtime-msp'); R = os.path.join(O, 'runtime')
def rd(p):
    try: return open(p, encoding='utf-8').read()
    except Exception: return None
c = {}
c['claude_md'] = rd(os.path.join(M, 'CLAUDE.md')) is not None
c['settings'] = rd(os.path.join(M, '.claude', 'settings.json')) is not None
try:
    srv = json.loads(rd(os.path.join(M, 'mcp.json.example')) or '{}').get('mcpServers', {})
    c['one_server'] = len(srv) == 1 and list(srv.values())[0].get('url') == 'https://mcp.opalinvest.dev/mcp'
except Exception:
    c['one_server'] = False
try:
    c['msp_account'] = json.loads(rd(os.path.join(M, 'provision', 'runtime.msp.config.example.json')) or '{}').get('account_name') == 'Opal_MSP'
except Exception:
    c['msp_account'] = False
for s in ('provision/provision-account.ps1', 'provision/verify-boundary.ps1', 'launcher.ps1', 'launch-gate.ps1'):
    t = rd(os.path.join(R, s)) or ''
    c[os.path.basename(s)] = 'account_name' in t
print(' '.join('%s=%s' % (k, 'y' if v else 'n') for k, v in c.items()), 'verdict=%s' % ('OK' if all(c.values()) else 'NO'))
EOF
)
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
