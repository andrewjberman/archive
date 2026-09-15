"""DEPLOYED_VS_SOURCE_A1 -- POSN_AGGFIX.TO-A1-1, cell AF1-s-5 (C-NEVER-WIDEN). READ-ONLY.

The running yang-generate-positioning against its build input: get-function-configuration
(CodeSha256, LastModified); the function's own code location fetched to <worktree>/.scratch/
and unzipped, its sha256 checked against CodeSha256 (the fetched bundle IS the running code);
sha256 of the bundle's lambda_function.py against the same file at the last_deployed_commit
that infra/aws/lambda/ci/lambda-source-map.json records, and against HEAD; the diff stat
against HEAD; and every commit between last_deployed_commit and HEAD on the function's
directory. Author 0.9.0_WK_POSN_AGGFIX~1. Nothing is deployed or written outside .scratch/.
"""
import base64
import difflib
import hashlib
import io
import json
import os
import subprocess
import sys
import urllib.request
import zipfile

import boto3

FN = "yang-generate-positioning"
HERE = os.path.dirname(os.path.abspath(__file__))
TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()


def git(*args, text=True):
    r = subprocess.run(["git", *args], cwd=TOP, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"ERROR: git {' '.join(args)} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace')[:300]}")
    return r.stdout.decode("utf-8") if text else r.stdout


ROOT = git("rev-parse", "--show-toplevel").strip()
HEAD = git("rev-parse", "HEAD").strip()
SMAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"

lam = boto3.client("lambda", region_name="us-east-1")
cfg = lam.get_function_configuration(FunctionName=FN)
print("== DEPLOYED (get-function-configuration) ==")
for k in ("FunctionName", "CodeSha256", "LastModified", "CodeSize", "Runtime", "Handler", "Version", "RevisionId"):
    print(f"{k:<14} {cfg.get(k)}")

fn = lam.get_function(FunctionName=FN)
code = fn["Code"]
print(f"Code.RepositoryType {code.get('RepositoryType')}  (Location is a presigned URL; not printed)")
data = urllib.request.urlopen(code["Location"], timeout=120).read()
bundle_b64 = base64.b64encode(hashlib.sha256(data).digest()).decode()
print(f"fetched bundle {len(data)} B  sha256(b64) {bundle_b64}  "
      f"{'== CodeSha256 (the fetched bundle IS the running code)' if bundle_b64 == cfg['CodeSha256'] else '!= CodeSha256 -- the fetched bundle is NOT the running code'}")
scratch = os.path.join(ROOT, ".scratch", "a1_deployed")
os.makedirs(scratch, exist_ok=True)
with open(os.path.join(scratch, f"{FN}.zip"), "wb") as fh:
    fh.write(data)
zf = zipfile.ZipFile(io.BytesIO(data))
zf.extractall(os.path.join(scratch, "unzipped"))
names = zf.namelist()
print(f"unzipped to {os.path.relpath(os.path.join(scratch, 'unzipped'), ROOT)}: {len(names)} members -> {names}")

smap = json.loads(git("show", f"HEAD:{SMAP_REL}"))
ent = smap["functions"][FN]
ldc = ent["last_deployed_commit"]
src_dir = ent["source_dir"]
print()
print(f"== SOURCE MAP ({SMAP_REL} @ HEAD {HEAD[:10]}) ==")
for k in ("source_dir", "files", "last_deployed_commit", "last_deployed_at", "artifact_s3_key", "artifact_sha256", "recorded_by"):
    print(f"{k:<22} {ent.get(k)}")
print(f"artifact_sha256 {'==' if ent.get('artifact_sha256') == cfg['CodeSha256'] else '!='} deployed CodeSha256")
anc = subprocess.run(["git", "merge-base", "--is-ancestor", ldc, "HEAD"], cwd=TOP).returncode
pos = subprocess.run(["git", "merge-base", "--is-ancestor", "HEAD~1", "HEAD"], cwd=TOP).returncode
print(f"last_deployed_commit is ancestor of HEAD: {'YES' if anc == 0 else 'NO'} (positive control HEAD~1: {'YES' if pos == 0 else 'NO'})")
sitez = subprocess.run(["git", "rev-parse", "SITEZ"], cwd=TOP, capture_output=True, text=True)
print(f"HEAD {HEAD}; local ref SITEZ {sitez.stdout.strip() if sitez.returncode == 0 else 'UNRESOLVED'}")


def sha(b):
    return hashlib.sha256(b).hexdigest()


print()
print("== FILE BYTES ==")
blocking = False
dep_lf = None
head_lf = None
for f in ent["files"]:
    member = [n for n in names if n == f or n.endswith("/" + f)]
    dep = zf.read(member[0]) if member else None
    at_ldc = git("show", f"{ldc}:{src_dir}/{f}", text=False)
    at_head = git("show", f"HEAD:{src_dir}/{f}", text=False)
    d, l_, h = (sha(dep) if dep is not None else None), sha(at_ldc), sha(at_head)
    eq_ldc = d == l_
    print(f"{f}")
    print(f"  deployed bundle        sha256 {d}  ({'absent' if dep is None else str(len(dep)) + ' B'})")
    print(f"  @last_deployed_commit  sha256 {l_}  ({len(at_ldc)} B)  {ldc[:10]}")
    print(f"  @HEAD                  sha256 {h}  ({len(at_head)} B)  {HEAD[:10]}")
    print(f"  deployed vs last_deployed_commit: {'EQUAL' if eq_ldc else 'DIFFERENT'}")
    if dep is not None and not eq_ldc:
        norm = dep.replace(b"\r\n", b"\n") == at_ldc.replace(b"\r\n", b"\n")
        print(f"    after CRLF->LF normalisation: {'EQUAL' if norm else 'DIFFERENT'}")
    print(f"  deployed vs HEAD: {'EQUAL' if d == h else 'DIFFERENT'}")
    if f == "lambda_function.py":
        blocking = not eq_ldc
        dep_lf, head_lf = dep, at_head

print()
print("== lambda_function.py: last_deployed_commit -> HEAD ==")
print(git("diff", "--stat", ldc, "HEAD", "--", f"{src_dir}/lambda_function.py").rstrip() or "(no diff)")
if dep_lf is not None:
    a = dep_lf.decode("utf-8", "replace").splitlines()
    b = head_lf.decode("utf-8", "replace").splitlines()
    plus = minus = 0
    for ln in difflib.unified_diff(a, b, lineterm="", n=0):
        if ln.startswith("+") and not ln.startswith("+++"):
            plus += 1
        elif ln.startswith("-") and not ln.startswith("---"):
            minus += 1
    print(f"deployed bytes vs HEAD (difflib, same file): +{plus} -{minus} lines")

print()
print(f"== COMMITS {ldc[:10]}..HEAD on {src_dir}/ ==")
log = git("log", "--oneline", f"{ldc}..HEAD", "--", f"{src_dir}/").rstrip()
lines = [ln for ln in log.splitlines() if ln.strip()]
for ln in lines:
    print(ln[:220])
print(f"COMMIT COUNT {len(lines)}")
print()
if sitez.returncode == 0:
    sz = sitez.stdout.strip()
    print(f"== SITEZ ARM (local ref SITEZ {sz[:10]}; HEAD is this worktree's cut base {HEAD[:10]}) ==")
    at_sz = git("show", f"{sz}:{src_dir}/lambda_function.py", text=False)
    print(f"lambda_function.py @SITEZ sha256 {sha(at_sz)} -> deployed vs SITEZ: {'EQUAL' if dep_lf is not None and sha(dep_lf) == sha(at_sz) else 'DIFFERENT'}")
    print(git("diff", "--stat", ldc, sz, "--", f"{src_dir}/").rstrip() or "(no diff on the function directory last_deployed_commit..SITEZ)")
    szl = [ln for ln in git("log", "--oneline", f"{ldc}..{sz}", "--", f"{src_dir}/").splitlines() if ln.strip()]
    for ln in szl:
        print(ln[:220])
    print(f"COMMIT COUNT last_deployed_commit..SITEZ {len(szl)}")
    ctl = [ln for ln in git("log", "--oneline", "-3", ldc, "--", f"{src_dir}/").splitlines() if ln.strip()]
    print(f"CONTROL git log on the same pathspec at last_deployed_commit returns {len(ctl)} line(s) (the pathspec resolves): {ctl[:1]}")
print()
print("VERDICT deployed lambda_function.py vs last_deployed_commit: " + ("DIFFERENT -- BLOCKING row" if blocking else "EQUAL"))
sys.exit(0)
