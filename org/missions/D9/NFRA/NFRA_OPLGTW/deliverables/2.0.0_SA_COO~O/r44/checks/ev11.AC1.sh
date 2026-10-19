#!/usr/bin/env bash
# OPLGTW OG-ev-11 AC1 (round 44; round-43 analysis item 2): size the inline audit-write repair BEFORE building it. READ-ONLY; counts only; no product change.
# It completes OG-ev-8's table (W154/AUDIT_SITES.json, 81 sites at base 581ee61977): the 12 sites marked on_event_loop "unknown" are settled by reading the pinned `mcp` SDK's dispatch rule for a SYNC tool body,
# every site gets calls_7d (an integer or ABSENT with its reason), and a ranked repair proposal follows. The repair itself is a round-45 decision.
# Standing condition 3: the record PINS its base sha, and this check reads the call sites AT that sha (git grep <sha>), never at trunk.
# Record W/AUDIT_SITES_SIZED.json = {"body": {"base_sha": "<40 hex>",
#   "sites": [{"file", "line", "call" (<=120 chars), "on_event_loop": "yes|no", "loop_reason", "timeout_s": number|null, "timeout_reason", "calls_7d": integer|"ABSENT", "calls_7d_source" | "absent_reason"}],
#   "mcp_dispatch": {"package": "mcp", "version": "1.28.0", "source": "<how the package source was obtained>", "rule": "<one paragraph: does a sync @mcp.tool body run on the event loop or in a thread>", "evidence": ["<file>:<line>", ... (at least 2)]},
#   "lake": {"days": 7, "keys_listed": {"YYYY-MM-DD": n, ... 7 days}, "sample_every_k": k, "objects_read": n (at most 15000), "read_errors": 0, "method": "<how>"},
#   "per_tool_counts": [{"tool": "<name>", "observed": n, "scaled_7d": n (= observed x sample_every_k)}],
#   "ranking": [{"rank": 1, "proposal": "<at least 40 characters>", "sites": n, "basis": "<which counts or rule>"}]}}
# `keys_listed` is the EXACT denominator (every key of the day is listed); the bodies are read for every k-th key only, so k is printed beside every scaled number (a value carries its claim). No event body, principal or account value is copied.
# Override (dry-run controls only): EV11_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV11_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~157/AUDIT_SITES_SIZED.json}"
[ -f "$REC" ] || { echo "AUDIT_SITES_SIZED.json absent"; echo "RESULT: FAIL"; exit 1; }
sha=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));b=d.get('body',d);print(b.get('base_sha',''))" "$(native "$REC")" | tr -d '\r')
git cat-file -e "${sha}^{commit}" 2>/dev/null || { echo "base_sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
found=$(git grep -nE -e '\baudit\.[A-Za-z_]+\(' -e '\b_emit\(' "$sha" -- "$GW/app/*.py" | sed "s|^$sha:||" | cut -d: -f1,2 | sed "s|^$GW/app/||" | sort -u)
res=$(FOUND="$found" python -I - "$(native "$REC")" <<'PYEOF'
import json, os, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0
want = sorted(set(x.strip() for x in os.environ.get("FOUND", "").split("\n") if x.strip()))
sites = b.get("sites") or []
have = set(); bad = 0; unknown = 0; counted = 0; absent = 0
for s in sites:
    if not isinstance(s, dict) or not isinstance(s.get("line"), int) or not s.get("file"):
        bad += 1; continue
    ok = s.get("on_event_loop") in ("yes", "no") and bool(s.get("loop_reason"))
    if s.get("on_event_loop") not in ("yes", "no"):
        unknown += 1
    t = s.get("timeout_s")
    ok = ok and (t is None or isn(t)) and bool(s.get("timeout_reason"))
    c = s.get("calls_7d")
    if c == "ABSENT":
        ok = ok and bool(s.get("absent_reason")); absent += 1
    else:
        ok = ok and isinstance(c, int) and not isinstance(c, bool) and c >= 0 and bool(s.get("calls_7d_source")); counted += 1
    if not ok:
        bad += 1; continue
    f = str(s["file"]).replace(chr(92), "/").split("opal-gateway/app/")[-1]
    have.add("%s:%d" % (f, s["line"]))
missing = [w for w in want if w not in have]
extra = [h for h in have if h not in want]
md = b.get("mcp_dispatch") or {}
md_ok = (md.get("package") == "mcp" and md.get("version") == "1.28.0" and bool(md.get("source")) and isinstance(md.get("rule"), str) and len(md["rule"]) >= 40
         and isinstance(md.get("evidence"), list) and len(md["evidence"]) >= 2)
lk = b.get("lake") or {}
kl = lk.get("keys_listed") or {}
k = lk.get("sample_every_k"); nread = lk.get("objects_read"); total = sum(v for v in kl.values() if isinstance(v, int))
lk_ok = (lk.get("days") == 7 and len(kl) == 7 and all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(x)) and isinstance(v, int) and v > 0 for x, v in kl.items())
         and isinstance(k, int) and k >= 1 and isinstance(nread, int) and 0 < nread <= 15000 and lk.get("read_errors") == 0 and bool(lk.get("method"))
         and total > 0 and nread * k >= 0.9 * total and nread * k <= 1.1 * total + 8 * k)
pt = b.get("per_tool_counts") or []
pt_ok = bool(pt) and all(isinstance(p, dict) and p.get("tool") and isn(p.get("observed")) and isinstance(k, int) and p.get("scaled_7d") == p["observed"] * k for p in pt)
rk = b.get("ranking") or []
rk_ok = bool(rk) and [r.get("rank") for r in rk if isinstance(r, dict)] == list(range(1, len(rk) + 1)) and all(isinstance(r.get("proposal"), str) and len(r["proposal"]) >= 40 and isinstance(r.get("sites"), int) and bool(r.get("basis")) for r in rk)
leak = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
ok = len(want) >= 80 and not missing and not extra and not bad and unknown == 0 and md_ok and lk_ok and pt_ok and rk_ok and not leak
print("call sites at base %s matched by the pattern: %d (the cut counted 81); listed: %d; missing from the record %d (want 0); not at that sha %d (want 0); malformed rows %d (want 0); event-loop column unknown on %d site(s) (want 0)" % (
      str(b.get("base_sha"))[:10], len(want), len(have), len(missing), len(extra), bad, unknown))
print("frequency counted on %d site(s), ABSENT with a reason on %d; lake: 7 days listed %d keys, every %s-th key read (%s objects, errors %s), per-tool rows %d with scaled = observed x k: %s; mcp 1.28.0 dispatch rule with %d evidence lines: %s" % (
      counted, absent, total, k, nread, lk.get("read_errors"), len(pt), "ok" if (lk_ok and pt_ok) else "NOT OK", len(md.get("evidence") or []), "ok" if md_ok else "NOT OK"))
print("ranked proposals %d: %s; email-shaped strings %d (want 0)" % (len(rk), "ok" if rk_ok else "NOT OK", len(leak)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
