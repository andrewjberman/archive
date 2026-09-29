#!/usr/bin/env bash
# OPLGTW OG-o-3 AC2: section 7.2 names the manifest's live release, and every other commit it names (a rollback
# target) carries app/data_entitlement.py AND is a recorded opal-gateway deployed_commit in EC2_MANIFEST.json history.
. "$(dirname "$0")/_root.sh"
python - "$GW" <<'PY'
import json,re,subprocess,sys
gw=sys.argv[1]; M="infra/aws/ec2/EC2_MANIFEST.json"
def git(*a,inp=None): return subprocess.run(["git",*a],input=inp,capture_output=True).stdout
def dep(blob):
    try: return json.loads(blob.decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','')
    except Exception: return ''
live=dep(git("show","HEAD:"+M))
revs=git("log","--format=%H","HEAD","--",M).decode().split()
out=git("cat-file","--batch",inp="".join(f"{r}:{M}\n" for r in revs).encode())
hist=set(); i=0
while i<len(out):
    nl=out.index(b"\n",i); hdr=out[i:nl].split()
    if len(hdr)<3 or hdr[1]==b"missing": i=nl+1; continue
    n=int(hdr[2]); hist.add(dep(out[nl+1:nl+1+n])); i=nl+1+n+1
hist.discard('')
t=open(gw+"/runbooks/SCHWAB_PILOT_RUNBOOK.md",encoding='utf-8').read()
m=re.search(r"^### 7\.2.*?(?=^### 7\.3|\Z)",t,re.S|re.M); s=m.group(0) if m else ""
para="\n\n".join(s.split("\n\n")[:2])
shas=sorted(set(re.findall(r"`([0-9a-f]{10,40})`",para)))
nl_="yes" if any(live.startswith(x) for x in shas) else "no"
nv=len(re.findall(r"NO VALID ROLLBACK",s))
tg=[x for x in shas if not live.startswith(x)]
ng=[x for x in tg if subprocess.run(["git","cat-file","-e",f"{x}:{gw}/app/data_entitlement.py"],capture_output=True).returncode]
nh=[x for x in tg if not any(h.startswith(x) for h in hist)]
print(f"manifest history: {len(revs)} commits, {len(hist)} distinct deployed_commit values; live {live[:10]}")
for x in ng: print("  no guard:",x)
for x in nh: print("  not in manifest history:",x)
print(f"7.2 names live={nl_}; targets named {len(tg)}, without guard {len(ng)}, not in manifest history {len(nh)}; NO VALID ROLLBACK sentences {nv}")
ok= nl_=="yes" and tg and not ng and not nh and nv==0
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
