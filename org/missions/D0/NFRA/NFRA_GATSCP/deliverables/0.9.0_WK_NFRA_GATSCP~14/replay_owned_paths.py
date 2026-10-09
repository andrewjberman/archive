"""GS-h-1: attribution replay of the round-3 census's 26 owned-paths refusals (NFRA_GATSCP round 4, worker ~14).

Method (all measured from git; nothing is read from a commit's content, only `git log` / `git show --name-only` listings):
 1. Re-pair the log exactly as the census did: every BLOCK line stamped 2026-10-02T13:57Z..2026-10-09T14:03Z is matched
    one-to-one, in log order, with the first later OVERRIDE line by the same author within 400 lines.
 2. For each pair take the BLOCK line's violating paths (the hook logs the first three only) and the OVERRIDE line's
    staged-path count n and lane.
 3. OWN-PATH: the earliest non-merge commit authored (exact author name) by the BLOCK's serial, committed at or after the
    BLOCK stamp and no later than OVERRIDE+30 min, whose `git show --name-only` carries at least one BLOCK path.
 4. else OTHER-ACT: the one non-merge commit by that author committed within [OVERRIDE-15 s, OVERRIDE+10 min] whose
    file count equals the OVERRIDE's n and which carries none of the BLOCK paths (the commit the OVERRIDE served).
    When the OVERRIDE's lane is a lane in .owned-paths.yaml the commit must also carry a path that resolves to that lane
   (owned-paths-validate.py resolve_lane, the table at this worktree's HEAD); an Andrew-direct token is not a lane, and
   there the n match plus the token's own words decide.
 5. else UNATTRIBUTED, commit null; the evidence names what was searched.
Commits with a W73 evidence path in a listing are counted by raw line but the path is never kept or printed.
Run from anywhere inside the worktree: python replay_owned_paths.py
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
LOG = os.path.join(ROOT, "org", "git-author-override-audit.log")
OUT = os.path.join(HERE, "OWNED_PATHS_REPLAY_round4.json")
LO, HI = "2026-10-02T13:57", "2026-10-09T14:03"
LINE = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) (BLOCK|OVERRIDE)\s+(\S+)\s+(\d+)\s+(.*)$")


def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, encoding="utf-8", errors="replace").stdout


def T(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def names(h):
    """(file count by raw line, set of paths without any W73 evidence path)"""
    raw = [x for x in git("show", "--name-only", "--format=", h).split("\n") if x.strip()]
    return len(raw), {x for x in raw if "W73_S" not in x}


# lane membership, read-only, from the repo's own resolver and lane table at this worktree's HEAD
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("opv", os.path.join(ROOT, ".tools", "owned-paths-validate.py"))
_opv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_opv)
_cfg = _opv.load_yaml(os.path.join(ROOT, ".owned-paths.yaml"))
LANES = set((_cfg.get("lanes") or {}).keys())
PATHS = _cfg.get("paths") or {}

log = open(LOG, encoding="utf-8", errors="replace").read().splitlines()
blocks, ovrs = [], []
for i, ln in enumerate(log, 1):
    m = LINE.match(ln)
    if not m or not (LO <= m.group(1)[:16] <= HI):
        continue
    ts, kind, who, n, rest = m.groups()
    rec = dict(line=i, ts=ts, who=who, n=int(n), rest=rest)
    (blocks if kind == "BLOCK" else ovrs).append(rec)

used, pairs = set(), []
for b in blocks:
    for o in ovrs:
        if o["line"] > b["line"] and o["line"] - b["line"] <= 400 and o["who"] == b["who"] and o["line"] not in used:
            used.add(o["line"])
            pairs.append((b, o))
            break

# every non-merge commit since the window opened, with its committer stamp (UTC) and name-only listing
commits = []
cur = None
for ln in git("log", "--all", "--no-merges", "--since=2026-10-02T00:00Z", "--format=C%x09%H%x09%an%x09%cI", "--name-only").split("\n"):
    if ln.startswith("C\t"):
        _, h, an, ci = ln.split("\t")
        cur = dict(h=h, an=an, ci=dt.datetime.fromisoformat(ci).astimezone(dt.timezone.utc), n=0, f=set())
        commits.append(cur)
    elif ln.strip() and cur is not None:
        cur["n"] += 1
        if "W73_S" not in ln:
            cur["f"].add(ln)


def fmt(t):
    return t.strftime("%m-%dT%H:%M:%SZ")


out = []
for b, o in pairs:
    paths = re.findall(r"VIOLATION: (\S+) --", b["rest"])
    lane_b = re.findall(r"lane=(\S+)", b["rest"])[:1]
    lane_o = re.findall(r"--author-override (\S+)", o["rest"])[:1]
    bt, ot = T(b["ts"]), T(o["ts"])
    ps = set(paths)
    mine = [c for c in commits if c["an"] == b["who"]]
    own = sorted((c for c in mine if bt <= c["ci"] <= ot + dt.timedelta(minutes=30) and c["f"] & ps), key=lambda c: c["ci"])
    ent = dict(block_line=b["line"], author=b["who"], paths=paths, tie=None, commit=None, evidence="")
    if own:
        c = own[0]
        ent.update(tie="OWN-PATH", commit=c["h"], evidence=(
            "%s committed %s (%d files) at %s, after the BLOCK at %s, carrying blocked path %s; OVERRIDE line %d (%s, n=%d) at %s followed."
            % (b["who"], c["h"][:10], c["n"], fmt(c["ci"]), fmt(bt), sorted(c["f"] & ps)[0], o["line"], (lane_o or ["?"])[0], o["n"], fmt(ot))))
    else:
        srv = [c for c in mine if ot - dt.timedelta(seconds=15) <= c["ci"] <= ot + dt.timedelta(minutes=10)
               and c["n"] == o["n"] and not (c["f"] & ps)]
        if lane_o and lane_o[0] in LANES:
            srv = [c for c in srv if any(_opv.resolve_lane(f, PATHS) == lane_o[0] for f in c["f"])]
        if len(srv) == 1:
            c = srv[0]
            ent.update(tie="OTHER-ACT", commit=c["h"], evidence=(
                "OVERRIDE line %d (%s, n=%d) at %s was served by %s (%d files, committed %s, same author%s) which carries none of the BLOCK's paths "
                "(BLOCK lane %s, line %d, n=%d); no commit by %s carries a blocked path between the BLOCK and OVERRIDE+30 min."
                % (o["line"], (lane_o or ["?"])[0], o["n"], fmt(ot), c["h"][:10], c["n"], fmt(c["ci"]),
                   (", with a path in the OVERRIDE's lane" if (lane_o and lane_o[0] in LANES) else ", OVERRIDE token is not a lane; n and the token's words decide"),
                   (lane_b or ["?"])[0], b["line"], b["n"], b["who"])))
        else:
            others = [c for c in commits if c["an"] != b["who"] and bt <= c["ci"] <= ot + dt.timedelta(minutes=30) and c["f"] & ps]
            mg = []
            for h in git("log", "--all", "--merges", "--since=2026-10-02T00:00Z", "--author=" + re.escape(b["who"]), "--format=%H%x09%an%x09%cI").split("\n"):
                if not h.strip():
                    continue
                hh, an, ci = h.split("\t")
                t = dt.datetime.fromisoformat(ci).astimezone(dt.timezone.utc)
                if an == b["who"] and bt <= t <= ot + dt.timedelta(minutes=30) and names(hh)[1] & ps:
                    mg.append("%s merge at %s" % (hh[:10], fmt(t)))
            ev = ("no non-merge commit by %s between the BLOCK at %s and OVERRIDE+30 min carries any of %d blocked path(s); "
                  "no commit by that author within [OVERRIDE-15 s, OVERRIDE+10 min] has n=%d files (OVERRIDE line %d, %s) and none of the paths."
                  % (b["who"], fmt(bt), len(paths), o["n"], o["line"], (lane_o or ["?"])[0]))
            if others:
                ev += " Other authors' commits carrying a blocked path in that window (not this act): %s." % ", ".join(
                    "%s by %s at %s" % (c["h"][:10], c["an"], fmt(c["ci"])) for c in sorted(others, key=lambda c: c["ci"])[:4])
            if mg:
                ev += " Merge commit(s) by the author carrying a blocked path (merges are exempt from the lane hook, not the refused act): %s." % ", ".join(mg)
            ent.update(tie="UNATTRIBUTED", evidence=ev)
    out.append(ent)

json.dump(out, open(OUT, "w", encoding="utf-8", newline="\n"), indent=1)
cnt = {}
for e in out:
    cnt[e["tie"]] = cnt.get(e["tie"], 0) + 1
print("pairs=%d blocks_in_window=%d overrides_in_window=%d counts=%s out=%s" % (len(out), len(blocks), len(ovrs), cnt, OUT))
sys.exit(0 if len(out) == 26 else 1)
