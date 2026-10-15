#!/usr/bin/env bash
# OPLGTW OG-eg-2 AC1 (round-37 EGRESS, PRD v3.10 E1): the harvest runner's LIVE registration runs the merged silver cache.
#   The live task is Running; its working directory is a worktree whose HEAD descends from the OG-eg-1 merge (7662e9c016) and whose store.py holds silver_cache;
#   that worktree is LOCKED; its --publishers still hold bbg wsj barrons sa with --refresh-once; its --state-dir and --runtime-root equal the proof's old ones; the sentinel is not at HEAD.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZW"
[ -f "$W/EG2_PROOF.json" ] || { echo "EG2_PROOF.json absent"; echo "RESULT: FAIL"; exit 1; }
live=$(powershell.exe -NoProfile -Command "\$x = Export-ScheduledTask -TaskName 'Opal Data Harvest - Continuous Cycle'; \$e = ([xml]\$x).Task.Actions.Exec; \$s = (Get-ScheduledTask -TaskName 'Opal Data Harvest - Continuous Cycle').State; 'STATE=' + \$s; 'WORKDIR=' + \$e.WorkingDirectory; 'ARGS=' + \$e.Arguments" | tr -d '\r')
res=$(LIVE="$live" python - "$W/EG2_PROOF.json" <<'PY'
import json, os, re, subprocess, sys
prf = json.load(open(sys.argv[1], encoding="utf-8"))
live = os.environ["LIVE"]
state = (re.search(r"STATE=(\S+)", live) or [None, ""])[1]
wd = (re.search(r"WORKDIR=(.*)", live) or [None, ""])[1].strip()
args = live.split("ARGS=", 1)[-1]
def arg(name):
    m = re.search(r'--%s\s+"?([^"\r\n]+?)"?(?=\s+--|\s*$)' % name, args)
    return m.group(1).replace("\\", "/") if m else None
m = re.search(r"--publishers\s+((?:[a-z]+\s*)+?)(?=--|$)", args)
pubs = m.group(1).split() if m else []
def git(*a):
    r = subprocess.run(["git", "-C", wd] + list(a), capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")
rc_head, head = git("rev-parse", "HEAD")
rc_anc, _ = git("merge-base", "--is-ancestor", "7662e9c016", "HEAD")
rc_ctl, _ = git("merge-base", "--is-ancestor", "HEAD", "7662e9c016~1000") if rc_head == 0 else (1, "")
rc_show, store = git("show", "HEAD:lib/research/harvest/store.py")
has_cache = rc_show == 0 and "def silver_cache" in store
rc_wl, wl = git("worktree", "list", "--porcelain")
locked = False
cur = None
for line in wl.splitlines():
    if line.startswith("worktree "):
        cur = line[9:].strip().replace("\\", "/")
    if line.startswith("locked") and cur and cur.lower() == wd.replace("\\", "/").lower():
        locked = True
same_state = arg("state-dir") == str(prf.get("old_state_dir", "")).replace("\\", "/") and arg("runtime-root") == str(prf.get("old_runtime_root", "")).replace("\\", "/")
ok = (state == "Running" and rc_head == 0 and rc_anc == 0 and rc_ctl != 0 and has_cache and locked
      and all(p in pubs for p in ("bbg", "wsj", "barrons", "sa")) and "--refresh-once" in args and same_state)
print("live registration: task %s, workdir %s, descends from the eg-1 merge %s (control: an ancestor of the old line is not a descendant %s), store.py holds silver_cache %s, pin LOCKED %s, publishers %s, --refresh-once %s, state/runtime roots unchanged %s"
      % (state, wd, rc_anc == 0, rc_ctl != 0, has_cache, locked, pubs, "--refresh-once" in args, same_state))
sys.exit(0 if ok else 1)
PY
); rc=$?
printf '%s\n' "$res" | tr -d '\r'
sen=$(git ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/ | grep -c "nfra-oplgtw-harvest-runner-silver-cache" | tr -d '\r')
echo "sentinel at HEAD $sen (want 0)"
[ "$rc" = 0 ] && [ "$sen" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
