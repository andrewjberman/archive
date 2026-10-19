#!/usr/bin/env bash
# OPLGTW OG-ev-10 AC1 (round 44; row Z-W155-S1, ARMED): is the per-identity refusal's audit write failing? A READ with a verdict fixed BEFORE the run. NO product change.
# Record W/AUDIT_REFUSAL_WRITE.json = {"body": {
#   "journal": {"source": "<journalctl command>", "first_access_line_ts": "<iso>", "last_line_ts": "<iso>", "post_mcp_429_lines": n, "ratelimit_audit_warn_lines": n},
#   "lake": {"source": "<where counted>", "window_start": "<iso>", "window_end": "<iso>", "gw_ratelimit_rows": n, "denominator": n (objects listed), "read_errors": n},
#   "counter_exposed": true|false, "counter_evidence": "<file:line list: does any route or health read ratelimit.audit_failure_count()>",
#   "controlled_refusal": null | {"principal_ref": "****xxxx", "requests_made": n, "refusals_seen": n, "lake_row_within_120s": true|false, "halves": "<path of the ask with its three halves>"},
#   "ev7_unlabelled": {"window_start": "2026-10-18T21:08:03Z", "window_end": "2026-10-18T21:08:59Z", "records": n, "pairs": [{"label": "<label>", "tool": "<tool>", "n": n}], "source": "<where counted>"},
#   "writer_test": null | {"key_label": "<the synthetic key, labelled OG-ev-10, no real principal>", "lake_key": "<the object key written, printed so a consumer can exclude it>", "written": true|false, "read_back": true|false, "instance_role": true, "halves": "<path of the ask with its three halves>"},
#   "verdict": "WRITES|FAILS|NOT_EXPOSED", "reason": "<one line>"}}
# THE RULE, fixed before the run, in this order (the check recomputes it):
#   FAILS        if ratelimit_audit_warn_lines >= 1 (the writer's own stderr line "ratelimit-audit WARN: refusal row not recorded" is in the journal);
#   FAILS        else if a controlled refusal was seen (refusals_seen >= 1) and no lake row followed within 120 s;
#   FAILS        else if post_mcp_429_lines >= 1 and the lake holds 0 gw_ratelimit rows for the window;
#   FAILS        else if a writer_test (CTO ruling 35872, the one-object writer test under the service's instance role) was run and its object was NOT written or NOT read back;
#   WRITES       else if post_mcp_429_lines >= 1 with >= 1 lake row, or a controlled refusal seen with its lake row within 120 s, or a writer_test whose one object was written AND read back;
#   NOT_EXPOSED  otherwise (no refusal was observed and the counter is not readable from the running service).
# ev7_unlabelled must account for EVERY record of OG-ev-7's window that is not labelled probe: records == (lake objects in that window) - (probe:OG-ev-7 labelled) - (probe:unarmed labelled), read from PEERS_MEASURE.json; its pairs sum to records.
# The record carries no email, no principal, no account value and no token. Override (dry-run controls only): EV10_REC_OVERRIDE, EV10_PEERS_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${EV10_REC_OVERRIDE:-$W/AUDIT_REFUSAL_WRITE.json}"
PEERS="${EV10_PEERS_OVERRIDE:-$W/PEERS_MEASURE.json}"
[ -f "$REC" ] || { echo "AUDIT_REFUSAL_WRITE.json absent"; echo "RESULT: FAIL"; exit 1; }
[ -f "$PEERS" ] || { echo "PEERS_MEASURE.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$REC")" "$(native "$PEERS")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
pm = json.load(open(sys.argv[2], encoding="utf-8")); pb = pm.get("body", pm)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0
j = b.get("journal") or {}; lk = b.get("lake") or {}; cr = b.get("controlled_refusal"); un = b.get("ev7_unlabelled") or {}
j_ok = bool(j.get("source")) and isn(j.get("post_mcp_429_lines")) and isn(j.get("ratelimit_audit_warn_lines")) and bool(j.get("first_access_line_ts")) and bool(j.get("last_line_ts"))
lk_ok = bool(lk.get("source")) and isn(lk.get("gw_ratelimit_rows")) and isn(lk.get("denominator")) and lk.get("denominator") > 0 and lk.get("read_errors") == 0 and bool(lk.get("window_start")) and bool(lk.get("window_end"))
ce_ok = isinstance(b.get("counter_exposed"), bool) and bool(b.get("counter_evidence"))
wt = b.get("writer_test")
wt_ok = wt is None or (isinstance(wt, dict) and "OG-ev-10" in str(wt.get("key_label", "")) and bool(wt.get("lake_key")) and isinstance(wt.get("written"), bool) and isinstance(wt.get("read_back"), bool) and wt.get("instance_role") is True and bool(wt.get("halves")))
cr_ok = cr is None or (isinstance(cr, dict) and re.fullmatch(r"\*{4}[0-9A-Za-z]{4}", str(cr.get("principal_ref", ""))) and isn(cr.get("requests_made")) and isn(cr.get("refusals_seen"))
                       and isinstance(cr.get("lake_row_within_120s"), bool) and bool(cr.get("halves")))
warn = j.get("ratelimit_audit_warn_lines") or 0; n429 = j.get("post_mcp_429_lines") or 0; rows = lk.get("gw_ratelimit_rows") or 0
seen = (cr or {}).get("refusals_seen") or 0; crow = (cr or {}).get("lake_row_within_120s")
if warn >= 1: want = "FAILS"
elif cr and seen >= 1 and not crow: want = "FAILS"
elif wt and not (wt.get("written") and wt.get("read_back")): want = "FAILS"
elif n429 >= 1 and rows == 0: want = "FAILS"
elif (n429 >= 1 and rows >= 1) or (cr and seen >= 1 and crow) or (wt and wt.get("written") and wt.get("read_back")): want = "WRITES"
else: want = "NOT_EXPOSED"
v_ok = b.get("verdict") in ("WRITES", "FAILS", "NOT_EXPOSED") and b.get("verdict") == want and bool(b.get("reason"))
lake7 = (pb.get("counts") or {}).get("lake") or {}
need = (lake7.get("objects_in_window") or 0) - (lake7.get("probe_og_ev_7_labelled") or 0) - (lake7.get("probe_unarmed_labelled") or 0)
pairs = un.get("pairs") or []
pairs_ok = bool(pairs) and all(isinstance(p, dict) and p.get("label") and p.get("tool") and isn(p.get("n")) for p in pairs)
un_ok = (un.get("window_start") == "2026-10-18T21:08:03Z" and un.get("window_end") == "2026-10-18T21:08:59Z" and un.get("records") == need and need > 0
         and pairs_ok and sum(p["n"] for p in pairs if isinstance(p, dict) and isn(p.get("n"))) == un.get("records") and bool(un.get("source")))
leak = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = j_ok and lk_ok and ce_ok and cr_ok and wt_ok and v_ok and un_ok and not leak and not bignums
print("journal: 429 lines %s, writer WARN lines %s (first access line %s): %s; lake: gw_ratelimit rows %s over %s objects, read errors %s: %s" % (
      n429, warn, j.get("first_access_line_ts"), "ok" if j_ok else "NOT OK", rows, lk.get("denominator"), lk.get("read_errors"), "ok" if lk_ok else "NOT OK"))
print("writer test (CTO ruling 35872): %s: %s" % ("none" if wt is None else "written %s, read back %s, key %s" % (wt.get("written"), wt.get("read_back"), wt.get("lake_key")), "ok" if wt_ok else "NOT OK"))
print("counter exposed by a route %s; controlled refusal %s: %s; verdict by the rule fixed before the run: %s, the record says %s: %s" % (
      b.get("counter_exposed"), "none" if cr is None else "seen %s of %s requests, lake row within 120 s %s" % (seen, (cr or {}).get("requests_made"), crow), "ok" if (ce_ok and cr_ok) else "NOT OK", want, b.get("verdict"), "consistent" if v_ok else "NOT consistent"))
print("OG-ev-7 window records not labelled probe: %s (PEERS_MEASURE.json gives %s); pairs sum %s: %s; email-shaped strings %d (want 0); digit runs of 9 or more %d (want 0)" % (
      un.get("records"), need, sum(p.get("n", 0) for p in pairs if isinstance(p, dict) and isinstance(p.get("n"), int)), "ok" if un_ok else "NOT OK", len(leak), len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
