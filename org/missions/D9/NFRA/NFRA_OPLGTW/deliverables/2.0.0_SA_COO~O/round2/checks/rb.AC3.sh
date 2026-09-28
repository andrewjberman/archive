#!/usr/bin/env bash
# OPLGTW OG-o-3 AC3: every "section N[.M]" reference resolves to a heading, and the preamble's stated count of
# numbered top-level sections equals the number of "## <n>." headings.
. "$(dirname "$0")/_root.sh"
python - "$GW/runbooks/SCHWAB_PILOT_RUNBOOK.md" <<'PY'
import re,sys
t=open(sys.argv[1],encoding='utf-8').read()
heads=set(re.findall(r"^#{2,3} ([0-9]+(?:\.[0-9]+)?)[ .]",t,re.M))
top=[h for h in heads if "." not in h]
refs=re.findall(r"\bsections? ([0-9]+(?:\.[0-9]+)?)\b",t)
dang=[r for r in refs if r not in heads]
words={"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11}
m=re.search(r"\b(seven|eight|nine|ten|eleven|[0-9]+) (?:numbered )?sections\b",t[:1500],re.I)
stated=(words.get(m.group(1).lower()) if m and not m.group(1).isdigit() else (int(m.group(1)) if m else None))
print(f"headings {len(heads)} ({len(top)} top-level); section references {len(refs)}, dangling {len(dang)} {dang}; stated count {stated}")
okc = stated==len(top)
print(f"dangling section references {len(dang)}; stated section count {'equals' if okc else 'DIFFERS FROM'} headings")
ok = not dang and okc
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
