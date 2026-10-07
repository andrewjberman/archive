#!/usr/bin/env python3
"""check_canon_patch.py -- prove canon_fourth_verdict.patch on COPIES (LGIC_BLANKFIX.TO-BF-e-5).

Copies the renderer, the schema, the registry, the canon and GRADING_RULE.md into two temporary trees, applies the
patch to one with `git apply`, runs the renderer's own `--write` entry in both, and checks:
  - the patched section carries the NO-SYSTEM-ASKED verdict sentence from the schema;
  - the unpatched section does not (the difference control);
  - `git apply --check` of the patch succeeds against the files as HEAD carries them.
Reads the repository, writes only under the system temp directory. Last line is the verdict line.
"""
import difflib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATCH = HERE / "canon_fourth_verdict.patch"
VERDICT = "NO-SYSTEM-ASKED"
RENDERER = "infra/logic/render_naming_section.py"
CANON = "infra/logic/02_DOCTRINE.md"
REGISTRY = "infra/logic/registry/scopes.json"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
RULE = "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md"
FILES = (RENDERER, CANON, REGISTRY, SCHEMA, RULE)
BEGIN = "<!-- BEGIN GENERATED NAMING SECTION -->"
END = "<!-- END GENERATED NAMING SECTION -->"


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def repo_root():
    rc, out = run(["git", "rev-parse", "--show-toplevel"], HERE)
    if rc != 0:
        raise SystemExit("ERROR: not in a git work tree: %s" % out)
    return Path(out.strip())


def git_show(root, path):
    p = subprocess.run(["git", "show", "HEAD:" + path], cwd=str(root), stdout=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("ERROR: git show HEAD:%s rc=%d" % (path, p.returncode))
    return p.stdout


def build_tree(dest, root, patch=False):
    """Copy the five files (the working tree's bytes) under dest, optionally patch them."""
    for rel in FILES:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(root / rel), str(target))
    if patch:
        rc, out = run(["git", "apply", "--whitespace=nowarn", str(PATCH)], dest)
        return rc, out
    return 0, ""


def render(tree):
    rc, out = run([sys.executable, str(tree / RENDERER), "--write"], tree)
    text = (tree / CANON).read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    a, b = text.index(BEGIN), text.index(END)
    return rc, out, text, text[a:b + len(END)]


def main():
    root = repo_root()
    schema = json.loads((root / SCHEMA).read_bytes().decode("utf-8"))
    sentence = schema["grade"][VERDICT]
    bullet = "- **%s:** %s" % (VERDICT, sentence)

    with tempfile.TemporaryDirectory(prefix="canon_patch_") as td:
        td = Path(td)
        # 1. apply --check against the files as HEAD carries them
        head_tree = td / "head"
        for rel in (RENDERER, RULE):
            t = head_tree / rel
            t.parent.mkdir(parents=True, exist_ok=True)
            t.write_bytes(git_show(root, rel))
        rc_head, out_head = run(["git", "apply", "--check", str(PATCH)], head_tree)
        print("git apply --check against HEAD files: rc=%d %s" % (rc_head, out_head.strip()))
        applies = rc_head == 0

        # 2. the two arms
        unp, pat = td / "unpatched", td / "patched"
        build_tree(unp, root)
        rc_a, out_a = build_tree(pat, root, patch=True)
        print("git apply onto the copy: rc=%d %s" % (rc_a, out_a.strip()))
        applies = applies and rc_a == 0
        rc_u, out_u, canon_u, sec_u = render(unp)
        rc_p, out_p, canon_p, sec_p = render(pat)
        print("unpatched --write rc=%d: %s" % (rc_u, out_u.strip()))
        print("patched   --write rc=%d: %s" % (rc_p, out_p.strip()))

        has_pat = bullet in sec_p
        has_unp = bullet in sec_u
        print("schema sentence: %s" % bullet[:120])
        print("informational: the bare token %s in the UNPATCHED section (verdicts closed list): %s"
              % (VERDICT, VERDICT in sec_u))
        print("informational: GRADING_RULE.md worked case in the patched copy carries verdict NO-SYSTEM-ASKED: %s"
              % ('"name": "pandas-pyarrow-layer", "type": "LAMBDA_LAYER", "verdict": "NO-SYSTEM-ASKED"'
                 in (pat / RULE).read_text(encoding="utf-8")))

        # 3. what regenerating the canon moves
        committed = (root / CANON).read_bytes().replace(b"\r\n", b"\n").decode("utf-8").splitlines()
        drift = [ln for ln in difflib.unified_diff(committed, canon_u.splitlines(), lineterm="", n=0)
                 if ln[:1] in "+-" and ln[:3] not in ("+++", "---")]
        move = [ln for ln in difflib.unified_diff(canon_u.splitlines(), canon_p.splitlines(), lineterm="", n=0)
                if ln[:1] in "+-" and ln[:3] not in ("+++", "---")]
        print("canon as committed vs unpatched regeneration: %d changed lines" % len(drift))
        print("canon unpatched vs patched regeneration: %d changed lines" % len(move))
        for ln in move:
            print("  " + ln[:160])

        ok = applies and has_pat and not has_unp and rc_u == 0 and rc_p == 0
    print("CANON-PATCH ok=%s applies=%s rendered_has_verdict=%s unpatched_has_verdict=%s"
          % (ok, applies, has_pat, has_unp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
