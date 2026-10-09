"""BF-w-5: the naming-check README section types no count or timing; the root README and STEP 13 link it."""
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                      check=True).stdout.strip()
SECTION = "## Run the naming check"
TITLE = "Run the naming check"
TARGET = "infra/logic/README.md"
# a number followed by of / roots / names / holes / seconds / s, or a typed field=number
TYPED = re.compile(r"\b\d[\d,.]*\s*(?:of|roots?|names?|holes?|seconds?|s)\b|\b[a-z_]+=\d")


def read(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return fh.read().decode("utf-8")


def section(text):
    start = text.index(SECTION)
    m = re.search(r"^## ", text[start + len(SECTION):], re.M)
    return text[start:] if not m else text[start:start + len(SECTION) + m.start()]


def typed_sentences(body):
    flat = re.sub(r"\s+", " ", body)
    n = 0
    for sent in re.split(r"(?<=[.;:])\s+|\s\|\s", flat):
        if TYPED.search(sent):
            n += 1
            print("TYPED: " + sent[:160])
    return n


def links(text):
    return sum(1 for ln in text.splitlines() if TARGET in ln and TITLE in ln)


def step13_links(text):
    start = text.index("### STEP 13")
    m = re.search(r"^### STEP ", text[start + 5:], re.M)
    block = text[start:] if not m else text[start:start + 5 + m.start()]
    return 1 if (TARGET in block and TITLE in block) else 0


typed = typed_sentences(section(read(TARGET)))
root = min(1, links(read("README.md")))
check = step13_links(read("infra/logic/10_ONBOARDING_CHECKLIST.md"))
ok = typed == 0 and root == 1 and check == 1
print("README-RESIDUAL ok=%s typed_counts=%d root_link=%d checklist_link=%d" % (ok, typed, root, check))
sys.exit(0 if ok else 1)
