#!/usr/bin/env bash
# MP-pf-11 HOST read (after the round-38 release, the issuer's own read; not a worker criterion). Derived from pf9.AC2.sh: same SSM read, the bundle of mcportal 59e802a. Original header follows.
# MP-pf-9 AC2 (SERVED, on the host: deployed bytes against the BUILD INPUT, CLAUDE.md 22a): read-only, one SSM command. The host's dashboard bundle IS the build of mcportal c66ca82952:
#   /health = 200 (control); sha256 of dashboard/index.html, dashboard/routes.json, dashboard/assets/index-C2fVPBdg.css and dashboard/assets/index-xZd3bfhC.js equal the hashes of a local build of 59e802a
#   (measured by the issuer at ~12:2xZ; the same method, a local build of the deployed 090b9cdc85, matched the host byte for byte on all four members, so the comparison discriminates), and index.html names exactly those two assets;
#   no-identity GET / and GET /gateway each answer 401 or 403 (the owner gate holds); the registered MCP tool names equal in count before and after is the applier's own record, not read here.
# Control: the same read at the old live reads index.html a0ee33db... (the 090b9cdc85 build), so a PASS is not the check agreeing with everything.
. "$(dirname "$0")/../../pc/checks/_root.sh"
T="${TMPDIR:-/tmp}/mp_pf11host_$$"; mkdir -p "$T"
python - "$(cygpath -m "$T")/p.json" <<'PY'
import json, sys
cmd = ("cd /opt/opal-gateway/dashboard && "
       "echo INDEX=$(sudo sha256sum index.html | cut -d' ' -f1) && echo ROUTES=$(sudo sha256sum routes.json | cut -d' ' -f1) && "
       "echo CSS=$(sudo sha256sum assets/index-C2fVPBdg.css 2>&1 | cut -d' ' -f1) && echo JS=$(sudo sha256sum assets/index-xZd3bfhC.js 2>&1 | cut -d' ' -f1) && "
       "echo REFS=$(grep -o 'assets/[^\"]*' index.html | sort | tr '\\n' ' ') && "
       "B=http://127.0.0.1:8080; echo HEALTH=$(curl -s -o /dev/null -w %{http_code} $B/health) && echo ROOT=$(curl -s -o /dev/null -w %{http_code} $B/) && echo GATEWAY=$(curl -s -o /dev/null -w %{http_code} $B/gateway)")
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PY
ssm_run "$T/p.json"; rm -f "$T/p.json"; rmdir "$T" 2>/dev/null
v() { printf '%s\n' "$SSM_OUT" | sed -n "s#^$1=##p" | head -1; }
INDEX=$(v INDEX); ROUTES=$(v ROUTES); CSS=$(v CSS); JS=$(v JS); REFS=$(v REFS); H=$(v HEALTH); R=$(v ROOT); G=$(v GATEWAY)
E_INDEX=01e4a6a69b5e50139e2daae607e1298c50d42bd33e2429db3da039e56e307903; E_ROUTES=e6d4a9ac3ce7d275158a56c490b586076cc0e728ae01501d5a0c88cba70207f1
E_CSS=05691c2f4363e8876a411bfadaec81ef65034206e74dd61ea902fe89c824ccbf; E_JS=52466cffc886f76eb1562351543fd31959392e18445f877d49d103a2447289fb
b=no; [ "$INDEX" = "$E_INDEX" ] && [ "$ROUTES" = "$E_ROUTES" ] && [ "$CSS" = "$E_CSS" ] && [ "$JS" = "$E_JS" ] && b=yes
refs=no; [ "$(printf '%s' "$REFS" | tr -s ' ' | sed 's/ $//')" = "assets/index-C2fVPBdg.css assets/index-xZd3bfhC.js" ] && refs=yes
echo "ssm command=$SSM_CID status=$SSM_ST; /health=$H; no-identity / =$R /gateway=$G"
echo "host index.html=${INDEX:0:12} routes=${ROUTES:0:12} css=${CSS:0:12} js=${JS:0:12}; expected index=${E_INDEX:0:12}"
echo "host bundle == build of 59e802a: $b; index.html names exactly the two assets: $refs"
gate=yes; for s in "$R" "$G"; do case "$s" in 401|403) ;; *) gate=no;; esac; done
if [ "$SSM_ST" = Success ] && [ "$H" = 200 ] && [ "$gate" = yes ] && [ "$b" = yes ] && [ "$refs" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
