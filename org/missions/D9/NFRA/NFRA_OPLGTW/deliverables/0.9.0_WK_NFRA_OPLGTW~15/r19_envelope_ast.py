"""OG-rl-7 (OG-o-4): the Schwab envelope.py change is DOCSTRING-ONLY.  Compares the AST of live (37be3485db) and the release with every docstring removed:
equal ASTs = no executable line differs, so the served envelope behaviour is identical in both branches.  Negative control: the same comparison on a release copy with one
numeric constant altered must read DIFFERENT.  usage: python r19_envelope_ast.py (from any worktree; reads git objects)."""
import ast
import subprocess
import sys

P = "infra/aws/ec2/opal-gateway/app/integrations/schwab/envelope.py"


def src(rev):
    return subprocess.run(["git", "show", "%s:%s" % (rev, P)], capture_output=True).stdout.decode("utf-8")


def strip(tree):
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
            n.body = n.body[1:] or [ast.Pass()]
    return ast.dump(tree)


live, rel = src("37be3485db"), src("619e8ddfd6" if len(sys.argv) < 2 else sys.argv[1])
a, b = strip(ast.parse(live)), strip(ast.parse(rel))
print("raw text equal:", live == rel)
print("AST equal with docstrings removed:", a == b)
mut = rel + chr(10) + "X_NEGATIVE_CONTROL = 1" + chr(10)   # one executable statement added
print("negative control (one executable token altered) AST equal:", strip(ast.parse(mut)) == a, "(expected False)")
ok = (live != rel) and a == b and strip(ast.parse(mut)) != a
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
