#!/usr/bin/env bash
# MP-pf-9 AC2 (SERVED, on the host: deployed bytes against the BUILD INPUT, CLAUDE.md 22a): read-only, one SSM command. The host's dashboard bundle IS the build of mcportal c66ca82952:
#   /health = 200 (control); sha256 of dashboard/index.html, dashboard/routes.json, dashboard/assets/index-BRnJX9Mi.css and dashboard/assets/index-DbObnWYp.js equal the hashes of a local build of c66ca82952
#   (measured by the issuer at ~12:2xZ; the same method, a local build of the deployed 090b9cdc85, matched the host byte for byte on all four members, so the comparison discriminates), and index.html names exactly those two assets;
#   no-identity GET / and GET /gateway each answer 401 or 403 (the owner gate holds); the registered MCP tool names equal in count before and after is the applier's own record, not read here.
# Control: the same read at the old live reads index.html a0ee33db... (the 090b9cdc85 build), so a PASS is not the check agreeing with everything.
. "$(dirname "$0")/../../pc/checks/_root.sh"
T="${TMPDIR:-/tmp}/mp_pf9_$$"; mkdir -p "$T"
python - "$(cygpath -m "$T")/p.json" <<'PY'
import json, sys
cmd = ("cd /opt/opal-gateway/dashboard && "
       "echo INDEX=$(sudo sha256sum index.html | cut -d' ' -f1) && echo ROUTES=$(sudo sha256sum routes.json | cut -d' ' -f1) && "
       "echo CSS=$(sudo sha256sum assets/index-BRnJX9Mi.css 2>&1 | cut -d' ' -f1) && echo JS=$(sudo sha256sum assets/index-DbObnWYp.js 2>&1 | cut -d' ' -f1) && "
       "echo REFS=$(grep -o 'assets/[^\"]*' index.html | sort | tr '\\n' ' ') && "
       "B=http://127.0.0.1:8080; echo HEALTH=$(curl -s -o /dev/null -w %{http_code} $B/health) && echo ROOT=$(curl -s -o /dev/null -w %{http_code} $B/) && echo GATEWAY=$(curl -s -o /dev/null -w %{http_code} $B/gateway)")
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PY
ssm_run "$T/p.json"; rm -f "$T/p.json"; rmdir "$T" 2>/dev/null
v() { printf '%s\n' "$SSM_OUT" | sed -n "s#^$1=##p" | head -1; }
INDEX=$(v INDEX); ROUTES=$(v ROUTES); CSS=$(v CSS); JS=$(v JS); REFS=$(v REFS); H=$(v HEALTH); R=$(v ROOT); G=$(v GATEWAY)
E_INDEX=5a6e2eeef8ec0e9d332774452220bd0ac6020934bbe0cdb5b195fd60c9ca57ee; E_ROUTES=e6d4a9ac3ce7d275158a56c490b586076cc0e728ae01501d5a0c88cba70207f1
E_CSS=120ae5bbd491dd201ae22cff044f09dbd0e0407dee0d985a2f78bc49451921e4; E_JS=52466cffc886f76eb1562351543fd31959392e18445f877d49d103a2447289fb
b=no; [ "$INDEX" = "$E_INDEX" ] && [ "$ROUTES" = "$E_ROUTES" ] && [ "$CSS" = "$E_CSS" ] && [ "$JS" = "$E_JS" ] && b=yes
refs=no; [ "$(printf '%s' "$REFS" | tr -s ' ' | sed 's/ $//')" = "assets/index-BRnJX9Mi.css assets/index-DbObnWYp.js" ] && refs=yes
echo "ssm command=$SSM_CID status=$SSM_ST; /health=$H; no-identity / =$R /gateway=$G"
echo "host index.html=${INDEX:0:12} routes=${ROUTES:0:12} css=${CSS:0:12} js=${JS:0:12}; expected index=${E_INDEX:0:12}"
echo "host bundle == build of c66ca82952: $b; index.html names exactly the two assets: $refs"
gate=yes; for s in "$R" "$G"; do case "$s" in 401|403) ;; *) gate=no;; esac; done
if [ "$SSM_ST" = Success ] && [ "$H" = 200 ] && [ "$gate" = yes ] && [ "$b" = yes ] && [ "$refs" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
