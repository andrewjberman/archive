"""s13_shape.py -- MX-s-13 AC1 helper (row Z-S31). Counts NON-EMPTY literal BD_PASSWORD values/defaults in the tracked
files under a prefix. It prints counts and file paths ONLY -- never a value, never a fragment or hash of a value.

A literal is a right-hand side that is non-empty and is none of: a variable/command reference ($X, ${X...}, $(...)),
an angle-bracket placeholder (<...>), a mask (xxx, ***), or a placeholder word (REDACTED, CHANGEME, PLACEHOLDER).
Forms read:
  ${BD_PASSWORD:-rhs} / ${BD_PASSWORD-rhs}      a shell default ( ${BD_PASSWORD:?msg} is a refusal, not a default )
  BD_PASSWORD=rhs                               shell/env assignment, with or without export and quotes
  "BD_PASSWORD": "rhs" / BD_PASSWORD: 'rhs'     json/yaml key with a QUOTED value
  BD_PASSWORD || 'rhs'                          js/ts fallback

usage: python s13_shape.py <prefix> | --self-test
"""
import re
import subprocess
import sys

NAME = "BD_PASSWORD"
EXPANSION = re.compile(r"\$\{([^}]*)\}")
DEFAULT_BODY = re.compile(r"^%s:?-(.*)$" % NAME, re.S)
ASSIGN = re.compile(r"""\b%s=(["']?)([^"'\s#;]*)""" % NAME)
KEYVAL = re.compile(r"""(?:^|[\s{,])["']?%s["']?\s*:\s*(["'])([^"']*)\1""" % NAME)
JSOR = re.compile(r"""%s\s*\|\|\s*(["'])([^"']*)\1""" % NAME)
PLACEHOLDER_WORDS = {"REDACTED", "CHANGEME", "PLACEHOLDER"}


def _is_literal(rhs):
    rhs = rhs.strip().strip("\"'").strip()
    if not rhs:
        return False
    if rhs.startswith("$") or rhs.startswith("<"):
        return False
    if re.fullmatch(r"[xX*.]+", rhs):
        return False
    if rhs.upper() in PLACEHOLDER_WORDS:
        return False
    return True


def count_line(line):
    n = 0
    # 1. shell defaults inside ${...}; then blank every expansion so its text cannot match a later form.
    for m in EXPANSION.finditer(line):
        d = DEFAULT_BODY.match(m.group(1))
        if d and _is_literal(d.group(1)):
            n += 1
    flat = EXPANSION.sub("$VAR", line)
    for rx in (ASSIGN, KEYVAL, JSOR):
        for m in rx.finditer(flat):
            if _is_literal(m.group(2)):
                n += 1
    return n


def self_test():
    cases = [
        ('BD_PASSWORD="hunter2"', 1),
        ("export BD_PASSWORD=hunter2", 1),
        ('BD_PASSWORD="${BD_PASSWORD:-hunter2}"', 1),
        ('PW="${BD_PASSWORD-hunter2}"', 1),
        ('BD_PASSWORD="${BD_PASSWORD:?set BD_PASSWORD from Secrets Manager}"', 0),
        ('BD_PASSWORD="$(aws secretsmanager get-secret-value)"', 0),
        ("BD_PASSWORD=<from Secrets Manager opal/bd/credentials>", 0),
        ("BD_PASSWORD=xxx npx ts-node src/x.ts", 0),
        ('"BD_PASSWORD": "hunter2"', 1),
        ("  BD_PASSWORD: 'hunter2'", 1),
        ("const p = process.env.BD_PASSWORD || 'hunter2'", 1),
        ("const p = process.env.BD_PASSWORD || ''", 0),
        ("BD_PASSWORD=", 0),
        ("echo $BD_PASSWORD", 0),
        ("if (!process.env.BD_PASSWORD) throw new Error('BD_PASSWORD: required')", 0),
    ]
    bad = [i for i, (c, e) in enumerate(cases) if count_line(c) != e]
    print("self-test: %d of %d cases as expected%s" % (len(cases) - len(bad), len(cases),
                                                       "" if not bad else " (failing case indexes %s)" % bad))
    return 0 if not bad else 1


def main():
    if "--self-test" in sys.argv:
        return self_test()
    prefix = sys.argv[1]
    files = subprocess.run(["git", "ls-files", "--", prefix], capture_output=True, text=True,
                           encoding="utf-8", errors="replace").stdout.split()
    total, per = 0, []
    for f in files:
        try:
            text = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        c = sum(count_line(line) for line in text.splitlines())
        if c:
            per.append((f, c))
            total += c
    print("DENOMINATOR: %d tracked files under %s" % (len(files), prefix))
    for f, c in per:
        print("  %s: %d" % (f, c))
    print("non-empty BD_PASSWORD literals=%d" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
