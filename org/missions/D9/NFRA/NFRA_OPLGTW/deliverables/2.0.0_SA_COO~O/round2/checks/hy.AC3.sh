#!/usr/bin/env bash
# OPLGTW OG-h-1 AC3: the register OUT_OF_REPO_CITATIONS.md classifies every file:line in the project tree that cites
# a C:/tmp/nfra-oplgtw-* path, each as "DURABLE <location>" or "ABSENT-ON-SITE-Z". Excluded from the census: the register
# itself, this order's file, and the issuer's deliverables dir (drafts and checks that quote the paths).
. "$(dirname "$0")/_root.sh"
P=org/missions/D9/NFRA/NFRA_OPLGTW
REG=$(git ls-files "$P/deliverables/" | grep '/OUT_OF_REPO_CITATIONS\.md$' | head -1)
[ -n "$REG" ] || { echo "register absent"; echo "RESULT: FAIL"; exit 1; }
python - "$P" "$REG" <<'PY'
import re,subprocess,sys
P,REG=sys.argv[1],sys.argv[2]
g=subprocess.run(["git","grep","-nE",r"[Cc]:[/\]+tmp[/\]+nfra-oplgtw-","--",P],capture_output=True).stdout.decode('utf-8','replace')
cites=set()
for l in g.splitlines():
    f,n,_=l.split(":",2)
    if f==REG or "/task-orders/NFRA_OPLGTW.TO-OG-h-1." in f or "/deliverables/2.0.0_SA_COO~O/" in f: continue
    cites.add(f"{f}:{n}")
reg={}
for l in open(REG,encoding='utf-8'):
    m=re.match(r"^\|\s*(\S+?):(\d+)\s*\|.*\|\s*(DURABLE \S.*?|ABSENT-ON-SITE-Z|[^|]*?)\s*\|\s*$",l)
    if m: reg[f"{m.group(1)}:{m.group(2)}"]=m.group(3)
miss=sorted(cites-set(reg)); uncl=sorted(k for k in cites&set(reg) if not re.match(r"^(DURABLE \S|ABSENT-ON-SITE-Z$)",reg[k]))
for k in miss[:20]: print("  missing:",k)
for k in uncl[:20]: print("  unclassified:",k,repr(reg[k]))
print(f"citations in tree={len(cites)}; in register {len(set(reg)&cites)}; missing {len(miss)}; unclassified {len(uncl)}")
ok=cites and not miss and not uncl
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
