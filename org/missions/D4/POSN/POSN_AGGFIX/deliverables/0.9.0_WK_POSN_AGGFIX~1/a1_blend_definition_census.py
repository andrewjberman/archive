"""BLEND_DEFINITION_CENSUS_A1 -- POSN_AGGFIX.TO-A1-1, cell AF1-s-17 (C-MEMBERS). READ-ONLY.

Census of the patterns `opal_blend_5050`, `Opal Blend 5050` and `5050` (case-insensitive, fixed
strings) over the tracked files under data/mdpf/, org/standards/, lib/ and integrations/ at the
workspace commit, with the files-searched denominator per root and every hit printed. For each
file carrying a hit, the lines that STATE CONSTITUENTS of a blend (a blend key followed within six
lines by two or more (primary model key, share) pairs) are printed. One verdict line per blend,
CONFIRMED | CONTRADICTED | NO-DEFINITION-FOUND, against org/standards/POSN_AGGREGATE_MODEL_SET.json.
The standard itself is the claim under test and is never counted as a definition. A control arm
checks the comparator against a mutated standard. Author 0.9.0_WK_POSN_AGGFIX~1.
"""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS = ["data/mdpf/", "org/standards/", "lib/", "integrations/"]
PATTERNS = ["opal_blend_5050", "Opal Blend 5050", "5050"]
STANDARD = "org/standards/POSN_AGGREGATE_MODEL_SET.json"
WINDOW = 6
TOP = None  # set after the first rev-parse; every later git call runs at the toplevel so pathspecs are repo-rooted


def git(*args, text=True, ok=(0,)):
    r = subprocess.run(["git", *args], cwd=TOP if TOP else HERE, capture_output=True)
    if r.returncode not in ok:
        raise SystemExit(f"ERROR: git {' '.join(args)} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace')[:300]}")
    return r.stdout.decode("utf-8", "replace") if text else r.stdout


REV = git("rev-parse", "--short=10", "HEAD").strip()
TOP = git("rev-parse", "--show-toplevel").strip()
std = json.loads(git("show", f"{REV}:{STANDARD}"))
KEY_TO_CODE = {m["canonical_key"]: m["code"] for m in std["primary_models"]}
BLENDS = {b["canonical_key"]: {c["code"]: float(c["share"]) for c in b["constituents"]} for b in std["blends"]}
print(f"== STANDARD {STANDARD}@{REV} v{std.get('version')} ==")
for k, v in BLENDS.items():
    claim = [b["claim"] for b in std["blends"] if b["canonical_key"] == k][0]
    print(f"  {k}: {v}  claim={claim}")

print()
print(f"== CENSUS at workspace {REV} (git grep -n -I -i -F, tracked files) ==")
den_total = 0
for root in ROOTS:
    n = len([ln for ln in git("ls-tree", "-r", "--name-only", REV, "--", root).splitlines() if ln])
    den_total += n
    print(f"  root {root:<16} files searched {n}")
print(f"  TOTAL files searched {den_total} across {len(ROOTS)} roots")

hits = {}
union = set()
for pat in PATTERNS:
    out = git("grep", "-n", "-I", "-i", "-F", "-e", pat, REV, "--", *ROOTS, ok=(0, 1))
    rows = []
    for ln in out.splitlines():
        rest = ln[len(REV) + 1:]
        path, lno, text = rest.split(":", 2)
        rows.append((path, int(lno), text))
        union.add((path, int(lno)))
    hits[pat] = rows
    files = sorted({r[0] for r in rows})
    print()
    print(f"-- pattern '{pat}': {len(rows)} hit line(s) across {len(files)} file(s) --")
    for path, lno, text in rows:
        t = text.strip()
        print(f"  {path}:{lno}: {t[:200]}{' ...[' + str(len(t)) + ' chars]' if len(t) > 200 else ''}")
print()
print(f"UNION {len(union)} distinct hit line(s) across {len({p for p, _ in union})} file(s)")

# positive control: the standard's own two names found by the census
print()
pc = []
for k in BLENDS:
    at = [f"{p}:{n}" for p, n, t in hits["opal_blend_5050"] if p == STANDARD and k in t]
    pc.append(bool(at))
    print(f"POSITIVE CONTROL {k} in {STANDARD}: {'FOUND at ' + ', '.join(at) if at else 'NOT FOUND'}")
print(f"POSITIVE CONTROL {'PASS' if all(pc) else 'FAIL'} ({sum(pc)} of {len(pc)})")

# constituent statements
PAIR_TUPLE = re.compile(r"""[(]\s*["'](opal_[a-z_]+)["']\s*,\s*([0-9]*[.]?[0-9]+)\s*[)]""")
PAIR_DICT = re.compile(r"""["'](opal_[a-z_]+)["']\s*:\s*([0-9]*[.][0-9]+)""")
print()
print("== DEFINITION CANDIDATES (lines stating constituents) ==")
defs = {k: [] for k in BLENDS}
cand_files = sorted({p for rows in hits.values() for p, _, _ in rows})
for path in cand_files:
    lines = git("show", f"{REV}:{path}").splitlines()
    found_here = False
    for i, text in enumerate(lines):
        keys_on_line = [k for k in BLENDS if k in text]
        if not keys_on_line:
            continue
        k = keys_on_line[0]
        pairs, span = [], []
        for j in range(i, min(len(lines), i + 1 + WINDOW)):
            if j > i and any(b in lines[j] for b in BLENDS):
                break
            got = PAIR_TUPLE.findall(lines[j]) + PAIR_DICT.findall(lines[j])
            got = [(a, s) for a, s in got if a in KEY_TO_CODE]
            if got:
                pairs += got
                span.append(j)
        if len(pairs) >= 2:
            found_here = True
            mapping = {}
            for a, s in pairs:
                mapping[KEY_TO_CODE[a]] = mapping.get(KEY_TO_CODE[a], 0.0) + float(s)
            role = "STANDARD (claim under test, NOT a definition)" if path == STANDARD else "DEFINITION"
            last = git("log", "-1", "--format=%h %cs", REV, "--", path).strip()
            print(f"  {role}: {path}@{REV} (last touched {last}) lines {i + 1}-{span[-1] + 1}")
            for j in [i] + span:
                print(f"    {j + 1}: {lines[j].rstrip()[:160]}")
            print(f"    -> {k} = {mapping}")
            if path != STANDARD:
                defs[k].append((path, i + 1, span[-1] + 1, mapping, last))
    if not found_here:
        print(f"  no constituent statement: {path}")


def verdict(standard, found):
    if not found:
        return "NO-DEFINITION-FOUND"
    for _, _, _, mapping, _ in found:
        if set(mapping) != set(standard) or any(abs(mapping[c] - standard[c]) > 1e-9 for c in standard):
            return "CONTRADICTED"
    return "CONFIRMED"


print()
print("== VERDICTS ==")
for k, standard in BLENDS.items():
    v = verdict(standard, defs[k])
    cite = "; ".join(f"{p}:{a}-{b}@{REV} (file last touched {lt}) states {m}" for p, a, b, m, lt in defs[k]) or \
        f"census of {len(union)} hit lines over {den_total} files found no constituent statement"
    print(f"VERDICT {k}: {v} -- standard {standard}; {cite}")

# control: the comparator must say CONTRADICTED against a mutated standard
print()
mut = {k: dict(v) for k, v in BLENDS.items()}
first = next(iter(mut))
codes = list(mut[first])
mut[first] = {codes[0]: 0.5, "ULT": 0.5}
mv = verdict(mut[first], defs[first])
print(f"CONTROL mutated standard {first} = {mut[first]} -> {mv} "
      f"({'FIRED' if mv == 'CONTRADICTED' else ('N/A no definition' if not defs[first] else 'DID NOT FIRE')})")
