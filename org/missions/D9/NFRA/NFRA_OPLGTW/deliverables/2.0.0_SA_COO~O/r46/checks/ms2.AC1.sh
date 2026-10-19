#!/usr/bin/env bash
# OPLGTW OG-ms-2 AC1 (Phase A): master 08403355 is PREPARED into Alyssa's grant at its full current account set, nothing else changed.
#  - W/MS2_BEFORE.json: Alyssa with pk_hash, per-master counts and account-set hashes, the new master's current count and latest complete
#    date, the hash of the scope without masters and accounts, and a printed denominator (counts and hashes only);
#  - W/MS2_DIFF.json: changed_keys == ["accounts", "masters"], masters_added == ["08403355"], other masters' accounts unchanged;
#  - W/MS2_PREFLIGHT_DECIDE.json: on the candidate decide() admits the four read tools and refuses schwab_prepare_download for 08403355;
#  - W/NEVER_WIDEN_ASK_OG-ms-2.md: three headed halves, a process-wide-state line, 0 e-mail-shaped strings, 0 runs of 9+ digits.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
python - "$W" <<'EOF'
import json, os, re, sys
W = sys.argv[1]
def load(n):
    try:
        return json.load(open(os.path.join(W, n), encoding="utf-8"))
    except Exception:
        return None
b, d, p = load("MS2_BEFORE.json"), load("MS2_DIFF.json"), load("MS2_PREFLIGHT_DECIDE.json")
pr = (b or {}).get("principal") or {}
ok_b = bool(b) and pr.get("role") == "alyssa" and bool(pr.get("pk_hash")) and isinstance(pr.get("accounts_before"), dict) and isinstance(pr.get("accounts_sha256"), dict) \
    and set(pr["accounts_before"]) == set(pr["accounts_sha256"]) and pr.get("new_master") == "08403355" and isinstance(pr.get("new_master_accounts_current"), int) \
    and bool(pr.get("new_master_latest_complete_date")) and bool(pr.get("scope_sans_masters_accounts_sha256")) and bool((b.get("denominator") or {}).get("policy_items_scanned"))
al = (d or {}).get("alyssa") or {}
ok_d = al.get("changed_keys") == ["accounts", "masters"] and al.get("masters_added") == ["08403355"] and al.get("other_masters_accounts_unchanged") is True
tools = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")
pa = (p or {}).get("alyssa") or {}
ok_p = bool(p) and all((pa.get("admit") or {}).get(t) is True for t in tools) and (pa.get("refuse") or {}).get("schwab_prepare_download") is True and pa.get("master_in_scope") is True
try:
    ask = open(os.path.join(W, "NEVER_WIDEN_ASK_OG-ms-2.md"), encoding="utf-8").read()
except Exception:
    ask = ""
halves = all(re.search(r"(?mi)^#{2,4}\s.*\b%s\b" % h, ask) for h in ("CTO", "COO", "CVO"))
pws = "process-wide state this change touches" in ask
emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", ask))
digits = len(re.findall(r"\d{9,}", ask))
print("before-record: Alyssa with pk_hash, per-master counts and hashes, the new master's current count and date, scope hash, denominator: %s" % ("yes" if ok_b else "no"))
print("diff keys == [accounts, masters]: %s; other masters' accounts unchanged: %s; decide() pre-flight admits 4 and refuses prepare_download on the new master: %s" % ("yes" if al.get("changed_keys") == ["accounts", "masters"] else "no", "yes" if al.get("other_masters_accounts_unchanged") is True else "no", "yes" if ok_p else "no"))
print("ask: three halves %s; process-wide state line %s; e-mail-shaped strings %d (want 0); runs of 9+ digits %d (want 0)" % ("yes" if halves else "no", "yes" if pws else "no", emails, digits))
ok = ok_b and ok_d and ok_p and halves and pws and emails == 0 and digits == 0
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
EOF
