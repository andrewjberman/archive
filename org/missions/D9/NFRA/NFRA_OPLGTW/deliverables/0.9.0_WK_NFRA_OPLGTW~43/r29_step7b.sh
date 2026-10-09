#!/usr/bin/env bash
# OG-rl-15 PHASE A step 7, part B (R18): rl15.AC2.sh and rl15.AC3.sh (the issuer's, A7 @4ad91ce013) exercised in the scratch clone x29 left by r29_step7.sh, on STAND-IN records:
#   RL15_READ.json   = the host's own answer of the STAGED rehearsal run with the release sha as the served release (SSM id in the record), `installed_code` flipped (`STEP7_STANDIN` lines);
#   RL15_GRANTS.json = a SYNTHETIC body (no principal, no state-store access) whose digest a trivial SSM `echo` prints: it exercises rl15_attest.py's grant rule, nothing else.
# Neither stand-in is evidence of the release. Each is followed by negative controls. Outputs: r29_rl15.AC2_*.out, r29_rl15.AC3_*.out, r29_expect_match.out.
# usage: bash r29_step7b.sh <release sha>   (from the worker worktree root; the host rehearsal run happens before, see ANNOUNCE section 7)
set -u
REL="$1"
W="$(git rev-parse --show-toplevel)"
WD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43"
D="$W/$WD"; S="$W/.scratch/x29"
CD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"; C="$CD/r32/checks"
J="$W/.scratch/step7b"
python - "$REL" "$J" <<'PY'
import hashlib, json, os, subprocess, sys, time
rel, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
INST = "i-07dccb1615503ac99"
shim = os.path.join(os.getcwd(), ".tools", "aws.cmd" if sys.platform == "win32" else "aws")


def aws(*a):
    return subprocess.run([shim] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


good = {"served_release": rel, "principals_changed": 1, "fields_changed": ["calendar_months"], "calendar_months_after": [13],
        "other_principals_changed": 0, "prior_reach_recorded": 1, "thirteen_month_read_available_dates_min": 1}
digest = hashlib.sha256(json.dumps(good, sort_keys=True).encode("utf-8")).hexdigest()
pf = os.path.join(out, "p.json")
json.dump({"commands": ["echo RL15G_DIGEST %s" % digest]}, open(pf, "w"))
cid = aws("ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-15 step-7 grant-rule stand-in (echo only)",
          "--parameters", "file://" + pf.replace(chr(92), "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text")
for _ in range(40):
    time.sleep(3)
    if aws("ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text") in ("Success", "Failed", "TimedOut", "Cancelled"):
        break


def rec(body):
    return json.dumps({"body": body, "instance_id": INST, "ssm_command_id": cid}, indent=1, sort_keys=True) + chr(10)


def w(fn, body):
    open(os.path.join(out, fn), "w", encoding="utf-8", newline=chr(10)).write(rec(body))


w("RL15_GRANTS.json", good)
w("RL15_GRANTS.two.json", dict(good, principals_changed=2, calendar_months_after=[13, 13], prior_reach_recorded=2))      # control: two principals changed (the withdrawn D3 shape)
w("RL15_GRANTS.field.json", dict(good, fields_changed=["calendar_months", "operations"]))                              # control: another field changed
w("RL15_GRANTS.other.json", dict(good, other_principals_changed=1))                                                    # control: another principal changed
w("RL15_GRANTS.m12.json", dict(good, calendar_months_after=[12]))                                                      # control: 12 months, not 13
w("RL15_GRANTS.noprior.json", dict(good, prior_reach_recorded=0))                                                      # control: no prior reach recorded
w("RL15_GRANTS.empty.json", dict(good, thirteen_month_read_available_dates_min=0))                                     # control: the 13-month read returned no date
print("grant stand-in records written; ssm", cid)
PY
cd "$S" || exit 9
python - "$REL" "$J" <<'PY'
import json, shutil, sys
rel, j = sys.argv[1:3]
d = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43/"
# the rehearsal stand-in must carry the release sha as its served release
r = json.load(open(j + "/RL15_READ.json"))
assert r["body"]["served_release"] == rel, "run the rehearsal with the release sha first"
shutil.copyfile(j + "/RL15_GRANTS.json", d + "RL15_GRANTS.json")
shutil.copyfile(j + "/RL15_READ.json", d + "RL15_READ.json")
PY
{
echo "### rl15.AC2.sh EXPECTED-PASS FORM (stand-in: the staged rehearsal's host answer, installed_code flipped, served_release = the release sha), scratch clone x29"
timeout 120 bash "$C/rl15.AC2.sh"; echo "exit=$?"
} > "$D/r29_rl15.AC2_expected_pass_form.out" 2>&1
{
echo "### rl15.AC2.sh NEGATIVE CONTROL 1: the real worker worktree (RL15_READ.json absent)"
( cd "$W" && rm -f "$WD/RL15_READ.json"; timeout 120 bash "$S/$C/rl15.AC2.sh"; echo "exit=$?" )
echo
echo "### rl15.AC2.sh NEGATIVE CONTROL 2: the rehearsal's TRUE record (installed_code false: a staged run is never accepted as the installed gateway)"
cp "$J/RL15_READ.rehearsal.json" "$S/$WD/RL15_READ.json"; timeout 120 bash "$C/rl15.AC2.sh"; echo "exit=$?"
echo
echo "### rl15.AC2.sh NEGATIVE CONTROL 3: the live r28 answer (BEFORE: asker IRREVERSIBLE_SEND, no SendGate, no calendar_months)"
cp "$J/RL15_READ.before.json" "$S/$WD/RL15_READ.json"; timeout 120 bash "$C/rl15.AC2.sh"; echo "exit=$?"
echo
echo "### rl15.AC2.sh NEGATIVE CONTROL 4: the stand-in with one revoked concierge family"
cp "$J/RL15_READ.revoked.json" "$S/$WD/RL15_READ.json"; timeout 120 bash "$C/rl15.AC2.sh"; echo "exit=$?"
echo
echo "### rl15.AC2.sh NEGATIVE CONTROL 5: the stand-in with mail_domain_entries_signed one above the entries loaded"
cp "$J/RL15_READ.domains.json" "$S/$WD/RL15_READ.json"; timeout 120 bash "$C/rl15.AC2.sh"; echo "exit=$?"
echo
echo "### rl15.AC2.sh NEGATIVE CONTROL 6: the stand-in with a body field edited after the host printed its digest"
cp "$J/RL15_READ.edited.json" "$S/$WD/RL15_READ.json"; timeout 120 bash "$C/rl15.AC2.sh"; echo "exit=$?"
cp "$J/RL15_READ.json" "$S/$WD/RL15_READ.json"
} > "$D/r29_rl15.AC2_negative_controls.out" 2>&1
{
echo "### rl15.AC3.sh EXPECTED-PASS FORM (stand-in: a synthetic one-principal body whose digest an SSM echo printed), scratch clone x29"
timeout 120 bash "$C/rl15.AC3.sh"; echo "exit=$?"
} > "$D/r29_rl15.AC3_expected_pass_form.out" 2>&1
{
echo "### rl15.AC3.sh NEGATIVE CONTROL 1: RL15_GRANTS.json absent (the real worker worktree)"
( cd "$W" && rm -f "$WD/RL15_GRANTS.json"; timeout 120 bash "$S/$C/rl15.AC3.sh"; echo "exit=$?" )
n=1
for k in two field other m12 noprior empty; do
  n=$((n+1)); echo; echo "### rl15.AC3.sh NEGATIVE CONTROL $n: record '$k' (see r29_step7b.sh for what it changes)"
  cp "$J/RL15_GRANTS.$k.json" "$S/$WD/RL15_GRANTS.json"; timeout 120 bash "$C/rl15.AC3.sh"; echo "exit=$?"
done
cp "$J/RL15_GRANTS.json" "$S/$WD/RL15_GRANTS.json"
} > "$D/r29_rl15.AC3_negative_controls.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
face = open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-15.gateway-release-r29.md", encoding="utf-8").read().split("RECORD FACE")[0]
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', face, re.S))
rows = [("AC1", "r29_rl15.AC1_expected_pass_form.out", True), ("AC1", "r29_rl15.AC1_negative_controls.out", False),
        ("AC2", "r29_rl15.AC2_expected_pass_form.out", True), ("AC2", "r29_rl15.AC2_negative_controls.out", False),
        ("AC3", "r29_rl15.AC3_expected_pass_form.out", True), ("AC3", "r29_rl15.AC3_negative_controls.out", False)]
out, bad = [], 0
for cid, fn, want in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    if want:
        body = "\n".join(x for x in txt.split("\n") if not x.startswith("### "))
        m = re.search(exp[cid], body) is not None
        out.append("%s %s: re.search(<expect>) %s (the order wants MATCH) -> %s" % (cid, fn, "MATCH" if m else "NO MATCH", "OK" if m else "NOT MATCHABLE"))
        bad += 0 if m else 1
    else:
        blocks = re.split(r"^### .*NEGATIVE CONTROL \d.*$", txt, flags=re.M)[1:]
        for i, b in enumerate(blocks, 1):
            blk = "\n".join(x for x in b.split("\n") if not x.startswith("### "))
            m = re.search(exp[cid], blk) is not None
            out.append("%s %s control %d of %d: re.search(<expect>) %s (must NOT match) -> %s" % (cid, fn, i, len(blocks), "MATCH" if m else "NO MATCH", "WRONG" if m else "OK"))
            bad += 1 if m else 0
open(D + "/r29_expect_match.out", "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(out) + chr(10))
print(chr(10).join(out))
print("RESULT: " + ("PASS" if not bad else "FAIL"))
PY
