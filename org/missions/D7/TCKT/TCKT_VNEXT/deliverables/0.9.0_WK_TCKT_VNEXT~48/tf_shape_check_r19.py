"""AC1 (TO TCKT_VNEXT.TO-R19-TR, row IRPT_ANLREQ-D2-S134 items 1 and 2): shape check of the two Lambda environment values.

Reads infra/aws/terraform/ticket-center/main.tf (argv[1] overrides the default path) and the same file at BASE_SHA, the parent
of this order's first commit on the branch (4f3b61768c is the first; its parent is b84a2ca293). Prints

  TF-SHAPE-OK CLIENT_NOTICE_CONTACT_MAP={} ANALYST_INTAKE_ALLOWED_FIRMS=49financial,inflection,cottonwood

(exit 0) only when:
  (a) the environment_variables block of module "opal_ticket_api" holds CLIENT_NOTICE_CONTACT_MAP, whose decoded value is the
      empty JSON object, and ANALYST_INTAKE_ALLOWED_FIRMS, exactly "49financial,inflection,cottonwood"; each key occurs once,
      and neither occurs in the base;
  (b) the set of every OTHER key of that block, with its value text (the key line through the close of its brackets), equals
      the base block's set;
  (c) the file outside that block is byte-identical to the base file (the block's open and close lines included in the block).
Otherwise prints TF-SHAPE-BAD <why> and exits 1. Local git and file reads only; no AWS or network call.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
REL = "infra/aws/terraform/ticket-center/main.tf"
BASE_SHA = "b84a2ca293126a5343d49b6f3bcb06341b30d5ce"
MODULE_HEADER = 'module "opal_ticket_api" {'
BLOCK_OPEN = "  environment_variables = {"
BLOCK_CLOSE = "  }"
KEY_RE = re.compile(r"^    ([A-Za-z_][A-Za-z0-9_]*)\s*=")
NEW_KEYS = ("CLIENT_NOTICE_CONTACT_MAP", "ANALYST_INTAKE_ALLOWED_FIRMS")
ANALYST_VALUE = "49financial,inflection,cottonwood"
CLIENT_RE = re.compile(r'^    CLIENT_NOTICE_CONTACT_MAP = "([^"\r\n]*)"$')
ANALYST_RE = re.compile(r'^    ANALYST_INTAKE_ALLOWED_FIRMS = "([^"\r\n]*)"$')
STRING_RE = re.compile(r'"(?:[^"\\\n]|\\.)*"')


def bad(why):
    print("TF-SHAPE-BAD " + why)
    sys.exit(1)


def base_text():
    proc = subprocess.run(["git", "show", "%s:%s" % (BASE_SHA, REL)], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    if proc.returncode != 0:
        bad("cannot read base %s:%s: %s" % (BASE_SHA, REL, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8")


def read_text(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def find_block(lines, label):
    headers = [i for i, line in enumerate(lines) if line == MODULE_HEADER]
    if len(headers) != 1:
        bad("%s: module header found %d times, expected 1" % (label, len(headers)))
    opens = [i for i in range(headers[0] + 1, len(lines)) if lines[i] == BLOCK_OPEN]
    if not opens:
        bad("%s: no environment_variables open line in module opal_ticket_api" % label)
    start = opens[0]
    for j in range(start + 1, len(lines)):
        if lines[j] == BLOCK_CLOSE:
            return start, j
    bad("%s: environment_variables block has no close line" % label)


def depth_of(text):
    return sum(text.count(c) for c in "([{") - sum(text.count(c) for c in ")]}")


def parse_block(lines, start, end, label):
    pairs = []
    i = start + 1
    while i < end:
        m = KEY_RE.match(lines[i])
        if not m:
            i += 1
            continue
        key = m.group(1)
        depth = depth_of(STRING_RE.sub('""', lines[i].split("=", 1)[1]))
        j = i
        while depth > 0:
            j += 1
            if j >= end:
                bad("%s: value of %s never closes inside the block" % (label, key))
            if lines[j].lstrip().startswith("#"):
                continue
            depth += depth_of(STRING_RE.sub('""', lines[j]))
        pairs.append((key, "\n".join(lines[i:j + 1])))
        i = j + 1
    return pairs


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, REL)
    cur = read_text(path).split("\n")
    base = base_text().split("\n")
    cs, ce = find_block(cur, "current")
    bs, be = find_block(base, "base")
    cur_pairs = parse_block(cur, cs, ce, "current")
    base_pairs = parse_block(base, bs, be, "base")

    # (a) the two new keys: each once, absent from the base, exact values
    for name in NEW_KEYS:
        n = sum(1 for k, _ in cur_pairs if k == name)
        if n != 1:
            bad("%s occurs %d times in the environment block, expected 1" % (name, n))
        if any(k == name for k, _ in base_pairs):
            bad("%s already present in the base block" % name)
    client_text = [v for k, v in cur_pairs if k == "CLIENT_NOTICE_CONTACT_MAP"][0]
    m = CLIENT_RE.match(client_text)
    if not m:
        bad("CLIENT_NOTICE_CONTACT_MAP is not a single-line double-quoted string: %r" % client_text)
    try:
        decoded = json.loads(m.group(1))
    except ValueError as exc:
        bad("CLIENT_NOTICE_CONTACT_MAP does not decode as JSON: %s" % exc)
    if decoded != {}:
        bad("CLIENT_NOTICE_CONTACT_MAP decodes to %r, expected the empty JSON object" % (decoded,))
    analyst_text = [v for k, v in cur_pairs if k == "ANALYST_INTAKE_ALLOWED_FIRMS"][0]
    m2 = ANALYST_RE.match(analyst_text)
    if not m2:
        bad("ANALYST_INTAKE_ALLOWED_FIRMS is not a single-line double-quoted string: %r" % analyst_text)
    if m2.group(1) != ANALYST_VALUE:
        bad("ANALYST_INTAKE_ALLOWED_FIRMS is %r, expected %r" % (m2.group(1), ANALYST_VALUE))

    # (b) every other key and its value text, as a set with multiplicity
    cur_other = sorted((k, v) for k, v in cur_pairs if k not in NEW_KEYS)
    base_sorted = sorted(base_pairs)
    if cur_other != base_sorted:
        cur_keys = set(k for k, _ in cur_other)
        base_keys = set(k for k, _ in base_sorted)
        if cur_keys != base_keys:
            bad("other keys differ: missing=%s added=%s" % (sorted(base_keys - cur_keys), sorted(cur_keys - base_keys)))
        changed = sorted(k for (k, v), (_, bv) in zip(cur_other, base_sorted) if v != bv)
        bad("value text changed for other keys: %s" % (changed or "multiplicity"))

    # (c) the file outside the block
    if cur[:cs] + cur[ce + 1:] != base[:bs] + base[be + 1:]:
        bad("the file outside the environment block differs from the base at %s" % BASE_SHA)

    print("TF-SHAPE-OK CLIENT_NOTICE_CONTACT_MAP={} ANALYST_INTAKE_ALLOWED_FIRMS=%s" % ANALYST_VALUE)
    sys.exit(0)


if __name__ == "__main__":
    main()
