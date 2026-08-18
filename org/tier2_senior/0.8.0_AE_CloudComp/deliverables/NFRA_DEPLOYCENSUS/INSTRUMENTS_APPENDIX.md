# NFRA_DEPLOYCENSUS — census instruments (appendix)

**Why fenced listings and not `.py` files:** the Rule-14 commit gate (ruff py39) correctly refuses these one-shot evidence scripts (151 style findings — they are scratch instruments, not lane python), and `--force` does not bypass a gate failure by design. Committing them as listings keeps the method re-runnable (copy out, run) without placing non-conformant `.py` where a deploy lane or import could pick it up. Reads are 100% read-only: list/get-function/get-object/describe + SSM sha256sum/Get-FileHash.

## lambda_census_v3.py

```python
"""NFRA_DEPLOYCENSUS -- Lambda half, v2 (final). Rule 22a CODE layer. Classify only. Read-only.
Resolution is through the BUILD INPUT per source-map shape:
  A. BUILD_MANIFEST.json inside the package (assembled-from-pinned-commit builders): module -> repo_path + vintage
  B. inline_archive_file (TF data.archive_file over a directory): every file in that dir at HEAD minus excludes
  C. nodejs (bun build --minify): bytes are TRANSFORMED -> provenance chain live.CodeSha256 == map.artifact_sha256
     (the artifact built at last_deployed_commit) then git log last_deployed_commit..HEAD -- source_dir
  D. files[] empty but source_dir exists: members resolved against the source_dir tree by basename (the build
     input names the DIRECTORY, so directory+basename is the resolution -- declared weaker)
  E. default: source_dir + files[] -> zip member of the same relative path (build-and-upload.sh convention)
Discriminators on a DIFFERS member (.py): cosmetic-only (AST equal with docstrings stripped) / deployed==working-tree
/ deployed in path history (older) / deployed bytes found at another HEAD path.
"""
from __future__ import annotations
import boto3, json, hashlib, io, zipfile, subprocess, urllib.request, os, sys, re, time, collections, ast, difflib, base64
from concurrent.futures import ThreadPoolExecutor

OUT = os.path.dirname(os.path.abspath(__file__))
WS = subprocess.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip()
HEAD = subprocess.run(['git','-C',WS,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
smap = json.load(open(os.path.join(WS,'infra/aws/lambda/ci/lambda-source-map.json'),encoding='utf-8'))
funcs = smap['functions']

def sha256(b): return hashlib.sha256(b).hexdigest()
def blobsha(b): return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
def norm(b): return b.replace(b'\r\n', b'\n')
def git(*a, binary=False):
    r=subprocess.run(['git','-C',WS]+list(a),capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf-8','replace')

# ---- HEAD tree index --------------------------------------------------------
head_path2blob={}; blob2paths=collections.defaultdict(list); base2paths=collections.defaultdict(list)
for rec in git('ls-tree','-r','-z','HEAD',binary=True).split(b'\0'):
    if not rec: continue
    meta,path=rec.split(b'\t',1); sha=meta.decode().split(' ')[2]; p=path.decode('utf-8','replace')
    head_path2blob[p]=sha; blob2paths[sha].append(p); base2paths[os.path.basename(p)].append(p)
_blobcache={}
def blob_bytes(sha):
    if sha not in _blobcache: _blobcache[sha]=git('cat-file','blob',sha,binary=True)
    return _blobcache[sha]
def head_bytes(path):
    b=head_path2blob.get(path); return blob_bytes(b) if b else None
def wt_bytes(path):
    p=os.path.join(WS,path); return open(p,'rb').read() if os.path.isfile(p) else None
def commit_date(c): return git('show','-s','--format=%cI',c).strip()
def commit_subj(c): return git('show','-s','--format=%h %ci %an %s',c).strip()
_hist={}
def path_history(path, limit=400):
    if path in _hist: return _hist[path]
    out=[]
    for c in git('log','--format=%H','-n',str(limit),'--',path).split():
        t=git('ls-tree',c,'--',path).strip()
        if t: out.append((c,t.split()[2]))
    _hist[path]=out; return out

def strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef,ast.Module)):
            if node.body and isinstance(node.body[0],ast.Expr) and isinstance(getattr(node.body[0],'value',None),ast.Constant) and isinstance(node.body[0].value.value,str):
                node.body=node.body[1:] or [ast.Pass()]
    return tree
class _StrNorm(ast.NodeTransformer):
    def visit_Constant(self,node):
        if isinstance(node.value,str): return ast.copy_location(ast.Constant(value='<STR>'),node)
        return node
def strings_only(a,b):
    """AST-identical once every string constant is masked (docstrings stripped): the delta is ONLY string-literal VALUES."""
    try:
        ta=_StrNorm().visit(strip_docstrings(ast.parse(a))); tb=_StrNorm().visit(strip_docstrings(ast.parse(b)))
        return ast.dump(ta,include_attributes=False)==ast.dump(tb,include_attributes=False)
    except Exception: return None
HOLD_MSG_RE=re.compile(r'(NOT DEPLOYED|COMMIT ONLY|APPLY NOTHING|staged, not applied|STAGED-NOT-APPLIED|CTO-gated|COO-gated|DELIBERATELY NOT APPLIED|do not deploy|not to be deployed|deploy is a separate act|held|HOLD)',re.I)
def commit_hold_statements(repo_path, deployed_commit):
    """Scan messages of commits touching repo_path AFTER deployed_commit for a stated hold."""
    out=[]
    log=git('log','--format=%H%x00%s%n%b%x01',f'{deployed_commit}..HEAD','--',repo_path)
    for chunk in log.split('\x01'):
        if '\x00' not in chunk: continue
        h,msg=chunk.split('\x00',1); m=HOLD_MSG_RE.search(msg)
        if m:
            s0=max(0,m.start()-90); out.append(f"{h[:10]}: ...{' '.join(msg[s0:m.end()+110].split())}...")
    return out
def cosmetic_only(a,b):
    """True if two python sources are AST-identical after docstring removal (comments are not in the AST)."""
    try:
        ta=strip_docstrings(ast.parse(a)); tb=strip_docstrings(ast.parse(b))
        return ast.dump(ta,include_attributes=False)==ast.dump(tb,include_attributes=False)
    except Exception:
        return None
def sim(a,b):
    try: return round(difflib.SequenceMatcher(None,a.decode('utf-8','replace'),b.decode('utf-8','replace')).ratio(),3)
    except Exception: return None

CANON_RE=re.compile(r'^(data/[^/]+/(?:[^/]+/)?scripts/|lib/|tools/)')
SKIP_BASENAMES={'lambda_function.py','__init__.py','config.py','handler.py','index.py','utils.py','main.py','conftest.py','setup.py','_util.py','run.py','pipeline.py','formatter.py','orchestrator.py'}
# NOTE: the last five are known vendored/unrelated collisions found in pass 1 (pandas/bs4/h11/openai/pydantic and
# a deck engine); they are excluded from the CANDIDATE predicate only after being inspected -- listed in the method note.

# ---- live inventory --------------------------------------------------------------
lam=boto3.client('lambda',region_name='us-east-1')
live={}
for page in lam.get_paginator('list_functions').paginate():
    for f in page['Functions']: live[f['FunctionName']]=f
names=list(funcs.keys())
in_map_live=[n for n in names if n in live]; in_map_notlive=[n for n in names if n not in live]
live_not_in_map=sorted(set(live)-set(names))
print(f"HEAD={HEAD} | source-map N={len(names)} | live total={len(live)} | in-map&live={len(in_map_live)} | in-map NOT live={len(in_map_notlive)} | live NOT in map={len(live_not_in_map)}")

def fetch(name):
    try: gf=lam.get_function(FunctionName=name)
    except Exception as e: return name,None,f"get_function error: {e}"
    code=gf.get('Code',{}); cfg=gf['Configuration']
    if cfg.get('PackageType')=='Image' or 'ImageUri' in code: return name,{'cfg':cfg,'image':code},None
    try: data=urllib.request.urlopen(code.get('Location'),timeout=180).read()
    except Exception as e: return name,{'cfg':cfg},f"download error: {e}"
    return name,{'cfg':cfg,'zip':data},None
t0=time.time(); fetched={}
with ThreadPoolExecutor(max_workers=8) as ex:
    for name,obj,err in ex.map(fetch,in_map_live): fetched[name]=(obj,err)
print(f"fetched {len(fetched)} packages in {time.time()-t0:.0f}s")

def held_candidates(e):
    HOLD_RE=re.compile(r'(deliberately|\bheld\b|\bhold\b|DORMANT|UNWIRED|do not deploy|not yet deploy|pre.?stage|deferred|frozen|ignore_changes|managed outside|out-of-band|swap-into)',re.I)
    hits=[]
    for k,v in e.items():
        if isinstance(v,str):
            m=HOLD_RE.search(v)
            if m: s=max(0,m.start()-100); hits.append(f"{k}: ...{v[s:m.end()+140]}...")
    return hits

def member_verdict(m, repo_path, content, vintage_commit=None):
    """Fill m with verdict fields comparing deployed `content` to repo_path at HEAD (and vintage if given)."""
    m['repo_path']=repo_path; m['deployed_sha256']=sha256(content); m['deployed_blob']=blobsha(content)
    hb=head_path2blob.get(repo_path); m['head_blob']=hb
    if vintage_commit:
        vb=git('ls-tree',vintage_commit,'--',repo_path).strip()
        m['vintage_commit']=vintage_commit; m['vintage_blob']=vb.split()[2] if vb else None
        m['deployed_eq_vintage']=(m['vintage_blob'] is not None and (m['vintage_blob']==m['deployed_blob'] or norm(blob_bytes(m['vintage_blob']))==norm(content)))
    if hb is None:
        m['verdict']='NO-HEAD-SOURCE (deployed carries a member the repo lacks at HEAD)'; other=[p for p in blob2paths.get(m['deployed_blob'],[])]
        if other: m['deployed_bytes_found_at_HEAD']=other[:5]; return 'WRONGDIR'
        return 'NOSRC'
    hc=blob_bytes(hb)
    if m['deployed_blob']==hb or norm(hc)==norm(content):
        m['verdict']='CURRENT' if m['deployed_blob']==hb else 'CURRENT (eol-only)'; return 'CURRENT'
    m['verdict']='DIFFERS'; m['similarity_deployed_vs_head']=sim(content,hc)
    if repo_path.endswith('.py'):
        m['cosmetic_only']=cosmetic_only(hc.decode('utf-8','replace'),content.decode('utf-8','replace'))
        m['strings_only']=strings_only(hc.decode('utf-8','replace'),content.decode('utf-8','replace'))
    w=wt_bytes(repo_path); m['wt_dirty']=(w is not None and blobsha(w)!=hb)
    m['deployed_eq_working_tree']=(w is not None and norm(w)==norm(content))
    hist=path_history(repo_path); hit=[c for c,b in hist if b==m['deployed_blob']]
    if not hit:  # eol-normalized history scan
        for c,b in hist:
            if norm(blob_bytes(b))==norm(content): hit=[c]; break
    if hit:
        m['deployed_matches_history_commit']=hit[0]; m['deployed_commit']=commit_subj(hit[0])
        m['head_commit_for_path']=commit_subj(hist[0][0]) if hist else None
        newer=[c for c,b in hist]  # newest first
        m['commits_since_deployed']=newer.index(hit[0]) if hit[0] in newer else None
        m['hold_statements_in_commits']=commit_hold_statements(repo_path,hit[0])
        if m['hold_statements_in_commits']: return 'HELD-STATED'
        if m.get('cosmetic_only'): return 'COSMETIC'
        if m.get('strings_only'): return 'STRINGS'
        return 'OLDER'
    other=[p for p in blob2paths.get(m['deployed_blob'],[]) if p!=repo_path]
    if other: m['deployed_bytes_found_at_HEAD']=other[:5]; return 'WRONGDIR'
    if m['deployed_eq_working_tree']: return 'AHEAD-WT'
    return 'COSMETIC' if m.get('cosmetic_only') else 'UNATTRIBUTED'

rows=[]; findings=[]
def F(lam_name, axis, cls, subkind, evidence): findings.append({'lambda':lam_name,'axis':axis,'class':cls,'subkind':subkind,'evidence':evidence})

for name in names:
    e=funcs[name]; src_dir=(e.get('source_dir') or '').rstrip('/'); files=e.get('files') or []
    if isinstance(files,str):
        try: files=json.loads(files.replace("'",'"'))
        except Exception: files=[]
    row={'lambda':name,'source_dir':src_dir,'files':files,'tf_resource':e.get('tf_resource'),'map_last_deployed_commit':e.get('last_deployed_commit'),
         'map_last_deployed_at':e.get('last_deployed_at'),'map_artifact_sha256':e.get('artifact_sha256'),'resolution':None,'class':None,'subkind':None,
         'evidence':[],'members':[],'extra_py_members':[],'two_homes':[],'held_candidates':held_candidates(e)}
    if name not in live:
        row['class']='UNREAD'; row['subkind']='NOT-LIVE'; row['evidence'].append('map entry has no live function (absent from list_functions, all pages)')
        F(name,'own-tree','UNREAD','NOT-LIVE',row['evidence'][-1]); rows.append(row); continue
    obj,err=fetched[name]; cfg=obj['cfg'] if obj else {}
    row['live']={'CodeSha256':cfg.get('CodeSha256'),'LastModified':cfg.get('LastModified'),'Runtime':cfg.get('Runtime'),'PackageType':cfg.get('PackageType'),'CodeSize':cfg.get('CodeSize'),'Layers':[l.get('Arn','').split(':layer:')[-1] for l in cfg.get('Layers',[])]}
    row['live_eq_map_artifact']=(bool(e.get('artifact_sha256')) and e.get('artifact_sha256')==cfg.get('CodeSha256'))
    if err:
        row['class']='UNREAD'; row['subkind']='PACKAGE-UNREACHABLE'; row['evidence'].append(err); F(name,'own-tree','UNREAD','PACKAGE-UNREACHABLE',err); rows.append(row); continue
    if 'image' in obj:
        ev=f"container image {obj['image'].get('ImageUri')} resolved={obj['image'].get('ResolvedImageUri')} -- image layers not read (zip-member domain only)"
        row['class']='UNREAD'; row['subkind']='CONTAINER-IMAGE'; row['evidence'].append(ev); F(name,'own-tree','UNREAD','CONTAINER-IMAGE',ev); rows.append(row); continue
    try: z=zipfile.ZipFile(io.BytesIO(obj['zip']))
    except Exception as ex2:
        row['class']='UNREAD'; row['subkind']='ZIP-UNREADABLE'; row['evidence'].append(str(ex2)); F(name,'own-tree','UNREAD','ZIP-UNREADABLE',str(ex2)); rows.append(row); continue
    zsha={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
    row['package_member_count']=len(zsha)
    verdicts=[]; resolved_members=set()
    # ---- A. BUILD_MANIFEST -------------------------------------------------------------------
    if 'BUILD_MANIFEST.json' in zsha:
        row['resolution']='A:BUILD_MANIFEST'
        try: bm=json.loads(zsha['BUILD_MANIFEST.json'].decode('utf-8'))
        except Exception as ex2: bm=None; row['evidence'].append(f'BUILD_MANIFEST unparseable: {ex2}')
        if bm:
            vintage=(bm.get('source_vintage') or {}).get('commit'); row['build_manifest_vintage']=vintage
            for mod,info in (bm.get('modules') or {}).items():
                m={'file':mod,'zip_member':mod if mod in zsha else None}
                if mod not in zsha: m['verdict']='MISSING-IN-PACKAGE'; verdicts.append('MISSING'); row['members'].append(m); continue
                content=zsha[mod]; resolved_members.add(mod)
                m['manifest_sha256']=info.get('sha256'); m['manifest_sha_matches_deployed']=(info.get('sha256')==sha256(content))
                verdicts.append(member_verdict(m,info.get('repo_path') or f"{src_dir}/{mod}",content,vintage_commit=vintage))
                row['members'].append(m)
    # ---- B. inline archive_file ---------------------------------------------------------------
    elif e.get('inline_archive_file') or src_dir=='infra/aws/compdiff':
        row['resolution']='B:INLINE-ARCHIVE'
        excludes=('__pycache__','tests','org')
        for p,b in head_path2blob.items():
            if not p.startswith(src_dir+'/'): continue
            rel=p[len(src_dir)+1:]
            if any(rel.split('/')[0]==x or f'/{x}/' in '/'+rel for x in excludes): continue
            m={'file':rel,'zip_member':rel if rel in zsha else None}
            if rel not in zsha: m['verdict']='MISSING-IN-PACKAGE'; verdicts.append('MISSING'); row['members'].append(m); continue
            resolved_members.add(rel); verdicts.append(member_verdict(m,p,zsha[rel])); row['members'].append(m)
    # ---- C. nodejs transformed build --------------------------------------------------------
    elif e.get('build_type')=='nodejs' or any(str(f).endswith('.mjs') for f in files):
        row['resolution']='C:NODEJS-PROVENANCE-CHAIN'
        art=e.get('artifact_sha256'); ldc=e.get('last_deployed_commit')
        row['evidence'].append(f"bytes are bun-build --minify TRANSFORMED; byte-diff to source is malformed. Chain: live.CodeSha256={cfg.get('CodeSha256')} map.artifact_sha256={art} equal={row['live_eq_map_artifact']}")
        if row['live_eq_map_artifact'] and ldc and re.fullmatch(r'[0-9a-f]{7,40}',str(ldc)):
            moved=git('log','--format=%h %ci %s',f'{ldc}..HEAD','--',src_dir).strip().splitlines()
            row['evidence'].append(f"source_dir commits since last_deployed_commit {ldc[:10]}: {len(moved)}" + (' -> '+moved[0] if moved else ''))
            verdicts.append('OLDER' if moved else 'CURRENT')
            row['members'].append({'file':files,'verdict':'CURRENT (chain)' if not moved else 'DIFFERS (chain: source moved since recorded build)','commits_since':moved[:5]})
        else:
            verdicts.append('CHAIN-BROKEN'); row['members'].append({'file':files,'verdict':'PROVENANCE-CHAIN-BROKEN (live CodeSha256 != map artifact_sha256, or no last_deployed_commit)'})
    # ---- D. files[] empty, source_dir present ----------------------------------------------
    elif (not files) and src_dir and any(p.startswith(src_dir+'/') for p in head_path2blob):
        row['resolution']='D:SOURCE_DIR-BASENAME'
        for n,content in zsha.items():
            if not n.endswith('.py'): continue
            cands=[p for p in base2paths.get(os.path.basename(n),[]) if p.startswith(src_dir+'/')]
            m={'file':n,'zip_member':n}
            if not cands: m['verdict']='NO-HEAD-SOURCE'; verdicts.append('NOSRC'); row['members'].append(m); continue
            resolved_members.add(n); verdicts.append(member_verdict(m,cands[0],content)); row['members'].append(m)
    # ---- E. default source_dir + files[] ---------------------------------------------------------
    elif src_dir and src_dir!='EXTERNAL' and files:
        row['resolution']='E:SOURCE_DIR+FILES'
        for f in files:
            m={'file':f}; rel=f
            if rel not in zsha:
                alt=[n for n in zsha if os.path.basename(n)==os.path.basename(rel)]
                if alt: rel=alt[0]; m['note']='matched-by-basename'
                else: m['zip_member']=None; m['verdict']='MISSING-IN-PACKAGE'; verdicts.append('MISSING'); row['members'].append(m); continue
            m['zip_member']=rel; resolved_members.add(rel)
            verdicts.append(member_verdict(m,f"{src_dir}/{f}",zsha[rel])); row['members'].append(m)
    else:
        row['resolution']='NONE'
        row['class']='UNREAD'; row['subkind']='NO-REPO-SOURCE'
        row['evidence'].append(f"package read ({len(zsha)} members) but NO built-from source in repo (source_dir={src_dir!r}, files={files})")
        F(name,'own-tree','UNREAD','NO-REPO-SOURCE',row['evidence'][-1]); rows.append(row); continue
    # extra top-level .py not resolved
    for n in zsha:
        if n.endswith('.py') and '/' not in n and n not in resolved_members and n not in ('__init__.py',): row['extra_py_members'].append(n)
    # ---- bundled-copy axis (collision-filtered) --------------------------------------------------
    pkg_dirs={n.split('/')[0] for n in zsha if '/' in n}
    vendored_dirs={d for d in pkg_dirs if (f'{d}/__init__.py' in zsha or any(n.startswith(d+'/') and n.endswith('.dist-info/METADATA') for n in zsha)) and not any(p.startswith(f'{src_dir}/{d}/') for p in head_path2blob)}
    for n,content in zsha.items():
        if not n.endswith('.py'): continue
        if '/' in n and n.split('/')[0] in vendored_dirs: continue
        bn=os.path.basename(n)
        if bn in SKIP_BASENAMES: continue
        for h in base2paths.get(bn,[]):
            if not CANON_RE.match(h) or (src_dir and h.startswith(src_dir+'/')): continue
            hc=blob_bytes(head_path2blob[h]); s=sim(content,hc)
            brp=f"{src_dir}/{n}"; brb=head_path2blob.get(brp)
            b_eq=(norm(blob_bytes(brb))==norm(hc)) if brb else None
            d_eq=(norm(hc)==norm(content))
            th={'member':n,'bundled_repo_path':brp if brb else None,'canonical_path':h,'deployed_eq_canonical':d_eq,'bundled_repo_eq_canonical':b_eq,'similarity_deployed_vs_canonical':s,
                'canonical_head_commit':commit_subj(path_history(h)[0][0]) if path_history(h) else None}
            if not d_eq and h.endswith('.py'):
                th['cosmetic_only']=cosmetic_only(hc.decode('utf-8','replace'),content.decode('utf-8','replace'))
            # a real bundled-copy relationship: same logical file (similarity>=0.5) OR the source dir carries a same-named copy
            th['relationship']='BUNDLED-COPY' if (brb is not None or (s or 0)>=0.5) else 'NAME-COLLISION'
            row['two_homes'].append(th)
    # ---- classify own-tree ------------------------------------------------------------------
    hc_=row['held_candidates']
    vset=set(verdicts)
    MAP_STATED_HOLDS={'finbert-batch-processor':'source-map _note "Code managed outside TF (placeholder + ignore_changes)" -- adopted into TF 2026-08-04 with lifecycle ignore_changes on code'}
    if not verdicts: cls,sub='UNREAD','NO-MEMBER-VERDICTS'
    elif vset<={'CURRENT'}: cls,sub='CURRENT',None
    elif vset<={'CURRENT','COSMETIC'}: cls,sub='DELIBERATELY-HELD','COSMETIC-ONLY-DRIFT (AST-identical after docstring/comment strip; precedent COO 08-18 ~1355Z @d5d7342da4: no deploy off a docstring)'
    elif 'HELD-STATED' in vset and not (vset & {'WRONGDIR','AHEAD-WT','UNATTRIBUTED'}): cls,sub='DELIBERATELY-HELD','STATED-IN-COMMIT-MESSAGE (a commit after the deployed vintage declares the hold; cited in the member row)'
    elif name in MAP_STATED_HOLDS: cls,sub='DELIBERATELY-HELD','STATED-IN-SOURCE-MAP: '+MAP_STATED_HOLDS[name]
    elif 'CHAIN-BROKEN' in vset: cls,sub='UNREAD','TRANSFORMED-BUILD-PROVENANCE-BROKEN'
    elif vset & {'WRONGDIR'}: cls,sub='TWO-HOMES-DIVERGED','DEPLOYED-BYTES-LIVE-AT-ANOTHER-REPO-PATH (map source_dir is not the built-from dir)'
    elif vset & {'AHEAD-WT'}: cls,sub='TWO-HOMES-DIVERGED','DEPLOY-AHEAD-OF-REPO (deployed == uncommitted working-tree bytes; git never had them)'
    elif vset & {'UNATTRIBUTED'}: cls,sub='TWO-HOMES-DIVERGED','DEPLOYED-BYTES-NOT-IN-REPO-HISTORY (deploy home and git home diverged, ancestry unknown)'
    elif 'MISSING' in vset: cls,sub='STALE-BY-NEGLECT','COMMITTED-NEVER-DEPLOYED (files[] member absent from package)'
    elif vset & {'OLDER'}: cls,sub='STALE-BY-NEGLECT','DEPLOYED-OLDER-THAN-BUILT-FROM (code-level delta)'
    elif vset & {'STRINGS'}: cls,sub='STALE-BY-NEGLECT','DEPLOYED-OLDER-THAN-BUILT-FROM (STRING-LITERALS-ONLY delta -- paths/log text, e.g. the 06-11 provenance sweep @46d0b98aef; internally coherent older vintage)'
    elif vset & {'NOSRC'}: cls,sub='TWO-HOMES-DIVERGED','DEPLOYED-MEMBER-ABSENT-FROM-REPO (package carries a file git never had at that path)'
    else: cls,sub='UNREAD','UNCLASSIFIED:'+','.join(sorted(vset))
    row['own_tree_class']=cls; row['own_tree_subkind']=sub
    row['class']=cls; row['subkind']=sub
    if cls!='CURRENT':
        F(name,'own-tree',cls,sub,'; '.join(f"{m['file']}={m.get('verdict')}"+(f" (deployed@{m['deployed_commit'][:7]} vs head@{(m.get('head_commit_for_path') or '')[:7]}, {m.get('commits_since_deployed')} behind; delta={'cosmetic' if m.get('cosmetic_only') else ('strings-only' if m.get('strings_only') else 'code')}"+(f"; HOLD: {m['hold_statements_in_commits'][0][:170]}" if m.get('hold_statements_in_commits') else '')+")" if m.get('deployed_commit') else '') for m in row['members'] if not str(m.get('verdict','')).startswith('CURRENT')))
    # two-homes overlay: BUNDLED-COPY rows that diverge
    div=[t for t in row['two_homes'] if t['relationship']=='BUNDLED-COPY' and (t['deployed_eq_canonical'] is False or t['bundled_repo_eq_canonical'] is False)]
    if div:
        ev='; '.join(f"{t['member']} vs {t['canonical_path']} (deployed==canonical:{t['deployed_eq_canonical']}, source_dir-copy==canonical:{t['bundled_repo_eq_canonical']}, sim={t['similarity_deployed_vs_canonical']}, cosmetic_only={t.get('cosmetic_only')})" for t in div)
        F(name,'bundled-vs-canonical','TWO-HOMES-DIVERGED','BUNDLED-COPY-DIVERGED-FROM-CANONICAL',ev)
        if cls=='CURRENT':
            row['class']='TWO-HOMES-DIVERGED'; row['subkind']='BUNDLED-COPY-DIVERGED-FROM-CANONICAL (byte-identical to its OWN tree; the second home moved)'
        else:
            row['also_two_homes']=True
    rows.append(row)

summary=collections.Counter(r['class'] for r in rows)
fsum=collections.Counter((f['axis'],f['class']) for f in findings)
json.dump(rows,open(os.path.join(OUT,'lambda_census_v3_rows.json'),'w'),indent=1,default=str)
json.dump(findings,open(os.path.join(OUT,'lambda_census_v3_findings.json'),'w'),indent=1,default=str)
json.dump({'HEAD':HEAD,'N_map':len(names),'live_total':len(live),'in_map_live':len(in_map_live),'in_map_notlive':in_map_notlive,'live_not_in_map':live_not_in_map,
           'summary_per_lambda':dict(summary),'findings_per_axis_class':{f"{a}|{c}":n for (a,c),n in fsum.items()}},open(os.path.join(OUT,'lambda_census_v3_summary.json'),'w'),indent=1)
print("PER-LAMBDA:",dict(summary)); print("FINDINGS:",dict(fsum)); print("live NOT in map:",live_not_in_map)
```

## ec2_census_v2.py

```python
"""NFRA_DEPLOYCENSUS -- EC2 half. STAGED (S3 object) vs REPO source, and ON-BOX (SSM sha256) vs STAGED.
Rule 22a: staged is DESIRED, executing is APPLIED. Read-only: list/get objects, describe, SSM read-only commands
(sha256sum / Get-FileHash). No instance is started. Classify only.
"""
from __future__ import annotations
import boto3, json, hashlib, subprocess, os, re, time, collections
S=os.path.dirname(os.path.abspath(__file__))
WS=subprocess.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip()
HEAD=subprocess.run(['git','-C',WS,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
man=json.load(open(os.path.join(WS,'infra/aws/ec2/EC2_MANIFEST.json'),encoding='utf-8'))['services']
state=json.load(open(os.path.join(S,'ec2_state.json')))
s3=boto3.client('s3',region_name='us-east-1'); ssm=boto3.client('ssm',region_name='us-east-1')

def sha256(b): return hashlib.sha256(b).hexdigest()
def blobsha(b): return hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
def norm(b): return b.replace(b'\r\n',b'\n')
def git(*a,binary=False):
    r=subprocess.run(['git','-C',WS]+list(a),capture_output=True); return r.stdout if binary else r.stdout.decode('utf-8','replace')
head_path2blob={}; base2paths=collections.defaultdict(list)
for rec in git('ls-tree','-r','-z','HEAD',binary=True).split(b'\0'):
    if not rec: continue
    meta,path=rec.split(b'\t',1); sha=meta.decode().split(' ')[2]; p=path.decode('utf-8','replace')
    head_path2blob[p]=sha; base2paths[os.path.basename(p)].append(p)
_bc={}
def blob_bytes(sha):
    if sha not in _bc: _bc[sha]=git('cat-file','blob',sha,binary=True)
    return _bc[sha]
_hist={}
def path_history(path,limit=300):
    if path in _hist: return _hist[path]
    out=[]
    for c in git('log','--format=%H','-n',str(limit),'--',path).split():
        t=git('ls-tree',c,'--',path).strip()
        if t: out.append((c,t.split()[2]))
    _hist[path]=out; return out
def csubj(c): return git('show','-s','--format=%h %ci %an %s',c).strip()[:110]

CODE_EXT=('.py','.sh','.ps1','.mjs','.js','.json','.yaml','.yml','.service','.txt','.cfg','.toml','.html','.css')
def is_code(k): return k.lower().endswith(CODE_EXT)

def compare_bytes(content, repo_path):
    """Return (verdict, detail) comparing content to HEAD:repo_path."""
    hb=head_path2blob.get(repo_path)
    if hb is None: return 'NO-HEAD-SOURCE',{}
    hc=blob_bytes(hb)
    if blobsha(content)==hb or norm(hc)==norm(content): return 'CURRENT',{}
    hist=path_history(repo_path); dep=blobsha(content)
    hit=[c for c,b in hist if b==dep or norm(blob_bytes(b))==norm(content)]
    if hit:
        idx=[c for c,_ in hist].index(hit[0])
        return 'OLDER',{'staged_commit':csubj(hit[0]),'head_commit':csubj(hist[0][0]),'commits_behind':idx}
    wt=os.path.join(WS,repo_path)
    if os.path.isfile(wt) and norm(open(wt,'rb').read())==norm(content): return 'AHEAD-WT',{'note':'staged == uncommitted working-tree bytes'}
    ob=on_other_ref(content)
    if ob: return 'ON-OTHER-REF',{'note':'staged bytes reachable from another ref (e.g. SITEZ): '+ob,'similarity_vs_head':sim(content,blob_bytes(head_path2blob[repo_path]))}
    return 'UNATTRIBUTED',{'note':'staged bytes not in this path history on any ref','similarity_vs_head':sim(content,blob_bytes(head_path2blob[repo_path]))}

def resolve_repo_path(key, source_path, tree_hint=None):
    """Resolve an S3 key to its repo source: rel path under source_path, else basename within source_path tree,
    else (for code/{tier}/ trees) basename under data/*/scripts. Returns (path, how)."""
    bn=os.path.basename(key)
    if not bn: return None,None
    sp=source_path or ''
    if sp and not sp.endswith('.py'):
        # try progressively shorter suffixes of the key under source_path
        parts=key.split('/')
        for i in range(len(parts)):
            cand=sp.rstrip('/')+'/'+'/'.join(parts[i:])
            if cand in head_path2blob: return cand,'relpath-under-source_path'
        cands=[p for p in base2paths.get(bn,[]) if p.startswith(sp.rstrip('/')+'/')]
        if len(cands)==1: return cands[0],'basename-within-source_path'
        if len(cands)>1:
            # prefer tier match (code/gold/x.py -> .../gold/x.py)
            for c in cands:
                if any(f'/{t}/' in c and f'/{t}/' in '/'+key for t in ('gold','silver','bronze','runner','presentation','lib','_util','serving')): return c,'basename+tier-within-source_path'
            return cands[0],'basename-AMBIGUOUS-within-source_path:'+str(len(cands))
    elif sp and sp in head_path2blob and os.path.basename(sp)==bn: return sp,'exact-file'
    if tree_hint:
        cands=[p for p in base2paths.get(bn,[]) if p.startswith(tree_hint)]
        if len(cands)==1: return cands[0],'basename-within-tree-hint'
        if len(cands)>1:
            for c in cands:
                if any(f'/{t}/' in c and f'/{t}/' in '/'+key for t in ('gold','silver','bronze','runner')): return c,'basename+tier-within-tree-hint'
            return cands[0],'basename-AMBIGUOUS-within-tree-hint:'+str(len(cands))
    # global fallback: canonical trees only
    gcands=[p for p in base2paths.get(bn,[]) if re.match(r'^(data/[^/]+/(?:[^/]+/)?scripts/|lib/|infra/aws/ec2/|tools/)',p) and '/tests/' not in p]
    if len(gcands)==1: return gcands[0],'basename-GLOBAL-canonical'
    if len(gcands)>1:
        for c in gcands:
            if any(f'/{t}/' in c and f'/{t}/' in '/'+key for t in ('gold','silver','bronze','runner')): return c,'basename+tier-GLOBAL:'+str(len(gcands))
        return gcands[0],'basename-AMBIGUOUS-GLOBAL:'+str(len(gcands))
    return None,None

import difflib
def sim(a,b):
    try: return round(difflib.SequenceMatcher(None,a.decode('utf-8','replace'),b.decode('utf-8','replace')).ratio(),3)
    except Exception: return None
def on_other_ref(content):
    dep=blobsha(content)
    r=git('log','--all','--format=%H %D','-n','1','--find-object='+dep)
    line=r.strip().splitlines()[0] if r.strip() else None
    return line[:120] if line else None
def referenced_by(bn):
    r=git('grep','-l','-F',bn,'HEAD','--','infra/aws/ec2','data','tools')
    return [x.split(':',1)[1] for x in r.strip().splitlines() if ':' in x][:4]

# declared staging per service: (s3 uri prefix or object, repo tree hint) -- from the manifest strings + deploy scripts read above
STAGE={
 'consolidation-gold-runner':[('s3://opal-data-assets/code/consolidation-gold/','infra/aws/ec2/consolidation-gold-runner')],
 'orion-crawl-harness':[('s3://opal-313476888478-lambda-artifacts/ec2/crawl-harness/','infra/aws/ec2/crawl-harness')],
 'astn-wsjft-scraper':[('s3://opal-313476888478-lambda-artifacts/ec2/astn-wsjft/','tools/astn_wsjft')],
 'bd-49f-auto-login':[('s3://opal-313476888478-lambda-artifacts/ec2/bd-49f-auto-login/','infra/aws/ec2/bd-49f-auto-login')],
 'etfs-reports-reporter':[('s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/','data/etfs/scripts/presentation')],
 'bd-gold-layer-runner':[('s3://opal-data-bd/code/gold/','data/black_diamond/scripts'),('s3://opal-data-bd/code/silver/','data/black_diamond/scripts'),('s3://opal-data-bd/code/bronze/','data/black_diamond/scripts'),('s3://opal-data-bd/code/runner/','infra/aws/ec2/bd-gold-layer-runner')],
 'bd-gold-qa-runner':[('s3://opal-data-bd/code/runner-qa/','infra/aws/ec2/bd-gold-qa-runner')],
 'bd-allocations':[('s3://opal-data-bd/scripts/src/','infra/aws/ec2/bd-exporter')],
 'bd-transactions':[('s3://opal-data-bd/scripts/src/','infra/aws/ec2/bd-exporter')],
 'bd-fees':[('s3://opal-data-bd/scripts/src/','infra/aws/ec2/bd-exporter')],
 'bd-assets':[('s3://opal-data-bd/scripts/src/','infra/aws/ec2/bd-exporter')],
 'bd-price-runner':[('s3://opal-data-bd/code/silver/bd_price_update.py','data/black_diamond/scripts/silver/bd_price_update.py')],
 'inf-gold-layer-runner':[('s3://opal-data-inf/code/runner/','infra/aws/ec2/inf-gold-layer-runner'),('s3://opal-data-inf/code/gold/','data/inf/scripts'),('s3://opal-data-inf/code/watchdog-shutdown.sh','infra/aws/ec2/inf-gold-layer-runner/watchdog-shutdown.sh')],
 'inf-gold-qa-runner':[('s3://opal-data-inf/code/runner-qa/','infra/aws/ec2/inf-gold-qa-runner')],
 'inf-bronze-runner':[('s3://opal-data-inf/code/bronze-runner/','infra/aws/ec2/inf-bronze-runner')],
 'mdpf-daily-runner':[('s3://opal-data-mdpf/code/','infra/aws/ec2/mdpf-daily-runner')],
 'opal-website-wp':[('s3://opal-website-backups/code/website/','infra/aws/ec2/website')],
 'estate-report-runner':[('s3://opal-estate-report/code/','infra/aws/ec2/estate-report-runner')],
 'opal-gateway':[('s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/','infra/aws/ec2/opal-gateway')],
}
TREE_HINT={'s3://opal-data-bd/code/':'data/black_diamond/scripts/','s3://opal-data-inf/code/gold/':'data/inf/scripts/','s3://opal-data-mdpf/code/scripts/':'data/mdpf/scripts/','s3://opal-data-mdpf/code/':'data/mdpf/'}

def list_objs(uri):
    b,k=uri[5:].split('/',1); out=[]
    if not k.endswith('/'):
        try: h=s3.head_object(Bucket=b,Key=k); return [(b,k,h['ContentLength'],str(h['LastModified']))]
        except Exception as e: return []
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=b,Prefix=k):
        for o in page.get('Contents',[]): out.append((b,o['Key'],o['Size'],str(o['LastModified'])))
    return out

results={}
for svc,ent in man.items():
    st=state[svc]; r={'service':svc,'instance_id':ent.get('instance_id'),'ec2_state':st['ec2_state'],'ssm_ping':(st.get('ssm') or {}).get('ping'),
        'source_path':ent.get('source_path'),'remote_path':ent.get('remote_path'),'deploy_mechanism':ent.get('deploy_mechanism'),'staged':[],'staged_class':None,'onbox_class':None,'evidence':[]}
    stages=STAGE.get(svc)
    if not stages:
        r['staged_class']='UNREAD'; r['evidence'].append('NO DECLARED S3 STAGING in the manifest/deploy notes (deploy_mechanism=%s) -- nothing to read as DESIRED'%ent.get('deploy_mechanism'))
    else:
        total=0; verd=collections.Counter()
        for uri,hint in stages:
            objs=list_objs(uri)
            code=[o for o in objs if is_code(o[1]) and not o[1].endswith('/')]
            r['evidence'].append(f"{uri}: {len(objs)} objects listed (materialised), {len(code)} code-shaped")
            total+=len(code)
            for b,k,sz,lm in code[:400]:
                if sz>5_000_000: continue
                content=s3.get_object(Bucket=b,Key=k)['Body'].read()
                th=None
                for pfx,t in TREE_HINT.items():
                    if uri.startswith(pfx): th=t
                rp,how=resolve_repo_path(k[len(uri[5:].split('/',1)[1]):] if uri.endswith('/') else os.path.basename(k), hint if not hint.endswith('.py') else os.path.dirname(hint), th)
                if hint.endswith('.py'): rp,how=hint,'exact-file'
                if rp is None:
                    v,d='STAGED-ORPHAN',{'referenced_by':referenced_by(os.path.basename(k))}
                else:
                    v,d=compare_bytes(content,rp)
                    if v not in ('CURRENT','OLDER') and how and 'basename' in how:
                        hb2=head_path2blob.get(rp); s2=sim(content,blob_bytes(hb2)) if hb2 else None
                        d['similarity_vs_resolved']=s2
                        if s2 is not None and s2<0.5:
                            v,d='STAGED-ORPHAN',{'note':f'basename match {rp} rejected (similarity {s2}) -- name collision','referenced_by':referenced_by(os.path.basename(k))}
                verd[v]+=1
                r['staged'].append({'key':f"s3://{b}/{k}",'size':sz,'last_modified':lm,'sha256':sha256(content),'repo_path':rp,'resolution':how,'verdict':v,**d})
        r['staged_counts']=dict(verd); r['staged_total_code_objects']=total
        if total==0: r['staged_class']='UNREAD'; r['evidence'].append('declared staging prefix EMPTY / unreadable')
        elif set(verd)<={'CURRENT'}: r['staged_class']='CURRENT'
        elif verd.get('OLDER'): r['staged_class']='STALE-BY-NEGLECT'
        elif verd.get('AHEAD-WT') or verd.get('UNATTRIBUTED') or verd.get('ON-OTHER-REF') or verd.get('NO-HEAD-SOURCE'): r['staged_class']='TWO-HOMES-DIVERGED'
        elif verd.get('STAGED-ORPHAN'): r['staged_class']='STAGED-ORPHAN-ONLY'
        else: r['staged_class']='UNREAD'
    # on-box
    iid=ent.get('instance_id')
    if not iid or str(st['ec2_state']).startswith('ERROR') or st['ec2_state'] is None:
        r['onbox_class']='UNREAD'; r['evidence'].append(f"instance_id={iid} -> {st['ec2_state'] or 'none in manifest'} (manifest points at no/nonexistent instance)")
    elif st['ec2_state']!='running':
        r['onbox_class']='UNREAD'; r['evidence'].append(f"instance {iid} is {st['ec2_state']} (stopped-by-design for transient boxes); not started for a read-only census")
    elif (st.get('ssm') or {}).get('ping')!='Online':
        r['onbox_class']='UNREAD'; r['evidence'].append(f"instance {iid} running but SSM not Online")
    else:
        r['onbox_class']='PENDING-SSM'
    results[svc]=r
    print(f"{svc:28s} staged={str(r['staged_class']):20s} {r.get('staged_counts')} onbox={r['onbox_class']}")

json.dump(results,open(os.path.join(S,'ec2_census_v2_rows.json'),'w'),indent=1,default=str)
print("HEAD",HEAD)
```

## ec2_onbox.py

```python
"""NFRA_DEPLOYCENSUS -- on-box (APPLIED) reads via SSM, read-only (sha256sum / Get-FileHash / ls).
Boxes: the 5 SSM-Online. No starts, no writes, no code execution beyond hashing."""
from __future__ import annotations
import boto3, json, time, os
S=os.path.dirname(os.path.abspath(__file__))
ssm=boto3.client('ssm',region_name='us-east-1')

JOBS={
 'inf-gold-layer-runner':{'iid':'i-0ed5afded2ebd4ed4','doc':'AWS-RunShellScript','cmd':
   'echo ===run-gold-layer; sha256sum /home/ec2-user/run-gold-layer.sh 2>&1; '
   'echo ===watchdog; sha256sum /usr/local/bin/watchdog-shutdown.sh 2>&1; '
   'echo ===dispatch; sha256sum /home/ec2-user/orion-gold-dispatch.sh /home/ec2-user/inf-gold-layer/orion-gold-dispatch.sh 2>&1; '
   'echo ===scripts; find /home/ec2-user/inf-gold-layer -maxdepth 2 -name "*.py" 2>/dev/null | head -5; '
   'find /home/ec2-user -maxdepth 2 -name "*.sh" 2>/dev/null | head; echo ===gold_scripts_hash; '
   'find /home/ec2-user -type d -name scripts 2>/dev/null | head -3'},
 'mdpf-daily-runner':{'iid':'i-02448edb624a7a7cf','doc':'AWS-RunShellScript','cmd':
   'echo ===dispatch; sha256sum /opt/mdpf/mdpf-daily-dispatch.sh 2>&1; '
   'echo ===scripts; cd /opt/mdpf/scripts 2>/dev/null && find . -name "*.py" -o -name "*.json" -o -name "*.yaml" | sort | xargs sha256sum 2>&1 | head -60; '
   'echo ===config; cd /opt/mdpf/config 2>/dev/null && find . -type f | sort | xargs sha256sum 2>&1 | head -20'},
 'opal-gateway':{'iid':'i-07dccb1615503ac99','doc':'AWS-RunShellScript','cmd':
   'echo ===app; cd /opt/opal-gateway 2>/dev/null && find app -name "*.py" | sort | xargs md5sum 2>&1 | head -30; '
   'echo ===sha256; find app -name "*.py" | sort | xargs sha256sum 2>&1 | head -30'},
 'opal-website-wp':{'iid':'i-0152e3fe2599fa630','doc':'AWS-RunShellScript','cmd':
   'echo ===opt; ls /opt/opal/website 2>&1; cd /opt/opal/website 2>/dev/null && find . -maxdepth 2 -name "*.sh" | sort | xargs sha256sum 2>&1 | head -20'},
 'canonical-schwab-si2':{'iid':'i-0f3d57a97f14727af','doc':'AWS-RunPowerShellScript','cmd':
   'Write-Output "===SchwabData"; Get-ChildItem C:\\SchwabData -Filter *.ps1 -ErrorAction SilentlyContinue | ForEach-Object { $h=(Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(); Write-Output "$h  $($_.Name)" }; '
   'Write-Output "===py"; Get-ChildItem C:\\SchwabData -Filter *.py -ErrorAction SilentlyContinue | ForEach-Object { $h=(Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower(); Write-Output "$h  $($_.Name)" }; '
   'Write-Output "===tasks"; schtasks /Query /FO CSV | Select-String -Pattern "Schwab"'},
}
out={}
for svc,j in JOBS.items():
    params={'commands':[j['cmd']]}
    try:
        r=ssm.send_command(InstanceIds=[j['iid']],DocumentName=j['doc'],Parameters=params,Comment='NFRA_DEPLOYCENSUS read-only hash census')
        cid=r['Command']['CommandId']
        for _ in range(40):
            time.sleep(3)
            inv=ssm.get_command_invocation(CommandId=cid,InstanceId=j['iid'])
            if inv['Status'] in ('Success','Failed','Cancelled','TimedOut'): break
        out[svc]={'status':inv['Status'],'stdout':inv.get('StandardOutputContent','')[:8000],'stderr':inv.get('StandardErrorContent','')[:2000]}
        print("==",svc,inv['Status']); print(out[svc]['stdout'][:1500])
    except Exception as e:
        out[svc]={'status':'ERROR','error':str(e)}; print("==",svc,"ERROR",e)
json.dump(out,open(os.path.join(S,'ec2_onbox_raw.json'),'w'),indent=1)
```

