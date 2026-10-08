#!/usr/bin/env python3
"""check_instructions -- BF-v-1 (LGIC_BLANKFIX round 7): do the written instructions name the naming check?

Run from anywhere:  python <this file>      (reads the repository only; runs `census --all-roots` once, about 15 seconds)

Checks, then prints every failure as a FAIL: line and, last, exactly one summary line:
  INSTRUCTIONS ok=True files=2 named=2 live_on_newcomer_path=0 fields=N unexplained=0
  1. infra/logic/README.md and infra/logic/10_ONBOARDING_CHECKLIST.md each contain the command `census --all-roots`.
  2. The README has a section headed `## Run the naming check` and it carries no `--live`.
  3. STEP 13 of the checklist: the first backticked command is `python lib/opal_naming.py census --all-roots`, and no
     `--live` appears before the step labelled `Separate step`.
  4. Every field name of the live ALL-ROOTS last line (run once here) appears, in backticks, in the README section.
Python 3.9; ASCII only; no AWS and no network.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
COMMAND = "census --all-roots"
FULL = "python lib/opal_naming.py census --all-roots"
README = os.path.join(ROOT, "infra", "logic", "README.md")
CHECKLIST = os.path.join(ROOT, "infra", "logic", "10_ONBOARDING_CHECKLIST.md")
HEADING = "## Run the naming check"


def read(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def readme_section(text):
    """The text from the heading to the next `## ` heading (or the end); None when the heading is absent."""
    i = text.find("\n" + HEADING + "\n")
    if i < 0:
        return None
    body = text[i + 1:]
    m = re.search(r"\n## ", body[len(HEADING):])
    return body if m is None else body[:len(HEADING) + m.start()]


def step13(text):
    m = re.search(r"\n### STEP 13 .*?(?=\n### STEP 14|\Z)", text, re.S)
    return None if m is None else m.group(0)


def live_last_line():
    p = subprocess.run([sys.executable, os.path.join("lib", "opal_naming.py"), "census", "--all-roots"],
                       cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    lines = [ln for ln in p.stdout.decode("utf-8", "replace").splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def main():
    fails = []
    texts = {}
    for label, path in (("README", README), ("CHECKLIST", CHECKLIST)):
        try:
            texts[label] = read(path)
        except OSError as exc:
            texts[label] = ""
            fails.append("%s unreadable: %s" % (label, exc))
    named = sum(1 for t in texts.values() if COMMAND in t)
    if named != 2:
        fails.append("the command %r is in %d of 2 files" % (COMMAND, named))

    live = 0
    sec = readme_section(texts["README"])
    if sec is None:
        fails.append("README has no section headed %r" % HEADING)
        sec = ""
    else:
        live += sec.count("--live")
        if FULL not in sec:
            fails.append("the README section does not carry the full command %r" % FULL)

    st = step13(texts["CHECKLIST"])
    if st is None:
        fails.append("the checklist has no STEP 13")
    else:
        head = st.split("Separate step")[0]
        live += head.count("--live")
        if "Separate step" not in st:
            fails.append("STEP 13 has no step labelled 'Separate step' for the live command")
        first = next((s for s in re.findall(r"`([^`\n]+)`", st) if s.startswith("python ")), "")
        if first != FULL:
            fails.append("STEP 13's first backticked command is %r, not %r" % (first, FULL))

    last = live_last_line()
    fields = []
    if not last.startswith("ALL-ROOTS "):
        fails.append("the live last line is not an ALL-ROOTS line: %r" % last[:120])
    else:
        fields = ["ok"] + [tok.split("=", 1)[0] for tok in last.split()[2:] if "=" in tok]
        if not last.split()[1].startswith("ok="):
            fails.append("the live last line's first field is not ok=")
    missing = [f for f in fields if ("`%s`" % f) not in sec]
    for f in missing:
        fails.append("field %r of the live last line is not explained in backticks in the README section" % f)
    if live:
        fails.append("--live appears %d time(s) on the newcomer path" % live)

    for f in fails:
        print("FAIL: " + f)
    ok = not fails and bool(fields)
    print("INSTRUCTIONS ok=%s files=2 named=%d live_on_newcomer_path=%d fields=%d unexplained=%d"
          % (ok, named, live, len(fields), len(missing)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
