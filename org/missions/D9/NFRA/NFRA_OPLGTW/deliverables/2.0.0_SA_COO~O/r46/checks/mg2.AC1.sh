#!/usr/bin/env bash
# OPLGTW OG-mg-2 AC1 (Phase A): the Schwab grants of Andrew's and Alyssa's principals are PREPARED at each granted master's
# CURRENT account set, with nothing else changed; the in-process decide() pre-flight on Alyssa's candidate; the three-half ask.
#  - W/MG2_BEFORE.json: both roles, pk_hash, revisions, per-master account counts before and current (counts only), the
#    sha256 of the scope WITHOUT accounts, and a printed denominator;
#  - W/MG2_DIFF.json: for each role the changed scope keys of the candidate against the grant in force == ["accounts"];
#  - W/MG2_PREFLIGHT_DECIDE.json: on Alyssa's candidate decide() admits the four read tools and refuses schwab_prepare_download;
#  - W/NEVER_WIDEN_ASK_OG-mg-2.md: three headed halves, a process-wide-state line, 0 e-mail-shaped strings, 0 runs of 9+ digits.
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
b, d, p = load("MG2_BEFORE.json"), load("MG2_DIFF.json"), load("MG2_PREFLIGHT_DECIDE.json")
roles = {r.get("role"): r for r in (b or {}).get("principals", [])}
ok_b = bool(b) and {"andrew", "alyssa"} <= set(roles) and all(
    r.get("pk_hash") and isinstance(r.get("accounts_before"), dict) and isinstance(r.get("accounts_current"), dict)
    and r.get("scope_sans_accounts_sha256") for r in roles.values()) and bool((b.get("denominator") or {}).get("policy_items_scanned"))
grow = ok_b and all(all(r["accounts_current"].get(m, 0) >= n for m, n in r["accounts_before"].items()) and set(r["accounts_current"]) == set(r["accounts_before"]) for r in roles.values())
ok_d = bool(d) and all((d.get(k) or {}).get("changed_keys") == ["accounts"] for k in ("andrew", "alyssa"))
tools = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")
al = (p or {}).get("alyssa") or {}
ok_p = bool(p) and all((al.get("admit") or {}).get(t) is True for t in tools) and (al.get("refuse") or {}).get("schwab_prepare_download") is True
try:
    ask = open(os.path.join(W, "NEVER_WIDEN_ASK_OG-mg-2.md"), encoding="utf-8").read()
except Exception:
    ask = ""
halves = all(re.search(r"(?mi)^#{2,4}\s.*\b%s\b" % h, ask) for h in ("CTO", "COO", "CVO"))
pws = "process-wide state this change touches" in ask
emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", ask))
digits = len(re.findall(r"\d{9,}", ask))
print("before-record: both roles with pk_hash, counts before and current, scope hash, denominator: %s; current >= before on every master: %s" % ("yes" if ok_b else "no", "yes" if grow else "no"))
print("diff keys for each role == [accounts]: %s; decide() pre-flight on Alyssa admits 4 and refuses prepare_download: %s" % ("yes" if ok_d else "no", "yes" if ok_p else "no"))
print("ask: three halves %s; process-wide state line %s; e-mail-shaped strings %d (want 0); runs of 9+ digits %d (want 0)" % ("yes" if halves else "no", "yes" if pws else "no", emails, digits))
ok = ok_b and grow and ok_d and ok_p and halves and pws and emails == 0 and digits == 0
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
EOF
