"""AMGT_RESAPP round-99 PREP -- the portal repoint of the Thesis payload's `fiscal_year_figures` readers (CTO round-98 analysis section 2 step 1).

  python r99_repoint_readers.py <portal worktree root> --base <portal commit>

Step 1 of the removal: every reader of the TOP-LEVEL `fiscal_year_figures` reads `model.fiscal_year_figures` instead, so the API can later drop the top-level copy. Arms, run over
`<root>/src` (`.ts` and `.tsx`, the `__harness__` and test files excluded from the reader sweep):
    R1 NO TOP-LEVEL READER: every occurrence of `fiscal_year_figures` is classified; a comment line, a `model.`/`model?.` access or string path, or a type DECLARATION
       (`fiscal_year_figures:` / `fiscal_year_figures?:` at a member position of an interface) is allowed; anything else (`data.fiscal_year_figures`, `thesis.fiscal_year_figures`,
       a string path `'fiscal_year_figures[]...`) is a top-level read, printed with file:line. Zero required.
    R2 THE SWEEP SEES A MODEL READ (the control): at least one `model.fiscal_year_figures` access or string path is found, so a 0 in R1 is not a blind sweep.
    R3 THE MODEL BLOCK DECLARES IT: `types.ts` declares `fiscal_year_figures` inside `interface ThesisModelBlock`.
    R4 FIXTURES CARRY THE MODEL COPY: every fixture of `src/pages/SecurityAnalysis/__harness__` (`tabsFixture.*.json` `.thesis`, `thesisBundle*.json`) whose top-level
       `fiscal_year_figures` is non-empty carries `model.fiscal_year_figures` EQUAL to it.
    R5 NOTHING ELSE OF THE FIXTURES MOVED: each fixture, with its `model.fiscal_year_figures` key removed, equals that fixture at `--base` (parsed JSON equality); a fixture the
       base lacks, or any other changed key, fails.
Verdict: R99 REPOINT READERS: YES|NO (exit 0|1). At the base (DEV 44ec7e70a9): R1 FAIL (5 top-level reads), R2 PASS, R3 FAIL, R4 FAIL, R5 PASS.
"""
import glob
import json
import os
import re
import subprocess
import sys

SA = "src/pages/SecurityAnalysis"
TOKEN = re.compile(r"fiscal_year_figures")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def source_files(root):
    out = []
    for path in glob.glob(os.path.join(root, "src", "**", "*.ts"), recursive=True) + glob.glob(os.path.join(root, "src", "**", "*.tsx"), recursive=True):
        rel = os.path.relpath(path, root).replace("\\", "/")
        if "/__harness__/" in rel or ".test." in rel or "/tests/" in rel:
            continue
        out.append((rel, path))
    return sorted(out)


def classify(line, col):
    stripped = line.strip()
    if stripped.startswith(("*", "//", "/*")):
        return "comment"
    before = line[:col]
    if before.endswith(("model.", "model?.")):
        return "model"
    after = line[col + len("fiscal_year_figures"):].lstrip()
    if after.startswith(("?:", ":")) and re.match(r"^\s*$", before):
        return "declaration"
    return "top"


def main(argv):
    if len(argv) != 3 or argv[1] != "--base":
        print("usage: r99_repoint_readers.py <portal worktree root> --base <portal commit>")
        return 2
    root, base = argv[0], argv[2]
    top, model, declared = [], 0, []
    files = source_files(root)
    for rel, path in files:
        for no, line in enumerate(open(path, encoding="utf-8", errors="replace").read().splitlines(), 1):
            for m in TOKEN.finditer(line):
                kind = classify(line, m.start())
                if kind == "top":
                    top.append("%s:%d" % (rel, no))
                elif kind == "model":
                    model += 1
                elif kind == "declaration":
                    declared.append("%s:%d" % (rel, no))
    for site in top:
        print("   TOP-LEVEL READ %s" % site)
    res = [say(not top, "R1 no top-level reader of fiscal_year_figures in src (non-harness)", "%d top-level read(s) over %d files" % (len(top), len(files)))]
    res.append(say(model >= 1, "R2 the sweep sees a model.fiscal_year_figures read (control)", "%d model access(es)" % model))
    types_path = os.path.join(root, SA, "types.ts")
    types_text = open(types_path, encoding="utf-8", errors="replace").read()
    block = re.search(r"export interface ThesisModelBlock \{(.*?)\n\}\n", types_text, re.S)
    res.append(say(bool(block) and bool(re.search(r"^\s*fiscal_year_figures\??:", block.group(1), re.M)), "R3 ThesisModelBlock declares fiscal_year_figures"))
    fixtures = sorted(glob.glob(os.path.join(root, SA, "__harness__", "tabsFixture.*.json")) + glob.glob(os.path.join(root, SA, "__harness__", "thesisBundle*.json")))
    miss, moved = [], []
    for path in fixtures:
        rel = os.path.relpath(path, root).replace("\\", "/")
        new = json.loads(open(path, "rb").read().decode("utf-8"))
        th = new.get("thesis", new) if isinstance(new, dict) else new
        top_figs = th.get("fiscal_year_figures") or []
        mod_figs = ((th.get("model") or {}).get("fiscal_year_figures")) if isinstance(th.get("model"), dict) else None
        if top_figs and mod_figs != top_figs:
            miss.append(rel.split("/")[-1])
        got = subprocess.run(["git", "-C", root, "show", "%s:%s" % (base, rel)], capture_output=True)
        if got.returncode != 0:
            moved.append(rel.split("/")[-1] + " (absent at base)")
            continue
        old = json.loads(got.stdout.decode("utf-8"))
        stripped = json.loads(json.dumps(new))
        sth = stripped.get("thesis", stripped) if isinstance(stripped, dict) else stripped
        if isinstance(sth.get("model"), dict):
            sth["model"].pop("fiscal_year_figures", None)
            if not sth["model"] and "model" not in (old.get("thesis", old) if isinstance(old, dict) else {}):
                sth.pop("model", None)
        if stripped != old:
            moved.append(rel.split("/")[-1])
    res.append(say(not miss, "R4 every fixture with top-level figures carries an equal model.fiscal_year_figures", "%d fixtures, missing %s" % (len(fixtures), miss)))
    res.append(say(not moved, "R5 nothing else of the fixtures moved against %s" % base, "moved %s" % moved))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R99 REPOINT READERS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
