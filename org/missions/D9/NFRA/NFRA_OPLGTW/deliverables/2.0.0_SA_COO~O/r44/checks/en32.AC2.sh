#!/usr/bin/env bash
# OPLGTW OG-en-32 AC2 (round 44; row Z-S391): the CAUSE of the five 404-for-405 answers is named read-only, with its evidence, BEFORE any change.
# Record W/ROUTE_404_CAUSE.json = {"body": {"cause_class": "routing_library_version|real_routing_defect|test_premise",
#   "installed": {"starlette": "<version as `python -c "import starlette"` reads it here>"}, "pinned": {"requirements_line": "<the starlette line of requirements.txt, verbatim>"},
#   "evidence": ["<at least 3 strings: a file:line, a version, or the exact command and its printed answer>"],
#   "cases": [{"node_id": "<one of the five>", "expected": 405, "got_at_base": 404}, ... exactly five],
#   "change": {"kind": "none|test_update|one_line_repair", "files": ["<path>", ...], "why": "<one line>"}}}
# A cause_class of real_routing_defect needs a product change, which this order does NOT grant: the record is then written with change.kind "none" and the worker files a BLOCKING row (AC1 stays red; that is the correct outcome).
# Override (dry-run controls only): EN32_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EN32_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~158/ROUTE_404_CAUSE.json}"
[ -f "$REC" ] || { echo "ROUTE_404_CAUSE.json absent"; echo "RESULT: FAIL"; exit 1; }
reqline=$(grep -iE '^starlette' "$GW/requirements.txt" | head -1 | tr -d '\r')
inst=$(cd "$GW" && python -c "import starlette;print(starlette.__version__)" | tr -d '\r')
res=$(REQ="$reqline" INST="$inst" python -I - "$(native "$REC")" <<'PYEOF'
import json, os, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
IDS = {"tests/test_transcript_route.py::test_bearer_constant_time_own_prefix_only", "tests/test_teams_route.py::test_methods_and_unknown_routes",
       "tests/test_teams_route.py::test_new_routes_are_get_only_and_allowlist_still_refuses_neighbours", "tests/test_mail_route.py::test_transcript_and_ms_bearers_refused_on_mail_prefix",
       "tests/test_mail_route.py::test_graph_get_only_fails_closed"}
cls = b.get("cause_class")
cls_ok = cls in ("routing_library_version", "real_routing_defect", "test_premise")
inst = (b.get("installed") or {}).get("starlette"); pin = (b.get("pinned") or {}).get("requirements_line")
ver_ok = inst == os.environ.get("INST") and pin == os.environ.get("REQ") and bool(inst) and bool(pin)
ev = b.get("evidence") or []
ev_ok = isinstance(ev, list) and len(ev) >= 3 and all(isinstance(x, str) and len(x) >= 8 for x in ev)
cases = b.get("cases") or []
cases_ok = {c.get("node_id") for c in cases if isinstance(c, dict)} == IDS and len(cases) == 5 and all(c.get("expected") == 405 and c.get("got_at_base") == 404 for c in cases)
ch = b.get("change") or {}
ch_ok = ch.get("kind") in ("none", "test_update", "one_line_repair") and isinstance(ch.get("files"), list) and bool(ch.get("why")) and (ch.get("kind") != "none" or not ch.get("files"))
no_product = all(re.fullmatch(r"infra/aws/ec2/opal-gateway/tests/test_(transcript|teams|mail)_route\.py", str(f)) for f in (ch.get("files") or []))
defect_ok = not (cls == "real_routing_defect" and ch.get("kind") != "none")
leak = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
ok = cls_ok and ver_ok and ev_ok and cases_ok and ch_ok and no_product and defect_ok and not leak
print("cause class %s (%s); installed starlette %s equals what this tree reads (%s): %s; requirements line equals the file's: %s; evidence strings %d (want >= 3)" % (
      cls, "ok" if cls_ok else "NOT a class", inst, os.environ.get("INST"), "yes" if inst == os.environ.get("INST") else "NO", "yes" if pin == os.environ.get("REQ") else "NO", len(ev)))
print("five cases listed with expected 405 and got_at_base 404: %s; change kind %s over %d file(s), only the three route-test files: %s; a real defect changes nothing here: %s; email-shaped strings %d (want 0)" % (
      "yes" if cases_ok else "NO", ch.get("kind"), len(ch.get("files") or []), "yes" if no_product else "NO", "yes" if defect_ok else "NO", len(leak)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
