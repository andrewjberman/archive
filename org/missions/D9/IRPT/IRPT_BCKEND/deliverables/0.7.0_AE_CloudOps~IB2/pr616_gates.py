"""IRPT_BCKEND TO-IB-pr-616 step 1, READ ONLY: the signed bytes, the hop 2 ledger, the worktree union of .open_deploys, the live BEFORE state. Counts, hashes and words only.

  python pr616_gates.py
"""
import glob
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import boto3

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
B = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
DOCS = {
    "pair COO half": (B + "2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_COO_HALF.md", "9a036bf61794d7eb3be2fc4def3b3b442dc4c761"),
    "addendum 1 doc": (B + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_1_EXPORT_FILLED_READ_GRANT_DRAFT.md", "9462b5ad35af646c96ede013f03d4449e8815033"),
    "addendum 1 COO half": (B + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_1_COO_HALF.md", "a09b331c4153cba7aea872001ed7998145d0e984"),
    "addendum 2 COO half": (B + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_2_FENCE_ROW_COO_HALF.md", "b5c303ea69ffa4195ec441d455d9f1978c327678"),
}
PACKET = (B + "0.9.0_WK_IRPT_BCKEND~395/SERVE_PATH_PAIR_PACKET_V1.md", "7daa29f0fe10")
CTO = B + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_CTO_HALF.md"
HOP2 = "irpt-dashbd-49f-publish-hop2-reader-readgrant-20261016"
NAMED = re.compile(r"irpt-49f-reporting-read-lambda|irpt-export-render|reporting-read|export-render-role|reporting_read", re.I)
rc = 0


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT)).stdout


for name, (p, want) in DOCS.items():
    got = git("hash-object", p).strip()
    print("BYTES %s blob_equal=%s" % (name, got == want))
    rc |= got != want
sha = hashlib.sha256((ROOT / PACKET[0]).read_bytes()).hexdigest()
print("BYTES packet sha256 prefix equal=%s" % sha.startswith(PACKET[1]))
cto = (ROOT / CTO).read_text(encoding="utf-8")
print("CTO half SIGNED mentions: pair=%s addendum1(9462b5ad35af)=%s addendum2(b5c303ea69ff)=%s" % ("SIGNED" in cto, "9462b5ad35af" in cto, "b5c303ea69ff" in cto))
led = list((ROOT / "org/critical_paths/change_management").glob("*_%s_deploy_completion.md" % HOP2))
print("HOP2 ledger: %s" % ((led[0].read_text(encoding="utf-8", errors="replace")[:600].split("**Status:**")[1].split("\n")[0].strip()[:60]) if led else "NO FILE"))
wts = [ln[9:] for ln in git("worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
files, named = 0, {}
for wt in wts:
    for n in [x for x in git("-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
        files += 1
        if NAMED.search(git("-C", wt, "show", "HEAD:" + n)):
            named.setdefault(Path(n).stem, []).append(wt)
real = []
for slug, locs in named.items():
    f = glob.glob(str(ROOT / ("org/critical_paths/change_management/*_%s_deploy_completion.md" % slug)))
    head = open(f[0], encoding="utf-8", errors="replace").read(1500) if f else ""
    st = "CLOSED" if "**Status:** CLOSED" in head else ("ROLLED-BACK" if "**Status:** ROLLED-BACK" in head else "NOT-CLOSED")
    print("NAMED marker %s in %d worktree(s): ledger %s" % (slug, len(locs), st))
    if st == "NOT-CLOSED":
        real.append(slug)
print("CENSUS worktrees_read=%d marker_files_read=%d named_slugs=%d real_not_closed=%d %s" % (len(wts), files, len(named), len(real), real))
lam = boto3.client("lambda", region_name="us-east-1")
for fn, want in (("irpt-49f-reporting-read-lambda", "WjnDxvu2biEPXcwuF8oXJWRUqFaeUY550xnRxa2daa0="), ("irpt-export-render", "5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4=")):
    got = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
    print("BEFORE %s CodeSha256 equal=%s %s" % (fn, got == want, got))
    rc |= got != want
sys.exit(1 if (rc or real) else 0)
