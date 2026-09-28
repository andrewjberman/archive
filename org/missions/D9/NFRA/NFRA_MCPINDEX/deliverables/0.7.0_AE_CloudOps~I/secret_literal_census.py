#!/usr/bin/env python3
"""secret_literal_census.py -- find hardcoded credential literals WITHOUT ever printing one.

WHY THIS EXISTS (row NFRA_MCPINDEX-Z-S31, 2026-09-27). Row Z-S29 was built from
`git grep -c 'BD_PASSWORD=<one literal prefix>'` and named 6 files. Those 6 were redacted exactly as
asked -- and the literal they carried was SUPERSEDED. This census found 6 distinct literal password
values over 135 files, and one hash comparison against Secrets Manager showed the LIVE password sat
in 18 places across 16 files the row never named.

THE LESSON THIS ENCODES: a single-literal grep can only find the literal it was handed. Its output
does not look narrow -- it returns a real count against real files, and that count is correct for the
value it asked about. So "the password is out of the tree" does NOT follow from "that string returns
0". The guard is only as wide as its enumeration.

THE METHOD: match the ASSIGNMENT, then SUBTRACT the benign values, and print the denominator.
Never enumerate forward from a list of known-bad strings.

DISCLOSURE DISCIPLINE -- this tool never emits a secret. Each value is reported as
`len=<n> sha256=<12 hex>` plus a CHARACTER-CLASS SHAPE (A=upper a=lower 9=digit, punctuation
literal). That is enough to tell a real credential from a `your_password_here` placeholder, and
enough to prove two occurrences are the same value, without either entering a transcript, an argv, a
commit message or a report. `--verify-against-secret <id>` fetches a secret and compares HASHES only,
so the one read that settles which fingerprint is live also emits nothing.

INSTRUMENT TRAP, measured and the reason for two patterns instead of one: a single combined
alternation `(=|\\|\\|)` UNDERCOUNTS. On `const PASSWORD = process.env.BD_PASSWORD || '<lit>'` it
matches `PASSWORD =` and consumes `process.env.BD_PASSWORD` as the value, so the `|| '<lit>'` is
never reached. Measured on the real tree: 6 occurrences found vs 18 actually present. The two
patterns must fire independently over each line.

NOT A GATE. This is a census an owner may adopt; it installs nothing and refuses nothing.
CLAUDE.md section 2: proposing a gate is legal, implementing one is not.

Usage:
  python secret_literal_census.py <root> [<root> ...]
  python secret_literal_census.py <root> --verify-against-secret opal/bd/credentials
  python secret_literal_census.py <root> --fingerprint 161ff0eb3831   # locate one value, masked

Author: 0.7.0_AE_CloudOps~I   Project: NFRA_MCPINDEX (row Z-S31)
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import sys

SKIP_DIRS = {"node_modules", ".git", "__pycache__", "dist", "build", ".bun", ".venv"}
TEXT_EXT = {".md", ".ts", ".js", ".sh", ".json", ".yaml", ".yml", ".tf", ".py", ".txt", ".env"}

SECRETISH = r"[A-Z_]*(?:PASSWORD|PASSWD|SECRET|TOKEN|APIKEY|API_KEY)"
# TWO patterns, fired independently. See the INSTRUMENT TRAP note above.
PAT_ASSIGN = re.compile(r"""\b(%s)\s*=\s*(?P<v>'[^']*'|"[^"]*"|[^\s;"'|&#]+)""" % SECRETISH)
PAT_FALLBACK = re.compile(
    r"""process\.env\.(%s)\s*\|\|\s*(?P<v>'[^']*'|"[^"]*")""" % SECRETISH)

# A value that is NOT a secret: a variable ref, a placeholder, empty, a prompt, a command sub.
BENIGN = re.compile(
    r"""^(''|""|\$\{?[A-Za-z_].*|<[^>]*>|'<[^>]*>'|"<[^>]*>"|process\.env\..*"""
    r"""|\$\(.*\)|"\$[A-Za-z_{].*"|'\$[A-Za-z_{].*')$""")


def fingerprint(value: str) -> str:
    core = value.strip().strip("'\"")
    return "len=%d sha256=%s" % (len(core), hashlib.sha256(core.encode()).hexdigest()[:12])


def shape(value: str) -> str:
    core = value.strip().strip("'\"")
    out = []
    for ch in core:
        out.append("A" if ch.isupper() else "a" if ch.islower() else "9" if ch.isdigit() else ch)
    return "".join(out)


def scan(roots):
    hits, scanned = [], 0
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
                    continue
                path = os.path.join(dirpath, fn).replace("\\", "/")
                scanned += 1
                try:
                    lines = io.open(path, encoding="utf-8", errors="replace").read().split("\n")
                except OSError:
                    continue
                for lineno, line in enumerate(lines, 1):
                    for pat in (PAT_ASSIGN, PAT_FALLBACK):
                        for m in pat.finditer(line):
                            raw = m.group("v")
                            if BENIGN.match(raw.strip()):
                                continue
                            core = raw.strip().strip("'\"")
                            if not core or core.startswith("$"):
                                continue
                            hits.append({
                                "path": path, "line": lineno, "var": m.group(1),
                                "fp": fingerprint(raw), "shape": shape(raw), "value": core,
                            })
    return hits, scanned


def main(argv):
    roots = [a for a in argv if not a.startswith("--")]
    want_fp = None
    if "--fingerprint" in argv:
        want_fp = argv[argv.index("--fingerprint") + 1]
    secret_id = None
    if "--verify-against-secret" in argv:
        secret_id = argv[argv.index("--verify-against-secret") + 1]
    if not roots:
        print(__doc__)
        return 2

    hits, scanned = scan(roots)
    print("DENOMINATOR: %d text file(s) scanned under %s" % (scanned, ", ".join(roots)))
    print("LITERAL ASSIGNMENTS (benign values subtracted): %d across %d file(s)"
          % (len(hits), len({h["path"] for h in hits})))
    if scanned == 0:
        print("ZERO FILES SCANNED -- this is OUT-OF-CORPUS, not an absence. Check the root.")
        return 1

    if want_fp:
        sel = [h for h in hits if h["fp"].endswith(want_fp)]
        print("\noccurrences of %s: %d (line shown with the value MASKED)" % (want_fp, len(sel)))
        for h in sel:
            try:
                line = io.open(h["path"], encoding="utf-8", errors="replace").read().split("\n")[h["line"] - 1]
            except OSError:
                line = ""
            print("  %s:%d\n      %s" % (h["path"], h["line"], line.replace(h["value"], "@@SECRET@@").strip()))
        return 0

    groups = {}
    for h in hits:
        g = groups.setdefault(h["fp"], {"shape": h["shape"], "n": 0, "files": set(), "vars": set()})
        g["n"] += 1
        g["files"].add(h["path"])
        g["vars"].add(h["var"])
    print("\nDISTINCT VALUES BY FINGERPRINT: %d  (no value is printed)" % len(groups))
    print("%-30s %-5s %-6s %-28s %s" % ("FINGERPRINT", "N", "FILES", "SHAPE", "VAR"))
    for fp in sorted(groups, key=lambda k: -groups[k]["n"]):
        g = groups[fp]
        print("%-30s %-5d %-6d %-28s %s"
              % (fp, g["n"], len(g["files"]), g["shape"][:28], ",".join(sorted(g["vars"]))))
    print("\nSHAPE reads A=upper a=lower 9=digit, punctuation literal. An all-lowercase or")
    print("snake_case shape is almost always a doc placeholder; mixed case with digits and")
    print("punctuation is almost always a real credential. SHAPE IS A HINT, NEVER A VERDICT --")
    print("only --verify-against-secret settles which fingerprint is LIVE.")

    if secret_id:
        print("\n--- hash comparison against %s (values never printed) ---" % secret_id)
        try:
            out = subprocess.run(
                [".tools/aws", "secretsmanager", "get-secret-value", "--secret-id", secret_id,
                 "--query", "SecretString", "--output", "text"],
                capture_output=True, text=True, check=True).stdout
            doc = json.loads(out)
        except Exception as exc:  # noqa: BLE001 -- a failed fetch must not read as "no match"
            print("  FETCH FAILED (%s). This is NOT a no-match: the comparison did not run." % exc)
            return 1
        live = {k: hashlib.sha256(str(v).encode()).hexdigest()[:12] for k, v in doc.items()}
        matched = False
        for field, h in sorted(live.items()):
            for fp, g in groups.items():
                if fp.endswith(h):
                    matched = True
                    print("  *** LIVE: secret field %r IS fingerprint %s -- %d occurrence(s) in %d file(s) ***"
                          % (field, fp, g["n"], len(g["files"])))
                    for f in sorted(g["files"]):
                        print("        %s" % f)
        if not matched:
            print("  no repo literal matches any field of this secret.")
            print("  READ THIS CAREFULLY: it means the LIVE value is not in the scanned roots. It does")
            print("  NOT mean the literals found above are harmless -- they may be superseded")
            print("  credentials, which still warrant removal and still may be valid elsewhere.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
