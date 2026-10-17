#!/usr/bin/env bash
# OPLGTW OG-ap-35 AC1 (round 40, narrowing a client's grant: remove download_filtered from alyssa's live grant, PHASE A): the before-record, the usage counts and the ask.
# W/AG1_BEFORE.json = {"body": {"read_at", "denominator": {"policy_items_scanned": n}, "alyssa": {"pk_hash", "profile_revision", "grant_revision", "operations": [names], "scope_without_operations_hash"},
#  "usage": {"download_filtered_calls_since_grant": n, "last_use": iso|null, "window_start": iso, "source": "<fixed words>"}, "others_hash": {"andrew": h, "bbg": h}}}
#  - download_filtered is in the before operations; the usage counts are numbers (last_use a timestamp or null); the denominator is a positive int; hashes are 10 hex;
#  - the ask has the three half headings (CTO, COO, CVO), states the changed keys as "operations" only, a rollback by restore, the read-back, and that no seat contacts the client or the firm;
#  - no e-mail address and no digit run of 9 or more anywhere in either file.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
REC="${AG1_BEFORE_OVERRIDE:-$W/AG1_BEFORE.json}"
ASK="${AG1_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-35.md}"
[ -f "$REC" ] && [ -f "$ASK" ] || { echo "AG1_BEFORE.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$REC")" "$(native "$ASK")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
ask = open(sys.argv[2], encoding="utf-8").read()
d = json.loads(raw)
b = d.get("body", d)
a = b.get("alyssa") or {}
u = b.get("usage") or {}
h10 = lambda x: bool(re.fullmatch(r"[0-9a-f]{10}", str(x)))
ops = a.get("operations")
rec_ok = (isinstance(ops, list) and "download_filtered" in ops and len(ops) >= 2
          and isinstance(a.get("profile_revision"), int) and isinstance(a.get("grant_revision"), int)
          and h10(a.get("pk_hash")) and h10(a.get("scope_without_operations_hash"))
          and isinstance((b.get("denominator") or {}).get("policy_items_scanned"), int) and b["denominator"]["policy_items_scanned"] > 0
          and isinstance(u.get("download_filtered_calls_since_grant"), int) and u["download_filtered_calls_since_grant"] >= 0
          and (u.get("last_use") is None or isinstance(u.get("last_use"), str)) and isinstance(u.get("window_start"), str)
          and h10((b.get("others_hash") or {}).get("andrew")) and h10((b.get("others_hash") or {}).get("bbg")))
halves = all(re.search(r"(?mi)^#+ .*%s" % w, ask) for w in ("CTO", "COO", "CVO"))
items = {
    "changed keys operations only": re.search(r"(?i)changed keys?:\s*`?operations`?\s*(only)?\s*(\.|$|\n)", ask) is not None,
    "rollback by restore": re.search(r"(?i)rollback[^\n]*restor", ask) is not None,
    "read-back": re.search(r"(?i)read-back", ask) is not None,
    "no seat contacts the client": re.search(r"(?i)no seat contacts", ask) is not None,
}
txt = re.sub(r'"[0-9a-f]{10}"', '""', raw) + "\n" + ask
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", txt)
mails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", txt)
ok = rec_ok and halves and all(items.values()) and not runs and not mails
print("before-record complete (operations carry download_filtered, usage counts numeric, hashes 10 hex, denominator printed): %s" % ("yes" if rec_ok else "no"))
print("ask: three half headings %s; items %d of %d (%s)" % ("yes" if halves else "no", sum(items.values()), len(items), ", ".join(k for k, v in items.items() if not v) or "all present"))
print("content hygiene: long digit runs %d (want 0); e-mail addresses %d (want 0)" % (len(runs), len(mails)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
