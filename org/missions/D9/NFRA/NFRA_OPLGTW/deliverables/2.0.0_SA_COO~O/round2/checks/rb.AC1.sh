#!/usr/bin/env bash
# OPLGTW OG-o-3 AC1: the three repaired cross-references in SCHWAB_PILOT_RUNBOOK.md name their correct sections.
# Anchors (kept by the cell): "administration command" -> 6.1; "the disclosure" -> 8; "NEW grant revision" -> 6.1.
. "$(dirname "$0")/_root.sh"
python - "$GW/runbooks/SCHWAB_PILOT_RUNBOOK.md" <<'PY'
import re,sys
t=open(sys.argv[1],encoding='utf-8').read()
want=[("administration command","6.1"),("the disclosure","8"),("NEW grant revision","6.1")]
ok=0
for anchor,sec in want:
    hits=[m for m in re.finditer(re.escape(anchor)+r"[^\n]{0,80}?\(section ([0-9]+(?:\.[0-9]+)?)",t)]
    got=[h.group(1) for h in hits]
    good=bool(got) and all(g==sec for g in got)
    ok+=good
    print(f"  anchor '{anchor}': section refs {got or 'NONE'} want {sec} -> {'OK' if good else 'WRONG'}")
print(f"anchored references correct {ok} of {len(want)}")
print("RESULT: PASS" if ok==len(want) else "RESULT: FAIL"); sys.exit(0 if ok==len(want) else 1)
PY
