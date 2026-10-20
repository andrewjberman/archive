"""co8_recipe_check.py -- AMGT_HARVST HVST-co-8: the static check of the gold-refresh image recipe.

Run from the repo root of the worktree:  python -I <this file>
Writes co8_recipe.out in this folder (LF endings) and echoes it.

1. NEGATIVE CONTROL: plants one nonexistent COPY source and proves the at-HEAD existence test flags it.
2. Reads the Dockerfile COPY lines; a source is missing when it is absent from HEAD (file: cat-file; directory: ls-tree).
3. requirements.txt: every distribution line must be pinned by ==; boto3 must not be listed.
4. latest_tags: non-comment lines of the recipe files that carry a floating tag token.
5. non_ascii: characters above 127 across the recipe files (counted per character, not per byte).
"""
import os
import re
import subprocess
import sys

REPO = os.getcwd()
RECIPE = "infra/aws/harvest/gold-refresh"
DOCKERFILE = RECIPE + "/Dockerfile"
REQUIREMENTS = RECIPE + "/requirements.txt"
TAGGED_FILES = [DOCKERFILE, RECIPE + "/buildspec.yml", RECIPE + "/build-image.sh"]
ASCII_FILES = [DOCKERFILE, REQUIREMENTS, RECIPE + "/buildspec.yml", RECIPE + "/build-image.sh", RECIPE + "/.gitignore"]
OUT = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                   "0.9.0_WK_AMGT_HARVST~191", "co8_recipe.out")
COPY_RE = re.compile(r"^COPY\s+(\S+)\s+(\S+)\s*$")
PIN_RE = re.compile(r"^[A-Za-z0-9_.\-]+==[^\s=<>!~]+$")
LATEST_RE = re.compile(r":latest\b", re.IGNORECASE)

lines = []


def emit(text):
    lines.append(text)


def git(*args):
    proc = subprocess.run(["git"] + list(args), cwd=REPO, capture_output=True)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def absent_at_head(path):
    """True when `path` (a file, or a directory given with or without a trailing slash) is not in HEAD."""
    path = path.rstrip("/")
    rc, _out = git("cat-file", "-e", "HEAD:" + path)
    if rc == 0:
        return False
    rc, out = git("ls-tree", "-r", "--name-only", "HEAD", "--", path)
    return not (rc == 0 and out.strip())


def read_text(rel):
    with open(os.path.join(REPO, *rel.split("/")), "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def non_comment(text):
    return [ln for ln in text.split("\n") if ln.strip() and not ln.lstrip().startswith("#")]


# 1. negative control
planted = RECIPE + "/no_such_source_for_control.py"
control_flags = absent_at_head(planted)
emit("RECIPE-CONTROL planted_missing_source_detected=%s" % ("yes" if control_flags else "no"))

# 2. COPY sources at HEAD
dockerfile_text = read_text(DOCKERFILE)
copy_pairs = []
for raw in dockerfile_text.split("\n"):
    m = COPY_RE.match(raw.strip())
    if m:
        copy_pairs.append((m.group(1), m.group(2)))
missing = []
for src, _dst in copy_pairs:
    if absent_at_head(src):
        missing.append(src)
    else:
        emit("COPY-SOURCE ok %s" % src)
for src in missing:
    emit("COPY-SOURCE missing_at_head %s" % src)

# 3. requirements pins
pinned = 0
unpinned = 0
for ln in non_comment(read_text(REQUIREMENTS)):
    text = ln.strip()
    if text.lower().replace("_", "-").startswith("boto3"):
        unpinned += 1
        emit("REQ-FLAG boto3_listed %s" % text)
    elif PIN_RE.match(text):
        pinned += 1
    else:
        unpinned += 1
        emit("REQ-FLAG unpinned %s" % text)

# 4. floating tags in the non-comment lines
latest_tags = 0
for rel in TAGGED_FILES:
    for ln in non_comment(read_text(rel)):
        if LATEST_RE.search(ln):
            latest_tags += 1
            emit("TAG-FLAG %s: %s" % (rel, ln.strip()))

# 5. non-ASCII characters (per character)
non_ascii = 0
for rel in ASCII_FILES:
    text = read_text(rel)
    n = sum(1 for ch in text if ord(ch) > 127)
    if n:
        emit("ASCII-FLAG %s chars=%d" % (rel, n))
    non_ascii += n

emit("RECIPE-CHECK copy_lines=%d missing_sources=%d pinned=%d unpinned=%d latest_tags=%d non_ascii=%d"
     % (len(copy_pairs), len(missing), pinned, unpinned, latest_tags, non_ascii))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="ascii", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
for ln in lines:
    os.write(1, (ln + "\n").encode("ascii"))

if not control_flags:
    sys.exit(1)
