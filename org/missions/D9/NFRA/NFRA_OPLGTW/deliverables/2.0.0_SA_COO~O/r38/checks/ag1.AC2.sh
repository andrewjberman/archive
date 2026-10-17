#!/usr/bin/env bash
# OPLGTW OG-ap-35 AC2 (round 40, narrowing a client's grant, PHASE B): the one-key write landed, read back live, and nothing else moved.
# W/AG1_AFTER.json = {"body": {"read_at", "alyssa": {"profile_revision", "grant_revision", "operations": [names], "scope_without_operations_hash"},
#  "others_hash": {"andrew": h, "bbg": h}, "read_back": {"download_refused": bool, "other_operation": "<name>", "other_operation_answers": bool}}}
#  - ledger nfra-oplgtw-alyssa-no-download CLOSED and its sentinel gone;
#  - after.operations == before.operations minus download_filtered exactly; scope_without_operations_hash equal to before's; grant_revision == before + 1; the other two principals' hashes equal;
#  - the read-back: her download is refused; one other operation answers; no e-mail, no digit run of 9 or more.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
BEF="${AG1_BEFORE_OVERRIDE:-$W/AG1_BEFORE.json}"
AFT="${AG1_AFTER_OVERRIDE:-$W/AG1_AFTER.json}"
slug=nfra-oplgtw-alyssa-no-download; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -n "$AG1_NO_LEDGER" ] && { closed=1; sent=0; }
[ -f "$BEF" ] && [ -f "$AFT" ] || { echo "AG1_BEFORE.json or AG1_AFTER.json absent"; echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$BEF")" "$(native "$AFT")" <<'PYEOF'
import json, re, sys
rb = open(sys.argv[1], encoding="utf-8").read()
ra = open(sys.argv[2], encoding="utf-8").read()
b = json.loads(rb); b = b.get("body", b)
a = json.loads(ra); a = a.get("body", a)
ba, aa = b.get("alyssa") or {}, a.get("alyssa") or {}
bops, aops = ba.get("operations") or [], aa.get("operations") or []
want = [o for o in bops if o != "download_filtered"]
ops_ok = "download_filtered" in bops and sorted(aops) == sorted(want) and len(want) >= 1
scope_ok = ba.get("scope_without_operations_hash") and ba.get("scope_without_operations_hash") == aa.get("scope_without_operations_hash")
rev_ok = isinstance(ba.get("grant_revision"), int) and aa.get("grant_revision") == ba["grant_revision"] + 1
oth_ok = b.get("others_hash") == a.get("others_hash") and bool(a.get("others_hash"))
rd = a.get("read_back") or {}
rd_ok = rd.get("download_refused") is True and rd.get("other_operation_answers") is True and isinstance(rd.get("other_operation"), str) and rd.get("other_operation") != "download_filtered"
txt = re.sub(r'"[0-9a-f]{10}"', '""', rb + ra)
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", txt)
mails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", txt)
ok = ops_ok and scope_ok and rev_ok and oth_ok and rd_ok and not runs and not mails
print("operations after == before minus download_filtered: %s; scope without operations equal: %s; grant revision +1: %s; other principals unchanged: %s" % (
    "yes" if ops_ok else "no", "yes" if scope_ok else "no", "yes" if rev_ok else "no", "yes" if oth_ok else "no"))
print("read-back: download refused %s; one other operation answers %s; content hygiene: long digit runs %d, e-mail addresses %d (want 0)" % (
    rd.get("download_refused"), rd.get("other_operation_answers"), len(runs), len(mails)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
printf '%s\n' "$res" | sed '$d'
echo "after verdict: $(printf '%s\n' "$res" | tail -1)"
restore_audit
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
