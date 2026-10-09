#!/bin/bash
# NFRA_IAMROLES202609.TO-IAM-u-2 -- the POPULATION-SCALE re-run harness (FWD-8).
#
# WHAT IT DOES: re-asks round 3's question over the same population. One auto-paginated
# `aws iam list-roles`; every role at Path "/" is a member, roles at Path "/aws-service-role/"
# (service-linked) are excluded and NAMED; then, per member role,
#     timeout 120 bash "$REPO_ROOT/.tools/comp-iam-usage" permission-cold --role <ROLE> --lookback 90 --json
# and the answers are assembled into ONE bundle with the same top-level keys as round 3's
# permission-cold-raw-bundle.json. It COMPOSES the estate instrument; it re-implements none of it.
#
# RUN IT BY HAND, from anywhere inside the checkout you want to measure:
#   rerun-population.sh --dry-run                 print the rule, lookback and invocation; no AWS call; exit 0
#   rerun-population.sh --out BUNDLE.json         full run (about 5 s per role: ~20 min for ~220 roles)
# Chunk / resume (a bounded call at a time; per-role results are kept in --workdir):
#   rerun-population.sh --out B.json --offset 0   --limit 60    first 60 members
#   rerun-population.sh --out B.json --offset 60  --limit 60    next 60 ... (a finished role is skipped)
#   rerun-population.sh --out B.json --assemble-only            build B.json from what the workdir holds
# A run with no --limit does every member. The bundle is written only by the assemble step, and
# it is written even when members are missing: `attempted` is the population, `returned_rc0` the
# roles that answered, `per_role_rc` names every role that did not (rc != 0 is NEVER read as clean).
#
# Then compare against an earlier bundle (no cloud call):
#   python compare-runs.py <earlier-bundle.json> <this-bundle.json>
#
# READ-ONLY: only list-roles and what comp-iam-usage permission-cold reads (get-role, role and
# attached policies, Access Advisor). It changes nothing. AWS ACCESS ANALYZER IS NEVER CALLED
# (C-ANALYZER-PRICED-FIRST / G-25). This file schedules nothing, alarms nothing, monitors
# nothing, and never wakes itself (G-21): cadence stays a human decision every time.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
  echo "ERROR: cannot resolve the repo root from $SCRIPT_DIR (git rev-parse --show-toplevel failed)" >&2
  exit 1
fi
# Explicit .tools/ paths: a bare comp-* name resolves through a ~/bin forwarder to the MAIN checkout.
COMP_IAM_USAGE="$REPO_ROOT/.tools/comp-iam-usage"
AWS="$REPO_ROOT/.tools/aws"
COMP_PY="org/modules/graph/comp_iam_usage.py"
COMP_SH=".tools/comp-iam-usage"

LOOKBACK=90          # round 3's lookback; changing it makes the bundles NOT comparable
CALL_BUDGET=120      # seconds per AWS call
DRY_RUN=0
OUT=""
WORKDIR=""
OFFSET=0
LIMIT=0
ASSEMBLE_ONLY=0
TO_ID="NFRA_IAMROLES202609.TO-IAM-u-2"
PRODUCED_BY="${OPAL_AGENT_SERIAL:-unknown}"

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --out) OUT="$2"; shift 2 ;;
    --workdir) WORKDIR="$2"; shift 2 ;;
    --offset) OFFSET="$2"; shift 2 ;;
    --limit) LIMIT="$2"; shift 2 ;;
    --lookback) LOOKBACK="$2"; shift 2 ;;
    --assemble-only) ASSEMBLE_ONLY=1; shift ;;
    --to-id) TO_ID="$2"; shift 2 ;;
    --produced-by) PRODUCED_BY="$2"; shift 2 ;;
    -h|--help) sed -n '2,32p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "unrecognized argument: $1 (try --help)" >&2; exit 2 ;;
  esac
done

POP_RULE_TEMPLATE='every IAM role in account <ACCOUNT> at Path "/" as returned by a single auto-paginated aws iam list-roles; the <N> roles at Path "/aws-service-role/" are excluded and named'
INVOCATION="timeout $CALL_BUDGET bash \"\$REPO_ROOT/.tools/comp-iam-usage\" permission-cold --role <ROLE> --lookback $LOOKBACK --json"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "=== rerun-population.sh DRY RUN -- no AWS call is made ==="
  echo "REPO_ROOT=$REPO_ROOT"
  echo "lookback=$LOOKBACK"
  echo "population_rule: $POP_RULE_TEMPLATE"
  echo "step 1 (one read): timeout $CALL_BUDGET $AWS iam list-roles --output json   (auto-paginated)"
  echo "step 2 (per member role, <ROLE> = RoleName at Path \"/\"): $INVOCATION"
  echo "step 3: assemble the bundle (same top-level keys as round 3's), record per_role_rc for every member"
  echo "instrument blobs read at run time: git hash-object $COMP_SH $COMP_PY"
  echo "then: python compare-runs.py <earlier-bundle.json> <this-bundle.json>"
  exit 0
fi

if [ -z "$OUT" ]; then
  echo "ERROR: --out BUNDLE.json is required for a real run (use --dry-run to read the plan)" >&2
  exit 2
fi
[ -n "$WORKDIR" ] || WORKDIR="${OUT%.json}.work"
mkdir -p "$WORKDIR/roles" || exit 1
LISTFILE="$WORKDIR/list-roles.json"

if [ "$ASSEMBLE_ONLY" -eq 0 ]; then
  if [ ! -s "$LISTFILE" ]; then
    echo "--- list-roles (one auto-paginated read) ---"
    timeout "$CALL_BUDGET" "$AWS" iam list-roles --output json > "$LISTFILE.tmp"
    RC=$?
    if [ "$RC" -ne 0 ] || [ ! -s "$LISTFILE.tmp" ]; then
      echo "ERROR: list-roles rc=$RC (124 = timeout); nothing was run" >&2
      rm -f "$LISTFILE.tmp"
      exit 1
    fi
    mv "$LISTFILE.tmp" "$LISTFILE"
  else
    echo "--- list-roles: reusing $LISTFILE from an earlier chunk of this run (delete it to re-read) ---"
  fi

  # Member role names at Path "/" , one per line (service-linked excluded here, named at assemble).
  python -I - "$LISTFILE" > "$WORKDIR/members.txt" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for r in sorted(d["Roles"], key=lambda r: r["RoleName"]):
    if r["Path"] == "/":
        print(r["RoleName"])
PY
  TOTAL=$(wc -l < "$WORKDIR/members.txt" | tr -d ' ')
  echo "members at Path \"/\": $TOTAL"
  N=0
  DONE_NOW=0
  while IFS= read -r ROLE; do
    ROLE="${ROLE%$'\r'}"
    N=$((N+1))
    [ "$N" -le "$OFFSET" ] && continue
    if [ "$LIMIT" -gt 0 ] && [ "$DONE_NOW" -ge "$LIMIT" ]; then break; fi
    DONE_NOW=$((DONE_NOW+1))
    if [ -f "$WORKDIR/roles/$ROLE.rc" ] && [ "$(cut -d' ' -f1 "$WORKDIR/roles/$ROLE.rc")" = "0" ]; then
      continue    # resume: an rc0 role is not asked twice
    fi
    T0=$(date +%s)
    timeout "$CALL_BUDGET" bash "$COMP_IAM_USAGE" permission-cold --role "$ROLE" --lookback "$LOOKBACK" --json \
      > "$WORKDIR/roles/$ROLE.json" 2> "$WORKDIR/roles/$ROLE.err"
    RC=$?
    echo "$RC $(( $(date +%s) - T0 ))" > "$WORKDIR/roles/$ROLE.rc"
    echo "[$N/$TOTAL] $ROLE rc=$RC"
  done < "$WORKDIR/members.txt"
fi

if [ ! -s "$LISTFILE" ]; then
  echo "ERROR: $LISTFILE missing; run a (chunk of the) population first" >&2
  exit 1
fi

BLOB_SH="$(cd "$REPO_ROOT" && git hash-object "$COMP_SH")"
BLOB_PY="$(cd "$REPO_ROOT" && git hash-object "$COMP_PY")"
RUN_DATE="$(date -u +%F)"

python -I - "$LISTFILE" "$WORKDIR" "$OUT" "$LOOKBACK" "$TO_ID" "$PRODUCED_BY" "$BLOB_SH" "$BLOB_PY" "$RUN_DATE" "$POP_RULE_TEMPLATE" "$COMP_SH" "$COMP_PY" <<'PY'
import json, os, sys
(listfile, workdir, out, lookback, to_id, produced_by, blob_sh, blob_py,
 run_date, rule_t, comp_sh, comp_py) = sys.argv[1:13]
roles = json.load(open(listfile, encoding="utf-8"))["Roles"]
members = sorted(r["RoleName"] for r in roles if r["Path"] == "/")
excluded = sorted(r["RoleName"] for r in roles if r["Path"].startswith("/aws-service-role/"))   # service-linked paths carry a service subdirectory
other = sorted(r["RoleName"] for r in roles if r["Path"] != "/" and not r["Path"].startswith("/aws-service-role/"))
arn = roles[0]["Arn"].split(":")
account = arn[4]
results, per_rc = {}, {}
for name in members:
    rcf = os.path.join(workdir, "roles", name + ".rc")
    if not os.path.exists(rcf):
        continue                      # not yet attempted: absent from per_role_rc, attempted > rc entries
    rc, el = open(rcf).read().split()
    per_rc[name] = {"rc": int(rc), "elapsed_s": int(el)}
    if int(rc) == 0:
        try:
            results[name] = json.load(open(os.path.join(workdir, "roles", name + ".json"), encoding="utf-8"))
        except Exception as e:        # rc0 but unreadable JSON is a failure, never a clean role
            per_rc[name] = {"rc": 0, "elapsed_s": int(el), "json_error": str(e)}
rc0 = sum(1 for v in per_rc.values() if v["rc"] == 0 and "json_error" not in v)
bundle = {
    "produced_by": produced_by,
    "to_id": to_id,
    "instrument": "bash .tools/comp-iam-usage permission-cold --role <ROLE> --lookback %s --json" % lookback,
    "instrument_blobs": {comp_sh: blob_sh, comp_py: blob_py},
    "account": account,
    "run_date_utc": run_date,
    "lookback_days": int(lookback),
    "population_rule": rule_t.replace("<ACCOUNT>", account).replace("<N>", str(len(excluded))),
    "attempted": len(members),
    "returned_rc0": rc0,
    "note": ("Round-4 style run by rerun-population.sh. attempted = members at Path '/'; per_role_rc names every "
             "member attempted; a member with rc != 0 or no per_role_rc entry is NOT in results and is NOT clean. "
             "excluded_service_linked_roles names the Path '/aws-service-role/' roles left out by the rule."),
    "per_role_rc": per_rc,
    "results": results,
    "excluded_service_linked_roles": excluded,
    "roles_at_other_paths_not_counted": other,
    "list_roles_total": len(roles),
}
with open(out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(bundle, f, indent=1, sort_keys=False, ensure_ascii=False)
    f.write("\n")
failed = sorted(n for n in members if n in per_rc and (per_rc[n]["rc"] != 0 or "json_error" in per_rc[n]))
notrun = sorted(n for n in members if n not in per_rc)
print("BUNDLE %s: attempted=%d returned_rc0=%d results=%d" % (out, len(members), rc0, len(results)))
print("list_roles_total=%d  excluded_service_linked=%d  other_paths=%d" % (len(roles), len(excluded), len(other)))
print("NOT CLEAN (rc != 0), by name: %s" % (", ".join(failed) if failed else "none"))
print("NOT YET ATTEMPTED (chunk remaining): %d" % len(notrun))
PY
exit $?
