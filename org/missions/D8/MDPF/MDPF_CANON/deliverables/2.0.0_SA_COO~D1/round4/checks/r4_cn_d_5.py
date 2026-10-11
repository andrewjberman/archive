#!/usr/bin/env python3
"""MDPF_CANON round 4 -- issuer checks for cell CN-d-5 (the runner's `code/` equality step).

One subcommand per criterion; every arm prints one `ARM <name>: PASS|FAIL <detail>` line, then
`ROUND 4 <NAME>: k of n arms`; exit 0 only when every arm passes. ASCII only. Terminates well under 120 s.

  tool   5 arms, offline (S3 is a fake; no network): .tools/mdpf-code-equality.py compiles and answers --help; reuses the
         declared code trees and holds no write verb and no typed code prefix; compare_tree() classifies a synthetic
         tree exactly; a named file under no runner tree is REFUSED (exit 2, nothing read); the deploy-step document
         states the order of acts and the sequencing rule.
  live   2 arms, real S3, READ-ONLY: the tool runs against the real trees and prints one TREE line per tree plus its
         summary; its counts for the config tree equal an independent recount made here (md5 against ETag).

  --tool <path>  --doc <path>   the files under test (defaults: .tools/mdpf-code-equality.py and
                                docs/deployment/MDPF_RUNNER_CODE_SYNC.md). The issuer's dry-run passes reference copies.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
DEFAULT_TOOL = os.path.join(ROOT, ".tools", "mdpf-code-equality.py")
DEFAULT_DOC = os.path.join(ROOT, "docs", "deployment", "MDPF_RUNNER_CODE_SYNC.md")
WRITE_ATTRS = frozenset({"put_object", "upload_file", "upload_fileobj", "delete_object", "delete_objects",
                         "copy_object", "copy", "put_object_tagging", "delete_bucket"})
WRITE_SUBCMDS = frozenset({"cp", "sync", "rm", "mv"})


def write_verbs(src: str) -> list:
    """Write verbs a script CALLS: boto3 write methods, a string that starts `aws s3 `/`aws s3api `, an argv list
    holding "s3" then cp|sync|rm|mv. Comments, docstrings and regex text that merely NAME a command are not calls."""
    out = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return ["unparseable"]
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute) and n.attr in WRITE_ATTRS:
            out.add(n.attr)
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.startswith(("aws s3 ", "aws s3api ")):
            out.add(n.value[:20])
        if isinstance(n, (ast.List, ast.Tuple)):
            vals = [e.value for e in n.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            for a, b in zip(vals, vals[1:]):
                if a == "s3" and b in WRITE_SUBCMDS:
                    out.add("s3 " + b)
    return sorted(out)


CODE_PREFIX_LITERAL = re.compile(r"""["']code/(scripts|config)""")
BUCKET = "opal-data-mdpf"


def _run(args, timeout=100):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, timeout=timeout, cwd=ROOT)


class _Pg:
    def __init__(self, objs):
        self.objs = objs

    def paginate(self, **kw):
        pre = kw.get("Prefix", "")
        return [{"Contents": [{"Key": k, "ETag": '"%s"' % e} for k, e in self.objs.items() if k.startswith(pre)]}]


class _FakeS3:
    def __init__(self, objs):
        self.objs = objs

    def get_paginator(self, _name):
        return _Pg(self.objs)


def _md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()


def arms_tool(tool: str, doc: str):
    arms = []
    # 1 compiles and answers --help
    r1 = subprocess.run([sys.executable, "-m", "py_compile", tool], capture_output=True, text=True)
    r2 = _run([tool, "--help"]) if r1.returncode == 0 else None
    ok = r1.returncode == 0 and r2 is not None and r2.returncode == 0 and "--files" in r2.stdout
    arms.append(("COMPILES-HELP", ok, "py_compile rc=%s; --help rc=%s" % (r1.returncode, getattr(r2, "returncode", "n/a"))))
    # 2 reuses the declaration, read-only, no typed code prefix
    src = open(tool, encoding="utf-8").read() if os.path.exists(tool) else ""
    probs = []
    if "CODE_TREES" not in src:
        probs.append("does not read safe_deploy_core.CODE_TREES")
    w = write_verbs(src)
    if w:
        probs.append("write verb(s) present: %s" % w)
    if CODE_PREFIX_LITERAL.search(src):
        probs.append("a typed code/ prefix literal is present")
    arms.append(("REUSE-READONLY", not probs and bool(src), "; ".join(probs) or "reads CODE_TREES, no write verb, no typed code prefix"))
    # 3 compare_tree on a synthetic tree and a fake S3
    try:
        for p in (os.path.join(ROOT, ".tools"),):
            if p not in sys.path:
                sys.path.insert(0, p)
        spec = importlib.util.spec_from_file_location("eq_under_test", tool)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as td:
            files = {"same.py": b"a=1\n", "diff.py": b"b=2\n", "gone.py": b"c=3\n", "multi.py": b"d=4\n", "sub/n.json": b"{}\n"}
            for rel, body in files.items():
                path = os.path.join(td, *rel.split("/"))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(body)
            os.makedirs(os.path.join(td, "__pycache__"), exist_ok=True)
            with open(os.path.join(td, "__pycache__", "x.pyc"), "wb") as fh:
                fh.write(b"x")
            pre = "code/scripts/gold/"
            objs = {pre + "same.py": _md5(files["same.py"]), pre + "diff.py": _md5(b"OTHER"),
                    pre + "multi.py": _md5(files["multi.py"]) + "-3", pre + "sub/n.json": _md5(files["sub/n.json"]),
                    pre + "extra.py": _md5(b"z"), "code/scripts/other/outside.py": _md5(b"q")}
            res = mod.compare_tree(td, BUCKET, pre, _FakeS3(objs))
        want = {"equal": ["same.py", "sub/n.json"], "differ": ["diff.py"], "missing_on_s3": ["gone.py"],
                "extra_on_s3": ["extra.py"], "undetermined": ["multi.py"]}
        got = {k: sorted(res.get(k, [])) for k in want}
        ok = got == want and res.get("local") == 5
        arms.append(("CLASSIFIES", ok, "local=%s %s" % (res.get("local"), "exact" if ok else "got %r" % (got,))))
    except Exception as exc:  # noqa: BLE001
        arms.append(("CLASSIFIES", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    # 4 refuses a name under no tree before reading anything
    r4 = _run([tool, "--files", "docs/README_NOT_A_RUNNER_FILE.md"]) if os.path.exists(tool) else None
    ok4 = r4 is not None and r4.returncode == 2 and "REFUSED" in (r4.stdout + r4.stderr)
    arms.append(("REFUSES-UNMAPPED", ok4, "rc=%s" % getattr(r4, "returncode", "n/a")))
    # 5 the document states the act and the sequencing
    d = open(doc, encoding="utf-8").read() if os.path.exists(doc) else ""
    need = ["## ORDER OF ACTS", "## SEQUENCING", "mdpf-code-equality.py --files", "Named files only", "No scheduled sync job"]
    miss = [n for n in need if n not in d]
    arms.append(("DOC", bool(d) and not miss, "missing markers: %s" % miss if (miss or not d) else "all 5 markers present"))
    return arms


def arms_live(tool: str):
    arms = []
    try:
        r = _run([tool], timeout=110)
    except subprocess.TimeoutExpired:
        return [("LIVE-RUN", False, "timeout after 110 s"), ("RECOUNT", False, "not reached")]
    trees = [ln for ln in r.stdout.splitlines() if ln.startswith("TREE ")]
    summ = [ln for ln in r.stdout.splitlines() if ln.startswith("MDPF-CODE-EQUALITY:")]
    arms.append(("LIVE-RUN", r.returncode == 0 and len(trees) >= 5 and len(summ) == 1,
                 "rc=%s trees=%d summary_lines=%d" % (r.returncode, len(trees), len(summ))))
    cfg = [ln for ln in trees if ln.startswith("TREE data/mdpf/config ->")]
    if not cfg:
        arms.append(("RECOUNT", False, "no TREE line for data/mdpf/config"))
        return arms
    try:
        import boto3
        s3 = boto3.client("s3", region_name="us-east-1")
        home = os.path.join(ROOT, "data", "mdpf", "config")
        local = {}
        for root, dirs, files in os.walk(home):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in files:
                if not f.endswith(".pyc"):
                    p = os.path.join(root, f)
                    local[os.path.relpath(p, home).replace(os.sep, "/")] = hashlib.md5(open(p, "rb").read()).hexdigest()
        remote = {}
        for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="code/config/"):
            for o in pg.get("Contents", []):
                remote[o["Key"][len("code/config/"):]] = o["ETag"].strip('"')
        eq = sum(1 for k, v in local.items() if remote.get(k) == v and "-" not in v)
        mi = sum(1 for k in local if k not in remote)
        ex = sum(1 for k in remote if k not in local)
        line = cfg[0]
        got = {k: int(re.search(k + r" (\d+)", line).group(1)) for k in ("local", "EQUAL", "MISSING_ON_S3", "EXTRA_ON_S3")}
        want = {"local": len(local), "EQUAL": eq, "MISSING_ON_S3": mi, "EXTRA_ON_S3": ex}
        arms.append(("RECOUNT", got == want, "tool %r vs independent %r" % (got, want)))
    except Exception as exc:  # noqa: BLE001
        arms.append(("RECOUNT", False, "%s: %s" % (type(exc).__name__, str(exc)[:160])))
    return arms


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("tool", "live"))
    ap.add_argument("--tool", default=DEFAULT_TOOL)
    ap.add_argument("--doc", default=DEFAULT_DOC)
    a = ap.parse_args(argv)
    arms = arms_tool(a.tool, a.doc) if a.cmd == "tool" else arms_live(a.tool)
    for name, ok, detail in arms:
        print("ARM %s: %s %s" % (name, "PASS" if ok else "FAIL", detail))
    n_ok = sum(1 for _n, ok, _d in arms if ok)
    print("ROUND 4 %s: %d of %d arms" % (a.cmd.upper(), n_ok, len(arms)))
    return 0 if n_ok == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
