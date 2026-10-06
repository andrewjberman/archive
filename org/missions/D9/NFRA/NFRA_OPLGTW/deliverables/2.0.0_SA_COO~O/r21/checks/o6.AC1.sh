#!/usr/bin/env bash
# OPLGTW OG-o-6 AC1 (row Z-W15-S64, CTO R26(b)): runbooks/SCHWAB_PILOT_RUNBOOK.md section 5 (audit read / status
# summary) names the RAW lake prefix (opal-mcp-audit, audit/dt=<day>/) as the /login instrument of record and the
# gw_login fields (outcome, reason, email_digest); and LINEAGE_R18.json lists the runbook as a CLOUD_ONLY item (it is
# not shipped to the host, so CLOUD differs from live by it -- R16's list must say so).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
R="$GW/runbooks/SCHWAB_PILOT_RUNBOOK.md"; L="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~22/LINEAGE_R18.json"
python - "$(native "$R")" "$(native "$L")" <<'PY'
import json, re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"(?ms)^## 5\..*?(?=^## 6\.)", t); s5 = m.group(0) if m else ""
arms = {"prefix": "opal-mcp-audit" in s5 and "audit/dt=" in s5, "gw_login": "gw_login" in s5,
        "fields": all(f in s5 for f in ("outcome", "reason", "email_digest"))}
lin = json.load(open(sys.argv[2], encoding="utf-8"))
listed = any("runbooks/SCHWAB_PILOT_RUNBOOK.md" in str(i.get("path", "")) and i.get("kind") == "CLOUD_ONLY" for i in lin.get("items", []))
print("section 5 found %s; names raw prefix %s; gw_login %s; fields %s; runbook listed CLOUD_ONLY in LINEAGE %s"
      % (bool(s5), arms["prefix"], arms["gw_login"], arms["fields"], listed))
ok = bool(s5) and all(arms.values()) and listed
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
